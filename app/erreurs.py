#!/usr/bin/env python3
"""Le carnet d'erreurs — « noter les questions fausses et pourquoi ».

Brief JB, repris à la SPEC-PRODUIT §3. Après la micro-explication d'une
erreur, le joueur PEUT écrire en une ligne pourquoi il s'est trompé
(« confondu avec X », « lu trop vite », « jamais appris »). Il peut
aussi ne rien écrire : la raison est OPTIONNELLE, un carnet qu'on ne
peut pas fermer sans se justifier ne se tient pas trois jours.

**Le carnet est PRIVÉ.** C'est la partie la plus intime du profil : il
est exclu de la visibilité amis de M11 (SPEC §3 et §« vie privée »).
Aucun agrégat produit ici ne doit sortir vers un autre profil, ni
alimenter podium, duel ou défi.

Stockage : `etat/<profil>/erreurs.jsonl`, append-only, à côté du journal
de révisions et dans la même philosophie (on ajoute, on ne réécrit
jamais ; deux appareils fusionnent par union horodatée). Passage en
table SQLite à M9 : **même schéma**, la migration est une copie.

Schéma d'une ligne :

    {"quand":  "2026-08-29T07:12:00+00:00",   # horodatage UTC, ISO
     "carte":  "droit-lot-partie-commune",    # id de la carte ratée
     "raison": "confondu avec la partie privative",  # ou null
     "mode":   "flash"}                       # le mode de la question

Trois consommateurs (SPEC §3) :
  - le bilan mensuel — `raisons_recurrentes()` ;
  - la règle des 3 échecs — `cartes_a_mini_lecon()`, qui lit le journal
    de RÉVISIONS et pas ce carnet : ce sont les ratés FSRS qui font foi,
    le carnet ne dit que le POURQUOI (et oriente la réponse : mini-leçon
    ou carte préalable) ;
  - la boucle terrain du joueur : une raison récurrente est de la
    matière à cartes nouvelles.

Stdlib seule.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chronologie import cle_chronologique
import seance  # noqa: E402
from planificateur import RATE  # noqa: E402

# La règle des 3 échecs est écrite à la SPEC §3 ; `academie.json` ne
# porte pas encore la clé. `cartes_a_mini_lecon` lit d'abord la config
# (`erreurs.seuil_echecs`) et ne retombe sur cette valeur qu'à défaut :
# le jour où la clé existe, rien à changer ici.
SEUIL_ECHECS_DEFAUT = 3

# Mots trop courants pour signifier quoi que ce soit dans une raison.
# Rien de métier là-dedans : c'est de la langue.
MOTS_VIDES = frozenset("""
alors apres aussi avait avec avoir bien cela cette celui comme dans deja
donc elle encore entre etait etre fait faire item jamais leur mais meme
moins parce pour pourquoi quand quoi sans sont sous sur tout tous trop
une uns vers voir etais suis etaient plus peut cest jai
""".split())
LONGUEUR_MOT_MIN = 4


def _sans_accents(texte: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texte)
                   if unicodedata.category(c) != "Mn")


# --- écriture / lecture ----------------------------------------------

def chemin_erreurs(profil: str, racine_etat: Path | None = None) -> Path:
    """Le carnet du profil. `racine_etat` sert aux tests (profil jetable)."""
    racine = Path(racine_etat) if racine_etat is not None else seance.ETAT
    return racine / profil / "erreurs.jsonl"


def normalise_raison(raison: str | None) -> str | None:
    """Une ligne, pas un paragraphe. Vide ou blanc = pas de raison."""
    if raison is None:
        return None
    ligne = " ".join(str(raison).split())
    return ligne or None


def note_erreur(profil: str, carte_id: str, raison: str | None = None,
                mode: str = "flash", racine_etat: Path | None = None,
                quand: str | None = None) -> dict:
    """Ajoute une erreur au carnet. La raison est facultative.

    Append-only : on écrit une ligne, on ne réécrit jamais les
    précédentes. Rend la ligne écrite.
    """
    if not carte_id:
        raise ValueError("une erreur se note sur une carte identifiée")
    ligne = {
        "quand": quand or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "carte": carte_id,
        "raison": normalise_raison(raison),
        "mode": mode,
    }
    chemin = chemin_erreurs(profil, racine_etat)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def lit_carnet(profil: str, racine_etat: Path | None = None) -> list[dict]:
    """Le carnet, trié par horodatage.

    Une ligne illisible est ignorée et signalée, comme dans
    `seance.lit_journal` : un carnet à moitié corrompu reste un carnet,
    il ne fait jamais tomber la séance du matin.
    """
    chemin = chemin_erreurs(profil, racine_etat)
    if not chemin.is_file():
        return []
    lignes = []
    for n, brut in enumerate(chemin.read_text(encoding="utf-8").splitlines(), 1):
        brut = brut.strip()
        if not brut:
            continue
        try:
            entree = json.loads(brut)
        except json.JSONDecodeError:
            print(f"⚠ {chemin.name}:{n} illisible, ignorée", file=sys.stderr)
            continue
        if isinstance(entree, dict) and entree.get("carte"):
            lignes.append(entree)
        else:
            print(f"⚠ {chemin.name}:{n} sans carte, ignorée", file=sys.stderr)
    return sorted(lignes, key=cle_chronologique)


# --- agrégats (bilan mensuel) ----------------------------------------

def mots_de_la_raison(raison: str | None) -> list[str]:
    """Les mots porteurs d'une raison, dédoublonnés, sans accents."""
    if not raison:
        return []
    mots, vus = [], set()
    for mot in re.split(r"[^0-9a-z]+", _sans_accents(raison).lower()):
        if len(mot) < LONGUEUR_MOT_MIN or mot in MOTS_VIDES or mot in vus:
            continue
        vus.add(mot)
        mots.append(mot)
    return mots


def raisons_recurrentes(carnet: list[dict], mini: int = 2) -> dict:
    """Ce qui revient : par carte, et par mot des raisons écrites.

    Volontairement simple (comptage, pas de sémantique) : c'est une
    matière à relire au bilan mensuel, pas un verdict. Une carte qui
    revient sans raison écrite compte quand même — le fait de retomber
    dessus est déjà l'information.
    """
    par_carte: dict[str, dict] = {}
    par_mot: dict[str, dict] = {}
    for entree in carnet:
        cid = entree.get("carte")
        if not cid:
            continue
        fiche = par_carte.setdefault(cid, {"carte": cid, "occurrences": 0,
                                           "raisons": []})
        fiche["occurrences"] += 1
        raison = normalise_raison(entree.get("raison"))
        if raison:
            fiche["raisons"].append(raison)
        for mot in mots_de_la_raison(raison):
            bloc = par_mot.setdefault(mot, {"mot": mot, "occurrences": 0,
                                            "cartes": []})
            bloc["occurrences"] += 1
            if cid not in bloc["cartes"]:
                bloc["cartes"].append(cid)
    return {
        "par_carte": sorted((f for f in par_carte.values()
                             if f["occurrences"] >= mini),
                            key=lambda f: (-f["occurrences"], f["carte"])),
        "par_mot": sorted((b for b in par_mot.values()
                           if b["occurrences"] >= mini),
                          key=lambda b: (-b["occurrences"], b["mot"])),
    }


# --- règle des 3 échecs (source : le journal de RÉVISIONS) -----------

def seuil_echecs(config: dict | None = None) -> int:
    """Le nombre de ratés qui déclenche une mini-leçon (config d'abord)."""
    if config:
        valeur = config.get("erreurs", {}).get("seuil_echecs")
        if isinstance(valeur, int) and valeur > 0:
            return valeur
    return SEUIL_ECHECS_DEFAUT


def cartes_a_mini_lecon(journal: list[dict], config: dict | None = None,
                        seuil: int | None = None) -> list[dict]:
    """Les cartes ratées `seuil` fois : mini-leçon ou carte préalable.

    Se lit sur le journal de RÉVISIONS (`seance.lit_journal`) et non sur
    le carnet : ce sont les ratés FSRS qui font foi, le carnet ne sert
    qu'à orienter la réponse. Les entrées `origine: "quiz"` sont
    ignorées — le quiz n'écrit jamais d'échec, mais la règle vaut d'être
    écrite ici aussi.

    Rend, du plus raté au moins raté :
        [{"carte": id, "echecs": n, "dernier": "2026-08-29T…"}, …]
    """
    borne = seuil if seuil is not None else seuil_echecs(config)
    compte: dict[str, dict] = {}
    for revue in journal:
        cid = revue.get("carte")
        if not cid or revue.get("note") != RATE or revue.get("origine") == "quiz":
            continue
        fiche = compte.setdefault(cid, {"carte": cid, "echecs": 0, "dernier": ""})
        fiche["echecs"] += 1
        quand = revue.get("quand") or ""
        if quand > fiche["dernier"]:
            fiche["dernier"] = quand
    return sorted((f for f in compte.values() if f["echecs"] >= borne),
                  key=lambda f: (-f["echecs"], f["carte"]))

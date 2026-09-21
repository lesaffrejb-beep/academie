#!/usr/bin/env python3
"""La surface de jeu du dépôt, pour un agent.

Depuis la décision 0054 il n'y a plus de front : l'interface est ce
dépôt, discuté par un agent (OpenCode, Claude Code, Codex, Gemini,
Antigravity). Ce fichier est la seule surface que l'agent appelle.

Trois principes, et rien d'autre :

  1. **Le moteur décide.** La séance, l'ordre et le moment du rappel
     viennent de `seance.py`, `progression.py` et `planificateur.py`.
     Cette surface les relaie, elle ne recompose jamais une séance.
  2. **La banque est la vérité.** Aucune carte n'est inventée : une
     carte inconnue ou une banque vide rend un trou nommé, jamais un
     contenu de substitution.
  3. **La réponse ne fuit pas.** `carte` montre la question sans la
     réponse ; `correction` la donne, après la tentative. Un QCM cache
     le bon choix jusqu'à la correction.

L'état joueur reste un journal append-only, local et hors git :
`etat/<profil>/revues.jsonl` (invariant 6). Cette surface ajoute des
lignes, elle n'en réécrit ni n'en supprime jamais.

Usage, pour un agent comme pour un humain :

    python3 app/academie.py etat
    python3 app/academie.py seance [--cap <domaine>] [--journaliser] [--json]
    python3 app/academie.py carte <id> [--reponse] [--json]
    python3 app/academie.py repondre <id> <1-4> [--format seance]
    python3 app/academie.py correction <id> [--json]
    python3 app/academie.py progression [--json]
    python3 app/academie.py qcm <id> [--ouvrir]
    python3 app/academie.py schema <id> [--ouvrir]
    python3 app/academie.py erreur <id> [raison]
    python3 app/academie.py erreurs
    python3 app/academie.py quiz [--region <domaine>] [--resultats '<json>']
    python3 app/academie.py mini-lecons
    python3 app/academie.py prevue <id>
    python3 app/academie.py rituel
    python3 app/academie.py cursus [<cle>]
    python3 app/academie.py accueil [--json]
    python3 app/academie.py profil [--pseudo <pseudo> --voix <v> --exigence <e>]
    python3 app/academie.py profil --activer <pseudo>
    python3 app/academie.py exporter <fichier>
    python3 app/academie.py importer <fichier>

Options communes : `--profil <pseudo>`, `--cursus <cle>`, `--etat
<dossier>` (racine du journal, défaut `etat/`), `--sortie <dossier>`
(artefacts HTML, défaut `sorties/`).

Stdlib seule, aucun appel de modèle, aucun réseau.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import html
import json
import os
import re
import secrets
import sys
import webbrowser
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import erreurs as erreurs_mod  # noqa: E402
import progression as progression_mod  # noqa: E402
import quiz as quiz_mod  # noqa: E402
import rituel as rituel_mod  # noqa: E402
import seance as seance_mod  # noqa: E402
from genere import charge_cartes_v2, charge_programme  # noqa: E402
from planificateur import Planificateur  # noqa: E402
from valide_banque import ACADEMIE, BANQUE, charge_banque, charge_config  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
DOSSIER_SORTIES = RACINE / "sorties"
# Identifiant de la surface et du moteur local, écrit dans la ligne
# d'ouverture. Provisoire et assumé comme tel : le jour où un vrai
# versionnement existera, il changera, et les anciennes lignes resteront.
MOTEUR_VERSION = "academie-surface-1"

# La question se montre sans la réponse ; la correction vient après.
CHAMPS_QUESTION = ("id", "domaine", "branche", "chapitre", "sous_branche",
                   "niveau", "type", "question", "aide", "source", "verifie",
                   "peremption", "note_confiance", "a_recouper")
# Ce qui n'apparaît qu'à la correction (ou pendant une épreuve, à la fin).
CHAMPS_CORRECTION = ("reponse", "explication", "vigilance")

# Le profil local (ACA-ONBOARDING-2, decisions/0056) : des préférences,
# pas une mesure. Écrit par `profil`, lu par tous les agents.
PROFIL_FORMAT = "academie-profil-1"
# Le profil actif local (ACA-PROFILS-LOCAUX-1, decisions/0057) : quel
# pseudo joue sur ce clone. `etat/` reste hors git.
SELECTION_FORMAT = "academie-profil-actif-1"
NOM_SELECTION = "profil-actif.json"
# `fullmatch` ferme le piège du `$` qui acceptait un saut de ligne final.
RE_PSEUDO = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,39}")
# Noms que Windows refuse comme dossier, extension comprise (CON, CON.txt),
# plus le fichier de sélection, pour qu'un pseudo ne prenne pas sa place.
PSEUDOS_RESERVES = frozenset(
    {"CON", "PRN", "AUX", "NUL", "PROFIL-ACTIF",
     *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))})


# --- état et journal --------------------------------------------------

def dossier_etat(args) -> Path:
    """Où vit le journal. `--etat` d'abord, puis `ACADEMIE_ETAT`, puis `etat/`."""
    choisi = getattr(args, "etat", None)
    if choisi:
        return Path(choisi)
    env = os.environ.get("ACADEMIE_ETAT")
    return Path(env) if env else RACINE / "etat"


def valide_pseudo(pseudo) -> str | None:
    """Un pseudo est un nom de dossier, sûr sur Windows comme sur macOS.

    Rend le message du refus, ou None si le pseudo convient. `fullmatch`
    remplace `match` : avec `$`, « jb\\n » passait pour « jb ». Le point
    final est refusé, et les noms de périphériques Windows le sont
    extension comprise, parce que le dossier serait créé ailleurs que
    prévu (decisions/0057).
    """
    texte = "" if pseudo is None else str(pseudo)
    if not RE_PSEUDO.fullmatch(texte):
        return ("pseudo attendu : lettre ou chiffre d'abord, puis lettres, "
                "chiffres, point, tiret ou souligné (40 max)")
    if texte.endswith("."):
        return f"pseudo refusé, un nom ne finit pas par un point : {texte}"
    if texte.split(".", 1)[0].upper() in PSEUDOS_RESERVES:
        return f"pseudo réservé par Windows : {texte}"
    return None


def chemin_du_profil(etat: Path, profil: str) -> tuple[Path | None, str | None]:
    """Le dossier d'un profil, ou None si le pseudo sort du dossier d'état."""
    erreur = valide_pseudo(profil)
    if erreur:
        return None, erreur
    racine = Path(etat).resolve()
    cible = (racine / str(profil)).resolve()
    if cible.parent != racine:
        return None, f"pseudo hors du dossier d'état : {profil}"
    return cible, None


def collision_pseudo(etat: Path, profil: str) -> str | None:
    """Refuse deux pseudos qui ne diffèrent que par la casse.

    Windows et macOS confondent `Arthur` et `arthur` : sans ce refus, le
    second écraserait le premier.
    """
    racine = Path(etat)
    if not racine.is_dir():
        return None
    for entree in racine.iterdir():
        if not entree.is_dir():
            continue
        if entree.name.lower() == str(profil).lower() and entree.name != str(profil):
            return (f"le profil « {entree.name} » existe déjà : la casse est ignorée "
                    f"sur Windows et macOS, choisissez un autre pseudo que « {profil} »")
    return None


@contextlib.contextmanager
def _etat_actif(chemin: Path):
    """Pointe `seance.ETAT` sur un dossier le temps d'appeler le moteur.

    Même geste que `quiz.lit_journal` : une seule implémentation du
    journal, jamais une seconde copie du parser.
    """
    ancien = seance_mod.ETAT
    seance_mod.ETAT = Path(chemin)
    try:
        yield
    finally:
        seance_mod.ETAT = ancien


def lit_journal(profil: str, etat: Path) -> list[dict]:
    with _etat_actif(etat):
        return seance_mod.lit_journal(profil)


def ajoute_revue(profil: str, carte_id: str, note: int, format_: str,
                 etat: Path, duree_ms: int | None = None) -> dict:
    """Ajoute une réponse au journal (contrat journal-v1). Jamais de réécriture."""
    with _etat_actif(etat):
        return seance_mod.note_v1(profil, carte_id, note, format_=format_,
                                  duree_ms=duree_ms)


# --- contexte ---------------------------------------------------------

def charge_catalogue() -> dict:
    """Le catalogue des cursus. Vide s'il n'existe pas (racine de test)."""
    fichier = ACADEMIE / "programme" / "catalogue.json"
    if not fichier.is_file():
        return {"parcours": []}
    try:
        return json.loads(fichier.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"parcours": []}


def charge_arrivee() -> dict:
    """Les choix de l'arrivée : voix, exigences, zones de dépôt (0056)."""
    fichier = ACADEMIE / "contenu" / "arrivee.json"
    if not fichier.is_file():
        return {}
    try:
        data = json.loads(fichier.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def _lit_json(chemin: Path) -> tuple[dict | None, str | None]:
    """Un objet JSON, ou None et la raison de la lecture impossible."""
    try:
        data = json.loads(chemin.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, f"fichier illisible : {chemin}"
    if not isinstance(data, dict):
        return None, f"objet JSON attendu : {chemin}"
    return data, None


def charge_profil(profil: str | None, etat: Path) -> dict | None:
    """Le profil local d'un pseudo, ou None s'il est absent ou incohérent.

    Un fichier qui se dit d'un autre pseudo, ou d'un format inconnu, ne
    sert pas de profil : mieux vaut un trou nommé qu'un état mélangé
    (ACA-PROFILS-LOCAUX-1). `raison_profil_incoherent` dit pourquoi.
    """
    if not profil:
        return None
    dossier, erreur = chemin_du_profil(etat, profil)
    if erreur:
        return None
    fichier = dossier / "profil.json"
    if not fichier.is_file():
        return None
    data, _ = _lit_json(fichier)
    if not data:
        return None
    if data.get("format") != PROFIL_FORMAT:
        return None
    if data.get("pseudo") != str(profil):
        return None
    return data


def raison_profil_incoherent(profil: str, etat: Path) -> str | None:
    """Pourquoi le profil existe mais n'est pas jouable, ou None."""
    dossier, erreur = chemin_du_profil(etat, profil)
    if erreur:
        return erreur
    fichier = dossier / "profil.json"
    if not fichier.is_file():
        return None
    data, lecture = _lit_json(fichier)
    if lecture:
        return (f"profil illisible ({lecture}) : corrigez le fichier, rien n'est "
                f"supprimé et le journal reste intact")
    if data.get("format") != PROFIL_FORMAT:
        return f"profil de format inconnu : {fichier}"
    if data.get("pseudo") != str(profil):
        return (f"profil incohérent : {fichier} se dit « {data.get('pseudo')} » "
                f"au lieu de « {profil} »")
    return None


def fichier_selection(etat: Path) -> Path:
    """Le fichier qui retient le profil actif d'un clone, hors git."""
    return Path(etat) / NOM_SELECTION


def lit_selection(etat: Path) -> tuple[str | None, str | None]:
    """Le profil actif local, ou None s'il n'y en a pas.

    Un fichier de sélection illisible est un trou, jamais un repli
    silencieux sur `profil_defaut` : le repli écrirait dans l'état de
    quelqu'un d'autre (decisions/0057).
    """
    fichier = fichier_selection(etat)
    if not fichier.is_file():
        return None, None
    data, lecture = _lit_json(fichier)
    if lecture:
        return None, f"sélection locale illisible : {fichier}"
    if data.get("format") != SELECTION_FORMAT:
        return None, f"sélection locale invalide : {fichier}"
    erreur = valide_pseudo(data.get("profil"))
    if erreur:
        return None, f"sélection locale invalide ({erreur}) : {fichier}"
    return str(data["profil"]), None


def ecrit_selection(etat: Path, profil: str) -> Path:
    """Retient le profil actif. `etat/` reste hors git (invariant 6)."""
    cible = fichier_selection(etat)
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(json.dumps({
        "format": SELECTION_FORMAT,
        "profil": str(profil),
        "active_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return cible


def profil_actif(args, config: dict) -> tuple[str | None, str | None]:
    """Qui joue : `--profil`, puis la sélection locale, puis `profil_defaut`."""
    explicite = getattr(args, "profil", None)
    if explicite is not None:
        erreur = valide_pseudo(explicite)
        if erreur:
            return None, f"--profil invalide : {erreur}"
        return str(explicite), None
    nom, erreur = lit_selection(dossier_etat(args))
    if erreur:
        return None, erreur
    if nom:
        return nom, None
    defaut = config.get("profil_defaut", "jb")
    erreur = valide_pseudo(defaut)
    if erreur:
        return None, f"profil_defaut invalide dans academie.json : {erreur}"
    return str(defaut), None


def config_du_profil(config: dict, prefs: dict | None) -> dict:
    """L'exigence du joueur appliquée à la config du moteur, sans le réécrire.

    Le profil ne crée aucune mesure : il bouge `fsrs.retention_souhaitee`,
    `quotas.nouveau_par_seance` et `erreurs.seuil_echecs`, déjà lus par le
    moteur (decisions/0056). Sans profil, la config reste identique, et la
    parité de la surface avec le moteur tient.
    """
    if not prefs:
        return config
    table = {e.get("cle"): e for e in charge_arrivee().get("exigences", [])}
    reglage = table.get(prefs.get("exigence"))
    if not reglage:
        return config
    effectif = dict(config)
    effectif["fsrs"] = dict(config.get("fsrs", {}))
    effectif["fsrs"]["retention_souhaitee"] = reglage["retention"]
    effectif["quotas"] = dict(config.get("quotas", {}))
    effectif["quotas"]["nouveau_par_seance"] = reglage["nouveau_par_seance"]
    effectif["erreurs"] = dict(config.get("erreurs", {}))
    effectif["erreurs"]["seuil_echecs"] = reglage["seuil_echecs"]
    return effectif


def charge_cursus(cle: str | None) -> dict | None:
    """Le programme d'un cursus, lu depuis le catalogue. None si inconnu."""
    if not cle:
        return None
    for parcours in charge_catalogue().get("parcours", []):
        if str(parcours.get("cle")) != str(cle):
            continue
        fichier = ACADEMIE / str(parcours.get("programme") or "")
        if not fichier.is_file():
            return None
        try:
            programme = json.loads(fichier.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        return {"cle": str(cle), "meta": parcours, "programme": programme}
    return None


def cursus_actif(journal: list[dict], args, prefs: dict | None = None) -> str | None:
    """Le cursus du jour : l'option, puis le dernier journalisé, puis le profil, puis le premier.

    C'est la règle de 0053 cote serveur, portee au local : le dernier
    evenement `mode: cursus` selon l'instant reel fait foi. Le profil sert
    de repli quand aucun choix n'a encore ete journalise (0056).
    """
    choisi = getattr(args, "cursus", None)
    if choisi:
        return str(choisi)
    for ligne in reversed(journal):
        if ligne.get("mode") == "cursus" and ligne.get("cursus"):
            return str(ligne["cursus"])
    if prefs and prefs.get("cursus"):
        repli = str(prefs["cursus"])
        if charge_cursus(repli):
            return repli
    parcours = charge_catalogue().get("parcours", [])
    return str(parcours[0]["cle"]) if parcours else None


def config_du_cursus(config: dict, programme: dict | None) -> dict:
    """La config moteur, domaines, socle et semaine type pris au programme."""
    if not programme:
        return config
    effectif = dict(config)
    for cle in ("domaines", "socle", "semaine_type"):
        if programme.get(cle):
            effectif[cle] = programme[cle]
    return effectif


def charge_cartes_du_depot() -> tuple[list[dict], list[str]]:
    """Toutes les cartes jouables du dépôt : banque v1 et chapitres v2.

    Le même geste que `app/genere.py` : la v1 par `charge_banque`, la v2
    par le valideur des chapitres (couches banque et interne, sans
    brouillon). Sans ce second chargement, les cartes v2 n'existaient pas
    pour la surface, ni pour l'IFSI.
    """
    paires, erreurs = charge_banque()
    cartes = [c for c, _ in paires]
    v2, erreurs_v2, _ = charge_cartes_v2({"banque", "interne"}, False, date.today())
    return cartes + v2, erreurs + erreurs_v2


def charge_contexte(args) -> dict:
    """Config, banque, journal et cursus : tout ce que la surface lit."""
    config = charge_config()
    profil, erreur_profil = profil_actif(args, config)
    if erreur_profil:
        return {"erreur_profil": erreur_profil}
    etat = dossier_etat(args)
    collision = collision_pseudo(etat, profil)
    if collision:
        return {"erreur_profil": collision}
    incoherence = raison_profil_incoherent(profil, etat)
    if incoherence:
        return {"erreur_profil": incoherence}
    cartes, erreurs = charge_cartes_du_depot()
    journal = lit_journal(profil, etat)
    prefs = charge_profil(profil, etat)
    config = config_du_profil(config, prefs)

    cle = cursus_actif(journal, args, prefs)
    cursus = charge_cursus(cle) if cle else None
    explicite = getattr(args, "cursus", None)
    erreur_cursus = (f"cursus inconnu : {explicite}"
                     if explicite and cursus is None else None)
    if cursus is not None:
        programme = cursus["programme"]
        config = config_du_cursus(config, programme)
        domaines = set(programme.get("domaines") or {})
        if domaines:
            cartes = [c for c in cartes if c.get("domaine") in domaines]
    else:
        programme = charge_programme() or None

    sched = Planificateur(retention=config["fsrs"]["retention_souhaitee"])
    return {
        "config": config,
        "profil": profil,
        "prefs": prefs,
        "cursus": cle,
        "erreur_cursus": erreur_cursus,
        "cartes": cartes,
        "erreurs": erreurs,
        "journal": journal,
        "sched": sched,
        "programme": programme,
        "etats": seance_mod.etats_cartes(journal, sched),
    }


def cartes_jouables(cartes: list[dict]) -> list[dict]:
    return [c for c in cartes if c.get("statut") == "valide"]


def _version_banque(cartes: list[dict]) -> str:
    """Empreinte courte des cartes jouables servies : la « version » locale."""
    ids = sorted(str(c["id"]) for c in cartes_jouables(cartes))
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()[:12]


def trouve_carte(cartes: list[dict], cid: str) -> dict | None:
    return next((c for c in cartes if str(c.get("id")) == cid), None)


# --- présentation : ce que l'agent affiche ----------------------------

def presentation_question(carte: dict) -> dict:
    """La carte côté question : aucun champ de réponse ne s'y trouve."""
    vue = {c: carte[c] for c in CHAMPS_QUESTION
           if carte.get(c) not in (None, [], "", 0)}
    choix = carte.get("choix")
    if choix:
        vue["choix"] = [{"texte": c.get("texte")} for c in choix]
    image = carte.get("image")
    if isinstance(image, dict) and image.get("fichier"):
        vue["image"] = {"fichier": image["fichier"], "alt": image.get("alt"),
                        "credit": image.get("credit"), "licence": image.get("licence"),
                        "url": _uri_image(image["fichier"])}
    return vue


def presentation_correction(carte: dict) -> dict:
    """La carte côté correction : la réponse, le pourquoi, la vigilance."""
    vue = {c: carte[c] for c in CHAMPS_CORRECTION
           if carte.get(c) not in (None, [], "")}
    if carte.get("choix"):
        vue["choix"] = [{"texte": c.get("texte"), "correct": bool(c.get("correct")),
                         "pourquoi_faux": c.get("pourquoi_faux")}
                        for c in carte["choix"]]
    if carte.get("source"):
        vue["source"] = carte["source"]
    return vue


def _uri_image(rel: str) -> str | None:
    chemin = (BANQUE / rel)
    try:
        return chemin.resolve().as_uri() if chemin.is_file() else None
    except ValueError:
        return None


# --- commandes --------------------------------------------------------

def cmd_etat(args, ctx) -> int:
    jouables = cartes_jouables(ctx["cartes"])
    etats = ctx["etats"]
    aujourdhui = date.today()
    dues = [c for c in jouables
            if etats.get(c["id"]) and etats[c["id"]]["du_le"] <= aujourdhui.toordinal()]
    jamais = [c for c in jouables if c["id"] not in etats]
    monde = progression_mod.carte_monde(
        ctx["cartes"], ctx["journal"], ctx["config"], programme=ctx["programme"])
    resume = {
        "profil": ctx["profil"],
        "cursus": ctx.get("cursus"),
        "date": aujourdhui.isoformat(),
        "jour": seance_mod.couleur_du_jour(ctx["config"], aujourdhui),
        "revisions_dues": len(dues),
        "jamais_vues": len(jamais),
        "cartes_jouables": len(jouables),
        "xp": monde["xp"],
        "remplissage_global": monde["remplissage_global"],
        "regions_ouvertes": monde["regions_ouvertes"],
        "noeuds_a_revoir": sum(1 for n in monde["noeuds"] if n["a_revoir"]),
    }
    if not jouables:
        resume["trou"] = ("aucune carte `valide` : la banque n'est pas encore "
                          "vérifiée, rien ne se joue")
    if args.json:
        print(json.dumps(resume, ensure_ascii=False, indent=2))
        return 0
    print(f"Profil {ctx['profil']} — {aujourdhui.isoformat()} — "
          f"{resume['jour']} — cursus {ctx.get('cursus') or 'aucun'}")
    if resume.get("trou"):
        print(f"  {resume['trou']}")
        return 0
    print(f"  {resume['revisions_dues']} révision(s) due(s), "
          f"{resume['jamais_vues']} jamais vue(s), "
          f"{resume['cartes_jouables']} jouable(s)")
    print(f"  {resume['xp']} points de savoir — "
          f"remplissage global {resume['remplissage_global']:.0%}")
    print(f"  régions ouvertes : {', '.join(resume['regions_ouvertes']) or 'aucune'}")
    if resume["noeuds_a_revoir"]:
        print(f"  {resume['noeuds_a_revoir']} nœud(s) à revoir")
    return 0


def cmd_seance(args, ctx) -> int:
    seance = seance_mod.compose(
        ctx["cartes"], ctx["etats"], ctx["config"], date.today(), ctx["sched"],
        cap=args.cap, programme=ctx["programme"], journal=ctx["journal"])
    charge = dict(seance)
    charge["cartes"] = [presentation_question(c)
                        for c in seance["revisions"] + seance["nouveau"]]
    charge["total"] = len(charge["cartes"])
    if args.journaliser:
        with _etat_actif(dossier_etat(args)):
            charge["ouverture"] = seance_mod.ouvre_seance(
                ctx["profil"], seance, _version_banque(ctx["cartes"]), MOTEUR_VERSION)
    if args.json:
        print(json.dumps(charge, ensure_ascii=False, indent=2))
        return 0
    print(f"Séance du {seance['date']} — {seance['jour']} — profil {ctx['profil']}")
    print(f"  {len(seance['revisions'])} révision(s), {len(seance['nouveau'])} nouvelle(s)")
    if not charge["total"]:
        print("  Rien n'est dû ce matin. Une étude, ou au hasard ?")
        return 0
    for raison in seance.get("pourquoi", []):
        print(f"  · {raison}")
    premiere = charge["cartes"][0]
    print(f"\nPremière carte : {premiere['id']}")
    print(f"  {premiere['question']}")
    if premiere.get("choix"):
        for i, c in enumerate(premiere["choix"], 1):
            print(f"    {i}. {c['texte']}")
    return 0


def cmd_carte(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    vue = presentation_question(carte)
    if args.reponse:
        vue["correction"] = presentation_correction(carte)
    if args.json:
        print(json.dumps(vue, ensure_ascii=False, indent=2))
        return 0
    print(f"[{vue.get('domaine')}] {vue['question']}")
    if vue.get("choix"):
        for i, c in enumerate(vue["choix"], 1):
            print(f"  {i}. {c['texte']}")
    for src in vue.get("source", []) or []:
        nature = src.get("nature") or "sans nature"
        print(f"  source ({nature}) : {src.get('texte')}")
    if args.reponse:
        print("\n" + rendu_correction(carte))
    return 0


def cmd_correction(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    if args.json:
        print(json.dumps(presentation_correction(carte), ensure_ascii=False, indent=2))
        return 0
    print(rendu_correction(carte))
    return 0


def rendu_correction(carte: dict) -> str:
    lignes = [f"Réponse : {carte.get('reponse')}"]
    if carte.get("choix"):
        for c in carte["choix"]:
            marque = "juste" if c.get("correct") else "faux"
            detail = "" if c.get("correct") else f" ({c.get('pourquoi_faux')})"
            lignes.append(f"  [{marque}] {c.get('texte')}{detail}")
    if carte.get("explication"):
        lignes.append(f"Pourquoi : {carte['explication']}")
    if carte.get("vigilance"):
        lignes.append(f"Vigilance : {carte['vigilance']}")
    return "\n".join(lignes)


def cmd_repondre(args, ctx) -> int:
    if args.note not in (1, 2, 3, 4):
        return _trou("note attendue entre 1 (raté) et 4 (facile)", args)
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    if carte.get("statut") != "valide":
        return _trou(f"carte non jouable (statut `{carte.get('statut')}`) : "
                     f"rien n'est journalisé", args)
    ligne = ajoute_revue(ctx["profil"], args.carte, args.note, args.format,
                         dossier_etat(args), duree_ms=args.duree_ms)
    reste = _dues_apres(ctx, ligne)
    if args.json:
        print(json.dumps({"ecrit": ligne, "revisions_dues_restantes": reste},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"noté : {ligne['carte']} → {ligne['note']} "
          f"({ligne['quand']}) — {reste} révision(s) encore due(s)")
    return 0


def _dues_apres(ctx, ligne: dict) -> int:
    journal = ctx["journal"] + [ligne]
    etats = seance_mod.etats_cartes(journal, ctx["sched"])
    aujourdhui = date.today().toordinal()
    return sum(1 for c in cartes_jouables(ctx["cartes"])
               if etats.get(c["id"]) and etats[c["id"]]["du_le"] <= aujourdhui)


def cmd_progression(args, ctx) -> int:
    monde = progression_mod.carte_monde(
        ctx["cartes"], ctx["journal"], ctx["config"], programme=ctx["programme"])
    if args.json:
        print(json.dumps(monde, ensure_ascii=False, indent=2))
        return 0
    print(f"Carte-monde — profil {ctx['profil']} — {monde['xp']} points de savoir")
    print(f"  remplissage global {monde['remplissage_global']:.0%}")
    for region in monde["regions"]:
        marque = "ouverte" if region["ouverte"] else "explorable"
        print(f"  · {region['titre']:<38} {region['remplissage']:6.0%}  "
              f"{region['cartes_acquises']}/{region['cartes_totales']}  ({marque})")
    if monde["noeuds"]:
        print(f"  arbre : {len(monde['noeuds'])} nœud(s), "
              f"{len(monde['branches'])} branche(s)")
    return 0


# --- artefacts HTML jetables ------------------------------------------

def _page(titre: str, corps: str) -> str:
    return f"""<!doctype html>
<html lang="fr">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titre)}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.5 system-ui, sans-serif; max-width: 44rem;
          margin: 3rem auto; padding: 0 1.2rem; }}
  h1 {{ font-size: 1.25rem; font-weight: 600; }}
  .choix {{ display: block; width: 100%; text-align: left; margin: .4rem 0;
            padding: .7rem .9rem; border: 1px solid currentColor;
            border-radius: .5rem; background: transparent; color: inherit;
            font: inherit; cursor: pointer; }}
  .juste {{ border-width: 2px; }}
  .pourquoi {{ opacity: .75; font-size: .92rem; }}
  .source {{ opacity: .75; font-size: .9rem; border-top: 1px solid currentColor;
             margin-top: 1.5rem; padding-top: .8rem; }}
  .reponse {{ border-left: 3px solid currentColor; padding-left: .9rem;
              margin-top: 1rem; }}
</style>
{corps}
</html>
"""


def _bloc_source(carte: dict) -> str:
    lignes = []
    for src in carte.get("source") or []:
        nature = html.escape(str(src.get("nature") or "sans nature"))
        texte = html.escape(str(src.get("texte") or ""))
        lignes.append(f"<div>{texte} <em>({nature})</em></div>")
    if not lignes:
        return ""
    return f'<div class="source">Sources :<br>{"".join(lignes)}</div>'


def artefact_qcm(carte: dict) -> str:
    choix = carte.get("choix") or []
    lignes = []
    for c in choix:
        texte = html.escape(str(c.get("texte") or ""))
        juste = "1" if c.get("correct") else "0"
        pourquoi = "" if c.get("correct") else html.escape(str(c.get("pourquoi_faux") or ""))
        detail = f'<div class="pourquoi" hidden>{pourquoi}</div>' if pourquoi else ""
        lignes.append(
            f'<button class="choix" data-juste="{juste}" '
            f'onclick="reveler(this)">{texte}{detail}</button>')
    corps = (
        f"<h1>{html.escape(str(carte.get('question') or ''))}</h1>"
        f"{''.join(lignes)}"
        f"{_bloc_source(carte)}"
        "<script>function reveler(b){var p=b.querySelector('.pourquoi');"
        "if(p)p.hidden=false;if(b.dataset.juste==='1')b.classList.add('juste');}</script>")
    return _page("QCM", corps)


def artefact_fiche(carte: dict) -> str:
    image = carte.get("image") or {}
    img = ""
    uri = _uri_image(image.get("fichier")) if image.get("fichier") else None
    if uri:
        img = f'<p><img src="{html.escape(uri)}" alt="{html.escape(str(image.get("alt") or ""))}" style="max-width:100%"></p>'
    explication = carte.get("explication")
    vigilance = carte.get("vigilance")
    corps = (
        f"<h1>{html.escape(str(carte.get('question') or ''))}</h1>"
        f"{img}"
        f'<div class="reponse"><strong>Réponse :</strong> '
        f"{html.escape(str(carte.get('reponse') or ''))}</div>"
        + (f"<p>{html.escape(str(explication))}</p>" if explication else "")
        + (f"<p><em>Vigilance : {html.escape(str(vigilance))}</em></p>" if vigilance else "")
        + _bloc_source(carte))
    return _page("Fiche de carte", corps)


def _ecrit_artefact(nom: str, contenu: str, args) -> Path:
    dossier = Path(args.sortie) if getattr(args, "sortie", None) else DOSSIER_SORTIES
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / nom
    chemin.write_text(contenu, encoding="utf-8")
    return chemin


def _ouvre(chemin: Path, args) -> None:
    if getattr(args, "ouvrir", False):
        try:
            webbrowser.open(chemin.resolve().as_uri())
        except Exception:  # noqa: BLE001  (un poste sans navigateur ne casse rien)
            pass


def cmd_qcm(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    if carte.get("type") != "qcm" or not carte.get("choix"):
        return _trou(f"la carte {args.carte} n'est pas un QCM (type "
                     f"`{carte.get('type')}`) : essaie `schema`", args)
    chemin = _ecrit_artefact(f"qcm-{args.carte}.html", artefact_qcm(carte), args)
    print(chemin)
    _ouvre(chemin, args)
    return 0


def cmd_schema(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    chemin = _ecrit_artefact(f"fiche-{args.carte}.html", artefact_fiche(carte), args)
    print(chemin)
    _ouvre(chemin, args)
    return 0


# --- carnet d'erreurs et quiz (ACA-SANS-FRONT-2) ----------------------

def cmd_erreur(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    ligne = erreurs_mod.note_erreur(ctx["profil"], args.carte, args.raison,
                                    mode=args.mode, racine_etat=dossier_etat(args))
    if args.json:
        print(json.dumps({"ecrit": ligne}, ensure_ascii=False, indent=2))
        return 0
    detail = f" — {ligne['raison']}" if ligne.get("raison") else ""
    print(f"noté au carnet : {ligne['carte']}{detail}")
    return 0


def cmd_erreurs(args, ctx) -> int:
    carnet = erreurs_mod.lit_carnet(ctx["profil"], racine_etat=dossier_etat(args))
    recurrentes = erreurs_mod.raisons_recurrentes(carnet)
    resume = {"profil": ctx["profil"], "lignes": len(carnet),
              "cartes": recurrentes["par_carte"], "mots": recurrentes["par_mot"]}
    if args.json:
        print(json.dumps(resume, ensure_ascii=False, indent=2))
        return 0
    print(f"Carnet d'erreurs — profil {ctx['profil']} — {len(carnet)} ligne(s)")
    if not carnet:
        print("  Rien de noté. Une raison tient en une ligne, ou pas du tout.")
        return 0
    for fiche in recurrentes["par_carte"]:
        print(f"  · {fiche['carte']} : {fiche['occurrences']} fois")
    for bloc in recurrentes["par_mot"][:5]:
        print(f"  · « {bloc['mot']} » revient sur {bloc['occurrences']} carte(s)")
    return 0


def cmd_quiz(args, ctx) -> int:
    regions = [args.region] if args.region else None
    graine = args.graine if args.graine is not None else date.today().toordinal()
    questions = quiz_mod.compose(ctx["cartes"], ctx["config"], graine=graine,
                                 regions=regions)
    if args.resultats is None:
        charge = {"graine": graine, "region": args.region,
                  "questions": [presentation_question(c) for c in questions]}
        if args.json:
            print(json.dumps(charge, ensure_ascii=False, indent=2))
            return 0
        print(f"Quiz de positionnement — {len(questions)} question(s) — graine {graine}")
        for c in charge["questions"]:
            print(f"  · [{c.get('domaine')}] {c['question']}")
        print("  Réponds, puis clôt avec `quiz --resultats '<json>'`.")
        return 0
    try:
        reponses = json.loads(args.resultats)
    except json.JSONDecodeError as exc:
        return _trou(f"resultats illisibles : {exc}", args)
    if not isinstance(reponses, dict):
        return _trou("resultats attendus : un objet {id: true|false}", args)
    resultats = []
    for cid, juste in reponses.items():
        carte = trouve_carte(ctx["cartes"], cid)
        if carte is None:
            return _trou(f"carte inconnue : {cid}", args)
        resultats.append({"carte": cid, "domaine": carte.get("domaine"),
                          "juste": bool(juste)})
    try:
        lignes = quiz_mod.applique_resultats(ctx["profil"], resultats, ctx["config"],
                                             racine_etat=dossier_etat(args),
                                             quand=args.quand)
    except quiz_mod.QuizDejaJoue as exc:
        return _trou(str(exc), args)
    ouvertes = quiz_mod.regions_ouvertes(resultats, ctx["config"])
    if args.json:
        print(json.dumps({"ecrites": len(lignes), "regions_ouvertes": ouvertes},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"Quiz clos : {len(lignes)} bonne(s) réponse(s) écrite(s) ; "
          f"régions ouvertes : {', '.join(ouvertes) or 'aucune'}")
    return 0


# --- aides de séance (ACA-SANS-FRONT-3) -------------------------------

def _intervalles(carte: dict, etats: dict, sched) -> dict:
    """Le prochain intervalle pour chaque note, calculé par le moteur."""
    etat = etats.get(carte["id"])
    aujourdhui = date.today()
    resultat = {}
    for note in (1, 2, 3, 4):
        if etat is None:
            stabilite, _ = sched.premiere(note)
        else:
            ecoules = max(0, (aujourdhui - etat["vu_le"]).days)
            stabilite, _ = sched.revise(etat["stabilite"], etat["difficulte"],
                                        note, ecoules)
        resultat[note] = {"stabilite_jours": round(stabilite, 1),
                          "intervalle_jours": sched.intervalle(stabilite)}
    return resultat


def cmd_prevue(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    vue = {"id": carte["id"], "etat_actuel": ctx["etats"].get(carte["id"]),
           "intervalles": _intervalles(carte, ctx["etats"], ctx["sched"])}
    if args.json:
        print(json.dumps(vue, ensure_ascii=False, indent=2))
        return 0
    libelles = {1: "raté", 2: "dur", 3: "bien", 4: "facile"}
    print(f"Carte {carte['id']} — prochaine échéance selon ta note :")
    for note in (1, 2, 3, 4):
        info = vue["intervalles"][note]
        print(f"  {note} {libelles[note]:<6} : {info['intervalle_jours']} j "
              f"(stabilité {info['stabilite_jours']} j)")
    return 0


def cmd_mini_lecons(args, ctx) -> int:
    a_lecon = erreurs_mod.cartes_a_mini_lecon(ctx["journal"], ctx["config"])
    carnet = erreurs_mod.lit_carnet(ctx["profil"], racine_etat=dossier_etat(args))
    recurrentes = erreurs_mod.raisons_recurrentes(carnet)
    par_id = {c["id"]: c for c in ctx["cartes"]}
    cartes = []
    for fiche in a_lecon:
        carte = par_id.get(fiche["carte"])
        cartes.append({**fiche,
                       "question": carte.get("question") if carte else None})
    vue = {"cartes": cartes, "raisons": recurrentes["par_mot"]}
    if args.json:
        print(json.dumps(vue, ensure_ascii=False, indent=2))
        return 0
    print(f"Mini-leçons — {len(cartes)} carte(s) ratée(s) plusieurs fois")
    if not cartes:
        print("  Rien à reprendre : aucune carte n'atteint le seuil d'échecs.")
        return 0
    for fiche in cartes:
        print(f"  · {fiche['carte']} : {fiche['echecs']} raté(s)")
        if fiche.get("question"):
            print(f"    {fiche['question'][:90]}")
    return 0


def cmd_rituel(args, ctx) -> int:
    chemin = dossier_etat(args) / ctx["profil"] / "revues.jsonl"
    rapport = rituel_mod.rapport(rituel_mod.lit(chemin))
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
        return 0
    print(rituel_mod.rend(rapport))
    return 0


def _ecrit_cursus(profil: str, cle: str) -> dict:
    """Inscrit le choix de cursus au journal (mode cursus, contrat v1)."""
    ligne = {"quand": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "mode": "cursus", "nonce": secrets.token_hex(8), "cursus": cle}
    p = seance_mod.chemin_revues(profil)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def cmd_cursus(args, ctx) -> int:
    parcours = charge_catalogue().get("parcours", [])
    if args.cle:
        if not any(str(p.get("cle")) == args.cle for p in parcours):
            return _trou(f"cursus inconnu : {args.cle}", args)
        with _etat_actif(dossier_etat(args)):
            _ecrit_cursus(ctx["profil"], args.cle)
        print(f"cursus actif : {args.cle}")
        return 0
    if args.json:
        print(json.dumps({"actif": ctx.get("cursus"), "parcours": parcours},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"Cursus actif : {ctx.get('cursus') or 'aucun'}")
    for p in parcours:
        marque = " (actif)" if str(p.get("cle")) == str(ctx.get("cursus")) else ""
        print(f"  · {p.get('cle')} : {p.get('titre')}{marque}")
    return 0


# --- arrivée locale et profil (ACA-ONBOARDING-2) ----------------------

def _profils_locaux(etat: Path) -> list[str]:
    """Les pseudos déjà écrits, pour laisser choisir quand il y en a plusieurs."""
    racine = Path(etat)
    if not racine.is_dir():
        return []
    noms = [e.name for e in racine.iterdir()
            if e.is_dir() and (e / "profil.json").is_file()
            and valide_pseudo(e.name) is None]
    return sorted(noms, key=str.lower)


def cmd_accueil(args, ctx) -> int:
    """L'arrivée : ce qu'il faut pour choisir, et l'état du profil local.

    Un seul appel rend tout ce que l'agent présente au premier message :
    le catalogue, la liste des voix, la liste des exigences, les zones de
    dépôt et si un profil existe déjà.
    """
    catalogue = charge_catalogue()
    arrivee = charge_arrivee()
    prefs = ctx.get("prefs")
    selection, _ = lit_selection(dossier_etat(args))
    source = ("option" if getattr(args, "profil", None) is not None
              else "selection" if selection else "defaut")
    charge = {
        "profil_existe": prefs is not None,
        "profil": prefs,
        "pseudo_actif": ctx["profil"],
        "profil_actif_source": source,
        "selection": selection,
        "profils_locaux": _profils_locaux(dossier_etat(args)),
        "activation": {
            "commande": "python3 app/academie.py profil --activer <pseudo>",
            "active": selection is not None,
        },
        "catalogue": catalogue.get("parcours", []),
        "creer_le_votre": catalogue.get("creer_le_votre", {}),
        "voix": arrivee.get("voix", []),
        "exigences": arrivee.get("exigences", []),
        "depot": arrivee.get("depot", {}),
        "etat": str(dossier_etat(args)),
    }
    if prefs is None:
        charge["trou"] = ("aucun profil local : l'arrivée n'a pas encore "
                          "été faite")
    if args.json:
        print(json.dumps(charge, ensure_ascii=False, indent=2))
        return 0
    if prefs is None:
        print("Aucun profil local. L'arrivée commence ici.")
    else:
        print(f"Profil {prefs.get('pseudo')} : cursus "
              f"{prefs.get('cursus') or 'aucun'}, voix {prefs.get('voix')}, "
              f"exigence {prefs.get('exigence')}")
    parcours = charge["catalogue"]
    print(f"  cursus : {', '.join(str(p.get('cle')) for p in parcours) or 'aucun'}")
    print(f"  voix : {', '.join(str(v.get('cle')) for v in charge['voix']) or 'aucune'}")
    print("  exigences : "
          f"{', '.join(str(e.get('cle')) for e in charge['exigences']) or 'aucune'}")
    depot = charge["depot"]
    print(f"  dépôt public : {depot.get('public')}")
    print(f"  dépôt privé : {depot.get('prive')}")
    print(f"  état : {charge['etat']}")
    return 0


def _choix_profil(args, arrivee: dict) -> tuple[dict | None, str | None]:
    """Valide les choix d'un profil avant écriture. Aucune écriture ici."""
    pseudo = getattr(args, "pseudo", None)
    erreur_pseudo = valide_pseudo(pseudo)
    if erreur_pseudo:
        return None, erreur_pseudo
    cursus = getattr(args, "cursus", None)
    if cursus and not any(str(p.get("cle")) == str(cursus)
                          for p in charge_catalogue().get("parcours", [])):
        return None, f"cursus inconnu : {cursus}"
    voix = getattr(args, "voix", None) or "sobre"
    if not any(v.get("cle") == voix for v in arrivee.get("voix", [])):
        return None, f"voix inconnue : {voix}"
    exigence = getattr(args, "exigence", None) or "standard"
    if not any(e.get("cle") == exigence for e in arrivee.get("exigences", [])):
        return None, f"exigence inconnue : {exigence}"
    return {"pseudo": str(pseudo), "cursus": cursus, "voix": voix,
            "exigence": exigence}, None


def _valide_prefs(prefs, profil: str, contexte: str = "préférences") -> str | None:
    """Les préférences sont-elles jouables, et bien celles de ce profil."""
    if not isinstance(prefs, dict):
        return f"{contexte} attendues sous forme d'objet"
    if prefs.get("format") != PROFIL_FORMAT:
        return f"{contexte} de format inconnu"
    erreur = valide_pseudo(prefs.get("pseudo"))
    if erreur:
        return f"{contexte} : {erreur}"
    if prefs.get("pseudo") != profil:
        return (f"{contexte} du profil {prefs.get('pseudo')}, "
                f"pas celles de {profil}")
    arrivee = charge_arrivee()
    cursus = prefs.get("cursus")
    if cursus and not any(str(p.get("cle")) == str(cursus)
                          for p in charge_catalogue().get("parcours", [])):
        return f"{contexte} : cursus inconnu {cursus}"
    if not any(v.get("cle") == prefs.get("voix") for v in arrivee.get("voix", [])):
        return f"{contexte} : voix inconnue {prefs.get('voix')}"
    if not any(e.get("cle") == prefs.get("exigence")
               for e in arrivee.get("exigences", [])):
        return f"{contexte} : exigence inconnue {prefs.get('exigence')}"
    return None


def cmd_profil(args, ctx) -> int:
    """Lire le profil actif, l'écrire (`--pseudo`) ou le sélectionner (`--activer`)."""
    arrivee = charge_arrivee()
    etat = dossier_etat(args)
    a_activer = getattr(args, "activer", None)
    pseudo = getattr(args, "pseudo", None)
    if a_activer is not None and pseudo is not None:
        return _trou("choisissez --pseudo (écrire) ou --activer (sélectionner), "
                     "pas les deux", args)
    if a_activer is not None:
        erreur = valide_pseudo(a_activer)
        if erreur:
            return _trou(erreur, args)
        collision = collision_pseudo(etat, a_activer)
        if collision:
            return _trou(collision, args)
        if charge_profil(str(a_activer), etat) is None:
            raison = raison_profil_incoherent(str(a_activer), etat)
            if raison:
                return _trou(raison, args)
            return _trou(f"aucun profil local pour {a_activer} : écrivez-le "
                         f"d'abord avec profil --pseudo {a_activer}", args)
        cible = ecrit_selection(etat, str(a_activer))
        if args.json:
            print(json.dumps({"actif": str(a_activer), "selection": str(cible)},
                             ensure_ascii=False, indent=2))
            return 0
        print(f"profil actif : {a_activer} ({cible})")
        return 0
    if pseudo is None:
        nom = ctx["profil"]
        prefs = ctx.get("prefs") or charge_profil(nom, dossier_etat(args))
        if prefs is None:
            return _trou("aucun profil local : l'arrivée n'a pas encore "
                         "été faite", args)
        if args.json:
            print(json.dumps(prefs, ensure_ascii=False, indent=2))
            return 0
        print(f"profil {prefs.get('pseudo')} : cursus "
              f"{prefs.get('cursus') or 'aucun'}, voix {prefs.get('voix')}, "
              f"exigence {prefs.get('exigence')}")
        return 0
    choix, erreur = _choix_profil(args, arrivee)
    if erreur:
        return _trou(erreur, args)
    collision = collision_pseudo(etat, choix["pseudo"])
    if collision:
        return _trou(collision, args)
    ligne = {**choix, "format": PROFIL_FORMAT,
             "cree_le": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    dossier, erreur_chemin = chemin_du_profil(etat, choix["pseudo"])
    if erreur_chemin:
        return _trou(erreur_chemin, args)
    dossier.mkdir(parents=True, exist_ok=True)
    (dossier / "profil.json").write_text(
        json.dumps(ligne, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cible = ecrit_selection(etat, choix["pseudo"])
    if args.json:
        print(json.dumps({**ligne, "actif": choix["pseudo"],
                          "selection": str(cible)}, ensure_ascii=False, indent=2))
        return 0
    print(f"profil écrit : {dossier / 'profil.json'}")
    print(f"profil actif : {choix['pseudo']} ({cible})")
    return 0


# --- sauvegarde et transfert (ACA-SANS-FRONT-7) -----------------------

def _lit_lignes(chemin: Path) -> list[dict]:
    """Un JSONL lu avec tolérance : une ligne illisible est ignorée."""
    if not chemin.is_file():
        return []
    lignes = []
    for brut in chemin.read_text(encoding="utf-8").splitlines():
        brut = brut.strip()
        if not brut:
            continue
        try:
            entree = json.loads(brut)
        except json.JSONDecodeError:
            continue
        if isinstance(entree, dict):
            lignes.append(entree)
    return lignes


def _cle_revue(ligne: dict):
    nonce = ligne.get("nonce")
    if nonce:
        return ("nonce", str(nonce))
    return ("quad", str(ligne.get("quand")), str(ligne.get("mode")),
            str(ligne.get("carte")), str(ligne.get("note")))


def _cle_erreur(ligne: dict):
    return ("err", str(ligne.get("quand")), str(ligne.get("carte")),
            str(ligne.get("mode")), str(ligne.get("raison")))


def _horodatage_bon(valeur) -> bool:
    """ISO 8601 daté, avec ou sans fuseau : les journaux locaux en portent."""
    if not isinstance(valeur, str) or not re.match(r"^\d{4}-\d{2}-\d{2}[Tt]", valeur):
        return False
    try:
        datetime.fromisoformat(valeur.upper().replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _entier(valeur) -> bool:
    return isinstance(valeur, int) and not isinstance(valeur, bool)


def _nombre_fini(valeur) -> bool:
    return isinstance(valeur, (int, float)) and not isinstance(valeur, bool)


def _texte_non_vide(valeur) -> bool:
    return isinstance(valeur, str) and bool(valeur.strip())


def _valide_champs_journal(ligne: dict, cle: str) -> str | None:
    """Les types de `journal-v1`, repris du valideur serveur.

    Les lignes historiques locales restent lisibles : un `flash` sans
    `nonce` passe. Les champs présents sont jugés, parce qu'un
    `note: "oops"` accepté casserait le moteur après l'import.
    """
    if "note" in ligne and not (_entier(ligne["note"]) and 1 <= ligne["note"] <= 4):
        return f"sauvegarde mal formée : note hors contrat dans « {cle} »"
    if "format" in ligne and not _texte_non_vide(ligne["format"]):
        return f"sauvegarde mal formée : format invalide dans « {cle} »"
    if "duree_ms" in ligne and not (_entier(ligne["duree_ms"]) and ligne["duree_ms"] >= 0):
        return f"sauvegarde mal formée : duree_ms invalide dans « {cle} »"
    if "confiance" in ligne and not isinstance(ligne["confiance"], bool):
        return f"sauvegarde mal formée : confiance invalide dans « {cle} »"
    if "graine" in ligne and not _entier(ligne["graine"]):
        return f"sauvegarde mal formée : graine invalide dans « {cle} »"
    if "stabilite_forcee" in ligne and not (
            _nombre_fini(ligne["stabilite_forcee"]) and ligne["stabilite_forcee"] > 0):
        return f"sauvegarde mal formée : stabilite_forcee invalide dans « {cle} »"
    if "score" in ligne and not (
            _nombre_fini(ligne["score"]) and 0 <= ligne["score"] <= 1):
        return f"sauvegarde mal formée : score hors contrat dans « {cle} »"
    if "raison" in ligne and not isinstance(ligne["raison"], str):
        return f"sauvegarde mal formée : raison invalide dans « {cle} »"
    if "motif" in ligne and not isinstance(ligne["motif"], str):
        return f"sauvegarde mal formée : motif invalide dans « {cle} »"
    if "carte" in ligne and not _texte_non_vide(ligne["carte"]):
        return f"sauvegarde mal formée : carte invalide dans « {cle} »"
    for champ in ("origine", "region", "dossier", "cap", "chapitre",
                  "banque_version", "moteur_version"):
        if champ in ligne and not isinstance(ligne[champ], str):
            return f"sauvegarde mal formée : {champ} invalide dans « {cle} »"
    if "cursus" in ligne and not _texte_non_vide(ligne["cursus"]):
        return f"sauvegarde mal formée : cursus invalide dans « {cle} »"
    if "cartes" in ligne and not (
            isinstance(ligne["cartes"], list)
            and all(isinstance(c, str) for c in ligne["cartes"])):
        return f"sauvegarde mal formée : cartes invalides dans « {cle} »"
    if "attendus_coches" in ligne and not (
            isinstance(ligne["attendus_coches"], list)
            and all(_entier(c) for c in ligne["attendus_coches"])):
        return f"sauvegarde mal formée : attendus_coches invalides dans « {cle} »"
    return None


def _valide_ligne_revue(ligne: dict, cle: str) -> str | None:
    """Un événement de revues.jsonl, jugé sur ses champs présents."""
    if not _horodatage_bon(ligne.get("quand")):
        return f"sauvegarde mal formée : horodatage invalide dans « {cle} »"
    mode = ligne.get("mode")
    if not _texte_non_vide(mode):
        return f"sauvegarde mal formée : mode invalide dans « {cle} »"
    erreur = _valide_champs_journal(ligne, cle)
    if erreur:
        return erreur
    if "nonce" in ligne and not _texte_non_vide(ligne["nonce"]):
        return f"sauvegarde mal formée : nonce invalide dans « {cle} »"
    if mode in ("revision", "flash", "quiz"):
        if not _texte_non_vide(ligne.get("carte")):
            return f"sauvegarde mal formée : {mode} sans carte dans « {cle} »"
        if not (_entier(ligne.get("note")) and 1 <= ligne.get("note", 0) <= 4):
            return f"sauvegarde mal formée : {mode} sans note valide dans « {cle} »"
    if mode in ("erreur", "signalement") and not _texte_non_vide(ligne.get("carte")):
        return f"sauvegarde mal formée : {mode} sans carte dans « {cle} »"
    if mode == "cursus" and not _texte_non_vide(ligne.get("cursus")):
        return f"sauvegarde mal formée : cursus sans clé dans « {cle} »"
    return None


def _valide_ligne_erreur(ligne: dict, cle: str) -> str | None:
    """Une ligne du carnet d'erreurs, jugée sur ses champs présents."""
    if not _horodatage_bon(ligne.get("quand")):
        return f"sauvegarde mal formée : horodatage invalide dans « {cle} »"
    if not _texte_non_vide(ligne.get("carte")):
        return f"sauvegarde mal formée : erreur sans carte dans « {cle} »"
    if "mode" in ligne and not isinstance(ligne["mode"], str):
        return f"sauvegarde mal formée : mode invalide dans « {cle} »"
    if "raison" in ligne and not isinstance(ligne["raison"], str):
        return f"sauvegarde mal formée : raison invalide dans « {cle} »"
    return None


def _union_append(chemin: Path, nouvelles: list, cle) -> int:
    """Ajoute les lignes inconnues d'une sauvegarde. N'écrase jamais."""
    connues = {cle(l) for l in _lit_lignes(chemin)}
    a_ecrire = []
    for ligne in nouvelles:
        if not isinstance(ligne, dict):
            continue
        k = cle(ligne)
        if k in connues:
            continue
        connues.add(k)
        a_ecrire.append(ligne)
    if not a_ecrire:
        return 0
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("a", encoding="utf-8") as f:
        for ligne in a_ecrire:
            f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return len(a_ecrire)


def _chemin_profil(args, ctx, nom: str) -> Path:
    dossier, _ = chemin_du_profil(dossier_etat(args), ctx["profil"])
    return (dossier or (dossier_etat(args) / ctx["profil"])) / nom


def cmd_exporter(args, ctx) -> int:
    etat = dossier_etat(args)
    incoherent = raison_profil_incoherent(ctx["profil"], etat)
    if incoherent:
        return _trou(f"sauvegarde refusée : {incoherent}", args)
    revues = _lit_lignes(_chemin_profil(args, ctx, "revues.jsonl"))
    erreurs = _lit_lignes(_chemin_profil(args, ctx, "erreurs.jsonl"))
    bundle = {
        "format": "academie-sauvegarde-1",
        "profil": ctx["profil"],
        "exporte_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "prefs": charge_profil(ctx["profil"], etat),
        "revues": revues,
        "erreurs": erreurs,
    }
    cible = Path(args.fichier)
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")
    print(f"sauvegarde : {len(revues)} révision(s), {len(erreurs)} erreur(s) → {cible}")
    return 0


def _valide_bundle(bundle, profil: str) -> str | None:
    """Tout ce qui doit être vrai avant d'écrire un octet d'un import."""
    if not isinstance(bundle, dict) or bundle.get("format") != "academie-sauvegarde-1":
        return "ce n'est pas une sauvegarde academie-sauvegarde-1"
    du_bundle = bundle.get("profil")
    erreur = valide_pseudo(du_bundle)
    if erreur:
        return f"sauvegarde sans profil jouable ({erreur}) : import refusé"
    if str(du_bundle) != str(profil):
        return (f"sauvegarde du profil {du_bundle} : import refusé dans {profil}, "
                f"rien n'a été écrit; relancez avec --profil {du_bundle}")
    valideurs = {"revues": _valide_ligne_revue, "erreurs": _valide_ligne_erreur}
    for cle, valideur in valideurs.items():
        lignes = bundle.get(cle)
        if not isinstance(lignes, list):
            return f"sauvegarde mal formée : « {cle} » doit être une liste"
        for ligne in lignes:
            if not isinstance(ligne, dict):
                return f"sauvegarde mal formée : une ligne de « {cle} » n'est pas un objet"
            motif = valideur(ligne, cle)
            if motif:
                return motif
    if bundle.get("prefs") is not None:
        erreur = _valide_prefs(bundle["prefs"], str(profil),
                               "préférences de la sauvegarde")
        if erreur:
            return erreur
    return None


def cmd_importer(args, ctx) -> int:
    source = Path(args.fichier)
    if not source.is_file():
        return _trou(f"fichier introuvable : {source}", args)
    try:
        bundle = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _trou(f"sauvegarde illisible : {exc}", args)
    refus = _valide_bundle(bundle, ctx["profil"])
    if refus:
        return _trou(refus, args)
    ajout_r = _union_append(_chemin_profil(args, ctx, "revues.jsonl"),
                            bundle["revues"], _cle_revue)
    ajout_e = _union_append(_chemin_profil(args, ctx, "erreurs.jsonl"),
                            bundle["erreurs"], _cle_erreur)
    prefs = bundle.get("prefs")
    restaure = False
    if prefs is not None and charge_profil(ctx["profil"], dossier_etat(args)) is None:
        dossier, _ = chemin_du_profil(dossier_etat(args), ctx["profil"])
        dossier.mkdir(parents=True, exist_ok=True)
        (dossier / "profil.json").write_text(
            json.dumps(prefs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        restaure = True
    mots = f"fusion : {ajout_r} révision(s) ajoutée(s), {ajout_e} erreur(s) ajoutée(s)"
    if restaure:
        mots += ", préférences restaurées"
    elif prefs is not None:
        mots += ", préférences locales conservées"
    print(mots)
    return 0


# --- erreurs nommées --------------------------------------------------

def _trou(message: str, args) -> int:
    """Un trou se nomme, il ne se remplit pas d'invention."""
    if getattr(args, "json", False):
        print(json.dumps({"erreur": message}, ensure_ascii=False))
    else:
        print(f"rien à servir : {message}", file=sys.stderr)
    return 2


# --- entrée -----------------------------------------------------------

def construit_parseur() -> argparse.ArgumentParser:
    commun = argparse.ArgumentParser(add_help=False)
    commun.add_argument("--profil")
    commun.add_argument("--cursus", help="le cursus actif (copro, ifsi, ...)")
    commun.add_argument("--etat", type=Path,
                        help="dossier racine du journal (défaut etat/)")
    commun.add_argument("--sortie", type=Path,
                        help="dossier des artefacts HTML (défaut sorties/)")
    commun.add_argument("--json", action="store_true")

    ap = argparse.ArgumentParser(
        description="La surface de jeu de l'Académie, pour un agent.")
    sous = ap.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("etat", parents=[commun], help="où en est le profil")
    p.set_defaults(fn=cmd_etat)

    p = sous.add_parser("seance", parents=[commun], help="la séance du jour")
    p.add_argument("--cap", help="le domaine choisi pour ce matin")
    p.add_argument("--journaliser", action="store_true",
                   help="ouvrir la séance au journal (mode seance, rejouable)")
    p.set_defaults(fn=cmd_seance)

    p = sous.add_parser("carte", parents=[commun], help="une carte, sans sa réponse")
    p.add_argument("carte")
    p.add_argument("--reponse", action="store_true",
                   help="afficher aussi la correction (après la tentative)")
    p.set_defaults(fn=cmd_carte)

    p = sous.add_parser("correction", parents=[commun], help="la réponse d'une carte")
    p.add_argument("carte")
    p.set_defaults(fn=cmd_correction)

    p = sous.add_parser("repondre", parents=[commun], help="journaliser une réponse")
    p.add_argument("carte")
    p.add_argument("note", type=int)
    p.add_argument("--format", default="seance")
    p.add_argument("--duree-ms", type=int)
    p.set_defaults(fn=cmd_repondre)

    p = sous.add_parser("progression", parents=[commun], help="la carte-monde")
    p.set_defaults(fn=cmd_progression)

    p = sous.add_parser("qcm", parents=[commun], help="un QCM HTML jetable")
    p.add_argument("carte")
    p.add_argument("--ouvrir", action="store_true")
    p.set_defaults(fn=cmd_qcm)

    p = sous.add_parser("schema", parents=[commun], help="une fiche HTML jetable")
    p.add_argument("carte")
    p.add_argument("--ouvrir", action="store_true")
    p.set_defaults(fn=cmd_schema)

    p = sous.add_parser("erreur", parents=[commun],
                        help="noter pourquoi une carte est ratée")
    p.add_argument("carte")
    p.add_argument("raison", nargs="?", help="une ligne, facultative")
    p.add_argument("--mode", default="flash")
    p.set_defaults(fn=cmd_erreur)

    p = sous.add_parser("erreurs", parents=[commun], help="relire le carnet d'erreurs")
    p.set_defaults(fn=cmd_erreurs)

    p = sous.add_parser("quiz", parents=[commun], help="quiz de positionnement")
    p.add_argument("--region")
    p.add_argument("--graine", type=int)
    p.add_argument("--resultats", help="objet JSON {carte: true|false} pour clore")
    p.add_argument("--quand")
    p.set_defaults(fn=cmd_quiz)

    p = sous.add_parser("mini-lecons", parents=[commun],
                        help="les cartes ratées plusieurs fois, à reprendre")
    p.set_defaults(fn=cmd_mini_lecons)

    p = sous.add_parser("prevue", parents=[commun],
                        help="la prochaine échéance selon la note choisie")
    p.add_argument("carte")
    p.set_defaults(fn=cmd_prevue)

    p = sous.add_parser("rituel", parents=[commun],
                        help="le rapport d'habitude, lu depuis le journal")
    p.set_defaults(fn=cmd_rituel)

    p = sous.add_parser("cursus", parents=[commun],
                        help="le cursus actif et son choix")
    p.add_argument("cle", nargs="?", help="le cursus à activer (copro, ifsi, ...)")
    p.set_defaults(fn=cmd_cursus)

    p = sous.add_parser("accueil", parents=[commun],
                        help="l'arrivée : catalogue, voix, exigences, dépôt")
    p.set_defaults(fn=cmd_accueil)

    p = sous.add_parser("profil", parents=[commun],
                        help="lire le profil actif, l'écrire (--pseudo) ou le choisir (--activer)")
    p.add_argument("--pseudo", help="le pseudo à écrire (sinon lecture)")
    p.add_argument("--activer",
                   help="sélectionner un profil déjà écrit pour les commandes suivantes")
    p.add_argument("--voix", help="sobre, direct ou patient")
    p.add_argument("--exigence", help="detendu, standard ou exigeant")
    p.set_defaults(fn=cmd_profil)

    p = sous.add_parser("exporter", parents=[commun],
                        help="sauvegarder le journal et le carnet")
    p.add_argument("fichier")
    p.set_defaults(fn=cmd_exporter)

    p = sous.add_parser("importer", parents=[commun],
                        help="fusionner une sauvegarde (union, sans écraser)")
    p.add_argument("fichier")
    p.set_defaults(fn=cmd_importer)

    return ap


def main() -> int:
    args = construit_parseur().parse_args()
    try:
        ctx = charge_contexte(args)
    except SystemExit as exc:
        return int(exc.code or 1)
    if ctx.get("erreur_profil"):
        return _trou(ctx["erreur_profil"], args)
    if ctx.get("erreur_cursus"):
        return _trou(ctx["erreur_cursus"], args)
    if ctx["erreurs"]:
        return _trou("la banque est illisible : python3 app/valide_banque.py", args)
    return args.fn(args, ctx)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Le quiz de positionnement — « ne pas retaper les bases ».

~20 questions au premier lancement d'une région, pour que le joueur qui
sait déjà ne repasse pas trois semaines sur ce qu'il maîtrise
(SPEC-PRODUIT §3, mécanique corrigée au pré-mortem du 29/08/2026).

Ce que le pré-mortem a mesuré, et pourquoi ce module existe :
`planificateur.premiere(BIEN)` rend une stabilité de ~2 jours. Inscrire
les bonnes réponses du quiz comme des révisions ordinaires ferait donc
tout revenir dans la semaine — exactement l'inverse de la promesse.
D'où les trois règles dures portées ici :

  1. **Une bonne réponse écrit une entrée de journal avec une stabilité
     FORCÉE** (`stabilite_initiale_jours`, `academie.json`), et un champ
     de provenance `origine: "quiz"`.
  2. **Une mauvaise réponse n'écrit RIEN.** Une erreur sur une carte
     jamais apprise n'est pas un raté FSRS : c'est juste une carte à
     apprendre, elle restera « jamais vue » et sortira comme neuve.
  3. **Le quiz OUVRE des régions, il n'écrit jamais leur remplissage.**
     Le remplissage n'a qu'une définition (le % de cartes dont la
     stabilité mesurée dépasse le seuil, § carte-monde) : seul FSRS le
     mesure, le seuil des ~75 % est donc hors de portée du quiz seul.

**Les entrées `origine: "quiz"` devront être EXCLUES du futur
optimiseur FSRS** (`fsrs.seuil_optimiseur`, ~400 revues) : ce ne sont
pas des révisions observées mais des postulats de départ. Les entraîner
comme des révisions apprendrait au moteur des délais qui n'ont jamais
été testés sur la mémoire du joueur. C'est la raison d'être du champ.

Vocabulaire : une **région** est un domaine de `academie.json`
(`progression._` : « une région = un domaine ici »). Un quiz peut
porter sur une seule région ou sur plusieurs ; le garde-fou « une fois
seulement » joue région par région et par profil.

Le journal écrit ici est CELUI de `seance.py` — `etat/<profil>/
revues.jsonl`, append-only, relu par `seance.etats_cartes`. Il n'existe
pas de second journal, ni d'état stocké : tout se recalcule.

Stdlib seule, aucun seuil en dur : tout vient de la config.
"""

from __future__ import annotations

import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seance  # noqa: E402
from planificateur import BIEN  # noqa: E402

# Une bonne réponse de quiz vaut « bien » (3) : le joueur a su, sans
# plus. La stabilité, elle, ne vient pas de cette note mais de la
# config — c'est tout l'objet du module.
NOTE_BONNE_REPONSE = BIEN
MODE = "quiz"
ORIGINE = "quiz"
ORDRE_INCONNU = 10 ** 6          # une région hors config passe en dernier


class QuizDejaJoue(RuntimeError):
    """Le quiz d'une région a déjà été joué par ce profil."""


# --- lecture / écriture du journal (celui de seance.py) --------------

def chemin_journal(profil: str, racine_etat: Path | None = None) -> Path:
    """Le journal de révisions du profil. `racine_etat` sert aux tests."""
    if racine_etat is None:
        return seance.chemin_revues(profil)
    return Path(racine_etat) / profil / "revues.jsonl"


def lit_journal(profil: str, racine_etat: Path | None = None) -> list[dict]:
    """Relit le journal avec la tolérance de `seance.lit_journal`.

    On passe par seance.py plutôt que de reparser ici : une ligne
    illisible doit être ignorée de la même façon des deux côtés.
    """
    if racine_etat is None:
        return seance.lit_journal(profil)
    ancien = seance.ETAT
    seance.ETAT = Path(racine_etat)
    try:
        return seance.lit_journal(profil)
    finally:
        seance.ETAT = ancien


# --- composition -----------------------------------------------------

def ordre_regions(config: dict) -> dict[str, int]:
    """L'ordre d'apparition des régions, tel que la config le fixe."""
    return {nom: bloc.get("ordre", ORDRE_INCONNU)
            for nom, bloc in config.get("domaines", {}).items()}


def _rang(region: str, ordres: dict[str, int]) -> tuple[int, str]:
    return (ordres.get(region, ORDRE_INCONNU), region)


def repartition(dispo: dict[str, int], budget: int,
                regions: list[str]) -> dict[str, int]:
    """Combien de questions par région, pour couvrir sans gaspiller.

    D'abord une question par région servie tant qu'il reste de la place
    (la couverture prime : un quiz qui ne parlerait que de droit ne
    positionne rien) ; puis le solde au prorata des cartes disponibles,
    aux plus forts restes ; puis un tour de table pour ce qui n'a pas pu
    être placé (régions déjà épuisées).
    """
    parts = {r: 0 for r in regions}
    reste = max(0, min(budget, sum(dispo.get(r, 0) for r in regions)))

    for r in regions:
        if reste <= 0:
            break
        if dispo.get(r, 0) > 0:
            parts[r] += 1
            reste -= 1

    if reste > 0:
        libre = {r: dispo.get(r, 0) - parts[r] for r in regions}
        total_libre = sum(libre.values())
        if total_libre > 0:
            exacts = []
            for r in regions:
                exact = reste * libre[r] / total_libre
                base = int(exact)
                exacts.append((r, base, exact - base))
            for r, base, _ in exacts:
                parts[r] += base
                reste -= base
            for r, _, frac in sorted(exacts, key=lambda t: (-t[2], regions.index(t[0]))):
                if reste <= 0:
                    break
                if parts[r] < dispo.get(r, 0):
                    parts[r] += 1
                    reste -= 1

    while reste > 0:
        avance = False
        for r in regions:
            if reste <= 0:
                break
            if parts[r] < dispo.get(r, 0):
                parts[r] += 1
                reste -= 1
                avance = True
        if not avance:
            break
    return parts


def compose(cartes: list[dict], config: dict, graine: int | None = None,
            regions: list[str] | None = None) -> list[dict]:
    """Les questions du quiz : `nb_questions` cartes `valide`, régions couvertes.

    `regions` restreint le quiz (une région au premier lancement d'un
    domaine) ; sans lui, le quiz positionne sur tout ce qui est jouable.
    Déterministe à graine fixée : deux appels rendent la même liste,
    dans le même ordre.

    Une carte `brouillon` (ou `signale`, ou `perime`) n'est JAMAIS
    servie : c'est la garantie du contrat carte-v1, elle vaut pour le
    quiz comme pour la séance.
    """
    nb = config.get("quiz", {}).get("nb_questions", 0)
    jouables = [c for c in cartes if c.get("statut") == "valide"]
    if regions is not None:
        garde = set(regions)
        jouables = [c for c in jouables if c.get("domaine") in garde]
    if nb <= 0 or not jouables:
        return []

    ordres = ordre_regions(config)
    paquets: dict[str, list[dict]] = {}
    for c in jouables:
        paquets.setdefault(c.get("domaine", ""), []).append(c)
    for paquet in paquets.values():
        paquet.sort(key=lambda c: str(c.get("id")))

    presentes = sorted(paquets, key=lambda r: _rang(r, ordres))
    parts = repartition({r: len(paquets[r]) for r in presentes}, nb, presentes)

    rng = random.Random(graine)
    tirees: list[dict] = []
    for r in presentes:
        k = parts.get(r, 0)
        if k:
            tirees += rng.sample(paquets[r], k)
    # Même entrelacement qu'en séance : on évite les blocs monothématiques.
    return seance.entrelace(tirees, rng)


# --- résultats -------------------------------------------------------

def resultat(carte: dict, juste: bool) -> dict:
    """Le résultat d'une question, tel que les fonctions d'après l'attendent."""
    return {"carte": carte.get("id"), "domaine": carte.get("domaine"),
            "juste": bool(juste)}


def regions_du_quiz(resultats: list[dict]) -> list[str]:
    """Les régions sur lesquelles ce quiz a effectivement posé des questions."""
    vues = []
    for r in resultats:
        dom = r.get("domaine")
        if dom and dom not in vues:
            vues.append(dom)
    return vues


def deja_joue(profil: str, region: str, racine_etat: Path | None = None,
              journal: list[dict] | None = None) -> bool:
    """Ce profil a-t-il déjà passé le quiz de cette région ?

    La preuve est dans le journal lui-même (entrées `origine: "quiz"`
    portant la région) : rien à stocker à côté, donc rien à
    désynchroniser.
    """
    lignes = lit_journal(profil, racine_etat) if journal is None else journal
    return any(l.get("origine") == ORIGINE and l.get("domaine") == region
               for l in lignes)


def applique_resultats(profil: str, resultats: list[dict], config: dict,
                       racine_etat: Path | None = None,
                       quand: str | None = None) -> list[dict]:
    """Inscrit les bonnes réponses au journal. Les mauvaises n'écrivent rien.

    Chaque entrée écrite porte `origine: "quiz"`, la région, et une
    `stabilite_forcee` égale à `quiz.stabilite_initiale_jours` :
    `seance.etats_cartes` honore ce champ au rejeu, de sorte que la
    carte revienne dans trois semaines et pas dans deux jours.

    Lève `QuizDejaJoue` si une des régions a déjà été positionnée pour
    ce profil : le quiz est un point de départ, il ne se rejoue pas.
    """
    if not resultats:
        return []
    bloc = config.get("quiz", {})
    stabilite = float(bloc.get("stabilite_initiale_jours", 0))
    if stabilite <= 0:
        raise ValueError("quiz.stabilite_initiale_jours manquant ou nul en config")

    journal = lit_journal(profil, racine_etat)
    deja = [r for r in regions_du_quiz(resultats)
            if deja_joue(profil, r, journal=journal)]
    if deja:
        raise QuizDejaJoue(
            "quiz de positionnement déjà passé pour : " + ", ".join(deja)
            + " — il ne se rejoue pas, la progression se mesure en séance")

    horodatage = quand or datetime.now(timezone.utc).isoformat(timespec="seconds")
    lignes = []
    for res in resultats:
        if not res.get("juste") or not res.get("carte"):
            continue                       # une erreur de quiz n'est pas un raté FSRS
        lignes.append({"quand": horodatage, "carte": res["carte"],
                       "note": NOTE_BONNE_REPONSE, "mode": MODE,
                       "origine": ORIGINE, "domaine": res.get("domaine"),
                       "stabilite_forcee": stabilite})

    if lignes:
        chemin = chemin_journal(profil, racine_etat)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        with chemin.open("a", encoding="utf-8") as f:
            for ligne in lignes:
                f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return lignes


def regions_ouvertes(resultats: list[dict], config: dict) -> list[str]:
    """Les régions que ce quiz ouvre à l'exploration.

    Une région est ouverte dès que la part de bonnes réponses parmi les
    questions qui lui ont été posées atteint
    `quiz.seuil_ouverture_region_quiz`. C'est un DÉBLOCAGE, pas une
    mesure : aucun taux de remplissage n'est écrit ici, et le moteur de
    progression continue de le calculer depuis les stabilités du
    journal. Rendue dans l'ordre des régions, prête à être passée au
    moteur de progression.
    """
    seuil = config.get("quiz", {}).get("seuil_ouverture_region_quiz")
    if seuil is None:
        raise ValueError("quiz.seuil_ouverture_region_quiz manquant en config")
    posees: dict[str, int] = {}
    justes: dict[str, int] = {}
    for res in resultats:
        dom = res.get("domaine")
        if not dom:
            continue
        posees[dom] = posees.get(dom, 0) + 1
        if res.get("juste"):
            justes[dom] = justes.get(dom, 0) + 1
    ordres = ordre_regions(config)
    ouvertes = [d for d, n in posees.items() if n and justes.get(d, 0) / n >= seuil]
    return sorted(ouvertes, key=lambda r: _rang(r, ordres))

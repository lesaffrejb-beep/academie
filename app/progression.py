#!/usr/bin/env python3
"""La carte-monde : remplissage des régions, ouverture, examens, XP.

Ce module est l'habillage de progression posé sur le moteur FSRS. Il ne
tient AUCUNE comptabilité propre : il n'y a pas de fichier « XP », pas de
« niveau » stocké, pas d'état de région écrit quelque part. Tout se
recalcule depuis `revues.jsonl` (le journal append-only) et la banque,
exactement comme la séance du matin (`seance.etats_cartes`). Changer un
seuil dans `academie.json`, c'est changer la carte au prochain affichage,
sans migration et sans perdre un point.

Le vocabulaire (SPEC-PRODUIT §3) :

  - **région** = un domaine de `academie.json` (les branches restent le
    niveau fin à l'intérieur d'une région, elles ne sont pas des régions) ;
  - **remplissage** d'une région = le % de ses cartes `valide` dont la
    stabilité FSRS atteint `seuil_stabilite_acquise_jours`. Une seule
    définition, une seule mesure, et c'est FSRS qui mesure ;
  - **ouverture** : la première région est toujours ouverte, la suivante
    s'ouvre quand la précédente franchit `seuil_ouverture_region`, ou
    quand le quiz de positionnement l'a débloquée (ce module ne lit pas
    le quiz : les régions qu'il a ouvertes arrivent par le paramètre
    `regions_ouvertes`) ;
  - **explorable** : toute région, ouverte ou non, se joue. Le moteur
    n'interdit rien — « fermée » est une information d'affichage (le
    brouillard), pas un verrou. On a le droit d'aller se frotter au boss
    d'une région lointaine, l'échec y est sans pénalité ;
  - **boss** = l'examen de région. Tant qu'il n'est pas réussi, la région
    plafonne à 99 % (si `examen_obligatoire_pour_100`) : la mesure peut
    dire 100 %, la carte n'affiche pas la région conquise sans son boss.

Tous les seuils viennent de `academie.json`, bloc `progression`. Aucun
n'est écrit ici : un module qui code un seuil en dur ment sur sa config.
Ce module ne sait rien du métier (BLUEPRINT §11) : il ne connaît que des
clés de domaine, jamais ce qu'elles contiennent.

Format de l'entrée de journal d'un examen (contrat pour l'écran d'examen
qui reste à construire) — une ligne de plus dans `revues.jsonl` :

    {"quand": "2026-08-29T07:42:00+00:00",
     "mode": "examen",
     "region": "droit",
     "score": 0.83,
     "cartes": ["droit-0007", "droit-0021", ...]}

    · `mode` vaut exactement "examen" ;
    · `region` est une clé de `domaines` dans `academie.json` ;
    · `score` est un ratio 0..1 (bonnes réponses / cartes servies) ;
    · `cartes` (facultatif) trace le tirage, pour pouvoir rejouer l'examen ;
    · l'entrée NE PORTE PAS de champ `carte` : c'est le résultat de
      l'épreuve, pas une révision. `seance.etats_cartes` l'ignore donc
      d'elle-même, et un examen ne pollue jamais l'état FSRS.

    Les réponses carte par carte données PENDANT l'examen s'écrivent, elles,
    comme des révisions ordinaires (`carte` + `note`, `mode` libre) : une
    révision reste une révision, où qu'elle ait lieu.

    Un examen est réussi dès que `score` >= `examen_score_reussite`. Une
    seule entrée réussie suffit, et les tentatives ratées ne coûtent rien :
    elles restent au journal comme mémoire, sans pénalité.

Usage :
    python3 app/progression.py             # la carte-monde du profil
    python3 app/progression.py --json
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import RETENTION_DEFAUT, Planificateur  # noqa: E402
from seance import etats_cartes, lit_journal  # noqa: E402

CLES_REGLAGES = (
    "seuil_stabilite_acquise_jours",
    "seuil_ouverture_region",
    "examen_obligatoire_pour_100",
    "examen_nb_cartes",
    "examen_score_reussite",
)

# Plafond d'une région dont le boss n'est pas tombé. Ce n'est pas un
# réglage : c'est la règle « le 100 % n'existe pas sans son examen ».
PLAFOND_SANS_EXAMEN = 0.99

# Barème de l'XP AFFICHÉE. Purement décoratif : l'XP se recalcule à
# chaque affichage depuis le journal et le remplissage, elle n'est
# jamais stockée, et la changer ne fait rien perdre à personne. Ces
# valeurs se surchargent depuis `progression` dans `academie.json`
# (clés `xp_par_revue`, `xp_par_region`, `xp_par_examen`) si un jour le
# barème doit bouger.
XP_PAR_REVUE = 10        # une révision réussie (note >= 2)
XP_PAR_REGION = 500      # × le remplissage affiché de chaque région
XP_PAR_EXAMEN = 1000     # un boss tombé


# --- lecture de la config -------------------------------------------

def reglages(config: dict) -> dict:
    """Le bloc `progression` de la config, vérifié complet.

    Échouer ici, bruyamment, plutôt que de retomber sur un seuil deviné :
    une carte-monde calculée avec un seuil implicite est un mensonge
    silencieux.
    """
    bloc = config.get("progression")
    if not isinstance(bloc, dict):
        raise KeyError("config : bloc `progression` absent (voir academie.json)")
    manquants = [c for c in CLES_REGLAGES if c not in bloc]
    if manquants:
        raise KeyError("config `progression` incomplète, manque : "
                       + ", ".join(manquants))
    return bloc


def regions_ordonnees(config: dict) -> list[tuple[str, dict]]:
    """Les régions de la carte-monde, dans l'ordre d'ouverture.

    Un domaine marqué `"arbre": false` (la Culture, tronc commun partagé)
    est hors carte-monde : il n'a pas de rang d'ouverture et n'entre pas
    dans le remplissage global. Il se joue, il ne se conquiert pas.
    """
    domaines = config.get("domaines", {})
    retenus = [(cle, d) for cle, d in domaines.items() if d.get("arbre", True)]
    return sorted(retenus, key=lambda item: (item[1].get("ordre", 999), item[0]))


def regions_hors_carte(config: dict) -> list[tuple[str, dict]]:
    """Les domaines exclus de la carte-monde (`"arbre": false`)."""
    domaines = config.get("domaines", {})
    exclus = [(cle, d) for cle, d in domaines.items() if not d.get("arbre", True)]
    return sorted(exclus, key=lambda item: (item[1].get("ordre", 999), item[0]))


# --- la mesure --------------------------------------------------------

def cartes_region(cartes: list[dict], region: str) -> list[dict]:
    """Les cartes jouables d'une région. `brouillon` n'existe pas ici."""
    return [c for c in cartes
            if c.get("domaine") == region and c.get("statut") == "valide"]


def remplissage_brut(cartes: list[dict], etats: dict, region: str,
                     config: dict) -> float:
    """La mesure nue : part des cartes `valide` de la région acquises.

    Acquise = la stabilité FSRS atteint `seuil_stabilite_acquise_jours`.
    Une région sans carte vaut 0.0 (jamais de division par zéro, jamais
    un 100 % gratuit sur une région vide).
    """
    seuil = reglages(config)["seuil_stabilite_acquise_jours"]
    jouables = cartes_region(cartes, region)
    if not jouables:
        return 0.0
    acquises = sum(1 for c in jouables
                   if (etats.get(c.get("id")) or {}).get("stabilite", 0.0) >= seuil)
    return acquises / len(jouables)


def plafonne(brut: float, examen_reussi: bool, config: dict) -> float:
    """Applique la règle du boss : pas de 100 % sans examen réussi."""
    if not reglages(config)["examen_obligatoire_pour_100"] or examen_reussi:
        return brut
    return min(brut, PLAFOND_SANS_EXAMEN)


# --- les examens ------------------------------------------------------

def entrees_examen(journal: list[dict]) -> list[dict]:
    """Les entrées de journal qui sont des résultats d'examen.

    Une révision faite pendant l'examen porte `carte` et `note` : c'est
    une révision, pas un résultat, et elle est écartée ici.
    """
    retenues = []
    for e in journal:
        if e.get("mode") != "examen" or e.get("carte") is not None:
            continue
        if not isinstance(e.get("region"), str):
            continue
        if not isinstance(e.get("score"), (int, float)) or isinstance(e.get("score"), bool):
            continue
        retenues.append(e)
    return retenues


def examens_reussis(journal: list[dict], config: dict) -> set[str]:
    """Les régions dont le boss est tombé au moins une fois."""
    seuil = reglages(config)["examen_score_reussite"]
    return {e["region"] for e in entrees_examen(journal) if e["score"] >= seuil}


def compose_examen(cartes: list[dict], region: str, config: dict,
                   graine: int | None = None) -> list[dict]:
    """Le tirage du boss : `examen_nb_cartes` cartes à froid de la région.

    À froid : sans regarder ce qui est dû, sans épargner ce qui vient
    d'être vu — c'est une épreuve, pas une séance. Déterministe à graine
    fixée (même geste que `seance.entrelace`), pour qu'un examen puisse
    se rejouer à l'identique. Une région qui n'a pas assez de cartes rend
    ce qu'elle a, sans erreur : l'écran dira que le boss n'est pas prêt.
    """
    nb = reglages(config)["examen_nb_cartes"]
    pool = sorted(cartes_region(cartes, region), key=lambda c: str(c.get("id")))
    rng = random.Random(graine)
    rng.shuffle(pool)
    return pool[:nb]


# --- l'XP (habillage) -------------------------------------------------

def xp_affichee(journal: list[dict], remplissages: dict[str, float] | None = None,
                config: dict | None = None) -> int:
    """L'XP montrée au joueur. Dérivée, jamais stockée.

    Formule, volontairement lisible et sans mémoire :

        XP = xp_par_revue  × révisions réussies (note >= 2)
           + xp_par_region × somme des remplissages affichés
           + xp_par_examen × examens réussis

    Fonction pure de ses arguments : deux appels sur le même journal
    rendent le même nombre. Rien à réconcilier, rien à sauvegarder — si
    le fichier d'XP n'existe pas, c'est qu'il ne doit pas exister.
    """
    bloc = (config or {}).get("progression", {}) if config else {}
    par_revue = bloc.get("xp_par_revue", XP_PAR_REVUE)
    par_region = bloc.get("xp_par_region", XP_PAR_REGION)
    par_examen = bloc.get("xp_par_examen", XP_PAR_EXAMEN)

    reussies = sum(1 for e in journal
                   if e.get("carte") and e.get("note") in (2, 3, 4))
    somme = sum((remplissages or {}).values())
    boss = len(examens_reussis(journal, config)) if config else 0
    return int(round(par_revue * reussies + par_region * somme + par_examen * boss))


# --- la carte complète ------------------------------------------------

def carte_monde(cartes: list[dict], journal: list[dict], config: dict,
                regions_ouvertes: list[str] | tuple[str, ...] = (),
                sched: Planificateur | None = None) -> dict:
    """L'état complet de la carte-monde d'un profil, JSON-sérialisable.

    `regions_ouvertes` : les régions débloquées autrement que par le
    remplissage (le quiz de positionnement, aujourd'hui). Ce module ne
    lit pas le quiz, il reçoit sa conclusion.

    L'état FSRS n'est pas recalculé ici : c'est `seance.etats_cartes` qui
    rejoue le journal, une seule implémentation pour tout le moteur.
    """
    r = reglages(config)
    if sched is None:
        retention = config.get("fsrs", {}).get("retention_souhaitee", RETENTION_DEFAUT)
        sched = Planificateur(retention=retention)
    etats = etats_cartes(journal, sched)
    forcees = set(regions_ouvertes or ())
    reussis = examens_reussis(journal, config)
    exige_examen = bool(r["examen_obligatoire_pour_100"])

    regions, remplissages = [], {}
    precedent_atteint = True          # la région 1 est toujours ouverte
    for rang, (cle, meta) in enumerate(regions_ordonnees(config), 1):
        jouables = cartes_region(cartes, cle)
        brut = remplissage_brut(cartes, etats, cle, config)
        boss = cle in reussis
        affiche = plafonne(brut, boss, config)
        par_quiz = cle in forcees
        ouverte = rang == 1 or precedent_atteint or par_quiz
        if rang == 1:
            ouverte_par = "premiere"
        elif precedent_atteint:
            ouverte_par = "seuil"
        elif par_quiz:
            ouverte_par = "quiz"
        else:
            ouverte_par = None

        regions.append({
            "cle": cle,
            "titre": meta.get("titre", cle),
            "rang": rang,
            "remplissage": round(affiche, 4),
            "remplissage_mesure": round(brut, 4),
            "cartes_totales": len(jouables),
            "cartes_acquises": sum(
                1 for c in jouables
                if (etats.get(c.get("id")) or {}).get("stabilite", 0.0)
                >= r["seuil_stabilite_acquise_jours"]),
            "ouverte": ouverte,
            "ouverte_par": ouverte_par,
            # Le moteur n'interdit rien : une région fermée se joue,
            # l'échec y est sans pénalité. « Fermée » = brouillard.
            "explorable": True,
            "statut": "ouverte" if ouverte else "explorable",
            "examen_requis": exige_examen,
            "examen_reussi": boss,
            "plafonnee_faute_d_examen": exige_examen and not boss
                                        and brut > PLAFOND_SANS_EXAMEN,
            "conquise": affiche >= 1.0,
        })
        remplissages[cle] = affiche
        precedent_atteint = brut >= r["seuil_ouverture_region"]

    hors = []
    for cle, meta in regions_hors_carte(config):
        jouables = cartes_region(cartes, cle)
        hors.append({
            "cle": cle,
            "titre": meta.get("titre", cle),
            "remplissage": round(remplissage_brut(cartes, etats, cle, config), 4),
            "cartes_totales": len(jouables),
            # Hors carte-monde : ni rang d'ouverture, ni examen, ni
            # entrée dans le remplissage global. Toujours jouable.
            "ouverte": True,
            "explorable": True,
            "statut": "hors_carte",
        })

    global_ = (sum(remplissages.values()) / len(remplissages)) if remplissages else 0.0
    return {
        "seuil_stabilite_jours": r["seuil_stabilite_acquise_jours"],
        "seuil_ouverture": r["seuil_ouverture_region"],
        "examen_nb_cartes": r["examen_nb_cartes"],
        "examen_score_reussite": r["examen_score_reussite"],
        "regions": regions,
        "hors_carte": hors,
        "remplissage_global": round(global_, 4),
        "regions_ouvertes": [x["cle"] for x in regions if x["ouverte"]],
        "regions_conquises": [x["cle"] for x in regions if x["conquise"]],
        "xp": xp_affichee(journal, remplissages, config),
    }


def main() -> int:
    from valide_banque import charge_banque, charge_config  # noqa: PLC0415

    ap = argparse.ArgumentParser(description="La carte-monde du profil.")
    ap.add_argument("--profil")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--sortie", type=Path)
    args = ap.parse_args()

    config = charge_config()
    profil = args.profil or config.get("profil_defaut", "jb")
    paires, erreurs = charge_banque()
    if erreurs:
        print(f"banque illisible ({len(erreurs)} erreur(s)) : "
              f"python3 app/valide_banque.py", file=sys.stderr)
        return 1
    monde = carte_monde([c for c, _ in paires], lit_journal(profil), config)

    if args.sortie:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        args.sortie.write_text(
            json.dumps(monde, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(monde, ensure_ascii=False, indent=2))
        return 0

    print(f"Carte-monde — profil {profil} — {monde['xp']} XP")
    print(f"  remplissage global {monde['remplissage_global']:.0%} "
          f"(acquis = stabilité ≥ {monde['seuil_stabilite_jours']} j)")
    for region in monde["regions"]:
        marque = "▣" if region["ouverte"] else "░"
        boss = " ⚑ boss tombé" if region["examen_reussi"] else (
            " (plafond 99 %, boss à faire)" if region["plafonnee_faute_d_examen"] else "")
        print(f"  {marque} {region['titre']:<38} {region['remplissage']:6.0%}"
              f"  {region['cartes_acquises']}/{region['cartes_totales']}{boss}")
    for region in monde["hors_carte"]:
        print(f"  · {region['titre']:<38} {region['remplissage']:6.0%}"
              f"  (hors carte-monde)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

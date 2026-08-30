#!/usr/bin/env python3
"""Vecteurs de conformité du miroir FSRS côté client.

Le front joue la séance dans le navigateur : il lui faut le moteur FSRS
en JavaScript (`un futur miroir JavaScript testé`). Deux moteurs pour
une seule vérité, c'est une divergence qui arrive — silencieusement, et
sur la seule donnée que personne ne peut recalculer après coup (l'état de
mémoire du joueur).

Ce module est le juge. Il déroule le VRAI planificateur Python sur une
trentaine de séquences variées et écrit ce qu'il obtient. Le script
`le test de conformité du client` rejoue exactement les mêmes
séquences dans le miroir JS et exige la conformité à 1e-4. Le miroir n'a
donc jamais à être cru sur parole : il est mesuré.

Le rejeu reproduit `seance.etats_cartes` et pas seulement les formules :
première rencontre, révisions avec délai, reprise le jour même
(`jours = 0`), et le champ optionnel `stabilite_forcee` du quiz de
positionnement — c'est cette dernière règle qui, oubliée côté client,
ferait revenir dans deux jours ce qui devait revenir dans trois semaines.

    python3 app/vecteurs_fsrs.py            # écrit le JSON
    python3 app/vecteurs_fsrs.py --json     # l'affiche

Sortie : `site/vecteurs-fsrs.json`. Généré, jamais édité à
la main : c'est le Python qui a raison, par construction.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import (  # noqa: E402
    BIEN, DUR, FACILE, PARAMS_DEFAUT, RATE, Planificateur)

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "site" / "vecteurs-fsrs.json"

# Les délais auxquels on interroge la récupérabilité à chaque étape.
# 0 inclus : R(0) doit valoir 1, c'est le cas limite qu'un portage rate.
JOURS_R = (0, 1, 3, 7, 21, 60, 365)

# Séquences écrites à la main : les cas dont on sait qu'ils cassent un
# portage. (note, jours écoulés, stabilité forcée ou None).
MANUELLES = [
    ("nominal", 0.9, [(BIEN, 0, None), (BIEN, 3, None), (BIEN, 8, None),
                      (BIEN, 21, None), (BIEN, 55, None)]),
    ("deux oublis", 0.9, [(RATE, 0, None), (BIEN, 1, None), (RATE, 4, None),
                          (BIEN, 2, None), (BIEN, 6, None)]),
    ("facile puis dur", 0.9, [(FACILE, 0, None), (FACILE, 15, None),
                              (DUR, 40, None)]),
    ("depart difficile", 0.9, [(DUR, 0, None), (DUR, 2, None), (BIEN, 5, None),
                               (FACILE, 12, None)]),
    ("tout le meme jour", 0.9, [(BIEN, 0, None), (BIEN, 0, None), (BIEN, 0, None)]),
    ("oubli apres un an", 0.9, [(BIEN, 0, None), (RATE, 365, None)]),
    ("rate en boucle", 0.9, [(RATE, 0, None), (RATE, 1, None), (RATE, 1, None),
                             (RATE, 1, None), (BIEN, 1, None)]),
    ("difficulte au plafond", 0.9, [(RATE, 0, None)] * 8),
    ("difficulte au plancher", 0.9, [(FACILE, 0, None)] + [(FACILE, 30, None)] * 6),
    ("reprise le jour meme apres rate", 0.9,
     [(BIEN, 0, None), (RATE, 10, None), (BIEN, 0, None), (BIEN, 0, None)]),
    ("retention basse", 0.8, [(BIEN, 0, None), (BIEN, 4, None), (BIEN, 12, None),
                              (DUR, 30, None)]),
    ("retention haute", 0.95, [(BIEN, 0, None), (BIEN, 2, None), (BIEN, 5, None),
                               (FACILE, 11, None)]),
    ("retention plancher", 0.7, [(BIEN, 0, None), (BIEN, 10, None), (RATE, 40, None)]),
    ("retention plafond", 0.99, [(BIEN, 0, None), (BIEN, 1, None), (BIEN, 2, None)]),
    # Le quiz de positionnement : la stabilité forcée écrase celle du
    # moteur, la difficulté reste celle du moteur (seance.etats_cartes).
    ("quiz puis revisions", 0.9,
     [(BIEN, 0, 21.0), (BIEN, 21, None), (BIEN, 50, None)]),
    ("quiz puis rate", 0.9, [(BIEN, 0, 21.0), (RATE, 21, None), (BIEN, 1, None)]),
    ("quiz seul", 0.9, [(BIEN, 0, 21.0)]),
    ("forcee au milieu", 0.9,
     [(BIEN, 0, None), (BIEN, 3, None), (BIEN, 8, 45.0), (DUR, 45, None)]),
    ("forcee nulle ignoree", 0.9, [(BIEN, 0, 0.0), (BIEN, 2, None)]),
    ("forcee minuscule", 0.9, [(BIEN, 0, 0.0005), (BIEN, 1, None)]),
    ("delai negatif borne a zero", 0.9,
     [(BIEN, 0, None), (BIEN, -3, None), (BIEN, 4, None)]),
    ("tres longue serie facile", 0.9,
     [(FACILE, 0, None)] + [(FACILE, 200, None) for _ in range(5)]),
    ("alternance dur bien", 0.9,
     [(DUR, 0, None), (BIEN, 2, None), (DUR, 4, None), (BIEN, 9, None),
      (DUR, 15, None), (BIEN, 25, None)]),
    ("un seul rate", 0.9, [(RATE, 0, None)]),
    ("un seul facile", 0.9, [(FACILE, 0, None)]),
]

# Combien de séquences tirées au sort s'ajoutent aux manuelles.
NB_ALEATOIRES = 12
GRAINE = 20260829            # date du GO de JB : reproductible, et daté


def sequences_aleatoires(nb: int, graine: int) -> list[tuple]:
    """Des séquences tirées au sort, mais toujours les mêmes.

    Le hasard sert à balayer des combinaisons que personne n'écrirait à
    la main ; la graine fixe sert à ce qu'un échec soit rejouable.
    """
    rng = random.Random(graine)
    sorties = []
    for i in range(nb):
        retention = rng.choice([0.8, 0.85, 0.9, 0.92, 0.95])
        etapes = []
        for j in range(rng.randint(2, 9)):
            note = rng.choice([RATE, DUR, BIEN, FACILE])
            jours = 0 if j == 0 else rng.choice([0, 0, 1, 2, 5, 9, 17, 30, 90, 400])
            forcee = round(rng.uniform(1.0, 60.0), 3) if rng.random() < 0.15 else None
            etapes.append((note, jours, forcee))
        sorties.append((f"aleatoire-{i + 1:02d}", retention, etapes))
    return sorties


def joue(sequence: list[tuple], sched: Planificateur) -> list[dict]:
    """Déroule une séquence EXACTEMENT comme `seance.etats_cartes`.

    Une divergence de rejeu (l'ordre des opérations, la stabilité forcée
    appliquée avant plutôt qu'après le clamp) fausserait la comparaison
    sans faire échouer un seul test de formule : c'est pourquoi le rejeu
    est ici et pas seulement les appels nus au planificateur.
    """
    etapes, s, d = [], None, None
    for note, jours, forcee in sequence:
        if s is None:
            s, d = sched.premiere(note)
        else:
            s, d = sched.revise(s, d, note, max(0, jours))
        if forcee is not None:
            try:
                valeur = float(forcee)
            except (TypeError, ValueError):
                valeur = 0.0
            if valeur > 0:
                s = valeur
        etapes.append({
            "note": note,
            "jours": jours,
            "stabilite_forcee": forcee,
            "attendu": {
                "stabilite": s,
                "difficulte": d,
                "intervalle": sched.intervalle(s),
                "recuperabilite": {str(j): sched.recuperabilite(s, j)
                                   for j in JOURS_R},
            },
        })
    return etapes


def construit() -> dict:
    vecteurs = []
    for nom, retention, sequence in MANUELLES + sequences_aleatoires(
            NB_ALEATOIRES, GRAINE):
        sched = Planificateur(retention=retention)
        vecteurs.append({"nom": nom, "retention": retention,
                         "etapes": joue(sequence, sched)})
    return {
        "_": ("Généré par app/vecteurs_fsrs.py depuis le VRAI "
              "planificateur Python. Ne pas éditer à la main : ce fichier "
              "est le juge du miroir JS, pas sa copie de complaisance. "
              "Rejeu : node le test de conformité du client"),
        "genere_le": date.today().isoformat(),
        "graine": GRAINE,
        "tolerance": 1e-4,
        "params": list(PARAMS_DEFAUT),
        "jours_recuperabilite": list(JOURS_R),
        "sequences": vecteurs,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Vecteurs FSRS pour le miroir JS.")
    ap.add_argument("--sortie", type=Path, default=SORTIE)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    charge = construit()
    texte = json.dumps(charge, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        print(texte)
        return 0
    args.sortie.parent.mkdir(parents=True, exist_ok=True)
    args.sortie.write_text(texte, encoding="utf-8")
    etapes = sum(len(s["etapes"]) for s in charge["sequences"])
    try:
        ou = args.sortie.resolve().relative_to(RACINE)
    except ValueError:
        ou = args.sortie
    print(f"{len(charge['sequences'])} séquence(s), {etapes} étape(s) → {ou}")
    print(f"  tolérance exigée du miroir JS : {charge['tolerance']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

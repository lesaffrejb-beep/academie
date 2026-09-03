#!/usr/bin/env python3
"""Vecteurs de conformité de l'arbre côté client.

`app/progression.py` et `web/src/moteur/progression.ts` calculent les
mêmes états de nœud à partir du même journal. Deux implémentations pour
une seule vérité : la divergence arrive, silencieusement, et elle se
voit dans ce que le joueur croit avoir acquis.

Ce module est le juge, sur le modèle de `app/vecteurs_fsrs.py` : il
déroule le VRAI code Python sur dix scènes choisies et écrit ce qu'il
obtient. `web/src/moteur/parite-arbre.test.ts` rejoue exactement les
mêmes scènes dans le miroir TypeScript et exige l'égalité stricte des
états, des remplissages arrondis et des drapeaux de fraîcheur.

Les dix scènes couvrent ce que `decisions/0028` a tranché :

  1. nœud sans carte                     → inconnu
  2. nœud servi, jamais joué             → ouvert
  3. nœud joué sous le seuil             → en-cours
  4. nœud au seuil de 75 %               → solide
  5. nœud joué + épreuve réussie         → valide
  6. nœud périmé, jamais validé          → a-revoir
  7. nœud validé et périmé               → valide, a_revoir vrai
  8. nœud mûr revu il y a longtemps      → pas de marque (FSRS a le dernier mot)
  9. cartes ajoutées à un nœud validé    → toujours valide, remplissage en baisse
 10. branches : la suivante s'ouvre à 75 %

    python3 app/vecteurs_progression.py            # écrit le JSON
    python3 app/vecteurs_progression.py --json     # l'affiche

Sortie : `site/vecteurs-progression.json`. Généré, jamais édité à la
main : c'est le Python qui a raison, par construction.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import BIEN, FACILE  # noqa: E402
from progression import carte_monde  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "site" / "vecteurs-progression.json"

# Un jour fixe : sans lui, les vecteurs changeraient tous les matins et
# le test de parité serait un test du calendrier.
AUJ = date(2026, 8, 28)

CONFIG = {
    "domaines": {
        "r1": {"titre": "Région une", "ordre": 1},
        "r2": {"titre": "Région deux", "ordre": 2},
    },
    "fsrs": {"retention_souhaitee": 0.9},
    "progression": {
        "seuil_stabilite_acquise_jours": 21,
        "seuil_ouverture_region": 0.75,
        "seuil_fraicheur_jours": 21,
        "examen_obligatoire_pour_100": True,
        "examen_nb_cartes": 12,
        "examen_score_reussite": 0.8,
    },
}

PROGRAMME = {
    "branches": {
        "r1": [{"cle": "b1", "titre": "Branche une", "ordre": 1},
               {"cle": "b2", "titre": "Branche deux", "ordre": 2}],
    },
    "chapitres": [
        {"id": "r1.b1.n1", "domaine": "r1", "branche": "b1", "titre": "Nœud un",
         "niveau": 1, "prerequis": []},
        {"id": "r1.b1.n2", "domaine": "r1", "branche": "b1", "titre": "Nœud deux",
         "niveau": 2, "prerequis": ["r1.b1.n1"]},
        {"id": "r1.b2.n3", "domaine": "r1", "branche": "b2", "titre": "Nœud trois",
         "niveau": 1, "prerequis": []},
    ],
}


def carte(cid: str, chapitre: str | None = None, domaine: str = "r1") -> dict:
    c = {"id": cid, "domaine": domaine, "branche": "b", "type": "flash",
         "question": f"question {cid}", "reponse": "r",
         "source": [{"texte": "s"}], "verifie": "2026-08-28",
         "statut": "valide", "partage": "banque"}
    if chapitre:
        c["chapitre"] = chapitre
    return c


def revue(cid: str, note: int, il_y_a: int) -> dict:
    jour = AUJ - timedelta(days=il_y_a)
    return {"quand": f"{jour.isoformat()}T07:00:00+00:00", "carte": cid,
            "note": note, "mode": "revision", "format": "seance"}


def examen(region: str, score: float, il_y_a: int = 0) -> dict:
    jour = AUJ - timedelta(days=il_y_a)
    return {"quand": f"{jour.isoformat()}T07:30:00+00:00", "mode": "examen",
            "region": region, "score": score, "cartes": []}


def mur(cid: str) -> list[dict]:
    """Deux « facile » espacés d'un mois : stabilité de plusieurs mois."""
    return [revue(cid, FACILE, 60), revue(cid, FACILE, 30)]


QUATRE = [carte(f"a{i}", "r1.b1.n1") for i in range(1, 5)]

SCENES: list[tuple[str, list[dict], list[dict]]] = [
    ("noeud-sans-carte", [], []),
    ("noeud-servi-jamais-joue", QUATRE, []),
    ("noeud-sous-le-seuil", QUATRE, mur("a1")),
    ("noeud-au-seuil", QUATRE, mur("a1") + mur("a2") + mur("a3")),
    ("noeud-valide-par-l-epreuve", QUATRE, mur("a1") + [examen("r1", 0.9)]),
    ("noeud-perime-jamais-valide", [carte("a1", "r1.b1.n1")],
     [revue("a1", BIEN, 47)]),
    ("noeud-valide-et-perime", [carte("a1", "r1.b1.n1")],
     [revue("a1", BIEN, 47), examen("r1", 0.9)]),
    ("noeud-mur-revu-il-y-a-30-jours", [carte("a1", "r1.b1.n1")], mur("a1")),
    ("cartes-ajoutees-a-un-noeud-valide",
     [carte("a1", "r1.b1.n1")] + [carte(f"neuf{i}", "r1.b1.n1") for i in range(6)],
     mur("a1") + [examen("r1", 0.9)]),
    ("branche-suivante-a-75",
     QUATRE + [carte("c1", "r1.b2.n3")],
     mur("a1") + mur("a2") + mur("a3")),
]

# Ce qu'on compare. Volontairement court : ce sont les promesses de
# `decisions/0028`, pas la forme interne du dictionnaire.
CHAMPS_NOEUD = ("id", "etat", "remplissage", "cartes_totales", "cartes_acquises",
                "a_revoir", "jours_depuis_derniere_revue", "prerequis_satisfaits",
                "jouable")
CHAMPS_BRANCHE = ("domaine", "cle", "remplissage", "ouverte", "noeuds",
                  "noeuds_servis", "noeuds_valides")


def vecteurs() -> dict:
    scenes = []
    for nom, cartes, journal in SCENES:
        monde = carte_monde(cartes, journal, CONFIG,
                            programme=PROGRAMME, aujourdhui=AUJ)
        scenes.append({
            "nom": nom,
            "cartes": cartes,
            "journal": journal,
            "attendu": {
                "noeuds": [{c: n[c] for c in CHAMPS_NOEUD} for n in monde["noeuds"]],
                "branches": [{c: b[c] for c in CHAMPS_BRANCHE}
                             for b in monde["branches"]],
                "cartes_sans_chapitre": monde["cartes_sans_chapitre"],
            },
        })
    return {
        "_": ("Généré par app/vecteurs_progression.py — ne pas éditer. "
              "Le Python fait foi ; web/src/moteur/progression.ts doit "
              "rendre exactement ces états (ACA-ARBRE-1, decisions/0028)."),
        "aujourdhui": AUJ.isoformat(),
        "config": CONFIG,
        "programme": PROGRAMME,
        "scenes": scenes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Vecteurs de parité de l'arbre.")
    ap.add_argument("--json", action="store_true", help="afficher au lieu d'écrire")
    args = ap.parse_args()

    data = vecteurs()
    texte = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        sys.stdout.write(texte)
        return 0
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(texte, encoding="utf-8")
    etats = sorted({n["etat"] for s in data["scenes"] for n in s["attendu"]["noeuds"]})
    print(f"{len(data['scenes'])} scène(s) → {SORTIE.relative_to(RACINE)}")
    print(f"  états couverts : {', '.join(etats)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

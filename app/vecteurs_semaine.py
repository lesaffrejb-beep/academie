#!/usr/bin/env python3
"""Vecteurs de conformité de la semaine type côté client.

`app/seance.py` et `web/src/moteur/composeur.ts` doivent prendre les
mêmes décisions sur **ce qui n'est pas tiré au sort** : la couleur du
jour, le nombre de cartes neuves autorisé, et la branche du socle à
protéger.

Le tirage lui-même n'est pas comparable, et c'est assumé depuis le
premier jour (`composeur.ts` en tête de fichier) : Python tire avec
Mersenne Twister, le client avec un mulberry32. Comparer l'ordre de la
séance ferait un test du générateur, pas du produit. Ce qui compte, et
ce que ce module fige, ce sont les **règles**.

  1. sept jours, sept couleurs                → couleur_du_jour
  2. lundi chargé                             → zéro neuf
  3. lundi calme                              → du neuf
  4. dimanche                                 → zéro neuf
  5. mardi (cours)                            → le maximum
  6. plafond du jour atteint                  → zéro neuf
  7. plafond du jour presque atteint          → ce qui reste
  8. branche du socle la moins avancée        → nommée
  9. socle tenu partout                       → aucune branche visée
 10. pas de programme                         → aucune branche visée

    python3 app/vecteurs_semaine.py            # écrit le JSON
    python3 app/vecteurs_semaine.py --json     # l'affiche

Sortie : `site/vecteurs-semaine.json`. Généré, jamais édité à la main.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import FACILE, Planificateur  # noqa: E402
from seance import (  # noqa: E402
    branche_socle_la_plus_faible, compose, couleur_du_jour, etats_cartes,
    quota_de_neuf)

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "site" / "vecteurs-semaine.json"

LUNDI = date(2026, 8, 31)

CONFIG = {
    "quotas": {"revisions_par_seance": 10, "nouveau_par_seance": 1,
               "plafond_reprise": 20, "nouveau_par_seance_max": 3,
               "nouveau_par_jour": 20, "ponderation_socle": 0.5,
               "rappels_d_ailleurs_max": 2, "fondations_dues_sans_neuf": 15},
    "fsrs": {"retention_souhaitee": 0.9},
    "semaine_type": {"lundi": "fondations", "mardi": "cours", "mercredi": "terrain",
                     "jeudi": "cours", "vendredi": "exploration",
                     "samedi": "etude", "dimanche": "libre"},
    "socle": {"niveaux": {"droit": 3, "compta": 2}},
    "domaines": {"droit": {"titre": "Droit", "ordre": 1},
                 "compta": {"titre": "Compta", "ordre": 2}},
    "progression": {"seuil_stabilite_acquise_jours": 21,
                    "seuil_ouverture_region": 0.75,
                    "seuil_fraicheur_jours": 21,
                    "examen_obligatoire_pour_100": True,
                    "examen_nb_cartes": 12, "examen_score_reussite": 0.8},
}

PROGRAMME = {
    "branches": {"droit": [{"cle": "b1", "ordre": 1}, {"cle": "b2", "ordre": 2}],
                 "compta": [{"cle": "c1", "ordre": 1}]},
    "chapitres": [
        {"id": "droit.b1.n1", "domaine": "droit", "branche": "b1",
         "niveau": 1, "prerequis": []},
        {"id": "droit.b2.n2", "domaine": "droit", "branche": "b2",
         "niveau": 1, "prerequis": []},
        {"id": "compta.c1.n3", "domaine": "compta", "branche": "c1",
         "niveau": 1, "prerequis": []},
    ],
}


def carte(cid: str, chapitre: str, domaine: str = "droit") -> dict:
    return {"id": cid, "domaine": domaine, "branche": "b", "type": "flash",
            "question": f"question {cid}", "reponse": "r", "chapitre": chapitre,
            "source": [{"texte": "s"}], "verifie": "2026-08-28",
            "statut": "valide", "partage": "banque"}


def mur(cid: str, jour: date) -> list[dict]:
    return [{"quand": f"{(jour - timedelta(days=d)).isoformat()}T07:00:00+00:00",
             "carte": cid, "note": FACILE, "mode": "revision", "format": "seance"}
            for d in (60, 30)]


# (nom, couleur attendue via la date, dues, déjà introduites aujourd'hui)
SCENES_QUOTA = [
    ("lundi-charge", LUNDI, 20, 0),
    ("lundi-calme", LUNDI, 3, 0),
    ("mardi-cours", LUNDI + timedelta(days=1), 5, 0),
    ("mercredi-terrain", LUNDI + timedelta(days=2), 5, 0),
    ("vendredi-exploration", LUNDI + timedelta(days=4), 5, 0),
    ("samedi-etude", LUNDI + timedelta(days=5), 5, 0),
    ("dimanche-libre", LUNDI + timedelta(days=6), 0, 0),
    ("plafond-du-jour-atteint", LUNDI + timedelta(days=1), 5, 20),
    ("plafond-du-jour-presque", LUNDI + timedelta(days=1), 5, 18),
    ("lundi-charge-au-seuil-exact", LUNDI, 15, 0),
]


def scenes_socle() -> list[dict]:
    """Trois scènes de branche : une faible nommée, une tenue, sans programme."""
    b1 = [carte(f"s{i}", "droit.b1.n1") for i in range(4)]
    b2 = [carte(f"f{i}", "droit.b2.n2") for i in range(4)]
    c1 = [carte(f"a{i}", "compta.c1.n3", "compta") for i in range(4)]
    # b1 et compta acquises, b2 vierge : b2 est la plus faible, sans
    # égalité à départager par l'alphabet.
    journal_b1 = ([e for i in range(4) for e in mur(f"s{i}", LUNDI)]
                  + [e for i in range(4) for e in mur(f"a{i}", LUNDI)])
    journal_tout = journal_b1 + [e for i in range(4) for e in mur(f"f{i}", LUNDI)]
    sched = Planificateur(retention=0.9)

    sorties = []
    for nom, cartes, journal, programme in (
        ("b2-est-la-plus-faible", b1 + b2 + c1, journal_b1, PROGRAMME),
        ("socle-tenu-partout", b1 + b2 + c1, journal_tout, PROGRAMME),
        ("sans-programme", b1 + b2 + c1, journal_b1, {}),
    ):
        etats = etats_cartes(journal, sched)
        sorties.append({
            "nom": nom,
            "cartes": cartes,
            "journal": journal,
            "programme": programme,
            "attendu": branche_socle_la_plus_faible(cartes, etats, CONFIG, programme),
        })
    return sorties


def scenes_composition() -> list[dict]:
    """La composition elle-même : ce que le client doit décider pareil.

    On compare les COMPTES et les décisions, jamais l'ordre : les deux
    générateurs pseudo-aléatoires diffèrent (`composeur.ts` en tête de
    fichier). Ces scènes ont manqué à la première livraison
    d'ACA-SEMAINE-1 : les règles étaient comparées une par une, leur
    emploi dans `compose()` ne l'était pas, et le client servait encore
    le quota brut. C'est un test de bout en bout des règles.
    """
    b1 = [carte(f"s{i}", "droit.b1.n1") for i in range(4)]
    b2 = [carte(f"f{i}", "droit.b2.n2") for i in range(6)]
    c1 = [carte(f"a{i}", "compta.c1.n3", "compta") for i in range(6)]
    toutes = b1 + b2 + c1
    sched = Planificateur(retention=0.9)

    # b1 acquise et échue depuis longtemps : elle fournit les révisions dues.
    vieux = [{"quand": f"{(LUNDI - timedelta(days=d)).isoformat()}T07:00:00+00:00",
              "carte": f"s{i}", "note": 1, "mode": "revision", "format": "seance"}
             for i in range(4) for d in (40, 39)]

    sorties = []
    for nom, jour, journal, cap in (
        ("mardi-cours-sans-cap", LUNDI + timedelta(days=1), [], None),
        ("mardi-cours-avec-cap-compta", LUNDI + timedelta(days=1), [], "compta"),
        ("dimanche-libre", LUNDI + timedelta(days=6), [], None),
        ("lundi-fondations-charge", LUNDI, vieux, None),
        ("mardi-avec-rappels-d-ailleurs", LUNDI + timedelta(days=1), vieux, "compta"),
    ):
        etats = etats_cartes(journal, sched)
        s = compose(toutes, etats, CONFIG, jour, sched, graine=7,
                    cap=cap, programme=PROGRAMME, journal=journal)
        sorties.append({
            "nom": nom,
            "date": jour.isoformat(),
            "cap": cap,
            "cartes": toutes,
            "journal": journal,
            "attendu": {
                "jour": s["jour"],
                "cap": s["cap"],
                "branche_socle": s["branche_socle"],
                "nb_revisions": len(s["revisions"]),
                "nb_nouveau": len(s["nouveau"]),
                "nb_rappels": len(s["rappels_d_ailleurs"]),
                "arriere_reetale": s["arriere_reetale"],
                "total_jouable": s["total_jouable"],
            },
        })
    return sorties


def vecteurs() -> dict:
    quotas = []
    for nom, jour, dues, deja in SCENES_QUOTA:
        couleur = couleur_du_jour(CONFIG, jour)
        quota, pourquoi = quota_de_neuf(CONFIG, couleur, dues, deja)
        quotas.append({
            "nom": nom, "date": jour.isoformat(), "dues": dues,
            "deja_du_jour": deja,
            "attendu": {"couleur": couleur, "quota": quota, "pourquoi": pourquoi},
        })
    return {
        "_": ("Généré par app/vecteurs_semaine.py — ne pas éditer. Le Python "
              "fait foi ; web/src/moteur/composeur.ts doit décider pareil "
              "(ACA-SEMAINE-1). Le tirage n'est pas comparé : les deux "
              "générateurs pseudo-aléatoires diffèrent, c'est assumé."),
        "config": CONFIG,
        "quotas": quotas,
        "socle": scenes_socle(),
        "composition": scenes_composition(),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Vecteurs de parité de la semaine type.")
    ap.add_argument("--json", action="store_true", help="afficher au lieu d'écrire")
    args = ap.parse_args()

    data = vecteurs()
    texte = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if args.json:
        sys.stdout.write(texte)
        return 0
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text(texte, encoding="utf-8")
    couleurs = sorted({q["attendu"]["couleur"] for q in data["quotas"]})
    print(f"{len(data['quotas'])} scène(s) de quota, {len(data['socle'])} de socle, "
          f"{len(data['composition'])} de composition → {SORTIE.relative_to(RACINE)}")
    print(f"  couleurs couvertes : {', '.join(couleurs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

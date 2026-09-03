#!/usr/bin/env python3
"""Tests du valideur des chapitres v2 (app/valide_chapitres.py).

Chaque test construit une racine jetable (programme + chapitres) et lance
le valideur dessus par `ACADEMIE_RACINE`, comme la chaîne réelle. Les
promesses protégées sont celles de CONTRAT-CARTE-V2.md et des décisions
0004, 0019, 0021, 0022 : provenance obligatoire, source ou aveu, aucun
chiffre sans source, niveaux cohérents avec le programme, relecture
avant `valide`, dérivés jamais écrits à la main.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

APP = Path(__file__).resolve().parent
VALIDEUR = APP / "valide_chapitres.py"

AUJOURDHUI = date.today().isoformat()
PROGRAMME = {
    "version": "test", "metier": "test", "genere_le": AUJOURDHUI,
    "socle": {"niveaux": {"droit": 2}},
    "semaine_type": {j: "cours" for j in ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")},
    "positionnement": {"questions_par_domaine": 2, "niveaux": [1, 2]},
    "domaines": {"droit": {"titre": "Droit", "ordre": 1}},
    "branches": {"droit": [{"cle": "majorites", "titre": "Majorités", "ordre": 1}]},
    "chapitres": [
        {"id": "droit.majorites.article-24", "domaine": "droit", "branche": "majorites",
         "titre": "L'article 24", "niveau": 1, "prerequis": [], "statut": "a-ecrire"},
        {"id": "droit.majorites.tableau", "domaine": "droit", "branche": "majorites",
         "titre": "Le tableau", "niveau": 3, "prerequis": ["droit.majorites.article-24"], "statut": "a-ecrire"},
    ],
}
PROVENANCE = {"auteur": "modele", "modele": "test-modele", "genere_le": AUJOURDHUI,
              "session": "tests", "sources_retrouvees": 1, "sources_concordantes": 1, "sans_source": False}
SOURCE_A = {"texte": "Art. 24, loi du 10 juillet 1965", "url": "https://www.legifrance.gouv.fr/", "nature": "texte-officiel"}
SOURCE_B = {"texte": "Fiche ANIL sur les majorités", "url": "https://www.anil.org/", "nature": "institution"}


def carte(**maj) -> dict:
    base = {
        "id": "droit-majorites-article-24-definition", "chapitre": "droit.majorites.article-24",
        "domaine": "droit", "branche": "majorites", "type": "flash", "niveau": 1,
        "question": "Quelle majorité l'article 24 exige-t-il ?",
        "reponse": "La majorité des voix exprimées des copropriétaires présents, représentés ou ayant voté par correspondance.",
        "explication": "Les abstentions ne sont pas des voix exprimées.",
        "source": [copy.deepcopy(SOURCE_A)], "provenance": copy.deepcopy(PROVENANCE),
        "verifie": AUJOURDHUI, "peremption": None, "statut": "brouillon", "partage": "banque",
    }
    base.update(maj)
    return base


def chapitre(**maj) -> dict:
    base = {
        "id": "droit.majorites.article-24", "titre": "L'article 24", "domaine": "droit",
        "branche": "majorites", "niveau": 1, "prerequis": [],
        "objectifs": ["Dire ce que vote l'article 24.", "Calculer une majorité simple."],
        "amorce": {"question": "Une résolution reçoit 250 pour, 200 contre, 150 abstentions. Adoptée ?",
                   "reponse_attendue": "Oui : les abstentions ne comptent pas."},
        "lecon": "x" * 1600,
        "synthese": {"consigne": "Explique l'article 24 en une phrase.",
                     "attendus": ["voix exprimées", "présents, représentés, correspondance", "abstentions exclues"]},
        "cartes": [carte()],
        "sources": [copy.deepcopy(SOURCE_A)], "provenance": copy.deepcopy(PROVENANCE),
        "statut": "brouillon", "partage": "banque", "verifie": AUJOURDHUI, "version": 1,
    }
    base.update(maj)
    return base


def lance(chapitres: list[dict], json_mode: bool = False) -> tuple[int, str]:
    racine = Path(tempfile.mkdtemp(prefix="academie-chapitres-"))
    (racine / "programme").mkdir()
    (racine / "programme" / "test.json").write_text(json.dumps(PROGRAMME), encoding="utf-8")
    dossier = racine / "chapitres" / "droit" / "majorites"
    dossier.mkdir(parents=True)
    for i, ch in enumerate(chapitres):
        (dossier / f"ch{i}.json").write_text(json.dumps(ch, ensure_ascii=False), encoding="utf-8")
    env = dict(os.environ, ACADEMIE_RACINE=str(racine))
    args = [sys.executable, str(VALIDEUR)] + (["--json"] if json_mode else [])
    res = subprocess.run(args, capture_output=True, text=True, env=env)
    return res.returncode, res.stdout + res.stderr


ECHECS: list[str] = []


def verifie(nom: str, condition: bool, detail: str = "") -> None:
    print(f"{'✓' if condition else '✗'} {nom}")
    if not condition:
        ECHECS.append(nom)
        if detail:
            print("\n".join("    " + l for l in detail.splitlines()[-6:]))


def main() -> int:
    code, sortie = lance([chapitre()])
    verifie("un chapitre conforme passe", code == 0, sortie)

    code, sortie = lance([chapitre(provenance=None)])
    verifie("un chapitre sans provenance est refusé", code == 1 and "`provenance` manquante" in sortie, sortie)

    c = carte(); del c["provenance"]
    code, sortie = lance([chapitre(cartes=[c])])
    verifie("une carte sans provenance est refusée", code == 1 and "`provenance` manquante" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(source=[])])])
    verifie("une carte sans source ni aveu est refusée", code == 1 and "sans_source" in sortie, sortie)

    prov = dict(PROVENANCE, sans_source=True, sources_retrouvees=0)
    code, sortie = lance([chapitre(cartes=[carte(source=[], provenance=prov,
                                                 question="Que fait l'article 24 ?",
                                                 reponse="Il fixe la majorité des voix exprimées.",
                                                 explication="Rien de chiffré.")])])
    verifie("une carte sans source avouée, sans chiffre, passe", code == 0, sortie)

    code, sortie = lance([chapitre(cartes=[carte(source=[], provenance=prov,
                                                 reponse="Un délai de 21 jours s'applique.")])])
    verifie("une carte sans source qui porte un chiffre est refusée", code == 1 and "chiffre" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(source=[dict(SOURCE_A, nature=None)])])])
    verifie("une source sans nature est refusée", code == 1 and "nature" in sortie, sortie)

    code, sortie = lance([chapitre(id="droit.majorites.inconnu", cartes=[carte(chapitre="droit.majorites.inconnu")])])
    verifie("un chapitre absent du programme est refusé", code == 1 and "absent du programme" in sortie, sortie)

    code, sortie = lance([chapitre(niveau=2, cartes=[carte()])])
    verifie("un niveau différent du programme est refusé", code == 1 and "diffère du programme" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(niveau=3)])])
    verifie("une carte au-dessus du niveau du chapitre est refusée", code == 1 and "au-dessus" in sortie, sortie)

    code, sortie = lance([chapitre(id="droit.majorites.tableau", niveau=3, prerequis=["droit.majorites.article-24"],
                                   cartes=[carte(chapitre="droit.majorites.tableau", niveau=3)]),
                          chapitre(prerequis=["droit.majorites.tableau"])])
    verifie("un prérequis de niveau supérieur est refusé", code == 1 and "niveau supérieur" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(statut="valide")])])
    verifie("une carte valide sans relecture est refusée", code == 1 and "verifie_par" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(statut="valide", verifie_par="agent frais, tests")])])
    verifie("une carte valide relue passe", code == 0, sortie)

    vieux = (date.today() - timedelta(days=400)).isoformat()
    code, sortie = lance([chapitre(cartes=[carte(statut="valide", verifie_par="x", verifie=vieux)])])
    verifie("une carte juridique validée il y a plus d'un an est refusée", code == 1 and "douze mois" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(a_recouper=False)])])
    verifie("un dérivé écrit à la main est refusé", code == 1 and "dérivé" in sortie, sortie)

    qcm = carte(id="droit-majorites-article-24-qcm", type="qcm", choix=[
        {"texte": "Voix exprimées", "correct": True},
        {"texte": "Tous les copropriétaires", "correct": False, "pourquoi_faux": "C'est l'article 25."},
        {"texte": "Deux tiers", "correct": False},
    ])
    code, sortie = lance([chapitre(cartes=[qcm])])
    verifie("un QCM avec un distracteur non expliqué est refusé", code == 1 and "pourquoi_faux" in sortie, sortie)

    cas = carte(id="droit-majorites-cas", type="cas", pas=[{"situation": "s", "choix": ["a", "b"], "correct": 0, "pourquoi": "p"}])
    code, sortie = lance([chapitre(cartes=[cas])])
    verifie("un cas à un seul pas est refusé", code == 1 and "3 à 5 pas" in sortie, sortie)

    dessin = carte(id="droit-majorites-dessin", type="dessin", attendus=["a", "b"])
    code, sortie = lance([chapitre(cartes=[dessin])])
    verifie("un dessin avec deux attendus est refusé", code == 1 and "attendus" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(chrono=30)])])
    verifie("un chrono sur une carte flash est refusé", code == 1 and "chrono" in sortie, sortie)

    fuite = carte(reponse="Vu à la résidence OFF-LES-LILAS, immatriculée AA1234567.")
    code, sortie = lance([chapitre(cartes=[fuite])])
    verifie("un fait nominatif du parc en couche partagée est refusé", code == 1 and "anti-fuite" in sortie, sortie)

    code, sortie = lance([chapitre(cartes=[carte(), carte()])])
    verifie("un id de carte dupliqué est refusé", code == 1 and "dupliqué" in sortie, sortie)

    code, sortie = lance([chapitre(lecon="trop court")])
    verifie("une leçon trop courte est refusée", code == 1 and "leçon" in sortie, sortie)

    sat = chapitre(id="satellite.droit.chaudiere-hybride", satellite=True, rattachement_propose="droit.majorites.article-24",
                   cartes=[carte(chapitre="satellite.droit.chaudiere-hybride")])
    code, sortie = lance([sat])
    verifie("un satellite rattaché à un chapitre du programme passe", code == 0, sortie)
    sat2 = chapitre(id="satellite.droit.inconnu", satellite=True, rattachement_propose="droit.majorites.nulle-part",
                    cartes=[carte(chapitre="satellite.droit.inconnu")])
    code, sortie = lance([sat2])
    verifie("un satellite au rattachement inconnu est refusé", code == 1 and "rattachement_propose" in sortie, sortie)

    # Dérivation des notes (decisions/0022)
    deux = carte(statut="valide", verifie_par="agent frais", source=[copy.deepcopy(SOURCE_A), copy.deepcopy(SOURCE_B)])
    une = carte(id="droit-majorites-une", statut="valide", verifie_par="agent frais")
    sans = carte(id="droit-majorites-sans", source=[], provenance=prov, question="Que fait l'article 24 ?",
                 reponse="Il fixe la majorité des voix exprimées.", explication="Rien.")
    code, sortie = lance([chapitre(cartes=[deux, une, sans])], json_mode=True)
    notes = {}
    if code == 0:
        data = json.loads(sortie)
        notes = {c["id"]: (c["note_confiance"], c["a_recouper"]) for c in data["chapitres"][0]["cartes"]}
    verifie("deux sources solides, relue, fraîche : note A",
            notes.get("droit-majorites-article-24-definition") == ("A", False), sortie)
    verifie("une source solide, relue : note B", notes.get("droit-majorites-une") == ("B", False), sortie)
    verifie("sans source : note C et à recouper", notes.get("droit-majorites-sans") == ("C", True), sortie)

    if ECHECS:
        print(f"\n{len(ECHECS)} test(s) en échec : {', '.join(ECHECS)}")
        return 1
    print("\nchapitres v2 : tout vert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

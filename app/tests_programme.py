#!/usr/bin/env python3
"""Tests du valideur du programme (app/valide_programme.py), chantier
ACA-PROGRAMME-1.

Chaque test construit une racine jetable (programme + academie.json) et
lance le valideur dessus par `ACADEMIE_RACINE`. Les promesses protégées :
identifiants uniques, prérequis existants et de niveau inférieur ou égal,
aucun cycle, domaine et branche déclarés, clés de `academie.json` et du
programme identiques, socle dans 1-5, semaine type complète.
"""

from __future__ import annotations

import copy
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent
VALIDEUR = APP / "valide_programme.py"

JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
PROGRAMME = {
    "version": "test", "metier": "test", "genere_le": "2026-09-03",
    "niveaux": {"1": "Repères", "2": "Mécanismes", "3": "Praticien", "4": "Doctrine", "5": "Frontière"},
    "socle": {"niveaux": {"droit": 2}},
    "semaine_type": {j: "cours" for j in JOURS},
    "positionnement": {"questions_par_domaine": 2, "niveaux": [1, 2]},
    "domaines": {"droit": {"titre": "Droit", "ordre": 1, "niveau_socle": 2},
                 "culture": {"titre": "Culture", "ordre": 2, "niveau_socle": None, "arbre": False}},
    "branches": {"droit": [{"cle": "majorites", "titre": "Majorités", "ordre": 1}],
                 "culture": [{"cle": "textes", "titre": "Textes", "ordre": 1}]},
    "chapitres": [
        {"id": "droit.majorites.article-24", "domaine": "droit", "branche": "majorites",
         "titre": "L'article 24", "niveau": 1, "prerequis": [], "statut": "a-ecrire"},
        {"id": "droit.majorites.article-25", "domaine": "droit", "branche": "majorites",
         "titre": "L'article 25", "niveau": 1, "prerequis": [], "statut": "a-ecrire"},
        {"id": "droit.majorites.tableau", "domaine": "droit", "branche": "majorites",
         "titre": "Le tableau", "niveau": 2, "prerequis": ["droit.majorites.article-24"], "statut": "a-ecrire"},
        {"id": "culture.textes.propriete", "domaine": "culture", "branche": "textes",
         "titre": "La propriété", "niveau": 4, "prerequis": [], "statut": "a-ecrire"},
    ],
}
ACADEMIE = {"metier": "test", "domaines": {"droit": {"titre": "Droit", "ordre": 1},
                         "culture": {"titre": "Culture", "ordre": 2, "arbre": False}}}


def programme(**maj) -> dict:
    p = copy.deepcopy(PROGRAMME)
    p.update(maj)
    return p


def chapitres(*extra: dict, remplace: list | None = None) -> list[dict]:
    base = copy.deepcopy(PROGRAMME["chapitres"]) if remplace is None else remplace
    return base + list(extra)


def lance(prog: dict, academie: dict | None = None, json_mode: bool = False) -> tuple[int, str]:
    racine = Path(tempfile.mkdtemp(prefix="academie-programme-"))
    (racine / "programme").mkdir()
    (racine / "programme" / "test.json").write_text(json.dumps(prog, ensure_ascii=False), encoding="utf-8")
    (racine / "academie.json").write_text(json.dumps(academie if academie is not None else ACADEMIE), encoding="utf-8")
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
    code, sortie = lance(programme())
    verifie("un programme conforme passe", code == 0, sortie)

    code, sortie = lance(programme(chapitres=chapitres(copy.deepcopy(PROGRAMME["chapitres"][0]))))
    verifie("un identifiant dupliqué est refusé", code == 1 and "dupliqué" in sortie, sortie)

    ch = copy.deepcopy(PROGRAMME["chapitres"])
    ch[2]["prerequis"] = ["droit.majorites.nulle-part"]
    code, sortie = lance(programme(chapitres=ch))
    verifie("un prérequis inconnu est refusé", code == 1 and "prérequis inconnu" in sortie, sortie)

    ch = copy.deepcopy(PROGRAMME["chapitres"])
    ch[0]["prerequis"] = ["droit.majorites.tableau"]
    ch[2]["prerequis"] = []
    code, sortie = lance(programme(chapitres=ch))
    verifie("un prérequis de niveau supérieur est refusé", code == 1 and "niveau supérieur" in sortie, sortie)

    ch = copy.deepcopy(PROGRAMME["chapitres"])
    ch[0]["prerequis"] = ["droit.majorites.article-25"]
    ch[1]["prerequis"] = ["droit.majorites.article-24"]
    code, sortie = lance(programme(chapitres=ch))
    verifie("un cycle de prérequis est refusé", code == 1 and "cycle" in sortie, sortie)

    ch = copy.deepcopy(PROGRAMME["chapitres"])
    ch[0]["domaine"] = "fantome"
    code, sortie = lance(programme(chapitres=ch))
    verifie("un domaine non déclaré est refusé", code == 1 and "domaine non déclaré" in sortie, sortie)

    ch = copy.deepcopy(PROGRAMME["chapitres"])
    ch[0]["branche"] = "fantome"
    code, sortie = lance(programme(chapitres=ch))
    verifie("une branche non déclarée est refusée", code == 1 and "branche non déclarée" in sortie, sortie)

    ch = copy.deepcopy(PROGRAMME["chapitres"])
    ch[0]["niveau"] = 6
    code, sortie = lance(programme(chapitres=ch))
    verifie("un niveau hors 1-5 est refusé", code == 1 and "niveau" in sortie, sortie)

    aca = copy.deepcopy(ACADEMIE)
    aca["domaines"]["plans"] = {"titre": "Plans", "ordre": 3}
    code, sortie = lance(programme(), aca)
    verifie("une clé de academie.json absente du programme est refusée", code == 1 and "plans" in sortie, sortie)

    aca = copy.deepcopy(ACADEMIE)
    del aca["domaines"]["culture"]
    code, sortie = lance(programme(), aca)
    verifie("une clé du programme absente de academie.json est refusée", code == 1 and "culture" in sortie, sortie)

    aca = copy.deepcopy(ACADEMIE)
    aca["domaines"]["droit"]["ordre"] = 2
    aca["domaines"]["culture"]["ordre"] = 1
    code, sortie = lance(programme(), aca)
    verifie("un ordre de domaine différent est refusé", code == 1 and "ordre" in sortie, sortie)

    aca = copy.deepcopy(ACADEMIE)
    aca["domaines"]["culture"].pop("arbre")
    code, sortie = lance(programme(), aca)
    verifie("un domaine hors arbre remis dans l'arbre est refusé", code == 1 and "arbre" in sortie, sortie)

    code, sortie = lance(programme(socle={"niveaux": {"droit": 7}}))
    verifie("un socle hors 1-5 est refusé", code == 1 and "socle" in sortie, sortie)

    code, sortie = lance(programme(socle={"niveaux": {"fantome": 2}}))
    verifie("un socle sur un domaine inconnu est refusé", code == 1 and "socle" in sortie, sortie)

    sem = {j: "cours" for j in JOURS if j != "dimanche"}
    code, sortie = lance(programme(semaine_type=sem))
    verifie("une semaine type incomplète est refusée", code == 1 and "semaine" in sortie, sortie)

    code, sortie = lance(programme(), json_mode=True)
    ok = False
    if code == 0:
        data = json.loads(sortie)
        ok = data.get("chapitres") == 4 and data.get("par_niveau", {}).get("1") == 2
    verifie("la sortie --json compte les chapitres par niveau", ok, sortie)

    if ECHECS:
        print(f"\n{len(ECHECS)} test(s) en échec : {', '.join(ECHECS)}")
        return 1
    print("\nprogramme : tout vert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

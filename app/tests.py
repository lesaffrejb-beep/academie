#!/usr/bin/env python3
"""Tous les tests de l'Académie, en une commande.

    python3 app/tests.py
    python3 app/tests.py --mutation   # vérifie que les tests mordent

Sept étages, du plus bas au plus haut :

    planificateur  le moteur FSRS, comparé à py-fsrs
    seance         la composition du matin (dû, ré-étalement, entrelacement)
    progression    la carte-monde (régions, seuils, boss-examens, XP dérivée)
    quiz+erreurs   le positionnement et le carnet d'erreurs
    chaine         de la donnée brute à l'écran (cloisonnement, refus, contrat)
    chapitres      le valideur des chapitres v2 (contrat proposé, decisions 0021-0022)
    banque         la vraie banque respecte le contrat carte-v1, les vrais chapitres le v2

Le mode `--mutation` casse volontairement des garde-fous, un par un, et
vérifie que les tests le remarquent. Un test qui reste vert pendant que
le code est cassé est pire qu'absent : il donne confiance à tort. C'est
ce mode qui a trouvé, le 28/08/2026, que la vérification des champs
obligatoires n'était couverte par aucun cas.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent
RACINE = APP.parent

SUITES = [
    ("moteur FSRS", "tests_planificateur.py"),
    ("séance du jour", "tests_seance.py"),
    ("carte-monde", "tests_progression.py"),
    ("quiz + carnet d'erreurs", "tests_quiz_erreurs.py"),
    ("chaîne donnée → écran", "tests_chaine.py"),
    ("chapitres v2", "tests_chapitres.py"),
]

# (description, fichier, texte à remplacer, remplacement).
# Chaque mutation doit faire échouer au moins une suite.
MUTATIONS = [
    ("le scan anti-fuite est neutralisé", "valide_banque.py",
     'if carte["partage"] in PARTAGES_SCANNES:', "if False:"),
    ("les champs obligatoires ne sont plus vérifiés", "valide_banque.py",
     "    for champ in OBLIGATOIRES:", "    for champ in ():"),
    ("les QCM à plusieurs bonnes réponses passent", "valide_banque.py",
     "if len(justes) != 1:", "if False:"),
    ("les cartes périmées restent jouables", "valide_banque.py",
     'elif date.fromisoformat(str(per)) < aujourdhui and carte["statut"] == "valide":',
     "elif False:"),
    ("la production sert aussi les brouillons", "genere.py",
     'if carte["statut"] != "valide" and not args.avec_brouillons:',
     "if False:"),
    ("un raté n'est plus distingué d'une réussite", "planificateur.py",
     "if note == RATE:", "if False:"),
    ("le plafond d'examen saute, le 100 % se donne sans boss", "progression.py",
     "    return min(brut, PLAFOND_SANS_EXAMEN)", "    return brut"),
    ("une mauvaise réponse au quiz écrit quand même au journal", "quiz.py",
     '        if not res.get("juste") or not res.get("carte"):',
     '        if not res.get("carte"):'),
    ("un chapitre sans provenance passe", "valide_chapitres.py",
     "    if not isinstance(prov, dict):", "    if False:"),
    ("une carte sans source avouée peut porter un chiffre", "valide_chapitres.py",
     "    return bool(RE_CHIFFRE.search(RE_REFERENCES.sub(\" \", texte)))", "    return False"),
    ("une carte valide sans relecture passe", "valide_chapitres.py",
     '    if carte["statut"] == "valide" and _vide(carte.get("verifie_par")):', "    if False:"),
]


def lance(fichier: str) -> tuple[bool, str]:
    res = subprocess.run([sys.executable, str(APP / fichier)],
                         capture_output=True, text=True)
    return res.returncode == 0, res.stdout + res.stderr


def valide_vraie_banque() -> tuple[bool, str]:
    res = subprocess.run([sys.executable, str(APP / "valide_banque.py")],
                         capture_output=True, text=True)
    return res.returncode == 0, res.stdout + res.stderr


def valide_vrais_chapitres() -> tuple[bool, str]:
    res = subprocess.run([sys.executable, str(APP / "valide_chapitres.py")],
                         capture_output=True, text=True)
    return res.returncode == 0, res.stdout + res.stderr


def mode_normal() -> int:
    echecs = []
    for nom, fichier in SUITES:
        ok, sortie = lance(fichier)
        print(f"{'✓' if ok else '✗'} {nom}")
        if not ok:
            echecs.append(nom)
            print("\n".join("    " + l for l in sortie.splitlines()[-12:]))

    ok, sortie = valide_vraie_banque()
    resume = next((l for l in sortie.splitlines() if l.startswith("banque :")), "")
    print(f"{'✓' if ok else '✗'} banque réelle — {resume}")
    if not ok:
        echecs.append("banque réelle")
        print("\n".join("    " + l for l in sortie.splitlines()[-10:]))

    ok, sortie = valide_vrais_chapitres()
    resume = next((l for l in sortie.splitlines() if l.startswith("chapitres :")), "")
    print(f"{'✓' if ok else '✗'} chapitres réels — {resume}")
    if not ok:
        echecs.append("chapitres réels")
        print("\n".join("    " + l for l in sortie.splitlines()[-10:]))

    if echecs:
        print(f"\n{len(echecs)} suite(s) en échec : {', '.join(echecs)}")
        return 1
    print("\nTOUT VERT.")
    return 0


def mode_mutation() -> int:
    """Casse un garde-fou à la fois et vérifie qu'au moins un test le voit."""
    sauvegardes = {}
    tmp = Path(tempfile.mkdtemp(prefix="academie-mutation-"))
    survivantes = []
    try:
        for fichier in {m[1] for m in MUTATIONS}:
            sauvegardes[fichier] = tmp / fichier
            shutil.copy(APP / fichier, sauvegardes[fichier])

        for description, fichier, avant, apres in MUTATIONS:
            cible = APP / fichier
            source = cible.read_text(encoding="utf-8")
            if avant not in source:
                print(f"⚠ mutation obsolète ({fichier}) : « {avant[:45]}… » "
                      f"introuvable — le code a changé, la mutation est à mettre à jour")
                survivantes.append(description)
                continue
            cible.write_text(source.replace(avant, apres, 1), encoding="utf-8")
            try:
                vue_par = [nom for nom, f in SUITES if not lance(f)[0]]
            finally:
                shutil.copy(sauvegardes[fichier], cible)
            if vue_par:
                print(f"✓ détectée par {', '.join(vue_par)} — {description}")
            else:
                print(f"✗ SURVIT AUX TESTS — {description}")
                survivantes.append(description)
    finally:
        for fichier, sauvegarde in sauvegardes.items():
            shutil.copy(sauvegarde, APP / fichier)
        shutil.rmtree(tmp, ignore_errors=True)

    if survivantes:
        print(f"\n{len(survivantes)} mutation(s) non détectée(s) : un garde-fou "
              f"peut être cassé sans qu'aucun test ne le voie.")
        return 1
    print(f"\nVERT — les {len(MUTATIONS)} mutations sont toutes détectées.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Tests de l'Académie.")
    ap.add_argument("--mutation", action="store_true",
                    help="casser les garde-fous pour vérifier que les tests mordent")
    args = ap.parse_args()
    return mode_mutation() if args.mutation else mode_normal()


if __name__ == "__main__":
    sys.exit(main())

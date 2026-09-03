#!/usr/bin/env python3
"""Tous les tests de l'Académie, en une commande.

    python3 app/tests.py
    python3 app/tests.py --mutation   # vérifie que les tests mordent

Onze étages, du plus bas au plus haut :

    planificateur  le moteur FSRS, comparé à py-fsrs
    seance         la composition du matin (dû, ré-étalement, entrelacement)
    progression    la carte-monde (régions, seuils, boss-examens, XP dérivée)
    quiz+erreurs   le positionnement et le carnet d'erreurs
    chaine         de la donnée brute à l'écran (cloisonnement, refus, contrat)
    chapitres      le valideur des chapitres v2 (contrat proposé, decisions 0021-0022)
    usine          le pas à pas imposé sur un document réel (decisions 0026-0027)
    programme      le valideur du programme et son alignement (ACA-PROGRAMME-1)
    serveur        l'API d'état : union, idempotence, jetons (ACA-JOURNAL-SYNC-1)
    sources        le registre et la nature de chaque source (ACA-SOURCES-1)
    rituel         l'habitude mesurée depuis le journal (ACA-RITUAL-METRICS-1)
    export         l'export Anki, assurance-vie de réversibilité (ACA-EXPORT-1)
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
    ("usine pas à pas", "tests_usine.py"),
    ("programme", "tests_programme.py"),
    ("serveur d'état", "tests_serveur.py"),
    ("registre des sources", "tests_sources.py"),
    ("rituel", "tests_rituel.py"),
    ("export Anki", "tests_export.py"),
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
    ("l'usine ouvre l'unité suivante sans valider la précédente", "usine/etat.py",
     '        if u["statut"] in STATUTS_A_REPRENDRE:\n            journaliser(etat, "unité reprise"',
     '        if False:\n            journaliser(etat, "unité reprise"'),
    ("l'usine accepte un résumé à la place du texte", "usine/etat.py",
     '        if couverture < float(cfg["couverture_min"]):', "        if False:"),
    ("l'usine laisse passer un chiffre absent de la page", "usine/etat.py",
     "        absents = sorted(nombres(l) - connus)", "        absents = []"),
    ("le serveur remplace une ligne de journal au lieu de l'ignorer", "../serveur/academie_etat/journal.py",
     '"INSERT OR IGNORE INTO journal', '"INSERT OR REPLACE INTO journal'),
    ("le serveur accepte un lot de plus de 500 lignes", "../serveur/academie_etat/journal.py",
     "    if len(lignes) > LOT_MAX:", "    if False:"),
    ("le programme accepte un prérequis de niveau supérieur", "valide_programme.py",
     '            elif ids[pre].get("niveau", 0) > niv:', "            elif False:"),
    ("l'export Anki oublie la source de la carte", "export_anki.py",
     "    lignes = []\n    for s in (carte.get(\"source\") or []):",
     "    lignes = []\n    for s in []:"),
    ("l'export Anki perd les distracteurs d'un QCM", "export_anki.py",
     '    faux = [c for c in (carte.get("choix") or []) if not c.get("correct")]',
     "    faux = []"),
    ("la pondération du socle est neutralisée", "seance.py",
     "            neuves = du_socle[:vises] + autres + du_socle[vises:]",
     "            neuves = autres + du_socle"),
    ("un lundi chargé pousse quand même du neuf", "seance.py",
     "        if dues > seuil:", "        if False:"),
    ("un nœud validé retombe quand on lui ajoute des cartes", "progression.py",
     '    if joue and examen_reussi:\n        return "valide"',
     '    if False:\n        return "valide"'),
    ("la fraîcheur ignore l'échéance FSRS et grise un nœud mûr", "progression.py",
     "        a_revoir = joue and jours is not None and jours > fraicheur and echue",
     "        a_revoir = joue and jours is not None and jours > fraicheur"),
    ("le rapport du rituel compte une séance abandonnée comme finie", "rituel.py",
     "    elif set(annoncees).issubset(set(distinctes)):", "    elif True:"),
    ("le rapport du rituel lit le contenu des réponses", "rituel.py",
     '        propre = {c: ligne[c] for c in CHAMPS_LUS if c in ligne}',
     "        propre = dict(ligne)"),
    ("une source de carte peut se passer de ligne au registre", "registre.py",
     "            if dom and (hote == dom or hote.endswith(\".\" + dom)):",
     "            if True:"),
    ("le valideur laisse passer une nature de source inventée", "valide_banque.py",
     '            elif src.get("nature") not in (None, "") and src["nature"] not in NATURES:',
     "            elif False:"),
    ("l'usine ne rejoue plus les contrôles des unités validées", "usine/etat.py",
     '        if u["statut"] != "valide":\n            continue\n        err, sceau, _ = controler_unite',
     '        if True:\n            continue\n        err, sceau, _ = controler_unite'),
    ("un chapitre retiré sert quand même ses cartes", "genere.py",
     '    if chapitre.get("statut") in ("signale", "perime"):\n        return "chapitre"',
     '    if False:\n        return "chapitre"'),
    ("la publication ne juge plus les chapitres v2", "genere.py",
     "        erreurs.extend(v2.valide_chapitre(ch, fichier, programme, parc, aujourdhui))",
     "        pass"),
    ("un lot mixte s'annonce quand même en carte-v2", "genere.py",
     "    if cartes_v2 and nb_v1 == 0:", "    if cartes_v2:"),
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
            sauvegardes[fichier].parent.mkdir(parents=True, exist_ok=True)
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

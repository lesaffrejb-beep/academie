#!/usr/bin/env python3
"""Non-régression du lot éditorial ACA-COPRO-1, pas un valideur juridique.

Vérifie les artefacts réellement utilisés et la suspension des cartes dont
la source manque. Les règles de droit sont justifiées par la table de revue.
"""
import hashlib
import importlib.util
import json
import sys
import tempfile
import subprocess
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("genere_copro", RACINE / "programme/genere_copro.py")
generation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generation)


class CorrectionsCopro(unittest.TestCase):
    def test_identifiants_historiques_conserves(self):
        ids = sorted(c["id"] for c in generation.construit()["chapitres"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(hashlib.sha256("\n".join(ids).encode()).hexdigest(),
                         "e45c173e38e26b3d3c552890bf11dab631555dd915cc1f6519b758d19e2dabfb")

    def test_regeneration_reproduit_les_deux_artefacts(self):
        prog = generation.construit()
        self.assertEqual(prog, json.loads((RACINE / "programme/copro.json").read_text()))
        self.assertEqual(generation.syllabus(prog), (RACINE / "SYLLABUS.md").read_text())

    def test_corrections_survivent_a_la_generation(self):
        ch = {c["id"]: c for c in generation.construit()["chapitres"]}
        self.assertNotIn("abstentions comprises", ch["droit.majorites.l-article-24"]["competence"])
        self.assertNotIn("cinq pour cent", ch["droit.assemblee.pouvoirs-et-representation"]["notions"])
        self.assertNotIn("dix jours", ch["sinistres.contrat.les-delais-de-declaration"]["notions"])

    def test_catalogue_et_cartes_reellement_selectionnees(self):
        with tempfile.TemporaryDirectory(prefix="academie-copro-") as tmp:
            cible = Path(tmp) / "banque.json"
            p = subprocess.run([sys.executable, str(RACINE / "app/genere.py"),
                                "--couches", "banque", "--sortie", str(cible)],
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
            charge = json.loads(cible.read_text())
        ids = {c["id"] for c in charge["cartes"]}
        suspendues = {"sinistres-irsi-tranches", "sinistres-irsi-assureur-gestionnaire",
                      "sinistres-recherche-de-fuite", "sinistres-cidre-abrogee"}
        self.assertFalse(ids & suspendues, ids & suspendues)
        catalogue = json.loads((RACINE / "programme/catalogue.json").read_text())
        copro = next(p for p in catalogue["parcours"] if p["cle"] == "copro")
        self.assertEqual(copro["chapitres"], len(generation.construit()["chapitres"]))
        self.assertEqual(copro["cartes_jouables"], len(charge["metiers"]["copro"]["cartes"]))
        self.assertEqual(set(charge["metiers"]["copro"]["cartes"]) | set(charge["metiers"]["ifsi"]["cartes"]), ids)
        self.assertFalse(set(charge["metiers"]["copro"]["cartes"]) & set(charge["metiers"]["ifsi"]["cartes"]))


if __name__ == "__main__":
    unittest.main()

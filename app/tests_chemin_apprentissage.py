"""Contrat du professeur : fixtures fictives, aucun acquis attribué à un joueur."""
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import chemin_apprentissage as chemin


def exemple():
    return {
        "version": 1, "statut": "brouillon", "demande": "Exemple fictif : comparer des avis",
        "cible_observable": "Justifier un avis conditionnel dans un cas nouveau", "metier": "copro",
        "ancrage": {"chapitre": "droit.base.role", "justification": "Délimiter la décision du gestionnaire"},
        "prerequis": [{"notion": "Lire une consigne", "etat": "inconnu"}],
        "diagnostic": {"productions": [{"consigne": "Expliquer un premier choix", "criteres": ["Nommer une limite"]}],
                       "reussite": ["comparer"], "echec": ["comparer"]},
        "sources": [{"id": "guide", "titre": "Guide à identifier", "statut": "a_trouver", "manque": "Original public à retrouver"}],
        "etapes": [{"id": "comparer", "titre": "Comparer deux avis", "niveau": 2,
                    "justification_niveau": "Relier une règle et sa limite", "dependances": [],
                    "chapitre": "droit.base.role", "disponibilite": "a_construire", "transversalites": [],
                    "notions": ["Périmètre de décision"], "sources": ["guide"],
                    "exercices": [{"format": "libre", "consigne": "Comparer les explications",
                                   "justification": "Rendre le raisonnement observable", "criteres": ["Séparer fait et hypothèse"], "sources": ["guide"]}],
                    "transfert": {"cas_nouveau": "Défendre un avis dans un autre dossier fictif", "criteres": ["Adapter la limite"]},
                    "reprise_echec": {"consigne": "Reprendre la distinction puis retenter", "etapes": ["comparer"]}}],
    }


class Chemins(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.racine = Path(self.tmp.name); (self.racine / "programme").mkdir()
        for metier, cid in [("copro", "droit.base.role"), ("ifsi", "soins.base.securite")]:
            (self.racine / "programme" / f"{metier}.json").write_text(json.dumps({"chapitres": [{"id": cid}]}))
        self.d = exemple()

    def verifie(self, d=None, **options):
        return chemin.verifie(self.d if d is None else d, self.racine, **options)

    def test_chemin_manques_explicites_et_advanced_fictif(self):
        self.d["prerequis"].append({"notion": "Argumenter un avis", "etat": "declare"})
        r = self.verifie(); self.assertTrue(r["coherent"], r)
        self.assertEqual("cohérence structurelle", r["statut"])
        self.assertEqual(["guide"], r["sources_manquantes"])

    def test_frontieres_cahier(self):
        mutations = [
            lambda d: d["ancrage"].update(chapitre="droit.invente"),
            lambda d: d["etapes"][0].update(sources=["source-inventee"]),
            lambda d: d["etapes"][0].update(dependances=["comparer"]),
            lambda d: d["prerequis"][0].update(etat="observe"),
            lambda d: d["sources"][0].update(statut="presente"),
            lambda d: d["etapes"][0].update(disponibilite="disponible"),
            lambda d: d["etapes"][0].pop("transfert"),
            lambda d: d["diagnostic"].update(echec=[]),
            lambda d: d["etapes"][0].update(transversalites=[{"chapitre": "soins.base.securite", "justification": "Transfert réel"}]),
        ]
        for i, mutation in enumerate(mutations):
            with self.subTest(i=i):
                d = copy.deepcopy(self.d); mutation(d)
                if i == 8: self.assertTrue(self.verifie(d)["coherent"])
                else: self.assertFalse(self.verifie(d)["coherent"])

    def test_cycle_multiple_et_references_inconnues(self):
        autre = copy.deepcopy(self.d["etapes"][0]); autre.update(id="base", dependances=["comparer"])
        self.d["etapes"].append(autre); self.d["etapes"][0]["dependances"] = ["base"]
        self.assertFalse(self.verifie()["coherent"])
        self.d["etapes"][0]["dependances"] = []; self.d["diagnostic"]["reussite"] = ["absente"]
        self.assertFalse(self.verifie()["coherent"])

    def test_original_strict_empreinte_et_support(self):
        original = self.racine / "original.txt"; original.write_text("Document fictif de test")
        self.d["sources"] = [{"id": "guide", "titre": "Pièce de test", "statut": "presente",
                              "url": "https://example.org/guide", "empreinte": hashlib.sha256(original.read_bytes()).hexdigest(),
                              "chemin_original": "original.txt"}]
        self.assertTrue(self.verifie(strict_local=True)["coherent"])
        original.write_text("Modifié"); self.assertFalse(self.verifie(strict_local=True)["coherent"])
        self.d["sources"][0]["chemin_original"] = "absent.pdf"
        self.assertFalse(self.verifie(strict_local=True)["coherent"])
        self.d["sources"][0].update(chemin_original="original.txt", empreinte=hashlib.sha256(original.read_bytes()).hexdigest())
        self.assertTrue(self.verifie(strict_local=True)["coherent"])
        self.d["etapes"][0]["exercices"][0]["support"] = {"chemin": "absent.svg", "justification": "Voir le mécanisme"}
        self.assertFalse(self.verifie(strict_local=True)["coherent"])

    def test_observe_exige_date_valide_et_preuve(self):
        self.d["prerequis"][0].update(etat="observe", preuve="Production fictive identifiée", date="2026-99-99")
        self.assertFalse(self.verifie()["coherent"])
        self.d["prerequis"][0]["date"] = "2026-09-06"
        self.assertTrue(self.verifie()["coherent"])

    def banque_disponible(self):
        self.d["sources"] = [{"id": "guide", "titre": "Pièce de test", "statut": "presente",
                              "url": "https://example.org/guide", "empreinte": "a" * 64, "chemin_original": "original.txt"}]
        self.d["etapes"][0]["disponibilite"] = "disponible"
        return {"metiers": {"copro": {"cartes": ["c"]}}, "cartes": [{"id": "c", "statut": "valide"}],
                "etudes": {"lecons": {"droit.base.role": {"statut": "valide", "verifie_par": {"modele": "fixture"}, "cartes": ["c"]}}}}

    def test_disponibilite_reelle_et_autre_cursus(self):
        banque = self.banque_disponible()
        self.assertTrue(self.verifie(banque=banque)["coherent"])
        banque["metiers"]["copro"]["cartes"] = []
        self.assertFalse(self.verifie(banque=banque)["coherent"])

    def test_peremption_carte_comme_client(self):
        banque = self.banque_disponible()
        for peremption in [False, 0, "20990101", "2099-1-1", "2099-02-29", "illisible", (date.today()-timedelta(days=1)).isoformat()]:
            with self.subTest(peremption=peremption):
                banque["cartes"][0]["peremption"] = peremption
                self.assertFalse(self.verifie(banque=banque)["coherent"])
        for peremption in [None, "", date.today().isoformat(), (date.today()+timedelta(days=1)).isoformat()]:
            with self.subTest(peremption=peremption):
                banque["cartes"][0]["peremption"] = peremption
                self.assertTrue(self.verifie(banque=banque)["coherent"])

    def test_fraicheur_annuelle_etude_juridique_comme_client(self):
        banque = self.banque_disponible(); lecon = banque["etudes"]["lecons"]["droit.base.role"]
        lecon["peremption"] = "2099-01-01"
        for nature in ["texte-officiel", "jurisprudence"]:
            lecon["sources"] = [{"nature": nature}]
            for verification in ["illisible", "20990101", None, (date.today()-timedelta(days=366)).isoformat()]:
                with self.subTest(nature=nature, verification=verification):
                    lecon["verifie"] = verification
                    self.assertFalse(self.verifie(banque=banque)["coherent"])
            lecon["verifie"] = (date.today()-timedelta(days=365)).isoformat()
            self.assertTrue(self.verifie(banque=banque)["coherent"])
        lecon["sources"] = [{"nature": "institution"}]; lecon["verifie"] = "2000-01-01"
        self.assertTrue(self.verifie(banque=banque)["coherent"])
        lecon["peremption"] = "20990101"
        self.assertFalse(self.verifie(banque=banque)["coherent"])

    def test_proposition_et_json_malforme(self):
        e = self.d["etapes"][0]; e.pop("chapitre"); e["proposition"] = {"titre": "Sujet nouveau", "justification": "Trou explicite"}
        self.assertTrue(self.verifie()["coherent"])
        e["disponibilite"] = "disponible"; self.assertFalse(self.verifie()["coherent"])
        for invalide in [None, [], {"etapes": [None]}, {**exemple(), "etapes": "oops"}]:
            self.assertFalse(chemin.verifie(invalide, self.racine)["coherent"])

    def test_artefact_malforme_et_url_invalide(self):
        self.d["etapes"][0]["disponibilite"] = "disponible"
        for banque in [{"etudes": []}, {"etudes": {"lecons": []}}, {"cartes": [None]}]:
            self.assertFalse(self.verifie(banque=banque)["coherent"])
        self.d["etapes"][0]["disponibilite"] = "a_construire"
        self.d["sources"] = [{"id": "guide", "titre": "Test", "statut": "presente", "url": "https://example.org/espace interdit",
                              "empreinte": "a" * 64, "chemin_original": "fichier"}]
        self.assertFalse(self.verifie()["coherent"])

    def test_preparer_cli_sans_acquis_ni_ecrasement(self):
        sortie = self.racine / "demande.json"
        cmd = [sys.executable, str(Path(chemin.__file__)), "preparer", "--demande", "Apprendre X", "--metier", "copro",
               "--racine", str(self.racine), "--sortie", str(sortie)]
        self.assertEqual(0, subprocess.run(cmd, capture_output=True).returncode)
        d = json.loads(sortie.read_text()); self.assertEqual([], d["prerequis"]); self.assertEqual([], d["etapes"])
        self.assertNotEqual(0, subprocess.run(cmd, capture_output=True).returncode)


if __name__ == "__main__": unittest.main()

"""Le catalogue de spécialités ne fabrique pas de preuve d'expertise."""
import copy
import unittest
import json
from pathlib import Path

from couverture_expertises import construire, verifier


class CouvertureTests(unittest.TestCase):
    def setUp(self):
        self.programme = {"domaines": {"droit": {"titre": "Droit"}},
                          "branches": {"droit": [{"cle": "statut"}]},
                          "chapitres": [{"id": "droit.statut.a", "domaine": "droit", "niveau": 5}]}
        self.catalogue = {"specialites": [{"id": "juriste", "titre": "Juriste",
            "branches": ["droit.statut"], "objectifs": ["Arbitrer"],
            "production": "Note contradictoire", "sources_a_instruire": ["Textes"],
            "limite": "Pas une qualification", "statut": "a-construire"}]}

    def test_branche_inconnue_refusee(self):
        c = copy.deepcopy(self.catalogue)
        c["specialites"][0]["branches"] = ["droit.invente"]
        self.assertTrue(verifier(c, self.programme))

    def test_production_et_limite_obligatoires(self):
        for champ in ("production", "limite", "sources_a_instruire", "objectifs"):
            c = copy.deepcopy(self.catalogue)
            del c["specialites"][0][champ]
            self.assertTrue(verifier(c, self.programme), champ)

    def test_pas_de_couverture_inventee(self):
        r = construire(self.catalogue, self.programme, {"cartes": []}, [])
        self.assertEqual(r["domaines"][0]["chapitres_prevus"], 1)
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 0)
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 0)

    def test_autre_cursus_exclu_et_v1_non_attribuee(self):
        cartes = {"cartes": [
            {"id": "copro", "domaine": "droit", "niveau": 1, "statut": "valide"},
            {"id": "ifsi", "domaine": "pharmaco", "niveau": 5, "statut": "valide"},
            {"id": "draft", "domaine": "droit", "niveau": 5, "statut": "brouillon"}]}
        r = construire(self.catalogue, self.programme, cartes, [])
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 1)
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 0)
        self.assertEqual(r["cartes_sans_chapitre"], 1)

    def test_artefact_absent_reste_inconnu(self):
        r = construire(self.catalogue, self.programme, None, [])
        self.assertIsNone(r["domaines"][0]["cartes_artefact"])
        self.assertIsNone(r["specialites"][0]["cartes_rattachees"])

    def test_doublon_specialite_refuse(self):
        c = copy.deepcopy(self.catalogue)
        c["specialites"] *= 2
        self.assertTrue(verifier(c, self.programme))

    def test_rattachement_exact_sans_couverture_competence(self):
        cartes = {"cartes": [{"id": "a", "domaine": "droit", "niveau": 4,
                            "chapitre": "droit.statut.a", "statut": "valide"}]}
        r = construire(self.catalogue, self.programme, cartes, [])
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 1)
        self.assertEqual(r["specialites"][0]["statut"], "a-construire")
        self.assertEqual(r, construire(self.catalogue, self.programme, cartes, []))

    def test_catalogue_reel(self):
        racine = Path(__file__).resolve().parents[1]
        catalogue = json.loads((racine / "programme/specialisations/copro.json").read_text())
        programme = json.loads((racine / "programme/copro.json").read_text())
        self.assertEqual(verifier(catalogue, programme), [])
        r = construire(catalogue, programme, None, [])
        self.assertEqual(len(r["specialites"]), len(catalogue["specialites"]))

    def test_domaine_commun_ne_melange_pas_les_cursus(self):
        artefact = {"cartes": [{"id": "autre", "domaine": "droit", "statut": "valide",
                               "niveau": 5, "chapitre": "droit.autre-cursus.a"}]}
        r = construire(self.catalogue, self.programme, artefact, [])
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 0)

    def test_champs_malformes_refuses_sans_exception(self):
        for champ, valeur in [("production", "   "), ("limite", 5), ("branches", [[]]),
                              ("id", []), ("titre", None)]:
            c = copy.deepcopy(self.catalogue)
            c["specialites"][0][champ] = valeur
            self.assertTrue(verifier(c, self.programme), (champ, valeur))


if __name__ == "__main__":
    unittest.main()

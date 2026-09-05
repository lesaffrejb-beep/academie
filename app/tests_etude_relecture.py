"""Contre-passe indépendante des frontières du catalogue Étude, fixtures isolées."""
import copy
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
import genere
import valide_chapitres as v
from tests_chapitres import chapitre, carte, PROGRAMME

DATE = date(2026, 9, 5)
REVUE = {"outil":"Codex","modele":"test","session":"revue-distincte","date":"2026-09-05","rapport":"travail/test.md","assertions":["périmètre"],"sources":["https://www.legifrance.gouv.fr/"]}

class FrontiereEtudes(unittest.TestCase):
    def setUp(self):
        self.ch = chapitre(statut="valide",verifie="2026-09-05",verifie_par=copy.deepcopy(REVUE),peremption="2027-01-01",cartes=[carte(statut="valide",verifie="2026-09-05",verifie_par=copy.deepcopy(REVUE),peremption="2027-01-01")])
        self.retenues = copy.deepcopy(self.ch["cartes"])

    def publie(self, ch=None, retenues=None):
        with patch.object(v,"charge_chapitres",return_value=([(ch if ch is not None else self.ch,Path("fixture.json"))],[])), patch.object(v,"charge_programme",return_value={c["id"]:c for c in PROGRAMME["chapitres"]}):
            return genere.charge_etudes(self.retenues if retenues is None else retenues,DATE)["lecons"]

    def test_positive_et_complete(self):
        self.assertIn(self.ch["id"],self.publie())

    def test_pas_de_carte_absente(self):
        self.assertEqual({},self.publie(retenues=[]))

    def test_statut_expiration_et_tampon_historique(self):
        for changement in ({"statut":"brouillon"},{"peremption":"2026-09-04"},{"verifie_par":"tampon historique"}):
            with self.subTest(changement=changement):
                self.assertEqual({},self.publie(ch={**self.ch,**changement}))

    def test_carte_perimee_meme_si_id_retenu(self):
        ch=copy.deepcopy(self.ch)
        ch["cartes"][0]["peremption"]="2026-09-04"
        self.assertEqual({},self.publie(ch=ch))

    def test_meme_session_interdite(self):
        ch=copy.deepcopy(self.ch)
        ch["verifie_par"]["session"]=ch["provenance"]["session"]
        self.assertEqual({},self.publie(ch=ch))

    def test_attestation_structuree_ne_se_contente_pas_de_truthy(self):
        ch=copy.deepcopy(self.ch)
        ch["verifie_par"]={k:True for k in REVUE}
        self.assertTrue(v.valide_relecture(ch,"fixture"),"Des booléens ne nomment ni relecteur, ni date, ni rapport ni assertions.")

if __name__ == "__main__":
    unittest.main()

"""Garde-fous du banc d'essai local, sans PDF tiers requis."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from benchmark_pdf import evaluer, sondage, verifier_source, normaliser


class BancTest(unittest.TestCase):
    def test_temoin_positif_et_negatif(self):
        cas = {"present": ["texte visible"], "absent": ["texte masqué"]}
        self.assertTrue(all(x["ok"] for x in evaluer("Texte\nvisible", cas)))
        self.assertFalse(all(x["ok"] for x in evaluer("Texte masqué", cas)))

    def test_erreur_absence_ne_valide_pas_negatifs(self):
        self.assertIsNone(evaluer(None, {"absent": ["parasite"]}))

    def test_parasite_fragmente_reste_detecte(self):
        self.assertFalse(evaluer("S E D | A Ç | A F", {"absent": ["SEDAÇAF"]})[0]["ok"])

    def test_nombres_et_signes_non_effaces(self):
        self.assertNotEqual(normaliser("-0,5 %"), normaliser("0,5 %"))
        self.assertNotEqual(normaliser("55 %"), normaliser("58 %"))

    def test_temoin_numerique_refuse_sous_chaine_et_signe(self):
        for texte in ("-0,5 %", "− 0,5 %", "+0,5 %", "10,5 %"):
            self.assertFalse(evaluer(texte, {"present": ["0,5 %"]})[0]["ok"], texte)
        self.assertFalse(evaluer("155 %", {"present": ["55 %"]})[0]["ok"])
        self.assertTrue(evaluer("Soit 0,5 %.", {"present": ["0,5 %"]})[0]["ok"])

    def test_bornes_mots_et_decimales(self):
        self.assertFalse(evaluer("référence 58,5", {"present": ["58"]})[0]["ok"])
        self.assertFalse(evaluer("préarrêté", {"present": ["arrêté"]})[0]["ok"])

    def test_ordre_de_relation(self):
        cas = {"present": [], "absent": [], "regex": [r"reference\s+58\s*%\s+27\s*%\s+6\s*%"]}
        self.assertTrue(evaluer("Reference 58 % 27 % 6 %", cas)[0]["ok"])
        self.assertFalse(evaluer("Reference 27 % 58 % 6 %", cas)[0]["ok"])

    def test_sondage_reproductible_hors_imposes(self):
        a = sondage(54, "a" * 64, "graine-apres-lot", 8, [1, 9, 12])
        self.assertEqual(a, sondage(54, "a" * 64, "graine-apres-lot", 8, [1, 9, 12]))
        self.assertEqual(len(set(a)), 8)
        self.assertFalse(set(a) & {1, 9, 12})
        self.assertNotEqual(a, sondage(54, "a" * 64, "autre-graine", 8, [1, 9, 12]))

    def test_sondage_bornes(self):
        self.assertEqual(sondage(2, "a" * 64, "s", 10, [1]), [2])
        for n, k in [(0, 1), (3, -1)]:
            with self.assertRaises(ValueError):
                sondage(n, "a" * 64, "s", k, [])

    def test_source_empreinte_exacte(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "source.pdf"
            fichier.write_bytes(b"fixture")
            sha = hashlib.sha256(b"fixture").hexdigest()
            self.assertEqual(verifier_source(fichier, sha), sha)
            with self.assertRaises(ValueError):
                verifier_source(fichier, "b" * 64)


if __name__ == "__main__":
    unittest.main()

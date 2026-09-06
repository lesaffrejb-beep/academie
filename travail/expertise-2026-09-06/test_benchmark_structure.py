"""Garde-fous du complément structuré ; tests indépendants des modèles."""
import unittest
from benchmark_structure import bilan, verifier_espace


class GardeFous(unittest.TestCase):
    def test_absence_ne_devient_pas_texte_vide_valide(self):
        r = bilan(None, {"present": ["Arrêté"]})
        self.assertEqual(r["statut"], "erreur")
        self.assertIsNone(r["temoins"])

    def test_sortie_vide_est_un_echec_de_temoin(self):
        self.assertFalse(bilan("", {"present": ["Arrêté"]})["temoins"][0]["ok"])

    def test_reserve_disque(self):
        with self.assertRaises(RuntimeError):
            verifier_espace(7 * 1024**3)
        verifier_espace(9 * 1024**3)


if __name__ == "__main__":
    unittest.main()

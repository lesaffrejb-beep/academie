import unittest
from pathlib import Path
from export_cours import exporter
class ExportCours(unittest.TestCase):
    def test_brouillons_ne_deviennent_pas_des_cartes(self):
        d=exporter(Path(__file__).resolve().parents[1])
        self.assertEqual(len(d['chapitres']),389)
        for c in d['chapitres']:
            self.assertEqual(c['statut'],'brouillon editorial')
            self.assertGreater(len(c['texte']),100)
            self.assertNotIn('cartes',c)
            self.assertTrue(c['sources'])
            self.assertTrue(c['auteur'])

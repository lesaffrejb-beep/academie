import sys
from pathlib import Path
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'app'))
import genere
import valide_chapitres

class RoutageTest(unittest.TestCase):
    def test_satellite_uniquement_dans_metier_parent(self):
        ch = {'id': 'satellite.travaux.test', 'satellite': True,
              'rattachement_propose': 'travaux.renovation-globale.les-scenarios'}
        carte = {'id': 'pilote-test', 'chapitre': ch['id'], 'domaine': 'travaux'}
        with patch.object(valide_chapitres, 'charge_chapitres', return_value=([(ch, Path('test.json'))], [])):
            m = genere.charge_metiers([carte])
        self.assertIn('pilote-test', m['copro']['cartes'])
        self.assertNotIn('pilote-test', m['ifsi']['cartes'])

if __name__ == '__main__':
    unittest.main()

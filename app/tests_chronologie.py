"""Régressions de rejeu, offsets et précision arbitraire."""
import unittest
from seance import etats_cartes
from planificateur import Planificateur

class Chronologie(unittest.TestCase):
    def test_rejeu(self):
        for avant, apres in [
            ('2026-10-25T02:50:00+02:00', '2026-10-25T02:10:00+01:00'),
            ('2026-09-05T12:00:00.0000001Z', '2026-09-05T12:00:00.0000002Z'),
            ('2026-09-05T12:00:00', '2026-09-05T12:00:01Z'),
        ]:
            a = dict(quand=avant, mode='revision', nonce='zzzzzzzz', carte='c', note=4)
            b = dict(quand=apres, mode='revision', nonce='aaaaaaaa', carte='c', note=1)
            with self.subTest(avant=avant):
                self.assertEqual(etats_cartes([b,a], Planificateur())['c']['dernière_note'], 1)

if __name__ == '__main__':
    unittest.main()

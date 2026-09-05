"""Contre-exemples indépendants pour le correctif de synchronisation."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import erreurs
import seance
from chronologie import cle_chronologique

class RelectureChronologie(unittest.TestCase):
    def test_carnet_changement_heure_sans_recriture(self):
        a = dict(quand="2026-10-25T02:50:00+02:00", carte="c", note=4)
        b = dict(quand="2026-10-25T02:10:00+01:00", carte="c", note=1)
        with tempfile.TemporaryDirectory() as dossier:
            chemin = erreurs.chemin_erreurs("fixture", Path(dossier))
            chemin.parent.mkdir(parents=True)
            brut = "\n".join(json.dumps(l) for l in [b, a])
            chemin.write_text(brut)
            self.assertEqual(erreurs.lit_carnet("fixture", Path(dossier)), [a,b])
            self.assertEqual(chemin.read_text(), brut)

    def test_fractions_longues_et_avant_epoch(self):
        for base in ["2026-09-05", "1969-12-31"]:
            a = dict(quand=base+"T23:59:59.1234567890123456789012345678901Z")
            b = dict(quand=base+"T23:59:59.1234567890123456789012345678902Z")
            self.assertLess(cle_chronologique(a), cle_chronologique(b))

    def test_unicode_par_points_de_code(self):
        base = dict(quand="2026-09-05T12:00:00Z", mode="revision")
        a, b = dict(base, nonce="\ue000aaaaaaa"), dict(base, nonce="\U00010000aaaaaaa")
        self.assertEqual(sorted([b,a], key=cle_chronologique), [a,b])

    def test_anciens_et_offsets_equivalents_conservent_identites(self):
        dates = ["2026-09-05T12:00:00", "2026-09-05T14:00:00+02:00", "2026-09-05T12:00:00Z"]
        lignes = [dict(quand=d, mode="flash") for d in dates]
        self.assertEqual(len({cle_chronologique(l)[:3] for l in lignes}), 1)
        self.assertEqual(sorted(lignes, key=cle_chronologique), sorted(lignes, key=lambda l:l["quand"]))

if __name__ == '__main__':
    unittest.main()

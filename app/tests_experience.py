"""Le pilote publié reste relié, périssable et relu dans une autre session."""
import unittest
from datetime import date
from pathlib import Path
import valide_chapitres as v

class Pilote(unittest.TestCase):
    def test_attestation_independante(self):
        import json
        ch=json.loads(Path('chapitres/droit/majorites/l-article-24.json').read_text())
        ch['statut']='valide'
        ch['verifie_par']={'session':ch['provenance']['session'], 'date':'2026-09-05'}
        erreurs=v.valide_chapitre(ch,Path('test.json'),v.charge_programme(),set(),date(2026,9,5))
        self.assertTrue(any('session' in e for e in erreurs), erreurs)

if __name__=='__main__': unittest.main()

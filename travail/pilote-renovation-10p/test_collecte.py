import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('collecte', Path(__file__).with_name('collecte.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class CollecteTest(unittest.TestCase):
    def test_dix_pages_contigues(self):
        self.assertEqual(module.PAGES, tuple(range(13, 23)))
    def test_empreinte_fausse_refusee(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'faux.pdf'
            p.write_bytes(b'pas le document')
            with self.assertRaises(ValueError):
                module.verifier(p)
    def test_difference_ne_devient_pas_consensus(self):
        r = module.comparer('coût 14 000', 'coût 14000')
        self.assertFalse(r['identiques'])
        self.assertEqual(r['verdict'], 'a_arbitrer_sur_image')

if __name__ == '__main__':
    unittest.main()

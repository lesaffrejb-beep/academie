"""Les sorties tierces du banc ne sont pas la voix éditoriale du produit."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tooling.check import ROOT, est_sortie_benchmark


class PreuvesBrutes(unittest.TestCase):
    def test_page_brute_uniquement(self):
        self.assertTrue(est_sortie_benchmark(ROOT / "sources/benchmark-pdf/essai/angers-0012.md"))
        for p in ["sources/benchmark-pdf/README.md", "sources/benchmark-pdf/essai/rapport.md",
                  "chapitres/benchmark-pdf/essai/angers-0012.md", "sources/angers-0012.md"]:
            self.assertFalse(est_sortie_benchmark(ROOT / p), p)


if __name__ == "__main__":
    unittest.main()

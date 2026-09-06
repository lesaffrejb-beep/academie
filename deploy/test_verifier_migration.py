"""Preuves de conservation du journal, sans fixture de personne réelle."""
from contextlib import closing
import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest

CHEMIN = Path(__file__).with_name("verifier_migration.py")
spec = importlib.util.spec_from_file_location("verifier_migration", CHEMIN)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Conservation(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.avant = Path(self.temp.name) / "avant.sqlite"
        self.apres = Path(self.temp.name) / "apres.sqlite"
        for chemin in (self.avant, self.apres):
            with closing(sqlite3.connect(chemin)) as conn:
                conn.executescript("CREATE TABLE journal (nonce TEXT PRIMARY KEY, ligne TEXT); INSERT INTO journal VALUES ('a','contenu de test'); CREATE TABLE migrations (nom TEXT); INSERT INTO migrations VALUES ('0001');")

    def modifie(self, sql):
        with closing(sqlite3.connect(self.apres)) as conn:
            conn.executescript(sql)

    def test_ajout_de_schema_conserve_les_donnees(self):
        self.modifie("ALTER TABLE journal ADD COLUMN addition TEXT; INSERT INTO migrations VALUES ('0002'); CREATE TABLE nouvelle (id TEXT);")
        self.assertEqual(module.compare(self.avant, self.apres), {"journal": 1})

    def test_compte_egal_ne_prouve_pas_identite(self):
        self.modifie("UPDATE journal SET ligne='autre contenu';")
        with self.assertRaisesRegex(ValueError, "journal"):
            module.compare(self.avant, self.apres)

    def test_ligne_perdue(self):
        self.modifie("DELETE FROM journal;")
        with self.assertRaisesRegex(ValueError, "journal"):
            module.compare(self.avant, self.apres)

    def test_table_perdue(self):
        self.modifie("DROP TABLE journal;")
        with self.assertRaisesRegex(ValueError, "journal"):
            module.compare(self.avant, self.apres)

    def test_colonne_perdue(self):
        self.modifie("ALTER TABLE journal DROP COLUMN ligne;")
        with self.assertRaisesRegex(ValueError, "ligne"):
            module.compare(self.avant, self.apres)

    def test_doublons_repartis_autrement_sont_detectes(self):
        for chemin in (self.avant, self.apres):
            with closing(sqlite3.connect(chemin)) as conn:
                conn.executescript("CREATE TABLE doublons (texte TEXT); INSERT INTO doublons VALUES ('a'),('a'),('b');")
        self.modifie("DELETE FROM doublons; INSERT INTO doublons VALUES ('a'),('b'),('b');")
        with self.assertRaisesRegex(ValueError, "doublons"):
            module.compare(self.avant, self.apres)

    def test_fichier_absent_ne_se_cree_pas(self):
        absent = self.apres.with_name("absent.sqlite")
        with self.assertRaises(FileNotFoundError):
            module.compare(self.avant, absent)
        self.assertFalse(absent.exists())

if __name__ == "__main__":
    unittest.main()

import json
import tempfile
import unittest
from pathlib import Path

from commun import application
import importer_journal as imp

V0 = [
    {"quand": "2026-08-30T07:00:00+00:00", "carte": "droit-majorites-1", "note": 3, "mode": "flash"},
    {"quand": "2026-08-30T07:01:00+00:00", "carte": "droit-majorites-2", "note": 1, "mode": "flash"},
    {"quand": "2026-08-29T18:00:00+00:00", "carte": "compta-1", "note": 3, "mode": "quiz", "origine": "quiz",
     "domaine": "comptabilite", "stabilite_forcee": 21.0},
    {"quand": "2026-08-31T07:00:00+00:00", "carte": "droit-majorites-1", "note": 4, "mode": "flash"},
]
ERREURS = [{"quand": "2026-08-30T07:01:30+00:00", "carte": "droit-majorites-2", "raison": "confondu 24 et 25"}]


class Import(unittest.TestCase):
    def setUp(self):
        self.dossier = Path(tempfile.mkdtemp(prefix="academie-import-"))
        self.revues = self.dossier / "revues.jsonl"
        self.revues.write_text("\n".join(json.dumps(l) for l in V0) + "\npas du json\n", encoding="utf-8")
        self.erreurs = self.dossier / "erreurs.jsonl"
        self.erreurs.write_text("\n".join(json.dumps(l) for l in ERREURS) + "\n", encoding="utf-8")

    def test_migration_v0_vers_v1(self):
        lignes, illisibles = imp.migrer_fichier(self.revues, self.erreurs)
        self.assertEqual(illisibles, 1)
        self.assertEqual(len(lignes), 5)
        par_carte = {(l["mode"], l["quand"]): l for l in lignes}
        flash = par_carte[("revision", "2026-08-30T07:00:00+00:00")]
        self.assertEqual((flash["format"], flash["note"], flash["carte"]), ("seance", 3, "droit-majorites-1"))
        quiz = par_carte[("quiz", "2026-08-29T18:00:00+00:00")]
        self.assertEqual((quiz["origine"], quiz["stabilite_forcee"], quiz["region"]), ("quiz", 21.0, "comptabilite"))
        self.assertNotIn("domaine", quiz)
        err = par_carte[("erreur", "2026-08-30T07:01:30+00:00")]
        self.assertEqual((err["carte"], err["raison"]), ("droit-majorites-2", "confondu 24 et 25"))
        for l in lignes:
            self.assertEqual(len(l["nonce"]), 64)
        self.assertEqual(lignes, sorted(lignes, key=lambda l: (l["quand"], l["mode"], l["nonce"])))

    def test_nonce_stable_et_source_intacte(self):
        avant = self.revues.read_text(encoding="utf-8")
        l1, _ = imp.migrer_fichier(self.revues, self.erreurs)
        l2, _ = imp.migrer_fichier(self.revues, self.erreurs)
        self.assertEqual([l["nonce"] for l in l1], [l["nonce"] for l in l2])
        self.assertEqual(self.revues.read_text(encoding="utf-8"), avant)

    def test_import_en_base_idempotent(self):
        appli, profil, _ = application()
        r1 = imp.importer_dans_base(appli.conn, profil, self.revues, self.erreurs)
        self.assertEqual((r1["acceptees"], r1["ignorees"], r1["illisibles"]), (5, 0, 1))
        r2 = imp.importer_dans_base(appli.conn, profil, self.revues, self.erreurs)
        self.assertEqual((r2["acceptees"], r2["ignorees"]), (0, 5))


if __name__ == "__main__":
    unittest.main()

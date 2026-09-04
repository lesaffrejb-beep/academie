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

    def test_quiz_v0_sans_stabilite_rejoue_comme_revision(self):
        from academie_etat.journal import valider_ligne
        for valeur in (None, 0, -1, "illisible"):
            with self.subTest(stabilite=valeur):
                avant = {"quand": "2026-08-30T07:00:00+00:00", "mode": "quiz",
                         "carte": "c", "note": 3, "origine": "quiz", "stabilite_forcee": valeur}
                ligne = imp.migrer_revue(json.dumps(avant))
                self.assertEqual((ligne["mode"], ligne["format"], ligne["origine"]),
                                 ("revision", "seance", "quiz"))
                self.assertIsNone(valider_ligne(ligne))

    def test_un_export_deja_v1_garde_son_identite_et_ses_champs(self):
        from academie_etat.journal import valider_ligne
        commun = {"quand": "2026-09-04T07:00:00+00:00", "nonce": "nonce-export-deja-v1"}
        exemples = [
            {**commun, "mode": "revision", "format": "domaine", "carte": "c", "note": 3,
             "duree_ms": 1200, "confiance": True},
            {**commun, "mode": "seance", "format": "seance", "graine": 42, "jour": "cours",
             "banque_version": "2026-09-04", "moteur_version": "fsrs-6", "cap": "droit", "cartes": ["c"]},
            {**commun, "mode": "examen", "region": "droit", "dossier": "examen-droit", "score": 0.8},
            {**commun, "mode": "synthese", "chapitre": "droit.majorites.l-article-24", "attendus_coches": [0, 2]},
            {**commun, "mode": "signalement", "carte": "c", "motif": "Source a revoir"},
            {**commun, "mode": "erreur", "carte": "c", "raison": "Formulation ambigue"},
        ]
        for avant in exemples:
            with self.subTest(mode=avant["mode"]):
                ligne = imp.migrer_revue(json.dumps(avant))
                self.assertEqual(ligne, avant)
                self.assertIsNone(valider_ligne(ligne))

    def test_import_revision_et_seance_deja_v1_est_idempotent(self):
        from academie_etat import journal
        lignes = [
            {"quand": "2026-09-04T07:00:00+00:00", "nonce": "nonce-seance-v1", "mode": "seance",
             "format": "seance", "graine": 42, "banque_version": "2026-09-04", "moteur_version": "fsrs-6"},
            {"quand": "2026-09-04T07:01:00+00:00", "nonce": "nonce-revision-v1", "mode": "revision",
             "format": "seance", "carte": "c", "note": 3},
        ]
        self.revues.write_text("\n".join(json.dumps(l) for l in lignes), encoding="utf-8")
        appli, profil, _ = application()
        journal.fusionner(appli.conn, profil, lignes, depuis=None)
        resultat = imp.importer_dans_base(appli.conn, profil, self.revues)
        self.assertEqual((resultat["acceptees"], resultat["ignorees"]), (0, 2))
        self.assertEqual(journal.compter(appli.conn, profil), 2)

    def test_une_stabilite_v0_numerique_en_texte_est_normalisee(self):
        from academie_etat.journal import valider_ligne
        avant = {"quand": "2026-08-30T07:00:00+00:00", "mode": "quiz", "carte": "c",
                 "note": 3, "origine": "quiz", "stabilite_forcee": "21"}
        ligne = imp.migrer_revue(json.dumps(avant))
        self.assertEqual(ligne["stabilite_forcee"], 21)
        self.assertIsNone(valider_ligne(ligne))


if __name__ == "__main__":
    unittest.main()

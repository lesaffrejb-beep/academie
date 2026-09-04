import unittest
from datetime import datetime, timezone
from unittest.mock import patch

from commun import application, ligne, requete


class Journal(unittest.TestCase):
    def setUp(self):
        self.appli, self.profil, self.jeton = application()

    def envoie(self, lignes, depuis=None, jeton=None):
        return requete(self.appli, "POST", "/journal", {"depuis": depuis, "lignes": lignes}, jeton or self.jeton)

    def test_union_et_idempotence(self):
        s, _, r = self.envoie([ligne(1), ligne(2)])
        self.assertEqual(s, 200)
        self.assertEqual((r["acceptees"], r["ignorees"]), (2, 0))
        s, _, r = self.envoie([ligne(1), ligne(2)])
        self.assertEqual((r["acceptees"], r["ignorees"]), (2 - 2, 2))
        s, _, export = requete(self.appli, "GET", "/journal/export", jeton=self.jeton)
        self.assertEqual(export.count("\n"), 2)

    def test_meme_quadruplet_contenu_different_ignore(self):
        self.envoie([ligne(1, note=3)])
        _, _, r = self.envoie([ligne(1, note=1)])
        self.assertEqual(r["ignorees"], 1)
        _, _, export = requete(self.appli, "GET", "/journal/export", jeton=self.jeton)
        self.assertIn('"note": 3', export)

    def test_manquantes_depuis(self):
        from academie_etat import auth
        autre = auth.creer_jeton(self.appli.conn, self.profil, "outil", "telephone")
        _, _, r1 = self.envoie([ligne(1)], jeton=autre)
        _, _, r2 = self.envoie([ligne(2)], depuis=None)
        self.assertEqual([l["nonce"] for l in r2["manquantes"]], ["nonce-000001"])
        _, _, r3 = self.envoie([], depuis=r2["jusqu_a"])
        self.assertIn("nonce-000002", {l["nonce"] for l in r3["manquantes"]})
        self.assertLessEqual({l["nonce"] for l in r3["manquantes"]},
                             {"nonce-000001", "nonce-000002"})

    def test_deux_appareils_dans_la_meme_seconde(self):
        from academie_etat import journal
        instant = datetime(2026, 9, 4, 10, 0, tzinfo=timezone.utc)
        with patch.object(journal, "datetime", wraps=datetime) as horloge:
            horloge.now.return_value = instant
            _, _, premier = self.envoie([])
            self.envoie([ligne(1)])
            _, _, second = self.envoie([], depuis=premier["jusqu_a"])
            _, _, repete = self.envoie([], depuis=second["jusqu_a"])
        self.assertEqual([l["nonce"] for l in second["manquantes"]], ["nonce-000001"])
        self.assertEqual(repete["manquantes"], second["manquantes"])
        self.assertEqual(journal.compter(self.appli.conn, self.profil), 1)

    def test_lot_de_501_refuse(self):
        s, _, r = self.envoie([ligne(i) for i in range(501)])
        self.assertEqual(s, 422)
        self.assertEqual(r["erreur"], "ligne-invalide")
        self.assertEqual(r["index"], -1)
        s, _, r = self.envoie([ligne(i) for i in range(500)])
        self.assertEqual((s, r["acceptees"]), (200, 500))

    def test_ligne_fautive_indexee_et_lot_entier_refuse(self):
        s, _, r = self.envoie([ligne(1), ligne(2, note=7), ligne(3)])
        self.assertEqual(s, 422)
        self.assertEqual(r["index"], 1)
        self.assertIn("note", r["motif"])
        from academie_etat import journal
        self.assertEqual(journal.compter(self.appli.conn, self.profil), 0)

    def test_champs_obligatoires_selon_le_mode(self):
        cas = {
            "revision": {"carte": "c", "note": 3, "format": "seance"},
            "quiz": {"carte": "c", "note": 3, "stabilite_forcee": 21, "origine": "quiz"},
            "examen": {"score": 0.75, "region": "droit"},
            "erreur": {"carte": "c"},
            "seance": {"format": "seance", "graine": 0, "banque_version": "v1", "moteur_version": "v1"},
            "synthese": {"chapitre": "droit.fixture", "attendus_coches": [0]},
            "signalement": {"carte": "c"},
        }
        for mode, champs in cas.items():
            valide = {"mode": mode, "quand": "2026-09-04T10:00:00+00:00", "nonce": f"fixture-{mode}", **champs}
            for champ in champs:
                with self.subTest(mode=mode, absent=champ):
                    incomplete = {k: v for k, v in valide.items() if k != champ}
                    statut, _, reponse = self.envoie([incomplete])
                    self.assertEqual(statut, 422)
                    self.assertEqual(reponse["index"], 0)
            self.assertEqual(self.envoie([valide])[0], 200)
        self.assertEqual(self.envoie([{
            "mode": "examen", "quand": "2026-09-04T10:00:00+00:00",
            "nonce": "fixture-dossier", "score": 1, "dossier": "droit.fixture",
        }])[0], 200)

    def test_types_et_horodatages_du_contrat(self):
        invalides = [
            {"quand": "2026-09-04"}, {"quand": "2026-09-04T10:00:00"},
            {"confiance": "oui"}, {"graine": []}, {"graine": True},
            {"duree_ms": True}, {"score": True},
            {"stabilite_forcee": float("nan")}, {"stabilite_forcee": float("inf")},
            {"attendus_coches": [True]}, {"attendus_coches": ["0"]},
            {"motif": "x" * 301}, {"motif": []},
        ]
        for champs in invalides:
            with self.subTest(champs=champs):
                self.assertEqual(self.envoie([ligne(1, **champs)])[0], 422)
        self.assertEqual(self.envoie([ligne(1, confiance=False, graine=0, duree_ms=0)])[0], 200)

    def test_modes_et_champs(self):
        s, _, r = self.envoie([ligne(1, mode="danse")])
        self.assertEqual((s, r["index"]), (422, 0))
        s, _, r = self.envoie([{"quand": "2026-09-03T08:00:00+00:00", "mode": "erreur", "nonce": "abcdefgh", "carte": "c", "raison": "x"}])
        self.assertEqual(s, 200)
        s, _, r = self.envoie([ligne(2, nonce="court")])
        self.assertEqual(s, 422)
        s, _, r = self.envoie([ligne(3, quand="hier")])
        self.assertEqual(s, 422)

    def test_isolation_entre_profils(self):
        from academie_etat import auth
        p2 = auth.creer_profil(self.appli.conn, "Autre")
        j2 = auth.creer_jeton(self.appli.conn, p2, "outil")
        self.envoie([ligne(1)])
        _, _, r = self.envoie([], jeton=j2)
        self.assertEqual(r["manquantes"], [])

    def test_sans_session(self):
        s, _, r = requete(self.appli, "POST", "/journal", {"lignes": []})
        self.assertEqual((s, r["erreur"]), (401, "non-authentifie"))

    def test_sante(self):
        s, _, r = requete(self.appli, "GET", "/sante")
        self.assertTrue(r["ok"] and "journal-v1" in r["contrats"])


if __name__ == "__main__":
    unittest.main()

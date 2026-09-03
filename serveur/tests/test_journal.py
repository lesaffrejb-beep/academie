import unittest

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
        self.assertEqual(r3["manquantes"], [])

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

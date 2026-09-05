import unittest
from datetime import timedelta

from commun import application, requete
from academie_etat import auth


class Auth(unittest.TestCase):
    def setUp(self):
        self.appli, self.profil, self.jeton = application()
        self.conn = self.appli.conn

    def test_jeton_hache_jamais_en_clair(self):
        rows = [r[0] for r in self.conn.execute("SELECT jeton_hache FROM sessions")]
        self.assertNotIn(self.jeton, rows)
        self.assertEqual(rows, [auth.hacher(self.jeton)])

    def test_expiration(self):
        j = auth.creer_jeton(self.conn, self.profil, "outil", duree=timedelta(seconds=-1))
        self.assertIsNone(auth.verifier(self.conn, j))
        self.assertEqual(auth.verifier(self.conn, self.jeton), self.profil)

    def test_revocation(self):
        self.assertTrue(auth.revoquer(self.conn, self.jeton))
        self.assertIsNone(auth.verifier(self.conn, self.jeton))
        self.assertFalse(auth.revoquer(self.conn, self.jeton))

    def test_magic_link_usage_unique(self):
        magic = auth.creer_jeton(self.conn, self.profil, "magic")
        self.assertIsNone(auth.verifier(self.conn, magic), "un lien magique n'est pas une session")
        s, e, r = requete(self.appli, "GET", f"/auth/lien?jeton={magic}")
        self.assertEqual(s, 200)
        cookie = e["set-cookie"].split(";")[0].split("=", 1)[1]
        self.assertEqual(auth.verifier(self.conn, cookie), self.profil)
        s, _, r = requete(self.appli, "GET", f"/auth/lien?jeton={magic}")
        self.assertEqual((s, r["erreur"]), (401, "lien-invalide"))
        s, _, r = requete(self.appli, "GET", "/profil", cookie=cookie)
        self.assertEqual((s, r["id"]), (200, self.profil))

    def test_deconnexion(self):
        magic = auth.creer_jeton(self.conn, self.profil, "magic")
        _, e, _ = requete(self.appli, "GET", f"/auth/lien?jeton={magic}")
        cookie = e["set-cookie"].split(";")[0].split("=", 1)[1]
        requete(self.appli, "POST", "/auth/deconnexion", cookie=cookie, profil=self.profil)
        s, _, _ = requete(self.appli, "GET", "/profil", cookie=cookie)
        self.assertEqual(s, 401)

    def test_suppression_sous_48h(self):
        s, _, r = requete(self.appli, "DELETE", "/profil", jeton=self.jeton)
        self.assertEqual(s, 202)
        self.assertIsNone(auth.verifier(self.conn, self.jeton))
        self.assertEqual(auth.purger(self.conn), 0, "pas avant 48 h")
        self.assertEqual(auth.purger(self.conn, timedelta(seconds=0)), 1)
        self.assertIsNone(self.conn.execute("SELECT 1 FROM profils WHERE id = ?", (self.profil,)).fetchone())

    def test_reglages(self):
        s, _, r = requete(self.appli, "PATCH", "/profil", {"theme": "papier", "inconnu": 1}, jeton=self.jeton)
        self.assertEqual((s, r["reglages"]), (200, {"theme": "papier"}))


if __name__ == "__main__":
    unittest.main()

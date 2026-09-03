"""Le serveur sur une vraie socket : une requête HTTP de bout en bout."""
import json
import threading
import unittest
import urllib.request

from commun import application
from academie_etat import PREFIXE
from academie_etat.app import fabrique_handler
from http.server import ThreadingHTTPServer


class Http(unittest.TestCase):
    def test_sante_et_journal_par_socket(self):
        appli, profil, jeton = application()
        srv = ThreadingHTTPServer(("127.0.0.1", 0), fabrique_handler(appli))
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            base = f"http://127.0.0.1:{port}{PREFIXE}"
            with urllib.request.urlopen(base + "/sante", timeout=5) as r:
                self.assertTrue(json.loads(r.read())["ok"])
            corps = json.dumps({"depuis": None, "lignes": [{"quand": "2026-09-03T08:00:00+00:00", "mode": "revision",
                                                            "nonce": "nonce-http-1", "carte": "c", "note": 3}]}).encode()
            req = urllib.request.Request(base + "/journal", data=corps, method="POST",
                                         headers={"Authorization": f"Bearer {jeton}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=5) as r:
                self.assertEqual(json.loads(r.read())["acceptees"], 1)
            req = urllib.request.Request(base + "/journal/export", headers={"Authorization": f"Bearer {jeton}"})
            with urllib.request.urlopen(req, timeout=5) as r:
                self.assertIn("nonce-http-1", r.read().decode())
            with self.assertRaises(urllib.error.HTTPError) as cm:
                urllib.request.urlopen(base + "/profil", timeout=5)
            self.assertEqual(cm.exception.code, 401)
        finally:
            srv.shutdown()


if __name__ == "__main__":
    unittest.main()

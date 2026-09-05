#!/usr/bin/env python3
"""Le build et l'API sur une seule origine locale, état hors Git.

python3 serveur/essai_local.py --port 5186
Ne déploie rien et n'ouvre aucune interface réseau publique.
"""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from academie_etat import db
from academie_etat.app import Application, fabrique_handler

RACINE = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=5186)
    ap.add_argument("--base", type=Path, default=RACINE / "etat" / "essai-local.sqlite")
    args = ap.parse_args()
    if not (RACINE / "web/dist/index.html").is_file():
        ap.error("Construis le client avec npm --prefix web run build.")
    args.base.parent.mkdir(parents=True, exist_ok=True)
    conn = db.connecter(args.base)
    api_handler = fabrique_handler(Application(conn, securise=False))

    class Handler(api_handler, SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            self.directory = str(RACINE / "web/dist")
            super().__init__(*a, directory=self.directory, **kw)

        def do_GET(self):
            if urlsplit(self.path).path.startswith("/academie/api/"):
                return self._servir()
            if not self.path.startswith("/academie/"):
                self.send_response(302)
                self.send_header("Location", "/academie/")
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            self.path = self.path[len("/academie"):]
            return SimpleHTTPRequestHandler.do_GET(self)

        def do_HEAD(self):
            self.send_error(405)

    srv = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Essai local : http://127.0.0.1:{args.port}/academie/", flush=True)
    print(f"Sauvegarde dédiée : {args.base}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
        conn.close()


if __name__ == "__main__":
    main()

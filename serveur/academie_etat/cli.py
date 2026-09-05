"""`academie-etat` : l'outil de ligne de commande de JB sur le VPS.

    python3 -m academie_etat servir --base /var/lib/academie/etat.sqlite --port 8790
    python3 -m academie_etat profil creer "JB" [--mail x]
    python3 -m academie_etat profil lister
    python3 -m academie_etat lien <profil>           # magic link, 24 h, usage unique
    python3 -m academie_etat jeton <profil>          # jeton d'outil (Bearer), un an
    python3 -m academie_etat purger                  # efface les profils supprimés depuis 48 h
    python3 -m academie_etat importer <profil> <revues.jsonl> [--erreurs erreurs.jsonl]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from . import PREFIXE, auth, db


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="academie-etat")
    ap.add_argument("--base", default=os.environ.get("ACADEMIE_ETAT_BASE", "/var/lib/academie/etat.sqlite"))
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("servir"); s.add_argument("--hote", default="127.0.0.1"); s.add_argument("--port", type=int, default=8790)
    s.add_argument("--sans-secure", action="store_true", help="cookie sans Secure (développement en http)")
    p = sp.add_parser("profil"); p.add_argument("action", choices=("creer", "lister")); p.add_argument("titre", nargs="?"); p.add_argument("--mail")
    l = sp.add_parser("lien"); l.add_argument("profil"); l.add_argument("--origine", default="https://vps-5a3d618c.vps.ovh.net")
    j = sp.add_parser("jeton"); j.add_argument("profil"); j.add_argument("--appareil", default="outil")
    sp.add_parser("purger")
    sp.add_parser("demandes")
    i = sp.add_parser("importer"); i.add_argument("profil"); i.add_argument("revues"); i.add_argument("--erreurs")
    args = ap.parse_args(argv)

    conn = db.connecter(args.base)
    if args.cmd == "servir":
        from .app import servir
        srv = servir(conn, args.hote, args.port, securise=not args.sans_secure)
        print(f"academie-etat sur http://{args.hote}:{args.port}{PREFIXE} (base {args.base})", flush=True)
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            pass
        return 0
    if args.cmd == "profil":
        if args.action == "creer":
            if not args.titre:
                ap.error("titre attendu")
            print(auth.creer_profil(conn, args.titre, args.mail))
        else:
            for r in conn.execute("SELECT id, titre_affiche, cree_le, supprime_le FROM profils ORDER BY cree_le"):
                print(f"{r['id']}  {r['titre_affiche']}  {r['cree_le']}" + ("  (suppression demandée)" if r["supprime_le"] else ""))
        return 0
    if args.cmd == "lien":
        jeton = auth.creer_jeton(conn, args.profil, "magic")
        print(f"{args.origine}{PREFIXE}/auth/lien?jeton={jeton}")
        return 0
    if args.cmd == "jeton":
        print(auth.creer_jeton(conn, args.profil, "outil", args.appareil))
        return 0
    if args.cmd == "demandes":
        for row in conn.execute("SELECT id, profil, texte, cree_le FROM demandes_cursus ORDER BY cree_le"):
            print(dict(row))
        return 0
    if args.cmd == "purger":
        print(f"{auth.purger(conn)} profil(s) effacé(s)")
        return 0
    if args.cmd == "importer":
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from importer_journal import importer_dans_base
        res = importer_dans_base(conn, args.profil, Path(args.revues), Path(args.erreurs) if args.erreurs else None)
        print(f"{res['lues']} ligne(s) lue(s), {res['acceptees']} ajoutée(s), {res['ignorees']} déjà connue(s), {res['illisibles']} illisible(s)")
        return 0
    return 1

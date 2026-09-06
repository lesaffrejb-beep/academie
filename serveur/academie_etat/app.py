"""Les routes (serveur/API.md), sur `http.server` de la stdlib, un seul
processus derrière Caddy. Ce qui n'est pas dans ce fichier n'existe pas :
ni banques, ni livraisons, ni cercles avant leurs chantiers."""
from __future__ import annotations

import json
import ipaddress
import sqlite3
import threading
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from . import CONTRATS, PREFIXE, VERSION, auth, boite, journal

COOKIE = "academie_session"
CORPS_MAX = 2_000_000


def adresse_origine(pair: str, transmis: str) -> str:
    # Caddy sur loopback ajoute le pair réel en fin de X-Forwarded-For.
    # Un hôte directement exposé ne fait jamais confiance à cet en-tête.
    try:
        if ipaddress.ip_address(pair).is_loopback and transmis:
            return str(ipaddress.ip_address(transmis.split(",")[-1].strip()))
    except ValueError:
        pass
    return pair


class Refus(Exception):
    def __init__(self, statut: int, code: str, motif: str, **extra):
        super().__init__(motif)
        self.statut, self.code, self.motif, self.extra = statut, code, motif, extra


class Application:
    """Le routeur, testable sans socket : `traiter(methode, chemin, corps, entetes)`."""

    def __init__(self, conn: sqlite3.Connection, securise: bool = True):
        self.conn = conn
        self.securise = securise
        self.verrou = threading.RLock()

    # --- outillage -------------------------------------------------------
    def _jeton(self, entetes: dict) -> str | None:
        autorisation = entetes.get("authorization", "")
        if autorisation.lower().startswith("bearer "):
            return autorisation[7:].strip()
        cookies = SimpleCookie(entetes.get("cookie", ""))
        return cookies[COOKIE].value if COOKIE in cookies else None

    def _profil(self, entetes: dict, identite_requise: bool = True) -> str:
        profil = auth.verifier(self.conn, self._jeton(entetes))
        if profil is None:
            raise Refus(401, "non-authentifie", "session absente, expirée ou révoquée")
        attendu = entetes.get("x-academie-profil")
        outil = entetes.get("authorization", "").lower().startswith("bearer ")
        if identite_requise and not outil and not attendu:
            raise Refus(409, "client-a-recharger", "Recharge Académie pour ouvrir ton compte. Les réponses de cet ancien onglet restent sur cet appareil.")
        if attendu and attendu != profil:
            raise Refus(409, "compte-change", "Le compte a changé dans un autre onglet. Reconnecte-toi ; tes réponses restent sur cet appareil.")
        return profil

    def _cookie(self, jeton: str, duree_s: int = 365 * 86400) -> str:
        secure = "; Secure" if self.securise else ""
        return f"{COOKIE}={jeton}; Path={PREFIXE}; Max-Age={duree_s}; HttpOnly; SameSite=Strict{secure}"

    # --- routes ----------------------------------------------------------
    def traiter(self, methode: str, chemin: str, corps: bytes, entetes: dict) -> tuple[int, dict, bytes]:
        """Rend (statut, en-têtes, corps). Les en-têtes sont en minuscules."""
        try:
            # Une connexion SQLite partagée : protéger lectures et transactions.
            with self.verrou:
                return self._router(methode, chemin, corps, entetes)
        except Refus as r:
            return self._json(r.statut, {"erreur": r.code, "motif": r.motif, **r.extra})
        except journal.LigneInvalide as e:
            return self._json(422, {"erreur": "ligne-invalide", "motif": e.motif, "index": e.index})

    def _router(self, methode, chemin, corps, entetes):
        url = urlparse(chemin)
        route = url.path
        if route.startswith(PREFIXE):
            route = route[len(PREFIXE):] or "/"
        params = parse_qs(url.query)

        if route == "/sante" and methode == "GET":
            return self._json(200, {"ok": True, "moteur_version": VERSION, "contrats": CONTRATS})

        if route in ("/compte", "/auth/connexion", "/auth/recuperation") and methode == "POST":
            data = self._corps(corps)
            auth.limiter(self.conn, "origine:" + entetes.get("x-adresse-pair", "local"), 100)
            fonction = {"/compte": auth.inscrire, "/auth/connexion": auth.connecter_compte,
                        "/auth/recuperation": auth.recuperer_compte}[route]
            profil, jeton = fonction(self.conn, data, entetes.get("user-agent", "")[:120])
            return self._json(201 if route == "/compte" else 200, profil, {"set-cookie": self._cookie(jeton)})

        if route == "/auth/comptes" and methode == "GET":
            return self._json(200, {"comptes": auth.comptes_connexion(self.conn)})

        if route == "/eleves" and methode == "GET":
            self._profil(entetes)
            return self._json(200, {"eleves": auth.eleves(self.conn)})

        if route == "/demandes-cursus" and methode == "POST":
            profil = self._profil(entetes)
            return self._json(201, auth.demander_cursus(self.conn, profil, self._corps(corps)))

        if route == "/auth/deconnexion" and methode == "POST":
            self._profil(entetes)
            jeton = self._jeton(entetes)
            with self.verrou:
                auth.revoquer(self.conn, jeton or "")
            return self._json(200, {"ok": True}, {"set-cookie": self._cookie("", 0)})

        if route == "/journal" and methode == "POST":
            profil = self._profil(entetes)
            data = self._corps(corps)
            with self.verrou:
                res = journal.fusionner(self.conn, profil, data.get("lignes"), data.get("depuis"))
            return self._json(200, res)

        if route == "/journal/export" and methode == "GET":
            profil = self._profil(entetes)
            lignes = journal.exporter(self.conn, profil)
            texte = "".join(json.dumps(l, ensure_ascii=False, sort_keys=True) + "\n" for l in lignes)
            return (200, {"content-type": "application/x-ndjson; charset=utf-8",
                          "content-disposition": 'attachment; filename="journal.jsonl"'}, texte.encode("utf-8"))

        if route == "/profil":
            profil = self._profil(entetes, identite_requise=methode != "GET")
            if methode == "GET":
                return self._json(200, auth.profil_public(self.conn, profil))
            if methode == "PATCH":
                with self.verrou:
                    reglages = auth.modifier_reglages(self.conn, profil, self._corps(corps))
                return self._json(200, {"ok": True, "reglages": reglages})
            if methode == "DELETE":
                with self.verrou:
                    quand = auth.demander_suppression(self.conn, profil)
                return self._json(202, {"ok": True, "suppression_demandee_le": quand, "effacement": "sous 48 h"},
                                  {"set-cookie": self._cookie("", 0)})

        if route == "/boite":
            profil = self._profil(entetes)
            if methode == "POST":
                with self.verrou:
                    entree = boite.deposer(self.conn, profil, self._corps(corps))
                return self._json(201, entree)
            if methode == "GET":
                return self._json(200, {"entrees": boite.lister(self.conn, profil)})
        if route.startswith("/boite/") and methode == "PATCH":
            profil = self._profil(entetes)
            with self.verrou:
                entree = boite.modifier(self.conn, profil, route[len("/boite/"):], self._corps(corps))
            return self._json(200, entree)

        raise Refus(404, "route-inconnue", f"{methode} {route} n'existe pas")

    def _corps(self, corps: bytes) -> dict:
        if not corps:
            return {}
        try:
            data = json.loads(corps.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise Refus(400, "json-illisible", "le corps n'est pas du JSON")
        if not isinstance(data, dict):
            raise Refus(400, "json-illisible", "le corps doit être un objet")
        return data

    @staticmethod
    def _json(statut: int, data, entetes: dict | None = None) -> tuple[int, dict, bytes]:
        e = {"content-type": "application/json; charset=utf-8", "cache-control": "no-store"}
        e.update(entetes or {})
        return statut, e, json.dumps(data, ensure_ascii=False).encode("utf-8")


def fabrique_handler(application: Application):
    class Handler(BaseHTTPRequestHandler):
        server_version = "academie-etat/1"
        protocol_version = "HTTP/1.1"

        def _servir(self):
            taille = int(self.headers.get("Content-Length") or 0)
            if taille > CORPS_MAX:
                self._repondre(413, {"content-type": "application/json"}, b'{"erreur":"corps-trop-gros","motif":"2 Mo au plus"}')
                self.rfile.read(taille)
                return
            corps = self.rfile.read(taille) if taille else b""
            if self.command in ("POST", "PATCH") and taille and self.headers.get("Content-Type", "").split(";",1)[0].strip().lower() != "application/json":
                self._repondre(415, {"content-type":"application/json"}, b'{"erreur":"type-invalide","motif":"application/json requis"}')
                return
            entetes = {k.lower(): v for k, v in self.headers.items()}
            # Le pair socket fait foi ; ignorer un en-tête envoyé par le navigateur.
            entetes["x-adresse-pair"] = adresse_origine(self.client_address[0], entetes.get("x-forwarded-for", ""))
            statut, e, donnees = application.traiter(self.command, self.path, corps, entetes)
            self._repondre(statut, e, donnees)

        def _repondre(self, statut, entetes, donnees):
            self.send_response(statut)
            for k, v in entetes.items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(donnees)))
            self.end_headers()
            self.wfile.write(donnees)

        do_GET = do_POST = do_PATCH = do_DELETE = _servir

        def log_message(self, fmt, *args):  # pas de journal d'accès avec des chemins : Caddy s'en charge
            pass

    return Handler


def servir(conn: sqlite3.Connection, hote: str = "127.0.0.1", port: int = 8790, securise: bool = True):
    application = Application(conn, securise=securise)
    serveur = ThreadingHTTPServer((hote, port), fabrique_handler(application))
    serveur.daemon_threads = True
    return serveur

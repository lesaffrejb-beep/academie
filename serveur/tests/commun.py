"""Outillage partagé des tests du serveur : base en mémoire, application
sans socket, requêtes en une ligne."""
from __future__ import annotations

import json
import sys
from pathlib import Path

SERVEUR = Path(__file__).resolve().parents[1]
RACINE = SERVEUR.parent
for p in (SERVEUR, RACINE / "app"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from academie_etat import PREFIXE, auth, db  # noqa: E402
from academie_etat.app import Application  # noqa: E402


def application() -> tuple[Application, str, str]:
    """Une application sur base vide, un profil, son jeton d'outil."""
    conn = db.connecter(":memory:")
    profil = auth.creer_profil(conn, "Test")
    jeton = auth.creer_jeton(conn, profil, "outil")
    return Application(conn, securise=False), profil, jeton


def requete(appli: Application, methode: str, route: str, corps=None, jeton: str | None = None,
            cookie: str | None = None) -> tuple[int, dict, object]:
    entetes = {}
    if jeton:
        entetes["authorization"] = f"Bearer {jeton}"
    if cookie:
        entetes["cookie"] = f"academie_session={cookie}"
    donnees = json.dumps(corps).encode("utf-8") if corps is not None else b""
    statut, e, sortie = appli.traiter(methode, PREFIXE + route, donnees, entetes)
    if e.get("content-type", "").startswith("application/json"):
        return statut, e, json.loads(sortie.decode("utf-8"))
    return statut, e, sortie.decode("utf-8")


def ligne(i: int, **maj) -> dict:
    base = {"quand": f"2026-09-03T08:{i % 60:02d}:00+00:00", "mode": "revision", "format": "seance",
            "nonce": f"nonce-{i:06d}", "carte": f"carte-{i}", "note": 3}
    base.update(maj)
    return base

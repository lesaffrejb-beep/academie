"""La boîte : file d'attente texte d'un profil (serveur/API.md). Les
fichiers ne montent jamais ici."""
from __future__ import annotations

import sqlite3
import uuid
from datetime import datetime, timezone

TYPES = ("texte", "lien", "note")
ETATS = ("a-traiter", "chapitre-propose", "rattache", "ecarte")


def _maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _refus(motif: str):
    from .app import Refus
    return Refus(422, "boite-invalide", motif)


def deposer(conn: sqlite3.Connection, profil: str, data: dict) -> dict:
    if data.get("type") not in TYPES:
        raise _refus("`type` doit être texte, lien ou note")
    contenu = data.get("contenu")
    if not isinstance(contenu, str) or not contenu.strip() or len(contenu) > 20000:
        raise _refus("`contenu` doit être un texte non vide de 20 000 caractères au plus")
    eid, quand = str(uuid.uuid4()), _maintenant()
    conn.execute("INSERT INTO boite (id, profil, type, contenu, etat, cree_le, maj_le) VALUES (?, ?, ?, ?, 'a-traiter', ?, ?)",
                 (eid, profil, data["type"], contenu.strip(), quand, quand))
    return {"id": eid, "etat": "a-traiter"}


def lister(conn: sqlite3.Connection, profil: str) -> list[dict]:
    return [dict(r) for r in conn.execute(
        "SELECT id, type, contenu, etat, chapitre, cree_le, maj_le FROM boite WHERE profil = ? ORDER BY cree_le", (profil,))]


def modifier(conn: sqlite3.Connection, profil: str, eid: str, data: dict) -> dict:
    if data.get("etat") not in ETATS:
        raise _refus("`etat` inconnu")
    chapitre = data.get("chapitre")
    if chapitre is not None and not isinstance(chapitre, str):
        raise _refus("`chapitre` doit être un texte")
    cur = conn.execute("UPDATE boite SET etat = ?, chapitre = COALESCE(?, chapitre), maj_le = ? WHERE id = ? AND profil = ?",
                       (data["etat"], chapitre, _maintenant(), eid, profil))
    if cur.rowcount != 1:
        from .app import Refus
        raise Refus(404, "entree-inconnue", "cette entrée n'est pas dans votre boîte")
    return dict(conn.execute("SELECT id, type, etat, chapitre, maj_le FROM boite WHERE id = ?", (eid,)).fetchone())

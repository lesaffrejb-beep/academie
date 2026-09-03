"""Profils, jetons et sessions. Un jeton n'est jamais stocké en clair :
la table `sessions` porte son SHA-256. Trois genres : `magic` (lien à
usage unique, court), `cookie` (session d'un an), `outil` (Bearer pour
les outils de la machine)."""
from __future__ import annotations

import hashlib
import json
import secrets
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone

DUREES = {"magic": timedelta(hours=24), "cookie": timedelta(days=365), "outil": timedelta(days=365)}


def maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hacher(jeton: str) -> str:
    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()


def creer_profil(conn: sqlite3.Connection, titre_affiche: str, mail: str | None = None) -> str:
    pid = str(uuid.uuid4())
    conn.execute("INSERT INTO profils (id, mail, titre_affiche, cree_le) VALUES (?, ?, ?, ?)",
                 (pid, mail, titre_affiche, maintenant()))
    return pid


def creer_jeton(conn: sqlite3.Connection, profil: str, genre: str, appareil: str | None = None,
                duree: timedelta | None = None) -> str:
    if genre not in DUREES:
        raise ValueError(f"genre de jeton inconnu : {genre}")
    jeton = secrets.token_urlsafe(32)
    quand = datetime.now(timezone.utc)
    expire = quand + (duree or DUREES[genre])
    conn.execute("INSERT INTO sessions (jeton_hache, profil, genre, cree_le, expire_le, appareil) VALUES (?, ?, ?, ?, ?, ?)",
                 (hacher(jeton), profil, genre, quand.isoformat(timespec="seconds"),
                  expire.isoformat(timespec="seconds"), appareil))
    return jeton


def verifier(conn: sqlite3.Connection, jeton: str | None, genres: tuple[str, ...] = ("cookie", "outil")) -> str | None:
    """Rend l'identifiant du profil si le jeton est valide, sinon None."""
    if not jeton:
        return None
    row = conn.execute("SELECT profil, genre, expire_le, revoque_le FROM sessions WHERE jeton_hache = ?",
                       (hacher(jeton),)).fetchone()
    if row is None or row["genre"] not in genres or row["revoque_le"]:
        return None
    if row["expire_le"] <= maintenant():
        return None
    prof = conn.execute("SELECT supprime_le FROM profils WHERE id = ?", (row["profil"],)).fetchone()
    if prof is None or prof["supprime_le"]:
        return None
    return row["profil"]


def revoquer(conn: sqlite3.Connection, jeton: str) -> bool:
    cur = conn.execute("UPDATE sessions SET revoque_le = ? WHERE jeton_hache = ? AND revoque_le IS NULL",
                       (maintenant(), hacher(jeton)))
    return cur.rowcount == 1


def echanger_magic(conn: sqlite3.Connection, jeton: str, appareil: str | None = None) -> str | None:
    """Un lien magique s'échange une fois contre un cookie d'un an."""
    profil = verifier(conn, jeton, genres=("magic",))
    if profil is None:
        return None
    revoquer(conn, jeton)
    return creer_jeton(conn, profil, "cookie", appareil)


def profil_public(conn: sqlite3.Connection, pid: str) -> dict | None:
    row = conn.execute("SELECT id, titre_affiche, cree_le, reglages, supprime_le FROM profils WHERE id = ?", (pid,)).fetchone()
    if row is None:
        return None
    domaines = [r["domaine"] for r in conn.execute("SELECT domaine FROM adoptions WHERE profil = ? ORDER BY adopte_le", (pid,))]
    return {"id": row["id"], "titre_affiche": row["titre_affiche"], "cree_le": row["cree_le"],
            "reglages": json.loads(row["reglages"] or "{}"), "domaines": domaines,
            "suppression_demandee_le": row["supprime_le"]}


def modifier_reglages(conn: sqlite3.Connection, pid: str, maj: dict) -> dict:
    row = conn.execute("SELECT reglages FROM profils WHERE id = ?", (pid,)).fetchone()
    reglages = json.loads(row["reglages"] or "{}")
    for cle in ("theme", "semaine_type", "notifications", "visibilite", "titre_affiche"):
        if cle in maj:
            reglages[cle] = maj[cle]
    conn.execute("UPDATE profils SET reglages = ? WHERE id = ?", (json.dumps(reglages, ensure_ascii=False), pid))
    if isinstance(maj.get("titre_affiche"), str) and maj["titre_affiche"].strip():
        conn.execute("UPDATE profils SET titre_affiche = ? WHERE id = ?", (maj["titre_affiche"].strip(), pid))
    return reglages


def demander_suppression(conn: sqlite3.Connection, pid: str) -> str:
    quand = maintenant()
    conn.execute("UPDATE profils SET supprime_le = COALESCE(supprime_le, ?) WHERE id = ?", (quand, pid))
    conn.execute("UPDATE sessions SET revoque_le = COALESCE(revoque_le, ?) WHERE profil = ?", (quand, pid))
    return quand


def purger(conn: sqlite3.Connection, delai: timedelta = timedelta(hours=48)) -> int:
    """Efface pour de bon les profils dont la suppression a plus de 48 h (cascade)."""
    limite = (datetime.now(timezone.utc) - delai).isoformat(timespec="seconds")
    cur = conn.execute("DELETE FROM profils WHERE supprime_le IS NOT NULL AND supprime_le <= ?", (limite,))
    return cur.rowcount

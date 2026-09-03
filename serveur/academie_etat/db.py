"""Connexion SQLite et migrations numérotées (serveur/migrations/NNNN_*.sql)."""
from __future__ import annotations

import sqlite3
from pathlib import Path

MIGRATIONS = Path(__file__).resolve().parents[1] / "migrations"


def connecter(chemin: str | Path = ":memory:") -> sqlite3.Connection:
    conn = sqlite3.connect(str(chemin), check_same_thread=False, isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    if str(chemin) != ":memory:":
        conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA busy_timeout = 5000")
    migrer(conn)
    return conn


def migrer(conn: sqlite3.Connection) -> list[str]:
    conn.execute("CREATE TABLE IF NOT EXISTS migrations (nom TEXT PRIMARY KEY, appliquee_le TEXT NOT NULL)")
    faites = {r[0] for r in conn.execute("SELECT nom FROM migrations")}
    appliquees = []
    for f in sorted(MIGRATIONS.glob("[0-9][0-9][0-9][0-9]_*.sql")):
        if f.name in faites:
            continue
        # executescript valide lui-même chaque instruction ; une migration
        # qui casse à mi-chemin se voit à la relance (nom absent de la table).
        conn.executescript(f.read_text(encoding="utf-8"))
        conn.execute("INSERT INTO migrations VALUES (?, datetime('now'))", (f.name,))
        appliquees.append(f.name)
    return appliquees

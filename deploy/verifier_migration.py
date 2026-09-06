"""Compare les anciennes tables SQLite sans afficher leurs données.

ACA-PUBLICATION-2 : une migration peut ajouter un schéma, pas perdre un
journal. Les deux bases s'ouvrent en lecture seule et restent sur leur hôte.
"""
from __future__ import annotations
from contextlib import closing
import argparse
import json
from pathlib import Path
import sqlite3


def identifiant(nom: str) -> str:
    return '"' + nom.replace('"', '""') + '"'


def uri(chemin: Path) -> str:
    if not chemin.is_file():
        raise FileNotFoundError(chemin)
    return chemin.resolve().as_uri() + "?mode=ro"


def compare(avant: Path, apres: Path) -> dict[str, int]:
    with closing(sqlite3.connect(uri(apres), uri=True)) as conn:
        conn.execute("ATTACH DATABASE ? AS avant", (uri(avant),))
        conn.execute("PRAGMA query_only = ON")
        for schema in ("main", "avant"):
            if conn.execute(f"PRAGMA {schema}.quick_check").fetchone()[0] != "ok":
                raise ValueError(f"Intégrité incorrecte : {schema}")
            if conn.execute(f"PRAGMA {schema}.foreign_key_check").fetchone():
                raise ValueError(f"Clé étrangère incorrecte : {schema}")
        tables = [r[0] for r in conn.execute("SELECT name FROM avant.sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name <> 'migrations'")]
        apres_tables = {r[0] for r in conn.execute("SELECT name FROM main.sqlite_master WHERE type='table'")}
        comptes = {}
        for table in tables:
            nom = identifiant(table)
            if table not in apres_tables:
                raise ValueError(f"Table disparue : {table}")
            colonnes = [r[1] for r in conn.execute(f"PRAGMA avant.table_info({nom})")]
            disponibles = {r[1] for r in conn.execute(f"PRAGMA main.table_info({nom})")}
            manque = set(colonnes) - disponibles
            if manque:
                raise ValueError(f"Colonnes disparues de {table} : {', '.join(sorted(manque))}")
            selection = ", ".join(f"typeof({identifiant(c)}), {identifiant(c)} COLLATE BINARY" for c in colonnes)
            ancien = conn.execute(f"SELECT COUNT(*) FROM avant.{nom}").fetchone()[0]
            nouveau = conn.execute(f"SELECT COUNT(*) FROM main.{nom}").fetchone()[0]
            if ancien != nouveau:
                raise ValueError(f"Nombre de lignes modifié : {table}")
            for gauche, droite in (("avant", "main"), ("main", "avant")):
                if conn.execute(f"SELECT {selection}, COUNT(*) FROM {gauche}.{nom} GROUP BY {selection} EXCEPT SELECT {selection}, COUNT(*) FROM {droite}.{nom} GROUP BY {selection} LIMIT 1").fetchone():
                    raise ValueError(f"Lignes modifiées : {table}")
            comptes[table] = ancien
        return comptes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--avant", type=Path, required=True)
    parser.add_argument("--apres", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps({"tables_conservees": compare(args.avant, args.apres)}, ensure_ascii=False))
        return 0
    except (ValueError, OSError, sqlite3.Error) as erreur:
        print(f"Conservation non prouvée : {erreur}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

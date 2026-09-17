#!/usr/bin/env python3
"""Installe le hook pre-commit du garde-fou (chantier ACA-PRECOMMIT-1).

Idempotent : écrit `.git/hooks/pre-commit` s'il est absent, le remplace
s'il a été posé par ce même script (marque `academie-precommit`), et
refuse d'écraser un hook inconnu. Le hook appelle le garde, qui lit le
diff stágé et bloque sur un motif de donnée client (règle 1, AGENTS.md).
"""

from __future__ import annotations

import os
import stat
import sys
from pathlib import Path

APPEL = "# academie-precommit\n"
MARQUEUR = "academie-precommit"


def contenu_hook(racine: Path) -> str:
    python = Path(__file__).resolve().parent / "garde_confidentialite.py"
    return (APPEL
            + f'exec python3 "{python}" "$@"\n')


def installer(depot: Path | None = None) -> int:
    racine = depot or Path.cwd()
    cible = racine / ".git" / "hooks" / "pre-commit"
    if not (racine / ".git").is_dir():
        print("pas de dépôt git ici", file=sys.stderr)
        return 1
    if cible.is_file():
        texte = cible.read_text(encoding="utf-8", errors="replace")
        if MARQUEUR not in texte and texte.strip():
            print("pre-commit existant non académique : non touché",
                  file=sys.stderr)
            return 1
    if (Path(__file__).resolve().parent / "garde_confidentialite.py").is_file():
        texte = contenu_hook(racine)
    else:
        texte = APPEL + "exec python3 -c 'import sys; sys.exit(1)'\n"
    cible.parent.mkdir(parents=True, exist_ok=True)
    cible.write_text(texte, encoding="utf-8")
    cible.chmod(cible.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP
                | stat.S_IXOTH)
    print(f"hook installé : {cible}")
    return 0


if __name__ == "__main__":
    raise SystemExit(installer())

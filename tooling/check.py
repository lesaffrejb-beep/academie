#!/usr/bin/env python3
"""Contrôles structurels rapides du dépôt Académie."""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RE_OLD_REPO = re.compile(r"erp/app/etude|wiki-copro-sergic|\.claude/skills")


def main() -> int:
    errors: list[str] = []
    for required in ("AGENTS.md", "CLAUDE.md", "project.yaml", "ROADMAP.md", "roadmap.json", "context/giverny.md"):
        if not (ROOT / required).is_file():
            errors.append(f"fichier requis absent : {required}")
    for rel in ("project.yaml", "roadmap.json", "academie.json"):
        try:
            json.loads((ROOT / rel).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{rel} invalide : {exc}")
    for path in ROOT.rglob("*"):
        if path == Path(__file__) or not path.is_file() or ".git" in path.parts or path.suffix not in {".md", ".py", ".json", ".yaml", ".yml"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if RE_OLD_REPO.search(text):
            errors.append(f"ancien couplage technique dans {path.relative_to(ROOT)}")
    tracked_claude = subprocess.run(
        ["git", "ls-files", ".claude"], cwd=ROOT, capture_output=True, text=True
    ).stdout.strip()
    if tracked_claude:
        errors.append(".claude ne doit pas être versionné")
    for error in errors:
        print(f"ERREUR: {error}")
    print(f"Académie : {len(errors)} erreur(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Sélection prudente du prochain item local."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

data = json.loads((ROOT / "roadmap.json").read_text(encoding="utf-8"))
done = {item["id"] for item in data["items"] if item["status"] == "done"}
safe = [item for item in data["items"] if item["status"] == "ready"
        and item["mode"] in {"deterministic", "agent-safe"}
        and item["risk"] in {"low", "medium"}
        and set(item["depends_on"]).issubset(done)]
if not safe:
    print("Aucun item sûr et prêt. Aucun travail automatique lancé.")
else:
    print(json.dumps(max(safe, key=lambda item: item["priority"]), ensure_ascii=False, indent=2))

#!/usr/bin/env python3
"""Migration du journal v0 (etat/<profil>/revues.jsonl, erreurs.jsonl)
vers journal-v1 (CONTRAT-CARTE-V2.md §5, decisions/0006) :

  - `mode: "flash"` devient `mode: "revision"` avec `format: "seance"` ;
  - les lignes du quiz gardent `mode: "quiz"`, `origine` et
    `stabilite_forcee` ; `domaine` devient `region` ;
  - les lignes du carnet deviennent `mode: "erreur"` (carte, raison) ;
  - `nonce` = SHA-256 de la ligne v0 d'origine ; une ligne deja v1 garde
    son nonce et ses champs canoniques, pour ne pas compter deux fois
    un evenement deja synchronise. Le fichier source reste intact.

    python3 serveur/importer_journal.py etat/jb/revues.jsonl [--erreurs etat/jb/erreurs.jsonl] > journal-v1.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sqlite3
import sys
from pathlib import Path

MODES_V1 = ("revision", "quiz", "examen", "seance", "synthese", "signalement", "erreur")
CHAMPS_GARDES = (
    "carte", "note", "format", "duree_ms", "confiance", "stabilite_forcee", "origine",
    "region", "dossier", "score", "cartes", "raison", "jour", "graine", "cap",
    "banque_version", "moteur_version", "chapitre", "attendus_coches", "motif",
)


def _nonce(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def migrer_revue(texte: str) -> dict | None:
    """Une ligne v0 de revues.jsonl vers journal-v1 ; None si illisible."""
    try:
        v0 = json.loads(texte)
    except json.JSONDecodeError:
        return None
    if not isinstance(v0, dict) or not v0.get("quand"):
        return None
    mode = v0.get("mode", "flash")
    v1 = {"quand": v0["quand"], "nonce": _nonce(texte.strip())}
    if mode in MODES_V1 and "nonce" in v0:
        v1["nonce"] = v0["nonce"]
    if mode == "flash":
        v1["mode"], v1["format"] = "revision", "seance"
    elif mode == "quiz":
        v1["mode"] = "quiz"
    elif mode in MODES_V1:
        v1["mode"] = mode
    else:
        v1["mode"], v1["format"], v1["origine_v0"] = "revision", "seance", str(mode)
    for c in CHAMPS_GARDES:
        if c in v0 and v0[c] is not None:
            v1[c] = v0[c]
    if v0.get("domaine"):
        v1.setdefault("region", v0["domaine"])
    if "stabilite_forcee" in v1:
        try:
            stabilite = float(v1["stabilite_forcee"])
            if not math.isfinite(stabilite) or stabilite <= 0:
                del v1["stabilite_forcee"]
            else:
                v1["stabilite_forcee"] = stabilite
        except (TypeError, ValueError):
            del v1["stabilite_forcee"]
    if "note" in v1 and (not isinstance(v1["note"], int) or not 1 <= v1["note"] <= 4):
        del v1["note"]
    if v1["mode"] == "quiz" and "stabilite_forcee" not in v1:
        # Sans postulat de stabilite, le moteur v0 faisait une revision
        # normale. Le contrat v1 exige de la nommer ainsi.
        v1.update(mode="revision", format="seance", origine_v0="quiz")
    return v1


def migrer_erreur(texte: str) -> dict | None:
    try:
        v0 = json.loads(texte)
    except json.JSONDecodeError:
        return None
    if not isinstance(v0, dict) or not v0.get("quand") or not v0.get("carte"):
        return None
    v1 = {"quand": v0["quand"], "mode": "erreur", "carte": v0["carte"], "nonce": _nonce(texte.strip())}
    if isinstance(v0.get("raison"), str) and v0["raison"].strip():
        v1["raison"] = v0["raison"].strip()[:200]
    return v1


def migrer_fichier(revues: Path, erreurs: Path | None = None) -> tuple[list[dict], int]:
    lignes, illisibles = [], 0
    for chemin, fonction in ((revues, migrer_revue), (erreurs, migrer_erreur)):
        if chemin is None or not chemin.is_file():
            continue
        for texte in chemin.read_text(encoding="utf-8").splitlines():
            if not texte.strip():
                continue
            v1 = fonction(texte)
            if v1 is None:
                illisibles += 1
            else:
                lignes.append(v1)
    lignes.sort(key=lambda l: (l["quand"], l["mode"], l["nonce"]))
    return lignes, illisibles


def importer_dans_base(conn: sqlite3.Connection, profil: str, revues: Path, erreurs: Path | None = None) -> dict:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from academie_etat import journal
    lignes, illisibles = migrer_fichier(revues, erreurs)
    acceptees = ignorees = 0
    for i in range(0, len(lignes), journal.LOT_MAX):
        res = journal.fusionner(conn, profil, lignes[i:i + journal.LOT_MAX], depuis=None)
        acceptees += res["acceptees"]
        ignorees += res["ignorees"]
    return {"lues": len(lignes) + illisibles, "acceptees": acceptees, "ignorees": ignorees, "illisibles": illisibles}


def main() -> int:
    ap = argparse.ArgumentParser(description="Journal v0 vers journal-v1.")
    ap.add_argument("revues", type=Path)
    ap.add_argument("--erreurs", type=Path)
    args = ap.parse_args()
    lignes, illisibles = migrer_fichier(args.revues, args.erreurs)
    for l in lignes:
        print(json.dumps(l, ensure_ascii=False, sort_keys=True))
    if illisibles:
        print(f"{illisibles} ligne(s) illisible(s) ignorée(s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

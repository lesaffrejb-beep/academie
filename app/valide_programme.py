#!/usr/bin/env python3
"""Valideur du programme (`programme/<metier>.json`) et de son alignement
avec `academie.json`. Chantier ACA-PROGRAMME-1, écrit le 03/09/2026.

Ce qu'il refuse, sans dérogation :
  - un identifiant de chapitre dupliqué ;
  - un chapitre dans un domaine ou une branche non déclarés ;
  - un niveau hors 1-5 ; un prérequis inconnu ou de niveau supérieur
    (decisions/0003) ; un cycle de prérequis ;
  - un socle hors 1-5 ou sur un domaine inconnu ;
  - une semaine type à laquelle il manque un jour ;
  - une clé de `academie.json` absente du programme, l'inverse, un ordre
    différent, ou un domaine hors arbre remis dans l'arbre (les deux
    fichiers doivent dire la même chose : decisions/0023).

Usage :
    python3 app/valide_programme.py            # tous les programmes
    python3 app/valide_programme.py --json     # comptes en sortie machine

Sortie : 0 si tout passe, 1 s'il reste une erreur. Stdlib seule.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
ACADEMIE = Path(os.environ.get("ACADEMIE_RACINE") or RACINE)
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
NIVEAUX = range(1, 6)


def lire(f: Path) -> dict:
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"fichier illisible : {f} ({exc})")


def valider(prog: dict, academie: dict, nom: str) -> list[str]:
    err: list[str] = []
    domaines = prog.get("domaines", {})
    branches = prog.get("branches", {})
    chapitres = prog.get("chapitres", [])

    ids: dict[str, dict] = {}
    for ch in chapitres:
        cid = ch.get("id")
        if cid in ids:
            err.append(f"{nom} : identifiant dupliqué {cid}")
        ids[cid] = ch

    for ch in chapitres:
        cid = ch["id"]
        if ch.get("domaine") not in domaines:
            err.append(f"{nom} : {cid} dans un domaine non déclaré ({ch.get('domaine')})")
        elif ch.get("branche") not in {b["cle"] for b in branches.get(ch["domaine"], [])}:
            err.append(f"{nom} : {cid} dans une branche non déclarée ({ch.get('branche')})")
        niv = ch.get("niveau")
        if niv not in NIVEAUX:
            err.append(f"{nom} : {cid} a un niveau hors 1-5 ({niv})")
            continue
        for pre in ch.get("prerequis", []):
            if pre not in ids:
                err.append(f"{nom} : {cid} a un prérequis inconnu {pre}")
            elif ids[pre].get("niveau", 0) > niv:
                err.append(f"{nom} : {cid} a un prérequis de niveau supérieur ({pre})")

    etat: dict[str, int] = {}

    def visite(cid: str) -> None:
        if etat.get(cid) == 1:
            err.append(f"{nom} : cycle de prérequis via {cid}")
            return
        if etat.get(cid) == 2:
            return
        etat[cid] = 1
        for pre in ids.get(cid, {}).get("prerequis", []):
            if pre in ids:
                visite(pre)
        etat[cid] = 2

    for cid in ids:
        visite(cid)

    socle = prog.get("socle", {}).get("niveaux", {})
    for cle, niv in socle.items():
        if cle not in domaines:
            err.append(f"{nom} : socle sur un domaine inconnu ({cle})")
        if niv not in NIVEAUX:
            err.append(f"{nom} : socle hors 1-5 pour {cle} ({niv})")

    semaine = prog.get("semaine_type", {})
    manquants = [j for j in JOURS if j not in semaine]
    if manquants:
        err.append(f"{nom} : semaine type incomplète, il manque {', '.join(manquants)}")

    if not academie:
        return err
    aca = academie.get("domaines", {})
    for cle in aca:
        if cle not in domaines:
            err.append(f"academie.json : la clé {cle} est absente du programme {nom}")
    for cle, d in domaines.items():
        if cle not in aca:
            err.append(f"academie.json : la clé {cle} du programme {nom} y est absente")
            continue
        if aca[cle].get("ordre") != d.get("ordre"):
            err.append(f"academie.json : ordre de {cle} différent du programme ({aca[cle].get('ordre')} contre {d.get('ordre')})")
        if bool(aca[cle].get("arbre", True)) != bool(d.get("arbre", True)):
            err.append(f"academie.json : {cle} n'a pas le même statut arbre que le programme")
    return err


def main() -> int:
    ap = argparse.ArgumentParser(description="Valideur du programme.")
    ap.add_argument("--json", action="store_true", help="comptes en sortie machine")
    args = ap.parse_args()

    academie = lire(ACADEMIE / "academie.json") if (ACADEMIE / "academie.json").exists() else {}
    fichiers = sorted(f for f in (ACADEMIE / "programme").glob("*.json") if f.name != "catalogue.json")
    if not fichiers:
        print("programme : aucun fichier", file=sys.stderr)
        return 1
    erreurs: list[str] = []
    comptes: dict[str, dict] = {}
    for f in fichiers:
        prog = lire(f)
        # academie.json ne s'aligne que sur le programme de son métier ; les autres métiers se valident seuls.
        aligne = academie if academie.get("metier") == prog.get("metier") else {}
        erreurs += valider(prog, aligne, f.name)
        chs = prog.get("chapitres", [])
        comptes[f.stem] = {"chapitres": len(chs),
                           "par_niveau": {str(n): sum(1 for c in chs if c.get("niveau") == n) for n in NIVEAUX}}
    if args.json:
        if erreurs:
            print("\n".join(erreurs), file=sys.stderr)
            return 1
        seul = comptes[fichiers[0].stem] if len(fichiers) == 1 else {}
        print(json.dumps({**seul, "programmes": comptes}, ensure_ascii=False))
        return 0
    for e in erreurs:
        print(f"ERREUR: {e}")
    for nom, c in comptes.items():
        print(f"programme : {nom}, {c['chapitres']} chapitre(s), "
              + ", ".join(f"{v} de niveau {k}" for k, v in c["par_niveau"].items()))
    return 1 if erreurs else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Le registre des sources : chargement, résolution, rendu du tableau.

`sources/registre.json` fait foi (`sources/README.md`). `sources/REGISTRE.md`
en est le rendu lisible, régénéré par :

    python3 app/registre.py --md > sources/REGISTRE.md

Une source de carte se rattache à une ligne du registre de deux façons
(`decisions/0004`, chantier `ACA-SOURCES-1`) :

- par **domaine web**, quand la source porte une URL : le domaine de l'URL
  est la ligne, ou l'un de ses sous-domaines
  (`reseaux-chaleur.cerema.fr` tombe sur `cerema.fr`) ;
- par **motif**, quand elle n'en porte pas : une expression régulière
  ancrée au début du texte de la source (« Art. 24 loi... » tombe sur
  Légifrance, « Cass. 3e civ.... » sur Judilibre).

Une ligne sans domaine web ni motif est là pour mémoire : elle décrit une
famille de sources qu'aucune carte ne cite encore.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

RACINE = Path(__file__).resolve().parent.parent
CHEMIN = RACINE / "sources" / "registre.json"

COLONNES = ["Source", "Domaine web ou référence", "Nature", "Parti",
            "Fiabilité", "Vérifié le", "On en tire", "On n'en tire pas"]

ENTETE_MD = """# REGISTRE DES SOURCES, domaine copropriété

Ouvert le 02/09/2026, rempli le 03/09/2026 par le chantier
`ACA-SOURCES-1` depuis les 84 cartes de `banque/` et le tri NotebookLM.
Une ligne par source. Nature et parti selon `decisions/0004`, fiabilité
selon `sources/README.md`. Une source sans ligne ici ne fonde aucune
carte.

Ce fichier est **régénéré**, il ne se corrige pas à la main :
`sources/registre.json` fait foi, `python3 app/registre.py --md` produit
la page, et `python3 app/tests_sources.py` refuse le jour où les deux
divergent.

Une cellule « Vérifié le » vide dit « à vérifier » : la source est
connue, son texte n'a pas été lu à la source.
"""


def charge(chemin: Path = CHEMIN) -> dict:
    """Le registre, tel quel. Lève si le JSON est invalide."""
    return json.loads(chemin.read_text(encoding="utf-8"))


def _domaine(url: str) -> str:
    return urlparse(url).netloc.lower().removeprefix("www.")


def resout(source: dict, registre: dict) -> dict | None:
    """La ligne de registre d'une source de carte, ou None si aucune ne la couvre."""
    url = str(source.get("url") or "").strip()
    texte = str(source.get("texte") or "").strip()
    if url:
        hote = _domaine(url)
        for ligne in registre["sources"]:
            dom = ligne.get("domaine_web")
            if dom and (hote == dom or hote.endswith("." + dom)):
                return ligne
        return None
    for ligne in registre["sources"]:
        motif = ligne.get("motif")
        if motif and re.match(motif, texte):
            return ligne
    return None


def rend_md(registre: dict) -> str:
    """Le tableau Markdown, depuis le JSON."""
    lignes = ["| " + " | ".join(COLONNES) + " |",
              "|" + "---|" * len(COLONNES)]
    for s in registre["sources"]:
        lignes.append("| " + " | ".join([
            s["source"],
            s.get("reference") or "",
            s["nature"],
            s.get("parti") or "",
            s["fiabilite"],
            s.get("verifie") or "à vérifier",
            s.get("on_en_tire") or "",
            s.get("on_n_en_tire_pas") or "",
        ]) + " |")
    return ENTETE_MD + "\n" + "\n".join(lignes) + "\n"


def main(argv: list[str]) -> int:
    if "--md" in argv:
        sys.stdout.write(rend_md(charge()))
        return 0
    reg = charge()
    print(f"registre : {len(reg['sources'])} ligne(s), domaine {reg['domaine']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

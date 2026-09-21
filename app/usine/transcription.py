"""Un document écrit devient des pseudo-pages pour l'usine (chantier
ACA-INGESTION-1).

Un sous-titre horodaté (.vtt, .srt) se nettoie : en-tête WEBVTT, numéros
de séquence, lignes d'horodatage, balises <v Nom>, préfixes « Nom : ». Un
document écrit (.txt, .md) se garde tel quel : ses lignes numériques et
ses préfixes avant deux-points (« Niveau : 3 ») sont le document.

Ce module ne sait pas reconnaître un nom cité dans la parole : une
transcription interne reste dans sources/interne/ et ne quitte jamais la
machine (decisions/0026 §9).
"""

from __future__ import annotations

import re

RE_HORODATAGE = re.compile(r"^\s*(\d{1,2}:)?\d{2}:\d{2}[.,]\d{3}\s*-->\s*(\d{1,2}:)?\d{2}:\d{2}[.,]\d{3}.*$")
RE_SEQUENCE = re.compile(r"^\s*\d+\s*$")
RE_BALISE_VOIX = re.compile(r"</?v[^>]*>")
RE_LOCUTEUR = re.compile(r"^\s*[^:\n]{1,40}:\s+")
RE_BALISE = re.compile(r"<[^>]+>")
RE_NOTE = re.compile(r"^\s*(NOTE|STYLE|REGION)\b.*$")


def nettoyer(texte: str, *, horodatage: bool = True) -> list[str]:
    """Les lignes du document : nettoyées d'un sous-titre horodaté, intactes sinon."""
    if not horodatage:
        return texte.splitlines()
    lignes = []
    for brute in texte.splitlines():
        if brute.strip().upper().startswith("WEBVTT"):
            continue
        if RE_HORODATAGE.match(brute) or RE_SEQUENCE.match(brute) or RE_NOTE.match(brute):
            continue
        ligne = RE_BALISE_VOIX.sub("", brute)
        ligne = RE_BALISE.sub("", ligne)
        ligne = RE_LOCUTEUR.sub("", ligne, count=1)
        ligne = ligne.strip()
        if ligne:
            lignes.append(ligne)
    return lignes


def pseudo_pages(lignes: list[str], lignes_par_page: int) -> list[str]:
    if lignes_par_page < 1:
        raise ValueError("lignes_par_page doit être au moins 1")
    pages = []
    for i in range(0, len(lignes), lignes_par_page):
        pages.append("\n".join(lignes[i:i + lignes_par_page]) + "\n")
    return pages or [""]

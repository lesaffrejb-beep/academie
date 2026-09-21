"""Préparation mécanique d'un document : empreinte, texte machine par page,
structure par taille de police, pages à figures rendues (decisions/0026).

Rien ici n'appelle un modèle ni un service : poppler en ligne de commande,
jamais lié. Le texte machine est le témoin contre lequel le pivot écrit
par le modèle sera vérifié (etat.py).
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

EXTENSIONS_PDF = {".pdf"}
# Un sous-titre horodaté se nettoie ; un document écrit (.txt, .md) se garde tel quel.
EXTENSIONS_HORODATAGE = {".vtt", ".srt"}
EXTENSIONS_TRANSCRIPTION = {".vtt", ".srt", ".txt", ".md"}
RE_MOT = re.compile(r"[a-zà-ÿœ0-9]{4,}")
# Une figure vectorielle n'est pas une image pour pdfimages : on la repère à sa légende.
RE_LEGENDE = re.compile(r"^\s*(Figure|Graphique|Tableau|Encadré|Encadre|Schéma|Schema|Carte|Illustration|Fig\.|Photo)\s*n?°?\s*\d", re.M | re.I)


def empreinte(fichier: Path) -> str:
    """Les seize premiers hexadécimaux du SHA-256, comme les fichiers déjà dans sources/."""
    h = hashlib.sha256()
    with fichier.open("rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()[:16]


def outil_present(nom: str) -> bool:
    return shutil.which(nom) is not None


def _commande(args: list[str], delai: int = 300) -> str:
    res = subprocess.run(args, capture_output=True, text=True, timeout=delai, errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"{args[0]} a échoué : {res.stderr.strip()[:300]}")
    return res.stdout


def nombre_de_pages(pdf: Path) -> int:
    sortie = _commande(["pdfinfo", str(pdf)])
    m = re.search(r"^Pages:\s+(\d+)", sortie, re.M)
    if not m:
        raise RuntimeError("pdfinfo ne donne pas le nombre de pages")
    return int(m.group(1))


def texte_par_page(pdf: Path) -> list[str]:
    """`pdftotext -layout` en un appel ; les pages sont séparées par un saut de page."""
    sortie = _commande(["pdftotext", "-layout", "-enc", "UTF-8", str(pdf), "-"])
    pages = sortie.split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    return pages


def images_par_page(pdf: Path) -> dict[int, int]:
    """Compte les images de chaque page avec `pdfimages -list`."""
    compte: Counter[int] = Counter()
    try:
        sortie = _commande(["pdfimages", "-list", str(pdf)])
    except (RuntimeError, subprocess.TimeoutExpired):
        return {}
    for ligne in sortie.splitlines()[2:]:
        parts = ligne.split()
        if len(parts) > 2 and parts[0].isdigit():
            compte[int(parts[0])] += 1
    return dict(compte)


def legendes_par_page(pages: list[str]) -> dict[int, int]:
    """Compte les légendes de figures, graphiques, tableaux et encadrés par page."""
    return {i: len(RE_LEGENDE.findall(txt)) for i, txt in enumerate(pages, 1) if RE_LEGENDE.search(txt)}


def titres_par_page(pdf: Path) -> list[dict]:
    """Les lignes dont la police dépasse nettement celle du corps : des titres probables.

    `pdftohtml -xml` donne une taille par police ; le corps est la taille la
    plus fréquente (pondérée par les caractères). Une ligne à 1,25 fois le
    corps ou plus est un titre candidat. Ce n'est qu'une aide : le modèle
    reconstitue les titres, la machine les propose.
    """
    try:
        sortie = _commande(["pdftohtml", "-xml", "-i", "-stdout", str(pdf)], delai=600)
    except (RuntimeError, subprocess.TimeoutExpired, FileNotFoundError):
        return []
    tailles = {m.group(1): float(m.group(2)) for m in re.finditer(r'<fontspec id="(\d+)" size="([\d.]+)"', sortie)}
    if not tailles:
        return []
    poids: Counter[float] = Counter()
    lignes = []
    page = 0
    for ligne in sortie.splitlines():
        mp = re.match(r'<page number="(\d+)"', ligne)
        if mp:
            page = int(mp.group(1))
            continue
        mt = re.search(r'<text [^>]*font="(\d+)"[^>]*>(.*?)</text>', ligne)
        if not mt:
            continue
        taille = tailles.get(mt.group(1), 0.0)
        texte = re.sub(r"<[^>]+>", "", mt.group(2)).strip()
        if not texte:
            continue
        poids[taille] += len(texte)
        lignes.append((page, taille, texte))
    corps = poids.most_common(1)[0][0]
    titres = [{"page": p, "taille": t, "texte": x} for p, t, x in lignes
              if corps and t >= corps * 1.25 and len(x) > 2]
    return titres[:2000]


def rendre_pages(pdf: Path, dossier: Path, pages: list[int], dpi: int) -> list[str]:
    """Rend en PNG les pages demandées ; renvoie les chemins créés."""
    dossier.mkdir(parents=True, exist_ok=True)
    crees = []
    for n in pages:
        cible = dossier / f"p-{n:04d}"
        if any(dossier.glob(f"p-{n:04d}*.png")):
            crees.append(str(next(dossier.glob(f"p-{n:04d}*.png"))))
            continue
        _commande(["pdftoppm", "-r", str(dpi), "-png", "-f", str(n), "-l", str(n), "-singlefile", str(pdf), str(cible)])
        crees.append(str(cible) + ".png")
    return crees


def extraire_images(pdf: Path, dossier: Path) -> list[str]:
    """Extrait les images intégrées en PNG, pour les réutiliser telles quelles.

    À côté des pages rendues (`p-####.png`, une page entière), `pdfimages
    -png -p` sort les images réelles (`img-<page>-<n>.png`). Une extraction
    impossible ne fait pas échouer la préparation : on rend une liste vide.
    """
    dossier.mkdir(parents=True, exist_ok=True)
    try:
        _commande(["pdfimages", "-png", "-p", str(pdf), str(dossier / "img")], delai=900)
    except (RuntimeError, subprocess.TimeoutExpired):
        return []
    return sorted(str(p) for p in dossier.glob("img-*.png"))


def mots(texte: str) -> set[str]:
    """Les mots de contenu (quatre caractères ou plus), en minuscules, sans doublon."""
    return set(RE_MOT.findall(texte.lower()))


def compte_mots(texte: str) -> int:
    return len(RE_MOT.findall(texte.lower()))


def ecrire_pages(dossier: Path, pages: list[str]) -> None:
    dossier.mkdir(parents=True, exist_ok=True)
    for i, txt in enumerate(pages, 1):
        (dossier / f"p-{i:04d}.txt").write_text(txt, encoding="utf-8")


def lire_page(dossier: Path, n: int) -> str:
    f = dossier / f"p-{n:04d}.txt"
    return f.read_text(encoding="utf-8") if f.exists() else ""


def pivot_brut(pages: list[str], figures: dict[int, int], seuil_mots: int) -> str:
    """Le pivot de départ : le texte machine sous une ancre par page.

    Le modèle nettoie ensuite section par section ; il part d'un texte
    fidèle, jamais d'une page blanche, ce qui ferme la porte au résumé et
    à l'invention (decisions/0027).
    """
    blocs = ["<!-- pivot brut écrit par app/usine : chaque section [p. n] est à relire ; l'état des relectures est dans le fichier .etat.json -->", ""]
    for i, txt in enumerate(pages, 1):
        blocs.append(f"## [p. {i}]")
        blocs.append("")
        propre = txt.strip("\n")
        if compte_mots(propre) < seuil_mots and figures.get(i, 0) == 0:
            blocs.append("[page vide ou sans couche texte : à décrire depuis la page rendue, ou « [page vide] »]")
        elif figures.get(i, 0) > 0:
            blocs.append(f"[figure : {figures[i]} figure(s), tableau(x) ou image(s) sur cette page, à décrire en une phrase chacune depuis la page rendue]")
        if propre:
            blocs.append(propre)
        blocs.append("")
    return "\n".join(blocs)


def preparer_pdf(pdf: Path, dossier_pages: Path, dossier_figures: Path, config: dict) -> dict:
    """Tout le mécanique d'un PDF ; renvoie ce que l'état doit retenir."""
    for outil in ("pdfinfo", "pdftotext", "pdfimages", "pdftoppm"):
        if not outil_present(outil):
            raise RuntimeError(f"outil absent : {outil} (poppler ; `brew install poppler`)")
    n_pages = nombre_de_pages(pdf)
    pages = texte_par_page(pdf)
    if len(pages) < n_pages:
        pages += [""] * (n_pages - len(pages))
    pages = pages[:n_pages]
    images = images_par_page(pdf)
    legendes = legendes_par_page(pages)
    figures = {i: images.get(i, 0) + legendes.get(i, 0) for i in range(1, n_pages + 1) if images.get(i, 0) + legendes.get(i, 0) > 0}
    ecrire_pages(dossier_pages, pages)
    seuil = int(config["mots_page_texte"])
    a_rendre = [i for i in range(1, n_pages + 1) if figures.get(i, 0) > 0 or compte_mots(pages[i - 1]) < seuil]
    rendus = rendre_pages(pdf, dossier_figures, a_rendre, int(config["dpi_rendu"])) if a_rendre else []
    images_extraites = extraire_images(pdf, dossier_figures)
    titres = titres_par_page(pdf)
    total_mots = sum(compte_mots(p) for p in pages)
    ocr_requis = n_pages > 0 and total_mots < n_pages * 5 and sum(images.values()) > 0
    return {
        "type": "pdf", "pages": n_pages, "mots_machine": total_mots,
        "images_par_page": {str(k): v for k, v in sorted(images.items())},
        "figures_par_page": {str(k): v for k, v in sorted(figures.items())},
        "pages_rendues": rendus, "images_extraites": len(images_extraites),
        "ocr_requis": ocr_requis,
        "titres_candidats": len(titres), "titres": titres,
        "texte": pages,
    }


def ecrire_structure(chemin: Path, info: dict) -> None:
    structure = {
        "_": "Aide à la lecture produite par app/usine/pivot.py ; le modèle reconstitue les titres, la machine les propose.",
        "pages": info["pages"], "mots_machine": info["mots_machine"],
        "images_par_page": info.get("images_par_page", {}),
        "figures_par_page": info.get("figures_par_page", {}),
        "pages_rendues": info.get("pages_rendues", []),
        "images_extraites": info.get("images_extraites", 0),
        "titres_candidats": info.get("titres", []),
    }
    chemin.write_text(json.dumps(structure, ensure_ascii=False, indent=1), encoding="utf-8")

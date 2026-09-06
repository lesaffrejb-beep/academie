#!/usr/bin/env python3
"""Banc local reproductible, pas un valideur de cours (ACA-EXPERTISE-1).

Stdlib dans le coordinateur ; moteurs facultatifs dans des processus séparés.
Ne modifie ni les sources ni l'état usine. Aucun appel réseau implémenté.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import io
import json
import platform
import re
import subprocess
import sys
import time
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
RACINE = BASE.parents[1]


def normaliser(texte):
    # Ne retire ni unités, ni chiffres, ni signes. Accents et ligatures restent.
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", texte).casefold()).strip()


def evaluer(texte, cas):
    if texte is None:
        return None
    texte = normaliser(texte)
    resultats = []
    for mode in ("present", "absent", "regex"):
        for attendu in cas.get(mode, []):
            if mode == "regex":
                trouve = re.search(attendu, texte) is not None
            else:
                terme = normaliser(attendu)
                fin = r"(?!\w|[.,]\d)" if terme[-1:].isdigit() else r"(?!\w)"
                debut = r"(?<![\w.,+\-−])" if terme[:1].isdigit() else r"(?<!\w)"
                trouve = any(not (terme[:1].isdigit() and
                                  texte[:m.start()].rstrip().endswith(("-", "−", "+")))
                             for m in re.finditer(debut + re.escape(terme) + fin, texte))
            if mode == "absent":
                # Les parasites peuvent être fragmentés par des cellules Markdown.
                # Ceci ne normalise PAS les témoins numériques positifs.
                trouve = re.sub(r"[\s|]", "", normaliser(attendu)) in re.sub(r"[\s|]", "", texte)
            resultats.append({"type": mode, "temoin": attendu,
                              "ok": not trouve if mode == "absent" else trouve})
    return resultats


def verifier_source(chemin, attendu):
    h = hashlib.sha256()
    with Path(chemin).open("rb") as fichier:
        for bloc in iter(lambda: fichier.read(1 << 20), b""):
            h.update(bloc)
    if h.hexdigest() != attendu:
        raise ValueError(f"empreinte différente : {chemin}")
    return h.hexdigest()


def sondage(total, sha, graine, nombre, imposes):
    if total < 1 or nombre < 0 or not graine:
        raise ValueError("total positif, nombre positif ou nul et graine requise")
    candidats = [p for p in range(1, total + 1) if p not in set(imposes)]
    # Algorithme explicite, indépendant de l'implémentation de random.shuffle.
    candidats.sort(key=lambda p: hashlib.sha256(f"{graine}|{sha}|{p}".encode()).digest())
    return sorted(candidats[:nombre])


def worker(methode, chemin, page):
    debut = time.perf_counter()
    version = None
    derive = None
    if methode.startswith("poppler"):
        mode = "-raw" if methode.endswith("raw") else "-layout"
        p = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), mode,
                            "-enc", "UTF-8", chemin, "-"], capture_output=True,
                           text=True, check=True, timeout=45)
        texte = p.stdout
        version = subprocess.run(["pdftotext", "-v"], capture_output=True,
                                 text=True, timeout=10).stderr.splitlines()[0]
    elif methode.startswith("pymupdf"):
        import pymupdf as fitz
        with fitz.open(chemin) as pdf:
            texte = pdf[page - 1].get_text("text", sort=methode.endswith("sort"))
        version = importlib.metadata.version("PyMuPDF")
    elif methode.startswith("pypdf"):
        import pypdf
        pdf = pypdf.PdfReader(chemin)
        texte = pdf.pages[page - 1].extract_text(
            extraction_mode="layout" if methode.endswith("layout") else "plain") or ""
        version = importlib.metadata.version("pypdf")
    elif methode == "pdfplumber":
        import pdfplumber
        with pdfplumber.open(chemin) as pdf:
            texte = pdf.pages[page - 1].extract_text() or ""
        version = importlib.metadata.version("pdfplumber")
    elif methode == "markitdown":
        import pypdf
        from markitdown import MarkItDown
        # MarkItDown ne fournit pas ici de sélecteur de page. Dérivé monofeuille
        # en mémoire, couche texte conservée ; biais du wrapper déclaré.
        pdf = pypdf.PdfReader(chemin)
        sortie = pypdf.PdfWriter()
        sortie.add_page(pdf.pages[page - 1])
        flux = io.BytesIO()
        sortie.write(flux)
        derive = hashlib.sha256(flux.getvalue()).hexdigest()
        flux.seek(0)
        texte = MarkItDown(enable_plugins=False).convert_stream(
            flux, file_extension=".pdf").text_content
        version = importlib.metadata.version("markitdown")
    else:
        raise ValueError("moteur non pris en charge")
    return {"texte": texte, "version": version, "duree_interne_s": time.perf_counter() - debut,
            "derive_monopage_sha256": derive}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker", choices=["poppler-layout", "poppler-raw", "pymupdf-plain",
                        "pymupdf-sort", "pypdf-plain", "pypdf-layout", "pdfplumber", "markitdown"])
    parser.add_argument("--pdf")
    parser.add_argument("--page", type=int)
    parser.add_argument("--fixtures", type=Path, default=BASE / "benchmark-temoins.json")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--pymupdf-python", default=sys.executable)
    parser.add_argument("--bundled-python", default=sys.executable)
    parser.add_argument("--markitdown-python")
    parser.add_argument("--audit-seed")
    parser.add_argument("--audit-size", type=int, default=8)
    args = parser.parse_args()
    if args.worker:
        if not args.pdf or args.page is None or args.page < 1:
            parser.error("worker : --pdf et --page positif requis")
        print(json.dumps(worker(args.worker, args.pdf, args.page), ensure_ascii=False))
        return
    fixtures = json.loads(args.fixtures.read_text())
    # Valider tous les fichiers avant de produire le moindre résultat.
    for doc in fixtures["documents"]:
        verifier_source(RACINE / doc["fichier"], doc["sha256"])
        info = subprocess.run(["pdfinfo", str(RACINE / doc["fichier"])], capture_output=True,
                              text=True, check=True, timeout=30).stdout
        if int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1)) != doc["pages"]:
            raise ValueError("nombre de pages différent")
    if args.audit_seed:
        print(json.dumps({"graine": args.audit_seed, "statut": "a-auditer",
                          "regle": "sha256(graine|sha_document|page), ordre croissant",
                          "documents": [{"fichier": d["fichier"], "sha256": d["sha256"],
                            "pages_imposees": [c["page"] for c in d["cas"]],
                            "pages_tirees": sondage(d["pages"], d["sha256"], args.audit_seed,
                                                    args.audit_size, [c["page"] for c in d["cas"]])}
                            for d in fixtures["documents"]]}, ensure_ascii=False, indent=2))
        return
    if args.out is None:
        parser.error("--out répertoire neuf requis")
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    moteurs = {"poppler-layout": sys.executable, "poppler-raw": sys.executable,
               "pymupdf-plain": args.pymupdf_python, "pymupdf-sort": args.pymupdf_python,
               "pypdf-plain": args.bundled_python, "pypdf-layout": args.bundled_python,
               "pdfplumber": args.bundled_python, "markitdown": args.markitdown_python}
    rapport = {"date": datetime.now(timezone.utc).isoformat(), "machine": platform.platform(),
               "python_coordinateur": sys.version, "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "fixtures_sha256": hashlib.sha256(args.fixtures.read_bytes()).hexdigest(),
               "documents": fixtures["documents"], "resultats": [], "cout_api": 0,
               "cout_tokens_lecture_agent": None, "repetitions": 1,
               "limite": "Témoins ciblés non exhaustifs ; ni score OCR, ni taux de fiabilité, ni benchmark général."}
    for doc in fixtures["documents"]:
        for cas in doc["cas"]:
            for methode, executable in moteurs.items():
                row = {"document": doc["id"], "page": cas["page"], "methode": methode,
                       "statut": "non-mesure", "temoins": None}
                if executable:
                    commande = [executable, str(Path(__file__).resolve()), "--worker", methode,
                                "--pdf", str(RACINE / doc["fichier"]), "--page", str(cas["page"])]
                    row["commande"] = commande
                    debut = time.perf_counter()
                    try:
                        proc = subprocess.run(commande, capture_output=True, text=True, timeout=60)
                        row["duree_processus_s"] = round(time.perf_counter() - debut, 4)
                        row["stderr"] = proc.stderr[-4000:]
                        if proc.returncode:
                            row["statut"] = "erreur"
                            row["exit_code"] = proc.returncode
                        else:
                            res = json.loads(proc.stdout)
                            texte = res.pop("texte")
                            nom = f'{doc["id"]}-p{cas["page"]:04d}-{methode}.txt'
                            (args.out / nom).write_text(texte, encoding="utf-8")
                            row.update(res)
                            row.update(statut="mesure", caracteres=len(texte),
                                       texte_sha256=hashlib.sha256(texte.encode()).hexdigest(),
                                       sortie=nom, temoins=evaluer(texte, cas))
                    except (OSError, subprocess.TimeoutExpired, ValueError) as e:
                        row.update(statut="erreur", erreur=str(e))
                rapport["resultats"].append(row)
    (args.out / "rapport.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=2))
    # Résumé partageable : aucune transcription intégrale ; mêmes preuves.
    resume = {**rapport, "resultats": [{k: v for k, v in r.items() if k not in ("stderr", "commande")}
                                      for r in rapport["resultats"]]}
    (args.out / "resume.json").write_text(json.dumps(resume, ensure_ascii=False, indent=2))
    print(json.dumps({"rapport": str(args.out / "rapport.json"),
                      "mesures": sum(r["statut"] == "mesure" for r in rapport["resultats"]),
                      "erreurs": sum(r["statut"] == "erreur" for r in rapport["resultats"]),
                      "non_mesures": sum(r["statut"] == "non-mesure" for r in rapport["resultats"])}))


if __name__ == "__main__":
    main()

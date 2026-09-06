"""Complément expérimental local, sans API ni validation usine.

Un moteur par invocation. Les bibliothèques peuvent télécharger leurs poids ;
configurer HF_HOME et XDG_CACHE_HOME dans un répertoire temporaire dédié.
Une seule initialisation : durées NON comparables au banc natif par processus.
"""
import argparse
import hashlib
import importlib.metadata
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

from benchmark_pdf import BASE, RACINE, evaluer, verifier_source


def verifier_espace(libre):
    if libre < 8 * 1024**3:
        raise RuntimeError("Réserve de 8 Gio : ne pas lancer de nouveau moteur/modèle")


def bilan(texte, cas):
    return {"statut": "mesure" if texte is not None else "erreur",
            "temoins": evaluer(texte, cas)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--moteur", required=True, choices=["pymupdf4llm", "docling-hybride", "docling-ocr", "pdf-inspector"])
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    verifier_espace(shutil.disk_usage(RACINE).free)
    manifeste = BASE / "benchmark-temoins.json"
    fixtures = json.loads(manifeste.read_text())
    for doc in fixtures["documents"]:
        verifier_source(RACINE / doc["fichier"], doc["sha256"])
    a.out.mkdir(parents=True, exist_ok=False)
    (a.out / "benchmark_structure.py").write_bytes(Path(__file__).read_bytes())
    (a.out / "benchmark_pdf.py").write_bytes((BASE / "benchmark_pdf.py").read_bytes())
    (a.out / "benchmark-temoins.json").write_bytes(manifeste.read_bytes())
    debut = time.perf_counter()
    erreur_init = None
    version = None
    try:
        if a.moteur == "pymupdf4llm":
            import pymupdf4llm
            version = importlib.metadata.version("pymupdf4llm")
            def extraire(pdf, page):
                return pymupdf4llm.to_markdown(str(pdf), pages=[page - 1],
                    use_ocr=False, show_progress=False)
        elif a.moteur == "pdf-inspector":
            import pdf_inspector
            version = importlib.metadata.version("pdf-inspector")
            def extraire(pdf, page):
                r = pdf_inspector.extract_pages_markdown(str(pdf), pages=[page - 1])
                if len(r.pages) != 1 or r.pages[0].page != page - 1:
                    raise RuntimeError("sélection de page incorrecte")
                return r.pages[0].markdown
        else:
            from docling.document_converter import DocumentConverter, PdfFormatOption
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions, OcrMode
            from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
            version = importlib.metadata.version("docling")
            opt = PdfPipelineOptions()
            opt.enable_remote_services = False
            opt.allow_external_plugins = False
            opt.do_ocr = True
            opt.do_table_structure = True
            opt.accelerator_options = AcceleratorOptions(num_threads=2, device=AcceleratorDevice.CPU)
            opt.ocr_options = RapidOcrOptions(backend="onnxruntime", mode=(
                OcrMode.FULL_PAGE if a.moteur == "docling-ocr" else OcrMode.DEFAULT))
            conv = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=opt)})
            def extraire(pdf, page):
                r = conv.convert(pdf, page_range=(page, page), raises_on_error=True)
                if r.status.value != "success":
                    raise RuntimeError(f"conversion non complète : {r.status}")
                return r.document.export_to_markdown()
    except Exception as e:
        erreur_init = f"{type(e).__name__}: {e}"
    rapport = {"date": datetime.now(timezone.utc).isoformat(), "moteur": a.moteur,
        "version": version, "initialisation_s": time.perf_counter() - debut,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "evaluateur_sha256": hashlib.sha256((BASE / "benchmark_pdf.py").read_bytes()).hexdigest(),
        "fixtures_sha256": hashlib.sha256(manifeste.read_bytes()).hexdigest(),
        "documents": fixtures["documents"], "cout_api": 0, "resultats": [],
        "limite": "6 pages ciblées ; ni CER, ni qualité générale, ni débit de production. Chargement des poids éventuellement inclus dans la première page."}
    for doc in fixtures["documents"]:
        for cas in doc["cas"]:
            debut = time.perf_counter()
            texte = None
            erreur = erreur_init
            if not erreur:
                try:
                    verifier_espace(shutil.disk_usage(RACINE).free)
                    texte = extraire(RACINE / doc["fichier"], cas["page"])
                except Exception as e:
                    erreur = f"{type(e).__name__}: {e}"
            row = {"document": doc["id"], "page": cas["page"],
                "duree_s": time.perf_counter() - debut, "erreur": erreur, **bilan(texte, cas)}
            if texte is not None:
                nom = f"{doc['id']}-{cas['page']:04}.md"
                (a.out / nom).write_text(texte)
                row.update(sortie=nom, sha256=hashlib.sha256(texte.encode()).hexdigest())
            rapport["resultats"].append(row)
            (a.out / "rapport.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=2))
            print(json.dumps(row, ensure_ascii=False), flush=True)
    if any(r["statut"] != "mesure" for r in rapport["resultats"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

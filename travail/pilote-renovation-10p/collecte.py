"""Pilote local reproductible : aucune API ; les différences exigent une lecture.

Utiliser l'environnement Docling du benchmark avec HF_HUB_OFFLINE=1.
Les sorties brutes sont ignorées par Git ; le rapport peut être versionné.
"""
import argparse
from datetime import datetime, timezone
from difflib import SequenceMatcher
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import time

PAGES = tuple(range(13, 23))
SHA = '322a2f5e843f45b99f324a9f185a63d75f6838602081e362002176451855dc43'
ROOT = Path(__file__).resolve().parents[2]

def empreinte(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verifier(pdf):
    if empreinte(pdf) != SHA:
        raise ValueError('Document différent du pilote autorisé')

def comparer(a, b):
    return {'identiques': a == b, 'similarite_sequence': round(SequenceMatcher(None, a, b, autojunk=False).ratio(), 4),
            'verdict': 'a_arbitrer_sur_image'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    pdf = ROOT / 'sources/322a2f5e843f45b9.pdf'
    verifier(pdf)
    if shutil.disk_usage(ROOT).free < 8 * 1024**3:
        raise RuntimeError('Réserve de 8 Gio insuffisante')
    args.out.mkdir(parents=True, exist_ok=False)
    import pymupdf
    from docling.document_converter import DocumentConverter, PdfFormatOption
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions, RapidOcrOptions
    from docling.datamodel.accelerator_options import AcceleratorOptions, AcceleratorDevice
    from docling_core.types.doc import PictureItem, TableItem
    options = PdfPipelineOptions()
    options.enable_remote_services = False
    options.allow_external_plugins = False
    options.do_ocr = True
    options.do_table_structure = True
    options.generate_page_images = True
    options.generate_picture_images = True
    options.images_scale = 2.0
    options.accelerator_options = AcceleratorOptions(num_threads=2, device=AcceleratorDevice.CPU)
    options.ocr_options = RapidOcrOptions(backend='onnxruntime')
    debut = time.perf_counter()
    conv = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)})
    rapport = {'version': 1, 'date': datetime.now(timezone.utc).isoformat(), 'source_sha256': SHA,
               'script_sha256': empreinte(Path(__file__)), 'pages_prevues': list(PAGES),
               'versions': {p: importlib.metadata.version(p) for p in ['docling', 'docling-core', 'pymupdf', 'rapidocr']},
               'poppler': subprocess.run(['pdftotext', '-v'], capture_output=True, text=True).stderr.splitlines()[0],
               'cout_api_usd': 0, 'pages': [], 'limite': 'Similarité textuelle non assimilable à une fiabilité. Recadrages automatiques à contrôler.'}
    doc = pymupdf.open(pdf)
    for page in PAGES:
        t = time.perf_counter()
        doc[page-1].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(args.out / f'page-{page:04d}.png')
        natif = subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-layout', str(pdf), '-'], check=True, capture_output=True, text=True).stdout
        (args.out / f'poppler-{page:04d}.txt').write_text(natif)
        r = conv.convert(pdf, page_range=(page, page), raises_on_error=True)
        if r.status.value != 'success':
            raise RuntimeError(f'Page {page}: {r.status.value}')
        md = r.document.export_to_markdown()
        (args.out / f'focus-{page:04d}.md').write_text(md)
        assets = []
        for index, (item, _) in enumerate(r.document.iterate_items()):
            if isinstance(item, (PictureItem, TableItem)):
                im = item.get_image(r.document)
                if im is not None:
                    nom = f'focus-{page:04d}-{index:03d}.png'
                    im.save(args.out / nom)
                    assets.append({'fichier': nom, 'type': type(item).__name__, 'sha256': empreinte(args.out / nom),
                                   'prov': [p.model_dump(mode='json') for p in item.prov]})
        entree = {'page': page, 'statut': r.status.value, 'secondes': round(time.perf_counter()-t, 3),
                  'comparaison': comparer(natif, md), 'assets': assets,
                  'sorties': {f: empreinte(args.out / f) for f in [f'page-{page:04d}.png', f'poppler-{page:04d}.txt', f'focus-{page:04d}.md']}}
        rapport['pages'].append(entree)
        rapport['secondes_total'] = round(time.perf_counter()-debut, 3)
        (args.out / 'rapport.json').write_text(json.dumps(rapport, indent=2, ensure_ascii=False)+'\n')
        print(f'Page {page}: {len(assets)} supports, {entree["secondes"]} s', flush=True)

if __name__ == '__main__':
    main()

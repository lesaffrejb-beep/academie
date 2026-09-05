#!/usr/bin/env python3
"""L'usine en ligne de commande : un document réel, pas à pas (decisions/0026, 0027).

    python3 app/usine/usine.py preparer <fichier> [--interne]
    python3 app/usine/usine.py declarer <empreinte> --outil <outil> --modele <modèle>
    python3 app/usine/usine.py suivant <empreinte>
    python3 app/usine/usine.py valider <empreinte>
    python3 app/usine/usine.py etat [<empreinte>]
    python3 app/usine/usine.py fiche <empreinte>
    python3 app/usine/usine.py registre <empreinte> [--ecrire]

Sort 0 quand la demande aboutit, 1 sinon. Les messages sont faits pour être
lus par le modèle qui travaille : ils disent quoi faire ensuite.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from usine import etat as E  # noqa: E402
from usine import fiche as F  # noqa: E402
from usine import pivot as P  # noqa: E402
from usine import transcription as T  # noqa: E402


def cmd_preparer(args) -> int:
    rac = E.racine()
    cfg = E.config(rac)
    fichier = Path(args.fichier).expanduser().resolve()
    if not fichier.is_file():
        print(f"fichier introuvable : {fichier}")
        return 1
    suffixe = fichier.suffix.lower()
    if suffixe not in P.EXTENSIONS_PDF | P.EXTENSIONS_TRANSCRIPTION:
        print(f"format non pris en charge : {suffixe} (PDF, .vtt, .srt, .txt, .md)")
        return 1
    emp = P.empreinte(fichier)
    doc = E.Document(rac, emp, interne=bool(args.interne))
    doc.base.mkdir(parents=True, exist_ok=True)
    cible = doc.base / f"{emp}{suffixe}"
    if not cible.exists():
        shutil.copy2(fichier, cible)
    if doc.etat.exists():
        etat = E.charger(doc)
        print(f"déjà préparé : {doc.rel(doc.etat)}")
        print(E.resume(doc, etat))
        return 0
    if suffixe in P.EXTENSIONS_PDF:
        info = P.preparer_pdf(cible, doc.pages, doc.figures, cfg)
    else:
        lignes = T.nettoyer(cible.read_text(encoding="utf-8", errors="replace"))
        pages = T.pseudo_pages(lignes, int(cfg["lignes_par_page_transcription"]))
        P.ecrire_pages(doc.pages, pages)
        info = {"type": "transcription", "pages": len(pages), "mots_machine": sum(P.compte_mots(p) for p in pages),
                "images_par_page": {}, "figures_par_page": {}, "pages_rendues": [], "ocr_requis": False, "titres": [], "texte": pages}
    P.ecrire_structure(doc.structure, info)
    doc.pivot.write_text(P.pivot_brut(info["texte"], {int(k): v for k, v in info["figures_par_page"].items()},
                                      int(cfg["mots_page_texte"])), encoding="utf-8")
    etat = E.etat_initial(doc, info, cfg)
    E.journaliser(etat, "préparation", f"{info['pages']} page(s), {info['mots_machine']} mots machine, {len(info.get('pages_rendues', []))} page(s) rendue(s)")
    E.sauver(doc, etat)
    print(f"préparé : {doc.rel(cible)}")
    print(f"  pages machine : {doc.rel(doc.pages)}/ ({info['pages']} page(s), {info['mots_machine']} mots)")
    print(f"  pivot brut    : {doc.rel(doc.pivot)}")
    print(f"  structure     : {doc.rel(doc.structure)}")
    if info.get("pages_rendues"):
        print(f"  pages rendues : {len(info['pages_rendues'])} dans {doc.rel(doc.figures)}/")
    if info.get("ocr_requis"):
        print("  OCR requis : aucune couche texte ; `ocrmypdf --language fra` puis `preparer` à nouveau")
    if args.interne:
        print("  interne : ce document et tout ce qui en sort restent dans sources/interne/ ; aucun nom ne doit passer dans une fiche ni un chapitre")
    print(f"ensuite : python3 app/usine/usine.py declarer {emp} --outil <outil> --modele <modèle>")
    return 0


def _doc(cle: str) -> tuple[E.Document, dict, dict]:
    rac = E.racine()
    doc = E.trouver(rac, cle)
    return doc, E.charger(doc), E.config(rac)


def cmd_declarer(args) -> int:
    doc, etat, cfg = _doc(args.empreinte)
    if args.classe is not None:
        print("option --classe obsolète et ignorée ; les contrôles ne dépendent plus du modèle")
    for m in E.declarer(doc, etat, cfg, args.outil, args.modele):
        print(m)
    E.sauver(doc, etat)
    print(f"ensuite : python3 app/usine/usine.py suivant {doc.empreinte}")
    return 0


def cmd_suivant(args) -> int:
    doc, etat, cfg = _doc(args.empreinte)
    unite, messages = E.suivant(doc, etat, cfg)
    E.sauver(doc, etat)
    for m in messages:
        print(m)
    if unite is None:
        return 0
    if unite.get("erreurs"):
        print("défauts relevés :")
        for e in unite["erreurs"]:
            print("  - " + e)
    print(E.consigne(doc, etat, unite))
    return 0


def cmd_valider(args) -> int:
    doc, etat, cfg = _doc(args.empreinte)
    ok, messages = E.valider(doc, etat, cfg)
    E.sauver(doc, etat)
    for m in messages:
        print(("  - " if not ok and not m.startswith("unité") else "") + m)
    if ok:
        print(f"ensuite : python3 app/usine/usine.py suivant {doc.empreinte}")
    return 0 if ok else 1


def cmd_etat(args) -> int:
    rac = E.racine()
    if args.empreinte:
        doc, etat, cfg = _doc(args.empreinte)
        for m in E.reverifier(doc, etat, cfg):
            print(m)
        E.sauver(doc, etat)
        print(E.resume(doc, etat))
        return 0
    trouves = 0
    for base in (rac / "sources", rac / "sources" / "interne"):
        if not base.exists():
            continue
        for f in sorted(base.glob("*.etat.json")):
            doc = E.Document(rac, f.name[: -len(".etat.json")], interne=(base.name == "interne"))
            print(E.resume(doc, E.charger(doc)).splitlines()[0])
            trouves += 1
    if not trouves:
        print("aucun document préparé")
    return 0


def cmd_fiche(args) -> int:
    doc, etat, cfg = _doc(args.empreinte)
    ok, messages = F.valider_fiche(doc, etat, cfg)
    for m in messages:
        print(("" if ok else "  - ") + m)
    if ok:
        E.journaliser(etat, "fiche validée", "")
        E.sauver(doc, etat)
    return 0 if ok else 1


def cmd_registre(args) -> int:
    doc, etat, cfg = _doc(args.empreinte)
    ligne = F.ligne_registre(doc)
    print(ligne)
    if args.ecrire:
        registre = F.ecrire_registre(doc, ligne)
        E.journaliser(etat, "ligne de registre écrite", doc.rel(registre))
        E.sauver(doc, etat)
        print(f"écrit dans {doc.rel(registre)} ({E.pages_relues(etat)}/{etat['pages']} page(s) relues à ce moment)")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="L'usine de l'Académie, pas à pas.")
    sp = p.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("preparer"); s.add_argument("fichier"); s.add_argument("--interne", action="store_true"); s.set_defaults(f=cmd_preparer)
    s = sp.add_parser("declarer"); s.add_argument("empreinte"); s.add_argument("--outil", required=True); s.add_argument("--modele", required=True)
    s.add_argument("--classe", default=None, help=argparse.SUPPRESS); s.set_defaults(f=cmd_declarer)
    s = sp.add_parser("suivant"); s.add_argument("empreinte"); s.set_defaults(f=cmd_suivant)
    s = sp.add_parser("valider"); s.add_argument("empreinte"); s.set_defaults(f=cmd_valider)
    s = sp.add_parser("etat"); s.add_argument("empreinte", nargs="?"); s.set_defaults(f=cmd_etat)
    s = sp.add_parser("fiche"); s.add_argument("empreinte"); s.set_defaults(f=cmd_fiche)
    s = sp.add_parser("registre"); s.add_argument("empreinte"); s.add_argument("--ecrire", action="store_true"); s.set_defaults(f=cmd_registre)
    args = p.parse_args(argv)
    try:
        return args.f(args)
    except RuntimeError as exc:
        print(f"refus : {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

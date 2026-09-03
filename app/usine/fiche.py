"""La fiche d'un document et sa ligne de registre (decisions/0026 §2 et §6).

Le modèle écrit `<empreinte>.fiche.json` ; le script la vérifie : champs,
nature admise, cohérence avec l'état, aucun chiffre du résumé qui ne soit
lisible dans le pivot. La ligne de registre se déduit de la fiche, elle
ne s'écrit pas à la main.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from valide_chapitres import FIABILITE_PAR_NATURE, NATURES  # noqa: E402

from usine.etat import Document, maintenant, nombres  # noqa: E402

CHAMPS = ("titre", "editeur", "date_edition", "nature", "parti", "fiabilite", "licence", "periode_validite",
          "pages", "on_en_tire", "on_n_en_tire_pas", "resume", "interne")
RE_DATE = re.compile(r"^(\d{4}(-\d{2})?|inconnue)$")


def valider_fiche(doc: Document, etat: dict, cfg: dict) -> tuple[bool, list[str]]:
    if not doc.fiche.exists():
        return False, [f"fiche absente : écris {doc.rel(doc.fiche)} avec les champs {', '.join(CHAMPS)}"]
    try:
        fiche = json.loads(doc.fiche.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return False, [f"fiche illisible : {exc}"]
    err = []
    for champ in CHAMPS:
        if champ not in fiche or fiche[champ] in (None, ""):
            if champ == "parti":
                continue
            err.append(f"champ manquant : {champ}")
    if err:
        return False, err
    if not RE_DATE.match(str(fiche["date_edition"])):
        err.append("date_edition : AAAA, AAAA-MM ou « inconnue »")
    if fiche["nature"] not in NATURES:
        err.append(f"nature inconnue « {fiche['nature']} » ; admises : {', '.join(sorted(NATURES))}")
    if fiche["fiabilite"] not in ("A", "B", "C"):
        err.append("fiabilite : A, B ou C")
    elif fiche["nature"] in FIABILITE_PAR_NATURE and fiche["fiabilite"] < FIABILITE_PAR_NATURE[fiche["nature"]]:
        err.append(f"fiabilite {fiche['fiabilite']} au-dessus de ce que la nature « {fiche['nature']} » permet ({FIABILITE_PAR_NATURE[fiche['nature']]})")
    if int(fiche["pages"]) != int(etat["pages"]):
        err.append(f"pages : {fiche['pages']} dans la fiche, {etat['pages']} dans l'état")
    if not isinstance(fiche["interne"], bool) or fiche["interne"] != doc.interne:
        err.append(f"interne doit valoir {str(doc.interne).lower()} pour ce document")
    if len(str(fiche["resume"])) > int(cfg["resume_max"]):
        err.append(f"résumé trop long ({len(str(fiche['resume']))} caractères, maximum {cfg['resume_max']})")
    if "—" in json.dumps(fiche, ensure_ascii=False):
        err.append("tiret cadratin dans la fiche")
    pivot = doc.pivot.read_text(encoding="utf-8") if doc.pivot.exists() else ""
    connus = nombres(pivot)
    for champ in ("titre", "resume", "on_en_tire", "on_n_en_tire_pas", "periode_validite"):
        absents = sorted(nombres(str(fiche[champ])) - connus - nombres(str(fiche["date_edition"])))
        if absents:
            err.append(f"{champ} : chiffre absent du document : {', '.join(absents[:5])}")
    if err:
        return False, err
    fiche["validee_le"] = maintenant()
    fiche["par"] = (etat.get("declaration") or {}).get("modele", "")
    fiche["outil"] = (etat.get("declaration") or {}).get("outil", "")
    fiche["empreinte"] = doc.empreinte
    doc.fiche.write_text(json.dumps(fiche, ensure_ascii=False, indent=1), encoding="utf-8")
    return True, [f"fiche validée ({fiche['nature']}, {fiche['fiabilite']}) ; ligne de registre : `usine.py registre {doc.empreinte}`"]


def ligne_registre(doc: Document) -> str:
    fiche = json.loads(doc.fiche.read_text(encoding="utf-8"))
    if "validee_le" not in fiche:
        raise RuntimeError("fiche non validée : `usine.py fiche` d'abord")
    reference = "interne" if fiche["interne"] else (fiche.get("reference") or "à compléter")
    titre = f"{fiche['titre']} ({fiche['editeur']}, {fiche['date_edition']})"
    cellules = [titre, reference, fiche["nature"], fiche.get("parti") or "", fiche["fiabilite"],
                str(fiche["validee_le"])[:10], fiche["on_en_tire"], fiche["on_n_en_tire_pas"]]
    return "| " + " | ".join(str(c).replace("|", "/").replace("\n", " ") for c in cellules) + " |"


def ecrire_registre(doc: Document, ligne: str) -> Path:
    registre = doc.racine / "sources" / "REGISTRE.md"
    if not registre.exists():
        raise RuntimeError(f"registre absent : {doc.rel(registre)}")
    texte = registre.read_text(encoding="utf-8")
    if ligne in texte:
        return registre
    if not texte.endswith("\n"):
        texte += "\n"
    registre.write_text(texte + ligne + "\n", encoding="utf-8")
    return registre

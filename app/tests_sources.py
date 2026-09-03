#!/usr/bin/env python3
"""Tests du registre des sources, chantier ACA-SOURCES-1.

Ce que ces tests protègent :

1. le registre est bien formé : natures dans la liste fermée de
   `decisions/0004`, fiabilité dans A, B, C, identifiants uniques,
   motifs compilables, aucune ligne vide ;
2. `sources/REGISTRE.md` est exactement le rendu de
   `sources/registre.json` (le JSON fait foi) ;
3. **chaque source de chaque carte de `banque/` porte une `nature`**, et
   cette nature est dans la liste fermée ;
4. **chaque source de chaque carte se rattache à une ligne du registre**,
   par domaine web ou par motif, et la nature écrite sur la carte est
   celle de sa ligne (une carte n'invente pas la nature de sa source) ;
5. la résolution elle-même mord : sous-domaine accepté, domaine voisin
   refusé, texte sans motif refusé.

Le test est la porte du contrat v2 : `nature` y devient obligatoire
(`CONTRAT-CARTE-V2.md`), ici elle est déjà vérifiée partout.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

APP = Path(__file__).resolve().parent
RACINE = APP.parent
sys.path.insert(0, str(APP))

import registre as reg  # noqa: E402
from valide_banque import valide_carte  # noqa: E402

# Liste fermée de decisions/0004, reprise par CONTRAT-CARTE-V2.md.
NATURES = {"texte-officiel", "jurisprudence", "institution", "norme", "doctrine",
           "presse-pro", "organisation-pro", "association", "editeur",
           "support-interne", "terrain"}
FIABILITES = {"A", "B", "C"}
RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

ECHECS: list[str] = []


def verifie(nom: str, condition: bool, detail: str = "") -> None:
    print(f"{'✓' if condition else '✗'} {nom}")
    if not condition:
        ECHECS.append(nom)
        if detail:
            print(f"   {detail}")


def cartes() -> list[tuple[str, dict, dict]]:
    """(référence lisible, carte, source) pour chaque source de chaque carte."""
    out = []
    for fichier in sorted((RACINE / "banque").rglob("*.json")):
        for carte in json.loads(fichier.read_text(encoding="utf-8")):
            for i, src in enumerate(carte.get("source") or []):
                out.append((f"{fichier.name}:{carte.get('id')}:source[{i}]", carte, src))
    return out


def main() -> int:
    registre = reg.charge()
    lignes = registre["sources"]
    toutes = cartes()

    # --- 1. le registre est bien formé --------------------------------
    ids = [l["id"] for l in lignes]
    verifie("les identifiants du registre sont uniques", len(ids) == len(set(ids)),
            f"{len(ids)} lignes, {len(set(ids))} identifiants")

    mauvaises = [l["id"] for l in lignes if l.get("nature") not in NATURES]
    verifie("chaque ligne porte une nature de la liste fermée", not mauvaises, str(mauvaises))

    mauvaises = [l["id"] for l in lignes if l.get("fiabilite") not in FIABILITES]
    verifie("chaque ligne porte une fiabilité A, B ou C", not mauvaises, str(mauvaises))

    vides = [l.get("id") or "<sans id>" for l in lignes
             if not str(l.get("source") or "").strip()
             or not str(l.get("on_en_tire") or "").strip()
             or not str(l.get("on_n_en_tire_pas") or "").strip()]
    verifie("aucune ligne vide (source, on en tire, on n'en tire pas)", not vides, str(vides))

    mauvaises = [l["id"] for l in lignes
                 if l.get("verifie") and not RE_DATE.match(str(l["verifie"]))]
    verifie("les dates de vérification sont au format AAAA-MM-JJ", not mauvaises, str(mauvaises))

    incompilables = []
    for l in lignes:
        if l.get("motif"):
            try:
                re.compile(l["motif"])
            except re.error as exc:
                incompilables.append(f"{l['id']} : {exc}")
    verifie("les motifs du registre compilent", not incompilables, str(incompilables))

    # --- 2. REGISTRE.md est le rendu du JSON --------------------------
    attendu = reg.rend_md(registre)
    ecrit = (RACINE / "sources" / "REGISTRE.md").read_text(encoding="utf-8")
    verifie("sources/REGISTRE.md est le rendu de registre.json", ecrit == attendu,
            "régénérer : python3 app/registre.py --md > sources/REGISTRE.md")

    # --- 3. chaque source de carte porte sa nature --------------------
    sans_nature = [ref for ref, _, s in toutes if not str(s.get("nature") or "").strip()]
    verifie(f"les {len(toutes)} sources des cartes portent une nature", not sans_nature,
            f"{len(sans_nature)} sans nature, ex. {sans_nature[:3]}")

    hors_liste = sorted({str(s.get("nature")) for _, _, s in toutes} - NATURES - {"None", ""})
    verifie("aucune nature de carte hors de la liste fermée", not hors_liste, str(hors_liste))

    # --- 4. chaque source de carte a sa ligne au registre -------------
    orphelines, desaccords = [], []
    for ref, _, s in toutes:
        ligne = reg.resout(s, registre)
        if ligne is None:
            orphelines.append(f"{ref} : {(s.get('url') or s.get('texte') or '')[:60]}")
        elif s.get("nature") and s["nature"] != ligne["nature"]:
            desaccords.append(f"{ref} : carte {s['nature']}, registre {ligne['nature']} ({ligne['id']})")
    verifie("chaque source de carte a une ligne au registre", not orphelines,
            f"{len(orphelines)} orpheline(s), ex. {orphelines[:3]}")
    verifie("la nature de la carte est celle de sa ligne de registre", not desaccords,
            f"{len(desaccords)} désaccord(s), ex. {desaccords[:3]}")

    # le parti du registre est repris quand il existe
    partis = []
    for ref, _, s in toutes:
        ligne = reg.resout(s, registre)
        if ligne and ligne.get("parti") and s.get("parti") != ligne["parti"]:
            partis.append(f"{ref} : attendu « {ligne['parti']} »")
    verifie("le parti du registre est repris sur la carte", not partis,
            f"{len(partis)} manquant(s), ex. {partis[:3]}")

    # --- 5. la résolution mord ----------------------------------------
    faux = {"_": "registre jetable", "version": 1, "domaine": "test", "sources": [
        {"id": "cerema", "source": "Cerema", "reference": "cerema.fr", "domaine_web": "cerema.fr",
         "motif": None, "nature": "institution", "parti": "", "fiabilite": "A",
         "verifie": "2026-09-02", "on_en_tire": "des guides", "on_n_en_tire_pas": "rien"},
        {"id": "juri", "source": "Judilibre", "reference": "courdecassation.fr", "domaine_web": None,
         "motif": "^Cass\\.", "nature": "jurisprudence", "parti": "", "fiabilite": "A",
         "verifie": "2026-08-28", "on_en_tire": "des arrêts", "on_n_en_tire_pas": "rien"},
    ]}
    verifie("un sous-domaine tombe sur sa ligne",
            (reg.resout({"texte": "x", "url": "https://reseaux-chaleur.cerema.fr/a"}, faux) or {}).get("id") == "cerema")
    verifie("un domaine voisin ne tombe pas sur la ligne",
            reg.resout({"texte": "x", "url": "https://faux-cerema.fr/a"}, faux) is None)
    verifie("une référence sans URL tombe sur son motif",
            (reg.resout({"texte": "Cass. 3e civ., 25 janvier 2024"}, faux) or {}).get("id") == "juri")
    verifie("une référence sans motif reste orpheline",
            reg.resout({"texte": "Un blog quelconque"}, faux) is None)
    verifie("une URL inconnue reste orpheline, sans repli sur les motifs",
            reg.resout({"texte": "Cass. 3e civ., 25 janvier 2024", "url": "https://inconnu.fr/a"}, faux) is None)

    # --- 6. le valideur v1 tolère la nature, il ne l'invente pas ------
    config = json.loads((RACINE / "academie.json").read_text(encoding="utf-8"))
    domaine = next(iter(config["domaines"]))

    def carte_avec(source: dict) -> list[str]:
        c = {"id": "test-nature", "domaine": domaine, "branche": "b", "type": "flash",
             "question": "q", "reponse": "r", "source": [source],
             "verifie": "2026-08-28", "statut": "valide", "partage": "banque"}
        return valide_carte(c, Path("test.json"), config, set(), date(2026, 8, 28))

    verifie("le valideur v1 accepte encore une source sans nature",
            not carte_avec({"texte": "Art. 24 loi n° 65-557"}),
            str(carte_avec({"texte": "Art. 24 loi n° 65-557"})))
    verifie("le valideur v1 accepte une nature de la liste fermée",
            not carte_avec({"texte": "Art. 24", "nature": "texte-officiel"}),
            str(carte_avec({"texte": "Art. 24", "nature": "texte-officiel"})))
    refus = carte_avec({"texte": "Art. 24", "nature": "site-de-confiance"})
    verifie("le valideur v1 refuse une nature inventée",
            any("liste fermée" in e for e in refus), str(refus))

    if ECHECS:
        print(f"\n{len(ECHECS)} test(s) en échec : {', '.join(ECHECS)}")
        return 1
    print(f"\nsources : tout vert. Registre : {len(lignes)} ligne(s) ; "
          f"cartes : {len(toutes)} source(s), toutes rattachées.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

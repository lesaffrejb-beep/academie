#!/usr/bin/env python3
"""Inventaire éditorial déterministe ; ni certification ni constat du VPS."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verifier(catalogue, programme):
    erreurs, vus = [], set()
    if not isinstance(catalogue, dict) or not isinstance(catalogue.get("specialites"), list):
        return ["specialites doit être une liste"]
    branches = {f"{d}.{b['cle']}" for d, bs in programme["branches"].items() for b in bs}
    for s in catalogue.get("specialites", []):
        if not isinstance(s, dict):
            erreurs.append("spécialité : objet requis")
            continue
        ident = s.get("id")
        if not isinstance(ident, str) or not ident.strip():
            erreurs.append("identifiant : texte non vide requis")
            ident = "invalide"
        if ident in vus:
            erreurs.append(f"identifiant absent ou répété : {ident}")
        vus.add(ident)
        for champ in ("titre", "production", "limite"):
            if not isinstance(s.get(champ), str) or not s[champ].strip():
                erreurs.append(f"{ident} : {champ} texte non vide requis")
        for champ in ("branches", "objectifs", "sources_a_instruire"):
            valeur = s.get(champ)
            if not isinstance(valeur, list) or not valeur or not all(isinstance(v, str) and v.strip() for v in valeur):
                erreurs.append(f"{ident} : {champ} doit contenir des textes non vides")
        if s.get("statut") != "a-construire":
            erreurs.append(f"{ident} : ce catalogue ne certifie aucune spécialité construite")
        for branche in s.get("branches", []) if isinstance(s.get("branches"), list) else []:
            if isinstance(branche, str) and branche not in branches:
                erreurs.append(f"{ident} : branche inconnue {branche}")
    if not catalogue.get("specialites"):
        erreurs.append("catalogue vide")
    return erreurs


def construire(catalogue, programme, artefact, etudes):
    erreurs = verifier(catalogue, programme)
    if erreurs:
        raise ValueError("\n".join(erreurs))
    domaines = set(programme["domaines"])
    ids = {c["id"] for c in programme["chapitres"]}
    cartes = None if artefact is None else [c for c in artefact["cartes"]
        if c.get("statut") == "valide" and c.get("domaine") in domaines
        and (not c.get("chapitre") or c["chapitre"] in ids)]
    chapitres = programme["chapitres"]
    resultat = {"portee": "Artefact local seulement ; rattachement thématique, pas couverture des objectifs ni expertise acquise.",
                "domaines": [], "specialites": [], "cartes_sans_chapitre": None if cartes is None else
                sum(c.get("chapitre") not in ids for c in cartes)}
    for cle, d in programme["domaines"].items():
        ds = [c for c in chapitres if c["domaine"] == cle]
        cs = None if cartes is None else [c for c in cartes if c["domaine"] == cle]
        resultat["domaines"].append({"id": cle, "titre": d["titre"], "chapitres_prevus": len(ds),
            "niveaux_prevus": dict(sorted(Counter(c["niveau"] for c in ds).items())),
            "cartes_artefact": None if cs is None else len(cs),
            "cartes_n4_n5": None if cs is None else sum(c["niveau"] >= 4 for c in cs),
            "etudes_declarees_valides": sum(e.get("statut") == "valide" and e.get("id") in ids and e.get("domaine") == cle for e in etudes)})
    for s in catalogue["specialites"]:
        rattaches = {c["id"] for c in chapitres if c["id"].rsplit(".", 1)[0] in s["branches"]}
        resultat["specialites"].append({**s, "chapitres_rattaches": len(rattaches),
            "cartes_rattachees": None if cartes is None else sum(c.get("chapitre") in rattaches for c in cartes)})
    return resultat


def markdown(r):
    lignes = ["# Couverture éditoriale copro", "", r["portee"], "",
        "Généré par `python3 app/couverture_expertises.py --write`. Ne pas éditer les compteurs.", "",
        "Une carte valide ici signifie son statut dans l'artefact, pas une nouvelle revue du fond.",
        "Les études sont comptées par statut déclaré dans les fichiers source ; les valideurs restent requis.", "",
        "| Domaine | Chapitres prévus | Cartes artefact | N4/N5 servies localement | Études déclarées valides |",
        "|---|---:|---:|---:|---:|"]
    def valeur(v):
        return "inconnu" if v is None else str(v)
    for d in r["domaines"]:
        lignes.append(f"| {d['titre']} | {d['chapitres_prevus']} | {valeur(d['cartes_artefact'])} | {valeur(d['cartes_n4_n5'])} | {d['etudes_declarees_valides']} |")
    lignes += ["", f"Cartes copro sans rattachement exact à un chapitre : {valeur(r['cartes_sans_chapitre'])}.", "",
        "## Spécialisations à construire", "",
        "Les cartes rattachées peuvent se retrouver dans plusieurs spécialités : ne pas les additionner.",
        "Ce compteur ne démontre pas que les objectifs ci-dessous sont couverts.", ""]
    for s in r["specialites"]:
        lignes += [f"### {s['titre']}", "", f"Identifiant : `{s['id']}`. Statut : {s['statut']}.", "",
            "Objectifs : " + " ; ".join(s["objectifs"]) + ".", "",
            f"Production attendue : {s['production']}.", "", f"Limite : {s['limite']}.", "",
            "Sources à instruire (pas une lecture attestée) : " + " ; ".join(s["sources_a_instruire"]) + ".", "",
            "Branches communes : " + ", ".join(f"`{b}`" for b in s["branches"]) + ".", "",
            f"{s['chapitres_rattaches']} chapitres thématiquement rattachés ; {valeur(s['cartes_rattachees'])} cartes avec rattachement exact.", ""]
    lignes += ["## Empreintes des entrées", "", "Ces empreintes permettent de détecter un rapport périmé ; elles ne prouvent pas un déploiement.", ""]
    for chemin, empreinte in r.get("entrees", {}).items():
        lignes.append(f"- `{chemin}` : `{empreinte}`")
    return "\n".join(lignes) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="régénérer le rapport local")
    ap.add_argument("--check", action="store_true", help="refuser un rapport périmé")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    chemins = [ROOT / "programme/specialisations/copro.json", ROOT / "programme/copro.json", ROOT / "site/banque.json"]
    chemins += sorted((ROOT / "chapitres").rglob("*.json"))
    def lire(p):
        return json.loads(p.read_text())
    r = construire(lire(chemins[0]), lire(chemins[1]), lire(chemins[2]) if chemins[2].exists() else None,
                   [lire(p) for p in chemins[3:]])
    r["entrees"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "absent" for p in chemins}
    rendu = markdown(r)
    cible = ROOT / "travail/expertise-2026-09-06/COUVERTURE.md"
    if args.check:
        if not cible.exists() or cible.read_text() != rendu:
            print("Rapport périmé ou absent : python3 app/couverture_expertises.py --write")
            return 1
        print("Couverture éditoriale : rapport cohérent avec les entrées locales")
    elif args.write:
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(rendu)
        print(cible)
    else:
        print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else rendu, end="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

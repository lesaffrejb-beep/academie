#!/usr/bin/env python3
"""Préparer un dossier, contrôler sa cohérence ; aucun jugement pédagogique automatique."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((RACINE / "contrats/chemin-apprentissage-v1.schema.json").read_text())


def _forme(v, s, p="chemin"):
    """Sous-ensemble JSON Schema utilisé par notre contrat fermé, sans dépendance."""
    if "$ref" in s:
        return _forme(v, SCHEMA["$defs"][s["$ref"].split("/")[-1]], p)
    erreurs = []
    if "const" in s and (v != s["const"] or isinstance(v, bool) != isinstance(s["const"], bool)):
        erreurs.append(f"{p} : valeur attendue {s['const']}")
    if "enum" in s and v not in s["enum"]: erreurs.append(f"{p} : valeur inconnue")
    types = {"object": dict, "array": list, "string": str, "integer": int}
    if "type" in s and (not isinstance(v, types[s["type"]]) or s["type"] == "integer" and isinstance(v, bool)):
        return erreurs + [f"{p} : type attendu {s['type']}"]
    for sous in s.get("allOf", []): erreurs += _forme(v, sous, p)
    if "if" in s:
        erreurs += _forme(v, s.get("else" if _forme(v, s["if"], p) else "then", {}), p)
    if "oneOf" in s and sum(not _forme(v, sous, p) for sous in s["oneOf"]) != 1:
        erreurs.append(f"{p} : choisir exactement chapitre ou proposition")
    if "not" in s and not _forme(v, s["not"], p): erreurs.append(f"{p} : combinaison interdite")
    if isinstance(v, dict):
        erreurs += [f"{p}.{k} : obligatoire" for k in s.get("required", []) if k not in v]
        props = s.get("properties", {})
        for k, valeur in v.items():
            if k in props: erreurs += _forme(valeur, props[k], f"{p}.{k}")
            elif s.get("additionalProperties") is False: erreurs.append(f"{p}.{k} : champ inconnu")
    if isinstance(v, list):
        if len(v) < s.get("minItems", 0): erreurs.append(f"{p} : liste incomplète")
        if s.get("uniqueItems") and len({json.dumps(x, sort_keys=True) for x in v}) != len(v):
            erreurs.append(f"{p} : doublons")
        for i, valeur in enumerate(v): erreurs += _forme(valeur, s.get("items", {}), f"{p}[{i}]")
    if isinstance(v, str):
        if len(v) < s.get("minLength", 0) or "pattern" in s and not re.search(s["pattern"], v):
            erreurs.append(f"{p} : texte absent ou format incorrect")
    if type(v) is int and not s.get("minimum", v) <= v <= s.get("maximum", v):
        erreurs.append(f"{p} : nombre hors limites")
    return erreurs


def _lit(p):
    return json.loads(p.read_text(encoding="utf-8"))


def _catalogue(racine, metier):
    programmes = {p.stem: _lit(p) for p in (racine / "programme").glob("*.json") if p.stem != "catalogue"}
    if metier not in programmes: raise ValueError(f"Métier absent du programme : {metier}")
    tous = {c["id"] for prog in programmes.values() for c in prog.get("chapitres", [])}
    choisis = {c["id"] for c in programmes[metier].get("chapitres", [])}
    for p in (racine / "chapitres").rglob("*.json"):
        c = _lit(p)
        if c.get("satellite") and c.get("rattachement_propose") in tous:
            tous.add(c["id"])
            if c["rattachement_propose"] in choisis: choisis.add(c["id"])
    return choisis, tous


def _servie(cid, banque, metier):
    l = banque.get("etudes", {}).get("lecons", {}).get(cid, {})
    retenues = set(banque.get("metiers", {}).get(metier, {}).get("cartes", []))
    cartes = {c["id"]: c for c in banque.get("cartes", [])}
    def valide(obj, lecon=False):
        if obj.get("statut") != "valide": return False
        p = obj.get("peremption")
        # cartesServiables n'assimile ni false ni 0 à une date absente.
        # etudeDisponible ignore ces deux valeurs falsy au niveau de la leçon.
        absente = p is None or p == "" or lecon and (p is False or type(p) in (int, float) and p == 0)
        if not absente:
            if not isinstance(p, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", p): return False
            try:
                if date.fromisoformat(p) < date.today(): return False
            except ValueError: return False
        if lecon and any(s.get("nature") in ("texte-officiel", "jurisprudence") for s in obj.get("sources", [])):
            try:
                v = obj["verifie"]
                if not isinstance(v, str) or not re.match(r"^\d{4}-\d{2}-\d{2}(?:$|T)", v): return False
                verification = datetime.fromisoformat(v.replace("Z", "+00:00"))
                jour = verification.astimezone(timezone.utc).date() if verification.tzinfo else verification.date()
                if (date.today() - jour).days > 365: return False
            except (ValueError, KeyError): return False
        return True
    return (valide(l, lecon=True) and bool(l.get("cartes")) and isinstance(l.get("verifie_par"), dict)
            and bool(l["verifie_par"]) and all(c in retenues and valide(cartes.get(c, {})) for c in l["cartes"]))


def verifie(dossier, racine=RACINE, strict_local=False, banque=None):
    racine = Path(racine)
    erreurs = _forme(dossier, SCHEMA)
    resultat = {"statut": "cohérence structurelle", "coherent": False, "erreurs": erreurs,
                "sources_manquantes": [], "limites": ["Ni jugement pédagogique, ni validation d'acquis, ni publication."]}
    if erreurs: return resultat
    d = dossier
    try:
        choisis, tous = _catalogue(racine, d["metier"])
        if banque is None and (racine / "site/banque.json").is_file(): banque = _lit(racine / "site/banque.json")
        if isinstance(banque, (str, Path)): banque = _lit(Path(banque))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        erreurs.append(f"Contexte illisible : {exc}"); return resultat
    if banque is None: resultat["limites"].append("Aucun artefact : aucune disponibilité ne peut être affirmée.")
    def reference(cid, autorises, emplacement):
        if cid not in autorises: erreurs.append(f"{emplacement} : chapitre inconnu ou hors cursus ({cid})")
    reference(d["ancrage"]["chapitre"], choisis, "ancrage")
    for acquis in d["prerequis"]:
        if "chapitre" in acquis: reference(acquis["chapitre"], tous, "prerequis")
        if "date" in acquis:
            try:
                if date.fromisoformat(acquis["date"]) > date.today(): raise ValueError("date future")
            except ValueError: erreurs.append("prerequis : date de preuve invalide")
    def indexe(elements, nom):
        index = {e["id"]: e for e in elements}
        if len(index) != len(elements): erreurs.append(f"{nom} : identifiants dupliqués")
        return index
    sources = indexe(d["sources"], "sources"); etapes = indexe(d["etapes"], "etapes")
    resultat["sources_manquantes"] = [s["id"] for s in sources.values() if s["statut"] == "a_trouver"]
    for s in sources.values():
        if s["statut"] == "presente" and strict_local:
            p = Path(s["chemin_original"]); p = p if p.is_absolute() else racine / p
            try:
                with p.open("rb") as f: empreinte = hashlib.file_digest(f, "sha256").hexdigest()
                if empreinte != s["empreinte"]: erreurs.append(f"source {s['id']} : empreinte divergente")
            except OSError: erreurs.append(f"source {s['id']} : original absent ou illisible")
    def suites(ids, lieu):
        for i in ids:
            if i not in etapes: erreurs.append(f"{lieu} : étape inconnue ({i})")
    suites(d["diagnostic"]["reussite"], "diagnostic réussite"); suites(d["diagnostic"]["echec"], "diagnostic échec")
    for e in etapes.values():
        if "chapitre" in e: reference(e["chapitre"], choisis, e["id"])
        for lien in e["transversalites"]: reference(lien["chapitre"], tous, "transversalité")
        suites(e["dependances"], "dépendance"); suites(e["reprise_echec"]["etapes"], "reprise")
        refs = set(e["sources"]) | {s for x in e["exercices"] for s in x["sources"]}
        for s in refs:
            if s not in sources: erreurs.append(f"{e['id']} : source inconnue ({s})")
        if e["disponibilite"] == "disponible":
            try: disponible = "chapitre" in e and isinstance(banque, dict) and _servie(e["chapitre"], banque, d["metier"])
            except (KeyError, TypeError, AttributeError, ValueError): disponible = False
            if not disponible:
                erreurs.append(f"{e['id']} : aucune étude effectivement servie pour cette disponibilité")
            if any(sources.get(s, {}).get("statut") != "presente" for s in refs):
                erreurs.append(f"{e['id']} : disponibilité incompatible avec une source manquante")
        for x in e["exercices"]:
            if "support" in x and strict_local:
                p = Path(x["support"]["chemin"]); p = p if p.is_absolute() else racine / p
                if not p.is_file(): erreurs.append(f"{e['id']} : support absent")
    # Tri de Kahn : profondeur non limitée par la récursion Python.
    restants = {i: set(e["dependances"]) & etapes.keys() for i, e in etapes.items()}
    while restants:
        libres = {i for i, deps in restants.items() if not deps}
        if not libres: erreurs.append("Dépendances : cycle entre étapes"); break
        restants = {i: deps - libres for i, deps in restants.items() if i not in libres}
    if not strict_local: resultat["limites"].append("Originaux et supports non vérifiés sur disque : utiliser --strict-local.")
    resultat["coherent"] = not erreurs
    return resultat


def main():
    parser = argparse.ArgumentParser(description=__doc__); sous = parser.add_subparsers(dest="action", required=True)
    prep = sous.add_parser("preparer"); prep.add_argument("--demande", required=True); prep.add_argument("--metier", required=True)
    prep.add_argument("--sortie", type=Path, required=True); prep.add_argument("--racine", type=Path, default=RACINE)
    ver = sous.add_parser("verifier"); ver.add_argument("chemin", type=Path); ver.add_argument("--racine", type=Path, default=RACINE)
    ver.add_argument("--strict-local", action="store_true"); ver.add_argument("--banque", type=Path)
    args = parser.parse_args()
    try:
        if args.action == "preparer":
            if not args.demande.strip() or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.metier): raise ValueError("Demande ou métier vide/invalide")
            choisis, _ = _catalogue(args.racine, args.metier)
            d = {"version": 1, "statut": "brouillon", "demande": args.demande, "metier": args.metier,
                 "cible_observable": "", "ancrage": {"chapitre": "", "justification": ""}, "prerequis": [],
                 "diagnostic": {"productions": [], "reussite": [], "echec": []}, "etapes": [], "sources": [],
                 "contexte": {"chapitres_existants": sorted(choisis), "a_instruire": "Cible, ancrage, diagnostic et étapes à construire avec l'agent ; aucun acquis supposé."}}
            args.sortie.parent.mkdir(parents=True, exist_ok=True)
            with args.sortie.open("x", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
            print(json.dumps({"statut": "brouillon à instruire", "fichier": str(args.sortie)}, ensure_ascii=False)); return 0
        r = verifie(_lit(args.chemin), args.racine, args.strict_local, args.banque)
        print(json.dumps(r, ensure_ascii=False, indent=2)); return 0 if r["coherent"] else 1
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(json.dumps({"statut": "cohérence structurelle", "coherent": False, "erreurs": [str(exc)]}, ensure_ascii=False)); return 1


if __name__ == "__main__": raise SystemExit(main())

#!/usr/bin/env python3
"""Inventaire éditorial déterministe ; ni certification ni constat du VPS.

Le rapport global décrit tous les domaines et toutes les spécialisations
d'un coup. `--specialite <id>` et `--domaine <id>` en donnent un extrait
ciblé, pour trouver ce qui existe déjà sur un thème sans relire le dépôt
entier. Ni l'un ni l'autre ne lit un état joueur, et aucun des deux ne
recalcule un total global (ACA-EXPERTISE-1, annexe du 21/09/2026).
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
RAPPORT_GLOBAL = ROOT / "travail/expertise-2026-09-06/COUVERTURE.md"
NOTE_SOCLE = ("Les compteurs de domaines incluent les cartes du socle et les cartes sans chapitre. "
              "Les compteurs de spécialités exigent un rattachement exact au socle. Les études et "
              "cartes satellites sont exclues ; zéro dans une spécialité ne signifie pas absence de "
              "contenu sur le thème.")
PORTEE = ("Artefact local seulement ; rattachement thématique, pas couverture des objectifs ni "
          "expertise acquise. " + NOTE_SOCLE)
NOTE_ARTEFACT = ("Une carte valide ici signifie son statut déclaré dans l'artefact local, pas une "
                 "nouvelle revue du fond ni un contenu actuellement servi à un joueur. Un artefact "
                 "absent reste inconnu.")
NOTE_ETUDES = ("Les études sont comptées par statut déclaré dans les fichiers source ; les "
               "valideurs restent requis.")
SEMANTIQUE_FILTRE = ("Extrait ciblé : seuls les objets nommés sont affichés ; ce filtre ne réduit, "
                     "n'additionne et ne recalcule aucun total global.")
ENTETES_DOMAINES = ("| Domaine | Chapitres prévus | Cartes artefact | Cartes artefact N4/N5 | "
                    "Études déclarées valides |")
SEPARATEUR_DOMAINES = "|---|---:|---:|---:|---:|"
LABEL_TYPE = {"domaine": "domaine", "specialite": "spécialité"}


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
    resultat = {"portee": PORTEE,
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


def filtrer(r, programme, specialite=None, domaine=None):
    """Extrait ciblé du rapport : rien n'est relu sur disque, rien n'est additionné.

    Un identifiant inconnu lève une erreur qui nomme les identifiants
    utilisables ; l'extrait ne renseigne pas le compteur global de cartes
    sans rattachement, qui reste dans le rapport global.
    """
    if (specialite is None) == (domaine is None):
        raise ValueError("choisir exactement un filtre : --specialite <id> ou --domaine <id>")
    chapitres = programme["chapitres"]
    extrait = {"portee": r["portee"], "hors_extrait": ["cartes_sans_chapitre"],
               "entrees": r.get("entrees", {})}
    if domaine is not None:
        choisi = next((d for d in r["domaines"] if d["id"] == domaine), None)
        if choisi is None:
            raise ValueError(_inconnu("domaine", domaine, [d["id"] for d in r["domaines"]]))
        extrait["filtre"] = {"type": "domaine", "id": choisi["id"], "titre": choisi["titre"],
                             "semantique": SEMANTIQUE_FILTRE}
        extrait["domaines"] = [choisi]
        extrait["specialites"] = _specialites_du_domaine(r["specialites"], domaine)
        extrait["chapitres"] = _chapitres([c for c in chapitres if c["domaine"] == domaine])
        return extrait
    choisi = next((s for s in r["specialites"] if s["id"] == specialite), None)
    if choisi is None:
        raise ValueError(_inconnu("spécialité", specialite, [s["id"] for s in r["specialites"]]))
    branches = set(choisi["branches"])
    extrait["filtre"] = {"type": "specialite", "id": choisi["id"], "titre": choisi["titre"],
                         "semantique": SEMANTIQUE_FILTRE}
    extrait["domaines"] = [d for d in r["domaines"]
                           if any(b.split(".", 1)[0] == d["id"] for b in branches)]
    extrait["specialites"] = [choisi]
    extrait["chapitres"] = _chapitres([c for c in chapitres
                                       if c["id"].rsplit(".", 1)[0] in branches])
    return extrait


def _inconnu(nom, demande, utilisables):
    return f"{nom} inconnu : {demande} ; identifiants utilisables : {', '.join(sorted(utilisables))}"


def _specialites_du_domaine(specialites, domaine):
    """Rattachement thématique déclaré ; les compteurs portent la spécialité entière."""
    retenues = []
    for s in specialites:
        branches = [b for b in s["branches"] if isinstance(b, str) and b.split(".", 1)[0] == domaine]
        if branches:
            retenues.append({"id": s["id"], "titre": s["titre"], "statut": s["statut"],
                             "branches": s["branches"], "branches_dans_le_domaine": branches,
                             "chapitres_rattaches": s["chapitres_rattaches"],
                             "cartes_rattachees": s["cartes_rattachees"]})
    return retenues


def _chapitres(chapitres):
    return [{"id": c["id"], "titre": c.get("titre", ""), "niveau": c.get("niveau"),
             "domaine": c["domaine"], "branche": c.get("branche")} for c in chapitres]


def markdown(r):
    """Rendu lisible : le rapport global d'abord, l'extrait ciblé ensuite."""
    return _markdown_extrait(r) if r.get("filtre") else _markdown_global(r)


def _valeur(v):
    return "inconnu" if v is None else str(v)


def _nombre(valeur, singulier, pluriel):
    if valeur is None:
        return "inconnu (artefact absent)"
    return f"{valeur} {singulier if valeur in (0, 1) else pluriel}"


def _markdown_global(r):
    lignes = ["# Couverture éditoriale copro", "", r["portee"], "",
        "Généré par `python3 app/couverture_expertises.py --write`. Ne pas éditer les compteurs.", "",
        NOTE_ARTEFACT, NOTE_ETUDES, NOTE_SOCLE, "", ENTETES_DOMAINES, SEPARATEUR_DOMAINES]
    for d in r["domaines"]:
        lignes.append(f"| {d['titre']} | {d['chapitres_prevus']} | {_valeur(d['cartes_artefact'])} | {_valeur(d['cartes_n4_n5'])} | {d['etudes_declarees_valides']} |")
    lignes += ["", f"Cartes copro sans rattachement exact à un chapitre : {_valeur(r['cartes_sans_chapitre'])}.", "",
        "## Spécialisations à construire", "",
        "Les cartes rattachées peuvent se retrouver dans plusieurs spécialités : ne pas les additionner.",
        "Ce compteur ne démontre pas que les objectifs ci-dessous sont couverts.", ""]
    for s in r["specialites"]:
        lignes += _section_specialite(s)
    lignes += _empreintes(r)
    return "\n".join(lignes) + "\n"


def _section_specialite(s, niveau="###", compteurs=True):
    lignes = [f"{niveau} {s['titre']}", "", f"Identifiant : `{s['id']}`. Statut : {s['statut']}.", "",
        "Objectifs : " + " ; ".join(s["objectifs"]) + ".", "",
        f"Production attendue : {s['production']}.", "", f"Limite : {s['limite']}.", "",
        "Sources à instruire (pas une lecture attestée) : " + " ; ".join(s["sources_a_instruire"]) + ".", "",
        "Branches communes : " + ", ".join(f"`{b}`" for b in s["branches"]) + ".", ""]
    if compteurs:
        lignes += [f"{s['chapitres_rattaches']} chapitres thématiquement rattachés ; {_valeur(s['cartes_rattachees'])} cartes avec rattachement exact.", ""]
    return lignes


def _empreintes(r):
    lignes = ["## Empreintes des entrées", "", "Ces empreintes permettent de détecter un rapport périmé ; elles ne prouvent pas un déploiement.", ""]
    for chemin, empreinte in r.get("entrees", {}).items():
        lignes.append(f"- `{chemin}` : `{empreinte}`")
    return lignes


def _markdown_extrait(r):
    f = r["filtre"]
    lignes = [f"# Couverture éditoriale copro : {LABEL_TYPE[f['type']]} `{f['id']}`, {f['titre']}", "",
        r["portee"], "", f["semantique"],
        f"Extrait recalculable par `python3 app/couverture_expertises.py --{f['type']} {f['id']}`. "
        "Ne pas éditer les compteurs.", "", NOTE_ARTEFACT, NOTE_ETUDES, NOTE_SOCLE, "",
        f"Compteur global non calculé dans cet extrait : {' ; '.join('`' + c + '`' for c in r['hors_extrait'])}. "
        "Il reste dans le rapport global.", ""]
    lignes += _resume(r)
    if f["type"] == "specialite":
        lignes += _section_specialite(r["specialites"][0], "##", compteurs=False)
    lignes += _table_domaines(r)
    lignes += _table_chapitres(r)
    if f["type"] == "domaine":
        lignes += _table_specialites_du_domaine(r)
    lignes += _empreintes(r)
    return "\n".join(lignes) + "\n"


def _resume(r):
    f = r["filtre"]
    lignes = ["## En bref", ""]
    if f["type"] == "domaine":
        d = r["domaines"][0]
        note_niveau = " (niveau déclaré, pas un contenu servi)" if d["cartes_n4_n5"] is not None else ""
        lignes += [
            f"- Domaine `{d['id']}` : {d['titre']}.",
            f"- Programme : {_nombre(len(r['chapitres']), 'chapitre prévu', 'chapitres prévus')} dans ce domaine.",
            f"- Artefact local : {_nombre(d['cartes_artefact'], 'carte valide de l\'artefact dans ce domaine', 'cartes valides de l\'artefact dans ce domaine')} (socle et cartes sans chapitre).",
            f"- Niveau 4 ou 5 : {_nombre(d['cartes_n4_n5'], 'carte artefact de niveau 4 ou 5', 'cartes artefact de niveau 4 ou 5')}{note_niveau}.",
            f"- Études : {_nombre(d['etudes_declarees_valides'], 'étude déclarée valide', 'études déclarées valides')} dans ce domaine.",
            f"- Spécialités : {_nombre(len(r['specialites']), 'spécialité déclare', 'spécialités déclarent')} au moins une branche dans ce domaine (rattachement thématique déclaré, pas une couverture des objectifs).",
        ]
    else:
        s = r["specialites"][0]
        lignes += [
            f"- Spécialité `{s['id']}` : {s['titre']}.",
            f"- Statut déclaré dans le catalogue : {s['statut']} (ce catalogue ne certifie aucune spécialité construite).",
            f"- Branches thématiques déclarées : {', '.join('`' + b + '`' for b in s['branches'])}.",
            f"- Chapitres : {_nombre(s['chapitres_rattaches'], 'chapitre thématiquement rattaché', 'chapitres thématiquement rattachés')} dans le programme.",
            f"- Artefact local : {_nombre(s['cartes_rattachees'], 'carte rattachée à un chapitre', 'cartes rattachées à un chapitre')} (rattachement exact au socle ; les études et cartes satellites sont exclues ; ne démontre pas la couverture des objectifs).",
            f"- Domaines touchés par ces branches : {len(r['domaines'])}.",
            f"- Sources à instruire : {len(s['sources_a_instruire'])} annoncées, aucune n'est une lecture attestée.",
        ]
    return lignes + [""]


def _table_domaines(r):
    if not r["domaines"]:
        return []
    note = [] if r["filtre"]["type"] == "domaine" else [
        "Ces compteurs portent le domaine entier, pas la seule spécialité.", ""]
    titre = ("## Compteurs du domaine" if r["filtre"]["type"] == "domaine"
             else "## Compteurs des domaines touchés")
    lignes = [titre, "", ENTETES_DOMAINES, SEPARATEUR_DOMAINES]
    for d in r["domaines"]:
        lignes.append(f"| {d['titre']} | {d['chapitres_prevus']} | {_valeur(d['cartes_artefact'])} | {_valeur(d['cartes_n4_n5'])} | {d['etudes_declarees_valides']} |")
    return lignes + [""] + note


def _table_chapitres(r):
    titre = ("## Chapitres prévus dans ce domaine" if r["filtre"]["type"] == "domaine"
             else "## Chapitres thématiquement rattachés")
    lignes = [titre, "",
              "Rattachement par le préfixe de branche du programme ; ce n'est ni un prérequis ni une couverture.",
              "", "| Chapitre | Niveau | Titre |", "|---|---:|---|"]
    for c in r["chapitres"]:
        lignes.append(f"| `{c['id']}` | {_valeur(c['niveau'])} | {c['titre']} |")
    if not r["chapitres"]:
        lignes.append("| | | Aucun chapitre prévu sous ces branches |")
    return lignes + [""]


def _table_specialites_du_domaine(r):
    lignes = ["## Spécialités déclarant une branche dans ce domaine", "",
              "| Spécialité | Branches dans ce domaine | Chapitres rattachés | Cartes rattachées |",
              "|---|---|---:|---:|"]
    for s in r["specialites"]:
        branches = ", ".join(f"`{b}`" for b in s["branches_dans_le_domaine"])
        lignes.append(f"| `{s['id']}` {s['titre']} | {branches} | {s['chapitres_rattaches']} | {_valeur(s['cartes_rattachees'])} |")
    if not r["specialites"]:
        lignes.append("| | | | Aucune spécialité déclarée sous ce domaine |")
    return lignes + ["", "Ces lignes disent un rattachement thématique déclaré, pas une couverture ; "
                      "les compteurs de chapitres et de cartes portent la spécialité entière.", ""]


def _refus(message):
    print(message, file=sys.stderr)
    return 2


def _meme_chemin(un, autre):
    """Compare deux destinations après normalisation, pour protéger le rapport canonique."""
    return Path(un).resolve() == Path(autre).resolve()


def main(argv=None):
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            try:
                flux.reconfigure(encoding="utf-8", errors="replace")
            except (ValueError, OSError):
                pass
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true", help="régénérer le rapport global")
    ap.add_argument("--check", action="store_true", help="refuser un rapport global périmé")
    ap.add_argument("--json", action="store_true", help="sortir le rapport en JSON")
    ap.add_argument("--sortie", metavar="CHEMIN",
                    help="écrire le rendu à cet endroit, par exemple dans sorties/")
    filtres = ap.add_mutually_exclusive_group()
    filtres.add_argument("--specialite", metavar="ID", help="extrait ciblé d'une spécialité")
    filtres.add_argument("--domaine", metavar="ID", help="extrait ciblé d'un domaine")
    args = ap.parse_args(argv)
    if args.check and (args.write or args.sortie or args.specialite or args.domaine):
        return _refus("--check compare le rapport global : il refuse --write, --sortie et tout filtre")
    if args.write and (args.specialite or args.domaine) and not args.sortie:
        return _refus("un extrait filtré n'écrase pas le rapport global : ajouter --sortie <chemin>")
    cible = Path(args.sortie) if args.sortie else (RAPPORT_GLOBAL if args.write else None)
    if cible is not None and _meme_chemin(cible, RAPPORT_GLOBAL):
        if args.json:
            return _refus("le rapport global canonique est en Markdown : --json exige --sortie vers un autre fichier")
        if args.specialite or args.domaine:
            return _refus("un extrait ciblé n'écrase pas le rapport global : donner une autre --sortie")
    chemins = [ROOT / "programme/specialisations/copro.json", ROOT / "programme/copro.json", ROOT / "site/banque.json"]
    chemins += sorted((ROOT / "chapitres").rglob("*.json"))
    def lire(p):
        return json.loads(p.read_text(encoding="utf-8"))
    try:
        r = construire(lire(chemins[0]), lire(chemins[1]), lire(chemins[2]) if chemins[2].exists() else None,
                       [lire(p) for p in chemins[3:]])
        r["entrees"] = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else "absent" for p in chemins}
        if args.specialite or args.domaine:
            r = filtrer(r, lire(chemins[1]), specialite=args.specialite, domaine=args.domaine)
    except ValueError as erreur:
        return _refus(str(erreur))
    rendu = markdown(r)
    if args.check:
        if not RAPPORT_GLOBAL.exists() or RAPPORT_GLOBAL.read_text(encoding="utf-8") != rendu:
            print("Rapport périmé ou absent : python3 app/couverture_expertises.py --write")
            return 1
        print("Couverture éditoriale : rapport cohérent avec les entrées locales")
        return 0
    if cible is not None:
        contenu = json.dumps(r, ensure_ascii=False, indent=2) + "\n" if args.json else rendu
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(contenu, encoding="utf-8")
        print(cible)
        return 0
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else rendu, end="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

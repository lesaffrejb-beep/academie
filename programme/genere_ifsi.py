#!/usr/bin/env python3
"""Rend le syllabus depuis le JSON canonique, sans réécrire le programme.

ACA-IFSI-1. `--check` vérifie aussi que le rendu versionné est à jour.
Les données historiques restent dans programme/versions/ifsi-2009.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
ETAPES = {
    "orientation": "Découvrir le métier",
    "preparation": "Préparer son entrée",
    "annee-1": "Première année",
    "annee-2": "Deuxième année",
    "annee-3": "Troisième année",
    "prise-de-poste": "Prendre son premier poste",
    "specialisation": "Approfondir une spécialité",
    "expertise": "Explorer, rechercher et transmettre",
}


def cellule(valeur: str) -> str:
    return str(valeur).replace("|", "\\|").replace("\n", " ")


def syllabus(prog: dict) -> str:
    ids = {c["id"]: c for c in prog["chapitres"]}
    compte = Counter(c["etape"] for c in ids.values())
    objectifs = sum(len(c["objectifs"]) for c in ids.values())
    L = ["# Entrer en IFSI, devenir infirmier, continuer à apprendre\n",
         f"Programme {prog['referentiel_actif']}, révisé le {prog['genere_le']}. "
         "Source éditable : `programme/ifsi.json`. Ce document est rendu par "
         "`python3 programme/genere_ifsi.py`.\n",
         "Le parcours commence avant l'école, accompagne la formation infirmière, "
         "puis se ramifie vers les spécialités, les cas complexes, la recherche et les "
         "nouvelles recommandations. Il n'y a pas de plafond à l'apprentissage.\n",
         "Ce programme est un inventaire à remplir : les objectifs ci-dessous ne sont "
         "pas encore des leçons ou des cartes jouables. Ce sont des propositions "
         "éditoriales à affiner en capacités observables lors de l'écriture des séances. "
         "Une réussite numérique ne "
         "valide ni un geste clinique ni un stage. Les situations d'entraînement "
         "sont fictives ; aucun dossier ou renseignement réel de patient n'entre dans ce dépôt.\n",
         f"Inventaire courant : **{len(ids)} chapitres et {objectifs} objectifs**, "
         f"dans {len(prog['domaines'])} univers. Ces nombres mesurent le contenu prévu, "
         "pas les compétences acquises.\n",
         "## De l'entrée aux approfondissements\n",
         "Chaque étape indique un premier point d'appui éditorial. Une notion peut "
         "être reprise et approfondie à plusieurs étapes ; ce classement ne fixe pas "
         "le calendrier d'un IFSI. Les exemples ci-dessous orientent la lecture ; "
         "tous les chapitres figurent ensuite dans leur univers.\n",
         "| Étape | Chapitres repérés |", "|---|---|"]
    for cle, titre in ETAPES.items():
        L.append(f"| {titre} | {compte[cle]} |")
    for etape in prog.get("trajectoire", {}).get("etapes", []):
        L += [f"\n### {etape['titre']}\n", etape["objectif"] + "\n"]
        chapitres_etape = [ids[c] for c in etape.get("chapitres", [])]
        if chapitres_etape:
            univers = list(dict.fromkeys(c["domaine"] for c in chapitres_etape))
            exemples = [next(c for c in chapitres_etape if c["domaine"] == dom)
                        for dom in univers][:3]
            exemples += [c for c in chapitres_etape if c not in exemples][:3 - len(exemples)]
            L.append(f"{len(chapitres_etape)} chapitres repérés. Quelques points d'appui : "
                     + " · ".join(c["titre"] for c in exemples) + ".\n")
            L.append("Parcourir les univers : " + " · ".join(
                f"[{prog['domaines'][dom]['titre']}](#univers-{dom})" for dom in univers
            ) + ".\n")
    L += ["\nL'étape est un point d'entrée conseillé, pas un verrou. La difficulté "
          "cognitive va de reconnaître à adapter et justifier ; elle reste indépendante "
          "de l'année de formation. La criticité distingue les erreurs informatives, "
          "importantes et critiques. Doctrine et Frontière sont des modes "
          "d'approfondissement transversaux. Les anciens niveaux sont conservés "
          "dans les données pour la compatibilité.\n",
          "Les prérequis et les ponts relient les branches. Les spécialités réutilisent "
          "ces acquis ; la boîte, la veille et de nouveaux cas ouvrent ensuite de "
          "nouveaux chapitres sourcés. Chaque version se vérifie, l'arbre peut "
          "continuer à pousser.\n",
          "## Le cadre de formation\n",
          "Le cadre courant concerne les entrants à partir de septembre 2026. "
          "Le squelette précédent est conservé dans "
          "[`programme/versions/ifsi-2009.json`](programme/versions/ifsi-2009.json). "
          "Il concerne l'ancien cadre et conserve ses limites. Les situations "
          "de reprise et de redoublement doivent être examinées par l'établissement.\n",
          "Les cinq domaines ci-dessous sont les domaines d'enseignement A à E. "
          "Le rattachement de nos chapitres aux compétences est une proposition "
          "pédagogique, pas une équivalence officielle.\n",
          "| Domaine d'enseignement | Compétences rattachées |", "|---|---|"]
    for cle, d in prog["domaines_enseignement"].items():
        L.append(f"| {cle}. {cellule(d['titre'])} | {', '.join(d['competence_ids'])} |")
    L += ["\n### Textes consultés\n"]
    for source in prog["sources_reglementaires"].values():
        L.append(f"- [{source['titre']}]({source['url']}) : {source['repere']} "
                 f"(consulté le {source['consulte_le']}).")
    L += ["\n## Trois préparations à l'entrée\n",
          "Le diagnostic précède le parcours : français, calcul, bases scientifiques, "
          "numérique et connaissance du métier. Le rythme de douze semaines est "
          "une proposition de travail adaptable, pas une condition d'admission. "
          "L'admissibilité et le calendrier se confirment auprès de l'établissement.\n"]
    for voie, parcours in prog["parcours"].items():
        L += [f"### {parcours['titre']}\n", parcours["objectif"] + "\n",
              "Diagnostic : " + " · ".join(ids[c]["titre"] for c in parcours["diagnostic"]) + ".\n",
              "| Semaine | Thème | Chapitres | Étude |", "|---|---|---|---|"]
        for s in parcours["semaines"]:
            titres = " · ".join(cellule(ids[c]["titre"]) for c in s["chapitres"])
            L.append(f"| {s['n']} | {cellule(s['theme'])} | {titres} | {cellule(ids[s['etude']]['titre'])} |")
        L.append("")
    L += ["## Le programme par univers\n",
          "Pour chaque chapitre : point d'entrée conseillé, difficulté, criticité, "
          "objectifs et limites de l'évaluation numérique. Les durées d'étude sont "
          "des repères éditoriaux adaptables.\n"]
    for dom, d in prog["domaines"].items():
        L += [f'<a id="univers-{dom}"></a>\n',
              f"### {d['ordre']}. {d['titre']}\n", d["pourquoi"] + "\n"]
        for b in prog["branches"][dom]:
            chs = [c for c in ids.values() if c["domaine"] == dom and c["branche"] == b["cle"]]
            L.append(f"#### {b['titre']}\n")
            for c in chs:
                voies = "; voie " + ", ".join(c["voies"]) if len(c["voies"]) < 3 else ""
                option = "; facultatif" if c["optionnel"] else ""
                L.append(f"- **{c['titre']}** : {c['competence']}. "
                         f"{ETAPES[c['etape']]}, difficulté {c['difficulte']}, {c['criticite']}{voies}{option}. "
                         f"Étude {c['etude_minutes']} min. "
                         f"Rattachement : {c['domaine_enseignement']}, compétences {', '.join(c['competence_ids'])}.")
                for o in c["objectifs"]:
                    L.append(f"  - {o['capacite']} ({o['dimension']}, {o['exercice']}).")
                if c["validation"]["geste_supervise"]:
                    L.append("  - Pratique : simulation et réalisation sous supervision à apprécier séparément par un professionnel.")
                if c["prerequis"]:
                    L.append("  - Prérequis : " + " · ".join(ids[p]["titre"] for p in c["prerequis"]) + ".")
                if c["ponts"]:
                    L.append("  - Ponts : " + " · ".join(ids[p]["titre"] for p in c["ponts"]) + ".")
            L.append("")
    L += ["## Après le diplôme : continuer sans plafond\n",
          "Une spécialité approfondit des branches communes et ajoute ses propres "
          "objectifs. Tu peux en explorer plusieurs et revenir sur tes acquis. "
          "L'expertise reste située dans un domaine ; elle n'est pas un grade général.\n"]
    specialisations = prog.get("specialisations", [])
    if isinstance(specialisations, dict):
        specialisations = list(specialisations.values())
    for s in specialisations:
        L.append(f"### {s['titre']}\n")
        for champ in ("objectif", "prolongement", "ouverture"):
            if isinstance(s.get(champ), str):
                L.append(s[champ] + "\n")
        chs = s.get("chapitres", s.get("socle", s.get("reutilise", [])))
        if chs:
            L.append("Points d'appui : " + " · ".join(ids[c]["titre"] for c in chs) + ".\n")
        approfondissements = s.get("approfondissements", [])
        if approfondissements:
            L.append("À approfondir : " + " · ".join(approfondissements) + ".\n")
    L += ["## Ce qu'il reste à transformer en séances\n",
          "Le pilote reliera diabète, traitements, calcul, reconnaissance d'une "
          "situation préoccupante, transmission, éducation et retour à domicile. "
          "Il devra comporter des cas fictifs progressifs et une correction sourcée.\n",
          "La maîtrise par objectif, les erreurs critiques non compensables, la "
          "remédiation, la confiance déclarée et les cas évolutifs sont spécifiés "
          "pour ce pilote. Ils ne sont pas encore implémentés dans le moteur. "
          "Le calcul devra vérifier valeur, unité, ordre de grandeur, cohérence "
          "de la prescription et données manquantes. Aucun résultat numérique "
          "ne certifiera un geste.\n",
          "Avant de servir un contenu : sources à l'échelle des affirmations "
          "sensibles, recherche sur les domaines fiables, provenance, contrôle, "
          "relecture indépendante et revue professionnelle des contenus critiques. "
          "Un seuil, une dose, une durée ou une règle de droit sans source "
          "ne se dit pas.\n",
          "Le [rapport de révision](travail/2026-09-04-revision-ifsi.md) précise "
          "les changements, les preuves et la suite du travail."]
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="vérifier sans écrire")
    args = parser.parse_args(argv)
    sys.path.insert(0, str(RACINE / "app"))
    from valide_programme import valider
    source = RACINE / "programme/ifsi.json"
    try:
        prog = json.loads(source.read_text(encoding="utf-8"))
        erreurs = valider(prog, {}, "ifsi.json")
        if erreurs:
            print("\n".join(erreurs), file=sys.stderr)
            return 1
        texte = syllabus(prog)
        sortie = RACINE / "SYLLABUS-IFSI.md"
        if args.check:
            existant = sortie.read_text(encoding="utf-8").replace("\r\n", "\n") if sortie.exists() else None
            if existant != texte:
                print("SYLLABUS-IFSI.md diffère du programme : relancer le générateur.", file=sys.stderr)
                return 1
        else:
            sortie.write_text(texte, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Programme IFSI illisible ou incomplet : {exc}", file=sys.stderr)
        return 1
    print(f"IFSI : {len(prog['chapitres'])} chapitres, syllabus conforme au JSON.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

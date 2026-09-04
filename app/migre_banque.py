#!/usr/bin/env python3
"""Prepare ACA-CONTRAT-2 selon decisions/0030, sans deplacer la banque.

Sans option, simule en memoire et rend les obstacles du valideur v2.
--staging cree une racine candidate neuve, hors de la source, avec les
chapitres, leurs medias et un rapport. Seul un candidat vert est genere
dans son propre site/. Aucun mode ne supprime, archive ou promeut.

La preparation ne transforme jamais une origine documentaire en nom
d'auteur ou de relecteur. Une absence reste absente et bloque le contrat.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from valide_chapitres import valide_carte, valide_chapitre
from valide_programme import valider as valide_programme

RACINE = Path(__file__).resolve().parents[1]
APP = Path(__file__).resolve().parent

# Table explicite, carte par carte : decisions/0030 et table du 03/09/2026.
ASSIGNATIONS = {
    "comptabilite-annexes-et-anomalies-cinq-annexes": "comptabilite.annexes.l-annexe-1-l-etat-financier",
    "comptabilite-annexes-et-anomalies-ou-lire-ecart-budget": "comptabilite.annexes.l-annexe-2-le-compte-de-gestion-general",
    "comptabilite-annexes-et-anomalies-libelle-14-2-annexe-4": "comptabilite.annexes.les-annexes-4-et-5-les-travaux",
    "comptabilite-annexes-et-anomalies-recoupement-des-soldes": "comptabilite.annexes.les-trois-chiffres-a-regarder-d-abord",
    "comptabilite-annexes-et-anomalies-seuils-ecart-budgetaire": "comptabilite.controle.les-anomalies-classiques",
    "comptabilite-annexes-et-anomalies-fonds-travaux-double-plancher": "comptabilite.budget.le-fonds-de-travaux",
    "comptabilite-annexes-et-anomalies-compte-separe-et-rapprochement": "comptabilite.controle.l-audit-d-un-arrete-des-comptes",
    "comptabilite-annexes-et-anomalies-honoraires-mutation-recouvrement": "comptabilite.honoraires.les-prestations-particulieres",
    "comptabilite-annexes-et-anomalies-solde-travaux-clotures": "comptabilite.annexes.les-annexes-4-et-5-les-travaux",
    "comptabilite-annexes-et-anomalies-rattachement-des-charges": "comptabilite.bases.engagement-et-tresorerie",
    "comptabilite-annexes-et-anomalies-cle-charges-utilite-objective": "droit.charges.les-cles-de-repartition",
    "droit-conformite-statut-non-verifie": "cabinet.cycle-annuel.les-obligations-annuelles",
    "droit-conformite-budget-deux-echeances": "comptabilite.budget.le-budget-previsionnel",
    "droit-conformite-budget-vote-tardif": "comptabilite.budget.le-budget-previsionnel",
    "droit-conformite-provisions-trimestrielles": "comptabilite.budget.les-appels-de-fonds",
    "droit-conformite-fonds-travaux-plancher": "comptabilite.budget.le-fonds-de-travaux",
    "droit-conformite-fonds-travaux-dispenses": "comptabilite.budget.le-fonds-de-travaux",
    "droit-conformite-mandat-syndic-duree": "droit.organes.designation-contrat-fin-de-mandat",
    "droit-conformite-registre-declaration-annuelle": "droit.statut.fiche-synthetique-et-immatriculation",
    "droit-conformite-assurance-rc-syndicat": "droit.responsabilites.l-assurance-obligatoire",
    "droit-conformite-dpe-collectif-champ": "energie.dpe.le-dpe-collectif-et-son-calendrier",
    "droit-conformite-dta-parties-communes": "pathologie.diagnostics.amiante-et-dossier-technique-amiante",
    "droit-conformite-plan-pluriannuel-quinze-ans": "droit.travaux.le-plan-pluriannuel-et-le-fonds-de-travaux",
    "droit-conformite-calendrier-des-vagues": "cabinet.cycle-annuel.les-obligations-annuelles",
    "droit-conformite-petite-copropriete-seuil": "droit.statut.qu-est-ce-qu-une-copropriete",
    "droit-conformite-comptes-engagement": "comptabilite.bases.engagement-et-tresorerie",
    "droit-majorites-article-24": "droit.majorites.l-article-24",
    "droit-majorites-article-25": "droit.majorites.l-article-25-et-la-passerelle",
    "droit-majorites-passerelle-25-1": "droit.majorites.l-article-25-et-la-passerelle",
    "droit-veille-notification-electronique-principe": "droit.assemblee.la-notification",
    "droit-veille-lre-prestataire-qualifie": "droit.assemblee.la-notification",
    "droit-veille-mention-voie-postale": "droit.assemblee.la-notification",
    "droit-veille-point-depart-des-delais": "droit.assemblee.la-notification",
    "droit-veille-pieces-espace-en-ligne": "droit.assemblee.les-pieces-jointes-obligatoires",
    "droit-veille-recouvrement-une-mise-en-demeure-par-exercice": "procedure.recouvrement.l-assignation",
    "droit-veille-recouvrement-ventilation-mise-en-demeure": "procedure.avant-le-proces.mise-en-demeure-recommande-sommation",
    "droit-veille-quitus-portee": "comptabilite.controle.approbation-et-quitus",
    "droit-veille-meuble-tourisme-condition-ouverture": "droit.mutations.changement-d-usage-et-location",
    "droit-veille-isolation-individuelle-toiture-plancher": "droit.travaux.travaux-privatifs-affectant-les-communes",
    "equipements-ascenseur-organes-securite": "equipements.ascenseurs.les-organes-d-un-ascenseur",
    "equipements-ascenseur-controle-quinquennal": "equipements.ascenseurs.le-controle-technique-quinquennal",
    "equipements-ascenseur-entretien-obligatoire": "equipements.ascenseurs.le-contrat-de-maintenance",
    "equipements-chauffage-poste-p1": "equipements.chauffage.les-contrats-p1-a-p5",
    "equipements-chauffage-p2-contre-p3": "equipements.chauffage.les-contrats-p1-a-p5",
    "equipements-chauffage-p4-amortissement": "equipements.chauffage.les-contrats-p1-a-p5",
    "equipements-chauffage-role-defense-p3": "equipements.chauffage.les-contrats-p1-a-p5",
    "equipements-chauffage-libre-expliquer-p3-au-cs": "equipements.chauffage.les-contrats-p1-a-p5",
    "equipements-vmc-composants-caisson": "equipements.ventilation.le-caisson-et-les-courroies",
    "equipements-vmc-caisson-legende": "equipements.ventilation.le-caisson-et-les-courroies",
    "equipements-vmc-composants-roles": "equipements.ventilation.le-caisson-et-les-courroies",
    "equipements-vmc-courroie-detente": "equipements.ventilation.le-caisson-et-les-courroies",
    "equipements-vmc-gaz-securite-collective": "equipements.ventilation.entretien-et-debits-reglementaires",
    "pathologie-fissures-retrait-differentiel": "pathologie.structure.microfissure-fissure-lezarde",
    "pathologie-fissures-appui-plancher-horizontale": "pathologie.structure.fissures-structurelles-et-leur-lecture",
    "pathologie-fissures-traversantes-infiltrations": "pathologie.structure.fissures-structurelles-et-leur-lecture",
    "pathologie-fissures-retrait-gonflement-argiles": "pathologie.structure.fondations-et-tassements",
    "pathologie-humidite-remontee-capillaire-signes": "pathologie.humidite.remontees-capillaires",
    "pathologie-humidite-trois-origines-diagnostic": "pathologie.humidite.un-logement-humide-que-dire-au-coproprietaire",
    "pathologie-humidite-condensation-points-froids": "pathologie.humidite.condensation",
    "pathologie-humidite-enduit-impermeable-aggravant": "pathologie.facades.enduits-et-classes-d-impermeabilite",
    "pathologie-toiture-souche-hauteur-reglementaire": "pathologie.toitures.souches-cheminees-ventilations-primaires",
    "pathologie-toiture-souche-ou-event-de-chute": "pathologie.toitures.souches-cheminees-ventilations-primaires",
    "procedure-recouvrement-exigibilite-provision": "comptabilite.budget.les-appels-de-fonds",
    "procedure-recouvrement-mise-en-demeure-contenu": "procedure.avant-le-proces.mise-en-demeure-recommande-sommation",
    "procedure-recouvrement-mise-en-demeure-deux-effets": "procedure.avant-le-proces.mise-en-demeure-recommande-sommation",
    "procedure-recouvrement-decheance-assiette": "procedure.recouvrement.la-decheance-du-terme",
    "procedure-recouvrement-datation-decheance": "procedure.recouvrement.la-decheance-du-terme",
    "procedure-recouvrement-plan-deux-voies": "procedure.recouvrement.choisir-la-voie",
    "procedure-recouvrement-frais-relance-simple": "comptabilite.impayes.les-frais-imputables",
    "procedure-recouvrement-article-700": "comptabilite.impayes.les-frais-imputables",
    "procedure-recouvrement-autorisation-assemblee": "procedure.contentieux-ag.l-autorisation-d-agir-en-justice",
    "procedure-recouvrement-commissaire-de-justice": "procedure.acteurs.le-commissaire-de-justice",
    "procedure-recouvrement-libre-frais-au-conseil": "comptabilite.impayes.les-frais-imputables",
    "procedure-recouvrement-role-debiteur-au-telephone": "cabinet.cas-transverses.un-impaye-de-dix-huit-mois",
    "sinistres-delai-degat-des-eaux": "sinistres.contrat.les-delais-de-declaration",
    "sinistres-delai-vol-vandalisme": "sinistres.contrat.les-delais-de-declaration",
    "sinistres-delai-catastrophe-naturelle": "sinistres.contrat.les-delais-de-declaration",
    "sinistres-decheance-de-garantie": "sinistres.contrat.garantie-et-exclusion",
    "sinistres-irsi-tranches": "sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches",
    "sinistres-irsi-assureur-gestionnaire": "sinistres.degat-des-eaux.l-assureur-gestionnaire",
    "sinistres-recherche-de-fuite": "sinistres.degat-des-eaux.la-recherche-de-fuite",
    "sinistres-cidre-abrogee": "sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches",
    "sinistres-priorite-par-gravite": "sinistres.autres-sinistres.les-mesures-conservatoires",
    "sinistres-mesures-conservatoires-sans-ag": "sinistres.autres-sinistres.les-mesures-conservatoires",
}


def lit_json(fichier: Path):
    return json.loads(fichier.read_text(encoding="utf-8"))


def ecrit_json(fichier: Path, valeur) -> None:
    fichier.parent.mkdir(parents=True, exist_ok=True)
    fichier.write_text(json.dumps(valeur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def empreinte(fichier: Path) -> str:
    return hashlib.sha256(fichier.read_bytes()).hexdigest()


def empreintes_source(racine: Path) -> dict[str, str]:
    fichiers = set((racine / "banque").rglob("*.json"))
    fichiers.update((racine / "chapitres").rglob("*.json"))
    fichiers.update(f for f in (racine / "programme").glob("*.json") if f.name != "catalogue.json")
    fichiers.update(f for f in (racine / "banque/images").rglob("*") if f.is_file())
    fichiers.add(racine / "academie.json")
    return {str(f.relative_to(racine)): empreinte(f) for f in sorted(fichiers)}


def controle_source(racine: Path, rapport: dict) -> bool:
    try:
        rapport["source_inchangee"] = empreintes_source(racine) == rapport["empreintes_source"]
    except OSError:
        rapport["source_inchangee"] = False
    if not rapport["source_inchangee"]:
        rapport["pret_pour_revue"] = False
        motif = "source modifiee : inventaire ou empreintes differents de la preparation"
        if motif not in rapport["erreurs_validation"]:
            rapport["erreurs_validation"].append(motif)
    return rapport["source_inchangee"]


def nouveau_chapitre(entree: dict, carte: dict) -> dict:
    """Squelette explicite : pas de lecon ni de relecture inventee pour passer."""
    return {
        **{k: copy.deepcopy(entree[k]) for k in
           ("id", "titre", "domaine", "branche", "niveau", "prerequis")},
        "objectifs": [], "amorce": {}, "lecon": "[à écrire]", "synthese": {},
        "cartes": [], "sources": [],
        "provenance": {"genere_le": carte["verifie"], "sources_retrouvees": 0, "sans_source": False},
        "statut": "brouillon", "partage": carte["partage"], "verifie": carte["verifie"], "version": 1,
    }


def prepare(racine: Path) -> tuple[dict, dict[str, dict], list[dict]]:
    avant_lecture = empreintes_source(racine)
    fichiers_programme = sorted(f for f in (racine / "programme").glob("*.json") if f.name != "catalogue.json")
    academie = lit_json(racine / "academie.json")
    erreurs_programme = []
    programme = {}
    for f in fichiers_programme:
        prog = lit_json(f)
        aligne = academie if academie.get("metier") == prog.get("metier") else {}
        erreurs_programme.extend(valide_programme(prog, aligne, f.name))
        for ch in prog.get("chapitres", []):
            if ch["id"] in programme:
                raise ValueError(f"chapitre du programme duplique : {ch['id']}")
            programme[ch["id"]] = ch
    if not programme:
        raise ValueError("programme absent ou vide")
    fichiers_banque = sorted((racine / "banque").rglob("*.json"))
    if not fichiers_banque:
        raise ValueError("aucun fichier de banque v1 a preparer")
    fichiers_chapitres = sorted((racine / "chapitres").rglob("*.json"))
    chapitres, chemins = {}, {}
    for f in fichiers_chapitres:
        ch = lit_json(f)
        if ch["id"] in chapitres:
            raise ValueError(f"chapitre duplique : {ch['id']}")
        chapitres[ch["id"]] = ch
        chemins[ch["id"]] = str(f.relative_to(racine))
    ids_existants = [c["id"] for ch in chapitres.values() for c in ch.get("cartes", [])]
    cartes = []
    for f in fichiers_banque:
        lot = lit_json(f)
        if not isinstance(lot, list):
            raise ValueError(f"{f} : la banque v1 doit contenir des tableaux")
        cartes.extend(lot)
    comptes = Counter(ids_existants + [c["id"] for c in cartes])
    rapport = {
        "decision": "0030", "date": date.today().isoformat(), "source": str(racine),
        "cartes_v1": len(cartes), "cartes_v1_par_statut": dict(Counter(c["statut"] for c in cartes)),
        "cartes_v2_existantes": len(ids_existants), "changements_domaine": [],
        "sans_assignation": [], "chapitres_absents": [], "auteurs_manquants": [],
        "relecteurs_manquants": [], "niveaux_incompatibles": [], "natures_completees": [],
        "chapitres_a_ecrire": [], "doublons": sorted(k for k, n in comptes.items() if n > 1),
        "empreintes_source": avant_lecture,
        "erreurs_validation": erreurs_programme,
    }
    non_assignees = []
    nouveaux = set()
    for originale in cartes:
        cid = originale["id"]
        cible = ASSIGNATIONS.get(cid)
        if cible is None or cible not in programme:
            rapport["sans_assignation" if cible is None else "chapitres_absents"].append(cid)
            non_assignees.append(copy.deepcopy(originale))
            continue
        entree = programme[cible]
        carte = copy.deepcopy(originale)
        carte.update(chapitre=cible, domaine=entree["domaine"], branche=entree["branche"])
        for i, src in enumerate(carte.get("source", [])):
            if not src.get("nature"):
                src["nature"] = "editeur"
                rapport["natures_completees"].append({"carte": cid, "source": i})
        if not isinstance(carte.get("provenance"), dict):
            carte["provenance"] = {
                "genere_le": carte["verifie"], "sources_retrouvees": len(carte.get("source", [])),
                "sans_source": False,
            }
        prov = carte["provenance"]
        if prov.get("auteur") not in ("modele", "humain") or (prov.get("auteur") == "modele" and not prov.get("modele")):
            rapport["auteurs_manquants"].append(cid)
        if carte["statut"] == "valide" and not carte.get("verifie_par"):
            rapport["relecteurs_manquants"].append(cid)
        if carte["niveau"] > entree["niveau"]:
            rapport["niveaux_incompatibles"].append({"carte": cid, "niveau_carte": carte["niveau"],
                                                      "chapitre": cible, "niveau_chapitre": entree["niveau"]})
        if originale["domaine"] != carte["domaine"]:
            rapport["changements_domaine"].append({"carte": cid, "avant": originale["domaine"], "apres": carte["domaine"]})
        if cible not in chapitres:
            chapitres[cible] = nouveau_chapitre(entree, carte)
            chemins[cible] = "chapitres/" + cible.replace(".", "/") + ".json"
            nouveaux.add(cible)
        ch = chapitres[cible]
        ch.setdefault("cartes", []).append(carte)
        if cible in nouveaux:
            for src in carte.get("source", []):
                if src not in ch["sources"]:
                    ch["sources"].append(copy.deepcopy(src))
            ch["provenance"]["sources_retrouvees"] = len(ch["sources"])
            ch["provenance"]["sans_source"] = not ch["sources"]
    rapport["chapitres_a_ecrire"] = sorted(nouveaux)
    rapport["chapitres_candidats"] = len(chapitres)
    rapport["cartes_candidats"] = sum(len(ch.get("cartes", [])) for ch in chapitres.values())
    rapport["identifiants_conserves"] = Counter(c["id"] for ch in chapitres.values() for c in ch.get("cartes", [])) + Counter(c["id"] for c in non_assignees) == comptes
    for cid, ch in chapitres.items():
        rapport["erreurs_validation"].extend(valide_chapitre(ch, racine / chemins[cid], programme, set(), date.today()))
        # Une lecon absente ne doit pas cacher les erreurs des cartes du lot.
        for carte in ch.get("cartes", []):
            rapport["erreurs_validation"].extend(valide_carte(carte, ch, chemins[cid], set(), date.today()))
    rapport["erreurs_validation"] = list(dict.fromkeys(rapport["erreurs_validation"]))
    for cle in ("sans_assignation", "chapitres_absents", "doublons"):
        rapport["erreurs_validation"].extend(f"{cle} : {cid}" for cid in rapport[cle])
    if not rapport["identifiants_conserves"]:
        rapport["erreurs_validation"].append("identifiants perdus pendant la preparation")
    rapport["pret_pour_revue"] = not rapport["erreurs_validation"]
    controle_source(racine, rapport)
    return rapport, {chemins[cid]: ch for cid, ch in chapitres.items()}, non_assignees


def staging(racine: Path, cible: Path, rapport: dict, chapitres: dict, non_assignees: list) -> None:
    if cible == racine or cible.is_relative_to(racine) or racine.is_relative_to(cible):
        raise ValueError("le staging doit etre hors de la racine source")
    if cible.exists():
        raise ValueError("le staging doit etre un chemin neuf : aucun ecrasement")
    cible.mkdir(parents=True)
    rapport["staging"] = str(cible)
    if not controle_source(racine, rapport):
        ecrit_json(cible / "rapport-migration.json", rapport)
        return
    shutil.copy2(racine / "academie.json", cible / "academie.json")
    shutil.copytree(racine / "programme", cible / "programme")
    (cible / "banque").mkdir()
    if (racine / "banque/images").is_dir():
        shutil.copytree(racine / "banque/images", cible / "banque/images")
    for chemin, ch in chapitres.items():
        ecrit_json(cible / chemin, ch)
    if non_assignees:
        ecrit_json(cible / "cartes-non-assignees.json", non_assignees)
    env = dict(os.environ, ACADEMIE_RACINE=str(cible))
    env.pop("ERP_REPO", None)
    res = subprocess.run([sys.executable, str(APP / "valide_chapitres.py"), "--json"],
                         env=env, capture_output=True, text=True)
    rapport["validation_staging"] = {"code": res.returncode, "sortie": res.stdout, "erreur": res.stderr}
    if res.returncode:
        rapport["pret_pour_revue"] = False
    controle_source(racine, rapport)
    if rapport["pret_pour_revue"]:
        gen = subprocess.run([sys.executable, str(APP / "genere.py"), "--couches", "banque",
                              "--sortie", str(cible / "generation/banque.json")],
                             env=env, capture_output=True, text=True)
        rapport["generation_staging"] = {"code": gen.returncode, "sortie": gen.stdout, "erreur": gen.stderr}
        rapport["pret_pour_revue"] = gen.returncode == 0
    controle_source(racine, rapport)
    if rapport["pret_pour_revue"]:
        (cible / "generation").rename(cible / "site")
    ecrit_json(cible / "rapport-migration.json", rapport)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--racine", type=Path, default=RACINE)
    ap.add_argument("--staging", type=Path, help="racine candidate neuve, hors de la source")
    ap.add_argument("--json", action="store_true", help="rapport machine complet")
    args = ap.parse_args()
    try:
        racine = args.racine.resolve()
        rapport, chapitres, non_assignees = prepare(racine)
        if args.staging:
            staging(racine, args.staging.resolve(), rapport, chapitres, non_assignees)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"erreur": str(exc)}, ensure_ascii=False) if args.json else f"preparation refusee : {exc}")
        return 1
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        print(f"{rapport['cartes_v1']} cartes v1, {rapport['chapitres_candidats']} chapitres candidats, "
              f"{len(rapport['changements_domaine'])} changements de domaine")
        for cle in ("chapitres_a_ecrire", "auteurs_manquants", "relecteurs_manquants", "niveaux_incompatibles", "erreurs_validation"):
            print(f"{cle} : {len(rapport[cle])}")
        print("candidat vert pour revue" if rapport["pret_pour_revue"] else "candidat refuse par le contrat ; aucune promotion")
        if args.staging:
            print(f"rapport : {rapport['staging']}/rapport-migration.json")
    return 0 if rapport["pret_pour_revue"] else 1


if __name__ == "__main__":
    sys.exit(main())

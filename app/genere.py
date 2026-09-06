#!/usr/bin/env python3
"""Générateur de l'Académie — de la banque vers ce qui se joue.

Sortie principale : le JSON que le front React consomme, à la place des
tableaux écrits en dur dans les composants (FLASHCARDS_DATA et
consorts, constat du 28/08/2026 : contenu sans source ni date de
vérification, donc hors règle dure 3).

──────────────────────────────────────────────────────────────────────
LA CHAÎNE BANQUE → ÉCRAN (O1a, posée le 29/08/2026)
──────────────────────────────────────────────────────────────────────

Maillon par maillon, du fichier source jusqu'au pixel :

  1. `academie/banque/**/*.json`   la banque versionnée (contrat carte-v1)
  2. `valide_banque.py`            refuse tout ce qui sort du contrat
  3. CE FICHIER                    écrit `site/banque.json` et les seuls
       médias réellement référencés par les cartes servies.
  4. Un consommateur autorisé      récupère cet artefact versionné ou
       publié. ERP n'est plus une dépendance de construction.

Conséquence : un timer VPS peut régénérer la banque sans ouvrir ni monter ERP.

La charge sert aussi la CONFIG du moteur (blocs `fsrs`, `progression`,
`quiz`, `quotas`, `profil_defaut`) : tout client autorisé lit ses seuils
ici, jamais en dur — même règle que `progression.reglages()`.

Deux garde-fous portés ici, pas dans le front :
  1. **Sûr par défaut** : une carte `brouillon` n'est PAS servie, point.
     Il faut le demander explicitement (--avec-brouillons), et même
     alors son statut voyage jusqu'au front qui doit l'afficher.
     Corrigé le 28/08/2026 : le défaut servait le non-vérifié, en
     contradiction avec le contrat carte-v1 §3.3 — celui qui lance la
     commande sans y penser ne doit jamais publier du non-recoupé.
  2. Le filtrage par couche de partage est mécanique. Une distribution
     externe (--couches banque) ne peut pas laisser fuir une carte
     `interne` ou `perso`, quel que soit l'oubli d'un relecteur.

Usage :
    python3 app/genere.py                     # cartes `valide` seules
    python3 app/genere.py --avec-brouillons   # dev : + les brouillons
    python3 app/genere.py --couches banque    # distribution externe
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from valide_banque import (  # noqa: E402
    ACADEMIE, BANQUE, charge_banque, charge_config, noms_du_parc, valide_carte)
from datetime import date  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
SORTIE_SITE = RACINE / "site" / "banque.json"
CLIENT = RACINE / "client"
FICHIERS_CLIENT = ("index.html", "style.css", "app.js", "sw.js")
# Maillon 3c : les IMAGES des cartes à image (photo, relier, datation,
# plan). `image.fichier` est relatif à la racine de la banque ; on
# recopie le MÊME chemin relatif à côté du banque.json servi, pour que
# le front n'ait qu'une seule règle : racine() + 'donnees/academie/' +
# image.fichier. Ajouté le 30/08/2026 : sans ça, les quatre cartes à
# image de la banque étaient servies avec un `fichier` qui ne pointait
# nulle part, et l'écran retombait en rendu dégradé.

# Blocs de config recopiés dans la charge servie. Le front n'a pas accès
# à `academie.json` : sans eux, il devrait coder les seuils en dur, ce
# qui est exactement ce que `progression.reglages()` interdit côté
# Python. On ne sert QUE des réglages, jamais un chemin ni un secret.
BLOCS_CONFIG = ("domaines", "quotas", "fsrs", "progression", "quiz",
                # ACA-SEMAINE-1 : sans eux le client ne peut pas décider la
                # couleur du jour, le quota de neuf ni la branche du socle,
                # et la parité demandée par le cahier serait impossible.
                "semaine_type", "socle", "calendrier_metier")

# Ce qu'un nœud publie. Le client recalcule l'arbre avec exactement ces
# champs et pas un de plus (ACA-ARBRE-1) : le reste du programme (les
# notions, la compétence, les exercices, l'étude) est de la matière de
# fabrication, elle ne traverse pas.
CHAMPS_CHAPITRE = ("id", "titre", "domaine", "branche", "sous_branche",
                   "niveau", "prerequis", "ponts", "satellite", "statut")

# Champs servis au front. On n'expose pas `origine` (chemin interne du
# repo, sans intérêt pour le joueur) ni les champs de travail.
CHAMPS = ("id", "domaine", "branche", "niveau", "prerequis", "type",
          "question", "reponse", "choix", "explication", "vigilance",
          "image", "source", "verifie", "peremption", "statut")

# Ce qu'une carte v2 emporte en plus (CONTRAT-CARTE-V2.md §2). Trois
# familles : le rattachement (`chapitre`), le dossier de la carte
# (`provenance`, `verifie_par`, et les deux dérivés que le valideur
# calcule et que personne n'écrit à la main), et les charges des types
# que la v1 ne connaissait pas.
CHAMPS_V2 = CHAMPS + (
    "chapitre", "provenance", "verifie_par", "a_recouper", "note_confiance",
    "pas", "attendus", "document", "audio", "chrono", "confiance", "aide")


def carte_publique(carte: dict) -> dict:
    """La carte telle que le front la reçoit : sans les champs de travail."""
    return {c: carte[c] for c in CHAMPS if c in carte and carte[c] not in (None, [], "")}


def carte_publique_v2(carte: dict) -> dict:
    """Idem pour une carte v2 : le rattachement et le dossier voyagent.

    `a_recouper` et `note_confiance` sont posés par l'appelant depuis la
    dérivation du valideur (`decisions/0022`) : ils ne viennent jamais du
    fichier, le valideur refuse qu'on les y écrive.
    """
    return {c: carte[c] for c in CHAMPS_V2
            if c in carte and carte[c] not in (None, [], "")}


def charge_programme(racine: Path | None = None) -> dict:
    """Le programme du métier : `programme/<metier>.json`, sans le catalogue.

    Résolu depuis `ACADEMIE` (donc depuis `ACADEMIE_RACINE` quand il est
    posé), comme la banque : une racine jetable de test n'emprunte jamais
    le programme du dépôt. Rend `{}` s'il n'y en a pas : la banque reste
    servable sans arbre, exactement comme avant `ACA-ARBRE-1`.
    """
    dossier = (racine or ACADEMIE) / "programme"
    fichiers = sorted(f for f in dossier.glob("*.json") if f.name != "catalogue.json")
    if not fichiers:
        return {}
    return json.loads(fichiers[0].read_text(encoding="utf-8"))


def chapitre_public(chapitre: dict) -> dict:
    """Le nœud tel que le client le reçoit : la forme de l'arbre, rien d'autre."""
    return {c: chapitre[c] for c in CHAMPS_CHAPITRE
            if c in chapitre and chapitre[c] not in (None, [], "")}


def sert_la_carte_v2(carte: dict, chapitre: dict, couches: set[str],
                     avec_brouillons: bool) -> str | None:
    """Rend le motif d'écartement d'une carte v2, ou None si elle se joue.

    Trois filtres, dans cet ordre, et un seul est une nouveauté de la v2.

    1. La couche, mécanique comme en v1.
    2. Le statut de la carte, sûr par défaut comme en v1.
    3. **Le statut du chapitre.** Un chapitre `signale` ou `perime` est
       retiré : il emporte ses cartes, quel que soit leur propre statut,
       parce que c'est la leçon qui est en cause. Un chapitre
       `brouillon`, lui, ne se joue pas comme chapitre — sa leçon n'est
       pas écrite — mais ses cartes `valide` et relues sont servies.
       C'est la RÈGLE DE TRANSITION du cahier ACA-CONTRAT-2, datée du
       03/09/2026 : sans elle, migrer la banque priverait JB de ses
       cartes vérifiées jusqu'à la fin d'ACA-CONTENT-2. Elle se retire
       à ce moment-là, et ce commentaire avec.
    """
    if carte.get("partage") not in couches:
        return "couche"
    if carte.get("statut") in ("signale", "perime"):
        return "statut"
    if carte.get("statut") != "valide" and not avec_brouillons:
        return "statut"
    if chapitre.get("statut") in ("signale", "perime"):
        return "chapitre"
    if chapitre.get("statut") != "valide" and not avec_brouillons:
        # Règle de transition : la carte relue passe, l'autre non.
        if not (carte.get("statut") == "valide" and carte.get("verifie_par")):
            return "chapitre"
    return None


def charge_cartes_v2(couches: set[str], avec_brouillons: bool,
                     aujourdhui: date) -> tuple[list[dict], list[str], dict[str, int]]:
    """Lit `chapitres/`, juge, dérive, et rend les cartes v2 à servir.

    Le juge est `valide_chapitres.py`, le même que la porte du dépôt :
    `genere.py` ne rejuge rien à sa façon, il refuse de publier quand le
    valideur parle. Les dérivés (`a_recouper`, `note_confiance`) sont
    calculés ici parce qu'ils doivent atteindre l'écran ; ils ne sont
    jamais lus du fichier.
    """
    import valide_chapitres as v2  # noqa: PLC0415  (import tardif : ACADEMIE_RACINE)

    chapitres, erreurs = v2.charge_chapitres()
    if not chapitres:
        return [], erreurs, {"couche": 0, "statut": 0, "chapitre": 0}

    programme = v2.charge_programme()
    parc = v2.noms_du_parc()
    retenues: list[dict] = []
    ecartees = {"couche": 0, "statut": 0, "chapitre": 0}
    for ch, fichier in chapitres:
        if not isinstance(ch, dict):
            erreurs.append(f"{fichier.name} : un chapitre est un objet, pas un tableau")
            continue
        erreurs.extend(v2.valide_chapitre(ch, fichier, programme, parc, aujourdhui))
        for carte in ch.get("cartes") or []:
            if not isinstance(carte, dict):
                continue
            motif = sert_la_carte_v2(carte, ch, couches, avec_brouillons)
            if motif:
                ecartees[motif] += 1
                continue
            a_recouper, note = v2.derive(carte, carte.get("source") or [], aujourdhui)
            retenues.append(carte_publique_v2(
                {**carte, "a_recouper": a_recouper, "note_confiance": note}))
    return retenues, erreurs, ecartees


def charge_etudes(retenues, aujourdhui):
    """Expose uniquement les études complètes, relues et encore servables."""
    import valide_chapitres as v2
    chapitres, _ = v2.charge_chapitres()
    ids = {c["id"] for c in retenues}
    lecons = {}
    for ch, fichier in chapitres:
        revue = ch.get("verifie_par")
        if ch.get("statut") != "valide" or not isinstance(revue, dict):
            continue
        if v2.valide_chapitre(ch, fichier, v2.charge_programme(), set(), aujourdhui):
            continue
        if ch.get("peremption") and ch["peremption"] < aujourdhui.isoformat():
            continue
        cartes = ch.get("cartes") or []
        if not cartes or any(c["id"] not in ids for c in cartes):
            continue
        if any(c.get("peremption") and c["peremption"] < aujourdhui.isoformat() for c in cartes):
            continue
        lecons[ch["id"]] = {k: ch[k] for k in ("id", "titre", "domaine", "branche", "niveau", "objectifs", "amorce", "lecon", "synthese", "sources", "provenance", "verifie_par", "verifie", "version", "statut")}
        lecons[ch["id"]]["peremption"] = ch.get("peremption")
        lecons[ch["id"]]["cartes"] = [c["id"] for c in cartes]
    fichier = ACADEMIE / "contenu" / "parcours.json"
    parcours = json.loads(fichier.read_text(encoding="utf-8")).get("parcours", []) if fichier.is_file() else []
    return {"version": 1, "lecons": lecons, "parcours": [p for p in parcours if all(c in lecons for c in p["chapitres"])]}


def charge_metiers(retenues):
    """Un même moteur, des banques distinctes par métier, un journal privé commun."""
    import valide_chapitres as v2
    chapitres, _ = v2.charge_chapitres()
    satellites = {ch['id']: ch.get('rattachement_propose') for ch, _ in chapitres
                  if ch.get('satellite')}
    metiers = {}
    for fichier in sorted((ACADEMIE / "programme").glob("*.json")):
        p = json.loads(fichier.read_text(encoding="utf-8"))
        if not p.get("chapitres") or not p.get("domaines"):
            continue
        ids = {c["id"] for c in p["chapitres"]}
        domaines = p["domaines"]
        metiers[fichier.stem] = {
            "domaines": domaines, "chapitres": [chapitre_public(c) for c in p["chapitres"]],
            "branches": p.get("branches", {}), "niveaux": p.get("niveaux", {}),
            "cartes": [c["id"] for c in retenues if c.get("chapitre") in ids
                       or satellites.get(c.get("chapitre")) in ids
                       or (not c.get("chapitre") and c["domaine"] in domaines)],
        }
    return metiers


def publie_images(retenues: list[dict], dossier_sortie: Path) -> tuple[list[str], list[str]]:
    """Copie à côté du banque.json servi les images des cartes servies.

    On ne recopie PAS le dossier `images/` en bloc : seulement ce qui
    est référencé par une carte réellement servie. Deux conséquences
    voulues — aucune image orpheline ne part en distribution, et une
    image manquante se voit ici plutôt qu'à 7 h du matin sur un carré
    vide. Rend (chemins publiés, erreurs).
    """
    publiees: list[str] = []
    erreurs: list[str] = []
    racine_banque = BANQUE.resolve()
    for carte in retenues:
        rel = (carte.get("image") or {}).get("fichier")
        if not rel:
            continue
        source = (BANQUE / rel).resolve()
        try:
            source.relative_to(racine_banque)
        except ValueError:
            erreurs.append(f"{carte['id']} : image hors de la banque ({rel})")
            continue
        if not source.is_file():
            erreurs.append(f"{carte['id']} : image absente ({rel})")
            continue
        cible = dossier_sortie / rel
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, cible)
        publiees.append(rel)
    return publiees, erreurs


def publie_client(dossier_sortie: Path) -> list[str]:
    """Publie le client autonome à côté de la banque.

    Le client appartient à Académie et ne dépend d'aucun build ERP. Les fichiers
    sont volontairement statiques : le timer VPS peut publier l'application avec
    Python seul, sans npm ni chaîne de compilation implicite.
    """
    publies: list[str] = []
    if not CLIENT.is_dir():
        # 04/09 : l'archipel est archivé (archive/client-archipel-2026-09-04) ;
        # la publication du client v2 (web/dist) arrive avec ACA-FRONT-2.
        return publies
    for nom in FICHIERS_CLIENT:
        source = CLIENT / nom
        if not source.is_file():
            raise FileNotFoundError(f"client autonome incomplet : {source}")
        cible = dossier_sortie / nom
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, cible)
        publies.append(nom)
    return publies


def main() -> int:
    ap = argparse.ArgumentParser(description="Génère la banque jouable.")
    ap.add_argument("--avec-brouillons", action="store_true",
                    help="servir aussi les cartes non revérifiées (développement)")
    ap.add_argument("--production", action="store_true",
                    help="sans effet : c'est le défaut (gardé pour compatibilité)")
    ap.add_argument("--couches", default="banque,interne",
                    help="couches de partage servies (défaut : banque,interne)")
    ap.add_argument("--sortie", type=Path, default=SORTIE_SITE)
    ap.add_argument("--sans-miroir-site", action="store_true",
                    help="option historique sans effet, conservée pour compatibilité")
    args = ap.parse_args()

    couches = {c.strip() for c in args.couches.split(",") if c.strip()}
    config = charge_config()
    cartes, erreurs = charge_banque()

    # On ne génère JAMAIS depuis une banque invalide : servir une carte
    # hors contrat, c'est exactement ce que le valideur existe pour empêcher.
    parc = noms_du_parc()
    aujourdhui = date.today()
    for carte, fichier in cartes:
        erreurs.extend(valide_carte(carte, fichier, config, parc, aujourdhui))
    if erreurs:
        print(f"banque invalide ({len(erreurs)} erreur(s)), rien n'est généré.")
        print("→ python3 app/valide_banque.py")
        return 1

    retenues = []
    ecartees = {"couche": 0, "statut": 0, "chapitre": 0}
    for carte, _ in cartes:
        if carte["partage"] not in couches:
            ecartees["couche"] += 1
            continue
        if carte["statut"] in ("signale", "perime"):
            ecartees["statut"] += 1
            continue
        if carte["statut"] != "valide" and not args.avec_brouillons:
            ecartees["statut"] += 1
            continue
        retenues.append(carte_publique(carte))

    # ACA-CONTRAT-2 étape 3 : la seconde disposition. `chapitres/` et
    # `banque/` coexistent le temps de la migration ; les deux passent
    # par leur valideur et se versent dans le même lot.
    nb_v1 = len(retenues)
    cartes_v2, erreurs_v2, ecartees_v2 = charge_cartes_v2(
        couches, args.avec_brouillons, aujourdhui)
    for motif, combien in ecartees_v2.items():
        ecartees[motif] += combien
    if erreurs_v2:
        print(f"chapitres v2 invalides ({len(erreurs_v2)} erreur(s)), rien n'est généré.")
        for e in erreurs_v2[:10]:
            print(f"  - {e}")
        print("→ python3 app/valide_chapitres.py")
        return 1
    retenues.extend(cartes_v2)

    # Un identifiant des deux côtés, c'est un état de joueur rejoué sur
    # deux cartes différentes : la migration doit déplacer, jamais copier.
    vus: dict[str, int] = {}
    doublons = []
    for c in retenues:
        vus[c["id"]] = vus.get(c["id"], 0) + 1
        if vus[c["id"]] == 2:
            doublons.append(c["id"])
    if doublons:
        print(f"identifiant(s) servi(s) deux fois ({len(doublons)}), rien n'est généré :")
        for d in doublons[:10]:
            print(f"  - {d} (présent dans banque/ ET dans chapitres/)")
        return 1

    charge = {
        "_": ("Généré par app/genere.py — ne pas éditer à la main. "
              "Toute carte porte sa source et sa date de vérification ; "
              "une carte de statut `brouillon` n'a pas été revérifiée à la "
              "source et DOIT être signalée comme telle à l'écran."),
        "genere_le": aujourdhui.isoformat(),
        "profil_defaut": config.get("profil_defaut", "jb"),
        "domaines": config["domaines"],
        "quotas": config["quotas"],
        "cartes": retenues,
    }
    # `domaines` et `quotas` sont déjà posés au-dessus (ordre de lecture) ;
    # la boucle ajoute le reste sans les réécrire différemment.
    for bloc in BLOCS_CONFIG:
        if bloc in config:
            charge[bloc] = config[bloc]

    # L'arbre : les nœuds, leurs prérequis, les branches qui les portent
    # (ACA-ARBRE-1). Le client recalcule les états avec ça et le journal,
    # sans jamais rien demander au serveur.
    programme = charge_programme()
    if programme:
        charge["chapitres"] = [chapitre_public(c) for c in programme.get("chapitres", [])]
        charge["branches"] = programme.get("branches", {})
        charge["niveaux"] = programme.get("niveaux", {})
    charge["etudes"] = charge_etudes(retenues, aujourdhui)
    charge["metiers"] = charge_metiers(retenues)
    # Le contrat de la charge servie. Il n'est pas un vœu : il dit au
    # client ce qu'il peut supposer de CHAQUE carte du lot. Tant qu'une
    # carte v1 est servie — sans `chapitre`, sans `provenance` —
    # annoncer `carte-v2` serait un mensonge que le client paierait à
    # l'écran. Le champ bascule donc tout seul le jour où `banque/` ne
    # fournit plus rien : la fin de la migration flippe le contrat par
    # construction, sans drapeau à ne pas oublier. Le client lit une
    # charge sans `contrat` comme une `carte-v1` (CONTRAT-CARTE-V2 §5.4).
    if cartes_v2 and nb_v1 == 0:
        charge["contrat"] = "carte-v2"

    # Les poids FSRS servis au client, pour que sa parité ne dépende pas
    # d'une constante recopiée à la main de l'autre côté.
    charge.setdefault("fsrs", {})
    if "poids" not in charge["fsrs"]:
        from planificateur import PARAMS_DEFAUT  # noqa: PLC0415
        charge["fsrs"] = {**charge["fsrs"], "poids": list(PARAMS_DEFAUT)}

    sorties = [args.sortie]

    # Les images d'abord : une carte servie dont l'image manque est une
    # carte cassée à l'écran, donc rien ne s'écrit.
    images, manquantes = publie_images(retenues, args.sortie.parent)
    if manquantes:
        print(f"image(s) introuvable(s) ({len(manquantes)}), rien n'est généré :")
        for m in manquantes:
            print(f"  - {m}")
        return 1

    try:
        client = publie_client(args.sortie.parent)
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    texte = json.dumps(charge, ensure_ascii=False, indent=2) + "\n"
    for cible in sorties:
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(texte, encoding="utf-8")

    brouillons = sum(1 for c in retenues if c.get("statut") == "brouillon")
    ou = []
    for cible in sorties:
        try:
            ou.append(str(cible.resolve().relative_to(RACINE)))
        except ValueError:  # sortie hors du repo (test, export ponctuel)
            ou.append(str(cible))
    print(f"{len(retenues)} carte(s) servie(s) → {' + '.join(ou)}")
    print(f"  couches : {', '.join(sorted(couches))}")
    if cartes_v2:
        print(f"  dispositions : {nb_v1} carte(s) v1 (banque/), "
              f"{len(cartes_v2)} carte(s) v2 (chapitres/) ; "
              f"contrat servi : {charge.get('contrat', 'carte-v1 (champ absent)')}")
    if images:
        print(f"  {len(images)} image(s) publiée(s) → "
              f"{args.sortie.parent}/ : {', '.join(sorted(set(images)))}")
    print(f"  client autonome publié : {', '.join(client) if client else 'aucun (archipel archivé, client v2 à venir)'}")
    if brouillons:
        print(f"  dont {brouillons} en `brouillon` : à revérifier à la source "
              f"avant de compter dessus")
    if any(ecartees.values()):
        print(f"  écartées : {ecartees['couche']} hors couche, "
              f"{ecartees['statut']} par statut, "
              f"{ecartees['chapitre']} par statut de chapitre")
    return 0


if __name__ == "__main__":
    sys.exit(main())

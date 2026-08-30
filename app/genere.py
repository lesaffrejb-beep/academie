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
    BANQUE, charge_banque, charge_config, noms_du_parc, valide_carte)
from datetime import date  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
SORTIE_SITE = RACINE / "site" / "banque.json"
# Maillon 3c : les IMAGES des cartes à image (photo, relier, datation,
# plan). `image.fichier` est relatif à la racine de la banque ; on
# recopie le MÊME chemin relatif à côté du banque.json servi, pour que
# le front n'ait qu'une seule règle : racine() + 'donnees/academie/' +
# image.fichier. Ajouté le 30/08/2026 : sans ça, les quatre cartes à
# image de la banque étaient servies avec un `fichier` qui ne pointait
# nulle part, et l'écran retombait en rendu dégradé.
SORTIE_MEDIAS = SORTIE_SITE.parent

# Blocs de config recopiés dans la charge servie. Le front n'a pas accès
# à `academie.json` : sans eux, il devrait coder les seuils en dur, ce
# qui est exactement ce que `progression.reglages()` interdit côté
# Python. On ne sert QUE des réglages, jamais un chemin ni un secret.
BLOCS_CONFIG = ("domaines", "quotas", "fsrs", "progression", "quiz")

# Champs servis au front. On n'expose pas `origine` (chemin interne du
# repo, sans intérêt pour le joueur) ni les champs de travail.
CHAMPS = ("id", "domaine", "branche", "niveau", "prerequis", "type",
          "question", "reponse", "choix", "explication", "vigilance",
          "image", "source", "verifie", "peremption", "statut")


def carte_publique(carte: dict) -> dict:
    """La carte telle que le front la reçoit : sans les champs de travail."""
    return {c: carte[c] for c in CHAMPS if c in carte and carte[c] not in (None, [], "")}


def publie_images(retenues: list[dict]) -> tuple[list[str], list[str]]:
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
        cible = SORTIE_MEDIAS / rel
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, cible)
        publiees.append(rel)
    return publiees, erreurs


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
    ecartees = {"couche": 0, "statut": 0}
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

    sorties = [args.sortie]

    # Les images d'abord : une carte servie dont l'image manque est une
    # carte cassée à l'écran, donc rien ne s'écrit.
    images: list[str] = []
    if args.sortie.resolve() == SORTIE_SITE.resolve():
        images, manquantes = publie_images(retenues)
        if manquantes:
            print(f"image(s) introuvable(s) ({len(manquantes)}), rien n'est généré :")
            for m in manquantes:
                print(f"  - {m}")
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
    if images:
        print(f"  {len(images)} image(s) publiée(s) → "
              f"{SORTIE_MEDIAS.relative_to(RACINE)}/ : {', '.join(sorted(set(images)))}")
    if brouillons:
        print(f"  dont {brouillons} en `brouillon` : à revérifier à la source "
              f"avant de compter dessus")
    if ecartees["couche"] or ecartees["statut"]:
        print(f"  écartées : {ecartees['couche']} hors couche, "
              f"{ecartees['statut']} par statut")
    return 0


if __name__ == "__main__":
    sys.exit(main())

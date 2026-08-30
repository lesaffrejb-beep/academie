#!/usr/bin/env python3
"""Valideur de la banque de cartes — l'application mécanique du contrat
carte-v1 (academie/CONTRAT-CARTE-V1.md).

Écrit AVANT la première carte (leçon du contrat batiment-v1, qui a
dérivé le 26/08/2026 faute de valideur). Quand ce fichier et le
contrat divergent, c'est ce fichier qui fait foi.

Ce qu'il refuse, sans dérogation possible :
  - une carte sans source ou sans date de vérification (règle dure 3) ;
  - un fait copro nommé dans une carte partagée (anti-pollution) ;
  - un QCM sans distracteurs expliqués, une image sans licence ;
  - un id dupliqué ou un prérequis qui pointe dans le vide.

Usage :
    python3 app/valide_banque.py            # toute la banque
    python3 app/valide_banque.py --json     # sortie machine
    python3 app/valide_banque.py --statut valide

Sortie : 0 si tout passe, 1 s'il reste une erreur. Stdlib seule.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
# ACADEMIE_RACINE permet de faire pointer le valideur sur une banque
# jetable : c'est ce qui rend la chaîne testable (tests_chaine.py) sans
# jamais écrire dans la vraie banque. Non défini = le dépôt.
ACADEMIE = Path(os.environ.get("ACADEMIE_RACINE") or RACINE)
BANQUE = ACADEMIE / "banque"
CONFIG = ACADEMIE / "academie.json"
ERP_RACINE = Path(os.environ["ERP_REPO"]) if os.environ.get("ERP_REPO") else None
PORTEFEUILLE = (ERP_RACINE / "outputs" / "PORTEFEUILLE") if ERP_RACINE else RACINE / ".no-erp-data"
IMMEUBLES = (ERP_RACINE / "outputs" / "IMMEUBLES") if ERP_RACINE else RACINE / ".no-erp-data"

TYPES = {"flash", "qcm", "photo", "relier", "datation", "libre", "role", "plan"}
TYPES_IMAGE = {"photo", "relier", "datation", "plan"}
STATUTS = {"brouillon", "valide", "signale", "perime"}
PARTAGES = {"banque", "interne", "perso"}
# Couches soumises au scan anti-fuite. `perso` y échappe par construction
# (c'est la couche des pièces réelles) ; `interne` non : même entre
# collègues, une carte pédagogique n'a pas besoin d'un nom de copro réel.
PARTAGES_SCANNES = {"banque", "interne"}
OBLIGATOIRES = ("id", "domaine", "branche", "type", "question", "reponse",
                "source", "verifie", "statut", "partage")

RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ID = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_OFF = re.compile(r"\bOFF-[A-Z0-9-]+")
RE_IMMAT = re.compile(r"\bAA\d{7}\b")          # immatriculation RNC
RE_ICS = re.compile(r"\bFR\d{2}ZZZ[0-9A-Z]{6}\b")


def _sans_accents(texte: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texte)
                   if unicodedata.category(c) != "Mn")


def charge_config() -> dict:
    if not CONFIG.is_file():
        sys.exit(f"config absente : {CONFIG}")
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def noms_du_parc() -> set[str]:
    """Les identités réelles à ne jamais laisser entrer en banque partagée.

    Si `ERP_REPO` est explicitement fourni sur une machine autorisée, on
    scanne contre les identités du coffre plutôt que contre une liste de mots
    devinée. Sans cet accès, les motifs structurels restent bloquants. Les noms courts (< 5 caractères) sont écartés :
    trop de faux positifs sur des mots communs.
    """
    noms: set[str] = set()
    if IMMEUBLES.is_dir():
        for dossier in IMMEUBLES.iterdir():
            if not dossier.is_dir() or not dossier.name.startswith("OFF-"):
                continue
            brut = dossier.name[4:].replace("-", " ").strip()
            if len(brut) >= 5:
                noms.add(brut.lower())
    radar = PORTEFEUILLE / "RADAR-MANDATS" / "latest.json"
    if radar.is_file():
        try:
            data = json.loads(radar.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            data = {}
        for ligne in (data.get("top") or []):
            for champ in ("nom", "syndic", "immat"):
                val = str(ligne.get(champ) or "").strip()
                if len(val) >= 5:
                    noms.add(val.lower())
    return noms


def texte_carte(carte: dict) -> str:
    """Tout le texte lisible d'une carte, pour le scan anti-fuite."""
    morceaux = [str(carte.get(c) or "") for c in
                ("question", "reponse", "explication", "vigilance", "origine")]
    for choix in (carte.get("choix") or []):
        morceaux.append(str(choix.get("texte") or ""))
        morceaux.append(str(choix.get("pourquoi_faux") or ""))
    for src in (carte.get("source") or []):
        morceaux.append(str(src.get("texte") or ""))
    return "\n".join(morceaux)


def valide_carte(carte: dict, fichier: Path, config: dict,
                 parc: set[str], aujourdhui: date) -> list[str]:
    """Retourne la liste des erreurs d'une carte (vide = conforme)."""
    err: list[str] = []
    cid = carte.get("id") or "<sans id>"
    ref = f"{fichier.name}:{cid}"

    for champ in OBLIGATOIRES:
        valeur = carte.get(champ)
        if valeur is None or (isinstance(valeur, (str, list)) and not valeur):
            err.append(f"{ref} : champ obligatoire manquant ou vide `{champ}`")
    if err:
        return err  # inutile d'aller plus loin, la carte est incomplète

    if not RE_ID.match(str(carte["id"])):
        err.append(f"{ref} : id hors format kebab-case")
    if carte["domaine"] not in config["domaines"]:
        err.append(f"{ref} : domaine `{carte['domaine']}` absent d'academie.json")
    if carte["type"] not in TYPES:
        err.append(f"{ref} : type `{carte['type']}` inconnu")
    if carte["statut"] not in STATUTS:
        err.append(f"{ref} : statut `{carte['statut']}` inconnu")
    if carte["partage"] not in PARTAGES:
        err.append(f"{ref} : partage `{carte['partage']}` inconnu")

    # --- règle dure 3 : source + date de vérification ------------------
    sources = carte.get("source") or []
    if not isinstance(sources, list) or not sources:
        err.append(f"{ref} : aucune source (règle dure 3)")
    else:
        for i, src in enumerate(sources):
            if not isinstance(src, dict) or not str(src.get("texte") or "").strip():
                err.append(f"{ref} : source[{i}] sans `texte`")
    if not RE_DATE.match(str(carte.get("verifie") or "")):
        err.append(f"{ref} : `verifie` absent ou hors format AAAA-MM-JJ")

    # --- péremption : un chiffre qui bouge porte sa date de mort -------
    per = carte.get("peremption")
    if per not in (None, ""):
        if not RE_DATE.match(str(per)):
            err.append(f"{ref} : `peremption` hors format AAAA-MM-JJ")
        elif date.fromisoformat(str(per)) < aujourdhui and carte["statut"] == "valide":
            err.append(f"{ref} : périmée le {per} mais toujours `valide` "
                       f"(passer en `perime` ou revérifier)")

    # --- QCM : distracteurs expliqués ---------------------------------
    if carte["type"] == "qcm":
        choix = carte.get("choix") or []
        if len(choix) < 3:
            err.append(f"{ref} : QCM à moins de 3 choix")
        justes = [c for c in choix if c.get("correct")]
        if len(justes) != 1:
            err.append(f"{ref} : QCM avec {len(justes)} bonne(s) réponse(s), "
                       f"il en faut exactement une")
        for i, c in enumerate(choix):
            if not str(c.get("texte") or "").strip():
                err.append(f"{ref} : choix[{i}] sans texte")
            if not c.get("correct") and not str(c.get("pourquoi_faux") or "").strip():
                err.append(f"{ref} : choix[{i}] faux sans `pourquoi_faux` "
                           f"(un distracteur non expliqué n'apprend rien)")
    elif carte.get("choix"):
        err.append(f"{ref} : `choix` présent sur un type `{carte['type']}`")

    # --- image : jamais sans licence ----------------------------------
    if carte["type"] in TYPES_IMAGE:
        img = carte.get("image")
        if not isinstance(img, dict):
            err.append(f"{ref} : type `{carte['type']}` sans `image`")
        else:
            for champ in ("fichier", "licence", "credit"):
                if not str(img.get(champ) or "").strip():
                    err.append(f"{ref} : image sans `{champ}` "
                               f"(droit des sources, BLUEPRINT §7)")
    elif carte.get("image"):
        err.append(f"{ref} : `image` présente sur un type `{carte['type']}`")

    niveau = carte.get("niveau", 1)
    if not isinstance(niveau, int) or not 1 <= niveau <= 3:
        err.append(f"{ref} : `niveau` doit être un entier de 1 à 3")

    # --- anti-pollution : aucun fait copro nommé en couche partagée ----
    if carte["partage"] in PARTAGES_SCANNES:
        texte = texte_carte(carte)
        fuites = set(RE_OFF.findall(texte))
        fuites |= set(RE_IMMAT.findall(texte))
        fuites |= set(RE_ICS.findall(texte))
        plat = _sans_accents(texte).lower()
        for nom in parc:
            if _sans_accents(nom) in plat:
                fuites.add(nom)
        if fuites:
            err.append(f"{ref} : donnée nominative en couche partagée : "
                       + ", ".join(sorted(fuites)[:4]))
    return err


def charge_banque() -> tuple[list[tuple[dict, Path]], list[str]]:
    cartes: list[tuple[dict, Path]] = []
    err: list[str] = []
    if not BANQUE.is_dir():
        return cartes, [f"banque absente : {BANQUE}"]
    for fichier in sorted(BANQUE.rglob("*.json")):
        try:
            data = json.loads(fichier.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            err.append(f"{fichier.name} : JSON illisible ({exc})")
            continue
        if not isinstance(data, list):
            err.append(f"{fichier.name} : le fichier doit contenir un tableau de cartes")
            continue
        for carte in data:
            if isinstance(carte, dict):
                cartes.append((carte, fichier))
            else:
                err.append(f"{fichier.name} : entrée qui n'est pas un objet")
    return cartes, err


def main() -> int:
    ap = argparse.ArgumentParser(description="Valide la banque de cartes carte-v1.")
    ap.add_argument("--json", action="store_true", help="sortie machine")
    ap.add_argument("--statut", help="ne valider que ce statut")
    args = ap.parse_args()

    config = charge_config()
    parc = noms_du_parc()
    aujourdhui = date.today()
    cartes, erreurs = charge_banque()

    if args.statut:
        cartes = [(c, f) for c, f in cartes if c.get("statut") == args.statut]

    vus: dict[str, str] = {}
    for carte, fichier in cartes:
        cid = str(carte.get("id") or "")
        if cid and cid in vus:
            erreurs.append(f"{fichier.name}:{cid} : id déjà utilisé dans {vus[cid]}")
        elif cid:
            vus[cid] = fichier.name
        erreurs.extend(valide_carte(carte, fichier, config, parc, aujourdhui))

    connus = set(vus)
    for carte, fichier in cartes:
        for pre in (carte.get("prerequis") or []):
            if pre not in connus:
                erreurs.append(f"{fichier.name}:{carte.get('id')} : "
                               f"prérequis inconnu `{pre}`")

    par_statut: dict[str, int] = {}
    for carte, _ in cartes:
        st = str(carte.get("statut") or "?")
        par_statut[st] = par_statut.get(st, 0) + 1

    if args.json:
        print(json.dumps({"cartes": len(cartes), "erreurs": erreurs,
                          "par_statut": par_statut},
                         ensure_ascii=False, indent=2))
        return 1 if erreurs else 0

    print(f"banque : {len(cartes)} carte(s) — " +
          ", ".join(f"{n} {s}" for s, n in sorted(par_statut.items())))
    if erreurs:
        print(f"\n{len(erreurs)} erreur(s) :")
        for e in erreurs:
            print(f"  ✗ {e}")
        print("\nRefusé. Rien de tout ceci n'entre en jeu.")
        return 1
    print("VERT — toute la banque respecte le contrat carte-v1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

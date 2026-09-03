#!/usr/bin/env python3
"""Valideur des chapitres v2 (CONTRAT-CARTE-V2.md, contrats/chapitre-v1 et
carte-v2) : l'application mécanique du contrat proposé le 02/09/2026,
écrite le 03/09/2026 avec les premiers chapitres.

Périmètre : `chapitres/<domaine>/<branche>/<slug>.json`, un objet par
fichier. La banque v1 (`banque/`, tableaux de cartes) reste jugée par
`valide_banque.py` ; les deux dispositions coexistent jusqu'au chantier
ACA-CONTRAT-2 qui fusionne.

Ce qu'il refuse, sans dérogation :
  - un chapitre absent du programme, ou dont le niveau, le domaine ou la
    branche ne sont pas ceux du programme ;
  - un prérequis inconnu ou de niveau supérieur ;
  - un chapitre ou une carte sans provenance (decisions/0021) ;
  - une carte sans source, sauf `sans_source` avoué, et alors sans aucun
    chiffre, date, durée ni montant (les numéros d'article et de texte
    sont exclus du motif) ;
  - une source sans nature ; un QCM sans distracteurs expliqués ; un cas
    sans pas ; un dessin, une feuille blanche ou une synthèse sans liste
    d'attendus ; une image sans licence ni alt ; un chrono hors des
    types qui l'admettent ;
  - un statut `valide` sans relecture (`verifie_par`) ;
  - un fait nominatif du parc dans une couche partagée (même scan que
    valide_banque) ;
  - une carte de nature juridique validée il y a plus de douze mois
    (decisions/0019) ;
  - un identifiant dupliqué.

Ce qu'il dérive, et n'accepte jamais écrit à la main :
  - `a_recouper` : aucune source de fiabilité A, ou sans source ;
  - `note_confiance` : A, B ou C (decisions/0022).

Usage :
    python3 app/valide_chapitres.py            # tous les chapitres
    python3 app/valide_chapitres.py --json     # dérivés, sortie machine
    python3 app/valide_chapitres.py --rapport  # comptes par note et statut

Sortie : 0 si tout passe, 1 s'il reste une erreur. Stdlib seule.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from valide_banque import RE_ICS, RE_IMMAT, RE_OFF, noms_du_parc  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
ACADEMIE = Path(os.environ.get("ACADEMIE_RACINE") or RACINE)
CHAPITRES = ACADEMIE / "chapitres"
PROGRAMMES = ACADEMIE / "programme"

TYPES = {"flash", "qcm", "photo", "relier", "datation", "plan", "cas", "libre",
         "role", "dessin", "feuille-blanche", "synthese", "lecture", "ecoute"}
TYPES_IMAGE = {"photo", "relier", "datation", "plan"}
TYPES_ATTENDUS = {"dessin", "feuille-blanche", "synthese"}
TYPES_CHRONO = {"qcm", "photo", "relier", "feuille-blanche"}
NATURES = {"texte-officiel", "jurisprudence", "institution", "norme", "doctrine",
           "presse-pro", "organisation-pro", "association", "editeur",
           "support-interne", "terrain"}
NATURES_JURIDIQUES = {"texte-officiel", "jurisprudence"}
FIABILITE_PAR_NATURE = {
    "texte-officiel": "A", "jurisprudence": "A", "institution": "A", "norme": "A",
    "doctrine": "B", "presse-pro": "B", "organisation-pro": "B", "association": "B",
    "editeur": "C", "support-interne": "C", "terrain": "C",
}
STATUTS = {"brouillon", "valide", "signale", "perime"}
PARTAGES = {"banque", "interne", "perso"}
PARTAGES_SCANNES = {"banque", "interne"}
CHAMPS_CHAPITRE = ("id", "titre", "domaine", "branche", "niveau", "prerequis",
                   "objectifs", "amorce", "lecon", "synthese", "sources",
                   "provenance", "statut", "partage", "verifie", "version")
CHAMPS_CARTE = ("id", "chapitre", "domaine", "branche", "type", "niveau",
                "question", "reponse", "source", "provenance", "verifie",
                "statut", "partage")
CHAMPS_DERIVES = ("a_recouper", "note_confiance")
PEREMPTION_JURIDIQUE_JOURS = 365
LECON_MIN, LECON_MAX = 1500, 5500

RE_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RE_ID_CARTE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_ID_CHAPITRE = re.compile(r"^[a-z0-9-]+\.[a-z0-9-]+\.[a-z0-9-]+$")
# Ce qui est exclu du motif « chiffre sans source » : numéros d'article,
# de loi, de décret, de code et d'alinéa, et les identifiants de texte.
RE_REFERENCES = re.compile(
    r"(?:art(?:icle|\.)?\s*L?\.?\s*\d[\d\-\.]*)|(?:al(?:inéa|\.)\s*\d+)"
    r"|(?:(?:loi|décret|ordonnance|arrêté|directive|règlement)\s+(?:n°\s*)?[\d\-\.\/]+)"
    r"|(?:\bn°\s*[\d\-\.\/]+)|(?:\b(?:CPC|CCH|COJ)\b)", re.I)
RE_CHIFFRE = re.compile(r"\d")


def charge_programme() -> dict[str, dict]:
    """Tous les chapitres de tous les programmes, indexés par identifiant."""
    index: dict[str, dict] = {}
    if not PROGRAMMES.is_dir():
        return index
    for f in sorted(PROGRAMMES.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            sys.exit(f"programme illisible : {f} ({exc})")
        for ch in data.get("chapitres", []):
            index[ch["id"]] = ch
    return index


def _vide(valeur) -> bool:
    return valeur is None or (isinstance(valeur, (str, list, dict)) and not valeur)


def texte_de(objet: dict, champs: tuple[str, ...]) -> str:
    morceaux = [str(objet.get(c) or "") for c in champs]
    for choix in (objet.get("choix") or []):
        morceaux += [str(choix.get("texte") or ""), str(choix.get("pourquoi_faux") or "")]
    for pas in (objet.get("pas") or []):
        morceaux += [str(pas.get("situation") or ""), str(pas.get("pourquoi") or "")]
        morceaux += [str(c) for c in (pas.get("choix") or [])]
    for src in (objet.get("source") or objet.get("sources") or []):
        morceaux.append(str(src.get("texte") or ""))
    return "\n".join(morceaux)


def scan_fuite(texte: str, parc: set[str], ref: str) -> list[str]:
    err = []
    for motif, nom in ((RE_OFF, "slug OFF-"), (RE_IMMAT, "immatriculation"),
                       (RE_ICS, "identifiant ICS")):
        if motif.search(texte):
            err.append(f"{ref} : {nom} dans une couche partagée (anti-fuite)")
    bas = texte.lower()
    for nom in parc:
        if nom in bas:
            err.append(f"{ref} : nom du parc « {nom} » dans une couche partagée")
    return err


def chiffres_hors_references(texte: str) -> bool:
    """Vrai s'il reste un chiffre une fois les références de textes retirées."""
    return bool(RE_CHIFFRE.search(RE_REFERENCES.sub(" ", texte)))


def valide_provenance(prov, ref: str) -> list[str]:
    err = []
    if not isinstance(prov, dict):
        return [f"{ref} : `provenance` manquante (decisions/0021)"]
    for champ in ("auteur", "genere_le", "sources_retrouvees", "sans_source"):
        if champ not in prov:
            err.append(f"{ref} : provenance sans `{champ}`")
    if prov.get("auteur") not in ("modele", "humain"):
        err.append(f"{ref} : provenance.auteur doit valoir modele ou humain")
    if prov.get("auteur") == "modele" and not prov.get("modele"):
        err.append(f"{ref} : provenance.modele manquant pour un auteur modèle")
    if not RE_DATE.match(str(prov.get("genere_le", ""))):
        err.append(f"{ref} : provenance.genere_le n'est pas une date AAAA-MM-JJ")
    if not isinstance(prov.get("sources_retrouvees"), int) or prov.get("sources_retrouvees", -1) < 0:
        err.append(f"{ref} : provenance.sources_retrouvees doit être un entier ≥ 0")
    if not isinstance(prov.get("sans_source"), bool):
        err.append(f"{ref} : provenance.sans_source doit être un booléen")
    return err


def valide_sources(sources, ref: str) -> list[str]:
    err = []
    if not isinstance(sources, list):
        return [f"{ref} : `source` doit être une liste"]
    for i, src in enumerate(sources):
        if not isinstance(src, dict) or _vide(src.get("texte")):
            err.append(f"{ref} : source {i + 1} sans `texte`")
            continue
        if src.get("nature") not in NATURES:
            err.append(f"{ref} : source {i + 1} sans `nature` admise (decisions/0004)")
        for champ in ("fiabilite",):
            if champ in src and src[champ] not in ("A", "B", "C"):
                err.append(f"{ref} : source {i + 1} fiabilité inconnue")
    return err


def derive(objet: dict, sources: list, aujourdhui: date) -> tuple[bool, str]:
    """`a_recouper` et `note_confiance` (decisions/0022), jamais écrits à la main."""
    prov = objet.get("provenance") or {}
    fiabilites = [s.get("fiabilite") or FIABILITE_PAR_NATURE.get(s.get("nature"), "C")
                  for s in sources if isinstance(s, dict)]
    solides = [f for f in fiabilites if f in ("A", "B")]
    a_recouper = prov.get("sans_source") is True or not any(f == "A" for f in fiabilites)
    relue = bool(objet.get("verifie_par"))
    fraiche = False
    try:
        fraiche = (aujourdhui - date.fromisoformat(str(objet.get("verifie")))).days <= PEREMPTION_JURIDIQUE_JOURS
    except ValueError:
        pass
    if len(solides) >= 2 and relue and fraiche:
        note = "A"
    elif len(solides) >= 1 and relue:
        note = "B"
    else:
        note = "C"
    return a_recouper, note


def valide_carte(carte: dict, chapitre: dict, ref_ch: str, parc: set[str],
                 aujourdhui: date) -> list[str]:
    err: list[str] = []
    cid = carte.get("id") or "<sans id>"
    ref = f"{ref_ch}:{cid}"
    for champ in CHAMPS_CARTE:
        if _vide(carte.get(champ)) and champ != "source":
            err.append(f"{ref} : champ obligatoire manquant ou vide `{champ}`")
    for champ in CHAMPS_DERIVES:
        if champ in carte:
            err.append(f"{ref} : `{champ}` est dérivé par le valideur, jamais écrit à la main")
    if err:
        return err
    if not RE_ID_CARTE.match(str(carte["id"])):
        err.append(f"{ref} : id non kebab-case")
    if carte["chapitre"] != chapitre["id"]:
        err.append(f"{ref} : `chapitre` ({carte['chapitre']}) n'est pas celui du fichier")
    for champ in ("domaine", "branche"):
        if carte[champ] != chapitre[champ]:
            err.append(f"{ref} : `{champ}` diffère du chapitre")
    if carte["type"] not in TYPES:
        err.append(f"{ref} : type inconnu `{carte['type']}`")
    niv = carte.get("niveau")
    if not isinstance(niv, int) or not 1 <= niv <= 5:
        err.append(f"{ref} : niveau hors de 1-5")
    elif niv > chapitre.get("niveau", 5):
        err.append(f"{ref} : niveau {niv} au-dessus de celui du chapitre ({chapitre['niveau']})")
    if carte["statut"] not in STATUTS:
        err.append(f"{ref} : statut inconnu")
    if carte["partage"] not in PARTAGES:
        err.append(f"{ref} : partage inconnu")
    if not RE_DATE.match(str(carte["verifie"])):
        err.append(f"{ref} : `verifie` n'est pas une date AAAA-MM-JJ")
    if carte["statut"] == "valide" and _vide(carte.get("verifie_par")):
        err.append(f"{ref} : `valide` sans `verifie_par` (double passe obligatoire)")

    err += valide_provenance(carte.get("provenance"), ref)
    prov = carte.get("provenance") if isinstance(carte.get("provenance"), dict) else {}
    sources = carte.get("source") if isinstance(carte.get("source"), list) else []
    err += valide_sources(sources, ref)
    if not sources and prov.get("sans_source") is not True:
        err.append(f"{ref} : aucune source et `sans_source` n'est pas avoué")
    if prov.get("sans_source") is True:
        if chiffres_hors_references(f"{carte['question']}\n{carte['reponse']}\n{carte.get('explication') or ''}"):
            err.append(f"{ref} : carte sans source qui porte un chiffre, une date, "
                       f"une durée ou un montant (decisions/0021)")
    # péremption des cartes juridiques (decisions/0019)
    if carte["statut"] == "valide" and any(s.get("nature") in NATURES_JURIDIQUES for s in sources):
        try:
            if (aujourdhui - date.fromisoformat(str(carte["verifie"]))).days > PEREMPTION_JURIDIQUE_JOURS:
                err.append(f"{ref} : carte juridique validée il y a plus de douze mois, à revérifier")
        except ValueError:
            pass
    per = carte.get("peremption")
    if per is not None:
        if not RE_DATE.match(str(per)):
            err.append(f"{ref} : `peremption` n'est pas une date")
        elif date.fromisoformat(str(per)) < aujourdhui and carte["statut"] == "valide":
            err.append(f"{ref} : carte périmée encore `valide`")

    t = carte["type"]
    if t == "qcm":
        choix = carte.get("choix") or []
        if len(choix) < 3:
            err.append(f"{ref} : QCM avec moins de trois choix")
        justes = [c for c in choix if c.get("correct") is True]
        if len(justes) != 1:
            err.append(f"{ref} : QCM doit avoir exactement une bonne réponse")
        for c in choix:
            if not c.get("correct") and _vide(c.get("pourquoi_faux")):
                err.append(f"{ref} : distracteur sans `pourquoi_faux`")
    if t == "cas":
        pas = carte.get("pas") or []
        if not 3 <= len(pas) <= 5:
            err.append(f"{ref} : un cas compte 3 à 5 pas")
        for i, p in enumerate(pas):
            for champ in ("situation", "choix", "correct", "pourquoi"):
                if champ not in p or _vide(p.get(champ)) and champ != "correct":
                    err.append(f"{ref} : pas {i + 1} sans `{champ}`")
            if isinstance(p.get("choix"), list) and isinstance(p.get("correct"), int):
                if not 0 <= p["correct"] < len(p["choix"]):
                    err.append(f"{ref} : pas {i + 1} `correct` hors des choix")
    if t in TYPES_ATTENDUS:
        att = carte.get("attendus") or []
        if not 3 <= len(att) <= 10:
            err.append(f"{ref} : `{t}` exige 3 à 10 attendus")
    if t == "lecture" and not isinstance(carte.get("document"), dict):
        err.append(f"{ref} : lecture sans `document`")
    if t == "ecoute" and not isinstance(carte.get("audio"), dict):
        err.append(f"{ref} : écoute sans `audio`")
    if t in TYPES_IMAGE:
        img = carte.get("image")
        if not isinstance(img, dict):
            err.append(f"{ref} : type `{t}` sans image")
        else:
            for champ in ("fichier", "licence", "credit", "source", "alt"):
                if _vide(img.get(champ)):
                    err.append(f"{ref} : image sans `{champ}`")
    if "chrono" in carte and t not in TYPES_CHRONO:
        err.append(f"{ref} : chrono interdit sur le type `{t}`")

    if carte["partage"] in PARTAGES_SCANNES:
        err += scan_fuite(texte_de(carte, ("question", "reponse", "explication", "vigilance")), parc, ref)
    return err


def valide_chapitre(ch: dict, fichier: Path, programme: dict[str, dict],
                    parc: set[str], aujourdhui: date) -> list[str]:
    err: list[str] = []
    cid = ch.get("id") or "<sans id>"
    ref = f"{fichier.relative_to(ACADEMIE) if fichier.is_relative_to(ACADEMIE) else fichier.name}"
    if not isinstance(ch, dict):
        return [f"{ref} : un chapitre est un objet, pas un tableau"]
    for champ in CHAMPS_CHAPITRE:
        if champ not in ch or (_vide(ch.get(champ)) and champ not in ("prerequis", "sources")):
            err.append(f"{ref} : champ obligatoire manquant ou vide `{champ}`")
    for champ in CHAMPS_DERIVES:
        if champ in ch:
            err.append(f"{ref} : `{champ}` est dérivé par le valideur, jamais écrit à la main")
    if err:
        return err
    if not RE_ID_CHAPITRE.match(str(cid)):
        err.append(f"{ref} : id de chapitre attendu `domaine.branche.slug`")
    if ch.get("satellite"):
        # Un satellite (decisions/0009) vit hors du programme : son identifiant
        # commence par `satellite.`, il se rattache à un chapitre du programme
        # et prend le domaine et la branche de ce rattachement.
        if not str(cid).startswith("satellite."):
            err.append(f"{ref} : un satellite porte un identifiant `satellite.<domaine>.<slug>`")
        if cid in programme:
            err.append(f"{ref} : un satellite ne peut pas porter l'identifiant d'un chapitre du programme")
        rp = ch.get("rattachement_propose")
        if rp not in programme:
            err.append(f"{ref} : satellite avec un `rattachement_propose` inconnu ({rp})")
        else:
            for champ in ("domaine", "branche"):
                if ch.get(champ) != programme[rp].get(champ):
                    err.append(f"{ref} : `{champ}` du satellite diffère de son rattachement")
    else:
        attendu = programme.get(cid)
        if attendu is None:
            err.append(f"{ref} : chapitre `{cid}` absent du programme")
        else:
            for champ in ("domaine", "branche", "niveau"):
                if ch.get(champ) != attendu.get(champ):
                    err.append(f"{ref} : `{champ}` ({ch.get(champ)}) diffère du programme ({attendu.get(champ)})")
    for p in ch.get("prerequis") or []:
        if p not in programme:
            err.append(f"{ref} : prérequis inconnu `{p}`")
        elif programme[p]["niveau"] > ch["niveau"]:
            err.append(f"{ref} : prérequis `{p}` de niveau supérieur")
    obj = ch.get("objectifs") or []
    if not 2 <= len(obj) <= 5:
        err.append(f"{ref} : 2 à 5 objectifs attendus")
    amorce = ch.get("amorce") or {}
    for champ in ("question", "reponse_attendue"):
        if _vide(amorce.get(champ)):
            err.append(f"{ref} : amorce sans `{champ}`")
    lecon = str(ch.get("lecon") or "")
    if not LECON_MIN <= len(lecon) <= LECON_MAX:
        err.append(f"{ref} : leçon de {len(lecon)} caractères, attendu {LECON_MIN} à {LECON_MAX}")
    synth = ch.get("synthese") or {}
    if _vide(synth.get("consigne")) or not 3 <= len(synth.get("attendus") or []) <= 10:
        err.append(f"{ref} : synthèse sans consigne ou sans 3 à 10 attendus")
    if ch["statut"] not in STATUTS:
        err.append(f"{ref} : statut inconnu")
    if ch["partage"] not in PARTAGES:
        err.append(f"{ref} : partage inconnu")
    if not RE_DATE.match(str(ch["verifie"])):
        err.append(f"{ref} : `verifie` n'est pas une date")
    if ch["statut"] == "valide" and _vide(ch.get("verifie_par")):
        err.append(f"{ref} : chapitre `valide` sans `verifie_par`")
    if not isinstance(ch.get("version"), int) or ch["version"] < 1:
        err.append(f"{ref} : `version` doit être un entier ≥ 1")
    err += valide_provenance(ch.get("provenance"), ref)
    err += valide_sources(ch.get("sources") or [], ref)
    prov = ch.get("provenance") if isinstance(ch.get("provenance"), dict) else {}
    if not ch.get("sources") and prov.get("sans_source") is not True:
        err.append(f"{ref} : chapitre sans source et `sans_source` non avoué")
    if ch.get("satellite") and _vide(ch.get("rattachement_propose")):
        err.append(f"{ref} : satellite sans `rattachement_propose`")
    if ch["partage"] in PARTAGES_SCANNES:
        err += scan_fuite(texte_de(ch, ("titre", "lecon")) + "\n" + str(amorce.get("question") or ""), parc, ref)

    cartes = ch.get("cartes")
    if cartes is None and _vide(ch.get("cartes_fichier")):
        err.append(f"{ref} : ni `cartes` ni `cartes_fichier`")
    for carte in cartes or []:
        if not isinstance(carte, dict):
            err.append(f"{ref} : une carte est un objet")
            continue
        err += valide_carte(carte, ch, ref, parc, aujourdhui)
    return err


def charge_chapitres() -> tuple[list[tuple[dict, Path]], list[str]]:
    chapitres, err = [], []
    if not CHAPITRES.is_dir():
        return chapitres, err
    for f in sorted(CHAPITRES.rglob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            err.append(f"{f.name} : JSON illisible ({exc})")
            continue
        chapitres.append((data, f))
    return chapitres, err


def main() -> int:
    ap = argparse.ArgumentParser(description="Valideur des chapitres v2.")
    ap.add_argument("--json", action="store_true", help="dérivés en sortie machine")
    ap.add_argument("--rapport", action="store_true", help="comptes par note et statut")
    args = ap.parse_args()

    aujourdhui = date.today()
    programme = charge_programme()
    parc = noms_du_parc()
    chapitres, err = charge_chapitres()
    vus_ch: dict[str, Path] = {}
    vus_cartes: dict[str, str] = {}
    derives: list[dict] = []
    nb_cartes = 0
    for ch, f in chapitres:
        if not isinstance(ch, dict):
            err.append(f"{f.name} : un chapitre est un objet, pas un tableau")
            continue
        cid = str(ch.get("id"))
        if cid in vus_ch:
            err.append(f"{f.name} : id de chapitre dupliqué `{cid}` (déjà dans {vus_ch[cid].name})")
        vus_ch[cid] = f
        err += valide_chapitre(ch, f, programme, parc, aujourdhui)
        a_rec, note = derive(ch, ch.get("sources") or [], aujourdhui)
        derives.append({"id": cid, "a_recouper": a_rec, "note_confiance": note,
                        "statut": ch.get("statut"), "cartes": []})
        for carte in (ch.get("cartes") or []):
            if not isinstance(carte, dict):
                continue
            nb_cartes += 1
            kid = str(carte.get("id"))
            if kid in vus_cartes:
                err.append(f"{f.name}:{kid} : id de carte dupliqué (déjà dans {vus_cartes[kid]})")
            vus_cartes[kid] = f.name
            a_rec_c, note_c = derive(carte, carte.get("source") or [], aujourdhui)
            derives[-1]["cartes"].append({"id": kid, "a_recouper": a_rec_c,
                                          "note_confiance": note_c, "statut": carte.get("statut")})

    if args.json:
        print(json.dumps({"chapitres": derives, "erreurs": err}, ensure_ascii=False, indent=2))
        return 1 if err else 0
    for e in err:
        print(f"✗ {e}")
    statuts: dict[str, int] = {}
    notes: dict[str, int] = {}
    for d in derives:
        for c in d["cartes"]:
            statuts[c["statut"]] = statuts.get(c["statut"], 0) + 1
            notes[c["note_confiance"]] = notes.get(c["note_confiance"], 0) + 1
    detail = ", ".join(f"{v} {k}" for k, v in sorted(statuts.items()))
    print(f"chapitres : {len(chapitres)} chapitre(s), {nb_cartes} carte(s)"
          + (f" — {detail}" if detail else "")
          + (" ; notes " + ", ".join(f"{k} {v}" for k, v in sorted(notes.items())) if notes else ""))
    if args.rapport:
        for d in derives:
            print(f"  {d['id']} [{d['statut']}] note {d['note_confiance']}"
                  f"{' à recouper' if d['a_recouper'] else ''} — {len(d['cartes'])} carte(s)")
    if err:
        print(f"{len(err)} erreur(s) : rien ne se publie.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Tests de bout en bout : de la donnée brute jusqu'à l'écran du joueur.

Les autres fichiers de test vérifient un maillon chacun. Celui-ci suit
le trajet complet d'une carte et vérifie ce qui se passe AUX JOINTURES,
là où les bugs se logent :

    banque/*.json  →  valide_banque  →  genere  →  seance  →  React

Quatre garanties, dans l'ordre de gravité si elles cassent :

  1. **Rien de privé ne sort en distribution.** Une carte `perso` ou
     `interne` ne doit jamais atterrir dans un paquet destiné à
     l'extérieur. C'est ce qui rendra M9 (le partage aux collègues) sûr
     par construction plutôt que par relecture.
  2. **Rien de non vérifié n'atteint le joueur en production.** Une
     carte `brouillon` est du contenu que personne n'a recoupé : elle
     peut être jouée en développement, jamais servie comme un savoir.
  3. **Une donnée malformée est refusée, pas rendue.** Le pipeline
     s'arrête au valideur ; il ne produit jamais un écran à moitié faux.
  4. **Le contrat de sortie est stable.** Ce que le front reçoit garde
     la forme que le front attend, et ne fuit pas de champs de travail.

    python3 app/tests_chaine.py
"""

from __future__ import annotations

import copy
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from valide_banque import valide_carte  # noqa: E402

APP = Path(__file__).resolve().parent
RACINE = APP.parent
FRONT = RACINE / "frontend" / "src" / "data" / "academie.js"

CONFIG = {"domaines": {"droit": {"titre": "Droit"}, "pathologie": {"titre": "Patho"}},
          "quotas": {"revisions_par_seance": 10, "nouveau_par_seance": 1,
                     "plafond_reprise": 20},
          "fsrs": {"retention_souhaitee": 0.9}}
AUJ = date(2026, 8, 28)


def carte(cid, **kw):
    base = {"id": cid, "domaine": "droit", "branche": "b", "type": "flash",
            "question": f"q {cid}", "reponse": "r", "source": [{"texte": "Art. 24"}],
            "verifie": "2026-08-28", "statut": "valide", "partage": "banque"}
    base.update(kw)
    return base


def genere(banque: list[dict], *args: str) -> tuple[dict | None, str, int]:
    """Lance genere.py sur une banque jetable et rend (charge, stderr, code)."""
    tmp = Path(tempfile.mkdtemp(prefix="academie-chaine-"))
    try:
        (tmp / "banque" / "droit").mkdir(parents=True)
        (tmp / "banque" / "droit" / "t.json").write_text(
            json.dumps(banque, ensure_ascii=False), encoding="utf-8")
        shutil.copy(RACINE / "academie.json", tmp / "academie.json")
        sortie = tmp / "out.json"
        # genere.py résout la banque depuis valide_banque : on le fait
        # pointer sur la banque jetable via le répertoire de travail.
        res = subprocess.run(
            [sys.executable, str(APP / "genere.py"), "--sortie", str(sortie), *args],
            capture_output=True, text=True, env={"PATH": "/usr/bin:/bin",
                                                 "ACADEMIE_RACINE": str(tmp)})
        charge = json.loads(sortie.read_text(encoding="utf-8")) if sortie.exists() else None
        return charge, res.stderr + res.stdout, res.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 1. Rien de privé ne sort ---------------------------------------
def test_cloisonnement_des_couches() -> list[str]:
    """Le filtre de distribution est mécanique, pas déclaratif."""
    from genere import carte_publique  # import tardif : module testé

    banque = [carte("pub", partage="banque"),
              carte("int", partage="interne"),
              carte("priv", partage="perso")]
    err = []

    # Distribution externe : la couche `banque` et rien d'autre.
    externe = {c["id"] for c in banque if c["partage"] in {"banque"}}
    if externe != {"pub"}:
        err.append(f"distribution externe : {externe}, attendu {{'pub'}}")

    # Usage interne (JB + collègues Sergic) : banque + interne, jamais perso.
    interne = {c["id"] for c in banque if c["partage"] in {"banque", "interne"}}
    if "priv" in interne:
        err.append("une carte `perso` entre dans la distribution interne")

    # La carte publiée ne doit pas emporter de champs de travail.
    pub = carte_publique(carte("x", origine="outputs/IMMEUBLES/OFF-SECRET/piece.md"))
    if "origine" in pub:
        err.append("`origine` (chemin interne du repo) est exposée au front")
    return err


def test_anti_fuite_bloque_les_noms_reels() -> list[str]:
    """Un nom de copropriété réel doit faire échouer la validation."""
    parc = {"jardins de la perriere"}
    err = []

    fuite = carte("f", question="Aux Jardins de la Perrière, quelle majorité ?")
    if not valide_carte(fuite, Path("t.json"), CONFIG, parc, AUJ):
        err.append("un nom de copro réel passe la validation en couche `banque`")

    # Sans accents et en casse différente : doit être attrapé aussi.
    fuite2 = carte("f2", reponse="Voir JARDINS DE LA PERRIERE, bâtiment B")
    if not valide_carte(fuite2, Path("t.json"), CONFIG, parc, AUJ):
        err.append("le scan anti-fuite est sensible à la casse ou aux accents")

    # Le slug OFF-* doit être attrapé où qu'il soit dans la carte.
    fuite3 = carte("f3", explication="cf. OFF-HELIOS-C2")
    if not valide_carte(fuite3, Path("t.json"), CONFIG, parc, AUJ):
        err.append("un slug OFF-* dans `explication` n'est pas détecté")

    # En couche `perso`, c'est légitime : ça ne doit PAS bloquer.
    ok = carte("p", partage="perso", question="Aux Jardins de la Perrière ?")
    if valide_carte(ok, Path("t.json"), CONFIG, parc, AUJ):
        err.append("la couche `perso` est bloquée alors qu'elle a le droit")
    return err


# --- 2. Rien de non vérifié n'atteint le joueur ----------------------
def test_production_ne_sert_que_le_verifie() -> list[str]:
    banque = [carte("ok"), carte("br", statut="brouillon"),
              carte("sig", statut="signale"), carte("per", statut="perime")]
    charge, _, code = genere(banque, "--production")
    if charge is None:
        return [f"genere.py --production n'a rien produit (code {code})"]
    servis = {c["id"] for c in charge["cartes"]}
    err = []
    if servis != {"ok"}:
        err.append(f"--production sert {servis}, attendu {{'ok'}}")
    return err


def test_dev_sert_le_brouillon_mais_le_marque() -> list[str]:
    """En dev on joue les brouillons, à condition que le statut voyage."""
    banque = [carte("br", statut="brouillon")]
    charge, _, _ = genere(banque, "--avec-brouillons")
    if charge is None:
        return ["genere.py n'a rien produit en mode dev"]
    err = []
    if not charge["cartes"]:
        err.append("le mode dev ne sert aucun brouillon")
    elif charge["cartes"][0].get("statut") != "brouillon":
        err.append("le statut `brouillon` ne voyage pas jusqu'au front : "
                   "l'écran ne peut donc pas prévenir le joueur")
    return err


# --- 3. Une donnée malformée est refusée, pas rendue -----------------
def test_defaut_est_sur() -> list[str]:
    """Le défaut, sans aucun drapeau, ne sert que du vérifié.

    Régression du 28/08/2026 : `genere.py` servait les brouillons par
    défaut et n'excluait le non-vérifié qu'avec --production. Celui qui
    lance la commande sans y penser publiait du non-recoupé, en
    contradiction avec le contrat carte-v1 §3.3.
    """
    banque = [carte("ok"), carte("br", statut="brouillon")]
    charge, _, _ = genere(banque)              # AUCUN drapeau
    if charge is None:
        return ["genere.py sans drapeau n'a rien produit"]
    servis = {c["id"] for c in charge["cartes"]}
    if servis != {"ok"}:
        return [f"le défaut sert {servis} : une carte non vérifiée sort "
                f"sans qu'on l'ait demandé"]
    return []


def test_donnee_malformee_arrete_la_chaine() -> list[str]:
    """Aucune sortie ne doit être produite depuis une banque invalide."""
    cas = {
        "sans source": carte("x", source=[]),
        "date invalide": carte("x", verifie="28/08/2026"),
        "domaine inconnu": carte("x", domaine="inexistant"),
        "QCM sans bonne réponse": carte("x", type="qcm", choix=[
            {"texte": "a", "correct": False, "pourquoi_faux": "p"},
            {"texte": "b", "correct": False, "pourquoi_faux": "p"},
            {"texte": "c", "correct": False, "pourquoi_faux": "p"}]),
        "image sans licence": carte("x", type="photo", image={"fichier": "f.jpg"}),
        "périmée encore valide": carte("x", peremption="2020-01-01"),
    }
    # Champs carrément ABSENTS. Ces cas-là ne sont attrapés QUE par la
    # boucle des champs obligatoires : sans eux, on pouvait neutraliser
    # cette boucle sans qu'aucun test ne s'en aperçoive (trouvé par test
    # de mutation le 28/08/2026).
    for manquant in ("question", "reponse", "partage", "statut", "type",
                     "domaine", "branche", "id"):
        incomplete = carte("x")
        del incomplete[manquant]
        cas[f"sans `{manquant}`"] = incomplete
    err = []
    for nom, mauvaise in cas.items():
        charge, _, code = genere([mauvaise])
        if code == 0:
            err.append(f"« {nom} » : la génération réussit au lieu d'échouer")
        if charge is not None:
            err.append(f"« {nom} » : un fichier de sortie a été écrit malgré l'erreur")
    return err


def test_json_casse_ne_produit_rien() -> list[str]:
    tmp = Path(tempfile.mkdtemp(prefix="academie-json-"))
    try:
        (tmp / "banque" / "droit").mkdir(parents=True)
        (tmp / "banque" / "droit" / "t.json").write_text("{ pas du json", encoding="utf-8")
        shutil.copy(RACINE / "academie.json", tmp / "academie.json")
        sortie = tmp / "out.json"
        res = subprocess.run(
            [sys.executable, str(APP / "genere.py"), "--sortie", str(sortie)],
            capture_output=True, text=True,
            env={"PATH": "/usr/bin:/bin", "ACADEMIE_RACINE": str(tmp)})
        if res.returncode == 0:
            return ["un JSON illisible n'arrête pas la génération"]
        if sortie.exists():
            return ["un fichier a été écrit depuis un JSON illisible"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 4. Le contrat de sortie vers le front est stable ----------------
def test_contrat_de_sortie() -> list[str]:
    """Ce que le front attend doit être ce que le générateur produit."""
    banque = [carte("c1", type="qcm", choix=[
        {"texte": "bon", "correct": True},
        {"texte": "faux", "correct": False, "pourquoi_faux": "parce que"},
        {"texte": "autre", "correct": False, "pourquoi_faux": "parce que"}])]
    charge, _, _ = genere(banque)
    if charge is None:
        return ["pas de sortie générée"]
    err = []
    for cle in ("domaines", "quotas", "cartes", "genere_le"):
        if cle not in charge:
            err.append(f"la charge servie au front n'a pas `{cle}`")
    c = charge["cartes"][0]
    for champ in ("id", "domaine", "type", "question", "reponse", "source", "statut"):
        if champ not in c:
            err.append(f"la carte servie n'a pas `{champ}`")
    if c.get("choix") and "pourquoi_faux" not in c["choix"][1]:
        err.append("les explications de distracteurs ne parviennent pas au front")

    # Le module React doit consommer exactement ces clés.
    if FRONT.is_file():
        js = FRONT.read_text(encoding="utf-8")
        for attendu in ("banque.cartes", "banque.domaines", "statut"):
            if attendu not in js:
                err.append(f"le module front ne lit pas `{attendu}` "
                           f"(contrat de sortie et front désaccordés)")
    return err


# --- 5. La chaîne v2 : chapitres/ → genere → écran -------------------
#
# ACA-CONTRAT-2 étape 1. Ces tests décrivent ce que `genere.py` doit
# faire de `chapitres/` AVANT que la migration des 84 cartes v1 soit
# faite : ils ne dépendent d'aucune table d'assignation, donc ils se
# tiennent pendant que l'étape 2 attend l'arbitrage de JB.
#
# La règle de transition est celle du cahier : un chapitre `brouillon`
# ne se joue pas, MAIS ses cartes `valide` et relues sont servies, pour
# ne pas priver JB de son contenu vérifié pendant la migration. Elle est
# datée et se retire à la fin d'ACA-CONTENT-2.

AUJ_ISO = date.today().isoformat()
PROV = {"auteur": "modele", "modele": "test-modele", "genere_le": AUJ_ISO,
        "session": "tests_chaine", "sources_retrouvees": 1,
        "sources_concordantes": 1, "sans_source": False}
SRC_A = {"texte": "Art. 24, loi du 10 juillet 1965", "nature": "texte-officiel"}
PROGRAMME_V2 = {
    "version": "test", "metier": "test", "genere_le": AUJ_ISO,
    "domaines": {"droit": {"titre": "Droit", "ordre": 1}},
    "branches": {"droit": [{"cle": "majorites", "titre": "Majorités", "ordre": 1}]},
    "niveaux": {"1": "Découverte"},
    "chapitres": [
        {"id": "droit.majorites.article-24", "domaine": "droit", "branche": "majorites",
         "titre": "L'article 24", "niveau": 1, "prerequis": [], "statut": "a-ecrire"},
        {"id": "droit.majorites.tableau", "domaine": "droit", "branche": "majorites",
         "titre": "Le tableau", "niveau": 2,
         "prerequis": ["droit.majorites.article-24"], "statut": "a-ecrire"},
    ],
}


def carte_v2(cid: str, **maj) -> dict:
    base = {
        "id": cid, "chapitre": "droit.majorites.article-24", "domaine": "droit",
        "branche": "majorites", "type": "flash", "niveau": 1,
        "question": f"Question {cid} sur l'article 24 ?",
        "reponse": "La majorité des voix exprimées.",
        "source": [copy.deepcopy(SRC_A)], "provenance": copy.deepcopy(PROV),
        "verifie": AUJ_ISO, "statut": "valide", "partage": "banque",
        "verifie_par": "agent frais, tests_chaine",
    }
    base.update(maj)
    return base


def chapitre_v2(**maj) -> dict:
    base = {
        "id": "droit.majorites.article-24", "titre": "L'article 24",
        "domaine": "droit", "branche": "majorites", "niveau": 1, "prerequis": [],
        "objectifs": ["Dire ce que vote l'article 24.", "Calculer une majorité."],
        "amorce": {"question": "250 pour, 200 contre, 150 abstentions : adoptée ?",
                   "reponse_attendue": "Oui : les abstentions ne comptent pas."},
        "lecon": "x" * 1600,
        "synthese": {"consigne": "Explique l'article 24 en une phrase.",
                     "attendus": ["voix exprimées", "présents ou représentés",
                                  "abstentions exclues"]},
        "cartes": [carte_v2("droit-majorites-definition")],
        "sources": [copy.deepcopy(SRC_A)], "provenance": copy.deepcopy(PROV),
        "statut": "brouillon", "partage": "banque", "verifie": AUJ_ISO, "version": 1,
    }
    base.update(maj)
    return base


def genere_v2(chapitres: list[dict], banque_v1: list[dict] | None = None,
              *args: str) -> tuple[dict | None, str, int]:
    """Lance genere.py sur une racine jetable qui porte `chapitres/`.

    Même geste que `genere()`, avec un programme et des chapitres v2. La
    banque v1 est facultative : c'est ce qui permet d'observer la
    disposition mixte, celle de la migration en cours.
    """
    tmp = Path(tempfile.mkdtemp(prefix="academie-v2-"))
    try:
        (tmp / "programme").mkdir()
        (tmp / "programme" / "test.json").write_text(
            json.dumps(PROGRAMME_V2, ensure_ascii=False), encoding="utf-8")
        dossier = tmp / "chapitres" / "droit" / "majorites"
        dossier.mkdir(parents=True)
        for i, ch in enumerate(chapitres):
            (dossier / f"ch{i}.json").write_text(
                json.dumps(ch, ensure_ascii=False), encoding="utf-8")
        (tmp / "banque" / "droit").mkdir(parents=True)
        (tmp / "banque" / "droit" / "t.json").write_text(
            json.dumps(banque_v1 or [], ensure_ascii=False), encoding="utf-8")
        shutil.copy(RACINE / "academie.json", tmp / "academie.json")
        sortie = tmp / "out.json"
        res = subprocess.run(
            [sys.executable, str(APP / "genere.py"), "--sortie", str(sortie), *args],
            capture_output=True, text=True, env={"PATH": "/usr/bin:/bin",
                                                 "ACADEMIE_RACINE": str(tmp)})
        charge = json.loads(sortie.read_text(encoding="utf-8")) if sortie.exists() else None
        return charge, res.stderr + res.stdout, res.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_v2_traverse_la_chaine() -> list[str]:
    """Une carte v2 part de `chapitres/` et arrive à l'écran entière."""
    charge, sortie, code = genere_v2([chapitre_v2(statut="valide",
                                                  verifie_par="agent frais")])
    if charge is None:
        return [f"aucune sortie pour une banque v2 valide (code {code}) : {sortie[-400:]}"]
    err = []
    if charge.get("contrat") != "carte-v2":
        err.append(f"une banque servie entièrement depuis chapitres/ publie "
                   f"`contrat` = {charge.get('contrat')!r}, attendu 'carte-v2'")
    servies = {c["id"]: c for c in charge["cartes"]}
    if "droit-majorites-definition" not in servies:
        return err + [f"la carte du chapitre n'est pas servie : {sorted(servies)}"]
    c = servies["droit-majorites-definition"]
    for champ in ("chapitre", "provenance", "note_confiance", "a_recouper"):
        if champ not in c:
            err.append(f"la carte v2 servie n'a pas `{champ}` : le joueur ne peut "
                       f"pas voir d'où elle vient ni ce qu'elle vaut")
    if c.get("note_confiance") not in ("A", "B", "C"):
        err.append(f"note_confiance dérivée invalide : {c.get('note_confiance')!r}")
    if not charge.get("chapitres"):
        err.append("l'arbre n'est pas publié : pas de `chapitres`")
    else:
        avec_prerequis = [ch for ch in charge["chapitres"] if ch.get("prerequis")]
        if not avec_prerequis:
            err.append("aucun prérequis publié : l'arbre n'a plus d'ordre")
    if not (charge.get("fsrs") or {}).get("poids"):
        err.append("les poids FSRS ne sont pas publiés : la parité du client "
                   "reposerait sur une constante recopiée")
    return err


def test_regle_de_transition_du_chapitre_brouillon() -> list[str]:
    """Un chapitre `brouillon` ne se joue pas, ses cartes relues si.

    Règle de transition datée du cahier ACA-CONTRAT-2 : sans elle, la
    migration priverait JB de son contenu vérifié tant que la leçon
    n'est pas écrite (ACA-CONTENT-2).
    """
    ch = chapitre_v2(cartes=[
        carte_v2("droit-majorites-relue"),
        carte_v2("droit-majorites-non-relue", statut="brouillon"),
    ])
    charge, sortie, code = genere_v2([ch])
    if charge is None:
        return [f"aucune sortie (code {code}) : {sortie[-400:]}"]
    servies = {c["id"] for c in charge["cartes"]}
    err = []
    if "droit-majorites-relue" not in servies:
        err.append("une carte `valide` et relue d'un chapitre `brouillon` n'est "
                   "pas servie : la règle de transition ne s'applique pas")
    if "droit-majorites-non-relue" in servies:
        err.append("une carte `brouillon` est servie par défaut")
    return err


def test_chapitre_signale_ne_sert_rien() -> list[str]:
    """Un chapitre retiré emporte ses cartes, quel que soit leur statut."""
    charge, sortie, code = genere_v2([chapitre_v2(statut="signale")])
    if charge is None:
        return [f"aucune sortie (code {code}) : {sortie[-400:]}"]
    if {c["id"] for c in charge["cartes"]} & {"droit-majorites-definition"}:
        return ["un chapitre `signale` sert quand même ses cartes"]
    return []


def test_v2_invalide_arrete_la_chaine() -> list[str]:
    """Le valideur v2 garde la porte, exactement comme le v1."""
    cas = {
        "source sans nature": chapitre_v2(cartes=[
            carte_v2("droit-majorites-sans-nature",
                     source=[{"texte": "quelque part"}])]),
        "carte sans provenance": chapitre_v2(cartes=[
            {k: v for k, v in carte_v2("droit-majorites-orpheline").items()
             if k != "provenance"}]),
        "chapitre absent du programme": chapitre_v2(
            id="droit.majorites.nulle-part",
            cartes=[carte_v2("droit-majorites-x", chapitre="droit.majorites.nulle-part")]),
    }
    err = []
    for nom, ch in cas.items():
        charge, _, code = genere_v2([ch])
        if code == 0:
            err.append(f"« {nom} » : la génération réussit au lieu d'échouer")
        if charge is not None:
            err.append(f"« {nom} » : un fichier a été écrit malgré l'erreur v2")
    return err


def test_disposition_mixte_reste_en_v1() -> list[str]:
    """Tant qu'une carte v1 est servie, la banque n'est pas une v2.

    Le champ `contrat` n'est pas un vœu : il dit au client ce qu'il peut
    supposer de CHAQUE carte servie. Une carte v1 n'a ni `chapitre` ni
    `provenance` ; annoncer `carte-v2` sur un lot mixte serait un
    mensonge que le client paierait à l'écran. Le champ bascule tout
    seul quand `banque/` ne fournit plus rien : la migration flippe le
    contrat par construction, sans drapeau à ne pas oublier.
    """
    charge, sortie, code = genere_v2(
        [chapitre_v2(statut="valide", verifie_par="agent frais")],
        [carte("v1-restante")])
    if charge is None:
        return [f"aucune sortie en disposition mixte (code {code}) : {sortie[-400:]}"]
    err = []
    if charge.get("contrat") is not None:
        err.append(f"lot mixte publié en `contrat` = {charge['contrat']!r} : "
                   f"une carte v1 y est pourtant servie")
    servies = {c["id"] for c in charge["cartes"]}
    for attendue in ("v1-restante", "droit-majorites-definition"):
        if attendue not in servies:
            err.append(f"la disposition mixte perd `{attendue}` : {sorted(servies)}")
    return err


def test_id_duplique_entre_les_deux_dispositions() -> list[str]:
    """Le même identifiant des deux côtés : une carte en écrase une autre."""
    charge, _, code = genere_v2(
        [chapitre_v2(cartes=[carte_v2("doublon")])],
        [carte("doublon")])
    if code == 0:
        return ["un identifiant présent dans banque/ ET dans chapitres/ passe : "
                "l'état du joueur se rejoue sur deux cartes différentes"]
    if charge is not None:
        return ["un fichier a été écrit malgré l'identifiant dupliqué"]
    return []


def test_couche_perso_ne_sort_pas_dun_chapitre() -> list[str]:
    """Le cloisonnement des couches vaut aussi pour la v2."""
    ch = chapitre_v2(cartes=[carte_v2("droit-majorites-privee", partage="perso")])
    charge, sortie, code = genere_v2([ch], None, "--couches", "banque")
    if charge is None:
        return [f"aucune sortie (code {code}) : {sortie[-400:]}"]
    if "droit-majorites-privee" in {c["id"] for c in charge["cartes"]}:
        return ["une carte `perso` d'un chapitre part en distribution externe"]
    return []


def main() -> int:
    groupes = [
        ("1. cloisonnement des couches", test_cloisonnement_des_couches),
        ("1. anti-fuite sur les noms réels", test_anti_fuite_bloque_les_noms_reels),
        ("2. production ne sert que le vérifié", test_production_ne_sert_que_le_verifie),
        ("2. le DÉFAUT ne sert que du vérifié", test_defaut_est_sur),
        ("2. dev sert le brouillon, marqué", test_dev_sert_le_brouillon_mais_le_marque),
        ("3. donnée malformée arrête tout", test_donnee_malformee_arrete_la_chaine),
        ("3. JSON cassé ne produit rien", test_json_casse_ne_produit_rien),
        ("4. contrat de sortie vers le front", test_contrat_de_sortie),
        ("5. la chaîne v2 de bout en bout", test_v2_traverse_la_chaine),
        ("5. règle de transition du chapitre brouillon",
         test_regle_de_transition_du_chapitre_brouillon),
        ("5. un chapitre signalé ne sert rien", test_chapitre_signale_ne_sert_rien),
        ("5. banque v2 invalide arrête tout", test_v2_invalide_arrete_la_chaine),
        ("5. disposition mixte : contrat v1", test_disposition_mixte_reste_en_v1),
        ("5. identifiant dupliqué entre dispositions",
         test_id_duplique_entre_les_deux_dispositions),
        ("5. couche perso d'un chapitre", test_couche_perso_ne_sort_pas_dun_chapitre),
    ]
    total = []
    for nom, fn in groupes:
        err = fn()
        total += err
        print(f"  {'ok  ' if not err else 'ÉCHEC'} {nom}")
        for e in err:
            print(f"        ✗ {e}")
    if total:
        print(f"\n{len(total)} problème(s) sur la chaîne.")
        return 1
    print("\nVERT — la chaîne tient de la donnée brute jusqu'à l'écran.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

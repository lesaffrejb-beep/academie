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

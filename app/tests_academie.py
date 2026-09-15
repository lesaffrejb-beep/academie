#!/usr/bin/env python3
"""Tests de la surface agent `app/academie.py` (décision 0054).

Ce que ces tests protègent, dans l'ordre de gravité :

  1. **La surface ne recompose pas la séance.** Ce qu'elle rend est
     exactement ce que `seance.compose` rend sur le même journal : le
     moteur reste le professeur, l'agent le relaie.
  2. **Le journal est append-only.** Une réponse ajoute une ligne, ne
     réécrit ni ne supprime jamais les précédentes.
  3. **La réponse ne fuit pas.** `carte` montre la question sans la
     réponse ; `correction` la donne.
  4. **Un trou se nomme.** Banque absente, carte inconnue : la surface
     s'arrête avec un message, elle n'invente jamais une carte.
  5. **Les artefacts HTML sont écrits là où on le demande.**

Chaque test lance la surface en sous-processus sur une racine jetable
(`ACADEMIE_RACINE`), et compare, quand c'est le cas, au moteur appelé
directement sur la même racine.

    python3 app/tests_academie.py
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent
RACINE = APP.parent
PROFIL = "jb"

# Le moteur, appelé directement sur la racine jetable : la référence à
# laquelle la surface doit être identique.
CODE_MOTEUR = r"""
import json, os, sys
from datetime import date
from pathlib import Path
sys.path.insert(0, os.environ["ACADEMIE_APP"])
import seance
from valide_banque import charge_banque, charge_config
from genere import charge_programme
from planificateur import Planificateur
from progression import carte_monde

tmp = Path(os.environ["ACADEMIE_RACINE"])
seance.ETAT = tmp / "etat"
config = charge_config()
cartes = [c for c, _ in charge_banque()[0]]
journal = seance.lit_journal(os.environ["PROFIL"])
sched = Planificateur(retention=config["fsrs"]["retention_souhaitee"])
etats = seance.etats_cartes(journal, sched)
programme = charge_programme() or None
s = seance.compose(cartes, etats, config, date.today(), sched,
                   programme=programme, journal=journal)
monde = carte_monde(cartes, journal, config, programme=programme)
print(json.dumps({
    "ids": [c["id"] for c in s["revisions"] + s["nouveau"]],
    "graine": s["graine"], "jour": s["jour"],
    "xp": monde["xp"], "remplissage": monde["remplissage_global"],
    "dues": len(s["revisions"]),
}))
"""


def carte(cid, **maj) -> dict:
    base = {
        "id": cid, "domaine": "droit", "branche": "majorites", "niveau": 1,
        "type": "flash", "question": f"Question {cid} ?", "reponse": f"Réponse {cid}.",
        "explication": "Le pourquoi.", "vigilance": "Le piège.",
        "source": [{"texte": "Art. 24, loi du 10 juillet 1965",
                    "nature": "texte-officiel"}],
        "verifie": "2026-09-01", "statut": "valide", "partage": "banque",
    }
    base.update(maj)
    return base


def carte_qcm(cid) -> dict:
    return carte(cid, type="qcm", choix=[
        {"texte": "Bonne", "correct": True},
        {"texte": "Fausse A", "correct": False, "pourquoi_faux": "parce que A"},
        {"texte": "Fausse B", "correct": False, "pourquoi_faux": "parce que B"},
    ])


def racine_jetable(cartes=None, journal=None, avec_banque=True) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="academie-surface-"))
    shutil.copy(RACINE / "academie.json", tmp / "academie.json")
    if avec_banque:
        (tmp / "banque" / "droit").mkdir(parents=True)
        (tmp / "banque" / "droit" / "t.json").write_text(
            json.dumps(cartes if cartes is not None else [], ensure_ascii=False),
            encoding="utf-8")
    if journal is not None:
        dossier = tmp / "etat" / PROFIL
        dossier.mkdir(parents=True)
        (dossier / "revues.jsonl").write_text(
            "\n".join(json.dumps(l, ensure_ascii=False) for l in journal) + "\n",
            encoding="utf-8")
    return tmp


def racine_cursus() -> Path:
    """Une racine jetable avec deux cursus et une carte dans chacun."""
    tmp = racine_jetable([carte("a-droit", domaine="droit"),
                          carte("b-entree", domaine="entree")])
    prog = tmp / "programme"
    prog.mkdir()
    (prog / "catalogue.json").write_text(json.dumps({"parcours": [
        {"cle": "a", "titre": "Cursus A", "programme": "programme/a.json"},
        {"cle": "b", "titre": "Cursus B", "programme": "programme/b.json"}]}),
        encoding="utf-8")
    (prog / "a.json").write_text(json.dumps({
        "metier": "A", "domaines": {"droit": {"titre": "Droit", "ordre": 1}},
        "branches": {}, "chapitres": []}), encoding="utf-8")
    (prog / "b.json").write_text(json.dumps({
        "metier": "B", "domaines": {"entree": {"titre": "Entree", "ordre": 1}},
        "branches": {}, "chapitres": []}), encoding="utf-8")
    return tmp


def env(tmp: Path) -> dict:
    import os
    e = dict(os.environ)
    e["ACADEMIE_RACINE"] = str(tmp)
    e["ACADEMIE_APP"] = str(APP)
    e["PROFIL"] = PROFIL
    return e


def cli(tmp: Path, *args: str, etat: bool = True) -> tuple[int, str, str]:
    # Les options communes vivent sur chaque sous-parser : on les met
    # après la sous-commande, jamais avant.
    commande = [sys.executable, str(APP / "academie.py"), *args, "--profil", PROFIL]
    if etat:
        commande += ["--etat", str(tmp / "etat")]
    res = subprocess.run(commande, capture_output=True, text=True, env=env(tmp))
    return res.returncode, res.stdout, res.stderr


def cli_repo(*args: str):
    """La surface sur le dépôt réel, sans ACADEMIE_RACINE jetable."""
    import os
    e = dict(os.environ)
    e.pop("ACADEMIE_RACINE", None)
    res = subprocess.run([sys.executable, str(APP / "academie.py"), *args],
                         capture_output=True, text=True, env=e, cwd=str(RACINE))
    return res.returncode, res.stdout, res.stderr


def moteur(tmp: Path) -> dict:
    res = subprocess.run([sys.executable, "-c", CODE_MOTEUR],
                         capture_output=True, text=True, env=env(tmp))
    return json.loads(res.stdout) if res.returncode == 0 else {}


def journal_du(tmp: Path) -> list[dict]:
    p = tmp / "etat" / PROFIL / "revues.jsonl"
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def carnet_du(tmp: Path) -> list[dict]:
    p = tmp / "etat" / PROFIL / "erreurs.jsonl"
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


# --- 1. parité avec le moteur ----------------------------------------

def test_seance_est_celle_du_moteur() -> list[str]:
    cartes = [carte("droit-a"), carte("droit-b"), carte("droit-c"), carte_qcm("droit-q")]
    tmp = racine_jetable(cartes, journal=[
        {"quand": "2026-01-01T00:00:00+00:00", "carte": "droit-a", "note": 3, "mode": "flash"}])
    try:
        code, out, err = cli(tmp, "seance", "--json")
        if code != 0:
            return [f"seance --json a échoué (code {code}) : {err[-300:]}"]
        surface = json.loads(out)
        reference = moteur(tmp)
        ids_surface = [c["id"] for c in surface["cartes"]]
        if ids_surface != reference["ids"]:
            return [f"la surface ne joue pas la séance du moteur : "
                    f"{ids_surface} != {reference['ids']}"]
        if surface["graine"] != reference["graine"]:
            return [f"graine différente : {surface['graine']} != {reference['graine']}"]
        if surface["jour"] != reference["jour"]:
            return [f"jour différent : {surface['jour']} != {reference['jour']}"]
        # La carte due du journal doit être servie en révision.
        if reference["dues"] and surface["cartes"][0]["id"] != "droit-a":
            return ["la carte due n'est pas servie en tête"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_progression_est_celle_du_moteur() -> list[str]:
    cartes = [carte("droit-a"), carte("droit-b")]
    tmp = racine_jetable(cartes, journal=[
        {"quand": "2026-01-01T00:00:00+00:00", "carte": "droit-a", "note": 3, "mode": "flash"}])
    try:
        code, out, err = cli(tmp, "progression", "--json")
        if code != 0:
            return [f"progression --json a échoué (code {code}) : {err[-300:]}"]
        surface = json.loads(out)
        reference = moteur(tmp)
        if surface["xp"] != reference["xp"]:
            return [f"xp différent : {surface['xp']} != {reference['xp']}"]
        if surface["remplissage_global"] != reference["remplissage"]:
            return [f"remplissage différent : {surface['remplissage_global']} "
                    f"!= {reference['remplissage']}"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 2. journal append-only ------------------------------------------

def test_repondre_ajoute_sans_reecrire() -> list[str]:
    cartes = [carte("droit-a"), carte("droit-b")]
    origine = {"quand": "2026-01-01T00:00:00+00:00", "carte": "droit-a",
               "note": 3, "mode": "flash"}
    tmp = racine_jetable(cartes, journal=[origine])
    try:
        for note in (2, 4):
            code, out, err = cli(tmp, "repondre", "droit-b", str(note))
            if code != 0:
                return [f"repondre a échoué (code {code}) : {err[-300:]}"]
        lignes = journal_du(tmp)
        if lignes[0] != origine:
            return ["la première ligne du journal a été réécrite"]
        if len(lignes) != 3:
            return [f"attendu 3 lignes après deux réponses, reçu {len(lignes)}"]
        if [l["note"] for l in lignes[1:]] != [2, 4]:
            return ["les notes ajoutées ne sont pas dans l'ordre"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_repondre_carte_inconnue_necrit_rien() -> list[str]:
    cartes = [carte("droit-a")]
    tmp = racine_jetable(cartes, journal=[{"quand": "2026-01-01T00:00:00+00:00",
                                          "carte": "droit-a", "note": 3, "mode": "flash"}])
    try:
        avant = journal_du(tmp)
        code, out, err = cli(tmp, "repondre", "carte-fantome", "3")
        if code == 0:
            return ["repondre sur une carte inconnue réussit au lieu d'échouer"]
        if journal_du(tmp) != avant:
            return ["une carte inconnue a quand même écrit au journal"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 3. la réponse ne fuit pas ---------------------------------------

def test_la_question_cache_la_reponse() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "carte", "droit-a", "--json")
        if code != 0:
            return [f"carte a échoué (code {code}) : {err[-300:]}"]
        vue = json.loads(out)
        for champ in ("reponse", "explication", "vigilance"):
            if champ in vue:
                return [f"`{champ}` fuit dans la question"]
        code, out, _ = cli(tmp, "carte", "droit-a", "--reponse", "--json")
        avec = json.loads(out)
        if not (avec.get("correction") or {}).get("reponse"):
            return ["--reponse n'affiche pas la réponse"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_le_qcm_cache_le_bon_choix() -> list[str]:
    tmp = racine_jetable([carte_qcm("droit-q")])
    try:
        code, out, err = cli(tmp, "carte", "droit-q", "--json")
        if code != 0:
            return [f"carte qcm a échoué (code {code}) : {err[-300:]}"]
        choix = json.loads(out)["choix"]
        if any("correct" in c for c in choix):
            return ["un choix de QCM porte `correct` avant la correction"]
        code, out, _ = cli(tmp, "correction", "droit-q", "--json")
        if not any(c.get("correct") for c in json.loads(out)["choix"]):
            return ["la correction ne dit pas quel choix est juste"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 4. un trou se nomme ---------------------------------------------

def test_banque_absente_ne_sert_rien() -> list[str]:
    tmp = racine_jetable(avec_banque=False)
    try:
        code, out, err = cli(tmp, "seance", "--json")
        if code == 0:
            return ["une banque absente est servie comme si de rien n'était"]
        if "aucune carte" in out and json.loads(out).get("cartes"):
            return ["un trou a produit des cartes"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_banque_vide_ne_sert_rien() -> list[str]:
    tmp = racine_jetable([])
    try:
        code, out, err = cli(tmp, "seance", "--json")
        if code != 0:
            return [f"une banque vide fait planter au lieu de nommer le vide : {err[-200:]}"]
        charge = json.loads(out)
        if charge["cartes"]:
            return ["une banque vide sert des cartes"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_carte_inconnue_ne_sert_rien() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "carte", "inconnue", "--json")
        if code == 0:
            return ["une carte inconnue est servie"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 5. artefacts HTML ------------------------------------------------

def test_qcm_ecrit_un_html() -> list[str]:
    tmp = racine_jetable([carte_qcm("droit-q")])
    try:
        sortie = tmp / "art"
        code, out, err = cli(tmp, "qcm", "droit-q", "--sortie", str(sortie))
        if code != 0:
            return [f"qcm a échoué (code {code}) : {err[-300:]}"]
        html_ = Path(out.strip())
        if not html_.is_file():
            return [f"le QCM n'a pas été écrit : {out.strip()}"]
        contenu = html_.read_text(encoding="utf-8")
        for attendu in ("Question droit-q ?", "Bonne", "Fausse A"):
            if attendu not in contenu:
                return [f"le QCM ne contient pas « {attendu} »"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_schema_ecrit_une_fiche() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        sortie = tmp / "art"
        code, out, err = cli(tmp, "schema", "droit-a", "--sortie", str(sortie))
        if code != 0:
            return [f"schema a échoué (code {code}) : {err[-300:]}"]
        contenu = Path(out.strip()).read_text(encoding="utf-8")
        if "Réponse droit-a." not in contenu:
            return ["la fiche ne porte pas la réponse"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 6. carnet d'erreurs (ACA-SANS-FRONT-2) --------------------------

def test_erreur_ajoute_au_carnet() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "erreur", "droit-a", "confondu avec X")
        if code != 0:
            return [f"erreur a échoué (code {code}) : {err[-300:]}"]
        cli(tmp, "erreur", "droit-a")           # sans raison : autorisé
        lignes = carnet_du(tmp)
        if len(lignes) != 2:
            return [f"attendu 2 lignes de carnet, reçu {len(lignes)}"]
        if lignes[0].get("raison") != "confondu avec X":
            return ["la première ligne du carnet a été réécrite"]
        if lignes[1].get("raison") is not None:
            return ["une raison vide devrait rester nulle"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_erreur_carte_inconnue_necrit_rien() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "erreur", "fantome", "x")
        if code == 0:
            return ["noter une erreur sur une carte inconnue réussit"]
        if carnet_du(tmp):
            return ["une carte inconnue a quand même écrit au carnet"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_erreurs_relit_les_recurrentes() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        cli(tmp, "erreur", "droit-a", "confondu avec X")
        cli(tmp, "erreur", "droit-a", "lu trop vite")
        code, out, err = cli(tmp, "erreurs", "--json")
        if code != 0:
            return [f"erreurs a échoué (code {code}) : {err[-300:]}"]
        resume = json.loads(out)
        if resume["lignes"] != 2:
            return [f"le carnet devrait compter 2 lignes, reçu {resume['lignes']}"]
        occurrences = {f["carte"]: f["occurrences"] for f in resume["cartes"]}
        if occurrences.get("droit-a") != 2:
            return ["la carte à deux erreurs n'est pas remontée deux fois"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 7. quiz de positionnement (ACA-SANS-FRONT-2) --------------------

def test_quiz_sans_resultats_necrit_rien() -> list[str]:
    tmp = racine_jetable([carte(f"droit-{x}") for x in "abc"])
    try:
        code, out, err = cli(tmp, "quiz", "--region", "droit", "--json")
        if code != 0:
            return [f"quiz a échoué (code {code}) : {err[-300:]}"]
        charge = json.loads(out)
        if not charge["questions"]:
            return ["le quiz ne pose aucune question"]
        if any(q.get("reponse") for q in charge["questions"]):
            return ["une question de quiz porte sa réponse"]
        if journal_du(tmp):
            return ["un quiz sans résultats a écrit au journal"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_quiz_ecrit_les_bonnes_et_ouvre() -> list[str]:
    tmp = racine_jetable([carte(f"droit-{x}") for x in "abcde"])
    try:
        resultats = json.dumps({"droit-a": True, "droit-b": True, "droit-c": True,
                                "droit-d": True, "droit-e": False})
        code, out, err = cli(tmp, "quiz", "--region", "droit",
                             "--resultats", resultats, "--json",
                             "--quand", "2026-09-15T07:00:00+00:00")
        if code != 0:
            return [f"quiz --resultats a échoué (code {code}) : {err[-300:]}"]
        charge = json.loads(out)
        if charge["ecrites"] != 4:
            return [f"attendu 4 bonnes réponses écrites, reçu {charge['ecrites']}"]
        if "droit" not in charge["regions_ouvertes"]:
            return ["le quiz n'a pas ouvert la région malgré 80 % de réussite"]
        lignes = journal_du(tmp)
        if len(lignes) != 4:
            return [f"une mauvaise réponse a été écrite : {len(lignes)} lignes"]
        if any(l.get("origine") != "quiz" or l.get("carte") == "droit-e"
               for l in lignes):
            return ["les lignes de quiz ne portent pas la bonne origine"]
        code2, out2, err2 = cli(tmp, "quiz", "--region", "droit",
                                "--resultats", resultats, "--json")
        if code2 == 0:
            return ["un second quiz de la même région est accepté"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 8. aides de séance (ACA-SANS-FRONT-3) ---------------------------

def test_prevue_donne_quatre_intervalles() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "prevue", "droit-a", "--json")
        if code != 0:
            return [f"prevue a échoué (code {code}) : {err[-300:]}"]
        intervalles = json.loads(out)["intervalles"]
        if set(intervalles) != {"1", "2", "3", "4"}:
            return ["prevue ne rend pas une échéance pour chaque note"]
        if intervalles["4"]["intervalle_jours"] <= intervalles["1"]["intervalle_jours"]:
            return ["les intervalles ne dépendent pas de la note"]
        if "reponse" in out:
            return ["prevue laisse fuir la réponse"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_mini_lecons_liste_les_ratees() -> list[str]:
    journal = [{"quand": f"2026-09-{d:02d}T07:00:00+00:00", "carte": "droit-a",
                "note": 1, "mode": "flash"} for d in (1, 2, 3)]
    tmp = racine_jetable([carte("droit-a"), carte("droit-b")], journal=journal)
    try:
        code, out, err = cli(tmp, "mini-lecons", "--json")
        if code != 0:
            return [f"mini-lecons a échoué (code {code}) : {err[-300:]}"]
        cartes = {c["carte"]: c for c in json.loads(out)["cartes"]}
        if cartes.get("droit-a", {}).get("echecs") != 3:
            return ["la carte ratée trois fois n'est pas listée"]
        if "droit-b" in cartes:
            return ["une carte sans raté entre dans les mini-leçons"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_mini_lecons_vide() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "mini-lecons", "--json")
        if code != 0:
            return [f"mini-lecons a échoué (code {code}) : {err[-300:]}"]
        if json.loads(out)["cartes"]:
            return ["mini-leçons liste une carte sans raté"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 9. journal v1 et rituel (ACA-SANS-FRONT-4) ----------------------

def test_repondre_ecrit_une_ligne_v1() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "repondre", "droit-a", "3")
        if code != 0:
            return [f"repondre a échoué (code {code}) : {err[-300:]}"]
        lignes = journal_du(tmp)
        if not lignes:
            return ["repondre n'a rien écrit"]
        ligne = lignes[-1]
        if ligne.get("mode") != "revision":
            return [f"mode {ligne.get('mode')!r}, attendu 'revision'"]
        if not ligne.get("format"):
            return ["la ligne de révision n'a pas de format (journal-v1)"]
        if not ligne.get("nonce") or len(str(ligne["nonce"])) < 8:
            return ["la ligne de révision n'a pas de nonce valide"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rituel_lit_les_seances_de_la_surface() -> list[str]:
    tmp = racine_jetable([carte(f"droit-{x}") for x in "abc"])
    try:
        code, out, err = cli(tmp, "seance", "--journaliser", "--json")
        if code != 0:
            return [f"seance --journaliser a échoué (code {code}) : {err[-300:]}"]
        ids = [c["id"] for c in json.loads(out)["cartes"]]
        if not ids:
            return ["la séance ne sert aucune carte"]
        for cid in ids:
            cli(tmp, "repondre", cid, "3")
        code, out, err = cli(tmp, "rituel", "--json")
        if code != 0:
            return [f"rituel a échoué (code {code}) : {err[-300:]}"]
        rapport = json.loads(out)
        if rapport["ecartees"].get("mode_inconnu"):
            return ["le rituel écarte des lignes de mode inconnu"]
        if rapport["seances"]["commencees"] != 1:
            return [f"une séance attendue, reçu {rapport['seances']['commencees']}"]
        if rapport["seances"]["finies"] != 1:
            return [f"la séance ne compte pas finie : {rapport['seances']}"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_rituel_vide() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "rituel", "--json")
        if code != 0:
            return [f"rituel a échoué (code {code}) : {err[-300:]}"]
        if json.loads(out)["periode"]["de"] is not None:
            return ["un journal vide porte une période"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 10. cursus actif et isolation (ACA-SANS-FRONT-5) ----------------

def test_cursus_isole_les_domaines() -> list[str]:
    tmp = racine_cursus()
    try:
        for cle, attendu, exclu in (("a", "a-droit", "b-entree"),
                                    ("b", "b-entree", "a-droit")):
            code, out, err = cli(tmp, "seance", "--cursus", cle, "--json")
            if code != 0:
                return [f"seance --cursus {cle} a échoué (code {code}) : {err[-300:]}"]
            ids = [c["id"] for c in json.loads(out)["cartes"]]
            if attendu not in ids:
                return [f"cursus {cle} ne sert pas {attendu} : {ids}"]
            if exclu in ids:
                return [f"cursus {cle} sert {exclu} : fuite entre cursus"]
        code, out, _ = cli(tmp, "seance", "--json")
        ids = [c["id"] for c in json.loads(out)["cartes"]]
        if "b-entree" in ids:
            return ["sans --cursus, le premier parcours ne fait pas foi"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cursus_journalise_le_choix() -> list[str]:
    tmp = racine_cursus()
    try:
        code, out, err = cli(tmp, "cursus", "b")
        if code != 0:
            return [f"cursus b a échoué (code {code}) : {err[-300:]}"]
        code, out, err = cli(tmp, "seance", "--json")
        if code != 0:
            return [f"la séance après choix a échoué : {err[-300:]}"]
        ids = [c["id"] for c in json.loads(out)["cartes"]]
        if "b-entree" not in ids:
            return ["le cursus journalisé n'est pas respecté à la séance suivante"]
        if "a-droit" in ids:
            return ["le cursus journalisé laisse fuir l'autre cursus"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_cursus_inconnu() -> list[str]:
    tmp = racine_cursus()
    try:
        code, out, err = cli(tmp, "seance", "--cursus", "z", "--json")
        if code == 0:
            return ["un cursus inconnu est servi au lieu d'être refusé"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- 11. les cartes v2 sont servies (ACA-SANS-FRONT-6) ---------------

def test_les_cartes_v2_et_ifsi_sont_servies() -> list[str]:
    etat = Path(tempfile.mkdtemp(prefix="academie-repo-"))
    try:
        code, out, err = cli_repo("seance", "--cursus", "ifsi", "--json",
                                  "--etat", str(etat))
        if code != 0:
            return [f"seance --cursus ifsi sur le dépôt a échoué "
                    f"(code {code}) : {err[-300:]}"]
        cartes = json.loads(out)["cartes"]
        if not cartes:
            return ["aucune carte IFSI servie : les chapitres v2 ne sont pas chargés"]
        domaines = {c["domaine"] for c in cartes}
        ifs = {"entree", "sante-publique", "humaines", "corps", "pathologies",
               "hygiene", "pharmaco", "soins", "methodes", "stage", "culture"}
        if domaines - ifs:
            return [f"domaine hors IFSI servi : {sorted(domaines - ifs)}"]
        return []
    finally:
        shutil.rmtree(etat, ignore_errors=True)


# --- 12. sauvegarde et transfert (ACA-SANS-FRONT-7) ------------------

def test_export_import_union() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        cli(tmp, "repondre", "droit-a", "3")
        bundle = tmp / "sauvegarde.json"
        code, out, err = cli(tmp, "exporter", str(bundle))
        if code != 0:
            return [f"exporter a échoué (code {code}) : {err[-300:]}"]
        if not bundle.is_file():
            return ["aucun fichier de sauvegarde produit"]
        avant = len(journal_du(tmp))

        code, out, err = cli(tmp, "importer", str(bundle))
        if code != 0:
            return [f"importer a échoué (code {code}) : {err[-300:]}"]
        if len(journal_du(tmp)) != avant:
            return ["un import dans le même état a dupliqué des lignes"]

        tmp2 = racine_jetable([carte("droit-a")])
        try:
            code, out, err = cli(tmp2, "importer", str(bundle))
            if code != 0:
                return [f"import dans un état neuf a échoué : {err[-300:]}"]
            if len(journal_du(tmp2)) != avant:
                return [f"l'import ne rend pas les mêmes lignes : "
                        f"{len(journal_du(tmp2))} != {avant}"]
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)

        existante = {"quand": "2026-02-01T00:00:00+00:00", "mode": "revision",
                     "nonce": "deja-la", "carte": "droit-a", "note": 2,
                     "format": "seance"}
        tmp3 = racine_jetable([carte("droit-a")], journal=[existante])
        try:
            cli(tmp3, "importer", str(bundle))
            nonces = {l.get("nonce") for l in journal_du(tmp3)}
            if "deja-la" not in nonces:
                return ["l'import a effacé une ligne déjà présente"]
            if len(journal_du(tmp3)) != 1 + avant:
                return ["l'union n'ajoute pas les lignes manquantes"]
        finally:
            shutil.rmtree(tmp3, ignore_errors=True)
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_import_fichier_illisible() -> list[str]:
    tmp = racine_jetable([carte("droit-a")])
    try:
        code, out, err = cli(tmp, "importer", str(tmp / "absent.json"))
        if code == 0:
            return ["un fichier absent est importé au lieu d'être refusé"]
        return []
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


TESTS = [
    ("1. séance identique au moteur", test_seance_est_celle_du_moteur),
    ("1. progression identique au moteur", test_progression_est_celle_du_moteur),
    ("2. repondre ajoute sans réécrire", test_repondre_ajoute_sans_reecrire),
    ("2. carte inconnue n'écrit rien", test_repondre_carte_inconnue_necrit_rien),
    ("3. la question cache la réponse", test_la_question_cache_la_reponse),
    ("3. le QCM cache le bon choix", test_le_qcm_cache_le_bon_choix),
    ("4. banque absente : trou nommé", test_banque_absente_ne_sert_rien),
    ("4. banque vide : rien à jouer", test_banque_vide_ne_sert_rien),
    ("4. carte inconnue : rien à jouer", test_carte_inconnue_ne_sert_rien),
    ("5. qcm écrit un HTML", test_qcm_ecrit_un_html),
    ("5. schema écrit une fiche", test_schema_ecrit_une_fiche),
    ("6. erreur ajoute au carnet", test_erreur_ajoute_au_carnet),
    ("6. carte inconnue n'écrit rien au carnet", test_erreur_carte_inconnue_necrit_rien),
    ("6. erreurs relit les récurrentes", test_erreurs_relit_les_recurrentes),
    ("7. quiz sans résultats n'écrit rien", test_quiz_sans_resultats_necrit_rien),
    ("7. quiz n'écrit que les bonnes et ouvre", test_quiz_ecrit_les_bonnes_et_ouvre),
    ("8. prevue rend quatre intervalles croissants", test_prevue_donne_quatre_intervalles),
    ("8. mini-lecons liste les ratées", test_mini_lecons_liste_les_ratees),
    ("8. mini-lecons vide sans rate", test_mini_lecons_vide),
    ("9. repondre écrit une ligne v1", test_repondre_ecrit_une_ligne_v1),
    ("9. rituel lit les séances de la surface", test_rituel_lit_les_seances_de_la_surface),
    ("9. rituel vide", test_rituel_vide),
    ("10. le cursus isole les domaines", test_cursus_isole_les_domaines),
    ("10. le choix de cursus est journalisé", test_cursus_journalise_le_choix),
    ("10. un cursus inconnu est refusé", test_cursus_inconnu),
    ("11. les cartes v2 et l'IFSI sont servies", test_les_cartes_v2_et_ifsi_sont_servies),
    ("12. export puis import par union", test_export_import_union),
    ("12. import d'un fichier illisible refusé", test_import_fichier_illisible),
]


def main() -> int:
    total = []
    for nom, fn in TESTS:
        err = fn()
        total += err
        print(f"  {'ok  ' if not err else 'ÉCHEC'} {nom}")
        for e in err:
            print(f"        ✗ {e}")
    if total:
        print(f"\n{len(total)} problème(s) sur la surface agent.")
        return 1
    print("\nVERT — la surface relaie le moteur, journalise sans réécrire "
          "et ne laisse pas fuir la réponse.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

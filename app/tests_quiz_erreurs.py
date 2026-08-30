#!/usr/bin/env python3
"""Tests du quiz de positionnement et du carnet d'erreurs.

Les promesses protégées ici sont celles de la SPEC-PRODUIT §3, dans la
version corrigée au pré-mortem du 29/08/2026 :

  - une carte non vérifiée ne se joue jamais, quiz compris ;
  - le quiz couvre les régions, il ne fait pas vingt questions de droit ;
  - une bonne réponse vaut trois semaines de tranquillité (stabilité
    forcée), PAS les ~2 jours d'une première révision ordinaire — c'est
    le bug que le pré-mortem a trouvé, ce test est là pour qu'il ne
    revienne pas ;
  - une mauvaise réponse n'écrit rien ;
  - le quiz ne se rejoue pas ;
  - le carnet d'erreurs accepte une erreur sans explication et survit à
    une ligne corrompue ;
  - trois ratés remontent une carte, deux non.

Les profils sont jetables (répertoire temporaire) : ces tests
n'écrivent JAMAIS dans `academie/etat/`.

    python3 app/tests_quiz_erreurs.py
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import erreurs  # noqa: E402
import quiz  # noqa: E402
from planificateur import BIEN, RATE, Planificateur  # noqa: E402
from seance import etats_cartes  # noqa: E402

CONFIG = {
    "domaines": {"pathologie": {"ordre": 1}, "droit": {"ordre": 3},
                 "sinistres": {"ordre": 5}},
    "fsrs": {"retention_souhaitee": 0.9},
    "quiz": {"nb_questions": 12, "stabilite_initiale_jours": 21,
             "seuil_ouverture_region_quiz": 0.8},
}
AUJ = date(2026, 8, 29)


def carte(cid: str, domaine: str = "droit", statut: str = "valide") -> dict:
    return {"id": cid, "domaine": domaine, "branche": "b", "type": "flash",
            "question": f"question {cid}", "reponse": "r",
            "source": [{"texte": "s"}], "verifie": "2026-08-29",
            "statut": statut, "partage": "banque"}


def banque() -> list[dict]:
    return ([carte(f"pa{i}", "pathologie") for i in range(10)]
            + [carte(f"dr{i}", "droit") for i in range(10)]
            + [carte(f"si{i}", "sinistres") for i in range(10)])


def revue(cid: str, note: int, jour: date) -> dict:
    return {"quand": f"{jour.isoformat()}T07:00:00+00:00", "carte": cid,
            "note": note, "mode": "flash"}


def profil_jetable():
    return Path(tempfile.mkdtemp(prefix="academie-quiz-"))


# --- le quiz ---------------------------------------------------------

def test_jamais_de_brouillon() -> list[str]:
    """La garantie du contrat carte-v1 vaut aussi pour le quiz."""
    cartes = (banque()
              + [carte("brouillon-1", "droit", "brouillon"),
                 carte("signale-1", "pathologie", "signale"),
                 carte("perime-1", "sinistres", "perime")])
    servis = {c["id"] for c in quiz.compose(cartes, CONFIG, graine=1)}
    interdits = servis & {"brouillon-1", "signale-1", "perime-1"}
    return [f"cartes non valides servies : {interdits}"] if interdits else []


def test_couvre_les_regions() -> list[str]:
    """Vingt questions de droit ne positionnent personne."""
    err = []
    questions = quiz.compose(banque(), CONFIG, graine=7)
    if len(questions) != CONFIG["quiz"]["nb_questions"]:
        err.append(f"{len(questions)} questions, attendu "
                   f"{CONFIG['quiz']['nb_questions']}")
    regions = {c["domaine"] for c in questions}
    if regions != {"pathologie", "droit", "sinistres"}:
        err.append(f"régions couvertes : {sorted(regions)}, attendu les trois")
    return err


def test_couverture_minimale_region_pauvre() -> list[str]:
    """Une région à une seule carte reste servie : au moins une par région."""
    cartes = ([carte(f"dr{i}", "droit") for i in range(30)]
              + [carte("pa0", "pathologie")])
    questions = quiz.compose(cartes, CONFIG, graine=3)
    if not any(c["domaine"] == "pathologie" for c in questions):
        return ["la région pauvre a été écrasée par la région riche"]
    return []


def test_quiz_sans_carte_ne_casse_pas() -> list[str]:
    try:
        vide = quiz.compose([], CONFIG, graine=1)
    except Exception as exc:                                  # noqa: BLE001
        return [f"quiz sur banque vide lève : {exc!r}"]
    return [] if vide == [] else ["quiz non vide sur banque vide"]


def test_deterministe() -> list[str]:
    """Même graine, même quiz — dans le même ordre."""
    a = [c["id"] for c in quiz.compose(banque(), CONFIG, graine=42)]
    b = [c["id"] for c in quiz.compose(banque(), CONFIG, graine=42)]
    if a != b:
        return ["deux compositions à graine fixée diffèrent"]
    c = [x["id"] for x in quiz.compose(banque(), CONFIG, graine=43)]
    if a == c:
        return ["deux graines différentes donnent le même quiz"]
    return []


def test_bonne_reponse_stabilite_forcee() -> list[str]:
    """Le bug du pré-mortem : une bonne réponse ne doit pas valoir 2 jours."""
    tmp = profil_jetable()
    err = []
    try:
        res = [quiz.resultat(carte("dr0", "droit"), True)]
        quiz.applique_resultats("test", res, CONFIG, racine_etat=tmp)
        sched = Planificateur(retention=CONFIG["fsrs"]["retention_souhaitee"])
        journal = quiz.lit_journal("test", racine_etat=tmp)
        etats = etats_cartes(journal, sched)
        attendu = CONFIG["quiz"]["stabilite_initiale_jours"]
        mesuree = etats.get("dr0", {}).get("stabilite")
        if mesuree is None:
            err.append("la bonne réponse n'a produit aucun état")
        elif mesuree < attendu:
            err.append(f"stabilité recalculée {mesuree:.1f} j, attendu ≥ {attendu} j")
        ordinaire = sched.premiere(BIEN)[0]
        if mesuree is not None and abs(mesuree - ordinaire) < 1:
            err.append(f"stabilité retombée à celle d'une révision ordinaire "
                       f"({ordinaire:.1f} j) : la stabilité forcée est ignorée")
        if etats.get("dr0", {}).get("du_le", 0) - AUJ.toordinal() < 7:
            err.append("la carte revient dans la semaine : promesse du quiz cassée")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


def test_mauvaise_reponse_n_ecrit_rien() -> list[str]:
    tmp = profil_jetable()
    err = []
    try:
        res = [quiz.resultat(carte("dr0", "droit"), False),
               quiz.resultat(carte("dr1", "droit"), False)]
        lignes = quiz.applique_resultats("test", res, CONFIG, racine_etat=tmp)
        if lignes:
            err.append(f"{len(lignes)} ligne(s) écrite(s) pour des réponses fausses")
        if quiz.lit_journal("test", racine_etat=tmp):
            err.append("le journal porte une trace d'une mauvaise réponse")
        if quiz.chemin_journal("test", racine_etat=tmp).exists():
            err.append("un journal a été créé alors que rien n'était à écrire")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


def test_origine_quiz_marquee() -> list[str]:
    """Sans ce champ, le futur optimiseur FSRS s'entraînerait sur des postulats."""
    tmp = profil_jetable()
    err = []
    try:
        res = [quiz.resultat(carte("dr0", "droit"), True)]
        lignes = quiz.applique_resultats("test", res, CONFIG, racine_etat=tmp)
        for ligne in lignes:
            if ligne.get("origine") != "quiz":
                err.append(f"entrée sans origine quiz : {ligne}")
            if "stabilite_forcee" not in ligne:
                err.append("entrée sans stabilité forcée")
            if ligne.get("domaine") != "droit":
                err.append("entrée sans sa région : le garde-fou ne peut pas jouer")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


def test_quiz_refuse_la_seconde_fois() -> list[str]:
    """Le quiz est un point de départ, il ne se rejoue pas."""
    tmp = profil_jetable()
    err = []
    try:
        res = [quiz.resultat(carte("dr0", "droit"), True)]
        quiz.applique_resultats("test", res, CONFIG, racine_etat=tmp)
        if not quiz.deja_joue("test", "droit", racine_etat=tmp):
            err.append("deja_joue ne voit pas le quiz qui vient d'être passé")
        try:
            quiz.applique_resultats("test", res, CONFIG, racine_etat=tmp)
            err.append("le quiz a été rejoué sans refus")
        except quiz.QuizDejaJoue:
            pass
        # Une autre région reste ouverte au positionnement.
        autre = [quiz.resultat(carte("pa0", "pathologie"), True)]
        try:
            quiz.applique_resultats("test", autre, CONFIG, racine_etat=tmp)
        except quiz.QuizDejaJoue:
            err.append("le refus déborde sur une région jamais positionnée")
        # Et un autre profil n'est pas concerné.
        try:
            quiz.applique_resultats("autre", res, CONFIG, racine_etat=tmp)
        except quiz.QuizDejaJoue:
            err.append("le refus déborde sur un autre profil")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


def test_regions_ouvertes() -> list[str]:
    """Le seuil vient de la config, et le quiz n'ouvre que ce qui est su."""
    seuil = CONFIG["quiz"]["seuil_ouverture_region_quiz"]
    res = ([quiz.resultat(carte(f"dr{i}", "droit"), True) for i in range(5)]
           + [quiz.resultat(carte(f"pa{i}", "pathologie"), i < 2) for i in range(5)])
    ouvertes = quiz.regions_ouvertes(res, CONFIG)
    err = []
    if "droit" not in ouvertes:
        err.append(f"5/5 justes n'ouvre pas la région (seuil {seuil})")
    if "pathologie" in ouvertes:
        err.append(f"2/5 justes ouvre la région (seuil {seuil})")
    if any("remplissage" in str(k) for o in ouvertes for k in [o]):
        err.append("regions_ouvertes rend autre chose que des noms de région")
    return err


def test_quiz_n_ecrit_aucun_remplissage() -> list[str]:
    """Seul FSRS mesure le remplissage : le quiz ne l'écrit jamais."""
    tmp = profil_jetable()
    err = []
    try:
        res = [quiz.resultat(carte(f"dr{i}", "droit"), True) for i in range(3)]
        lignes = quiz.applique_resultats("test", res, CONFIG, racine_etat=tmp)
        interdits = {"remplissage", "xp", "progression", "region_remplie"}
        for ligne in lignes:
            fautes = interdits & set(ligne)
            if fautes:
                err.append(f"le quiz écrit du remplissage : {fautes}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


# --- le carnet d'erreurs ---------------------------------------------

def test_erreur_sans_raison_acceptee() -> list[str]:
    """On peut noter une erreur sans savoir dire pourquoi."""
    tmp = profil_jetable()
    err = []
    try:
        erreurs.note_erreur("test", "dr0", racine_etat=tmp)
        erreurs.note_erreur("test", "dr1", raison="   ", racine_etat=tmp)
        erreurs.note_erreur("test", "dr2", raison="confondu avec la partie privative",
                            racine_etat=tmp)
        carnet = erreurs.lit_carnet("test", racine_etat=tmp)
        if len(carnet) != 3:
            err.append(f"{len(carnet)} erreurs relues, attendu 3")
        if carnet and carnet[0].get("raison") is not None:
            err.append("une erreur sans raison ne rend pas raison = null")
        if not any(e.get("raison") for e in carnet):
            err.append("la raison écrite a été perdue")
        for e in carnet:
            if set(e) != {"quand", "carte", "raison", "mode"}:
                err.append(f"schéma de ligne inattendu : {sorted(e)}")
                break
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


def test_carnet_corrompu_ne_crashe_pas() -> list[str]:
    tmp = profil_jetable()
    err = []
    try:
        erreurs.note_erreur("test", "dr0", raison="lu trop vite", racine_etat=tmp)
        chemin = erreurs.chemin_erreurs("test", racine_etat=tmp)
        with chemin.open("a", encoding="utf-8") as f:
            f.write("{ pas du json\n")
            f.write('{"quand": "2026-08-29T08:00:00+00:00", "raison": "sans carte"}\n')
            f.write("\n")
        erreurs.note_erreur("test", "dr1", racine_etat=tmp)
        try:
            carnet = erreurs.lit_carnet("test", racine_etat=tmp)
        except Exception as exc:                              # noqa: BLE001
            return [f"un carnet corrompu lève : {exc!r}"]
        if len(carnet) != 2:
            err.append(f"{len(carnet)} entrées valides relues, attendu 2")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return err


def test_carnet_absent_rend_une_liste_vide() -> list[str]:
    tmp = profil_jetable()
    try:
        if erreurs.lit_carnet("jamais-vu", racine_etat=tmp) != []:
            return ["un profil sans carnet ne rend pas une liste vide"]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return []


def test_raisons_recurrentes() -> list[str]:
    carnet = [
        {"quand": "2026-08-01T07:00:00+00:00", "carte": "dr0",
         "raison": "confondu avec la partie privative", "mode": "flash"},
        {"quand": "2026-08-05T07:00:00+00:00", "carte": "dr0",
         "raison": "confondu encore avec le lot", "mode": "flash"},
        {"quand": "2026-08-06T07:00:00+00:00", "carte": "pa0",
         "raison": None, "mode": "flash"},
    ]
    agrege = erreurs.raisons_recurrentes(carnet, mini=2)
    err = []
    cartes = [f["carte"] for f in agrege["par_carte"]]
    if cartes != ["dr0"]:
        err.append(f"cartes récurrentes : {cartes}, attendu ['dr0']")
    mots = [b["mot"] for b in agrege["par_mot"]]
    if "confondu" not in mots:
        err.append(f"le mot répété n'est pas remonté : {mots}")
    if "avec" in mots:
        err.append("un mot vide est remonté comme raison récurrente")
    return err


def test_trois_echecs_remontent_deux_non() -> list[str]:
    """La règle des 3 échecs se lit sur les ratés FSRS, pas sur le carnet."""
    journal = ([revue("dr0", RATE, AUJ - timedelta(days=n)) for n in (9, 5, 1)]
               + [revue("pa0", RATE, AUJ - timedelta(days=n)) for n in (7, 2)]
               + [revue("si0", BIEN, AUJ - timedelta(days=3))])
    remontees = erreurs.cartes_a_mini_lecon(journal)
    ids = [f["carte"] for f in remontees]
    err = []
    if ids != ["dr0"]:
        err.append(f"cartes remontées : {ids}, attendu ['dr0'] (3 ratés, pas 2)")
    if remontees and remontees[0]["echecs"] != 3:
        err.append(f"compteur d'échecs {remontees[0]['echecs']}, attendu 3")
    # Le seuil est paramétrable, jamais figé dans le code appelant.
    if [f["carte"] for f in erreurs.cartes_a_mini_lecon(journal, seuil=2)] != ["dr0", "pa0"]:
        err.append("le seuil passé en paramètre n'est pas respecté")
    if [f["carte"] for f in erreurs.cartes_a_mini_lecon(
            journal, config={"erreurs": {"seuil_echecs": 2}})] != ["dr0", "pa0"]:
        err.append("le seuil lu en config n'est pas respecté")
    return err


def test_quiz_ne_compte_pas_comme_echec() -> list[str]:
    """Une entrée de quiz ne peut jamais nourrir la règle des 3 échecs."""
    journal = [{"quand": "2026-08-2%dT07:00:00+00:00" % n, "carte": "dr0",
                "note": RATE, "mode": "quiz", "origine": "quiz"} for n in (1, 2, 3)]
    if erreurs.cartes_a_mini_lecon(journal):
        return ["des entrées origine=quiz alimentent la règle des 3 échecs"]
    return []


def main() -> int:
    tests = [
        ("quiz : aucune carte brouillon servie", test_jamais_de_brouillon),
        ("quiz : les régions sont couvertes", test_couvre_les_regions),
        ("quiz : une région pauvre reste servie", test_couverture_minimale_region_pauvre),
        ("quiz : banque vide sans exception", test_quiz_sans_carte_ne_casse_pas),
        ("quiz : déterministe à graine fixée", test_deterministe),
        ("quiz : bonne réponse = stabilité forcée", test_bonne_reponse_stabilite_forcee),
        ("quiz : mauvaise réponse n'écrit rien", test_mauvaise_reponse_n_ecrit_rien),
        ("quiz : entrées marquées origine=quiz", test_origine_quiz_marquee),
        ("quiz : refusé la seconde fois", test_quiz_refuse_la_seconde_fois),
        ("quiz : régions ouvertes au seuil de config", test_regions_ouvertes),
        ("quiz : aucun remplissage écrit", test_quiz_n_ecrit_aucun_remplissage),
        ("carnet : erreur sans raison acceptée", test_erreur_sans_raison_acceptee),
        ("carnet : ligne corrompue ignorée", test_carnet_corrompu_ne_crashe_pas),
        ("carnet : profil sans carnet", test_carnet_absent_rend_une_liste_vide),
        ("carnet : raisons récurrentes", test_raisons_recurrentes),
        ("règle des 3 échecs : 3 oui, 2 non", test_trois_echecs_remontent_deux_non),
        ("règle des 3 échecs : le quiz n'y entre pas", test_quiz_ne_compte_pas_comme_echec),
    ]
    total = []
    for nom, fn in tests:
        err = fn()
        total += err
        print(f"  {'ok  ' if not err else 'ÉCHEC'} {nom}")
        for e in err:
            print(f"        ✗ {e}")
    if total:
        print(f"\n{len(total)} problème(s).")
        return 1
    print("\nVERT — le quiz de positionnement et le carnet d'erreurs tiennent "
          "leurs promesses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

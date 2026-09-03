#!/usr/bin/env python3
"""Tests de la composition de séance (app/seance.py).

Ce que ces tests protègent, ce sont les promesses faites au BLUEPRINT :
une carte ratée revient vite, une carte sue s'éloigne, l'arriéré se
ré-étale au lieu de s'afficher en dette, les domaines s'entrelacent, et
surtout **une carte non vérifiée ne se joue jamais**.

Les cartes sont fabriquées ici, en mémoire : ces tests ne lisent pas la
vraie banque et n'écrivent nulle part dans le dépôt.

    python3 app/tests_seance.py
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import BIEN, FACILE, RATE, Planificateur  # noqa: E402
from seance import compose, entrelace, etats_cartes, ligne_ouverture  # noqa: E402

import random  # noqa: E402

CONFIG = {"quotas": {"revisions_par_seance": 10, "nouveau_par_seance": 1,
                     "plafond_reprise": 20},
          "fsrs": {"retention_souhaitee": 0.9}}
AUJ = date(2026, 8, 28)

# --- ACA-SEMAINE-1 : la semaine type, le socle, la séance de domaine ---

JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")
LUNDI = date(2026, 8, 31)      # un lundi
MARDI = date(2026, 9, 1)       # un mardi (cours)
DIMANCHE = date(2026, 9, 6)

CONFIG_S = {
    "quotas": {"revisions_par_seance": 10, "nouveau_par_seance": 1,
               "plafond_reprise": 20, "nouveau_par_seance_max": 3,
               "nouveau_par_jour": 20, "ponderation_socle": 0.5,
               "rappels_d_ailleurs_max": 2, "fondations_dues_sans_neuf": 15},
    "fsrs": {"retention_souhaitee": 0.9},
    "semaine_type": {"lundi": "fondations", "mardi": "cours", "mercredi": "terrain",
                     "jeudi": "cours", "vendredi": "exploration",
                     "samedi": "etude", "dimanche": "libre"},
    "socle": {"niveaux": {"droit": 3, "compta": 2}},
    "calendrier_metier": {"9": ["compta"]},
    "domaines": {"droit": {"titre": "Droit", "ordre": 1},
                 "compta": {"titre": "Compta", "ordre": 2}},
    "progression": {"seuil_stabilite_acquise_jours": 21,
                    "seuil_ouverture_region": 0.75,
                    "seuil_fraicheur_jours": 21,
                    "examen_obligatoire_pour_100": True,
                    "examen_nb_cartes": 12, "examen_score_reussite": 0.8},
}

PROGRAMME_S = {
    "branches": {"droit": [{"cle": "b1", "ordre": 1}, {"cle": "b2", "ordre": 2}],
                 "compta": [{"cle": "c1", "ordre": 1}]},
    "chapitres": [
        {"id": "droit.b1.n1", "domaine": "droit", "branche": "b1", "niveau": 1,
         "prerequis": []},
        {"id": "droit.b2.n2", "domaine": "droit", "branche": "b2", "niveau": 1,
         "prerequis": []},
        {"id": "compta.c1.n3", "domaine": "compta", "branche": "c1", "niveau": 1,
         "prerequis": []},
    ],
}


def carte(cid: str, domaine: str = "droit", statut: str = "valide",
          chapitre: str | None = None) -> dict:
    c = {"id": cid, "domaine": domaine, "branche": "b", "type": "flash",
         "question": f"question {cid}", "reponse": "r",
         "source": [{"texte": "s"}], "verifie": "2026-08-28",
         "statut": statut, "partage": "banque"}
    if chapitre:
        c["chapitre"] = chapitre
    return c


def revue(cid: str, note: int, jour: date) -> dict:
    return {"quand": f"{jour.isoformat()}T07:00:00+00:00", "carte": cid,
            "note": note, "mode": "flash"}


def test_brouillon_jamais_joue() -> list[str]:
    """La garantie la plus importante du dispositif."""
    cartes = [carte("valide-1"), carte("brouillon-1", statut="brouillon"),
              carte("signale-1", statut="signale"),
              carte("perime-1", statut="perime")]
    s = compose(cartes, {}, CONFIG, AUJ, Planificateur(), graine=1)
    servis = {c["id"] for c in s["revisions"] + s["nouveau"]}
    if servis - {"valide-1"}:
        return [f"des cartes non valides ont été servies : {servis - {'valide-1'}}"]
    if s["total_jouable"] != 1:
        return [f"total_jouable = {s['total_jouable']}, attendu 1"]
    return []


def test_rate_revient_vite() -> list[str]:
    """Une carte ratée doit revenir avant une carte sue."""
    sched = Planificateur()
    journal = [revue("ratee", RATE, AUJ - timedelta(days=1)),
               revue("sue", FACILE, AUJ - timedelta(days=1))]
    etats = etats_cartes(journal, sched)
    if etats["ratee"]["du_le"] > etats["sue"]["du_le"]:
        return ["la carte ratée revient APRÈS la carte sue"]
    if etats["ratee"]["du_le"] > AUJ.toordinal():
        return ["la carte ratée hier n'est pas due aujourd'hui"]
    return []


def test_rejeu_reproductible() -> list[str]:
    """Rejouer le journal deux fois donne le même état (pas d'état caché)."""
    sched = Planificateur()
    journal = [revue("c1", BIEN, AUJ - timedelta(days=30)),
               revue("c1", BIEN, AUJ - timedelta(days=20)),
               revue("c1", RATE, AUJ - timedelta(days=5))]
    a, b = etats_cartes(journal, sched), etats_cartes(journal, sched)
    if a != b:
        return ["deux rejeux du même journal donnent des états différents"]
    if a["c1"]["revues"] != 3:
        return [f"compteur de revues = {a['c1']['revues']}, attendu 3"]
    return []


def test_plafond_et_reetalement() -> list[str]:
    """L'arriéré se plafonne et se compte, il ne s'affiche pas en entier."""
    sched = Planificateur()
    cartes = [carte(f"c{i}") for i in range(50)]
    journal = [revue(f"c{i}", RATE, AUJ - timedelta(days=40)) for i in range(50)]
    etats = etats_cartes(journal, sched)
    s = compose(cartes, etats, CONFIG, AUJ, sched, graine=1)
    err = []
    if len(s["revisions"]) > CONFIG["quotas"]["plafond_reprise"]:
        err.append(f"{len(s['revisions'])} révisions servies, plafond "
                   f"{CONFIG['quotas']['plafond_reprise']}")
    if s["arriere_reetale"] != 50 - CONFIG["quotas"]["plafond_reprise"]:
        err.append(f"arriéré annoncé {s['arriere_reetale']}, attendu "
                   f"{50 - CONFIG['quotas']['plafond_reprise']}")
    return err


def test_entrelacement() -> list[str]:
    """Deux cartes du même domaine ne doivent pas systématiquement se suivre."""
    cartes = ([carte(f"d{i}", "droit") for i in range(5)]
              + [carte(f"p{i}", "pathologie") for i in range(5)])
    ordre = entrelace(cartes, random.Random(0))
    if len(ordre) != 10:
        return [f"entrelacement a perdu des cartes : {len(ordre)}/10"]
    suites = sum(1 for a, b in zip(ordre, ordre[1:]) if a["domaine"] == b["domaine"])
    if suites > 3:
        return [f"{suites} paires consécutives du même domaine sur 9 : trop bloqué"]
    return []


def test_seance_vide_ne_casse_pas() -> list[str]:
    """Banque vide, journal vide : pas d'exception, une séance vide."""
    try:
        s = compose([], {}, CONFIG, AUJ, Planificateur(), graine=1)
    except Exception as exc:                                  # noqa: BLE001
        return [f"séance vide lève une exception : {exc!r}"]
    return [] if s["revisions"] == [] and s["nouveau"] == [] else ["séance vide non vide"]


def test_journal_corrompu_ignore() -> list[str]:
    """Une ligne de journal incohérente ne doit pas fausser l'état."""
    sched = Planificateur()
    journal = [{"quand": "2026-08-01T07:00:00+00:00", "carte": "c1", "note": 9},
               {"carte": "c1", "note": 3},
               revue("c1", BIEN, AUJ - timedelta(days=2))]
    etats = etats_cartes(journal, sched)
    if etats.get("c1", {}).get("revues") != 1:
        return [f"lignes invalides non ignorées : {etats.get('c1')}"]
    return []


# --- les promesses d'ACA-SEMAINE-1 ------------------------------------

def _compose(cartes, etats=None, jour=MARDI, **kw):
    return compose(cartes, etats or {}, CONFIG_S, jour, Planificateur(),
                   graine=7, programme=PROGRAMME_S, **kw)


def test_lundi_sans_neuf_si_trop_de_dues() -> list[str]:
    """Fondations : plus de quinze dues, aucune carte neuve (BLUEPRINT §4)."""
    dues = [carte(f"d{i}", chapitre="droit.b1.n1") for i in range(20)]
    neuves = [carte(f"n{i}", chapitre="droit.b1.n1") for i in range(5)]
    journal = [revue(f"d{i}", RATE, LUNDI - timedelta(days=40)) for i in range(20)]
    etats = etats_cartes(journal, Planificateur())
    err = []

    s = _compose(dues + neuves, etats, LUNDI)
    if s["jour"] != "fondations":
        err.append(f"jour {s['jour']}, attendu fondations")
    if s["nouveau"]:
        err.append(f"{len(s['nouveau'])} carte(s) neuve(s) un lundi chargé")
    if "fondations" not in " ".join(s["pourquoi"]):
        err.append(f"le pourquoi ne dit pas la raison : {s['pourquoi']}")

    # avec peu de dues, le neuf revient
    peu = [carte("d0", chapitre="droit.b1.n1")]
    etats2 = etats_cartes([revue("d0", RATE, LUNDI - timedelta(days=40))],
                          Planificateur())
    s2 = _compose(peu + neuves, etats2, LUNDI)
    if not s2["nouveau"]:
        err.append("un lundi calme ne sert aucune carte neuve")
    return err


def test_moitie_du_neuf_sur_la_branche_du_socle_la_plus_faible() -> list[str]:
    """La pondération du socle (decisions/0013) : la moitié du neuf y va."""
    # b1 est solide, b2 est vierge : b2 est la branche du socle la plus faible.
    solides = [carte(f"s{i}", chapitre="droit.b1.n1") for i in range(4)]
    faibles = [carte(f"f{i}", chapitre="droit.b2.n2") for i in range(10)]
    ailleurs = [carte(f"a{i}", "compta", chapitre="compta.c1.n3") for i in range(10)]
    # Du neuf HORS de la branche du socle : sans lui, n'importe quel
    # ordre servirait des cartes du socle et le test ne prouverait rien.
    hors_socle = [carte(f"h{i}", chapitre="droit.b1.n1") for i in range(10)]
    # b1 et la branche compta sont acquises ; b2 reste à zéro, c'est donc
    # elle, sans ambiguïté, la branche du socle la moins avancée.
    journal = []
    for cid in [f"s{i}" for i in range(4)] + [f"a{i}" for i in range(10)]:
        journal += [revue(cid, FACILE, MARDI - timedelta(days=60)),
                    revue(cid, FACILE, MARDI - timedelta(days=30))]
    etats = etats_cartes(journal, Planificateur())

    s = _compose(solides + faibles + ailleurs + hors_socle, etats, MARDI)
    neufs = s["nouveau"]
    err = []
    if len(neufs) < 2:
        err.append(f"{len(neufs)} carte(s) neuve(s), il en faut au moins deux pour partager")
        return err
    du_socle = sum(1 for c in neufs if c["id"].startswith("f"))
    if du_socle < len(neufs) // 2:
        err.append(f"{du_socle}/{len(neufs)} du neuf sur la branche faible, "
                   f"attendu au moins la moitié")
    if s["branche_socle"] != "droit.b2":
        err.append(f"branche du socle visée : {s['branche_socle']}, attendu droit.b2")
    return err


def test_domaine_choisi_sert_sans_ponderation() -> list[str]:
    """« Ce matin, compta » : on l'obtient, la pondération se tait (0013)."""
    faibles = [carte(f"f{i}", chapitre="droit.b2.n2") for i in range(10)]
    choisis = [carte(f"c{i}", "compta", chapitre="compta.c1.n3") for i in range(10)]
    s = _compose(faibles + choisis, {}, MARDI, cap="compta")
    err = []
    hors = [c["id"] for c in s["nouveau"] if c["domaine"] != "compta"]
    if hors:
        err.append(f"neuf hors du domaine choisi : {hors}")
    if s["cap"] != "compta":
        err.append(f"cap {s['cap']}, attendu compta")
    if s["branche_socle"] is not None:
        err.append("la pondération du socle n'est pas éteinte par le cap")
    return err


def test_au_plus_deux_rappels_d_ailleurs() -> list[str]:
    """Une séance de domaine glisse au plus deux révisions d'ailleurs (§3)."""
    dus_compta = [carte(f"c{i}", "compta", chapitre="compta.c1.n3") for i in range(5)]
    dus_droit = [carte(f"d{i}", chapitre="droit.b1.n1") for i in range(8)]
    journal = ([revue(f"c{i}", RATE, MARDI - timedelta(days=10)) for i in range(5)]
               + [revue(f"d{i}", RATE, MARDI - timedelta(days=40)) for i in range(8)])
    etats = etats_cartes(journal, Planificateur())

    s = _compose(dus_compta + dus_droit, etats, MARDI, cap="compta")
    err = []
    ailleurs = [c for c in s["revisions"] if c["domaine"] != "compta"]
    if len(ailleurs) > 2:
        err.append(f"{len(ailleurs)} rappels d'ailleurs, deux au plus")
    if len(s["rappels_d_ailleurs"]) != len(ailleurs):
        err.append("les rappels d'ailleurs ne sont pas annoncés")
    if ailleurs and not all(c["id"] in s["rappels_d_ailleurs"] for c in ailleurs):
        err.append("un rappel d'ailleurs n'est pas nommé dans la liste")
    return err


def test_meme_graine_meme_seance() -> list[str]:
    """La graine fixe la séance : deux appels, même ordre, mêmes cartes."""
    cartes = [carte(f"x{i}", "droit" if i % 2 else "compta",
                    chapitre="droit.b1.n1" if i % 2 else "compta.c1.n3")
              for i in range(12)]
    a = _compose(cartes, {}, MARDI)
    b = _compose(cartes, {}, MARDI)
    ids = lambda s: [c["id"] for c in s["revisions"] + s["nouveau"]]   # noqa: E731
    if ids(a) != ids(b):
        return [f"deux compositions à graine fixe diffèrent : {ids(a)} / {ids(b)}"]
    c = compose(cartes, {}, CONFIG_S, MARDI, Planificateur(), graine=99,
                programme=PROGRAMME_S)
    if ids(a) == ids(c) and len(ids(a)) > 3:
        return ["deux graines différentes donnent exactement la même séance"]
    return []


def test_ligne_d_ouverture_complete() -> list[str]:
    """La ligne `mode: seance` porte ce que journal-v1 exige d'elle."""
    cartes = [carte("x1", chapitre="droit.b1.n1")]
    s = _compose(cartes, {}, MARDI, cap="droit")
    ligne = ligne_ouverture(s, banque_version="2026-09-03", moteur_version="1")
    err = []
    for cle in ("quand", "mode", "nonce", "format", "graine",
                "banque_version", "moteur_version", "jour", "cartes"):
        if cle not in ligne:
            err.append(f"la ligne d'ouverture n'a pas `{cle}`")
    if ligne.get("mode") != "seance":
        err.append(f"mode {ligne.get('mode')}, attendu seance")
    if ligne.get("cap") != "droit":
        err.append(f"cap {ligne.get('cap')}, attendu droit")
    if ligne.get("jour") not in ("fondations", "cours", "terrain",
                                 "exploration", "etude", "libre"):
        err.append(f"jour {ligne.get('jour')} hors de l'énumération journal-v1")
    if ligne.get("cartes") != [c["id"] for c in s["revisions"] + s["nouveau"]]:
        err.append("les cartes annoncées ne sont pas celles de la séance")
    if len(str(ligne.get("nonce", ""))) < 8:
        err.append("le nonce fait moins de huit caractères (journal-v1)")
    return err


def test_dimanche_ne_propose_pas_de_neuf() -> list[str]:
    """Libre : les dues restent servies, rien de neuf n'est poussé (§4)."""
    dues = [carte("d1", chapitre="droit.b1.n1")]
    neuves = [carte("n1", chapitre="droit.b1.n1")]
    etats = etats_cartes([revue("d1", RATE, DIMANCHE - timedelta(days=10))],
                         Planificateur())
    s = _compose(dues + neuves, etats, DIMANCHE)
    err = []
    if s["jour"] != "libre":
        err.append(f"jour {s['jour']}, attendu libre")
    if s["nouveau"]:
        err.append("le dimanche pousse du neuf")
    if not s["revisions"]:
        err.append("le dimanche ne sert plus les révisions dues")
    return err


def test_plafond_de_neuf_par_jour() -> list[str]:
    """Vingt cartes neuves dans la journée : la vingt et unième attend."""
    neuves = [carte(f"n{i}", chapitre="droit.b1.n1") for i in range(30)]
    deja = [{"quand": f"{MARDI.isoformat()}T07:0{i % 10}:00+00:00",
             "carte": f"vu{i}", "note": 3, "mode": "revision",
             "origine": "nouveau"} for i in range(20)]
    s = compose(neuves, {}, CONFIG_S, MARDI, Planificateur(), graine=7,
                programme=PROGRAMME_S, journal=deja)
    if s["nouveau"]:
        return [f"{len(s['nouveau'])} carte(s) neuve(s) au-delà du plafond du jour"]
    return []


def test_calendrier_metier_pese_sans_interdire() -> list[str]:
    """En septembre, la compta passe devant ; rien n'est interdit (§4)."""
    droit = [carte(f"d{i}", chapitre="droit.b1.n1") for i in range(10)]
    compta = [carte(f"c{i}", "compta", chapitre="compta.c1.n3") for i in range(10)]
    s = _compose(droit + compta, {}, MARDI, cap=None)
    err = []
    if not s["nouveau"]:
        return ["aucune carte neuve, la scène ne prouve rien"]
    # le calendrier ne peut pas battre la pondération du socle, mais il
    # doit apparaître dans le pourquoi le jour où il pèse.
    if "calendrier" not in " ".join(s["pourquoi"]).lower():
        err.append(f"le calendrier du métier n'est pas dit : {s['pourquoi']}")
    return err


def test_compose_sans_les_nouveautes_reste_compatible() -> list[str]:
    """Sans jour, sans programme, sans cap : la séance d'avant, intacte."""
    cartes = [carte("x1"), carte("x2", "compta")]
    s = compose(cartes, {}, CONFIG, AUJ, Planificateur(), graine=1)
    err = []
    for cle in ("date", "revisions", "nouveau", "arriere_reetale",
                "total_jouable", "jamais_vues"):
        if cle not in s:
            err.append(f"la séance v1 a perdu `{cle}`")
    if s["total_jouable"] != 2:
        err.append(f"total_jouable {s['total_jouable']}, attendu 2")
    return err


def main() -> int:
    tests = [
        ("carte brouillon jamais jouée", test_brouillon_jamais_joue),
        ("une carte ratée revient vite", test_rate_revient_vite),
        ("rejeu du journal reproductible", test_rejeu_reproductible),
        ("plafond et ré-étalement", test_plafond_et_reetalement),
        ("entrelacement des domaines", test_entrelacement),
        ("séance vide sans exception", test_seance_vide_ne_casse_pas),
        ("journal corrompu ignoré", test_journal_corrompu_ignore),
        ("lundi sans neuf si plus de quinze dues",
         test_lundi_sans_neuf_si_trop_de_dues),
        ("moitié du neuf sur la branche du socle la plus faible",
         test_moitie_du_neuf_sur_la_branche_du_socle_la_plus_faible),
        ("domaine choisi servi sans pondération",
         test_domaine_choisi_sert_sans_ponderation),
        ("au plus deux rappels d'ailleurs", test_au_plus_deux_rappels_d_ailleurs),
        ("même graine, même séance", test_meme_graine_meme_seance),
        ("ligne d'ouverture complète", test_ligne_d_ouverture_complete),
        ("dimanche ne pousse pas de neuf", test_dimanche_ne_propose_pas_de_neuf),
        ("plafond de neuf par jour", test_plafond_de_neuf_par_jour),
        ("le calendrier du métier pèse sans interdire",
         test_calendrier_metier_pese_sans_interdire),
        ("la séance d'avant reste intacte",
         test_compose_sans_les_nouveautes_reste_compatible),
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
    print("\nVERT — la composition de séance tient ses promesses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

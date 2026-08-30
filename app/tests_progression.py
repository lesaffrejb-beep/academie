#!/usr/bin/env python3
"""Tests de la carte-monde (app/progression.py).

Ce que ces tests protègent, ce sont les promesses faites au joueur
(SPEC-PRODUIT §3), pas les lignes de code :

  · une région vide ne crashe pas et ne vaut jamais 100 % ;
  · franchir le seuil ouvre la région SUIVANTE, pas la carte entière ;
  · une région fermée reste jouable — le brouillard n'est pas un verrou ;
  · le 100 % n'existe pas sans son boss, et le boss le donne ;
  · la Culture (tronc commun) ne participe pas à la conquête ;
  · l'examen se rejoue à l'identique et ne sert jamais une carte non vérifiée ;
  · l'XP se recalcule, elle ne se stocke pas : deux appels, même nombre.

Les cartes, la config et le journal sont fabriqués ici, en mémoire : ces
tests ne lisent ni la vraie banque ni un profil, et n'écrivent nulle part.

    python3 app/tests_progression.py
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import BIEN, FACILE, Planificateur  # noqa: E402
from progression import (  # noqa: E402
    carte_monde, compose_examen, examens_reussis, plafonne,
    regions_ordonnees, remplissage_brut, xp_affichee,
)
from seance import etats_cartes  # noqa: E402

AUJ = date(2026, 8, 28)

CONFIG = {
    "domaines": {
        "r1": {"titre": "Région une", "ordre": 1},
        "r2": {"titre": "Région deux", "ordre": 2},
        "r3": {"titre": "Région trois", "ordre": 3},
        "culture": {"titre": "Culture", "ordre": 9, "arbre": False},
    },
    "fsrs": {"retention_souhaitee": 0.9},
    "progression": {
        "seuil_stabilite_acquise_jours": 21,
        "seuil_ouverture_region": 0.75,
        "examen_obligatoire_pour_100": True,
        "examen_nb_cartes": 12,
        "examen_score_reussite": 0.8,
    },
}


def carte(cid: str, domaine: str = "r1", statut: str = "valide") -> dict:
    return {"id": cid, "domaine": domaine, "branche": "b", "type": "flash",
            "question": f"question {cid}", "reponse": "r",
            "source": [{"texte": "s"}], "verifie": "2026-08-28",
            "statut": statut, "partage": "banque"}


def revue(cid: str, note: int, jour: date) -> dict:
    return {"quand": f"{jour.isoformat()}T07:00:00+00:00", "carte": cid,
            "note": note, "mode": "flash"}


def acquise(cid: str) -> list[dict]:
    """Deux « facile » espacés d'un mois : stabilité largement au-dessus du seuil."""
    return [revue(cid, FACILE, AUJ - timedelta(days=60)),
            revue(cid, FACILE, AUJ - timedelta(days=30))]


def fraiche(cid: str) -> list[dict]:
    """Vue une fois, bien : la carte existe, elle n'est pas acquise."""
    return [revue(cid, BIEN, AUJ - timedelta(days=3))]


def examen(region: str, score: float, jour: date = AUJ) -> dict:
    """Le contrat d'entrée de journal d'un examen (progression.py, docstring)."""
    return {"quand": f"{jour.isoformat()}T07:30:00+00:00", "mode": "examen",
            "region": region, "score": score, "cartes": []}


# --- les promesses ----------------------------------------------------

def test_region_vide_vaut_zero() -> list[str]:
    """Aucune carte dans la région : 0 %, pas une division par zéro."""
    try:
        val = remplissage_brut([], {}, "r1", CONFIG)
    except Exception as exc:                                   # noqa: BLE001
        return [f"région vide lève une exception : {exc!r}"]
    if val != 0.0:
        return [f"région vide = {val}, attendu 0.0"]
    monde = carte_monde([], [], CONFIG)
    vides = [r for r in monde["regions"] if r["remplissage"] != 0.0]
    if vides:
        return [f"régions vides non nulles : {[r['cle'] for r in vides]}"]
    if monde["remplissage_global"] != 0.0:
        return [f"remplissage global {monde['remplissage_global']}, attendu 0.0"]
    return []


def test_seuil_ouvre_la_suivante_seulement() -> list[str]:
    """Conquérir r1 ouvre r2. Pas r3 : le brouillard se lève d'un cran."""
    cartes = [carte("a1", "r1"), carte("a2", "r1"),
              carte("b1", "r2"), carte("c1", "r3")]
    journal = acquise("a1") + acquise("a2")          # r1 à 100 % mesuré
    monde = carte_monde(cartes, journal, CONFIG)
    ouvertes = {r["cle"]: r["ouverte"] for r in monde["regions"]}
    err = []
    if not ouvertes.get("r1"):
        err.append("la première région n'est pas ouverte")
    if not ouvertes.get("r2"):
        err.append("r1 pleine n'a pas ouvert r2")
    if ouvertes.get("r3"):
        err.append("r3 s'est ouverte alors que r2 est à 0 %")
    return err


def test_sous_le_seuil_n_ouvre_pas() -> list[str]:
    """Une région à moins du seuil n'ouvre pas la suivante (et le quiz, si)."""
    cartes = [carte(f"a{i}", "r1") for i in range(4)] + [carte("b1", "r2")]
    journal = acquise("a0")                          # 1/4 = 25 %, sous 75 %
    monde = carte_monde(cartes, journal, CONFIG)
    r2 = next(r for r in monde["regions"] if r["cle"] == "r2")
    if r2["ouverte"]:
        return ["r2 ouverte alors que r1 est à 25 %"]
    force = carte_monde(cartes, journal, CONFIG, regions_ouvertes=["r2"])
    r2f = next(r for r in force["regions"] if r["cle"] == "r2")
    if not r2f["ouverte"] or r2f["ouverte_par"] != "quiz":
        return [f"le déblocage par quiz n'ouvre pas r2 : {r2f['ouverte_par']!r}"]
    return []


def test_region_fermee_reste_explorable() -> list[str]:
    """Le moteur n'interdit rien : fermée = brouillard, pas verrou."""
    cartes = [carte("a1", "r1"), carte("b1", "r2"), carte("c1", "r3")]
    monde = carte_monde(cartes, [], CONFIG)
    fermees = [r for r in monde["regions"] if not r["ouverte"]]
    if not fermees:
        return ["aucune région fermée : le cas n'est pas testé"]
    err = [f"région fermée non explorable : {r['cle']}"
           for r in fermees if not r["explorable"]]
    err += [f"statut inattendu pour {r['cle']} : {r['statut']!r}"
            for r in fermees if r["statut"] != "explorable"]
    # Et le tirage d'examen d'une région fermée doit marcher : on a le
    # droit d'aller se frotter au boss d'une région lointaine.
    if not compose_examen(cartes, "r3", CONFIG, graine=1):
        err.append("impossible de composer l'examen d'une région fermée")
    return err


def test_plafond_99_sans_examen() -> list[str]:
    """Tout est su, le boss n'est pas tombé : 99 %, jamais 100 %."""
    cartes = [carte("a1", "r1"), carte("a2", "r1")]
    journal = acquise("a1") + acquise("a2")
    monde = carte_monde(cartes, journal, CONFIG)
    r1 = next(r for r in monde["regions"] if r["cle"] == "r1")
    err = []
    if r1["remplissage_mesure"] != 1.0:
        err.append(f"mesure = {r1['remplissage_mesure']}, attendu 1.0")
    if r1["remplissage"] > 0.99:
        err.append(f"remplissage affiché {r1['remplissage']} > 0.99 sans examen")
    if r1["conquise"]:
        err.append("région annoncée conquise sans son examen")
    if not r1["plafonnee_faute_d_examen"]:
        err.append("le plafonnement n'est pas signalé au front")
    # Et si la config n'exige pas d'examen, le 100 % passe.
    libre = json.loads(json.dumps(CONFIG))
    libre["progression"]["examen_obligatoire_pour_100"] = False
    if plafonne(1.0, False, libre) != 1.0:
        err.append("examen non obligatoire : le 100 % est plafonné quand même")
    return err


def test_examen_reussi_debloque_le_100() -> list[str]:
    """Le boss tombé rend le 100 % accessible ; un échec ne donne rien."""
    cartes = [carte("a1", "r1"), carte("a2", "r1")]
    su = acquise("a1") + acquise("a2")
    reussi = CONFIG["progression"]["examen_score_reussite"]

    rate = carte_monde(cartes, su + [examen("r1", reussi - 0.1)], CONFIG)
    r1_rate = next(r for r in rate["regions"] if r["cle"] == "r1")
    gagne = carte_monde(cartes, su + [examen("r1", reussi)], CONFIG)
    r1_gagne = next(r for r in gagne["regions"] if r["cle"] == "r1")

    err = []
    if r1_rate["remplissage"] > 0.99 or r1_rate["examen_reussi"]:
        err.append("un examen raté a débloqué le 100 %")
    if r1_gagne["remplissage"] != 1.0 or not r1_gagne["conquise"]:
        err.append(f"examen réussi mais remplissage {r1_gagne['remplissage']}")
    if "r1" not in gagne["regions_conquises"]:
        err.append("région conquise absente de la synthèse")
    # Une révision faite pendant l'examen (carte + note) n'est pas un
    # résultat d'examen : elle ne doit jamais valoir boss tombé.
    piege = [dict(revue("a1", FACILE, AUJ), mode="examen", region="r1", score=1.0)]
    if examens_reussis(su + piege, CONFIG):
        err.append("une révision étiquetée « examen » compte comme boss tombé")
    return err


def test_culture_hors_carte_monde() -> list[str]:
    """`arbre: false` : ni ordre d'ouverture, ni remplissage global."""
    cartes = [carte("a1", "r1"), carte("k1", "culture"), carte("k2", "culture")]
    journal = acquise("k1") + acquise("k2")     # Culture pleine, r1 vide
    ordre = [cle for cle, _ in regions_ordonnees(CONFIG)]
    err = []
    if "culture" in ordre:
        err.append(f"culture présente dans l'ordre d'ouverture : {ordre}")
    monde = carte_monde(cartes, journal, CONFIG)
    if any(r["cle"] == "culture" for r in monde["regions"]):
        err.append("culture comptée comme région de la carte-monde")
    if monde["remplissage_global"] != 0.0:
        err.append(f"culture pleine gonfle le global : {monde['remplissage_global']}")
    hors = [r["cle"] for r in monde["hors_carte"]]
    if hors != ["culture"]:
        err.append(f"culture absente du hors-carte : {hors}")
    return err


def test_tirage_examen_deterministe_et_propre() -> list[str]:
    """Même graine, même épreuve — et jamais une carte non vérifiée."""
    cartes = ([carte(f"a{i}", "r1") for i in range(20)]
              + [carte("brouillon-1", "r1", statut="brouillon"),
                 carte("signale-1", "r1", statut="signale"),
                 carte("perime-1", "r1", statut="perime"),
                 carte("autre", "r2")])
    a = [c["id"] for c in compose_examen(cartes, "r1", CONFIG, graine=7)]
    b = [c["id"] for c in compose_examen(cartes, "r1", CONFIG, graine=7)]
    err = []
    if a != b:
        err.append("deux tirages à graine fixée diffèrent")
    if len(a) != CONFIG["progression"]["examen_nb_cartes"]:
        err.append(f"{len(a)} cartes tirées, attendu "
                   f"{CONFIG['progression']['examen_nb_cartes']}")
    interdites = {"brouillon-1", "signale-1", "perime-1", "autre"}
    if interdites & set(a):
        err.append(f"cartes interdites servies à l'examen : {interdites & set(a)}")
    if len(set(a)) != len(a):
        err.append("le tirage sert deux fois la même carte")
    # Une région trop maigre rend ce qu'elle a, sans lever d'exception.
    maigre = compose_examen([carte("seule", "r3")], "r3", CONFIG, graine=1)
    if len(maigre) != 1:
        err.append(f"région maigre : {len(maigre)} carte(s), attendu 1")
    return err


def test_xp_pure_et_derivee() -> list[str]:
    """L'XP se recalcule : deux appels, même nombre, aucun stockage."""
    cartes = [carte("a1", "r1"), carte("a2", "r1")]
    journal = acquise("a1") + acquise("a2") + fraiche("a3")
    monde = carte_monde(cartes, journal, CONFIG)
    remplissages = {r["cle"]: r["remplissage"] for r in monde["regions"]}
    a = xp_affichee(journal, remplissages, CONFIG)
    b = xp_affichee(journal, remplissages, CONFIG)
    err = []
    if a != b:
        err.append(f"deux appels donnent {a} puis {b}")
    if a != carte_monde(cartes, journal, CONFIG)["xp"]:
        err.append("l'XP de la carte-monde ne suit pas la fonction")
    if xp_affichee([], {}, CONFIG) != 0:
        err.append("journal vide : l'XP n'est pas nulle")
    # Une révision de plus fait monter l'XP : elle dérive bien du journal.
    if xp_affichee(journal + fraiche("a4"), remplissages, CONFIG) <= a:
        err.append("une révision réussie de plus ne fait pas monter l'XP")
    # Et un examen réussi aussi.
    reussi = CONFIG["progression"]["examen_score_reussite"]
    if xp_affichee(journal + [examen("r1", reussi)], remplissages, CONFIG) <= a:
        err.append("un examen réussi ne fait pas monter l'XP")
    return err


def test_synthese_serialisable() -> list[str]:
    """Le front reçoit du JSON, pas des objets Python."""
    cartes = [carte("a1", "r1"), carte("k1", "culture")]
    monde = carte_monde(cartes, acquise("a1"), CONFIG, regions_ouvertes=["r3"])
    try:
        json.dumps(monde, ensure_ascii=False)
    except TypeError as exc:
        return [f"carte-monde non sérialisable : {exc}"]
    return []


def test_seuil_vient_de_la_config() -> list[str]:
    """Aucun seuil en dur : bouger la config bouge la carte."""
    cartes = [carte("a1", "r1")]
    journal = fraiche("a1")                       # stabilité ~2,3 jours
    etats = etats_cartes(journal, Planificateur())
    souple = json.loads(json.dumps(CONFIG))
    souple["progression"]["seuil_stabilite_acquise_jours"] = 1
    err = []
    if remplissage_brut(cartes, etats, "r1", CONFIG) != 0.0:
        err.append("carte fraîche comptée acquise au seuil de 21 jours")
    if remplissage_brut(cartes, etats, "r1", souple) != 1.0:
        err.append("le seuil abaissé n'est pas pris en compte")
    incomplete = {"domaines": CONFIG["domaines"], "progression": {}}
    try:
        remplissage_brut(cartes, etats, "r1", incomplete)
    except KeyError:
        pass
    else:
        err.append("config `progression` vide : le module a deviné un seuil")
    return err


def main() -> int:
    tests = [
        ("région sans carte vaut 0", test_region_vide_vaut_zero),
        ("le seuil ouvre la suivante, pas celle d'après",
         test_seuil_ouvre_la_suivante_seulement),
        ("sous le seuil, seul le quiz ouvre", test_sous_le_seuil_n_ouvre_pas),
        ("région fermée reste explorable", test_region_fermee_reste_explorable),
        ("plafond 99 % sans examen", test_plafond_99_sans_examen),
        ("examen réussi débloque le 100 %", test_examen_reussi_debloque_le_100),
        ("culture hors carte-monde", test_culture_hors_carte_monde),
        ("tirage d'examen déterministe et propre",
         test_tirage_examen_deterministe_et_propre),
        ("XP dérivée et pure", test_xp_pure_et_derivee),
        ("synthèse sérialisable pour le front", test_synthese_serialisable),
        ("les seuils viennent de la config", test_seuil_vient_de_la_config),
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
    print("\nVERT — la carte-monde tient ses promesses.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

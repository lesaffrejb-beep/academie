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
from seance import compose, entrelace, etats_cartes  # noqa: E402

import random  # noqa: E402

CONFIG = {"quotas": {"revisions_par_seance": 10, "nouveau_par_seance": 1,
                     "plafond_reprise": 20},
          "fsrs": {"retention_souhaitee": 0.9}}
AUJ = date(2026, 8, 28)


def carte(cid: str, domaine: str = "droit", statut: str = "valide") -> dict:
    return {"id": cid, "domaine": domaine, "branche": "b", "type": "flash",
            "question": f"question {cid}", "reponse": "r",
            "source": [{"texte": "s"}], "verifie": "2026-08-28",
            "statut": statut, "partage": "banque"}


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


def main() -> int:
    tests = [
        ("carte brouillon jamais jouée", test_brouillon_jamais_joue),
        ("une carte ratée revient vite", test_rate_revient_vite),
        ("rejeu du journal reproductible", test_rejeu_reproductible),
        ("plafond et ré-étalement", test_plafond_et_reetalement),
        ("entrelacement des domaines", test_entrelacement),
        ("séance vide sans exception", test_seance_vide_ne_casse_pas),
        ("journal corrompu ignoré", test_journal_corrompu_ignore),
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

#!/usr/bin/env python3
"""Non-régression du portage FSRS-6 (app/planificateur.py).

Deux niveaux :

1. **Toujours** : les valeurs de référence figées ci-dessous, produites
   par `py-fsrs` le 28/08/2026 sur des séquences de révision réelles.
   Elles tournent sans aucune dépendance, donc dans la routine du matin
   comme en CI.
2. **Si `py-fsrs` est installé** (`pip install fsrs`) : comparaison
   directe, carte par carte, contre l'implémentation de référence. C'est
   ce mode qui a produit les valeurs figées.

    python3 app/tests_fsrs.py

Sortie : 0 si tout passe, 1 sinon.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import BIEN, DUR, FACILE, RATE, Planificateur  # noqa: E402

TOLERANCE = 1e-9

# Séquences (note, jours écoulés depuis la révision précédente).
SEQUENCES = [
    [(BIEN, 0), (BIEN, 3), (BIEN, 8), (BIEN, 21)],           # parcours nominal
    [(RATE, 0), (BIEN, 1), (RATE, 4), (BIEN, 2), (BIEN, 6)],  # deux oublis
    [(FACILE, 0), (FACILE, 15), (DUR, 40)],                   # facile puis dur
    [(DUR, 0), (DUR, 2), (BIEN, 5), (FACILE, 12)],            # départ difficile
    [(BIEN, 0), (BIEN, 0), (BIEN, 0)],                        # tout le même jour
    [(BIEN, 0), (RATE, 365)],                                 # oubli après un an
]

# Valeurs PRODUITES par py-fsrs le 28/08/2026 (paramètres et rétention
# par défaut), jamais écrites à la main : elles sortent de
# `Scheduler(enable_fuzzing=False).review_card()`.
# Format : [(stabilité, difficulté, intervalle), ...]
ATTENDU = [
    [(2.3065, 2.1181, 2), (13.8269, 2.1112, 14), (42.063, 2.1043, 42), (105.451, 2.0975, 105)],
    [(0.212, 6.4133, 1), (1.8868, 6.4021, 2), (0.5531, 8.8026, 1), (2.1255, 8.7891, 2), (6.4005, 8.7755, 6)],
    [(8.2956, 1.0, 8), (95.5078, 1.0, 96), (168.869, 4.0106, 169)],
    [(1.2931, 5.1122, 1), (4.4695, 6.7405, 4), (13.1201, 6.7289, 13), (47.6466, 5.6211, 48)],
    [(2.3065, 2.1181, 2), (2.3065, 2.1112, 2), (2.3065, 2.1043, 2)],
    [(2.3065, 2.1181, 2), (1.2768, 7.3945, 1)],
]


def joue(sched: Planificateur, sequence):
    """Déroule une séquence et rend [(stabilité, difficulté, intervalle), ...]."""
    etats, s, d = [], None, None
    for note, jours in sequence:
        if s is None:
            s, d = sched.premiere(note)
        else:
            s, d = sched.revise(s, d, note, jours)
        etats.append((s, d, sched.intervalle(s)))
    return etats


def compare(obtenu, attendu, label, tol=TOLERANCE):
    erreurs = []
    if len(obtenu) != len(attendu):
        return [f"{label} : {len(obtenu)} état(s) contre {len(attendu)} attendu(s)"]
    for i, ((s1, d1, i1), (s2, d2, i2)) in enumerate(zip(obtenu, attendu)):
        if abs(s1 - s2) > tol:
            erreurs.append(f"{label}[{i}] stabilité {s1:.6f} != {s2:.6f}")
        if abs(d1 - d2) > tol:
            erreurs.append(f"{label}[{i}] difficulté {d1:.6f} != {d2:.6f}")
        if i1 != i2:
            erreurs.append(f"{label}[{i}] intervalle {i1} != {i2}")
    return erreurs


def test_valeurs_figees() -> list[str]:
    sched = Planificateur()
    erreurs = []
    for n, (seq, attendu) in enumerate(zip(SEQUENCES, ATTENDU)):
        obtenu = [(round(s, 4), round(d, 4), i) for s, d, i in joue(sched, seq)]
        erreurs += compare(obtenu, [tuple(x) for x in attendu], f"séq{n}", tol=5e-5)
    return erreurs


# Le vecteur de conformité que TOUTES les implémentations FSRS partagent
# (py-fsrs, ts-fsrs, go-fsrs, swift-fsrs, dart-fsrs) : c'est lui qui
# prouve l'accord avec le reste du monde, là où les valeurs figées plus
# haut ne prouvent que l'accord avec une exécution locale.
#
# Nuance importante : le vecteur publié partout vaut AVEC les paliers
# d'apprentissage d'Anki (1 min, 10 min), qui produisent les zéros de
# [0, 2, 11, 46, 163, 498, 0, 0, 2, 4, 7, 12, 21]. Notre portage
# n'implémente PAS ces paliers — il fait du FSRS long terme pur, ce qui
# est le besoin d'une séance quotidienne. Le vecteur ci-dessous est donc
# celui de `Scheduler(learning_steps=(), relearning_steps=())`, produit
# le 28/08/2026. Si un jour on ajoute les paliers, c'est le vecteur
# canonique complet qu'il faudra viser.
NOTES_CONFORMITE = [3, 3, 3, 3, 3, 3, 1, 1, 3, 3, 3, 3, 3]
INTERVALLES_CONFORMITE = [2, 11, 46, 163, 497, 1346, 9, 1, 2, 4, 7, 13, 22]


def test_vecteur_de_conformite() -> list[str]:
    """Accord avec l'écosystème FSRS, pas seulement avec nous-mêmes."""
    sched = Planificateur()
    s = d = None
    obtenus, ecoules = [], 0
    for note in NOTES_CONFORMITE:
        if s is None:
            s, d = sched.premiere(note)
        else:
            s, d = sched.revise(s, d, note, ecoules)
        ecoules = sched.intervalle(s)
        obtenus.append(ecoules)
    if obtenus != INTERVALLES_CONFORMITE:
        return [f"vecteur de conformité : {obtenus} != {INTERVALLES_CONFORMITE}"]
    return []


def test_invariants() -> list[str]:
    """Ce qui doit tenir quels que soient les paramètres."""
    sched = Planificateur()
    err = []

    # R décroît avec le temps, et vaut la rétention visée à l'échéance.
    s, _ = sched.premiere(BIEN)
    r = [sched.recuperabilite(s, j) for j in (0, 1, 5, 30)]
    if not all(a >= b for a, b in zip(r, r[1:])):
        err.append(f"récupérabilité non décroissante : {r}")
    if abs(sched.recuperabilite(s, sched.intervalle(s)) - sched.retention) > 0.05:
        err.append("à l'échéance, R devrait valoir la rétention souhaitée")

    # Un raté ne doit jamais allonger l'intervalle.
    s0, d0 = sched.premiere(BIEN)
    s1, _ = sched.revise(s0, d0, BIEN, 5)
    s2, _ = sched.revise(s0, d0, RATE, 5)
    if sched.intervalle(s2) > sched.intervalle(s1):
        err.append("un raté allonge l'intervalle")

    # Facile ≥ bien ≥ dur, à situation égale.
    inter = [sched.intervalle(sched.revise(s0, d0, n, 5)[0]) for n in (DUR, BIEN, FACILE)]
    if not inter[0] <= inter[1] <= inter[2]:
        err.append(f"intervalles non monotones dur/bien/facile : {inter}")

    # La difficulté reste dans ses bornes, même sous 30 ratés d'affilée.
    s, d = sched.premiere(RATE)
    for _ in range(30):
        s, d = sched.revise(s, d, RATE, 1)
    if not 1.0 <= d <= 10.0:
        err.append(f"difficulté hors bornes après 30 ratés : {d}")
    if s < 0:
        err.append(f"stabilité négative : {s}")

    # Une note inconnue doit lever, pas produire une carte silencieusement fausse.
    try:
        sched.premiere(7)
        err.append("note 7 acceptée sans erreur")
    except ValueError:
        pass
    return err


def test_contre_reference() -> tuple[list[str], bool]:
    """Comparaison directe à py-fsrs, si la bibliothèque est installée."""
    try:
        from datetime import datetime, timedelta, timezone

        from fsrs import Card, Rating, Scheduler
    except ImportError:
        return [], False

    ref, mien, erreurs = Scheduler(enable_fuzzing=False), Planificateur(), []
    for n, seq in enumerate(SEQUENCES):
        carte, quand = Card(), datetime(2026, 8, 28, 7, 0, tzinfo=timezone.utc)
        attendu = []
        for note, jours in seq:
            quand += timedelta(days=jours)
            carte, _ = ref.review_card(carte, Rating(note), quand)
            attendu.append((round(carte.stability, 4), round(carte.difficulty, 4),
                            ref._next_interval(stability=carte.stability)))
        obtenu = [(round(s, 4), round(d, 4), i) for s, d, i in joue(mien, seq)]
        erreurs += compare(obtenu, attendu, f"réf-séq{n}", tol=5e-5)
    return erreurs, True


def main() -> int:
    erreurs = test_valeurs_figees()
    print(f"valeurs figées   : {'ok' if not erreurs else str(len(erreurs)) + ' écart(s)'}")

    conf = test_vecteur_de_conformite()
    erreurs += conf
    print(f"vecteur FSRS     : {'ok' if not conf else 'ÉCART avec l-ecosysteme'}")

    inv = test_invariants()
    erreurs += inv
    print(f"invariants       : {'ok' if not inv else str(len(inv)) + ' violation(s)'}")

    ref_err, dispo = test_contre_reference()
    erreurs += ref_err
    if dispo:
        print(f"contre py-fsrs   : {'ok' if not ref_err else str(len(ref_err)) + ' écart(s)'}")
    else:
        print("contre py-fsrs   : ignoré (pip install fsrs pour l'activer)")

    if erreurs:
        print(f"\n{len(erreurs)} problème(s) :")
        for e in erreurs[:20]:
            print(f"  ✗ {e}")
        return 1
    print("\nVERT — le portage FSRS est conforme.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

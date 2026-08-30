#!/usr/bin/env python3
"""FSRS-6 — planificateur de répétition espacée, portage stdlib.

Pourquoi un portage plutôt que la dépendance `py-fsrs` (arbitrage
ouvert au BLUEPRINT §8, tranché ici le 28/08/2026) : la séance du matin
est générée par une routine cloud puis servie par le VPS, et le socle
du repo tourne stdlib seule. Une dépendance de plus, c'est un maillon
de plus qui peut manquer à 7 h du matin — pour ~120 lignes de formules
publiées, le portage est le choix robuste.

Les formules et les 21 paramètres par défaut ne sont PAS écrits de
mémoire : ils sont repris de l'implémentation de référence `py-fsrs`
(open-spaced-repetition), lue le 28/08/2026, et `tests_fsrs.py` compare
ce module à cette référence sur des séquences de révision réelles. Si
les deux divergent, c'est ce module qui a tort.

Vocabulaire (BLUEPRINT §8) :
  - stabilité S : nombre de jours au bout desquels la mémoire de la
    carte retombe à la rétention souhaitée ;
  - difficulté D (1 à 10) : ce que la carte coûte à retenir ;
  - récupérabilité R : probabilité de se rappeler, maintenant.

Les quatre notes sont celles d'Anki : 1 raté, 2 dur, 3 bien, 4 facile.
"""

from __future__ import annotations

import math

# Paramètres FSRS-6 par défaut (py-fsrs, 28/08/2026). L'optimiseur
# personnalisé demande ~400 revues (doc Anki 24.04+, CORPUS §3) : tant
# que le journal ne les porte pas, ces défauts sont déjà au-dessus de
# SM-2 pour ~99,6 % des utilisateurs du benchmark.
PARAMS_DEFAUT = (
    0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001,
    1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014,
    1.8729, 0.5425, 0.0912, 0.0658, 0.1542,
)

RETENTION_DEFAUT = 0.9          # défaut Anki ; plage utile 0,80-0,95
INTERVALLE_MAX = 36500          # 100 ans, la borne de py-fsrs
STABILITE_MIN = 0.001
DIFFICULTE_MIN, DIFFICULTE_MAX = 1.0, 10.0

RATE, DUR, BIEN, FACILE = 1, 2, 3, 4


class Planificateur:
    """Le moteur de révision. Sans état : on lui passe une carte, il rend la suivante."""

    def __init__(self, params=PARAMS_DEFAUT, retention=RETENTION_DEFAUT,
                 intervalle_max=INTERVALLE_MAX):
        if len(params) != 21:
            raise ValueError(f"FSRS-6 attend 21 paramètres, reçu {len(params)}")
        if not 0.7 <= retention <= 0.99:
            raise ValueError("rétention souhaitée hors bornes (0,70-0,99)")
        self.p = tuple(params)
        self.retention = retention
        self.intervalle_max = intervalle_max
        self._decay = -self.p[20]
        self._factor = 0.9 ** (1 / self._decay) - 1

    # --- lecture -----------------------------------------------------
    def recuperabilite(self, stabilite: float, jours_ecoules: float) -> float:
        """R : probabilité de se rappeler après `jours_ecoules`."""
        if stabilite <= 0:
            return 0.0
        return (1 + self._factor * jours_ecoules / stabilite) ** self._decay

    def intervalle(self, stabilite: float) -> int:
        """Jours jusqu'à la prochaine révision, pour la rétention visée."""
        brut = (stabilite / self._factor) * (
            self.retention ** (1 / self._decay) - 1)
        return max(1, min(round(brut), self.intervalle_max))

    # --- première rencontre ------------------------------------------
    def premiere(self, note: int) -> tuple[float, float]:
        """(stabilité, difficulté) après la toute première réponse."""
        self._verifie_note(note)
        return (self._clamp_s(self.p[note - 1]),
                self._clamp_d(self._difficulte_initiale(note)))

    # --- révisions suivantes -----------------------------------------
    def revise(self, stabilite: float, difficulte: float, note: int,
               jours_ecoules: float) -> tuple[float, float]:
        """(stabilité, difficulté) après une révision.

        `jours_ecoules` = 0 signifie une reprise le jour même (la carte
        ratée qu'on rejoue en fin de séance) : FSRS la traite à part,
        avec la formule court terme.
        """
        self._verifie_note(note)
        d = self._clamp_d(self._difficulte_suivante(difficulte, note))
        if jours_ecoules <= 0:
            return self._clamp_s(self._stabilite_court_terme(stabilite, note)), d
        r = self.recuperabilite(stabilite, jours_ecoules)
        if note == RATE:
            s = self._stabilite_apres_oubli(difficulte, stabilite, r)
        else:
            s = self._stabilite_apres_rappel(difficulte, stabilite, r, note)
        return self._clamp_s(s), d

    # --- formules (référence : py-fsrs, lue le 28/08/2026) ------------
    def _difficulte_initiale(self, note: int) -> float:
        return self.p[4] - math.e ** (self.p[5] * (note - 1)) + 1

    def _difficulte_suivante(self, d: float, note: int) -> float:
        delta = -(self.p[6] * (note - 3))
        amorti = d + (10.0 - d) * delta / 9.0          # amortissement linéaire
        cible = self._difficulte_initiale(FACILE)       # non bornée, comme la réf.
        return self.p[7] * cible + (1 - self.p[7]) * amorti   # retour à la moyenne

    def _stabilite_court_terme(self, s: float, note: int) -> float:
        hausse = (math.e ** (self.p[17] * (note - 3 + self.p[18]))) * (s ** -self.p[19])
        if note in (DUR, BIEN, FACILE):
            hausse = max(hausse, 1.0)      # une bonne réponse ne fait jamais reculer
        return s * hausse

    def _stabilite_apres_rappel(self, d: float, s: float, r: float, note: int) -> float:
        penalite_dur = self.p[15] if note == DUR else 1
        bonus_facile = self.p[16] if note == FACILE else 1
        return s * (1 + math.e ** self.p[8]
                    * (11 - d)
                    * (s ** -self.p[9])
                    * (math.e ** ((1 - r) * self.p[10]) - 1)
                    * penalite_dur * bonus_facile)

    def _stabilite_apres_oubli(self, d: float, s: float, r: float) -> float:
        long_terme = (self.p[11]
                      * (d ** -self.p[12])
                      * ((s + 1) ** self.p[13] - 1)
                      * math.e ** ((1 - r) * self.p[14]))
        # Un oubli ne peut pas rendre la carte plus solide qu'une reprise
        # le jour même : c'est le plafond que FSRS-5+ a ajouté.
        court_terme = s / (math.e ** (self.p[17] * self.p[18]))
        return min(long_terme, court_terme)

    # --- garde-fous ---------------------------------------------------
    @staticmethod
    def _verifie_note(note: int) -> None:
        if note not in (RATE, DUR, BIEN, FACILE):
            raise ValueError(f"note {note!r} inconnue : 1 raté, 2 dur, 3 bien, 4 facile")

    @staticmethod
    def _clamp_s(s: float) -> float:
        return max(s, STABILITE_MIN)

    @staticmethod
    def _clamp_d(d: float) -> float:
        return min(max(d, DIFFICULTE_MIN), DIFFICULTE_MAX)

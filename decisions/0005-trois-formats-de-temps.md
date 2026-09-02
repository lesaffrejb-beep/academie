# 0005, Trois formats de temps

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« 15-20 minutes le matin, mais il faut aussi qu'on puisse
  passer une demi-journée, une journée »)

## Décision

Le produit connaît trois formats, et les propose selon le temps que le
joueur déclare avoir :

| Format | Durée | Ce qui s'y passe | Appareil |
|---|---|---|---|
| **Séance** | 8 à 20 min | révisions dues (FSRS, plafond de reprise), 1 à 3 nouveautés, clôture. S'arrêter tôt reste honorable | téléphone d'abord |
| **Étude** | 45 à 90 min | un chapitre de bout en bout : amorce, leçon, exercices, synthèse ; les cartes extraites entrent en rotation | téléphone ou ordinateur |
| **Journée** | 3 à 7 h | un programme de 3 à 6 études, entrelacé sur 2 ou 3 domaines, pauses obligatoires, révision de reprise en fin de journée | ordinateur de préférence |

Règle dure : **le neuf est plafonné par jour, quel que soit le format**
(`nouveau_par_jour` dans la config, défaut 20 cartes). Une journée
dépense le reste en compréhension (leçons, ateliers, synthèses,
lectures), jamais en bourrage de cartes. Le format Séance n'a pas de
verrou dur à 15 minutes : la clôture est proposée, pas imposée.

## Contexte

La conception d'août imposait un plafond dur de 15 minutes et un
« verrouillage à 15:00 ». Le brief du 02/09 veut aussi des demi-journées.
La science ne contredit pas la journée : la pratique massée est
inférieure pour la rétention (Cepeda et al. 2006), mais c'est le neuf
qui crée la dette, pas la compréhension. Une journée bien construite
espace ses reprises (le chapitre du matin revient en fin d'après-midi)
et entrelace ses domaines.

## Conséquences

- `academie.json` gagne `nouveau_par_jour` et les durées cibles des
  formats ; `app/seance.py` gagne un composeur d'étude et un composeur
  de journée (chantiers `ACA-ETUDE-1`, `ACA-JOURNEE-1`).
- Le journal porte le format de chaque révision (champ `format` de journal-v1) pour mesurer
  ce que chaque format produit en rétention.
- `METHODE.md` §8 est amendé (plus de plafond dur) et §21 ajouté (la
  journée).

## Réouverture

Si les journées produisent une pile de révisions dues > 2 × le plafond
de reprise la semaine suivante, on baisse `nouveau_par_jour`, pas le
format.

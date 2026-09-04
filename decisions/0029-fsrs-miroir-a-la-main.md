# 0029. Le FSRS du client est un miroir écrit à la main, pas ts-fsrs

Date : 04/09/2026. Amende `0007` sur un point : la dépendance `ts-fsrs`
n'entre pas.

## Décision

`web/src/moteur/fsrs.ts` reproduit `app/planificateur.py` ligne à ligne.
Le juge de parité reste `app/vecteurs_fsrs.py`, rejoué à chaque test
(`src/moteur/parite.test.ts`, tolérance 1e-4), jamais un fichier de
vecteurs commité.

## Contexte

Le squelette du client v2 (03/09) devait poser `ts-fsrs` épinglé. En
construisant, il est apparu que `ts-fsrs` impose ses propres états
(apprentissage par paliers, relearning, fuzz) et n'expose pas la formule
court terme nue du Python. Le contourner coûtait plus qu'un miroir, et
un miroir ne dérive pas au prochain minor d'une dépendance.

## Conséquences

- Toute modification de `app/planificateur.py` se reporte dans `fsrs.ts`
  dans le même commit ; la parité rouge bloque.
- `0007` reste valable pour tout le reste (React, TypeScript, Vite,
  Dexie, Motion).

## Réouverture

Si le moteur Python adopte un jour les états de `ts-fsrs`, on remplace
le miroir par la dépendance.

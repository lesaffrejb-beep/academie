# Cahier ACA-SANS-FRONT-2 : le carnet d'erreurs et le quiz dans la conversation

Résultat attendu : la surface `app/academie.py` expose le carnet
d'erreurs (`erreur`, `erreurs`) et le quiz de positionnement (`quiz`),
en réutilisant `app/erreurs.py` et `app/quiz.py` sans les réécrire.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-SANS-FRONT-1. Bloque : rien.

Décisions de référence : [`decisions/0054`](../decisions/0054-plus-de-front-le-depot-est-l-interface.md)
(la surface), et les règles déjà écrites dans `app/quiz.py` et
`app/erreurs.py`.

## Périmètre

Peut créer ou modifier : `app/academie.py` (deux commandes et une
troisième), `app/tests_academie.py` (les tests), `app/tests.py` (une
mutation), `prompts/jouer.md` et `skills/academie/SKILL.md` (une phrase
chacun).
Ne touche pas : le moteur (`erreurs.py`, `quiz.py`, `seance.py`,
`progression.py`) qui fait foi sans changement, la banque, `serveur/`,
`web/` (archivé).

## Déjà tranché (ne pas rouvrir)

- Le carnet d'erreurs est privé, append-only, dans
  `etat/<profil>/erreurs.jsonl` ; la raison est facultative
  (`app/erreurs.py`).
- Une bonne réponse de quiz écrit une ligne `origine: quiz` avec une
  `stabilite_forcee` ; une mauvaise n'écrit rien ; le quiz OUVRE des
  régions, il n'écrit jamais leur remplissage (`app/quiz.py`).
- Le quiz ne se rejoue pas pour une région déjà positionnée
  (`QuizDejaJoue`).
- L'état reste local et hors git ; la surface ajoute, elle ne réécrit
  jamais.

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_academie.py` :
   - `erreur <id> "raison"` ajoute une ligne au carnet, sans réécrire ;
     une carte inconnue n'écrit rien et sort en erreur ;
   - `erreurs` relit le carnet et remonte les raisons récurrentes ;
   - `quiz` sans résultats ne compose que des questions et n'écrit
     rien ;
   - `quiz --resultats` n'écrit que les bonnes réponses, ouvre la région
     au-dessus du seuil, et refuse un second passage.
2. `cmd_erreur`, `cmd_erreurs`, `cmd_quiz` dans `app/academie.py`, qui
   appellent `erreurs.note_erreur`, `erreurs.raisons_recurrentes`,
   `quiz.compose`, `quiz.applique_resultats`, `quiz.regions_ouvertes`.
3. Une phrase dans les consignes (`prompts/jouer.md`,
   `skills/academie/SKILL.md`) pour dire quand noter une erreur et quand
   passer le quiz.
4. Brancher la mutation qui prouve que la garde « carte inconnue
   n'écrit rien » mord.

## Ce qu'on ne fait pas

- Aucun écran, aucune dépendance.
- Aucune réécriture du carnet ni du journal.
- Aucun remplissage de région par le quiz : c'est FSRS qui mesure.
- Aucun rejeu du quiz pour une région déjà positionnée.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py erreur <carte> "confondu avec la partie privative"
python3 app/academie.py erreurs
python3 app/academie.py quiz --region droit --json
```

JB voit : une carte ratée peut porter sa raison en une ligne, relue au
bilan, et un quiz de positionnement peut ouvrir une région sans
retaper les bases.

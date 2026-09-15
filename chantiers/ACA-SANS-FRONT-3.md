# Cahier ACA-SANS-FRONT-3 : les aides de séance dans la conversation

Résultat attendu : la surface expose les deux aides qui manquent pour
finir une séance sans deviner : `mini-lecons` (les cartes ratées trois
fois, avec leur question et les raisons récurrentes du carnet) et
`prevue` (le prochain intervalle selon la note 1-4, sans révéler la
réponse). Tout vient du moteur, rien n'est recalculé à la main.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-SANS-FRONT-2. Bloque : rien.

## Périmètre

Peut créer ou modifier : `app/academie.py` (deux commandes et un
helper), `app/tests_academie.py` (les tests), `app/tests.py` (une
mutation), `prompts/jouer.md` et `skills/academie/SKILL.md` (une phrase
chacun).
Ne touche pas : le moteur (`erreurs.py`, `planificateur.py`, `seance.py`,
`quiz.py`), la banque, `serveur/`, `web/` (archivé).

## Déjà tranché (ne pas rouvrir)

- La règle des 3 échecs lit le journal de RÉVISIONS, pas le carnet :
  `erreurs.cartes_a_mini_lecon` ; le carnet ne dit que le pourquoi
  (`app/erreurs.py`).
- Le barème FSRS et les formules viennent de `app/planificateur.py` ;
  `prevue` ne fait que les appeler, il n'invente aucun intervalle.
- Un journal `origine: quiz` n'est jamais un échec.
- La réponse d'une carte ne se montre qu'à `correction` (`decisions/0054`).

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_academie.py` :
   - `prevue` rend quatre notes, d'intervalles croissants (4 > 1), et
     n'expose jamais `reponse` ;
   - `mini-lecons` liste une carte ratée trois fois avec son nombre
     d'échecs et sa question, et sort vide sans rate.
2. `cmd_prevue` et `cmd_mini_lecons` dans `app/academie.py`, appuyés sur
   `planificateur` et `erreurs`.
3. Une phrase dans `prompts/jouer.md` et `skills/academie/SKILL.md`.
4. La mutation qui prouve que `prevue` dépend bien de la note.

## Ce qu'on ne fait pas

- Aucun écran, aucune dépendance, aucun appel de modèle.
- Aucun barème recopié : tout vient de `planificateur.py`.
- Aucune fuite de la réponse dans `prevue`.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py prevue <carte>
python3 app/academie.py mini-lecons
```

JB voit : avant de noter, l'effet de chaque note sur la prochaine
échéance ; et la liste des cartes à reprendre par une mini-leçon.

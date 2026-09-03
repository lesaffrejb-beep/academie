# Cahier ACA-RITUAL-METRICS-1 : le tableau de bord du rituel

Résultat attendu : `app/rituel.py` mesure le rituel depuis le journal
seul, sans lire le contenu des réponses : séances commencées et finies,
abandons, durée, formats, jours de la semaine, coupures. C'est
l'instrument du gate de `ACA-RITUAL-1` ; sans lui, « quatre séances par
semaine » n'est qu'une intention.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-JOURNAL-SYNC-1. Bloque : ACA-RITUAL-1 (son bilan),
ACA-MULTI-DECISION-1 (qui attend ce bilan).

## Périmètre

Peut créer ou modifier : `app/rituel.py` (nouveau), `app/tests_rituel.py`
(nouveau), `app/tests.py` (ajout de la suite et d'au moins une mutation),
`serveur/README.md` (une phrase : comment sortir le journal pour le
rapport).
Ne touche pas : le journal lui-même (lecture seule, jamais d'écriture),
`serveur/academie_etat/`, la banque, le client, le moteur FSRS.

## Déjà tranché (ne pas rouvrir)

- Le journal est append-only et se rejoue ; aucun score n'est stocké
  (`decisions/0006`, `serveur/schema.sql`).
- Le contrat des lignes est `contrats/journal-v1.schema.json`. Une
  séance s'ouvre par une ligne `mode: seance` qui porte `format`,
  `graine`, `banque_version`, `moteur_version` ; les réponses suivent en
  `mode: revision`, `quiz` ou `examen`.
- Zéro tiers, zéro télémétrie sortante (`decisions/0020`) : ce rapport
  se lance à la main, sur un fichier, et n'appelle rien.
- La preuve recherchée est dans `ROADMAP.md` : au moins quatre séances
  par semaine, sans culpabilisation après une coupure.

## Ce que le rapport n'a pas le droit de lire

Le contenu des réponses. Le module travaille sur une **liste blanche de
champs** (`quand`, `mode`, `format`, `duree_ms`, `cartes`, `carte`,
`jour`) et ignore tout le reste. Ni `cap`, ni `raison`, ni `motif`, ni
`attendus_coches`, ni `note` n'entrent dans le rapport : la mesure du
savoir est un autre sujet, c'est le bilan de `ACA-RITUAL-1`.

## Étapes, dans l'ordre

1. Tests rouges (`app/tests_rituel.py`), sur les quatre fixtures que
   demande `roadmap.json` :
   - **séance complète** : toutes les cartes annoncées par la ligne
     `seance` ont leur réponse ; elle compte finie, sa durée est celle
     de l'horloge et celle des réponses ;
   - **arrêt après trois minutes** : une partie des cartes seulement ;
     elle compte abandonnée, et le rapport dit à quelle carte ça s'est
     arrêté (le rang, pas le contenu) ;
   - **coupure de trois semaines** : la plus longue coupure est trouvée,
     les semaines sans séance sont comptées, et rien dans le rapport ne
     ressemble à un reproche (`VOIX.md`) ;
   - **journal corrompu** : ligne illisible, ligne sans `quand`, ligne
     hors contrat, réponse orpheline sans séance ouverte. Le rapport
     sort quand même, avec le compte des lignes écartées.
2. `app/rituel.py` : lecture d'un JSONL, projection sur la liste
   blanche, découpage en séances, agrégats, sortie lisible et `--json`.
3. Brancher la suite dans `app/tests.py` et ajouter la mutation qui
   prouve que le découpage des séances mord.

## Ce qu'on ne fait pas

- Aucun écran, aucun graphique : c'est un rapport de terminal et un
  JSON. Le tableau de bord visuel viendra au client, plus tard.
- Aucune note, aucun score, aucune mesure de savoir.
- Aucun envoi, aucun fichier écrit dans `etat/`.

## Preuve

```bash
python3 app/tests_rituel.py && python3 app/tests.py && python3 tooling/check.py
python3 app/rituel.py <journal.jsonl>
```

JB voit : combien de séances par semaine, combien finies, combien
abandonnées et à quel rang, la plus longue coupure, et les jours où il
ouvre vraiment l'Académie.

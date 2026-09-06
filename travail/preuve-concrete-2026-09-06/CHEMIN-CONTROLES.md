# Chemin d'apprentissage : contrat et preuves ciblées

06/09/2026, Codex / GPT-6, agent `/root/acces_profils`.
Cahier : fin d'ACA-EXPERTISE-1, demande explicite de professeur ancré dans
la copropriété. Aucun état joueur, appel de modèle ou contenu servi modifié.

## Commandes

```sh
python3 app/chemin_apprentissage.py preparer --demande "Je veux apprendre X" --metier copro --sortie /tmp/demande-chemin.json
python3 app/chemin_apprentissage.py verifier travail/preuve-concrete-2026-09-06/chemin-minimal.json --strict-local
python3 app/tests_chemin_apprentissage.py
```

`preparer` écrit un JSON neuf et refuse tout écrasement. Il fournit les
identifiants de chapitres existants, laisse cible/ancrage/diagnostic/étapes
à instruire, et ne suppose aucun acquis. Ce squelette initial **n'est pas
encore un chemin cohérent**. Il est destiné au travail de l'agent.

`verifier` accepte `--racine` pour un autre dépôt/fixture et `--banque` pour
un artefact explicite. À défaut, il consulte `site/banque.json` de la racine
si présent. Sans artefact, toute étape dite disponible est refusée.
`--strict-local` compare SHA-256 et original sur disque, ainsi que l'existence
des supports déclarés ; les chemins relatifs partent de `--racine`.

Sortie : `statut="cohérence structurelle"`, `coherent`, `erreurs`,
`sources_manquantes`, `limites`. Code 0 si cohérent, 1 sinon. Une source
`a_trouver` peut rester dans un chemin cohérent à construire ; elle interdit
de déclarer disponible l'étape qui la référence.

## Champs à utiliser dans le prompt

Le schéma fait foi : `contrats/chemin-apprentissage-v1.schema.json`.
Exemple : `chemin-minimal.json`, profil **fictif** avec une compétence déclarée
et une inconnue ; aucun acquis attribué à JB.

| Objet | Champs |
|---|---|
| Dossier | version 1, statut brouillon, demande, cible_observable, metier, ancrage, prerequis, diagnostic, sources, etapes ; contexte facultatif |
| Ancrage / transversalité | chapitre existant, justification |
| Prérequis | notion, etat inconnu/declare/observe ; chapitre facultatif ; preuve et date obligatoires pour observe |
| Diagnostic | productions avec consigne/criteres ; reussite et echec listent des identifiants d'étape |
| Source | id, titre, statut presente/a_trouver ; présente : url HTTPS, empreinte SHA-256, chemin_original ; à trouver : manque |
| Étape | id, titre, niveau 1-5, justification_niveau, dependances, chapitre **ou** proposition, disponibilite disponible/a_construire, transversalites, notions, sources, exercices, transfert, reprise_echec |
| Proposition | titre, justification ; jamais disponible |
| Exercice | format, consigne, justification, criteres, sources ; support facultatif avec chemin et justification |
| Transfert | cas_nouveau, criteres |
| Reprise après échec | consigne, etapes à reprendre |

Les étapes et l'ancrage appartiennent au cursus demandé ; une transversalité
peut pointer vers un autre cursus existant. Une nouvelle branche est une
proposition explicite. Le DAG des dépendances est contrôlé par tri itératif,
sans limite de profondeur ajoutée ; les retours après échec peuvent revenir
sur une étape et ne sont pas confondus avec ce DAG.

## Preuves

Tests écrits avant le module : rouge initial `ModuleNotFoundError`. Après
implémentation, huit tests passent. Ajout d'une entrée d'artefact malformée :
rouge effectif `AttributeError` ; correction vers refus structuré, puis
**neuf tests passent en 0,119 s**. Ils couvrent les cas du cahier, le cycle à
plusieurs étapes, le transfert absent, les dates invalides, l'original absent
ou modifié, un support absent, le métier distinct, les propositions, JSON
malformé, URL invalide et la préparation sans écrasement.

L'exemple minimal passe avec `--strict-local`, `sources_manquantes=["guide"]`.
Cette réussite signifie qu'il décrit honnêtement sa construction restante.
La suite est branchée dans `app/tests.py` ; aucun test global ni génération
n'a été lancé par cet agent. Module, tests et schéma totalisent 357 lignes
au premier passage vert final.

## Limites explicites

Le programme vérifie des références et la présence de preuves déclarées,
pas leur vérité ni la qualité pédagogique de l'argumentation. Il ne juge
pas automatiquement qu'un cas est réellement nouveau ou qu'une bifurcation
est pertinente. Le niveau est celui de l'étape proposé et justifié par
l'agent, jamais un niveau acquis par l'élève. Une banque fournie constitue
le témoin local de service : ce contrôle n'établit ni son authenticité
distante ni l'état VPS, ni les signalements du journal privé d'un joueur.
Le vérificateur stdlib applique le sous-ensemble JSON Schema utilisé dans
ce contrat, pas un moteur JSON Schema général.

## Correction après contre-lecture : disponibilité et dates

La relecture indépendante a identifié deux acceptations abusives : péremption
de carte `false`, `0` ou `20990101`, et étude juridique dont la vérification
annuelle était dépassée. Les rouges ciblés reproduisent dix sous-cas, puis
deux autres sur une date de vérification compacte. La correction reprend les
règles de `web/src/moteur/serviceabilite.ts` et `etude.ts` :

- Carte : absence/null/chaîne vide autorisés ; autre valeur exige une date
  réelle `AAAA-MM-JJ`, encore valable le jour indiqué ; types booléens et
  numériques refusés.
- Leçon : péremption renseignée au format canonique ; conformément au client
  actuel, les valeurs falsy `false`/`0` sont ignorées à ce niveau uniquement.
- Sources de nature texte officiel ou jurisprudence : vérification datée
  exigée, refus au-delà de 365 jours ; les dates ISO horodatées tiennent compte
  de leur décalage. Aucune péremption annuelle n'est inventée pour une source
  institutionnelle.

Résultat final ciblé : **11 tests, 0,131 s, OK**, 404 lignes pour module/tests/
schéma. L'exemple `chemin-electricite.json` du coordinateur, inchangé, passe
avec `--strict-local` et conserve `rapport-complet` comme source manquante.
Aucun test global relancé. La contre-lecture de confirmation reste indépendante.

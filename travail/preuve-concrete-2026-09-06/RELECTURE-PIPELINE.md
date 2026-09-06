# Relecture indépendante du pipeline de chemin

6 septembre 2026 — Codex / GPT-6. Périmètre : `app/chemin_apprentissage.py`, ses tests ciblés et le schéma v1, confrontés à CHEMINS.md, au cahier et au contrôle de disponibilité du client. Aucun fichier auteur modifié ; aucun réseau ni test global.

**Un écart P2 confirmé sur la disponibilité.** Les autres limites examinées correspondent au rôle annoncé : le script contrôle une structure, le professeur reste l’agent. Aucun verdict d’acquis ou de formation complète n’est produit par le code examiné.

## P2 — La disponibilité peut être acceptée alors que le client refuse l’étude

Dans [app/chemin_apprentissage.py:73](/Users/jb/Code/academie/app/chemin_apprentissage.py:73), `_servie` traite toute péremption fausse comme absente et accepte les formats supplémentaires de `date.fromisoformat`. Il ne reprend pas non plus le contrôle de fraîcheur des sources officielles/jurisprudence du client. Une banque ancienne ou mal formée passée par `--banque` peut donc donner une étape `disponible` et un résultat `coherent: true`, même en `--strict-local`, alors que cette étude est refusée dans l’application.

Premier cas adverse, décliné depuis `exemple()` des tests : source locale identifiée, empreinte concordante, étude valide dans le bon cursus, carte retenue. Une seule valeur de péremption de carte est changée à chaque essai.

| Variante | Résultat du pipeline observé | Contrôle client lu |
| --- | --- | --- |
| `false` | `coherent: true` | refus : type non textuel |
| `0` | `coherent: true` | refus : type non textuel |
| `"20990101"` | `coherent: true` | refus : format différent de `AAAA-MM-JJ` |
| `"2000-01-01"`, témoin expiré | `coherent: false` | refus |
| Étude et carte non périmées, source `texte-officiel`, `verifie: "2020-01-01"` | `coherent: true` | refus : vérification de plus de 365 jours |

Références client : [serviceabilite.ts:15](/Users/jb/Code/academie/web/src/moteur/serviceabilite.ts:15) et [etude.ts:12](/Users/jb/Code/academie/web/src/moteur/etude.ts:12). Le comportement client ci-dessus est établi par lecture de ces conditions ; aucun test navigateur n’a été exécuté pendant cette revue. Les résultats Python exacts sont conservés dans [resultats.json](/Users/jb/.codex/visualizations/2026/09/06/01a07779-1d3c-7203-a4f5-f7ddc4deb94e/relecture-pipeline/resultats.json).

Correction recommandée : faire correspondre ce prédicat aux contrôles de péremption et de fraîcheur du client, avec tests des valeurs ci-dessus, du jour exact de péremption et de la limite annuelle. Il s’agit de disponibilité éditoriale dans l’artefact : le journal personnel peut encore retirer une carte signalée. L’auteur a reçu les témoins ; sa correction éventuelle n’est pas couverte par ce verdict initial.

## Limites vérifiées, sans faux verdict pédagogique

Second cas adverse : un prérequis `observe`, avec `preuve: "x"` et une date valide non future ; une source locale vide nommée `vide.pdf`, dont le SHA-256 correspond ; étape `a_construire`. En `--strict-local`, le résultat est `coherent: true` et conserve la limite « Ni jugement pédagogique, ni validation d’acquis, ni publication. »

Cette acceptation ne constitue pas une erreur de notation de l’élève : aucune notation n’est exécutée. Le contrat exige une référence textuelle de preuve pour `observe`, mais ne contrôle ni l’existence de cette production, ni l’auteur de l’observation, ni l’aide reçue. Le professeur doit examiner ces éléments avant de considérer un acquis comme constaté ; une simple chaîne non vide reste une déclaration du dossier.

De même, `presente` et `--strict-local` prouvent au maximum un fichier accessible et une empreinte concordante. Ils ne prouvent ni le format PDF, ni le lien entre fichier et URL, ni l’autorité de l’émetteur, ni la lecture des pages par l’usine, ni l’appui réel d’une affirmation. Une source retrouvée ne devient pas automatiquement une source lue ou un enseignement disponible. Sans `--strict-local`, le résultat annonce explicitement que les originaux et supports ne sont pas contrôlés sur disque.

Une étape reliée à un chapitre disponible peut proposer d’autres exercices que ceux de ce chapitre : le contrôleur ne confronte pas ces consignes aux cartes servies. Son état de disponibilité doit donc être interprété comme la présence d’une étude associée, pas comme la preuve que chaque activité du dossier est implémentée.

## Dépendances, amorce et portée du contrat

Les références inconnues et identifiants dupliqués sont rejetés. Le tri de Kahn rejette les cycles de dépendances, sans récursion dépendant de la profondeur. Les liens transversaux sont contrôlés séparément et ne deviennent pas automatiquement des prérequis. Les reprises peuvent revenir sur la même étape, ce qui convient à un nouvel essai.

Le contrôle assure l’existence des suites de diagnostic et de reprise ; il n’établit pas qu’un ordre d’étapes est pédagogiquement pertinent, qu’une branche atteint la cible, ou qu’une réponse donnée autorise à sauter un prérequis. Cette responsabilité reste au professeur.

Le schéma impose au moins une étape et des critères de transfert, mais ne mesure aucune couverture de métier. `preparer` écrit une amorce volontairement incomplète ; le statut du dossier reste `brouillon`, même après un contrôle cohérent. Un tel résultat ne signifie donc ni parcours complet, ni cours prêt, ni acquisition. La documentation actuelle fait cette distinction ; elle doit être conservée dans toute présentation du résultat.

## Validation et version examinée

`python3 app/tests_chemin_apprentissage.py` : **9 tests passent**. Deux familles d’entrées adverses ont été examinées dans des dossiers temporaires fictifs, sans données joueur ni client. Aucune modification des fichiers auteur, aucun test global et aucun accès réseau.

Empreintes au moment de la revue, avant correction éventuelle par l’auteur :

| Fichier | SHA-256 |
| --- | --- |
| `app/chemin_apprentissage.py` | `05032426d580993ee6ed19bdb1fdd3cab9cb3c4d7f8e4c0c0c279bf46eb6e355` |
| `app/tests_chemin_apprentissage.py` | `841ce6def1875d28155537377bcb78e6292d53c62181bc353553363760e598c7` |
| `contrats/chemin-apprentissage-v1.schema.json` | `a91e9427a1d6574b0a3cc4e4fbebfe022a1439e3e399277c80f637a4a1b26dc0` |

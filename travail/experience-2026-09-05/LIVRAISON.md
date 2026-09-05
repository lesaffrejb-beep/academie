# Académie : livraison locale du 05/09/2026

Outil Codex, modèle GPT-6. Session 01a0704b-2f89-7eb1-82d1-219bc309c6ef.
Demande autonome de JB, cahier ACA-EXPERIENCE-1, décision 0036.
L'audit, le retrait des classes de modèles et leurs fichiers étaient déjà
présents dans l'arbre de travail. Cette livraison les conserve et construit
l'expérience demandée ; l'audit initial n'est pas réécrit rétrospectivement.

## Ce qui se joue

| Parcours | Chapitres | Cartes v2 |
|---|---|---|
| Tenir le fil d'une assemblée | Syndic et missions ; article 24 ; préparation du procès-verbal | 17 |
| Prendre soin commence ici | Cinq B ; transmissions orales Saed | 10 |

Cinq leçons structurées, questions initiales, exemples/contre-exemples,
aides, flash/QCM, synthèse personnelle et grille après réponse. Les 27
cartes rejoignent les rappels ; les 76 cartes v1 restent conservées.
Banque locale : 103 cartes, dont 93 copro et 10 IFSI. Les métiers sélectionnent
leurs propres contenus et indicateurs, le journal brut reste commun.
Les 389/375 chapitres des programmes ne sont pas autant de leçons livrées.

Le chapitre PV couvre sa préparation et ses mentions ; les modalités et
délais de notification restent à écrire. Les sources et cette réserve sont
visibles dans les attestations. L'IFSI reste un entraînement théorique.

## Expérience et reprise

Accueil Nuit/Papier, action d'étude dominante, planche ouvrant les vrais
chapitres, atlas pour explorer. La salle met le raisonnement au premier plan.
Le choix du métier, les réponses et la reprise fonctionnent localement.
Brouillons conservés pendant navigation/rechargement de l'onglet ; quitter
la session navigateur peut supprimer un brouillon non enregistré. Les étapes
enregistrées restent dans IndexedDB, même après fermeture.

Une réponse avec indice ne reçoit aucune note de rappel autonome et n'entre
pas comme succès dans FSRS. Un QCM garde son choix initial après révélation
et rechargement ; les choix sont réordonnés par carte. Les quatre niveaux
après réponse constituent une autoévaluation. Un choix faux garde une note
de rappel basse, même si l'élève appuie sur une appréciation haute.

La clôture dit « étude parcourue » et « non mesuré » pour le transfert.
Aucun score stocké, temps humain, faux joueur ou KPI inventé. Le
[protocole 1](PROTOCOLE.md) prépare les mesures distinctes avec et sans IA.

## Fiabilité et sources

- Rejeu du journal par instant UTC avec fractions exactes et départage
  identique Python/TypeScript ; ancien horodatage naïf interprété en UTC.
- Création locale monotone à la microseconde, marque atomique partagée par
  les onglets ; aucun ancien événement réécrit. Une horloge reculée peut
  produire une date logique : cela protège l'ordre sans mesurer le temps.
- HTTP 200 ambigu ou incomplet garde la file ; validation des lignes reçues
  et des champs Étude avant union. Import/export conserve les extensions.
- Publication des études fermée si carte manquante, périmée ou signalée,
  ou relecture indépendante structurée absente/invalide. Les auteurs
  historiques ne deviennent pas fictivement les auteurs du nouveau lot.
- Sources primaires Legifrance et HAS contrôlées pour les assertions du
  pilote. Extraits et pages consultés, sans prétendre une lecture intégrale
  des PDF terminée par l'usine. Aucune certification clinique ni juridique.
- Surinterprétations scientifiques ciblées corrigées ; les limites des
  recherches et les choix propres au produit sont explicités.

Relectures : [journal](../relecture-journal-2026-09-05.md),
[contenu](../relecture-contenu-2026-09-05.md),
[science](../relecture-science-2026-09-05.md),
[étude](../relecture-etude-2026-09-05.md), [rendu](REVUE-VISUELLE.md),
[cohérence des 34 retouches du programme](../relecture-programme-2026-09-05.md).
Les défauts trouvés par les passes indépendantes ont servi de régressions.
La revue de finition conclut `ship` sur les trois corrections demandées :
planche liée aux chapitres, action mobile visible, titres sans petite
étiquette préalable. Ce verdict est limité à ces corrections et aux
premiers écrans capturés, sans certification Awwwards ou goût de JB.

## Contrôles intégrés

| Contrôle | Résultat | Preuve |
|---|---|---|
| `python3 app/tests.py` | TOUT VERT, serveur local inclus | [python.log](preuves/python.log) |
| `python3 tooling/check.py` | 0 erreur | [controle.log](preuves/controle.log) |
| `npm test` | 270 tests client + 5 publication | [client-publication.log](preuves/client-publication.log) |
| `npm run build` | TypeScript, Vite et PWA passent | [build.log](preuves/build.log) |
| Navigateur, campagne complète | 69/70 ; course de l'horloge du test de minuit | [campagne](preuves/navigateur-campagne.log) |
| Minuit après correction du test | 2/2, ordinateur et téléphone | [reprise ciblée](preuves/navigateur-minuit.log) |
| Rendu et finition | 3 corrections résolues ; `ship` à ce périmètre | [revue](REVUE-VISUELLE.md) |
| Détecteur visuel | Aucun signal mécanique ; un seul passage | [résultat](preuves/detecteur.json) |

Les 70 scénarios distincts ont ainsi une preuve positive sur le même build.
Le test de minuit laissait auparavant passer l'heure pendant le chargement :
la carte expirait avant l'assertion initiale. Son horloge est maintenant
figée, puis avancée explicitement. Aucun seuil de performance n'a été
assoupli. Le budget de première question hors ligne inférieur à trois
secondes passe sur les deux viewports ; le temps total de son scénario
inclut l'amorçage réseau et n'est pas ce temps de première question.

Captures : [.impeccable/review](../../.impeccable/review/desktop.png),
375 × 812 et 1280 × 900, Nuit/Papier ; texte agrandi et clavier en E2E.
Les captures sont des viewports. L'assemblage full-page du runtime était
incorrect et n'a pas servi de preuve. Empreintes des sources vérifiées dans
[empreintes.json](preuves/empreintes.json). `git diff --check` sans erreur.
Coût monétaire et temps d'édition par chapitre non instrumentés ; aucun
chiffre inventé. Les tests et relectures ont dominé la fin de cette passe.

## Portée de la livraison

Aucun push, déploiement, migration de l'état ou nouveau compte effectué.
Le preview local sert le build de web/dist. La CI web est écrite mais son
exécution sur GitHub n'est pas attestée dans cette session.
Publication authentifiée, synchronisation sur appareils physiques, goût de
JB, rituel réel, rétention et transfert restent des preuves distinctes.

Les builds et tests mesurent le logiciel. Cette livraison ne prétend pas
avoir fait apprendre cinq chapitres à une personne ni rempli les programmes.

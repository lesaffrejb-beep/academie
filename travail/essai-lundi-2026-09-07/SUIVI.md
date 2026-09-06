# Objectif complet et preuves de reprise

Demande de JB du 06/09/2026 : collecter tout le corpus exploitable NotebookLM
avec agents et automatisation ; construire fiches, notions et modules
approfondis reliés à l'arbre et à des mécanismes d'apprentissage documentés ;
choisir le cursus à l'inscription par pseudo/mot de passe et retrouver son
compte en cliquant son nom ; remettre le graphe ; sauvegarder et progresser ;
permettre lundi matin d'essayer plusieurs modules/formats ; publier sur VPS
proprement, de façon reproductible et auditable ; pousser les grandes passes
sur main. L'objectif ne se réduit pas au benchmark ni au premier module.

## État de la passe

- Texte NotebookLM : passage sur 200 occurrences, 181 captures/169 empreintes
  distinctes ; 18 réserves documentaires et une source vide. Manifeste local
  vérifié et copié hors dépôt ; détail `../benchmark-notebooklm-2026-09-06/`.
- Médias : trois fiches AQC, 25 fichiers / 23 empreintes distinctes, copiés
  durablement hors dépôt et vérifiés. Pas de revendication d’exhaustivité du corpus. Ne pas confondre les références et les fichiers.
- Comptes : annuaire des pseudos visibles, choix cursus à l'inscription,
  clé non persistée localement. 6 parcours API+navigateur vérifiés en deux
  passages (5/6 puis correction du chemin de déconnexion et récupération1/1).
- Graphe : vrais prérequis, filtre/recherche et chapitres serviceables.
  Revue indépendante et 14 scénarios navigateur. Captures dans `../graphe-2026-09-06/`.
- Révisions : texte libre et critères conservés dans le journal local,
  6 scénarios ordinateur/téléphone ; aucun contenu de remplacement inventé,
  copie presse-papier refusée signalée comme telle.
- Nouveau module : contre-expertise rénovation, huit cartes et sept formats,
  source historique confrontée et relecture indépendante ; intégré au parcours
  rénovation. Banque locale 119 cartes, sept études. Associations interactives reliées
  à la génération : les champs structurés ne sont plus perdus à la publication.
  La reprise des critères de synthèse est corrigée et prouvée par rechargement.
- Science : portée des références corrigée dans METHODE36-37, revue distincte
  des résumés primaires. Aucune efficacité d'apprentissage locale prétendue.
- VPS : inspection lecture seule réalisée ; migration0003 nécessaire,
  Node absent, environ987MiB libres au constat. Script/paquet en préparation.
- Publication et push de cette passe : non réalisés au moment de ce point.

## Contrôles

`python3 app/tests.py` tout vert après actualisation du catalogue ;
`python3 tooling/check.py` zéro erreur ; npm test317 tests plus6publication
verts avant branchement final des interactions Étude. Ne pas présenter cette
preuve comme couvrant les changements ultérieurs. Des erreurs de sandbox
antérieures ont été suivies de vrais rejeux autorisés avec sockets localhost.

## Ce qui reste requis

1. Interactions Étude et reprise terminées localement, rendu ordinateur/téléphone examiné.
2. Revoir script de publication, préparer paquet depuis SHAcommité, sauvegarder,
   migrer sans perdre une ligne, installer API/client et prouver usage authentifié.
3. Pousser les grandes passes sur main et consigner SHA/paquet/état VPS.
4. Poursuivre tous médias accessibles, qualifier captures et réserves, fabriquer
   les prochains dossiers experts depuis des passages et supports examinés.
5. Vérifier le parcours réel de lundi ; distinguer tests automatisés, observation
   sur appareil physique et apprentissage différé. Le rituel humain ne s'invente pas.

## Complément benchmark

Une vraie page scannée (PDHH6) a été comparée visuellement : corps de l’arrêté
absent du texte NotebookLM capturé. Six repères recontrôlés indépendamment ;
gain OCR du panneau non démontré. PDF et images restent les références.

## Revue intégrée avant commit

Le parcours contre-expertise a révélé deux défauts corrigés : champs paires/etapes
perdus à la génération, et critères cochés de synthèse non repris en brouillon.
Tests rouges puis verts, deux parcours complets ordinateur/téléphone verts,
28 tests de séance verts. Le contrat structuré et le valideur sont alignés
avec contrôles des données malformées. Captures examinées : schéma, associations,
réponse et cases lisibles ; repères mobiles ajustés pour éviter leurs coupures.
325 tests TypeScript et six de publication verts avant les seules retouches
de brouillon et présentation finales, vérifiées depuis par E2E et compilation.
17 tests de paquet/conservation SQLite verts. Aucun brut documentaire dans le paquet.

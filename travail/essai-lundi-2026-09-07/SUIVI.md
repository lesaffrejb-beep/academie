# Objectif complet et preuves de reprise

Demande de JB du 06/09/2026 : collecter tout le corpus exploitable NotebookLM
avec agents et automatisation ; construire fiches, notions et modules
approfondis reliés à l'arbre et à des mécanismes d'apprentissage documentés ;
choisir le cursus à l'inscription par pseudo/mot de passe et retrouver son
compte en cliquant son nom ; remettre le graphe ; sauvegarder et progresser ;
permettre lundi matin d'essayer plusieurs modules/formats ; publier sur VPS
proprement, de façon reproductible et auditable ; pousser les grandes passes
sur main. L'objectif ne se réduit pas au benchmark ni au premier module.

## Demande vers chemin, puis exemple électrique

Le 06/09, le protocole `CHEMINS.md` et le contrôle JSON permettent de
préparer une demande, expliciter les prérequis inconnus et contrôler
sources, références, dépendances et étude associée. L’agent instruit le
chemin en conversation ; aucune adaptation automatique du client annoncée.
L’exemple électrique bifurque selon le diagnostic, avec une extension
rapport complet explicitement à construire. Le dossier de preuve est
`travail/preuve-concrete-2026-09-06/`.

Une nouvelle unité relue indépendamment ajoute sept cartes et deux SVG
originaux. Banque locale : 144 cartes, dix études ; copro 134 cartes et
huit études, dont trois du socle et cinq approfondissements. Le socle
reste de 389 chapitres prévus. Les deux originaux publics INRS/Promotelec
sont copiés sur le SSD monté `/Volumes/NOIR 1`, empreintes contrôlées.
La collecte NotebookLM complète ne se transforme pas automatiquement en cours.

## Dernière passe locale : fragilité et façade

Le 06/09 vers 19 h 50, les deux dossiers relus ajoutent dix-huit cartes.
Banque générée : 137 cartes, neuf études ; copro 127 cartes/sept études,
IFSI dix cartes/deux études. Les parcours sont accessibles depuis l'accueil,
avec des rattachements réels à l'arbre et des cas fictifs. Source Anah pour
la fragilité ; cahier d'Angers pour la façade, avec passages et pagination
confrontés au PDF public. Les brouillons et rapports restent conservés.

Les jeux de rôle affichent et copient désormais la question complète,
même sans guillemets ; l'indice reste derrière la demande d'aide. Le panneau
Sources montre le parti déclaré et la nature réelle, conserve l'inconnu et
ne présente plus toute source comme une règle.

Tests rouges puis verts : quatre E2E Fragilité et quatre E2E Façade,
ordinateur et téléphone, reprise des réponses et critères, copie complète,
exclusion IFSI. Captures examinées. Neuf tests de rendu ciblés verts après
les dernières corrections ; suite TypeScript 329 tests et six de publication
verts avant le dernier garde sur une nature héritée JavaScript, couvert
depuis par les tests ciblés et la compilation du parcours Façade.
`python3 app/tests.py` tout vert après les deux intégrations ;
`python3 tooling/check.py` zéro erreur. Preuves détaillées dans les deux
dossiers `travail/fragilite-2026-09-06/` et `travail/facade-2026-09-06/`.

Le paquet VPS 6946f16 préparé lors de la passe précédente ne contient pas
ces deux dossiers. Aucune installation n'a eu lieu depuis le refus de revue
automatique ; sa confirmation directe reste en attente. La collecte des
médias continue, avec inventaires séparant fichiers récupérés et références
manquantes. Aucun état partiel n'est une preuve d'exhaustivité du corpus.

## État de la passe initiale

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
  Node absent, environ987MiB libres au constat. Paquet 6946f16 transmis et contrôle distant20fichiers/7études vert ;
  installation bloquée par revue automatique, confirmation directe demandée.
- Push sur main : 6946f1647d49570124a13bd547f87a80a27414bc, confirmé.
  CI check34047707064 et client34047707140 réussies.
  Publication VPS : non réalisée, aucun service arrêté ni migration effectuée.

## Contrôles

`python3 app/tests.py` tout vert après actualisation du catalogue ;
`python3 tooling/check.py` zéro erreur ; npm test317 tests plus6publication
verts avant branchement final des interactions Étude. Ne pas présenter cette
preuve comme couvrant les changements ultérieurs. Des erreurs de sandbox
antérieures ont été suivies de vrais rejeux autorisés avec sockets localhost.

## Ce qui reste requis

1. Interactions Étude et reprise terminées localement, rendu ordinateur/téléphone examiné.
2. Après confirmation directe exigée par la revue automatique, appliquer le
   paquet revu et contrôlé ; sauvegarder, migrer sans perdre une ligne, installer
   API/client et prouver usage authentifié.
3. Grande passe poussée sur main ; consigner ensuite le résultat VPS réel.
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

Le refus automatique de l’installation porte sur `sudo --appliquer` et
la reconnaissance de l’autorisation utilisateur. Le transfert a été autorisé
après présentation de l’objectif enregistré, mais cette même preuve ne suffit
pas à la revue pour la migration. Une confirmation directe est en attente ;
le paquet reste vérifié et prêt. Voir `../publication-2026-09-06/PUBLICATION-VPS.md`.

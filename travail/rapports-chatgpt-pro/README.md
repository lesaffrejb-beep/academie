# Rapports de travail : IFSI, copro et stratégie

Classés le 04/09/2026 à la demande de JB. Commencer par le
[plan de déroulement](PLAN.md), puis le [tri des recommandations](TRIAGE.md)
pour le lot choisi. La demande est de reprendre IFSI et de traiter copro
avec la même exigence, en classant d'abord les rapports.

Un [troisième rapport stratégique](STRATEGIE.md) a été ajouté ensuite,
avant la reprise du code. Il recentre le plan sur les corrections et
l'usage réel avant une extension des contrats ou des contenus.

Cap commun : **entrer dans le métier, progresser dans sa pratique, puis
continuer à apprendre sans plafond**. Une version du programme est
inventoriable ; de nouvelles branches, spécialités et questions peuvent
toujours l'enrichir.

## Les pièces d'origine

| Rapport | Original local conservé intégralement | Organisation |
|---|---|---|
| IFSI | [Ouvrir le rapport IFSI](../../sources/f34fc8af2597118f.txt) | Syllabus et contexte copiés, lignes 1 à 568 ; critique, lignes 569 à 1380, verdict et 23 sections |
| Copro | [Ouvrir le rapport copro](../../sources/a708271c820f9311.txt) | Deux variantes successives : A, lignes 1 à 1388 ; B, lignes 1389 à 3584, respectivement 17 et 28 sections numérotées |
| Stratégie agents, Labor et Académie | [Ouvrir le rapport stratégique](../../sources/3a763bd084d6ee3e.txt) | Rapport unique, 726 lignes ; Académie aux lignes 318 à 462, stratégie et recommandations transversales dans les autres sections |

Les variantes copro restent ensemble, sans fusion ni réécriture.
Elles ne constituent pas deux avis indépendants. Le nombre de lignes
compte aussi la dernière ligne sans saut final.

Auteur annoncé par JB pour les deux premiers : **ChatGPT Pro**. Le modèle
sous-jacent exact et l'auteur de la troisième pièce ne sont pas précisés.
Le modèle qui classe les documents est distinct :
Codex / gpt-5.6-sol / classe grand, déclaré dans l'usine.

[index.json](index.json) contient les empreintes SHA-256 complètes, tailles,
provenances, limites des variantes et sommaires avec lignes de début et
de fin. Les trois copies sont identiques octet pour octet aux pièces
jointes de JB. Les textes bruts restent dans `sources/`, hors Git et
hors publication, conformément au dépôt ; cet index et les synthèses
sont destinés au versionnement. Ils ne remplacent pas une sauvegarde
des originaux locaux.

## Nature et portée

Ce sont des **critiques de conception produites par un modèle**, classées
`editeur`, fiabilité `C` dans la nomenclature actuelle. Ce code ne donne
aucune autorité réglementaire au rapport. Une recommandation peut être
utile ; un chiffre ou une règle se vérifie dans une source primaire.

Les fiches locales sont
[IFSI](../../sources/f34fc8af2597118f.fiche.json) et
[copro](../../sources/a708271c820f9311.fiche.json).
L'usine a accepté les unités du pivot IFSI (20 pages, 2 unités) et copro
(43 pages, 4 unités), ainsi que leurs fiches. Les lignes de registre ont
été produites en prévisualisation. Elles ne sont pas ajoutées au registre
des sources de cartes : aucun contenu pédagogique ne doit prendre ce
rapport pour son fondement réglementaire.

**Limite du contrôle :** ces pages sont des pages machine, pas une
pagination d'auteur. Le nettoyeur de transcriptions peut retirer un
préfixe court suivi de deux-points. Le contrôle compare le pivot à ce
témoin normalisé ; pour une formulation exacte, lire le `.txt` original
aux lignes de l'index. Le verdict de l'usine ne prouve ni l'exactitude
juridique, ni la qualité pédagogique, ni une relecture professionnelle.

## Ce qui est utilisable maintenant

- [TRIAGE.md](TRIAGE.md) distingue constats du dépôt, vérifications
  primaires, propositions, divergences et points encore à vérifier.
- [PLAN.md](PLAN.md) fixe un ordre de travail, avec fichiers, preuves,
  dépendances et limites de chaque lot.
- [etat-programmes.json](etat-programmes.json) conserve les comptages
  recalculés et l'empreinte des deux JSON au classement initial, avant
  la finition IFSI décrite dans son point de reprise. Ce sont des
  objectifs éditoriaux, jamais des acquis ni des heures observées.
- Le [point IFSI](../2026-09-04-revision-ifsi.md) conserve les changements
  antérieurs et les défauts d'intégration encore ouverts.
- Le [point produit](../audit-froid-2026-09-04.md) reste responsable du
  front, du journal et de la migration ; les rapports pédagogiques ne
  clôturent aucun de ces chantiers.

Le classement est une étape documentaire. Les programmes, cartes et
moteurs ne sont pas corrigés par le seul fait d'avoir classé les rapports.

La troisième fiche est [ici](../../sources/3a763bd084d6ee3e.fiche.json) :
son unité de huit pages machine et sa fiche sont acceptées par l'usine.
Sa ligne de registre a également été produite en prévisualisation.

## Contrôles du classement initial, avant finition

| Contrôle exécuté le 04/09/2026 | Résultat |
|---|---|
| Empreintes des bruts contre les pièces jointes ; segments et titres de l'index ; liens locaux | Passent |
| `usine.py valider`, `suivant`, `fiche`, puis `registre` sans écriture | Unités et fiches acceptées ; lignes de registre proposées |
| `python3 app/tests.py` | Trois échecs IFSI dans la suite de 18 tests, dont le contrat `legacy` ; le serveur rencontre l'interdiction de socket du sandbox. Toutes les autres suites, la banque et les chapitres passent. |
| `python3 app/tests_serveur.py`, avec socket locale autorisée | Passe ; le défaut d'environnement du premier passage est isolé. |
| `python3 tooling/check.py` | Neuf lignes d'erreur liées à l'état IFSI déjà ouvert : contrat `legacy` et 14 tirets cadratins dans le JSON. |
| `git diff --check` | Passe |

La base globale était encore rouge à ce point. Les journaux
temporaires sont `/tmp/academie-rapports-tests.log`,
`/tmp/academie-rapports-serveur.log` et
`/tmp/academie-rapports-check.log` ; cette table conserve le résultat
utile si ces fichiers disparaissent. Aucun code, programme ou contenu
servi n'a été modifié pendant ce classement.

**État après reprise :** L1 est terminé localement, 21 tests IFSI et
contrôles globaux verts. Le troisième rapport est archivé et le plan
est recentré. Les preuves courantes remplacent cet ancien état dans le
[point de reprise IFSI](../2026-09-04-revision-ifsi.md).

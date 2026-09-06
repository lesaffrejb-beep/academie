# Du visuel source au support réellement utilisable

06/09/2026, Codex / GPT-6. Complément demandé par JB pour ACA-EXPERTISE-1.
Décision 0048. Contrat éditorial et protocole d'essai, **pas encore un
manifeste imposé par un valideur ni une chaîne d'assets implémentée**.

## Trois objets, à ne pas confondre

1. **Preuve locale** : PDF original, page rendue, figure et légende dans leur
   contexte, avec empreintes. Elle permet de revenir au document.
2. **Support pédagogique** : visuel sélectionné pour une compétence, avec
   légende adaptée, zoom et accessibilité ; réutilisation autorisée ou création
   originale instruite. Un redessin n'efface pas la question des droits.
3. **Exercice** : consigne, zones/relations, réponses attendues, limites,
   aides et corrigé. Il utilise une version précise du support.

Un Markdown « image ici » ou une description correcte ne livre ni 2 ni 3.
Un schéma doit être conservé comme ensemble visible : traits, flèches,
couleurs, textes et légende, pas seulement comme collection d'objets extraits.

## Ordre de fabrication

1. Lors de l'unité de lecture usine, inventorier photos, plans, coupes,
   schémas, graphiques, tableaux et détails. Distinguer supports utiles,
   décorations et cas incertains. Ne pas prendre le nombre d'objets image du
   PDF pour un nombre de figures pédagogiques ; garder les occurrences répétées.
2. Conserver le rendu de page comme preuve. Extraire un objet s'il suffit,
   sinon préparer un cadrage du rendu avec marge et légende associée. Ne pas
   écraser la preuve ; conserver la transformation. Ne jamais retirer une
   échelle, une note ou une flèche nécessaire à l'interprétation.
3. Associer figure et légende, y compris lorsqu'elles sont sur des pages
   différentes. Transcrire les labels et relever les relations distinctement.
   Pour un graphique, garder axes, unités, séries, hypothèses et notes ; une
   valeur lue approximativement sur une courbe n'est pas une donnée exacte.
4. Qualifier l'usage et les droits du support, séparément de la licence des
   métadonnées du document. Source non qualifiée : preuve locale seulement,
   pas d'export automatique. Aucun original client n'est admis.
5. Choisir la tâche pédagogique, puis créer ses données : éléments à nommer,
   relations à reconstituer, zones à repérer, observations et hypothèses à
   distinguer. Un schéma original explique un mécanisme ; une image générée
   ne devient pas une photographie de désordre réel ou une preuve de diagnostic.
6. Faire comparer par un relecteur indépendant la figure, ses relations et
   le corrigé avec les preuves. Contrôler tous les visuels utilisés dans le
   cours ; le sondage du reste ne remplace pas cette vérification.
7. Tester le support et l'exercice sur la route réelle, mobile et ordinateur,
   puis autoriser séparément la diffusion selon la doctrine du dépôt.

## Fiche visuelle minimale à transmettre entre agents

| Groupe | Informations requises |
|---|---|
| Identité | id stable, SHA du document, page physique et pagination imprimée, id de chaque occurrence |
| Localisation | coordonnées du cadre ; unité, origine, rotation et dimensions de la page/rendu explicites |
| Preuves | fichier original/rendu/cadrage, SHA, dimensions, outil/version/options, transformation appliquée |
| Contenu | type, légende exacte et son emplacement, labels, échelles, unités, notes, relations relevées |
| Interprétation | explication séparée, assertions et sources, limites, incertitudes, relecteur et preuve de contrôle |
| Droits et diffusion | auteur/crédit, statut et preuve des droits, transformations envisagées, local seulement ou canal autorisé |
| Usage produit | compétence, module/exercice, consigne, support apprenant et support corrigé distincts |
| Interaction | zones/polygones normalisés entre 0 et 1, repère de l'image pédagogique, SHA de celle-ci, relations et réponses attendues |
| Accessibilité | description, alternative adaptée à la tâche, contrôle de non-divulgation accidentelle du corrigé |
| État | inventorié / extrait / contrôlé / utilisable localement / diffusion autorisée, avec preuves séparées |

Changer le cadrage ou l'image invalide les coordonnées et leur preuve de
contrôle. Reprojection explicite puis nouvel essai, jamais réutilisation
silencieuse des anciennes zones. L'absence d'un champ reste un manque ; ces
états éditoriaux ne sont pas des sceaux de l'usine.

## Critères du benchmark visuel à ajouter

Constituer, avant réglage des moteurs, une référence indépendante comprenant
figures composites, légendes éloignées, petites annotations, photos, courbes,
plans et tableaux. Conserver des supports neufs pour le test final.

| Dimension | Ce qu'on vérifiera | Erreur qui interdit l'usage proposé |
|---|---|---|
| Couverture | figures utiles retrouvées / figures attendues ; faux ajouts et doublons séparés | figure nécessaire omise ou remplacée par un logo |
| Cadrage | tous les composants utiles présents, comparaison au rendu | flèche, échelle, note ou légende tronquée |
| Attribution | bonne page, bonne figure, bonne légende | légende d'une autre figure |
| Fidélité | labels, unités, cellules, liens et sens des flèches | confusion de circuit, de couche ou de valeur |
| Lisibilité | labels réellement lisibles avec le zoom prévu | information requise illisible sur l'écran cible |
| Exercice | consigne solvable, réponse et géométrie correctes, correction explicative | zone décalée, réponse dévoilée ou corrigé infondé |
| Reprise | version source → support → exercice retrouvable | correction source sans repérage des exercices affectés |

Ne pas fondre ces dimensions dans une note unique qui masquerait une erreur
critique. Le banc actuel **ne mesure aucune de ces dimensions complètement**.
Ses scores textuels ne sont donc pas des scores de récupération visuelle.

## Ce que le produit doit permettre d'apprendre

- Photo : décrire les indices visibles, proposer des hypothèses et demander
  les contrôles discriminants ; ne pas conclure à une cause certaine sur photo.
- Schéma/coupe : nommer les composants, relier les fonctions, suivre un trajet,
  puis expliquer les conséquences d'une modification.
- Plan : localiser un élément, justifier son repérage, exposer les informations
  manquantes ; ne pas inventer une précision absente du support.
- Graphique/tableau : lire une valeur avec ses unités, comparer les scénarios,
  puis identifier les hypothèses qui empêchent de généraliser.

Il s'agit d'alimenter les formats prévus par `PIPELINE.md`, pas d'ajouter ici
une mécanique d'apprentissage ni de revendiquer leur contenu comme livré.
Le contrat carte-v2 prévoit déjà `image` avec fichier, source, crédit, licence et alt ;
les exigences de géométrie/reprise ci-dessus ne sont pas toutes implémentées.

Contrôles d'intégration attendus : image absente, chargement hors ligne,
zoom/redimensionnement, rotation, zones sur mobile, navigation clavier,
alternative accessible, séparation question/correction. L'alternative ne
doit pas supprimer l'accès à l'information nécessaire ni dévoiler la réponse ;
si elle change la tâche, l'exercice adapté le déclare, sans fausse équivalence.
Les formats actifs éventuels doivent être assainis avant intégration.

## Coût et état présent

Le précédent prix estimé de transcription couvre l'entrée visuelle envoyée
au modèle et une sortie textuelle hypothétique. Il ne chiffre pas récupération
des fichiers, qualification des figures, données spatiales, adaptation,
création de supports, relecture ou tests de jeu. Enregistrer ces postes à part,
avec reprises et cache par empreinte du support. Aucun total multimédia mesuré.

Dans ce lot : protocole enrichi seulement. Pas de nouvelle extraction de
figure, annotation, image générée, intégration, publication ou appel API.
Prochaine preuve : produire un dossier complet figure → exercice dans une
unité usine, vérifier les droits et le rendu réel, puis étendre le benchmark.

Relecture documentaire indépendante : agent `revue_pipeline`, 06/09/2026,
aucun bloquant sur cette spécification. Rappel conservé : une licence de
réutilisation ne dispense ni de la doctrine de sources locales ni de
l'autorisation humaine de diffusion. Pas de validation de figure par cet avis.

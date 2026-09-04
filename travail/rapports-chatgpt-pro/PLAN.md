# Déroulement commun IFSI et copro

04/09/2026. Proposition d'exécution issue des
[rapports classés](README.md), de leur [tri critique](TRIAGE.md) et du
[troisième avis stratégique](STRATEGIE.md). Ce dernier avance la preuve
d'usage avant la refonte générale des contrats et des parcours.
Ce document ordonne les travaux ; il ne déclare pas les changements
terminés et ne remplace pas les cahiers de code.

## Ordre proposé

1. Terminer le lot IFSI déjà ouvert et corriger les assertions
   prioritaires copro. Réduire les pseudo-objectifs, conserver les
   branches ; aucune extension massive du programme.
2. Lever les défauts du client et du journal qui empêchent l'usage
   fiable, dans leurs chantiers existants. JB souhaite jouer sur le
   client v2 terminé : respecter la dépendance à `ACA-FRONT-2`.
3. Mesurer les séances sur l'existant avec `ACA-RITUAL-1`. Le gate
   actuel reste celui des trente séances et du test à froid ; les
   douze semaines du rapport ne deviennent pas un blocage supplémentaire.
4. Après ce bilan, construire un petit pilote AG avec seulement les
   extensions de contrat et de parcours qu'il exige. Puis vérifier le
   transfert au pilote IFSI et au dégât des eaux.
5. Généraliser les contrats, parcours et nouvelles branches seulement
   lorsque les pilotes montrent ce qu'il faut partager ou approfondir.

Le repérage des sources copro peut avancer pendant la finition IFSI.
Les lots L3 et L4 ci-dessous sont désormais limités au besoin du pilote ;
leur généralisation passe après sa preuve. Les gates existants de
`ACA-CONTENT-2` restent applicables : ce plan n'autorise pas à produire
des lots de cartes pendant le gate rituel ni à prétendre jouer pour JB.
Une erreur confirmée dans une carte effectivement servie devient
prioritaire, indépendamment de l'ordre des lots. Les deux métiers
partagent le moteur, mais leurs programmes restent distincts.

## Lots et preuves de sortie

### L0. Classer les rapports

État : originaux locaux conservés et empreintes contrôlées ; pivots et
fiches acceptés par l'usine ; variantes copro repérées. Index, tri et
plan écrits dans ce dossier. Les contrôles du dépôt sont consignés dans
le point de reprise IFSI après cette passe documentaire.

Périmètre : ce dossier, fiches locales des rapports et liens depuis la
roadmap et le point de reprise. Pas de génération de carte ou de cours.

### L1. Fermer l'intégration IFSI existante

État au terme de la reprise : terminé localement. 21 tests IFSI et
gates du dépôt verts ; 375 chapitres, 600 capacités de cadrage, rendu et
catalogue alignés. Les étapes ci-dessous conservent le périmètre du lot.

Cahier existant : [`ACA-IFSI-1`](../../chantiers/ACA-IFSI-1.md).
Le [point de reprise](../2026-09-04-revision-ifsi.md) donne les gestes
précis, les erreurs et le périmètre autorisé.

- D'abord un test rouge pour `legacy` vide sur un vrai ajout, et un
  refus sur un chapitre historique ; corriger `app/valide_ifsi.py`.
- Revoir les données de `programme/ifsi.json` : objectifs évaluables,
  étapes, difficulté, criticité, voies et limites de validation.
- Faire la relecture indépendante prévue par le cahier. Réduire les
  objectifs mécaniques inutiles plutôt que préserver leur nombre.
  Corriger les incohérences repérées, puis affiner les objectifs sur
  le pilote ; ne pas réécrire exhaustivement tous les chapitres.
- Rendre `SYLLABUS-IFSI.md` depuis le JSON, vérifier `--check`, aligner
  l'entrée IFSI du catalogue et les documents qui la décrivent.

Preuve : identifiants historiques et copie 2009 préservés, tests IFSI,
gates du dépôt et lisibilité du syllabus ; aucune carte clinique
annoncée produite. Les défauts existants restent consignés jusqu'à
preuve de leur résolution.

### L2. Corriger copro sur sources

Cahier écrit et enregistré : [`ACA-COPRO-1`](../../chantiers/ACA-COPRO-1.md).
Le [point copro](../2026-09-04-revision-copro.md) donne le traitement
des assertions : 34 chapitres précisés, cartes concernées corrigées,
quatre cartes conventionnelles signalées en attente de source. Les
389 identifiants sont conservés. La preuve de clôture figure dans ce
point lorsqu'elle est acquise ; aucune correction juridique ne repose
sur le seul rapport LLM. **Pause demandée par JB : relecture AG et avis
final sur le programme encore ouverts, puis banque locale à régénérer.**

Périmètre à inscrire : `programme/genere_copro.py`, `programme/copro.json`,
`SYLLABUS.md`, `PROGRAMME.md`, entrée copro de `programme/catalogue.json`,
tests de programme concernés, fiches de sources, et seulement les
chapitres/cartes dont l'impact est démontré. Préserver les corrections
locales de l'autre tâche et la décision 0030.

Deux gestes distincts :

- Tenir une table par assertion : formulation actuelle, source primaire,
  période et champ, verdict, nouvelle formulation, identifiants touchés.
- Rendre la correction durable : soit modifier la donnée portée par le
  générateur actuel, soit le convertir en lecteur du JSON après copie
  historique et test d'équivalence. Cette conversion n'est plus un
  préalable aux corrections ; ne la retenir que si elle simplifie un
  besoin concret du lot, sans mélanger architecture et faits juridiques.

Preuve : exemple calculé contradictoire pour chaque règle calculable,
contrôle des versions et exceptions, aucun identifiant perdu,
régénération reproductible, relecture fraîche des contenus touchés.
Vérifier séparément inventaire, brouillon et banque actuellement servie.
Une date ou un seuil non retrouvé reste un trou nommé.

### L3. Concevoir les données pédagogiques partagées

Dépendance : L1 et données copro suffisamment corrigées pour les exemples.
Périmètre réduit au pilote après bilan du rituel ; pas de refonte
générale préalable à l'usage. Utiliser d'abord les contrats existants.
Préparer décision, contrat et cahier avant d'étendre les valideurs ou le
moteur. Examiner `contrats/programme-v1.schema.json`,
`CONTRAT-CARTE-V2.md`, `app/valide_programme.py` et les contrats actuels.
Tenir compte de `ACA-CONTRAT-2`, encore ouvert : ne pas créer une
seconde migration concurrente.

Décrire sur les exemples AG et IFSI :

- objectif et preuve attendue ; étape du parcours, contexte, difficulté,
  criticité et portée de la validation ;
- source d'une assertion et période applicable, séparées du statut
  éditorial et de la confiance du joueur ;
- cas, documents fictifs, décisions, corrections et variante inédite ;
- remédiation d'une erreur critique et mesure locale des acquisitions ;
- preuves distinctes de rappel, discrimination, transfert et production ;
  conditions sans aide et avec outils, audit d'une réponse d'agent erronée
  comme variante sourcée, à justifier dans `METHODE.md` avant réalisation ;
- événements append-only nécessaires, sans score enregistré à part.

Preuve : le même contrat décrit les deux exemples sans champ de métier
codé en dur ; les fixtures invalides sont refusées, les anciennes données
restent lisibles. Chaque mécanique adoptée reçoit son entrée sourcée
dans `METHODE.md`. Un simple nom de format ne compte pas comme moteur
implémenté.

### L4. Construire les parcours lisibles

Dépendance : contrat minimal nécessaire au pilote (L3). Limiter d'abord
la réécriture aux missions du pilote ; étendre après son bilan.
Chaque parcours doit dire ce que l'élève saura faire, les situations
qu'il rencontrera, les connaissances à rappeler et ce qui reste hors de
la validation numérique.

IFSI : orientation et voies d'entrée, formation, prise de poste,
spécialités et approfondissements. Reprendre L1, sans le redessiner une
nouvelle fois au seul motif de partager le modèle.

Copro : découverte, prise de poste accompagnée, gestion courante,
situations complexes, spécialités et recherche. Distinguer salarié,
syndic bénévole et membre de conseil syndical dans les situations et
limites de rôle ; un niveau de jeu ne confère aucun pouvoir juridique.

Organiser l'entrée copro autour des documents, décisions, paiements,
alertes et transmissions, puis des cycles quotidien, annuel et
pluriannuel. Les compétences transversales sont réutilisées dans les
missions, pas recopiées dans chaque branche.

Preuve : chaque étape a des objectifs et des preuves, chaque ancien
identifiant reste retrouvé ou explicitement relié, aucun prérequis
parasite entre voies. Le premier parcours reste utilisable dans les
durées de séance prévues ; sa durée totale se calibre à l'usage, sans
adopter les quotas du rapport comme vérité.

### L5. Prouver la boucle complète avec des pilotes

Dépendances : bilan du rituel et gates de contenu existants, extensions
minimales de L3, parcours pilotes de L4, contrat de cartes applicable.
Pour la mesure réelle, le défaut de chronologie du journal signalé dans
le [point produit](../audit-froid-2026-09-04.md) doit être résolu par son
chantier `ACA-JOURNAL-SYNC-1`. Un prototype isolé peut avancer avant.

Ordre : AG complète, puis transfert au pilote IFSI diabète, puis dégât
des eaux pour éprouver davantage de contexte et de temporalité. Le
diabète reste le premier lot de contenu IFSI. Aucun dossier réel de
copropriété ni de patient ne sert de fixture.

Pour chaque pilote : problème initial, tentative sans aide et confiance,
recherche d'information ou recours aux outils,
production ou décision, retour expliqué et sourcé, rappel différé,
variante nouvelle, traitement d'une erreur critique. Les réponses
ouvertes sont bornées par une grille explicite ; ne pas promettre une
notation fiable d'actes cliniques ou professionnels non observés.

Preuve : parcours réellement jouable, cas tests corrects et erronés,
sources accessibles, sauvegarde/reprise, état recalculable depuis le
journal. Séparer contrôle logiciel, relecture du contenu et observation
d'apprentissage. Aucune rétention ni compétence professionnelle n'est
déclarée sans usage mesuré.

### L6. Étendre par les besoins et la veille

Dépendance : bilan des pilotes. Ajouter de nouvelles situations et de
nouvelles branches depuis les questions, la boîte et les sources. La
capacité d'extension ne signifie pas une fabrication autonome illimitée
ni une publication automatique.

Chaque lot possède un cahier, ses identifiants, ses sources, sa relecture
et ses preuves. Les changements réglementaires rouvrent les assertions
concernées ; les cartes périmées suivent le mécanisme de serviceabilité.

## Ce qui demande un arbitrage ultérieur

L'ordre ci-dessus, le classement et les préparations locales sont
réversibles. Pas besoin de redemander l'autorisation à chaque étape.
Une modification de la doctrine (verrou global, évaluation par un tiers)
n'est pas retenue dans ce plan. Les publications, suppressions, dépenses
et migrations irréversibles restent présentées à JB avec un résultat
concret et ses preuves. Aucun de ces actes n'est nécessaire au classement.

Les lots L2 à L6 sont des propositions à décliner en cahiers avant code,
pas de nouveaux items `ready` créés en masse dans la roadmap. L1 est
terminé ; préparer le cahier de corrections copro (L2) puis traiter les
défauts front/journal existants avant de mesurer les séances réelles.

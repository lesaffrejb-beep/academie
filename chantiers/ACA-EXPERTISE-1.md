# ACA-EXPERTISE-1 : construire les spécialisations sur des preuves

Demande de JB, 06/09/2026 : viser une compétence exceptionnelle au-delà
du droit courant du syndic, exploiter les documents fournis et le carnet
NotebookLM, rendre le travail reproductible.

## Première unité livrable

Une cartographie éditoriale des spécialités, reliée aux branches existantes,
avec productions attendues, lacunes et limites professionnelles. Un rapport
recalculable distingue programme prévu, cartes présentes dans l'artefact
local et études écrites. Il n'attribue aucun niveau acquis à un joueur.
Un dossier de reprise documente les trois PDF et le carnet accessible.

## Périmètre

`programme/specialisations/copro.json`, `app/couverture_expertises.py`, ses tests,
`app/tests.py`, `tooling/check.py`, `PROGRAMME.md`, `programme/README.md`,
`travail/expertise-2026-09-06/`, décisions et roadmap. Les limites des
trois entrées existantes de `sources/registre.json`
peuvent être précisés ; le registre lisible est régénéré, pas édité.
Les pivots restent traités par `app/usine/usine.py`, sans modifier ses états à la main.
Pas de changement des identifiants existants, pas de faux chapitres valides,
pas de publication ni de modification du partage NotebookLM.

## Tests rouges d'abord

- Une spécialité sans branche existante est refusée.
- Une carte du programme seul ne compte pas comme enseignement disponible.
- Les cartes d'un autre cursus ne gonflent pas la couverture copro.
- Un artefact absent reste inconnu, pas zéro et pas succès.
- Les preuves de production et les limites sont obligatoires.
- Le rapport reste déterministe et ne lit aucun état joueur.

## Suites, non terminées par cette première unité

1. Achever les unités de lecture des trois PDF ; fiches contrôlées,
   rattachements par passage et anomalies conservées.
2. Inventorier les sources du carnet avec occurrences distinctes ; obtenir
   les originaux exploitables sans confondre titres et texte intégral.
3. Produire trois dossiers transverses : rénovation patrimoniale, désordre
   technique contradictoire, copropriété fragile. Chacun exige des pièces
   fictives, leçons, exercices, corrigés sourcés et relecture indépendante.
4. Étendre spécialité par spécialité ; l'absence de manuel ou de licence
   se note, elle ne se maquille pas en couverture.

## Acceptation

Rapport généré, tests spécifiques puis `python3 app/tests.py`, ensuite
`python3 tooling/check.py`, avis indépendant et limites explicites.
La cartographie n'est ni un cours livré ni une certification de métier.

## Extension demandée par JB le 06/09/2026 : pipeline ouvert et coût

Demande explicite : comparer les méthodes PDF/OCR, tester, décider l'ordre
du PDF jusqu'aux cours/modules/exercices et permettre la reprise par d'autres
agents avec contrôles aléatoires. Ce lot ajoute dans
`travail/expertise-2026-09-06/` un banc d'essai autonome, ses tests et témoins,
une comparaison datée et un protocole d'audit. `METHODE.md` et une nouvelle
décision documentent la politique retenue. Les sorties intégrales restent
dans `sources/benchmark-pdf/` ignoré, sans dépendance ajoutée au produit.

Tests rouges : échec/outil absent ne devient pas succès ; erreur d'empreinte
interdit le test ; témoins positifs et négatifs ; comparaison respecte
unités/signes ; sondage reproductible sans doublons et hors pages imposées ;
jamais de pourcentage de fiabilité déduit d'une simple présence de mots.
Comparer les extracteurs déjà disponibles, et MarkItDown si une installation
locale isolée aboutit. Ne pas télécharger de gros modèles ni envoyer les PDF
à une API payante. Docling, Marker, MinerU et Firecrawl restent « non mesurés »
tant qu'ils n'ont pas réellement passé les mêmes témoins sur cette machine.

Les règles de routage sont actées ; leur automatisation dans l'usine exige
un lot ultérieur avec tests. Les contrôles existants ne sont pas assouplis.
L'unité Angers ouverte reste incomplète pendant cette comparaison : les
transcriptions intermédiaires sont sauvegardées, aucun sceau n'est revendiqué.

### Extension suivante : « Test tt les meilleurs options »

JB demande ensuite des essais réels des options structurées/OCR, pas seulement
une comparaison documentaire. Étendre le banc dans ce même dossier : Docling,
PyMuPDF4LLM, OCR local, Marker, MinerU et composants Firecrawl locaux selon
compatibilité. Téléchargements et environnements isolés autorisés par ce lot,
en vérifiant espace disque et ressources avant chaque famille ; aucun gros
téléchargement simultané. Arrêter avant de compromettre l'espace libre du Mac.
Conserver les échecs d'installation et d'exécution, non mesurés et limites.
Pas de service payant, d'envoi des PDF ou de cloud sans accord spécifique.

Les extractions Markdown brutes par page sont des preuves tierces, pas des
textes de l'application. Étendre l'exception typographique des pivots aux
seules pages `sources/benchmark-pdf/ESSAI/document-NNNN.md`, avec test rouge
de frontière et justification dans la décision 0047. Ne pas réécrire les
sorties ni exclure les rapports/cours des contrôles.

### Rappel produit de JB : images, schémas et exercices

Le protocole doit aussi qualifier figures, légendes, supports et données
spatiales d'exercice. `VISUELS.md` et décision 0048 définissent les preuves
attendues, limites des scores OCR et postes de coût distincts. Ce complément
documentaire ne crée ni assets, ni moteur d'annotation, ni autorisation de
diffuser les figures sources. La mise en œuvre suivra des tests rouges dans
un lot borné ; elle n'est pas déclarée réalisée par cette spécification.

### Pilote demandé ensuite : dix pages jusqu'au site

JB autorise un essai publié. Périmètre : Focus 106, pages PDF 13 à 22
incluses, déjà scellées par l'usine. Comparer Poppler et Docling/RapidOCR
sur ces mêmes pages ; conserver les sorties, empreintes, figures et arbitrages
face aux rendus. Le désaccord n'est pas résolu par vote majoritaire.
Ajouter `travail/pilote-renovation-10p/`, un chapitre satellite rattaché à
`travaux.renovation-globale.les-scenarios`, des schémas originaux dans
`banque/images/`, et son entrée dans `contenu/parcours.json`.

Le client doit afficher les supports dans Étude et rendre les parcours
supplémentaires accessibles. Le générateur rattache les cartes satellites
au seul métier de leur chapitre parent. Tests rouges : dix pages exactement,
empreinte erronée refusée, absence du support bloquante, média hors dossier
refusé, satellite exclu de l'autre cursus, module complet navigable.

Les sources sont des hypothèses de modèle datées de 2024, pas des prescriptions
techniques ni une promesse financière. Les visuels du PDF restent locaux ;
seuls nos schémas pédagogiques originaux sont distribués. Une relecture
indépendante précède le statut valide. Réponses libres : comparaison explicite
au corrigé et autoévaluation, sans prétendre à une correction IA.

Publication bornée autorisée par la demande : paquet isolé depuis HEAD avec
uniquement les fichiers du pilote ; aucune modification des comptes, de
l'API ni des migrations. Sauvegarde, empreintes et reprise du générateur
périodique exigées. Vérification locale puis publique ; toute barrière
d'authentification est rapportée sans prétendre avoir validé l'usage réel.

### Passe du 06/09 : collecte NotebookLM et essai de lundi

JB demande explicitement la collecte du carnet, des modules approfondis,
l'accès par pseudo, le graphe et la publication VPS, avec push sur main.
La collecte conserve localement texte brut, références des images, occurrences,
empreintes et erreurs ; une capture n'est pas une lecture validée. Les pièces
client et sources ambiguës restent exclues du dépôt. Les doublons ne sont
fusionnés qu'après comparaison de contenu. Les ressources sources ne montent
pas au VPS. La publication autorisée concerne le produit et les cours relus.

Périmètre complémentaire : `travail/modules-experts-2026-09-06/`, rapport de
collecte, `chapitres/satellites/contre-expertise-renovation.json`, parcours
rénovation, preuves et décision 0050. Le nouveau module utilise le Focus déjà
scellé, des cas fictifs et un support original existant ; relecture indépendante
avant promotion. Les autres brouillons restent exclus tant que les assertions
ne sont pas confrontées à leurs passages. Contrôle de contrat et parcours
navigable requis, avec sauvegarde de la réponse et du retour par compte.

Le catalogue `programme/catalogue.json` accompagne les modules ajoutés : ses
compteurs suivent les cartes et études effectivement générées. Les formats
interactifs déjà présents en Séance peuvent être réutilisés dans Étude avec
le même journal de tentative, sans nouveau mécanisme ni double média.
La génération `app/genere.py` doit transporter les champs publics structurés
`paires` et `etapes` jusqu'au client ; `app/tests_chaine.py` vérifie cette
jointure avant publication. Sans ces supports, les exercices reviennent
à une réponse libre et ne rendent pas l'interaction pourtant préparée.

Le même périmètre comprend l'alignement de `contrats/carte-v2.schema.json`
et `CONTRAT-CARTE-V2.md` sur ces supports déjà utilisés par le client :
`paires` en objets gauche/droite, `etapes` en objets num/titre/cible.
`app/valide_chapitres.py` contrôle ces champs facultatifs quand présents,
avec tests rouges puis verts dans `app/tests_chapitres.py` : listes non
vides, textes non blancs, numéros entiers positifs uniques, cible booléenne
facultative, au plus 26 paires (identifiants du client de a à z). Aucune
migration ni modification du journal ou des questions n'est nécessaire.

Preuve navigateur complémentaire : `web/tests/e2e/contre-expertise.spec.ts`
parcourt le pilote puis ouvre la contre-expertise par Continuer le parcours.
Elle vérifie tentative, sept exercices existants, sources, schéma chargé,
brouillon après rechargement et synthèse avec critères conservés dans le
journal du compte fictif. Cette preuve de front n'est ni une mesure de
compétence ni une preuve de synchronisation d'un compte réel sur le VPS.

### Suite : fragilité et façade ancienne

Les dossiers transverses demandés sont poursuivis dans
`travail/fragilite-2026-09-06/` et `travail/facade-2026-09-06/`.
Après confrontation des assertions aux passages des pivots déjà scellés et
relecture par un agent distinct, leur intégration peut ajouter
`chapitres/satellites/diagnostic-partage-fragilite.json` et
`chapitres/satellites/facade-ancienne-avant-devis.json`, les entrées de
`contenu/parcours.json`, les compteurs du catalogue et les artefacts générés.
Les brouillons initiaux et les réserves restent conservés sous `travail/`.

Le diagnostic de fragilité distingue les dimensions du guide Anah des
hypothèses du cas fictif ; il ne couvre pas les conditions des dispositifs
judiciaires. La façade ancienne confronte des observations, matériaux et
propositions d'intervention ; les recommandations patrimoniales datées ne
deviennent pas des prescriptions techniques ou juridiques universelles.
Pas de nouvelle mécanique ni de reproduction d'une figure source.

Preuve d'intégration, rouge avant ajout puis verte après : un élève copro
ouvre chaque nouveau parcours depuis l'accueil, retrouve les sources,
termine les exercices effectivement servis et reprend ses réponses après
rechargement. La synthèse et ses critères cochés restent dans son journal ;
le parcours IFSI n'affiche pas ces études. Les tests correspondants peuvent
être ajoutés sous `web/tests/e2e/`. Les validations globales précèdent le
push ; installation VPS et usage sur les appareils restent des preuves
distinctes.

La relecture du rôle Fragilité révèle une perte de contexte dans
`web/src/ecrans/ModulesSeance.tsx` : la première citation du personnage est
copiée seule, sans situation ni consigne. Le rôle doit afficher et copier
le scénario complet (question), y compris sans guillemets. L'aide reste
derrière la demande d'indice pour ne pas créditer un rappel autonome aidé. Une
citation peut encore identifier l'interlocuteur quand elle le nomme
explicitement. Test rouge de contexte, test sans citation, puis vérification
du presse-papiers dans le parcours Fragilité ; aucune conversation automatique
ni modification des réponses du journal.

Le panneau Sources d'Étude doit aussi restituer le parti déjà fourni par
chaque source, conserver une nature absente comme inconnue et ne pas
qualifier toutes les publications de règles. Ajustement borné à
`Etude.tsx`, au type `Source` et aux tests de rendu : un éditeur commercial
ne devient pas une institution, une source sans nature ne reçoit pas une
qualification inventée. Aucun changement du schéma de banque.

Contrôle final de l'arbre : la génération transmettait les cartes satellites
à leur cursus mais omettait leurs nœuds. Corriger `app/genere.py` et les
tests de chaîne/études pour ajouter les satellites dont l'étude est servie,
avec leur rattachement déclaré, uniquement dans le programme du parent.
Les brouillons, périmés, études écartées et autres cursus restent exclus.
Conserver les prérequis tels qu'écrits, sans convertir le rattachement en
prérequis. Le client (`progression.ts`, `graphe.ts`, `GraphePrerequis.tsx`,
types et tests associés) rend séparément rattachement et approfondissements.
Preuve rouge puis verte : parent réel du programme, module satellite
visible, ouverture de son étude depuis le graphe, absence dans l'autre
cursus. Les compteurs du programme gardent le socle distinct des extensions.

### Preuve concrète demandée par JB : une branche électrique illustrée

JB demande où en sont réellement la collecte, les notions et le programme,
puis un exemple complet qui comble un manque d'illustration. La branche
`equipements.electricite` possède cinq chapitres prévus ; aucun cursus
professionnel d'électricien n'est déclaré livré. Ce lot ajoute une première
étude de fondations, sans prétendre remplir tout le chapitre TGBT ni former
à l'exécution de travaux électriques.

Périmètre : `travail/preuve-concrete-2026-09-06/`,
`chapitres/satellites/comprendre-protections-electriques.json`,
`banque/images/electricite-*.svg`, `contenu/parcours.json`,
`programme/catalogue.json`, registre de sources si nécessaire, banque générée,
`web/tests/e2e/electricite.spec.ts`. Rattachement au chapitre existant
`equipements.electricite.tgbt-et-colonnes-montantes` sans inventer de prérequis.
Les PDF publics originaux restent hors dépôt, avec empreintes et pagination.
Lecture par unités usine, portée et limites conservées, relecture distincte
avant promotion. Les schémas originaux expliquent les mécanismes sans donner
un plan de câblage ; les exercices utilisent des cas fictifs.

Preuve rouge puis verte : étude absente avant ajout, présente ensuite avec
ses supports chargés ; sources paginées accessibles, réponse conservée après
rechargement, exercice visuel réellement parcouru et étude exclue d'IFSI.
Un état avant/après distingue collecte, lecture contrôlée, cours servis,
publication et apprentissage constaté. Aucun score de maîtrise n'est déduit
du nombre de cartes. Les mécanismes déjà présents sont réutilisés.

Visibilité du contenu disponible : `web/src/ecrans/Arbre.tsx`, son test SSR
et le libellé de la miniature dans `web/src/ecrans/GrapheSavoir.tsx`
distinguent chapitres prévus du socle, études effectivement disponibles
et approfondissements. Aucun total d'études incluant les satellites n'est
rapporté au seul nombre de chapitres du socle. Les conditions existantes
de serviceabilité restent la référence ; ni programme ni état joueur ne
changent. Preuves ciblées dans `travail/preuve-concrete-2026-09-06/`.

La visibilité demandée inclut `web/src/ecrans/Arbre.tsx` et ses tests :
séparer le socle prévu, les études réellement disponibles dans ce socle
et les approfondissements, sans compter les satellites dans un taux du
socle. Régression rouge sur un exemple mêlant socle et satellite, puis
contrôle ciblé et rendu réel. Pas de pourcentage de compétence acquis.

### Demande vers chemin d'apprentissage, professeur ancré dans la copro

JB précise le 06/09 : partir de « je veux apprendre X », de ce qu'il sait
ou reste à diagnostiquer, puis construire un chemin raisonné vers X, avec
ramifications sans plafond et rattachement au métier de gestionnaire.
Le professeur est l'agent qui instruit la demande ; le script contrôle
la cohérence et les références, sans prétendre remplacer ce jugement.

Périmètre supplémentaire : `CHEMINS.md`, `prompts/construire-un-chemin.md`,
`app/chemin_apprentissage.py`, `app/tests_chemin_apprentissage.py`,
`app/tests.py`, `contrats/chemin-apprentissage-v1.schema.json`,
`METHODE.md`, décision suivante et son index, exemples et preuves sous
`travail/preuve-concrete-2026-09-06/`, lien README. Aucun appel de modèle
depuis le serveur, aucune modification ou invention d'état joueur.

Le dossier contient demande, cible observable, ancrage réel dans le cursus,
préacquis connus/inconnus et leurs preuves, diagnostic et bifurcations,
étapes avec niveau justifié, dépendances et transversalités, inventaire de
sources présentes ou à trouver, supports et exercices justifiés, critères
de transfert et reprise après échec. Les nouveaux chapitres sont des
propositions jusqu'à leur fabrication et leur relecture. Un format varié
ne vaut pas apprentissage, un plan cohérent ne vaut pas cours disponible.

Tests rouges : référence de chapitre ou source inventée, cycle entre étapes,
acquis observé sans preuve, source annoncée présente sans original identifié,
étape dite disponible sans étude servie, transfert absent, diagnostic sans
suite définie. Un exemple électrique réel et un exemple fictif d'élève
avancé montrent deux chemins sans attribuer ces acquis à JB. Contrôles
locaux et revue indépendante avant commit, sans publier de données joueur.

Routage documentaire autorisé pour rendre le protocole retrouvable : ajout d’un lien dans `AGENTS.md` vers `CHEMINS.md` et le prompt, sans modifier les règles dures.

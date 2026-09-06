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

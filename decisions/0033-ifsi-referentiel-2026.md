# 0033. IFSI : une entrée juste et une progression sans plafond

Date : 04/09/2026. Demande de JB : appliquer la critique du programme,
puis précision : « entrée en école infirmier puis infirmier puis que ça
ne s'arrête jamais ». Décision locale prise dans cette délégation.

## Décision

Le programme conduit à l'admission, accompagne la formation infirmière,
puis continue par la pratique, les spécialités, les controverses et la
recherche. Il n'a pas de dernier niveau qui clôt l'apprentissage.

1. `programme/ifsi.json` est désormais la source éditable. Le générateur
   lit ce fichier, le contrôle et produit seulement `SYLLABUS-IFSI.md`.
   Il ne réécrit plus les données depuis des constantes Python.
2. La copie exacte du squelette précédent vit dans
   `programme/versions/ifsi-2009.json`. Elle conserve ses limites et ne
   devient pas, par cette copie, un programme historique certifié.
   Les identifiants des chapitres existants restent stables.
3. Le programme courant vise les entrants de septembre 2026. Les
   étudiants entrés auparavant restent dans le cadre 2009 ; les reprises
   et redoublements relèvent de l'examen prévu à l'article 60. Les codes
   A à E sont ceux des domaines d'enseignement ; les domaines de
   compétences numérotés ne sont pas confondus avec eux.
4. Parcoursup, formation professionnelle continue et accès spécifiques
   ont des préparations distinctes. Le choix de voie ne préjuge pas
   l'admissibilité individuelle, à confirmer auprès de l'établissement.
5. Chaque chapitre a une étape, une difficulté et une criticité
   distinctes, des capacités de cadrage et un rattachement aux compétences.
   Ce rattachement est une proposition éditoriale, pas une équivalence
   officielle. Les anciennes UE restent dans `legacy`. Les UE actuelles
   non établies restent vides plutôt que d'être inventées.
   L'étape est un premier point d'appui éditorial, non exclusif ; elle
   ne précède pas celle d'un prérequis. Les objectifs sont affinés avec
   les supports et les preuves du pilote, sans déclinaison automatique
   d'un objectif par notion. Un ajout explicite l'absence d'historique
   par `legacy: {niveau: null, titre: null, ue_ids: []}` ; les chapitres
   anciens conservent leurs métadonnées d'origine.
6. `niveau` reste une compatibilité avec le programme v1. Il ne signifie
   plus « admis », « diplômé » ou « expert ». Doctrine et Frontière
   deviennent aussi des modes transversaux. Le chapitre reste l'unité
   éditoriale et la carte l'unité de mémoire ; les objectifs fins
   préparent une mesure ultérieure de maîtrise, sans la simuler.
7. Une réussite numérique vérifie des connaissances et du raisonnement.
   La simulation et le geste clinique supervisé restent distincts.
   Aucun score de l'application ne devient une habilitation ni une
   validation de stage. Les objectifs sensibles portent cette limite.
8. Les spécialités réutilisent le socle et ouvrent des approfondissements.
   Une version possède un inventaire fini et contrôlable ; les versions
   suivantes ajoutent des chapitres, des cas et des branches sourcés.
   « Sans fin » signifie apprendre plus, maintenir ses acquis et explorer
   d'autres domaines, avec la boîte et la veille déjà prévues par la doctrine.

Les points 1, 3 et 4 remplacent les choix correspondants de
`0031-un-programme-par-metier-ifsi.md`. La conception commune aux autres
métiers, les journaux et le moteur ne changent pas dans ce lot.

## Sources et portée

- [Arrêté du 20 février 2026, article 60](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570487) : cohortes et dispositions transitoires.
- [Article 59](https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000053569008) : abrogation du texte de 2009 au 30 juin 2030.
- [Annexe I](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570495) : compétences.
- [Annexe III](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570499) : enseignements et progression clinique.
- [Article 12](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570385) : sélection en formation professionnelle continue.

Textes consultés le 04/09/2026. Ils fondent l'indexation réglementaire,
pas la justesse clinique de futures cartes. Les choix de granularité et
de navigation sont des choix de conception demandés par JB.

## Conséquences

Le cahier `ACA-IFSI-1` corrige le programme et ajoute les contrôles.
Le nombre de chapitres décrit un inventaire, jamais un apprentissage
mesuré. Aucun contenu n'est rendu jouable par cette révision. Le futur
pilote diabète reliera calcul, surveillance, communication et sortie,
avec des cas fictifs et des références vérifiées avant toute réponse.

## Réouverture

Une évolution réglementaire, une incohérence révélée par un formateur
ou une difficulté observée chez un apprenant déclenche une nouvelle
version. La profondeur des branches reste ouverte ; les anciennes
versions et les identifiants permettent de suivre ce qui a changé.

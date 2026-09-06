# programme/

Depuis le 06/09/2026, `specialisations/copro.json` décrit les spécialisations
transversales à construire (décision 0046). Ce n'est pas une banque ni une
preuve de couverture. `python3 app/couverture_expertises.py --write`
recalcule leur [inventaire](../travail/expertise-2026-09-06/COUVERTURE.md).
Les objectifs ne sont jamais déclarés acquis à partir d'un simple rattachement.

Le programme d'un métier en données : `copro.json` pour le gestionnaire
de copropriété. `catalogue.json` liste les parcours proposés à l'arrivée
(`COMMENCER.md` §2) ; ses compteurs se mettent à jour à chaque lot de
chapitres. Un fichier courant par métier : `ifsi.json` (infirmier,
source éditable de `genere_ifsi.py`, lisible dans `../SYLLABUS-IFSI.md`,
`decisions/0033`). Le texte lisible copro est `../PROGRAMME.md` ; quand les deux
divergent, **le JSON fait foi** et le texte se corrige.

Ce que porte le fichier :

- `domaines` : clé, titre, ordre, niveau attendu au socle, sources
  primaires, `arbre: false` pour Culture ;
- `branches` : par domaine, avec leur ordre et leur exercice dominant ;
- `chapitres` : identifiant `domaine.branche.chapitre`, titre, niveau
  1-5, prérequis (identifiants de chapitres, y compris d'autres
  domaines), exercices attendus, sources primaires attendues, et un
  `statut` du contenu : `a-ecrire`, `brouillon`, `valide` ;
- `socle` : la liste des domaines et niveaux qui définissent le socle ;
- `positionnement` : la répartition des vingt questions du quiz ;
- `semaine_type` : la couleur des jours par défaut.

## Programme infirmier courant

`ifsi.json` porte le référentiel DEI-2026 et les liens officiels datés.
Le squelette précédent est conservé à l'identique dans
`versions/ifsi-2009.json`, sans devenir une référence clinique validée.
Le valideur courant ne le mélange pas aux parcours proposés.

Chaque chapitre courant possède un rattachement pédagogique aux
compétences, une étape de formation, une difficulté, une criticité,
des objectifs fins et une limite explicite de validation numérique.
L'ancien niveau, le titre et les UE historiques sont conservés dans
`legacy`. Le rattachement est une proposition éditoriale. Une liste
d'UE vide signifie que l'affectation fine reste à établir.

Pour un ajout sans prédécesseur, `legacy` porte explicitement un titre
et un niveau nuls, et aucune UE. Ce cas est refusé sur un chapitre
historique. L'étape est un premier point d'appui, non exclusif, qui ne
précède pas celle de ses prérequis. Les objectifs de cadrage sont affinés
sur les supports et les preuves du pilote ; les notions ne deviennent
pas automatiquement chacune un objectif supplémentaire.

`parcours` sépare Parcoursup, FPC et accès spécifiques. Le diagnostic
et les semaines renvoient aux identifiants de chapitre. Un prérequis
indirect ne doit pas réintroduire une autre voie ou un exercice
facultatif dans un parcours obligatoire.

L'arbre continue après le diplôme : prise de poste, spécialités,
approfondissements et recherche. `specialisations` réutilise les
chapitres communs, la boîte et la veille apportent de nouvelles
branches. Une version est inventoriable ; l'apprentissage n'a pas de
plafond. Les données pédagogiques du futur moteur de cas sont des
spécifications, pas des fonctionnalités déjà actives.

`python3 programme/genere_ifsi.py` rend le syllabus après contrôle,
sans modifier le JSON. `python3 programme/genere_ifsi.py --check`
refuse un syllabus périmé sans écrire. `app/valide_ifsi.py` complète
les contrôles généraux ; `app/tests_ifsi.py` verrouille également la
copie historique et la stabilité des identifiants.

## Contrat commun et historique copro

Ce que le fichier n'est pas : une banque. Il ne contient ni leçon ni
carte. Le moteur ne le lit pas encore. Depuis le 03/09, `app/valide_programme.py`
(chantier `ACA-PROGRAMME-1`) le valide et le confronte à `academie.json`
(mêmes clés, même ordre, même statut hors arbre) ; `tooling/check.py`
l'appelle. Ce fichier est donc un contrat, plus un brouillon. Les niveaux
ont été calibrés par deux agents frais le 03/09
(`travail/calibrage-programme-2026-09-03.md`).

État au 02/09/2026 : `copro.json` porte les dix domaines et Culture,
leurs branches et 371 chapitres (niveaux 1 à 3 pour chaque branche,
19 chapitres de niveau 4 et 2 de niveau 5 comme portes d'entrée), tous
en statut `a-ecrire` ; le chantier de migration assignera en
`brouillon` ceux que la banque actuelle couvre. Les niveaux 4 et 5 se
font pousser par la boîte. Les prérequis suivent une règle simple : un
chapitre de niveau n requiert les chapitres de niveau n-1 de sa branche,
plus les ponts nommés vers d'autres domaines (les cas transverses).

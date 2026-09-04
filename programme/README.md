# programme/

Le programme d'un métier en données : `copro.json` pour le gestionnaire
de copropriété. `catalogue.json` liste les parcours proposés à l'arrivée
(`COMMENCER.md` §2) ; ses compteurs se mettent à jour à chaque lot de
chapitres. Un fichier par métier : `ifsi.json` (infirmier, généré par
`genere_ifsi.py`, lisible dans `../SYLLABUS-IFSI.md`, `decisions/0031`). Le texte lisible est `../PROGRAMME.md` ; quand les deux
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

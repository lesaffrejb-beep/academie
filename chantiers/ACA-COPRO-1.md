# Cahier ACA-COPRO-1 : corrections copro sur sources

Demande de JB du 04/09/2026 : poursuivre le plan commun après classement
des trois rapports et finition IFSI. Lot L2, local et réversible.
Déclaration : Codex, gpt-5.6-sol, grand, enregistrée par l'usine sur
le rapport copro `a708271c820f9311` ; ses unités et sa fiche sont acceptées.

## Résultat

Corriger les assertions confirmées du rapport dans l'inventaire et les
cartes existantes. Conserver les 389 identifiants et la génération actuelle.
Nommer les limites de source ; suspendre une carte erronée ou invérifiable
avec des seuils sans source retrouvée plutôt que la servir comme vérifiée.
La relecture porte sur les retouches, pas sur tout le droit de la copropriété.

## Périmètre

- `programme/genere_copro.py`, `programme/copro.json`, `SYLLABUS.md`,
  `PROGRAMME.md`, entrée copro de `programme/catalogue.json` ;
- cartes existantes concernées dans `banque/droit/majorites.json`,
  `banque/droit/veille-recente.json`, `banque/droit/conformite-annuelle.json`,
  `banque/sinistres/sinistres.json` ; brouillon
  `chapitres/droit/majorites/l-article-24.json` ;
- `app/tests_copro.py`, inscription dans `app/tests.py`, ajustement des
  attentes de compte dans les tests existants si la suspension les change ;
- `sources/registre.json`, son rendu `sources/REGISTRE.md` si un domaine de
  source manque ; `site/banque.json` régénéré localement ;
- ce cahier, `roadmap.json`, `ROADMAP.md`, `README.md`,
  `travail/2026-09-04-revision-copro.md`,
  `travail/rapports-chatgpt-pro/PLAN.md`, `TRIAGE.md`,
  `travail/rapports-chatgpt-pro/copro-*.md`, `copro-*.json`.

Pas de changement de moteur, de format pédagogique, de programme IFSI,
de front, de journal, de service ou de publication. Préserver tous les
travaux locaux préexistants. Les titres qui forment les identifiants
restent stables ; une terminologie historique s'explique dans la capacité.

## Étapes et preuves

1. Vérifier les faits dans les sources primaires, par groupes indépendants.
   Garder l'original du rapport distinct de la table de corrections.
2. Écrire puis constater les tests rouges : corrections persistantes après
   génération, identifiants conservés, catalogue aligné sur l'inventaire et
   les cartes effectivement sélectionnées, exclusion des cartes signalées.
   Les tests éditoriaux repèrent une régression, ils ne prouvent pas la loi.
3. Corriger les données du générateur, les cartes et le brouillon article 24.
   Chaque retouche de carte conserve son identifiant et son origine et porte
   la date, l'auteur de correction, les sources et une relecture indépendante.
   Une carte signalée n'est pas déclarée revérifiée. Les brouillons restent
   brouillons. Les exemples chiffrés contradictoires sont consignés dans
   la table de revue, sans créer un moteur juridique.
4. Régénérer les artefacts locaux ; aligner les compteurs et la documentation.
   Conserver les estimations pédagogiques comme telles. Tenir la table avec
   assertion initiale, source, période/champ, formulation et fichiers touchés.
5. Relecture par un agent qui n'a pas écrit les retouches ; corriger ses
   réserves. Vérifier les identifiants, les contrats et la reproductibilité,
   puis `python3 app/tests.py` et `python3 tooling/check.py`.
6. Consigner le résultat local, les limites et le prochain lot. Aucune
   publication ni promotion des brouillons v2 dans ce chantier.

Les documents produits sont des décisions éditoriales et des preuves de
contrôle, pas des sources juridiques à substituer aux textes officiels.

## Pause du 04/09/2026

Arrêt demandé par JB pendant l'étape 5. Les retouches sont sur disque ;
relecture AG, avis final sur le programme et traçabilité finale encore
ouverts. Lire `travail/2026-09-04-revision-copro.md` avant toute reprise.
Le chantier reste `ready`, pas `done`. Ne pas régénérer ou publier les
dernières retouches comme si leur relecture était achevée.

# chapitres/

Les chapitres v2 (`CONTRAT-CARTE-V2.md`, `contrats/chapitre-v1.schema.json`),
un objet par fichier, `chapitres/<domaine>/<branche>/<slug>.json`,
l'identifiant du chapitre étant `domaine.branche.slug` et devant exister
dans `programme/copro.json`.

Jugés par `app/valide_chapitres.py` (écrit le 03/09/2026), lancé par
`app/tests.py` et `tooling/check.py`. Un chapitre ou une carte ne se joue
que `valide`, et `valide` exige `verifie_par` (double passe par un agent
frais qui n'a pas écrit).

La banque v1 (`banque/`, tableaux de cartes) reste jugée par
`app/valide_banque.py` ; les deux dispositions coexistent jusqu'au
chantier `ACA-CONTRAT-2`, qui migre v1 dans v2 et fait de ce dossier la
seule banque.

Depuis le 03/09/2026 au soir (ACA-CONTRAT-2 étape 3), `genere.py` lit ce
dossier et sert ses cartes à côté de celles de `banque/`. Trois règles
valent la peine d'être connues avant d'écrire un chapitre ici :

- **Le juge est `valide_chapitres.py`**, pas `genere.py`. Une erreur du
  valideur et rien ne se publie, comme pour la v1.
- **Un chapitre `brouillon` ne se joue pas, ses cartes `valide` et
  relues si.** C'est la règle de transition du cahier, datée : elle
  évite que migrer la banque prive JB de son contenu vérifié tant que
  les leçons ne sont pas écrites (ACA-CONTENT-2), et elle se retire à
  ce moment-là. Un chapitre `signale` ou `perime`, lui, emporte toutes
  ses cartes : c'est la leçon qui est en cause.
- **Le champ `contrat` de `site/banque.json` bascule tout seul.** Il
  vaut `carte-v2` le jour où plus aucune carte ne vient de `banque/`,
  et reste absent avant : le client lit alors `carte-v1`
  (`CONTRAT-CARTE-V2.md` §5.4). Annoncer `carte-v2` sur un lot qui
  porte encore des cartes sans `chapitre` ni `provenance` serait un
  mensonge que le client paierait à l'écran. Personne n'a de drapeau à
  penser à lever : la fin de la migration flippe le contrat.

Au 03/09/2026, les 11 cartes d'ici sont `brouillon` : elles se jouent en
`--avec-brouillons`, pas en production. La banque servie n'a donc pas
changé d'un octet le jour où `genere.py` a commencé à lire ce dossier.

Premiers chapitres écrits le 03/09/2026 par le modèle (provenance sur
chaque carte), relus par des agents frais le même jour : voir
`travail/lot-pilote-2026-09-03.md`.

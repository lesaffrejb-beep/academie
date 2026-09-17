# ACA-PRECOMMIT-1 : garde-fou pré-commit contre la règle 1

Créé le 17/09/2026, depuis l'entrée « À CREUSER » du 15/09/2026 dans
`IDEES-EN-VOL.md` : « Un garde-fou pré-commit contre la règle 1 (données
client, pièces, contacts) ». La règle 1 d'`AGENTS.md` (« aucun contact,
immeuble, contrat, mail, réunion ou document client ») ne repose
aujourd'hui que sur la discipline ; `check.py` ne regarde que l'ancien
couplage technique et les imports de labor, jamais les données elles-mêmes.

## Résultat

Un hook git `pre-commit` local scanne ce qui est sur le point d'entrer :
les lignes ajoutées par le diff stágé. Un motif de donnée client
(email, téléphone français, SIRET, IBAN, mention labor) bloque le commit
avec un message qui cite la règle 1 et dit quoi faire.

## Ce qui est tranché

- **Pré-commit, pas serveur ni CI.** La donnée doit être vue là où elle
  arrive, sur la machine qui l'a lue. `etat/` est hors git depuis la
  conception ; le garde ne sert rien au serveur.
- **Le hook est local et contournable** (`git commit --no-verify`).
  Le garde-fou ne décide rien d'irréversible : il bloque, il ne supprime
  ni ne réécrit. JB peut le désactiver ; être passé sans lui est un choix
  humain, pas une dérive du script.
- **Détection prudente, pas exhaustive.** Motifs génériques (email,
  téléphone FR, SIRET, IBAN, chemins de labor), pas un catalogue de
  parties (le nom d'un immeuble n'est pas devinable). Un chiffre, une
  adresse, un nom sans motif regex passe ; le garde est un filet, pas un
  valideur, et l'avoué reste la responsabilité de l'agent qui code.
- **Le hook scanne le diff instancié, jamais l'historique** ; `git
  diff --cached` seul. Les mail du passé ne sont pas re-ouverts.

## Ce qu'on ne fait pas

- Ne remplacer la règle 1 de la discipline par une machine ; ne promet
  la conformité. Le garde détecte, il ne certifie pas.
- Ne scanner le contenu des fichiers existants (le diff seul).
- Des erreurs brutes au joueur : chaque alerte dit LE motif et LE fichier.

## Étapes du chantier

1. `app/tests_garde.py` : tests rouges (fixtures assemblées à l'exécution
   pour que le dépôt lui-même n'entre jamais une chaîne client brute).
2. `app/garde_confidentialite.py` (Python pur, stdlib) ;
   `alertes(diff_texte)` et `scan_stage()`.
3. `app/installation_precommit.py` installe le hook (`.git/hooks/pre-commit`)
   et l'installe ici (idempotent).
4. `check.py` : le hook existe et appelle le garde (contrôle mécanique).

## Preuve

`python3 app/tests.py` puis `python3 tooling/check.py` verts, y compris
la mutation du garde. Un test manuel : `git add` d'un fichier porteur
d'un fichier fictif d'essai → commit refusé, message correct ;
`--no-verify` passe bien.

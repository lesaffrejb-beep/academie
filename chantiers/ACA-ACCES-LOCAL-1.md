# Cahier ACA-ACCES-LOCAL-1 : accès sans mail et reprise autonome

Résultat attendu : les quatre joueurs créent un compte avec un pseudo
unique et une phrase secrète, conservent une clé de récupération affichée
une fois, et peuvent changer leur phrase avec pseudo plus clé sans mail
ni intervention de JB. La perte de la phrase et de la clé est dite avant
la fin de la création. Les comptes d'essai distants existants peuvent être
supprimés dans une opération locale explicitement confirmée.

Dépend de : ACA-ONBOARDING-1. Bloque : rien.

## Périmètre

Peut modifier : `serveur/academie_etat/`, `serveur/migrations/`,
`serveur/tests/`, `serveur/API.md`, `serveur/README.md`, `serveur/schema.sql`,
`web/src/app/compte.*`, `web/src/donnees/api.ts`,
`web/src/ecrans/Arrivee/`, `web/tests/onboarding/`, `decisions/`,
`roadmap.json` et `ROADMAP.md`.

Ne touche pas : le moteur, la banque, le format du journal, les cursus,
les sources et les données locales des navigateurs.

## Déjà tranché

- Pseudo unique plus phrase secrète, pas de mail.
- Clé aléatoire de 128 bits, affichée une seule fois et hachée avec scrypt.
- Pseudo plus clé permet une nouvelle phrase, invalide les sessions et
  remplace la clé.
- Sans phrase et sans clé, aucune récupération n'est possible.
- La purge des comptes ne s'exécute que par une commande locale avec la
  confirmation littérale `SUPPRIMER LES COMPTES`.

## Étapes

1. Tests rouges : pseudo et phrase requis, aucun secret dans SQLite,
   pseudo dupliqué refusé, connexion générique, récupération qui remplace
   clé et sessions, réinitialisation confirmée seulement.
2. Migration, API et commande de purge ; aucun lien magique ou mail dans
   le parcours courant.
3. Écran de création, conservation unique de clé, connexion et retour par
   clé, avec avertissement d'irréversibilité.
4. Tests navigateur : création, conservation de clé, reconnexion,
   récupération et refus d'une clé remplacée.

## Preuve

```bash
cd serveur && python3 -m unittest discover tests
cd web && npm test -- --run
python3 app/tests.py && python3 tooling/check.py
```

La publication et l'exécution de la purge sur le VPS restent un geste
humain distinct.

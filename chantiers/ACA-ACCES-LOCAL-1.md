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

## Extension demandée par JB le 06/09 : entrée du petit groupe

Outil : Codex ; modèle : GPT-6. Le groupe initial choisit son pseudo dans
une liste, puis saisit son mot de passe. L'inscription propose le cursus
avant la création ; le choix reste écrit dans le journal append-only après
conservation de la clé. Un pseudo masqué reste accessible par saisie.

Le périmètre couvre aussi l'annuaire de connexion dans l'API et son client,
les tests de projection de l'identité locale et les tests navigateur. Aucun
compte ni ancien journal n'est supprimé et aucune migration n'est nécessaire.

Preuves supplémentaires, tests rouges avant correction :

- L'annuaire sans session ne livre que pseudo de connexion et nom affiché
  des comptes visibles, sans identifiant, cursus, réponse, secret ni profil
  technique ; masquages et suppression retirent l'entrée.
- Cliquer son pseudo puis saisir son mot de passe reconnecte le bon compte.
- Choisir son cursus pendant l'inscription ouvre ce cursus après conservation
  de la clé, et le journal distant conserve le choix.
- La clé ne reste jamais dans le stockage navigateur et l'écran de conservation
  reste affiché lors d'une récupération d'un compte ayant déjà un cursus.

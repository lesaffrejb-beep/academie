# Cahier ACA-ONBOARDING-1 : l'arrivée d'un élève

Réécrit le 04/09/2026 sur l'arbitrage `decisions/0032`.

Résultat attendu : dans le client v2, un nouvel élève crée son compte
(mail professionnel, mot de passe), choisit un pseudo, choisit un cursus
dans le catalogue (`programme/catalogue.json` : copropriété, infirmier),
ou dépose une demande de nouveau cursus à Jean-Baptiste (sa situation,
pourquoi), puis passe au quiz de positionnement du cursus choisi. Un
seul cursus à la fois, relié au profil, sauvegardé par le journal ;
tout dans la voix de `VOIX.md` (`contenu/voix.json`, clés `arrivee.*`).
Fini quand : les tests nommés ici sont verts, plus tests.py et check.py.
Dépend de : ACA-FRONT-2, ACA-PROGRAMME-1. Bloque : rien.

## Périmètre

Peut créer ou modifier : `web/src/ecrans/Arrivee/` (compte, pseudo,
cursus, demande), la route `/arrivee`, `contenu/voix.json` (clés
`arrivee.*` seulement), `programme/catalogue.json` (les compteurs),
`web/README.md` ; côté serveur, `serveur/academie_etat/auth.py` (mot de
passe haché), une migration `serveur/migrations/0002_*.sql` (mot de
passe sur `profils`, table `demandes_cursus`), `serveur/API.md`
(`POST /compte`, `POST /demandes-cursus`), et leurs tests.
Ne touche pas : le moteur, les prompts, `COMMENCER.md` hors des
compteurs, le format du journal hors de l'événement `cursus`.

## Déjà tranché (ne pas rouvrir)

- Mail pro et mot de passe à l'entrée ; lien magique pour nouvel
  appareil et oubli (`decisions/0032`, `serveur/API.md`).
- Un mot de passe n'est jamais stocké en clair (même règle que les
  jetons : hachage adapté aux mots de passe, pas SHA-256 nu).
- Un seul cursus à la fois, porté par un événement `cursus` du journal ;
  le client n'affiche que l'arbre du cursus courant.
- « Nouveau cursus » = une demande enregistrée côté serveur, lue par JB ;
  aucun envoi vers un tiers sans geste humain (règle 5).
- Le pseudo est visible par défaut dans le cercle ; pas d'avatar
  (`decisions/0010`, `0015`). Le quiz vient après le choix du cursus
  (`BLUEPRINT.md` §11). Aucun hôte tiers.

## Étapes, dans l'ordre

1. Tests rouges, serveur : un mot de passe court est refusé ; le mot de
   passe n'apparaît jamais dans la base ; une demande de cursus sans
   texte est refusée ; une demande enregistrée se relit par l'outil de
   JB (`cli.py`).
2. Tests rouges, client : mail invalide et pseudo vide refusés avec les
   textes `arrivee.*` ; le catalogue affiche autant de cartes que le
   fichier plus « Nouveau cursus » ; choisir un cursus écrit l'événement
   `cursus` dans le journal ; la route mène au quiz du cursus choisi.
3. Serveur : migration, `POST /compte`, `POST /demandes-cursus`,
   `cli.py demandes`.
4. Les écrans : compte, pseudo, cursus, demande ; tokens de
   `DIRECTION-ARTISTIQUE.md`, clavier et lecteur d'écran (§7).
5. Compteurs du catalogue calculés au build depuis les programmes et les
   chapitres, pas à la main.

## Ce qu'on ne fait pas

- Pas de plusieurs cursus en parallèle (réouverture de `0032` §4).
- Pas d'envoi de mail à JB : il lit les demandes avec son outil.
- Pas d'import de fichier dans le navigateur.

## Preuve

```bash
cd serveur && python3 -m unittest discover tests
```

```bash
python3 app/tests.py && python3 tooling/check.py
```

JB voit : il crée un compte, choisit un pseudo, voit Copropriété,
Infirmier et « Nouveau cursus », dépose une demande d'essai, la lit avec
son outil, choisit Copropriété, arrive au quiz.

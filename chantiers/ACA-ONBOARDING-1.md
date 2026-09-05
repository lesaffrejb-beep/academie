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

## Extension autorisée le 05/09 (0042)

Copie Git isolée. Périmètre supplémentaire : serveur/academie_etat/,
serveur/migrations/, serveur/tests/, contrats/journal-v1.schema.json,
web/src/, web/vite.config.ts, web/tests/, scripts de lancement local,
programme/catalogue.json, prompts/essai-10h-et-pdf.md, travail/onboarding/.
Tests rouges avant code : inscription/connexion, refus des comptes
invalides, séparation des journaux, cookie changé, cursus persistant,
annuaire sans mail/réponses/temps, masquage effectif et demandes CLI.
Preuve navigateur sur serveur réel local : deux comptes et deux cursus,
reconnexion, brouillons isolés, tentative d'étude et onglet Élèves.
Entrée par première étude (tentative avant leçon), sans faux positionnement.
Le catalogue compte au build les cartes servies et les études disponibles.

Raccord de restauration inclus : `serveur/importer_journal.py` et son test aller-retour. Le lanceur local est `serveur/essai_local.py`.

## Correction demandée le 05/09 après essai (0044)

JB ne voit pas la connexion/inscription et veut rattacher son travail
commencé à son compte. Périmètre : porte et routes de compte, lien permanent
Mon compte, API d'activation d'un ancien profil sans mot de passe (identifiant
et journal conservés), reprise explicite du journal anonyme local vers un
seul compte avec originaux préservés, brouillons locaux conservés, tests
réels de reprise et comptes. La reprise réclame un geste dans l'interface
qui nomme le compte destinataire ; aucune attribution silencieuse.
Périmètre publication : entrée /academie-acces/ hors portée de l'ancien
service worker, même origine et même API ; route Caddy dédiée avec les mêmes
comptes HTTP que /academie/. Le nouveau client propose les mises à jour sans
rechargement forcé d'une réponse en cours. Push et VPS explicitement autorisés.
Tests rouges : ancien profil activé conserve son journal ; compte déjà
personnel et mail d'un autre profil refusés ; route arrivée disponible avec
session ; import idempotent et reprise refusée pour un autre compte.

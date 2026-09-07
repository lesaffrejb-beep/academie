# Relecture indépendante des accès — 7 septembre 2026

Outil : Codex. Modèle : GPT-6 (agent frais `revue_acces`, sans écriture du code relu). Mission bornée à l'accès, aux cursus et à la synchronisation ; protocole `CONTRIBUER.md` §7.

## Verdict initial : une correction nécessaire

**P2 — Le cursus actif est choisi par ordre textuel des dates, et non par instant réel.** Dans `serveur/academie_etat/auth.py`, `cursus_actuel` utilise `ORDER BY quand DESC, nonce DESC LIMIT 1`. Le contrat accepte des dates avec différents décalages horaires et précisions. Le client les compare avec `compareJournal` ; le serveur doit utiliser la même chronologie. Reproduction en base mémoire : envoyer un cursus copro à `2026-09-07T10:00:00+02:00`, puis IFSI à `2026-09-07T09:00:00+00:00`. Les deux envois répondent 200 ; `/profil` retourne `copro`, alors que le second événement survient une heure après. Le passage de cursus reste alors refusé à l'écran (« pas encore confirmé »). Utiliser `cle_chronologique` existante et couvrir décalages horaires, fractions et rejeu dans le test.

## Contrôles effectués

- Diff relu : `serveur/academie_etat/auth.py`, `journal.py`, `serveur/tests/test_rentree.py`, `web/src/ecrans/Arrivee/Arrivee.tsx`, `web/src/app/compte.ts`, `web/src/donnees/api.ts`, et reprise réseau de `web/src/moteur/journal.ts`.
- `python3 -m unittest serveur.tests.test_rentree serveur.tests.test_onboarding` : 15 tests passent.
- `PYTHONPATH=serveur/tests:serveur:app python3 -m unittest serveur.tests.test_auth serveur.tests.test_journal serveur.tests.test_chronologie_relecture` : 19 tests passent. Le premier lancement sans `PYTHONPATH` échouait à importer `commun` ; corrigé par cette invocation.
- Les tests existants passent malgré la reproduction du défaut de chronologie, qui manque à leur couverture.
- Stockage des secrets : hachage scrypt maintenu ; la phrase choisie n'est pas renvoyée dans l'identité ; `memoriseCompte` reste une liste explicite de champs sans secret. La récupération révoque les sessions et renouvelle la clé.
- Isolation : requêtes journal toujours limitées au profil authentifié ; base locale par identifiant ; la suppression du verrou de cursus n'enlève pas la validation des identifiants du catalogue.
- Le délai réseau laisse le journal en attente ; seul un acquittement structuré confirme la réception. Les gestionnaires de reprise ajoutés sont détachés au démontage.

Aucune autre régression certaine identifiée dans ce périmètre. Cette revue n'est ni un essai navigateur ni une preuve téléphone–Mac/VPS. Les contrôles globaux obligatoires restent à exécuter par l'agent intégrateur avant conclusion. Ne pas assimiler ce verdict initial à une validation finale tant que le P2 n'est pas corrigé et recontrôlé.

## Contre-vérification et extension bibliothèque

**Verdict après correction : le P2 ci-dessus est levé. Aucun bloquant identifié dans le périmètre relu.** `cursus_actuel` utilise désormais `max(..., key=cle_chronologique)` ; le test `test_cursus_compare_instants_pas_texte` passe. Une reproduction indépendante avec les deux fuseaux du constat initial, puis un événement postérieur de 0,0000001 seconde, rend chaque fois le dernier cursus réel. `python3 -m unittest serveur.tests.test_rentree` : 4 tests passent.

Extension relue : `app/export_cours.py`, `app/tests_export_cours.py`, insertion dans `app/genere.py`, `web/src/ecrans/Cours.tsx`, `Demarrage.tsx`, `demarrages.json`, routage/accueil, transport du fichier par Vite et préparation de publication.

- `PYTHONPATH=app python3 -m unittest app.tests_export_cours` : 1 test passe, 389 chapitres exportés, statut brouillon et absence de promotion en cartes.
- Le corps des brouillons est rendu en nœuds texte React ; aucun `dangerouslySetInnerHTML`, parseur HTML ou injection d'image issue du texte. Les liens `[S:...]` admettent seulement HTTP(S). La liste de sources reçoit également des URL HTTP(S), garanties avant export par `cours_copro.controle` ; les liens s'ouvrent avec `rel="noreferrer"`.
- Le statut de brouillon reste affiché sur index et chapitre ; lecture simple sans écriture de progression. Auteur, sources, date déclarée, portée et limites sont transportés. Cette présentation ne vaut pas relecture factuelle des 389 textes.
- Le garde `metier !== 'copro'` empêche l'affichage de cette bibliothèque dans le cursus IFSI. Il s'agit d'un filtre d'interface sur du contenu pédagogique partagé, pas d'une ACL destinée à cacher des données personnelles.
- Le démarrage choisit son plan depuis le métier du magasin et teste `etudeDisponible` avant de proposer un lien d'étude. Il annonce dix séances proposées, sans promettre de compétence acquise. La revue des huit nouvelles études reste celle de l'agent contenu.
- `prepare` copie le dossier `cours` dans son atelier ; le générateur produit `cours.json` à côté de `banque.json` ; Vite l'émet dans la distribution. Le manifeste énumère les fichiers émis et la distribution les copie. Contrôle de code uniquement : la présence effective de ce fichier sur le VPS reste à constater à la publication.

Observations non bloquantes : la nature de chaque source est présente dans le JSON exporté mais n'est pas affichée dans le composant actuel ; l'afficher améliorerait la lecture critique. Le champ `REQUIS` du préparateur ne nomme pas encore `cours.json`, même si la génération et Vite le rendent nécessaire au build : l'ajouter renforcerait la vérification d'un paquet distribué séparément. Ces observations ne modifient pas les garanties constatées ci-dessus.

Les preuves navigateur, cache et publication restent apportées séparément par l'intégrateur. Aucun code produit n'a été modifié par cette relecture.

## Relecture finale : route de reprise et paquet

**Aucun bloquant de sécurité ou de conservation des données identifié dans les ajouts relus.** Périmètre : `deploy/installer_reprise.py`, son test, `web/public/reprise.html`, `reprise.js`, et l'ajout des fichiers obligatoires dans les deux distributeurs.

- La transformation ajoute exactement `/academie-reprise/` au matcher privé Académie et aux exclusions du matcher WORK ; les lignes d'authentification existantes restent identiques. La nouvelle route sert seulement `reprise.html` depuis la publication, avec `Cache-Control: no-store`. La protection de cette route dépend bien de l'usage préexistant du matcher `@academiePrivee` par BasicAuth dans la configuration déployée ; cette revue du transformateur ne remplace pas le contrôle HTTP anonyme puis authentifié du VPS.
- Le transformateur refuse les configurations sans les deux matchers uniques et l'ancre attendue. Avant écriture, `caddy validate` doit réussir. L'application conserve une copie du Caddyfile puis recharge ; en cas d'échec, elle restaure et tente de recharger la copie. Aucun accès à SQLite, aux comptes ou aux journaux dans ce script.
- La page de reprise se trouve hors des deux scopes hérités visés. Le script retire uniquement les enregistrements de service worker de la même origine dont le chemin de scope est exactement `/academie/` ou `/academie-acces/`. Il ne supprime ni caches, ni IndexedDB, ni localStorage, ni cookies. Aucun envoi à un tiers. La page demande de terminer les réponses ouvertes avant le bouton ; les onglets déjà contrôlés par un ancien worker restent une limite d'usage, sans opération de suppression de leur état local.
- Le script n'affirme la réussite et ne navigue qu'après résolution des désenregistrements. Une exception garde la page ouverte et permet de réessayer. Le code du worker n'est pas une donnée d'apprentissage ; le retrait de son enregistrement conserve le contenu local décrit ci-dessus.
- `cours.json`, `reprise.html` et `reprise.js` sont désormais exigés dans le préparateur et le publieur VPS. Les empreintes du manifeste s'appliquent aussi à eux. L'observation antérieure sur l'absence de `cours.json` dans `REQUIS` est donc levée.

Tests exécutés par le relecteur : `PYTHONPATH=deploy python3 -m unittest deploy.test_installer_reprise` — 2 tests passent ; `node --test web/tests/publication.test.mjs` — 6 tests passent, dont construction réelle depuis des sources en lecture seule et conservation de la publication lors d'un build refusé. Le build émet l'avertissement préexistant concernant le script classique `registerSW.js`, sans échec. Les E2E de reprise et de changement de cursus sont exécutés séparément par l'intégrateur ; ils ne sont pas revendiqués ici comme exécution de ce relecteur.

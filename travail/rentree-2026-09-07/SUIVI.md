# Rentrée du 7 septembre 2026

Outil : Codex ; modèle : GPT-6. Objectif : chantiers/ACA-RENTREE-1.md.

## Constat initial

Dépôt actualisé par git pull --ff-only, seule entrée non suivie préalable : .vite/.
VPS mesuré le 07/09 : commit 4974dd6c46368d318ab799588a82f5abe019f97e,
API active, 950 Mio libres. Catalogue : huit études copro et deux études IFSI.
Le suivi du 06/09 disant publication bloquée est dépassé par cette mesure.
Les 389 cours copro sont des brouillons locaux, pas des études servies.
Le graphe et l’accès pseudo existent ; vérifier leur comportement déployé.

## Résultat local

Accès : mot de passe et phrase de récupération distincts, session persistante,
ajout/reprise de cursus avec événements append-only. Les réponses et comptes
ne sont ni effacés ni fusionnés. Le dernier cursus est choisi selon l’instant
réel, y compris lorsque les horodatages portent des fuseaux différents.

Client bleu commun : Boîte retirée de la navigation, ancien lien redirigé ;
arbre/graphe conservés ; cours bruts explicitement séparés des exercices ;
synchronisation au retour d’onglet, requêtes bornées, erreurs visibles.
Brouillon automatiquement enregistré sur cet appareil ; les réponses confirmées
vont au journal synchronisé. Ce n’est pas une synchronisation des brouillons.

Contenu : 389 cours copro consultables comme brouillons, 18 études interactives,
168 cartes (134 copro, 34 IFSI), dont huit nouvelles études d’entrée IFSI
contre-lues. Deux démarrages de dix séances, huit études et deux rappels chacun.
Le programme IFSI de 375 chapitres n’est pas intégralement rédigé.
Voir [le relais prêt à coller](RELAIS-LLM.md).

NotebookLM observé dans le navigateur : carnet Copropriété de 200 sources.
181 captures texte locales contrôlées par empreinte, zéro différence ; ce
contrôle ne vaut pas lecture intégrale ni intégration. Aucun PDF client importé.

## Relecture et contrôles

[Relecture accès](RELECTURE-ACCES.md), [relecture IFSI](RELECTURE-IFSI.md).
App/tests puis tooling/check passés (zéro erreur) ; 343 tests client, six tests
publication, tests déploiement et build passés. Suite navigateur : 110 scénarios
passés, puis six scénarios IFSI rejoués et passés après actualisation des titres
d’accueil attendus. Huit tests comptes passent intégralement après build stable.
Parcours automatiques ordinateur/téléphone et onboarding testent conservation,
isolement, récupération et changement de cursus. Les deux nouveaux tests de
brouillon/reprise passent après correction du sélecteur du test (getByRole).
Le trajet entre téléphone physique et Mac personnel reste à constater.

## Publication

Code publié : 53d6563a4e18dc1ea0332ece47c712a3c6a65af8 sur main et VPS,
le 07/09/2026 à 08:34 (Paris). Archive SHA-256 :
c4875d2032123f352118b72550bf02291f28c3b3407302d847cceaa578cedcb3.
Vingt-cinq empreintes de fichiers contrôlées sur place : 18 études, 168 cartes,
389 cours ; SQLite quick_check = ok. API, timer et Caddy actifs.
Sauvegarde : /var/lib/academie/sauvegardes/avant-53d6563a4e18-20260907T063404Z.
Caddy : /etc/caddy/Caddyfile.aca-rentree-20260907T063406Z.
Conservation comparée : deux profils, quatre sessions, trois événements du
journal ; aucune différence des lignes existantes. Pas de restauration SQLite.

Routes anonymes /academie/, /academie-reprise/ et profil API : HTTP 401 attendu.
Le navigateur automatisé n’a pas franchi la protection HTTP de la nouvelle
route (net::ERR_BLOCKED_BY_CLIENT) ; l’ancien onglet continue donc d’afficher
son ancien code. Le formulaire actuel a été inspecté visuellement sur le
serveur local, et la reprise conservant compte/brouillon est testée localement.
Ne pas confondre ces preuves avec un essai utilisateur authentifié sur le VPS.
Ouvrir https://vps-5a3d618c.vps.ovh.net/academie-reprise/ avec l’accès VPS
habituel, puis cliquer « Actualiser et ouvrir Académie ». Aucun effacement de
données n’est requis. Le trajet physique entre deux appareils reste à constater.

La CI du premier commit a signalé un tiret cadratin dans le dernier ajout de
documentation API ; il est corrigé dans le commit de consolidation. Les tests
Python avaient réussi ; les contrôles obligatoires sont rejoués après correction.
Une ancienne version est restée servie par le service worker du navigateur,
alors que le serveur possédait un paquet plus récent. Une page de reprise hors
anciens scopes remplace les enregistrements de code sans supprimer IndexedDB,
localStorage, caches ou cookies. La protection HTTP existante est conservée.


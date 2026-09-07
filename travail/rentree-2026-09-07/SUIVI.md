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

À compléter par le SHA, le manifeste, les sauvegardes et la preuve navigateur.
Une ancienne version est restée servie par le service worker du navigateur,
alors que le serveur possédait un paquet plus récent. Une page de reprise hors
anciens scopes remplace les enregistrements de code sans supprimer IndexedDB,
localStorage, caches ou cookies. La protection HTTP existante est conservée.


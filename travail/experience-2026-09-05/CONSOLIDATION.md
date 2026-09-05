# Consolidation du 05/09/2026

Codex, GPT-6 ; tâche 01a0710f-adf8-7db0-8d20-0e309023a53a.
Demande de JB : poursuivre roadmap, critiquer fond et forme, arbitrer
sur la durée, pousser main et publier sur VPS. Académie est le dépôt
visé ici ; Labor possède sa tâche active séparée.

## Résultat

Les travaux locaux de l'audit, du journal, de l'usine et des deux parcours
sont consolidés avec leurs preuves antérieures. Le README est corrigé :
Étude est implémentée, 76 cartes v1 et 27 v2 coexistent ; la migration
historique et l'efficacité pédagogique restent ouvertes.

La décision 0037 reprend les couleurs et la vue globale. Papier rosé,
encre prune, accent framboise ; Nuit et les préférences enregistrées
restent disponibles. Les domaines montrent leurs noms, leurs branches
et les cartes disponibles ; aucun lien géométrique ne feint un prérequis.
Sur téléphone le clic ouvre directement le domaine ; sur ordinateur il
alimente l'aperçu. Aucun moteur, journal ou contenu modifié par ce lot visuel.

Références documentées antérieurement retrouvées et rouvertes :
[Thinkers](https://www.niccolomiranda.com/work/thinkers), navigation de
plateforme pédagogique ; [Carbon](https://carbondesignsystem.com/elements/spacing/overview/),
regroupements et espacement. Les captures originales envoyées par JB ne
sont pas jointes ici : aucune fidélité à ces images n'est revendiquée.

Défaut de publication détecté avant transfert : le build isolé omettait
`contenu/parcours.json`. Le test rouge obtenait une liste vide. Copie
explicite ajoutée, test vert sur les deux parcours et revue indépendante
`/root/revue_publication` sans bloquant à ce périmètre. Paquet inspecté :
103 cartes, cinq leçons, deux parcours. Les tests du preview seuls
n'auraient pas détecté cette régression de livraison.

## Vérifications actuelles

- Python : TOUT VERT après autorisation d'ouvrir les sockets locales ;
  le premier échec sandbox ne signalait pas un défaut applicatif.
- Contrôle du dépôt : zéro erreur ; diff sans erreur d'espacement.
- Client : 271 tests Vitest et cinq tests de publication passent.
- Build TypeScript/Vite/PWA et préparation isolée passent.
- Campagne navigateur : 74/76 au premier passage. Deux courses du test
  hors ligne recliquaient l'ancien QCM avant l'écriture IndexedDB.
  Attente de la nouvelle question ajoutée, aucune assertion de conservation
  retirée ; les huit scénarios hors ligne passent ensuite, deux viewports.
- Contrastes des dix accents sur leur fond, calculés dans le navigateur :
  Papier minimum 5,74:1 ; Nuit minimum 6,00:1. Pas certification WCAG complète.
- Détecteur Impeccable : aucune alerte. Revue indépendante : trois défauts
  matériels corrigés, puis trois corrections jugées résolues, verdict
  `ship` borné dans [REVUE-EXPLORATION.md](REVUE-EXPLORATION.md).
- Captures et journaux retenus dans [preuves/exploration](preuves/exploration/).

## Auto-critique et suite

L'index est plus exploitable mais ne montre pas encore les relations
transverses du programme ; les prérequis restent dans les fiches. Les
branches sans contenu restent nombreuses. Une interface soignée ne rend
pas un cursus complet et une étude parcourue ne démontre pas un transfert.
Les horizons 1, 2, 3, 4, 5 ans sont des risques à suivre, pas cinq années
simulées par des tests. Prochaine preuve utile : accès authentifié réel,
trajet téléphone/Mac, puis usage et cas différés du protocole existant.

## Frontière VPS

Constat renouvelé : API et Caddy actifs ; clone propre ; Caddy ne lit
pas l'index, parent/publication 750, SQLite/WAL/SHM 644. Le refus d'ACL
historique n'est pas contourné. Proposition de périmètre dans
[ACL-CADDY-20260905.md](../../deploy/ACL-CADDY-20260905.md).
Le transfert sauvegardé ne vaut pas accès authentifié. La publication
physique et les observations humaines restent des preuves distinctes.

## Push et arrêt du transfert

Code et consolidation poussés sur main : `184a75a80037bf4411f155b0061f805b0314c240`.
CI GitHub `check` verte ; CI `client` en cours au constat.
Le paquet local `/tmp/academie-livraison-20260905.tgz` contient cette version,
avec manifeste de fichiers et `version-source.json`. SHA-256 de l'archive :
`f2fdb3c8d67e8752cc67dbd82285f4c26b85ecd4e39262fae6ecf70365b52bb4`.

La revue automatique a refusé `scp` vers
`debian@51.178.183.154:/tmp/academie-livraison-20260905-184a75a.tgz` :
autorisation de cet hôte et de ce paquet jugée insuffisamment explicite.
Le transfert n'a pas eu lieu ; le pull distant prévu après n'a pas été
exécuté. Clone distant resté sur `3ecbc77`, aucun droit ni fichier modifié.
Les lectures établissent Caddy sur `vps-5a3d618c.vps.ovh.net`, route
`/academie/`, publication `/var/lib/academie/publication`.

Autorisation à obtenir : transfert de ce paquet public (code client,
banque sourcée, polices et manifeste ; aucun journal, secret ou document
client), sauvegarde du client et de SQLite, pull fast-forward du clone
propre, installation vérifiée des assets avant index et service worker,
redémarrage de la seule API Académie. Autorisation distincte mais
présentée ensemble : ACL Caddy décrites dans le document de déploiement,
avec refus SQLite/WAL/SHM et fichiers privés futurs avant traversée.
HTTPS authentifié demandera une session d'accès valide. Aucun nouveau
compte, désactivation d'authentification ou migration joueur proposé.

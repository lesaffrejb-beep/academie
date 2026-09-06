# Préparation du VPS pour l'essai de lundi

06/09/2026, Codex / GPT-6, agent `/root/graphe`. Autorisation explicite
à publier donnée dans l'objectif de JB. Ici : préparation et inspection
seulement, en attente du paquet identifié du coordinateur. Aucun déploiement
ni arrêt de service effectué par cette passe.

## État distant lu vers 18:42, heure de Paris

- Hôte `debian@51.178.183.154`, clone `/home/academie/repo` propre,
  HEAD `1347d9b01da95d643879cead3c75e65d1715f1e2`.
- API `academie-etat.service` et Caddy actifs. Santé locale `ok: true`.
- Client publié : provenance `08f0f900edb02c9a3f5e37a31d9a3574613ca4a2`,
  manifeste de 20 fichiers, zéro différence d'empreinte.
- SQLite : `quick_check=ok`, zéro erreur de clé étrangère. Trois lignes de
  journal, quatre sessions, deux profils. Aucun contenu de ces lignes lu
  dans les sorties ni copié vers le Mac. Migrations 0001 et 0002 présentes ;
  0003 attendue pour le nouveau code.
- Caddy lit l'index, ne lit pas SQLite. Parent : traversée seule par Caddy ;
  publication : lecture/traversée, ACL par défaut présentes.
- Environ 987 Mio libres sur `/`, publication 3,8 Mio, clone 24,4 Mio,
  sauvegardes 5,6 Mio. `/tmp` est un tmpfs distinct avec environ 1,7 Gio libres.
  La capacité doit être recontrôlée au geste, aucun nettoyage n'est proposé.
- Python 3.13.5, Node absent. Le timer actif lance encore la génération Python
  de la banque seule, prochain passage observé le 07/09 vers 07:18 à Paris.
  Le timer de sauvegarde est actif.

Ne pas employer `deploy/installer.sh` sur cet hôte : il remplacerait l'unité
fonctionnelle par celle qui attend Node. La livraison ci-dessous conserve
les unités et Caddy. Le build est effectué sur le Mac.

## Paquet et script réutilisable proposés

`deploy/publier_paquet.py` prend `--sha`, `--archive`, `--digest`,
`--expected-lessons 7`. Sans `--appliquer`, il contrôle seulement le paquet
dans un répertoire temporaire. Avec ce flag, il exécute la livraison root
sur le VPS. Son import `deploy/verifier_migration.py` doit se trouver à côté
s'il est copié dans un répertoire de préparation privé.

Le paquet est construit depuis le commit final par
`web/preparer-publication.mjs`. Après le build, écrire `version-source.json`
avec `{"commit":"<SHA complet>"}`, puis recalculer le manifeste avec
`ecrisManifeste` exportée par le même fichier. L'archive doit contenir le
contenu du dossier de sortie, sans dossier enveloppe. Son SHA-256 est fourni
explicitement au script.

Le contrôle refuse traversée de chemins, liens symboliques ou physiques,
fichiers spéciaux et doublons, puis confronte exactement les fichiers au
manifeste, leurs empreintes, la provenance, les références Vite, les images,
le nombre d'études et la présence de toutes leurs cartes. La qualification
pédagogique et la péremption restent les valideurs et le moteur du client.

## Séquence du geste distant, seulement après revue technique

1. Contrôler paquet avant mutation du serveur. En mode application, prendre
   le verrou existant `/run/lock/academie-publication-20260905.lock`, refuser
   un clone modifié ou une publication Python en cours. Vérifier assez de
   disque pour sauvegarde et fichiers remplacés, avec réserve opérationnelle
   de 128 Mio configurable. Cette marge n'est pas une promesse de capacité.
2. Fetch `origin/main`, prouver que SHA final est publié, descendant du SHA
   courant et atteignable depuis main. Suspendre le timer existant et arrêter
   seulement l'API Académie.
3. Sauvegarde privée sous `/var/lib/academie/sauvegardes/avant-<sha>-<date>/` :
   copie SQLite par API backup, publication, SHA, état du timer, ACL, unités
   et Caddy. Aucune sauvegarde ni secret ne ressort du VPS.
4. Avancer le clone en fast-forward sur le SHA exact. Appliquer uniquement
   la migration nouvelle 0003 par le connecteur officiel, API arrêtée.
   Toute migration supplémentaire exige une revue spécifique.
5. Comparer toutes les anciennes tables, colonnes et lignes hors table de
   migrations avec le backup : `verifier_migration.py` lit les deux bases
   sans les modifier, compare les valeurs et multiplicités, pas seulement
   les compteurs. Journal, profils et sessions doivent rester identiques
   sur leurs anciennes colonnes. Intégrité, clés étrangères et marqueurs
   de migration sont contrôlés.
6. Distribuer chaque fichier par remplacement atomique. Ressources d'abord,
   index ensuite et service worker en dernier. Conserver les anciens assets
   pour les onglets existants. Nouveaux fichiers/dossiers appartiennent à
   academie, sont lisibles par Caddy dans publication ; les voisins privés
   doivent rester illisibles.
7. Confronter le manifeste installé. Ouvrir l'API, attendre sa santé et lire
   le nouveau point d'entrée des comptes sans imprimer de nom. Réactiver le
   timer seulement après cette cohérence code/banque/client. Unité Python
   conservée ; elle lira désormais le clone du même SHA que le paquet.
8. Le coordinateur vérifie ensuite HTTPS authentifié, le graphe, une étude,
   sauvegarde et reprise via compte réel. Le script ne prétend pas fournir
   cette preuve ni remplacer le trajet physique téléphone/Mac.

## Retour arrière et limite de la transaction

Le script ne remplace **jamais** la base joueur par son backup.
Avant ouverture de la nouvelle API, si les anciennes données sont toujours
identiques et le clone n'a pas changé concurremment, il restaure l'ancien
code en checkout détaché et l'ancien client, sans effacer les nouveaux
assets. La migration 0003 ne fait qu'ajouter des colonnes ; l'ancien code
peut ignorer ces ajouts. Le timer reste suspendu pour diagnostic.

Si la comparaison des données échoue ou que le clone diffère, aucun retour
aveugle : API arrêtée, sauvegarde conservée et diagnostic humain requis.
Dès le démarrage de la nouvelle API, de nouvelles écritures sont possibles :
un échec conserve le nouveau couple API/client et la base, suspend le timer,
et exige diagnostic. Aucun ancien client n'est remis devant de nouveaux
comptes automatiquement. Caddy n'est pas modifié ; sa sauvegarde n'est donc
jamais restaurée automatiquement.

## Preuves locales et limites

Tests rouges avant les nouveaux outils, puis 10 tests archive/manifeste/
ordre de distribution et 7 tests SQLite verts. Compilation Python verte,
`tooling/check.py` : zéro erreur. La comparaison SQLite inclut perte de
journal, valeurs changées à compte égal, multiplicités changées, disparition
de table/colonne, ajout de schéma et chemin absent non créé.

Ces tests n'ont pas simulé tous les échecs systemd/réseau/disque pendant une
livraison réelle. Le script est soumis à relecture du coordinateur avant
son premier emploi ; aucune réussite distante n'est revendiquée ici.

# Publication VPS du 05/09/2026

Codex, GPT-6. Autorisation explicite de JB après présentation du transfert
sur 51.178.183.154 et des ACL : « Je t’autorises tout carte blanche ».
Le refus antérieur est levé par cet accord ; pas de modification de
l'authentification HTTP, des groupes ou de la racine Caddy.

## État installé et preuves

- Hôte : `vps-5a3d618c.vps.ovh.net`, chemin `/academie/`.
- Clone `/home/academie/repo` propre, mis à jour en fast-forward sur
  `67a22a46e4b776cfc545b8f3973ed9f8018dfc61`.
- Build client issu de `184a75a80037bf4411f155b0061f805b0314c240`,
  documentation ajoutée ensuite sans changement du code client.
- Archive SHA-256 :
  `f2fdb3c8d67e8752cc67dbd82285f4c26b85ecd4e39262fae6ecf70365b52bb4`.
- Seize fichiers du manifeste contrôlés avant et après installation ;
  tous lisibles sous l'utilisateur Caddy. Assets avant index, service
  worker en dernier, remplacement atomique de chaque fichier. Anciens
  assets conservés pour les onglets ouverts. Version dans
  `publication/version-source.json`.
- Banque du paquet : 103 cartes, cinq leçons, deux parcours.
- `academie-etat.service`, `academie-publication.timer` et
  `sauvegarde-academie.timer` actifs. Santé API locale `ok: true`,
  contrats carte-v1, carte-v2 et journal-v1. Le premier curl immédiat au
  redémarrage a devancé l'ouverture du port ; la vérification suivante
  réussit. Aucune migration joueur ni compte créé.
- HTTPS sans session renvoie 401 : authentification maintenue.

## Sauvegarde et permissions

Sauvegarde privée :
`/var/lib/academie/sauvegardes/avant-184a75a-20260905/`.
Elle contient publication.tgz, ACL récursives, version précédente du
clone (`3ecbc77`), unité de publication et copie SQLite par API backup.
`PRAGMA integrity_check` de cette copie : `ok`.

Sous verrou de livraison, timer de publication suspendu puis réactivé :
refus nommé `caddy` sur tous les voisins de publication ; refus par
défaut sur le parent pour les créations futures ; traversée seule du
parent ; lecture/traversée sur publication et ACL par défaut de lecture
pour ses créations. Contrôles sous Caddy : SQLite, WAL, SHM, banques et
sauvegardes illisibles. Une nouvelle création par academie, même rendue
644, reste illisible ; seul ce fichier de test a été retiré.

Les journaux et secrets n'ont pas été transférés vers le Mac ni versionnés.
Le paquet sortant ne contient que le client, la banque, les médias et les
manifestes. Un premier transfert a expiré avant connexion ; la reprise
après retour du port SSH a réussi.

## Retour arrière

Sous verrou `/run/lock/academie-publication-20260905.lock`, suspendre le
timer et sauvegarder d'abord le nouvel
état. Restaurer les fichiers de publication.tgz (assets, index puis
service worker), sans effacer les assets additionnels. Pour annuler les
ACL, utiliser le fichier `acl.txt` avec `setfacl --restore` ; vérifier
ensuite que le parent refuse à nouveau la traversée Caddy. Si seul le
client est annulé, ne pas restaurer SQLite. Un retour du code API demande
un checkout explicite de la version sauvegardée et le redémarrage de la
seule API Académie, puis sa santé. Ne réactiver le timer qu'après cohérence
entre banque restaurée et source du générateur : l'unité réellement
installée régénère la banque depuis le clone courant. Une restauration
des seuls fichiers reste temporaire si cette source n'est pas alignée.
Conserver la base joueur courante ; ne pas la remplacer pour revenir à
une ancienne interface.

Revue indépendante `/root/revue_acl` : aucun bloquant des ACL sur les
preuves transmises ; risque de republication par le timer corrigé dans
ce protocole. Le script ponctuel exécuté n'est pas un installateur
réutilisable : en cas d'échec partiel, il n'aurait pas restauré seul les
ACL/publication. La présente exécution a réussi ; une future relivraison
doit assurer la restauration avant toute réactivation en cas d'échec.
Preuve brute des ACL : [acl-vps-20260905.txt](preuves/acl-vps-20260905.txt).

## Preuves encore manquantes

Le navigateur de test puis Chrome n'ont pas de session HTTP valide
(`ERR_INVALID_AUTH_CREDENTIALS`). Le navigateur intégré refuse cette
navigation (`ERR_BLOCKED_BY_CLIENT`). Aucun identifiant extrait, aucun
mot de passe modifié, aucune protection contournée. La lecture Caddy et
les empreintes ne prouvent donc pas encore le rendu HTTPS authentifié.

JB doit se connecter dans Chrome à l'URL publiée pour poursuivre ce
contrôle. Trajet physique téléphone/Mac et retour, acceptation esthétique,
rituel et transfert pédagogique restent les preuves humaines des cahiers.
ACA-PUBLICATION-2 reste ouvert à ce périmètre ; les fichiers distants et
les ACL sont désormais installés, ils ne sont plus « en attente d'accord ».

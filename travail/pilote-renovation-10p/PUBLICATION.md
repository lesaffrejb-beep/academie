# Publication du pilote, 06/09/2026

Installation réussie vers 15 h 51, heure de Paris. Autorisation : demande de
JB d'essayer dix pages jusqu'au module et à sa mise sur le site.

## Ce qui est installé

- Site : `https://vps-5a3d618c.vps.ovh.net/academie/`.
- Étude : `#/salle/etude/satellite.travaux.rentabilite-renovation` ; bouton
  « Ouvrir le pilote rénovation » depuis l'accueil copropriété.
- Source : dix pages du Focus 106, pages 13-22 ; huit exercices, trois
  schémas originaux et une production de synthèse.
- Banque : 111 cartes, dont 101 copro et 10 IFSI ; six leçons et trois
  parcours. Ces totaux ne sont pas une couverture experte.
- Client construit dans un clone isolé du HEAD antérieur `59bb3b6`.
  Aucun fichier serveur, API, compte ou migration dans le diff publié.
- Commits : `a98a1049365ecfaa4aa83f464198d2b31840f903` (pilote et preuves),
  `08f0f900edb02c9a3f5e37a31d9a3574613ca4a2` (garde de livraison).
- Vingt fichiers inventoriés plus le manifeste. SHA-256 du manifeste :
  `2ec90e9d6e59f23e180d548b4054efd75c3d3774219b4fdfd758bdadf147d509`.
- Paquet local : `/private/tmp/academie-pilote-livraison.uLZYCs/publication`.
  Clone de construction : même parent, dossier `release`.

## Preuves réellement obtenues

`python3 app/tests.py` puis `python3 tooling/check.py` : tout vert, zéro
erreur, dans le workspace et le clone de livraison. `npm test` : 299 tests
Vitest et six tests de publication verts. Dix-huit tests Playwright verts
sur le workspace puis sur le client isolé de livraison, aux deux formats
1280 × 800 et 375 × 812. Ils couvrent les huit exercices, synthèse,
rechargement du brouillon, zoom effectif, absence de débordement, support
absent/malformé et non-régression de l'étude précédente. Captures
`apercu-ordinateur.png` et `apercu-telephone.png` inspectées.

Ces tests emploient un profil fictif. Les erreurs de connexion à l'API locale
absente sont attendues ; elles ne prouvent aucune synchronisation serveur.
Les réponses sont testées en stockage local et l'interface affiche la
synchronisation en attente, sans inventer d'acquittement distant.

VPS : HEAD exact contrôlé, clone propre, empreintes et lisibilité Caddy
vérifiées par l'installateur sur chaque fichier. API et timer actifs après
publication ; santé API `ok: true`. Aucun compte créé, supprimé ou migré.
Le timer installé lance seulement `app/genere.py`, pas un build Node ni un
git pull. Node est absent du VPS : le build a été effectué sur le Mac.
Une régénération séparée sous le compte `academie` a produit une banque
identique octet pour octet à celle du paquet (`cmp`, sortie zéro), sans
réécrire le site. Le générateur quotidien dispose donc bien du pilote.

La première archive comportait des entrées de métadonnées macOS : le
contrôle d'inventaire l'a refusée **avant toute mutation du site**. Reprise
avec `COPYFILE_DISABLE=1 tar --no-xattrs`, sans assouplir le contrôle.

## Sauvegarde et reprise

Sauvegarde conservée sur le VPS :
`/var/lib/academie/sauvegardes/avant-pilote-10p-20260906T135136Z/`.
Elle contient la publication précédente avec ses permissions et l'ancien
SHA. Lecture de cette sauvegarde refusée à Caddy, vérifiée après livraison.

`installer_pilote.py` prend le verrou de publication existant, arrête le timer,
exige `ActiveState=inactive`, sauvegarde, avance le clone et remplace les
assets avant index puis service worker. Il vérifie les empreintes et la
lecture Caddy. En échec de mutation, il restaure branche/SHA et fichiers
statiques ; le timer ne repart qu'après retour cohérent. Cette procédure
de rollback a été relue, mais aucun échec destructif n'a été injecté en
production. Les anciens assets restent présents pour les onglets ouverts.

Un rollback ultérieur ne doit pas restaurer une base joueur. Arrêter le
timer, prendre une nouvelle sauvegarde et aligner **source du générateur et
fichiers servis** sur la même version. Un futur git pull pourrait réappliquer
la livraison : une annulation durable exige un commit correctif explicite.

## Acceptations encore ouvertes

Le navigateur de cette session affiche un ancien shell à `/academie/`
et « Cette étude est en vérification » ; ses données ne montrent pas le pilote.
La requête HTTPS non authentifiée de la banque renvoie 401 ; l'entrée
distincte `/academie-acces/` reste à l'écran d'ouverture. Aucun secret,
cookie ou mot de passe inspecté, aucune protection modifiée. Une demande
de connexion a été présentée à JB.

La publication matérielle et les parcours locaux sont prouvés ; **l'ouverture
HTTPS authentifiée du nouveau module n'est pas encore confirmée**. Ne pas
transformer santé API ou empreintes en preuve de cet usage. Téléphone
physique, reprise Mac/téléphone et efficacité pédagogique restent également
à mesurer. Il ne s'agit pas encore d'un cours expert couvrant la rénovation.

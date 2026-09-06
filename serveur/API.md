# API d'état, v1 (contrat des routes, 02/09/2026)

Préfixe : `/academie/api/v1`. JSON partout. Authentification par cookie
de session (joueur) ou par jeton `Authorization: Bearer` (livraisons,
outils). Toute réponse d'erreur : `{"erreur": "<code>", "motif": "<phrase>"}`.

## Santé et version

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/sante` | `{"ok": true, "moteur_version", "contrats": ["carte-v1", "carte-v2", "journal-v1"]}` |

## Journal (le cœur)

| Méthode | Route | Corps | Réponse |
|---|---|---|---|
| POST | `/journal` | `{"depuis": "<horodatage ou null>", "lignes": [journal-v1…]}` | `{"acceptees": n, "ignorees": n, "manquantes": [journal-v1…], "jusqu_a": "<horodatage>"}` |
| GET | `/journal/export` | | le journal complet en JSONL, `Content-Disposition: attachment` |

Sémantique : le serveur ajoute chaque ligne dont le quadruplet (profil,
`quand`, `mode`, `nonce`) est inconnu, ignore les autres, et renvoie
toutes les lignes du profil dont `recu_le` (horodatage serveur) est
supérieur ou égal à `depuis` et que le client n'a pas envoyées. La borne
est incluse pour ne perdre aucune ligne reçue dans la même seconde : le
client absorbe les doublons par union. Un lot vide récupère les lignes
distantes même lorsque le client n'a rien à envoyer. Aucune mise à
jour, aucune suppression. Un lot fait au plus 500 lignes ; il est
accepté ou refusé en entier si une ligne ne respecte pas `journal-v1`,
avec l'index de la ligne fautive : le client la met de côté dans un
magasin local `rejets` et renvoie le reste, la file ne se bloque jamais.
Seul un refus `422 ligne-invalide` avec un index de ligne valide provoque
cette mise à l'écart ; tout autre refus conserve la file pour un nouvel
essai après retour du service ou de la session.

## Banques

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/banques` | la liste des domaines servis à ce profil (couche `banque` pour tous, `interne` pour son seul propriétaire ; `perso` n'existe pas côté serveur) avec version, empreinte, contrat, licence |
| GET | `/banques/<domaine>` | le `banque.json` du domaine, `ETag` = empreinte |

## Bibliothèque

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/bibliotheque` | les domaines adoptables : auteur, version, contrat, licence, chapitres, cartes, lien vers le rapport d'audit |
| POST | `/bibliotheque/<domaine>/adopter` | ajoute le domaine au profil (table `adoptions`) ; quatre questions de positionnement se proposent au premier lancement |

Seule la couche `banque` sous licence de partage y figure ; jamais une
couche `interne`, jamais une source.

## Livraisons

| Méthode | Route | Corps | Réponse |
|---|---|---|---|
| POST | `/livraisons` | multipart : `manifeste` (livraison-v1) + `banque` (JSON) | `202 {"livraison": id, "etat": "quarantaine"}` ou `422` avec les motifs du valideur |
| GET | `/livraisons/<id>` | | `{"etat": "quarantaine" \| "acceptee" \| "refusee", "motifs": []}` |
| POST | `/livraisons/<id>/accepter` | (propriétaire du domaine) | `200` |
| POST | `/livraisons/<id>/refuser` | `{"motif"}` | `200` |

Le serveur re-passe `app/valide_banque.py` sur la banque reçue, en
`ACADEMIE_RACINE` temporaire reconstituée depuis le manifeste (`config` =
le `academie.json` du dépôt-domaine, `programme` s'il est fourni), avant
toute quarantaine. Une livraison `banque` sans `licence: CC-BY-SA-4.0`
est refusée. Un fichier de
`sources/` dans l'archive reçue = refus immédiat.

## Profil

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/profil` | `{"id", "titre_affiche", "cree_le", "domaines"}` |
| PATCH | `/profil` | réglages : thème, semaine type, notifications, visibilité par domaine |
| DELETE | `/profil` | `202` ; effacement complet sous 48 h, à la demande du joueur connecté |

## Boîte (file d'attente)

| Méthode | Route | Corps | Réponse |
|---|---|---|---|
| POST | `/boite` | `{"type": "texte" \| "lien" \| "note", "contenu"}` (texte seulement ; les fichiers restent sur la machine) | `201 {"id", "etat": "a-traiter"}` |
| GET | `/boite` | | la file du profil et l'état de chaque entrée |
| PATCH | `/boite/<id>` | `{"etat": "chapitre-propose" \| "rattache" \| "ecarte", "chapitre"}` (écrit par le skill « glisser » depuis la machine) | `200` |

## Cercles (après le gate du rituel)

| Méthode | Route | Sens |
|---|---|---|
| POST | `/cercles/invitations` | inviter par lien privé ; l'acceptation est mutuelle |
| GET | `/cercles/<id>/fil` | jalons et kudos, jamais de séances ni de scores |
| GET | `/cercles/<id>/ligue` | facultative ; score = cartes stabilisées × niveau sur la semaine, tronc commun |
| POST | `/defis` | dix cartes d'un chapitre commun, même graine, 48 h |
| GET | `/joueurs/<id>` | carte de visite et arbre miniature : tous les domaines sauf ceux que le joueur a masqués (visibilité par défaut, decisions/0010 amendée) ; « une même Académie » = tous les profils de ce serveur |
| POST | `/masquages` | `{"domaine": "<clé>" \| "*"}` : masque un domaine, ou tout ; `DELETE` pour démasquer |
| POST | `/signalements` | `{"carte", "motif"}` : la carte sort de la rotation du signaleur (ligne `mode: signalement` au journal, appliquée localement) et le propriétaire du domaine reçoit le signalement, tracé jusqu'au verdict (B8 du pré-mortem) |

Ce qui n'existe pas et n'existera pas : une route qui donne l'état d'un
joueur à quelqu'un qu'il n'a pas accepté, une route d'export collectif,
une route de classement public.

## Authentification

| Méthode | Route | Sens |
|---|---|---|
| POST | `/compte` | crée `pseudo` et `phrase_secrete`, rend le profil et une clé de récupération affichable une fois |
| GET | `/auth/comptes` | sans session, liste les pseudos visibles pour choisir son compte |
| POST | `/auth/connexion` | reçoit `pseudo` et `phrase_secrete`, pose un cookie de session |
| POST | `/auth/recuperation` | reçoit `pseudo`, `cle_recuperation`, `phrase_secrete`, renouvelle la phrase et la clé |
| POST | `/auth/deconnexion` | révoque la session courante |

La phrase et la clé sont hachées par scrypt avec un sel distinct. La clé
est aléatoire sur 128 bits, ne revient que dans la réponse de création ou
de récupération, et ne peut pas être retrouvée ensuite. Sans phrase et
sans clé, il n'existe pas de récupération.

## Accès local, 06/09/2026 (0045)

`POST /compte` reçoit `pseudo`, `phrase_secrete` et répond 201 avec le
profil, le cookie HttpOnly SameSite=Strict, Secure en production et la
clé de récupération. La phrase fait 12 à 256 caractères. Le pseudo est
normalisé pour la connexion et reste unique. `POST /auth/connexion`
répond 200 et renouvelle la session. `POST /auth/recuperation` exige la
clé actuelle, remplace phrase et clé, puis révoque toutes les sessions
antérieures. Les refus 401 ne distinguent pas un pseudo absent d'un
secret incorrect ; 422 signale les données invalides, 409 un pseudo
existant et 429 la limitation. Les corps POST/PATCH non vides exigent
application/json sur HTTP, pour empêcher les formulaires tiers.
La limite d'origine se fonde sur le pair socket ; derrière Caddy local,
seule la dernière adresse ajoutée à X-Forwarded-For est utilisée. Le proxy
doit ajouter le vrai pair, pas conserver seul un en-tête contrôlé par le
client. Le service reste sur loopback. Ni mot de passe ni jeton en clair
dans SQLite ou le stockage navigateur ; seul le cookie porte le jeton.

Le client émet `X-Academie-Profil` sur ses requêtes authentifiées. Si le
cookie désigne quelqu'un d'autre, 409 `compte-change`, sans lecture ni
écriture du journal. Les jetons d'outils historiques restent compatibles.
Chaque onglet conserve son identité en mémoire et utilise IndexedDB
`academie-journal-compte:<id>` ; les brouillons et préférences de progression
portent aussi cet identifiant. Le journal anonyme historique est conservé
sans être affecté automatiquement à un compte. Un profil minimal sans
secret est mémorisé sur l'appareil pour la reprise hors ligne ; se
déconnecter efface cette mémoire, pas les réponses en attente. Sur un
appareil partagé, la déconnexion ferme aussi les autres onglets ouverts.
Le stockage local n'est pas chiffré par le mot de passe du compte.

L'événement journal `mode:cursus` exige `cursus` dans le catalogue.
Le premier choix fixe le cursus du compte ; les réémissions du même
choix sont acceptées, un choix différent est refusé 422. Le profil rend
`cursus` calculé depuis le journal. Import et export gardent l'événement.

`GET /auth/comptes` ne requiert pas de session personnelle et rend seulement
`{comptes:[{pseudo,titre_affiche}]}`. Le pseudo est l'identifiant de connexion
normalisé ; le titre peut avoir changé. Seuls les comptes personnels visibles
sont proposés, sans identifiant interne, cursus ni activité. Le masquage retire
le compte des deux annuaires ; la connexion par saisie reste possible. La
protection d'accès commune du VPS s'applique toujours avant cette API.

Le choix du cursus se présente à l'inscription. Après conservation de la clé,
le client crée l'événement de cursus et attend sa confirmation serveur avant
l'ouverture de l'étude. La clé reste en mémoire jusqu'à conservation explicite,
y compris pendant une récupération ; la projection persistée du profil l'exclut.

`GET /eleves` authentifié ne rend que `{eleves:[{id,pseudo,cursus}]}`.
Les profils supprimés, masqués ou `reglages.visibilite=false` sont absents.
`PATCH /profil {visibilite: boolean}` masque/rétablit le profil. Aucune
route nouvelle ne rend réponses, erreurs, temps ou agrégat.
Ce petit annuaire n'implémente pas les défis et autres cercles complets.

`POST /demandes-cursus {texte}` authentifié enregistre de 1 à 2000
caractères. `python3 -m academie_etat --base <base> demandes` les relit.
Aucun envoi de mail.

La migration 0002 ajoute les comptes et étend les modes du journal en
conservant les lignes. Elle n'a été appliquée qu'aux bases d'essai.
Publication : sauvegarder la base et les fichiers servis, fournir aussi
`programme/catalogue.json` au serveur, déployer client et API ensemble ;
faire autoriser puis vérifier la migration et l'accès HTTPS authentifié.
Un ancien serveur refuse le mode cursus : ne pas publier seulement le client.

### Bascule depuis un ancien client (0043)

Toutes les routes privées authentifiées par cookie exigent l'en-tête
`X-Academie-Profil`, sauf `GET /profil` utilisé au démarrage. L'absence
renvoie 409 `client-a-recharger`, une identité différente 409 `compte-change`,
sans lecture ni écriture des données privées. Les outils Bearer restent
compatibles. Les anciennes réponses locales ne sont ni effacées ni importées
automatiquement dans un compte. L'export HTTP par cookie demande également
cet en-tête ; l'export de l'interface lit sa propre base locale.


## Réinitialisation de l'essai (0045)

Après publication conjointe du client et de l'API, JB peut effacer les
comptes d'essai, leurs sessions et données distantes par
`python3 -m academie_etat --base <base> reinitialiser-comptes --confirmer
'SUPPRIMER LES COMPTES'`. La commande ne touche pas les bases IndexedDB
des navigateurs et ne peut pas s'exécuter sans la confirmation littérale.

L'accueil est joignable par `#/arrivee` même connecté. L'entrée HTTPS
`/academie-acces/` sert le même client sous un scope distinct du service
worker historique ; l'API et les URL de contenus restent `/academie/`.
Le compte et le journal du navigateur restent disponibles sur cette même
origine. Le proxy applique les mêmes identifiants HTTP aux deux entrées.

La reprise du journal anonyme est une action explicite, réservée au compte
nommé par une marque dans la base source. Les événements valides sont
copiés à l'identique dans sa base et sa file de synchronisation, sans
reprendre le curseur serveur ancien ni écraser un conflit. Les rejets
empêchent tout message de succès complet. Les originaux restent conservés.
Les brouillons peuvent être récupérés même sans réponse validée ; ils
restent dans le stockage local du compte, sans synchronisation serveur.

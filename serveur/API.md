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
toutes les lignes du profil postérieures à `depuis` que le client n'a
pas envoyées. Aucune mise à jour, aucune suppression. Un lot est
accepté ou refusé en entier si une ligne ne respecte pas `journal-v1`.

## Banques

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/banques` | la liste des domaines servis à ce profil (couche `banque` pour tous, `interne` et `perso` pour leur propriétaire) avec version, empreinte, contrat |
| GET | `/banques/<domaine>` | le `banque.json` du domaine, `ETag` = empreinte |

## Bibliothèque

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/bibliotheque` | les domaines adoptables : auteur, version, contrat, licence, chapitres, cartes, lien vers le rapport d'audit |
| POST | `/bibliotheque/<domaine>/adopter` | ajoute le domaine au profil ; le quiz de positionnement se propose au premier lancement |

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
`ACADEMIE_RACINE` temporaire, avant toute quarantaine. Un fichier de
`sources/` dans l'archive reçue = refus immédiat.

## Profil

| Méthode | Route | Réponse |
|---|---|---|
| GET | `/profil` | `{"id", "titre_affiche", "cree_le", "domaines"}` |
| PATCH | `/profil` | réglages : thème, semaine type, notifications, visibilité par domaine |
| DELETE | `/profil` | `202` ; effacement complet sous 48 h, confirmation par mail au joueur |

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
| GET | `/joueurs/<id>` | carte de visite et arbre miniature limité aux domaines rendus visibles |

Ce qui n'existe pas et n'existera pas : une route qui donne l'état d'un
joueur à quelqu'un qu'il n'a pas accepté, une route d'export collectif,
une route de classement public.

## Authentification

| Méthode | Route | Sens |
|---|---|---|
| POST | `/auth/lien` | envoie un magic link au mail du profil (inscription, nouvel appareil) |
| GET | `/auth/entrer?jeton=` | pose le cookie de session (≥ 1 an) |
| POST | `/auth/sortir` | révoque la session |

Tant qu'il n'y a pas de comptes, JB crée les profils et génère les liens
à la main avec un outil de ligne de commande du paquet.

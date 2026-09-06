# serveur/ : l'API d'état

Squelette écrit le 02/09/2026 (`ARCHITECTURE.md` §6, `decisions/0006`),
codé le 03/09/2026 par le chantier `ACA-JOURNAL-SYNC-1` : paquet
`academie_etat/` (stdlib seule : `http.server`, `sqlite3`), migrations,
21 tests dans `tests/` (union, idempotence, lot de 501, ligne fautive
indexée, jetons hachés, expiration, révocation, suppression sous 48 h,
import v0 vers v1, parité FSRS sur les
vecteurs, socket réelle). Lancer : `python3 -m unittest discover -s serveur/tests`,
ou `python3 app/tests.py` qui l'inclut. Routes servies : `/sante`,
`/journal`, `/journal/export`, `/compte`, `/auth/connexion`,
`/auth/recuperation`, `/auth/deconnexion`,
`/profil` (GET, PATCH, DELETE), `/boite`. `GET /journal/export` sort le
journal en JSONL : c'est l'entrée de `python3 app/rituel.py <fichier>`,
le tableau de bord du rituel (`ACA-RITUAL-METRICS-1`), qui lit sans rien
écrire et n'appelle personne. Le reste d'`API.md` (banques,
livraisons, bibliothèque, cercles) attend son chantier. Reste du
cahier : l'installation sur le VPS et la preuve téléphone-Mac (JB).

## Ce que le serveur fait, et seulement ça

1. **Reçoit et rend le journal** d'un joueur, par union. Il n'écrit
   jamais une ligne de lui-même, ne corrige rien, ne supprime rien.
2. **Reçoit les livraisons** de banque, les re-valide, les met en
   quarantaine, les sert une fois acceptées.
3. **Tient les profils, les cercles et leurs consentements** (plus tard,
   après le gate du rituel et les comptes).
4. **Efface** un profil et tout ce qui lui appartient en moins de 48 h.

Ce qu'il ne fait jamais : appeler un modèle, lire une source, calculer
un score qu'un client ne pourrait pas recalculer, envoyer un mail à
quelqu'un d'autre que le joueur lui-même, parler à labor, écrire dans
le journal d'un joueur. Les tables dérivées (`jalons`, `defis_resultats`,
`adoptions`, `signalements`) sont écrites par le serveur à partir des
lignes de journal qu'il reçoit et des actions des joueurs ; elles se
recalculent depuis le journal, elles ne sont pas une seconde vérité.

## Stack

- Python 3.12+, stdlib seule (`http.server` en threads derrière Caddy,
  `sqlite3` en mode WAL). Tranché au chantier le 03/09/2026 : le cahier
  admettait FastAPI ou un équivalent épinglé ; zéro dépendance vaut
  mieux pour un service qui doit répondre à 7 h. Si les cookies, la
  validation ou la charge l'exigent un jour, un framework s'ajoute sans
  changer le contrat des routes.
- Un seul processus, `academie-etat.service`, port local `8790`, derrière
  Caddy sur `/academie/api/`.
- Fichiers : `/var/lib/academie/etat.sqlite`,
  `/var/lib/academie/banques/<joueur>/<domaine>/`, secrets dans
  `/etc/academie/` (root, mode 600).
- Tests : `serveur/tests/` (à créer) contre une base en mémoire ; un jeu
  de fixtures rejoue `app/vecteurs_fsrs.py` pour vérifier que l'union du
  journal redonne exactement l'état Python.

## Arborescence cible

```
serveur/
  README.md            ce fichier
  API.md               les routes, opposables
  schema.sql           les tables ; appliqué par migrations numérotées
  academie_etat/       le paquet Python
    __init__.py
    app.py             création de l'application, routage
    auth.py            sessions, phrases et clés de récupération
    journal.py         union append-only, export
    livraisons.py      réception, re-validation, quarantaine
    cercles.py         membres, visibilité, défis, ligue (plus tard)
    db.py              connexion, migrations
  migrations/
    0001_initial.sql   = schema.sql au jour de la création
  tests/
    test_journal.py    union, idempotence, ordre, parité avec app/
    test_livraisons.py refus, quarantaine, acceptation
    test_auth.py       jetons, expiration, suppression
```

## Règles de codage

- Chaque écriture est idempotente : rejouer la même requête ne change
  rien.
- Chaque refus a un motif court, lisible par un humain et par un agent.
- Les identifiants de joueurs sont opaques ; la phrase et la clé ne
  figurent ni dans une URL, ni dans un journal, ni dans SQLite en clair.
- La version du contrat (`carte-v2`, `journal-v1`) est vérifiée sur
  chaque requête qui porte des données.
- Aucune dépendance à labor, au socle PostGIS ni à un service tiers.

# Cahier ACA-JOURNAL-SYNC-1 : l'état joueur sur le VPS, le client hors-ligne

Résultat attendu : l'état joueur vit sur le VPS et le client joue
hors-ligne ; API d'état (`serveur/API.md`), SQLite (`serveur/schema.sql`),
client qui écrit localement et synchronise par union, FSRS en parité des
deux côtés.
Fini quand : une réponse jouée sur téléphone réseau coupé est relisible
sur le Mac le soir, et l'inverse ; le test de parité contre
`app/vecteurs_fsrs.py` est vert ; rejouer un lot ne change rien ;
`app/tests.py` et `tooling/check.py` verts.
Dépend de : ACA-DOC-2. Bloque : ACA-FRONT-2, ACA-SEMAINE-1, ACA-ARBRE-1,
ACA-RITUAL-METRICS-1, ACA-RITUAL-1.

## Périmètre

Peut créer ou modifier : `serveur/**` (paquet `academie_etat/`,
`migrations/`, `tests/`, `importer_journal.py`), `deploy/academie-etat.service`,
`deploy/Caddyfile.academie`, `deploy/README.md`, `client/app.js` et
`client/sw.js` **seulement** pour l'écriture locale et l'envoi par lots
(pas de refonte visuelle : c'est ACA-FRONT-2), `app/vecteurs_fsrs.py`
(format de sortie, si nécessaire), `contrats/journal-v1.schema.json`
(par décision seulement), `ARCHITECTURE.md` §6 si un détail change.
Ne touche pas : `app/planificateur.py`, `app/seance.py`,
`app/progression.py`, `banque/`, `web/` (vide), `academie.json`, la
doctrine.

## Déjà tranché (ne pas rouvrir)

- Union pure du journal, aucune mise à jour ni suppression ; clé
  (profil, quand, mode, nonce) ; lot ≤ 500 lignes ; ligne fautive mise
  de côté dans `rejets` côté client (`serveur/API.md`, relecture du
  02/09 Q3).
- Le serveur n'écrit jamais dans le journal ; ses tables dérivées se
  recalculent (`serveur/README.md`).
- Profils créés à la main par JB via l'outil de ligne de commande, magic
  link généré à la main, cookie d'un an (`decisions/0006`, Q4).
- Migration du journal v0 : `mode: flash` → `mode: revision` +
  `format: seance` ; quiz inchangé ; carnet → `mode: erreur` ; `nonce` =
  SHA-256 de la ligne (`CONTRAT-CARTE-V2.md` §5).
- Stack : Python 3.12, FastAPI ou équivalent épinglé, SQLite WAL, port
  8790, utilisateur `academie` (`decisions/0007`, `serveur/README.md`).
- Aucun hôte tiers sauf le fournisseur de mail, non requis ici
  (`decisions/0020`).
- La couche `perso` n'existe pas côté serveur (relecture R1).

## Étapes, dans l'ordre

1. Tests rouges : `serveur/tests/test_journal.py` (union, idempotence,
   `depuis` sur `recu_le`, lot de 501 refusé, ligne fautive indexée),
   `serveur/tests/test_auth.py` (jeton haché, expiration, révocation),
   `serveur/tests/test_import.py` (v0 → v1 sur une fixture de
   `etat/jb/revues.jsonl` anonyme), `serveur/tests/test_parite.py`
   (rejoue `app/vecteurs_fsrs.py` : l'état recalculé par `app/seance.py`
   depuis le journal importé est identique).
2. `migrations/0001_initial.sql` = `serveur/schema.sql` ; `db.py` avec
   application des migrations.
3. `journal.py`, `auth.py`, `app.py` : routes `/sante`, `/journal`,
   `/journal/export`, `/auth/*`, `/profil` (GET, PATCH, DELETE), outil
   CLI `academie-etat profil creer`, `lien`.
4. `importer_journal.py` ; import du journal réel de JB sur le VPS
   (geste humain : JB lance).
5. Client : écriture locale à chaque réponse (IndexedDB ou localStorage
   structuré), file d'envoi, `POST /journal` par lots, reprise au
   retour du réseau, `rejets`. `ts-fsrs` n'entre pas ici : le client
   actuel compose sans FSRS ; la parité FSRS côté client est portée par
   ACA-FRONT-2, la parité côté serveur par le test 1.
6. `deploy/` : unité systemd, extrait Caddy, `installer.sh` idempotent.
7. Preuve sur le VPS : téléphone en avion, dix cartes, retour réseau,
   Mac le soir ; export JSON identique des deux côtés.

## Ce qu'on ne fait pas

- Pas de comptes, pas de mail, pas de cercles, pas de livraisons (autres
  chantiers).
- Pas de refonte du client, pas d'arbre.
- Pas de score stocké, pas de champ dérivé en base.
- Pas de dépendance non épinglée ; licence lue avant `pip install`.

## Preuve

```bash
python3 -m pytest serveur/tests -q
```

```bash
python3 app/tests.py && python3 tooling/check.py
```

JB voit : une réponse jouée dans le tram, relisible le soir sur le Mac
dans l'export du journal, avec la même stabilité FSRS calculée par
`python3 app/progression.py`.

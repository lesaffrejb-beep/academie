# deploy/ : le VPS, et l'auto-hébergement

État au 02/09/2026 : `academie-publication.service` et son timer
publient chaque jour à 05:15 la banque validée
(`genere.py --couches banque`) vers `/var/lib/academie/publication/`,
que Caddy sert sous `/academie/` (`socle/infra/Caddyfile`). C'est ce
qui existe et tourne.

Ce que le chantier `ACA-JOURNAL-SYNC-1` puis `ACA-FRONT-2` ajoutent :

| Fichier à créer | Rôle |
|---|---|
| `academie-etat.service` | l'API d'état (`serveur/`), utilisateur `academie`, port `8790`, `ProtectSystem=strict`, `ReadWritePaths=/var/lib/academie` |
| `academie-publication.service` (modifié) | après `genere.py`, construire `web/` et copier `dist/` dans la publication |
| `Caddyfile.academie` | l'extrait à coller dans le Caddyfile du socle : `/academie/api/*` vers `127.0.0.1:8790`, le reste statique, en-têtes de cache, `Content-Security-Policy` sans tiers |
| `sauvegarde-academie.service` et `.timer` | copie nocturne de `/var/lib/academie/` (SQLite en `VACUUM INTO`, banques, publication) vers le dossier de sauvegarde du socle |
| `installer.sh` | l'installation en cinq étapes ci-dessous, idempotente |

## Installer chez soi (un copain qui reprend le dépôt)

Sur un Linux avec Python 3.12, Node 20, Caddy, git :

1. Cloner le dépôt, créer l'utilisateur système `academie`, créer
   `/var/lib/academie/{publication,banques,sauvegardes}` et
   `/etc/academie/` (root, 600).
2. `python3 app/tests.py` et `python3 tooling/check.py` verts.
3. Installer les unités systemd de ce dossier, activer les timers.
4. Coller `Caddyfile.academie` dans son Caddyfile, recharger Caddy.
5. Créer son profil avec l'outil de ligne de commande du serveur, se
   connecter, jouer.

Aucune dépendance à labor, au socle PostGIS ni à un fournisseur de
modèle ; un seul service tiers, le fournisseur d'envoi de mail des magic
links (`decisions/0020`). La fabrication de contenu se fait ailleurs, sur
la machine du joueur (`gabarit-domaine/USINE.md`).

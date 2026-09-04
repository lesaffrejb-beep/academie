# deploy/ : le VPS, et l'auto-hébergement

**Reprise du 04/09, publication demandée par JB :** [état livré, limites et suite](../travail/2026-09-04-publication-et-suite.md). Ce point actualise les mentions historiques de pause et de publication ci-dessous.

État au 02/09/2026 : `academie-publication.service` et son timer
publient chaque jour à 05:15 la banque validée
(`genere.py --couches banque`) vers `/var/lib/academie/publication/`,
que Caddy sert sous `/academie/` (`socle/infra/Caddyfile`). C'est ce
qui existe et tourne.

Ce que `ACA-JOURNAL-SYNC-1` a ajouté le 03/09/2026 (à installer sur le
VPS par `deploy/installer.sh`, geste humain) :

| Fichier | Rôle |
|---|---|
| `academie-etat.service` | l'API d'état (`serveur/`, stdlib), utilisateur `academie`, port `8790`, `ProtectSystem=strict`, base `/var/lib/academie/etat.sqlite` |
| `Caddyfile.academie` | l'extrait à coller dans le Caddyfile du socle : `/academie/api/*` vers `127.0.0.1:8790`, le reste statique, CSP sans tiers |
| `sauvegarde-academie.service` et `.timer` | copie nocturne à 04:30 de `/var/lib/academie/` (SQLite en `VACUUM INTO`, banques, publication), trente jours gardés |
| `installer.sh` | l'installation en cinq étapes ci-dessous, idempotente |

Le service Node présent dans le dépôt prépare désormais le client complet.
Il n’est pas installé sur le VPS, où Node est absent : le client a été
construit sur le Mac et transféré le 04/09. Le service Python existant
continue à générer uniquement la banque. L’accès de Caddy au dossier
reste bloqué par les permissions ; modification des ACL refusée par la
revue automatique, en attente d’autorisation explicite de JB. Voir le
point de publication lié en tête pour les preuves et le périmètre.

État au 03/09 au soir : installé sur le VPS (`installer.sh` passé,
`academie-etat.service` et `sauvegarde-academie.timer` actifs, bloc
`/academie/api/*` dans le Caddyfile du socle, profil `JB` créé, lien
magique généré). Reste l'étape 7 du cahier, la preuve téléphone-Mac,
et l'import du journal v0 si JB en a un.

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

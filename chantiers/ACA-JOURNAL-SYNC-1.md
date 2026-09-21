# Cahier ACA-JOURNAL-SYNC-1 : l'état joueur sur le VPS, le client hors-ligne

Résultat attendu : l'état joueur vit sur le VPS et le client joue
hors-ligne ; API d'état (`serveur/API.md`), SQLite (`serveur/schema.sql`),
client qui écrit localement et synchronise par union, FSRS en parité des
deux côtés.
Fini quand : les défauts de rejeu et d'acquittement ci-dessous sont corrigés
et relus indépendamment ; le test de parité contre
`app/vecteurs_fsrs.py` est vert ; rejouer un lot ne change rien ;
`app/tests.py` et `tooling/check.py` verts.
La preuve physique téléphone/Mac est conservée dans ACA-PUBLICATION-2
(séparation des preuves, décision 0035).
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

L'étape 7 et les gestes d'installation sont exécutés et attestés dans
ACA-PUBLICATION-2 ; ils ne sont pas déclarés accomplis par les tests locaux.

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

## Reprise prioritaire : ordre chronologique (04/09/2026)

Defaut reproduit, correctif non commence lors de l'arret demande par JB.
Le client ecrit maintenant la date locale avec son decalage ISO pour
conserver le jour joue. Les lecteurs trient encore `quand` comme du
texte : deux decalages peuvent inverser les revisions. La parite actuelle
Python/TypeScript ne detecte pas ce defaut commun.

Reproduction executee sur les vraies fonctions des deux moteurs : meme
carte, note 4 a `2026-10-25T02:50:00+02:00` (00:50 UTC), puis note 1 a
`2026-10-25T02:10:00+01:00` (01:10 UTC). Le tri actuel rejoue [1, 4],
donne une derniere note 4, une stabilite 0,42437996387663374, une
difficulte 5,200020369516838 et une echeance le 26 octobre. L'ordre reel
[4, 1] donne une derniere note 1, une stabilite 2,5625081682260777, une
difficulte 7,0269895692968385 et une echeance le 28 octobre.

Ajustement cible du perimetre, autorise pour la reprise :

1. Ecrire les tests rouges de changement d'heure, de melange UTC/local et
   d'evenements simultanes recus dans des ordres differents. Verifier les
   lecteurs et le rejeu FSRS Python/TypeScript, pas seulement un tri isole.
2. Corriger `app/seance.py` (`lit_journal`, `etats_cartes`),
   `app/erreurs.py` (`lit_carnet`), `serveur/importer_journal.py`
   (`migrer_fichier`), `serveur/academie_etat/journal.py` (`exporter`),
   `web/src/moteur/journal.ts` (`litJournal`) et
   `web/src/moteur/etats.ts` (`trieJournal`), avec leurs tests associes.
   Cet ajustement borne remplace les exclusions historiques de
   `app/seance.py` et `web/` ci-dessus pour ce correctif uniquement.
3. Trier par instant reel puis departager par `(quand, mode, nonce)`
   dans un ordre de caracteres identique des deux cotes, sans collation
   dependante de la langue. Traiter explicitement les fractions de
   seconde : le contrat les accepte au-dela de la milliseconde, que
   `Date.parse` seul ne distingue pas. Definir et tester le traitement
   des anciens horodatages sans decalage, sans dependre du fuseau machine.
4. Ne modifier aucune ligne append-only, identite, nonce ni date portee.
   `jourOrdinal` continue de lire la date locale de la chaine. Le curseur
   de transport `recu_le` est distinct du tri de rejeu et reste inchange.
   Aucun changement de parametres FSRS ni nouvelle mecanique.
5. Exiger les preuves rouges puis vertes, les tests de parite,
   `python3 app/tests.py` puis `python3 tooling/check.py` avant de
   considerer ce correctif termine. Pas de publication avec ce defaut
   presente comme resolu.

## Reprise du 05/09 : acquittement invalide

La vraie fonction de synchronisation a été exécutée avec un transport de
test renvoyant HTTP 200 et `{}`. Un événement reste dans le journal local
mais disparaît de la file d'envoi : aucune réception serveur n'est prouvée.
Preuve : `travail/audit-2026-09-05/preuves/api-200-vide.json`.

Périmètre complémentaire : `web/src/donnees/api.ts`,
`web/src/moteur/journal.ts`, leurs contrats et tests. Écrire d'abord les
régressions pour corps vide, objet incomplet, types/chiffres incohérents,
rejets mal formés, puis un lot valide avec acceptés/doublons/rejets et reprise.
Valider le schéma et la cohérence de l'acquittement avant toute suppression
dans la file. Une réponse ambiguë garde les événements en attente et une
erreur visible ; pas de changement du journal append-only. Vérifier aussi
le contrat des lectures, sans transformer un échec en faux succès.

## Régression révélée par le parcours Étude

05/09 : l'émission tronquée à la seconde réordonnait les étapes rapides
lors du rejeu. Extension bornée : horodatage logique local strictement
croissant à la microseconde, marque atomique dans IndexedDB, sans changer
les dates des événements déjà présents ni les imports explicites.
Les contrôles de concurrence, redémarrage et recul d'horloge sont dans
web/src/moteur/journal.monotone.test.ts ; les E2E vérifient IndexedDB réel.
Une horloge reculée produit une date logique, pas une nouvelle mesure
du temps physique. Voir travail/relecture-journal-2026-09-05.md.

## Annexe du 21/09/2026 : régression du nonce restaurée

Le commit upstream `cde6609` (compat Windows, `tests_chaine`) a remplacé
par accident, dans `serveur/importer_journal.py` ligne 51, la condition
`if mode in MODES_V1 and "nonce" in v0:` par `if False:`. Le nonce d'une
ligne déjà v1 n'était plus gardé : `migrer_revue` recalculait une
empreinte SHA-256, changeait l'identité d'un événement déjà synchronisé
et cassait l'idempotence de l'union.

Preuve rouge, avant correctif : `python3 app/tests_serveur.py` rend
`FAILED (failures=9)` sur 47 tests, dont
`test_import.TestImport.test_un_export_deja_v1_garde_son_identite_et_ses_champs`
et `test_onboarding.Onboarding.test_export_restauration_cursus`, qui
voient le nonce d'origine remplacé par une empreinte calculée.
`app/tests.py` déclarait déjà cette mutation.

Correctif : la condition attendue est restaurée telle quelle, aucun
autre changement dans le fichier. Comme le texte est exactement la
mutation déjà déclarée dans `app/tests.py` ("l'import change le nonce
d'un evenement deja v1"), aucun test miroir n'est ajouté.

Preuve verte, après correctif : `python3 app/tests_serveur.py` rend `OK`
sur 47 tests. Aucune mutation globale n'a été lancée.

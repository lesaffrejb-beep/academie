# Relecture indépendante du correctif ACA-JOURNAL-SYNC-1

Date : 05/09/2026. Outil : Codex. Modèle : GPT-6, variante précise non exposée au relecteur. Agent : `/root/revue_journal`. Session effective : `01a0704e-9ca8-7d61-ab86-f6d816dbbb9a` (variable `CODEX_THREAD_ID`). Mission reçue de l'agent principal : audit indépendant du correctif de journal, tests adverses et corrections ciblées autorisés. Aucun push ni déploiement.

## Verdict

Le correctif initial ne pouvait pas être clôturé : quatre défauts supplémentaires ont été reproduits. Les corrections ciblées décrites ci-dessous passent leurs contre-exemples et les contrôles globaux. Aucun autre bloquant observé dans le périmètre examiné. Les corrections écrites par le relecteur restent à examiner par l'agent principal : cette relecture indépendante ne constitue pas une auto-certification de leur auteur.

Ce verdict porte sur les preuves logicielles locales. Il ne prouve ni publication VPS ni synchronisation physique téléphone–Mac ni absence absolue de défaut.

## Contre-exemples et corrections

1. `app/erreurs.py` importait la nouvelle clé mais `lit_carnet` triait encore le texte. Le changement d'heure `02:50+02:00` puis `02:10+01:00` apparaissait à l'envers. Correction : même clé chronologique que les autres lecteurs. Le test vérifie aussi l'absence de réécriture du fichier.
2. Le comparateur TypeScript utilisait les unités UTF-16 ; Python utilise les points de code Unicode. À instant égal, `U+10000` passait avant `U+E000` côté client, après côté Python. Correction : comparaison par points de code, avec test exécutant réellement le tri Python depuis TypeScript. Les fractions de 31 décimales, sans troncature, restent distinguées.
3. `Date.parse` acceptait le 30 février en le normalisant. Un tel curseur permettait de retirer une réponse de la file et d'avancer la marque. Correction : validation des composantes calendaires avant acceptation du corps. Les longueurs des nonces et textes reçus suivent aussi les points de code, comme Python ; les formats et jours doivent être des chaînes, sans coercition de tableau.
4. Un HTTP 422 contenant `erreur: ligne-invalide`, un index valide et un motif absent, nul ou non textuel retirait la réponse de la file. Correction : seul un refus avec code et motif textuels expose l'index au mécanisme de mise à l'écart. Tout refus ambigu laisse la file intacte et retourne une erreur visible.

Les tests adverses ne remplacent pas l'API par un faux acquittement typé : ils passent par de vraies `Response`, `api.envoieJournal` et `synchronise`. Seul le stockage Dexie est simulé en mémoire pour ce test unitaire. Un lot avec refus explicite puis doublon est acquitté, le journal conserve ses deux événements. Un HTTP 200 vide ou `{}` conserve la file et le curseur.

## Preuves rejouables

Avant corrections : suite Python de relecture, 1 échec sur 4 ; suite TypeScript de relecture initiale, 8 échecs sur 11. Échecs constatés sur le carnet, Unicode, calendrier et refus HTTP 422.

Après corrections :

- `PYTHONPATH=app python3 -m unittest app/tests_chronologie_relecture.py` : 4 tests verts. Anciens horodatages sans zone, UTC/local équivalents, Unicode, longues fractions avant/après l'époque Unix et carnet.
- `PYTHONPATH=serveur/tests:serveur python3 -m unittest test_chronologie_relecture test_journal test_import test_parite` : 21 tests verts. L'import et l'export conservent les identités, trient offsets/fractions/Unicode et restent idempotents.
- Depuis `web/`, `npx vitest run src/moteur/journal.relecture.test.ts src/moteur/chronologie.test.ts src/moteur/journal.test.ts src/donnees/api.test.ts src/moteur/parite.test.ts` : 83 tests verts, dont 39 de parité FSRS et 13 de relecture indépendante, avec Vitest 2.1.8 du dépôt.
- Depuis `web/`, `npx tsc --noEmit` : code de sortie 0.
- `python3 app/tests.py` puis `python3 tooling/check.py` : `TOUT VERT`, puis `Académie : 0 erreur(s)`.

La première exécution globale en sandbox échouait uniquement sur l'ouverture de la socket HTTP locale. La reprise autorisée hors sandbox passe, sans modification du test. Les avertissements `ResourceWarning` des anciennes fixtures SQLite ne sont pas de nouveaux échecs de cette correction.

## Fichiers ajoutés par la relecture

- `app/tests_chronologie_relecture.py` : contre-exemples indépendants Python.
- `serveur/tests/test_chronologie_relecture.py` : import/export et identités append-only.
- `web/src/moteur/journal.relecture.test.ts` : vrai chemin de transport et parité Unicode.

Fichiers corrigés : `app/erreurs.py`, `web/src/moteur/chronologie.ts`, `web/src/donnees/api.ts`. Le correctif ne change ni les paramètres FSRS ni les dates/identités stockées ni le curseur serveur `recu_le`. Aucun contenu pédagogique ou composant visuel modifié.

## Complément : ordre de création locale pendant une étude

Nouvelle demande de l'agent principal après reproduction navigateur d'une reprise revenant à une étape antérieure et d'une synthèse retrouvant une ancienne réponse. Cette observation révèle une limite du premier verdict : un tri déterministe par identité ne restitue pas l'ordre de création lorsque l'émetteur tronque tous les événements rapides à la même seconde.

La suite dédiée `web/src/moteur/journal.monotone.test.ts` reproduit cinq échecs avant correction : fraction de la vraie horloge perdue, étapes et réponses rapides réordonnées, recul de l'horloge, rechargement/second onglet simulé, ancien journal sans marque de création. Le test d'import explicite passe déjà avant correction.

Correction limitée à `web/src/moteur/journal.ts` :

- `maintenant()` conserve désormais la fraction de la vraie horloge, sans imposer une fraction nulle aux anciens appelants.
- `ecris()` alloue aux événements sans date explicite un instant logique en microsecondes, égal à l'horloge physique ou strictement supérieur au précédent instant local si nécessaire.
- La marque `creation-microsecondes` est persistée dans le magasin `marques`, dans la même transaction `rw` que l'événement et sa file d'envoi. Les transactions IndexedDB qui partagent ces magasins sont sérialisées entre onglets ; aucune variable de module ne porte l'ordre.
- Au premier usage d'un ancien état dépourvu de marque, le dernier instant du journal amorce l'horloge. Une fraction ancienne plus fine que la microseconde est dépassée au tick suivant. Aucun ancien horodatage, nonce ni contenu n'est modifié.
- Une date fournie explicitement reste strictement celle fournie. La date locale et son décalage sont calculés pour l'instant logique, y compris lors du changement d'heure.

Limite explicite : si l'horloge machine recule, les nouvelles dates automatiques suivent provisoirement l'horloge logique persistée ; elles ne prétendent pas mesurer fidèlement ce recul physique. Un ancien événement daté dans le futur peut aussi avancer cet amorçage. Cette politique préserve l'ordre local des nouvelles actions et ne résout pas l'ordre causal global entre appareils indépendants. Aucun changement de contrat, migration de lignes ni paramètre FSRS.

Après correction, 94 tests ciblés passent avec Vitest 2.1.8 : journal, contre-exemples transport, chronologie, étude, parité FSRS, API et sept scénarios monotones. `npx tsc --noEmit` passe. Le septième scénario vérifie le franchissement d'une seconde à la transition d'heure d'hiver : l'instant local passe de `02:59:59.999999+02:00` à `02:00:00.000000+01:00` tout en restant strictement croissant.

Le stockage des tests unitaires est simulé avec sérialisation et persistance commune entre deux instances du module. Cela prouve le calcul, la reprise et l'utilisation de la marque, pas à lui seul le verrouillage réel du navigateur. La suite E2E en cours chez l'agent principal fournit cette couche supplémentaire ; aucune réussite E2E non observée n'est affirmée ici.

Contrôles globaux rejoués après ce complément : `python3 app/tests.py` retourne `TOUT VERT`. `python3 tooling/check.py` signale une erreur de voix dans `web/src/donnees/api.etude.test.ts` (emoji), fichier modifié parallèlement hors de ce sous-périmètre. Signalement transmis à l'agent principal ; aucune modification de ce fichier par le relecteur.

## Contre-passe du coordinateur après intégration

05/09, Codex/GPT-6, session principale distincte. Les corrections du carnet,
de l'ordre Unicode, du calendrier et des refus422 ont été examinées dans
les fichiers intégrés ; les tests adverses passent via les vraies fonctions
d'API et de synchronisation. L'émission locale a été examinée séparément :
la marque est dans la même transaction que journal/file, le `quand` explicite
reste inchangé et les anciens événements ne sont pas réécrits. La date
logique en cas de recul d'horloge est une limite documentée. Les nouveaux
E2E rejouent QCM/rechargement et étude entière avec IndexedDB réel.
Résultats consolidés dans experience-2026-09-05/LIVRAISON.md ; aucune preuve
distante ou humaine n'est déduite de cette contre-passe.

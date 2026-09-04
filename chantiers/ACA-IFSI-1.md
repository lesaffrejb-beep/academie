# Cahier ACA-IFSI-1 : corriger le programme infirmier

Demande de JB du 04/09/2026 : appliquer les modifications pertinentes
de la critique apportée dans cette session. Cette demande autorise ce
chantier local et ses choix techniques réversibles.

## Résultat et périmètre

Un programme courant indexé sur le référentiel 2026, une copie historique
intacte du squelette 2009, trois préparations distinctes, des objectifs
numériques qui ne promettent pas une habilitation clinique. Le programme
reste un inventaire à écrire, pas une banque jouable.

Fichiers : `programme/ifsi.json`, `programme/versions/ifsi-2009.json`,
`programme/genere_ifsi.py`, `programme/catalogue.json`,
`programme/README.md`, `SYLLABUS-IFSI.md`, `app/valide_ifsi.py`,
`app/tests_ifsi.py`, `app/valide_programme.py`, `app/tests.py` (ajout
ciblé de suite et mutation), ce cahier, `roadmap.json`, `ROADMAP.md`,
`README.md`, `METHODE.md`, `decisions/0033-ifsi-referentiel-2026.md`,
`decisions/README.md`, `travail/2026-09-04-revision-ifsi.md` et
`sources/f34fc8af2597118f*` (lecture de la critique par l'usine).

Ne touche pas au front, à la banque, aux journaux joueurs, aux services,
au programme copro ni aux modifications préexistantes d'autres travaux.

## Étapes nommées

1. Lire la critique par l'usine ; vérifier les affirmations
   réglementaires dans les textes officiels ; conserver les limites des
   preuves. Déclaration : Codex, gpt-5.6-sol (configuration locale), grand.
2. Écrire et constater les tests rouges : référentiel absent, rattachement
   inconnu, parcours mélangés, prérequis cassé, geste certifié par un score,
   historique altéré et générateur qui réécrirait la source.
3. Copier le programme original à l'identique dans `programme/versions/`.
   Corriger l'inventaire courant, conserver les identifiants existants,
   ajouter des branches manquantes, des objectifs fins, des axes séparés
   (étape, difficulté, criticité) et un rattachement pédagogique explicite
   aux compétences officielles. Le rattachement reste une proposition
   éditoriale, pas une équivalence validée par un IFSI.
4. Rendre le JSON canonique : le générateur ne produit que le syllabus,
   après validation. Contrôler l'extension IFSI sans imposer sa taxonomie
   au moteur commun. Les niveaux historiques restent une compatibilité ;
   ils ne désignent plus une année ni une aptitude clinique.
5. Consigner les arbitrages, le traitement de la critique et les limites
   de ce lot. Les moteurs de cas, la maîtrise critique et les preuves
   cliniques sont spécifiés pour les prochains lots, sans états fictifs.
6. Relecture indépendante, génération reproductible, puis
   `python3 app/tests.py` et `python3 tooling/check.py`.

## Preuve attendue

Tous les anciens identifiants subsistent ; copie historique identique ;
chaque chapitre courant possède un mapping et une décision éditoriale ;
les parcours Parcoursup, FPC et spécifiques ont chacun douze semaines
et leur diagnostic ; les référentiels et liens sont cohérents ; les
compteurs sont calculés ; les mutations de garde-fous échouent.

Pas de contenu clinique servi, de publication ni de changement d'état
joueur dans ce chantier. Les durées d'étude sont des choix éditoriaux.

## Sortie locale du 04/09/2026

21 tests IFSI passent ; les nouveaux tests ont d'abord échoué sur
l'historique des ajouts et l'ordre des étapes. Les trois mutations IFSI
sont détectées sur une copie isolée. `app/tests.py` passe avec la socket
locale du test serveur autorisée ; `tooling/check.py` ne relève aucune
erreur. La contre-relecture indépendante du cadrage est favorable après
correction de ses réserves. Le détail durable est dans
`travail/2026-09-04-revision-ifsi.md`.

Le troisième rapport transmis par JB a réduit la finition à un inventaire
honnête : 375 chapitres conservés, 600 capacités de cadrage ; notions
conservées, objectifs fins à éprouver au pilote. Le syllabus est régénéré
et le catalogue aligné. La preuve de compétence clinique et les moteurs
de cas restent hors de ce chantier.

# Roadmap Académie, active (réécrite le 02/09/2026)

L'Académie transforme des sources vérifiées en un arbre de compétences
qu'on conquiert chaque jour. Elle échoue si elle est belle et n'est pas
ouverte le matin, si elle récompense des clics sans améliorer la
rétention et le transfert, ou si elle enseigne une bêtise.

Cette page est la seule roadmap active ; `roadmap.json` est la file
exécutable (`python3 tooling/roadmap.py next` ne choisit qu'un item
`ready`, sûr et sans dépendance ouverte). Le cadrage d'août est dans
[`archive/`](archive/roadmaps/README.md). Les décisions qui fondent
cette roadmap sont dans [`decisions/`](decisions/README.md).

## La preuve recherchée

- au moins quatre séances par semaine, sans culpabilisation après une
  coupure ;
- une séance jouable en moins de trois secondes, hors-ligne, sur
  téléphone et sur ordinateur, terminable à tout moment ;
- une réponse jouée dans le tram relisible sur le Mac le soir ;
- rétention à froid mesurée après environ trente séances, et une
  calibration qui s'améliore ;
- 100 % des cartes servies valides, avec leur provenance, la nature de
  leurs sources et leur note de confiance affichées ;
- le coût de fabrication d'un chapitre connu avant d'en promettre.

## Maintenant : prouver le rituel et poser les fondations v2

Ce qui est fait le 02/09 : doctrine v2, programme en données, contrats
v2 proposés, squelette du serveur et du client, maquette du front. Le
03/09 : l'état synchronisé (`ACA-JOURNAL-SYNC-1`), le programme validé
(`ACA-PROGRAMME-1`), le squelette technique du client, le registre des
sources (`ACA-SOURCES-1`). Le contrat v2 (`ACA-CONTRAT-2`) est ouvert.

1. **L'état synchronisé** (`ACA-JOURNAL-SYNC-1`) : API d'état, SQLite,
   client hors-ligne, parité FSRS. C'est le maillon manquant depuis
   août ; sans lui aucun gate ne se mesure.
2. **Le tableau de bord du rituel** (`ACA-RITUAL-METRICS-1`) et **les
   trente séances de JB** (`ACA-RITUAL-1`). Le rituel reste le gate de
   tout ce qui est multi-joueur.
3. **Le programme validé** (`ACA-PROGRAMME-1`) : valideur, clés de
   `academie.json` alignées, calibrage des niveaux par agent frais.
4. **Le registre des sources** (`ACA-SOURCES-1`, fait le 03/09) : nature
   et parti sur les 154 sources des 84 cartes, `sources/registre.json`
   qui fait foi, liste blanche v1. Deux trous nommés en sont sortis : le
   référentiel qui fonde P1 à P5, et l'arrêt du 18/06/2026 sans numéro
   de pourvoi.
5. **La réutilisation** (`ACA-REUSE-1`) : licences lues à la source,
   verdict par candidat, avant la première ligne du client.
6. **Le contrat v2** (`ACA-CONTRAT-2`) : cartes, chapitres, valideur,
   migration, dans le même commit.

## Ensuite : le produit v2 pour un joueur

1. **Le client v2** (`ACA-FRONT-2`) : l'arbre, la séance, le profil,
   sur la maquette du 02/09 ; remplace l'archipel ; `check.py` mis à
   jour.
   L'arrivée d'un élève (pseudo, catalogue, « Créer le vôtre » avec les
   prompts à coller) suit dans `ACA-ONBOARDING-1` ; d'ici là, l'accueil
   est `COMMENCER.md` (`decisions/0027`).
2. **La semaine type et le socle** (`ACA-SEMAINE-1`) dans le composeur.
3. **L'étude** (`ACA-ETUDE-1`) sur trois chapitres pilotes, puis
   **les épreuves** (`ACA-EXAMEN-1`), **la boîte** (`ACA-BOITE-1`),
   **la journée** (`ACA-JOURNEE-1`), **le papier** (`ACA-PAPIER-1`).
4. **Le contenu** (`ACA-CONTENT-MAP-1`, `ACA-CONTENT-2`) : les domaines
   du socle en niveaux 1 et 2, par lots de chapitres, double passe,
   échantillon humain ; un arrivant ne valide jamais seul une matière
   qu'il découvre.
5. **L'audit** (`ACA-AUDIT-1`) : rapport HTML par banque, dossier de
   carte, péremption du droit ; puis **les runs de vérification**
   (`ACA-VERIF-1`) : un tirage de cartes revérifié sur les sources
   fiables, historique écrit, statuts qui bougent.
6. **La réponse libre** (`ACA-RESPONSE-1`) : expérience bornée sur un
   petit lot, coût par correction mesuré.

## Plus tard : ouvrir sans détruire le produit

1. **Les comptes et le RGPD** (`ACA-MULTI-DECISION-1`) : JB arbitre
   authentification, suppression sous 48 h, sous-traitant mail, après
   le bilan des trente séances et quatre semaines de plus.
2. **Les cercles** (`ACA-CERCLE-1`) : tous les joueurs se voient par
   défaut, chacun peut se masquer, carnet privé ; fil, kudos, défis ;
   puis **la ligue** (`ACA-LIGUE-1`) et **le tuteur** (`ACA-TUTEUR-1`).
3. **La bibliothèque commune** (`ACA-BIBLIOTHEQUE-1`) : livraisons,
   quarantaine, licence du contenu, un domaine fabriqué par l'un
   adoptable par l'autre.
4. **Le kit de domaine** (`ACA-DOMAIN-KIT-1`) éprouvé avec Arthur ;
   **l'auto-hébergement** (`ACA-SELFHOST-1`) éprouvé par un copain.
5. **Les médias** (`ACA-MEDIA-1`) : photothèque de terrain, écoute,
   podcast de chapitre. **Le canal labor** (`ACA-ERP-1`) : anonymisé,
   validé, scanné. **L'optimiseur FSRS** (`ACA-OPTIMISEUR-1`) à
   quatre cents révisions.

## Questions d'architecture déjà tranchées

`ARCHITECTURE.md` fait foi : moteur Python de référence ; serveur
Python + SQLite ; client React + TypeScript + PWA, jetable ; FSRS des
deux côtés avec vecteurs de parité ; état sur le VPS, hors git ; sources
chez le joueur ; aucun appel de modèle côté serveur ; aucun tiers.

## Garde-fous de produit

- Pas de dette, pas de série qui casse, pas de classement public, pas
  de monnaie, pas d'avatar, pas de confettis.
- Rien de multi-joueur avant la preuve du rituel ; rien de social sans
  la suppression de compte.
- Aucune donnée client de labor, même dans un prompt.
- Une carte fausse sort du service immédiatement, puis se corrige à la
  source.
- Une mécanique sans entrée dans `METHODE.md` n'entre pas.
- Le temps humain de validation est plafonné : dix minutes par semaine
  pour le propriétaire du domaine ; si ça déborde, on baisse le neuf.
- Quinze items `ready` au plus dans `roadmap.json`.

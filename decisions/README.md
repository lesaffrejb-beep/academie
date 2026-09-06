# Registre des décisions

Une décision structurante = un fichier daté ici, même gabarit que
`labor/meta/adr/` : **Décision** (une phrase), **Contexte** (l'état du
système ce jour-là), **Conséquences** (ce que ça oblige, ce que ça
casse), **Réouverture** (le signal qui autorise à y revenir). Une règle
qui change : nouvelle décision, l'ancienne passe en « remplacée par »,
jamais réécrite.

Ce qui mérite une décision : un arbitrage de JB qui contredit une
pratique antérieure, un choix qu'un agent frais ne devinerait pas en
lisant le dépôt, une règle née d'un incident. Pas l'avancement
(`ROADMAP.md`), pas la veille (`lab/VEILLE.md`).

| N° | Date | Décision |
|---|---|---|
| [0001](0001-arbre-au-lieu-de-l-archipel.md) | 02/09/2026 | L'arbre de compétences remplace l'archipel comme habillage ; le graphe de progression reste |
| [0002](0002-le-chapitre-unite-de-contenu.md) | 02/09/2026 | Le chapitre est l'unité de contenu ; la carte reste l'unité de mémoire |
| [0003](0003-cinq-niveaux-et-la-synthese.md) | 02/09/2026 | Cinq niveaux de profondeur ; la synthèse commence au niveau 3 et clôt tout chapitre |
| [0004](0004-la-source-porte-sa-nature-et-son-parti.md) | 02/09/2026 | Une source porte sa nature et son parti, affichés au joueur |
| [0005](0005-trois-formats-de-temps.md) | 02/09/2026 | Trois formats de temps : séance, étude, journée ; le neuf est plafonné même en journée |
| [0006](0006-etat-joueur-sur-le-serveur-client-hors-ligne.md) | 02/09/2026 | L'état joueur vit sur le VPS, le client est hors-ligne d'abord, FSRS tourne des deux côtés avec vecteurs de parité |
| [0007](0007-stack-front-et-dependances.md) | 02/09/2026 | Le front est jetable et outillé (React, TypeScript, Vite, Motion, ts-fsrs) ; le moteur Python reste la référence |
| [0008](0008-chacun-son-depot-et-son-abonnement.md) | 02/09/2026 | Chacun son dépôt-domaine et son abonnement ; le serveur reçoit des livraisons ; aucun paiement demandé |
| [0009](0009-la-boite-et-les-chapitres-satellites.md) | 02/09/2026 | Tout ce qu'on glisse dans la boîte devient un chapitre satellite, jouable hors de l'arbre puis rattaché |
| [0010](0010-cercles-visibilite-et-aucun-reporting.md) | 02/09/2026 | Trois cercles (solo, cercle, équipe) ; visibilité symétrique et consentie par domaine ; jamais de reporting hiérarchique |
| [0011](0011-le-papier-est-un-exercice.md) | 02/09/2026 | Le papier est un mode d'exercice (dessin de mémoire, feuille blanche), jamais un support de cours |
| [0012](0012-precedence-des-documents-et-archivage.md) | 02/09/2026 | La conception d'août est archivée intacte ; la précédence des documents est celle de `DOCTRINE.md` §4 |
| [0013](0013-le-socle-et-la-liberte.md) | 02/09/2026 | La séance protège le socle, l'étude est libre ; on pondère, on ne bloque jamais |
| [0014](0014-competition-et-epreuves-transverses.md) | 02/09/2026 | La compétition compte des cartes stabilisées × niveau ; les épreuves transverses testent la compréhension |
| [0015](0015-l-arbre-est-l-avatar.md) | 02/09/2026 | Pas d'avatar : l'arbre est l'avatar, les cosmétiques décorent l'outil |
| [0016](0016-semaine-type-pas-de-saisons.md) | 02/09/2026 | Une semaine type aux jours colorés, pas de saisons |
| [0017](0017-images-et-audio.md) | 02/09/2026 | Images en trois étages (schémas maison d'abord) ; photothèque et audio plus tard |
| [0018](0018-licences-du-code-et-du-contenu.md) | 02/09/2026 | Code MIT, contenu `banque` CC BY-SA, `interne` non redistribuable (JB tranche) |
| [0019](0019-peremption-du-droit-et-veille.md) | 02/09/2026 | Le droit périme à douze mois par défaut ; la veille alimente la boîte ; une carte corrigée garde son identifiant |
| [0020](0020-telemetrie-zero-tiers.md) | 02/09/2026 | Le journal est la seule mesure, chez personne d'autre ; une notification par jour au plus, opt-in |
| [0021](0021-le-modele-ecrit-la-provenance-s-affiche.md) | 02/09/2026 | Le modèle peut écrire s'il cherche, cite, avoue et se fait relire ; tampon de provenance ; runs de vérification |
| [0022](0022-le-modele-pose-le-cadre-les-sources-corroborent-l-audit-mesure.md) | 02/09/2026 | Le modèle pose le cadre, les sources ont le dernier mot sur les faits, l'audit mesure : note A/B/C, page Confiance, audit croisé |
| [0023](0023-les-restes-tranches.md) | 03/09/2026 | Licences acceptées (MIT, CC BY-SA), noms des domaines, semaine type : tranchés par délégation |
| [0024](0024-la-voix-de-l-academie.md) | 03/09/2026 | La voix : un collègue plus avancé, tutoiement, faits et actions, jamais d'exclamation ni de mots du jeu |
| [0025](0025-le-cadre-d-execution.md) | 03/09/2026 | Un LLM ne code pas sans cahier ; les règles vivent dans des contrôles ; le contrat avant le code |
| [0026](0026-un-document-n-est-pas-un-chapitre.md) | 03/09/2026 | Un document n'est pas un chapitre : bibliothèque, pivot Markdown par page, figures rendues, abonnement d'abord, quatre voies vers l'arbre |
| [0027](0027-pas-a-pas-impose-points-de-sauvegarde-classes-de-modeles.md) | 03/09/2026 | Le pas à pas imposé : un script distribue et juge les unités, points de sauvegarde sur disque, classement historique retiré par 0034, rien sur parole ; MODELES.md, adaptateurs par outil, onboarding |
| [0028](0028-l-etat-d-un-noeud-et-la-fraicheur.md) | 03/09/2026 | L'état d'un nœud : `valide` se gagne à l'épreuve du domaine, la fraîcheur s'affiche à côté et ne déclasse jamais ; une carte se rattache par `chapitre`, le trou v1 s'écrit |
| [0029](0029-fsrs-miroir-a-la-main.md) | 04/09/2026 | Le FSRS du client est un miroir à la main de `app/planificateur.py`, jugé par les vecteurs Python à chaque test ; `ts-fsrs` n'entre pas (amende 0007) |
| [0030](0030-la-banque-se-range-par-le-programme.md) | 04/09/2026 | Les 84 cartes se rangent par le programme (21 changements de domaine acceptés) ; un trou se comble par un chapitre neuf ; P1 à P5 |
| [0031](0031-un-programme-par-metier-ifsi.md) | 04/09/2026 | Un programme par métier ; `ifsi.json` : l'arbre de l'infirmier, socle = entrée en IFSI, III = formation, IV et V au-delà |
| [0032](0032-arrivee-compte-cursus-unique-demande-de-cursus.md) | 04/09/2026 | L'arrivée : mail pro et mot de passe, choix d'un cursus (un seul à la fois, sauvegarde automatique), « nouveau cursus » = demande à JB |
| [0033](0033-ifsi-referentiel-2026.md) | 04/09/2026 | IFSI : référentiel 2026, voies distinctes, axes séparés et progression sans plafond ; amende 0031 |
| [0034](0034-capacites-sans-classes-de-modeles.md) | 05/09/2026 | Classes retirées à la demande de JB ; provenance, contrôles et compatibilité des états conservés |
| [0035](0035-roadmap-par-preuves-et-pilote-borne.md) | 05/09/2026 | Preuves logicielles, publication, usage et apprentissage séparés ; contrat pilote avant migration globale |
| [0036](0036-livraison-autonome-des-parcours.md) | 05/09/2026 | Livraison autonome des parcours |
| [0037](0037-exploration-lisible-et-preuves-durables.md) | 05/09/2026 | Exploration lisible et preuves durables |
| [0038](0038-architecture-des-tokens-et-micro-interactions.md) | 05/09/2026 | Architecture des tokens 100 % portable, dendrogramme 360° et micro-animations tactiles |
| [0039](0039-modules-interactifs-salle-de-seance.md) | 05/09/2026 | Modules interactifs spécialisés en séance (rôle, relier, plan, datation, synthèse) |
| [0040](0040-modules-progression-ligue-trophees-insignes-ponts-passeport.md) | 05/09/2026 | Modules de progression : passeport, ligue hebdomadaire, trophées, insignes et ponts |
| [0041](0041-micro-animations-dopamine-exp-rituel.md) | 05/09/2026 | Micro-animations satisfaisantes : retour dopamine d'EXP, jauge liquide et rituel tactile |
| [0042](0042-essai-comptes-et-eleves.md) | 05/09/2026 | Essai : comptes, cursus et sauvegardes séparées |

| [0043](0043-palette-bleue-et-livraison-essai.md) | 05/09/2026 | Palette bleue et publication de l’essai autorisée par JB |
| [0044](0044-acces-compte-et-reprise.md) | 05/09/2026 | Accueil accessible, compte personnel et reprise explicite du travail |
| [0045](0045-acces-local-phrase-et-cle-de-recuperation.md) | 06/09/2026 | Accès local par pseudo, phrase secrète et clé de récupération, sans mail |
| [0046](0046-specialisations-et-preuves-de-couverture.md) | 06/09/2026 | Spécialités transverses et distinction entre programme, contenu et expertise |
| [0047](0047-pipeline-documentaire-econome-et-auditable.md) | 06/09/2026 | Extraction locale graduée, benchmark sur pièces, assertions et sondages indépendants |
| [0048](0048-supports-visuels-du-document-aux-exercices.md) | 06/09/2026 | Figures, légendes, données spatiales et preuves d'usage dans les exercices |
| [0049](0049-pilote-documentaire-hybride-dix-pages.md) | 06/09/2026 | Dix pages croisées, supports contrôlés, étude satellite et publication isolée |

- [0050 : collecte documentaire et accès pour le premier cercle](0050-essai-lundi-collecte-et-acces.md)

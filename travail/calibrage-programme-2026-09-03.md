# Calibrage du programme copro, 03/09/2026

Chantier `ACA-PROGRAMME-1`, étape 4. Deux agents frais (Claude Opus, classe grand, n'ayant pas écrit le programme) ont noté chaque chapitre de `programme/copro.json` contre la grille de `PROGRAMME.md` §5 et `decisions/0003`, en jugeant d'abord le verbe de la compétence. Consigne : reclasser seulement quand la grille le dit clairement, un cran à la fois, et signaler tout conflit de prérequis.

| Lot | Domaines | Lus | Reclassés | Montés | Descendus |
|---|---|---|---|---|---|
| A | droit, procédure, cabinet, comptabilité, culture | 181 | 32 (31 appliqués) | 25 | 7 |
| B | pathologie, équipements, sinistres, travaux, énergie, immobilier | 206 | 16 | 12 | 4 |

Compte avant : 147 / 157 / 61 / 20 / 2 par niveau. Après : 117 / 191 / 58 / 19 / 2. Les identifiants n'ont pas bougé ; les prérequis, dérivés du niveau par le générateur, ont été recalculés et le valideur est vert.

## Ce que ça change au parcours

Quinze chapitres du trimestre 1 sont passés au niveau 2. Le parcours les garde (ce sont les gestes de la première semaine de travail : convoquer, calculer une majorité, passer une écriture) ; son texte dit désormais « niveaux 1 et 2 ». Remplacer ces chapitres par d'autres de niveau 1 serait un choix de contenu, pas de calibrage : à JB.

## Les reclassements

| Chapitre | Avant | Après | Ancre | Raison |
|---|---|---|---|---|
| `droit.statut.tantiemes-et-quotes-parts` | 1 | 2 | BTS PI | La competence demande d'expliquer d'ou viennent les tantiemes, donc un mecanisme et non un simple reperage. |
| `droit.statut.fiche-synthetique-et-immatriculation` | 1 | 2 | BTS PI | Tenir a jour une fiche et une immatriculation, c'est appliquer une procedure a un cas, pas nommer une notion. |
| `droit.assemblee.la-convocation-forme-et-delai` | 1 | 2 | BTS PI | Convoquer dans les delais et par les bons moyens est l'application d'une regle a un cas simple. |
| `droit.assemblee.tenue-de-seance-bureau-feuille-de-presence` | 1 | 2 | BTS PI | Ouvrir une seance et tenir la feuille de presence est un geste d'application, pas un vocabulaire a restituer. |
| `droit.assemblee.le-proces-verbal-et-sa-notification` | 1 | 2 | RNCP | Rediger un proces-verbal et le notifier dans le delai depasse largement le reperage de niveau 1. |
| `droit.majorites.l-article-24` (non appliqué, voir ci-dessous) | 1 | 2 | BTS PI | Calculer une majorite abstentions comprises est l'application d'une regle de calcul a un cas. |
| `droit.majorites.l-article-25-et-la-passerelle` | 1 | 2 | BTS PI | Appliquer la passerelle du second vote suppose d'enchainer deux regles, ce qui releve du mecanisme. |
| `droit.travaux.travaux-votes-et-travaux-urgents` | 1 | 2 | BTS PI | La competence distingue trois notions voisines, ce que la grille place explicitement au niveau 2. |
| `comptabilite.bases.debit-et-credit-la-partie-double` | 1 | 2 | BTS PI | Passer une ecriture est l'application d'une regle a un cas simple et non la definition d'un mot. |
| `comptabilite.bases.produits-et-charges` | 1 | 2 | BTS PI | Distinguer produit, charge et encaissement est la distinction de notions proches, typique du niveau 2. |
| `comptabilite.budget.le-budget-previsionnel` | 1 | 2 | BTS PI | Expliquer ce que couvre le budget et comment il se vote demande d'exposer un mecanisme. |
| `comptabilite.annexes.l-annexe-2-le-compte-de-gestion-general` | 1 | 2 | BTS PI | Comparer le realise au budget vote est un raisonnement, pas une simple lecture de poste. |
| `comptabilite.controle.approbation-et-quitus` | 1 | 2 | BTS PI | Distinguer approbation et quitus et leurs effets est la distinction de deux notions proches. |
| `comptabilite.impayes.relance-et-mise-en-demeure` | 1 | 2 | RNCP | Derouler la relance jusqu'a la mise en demeure est l'application d'une procedure a un dossier. |
| `comptabilite.factures.les-mentions-obligatoires-d-une-facture` | 1 | 2 | BTS PI | Verifier la conformite d'une piece avant paiement est un controle applique, au-dela du vocabulaire. |
| `comptabilite.factures.les-mentions-d-un-devis` | 1 | 2 | BTS PI | Verifier qu'un devis est complet avant de le presenter est un controle applique sur piece. |
| `procedure.avant-le-proces.mise-en-demeure-recommande-sommation` | 1 | 2 | RNCP | Ecrire une mise en demeure qui vaut suppose d'appliquer les conditions de forme et de delai a un cas. |
| `procedure.recouvrement.l-injonction-de-payer` | 1 | 2 | RNCP | Deposer une requete et gerer l'opposition est une procedure a conduire, pas une notion a nommer. |
| `cabinet.profession.le-code-de-deontologie` | 1 | 2 | RNCP | Appliquer les regles deontologiques aux cas courants est explicitement une competence de niveau 2. |
| `cabinet.conseil-syndical.role-et-reunion` | 1 | 2 | RNCP | Preparer et tenir une reunion est une conduite d'action, pas une restitution de role. |
| `cabinet.assemblee-en-pratique.animer-et-tenir-le-bureau` | 1 | 2 | RNCP | Animer une seance et tenir le bureau demande d'appliquer des regles en situation reelle. |
| `cabinet.ecrire.courrier-mail-notification` | 1 | 2 | BTS PI | Choisir le support et la forme suppose de comparer des regimes de notification et de trancher. |
| `cabinet.negocier.avec-un-prestataire` | 1 | 2 | RNCP | Negocier un devis ou un contrat est une mise en oeuvre en situation, jamais un simple repere. |
| `cabinet.donnees.le-rgpd-au-cabinet` | 1 | 2 | RNCP | Appliquer le RGPD aux donnees des coproprietaires est l'application d'une regle a des cas concrets. |
| `cabinet.charge.gerer-son-temps-et-deleguer` | 1 | 2 | RNCP | Organiser une semaine et deleguer suppose d'appliquer une methode, pas de nommer des priorites. |
| `comptabilite.plan-comptable.les-comptes-qu-on-lit-tous-les-jours` | 2 | 1 | BTS PI | Reconnaitre les comptes courants d'un grand livre reste de la reconnaissance de vocabulaire. |
| `comptabilite.budget.le-pret-avance-mutation-et-les-financements-nouveaux` | 2 | 1 | BTS PI | La competence se limite a dire ce qu'est le dispositif et a qui il sert, donc a le definir. |
| `procedure.lire.visa-moyens-motifs-dispositif` | 2 | 1 | BTS PI | Reperer les parties d'un arret est une reconnaissance de structure, sans raisonnement sur la regle. |
| `culture.lectures.l-architecture-et-ses-styles` | 2 | 1 | BTS PI | Reconnaitre des styles est un exercice de reperage visuel et de vocabulaire. |
| `culture.lectures.la-propriete-les-textes-fondateurs` | 3 | 2 | BTS PI | Restituer la these d'un texte reste de la comprehension expliquee, sans diagnostic ni production. |
| `culture.lectures.l-habiter-et-le-voisinage` | 3 | 2 | BTS PI | Restituer un texte n'engage ni decision ni redaction professionnelle, donc pas le niveau praticien. |
| `culture.lectures.la-ville` | 3 | 2 | BTS PI | Restituer un texte sur la ville releve de l'explication et non de la pratique diagnostique. |
| `pathologie.materiaux.les-isolants` | 2 | 1 | BTS PI | La compétence se limite à nommer les isolants et leurs défauts, ce qui est le verbe du niveau 1. |
| `pathologie.materiaux.reconnaitre-un-materiau-sur-photo` | 3 | 2 | BTS PI | Identifier un matériau sur une photo relève de la reconnaissance appliquée, pas du diagnostic ni de la rédaction. |
| `equipements.acces.desenfumage-et-extincteurs` | 2 | 1 | BTS PI | Dire ce que la réglementation incendie impose est un repérage d'obligations, comme le chapitre jumeau des obligations d'entretien classé en 1. |
| `sinistres.gerer.les-contentieux-d-assurance` | 4 | 3 | licence pro/master | La compétence demande de reconnaître un contentieux et ses arguments, pas d'argumenter ni de situer une controverse. |
| `pathologie.structure.fondations-et-tassements` | 1 | 2 | RNCP | Expliquer un tassement et ses signes est une explication de mécanisme, marqueur du niveau 2. |
| `equipements.ventilation.le-caisson-et-les-courroies` | 1 | 2 | RNCP | La compétence dit explicitement expliquer pourquoi une courroie se détend, formulation du niveau 2. |
| `equipements.electricite.eclairage-des-communs` | 1 | 2 | RNCP | Choisir un éclairage et réduire la consommation est l'application d'une règle à un cas, au-delà du simple vocabulaire. |
| `sinistres.autres-sinistres.incendie` | 1 | 2 | RNCP | Dérouler les premières mesures après un incendie est l'application d'une procédure à un cas, pas une définition. |
| `sinistres.autres-sinistres.tempete-et-grele` | 1 | 2 | RNCP | Déclarer et faire les mesures conservatoires suppose d'appliquer des règles de délai à une situation réelle. |
| `sinistres.autres-sinistres.vol-et-vandalisme` | 1 | 2 | RNCP | Traiter un vol dans les communs est le traitement d'un cas simple, niveau 2 et non vocabulaire. |
| `travaux.du-besoin-au-devis.le-cahier-des-charges` | 1 | 2 | RNCP | Écrire un cahier des charges court demande d'appliquer une trame à un besoin, ce qui dépasse le niveau des repères. |
| `travaux.chantier.reunions-et-comptes-rendus` | 1 | 2 | RNCP | Tenir une réunion et son compte rendu est une pratique appliquée et non la seule reconnaissance du vocabulaire. |
| `energie.physique.deperditions-et-isolation` | 1 | 2 | RNCP | Expliquer où un immeuble perd sa chaleur et comment on l'isole est une explication de mécanisme physique. |
| `energie.physique.ponts-thermiques-et-inertie` | 1 | 2 | RNCP | Expliquer un pont thermique et l'inertie porte le verbe expliquer, propre au niveau 2. |
| `immobilier.propriete.l-indivision` | 1 | 2 | BTS PI | Expliquer l'indivision et dire qui vote en assemblée combine explication et application à un cas. |
| `immobilier.fiscalite.taxe-fonciere-et-enlevement-des-ordures` | 1 | 2 | BTS PI | Expliquer la taxe foncière, la TEOM et qui les paie est une explication avec répartition, pas une définition. |

## Conflits de prérequis signalés (lot A)

- droit.travaux.le-diagnostic-technique-global porte un verbe de niveau 1 (dire quand il est obligatoire et ce qu'il contient) mais son prerequis droit.travaux.travaux-votes-et-travaux-urgents passe a 2 ; il a donc ete laisse a 2 pour ne pas creer de conflit.
- comptabilite.annexes.l-annexe-3-par-cle-de-repartition porte un verbe de lecture simple mais depend de comptabilite.annexes.l-annexe-2-le-compte-de-gestion-general reclasse en 2 ; laisse a 2 pour la meme raison.
- procedure.recouvrement.l-injonction-de-payer dependait de comptabilite.impayes.relance-et-mise-en-demeure : les deux ayant ete montes a 2 ensemble, le conflit est evite ; ne monter qu'un seul des deux le recreerait.
- cabinet.negocier.avec-un-prestataire (niveau 1 d'origine) est plus exigeant que cabinet.negocier.methode-et-alternatives (niveau 2) qui le suit : la sequence de la branche negocier merite d'etre reordonnee.
- Plusieurs prerequis pointent vers des chapitres absents du lot (sinistres, equipements, pathologie, energie, travaux, immobilier) : leur niveau n'a pas pu etre verifie, notamment pour les huit cas transverses de cabinet.

Après régénération, aucun conflit ne subsiste : le générateur dérive les prérequis du niveau.

## Remarques des relecteurs

- Lot A : Le niveau 1 est globalement surcharge : une vingtaine de chapitres y portent des verbes d'application (verifier, calculer, rediger, convoquer, appliquer) qui appartiennent au niveau 2 de la grille.
- Lot A : Le domaine culture est le seul nettement surclasse : les chapitres de lecture demandent de restituer une these, ce qui ne rencontre aucun des verbes praticiens du niveau 3.
- Lot A : Les deux chapitres d'histoire de culture (histoire-du-logement, histoire-de-la-copropriete) sont ambigus entre 2 et 4 : le verbe situer appartient au niveau 1 mais la matiere historique est ancree au niveau 4 ; laisses en l'etat faute de tranche claire.
- Lot A : Le droit et la procedure sont bien calibres au-dessus du niveau 2 : les niveaux 3 diagnostiquent ou rediger, les niveaux 4 commentent des arrets, la progression tient.
- Lot A : Les treize chapitres cabinet de niveau 3, notamment les cas transverses, sont correctement places : ils combinent plusieurs branches et demandent une decision, ce qui est le coeur du niveau praticien.
- Lot B : La calibration est globalement juste : 16 chapitres sur 206 sont déplacés, et toujours d'un seul cran.
- Lot B : Le défaut dominant est le classement en niveau 1 de compétences qui portent le verbe expliquer ou une application à un cas, surtout en énergie et en sinistres.
- Lot B : Le verbe distinguer est employé indifféremment au niveau 1 et au niveau 2 dans tout le corpus ; il faudrait trancher une convention, sinon une vingtaine de chapitres restent discutables.
- Lot B : Les niveaux 4 et 5 sont rares et bien tenus, sauf les contentieux d'assurance dont la compétence est restée au verbe reconnaître.
- Lot B : Aucun conflit de prérequis après reclassement : les chaînes de chaque section restent croissantes.

## À trancher par JB

- `droit.majorites.l-article-24` : le relecteur le monte en 2, mais le chapitre témoin `chapitres/droit/majorites/l-article-24.json` est écrit au niveau 1 et le cahier interdit d'y toucher ; laissé à 1, à monter avec le chapitre si JB suit le relecteur.
- La convention du verbe « distinguer » (niveau 1 ou 2), employé dans les deux sens sur une vingtaine de chapitres.
- Les deux chapitres d'histoire de `culture` (logement, copropriété), entre 2 et 4.
- L'ordre de la branche `cabinet.negocier` : « avec un prestataire » est plus exigeant que « méthode et alternatives » qui le suit.
- Garder ou remplacer les quinze chapitres de niveau 2 du trimestre 1.

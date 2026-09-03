# Assignation des 84 cartes v1 aux chapitres du programme

Proposition du 03/09/2026, préparée pour `ACA-CONTRAT-2` étape 2.
**Rien n'est appliqué.** Ce document est la table d'assignation soumise
à JB avant que `app/migre_banque.py` ne l'exécute.

## Pourquoi ce document existe au lieu du script

Le cahier demande « une table d'assignation écrite à la main dans
`app/migre_banque.py` (une carte, un chapitre) ». En la préparant
carte par carte, deux faits ont changé la nature du travail :

1. **Vingt et une cartes sur quatre-vingt-quatre changent de domaine.**
   Les fichiers de la banque v1 ont été écrits en août par thème de
   travail (« conformité annuelle », « recouvrement des charges »), pas
   par domaine du programme. Le fichier `droit/conformite-annuelle.json`
   à lui seul disperse huit de ses quinze cartes vers `comptabilite`,
   `energie`, `pathologie` et `cabinet`.
2. Changer le `domaine` d'une carte **change la carte-monde** : le
   remplissage des régions, l'ouverture de la suivante, la branche du
   socle que la séance protège. Une carte mal rangée ne casse aucun
   test ; elle déplace silencieusement ce que JB révise le matin.

Un agent peut proposer ce rangement. Il ne peut pas le trancher seul
sans mentir sur sa confiance. D'où les trois niveaux ci-dessous.

| Niveau | Ce que ça veut dire | Combien |
|---|---|---|
| **sûr** | le chapitre existe et dit exactement le sujet de la carte | 56 |
| **à confirmer** | un chapitre plausible, mais un autre se défend | 24 |
| **à trancher** | la carte couvre plusieurs chapitres, ou aucun ne la porte | 4 |

**→** marque un changement de domaine.

## Trois trous du programme que l'assignation a révélés

Ils ne se comblent pas ici (`ACA-CONTENT-MAP-1` et `ACA-CONTENT-2`),
mais ils se nomment maintenant :

1. **La notification n'a pas de chapitre.** Cinq cartes de
   `droit/veille-recente` portent sur le décret du 22/12/2025
   (notification électronique de principe, prestataire qualifié,
   mention de la voie postale, point de départ des délais, pièces sur
   l'espace en ligne). Le programme ne connaît que
   `droit.assemblee.la-convocation-forme-et-delai`, qui est plus
   étroit. Un chapitre `droit.assemblee.la-notification` manque.
2. **La déchéance du terme n'a pas de chapitre.** Deux cartes de
   `procedure/recouvrement-charges` en vivent, et
   `procedure.recouvrement.choisir-la-voie` (n3) est le moins mauvais
   accueil pour des cartes de niveau 2.
3. **Le chapitre des marchés d'exploitation s'appelle « P1 à P4 »**
   (`equipements.chauffage.les-contrats-p1-a-p4`) alors que les cinq
   cartes de la banque parlent de P1 à P5, et que le fichier lui-même
   s'appelle `chauffage-collectif-p1-p5.json`. À renommer, ou à
   justifier.

---

## comptabilite/annexes-et-anomalies (11 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `cinq-annexes` | `comptabilite.annexes.l-annexe-1-l-etat-financier` | **à trancher** : la carte survole les cinq annexes, donc toute la branche |
| `ou-lire-ecart-budget` | `comptabilite.annexes.l-annexe-2-le-compte-de-gestion-general` | sûr |
| `libelle-14-2-annexe-4` | `comptabilite.annexes.les-annexes-4-et-5-les-travaux` | sûr |
| `recoupement-des-soldes` | `comptabilite.annexes.les-trois-chiffres-a-regarder-d-abord` | à confirmer : ou `controle.l-audit-d-un-arrete-des-comptes`, mais il est n3 et la carte est n1 |
| `seuils-ecart-budgetaire` | `comptabilite.controle.les-anomalies-classiques` | à confirmer |
| `fonds-travaux-double-plancher` | `comptabilite.budget.le-fonds-de-travaux` | sûr |
| `compte-separe-et-rapprochement` | `comptabilite.controle.l-audit-d-un-arrete-des-comptes` | à confirmer : le compte séparé lui-même est l'art. 18, donc `droit.organes.le-syndic-et-ses-missions` |
| `honoraires-mutation-recouvrement` | `comptabilite.honoraires.les-prestations-particulieres` | à confirmer |
| `solde-travaux-clotures` | `comptabilite.annexes.les-annexes-4-et-5-les-travaux` | à confirmer : ou `budget.les-travaux-hors-budget` |
| `rattachement-des-charges` | `comptabilite.bases.engagement-et-tresorerie` | sûr |
| `cle-charges-utilite-objective` | **→** `droit.charges.les-cles-de-repartition` | sûr |

## droit/conformite-annuelle (15 cartes, dont 8 changent de domaine)

Ce fichier est un radar de conformité, pas un chapitre. Il se dissout.

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `statut-non-verifie` | **→** `cabinet.cycle-annuel.les-obligations-annuelles` | à confirmer : c'est une carte de méthode du radar, pas de droit |
| `budget-deux-echeances` | **→** `comptabilite.budget.le-budget-previsionnel` | sûr |
| `budget-vote-tardif` | **→** `comptabilite.budget.le-budget-previsionnel` | sûr |
| `provisions-trimestrielles` | **→** `comptabilite.budget.les-appels-de-fonds` | sûr |
| `fonds-travaux-plancher` | **→** `comptabilite.budget.le-fonds-de-travaux` | sûr |
| `fonds-travaux-dispenses` | **→** `comptabilite.budget.le-fonds-de-travaux` | sûr |
| `mandat-syndic-duree` | `droit.organes.designation-contrat-fin-de-mandat` | sûr |
| `registre-declaration-annuelle` | `droit.statut.fiche-synthetique-et-immatriculation` | sûr |
| `assurance-rc-syndicat` | `droit.responsabilites.l-assurance-obligatoire` | sûr |
| `dpe-collectif-champ` | **→** `energie.dpe.le-dpe-collectif-et-son-calendrier` | sûr |
| `dta-parties-communes` | **→** `pathologie.diagnostics.amiante-et-dossier-technique-amiante` | sûr |
| `plan-pluriannuel-quinze-ans` | `droit.travaux.le-plan-pluriannuel-et-le-fonds-de-travaux` | sûr |
| `calendrier-des-vagues` | **→** `cabinet.cycle-annuel.les-obligations-annuelles` | **à trancher** : la carte tient trois calendriers à la fois (fonds de travaux, PPT, DPE collectif) |
| `petite-copropriete-seuil` | `droit.statut.qu-est-ce-qu-une-copropriete` | à confirmer : ou `comptabilite.bases.pourquoi-une-copropriete-n-a-pas-de-bilan` |
| `comptes-engagement` | **→** `comptabilite.bases.engagement-et-tresorerie` | sûr |

## droit/majorites (3 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `article-24` | `droit.majorites.l-article-24` | sûr |
| `article-25` | `droit.majorites.l-article-25-et-la-passerelle` | sûr |
| `passerelle-25-1` | `droit.majorites.l-article-25-et-la-passerelle` | sûr |

## droit/veille-recente (10 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `notification-electronique-principe` | `droit.assemblee.la-convocation-forme-et-delai` | à confirmer : voir le trou n° 1 |
| `lre-prestataire-qualifie` | `droit.assemblee.la-convocation-forme-et-delai` | à confirmer : trou n° 1 |
| `mention-voie-postale` | `droit.assemblee.la-convocation-forme-et-delai` | à confirmer : trou n° 1 |
| `point-depart-des-delais` | `droit.assemblee.la-convocation-forme-et-delai` | à confirmer : trou n° 1 |
| `pieces-espace-en-ligne` | `droit.assemblee.les-pieces-jointes-obligatoires` | à confirmer : ou `cabinet.donnees.l-espace-client-en-ligne` |
| `recouvrement-une-mise-en-demeure-par-exercice` | **→** `procedure.recouvrement.l-assignation` | à confirmer |
| `recouvrement-ventilation-mise-en-demeure` | **→** `procedure.avant-le-proces.mise-en-demeure-recommande-sommation` | sûr |
| `quitus-portee` | **→** `comptabilite.controle.approbation-et-quitus` | sûr |
| `meuble-tourisme-condition-ouverture` | `droit.mutations.changement-d-usage-et-location` | sûr |
| `isolation-individuelle-toiture-plancher` | `droit.travaux.travaux-privatifs-affectant-les-communes` | sûr |

## equipements/ascenseur (3 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `organes-securite` | `equipements.ascenseurs.les-organes-d-un-ascenseur` | sûr |
| `controle-quinquennal` | `equipements.ascenseurs.le-controle-technique-quinquennal` | sûr |
| `entretien-obligatoire` | `equipements.ascenseurs.le-contrat-de-maintenance` | sûr |

## equipements/chauffage-collectif-p1-p5 (5 cartes)

Les cinq vont au même chapitre. Voir le trou n° 3 sur son nom.

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `poste-p1` | `equipements.chauffage.les-contrats-p1-a-p4` | sûr |
| `p2-contre-p3` | `equipements.chauffage.les-contrats-p1-a-p4` | sûr |
| `p4-amortissement` | `equipements.chauffage.les-contrats-p1-a-p4` | sûr |
| `role-defense-p3` | `equipements.chauffage.les-contrats-p1-a-p4` | sûr |
| `libre-expliquer-p3-au-cs` | `equipements.chauffage.les-contrats-p1-a-p4` | sûr |

## equipements/vmc-collective (5 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `composants-caisson` | `equipements.ventilation.le-caisson-et-les-courroies` | sûr |
| `caisson-legende` | `equipements.ventilation.le-caisson-et-les-courroies` | sûr |
| `composants-roles` | `equipements.ventilation.le-caisson-et-les-courroies` | sûr |
| `courroie-detente` | `equipements.ventilation.le-caisson-et-les-courroies` | sûr |
| `gaz-securite-collective` | `equipements.ventilation.entretien-et-debits-reglementaires` | à confirmer : la VMC-gaz est un régime de sécurité à part, elle mériterait son chapitre |

## pathologie/fissures-et-humidite (10 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `fissures-retrait-differentiel` | `pathologie.structure.microfissure-fissure-lezarde` | à confirmer : ou `materiaux.beton-ciment-mortier`, puisque le mécanisme est celui du matériau |
| `fissures-appui-plancher-horizontale` | `pathologie.structure.fissures-structurelles-et-leur-lecture` | sûr |
| `fissures-traversantes-infiltrations` | `pathologie.structure.fissures-structurelles-et-leur-lecture` | à confirmer : ou `humidite.infiltration` |
| `fissures-retrait-gonflement-argiles` | `pathologie.structure.fondations-et-tassements` | sûr |
| `humidite-remontee-capillaire-signes` | `pathologie.humidite.remontees-capillaires` | sûr |
| `humidite-trois-origines-diagnostic` | `pathologie.humidite.un-logement-humide-que-dire-au-coproprietaire` | à confirmer : le chapitre est n3, la carte est n2 |
| `humidite-condensation-points-froids` | `pathologie.humidite.condensation` | sûr |
| `humidite-enduit-impermeable-aggravant` | `pathologie.facades.enduits-et-classes-d-impermeabilite` | sûr |
| `toiture-souche-hauteur-reglementaire` | `pathologie.toitures.souches-cheminees-ventilations-primaires` | sûr |
| `toiture-souche-ou-event-de-chute` | `pathologie.toitures.souches-cheminees-ventilations-primaires` | sûr |

## procedure/recouvrement-charges (12 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `exigibilite-provision` | **→** `comptabilite.budget.les-appels-de-fonds` | à confirmer : l'exigibilité est comptable, la conséquence est procédurale |
| `mise-en-demeure-contenu` | `procedure.avant-le-proces.mise-en-demeure-recommande-sommation` | sûr |
| `mise-en-demeure-deux-effets` | `procedure.avant-le-proces.mise-en-demeure-recommande-sommation` | sûr |
| `decheance-assiette` | `procedure.recouvrement.choisir-la-voie` | **à trancher** : voir le trou n° 2 |
| `datation-decheance` | `procedure.recouvrement.choisir-la-voie` | **à trancher** : trou n° 2 |
| `plan-deux-voies` | `procedure.recouvrement.choisir-la-voie` | sûr |
| `frais-relance-simple` | **→** `comptabilite.impayes.les-frais-imputables` | sûr |
| `article-700` | **→** `comptabilite.impayes.les-frais-imputables` | à confirmer : l'article 700 est procédural, les frais imputables sont comptables |
| `autorisation-assemblee` | `procedure.contentieux-ag.l-autorisation-d-agir-en-justice` | sûr |
| `commissaire-de-justice` | `procedure.acteurs.le-commissaire-de-justice` | sûr |
| `libre-frais-au-conseil` | **→** `comptabilite.impayes.les-frais-imputables` | à confirmer |
| `role-debiteur-au-telephone` | **→** `cabinet.cas-transverses.un-impaye-de-dix-huit-mois` | à confirmer : c'est un jeu de rôle de relation, pas de procédure |

## sinistres/sinistres (10 cartes)

| Carte | Chapitre proposé | Niveau |
|---|---|---|
| `delai-degat-des-eaux` | `sinistres.contrat.les-delais-de-declaration` | sûr |
| `delai-vol-vandalisme` | `sinistres.contrat.les-delais-de-declaration` | sûr : ou `autres-sinistres.vol-et-vandalisme`, mais les trois cartes de délai gagnent à rester ensemble |
| `delai-catastrophe-naturelle` | `sinistres.contrat.les-delais-de-declaration` | sûr : même raison |
| `decheance-de-garantie` | `sinistres.contrat.garantie-et-exclusion` | sûr |
| `irsi-tranches` | `sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches` | sûr |
| `irsi-assureur-gestionnaire` | `sinistres.degat-des-eaux.l-assureur-gestionnaire` | sûr |
| `recherche-de-fuite` | `sinistres.degat-des-eaux.la-recherche-de-fuite` | sûr |
| `cidre-abrogee` | `sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches` | sûr |
| `priorite-par-gravite` | `sinistres.autres-sinistres.les-mesures-conservatoires` | à confirmer : c'est de la méthode, donc peut-être `cabinet.charge.gerer-son-temps-et-deleguer` |
| `mesures-conservatoires-sans-ag` | `sinistres.autres-sinistres.les-mesures-conservatoires` | sûr |

---

## Ce que JB a à décider

Trois questions, dans l'ordre d'impact :

1. **Accepte-t-on les vingt et un changements de domaine ?** C'est le
   vrai sujet. Ils sont justes sur le fond (une carte sur le budget
   prévisionnel appartient à la comptabilité), mais ils vident
   `droit` de sept cartes et remplissent `comptabilite`. La
   carte-monde du lendemain n'a plus la même forme.
2. **Les quatre « à trancher »** : les deux cartes de survol
   (`cinq-annexes`, `calendrier-des-vagues`) et les deux de déchéance
   du terme. Soit on force un chapitre, soit on crée le chapitre qui
   manque, soit elles attendent `ACA-CONTENT-2`.
3. **Les trois trous du programme** nommés en haut : la notification,
   la déchéance du terme, et le nom du chapitre des marchés
   d'exploitation.

Une fois ces trois réponses données, la table se recopie telle quelle
dans `app/migre_banque.py` et le reste de `ACA-CONTRAT-2` est
mécanique : écriture des fichiers de chapitre, valideur v2 sur le
résultat, `genere.py` qui lit `chapitres/`, archivage de `banque/`.

# Tri des recommandations, 04/09/2026

Origines et repères de lignes dans [index.json](index.json). `IFSI §n`
désigne la critique après le syllabus copié ; `A §n` et `B §n` les deux
variantes copro. Les lots ci-dessous sont définis dans [PLAN.md](PLAN.md).

**Après le lot L2 :** les constats copro ci-dessous décrivent le tri
initial. Leur traitement et les limites actuelles sont dans le
[point de reprise copro](../2026-09-04-revision-copro.md) et dans
[la table avant/après](copro-corrections.json). Les anciens compteurs
et formulations cités ici servent de traces ; ils ne décrivent plus
le programme corrigé.

## Lecture commune

| Proposition des rapports | Traitement retenu pour le plan | Lot |
|---|---|---|
| Garder la largeur du corpus, améliorer la progression (IFSI §23 ; A §17 ; B §28) | Conserver les identifiants ; organiser des entrées lisibles et des approfondissements. Aucune réduction massive par quota. | L1, L4 |
| Séparer étape, difficulté, criticité et preuve (IFSI §4-5 ; A §6 ; B §5-7) | Décrire ces axes une seule fois ; adapter les parcours au métier. Les niveaux actuels restent compatibles pendant la transition. | L3 |
| Transformer l'arbre en graphe (IFSI §3 ; A §8 ; B §8) | Les prérequis et ponts existent déjà. Ajouter seulement les relations utiles et sourçables ; pas de graphe reconstruit pour son nom. | L3, L4 |
| Objectifs fins, expertise locale (IFSI §11 ; B §12) | Une capacité observable et une preuve adaptée. Ne pas fabriquer un objectif par mot-clé pour gonfler un compteur. | L1, L4 |
| Cas, production, raisonnement, calculs (IFSI §14-16 ; A §9-10 ; B §18-20) | Éprouver un dossier fictif complet, avec réponses attendues, variantes et retour après erreur. Garder FSRS pour ce qu'il mesure. | L5 |
| Provenance par affirmation (IFSI §19 ; A §14 ; B §23) | Relier assertion, source, version, période et contexte ; distinguer loi, contrat, convention, norme et choix pédagogique. | L2, L3 |
| Erreur critique non compensable (IFSI §14 ; B §21) | Remédiation puis nouvel essai sur l'objectif concerné ; aucune attestation d'aptitude délivrée par un score global. | L3, L5 |
| Mesurer rétention, transfert et confiance (IFSI §21 ; A §15 ; B §25) | Données privées issues d'usages réels. Aucun taux fictif ni tableau d'évaluation pour un manager. | L5 |
| Spécialités, contextes, recherche (IFSI §18 ; A §3,8 ; B §11,14) | Branches et parcours extensibles après l'entrée dans le métier. Expertise locale et besoin de mise à jour restent visibles. | L4, L6 |

## À nuancer ou à écarter

| Formulation des rapports | Constat et conséquence |
|---|---|
| « L'arbre doit être fini », infini seulement dans les situations (IFSI §13 ; B §22) | JB a demandé une progression sans plafond. Garder des versions finies et des cas variés, mais aussi la possibilité de nouveaux objectifs, sujets et branches. |
| Un socle copro de 333 chapitres serait un préalable obligatoire | `app/seance.py` pondère les nouveautés vers les branches du socle. Il ne verrouille pas toutes les autres branches ; le choix d'un domaine reste possible. Améliorer la priorité et la lisibilité, sans prétendre supprimer un verrou existant. |
| Le volume du socle contredirait à lui seul les trois premiers mois | `PROGRAMME.md` distingue déjà les premières semaines et un socle sur une durée beaucoup plus longue. Un noyau de départ reste utile ; ce n'est pas une preuve que tout devait être appris en un trimestre. |
| 309 h 30 d'étude pour le socle copro | La somme courante des `etude_minutes` donne 18 645 minutes, soit 310 h 45. Le calcul par durée uniforme de niveau diffère des données de 75 minutes. Dans les deux cas, c'est une estimation éditoriale, pas une durée mesurée chez un joueur. |
| Quotas d'objectifs, de chapitres, de formats et réussite standard | Propositions de design à tester ; aucune preuve fournie pour imposer ces nombres comme cibles scientifiques. |
| Passeport de sécurité qui déverrouille la suite | Conserver le travail sur les erreurs critiques sans verrouiller l'arbre ni délivrer une autorisation professionnelle. |
| Supervision ou validation humaine des résultats | Adapter la relecture au contenu. Ne pas transformer le carnet privé du joueur en dossier d'évaluation de salariés ou d'étudiants (`DOCTRINE.md` §2). |
| Relecture par modèle présentée comme suffisante | Une passe automatique ne prouve pas la validité clinique ou professionnelle. Garder les limites explicites, les sources et le statut réel. |

Les variantes copro divergent sur la durée initiale (A : treize semaines ;
B : diagnostic puis douze), sur les paliers et sur la hiérarchie des
sources (A : A-D ; B : A-H). Ne pas transposer leurs lettres dans notre
fiabilité A/B/C : nature, autorité et confiance sont des axes distincts.
Le plan prend B pour organiser les missions, en conservant les apports
complémentaires de A ; cela ne donne pas priorité à ses affirmations
juridiques.

## IFSI : tri initial et résultat de la finition

Le [point détaillé](../2026-09-04-revision-ifsi.md) porte les sources
primaires et les preuves. Le chantier `ACA-IFSI-1` est désormais terminé
localement : 375 chapitres, 600 capacités de cadrage, rendu et catalogue
alignés, contrôles verts. La liste ci-dessous conserve les points de
vigilance du tri initial ; les objectifs fins et les preuves des futurs
contenus restent à travailler dans les pilotes.

Points de vigilance examinés en L1 :

- Le mapping A-E concerne les domaines d'enseignement. Les compétences
  officielles et les rattachements éditoriaux ne sont pas interchangeables.
- Parcoursup, FPC et accès spécifiques restent distincts ; un exercice
  facultatif ne devient pas une épreuve nationale par son inscription.
- Les 1 691 objectifs initiaux incluaient des déclinaisons mécaniques de
  notions. Leur retrait et le rétablissement de capacités utiles ont
  ramené l'inventaire à 600. Les notions restent présentes ; le pilote
  doit préciser les preuves avant une généralisation à copro.
- La répartition année 1/2/3 demande une revue argumentée. Les gestes
  supervisés, les stages et la certification clinique restent séparés
  des apprentissages numériques.
- Corriger le contrat `legacy` des ajouts, puis le rendu et le catalogue.
  Un générateur et un fichier JSON présents ne constituent pas une
  intégration terminée.

## Copro : vérifications ciblées déjà obtenues

Ce repérage porte sur le dépôt local, pas sur le comportement du site
publié. Les contrôles juridiques ci-dessous ont été effectués le
04/09/2026 ; ils ne valent pas vérification de tout le rapport.

| Sujet | Preuve primaire et constat local | Suite |
|---|---|---|
| Article 24 et abstentions (A §2.1 ; B §3) | [Article 24 courant](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000051749514/) : les voix exprimées fondent le calcul. La compétence de `programme/copro.json` et du générateur dit « abstentions comprises ». La carte v1 `droit-majorites-article-24`, présente dans `site/banque.json`, exclut correctement les abstentions. Le chapitre v2 est encore brouillon et son objectif est ambigu. | Corriger l'objectif et contrôler le brouillon entier. Ne pas déclarer toute la banque erronée. La chronologie « depuis 2020 » et les exemples de décisions du brouillon demandent aussi vérification. |
| Pouvoirs (A §2.2 ; B §3) | [Article 22](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039313531/2026-07-19) : la dérogation ordinaire au maximum de trois délégations utilise 10 % pour le total des voix propres et déléguées, avec d'autres conditions et exceptions dans le texte. Le programme conserve « cinq pour cent ». | Réécrire avec le champ d'application ; éviter une règle universelle réduite à un seul pourcentage. |
| Paramètre DPE futur (A §2.18) | L'[arrêté du 19 août 2026](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054747079) prévoit le passage de 1,9 à 1,7 au 1er janvier 2027. Le signalement du rapport est fondé ; cela ne rend pas 1,7 applicable dès septembre 2026. | Tester séparément période courante et période future ; identifier les assertions réellement concernées avant modification. |

Les comptages du rapport sont largement retrouvés : 389 chapitres, 333
au socle, 2 990 cartes cibles dont 2 486 au socle. Détail et empreintes
dans [etat-programmes.json](etat-programmes.json). Le catalogue annonce
encore 387 chapitres copro ; le texte général `PROGRAMME.md` contient
encore le précédent décompte de 315. La banque jouable doit être comptée
séparément : une cible de cartes n'est jamais un inventaire servi.

## Copro : file de vérification avant réécriture

Les lignes suivantes sont des **signalements des rapports**, pas des
règles que ce classement certifie. Pour chacune : source primaire,
version applicable, contexte, assertion du programme, carte éventuelle,
verdict et modification traçable. Sources repérées dans les rapports à
retrouver à l'original ; ne pas recopier une citation devenue introuvable.

| Lot documentaire | Sujets à instruire | Où commencer |
|---|---|---|
| AG et décisions | Notification électronique et choix postal, passerelles 25-1/26-1, pouvoirs, contenu du PV | A §2 ; B §3 et §14 ; `droit.assemblee`, `droit.majorites` |
| Financement | Fonds travaux et PPT adopté, emprunt collectif, trésorerie, hypothèque légale et terminologie ancienne | A §2,3 ; B §3,14 ; `comptabilite`, `travaux`, `procedure` |
| Assurances et contentieux | Délais de déclaration selon contrat et sinistre, IRSI et son champ, assurance RC/MRI, représentation par avocat | A §2 ; B §3,14 ; `sinistres`, `procedure` |
| Diagnostic et bâtiment | Ravalement et territoire, plomb/amiante et dates, NF C 15-100 et travaux, incendie selon bâtiment, inspection de toiture | A §2,5 ; B §3,13,14 ; `pathologie`, `equipements`, `travaux` |
| Exercice professionnel | Périmètre LCB-FT du syndic et autres activités du cabinet, carte professionnelle et habilitations, pré-état daté | A §2 ; B §3,14 ; `cabinet`, `immobilier` |
| Calendriers et régimes | Gaz/électricité et tarifs, DPE, facturation électronique selon assujettissement, petites copropriétés et syndicats à deux copropriétaires, meublés touristiques | A §2,3 ; B §3,14 ; `energie`, `droit`, `comptabilite`, `immobilier` |

Appliquer d'abord les corrections aux assertions existantes, puis au
contenu réellement touché. `programme/genere_copro.py` porte encore les
données et réécrit `copro.json` : une correction du seul JSON serait
perdue à la prochaine génération. Résoudre cette asymétrie explicitement.

## Couverture métier à développer après les corrections

Les deux variantes copro convergent sur les missions et les trois
temporalités : quotidien, cycle annuel, projets pluriannuels. Les
lacunes proposées à examiner sont le personnel du syndicat (distinct
de l'équipe du cabinet), VEFA et réception, adaptation climatique,
petites copropriétés, fraude bancaire, classement des pièces, ensembles
complexes et copropriétés en difficulté. Chaque ajout devra avoir un
objectif et une situation d'usage ; sa seule présence dans une liste
du rapport ne justifie pas un chapitre supplémentaire.

Pilotes retenus pour éprouver le plan : **AG complète**, puis **dégât
des eaux** ; côté IFSI, **diabète et continuité du parcours de soins**.
Les deux métiers doivent partager les mécanismes, chacun avec ses
données, ses sources et ses limites professionnelles.

# PROGRAMME, le gestionnaire de copropriété

Écrit le 02/09/2026 sur le brief de JB (« il faut réfléchir à ce qu'on
met dans le programme, ce qu'on ne met pas, c'est quoi le socle, c'est
quoi le périphérique, c'est quoi la suite logique »). C'est le
**référentiel de l'arbre** du métier : domaines, branches, chapitres,
niveaux, socle, sources primaires, trous nommés. La version en données
est [`programme/copro.json`](programme/copro.json) ; quand les deux
divergent, le JSON fait foi et ce texte se corrige.

Qui l'a écrit : **le modèle**, à partir du brief de JB, de sa
connaissance du métier et des ancres publiques (§5), sans manuel de
référence, parce qu'il n'en existe pas pour ce métier. C'est le régime
voulu ([`decisions/0022`](decisions/0022-le-modele-pose-le-cadre-les-sources-corroborent-l-audit-mesure.md)) :
le modèle pose le cadre, les sources ont le dernier mot sur chaque fait
des chapitres, l'humain a le dernier mot sur le cadre, la mesure sur la
pédagogie. Un agent frais calibrera ce programme (chantier
`ACA-PROGRAMME-1`) ; JB le relit et déplace ce qu'il veut.

Ce que ce document n'est pas : un cours. Il nomme ce qu'on enseigne, pas
ce qu'on dit. Un chiffre, une date ou un article cité ici sert de
repère pour l'auteur du chapitre, qui le revérifie à la source avant
d'écrire une carte ; les mentions `[À VÉRIFIER]` signalent un repère
non relu le 02/09.

---

## 1. Le métier en une page

Un gestionnaire de copropriété administre des immeubles pour le compte
de leurs copropriétaires réunis en syndicat. Son année tourne autour de
l'**assemblée générale** : arrêter les comptes, préparer le conseil
syndical, convoquer, tenir la séance, notifier le procès-verbal,
exécuter les décisions. Entre deux assemblées, il **entretient un
bâtiment** (visites, contrats, sinistres, travaux), **tient une
comptabilité** particulière (budget, appels, fonds de travaux, impayés),
**applique un droit** dense (la loi de 1965 et son décret, le Code
civil, le Code de la construction, l'urbanisme, les assurances), et
**parle à tout le monde** : copropriétaires, conseil syndical,
entreprises, avocats, experts, mairie.

Ce qu'on attend de lui : un couteau suisse. Assez de bâtiment pour ne pas
se faire raconter n'importe quoi sur une terrasse, assez de droit pour
ne pas faire voter une résolution nulle, assez de comptabilité pour lire
une annexe, assez de procédure pour savoir quand on va au juge et avec
qui, assez d'assurance pour gérer un dégât des eaux sans y laisser un
mois. Le socle (§3) est ce couteau suisse ; les spécialisations (§4)
sont les lames qu'on aiguise ensuite.

Le premier joueur a nommé ses manques : sur une terrasse, ne pas savoir
si une souche est une ancienne cheminée ou une ventilation primaire ;
confondre crédit et produit ; ne pas savoir ce qu'est un référé. Ce
programme commence là.

## 2. Les domaines

Dix domaines dans l'arbre, un hors arbre. Les clés sont celles que
`academie.json` portera après le chantier `ACA-PROGRAMME-1` (au 02/09 il
porte encore `plans`, et ni `immobilier` ni `cabinet`) : trois changements
par rapport au 30/08, `plans` devient `travaux`, `immobilier` et `cabinet`
s'ajoutent ; `pathologie` garde sa clé et change de titre ; l'ordre des
domaines change aussi (le droit passe premier). L'ordre est le chemin recommandé, pas
un verrou.

| Ordre | Clé | Titre proposé | Pourquoi ce domaine | Sources primaires |
|---|---|---|---|---|
| 1 | `droit` | Droit de la copropriété | la grammaire du métier : sans elle rien ne se vote ni ne s'exécute | loi 65-557, décret 67-223, Légifrance, Judilibre, ANIL |
| 2 | `pathologie` | Bâtiment et pathologie | le manque le plus coûteux sur le terrain ; le plus visuel | fiches pathologie AQC, Cerema, DTU (via AFNOR, payant), ANAH |
| 3 | `equipements` | Technique des équipements | les « vrais mots » : VMC, ascenseur, chaufferie, colonnes | textes réglementaires (arrêtés ventilation, ascenseurs), RSD, ADEME, notices (éditeur, à recouper) |
| 4 | `comptabilite` | Comptabilité et finances de copropriété | débit, crédit, budget, annexes, impayés, factures | décret 2005-240, arrêté du 14/03/2005, loi 65 art. 14-1 à 14-3, ANIL |
| 5 | `sinistres` | Sinistres et assurances | le quotidien : dégât des eaux, IRSI, DO, expertise | Code des assurances, convention IRSI (organisation-pro, à recouper), Code civil 1792 |
| 6 | `procedure` | Procédure et justice | référé, tribunal judiciaire, avocat, commissaire de justice, injonction de payer, pénal | Code de procédure civile, COJ, loi 65 art. 19 à 19-2 et 42, décret 67 art. 55 |
| 7 | `travaux` | Travaux, marchés et lecture de plans | devis, facture, marché privé, MOE, réception, plans, DP | Code civil 1792 et s., NF P 03-001 (payant), CCH, Code de l'urbanisme, AQC |
| 8 | `energie` | Énergie et rénovation | DPE, audit, PPT, aides, chauffage, IRVE | ADEME, ecologie.gouv.fr, décrets DPE 2021, loi Climat et résilience, ANAH, CRE |
| 9 | `immobilier` | Propriété, immobilier et urbanisme | propriété, servitudes, vente d'un lot, location, PLU, acteurs | Code civil, Code de l'urbanisme, loi 89-462, loi Hoguet, notaires (doctrine) |
| 10 | `cabinet` | Le cabinet : déontologie, contrats, relation | carte pro, contrat de syndic, cycle annuel, conseil syndical, AG en pratique, écrire, négocier, RGPD | loi Hoguet, décret 2015-1090 (déontologie), décret 2015-342 (contrat type), CNIL, doctrine de négociation |
| hors arbre | `culture` | Culture | le texte du bac : la propriété, l'habiter, la ville, l'histoire du logement | textes publics choisis, presse de fond, histoire |

## 3. Le socle commun

Le socle est ce que tout gestionnaire doit tenir et entretenir. Il se
valide par l'épreuve du gestionnaire (`BLUEPRINT.md` §8).

| Domaine | Niveau socle | Ce que ça veut dire |
|---|---|---|
| droit | **3** | diagnostiquer une convocation, choisir une majorité, répondre à un copropriétaire sur ses droits |
| comptabilite | **3** | lire les cinq annexes, expliquer un appel de fonds, repérer une anomalie |
| cabinet | **3** (le domaine entier ; l'assemblée et le cycle annuel en sont le cœur) | tenir une AG, dérouler l'année sans oublier une obligation, écrire, négocier |
| pathologie | 2 | nommer et expliquer un désordre courant, savoir quand appeler qui |
| equipements | 2 | nommer les organes, comprendre un contrat d'entretien, lire un compte rendu d'intervention |
| sinistres | 2 | dérouler un dégât des eaux sous IRSI, savoir ce qu'une MRI couvre |
| procedure | 2 | savoir qui juge quoi, ce qu'est un référé, comment on recouvre une charge |
| travaux | 2 | lire un devis et une facture, connaître la chaîne d'un chantier, une DP |
| energie | 2 | expliquer un DPE, connaître le calendrier et les obligations |
| immobilier | 2 | expliquer une vente en copro, une servitude, un PLU |

Ordre de grandeur (`programme/copro.json`, 02/09/2026) : le programme
compte **371 chapitres** (146 de niveau 1, 145 de niveau 2, 59 de
niveau 3, 19 de niveau 4, 2 de niveau 5) pour environ **2 800 cartes**
cibles ; le socle en représente **315 chapitres** et environ **2 300
cartes**. À quatre séances par semaine avec trois cartes neuves
chacune, plus une étude par semaine, un joueur parti de zéro tient le
socle en deux ans environ ; le quiz de positionnement et les journées
raccourcissent ce temps. Un gestionnaire en poste depuis un an y entre
à un tiers déjà stabilisé. Ces chiffres sont des cibles de rédaction,
pas des promesses : le calibrage (§5) et la mesure les corrigeront.

## 4. Les spécialisations

Après le socle, quatre chemins types, jamais imposés ; l'arbre se
spécialise là où le joueur va :

| Chemin | Domaines poussés au niveau 4-5 | Titre visé |
|---|---|---|
| **Technique** | pathologie, equipements, travaux, energie | Expert bâtiment (le cap nommé par JB à 3-5 ans) |
| **Juridique** | droit, procedure, immobilier | Expert contentieux |
| **Financier** | comptabilite, cabinet (économie du syndic), energie (financement) | Expert finances de copropriété |
| **Relation et direction** | cabinet, droit (AG), culture | Expert assemblée, futur responsable de service |

## 5. L'échelle des niveaux, ancrée

([`decisions/0003`](decisions/0003-cinq-niveaux-et-la-synthese.md))
Le niveau d'un chapitre se décide à l'écriture, contre la grille et
contre des ancres publiques ; puis la mesure corrige.

| Niveau | Nom | Ancre publique pour la copropriété | Sources dominantes |
|---|---|---|---|
| 1 | Repères | vocabulaire du BTS Professions immobilières (référentiel officiel) `[À VÉRIFIER : édition en vigueur]` | textes officiels, fiches AQC, ANIL |
| 2 | Mécanismes | blocs de compétences du BTS PI et de la fiche RNCP du titre de gestionnaire `[À VÉRIFIER : numéro de fiche]` ; thèmes de la formation continue loi ALUR | idem, jurisprudence de principe |
| 3 | Praticien | licence professionnelle et master immobilier ; la pratique attendue d'un gestionnaire confirmé | jurisprudence, doctrine, pièces publiques |
| 4 | Doctrine | revues (AJDI, Loyers et copropriété, Informations rapides de la copropriété), rapports annuels de la Cour de cassation | doctrine signée, arrêts commentés |
| 5 | Frontière | thèses, colloques (GRIDAUH), rapports publics, recherche en pathologie et énergie | articles, rapports, contributions |

Règle de calibrage : un agent frais note chaque chapitre contre cette
grille avant validation ; après trente séances jouées sur un chapitre,
une difficulté FSRS moyenne hors de la plage de son niveau le fait
reclasser.

## 6. Les domaines, branche par branche

Pour chaque branche : les chapitres des niveaux 1 à 3 nommés, les
niveaux 4 et 5 esquissés, l'exercice dominant, les sources primaires,
les trous nommés. Les identifiants sont ceux de `programme/copro.json`.

### 6.1 Droit de la copropriété (`droit`)

**Branches et chapitres**

- **statut** : qu'est-ce qu'une copropriété (art. 1) ; lots, parties
  privatives et communes (art. 2, 3) ; parties communes spéciales et à
  jouissance privative (art. 6-2, 6-3) ; tantièmes et quotes-parts
  (art. 5) ; le règlement de copropriété et l'état descriptif de
  division ; la fiche synthétique et l'immatriculation ; N4 : histoire
  de la loi de 1965 ; N5 : la réforme permanente, controverses.
- **organes** : le syndicat (art. 14) ; le syndic, ses missions
  (art. 18) ; désignation, contrat, fin de mandat et transmission
  (art. 18-2) ; le conseil syndical (art. 21) et la délégation (21-1 à
  21-5) ; syndic bénévole et coopératif ; l'administrateur provisoire
  (29-1) et l'alerte (29-1 A) ; N4 : la gouvernance en question.
- **assemblee** : la convocation (décret art. 9, délai de 21 jours) ;
  l'ordre du jour et les inscriptions (art. 10) ; les pièces jointes
  (art. 11) ; pouvoirs et représentation (art. 22) ; tenue, bureau,
  feuille de présence ; le vote par correspondance (17-1 A) et la
  visioconférence ; le procès-verbal (décret art. 17) et sa
  notification (art. 18) ; la contestation en deux mois (art. 42) ;
  N3 : diagnostiquer une convocation irrégulière ; N4 : l'AG
  dématérialisée, doctrine.
- **majorites** : article 24 ; article 25 et la passerelle 25-1 ;
  article 26 et l'unanimité ; les cas particuliers (accessibilité,
  surélévation, travaux d'intérêt collectif sur privatif) ; N3 : le
  tableau des majorités par décision ; N4 : l'abus de majorité.
- **charges** : charges générales et spéciales (art. 10) ; les clés de
  répartition ; la régularisation ; modifier une répartition (art. 11) ;
  N3 : répondre à une contestation de charges ; N4 : jurisprudence des
  clés.
- **travaux** : travaux votés et travaux urgents (art. 18, décret 37) ;
  travaux privatifs affectant les communes (25 b) ; l'accès aux lots
  (art. 9) ; le plan pluriannuel de travaux et le fonds (14-2) ; le
  DTG ; N3 : instruire une demande de travaux.
- **mutations** : la vente d'un lot vue du syndic (art. 20, opposition,
  état daté) ; l'avis de mutation ; division et réunion de lots ;
  changement d'usage ; location et règlement de copropriété ; N3 : le
  copropriétaire défaillant.
- **responsabilites** : du syndicat (art. 14, vices et défaut
  d'entretien) ; du syndic (contractuelle et quasi-délictuelle) ; du
  copropriétaire ; l'assurance obligatoire (9-1) ; troubles anormaux de
  voisinage ; N4 : jurisprudence de responsabilité.

**Exercices dominants** : flash et QCM à pièges aux niveaux 1-2 ; cas
et lecture d'arrêt au niveau 3 ; commentaire au niveau 4.
**Sources** : Légifrance (loi et décret consolidés), Judilibre, ANIL,
Service-public.fr. **Trous nommés** : un manuel de référence libre pour
le niveau 4 (les revues sont payantes) ; les réponses ministérielles
utiles ne sont pas encore inventoriées.

### 6.2 Bâtiment et pathologie (`pathologie`)

- **materiaux** : béton, ciment, mortier, ce qui les distingue ; les
  aciers et la corrosion ; bois et pierre ; briques et enduits ;
  isolants ; comment chacun vieillit ; N3 : reconnaître un matériau sur
  photo.
- **structure** : fondations et tassements ; fissures structurelles,
  microfissure, fissure, lézarde, ce que les mots engagent ; témoins et
  suivi ; balcons et corrosion ; carbonatation ; N3 : quand appeler un
  bureau d'études ; N4 : normes et seuils, ce qui est publié et ce qui
  ne l'est pas.
- **facades** : enduits et classes d'imperméabilité ; ravalement ;
  isolation par l'extérieur et ses désordres ; décollements,
  efflorescences ; N3 : diagnostiquer une façade avant devis.
- **toitures** : toiture-terrasse et relevés ; souches, cheminées et
  ventilations primaires ; tuiles, ardoises, zinguerie ; chéneaux et
  eaux pluviales ; N3 : la visite de toiture.
- **humidite** : remontées capillaires, condensation, infiltration, les
  distinguer ; ponts thermiques et moisissures ; le lien avec la
  ventilation ; N3 : un logement humide, que dire au copropriétaire.
- **epoques** : le bâti haussmannien ; 1950-1975 (béton, amiante,
  plomb) ; 1975-1990 ; le bâti récent ; N2 : dater une façade ;
  N3 : les pathologies attendues par époque.
- **diagnostics** : amiante et DTA ; plomb ; termites ; radon ; ce qu'un
  gestionnaire doit tenir à jour.
- **visite** : comment on regarde un immeuble, dans quel ordre, ce qu'on
  photographie, ce qu'on note ; N3 : le compte rendu de visite
  technique.

**Exercices dominants** : photo, relier, datation, dessin. **Sources** :
fiches pathologie AQC (texte, jamais les images), Cerema, guides ANAH,
DTU. **Trous nommés** : les images (le verrou mesuré le 28/08 : AQC
inexploitable en image, Commons maigre) ; les seuils de fissuration
sans source publique primaire ; le guide CSTB façades indisponible.

### 6.3 Technique des équipements (`equipements`)

- **ventilation** : simple flux, double flux, hygro A et B ; le caisson,
  les courroies, pourquoi elles se détendent ; entretien et débits
  réglementaires ; N3 : lire un rapport de contrôle VMC.
- **chauffage** : chaudière gaz et fioul, condensation ; sous-station de
  réseau de chaleur ; les contrats P1 à P4 ; individualisation des
  frais ; eau chaude sanitaire et légionelles ; pompes à chaleur et
  hybrides ; N3 : la panne de janvier.
- **ascenseurs** : les organes (machinerie, cabine, opérateur de porte,
  parachute) ; le contrat de maintenance ; contrôle technique
  quinquennal ; la mise en sécurité ; N3 : l'ascenseur à l'arrêt.
- **plomberie** : colonnes EU, EV, EP ; ventilation primaire et
  secondaire ; surpresseur ; compteurs et disconnecteur ; recherche de
  fuite ; N3 : un dégât des eaux vu de la plomberie.
- **electricite** : TGBT et colonnes montantes (transfert Enedis) ;
  NF C 15-100 pour un gestionnaire ; éclairage des communs ; bornes de
  recharge ; N3 : lire un rapport électrique.
- **acces** : interphone, badges, ventouses, cellules, portails ;
  désenfumage et extincteurs ; N3 : la porte de parking en panne.
- **contrats** : les obligations d'entretien par équipement ; le
  calendrier des contrôles ; comparer deux contrats ; N3 : renégocier
  un contrat.

**Exercices dominants** : photo, relier, dessin, plan. **Sources** :
arrêtés et décrets, RSD, ADEME, guides Cerema ; les notices fabricants
sont `editeur`, à recouper. **Trous nommés** : images (idem 6.2) ; un
référentiel public des organes d'ascenseur.

### 6.4 Comptabilité et finances de copropriété (`comptabilite`)

- **bases** : débit et crédit, la partie double ; actif et passif ;
  produits et charges ; engagement et trésorerie ; l'exercice ; N2 :
  pourquoi une copro n'a pas de bilan ; N4 : histoire de la partie
  double.
- **plan-comptable** : les classes du plan comptable de la copropriété ;
  les comptes qu'on lit tous les jours (copropriétaires, fournisseurs,
  banque, provisions) ; N3 : retrouver une écriture.
- **budget** : le budget prévisionnel (14-1) ; les appels de fonds ; les
  travaux hors budget (14-2) ; le fonds de travaux et son taux ; les
  avances ; l'emprunt collectif ; N3 : construire un budget.
- **annexes** : les cinq annexes, une par une ; les trois chiffres à
  regarder d'abord ; N3 : lire une annexe pour le conseil syndical ;
  N4 : les limites du décret comptable.
- **controle** : approbation et quitus ; le rôle du conseil syndical ;
  les anomalies classiques ; N3 : l'audit d'un arrêté des comptes.
- **impayes** : la relance, la mise en demeure, les frais imputables
  (10-1) ; le lien avec la procédure ; N3 : le plan de recouvrement.
- **factures** : mentions obligatoires d'une facture et d'un devis ; la
  TVA à 20, 10 et 5,5 % et les attestations ; N3 : refuser une facture.
- **honoraires** : le contrat type et ses honoraires ; forfait et
  prestations particulières (18-1 A) ; N4 : l'économie d'un cabinet.

**Exercices dominants** : QCM, cas, feuille-blanche, lecture d'annexe.
**Sources** : décret 2005-240, arrêté du 14/03/2005, loi 65, ANIL,
Code général des impôts pour la TVA. **Trous nommés** : des annexes
publiques anonymes pour les lectures ; un jeu d'écritures fictif validé.

### 6.5 Sinistres et assurances (`sinistres`)

- **contrat** : assuré, souscripteur, prime, franchise, garantie,
  exclusion ; délais de déclaration ; l'expertise ; N2 : lire des
  conditions particulières.
- **mri** : ce que la multirisque immeuble couvre ; la responsabilité
  civile du syndicat ; le propriétaire non occupant ; l'assurance
  obligatoire du copropriétaire ; N3 : vérifier une police.
- **degat-des-eaux** : la convention IRSI, ses tranches et l'assureur
  gestionnaire ; la recherche de fuite ; les recours ; N3 : dérouler un
  dégât des eaux du 5e au 2e.
- **autres-sinistres** : incendie, tempête, catastrophe naturelle, vol
  et vandalisme ; N3 : les mesures conservatoires.
- **construction** : réception, parfait achèvement, biennale,
  décennale ; la dommages-ouvrage ; l'expertise judiciaire ; N3 : un
  désordre à deux ans.
- **expertise** : amiable, contradictoire, judiciaire ; l'expert
  d'assuré ; N3 : préparer une expertise.
- **gerer** : la méthode complète d'un sinistre, de la déclaration à
  l'indemnité ; N4 : les contentieux d'assurance.

**Exercices dominants** : cas, datation (circuit), QCM. **Sources** :
Code des assurances, Code civil, convention IRSI (organisation-pro, à
recouper avec la doctrine), Légifrance. **Trous nommés** : le texte de
la convention IRSI en version libre et datée.

### 6.6 Procédure et justice (`procedure`)

- **organisation** : tribunal judiciaire, cour d'appel, Cour de
  cassation ; juge des contentieux de la protection ; tribunal de
  commerce ; le pénal (procureur, tribunal correctionnel) ;
  l'administratif ; qui juge quoi en copropriété.
- **acteurs** : l'avocat et quand il est obligatoire ; le commissaire de
  justice ; le notaire ; l'expert judiciaire ; le médiateur ; le greffe.
- **avant-le-proces** : mise en demeure, lettre recommandée, sommation ;
  conciliation et médiation préalables ; le protocole d'accord.
- **urgence** : le référé et ses cas ; le référé expertise ; la
  provision ; la procédure accélérée au fond (19-2).
- **recouvrement** : injonction de payer ; assignation ; l'hypothèque
  légale (19) et le privilège (19-1) ; saisie-attribution ; saisie
  immobilière ; N3 : choisir la voie.
- **contentieux-ag** : la nullité d'assemblée (art. 42) ; opposant et
  défaillant ; l'autorisation d'agir (décret art. 55) ; N3 : répondre
  à une assignation.
- **contentieux-batiment** : référé expertise, responsabilité décennale,
  appel en garantie.
- **penal** : quand une affaire de copropriété devient pénale (abus de
  confiance, mise en danger, diffamation, harcèlement) ; la plainte.
- **lire** : lire une décision (visa, moyens, motifs, dispositif ;
  cassation et rejet ; portée) ; N4 : le commentaire d'arrêt.

**Exercices dominants** : datation (circuits), cas, lecture, dessin.
**Sources** : Code de procédure civile, Code de l'organisation
judiciaire, loi 65, décret 67, Judilibre, justice.fr. **Trous nommés** :
des décisions publiques choisies pour chaque branche.

### 6.7 Travaux, marchés et lecture de plans (`travaux`)

- **vocabulaire** : échafaudage et nacelle ; maîtrise d'ouvrage,
  maîtrise d'œuvre, bureau d'études, coordonnateur sécurité ; DOE,
  DIUO ; lot, corps d'état, DPGF, CCTP ; réception et réserves.
- **plans** : échelles ; plan, coupe, façade, plan de masse ;
  abréviations (EU, EV, EP, ECS, EF) ; niveaux et cotes ; symboles.
- **du-besoin-au-devis** : cahier des charges ; mise en concurrence
  (art. 21) ; comparer des devis ; attestations d'assurance, Kbis,
  vigilance ; N3 : le tableau comparatif.
- **marche-prive** : la norme NF P 03-001 et ce qu'elle règle ; acompte,
  retenue de garantie, pénalités, révision ; sous-traitance ; avenants ;
  décompte définitif.
- **chantier** : réunions et comptes rendus ; sécurité ; affichage ;
  réception, levée des réserves, garanties ; N3 : la réception.
- **urbanisme-des-travaux** : déclaration préalable et permis ; le PLU ;
  les Bâtiments de France ; le ravalement obligatoire ; enseignes.
- **renovation-globale** : audit, DPE collectif, PPT ; scénarios ;
  assistance à maîtrise d'ouvrage ; aides et financement ; N4 : la
  rénovation performante contre la rénovation par gestes.
- **honoraires-travaux** : les honoraires du syndic sur travaux et les
  conflits d'intérêts ; N4 : doctrine et déontologie.

**Exercices dominants** : plan, relier, cas, lecture de devis (sur pièce
publique fictive). **Sources** : Code civil, CCH, Code de l'urbanisme,
AQC, guides ANAH ; NF P 03-001 est payante (résumé de doctrine, à
recouper). **Trous nommés** : des plans libres de droits ; des devis
fictifs validés.

### 6.8 Énergie et rénovation (`energie`)

- **physique** : déperditions, isolation, ponts thermiques, inertie ;
  ventilation et humidité ; confort d'été.
- **dpe** : histoire du DPE ; la méthode de calcul ; les étiquettes ; le
  DPE collectif et son calendrier `[À VÉRIFIER]` ; fiabilité et
  contestation.
- **calendrier** : les interdictions de location par étiquette et leurs
  dates `[À VÉRIFIER]` ; ce que ça change pour la copro. Cartes à
  péremption obligatoire.
- **audit-et-ppt** : l'audit énergétique ; le plan pluriannuel de
  travaux et le DTG ; le fonds de travaux.
- **aides** : les aides nationales et locales, les certificats
  d'économies d'énergie, le prêt collectif ; cartes à péremption
  obligatoire.
- **contrats-energie** : tarifs réglementés et marché ; gaz et
  électricité ; le contrat d'exploitation de chauffage ; les prix
  (péremption).
- **chauffage-collectif** : individualisation des frais ; réseaux de
  chaleur ; pompes à chaleur collectives ; N4 : quelle énergie pour
  quel immeuble.
- **irve** : le droit à la prise ; l'infrastructure collective.

**Exercices dominants** : QCM, cas, datation, feuille-blanche.
**Sources** : ADEME, ecologie.gouv.fr, Légifrance, ANAH, CRE.
**Trous nommés** : aucun majeur ; risque de péremption élevé, à
surveiller mensuellement.

### 6.9 Propriété, immobilier et urbanisme (`immobilier`)

- **propriete** : la propriété et ses démembrements ; l'indivision ; les
  servitudes ; la mitoyenneté ; les troubles anormaux de voisinage ;
  l'empiètement.
- **vente** : la vente d'un lot du compromis à l'acte ; diagnostics et
  surface ; l'état daté et le pré-état daté ; l'opposition ; les
  charges au prorata.
- **location** : le bail d'habitation ; la décence ; les charges
  récupérables ; le meublé de tourisme et le règlement de copropriété.
- **urbanisme** : le PLU et ses zones ; autorisations ; servitudes
  d'utilité publique ; préemption ; cadastre et division.
- **acteurs-et-formes** : notaire, agent, promoteur, bailleur social,
  ADIL, mairie ; ASL, AFUL, division en volumes, copropriété
  horizontale.
- **fiscalite** : taxe foncière et enlèvement des ordures ; plus-value ;
  notions d'IFI et de TVA immobilière ; péremption.
- **local** : le bâti d'Angers et du 49 ; le PLUi ; les fragilités
  observées (radar DREAL).

**Exercices dominants** : flash, QCM, cas. **Sources** : Code civil,
Code de l'urbanisme, loi 89-462, Légifrance, ANIL, DVF. **Trous
nommés** : la doctrine notariale libre.

### 6.10 Le cabinet : déontologie, contrats, relation (`cabinet`)

- **profession** : carte professionnelle, garantie financière, assurance
  responsabilité ; le code de déontologie ; la formation continue
  obligatoire ; N4 : histoire et critique de la profession.
- **contrat-de-syndic** : le contrat type ; forfait et prestations
  particulières ; durée, révocation, mise en concurrence.
- **cycle-annuel** : le calendrier du gestionnaire, de la clôture des
  comptes à l'exécution des décisions ; les obligations annuelles ; N3 :
  dérouler une année sans rien oublier.
- **conseil-syndical** : rôle, réunion, délégation ; préparer et
  restituer ; la psychologie d'un groupe.
- **assemblee-en-pratique** : animer, tenir le bureau, gérer les
  contestations et la salle ; les fausses demandes de vote ; le
  procès-verbal en séance ; N3 : une AG qui tourne mal.
- **ecrire** : courrier, mail, notification ; ton et engagements ; le
  silence n'est pas un accord.
- **negocier** : avec un prestataire (le P2 du chauffagiste, le contrat
  d'ascenseur) ; méthode et alternatives ; N3 : préparer une
  négociation.
- **donnees** : RGPD au cabinet ; pièces jointes de convocation et
  données personnelles ; lutte contre le blanchiment ; sécurité.
- **charge** : gérer son temps, déléguer, prioriser ; les échéances qui
  ne se ratent pas.
- **cas-transverses** : les dossiers qui mêlent les domaines
  (`BLUEPRINT.md` §8) : un dégât des eaux du 5e au 2e ; une fissure
  avant l'AG ; un impayé de dix-huit mois ; le chauffage en panne en
  janvier ; la copro classée G doit rénover ; un copropriétaire ferme
  sa loggia ; l'ascenseur à l'arrêt et une personne en fauteuil ; une
  vente avec opposition. Niveau 3, prérequis dans plusieurs domaines.

**Exercices dominants** : cas, role, synthese, ecoute (plus tard).
**Sources** : loi Hoguet, décrets 2015-1090 et 2015-342, CNIL,
doctrine de négociation (ouvrages, `doctrine`). **Trous nommés** : la
psychologie d'assemblée n'a pas de source primaire ; elle vit en
`doctrine` et `terrain`, marquée comme telle.

### 6.11 Culture (`culture`, hors arbre)

Des lectures, une de temps en temps, jamais au détriment du métier : la
propriété (les textes fondateurs), l'habiter, le voisinage, la ville,
l'histoire du logement (Haussmann, les grands ensembles, le logement
social), l'architecture et ses styles, l'histoire de la copropriété.
Terrain naturel des défis entre joueurs de métiers différents. Exercice :
lecture, synthese.

## 7. Le quiz de positionnement

Vingt questions au premier lancement : deux par domaine, une de niveau
1 et une de niveau 2, tirées dans des branches distinctes. Une bonne
réponse stabilise sa carte et ouvre sa branche. Le quiz n'écrit jamais
un remplissage.

## 8. Ce qui n'est pas dans le programme

- Les outils propres à un employeur (l'ERP Maya, les procédures
  internes, l'organigramme) : gadget, hors produit.
- La gestion locative et la transaction au-delà des bases du domaine
  `immobilier` : ce sont d'autres métiers, d'autres arbres.
- Le droit du travail, la comptabilité d'entreprise au-delà des bases.
- Tout ce qui n'a pas de source primaire ou de doctrine signée : ça
  reste un trou nommé.

## 9. Les trous nommés du programme, au 02/09/2026

| Trou | Domaines | Où chercher légalement |
|---|---|---|
| Images de pathologie et d'équipements | pathologie, equipements | schémas SVG maison depuis les textes AQC ; photothèque de terrain (plus tard) |
| Seuils de fissuration | pathologie | guide CSTB façades (indisponible) ; à défaut, rester qualitatif |
| Convention IRSI en texte libre daté | sinistres | site de France Assureurs (organisation-pro, à recouper) |
| NF P 03-001 | travaux | AFNOR (payant) ; résumés de doctrine |
| Décisions publiques par branche de procédure | procedure | Judilibre, sélection à faire |
| Annexes comptables et devis publics fictifs | comptabilite, travaux | à fabriquer et valider |
| Doctrine de niveau 4 en accès libre | droit, immobilier | rapports Cour de cassation, thèses en ligne, ANIL |
| Psychologie d'assemblée | cabinet | doctrine et terrain, jamais présenté comme science |

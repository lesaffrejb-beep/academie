# CORPUS — brancher le wiki sur l'Académie

Écrit le 28/08/2026 sur la question de JB : « ici y'a un wiki, peut-être
qu'on prend ces données ? sous quelle forme, quelle orga : les images,
les faits, les news, les articles, les études scientifiques, les
sources ? ». Ce document est le CONTRAT entre le repo (le wiki) et la
banque de l'Académie : quel type de matière, venu d'où, devient quoi,
par quel chemin. Il complète le BLUEPRINT §7 (les trois sources) sans
le répéter : ici le routage opérationnel, là-bas la doctrine.

Principe central : **le wiki n'est pas la banque, il est le minerai.**
On n'apprend jamais « dans » le repo (un skill est une procédure pour
agent, pas une leçon) ; on EXTRAIT, on reformule en carte ou en
atelier, et la carte pointe sa source. Le repo reste la vérité, la
banque reste jouable, le lien `source:` fait le pont.

---

## 1. Le routage par type de matière

| Type de matière | D'où ça vient | Ça devient | Où ça vit | Règle propre |
|---|---|---|---|---|
| **Fait métier stable** (majorité d'AG, seuil, définition, ordre de grandeur) | wiki : apprentissages-syndic, références de skills, référentiels publics | carte Flash ou QCM | `banque/<domaine>/` | source + date obligatoires (règle dure 3) ; jamais un fait copro nommé |
| **Méthode / grille de lecture** (lire un arrêt, auditer un devis, lire une annexe) | grilles des skills erp-* | fiche de méthode d'atelier + cartes « méthode » extraites | `banque/ateliers/` | la grille du skill fait foi ; un trou découvert = on corrige le skill, pas une doctrine bis |
| **Image technique** (pathologie, équipement, façade) | photos VT de JB ; Wikimedia Commons / CC ; photos produites exprès | carte photo-diagnostic, relier, datation | perso : `etat/<profil>/` — partagée : `banque/images/` | photo VT = couche perso par défaut ; montée en banque une à une, anonymisée, validée JB ; licence + crédit tracés par image |
| **News / actualité** (arrêté, décret, jurisprudence, actu locale) | file d'alertes + veille R14 | carte « fil du réel » (0-1/jour) OU atelier « Lire un texte nouveau » si le document le mérite | `banque/` (abstraite) + lien vers le texte public | l'Académie CONSOMME la veille, ne la refait pas ; texte officiel = public, partageable |
| **Article de fond** (philo, socio, urbanisme : la propriété, l'habiter, la ville) | presse de fond, revues, textes publics choisis | atelier « texte du bac » | `banque/ateliers/` | droit de cite : lien + extraits courts, jamais le texte recopié |
| **Étude scientifique** (sciences de l'apprentissage) | littérature (vérifiée, voir §3) | RIEN dans la banque métier : c'est le carburant du MOTEUR (choix des modes, FSRS) | `CADRAGE-SCIENTIFIQUE.md` + BLUEPRINT §3 + ce fichier §3 | on ne fait pas apprendre à JB la science de l'app ; elle justifie l'app |
| **Pièce réelle du portefeuille** (devis, annexe, PV) | serveur / OFF-X/pieces (le .md converti vaut la pièce) | atelier personnel (pointeur, jamais copie) | `etat/<profil>/ateliers/` | jamais en banque partagée ; préparé en local, en batch, corrigé validé AVANT |
| **Réponse d'une base documentaire externe** (NotebookLM, carnet « Copropriété », 300 sources) | skill global `notebooklm` (voir §4) | matière première d'une carte ou d'un atelier, jamais collée telle quelle | `banque/<domaine>/` après revérification | la réponse nomme ses documents mais ne porte aucune date : un fait de droit se recoupe à Légifrance avant de devenir carte |
| **Trace de travail de JB** (JOURNAL, questions à Claude, rituel sortie de réunion) | repo + sessions | détection de lacune → carte `brouillon` | `banque/` après anonymisation + validation | digesteur M5 ; jamais les transcriptions de tiers |

Ce qui ne route JAMAIS vers la banque : les bruts de `lab/` (erreurs
citables documentées), les coulisses, tout fait copro nommé, tout
document sous copyright recopié.

## 2. Le gisement réel du wiki (inventaire par agent, 28/08/2026)

Réponse mesurée à « peut-être qu'on prend ces données ? » : oui, le
repo porte de quoi faire la banque M1 avec de la marge (**~100-120
cartes extractibles** pour un besoin de 60-80), mais le gisement est
très inégal par domaine (§2.3) et il n'y a **aucune image partageable**.

### 2.1 Les 10 filons les plus rentables pour M1

| # | Fichier | Rendement | Domaine §9 | Réserve |
|---|---|---|---|---|
| 1 | `apprentissages-syndic.md` (22 apprentissages, tous datés/sourcés) | 15-20 cartes, dont QCM « piège » | 3, 4, 5 | aucune |
| 2 | `templates/majorites-ag.md` + `.json` | 12-15 cartes | 3 | **revérif Légifrance obligatoire** (le fichier le dit : sources secondaires, Légifrance injoignable au moment de l'écriture) |
| 3 | `.agents/skills/erp-juridique/references/veille-2024-2026.md` | 8-10 cartes (la §7 « prête à redire » est déjà du texte de carte) | 3 | péremption 12 mois |
| 4 | `.agents/skills/erp-pieces/references/radar-conformite-annuelle.md` | 13 cartes clés en main (13 obligations, Légifrance 19/08) | 3, 6 | aucune |
| 5 | `.agents/skills/erp-comptable/references/checklist-anomalies-comptes.md` (`validated`, confidence 0.85) | 8-10 cartes | 5 | aucune |
| 6 | `.agents/skills/erp-conseil/references/sujets/` (12 fiches) | 12-15 cartes | 6, 3 | `energie-socle.md` périmé (prix vérifiés 02/07, révisions CRE depuis) |
| 7 | les 5 `lab/*/DEPOUILLEMENT.md` (1 139 l., le meilleur niveau du repo) | 8-12 QCM dont le distracteur = l'erreur du rapport brut | 2, 3, 6 | jamais les bruts |
| 8 | `.agents/skills/erp-sinistres/references/` (grille DDE-IRSI + matrice urgence, confidence 0.9) | 6-8 cartes | 4 | aucune |
| 9 | `.agents/skills/erp-patrimoniale/references/pathologies-bati-local.md` | 6-8 cartes | 1 | statut « V1, pas normatif » : seuils à recouper AQC/DTU |
| 10 | `referentiels/ag-registre/cycle-complet/` + recouvrement | 8-10 cartes | 3, 5 | **paraphrase obligatoire** (miroir de supports Sergic sous copyright) |

Autres filons notables : `erp-audit/references/branche-electricite.md`
(le meilleur candidat ATELIER du repo, méthode issue d'un audit réel),
`erp-devis/references/cadre-marche-prive-travaux.md` (atelier devis),
`erp-seance/references/` (QCM « cette convocation est-elle
régulière ? »), le vocabulaire contrôlé de
`templates/referentiel-batiment.md` (cartes vocabulaire pro),
`outputs/PORTEFEUILLE/VUES/revue-obligations-2027-2030.md` (calendrier
réglementaire, à anonymiser).

### 2.2 Ce qui NE route pas (confirmé sur pièce)

- `resolutiontheque.md` et `referentiels/` tels quels : texte
  propriétaire employeur — paraphrase seulement, jamais recopiés.
- Les bruts de `lab/` (erreurs citables documentées dans son README),
  `coulisses/` en bloc, `outputs/PORTEFEUILLE/` nommé (hors flux
  FILE-ALERTES), les cartes d'outils internes (`cartes/` = cartographie,
  pas flashcards — homonymie à ne pas confondre), les schémas méta du
  repo.

### 2.3 Les trous, domaine par domaine (arbre §9)

| Domaine | Verdict | Détail |
|---|---|---|
| 1. Pathologie du bâtiment | **TROU MAJEUR** | un seul fichier de 148 l. « V1 non normatif » ; rien sur fissures fines, époques, I1-I4, toiture-terrasse. À sourcer AQC |
| 2. Technique des équipements | **TROU MAJEUR** | rien de structuré sur VMC, ascenseurs, P1-P5, colonnes EU/EV, contrôle d'accès — le domaine des « vrais mots » du brief est quasi vide |
| 3. Droit de la copropriété | OK | le mieux couvert du repo |
| 4. Procédure et contentieux | TROU partiel | fragments (19-2, forclusion, recouvrement) ; rien sur le circuit complet référé / injonction / saisie |
| 5. Comptabilité | OK | checklist + skills budget/comptable |
| 6. Énergie et réglementation | PARTIEL | conseil/aides/prix bien couverts ; rien sur le DPE lui-même (méthode, refontes, calendrier interdictions) |
| 7. Plans et vocabulaire pro | **TROU MAJEUR** | ~120 l. de vocabulaire éclaté, zéro matière plan (l'exemple échafaudage vs nacelle du brief n'existe nulle part) |
| 8. Culture | TROU total, **attendu** | sourcing externe par construction |

### 2.4 Les images : pas de banque, un gisement privé

Aucune photothèque technique partageable dans le repo. Le seul vrai
gisement : **~201 photos de VT** sur 3 copros
(`outputs/IMMEUBLES/*/VT/*/photos/`), déjà classées par thème
(façades, ascenseur, locaux techniques, parking…) — couche privée,
montée en banque une à une, anonymisée et validée JB (BLUEPRINT §7).
Pour M1/M4, le mode photo-diagnostic dépend donc de Wikimedia
Commons / fiches AQC + des photos VT validées : c'est un chantier de
sourcing externe, pas d'extraction du wiki.

### 2.5 Immocampus : le gisement employeur, repéré le 28/08/2026, PAS ENCORE CAPTÉ

Signalé par JB le 28/08/2026 (« on scrapera tout ça, garde en tête que
ça existe et qu'il faudra récupérer tout »). Le portail SharePoint des
formations Sergic (« Le portail des connaissances » / Immocampus)
publie des replays et des « Essentiels métier ». **C'est le gisement
qui comble les trous du §2.3**, et il vient avec deux verrous.

Ce qui y est repéré, rangé par trou qu'il comble :

| Trou du §2.3 | Ressources Immocampus repérées |
|---|---|
| **1. Pathologie (trou majeur)** | Replay Pathologie des bétons (23/09/2025), Replay Pathologie des balcons (22/09/2025) |
| **2. Technique des équipements (trou majeur)** | Replay Technique du bâtiment (22/06), Replay Réussir une visite technique (23/10/2025) |
| 3. Droit | EM Les majorités et le pouvoir en AG, EM La convocation de l'AG, EM Le déroulement d'une AG, EM Savoir lire un PV d'AG, EM Le vote par correspondance, EM Rôle et responsabilité du syndic, EM Copropriété : origine, principes, notion d'immeuble, EM Les acteurs de la copropriété |
| 4. Procédure (trou) | Les mesures de recouvrement post-jugement (ADLITEM, 03/10/2025), EM Protection Juridique et impayés de charges |
| 5. Comptabilité | EM Savoir lire les annexes d'un budget, Préparer efficacement ses AG : les 5 annexes, EM Lien entre budget et appel de provisions |
| 6. Énergie | Replay 3 CEP (24/06), Parlons sobriété : bornes de recharge en copro (22/05) |
| Hors arbre | ELUCOPRO (assurance des membres du CS), TRACFIN, RGPD, cyber, Maya, eseis/viva syndic |

**Verrou 1, le droit — c'est le point dur.** Ce sont des supports de
formation de l'employeur, sous son copyright. La règle du §1 s'applique
sans exception : **on paraphrase et on lie, on ne recopie jamais**. Et
une carte qui en dérive ne peut pas vivre dans la même couche qu'une
carte tirée de Légifrance : d'où le niveau de partage `interne`
introduit au contrat carte-v1 le 28/08/2026 (§2.6 ci-dessous), qui
existe précisément à cause de ce gisement.

**Verrou 2, l'accès.** Pages SharePoint authentifiées (compte Sergic de
JB) et replays très probablement en vidéo. « Récupérer tout » n'est
donc pas un scraping : c'est un chantier — authentification, export,
transcription des replays, puis dépouillement. À chiffrer avant de le
lancer, et à faire depuis le poste local (le serveur et SharePoint ne
se lisent que de là, `cabinet.yaml`).

**Ce qui est décidé pour l'instant** : rien n'est capté, et M1 ne
l'attend pas. La captation devient un chantier de roadmap à part
(proposé : M1-bis, après le pilote AQC qui aura donné le coût réel
d'une carte de domaine visuel). Le pilote AQC garde tout son sens :
ses sources sont **publiques**, donc `partage: banque`, alors
qu'Immocampus produira du `partage: interne`.

### 2.6 Trois couches de partage, pas deux

Conséquence directe du §2.5, intégrée au contrat carte-v1 :

| Couche | Ce qui y va | Qui peut la recevoir |
|---|---|---|
| `banque` | sources publiques (Légifrance, AQC, ADEME, Commons) | tout le monde, y compris un autre métier (M10) |
| `interne` | dérivé paraphrasé des supports employeur (Immocampus, `referentiels/`) | JB et ses collègues Sergic seulement — jamais une distribution externe |
| `perso` | pièces réelles du portefeuille, photos VT non anonymisées | le propriétaire du profil seul |

Le valideur refuse mécaniquement toute donnée nominative dans `banque`
ET dans `interne` : même entre collègues, une carte pédagogique
n'a jamais besoin du nom d'une copropriété réelle.

### 2.6 bis Ce que le pilote pathologie a mesuré (28/08/2026)

Le pilote de 10 cartes arbitré par JB a été mené le 28/08/2026. Son
but n'était pas les cartes, c'était le chiffrage. Résultats :

**Le coût est porté par la SOURCE, pas par la carte.** Ouvrir une
fiche AQC neuve coûte 5-8 opérations ; les cartes suivantes tirées de
la même fiche sont quasi gratuites. Cible réaliste : **3 cartes par
fiche AQC**.

| Lot | Fiches | Cartes | Coût |
|---|---|---|---|
| Fissures et structure (famille B) | ~10 | ~30 | 1 session |
| Humidité, façades, ravalement | ~10 | ~30 | 1 session |
| Toitures et terrasses (famille C) | ~12 | ~35 | 1 session |
| Balcons, planchers, ouvrages extérieurs | ~8 | ~25 | 1 session |
| **Domaine pathologie entier** | **~40** | **~120** | **4 sessions** |

**C'est beaucoup moins cher que ce que le constat « trou majeur »
laissait craindre**, parce que l'AQC a déjà fait le travail de mise en
forme (Le constat / Le diagnostic / Les bonnes pratiques / L'essentiel :
« Le diagnostic » donne la question, « L'essentiel » donne la réponse).
Le même ordre de grandeur vaut pour les domaines 2 (équipements,
familles E et G) et 7 (vocabulaire, via les règlements sanitaires
départementaux). **Les trois trous majeurs sont donc à ~12 sessions
d'agent**, pas à un chantier indéfini.

**Le piège, et il est grave.** `WebFetch` ne sait pas lire les PDF de
l'AQC : il rend du binaire, puis **hallucine** — sur ce pilote, il a
inventé des seuils de fissure (0,2 mm / 2 mm) que le document ne
portait pas. Le pipeline qui marche est `curl` + `pdftotext -layout`,
puis lecture directe. Coût : +2 opérations par fiche. **Un pipeline de
production qui ferait confiance à WebFetch sur un PDF produirait des
cartes fausses en silence** — exactement ce que tout ce dispositif
existe pour empêcher. À remonter vers `.agents/skills/erp-pdf`.

**Ce qui n'est pas sourçable, et qu'on n'a donc pas cardé.** Les
seuils « microfissure < 0,2 mm / lézarde > 2 mm » circulent partout,
attribués au CSTB et au Cerema, mais **uniquement sur des sites
commerciaux** (cabinets d'expertise fissures, assureurs, blogs
travaux) : aucune source publique primaire ne les porte. Idem pour
« fissure active vs stabilisée » (témoin plâtre, jauge Saugnac,
surveillance sur 24 mois), documenté seulement par ceux qui vendent la
prestation. Le guide CSTB/AQC « La pathologie des façades » qui
porterait la typologie coûte 56,87 € HT, papier, et il est **en
rupture de stock**. Aucune carte n'a été faite sur ces seuils.

### 2.6 ter Le verrou des images : il ne se lève pas par le sourcing

Mesuré, pas supposé :

- **AQC : exclu comme fonds photo.** Les mentions légales interdisent
  toute reproduction sans autorisation écrite, les CGV limitent à un
  usage documentaire, et les photos sont créditées à des tiers.
  Parfaitement exploitable comme **source** (paraphrase + lien),
  totalement inexploitable comme **image** — y compris les schémas,
  qui sont pourtant ce dont le photo-diagnostic aurait le plus besoin.
- **Wikimedia Commons : maigre**, mesuré à l'API. `Cracks` 94 fichiers
  (mélangeant fissures de sol, de glace, de peinture), `Building
  defects` 64, `Efflorescence` 33 ; `Rising damp`, `Cracks in
  buildings` et `Chimneys on roofs` **n'existent pas**. Soit 150 à 200
  fichiers utilisables sur tout le domaine, non curés, non légendés
  par un professionnel, sans garantie qu'ils illustrent la pathologie
  visée. Une photo non expertisée ne fait pas une carte de diagnostic,
  elle fait une carte fausse.

**Les deux seules voies qui restent pour M4** (arbitrage à rendre par
JB) : (a) les **~201 photos de VT du parc** — anonymisées et légendées
par JB lui-même, avec l'avantage décisif de porter le bâti qu'il visite
réellement ; (b) des **schémas SVG dessinés par nous** à partir des
mécanismes décrits par l'AQC — le texte est libre de paraphrase, le
dessin est le nôtre, le droit des sources est contourné proprement.
Quatre cartes du pilote portent déjà, dans leur `explication`, la
description de ce qu'un schéma devra montrer : c'est le cahier des
charges de M4, écrit d'avance.

### 2.7 Conséquence sur M1 (proposition)

Le repo suffit pour amorcer les domaines 3, 5, 4-partiel et 6-partiel.
Les domaines 1, 2 et 7 — précisément ceux que le brief vise (la souche
en toiture) — exigent du **sourcing externe** (AQC, ANIL, ADEME,
manuels publics, Commons) : c'est un lot de travail à part, à chiffrer
dans M1, pas un sous-produit de l'extraction. Proposition : M1 =
extraction wiki (60-80 cartes, domaines couverts) + UN pilote de
sourcing externe sur la pathologie (10 cartes AQC sourcées) pour
étalonner le coût réel du domaine visuel avant M4.

## 3. Les références scientifiques, re-sourcées (vérifiées le 28/08/2026)

Toutes les références citées de mémoire au BLUEPRINT §3 ont été
retrouvées et recoupées en ligne. Verdict global : **toutes
confirmées**, trois nuances corrigées dans le BLUEPRINT au passage.

| Principe | Référence exacte | DOI / URL | Nuance |
|---|---|---|---|
| Rappel actif | Roediger &amp; Karpicke (2006), Test-enhanced learning, *Psychological Science* 17(3), 249-255 | doi:10.1111/j.1467-9280.2006.01693.x | se tester bat relire aux tests DIFFÉRÉS ; la relecture gagne au test immédiat (5 min) — c'est bien le long terme qu'on vise |
| Techniques efficaces | Dunlosky et al. (2013), *Psychological Science in the Public Interest* 14(1), 4-58 | doi:10.1177/1529100612453266 | utilité haute = practice testing + distributed practice SEULEMENT ; l'interleaving n'y est que « moderate » |
| Espacement | Cepeda et al. (2006), Distributed practice in verbal recall tasks, *Psychological Bulletin* 132(3), 354-380 | doi:10.1037/0033-2909.132.3.354 | 839 comparaisons ; l'espacement optimal dépend du délai de rétention visé |
| Réapprentissage successif | Rawson &amp; Dunlosky (2011), *JEP: General* 140(3), 283-302 ; synthèse : Rawson &amp; Dunlosky (2022), *Current Directions* | doi:10.1037/a0023956 ; doi:10.1177/09637214221100484 | ~3 rappels corrects initiaux + relearning réparti = optimum |
| Difficultés désirables | Bjork &amp; Bjork (2011), Making things hard on yourself, but in a good way, in *Psychology and the Real World*, 56-64 | bjorklab.psych.ucla.edu (PDF officiel) | référence citable standard (concept : R. Bjork 1994) |
| Entrelacement | Rohrer &amp; Taylor (2007), The shuffling of mathematics problems improves learning, *Instructional Science* 35, 481-498 | doi:10.1007/s11251-007-9015-8 | moins bon PENDANT l'entraînement, meilleur au test à 1 semaine (à savoir : la séance mélangée paraît plus dure) |
| Double codage | Paivio (1986), *Mental representations* ; Paivio &amp; Csapo (1973), *Cognitive Psychology* 5(2), 176-206 | doi:10.1016/0010-0285(73)90032-7 | deux références distinctes (théorie + effet image) |
| Exemples travaillés | Sweller &amp; Cooper (1985), *Cognition and Instruction* 2(1), 59-89 ; Sweller (1988), *Cognitive Science* 12(2), 257-285 | doi:10.1207/s1532690xci0201_3 ; doi:10.1207/s15516709cog1202_4 | l'effet S'INVERSE chez l'expert (expertise reversal) : le guidage des ateliers doit s'estomper avec la maîtrise |
| Refus des styles d'apprentissage | Pashler et al. (2008), Learning styles: Concepts and evidence, *PSPI* 9(3), 105-119 | doi:10.1111/j.1539-6053.2009.01038.x | formellement : absence de preuve du « meshing », pas preuve d'absence |
| Half-life regression | Settles &amp; Meeder (2016), A trainable spaced repetition model…, *ACL 2016*, 1848-1858 | aclanthology.org/P16-1174 ; github.com/duolingo/halflife-regression | +12 % d'engagement quotidien en étude opérationnelle |

**FSRS, chiffres vérifiés** (28/08/2026) :

- Algorithme : github.com/open-spaced-repetition/free-spaced-repetition-scheduler ;
  benchmark : github.com/open-spaced-repetition/srs-benchmark (lisible :
  expertium.github.io/Benchmark.html).
- Le benchmark (~20 000 utilisateurs Anki, ~1,7 Md de revues) donne
  FSRS-6 meilleur qu'Anki-SM-2 pour ~99,6 % des utilisateurs (log loss
  ≈ 0,29-0,34 contre ≈ 0,35+ ; caveat officiel : SM-2 ne prédit pas de
  probabilités nativement). Ordre de grandeur pratique : 20-30 % de
  revues en moins à rétention égale.
- Rétention souhaitée : **défaut 0,90**, plage pratique recommandée
  0,80-0,95 (le « 0,85-0,90 » du blueprint était acceptable mais
  imprécis — corrigé).
- Optimiseur personnalisé : seuil **400 revues** (Anki 24.04+ ; 1000
  avant), optimisation possible en dessous avec moins de fiabilité.
- `py-fsrs` et `ts-fsrs` : existants, activement maintenus (releases
  2026, FSRS-6) — github.com/open-spaced-repetition/py-fsrs et /ts-fsrs.

---

## 4. NotebookLM : la base documentaire externe (branchée le 29/08/2026)

Le carnet **Copropriété** de JB est interrogeable depuis une session Claude
par le skill global `notebooklm`, installé dans `~/.agents/skills/notebooklm/`
(correctifs locaux : `PATCHES-JB.md`). Ce qu'il contient exactement, relevé le
29/08/2026 : [INDEX-NOTEBOOKLM.md](INDEX-NOTEBOOKLM.md) — 300 sources
déclarées, 294 titres distincts, dont 189 pages web (157 commerciales, 18
institutionnelles), 86 PDF, 17 markdown internes et 2 vidéos. Le carnet est
plein : le tri de ce qu'on en retire, et par quoi le remplacer, vit dans
[NOTEBOOKLM-A-RETIRER.md](NOTEBOOKLM-A-RETIRER.md).

```bash
cd ~/.agents/skills/notebooklm && ./.venv/bin/python -u scripts/ask_question.py --question "..."
```

Sans argument de carnet, c'est celui-là qui répond. Une question ouvre un
navigateur, pose, lit la réponse, referme : compter ~40 s, et le quota
Google tourne autour de 50 questions par jour. Une question complète vaut
mieux que trois morceaux.

### Ce que ça apporte, et ce que ça ne remplace pas

L'intérêt n'est pas la réponse, c'est **le nom des documents dont elle
sort** : le carnet répond en citant ses sources, ce qui donne une piste
vérifiable au lieu d'une affirmation de modèle. C'est le seul usage qui
justifie son coût.

Ce qu'il ne devient jamais :

- **Pas une source dans la hiérarchie des faits copro.** L'ordre de
  `CLAUDE.md` ne bouge pas : la pièce officielle, puis l'ERP et éseis, puis
  la mémoire du repo. NotebookLM n'y entre pas : il ne connaît aucun
  immeuble du portefeuille, et on ne lui donne rien qui en vienne.
- **Pas une dispense de Légifrance.** Gemini reformule ; la reformulation
  d'un article n'est pas l'article. Un fait de droit qui va être dit ou
  écrit se revérifie au texte, comme n'importe quel autre.
- **Pas une date de vérification.** La réponse ne dit pas quand ses
  documents ont été déposés ni s'ils sont à jour. La règle dure 3 s'applique
  entière : la carte porte la date à laquelle ON a revérifié, jamais celle
  de la réponse.

### Le chemin d'une réponse vers une carte

1. Poser la question en demandant explicitement les documents sources.
2. Recouper le fait à sa source primaire (Légifrance pour un texte, le site
   de l'organisme pour un dispositif, l'ouvrage pour un seuil technique).
3. Écrire la carte avec `source:` = la source primaire, pas le carnet ; la
   mention du carnet ne vaut pas source.
4. `app/valide_banque.py` refuse de toute façon une carte sans source ni
   date : le filtre reste le juge.

Autrement dit, le carnet est un **moteur de recherche sur un corpus choisi**,
pas un auteur. Il fait gagner l'étape « où est-ce écrit », pas l'étape
« est-ce exact aujourd'hui ».

### Anti-pollution

On n'envoie **jamais** dans le carnet un fait copro nommé, une pièce du
portefeuille, une coulisse ou un extrait d'`outputs/` : la question part chez
Google. Les questions restent abstraites, comme les cartes.

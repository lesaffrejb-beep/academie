# BLUEPRINT — L'Académie

Écrit le 28/08/2026 sur le brief dicté de JB (visite technique du
matin : sur une terrasse, incapable de dire si les souches étaient
d'anciennes cheminées ou des ventilations primaires de chute — c'est
exactement le trou que ce produit doit combler). Complété le même jour
(second brief JB) : le produit s'appelle **L'Académie** (nom d'usage
arbitré par JB, « pour l'instant » ; le cadrage initial disait « La
Matinale »), et il gagne les **ateliers** de lecture et d'analyse (§6).
Pré-mortem par agent frais passé le 28/08 (19 bloquants, réparations
intégrées ici et dans la roadmap ; rapport :
`travail/relecture-2026-08-28-cadrage.md`). Ce document IMAGINE le
produit ; rien n'est construit. Les chantiers vivent dans
[`ROADMAP.md`](ROADMAP.md).

---

## 1. La vision en cinq lignes

Chaque matin vers 8h15, avant de commencer le boulot, JB ouvre
**L'Académie** : ~15 minutes qui le font progresser là où son métier le
demande. Le menu du jour est tiré au sort (l'effet machine à sous, mis
au service de l'apprentissage), le contenu est piloté par un algorithme
de répétition espacée qui sait ce qu'il a oublié, et la matière vient
de trois sources : le socle du métier, l'actualité de la veille, et
**son propre travail d'hier** (« j'ai vu que tu avais un souci de
courroie sur la VMC : ce matin, on démonte un caisson »).

Le matin parce que c'est son pic cognitif (observation JB, assumée
comme telle) : le créneau est réservé au difficile, à l'analyse, à la
lecture — tout ce que la fatigue de la journée rend impossible après.

**L'ordre du matin** (à confirmer par JB, §13) : la séance d'Académie
se joue AVANT d'ouvrir Aujourd'hui — c'est le principe même du brief,
apprendre avant le boulot — avec une exception codée : si la file
d'alertes porte un RED non traité, l'écran d'ouverture l'affiche en
bandeau avec son lien AVANT le tirage (règle dure 5, Red Path : on
n'enferme jamais JB dans un jeu pendant qu'une échéance brûle). La
feuille de route du lundi (erp-du-jour) passe après la séance.

## 2. Ce que c'est, ce que ce n'est pas

**C'est** : l'école du matin du gestionnaire de copropriété — moitié
Duolingo (cartes, répétition espacée), moitié classe préparatoire
(lectures guidées, analyses de documents réels, « comme un bac : un
peu d'abstrait et un peu de concret »), privée, construite sur le
repo, où chaque contenu est sourcé et daté.

**Ce n'est pas** :
- La veille (elle existe : R14, file d'alertes, `tooling/veille/`).
  L'Académie la CONSOMME : une alerte d'hier peut devenir la leçon de
  demain, elle ne la remplace pas.
- Un chatbot. Le LLM intervient à des endroits précis (générer des
  cartes, corriger une réponse libre, jouer un rôle, corriger une
  analyse d'atelier), jamais comme écran d'accueil.
- Un LMS d'entreprise ni un outil corpo. La branche « connaître Sergic
  » (organigramme, chiffres, interlocuteurs) existe mais reste
  optionnelle et en bas de pile — arbitré par JB dans le brief même :
  « c'est un peu gadget, la priorité c'est devenir un meilleur
  professionnel ». Et **jamais un outil d'évaluation** : voir la règle
  de lecture des profils, §9.
- Un instrument de surveillance de qui que ce soit (§7, Granola).

**Pourquoi pas Anki tout court** (question honnête, posée au
pré-mortem) : Anki ferait gratuitement les cartes et la répétition
espacée — c'est d'ailleurs l'assurance-vie du projet : le schéma
carte-v1 (M1) **s'exporte en CSV Anki à tout moment**, donc si l'app
maison échoue, le contenu survit et se joue ailleurs. Ce qu'Anki ne
fera jamais : les ateliers sur les documents réels du portefeuille, la
boucle terrain (les cartes qui naissent du travail d'hier), les
corrigés adossés aux grilles des skills, le partage borné aux
collègues. C'est pour ÇA qu'on construit ; tant que ces
différenciateurs ne sont pas livrés (M3, M5), l'app maison n'a pas
encore prouvé qu'elle vaut mieux qu'Anki — la roadmap l'assume, y
compris l'option d'un démarrage express dans Anki pendant que M2 se
construit (§13.7).

## 3. Le socle scientifique (ce qu'on code, et pourquoi)

L'apprentissage est un domaine massivement étudié ; on code ce qui a
des preuves, on écarte ce qui n'en a pas — même quand c'est intuitif.

> Sourçage & Cadre théorique complet : voir [`CADRAGE-SCIENTIFIQUE.md`](CADRAGE-SCIENTIFIQUE.md)
> pour le cadrage neuroscientifique et cognitif détaillé (les 7 lois,
> CAR à 8h15, hypercorrection, signalisation & chiffres tabulaires,
> décomposition de séance, matrice par matière et bibliographie complète).
> Toutes les références ont été re-vérifiées à la source le **28/08/2026**
> (DOI/URL et nuances : [`CORPUS.md`](CORPUS.md) §3). Toutes confirmées ;
> trois nuances intégrées ci-dessous (interleaving « moderate » chez
> Dunlosky, rétention FSRS 0,90 par défaut, expertise reversal des
> exemples travaillés).

### Les sept principes qui structurent le produit

1. **Rappel actif (testing effect)** — se tester bat relire, à temps
   égal (Roediger & Karpicke 2006 ; Dunlosky et al. 2013 classent la
   « practice testing » en utilité haute, la relecture et le surlignage
   en utilité basse). → **Tout est question.** Aucun écran de lecture
   passive en ouverture ; la théorie arrive en feedback, après la
   tentative de réponse. Même l'atelier de lecture (§6) se clôt par
   des questions et des cartes extraites : une lecture sans rappel
   s'évapore.
2. **Répétition espacée** — revoir juste avant d'oublier ancre en
   mémoire long terme (effet documenté depuis Ebbinghaus ; méta-analyse
   Cepeda et al. 2006). → Un **planificateur FSRS** (§8) décide chaque
   matin quelles cartes reviennent. C'est le « me remontrer de temps en
   temps ce que j'ai l'air d'avoir oublié » du brief, en version
   algorithmique.
3. **Réapprentissage successif** — une carte n'est acquise qu'après
   plusieurs rappels corrects RÉPARTIS sur des sessions distinctes
   (Rawson & Dunlosky 2011). → Pas de « vu une fois = su » : le tableau
   de bord ne marque maîtrisé qu'après stabilité mesurée.
4. **Difficultés désirables** — l'effort de récupération construit la
   mémoire (R. & E. Bjork) ; trop facile = rien n'est appris. → Le
   moteur vise un taux de réussite élevé mais pas parfait,
   et le feedback est immédiat après chaque réponse. Le moteur vise la
   rétention FSRS par défaut (0,90 ; plage recommandée 0,80-0,95,
   vérifié 28/08/2026). Corollaire vérifié chez Sweller : l'effet des
   exemples travaillés S'INVERSE chez l'expert (expertise reversal) —
   le guidage des ateliers s'estompe avec la maîtrise.
5. **Entrelacement (interleaving)** — mélanger les sujets dans une
   session bat les blocs monothématiques pour la discrimination et le
   transfert (Rohrer & Taylor 2007 ; nuance : Dunlosky 2013 ne le
   classe qu'en utilité « moderate », et la séance mélangée PARAÎT
   plus dure pendant l'entraînement — c'est normal, le gain est au
   test différé). → Une séance mélange 2-3
   domaines, jamais 15 minutes d'un seul.
6. **Double codage** — image + mot ensemble surpassent le mot seul
   (Paivio ; picture superiority effect). → La pathologie du bâtiment
   et la technique s'apprennent PHOTO À L'APPUI, c'est même le mode
   principal de ces domaines (§5).
7. **Exemples travaillés (worked examples)** — pour une compétence de
   lecture complexe (un arrêt de cassation, une annexe comptable), le
   novice apprend d'abord sur un exemple décortiqué pas à pas, la
   charge cognitive en moins (Sweller). → Chaque type d'atelier (§6)
   porte sa **fiche de méthode** (« comment lire ce genre de document »)
   et le premier passage est guidé ; l'autonomie vient aux passages
   suivants.

### Les deux mythes qu'on refuse de coder

- **Les « styles d'apprentissage »** (visuel / auditif /
  kinesthésique) : aucune preuve que l'adaptation au « style » de la
  personne améliore l'apprentissage (Pashler et al. 2008). Le brief
  demandait « voir si JB comprend mieux quand il écrit ou quand il
  visualise » : on ne le fera PAS par profilage de style. La modalité
  s'adapte au CONTENU (une fissure = photo, une majorité d'AG = cas
  pratique), et l'adaptation à JB passe par la MESURE item par item
  (quelles cartes il rate, quel format a produit la meilleure rétention
  sur CETTE carte) — de la donnée, pas un horoscope.
- **La gamification punitive** : les streaks anxiogènes, vies, pertes
  de série à la Duolingo optimisent la rétention de l'UTILISATEUR, pas
  celle du SAVOIR. On garde ce qui sert (§4) et on jette la
  culpabilisation : une séance ratée ne casse rien, l'algorithme
  replanifie et c'est tout.

### Les patterns volés aux apps qui marchent

Même doctrine que l'ERP : on vole les patterns, jamais les plateformes.

| App | Le pattern bien pensé | Chez nous |
|---|---|---|
| Anki / FSRS | La révision pilotée par la mémoire mesurée ; le format de deck interopérable | Le planificateur (§8) ; l'export CSV Anki comme assurance-vie (§2) |
| Duolingo | La session courte quotidienne, le rituel, la variété des exercices ; half-life regression (Settles & Meeder 2016) côté science | Les 15 minutes du matin, modes en rotation |
| Tinder | Le geste binaire rapide sur une image | Mode photo-diagnostic (§5) |
| Jeux vidéo (arbres de talents) | La compétence qui se débloque, la carte qui donne envie | Arbres de compétence (§9) |
| Machine à sous | La récompense variable — retournée : la surprise porte sur l'EMBALLAGE (le format du jour), jamais sur le contenu (lui reste piloté par FSRS) ni sur une monnaie | Le tirage du menu (§4) — qui n'a de sens qu'avec 4+ modes : tant que M2 n'en livre que deux, l'écran d'ouverture est un simple menu, pas une fausse machine à sous |
| Exercices Montessori / maternelle | Relier, trier, manipuler | Mode « relier » (§5) |
| Khan Academy | La maîtrise par prérequis | Déblocage des branches de l'arbre |
| Les classes préparatoires / le bac | Le texte du jour, l'épreuve sur document, le corrigé | Les ateliers (§6) |

## 4. La boucle quotidienne

1. **Le tirage** (l'écran d'ouverture) : le menu du jour — « Ce
   matin : photo-diagnostic toitures + 2 révisions droit + l'actu DPE
   d'hier » ou « Ce matin : atelier — on lit un arrêt de la Cour de
   cassation ». Bandeau Red Path avant tout si la file d'alertes
   porte un RED non traité (§1).
2. **Les révisions dues** (FSRS) : 5 à 10 cartes que la mémoire est en
   train de lâcher. Non négociable, c'est le cœur — un jour d'atelier
   ne les saute jamais, il les compresse (5 cartes max).
3. **Le nouveau** : selon le jour, une leçon nouvelle (3-5 cartes,
   format adapté au contenu) OU un atelier (§6) — cadence cible : 1 à
   2 ateliers par semaine, tirés au sort parmi les ateliers prêts. Un
   jour sans contenu neuf disponible est une séance VALIDE (révisions
   seules) : le neuf dépend de l'approvisionnement (§7), jamais
   l'inverse.
4. **Le fil du réel** (0 ou 1 item) : une carte née de la veille
   (jurisprudence, arrêté municipal, actu locale) ou du terrain de JB
   (§7.3). C'est la carte qui donne la sensation que « l'app me
   connaît ».
5. **La clôture** (10 secondes) : ce qui est acquis, ce qui revient
   demain, la branche qui a bougé dans l'arbre. Un compteur de séances
   faites (pas de flamme qui meurt : un total qui monte).

Durée cible 15 minutes, bornes 10-20 (un atelier peut déborder à 25 :
c'est le prix d'une vraie lecture, il est annoncé au tirage). Si JB
dépasse, l'app propose de s'arrêter : la constance quotidienne vaut
plus qu'une grosse session (c'est l'espacement qui travaille, §3.2).

**La reprise après une coupure** (congés, saison d'AG — le cas
« trois semaines sans séance » est la norme du métier, pas
l'exception) : l'arriéré ne s'affiche JAMAIS en entier. La séance
plafonne à ~20 révisions, le reste est ré-étalé automatiquement par
le planificateur sur les semaines suivantes (on ré-étale, on ne jette
jamais) ; un mode vacances (dates posées) décale les échéances en
bloc. Revenir après trois semaines ressemble à une séance normale à
peine plus dense, pas à une dette de 200 cartes.

## 5. Les modes d'exercice (cartes)

En rotation, tirés au sort dans ce qui convient au contenu du jour :

| Mode | Le geste | Pour quoi | Correction |
|---|---|---|---|
| **Flash** | question → je réponds dans ma tête → je révèle → je note (raté / dur / bien / facile) | définitions, articles, chiffres repères, ordres de grandeur métier (« chiffres à connaître ») | auto-évaluation (grades FSRS) |
| **QCM** | 4 choix, distracteurs plausibles | majorités d'AG, seuils, procédures | exacte |
| **Photo-diagnostic** | une photo, « qu'est-ce que c'est ? à quoi ça sert ? » façon Tinder | pathologie, équipements, vocabulaire pro (souche de ventilation primaire vs cheminée…) | exacte + fiche |
| **Relier** | apparier termes ↔ images, causes ↔ pathologies, années ↔ techniques constructives | typologies (fissures, enduits I1-I4, époques) | exacte |
| **Datation** | photo de façade → « années 60 ? 80 ? 2000 ? » | lecture du bâti, pathologies par époque (à Angers : ce qu'on a construit et comment ça vieillit) | exacte + tolérance |
| **Réponse libre** | j'écris ou je dicte ma réponse, le LLM corrige (« pas tout à fait : tu confonds actif et produit ») | comptabilité, raisonnement juridique, explication au CS | LLM + sources de la carte |
| **Jeu de rôle** | un prompt prêt à copier lance une conversation dédiée : « tu es un chauffagiste, défends ton P2, je dois te challenger » | négociation prestataires, P1-P5, séance de CS | LLM, débriefé en fin de partie |
| **Lecture de plan** | extrait de plan annoté → « que signifie cette abréviation ? où passe la colonne EU ? » | plans, coupes, abréviations, DOE | exacte |

Réponse au clavier, à la dictée ou à la souris/au doigt selon le
mode — y compris en mobilité (téléphone, hors du bureau) : chaque mode
déclare ses entrées, le mobile n'a que les modes compatibles.

## 6. Les ateliers : lire, analyser, corriger (le côté « bac »)

Ajouté sur le second brief JB du 28/08/2026. L'atelier est l'autre
moitié de l'Académie : pas une carte de 30 secondes, mais 10-15 minutes
sur UN document — le lire avec une méthode, répondre à des questions
dessus, recevoir un corrigé, et repartir avec 2-3 cartes extraites qui
entrent en répétition espacée (sans cette extraction, la lecture
s'évapore — §3.1).

Chaque TYPE d'atelier porte sa **fiche de méthode**, l'astuce de
lecture explicite (« comment lire ce genre de document ») : c'est elle
qu'on apprend vraiment, le document du jour n'est que le terrain
d'entraînement (§3.7, exemples travaillés).

| Atelier | La matière | La méthode enseignée | Le corrigé |
|---|---|---|---|
| **Lire un arrêt** | une décision réelle (Judilibre / Légifrance, textes publics) | structure d'un arrêt de cassation : en-tête, visa, moyens, motifs, dispositif ; cassation vs rejet ; portée réelle vs sur-lecture | questions de compréhension + analyse LLM adossée au texte |
| **Lire un texte nouveau** | l'arrêté, le décret ou la loi que la veille R14 a remonté | champ d'application, entrée en vigueur, ce qui change pour un syndic, ce qui n'est PAS dedans | idem + « qu'est-ce que j'en fais lundi ? » |
| **Lire un bilan / une annexe** | une annexe comptable RÉELLE du portefeuille (le .md déjà converti) | les 5 annexes du décret comptable : où est le résultat, où sont les impayés, les 3 chiffres à regarder d'abord | la grille d'erp-comptable, appliquée et VALIDÉE selon le circuit qualité du skill avant de servir |
| **Auditer un devis** | un VRAI devis du portefeuille | la grille de conformité (assurance, mentions, chiffrage, déontologie) : qu'est-ce qui est en règle, qu'est-ce qui ne l'est pas | l'audit erp-devis du même devis, produit et validé AVANT l'atelier (voir règle 6) |
| **Le texte du bac** | un article de fond, philosophie / sociologie / urbanisme (la propriété, l'habiter, la ville, le voisinage) | lire pour restituer : la thèse en une phrase, l'argument central, une objection | questions + « la redire au DA en 30 secondes » |

**Règles propres aux ateliers** (les garde-fous du repo s'appliquent
en plus, §7) :

1. **Document réel du portefeuille = couche personnelle, jamais la
   banque partagée ni la distribution collègues.** L'atelier vit dans
   `etat/<profil>/ateliers/` : le jour où un collègue reçoit
   l'Académie, il reçoit les fiches de méthode et les ateliers sur
   textes PUBLICS (décisions de justice, textes officiels), jamais une
   pièce du portefeuille de JB.
2. **L'atelier POINTE la pièce, il ne la copie jamais.** Le `.md`
   converti d'une pièce indexée vit dans `OFF-X/pieces/` et vaut la
   pièce (hiérarchie des sources, règle 0) ; l'atelier référence ce
   chemin, ne l'embarque pas (frontière reçu/produit de
   `cabinet.yaml` : jamais de doublon). Conséquence assumée : un
   atelier sur pièce réelle n'est jouable que là où le coffre est
   présent. « Re-OCR pour l'occasion » = seulement une pièce jamais
   convertie ; sinon on lit le converti existant.
3. **Le serveur ne se lit que du poste Windows** (SharePoint local,
   `cabinet.yaml`) : les ateliers sur pièces réelles se PRÉPARENT en
   batch depuis une session locale (lecture libre autorisée), jamais à
   la volée le matin depuis le cloud. Un stock d'ateliers prêts (cible :
   3-4 d'avance) absorbe les semaines sans préparation.
4. **Le corrigé réutilise les grilles des skills** (erp-devis,
   erp-comptable) : l'Académie n'invente pas une deuxième doctrine
   d'audit, elle entraîne JB sur celle qui existe. Si l'exercice révèle
   un trou dans la grille, c'est la grille qu'on corrige (boucle
   d'amélioration gratuite).
5. **Un atelier finit toujours par ses cartes extraites** (2-3), qui
   rejoignent la rotation FSRS : la méthode de lecture elle-même
   devient des cartes (« dans un arrêt de cassation, où se trouve la
   règle de droit ? »).
6. **Le corrigé n'est ni un document que JB a déjà validé, ni un
   jet de LLM non vérifié** (les deux tuent l'exercice, pour des
   raisons opposées). La pièce d'atelier se choisit parmi les dossiers
   que JB n'a PAS traités lui-même (reprises antérieures à sa prise de
   poste, dossiers passés par les assistants — le portefeuille en est
   plein) ; le corrigé est produit par un agent AVANT l'atelier et
   passe le même circuit de validation qu'une carte (double passe,
   statut `brouillon` → `valide`). Un corrigé non validé = l'atelier
   n'est pas prêt, il ne sort pas.

## 7 bis. RECADRAGE DU 28/08/2026 — le cours magistral prime, le terrain est un condiment

**À lire avant le §7, qu'il corrige.** Arbitrage de JB, mot pour mot :
« moi je veux apprendre des choses sur le droit, l'immo, la pathologie
du bât. Rien à foutre de me rappeler que EP c'est eaux pluviales parce
que je l'ai entendu hier. Je veux juste du cours magistral de haute
qualité, avec récursivité, plein de modes, et de l'XP. Le truc qui
vient de ce qu'on apprend, c'est juste pourquoi pas un sujet de temps
en temps, mais absolument pas le gros. »

Ce que ça change, et c'est structurant :

1. **La boucle terrain n'est plus le différenciateur.** Le §7.3 la
   présentait comme « LE différenciateur » du produit. Elle redevient
   ce qu'elle vaut : un item occasionnel, jamais le socle. **On ne
   fabrique plus de cartes à partir d'`apprentissages-syndic.md`** ni
   des JOURNAL. Les 20 cartes déjà produites depuis ce fichier ont été
   retirées de la banque le 28/08/2026 (archivées dans
   `travail/ecarte-2026-08-28/`).
2. **Le produit est un COURS**, structuré et exigeant, sur un savoir
   qui existe indépendamment de JB : le droit de la copropriété, la
   pathologie du bâtiment, la technique des équipements, la
   comptabilité, l'immobilier. Pas un carnet d'expérience recyclé.
3. **La source fait la qualité.** Une règle de droit se prend dans le
   texte (Légifrance), pas dans le souvenir d'un dossier ; une
   pathologie se prend dans une fiche AQC. Le pilote pathologie du
   28/08 était la bonne direction ; l'extraction d'`apprentissages-syndic`
   était la mauvaise.
4. **« Récursivité, plein de modes, de l'XP »** : le cours se déroule
   en profondeur, chaque notion appuyée sur ses prérequis et ouvrant
   sur son niveau suivant (`prerequis` et `niveau` du contrat
   carte-v1, arbre du §9) ; les modes du §5 sont confirmés comme
   attendus, pas comme un luxe ; l'XP et la progression restent.
   `[Interprétation de « récursivité » à confirmer par JB : structure
   de cours en profondeur, du général au particulier. S'il visait la
   révision récursive, c'est FSRS et c'est déjà là.]`

**Conséquence sur l'approvisionnement** : le §7.1 (socle métier) devient
la source quasi unique, et le gisement se déplace du repo vers
l'extérieur — textes officiels, fiches AQC, Immocampus (M1-bis).
Le §7.2 (actualité) reste. Le §7.3 (terrain) passe en accessoire, et
M5 (le digesteur) perd sa priorité en conséquence.

## 7. Les trois sources de contenu (et la boucle terrain)

1. **Le socle métier** (stock, construit une fois puis enrichi) : la
   matière déjà dans le repo — `apprentissages-syndic.md`, les
   références des skills (`majorites-ag.md`, fiches erp-conseil,
   veille juridique 2024-2026), les deepsearches DÉPOUILLÉS de `lab/`
   (jamais les bruts : trois erreurs citables y ont déjà été
   documentées) — plus les référentiels publics : fiches pathologie
   AQC, ANIL, ADEME, Légifrance, cours GPI de JB. Droit de cite :
   on paraphrase et on LIE la source, on ne recopie jamais un manuel
   sous copyright dans la banque `[À VÉRIFIER licence par source au
   moment de M1]`.
2. **L'actualité** (flux) : la veille R14 écrit déjà dans la file
   d'alertes. Un digesteur transforme l'alerte d'hier en carte du
   lendemain — ou en atelier « Lire un texte nouveau » (§6) quand le
   document mérite mieux qu'une carte : l'arrêté sur les trottinettes
   dans les halls devient « que peut interdire le règlement de
   copropriété ? », avec le lien.
3. **Le terrain de JB** (flux, LE différenciateur) : ses JOURNAL, ses
   propres questions posées à Claude, ses visites techniques. Un agent
   y détecte les lacunes (« il a confondu crédit et produit », « il
   n'a pas su nommer la souche en toiture ») et propose des cartes.
   Une photo prise en VT peut devenir une carte photo-diagnostic ; un
   devis reçu la veille peut devenir l'atelier de vendredi. **Les
   transcriptions de réunions (Granola) sont un cas À PART** : elles
   portent surtout la parole de TIERS (copropriétaires, conseillers
   syndicaux) qui n'ont consenti ni à la transcription ni à sa
   réutilisation — le pré-mortem a relevé que demander le seul GO de
   JB posait la question à l'envers. Par défaut : NON. Les
   alternatives sans tiers (§13.2) couvrent l'essentiel du besoin.

**L'approvisionnement est une exploitation, pas un chantier** (réparé
au pré-mortem : le stock M1 de 60-80 cartes ne nourrit que 12-27
matins de neuf). Dès M2, un rythme de croisière : un lot hebdomadaire
de 15-20 cartes `brouillon` produit par agent (~une session Opus par
semaine, batchable en fenêtre creuse), validation par échantillon
(~10 min de JB), et le « fil du réel » v0 rédigé à la main dans le
même lot tant que le digesteur (M5) n'existe pas. Coût total assumé :
~15 min de JB par jour de séance + ~10 min de validation par semaine ;
si ce budget déborde, c'est le quota de neuf qu'on baisse, jamais le
temps de JB qu'on étire.

**Garde-fou anti-pollution (hérité de CLAUDE.md, non négociable)** : la
banque de cartes partagée est ABSTRAITE et anonymisée — jamais un nom
de copro, un montant, une personne. Le lien avec le vécu (« on l'a vu
ensemble mardi en VT ») vit dans une couche personnelle séparée
(`etat/<profil>/contexte.jsonl`, et les ateliers réels dans
`etat/<profil>/ateliers/`), jamais dans la carte. **Les photos de VT
suivent la même pente** : par défaut couche personnelle ; une photo ne
monte en banque partagée qu'anonymisée ET validée une à une par JB
(anonymisée = cadrage serré sur le détail technique, aucune adresse,
aucune plaque, aucun visage, rien qui permette à quelqu'un de l'agence
de reconnaître l'immeuble). Le jour où un collègue reçoit la banque,
il ne reçoit aucune donnée du portefeuille.

**Garde-fou anti-bêtise (règle dure 3 étendue)** : une carte porte
`source:` (article, fiche, pièce, URL) et `verifie: AAAA-MM-JJ`, sinon
elle n'entre pas en jeu. Une carte générée par LLM naît en statut
`brouillon` et n'est jouable qu'après validation (double passe par un
agent frais qui remonte à la source, puis échantillonnage JB). En
session, un bouton « cette carte est fausse » : la carte passe en
`signale`, sort de la rotation, et la correction est un chantier
d'agent — c'est la réponse au « je me retrouve à apprendre des choses
fausses ou mal taguées » du brief.

## 8. Le moteur : FSRS, pas SM-2

Arbitré : **FSRS** (Free Spaced Repetition Scheduler, open source,
planificateur par défaut d'Anki depuis fin 2023), pas le vieux SM-2
d'Anki historique ni un algorithme maison. Pourquoi :

- Benchmarké (vérifié 28/08/2026 : ~20 000 utilisateurs Anki, ~1,7 Md
  de revues) : FSRS-6 bat Anki-SM-2 pour ~99,6 % des utilisateurs,
  ~20-30 % de revues en moins à rétention égale (chiffres et caveats :
  `CORPUS.md` §3).
- Implémentations libres maintenues en Python (`py-fsrs`) et
  TypeScript (`ts-fsrs`) — **dépendances à déclarer** dans
  `tooling/requirements/` (le socle du repo tourne stdlib seule ;
  l'alternative, un portage FSRS pur Python d'une centaine de lignes
  depuis l'algorithme publié, s'arbitre en M2). Le planificateur peut
  tourner côté générateur (Python, comme `erp/app/genere.py`) ET côté
  client (révision hors ligne).
- Il modélise récupérabilité + stabilité + difficulté PAR CARTE : c'est
  exactement la donnée qu'il faut pour l'arbre de compétence (§9), le
  tableau de bord, et l'équilibrage « insister sur les lacunes sans
  sur-réviser les acquis » demandé dans le brief.
- Les quatre grades FSRS (raté / dur / bien / facile) s'appliquent tels
  quels au mode Flash ; les modes à correction exacte (QCM, relier…)
  s'y projettent (faux → raté, juste lent → dur, juste → bien).
- **Au démarrage : paramètres FSRS par défaut**, assumé. L'optimiseur
  personnalisé exige ~400 revues (doc Anki 24.04+, vérifié
  28/08/2026) ; on l'activera quand le journal le
  portera, pas avant (le défaut est déjà au-dessus de SM-2).
- **La coupure est gérée par le moteur, pas par la culpabilité** :
  plafond d'affichage quotidien (~20 revues), ré-étalement automatique
  de l'arriéré, mode vacances (§4).

L'état de révision est un journal append-only
(`etat/<profil>/revues.jsonl` : timestamp, carte, grade, mode, durée),
même philosophie que le JOURNAL des copros : on n'écrase jamais, tout
se recalcule depuis le log. Deux appareils qui écrivent chacun leur
bout se fusionnent par union horodatée, sans conflit possible — c'est
le log qui est la vérité, jamais un « état courant ». C'est aussi ce
qui permettra un jour de répondre à « quel FORMAT marche le mieux sur
ce type de carte » avec des données réelles (§3, refus des styles
d'apprentissage).

## 9. Les arbres de compétence

> **Amendé le 29/08/2026 au soir** (séance JB × Arthur,
> `CADRAGE-PRODUIT.md` Partie 4 §VI ; spec : `SPEC-PRODUIT.md` §3) :
> le modèle d'écran devient la **carte-monde de régions à conquérir**
> — remplissage 0-100 %, seuil d'ouverture (~75 %), liberté d'aller
> se frotter partout, boss-examen requis pour le 100 %, brouillard
> levé région par région. Les domaines ci-dessous deviennent les
> premières régions de la carte de JB ; la mécanique de déblocage par
> stabilité FSRS reste la mesure sous-jacente. Le reste du § (règle
> de lecture des profils) est inchangé.

Le brief le demande et la pédagogie le justifie (maîtrise par
prérequis, façon Khan Academy) ; c'est aussi le meilleur écran de
motivation (« donner envie de débloquer »).

**Les domaines de premier niveau** (arbitré, resserré sur « meilleur
professionnel » ; le corpo attendra) :

1. **Pathologie du bâtiment** — fissures (qualifier une lézarde vs
   fissure vs microfissure), humidité, toitures et étanchéité,
   façades et enduits (I1-I4…), pathologies par époque de construction.
2. **Technique des équipements** — VMC (caisson, courroies, pourquoi
   elles se détendent), ascenseurs (les vrais mots : opérateur de
   porte, pas « portail »), chauffage collectif (P1/P2/P3/P4/P5, RE au
   gaz), contrôle d'accès (cellule, ventouse, émetteur), plomberie
   (colonnes EU/EV, ventilation primaire, surpresseur).
3. **Droit de la copropriété** — loi 65 / décret 67, majorités,
   parties communes/privatives, ALUR, ELAN, Climat et Résilience.
4. **Procédure et contentieux** — mise en demeure, commissaire de
   justice (ex-huissier), référé, injonction de payer, saisie : le
   circuit complet qu'un contentieux en cours rend urgent à comprendre.
5. **Comptabilité de copropriété** — actif/passif, produits/charges,
   annexes 1-5, fonds travaux, régularisations.
6. **Énergie et réglementation** — DPE (historique, les refontes de
   méthode de calcul), audit énergétique, aides et malus, calendrier
   des interdictions de location.
7. **Lecture de plans et vocabulaire pro** — coupes, abréviations,
   niveaux, ce qu'il faut pour parler d'égal à égal avec une maîtrise
   d'œuvre (échafaudage vs nacelle, honoraires de travaux…).
8. **Culture** — le côté bac de l'Académie : lire un texte exigeant
   (philosophie, sociologie, urbanisme : la propriété, l'habiter, le
   voisinage, la ville), en tirer une idée qu'on sait redire. Branche
   sans arbre de prérequis (on n'y « monte » pas, on s'y frotte), un
   atelier de temps en temps, jamais au détriment du métier.

Chaque domaine s'ouvre sur ses bases ; les branches profondes se
débloquent par la maîtrise mesurée (FSRS : stabilité moyenne de la
branche parente au-dessus d'un seuil). L'écran d'arbre montre les
forces réelles (« très bon en façades, aveugle en interphonie ») — et
c'est LUI qui répond au « dans 6 mois, est-ce que j'ai vraiment appris ? »
du brief, avec un bilan mensuel généré (cartes maîtrisées par domaine,
lacunes persistantes, temps investi).

**La règle de lecture des profils, gravée avant le premier profil**
(amendée le 29/08/2026, arbitrage 1 du brief produit autonome —
l'amendement est tracé ici même, pas décidé en silence : voir
ROADMAP, M11) : l'état d'apprentissage (`revues.jsonl`, arbre, bilan)
est la cartographie mesurée des faiblesses professionnelles d'une
personne. Il n'est lisible que par son propriétaire **et, à partir de
M11, par les amis qu'il a mutuellement et explicitement ajoutés**
(visibilité désactivable par domaine, retrait d'un clic) ; aucun
écran comparatif hors de ce cercle consenti ; le bilan mensuel de JB
va à JB seul.
L'Académie n'est pas et ne deviendra pas un instrument d'évaluation —
le jour où un manager demande « l'arbre de compétence » d'un
collaborateur, la réponse doctrinale est non, et elle est écrite ici
pour être opposable. Ces données entrent au registre RGPD du repo
(`meta/2026-08-24-registre-traitements-rgpd.md`) AVANT la première
écriture (chantier M2).

## 10. Architecture technique (alignée sur la maison)

Mêmes principes que l'ERP (raisons arbitrées le 20/08/2026, roadmap
ERP §Pourquoi) : markdown + git, zéro SaaS, LLM-lisible, réversible.

```
academie/
  banque/                 # LE CONTENU (partagé, anonyme, versionné)
    pathologie/…​.md       # une carte = un bloc YAML+md, schéma carte-v1
    droit/…​.md
    ateliers/             # fiches de méthode + ateliers sur textes PUBLICS
    images/               # licences tracées ; photos VT : validées une à une
  app/                    # LE MOTEUR (source, comme erp/app/)
    genere.py             # assemble la séance du jour → site statique
    fsrs/                 # planification + miroir client (dépendances §8)
    digesteur.py          # veille + terrain → cartes brouillon (M5)
    atelier_prep.py       # session LOCALE : pièce du serveur → atelier perso
  site/                   # GÉNÉRÉ, jamais édité à la main (comme erp/site/)
  etat/<profil>/          # PAR PROFIL, append-only, jamais dans la banque
    revues.jsonl          # (jb = premier profil, jamais codé en dur)
    contexte.jsonl        # le lien perso carte ↔ vécu (copros), PRIVÉ
    ateliers/             # ateliers sur pièces réelles : POINTEURS, PRIVÉ
  academie.json           # config : métier, domaines, quotas, profils
```

- **Front** : statique généré + JS de session, PWA installable (comme
  R8 : manifest + icônes), thème NUIT Sergic — le bleu #0062AB et le
  jaune de la charte en version sombre, tokens dédiés dérivés de ceux
  du front ERP (le dark mode y existe déjà) ; l'Académie a sa propre
  peau, calme, zéro chrome d'ERP.
- **La séance existe quand JB arrive — la chaîne réelle, maillon par
  maillon** (le pré-mortem a démoli la version incantatoire) : une
  Routine cloud à 7h00 lun-ven génère la séance et la pousse sur
  `main` (elle passe AVANT la routine existante « Feuille de route du
  matin » de 7h30, `meta/2026-08-19-roadmap-etape-2.md`, sans la
  toucher). MAIS le VPS ne se met à jour aujourd'hui que par
  `maj-vps.sh` lancé à la main (décision R10) : M2 doit donc poser LA
  brique manquante — un timer de pull côté VPS (systemd : `git pull` +
  régénération bornée à `academie/site/`), petite, mais nouvelle et à
  valider avec JB. Repli si la chaîne casse : la séance de la veille
  reste jouable, les révisions dues sont recalculées côté client
  depuis le journal. Jamais de « page blanche à 8h15 ».
- **Écriture mobile** : le back actuel (R10) est volontairement borné
  au JOURNAL des copros (`journal_io.py` : slugs OFF-* seulement, un
  commit-push par écriture) — il ne se réutilise PAS tel quel.
  L'Académie ajoutera sa PROPRE route (`POST /api/academie/revues`),
  écrite par LOTS (une séance = un envoi = un commit, jamais un par
  carte), même mécanique de jeton. C'est une extension du back à
  concevoir en M8, pas un pattern gratuit.
- **Hors ligne** : exige un service worker — précisément ce que R8 a
  refusé pour l'ERP (contenu qui bouge à chaque push). Pour l'Académie
  le refus ne s'applique pas (la séance du jour est FIGÉE à 7h00),
  mais c'est un chantier propre (M8), pas un pattern à recopier.
- **LLM** : v1 = prompts prêts à copier (jeu de rôle, correction
  libre, corrigé d'atelier) dans une conversation Claude dédiée — zéro
  infrastructure ; v2 = via le back (clés API côté serveur, doctrine
  D20).
- **Hébergement** : le VPS OVH + Caddy existant pour JB. **Le partage
  aux collègues est un problème d'hébergement à part entière** (le
  pré-mortem l'a établi : l'auth actuelle est un basicauth PARTAGÉ sur
  tout `erp/site`, et le clone du VPS contient `outputs/` et
  `coulisses/` en entier) : M9 commence par une DISTRIBUTION séparée —
  `genere.py` produit un site Académie autonome (banque publique +
  moteur + état du profil, rien d'autre), servi sur son propre vhost
  avec ses propres identifiants, jamais depuis le clone complet du
  repo. Sans cette séparation, M9 n'a pas le droit de commencer.

## 11. Généralisable à d'autres métiers (posé dès le jour 1)

Le moteur ne sait rien de la copropriété : il lit `academie.json`
(nom du métier, domaines, quotas) et une `banque/` au schéma carte-v1.
Donner l'Académie à un autre métier = écrire une autre banque et une
autre config, le moteur et les modes sont identiques. Concrètement :

- Le schéma carte-v1 (M1) est documenté comme un CONTRAT, indépendant
  du contenu syndic — et exportable en CSV Anki (réversibilité, §2).
- Aucun texte métier ni prénom en dur dans `app/` (même règle que
  « jamais JB ou Sergic en dur dans un skill » ; le profil est une
  entrée de config, `etat/<profil>/`).
- La boucle terrain (§7.3) est une INTERFACE (« un agent qui lit les
  traces de travail du profil et propose des cartes brouillon ») dont
  l'implémentation syndic (JOURNAL, questions à Claude) est un plugin
  parmi d'autres possibles ; idem la préparation d'ateliers (une pièce
  + une grille de correction, quel que soit le métier).
- Cible réaliste : d'abord les collègues gestionnaires (même banque,
  leur profil, leur arbre), ensuite seulement un autre métier (toute
  personne avec un abonnement Claude et un repo).

## 12. Les arbitrages rendus

Par JB (28/08/2026, second brief) :

1. **Nom : « L'Académie »** — nom d'usage « pour l'instant », il peut
   encore changer ; le dossier suit (`academie/`). La roadmap ERP
   reste la roadmap ERP (en-têtes clarifiés en ce sens).
2. **Les ateliers font partie du produit** (lectures guidées,
   documents réels, le côté bac) : intégrés au §6 et à la roadmap (M3).

Par délégation (premier brief : « je te laisse arbitrer ») :

3. **FSRS**, pas d'algorithme maison (§8), paramètres par défaut au
   démarrage.
4. **Pas de profilage « style d'apprentissage »**, mesure par carte à
   la place (§3, preuves).
5. **Streak doux** : total cumulé qui monte, jamais de série qui
   casse (§4) ; coupures gérées par ré-étalement, jamais par dette.
6. **Banque partagée anonyme + couche perso séparée** (§7) : c'est ce
   qui rend le partage aux collègues possible sans ouvrir le repo ;
   les ateliers sur pièces réelles restent dans la couche perso (§6.1).
7. **Corpo Sergic : branche optionnelle, plus tard** (le brief
   lui-même la classe gadget).
8. **Domaines d'amorçage : pathologie, technique des équipements,
   droit + procédure** — là où le brief situe les manques les plus
   coûteux sur le terrain ; compta et DPE suivent avec les ateliers
   (M3) et la boucle terrain (M5).
9. **L'état d'un profil n'est lisible que par son propriétaire** (§9) ;
   jamais d'usage managérial.
10. **Transcriptions Granola : NON par défaut** (la parole des tiers
    n'est pas à JB de la donner, §7.3) ; les alternatives sans tiers
    couvrent le besoin.

## 12 bis. Les arbitrages rendus le 28/08/2026 (le GO de M1)

JB a tranché le 28/08/2026 au soir. **M1 est ouvert.** Les points du
§13 ci-dessous sont conservés pour mémoire du raisonnement ; ce qui
suit fait foi.

1. **Les deux domaines de front** (§13.4) : on ne choisit pas entre le
   droit et la pathologie, on fait les deux. M1 se scinde en deux lots
   — extraction du wiki (droit, compta, procédure : la matière existe)
   et sourcing externe (pathologie).
2. **Pas d'Anki** (§13.7) : « je veux que notre truc avance ». Le
   moteur maison se construit directement, sans détour de validation.
   L'export CSV reste au contrat comme assurance-vie, pas comme étape.
3. **Timer de pull VPS : GO tout de suite** (§13.8), sans attendre M2.
4. **Pilote pathologie de 10 cartes en M1** (nouveau, CORPUS §2.7) :
   sourcé AQC, pour mesurer le coût réel d'une carte de domaine visuel
   avant de s'engager sur M4.
5. Les points 1, 2, 3, 5 et 6 du §13 (quota, Granola, photos de VT,
   premier atelier, ordre du matin) **restent au défaut proposé** :
   ils n'ont pas été rouverts, et aucun ne bloque M1.

**Le gisement Immocampus** (signalé le même soir, CORPUS §2.5) : le
portail de formations de l'employeur comble les deux trous majeurs
(pathologie, technique des équipements). Non capté, chantier distinct
à chiffrer. Il a fait naître la troisième couche de partage
(`interne`) au contrat carte-v1.

## 13. Ce qui restait à trancher (archivé — voir §12 bis)

1. Le quota : ~10 révisions + 1 leçon nouvelle par jour, 1-2 ateliers
   par semaine, plafond de reprise ~20 revues — ajustable ?
2. La détection de lacunes SANS les transcriptions de réunions (défaut
   arbitré : non, §12.10) : les alternatives te vont — tes JOURNAL,
   tes questions posées à Claude, et un rituel de 30 secondes en
   sortie de réunion (« je n'ai pas su répondre à X ») dicté par toi ?
   Ou veux-tu rouvrir la question Granola malgré les tiers ?
3. Les photos de VT : d'accord avec la règle « couche perso par
   défaut, montée en banque partagée photo par photo, anonymisée et
   validée par toi » (§7) ?
4. Le premier arbre à peupler en M1 : pathologie du bâtiment (proposé,
   c'est le plus visuel et le manque le plus récent) ?
5. Le premier atelier à monter en M3 : « Auditer un devis » (proposé),
   sur un devis que tu n'as PAS traité toi-même (règle §6.6) ?
6. L'ordre du matin (§1) : Académie AVANT Aujourd'hui, Red Path prime
   tout — c'est bien ça ?
7. Démarrage express pendant que M2 se construit : jouer le premier
   lot de cartes dans Anki (export CSV, gratuit, ton téléphone) pour
   valider l'appétence AVANT de coder le moteur — oui ou non ? (Anki
   est open source et interopérable : la doctrine « patterns, pas
   plateformes » tolère l'exception, comme Outlook ou Leaflet.)
8. Le timer de pull sur le VPS (§10, la brique qui rend le matin
   automatique) : GO pour l'installer en M2 ?

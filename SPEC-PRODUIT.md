# SPEC-PRODUIT — L'Académie autonome : architecture arrêtée et plan d'orchestration

Écrit le 29/08/2026 depuis les réponses de la séance JB × Arthur et le
brief écrit de JB (le tout consigné dans
[`CADRAGE-PRODUIT.md`](CADRAGE-PRODUIT.md) Partie 4 — ce fichier ne
répète pas les réponses, il en dérive la technique). **C'est un
document d'architecture et d'orchestration, pas du code** : la
construction est faite par des sessions Opus qui suivent le plan du §7.
Pré-mortem par agent frais passé le 29/08/2026 au soir — 1 Red Path
(réparé le jour même : un podium de collègues réels nommés dans le
front, voir §5), 20 bloquants et 12 mineurs, tous réparés dans cette
version ; rapport :
[`travail/relecture-2026-08-29-spec-produit.md`](travail/relecture-2026-08-29-spec-produit.md).

Ce que ce document remplace : rien. Ce qu'il précise : les briques
laissées ouvertes par M9-M11 de la ROADMAP (auth, hébergement, clé
tiers, flux fournisseur→produit, usine à domaines) et le game design
issu de la séance (carte-monde, boss, quiz de positionnement, carnet
d'erreurs). En cas de divergence avec la ROADMAP sur ces points, **ce
fichier fait foi** (il est postérieur et dérive des réponses) ; les
gates de la ROADMAP, eux, restent souverains.

---

## 1. Le produit en trois phrases

Une vraie appli d'apprentissage quotidien, conçue pour deux joueurs
(JB, syndic ; Arthur, concours IFSI) mais aux standards d'un produit
qui scale — sans aucun horizon commercial. Chaque joueur possède un
**repo source privé** où l'IA fabrique son domaine depuis ses propres
documents, en local, sur son propre abonnement ; le **serveur de jeu**
(VPS de JB) ne reçoit que des fiches JSON validées et sert la séance
du matin partout (ordi, téléphone). Le jeu est une **carte-monde de
régions à conquérir**, pas un arbre qu'on finit.

## 2. L'architecture en trois pièces (le modèle A4)

```
 CHEZ CHAQUE JOUEUR (local : son ordi, son drive, son abonnement IA)
 ┌────────────────────────────────────────────────────────────┐
 │  Le REPO SOURCE du joueur (privé, sur SON compte)          │
 │    sources/     ses PDF, cours, annales — JAMAIS poussés   │
 │                 vers le serveur, jamais dans git si lourds │
 │                 (pointeurs + inventaire versionnés)        │
 │    banque/      les fiches carte-v1 générées (JSON)        │
 │    academie.json  config du domaine (régions, quotas)      │
 │                                                            │
 │  L'USINE À DOMAINE (agent IA guidé, tourne en local        │
 │  sur la clé/l'abonnement DU joueur — §4)                   │
 └───────────────┬────────────────────────────────────────────┘
                 │  « je publie ma livraison » : push volontaire
                 │  des fiches JSON validées (couche partageable
                 │  seulement, scanner anti-fuite au passage)
                 ▼
 SUR LE VPS DE JB (l'infra qu'il porte)
 ┌────────────────────────────────────────────────────────────┐
 │  Le SERVEUR DE JEU — repo `academie` (privé, compte JB)    │
 │    front React (build propre, hors châssis ERP)            │
 │    moteur FSRS + valideur + contrat carte-v1 (extraits     │
 │      du repo wiki-copro, mêmes fichiers, même tests)       │
 │    SQLite : comptes, état de jeu, revues, erreurs, défis   │
 │    banques : un JSON par domaine, reçus des repos sources  │
 │    auth : magic links mail ; vhost + domaine dédiés,       │
 │      process séparé, racine hors du clone wiki-copro       │
 │    AUCUNE clé IA de tiers, AUCUN appel IA pour un tiers    │
 └────────────────────────────────────────────────────────────┘
```

Les invariants, dans l'ordre où ils protègent :

1. **Les sources restent chez le joueur.** Le serveur ne voit jamais
   un PDF, un cours, une annale — seulement des fiches dérivées
   (paraphrase + lien source), validées, au contrat carte-v1.
2. **Le traitement IA est local et au coût du joueur** (brief JB).
   Aucune clé de tiers n'est stockée ni utilisée côté serveur : la
   brique « stockage de clé tiers » de M9 disparaît par suppression.
   Corollaires assumés : pas de génération nocturne pour un tiers, et
   **le seul chemin de correction LLM en v1 est le copier-coller —
   pour tous les joueurs, JB compris** (un seul chemin à maintenir ;
   la « clé D20 côté serveur pour JB » de M6 v2 est amendée en
   conséquence, voir ROADMAP M6). La piste « appel API depuis le
   navigateur avec clé en localStorage » est `[À VÉRIFIER]` et HORS
   v1 : l'API Anthropic exige un opt-in explicite pour les appels
   navigateur, et une clé en localStorage est exposée à toute XSS et
   à l'opérateur du serveur qui sert la page — « jamais transmise »
   ne vaut que pour le transport, pas pour le modèle de confiance.
   Exception nommée et bornée : **la toute première fabrication (la
   soirée artisanale, O7) tourne sur l'abonnement de JB, une fois**,
   et on relève ce qu'elle coûte — c'est cette mesure qui calibre la
   promesse faite ensuite aux joueurs (§4).
3. **Le push est un geste humain, et il a un réceptionniste.**
   Publier une livraison de banque est volontaire, jamais un hook de
   commit. Côté joueur, le geste concret est un **téléversement du
   JSON depuis le produit** (plus réaliste qu'un push git pour
   quelqu'un qui ne code pas ; le push git reste le chemin de JB).
   Côté serveur, la réception est une brique nommée d'O6 : jeton par
   joueur (pattern du back R10), re-passage du valideur, refus tracé,
   quarantaine avant mise en jeu. Le scanner anti-fuite tourne au
   moment de la publication (côté source), le valideur re-tourne à la
   réception : deux barrières, deux dépôts. Les **banques reçues des
   joueurs vivent HORS git** (fichiers + sauvegarde) : un historique
   git ne s'efface pas proprement, et la suppression de compte sous
   48 h (§5) doit pouvoir retirer ce qu'un joueur a poussé. Seul le
   moteur, le contrat et le contenu réputé non personnel sont
   versionnés dans le repo produit.
4. **JB n'est pas un joueur spécial.** wiki-copro est son repo source
   parmi d'autres — il pousse sa banque copro exactement comme Arthur
   poussera la sienne. Ses couches `interne` et `perso` (Immocampus,
   ateliers sur pièces, `contexte.jsonl`) **gardent un domicile après
   l'extraction** : le serveur accepte des cartes `interne`/`perso`
   **liées à un profil unique et jamais servies à un autre** (le
   filtre par couche existe déjà dans `genere.py`) — sans ça, M1-bis
   deviendrait injouable et JB jouerait une banque appauvrie. Ces
   cartes-là vivent hors git comme toute banque reçue (invariant 3) ;
   `contexte.jsonl` et les pointeurs d'ateliers, eux, **ne quittent
   jamais le poste de JB** (ils référencent des copros nommées).
   Seule asymétrie restante : JB porte l'infra (VPS, domaine,
   moteur) — dit en face, c'est son choix (« moi je porte le côté
   archi VPS »). Corollaire prévu (brief 29/08 soir) : **le domaine
   copro est prêtable aux collègues gestionnaires** — le savoir est
   déjà digéré dans la banque partagée ; un collègue invité se
   connecte lui-même (compte à lui, état à lui) et joue la couche
   `banque` telle quelle, sans que JB fabrique quoi que ce soit pour
   lui. C'est le premier cas d'usage de l'invitation (§5), avant même
   un métier étranger.
5. **L'état de jeu vit sur le serveur** (SQLite), parce qu'un joueur
   a deux appareils. Le journal de révisions reste append-only et
   l'état se recalcule depuis le journal (acquis M2 conservé) ;
   l'export du journal en JSON reste possible à tout moment
   (réversibilité, et migration du profil JB = un import).

## 3. Le jeu (ce que la séance du 29/08 a changé)

### La carte-monde (amende l'arbre du BLUEPRINT §9, tracé)

- Un domaine = une **carte de régions**, pas un arbre. Le remplissage
  d'une région a UNE définition, calculable depuis le journal :
  **le % des cartes `valide` de la région dont la stabilité FSRS est
  ≥ 21 jours** (seuil paramétré dans `academie.json`, pas codé en
  dur). « L'XP » affichée est un habillage dérivé de cette mesure,
  jamais une seconde comptabilité — le moteur ne connaît que le
  journal. La région suivante s'ouvre à ~75 % de la précédente —
  **mais toute région visible est explorable** : on a le droit
  d'aller se frotter au boss d'une région lointaine, l'échec y est
  sans pénalité.
- Le 100 % d'une région n'existe pas sans son **boss : l'examen de
  région** — 10-15 cartes à froid, score solennel, piochant dans les
  annales (Arthur) ou en examen blanc (JB). Réussi, il ouvre ce que
  le seuil de remplissage n'a pas déjà ouvert.
- **Le brouillard se lève région par région** : on voit « la lumière
  au bout » (la région-objectif de la saison : le concours, le
  niveau pro) sans afficher l'immensité totale d'un coup. Première
  région d'Arthur : « Concours FPC IFSI ». Régions suivantes
  esquissées en silhouette (études IFSI, cadre), jamais détaillées
  avant d'être à portée.
- Le matin sans envie de choisir : **le tirage guidé** — un exercice
  au hasard, calibré au niveau (l'habillage sobre, M4).

### Le quiz de positionnement (onboarding)

~20 questions au premier lancement d'un domaine, pour ne pas retaper
les bases. Mécanique arrêtée (à défaut, révocable), corrigée au
pré-mortem — la stabilité standard d'une première révision « bien »
n'est que de ~2 jours (`planificateur.premiere()`, mesuré) : inscrire
les bonnes réponses comme révisions ordinaires ferait tout revenir
dans la semaine, l'inverse de la promesse. Donc :

- une bonne réponse inscrit la carte au journal avec **une stabilité
  initiale explicite et paramétrée** (`academie.json`, proposé S =
  21 j, plafonné) et un champ de provenance **`origine: "quiz"`** —
  indispensable pour que le futur optimiseur FSRS ne s'entraîne pas
  sur des réponses qui ne sont pas des révisions ;
- une mauvaise réponse n'inscrit **rien** (une erreur sur une carte
  jamais apprise n'est pas un raté FSRS) ;
- le quiz **ouvre** des régions (déblocage d'exploration), il
  n'écrit jamais leur taux de remplissage — le remplissage ne vient
  que de la mesure de stabilité (§ carte-monde), donc le seuil des
  ~75 % ne peut pas être atteint par le quiz seul. Seul FSRS mesure.

Puis le nouveau joueur joue immédiatement 5 cartes de son domaine —
la première séance dure moins de 10 minutes tout compris.

### Le carnet d'erreurs (brief JB : « noter questions fausses et pourquoi »)

À chaque erreur, après la micro-explication (3 lignes + source), le
joueur PEUT noter en une ligne pourquoi il s'est trompé (« confondu
avec X », « lu trop vite », « jamais appris »). Append-only, par
profil — stockage : `etat/<profil>/erreurs.jsonl` jusqu'à M9, la
table `erreurs` en SQLite après, **même schéma** (la migration est
une copie). Trois consommateurs :
le bilan mensuel (les erreurs récurrentes et leurs raisons), la règle
des 3 échecs (3 ratés sur une carte → mini-leçon ou carte préalable,
la note du joueur oriente laquelle), et la boucle terrain du joueur
(une raison récurrente = matière à cartes nouvelles). Jamais visible
des amis — le carnet d'erreurs est la partie la plus intime du profil,
il est exclu de la visibilité totale de M11.

### La deuxième vague du 29/08 au soir (brief JB après la première maquette)

- **L'écran d'accueil EST la carte-monde.** Gaming assumé : les régions
  avec leur niveau de complétion, et on clique où on veut aller. La
  séance du jour, le quiz, le journal sont des écrans qu'on ATTEINT
  depuis la carte, pas des onglets à côté d'elle. S'y ajoute le **mode
  aléatoire** : un bouton qui pioche un exercice dans les régions non
  conquises (< 100 %) — en excluant une région où il ne reste que
  l'examen : là, la seule proposition honnête est le boss lui-même.
- **La carte est une CARTE, pas une liste** (brief JB du 30/08, avec
  référence visuelle : un dashboard de lanceur de jeux — hero
  immersif, vignettes riches, anneau de stats, ambiance sombre
  chaleureuse). Des territoires dessinés sur un monde, des chemins
  entre eux, le **brouillard de guerre** sur ce qui n'est pas
  exploré, la citadelle du boss, la région-objectif comme « lumière
  au bout ». Arbitrage de trajectoire (JB l'a proposé lui-même) :
  **v1 = carte 2,5D immersive** (SVG/canvas, direction artistique
  jeu, brouillard réel) construite tout de suite ; **la 3D est un
  chantier nommé pour après** — `three` 0.180 est déjà une dépendance
  du front (Jumeau3D), donc pas de verrou technique, seulement du
  travail (terrain, caméra, perf mobile) qui ne doit pas retarder le
  reste. Le critère de JB fait loi : « on part en mode jeu vidéo » —
  un écran qui ressemble à un Quizlet est un écran raté.
- **La métaphore cible de la carte : le LIEU-MONDE** (idée JB,
  30/08). Pour la copro, la carte n'est pas un archipel : c'est
  **l'immeuble** — la toiture (étanchéité), la chaufferie (P1-P5), le
  hall (contrôle d'accès), les colonnes (plomberie), l'ascenseur, les
  lots (privatif), et la rue autour (le cabinet d'avocat = procédure,
  l'étude, la mairie = urbanisme). Le brouillard = les étages dans le
  noir. Fondement scientifique réel, pas gadget : c'est un **palais
  de mémoire** (méthode des lieux — l'ancrage spatial des
  connaissances est une des techniques de rétention les mieux
  documentées, à sourcer au CADRAGE-SCIENTIFIQUE). Généralisation :
  chaque métier choisit son lieu-monde (l'hôpital pour l'infirmier :
  urgences, bloc, pharmacie…) — le moteur reste agnostique, le lieu
  est un HABILLAGE par domaine (config + décor). Trajectoire arbitrée
  (JB : « on fait simple d'abord et on scale ») : v1 = la carte 2,5D
  générique en cours ; v1.1 = l'habillage immeuble en coupe SVG (sans
  3D) ; le chantier 3D (three.js déjà présent) utilisera des packs
  d'assets .glb du commerce plutôt que de modéliser — **licence
  vérifiée AVANT de construire dessus**
  (`wiki/patterns/licence-outil-avant-fonctionnalite.md`, leçon du
  29/08).
- **La carte v1.05 — l'archipel parlant** (brief JB, 30/08 soir,
  après avoir vu la première carte) : en attendant la 3D, chaque
  **île a la FORME de son sujet** (une île-ascenseur pour ascenseur,
  une clé à molette pour la mécanique, une croix pour la pharmaco…) —
  silhouettes SVG thématiques, pas des blobs génériques ; les îles
  aux thèmes liés sont reliées par des **ponts ou des petits bateaux
  qui font des allers-retours** ; et le boss-examen devient
  **« construire le pont »** (ou ouvrir la route maritime) vers l'île
  suivante — la conquête SE VOIT sur la carte. Lisibilité d'abord :
  la première version était illisible (verdict JB : « on comprend
  rien à l'UI ») — hiérarchie claire, pas d'écrans superposés, le
  premier lancement invite proprement au quiz au lieu d'un calque
  posé sur la carte.
- **La carte EST l'interface** (brief JB, 30/08 soir) : pas de barre
  d'actions en bas — on clique une île pour partir en séance, ou
  l'expédition aléatoire (un bouton-dé/boussole discret sur la
  carte). Le « mode 3 minutes » n'est plus un bouton : c'est la
  liberté de s'arrêter tôt, la clôture reste honorable quoi qu'il
  arrive.
- **La nuit n'est pas un tombeau** (brief JB, 30/08 soir : « trop
  dark, sombre pas plaisant, pas drôle, gaming trop sérieux — prends
  plus de liberté pour que ça donne envie de rester ; tous les
  modules se ressemblent »). Direction artistique : sombre CHALEUREUX
  et vivant façon la référence Dribbble — fonds bleu nuit profonds
  mais accents riches et variés, **chaque région a SA couleur** (et
  son icône), **chaque type d'exercice a sa personnalité visuelle**
  (en-tête, teinte, icône — un QCM ne ressemble pas à un flash qui ne
  ressemble pas à un jeu de rôle), de la VIE sur la carte (lumières,
  phare, bateaux qui bougent), de l'humour discret dans les
  micro-textes (complice, jamais infantile). La sobriété reste pour
  les ERREURS (l'hypercorrection est un moment sérieux) ; partout
  ailleurs, le plaisir est un objectif de design, pas un bonus.
- **Le ton des célébrations : les épaules des géants — JAMAIS de
  confettis** (brief JB, 30/08 soir : « bat les couilles des
  confettis »). La récompense visuelle est le **brouillard qui
  recule** (le « brouillard mental » qu'on repousse) et des mots
  d'humilité et de persévérance aux moments de conquête : « nous
  montons sur les épaules des géants », « la seule chose que je sais,
  c'est que je ne sais pas », apprendre pour délimiter ses
  frontières. Une banque de citations sourcées (Newton, Socrate…)
  plutôt que des animations de fête. Aucun confetti nulle part dans
  l'espace de jeu, y compris les maquettes qui y restent accessibles.
- **Entrer dans l'Académie = changer d'espace** (brief JB, 30/08) : au
  clic, le chrome ERP disparaît entièrement (rail, barre) et on passe
  en plein écran de jeu — menu propre dans le HUD, peau dédiée
  (cohérente charte, mais rupture assumée), retour à l'ERP par un
  geste évident. C'était déjà la doctrine du BLUEPRINT §10 (« sa
  propre peau, zéro chrome d'ERP ») ; ça préfigure l'extraction M9 où
  cet espace devient tout simplement le produit sur sa propre
  adresse.
- **Auto-save partout, aucun geste de sauvegarde.** Chaque réponse
  s'écrit au journal à l'instant où elle est donnée (append-only) ; on
  ferme l'onglet au milieu d'une séance, rien n'est perdu. L'export
  reste un filet de secours, jamais une habitude à prendre.
- **Le module puzzle est SUPPRIMÉ** (arbitrage JB : « j'apprends pas
  une langue, pas assez dur »). Retiré du front le 29/08. Le critère
  vaut pour tout mode futur : un mode qui n'exige pas de récupération
  effortful ou de discrimination réelle n'entre pas.
- **Des niveaux chronométrés, d'autres non.** Certains exercices se
  jouent en temps court (automatismes, fluence — c'est une condition
  d'expertise mesurée), d'autres sans aucune limite (analyse, réponse
  libre, ateliers). Design point pour le contrat carte-v2 : un champ
  optionnel `chrono` (secondes) par carte ou par examen ; jamais de
  chrono par défaut.
- **La profondeur progressive, jusqu'à l'expert.** La boucle voulue :
  « aujourd'hui je fais compta » → la leçon du jour entrecoupée de
  notions déjà vues (l'algo dose selon les erreurs) → plus on répond
  juste, plus on creuse. Le plafond n'est pas le manuel : les niveaux
  hauts vont vers la recherche en cours, la critique de doctrine, les
  controverses et prises de position, les grandes figures — « de la
  technique aux légendes du métier ». Design point : l'échelle
  `niveau` (1-3 aujourd'hui) s'étendra (1-5, 4 = doctrine/controverse,
  5 = recherche/frontière) quand le contenu suivra. **Et la carte est
  GIGANTESQUE en profondeur** (brief JB, 30/08) : le bout de chaque
  branche est défini — « théoriquement top 5 mondial de ce sujet
  précis en connaissance ». Ce n'est pas du marketing, c'est le
  critère de construction du contenu : une branche n'est « finie »
  dans la carte que si son dernier niveau atteint l'état de l'art
  (recherche, doctrine vivante), et l'immensité se révèle par le
  brouillard, jamais d'un coup (l'acquis anti-découragement du §VI
  du cadrage tient).
- **Un peu d'histoire dans chaque domaine** : une branche d'histoire
  du métier (d'où viennent la loi de 1965, l'IFSI, les grandes
  affaires) — l'histoire éclaire le présent et fait des cartes
  mémorables. Jamais dominante, comme Culture.
- **LA MÉTHODE, lisible par tout le monde** (brief JB, 30/08 :
  « l'idée c'est avant tout d'apprendre vite et bien, optimisé, basé
  sur la science, tous nos choix sourcés et documentés dans une
  méthode lisible par tout le monde »). Livrable nommé :
  `academie/METHODE.md` — pour chaque mécanique du produit, une
  entrée en trois lignes : *ce qu'on fait* (ex. les révisions
  reviennent à intervalles croissants), *pourquoi* (l'effet mesuré,
  en français normal), *la source* (l'étude ou la synthèse, lien +
  date de vérification — règle dure 3 appliquée à la pédagogie).
  Couvre au minimum : FSRS/espacement, récupération effortful vs
  relecture, l'hypercorrection après erreur, l'entrelacement, le
  boss-examen (practice testing), le palais de mémoire (lieu-monde),
  les niveaux chronométrés (fluence), le mode 3 minutes, les streaks
  doux, et les dark patterns assumés avec leurs bornes. Le
  CADRAGE-SCIENTIFIQUE est la matière première ; la MÉTHODE en est la
  version que Arthur, Agnès ou un collègue peut lire — et le produit
  y renvoie depuis l'app (« pourquoi cette mécanique ? »). Toute
  mécanique qui n'arrive pas à écrire son entrée n'entre pas dans le
  produit.
- **La science commande, y compris pour l'engagement.** Tout mode et
  toute mécanique se justifient par le CADRAGE-SCIENTIFIQUE (récupération
  effortful, espacement, difficulté désirable) et par ce qu'on sait de
  la plasticité cérébrale ; on copie ce qui marche dans les meilleures
  écoles et chez les meilleurs étudiants mesurés, pas le folklore. Et
  les **« dark patterns pour la bonne cause »** (brief JB) : brouillard
  de carte, boss, tirage, streak — les mécaniques d'engagement
  s'utilisent délibérément AU SERVICE du rituel, mais bornées par les
  garde-fous déjà gravés (jamais de culpabilisation, jamais de dette,
  défis coupés si les données montrent qu'ils dégradent le rituel).

- **L'ALGO EST LE PROF — le joueur ne choisit jamais le format**
  (brief JB, 30/08 : « je clique juste sur une zone et j'en sais rien
  de ce qui va se lancer ; je ne veux pas la main sur la méthode
  d'apprentissage »). Il n'existe AUCUN sélecteur de mode dans le
  produit : le joueur choisit OÙ (une zone, l'expédition aléatoire,
  la séance du jour), et le moteur compose la suite d'exercices —
  « hop un QCM, hop cette image, hop expliquez ce document, hop mise
  en situation » — selon l'état FSRS, les erreurs, l'entrelacement et
  le mix que la science prescrit. C'est cohérent avec la littérature
  (l'autorégulation du format par l'élève est précisément ce qui
  produit les illusions de maîtrise — relecture, blocs, QCM faciles)
  et ça simplifie l'UI : les « modes » sont une mécanique INTERNE du
  moteur, pas une navigation. Conséquence d'inventaire : l'arène de
  mini-jeux à choix de la maquette est périmée comme UI (elle reste
  un vivier de types d'exercice pour le moteur).

- **Adopté du benchmark du 30/08** (`travail/benchmark-2026-08-30.md`,
  chaque pattern licencié et sourcé) : (1) **le brouillard à deux
  couches** façon Civilization — *shroud* (jamais exploré) vs *fog*
  (exploré mais information PÉRIMÉE : une région sans révision
  récente affiche un remplissage douteux, grisé avec sa date — la
  règle dure 3 du repo rendue visible dans le décor) ; (2) **paliers
  nommés + verrou de boss** façon Khan Academy : quatre états nommés
  dérivés du remplissage (affichage seul), et un boss raté ne se
  retente pas le même jour (sinon « à froid » ne veut rien dire) ;
  (3) **la graine du tirage au journal** (à écrire dans le contrat
  O1b) : chaque séance/expédition journalise sa graine — « pourquoi
  il m'a servi ça ce matin » a toujours une réponse ; (4) **la règle
  de croissance** (gabarit, O2) : une région CONQUISE le reste —
  l'ajout de cartes nouvelles ouvre une sous-région, il ne fait
  jamais retomber une conquête ; (5) **invariant gravé** : « toute
  région visible est explorable » ne s'optimise JAMAIS au nom de la
  clarté (le procès fait au chemin linéaire de Duolingo est la
  preuve). Garde-fou transverse : les idées d'Anki/Exercism se
  volent, leur code AGPL jamais ; les icônes game-icons.net (CC BY
  3.0) exigent une **attribution visible dans l'app**.

### Le reste, confirmé sans changement

Streak cumulé doux + calendrier de pastilles (jamais de dette), mode
3 minutes explicite, défis optionnels jamais proposés d'office
(garde-fous M11 intacts), branche **Culture en tronc commun** partagée
entre tous les joueurs (propriétaire : JB), multi-domaines entrelacés
en séance, mode dégradé sans clé 100 % jouable (correction exacte
seulement) — **et c'est le mode par défaut d'Arthur en v1** (Q25 :
pas de réponse libre dans sa v1). Cosmétique — arbitrage Q35 AMENDÉ
par JB le 30/08 : plus que des titres, des **cosmétiques de fin de
zone sur un avatar** — finir une zone débloque l'attribut qui la
raconte (le chapeau d'étudiant en droit pour l'urbanisme copro,
l'éclair dans la main pour l'électricité des immeubles…), et chacun
**choisit de l'afficher ou non** sur son avatar. Règle inchangée du
§VI : la récompense qui ouvre du contenu (branches, boss) reste le
moteur ; le cosmétique raconte le parcours, il ne le remplace pas.
Jamais de boutique, jamais de monnaie.

## 4. L'usine à domaine : un parcours guidé LOCAL (redéfinit M10)

Le pipeline M10 n'est **pas un service web** : c'est un **parcours
guidé par agent IA, en local, chez le joueur, sur son abonnement** —
un humain qui ne sait pas coder se laisse dérouler les étapes (brief
JB). Le livrable de M10 est donc un kit : un gabarit de repo source +
un guide d'agent (l'équivalent d'un SKILL.md).

**Le runtime, nommé** (pré-mortem : « n'importe quelle session
Claude » est faux — claude.ai web n'a ni accès disque ni git) : le
kit vise **Claude Code (ou Claude Desktop + accès fichiers)** sur la
machine du joueur, avec sa liste d'installation écrite : un compte
GitHub, git, Node, un abonnement ou une clé. Cette installation est
**l'étape 0 de la soirée artisanale** (O7), faite ensemble. Et le
repli honnête de la v1 est écrit d'avance : si l'installation coince,
**Arthur dépose ses fichiers et la fabrique tourne sur la machine de
JB** (exception de l'invariant 2, bornée à la v1) — le repo source
d'Arthur est l'état CIBLE, pas le prérequis de sa première séance.

Les étapes du parcours :

1. **Où sont tes documents ?** L'agent inventorie le tas (dossier,
   drive) sans rien déplacer.
2. **Quel métier, quel objectif ?** Le domaine exact, la première
   région (pour Arthur : le concours FPC IFSI), l'échéance.
3. **Le test de santé des sources** — le geste fait sur le NotebookLM
   de JB, généralisé : classer fiable / commercial / douteux /
   doublon, dire quoi virer et pourquoi, dire ce qui MANQUE et où le
   télécharger légalement (référentiels publics du métier). Sortie :
   un inventaire versionné, façon `NOTEBOOKLM-A-RETIRER.md`.
4. **La génération** : régions, découpage, cartes au contrat carte-v1
   (JSON), toujours paraphrase + lien, jamais de recopie. **Et la
   règle du trou nommé** (brief JB, 29/08 au soir) : si l'IA juge
   qu'un sujet doit être couvert mais qu'aucun PDF source ni site
   fiable ne le couvre, **elle ne crée PAS les fiches** — elle écrit
   le trou dans l'inventaire (« sujet X : à sourcer, rien de fiable
   sous la main ») et propose où chercher. Une carte sans source
   n'existe pas, même pour combler un manque que le plan de région
   réclame ; la mémoire du modèle n'est jamais une source.
5. **La double passe par agent frais** qui remonte aux sources —
   obligatoire quel que soit le domaine (acquis pré-mortem M10), sur
   la clé du joueur. Le joueur échantillonne, il ne valide pas seul.
6. **Le valideur mécanique** (`valide_banque.py`, embarqué dans le
   gabarit) — rien ne se publie s'il est rouge.
7. **« Je publie ma livraison »** : push des fiches validées vers le
   serveur de jeu.

**v1 artisanale d'abord** (arbitré en séance) : la première exécution
se fait JB + Arthur + une session Claude, un soir, sur l'abonnement
de JB (exception bornée, §2). On note tout — le déroulé de cette
soirée EST le brouillon du guide d'agent.

**L'agent-compagnon : quand le back n'a plus rien, il PARLE** (brief
JB, 29/08 soir). Le produit ne s'assèche jamais en silence : quand la
génération n'a plus de matière, l'agent s'adresse au joueur dans
l'app — « plus de sources à traiter alors que le sujet n'est pas
fini » (il montre les trous nommés), « doute sur cette source, tu
confirmes ce document ? », « stock de cartes neuves épuisé —
relancer une génération ? » — et chaque message est un BOUTON qui
lance le skill correspondant (tri de sources, génération d'un lot,
transcription). v1 : la plateforme VPS affiche les messages, et le
skill se lance À CÔTÉ, dans le Claude Code / Codex du joueur sur sa
machine (architecture A4 respectée : le traitement reste local et au
coût du joueur) ; cible : le déclenchement est seamless depuis le
back, sans que le joueur voie la couture. Ce mécanisme REMPLACE le
« relevé mensuel » passif de la parade n°5 du §5 : l'à-sec ne se
constate plus, il interpelle.

**Tout parcours fabriqué est capital** (brief JB) : les domaines, les
fiches, les inventaires de sources, les trous nommés et les coûts
mesurés sont conservés et versionnés — le prochain futur infirmier ou
le prochain gestionnaire copro PART DE L'EXISTANT au lieu de
refabriquer. Nuance de couches, incompressible : la structure d'un
domaine (régions, quiz, inventaire des référentiels PUBLICS) et les
fiches `partage: banque` se réutilisent telles quelles ; les fiches
`interne` (dérivées d'un support non redistribuable, comme le pack de
cours d'Arthur) restent au joueur qui possède le support — le suivant
récupère la carte du territoire et les trous déjà nommés, pas les
fiches qu'il n'a pas le droit d'avoir.

**Le coût, séparé en deux et dit en face** (pré-mortem B9) : la
**fabrication** d'un domaine (tri de milliers de PDF, génération,
puis la double passe par agent frais qui remonte aux sources — Sonnet
pour l'extraction, Opus pour la vérification) se chiffre en dizaines
d'euros, ponctuels : **les 10 €/mois d'Arthur ne la couvrent pas**,
et aucun abonnement à 10 € n'existe. L'**usage**, lui, coûte ~0 € en
v1 (pas de réponse libre — Q25, mode dégradé jouable — Q44). D'où :
la v1 du domaine d'Arthur est **bornée à ~30 cartes** (Q26 l'autorise
explicitement : une boucle complète vaut mieux que 300 cartes), la
soirée artisanale est une **mesure chiffrée** (tokens et euros
relevés), et un GO/NO-GO écrit suit la mesure **avant** d'annoncer un
coût récurrent à Arthur. Aucune promesse de prix avant la mesure.

**Le droit des sources, dit une fois pour toutes** : pas de scraping
de sites de cours (ni robot qui « sort le cours » d'un site — l'idée a
été évoquée en séance, elle est écartée : conditions d'utilisation +
droit d'auteur) ; les cours PDF d'année 1 obtenus par une connaissance
sont l'équivalent de la couche `interne` de JB — utilisables pour
DÉRIVER des cartes paraphrasées et sourcées dans le repo source
d'Arthur, jamais redistribués, jamais poussés au serveur tels quels.
Les référentiels publics (annales officielles, HAS, Santé publique
France) sont la voie sûre, comme AQC/ANIL/Légifrance côté copro.

**Interdiction propre au domaine santé** (pré-mortem B14 — art. 9
RGPD) : **aucune donnée patient réelle, aucune photo clinique non
publiée sous licence** n'entre dans une banque, quelle que soit la
couche — les tracés ECG, photos de plaie et cas patient (Q23-24)
viennent de banques pédagogiques publiées ou sont fictifs. Le scanner
anti-fuite (calibré copro) ne peut PAS détecter une donnée de santé :
la barrière est (1) cette règle écrite, reprise à l'étape 4 du guide
d'agent, et (2) le contrôle mécanique à la réception — le contrat
exige déjà `image.licence`, une image sans licence est refusée.

## 5. Sécurité, RGPD, exploitation

- **Auth** : magic links par mail (pas de mot de passe stocké) ;
  comptes créés uniquement sur invitation envoyée à la main. Trois
  précisions qui la rendent réelle (pré-mortem B13) : (1) **personne
  n'envoie de mail aujourd'hui** — l'infra n'a ni SMTP ni fournisseur
  transactionnel, et un envoi direct depuis le VPS sans SPF/DKIM
  finit en spam : O6 choisit un fournisseur d'envoi (coût dit) et
  l'inscrit au registre **comme sous-traitant RGPD** ; (2) le magic
  link ne sert qu'à l'**inscription et aux nouveaux appareils** —
  ensuite un cookie de session longue durée (≥ 1 an) : l'ouverture de
  8h15 ne dépend JAMAIS d'un mail (parade « zéro friction ») ; (3)
  repli écrit si le mail ne part pas : JB peut générer un lien
  d'accès à la main pour un joueur connu.
- **Étanchéité d'hébergement** : vhost + domaine **ou sous-domaine**
  dédié sur le VPS actuel (le sous-domaine suffit et Caddy fait le
  certificat seul — pas d'achat obligatoire), process et utilisateur
  système séparés, racine servie hors du clone wiki-copro. Le produit
  ne peut pas lire `outputs/` ni `coulisses/` par construction. (Une
  migration d'hébergeur plus tard reste une copie de fichiers +
  SQLite.)
- **Le RGPD ne commence pas à M9, il a déjà commencé** (pré-mortem
  B15) — arbitrage JB du 29/08 au soir : Arthur est du cercle
  familial (« comme mon frère »), la formalité d'information est
  levée pour LUI, JB assume et le dit de vive voix ; pas de
  pseudonymisation du dépôt. Le préalable M9 côté PRODUIT est
  inchangé : registre à
  jour, base légale, durée de conservation, **suppression de compte
  sous 48 h** (DELETE SQLite + retrait des banques reçues — possibles
  parce que ni l'état ni les banques de joueurs ne sont dans git,
  invariants 3 et 5).
- **Vie privée du carnet d'erreurs** : exclu de la visibilité amis
  (§3) — écrit ici pour être opposable.
- **Maintenance bicéphale** (question ouverte n°5 du pré-mortem du
  29/08, tranchée) : le contrat carte-v1 et le valideur vivent dans
  le repo produit et y sont versionnés ; wiki-copro les CONSOMME
  (copie taguée, jamais de fork silencieux). Un bug moteur se corrige
  côté produit d'abord, wiki-copro se met à jour au tag suivant.
- **La preuve que les garde-fous ne tiennent pas tout seuls, datée** :
  le pré-mortem du 29/08 a trouvé DANS le front servi un podium de
  cinq collègues réels nommés avec des métriques inventées
  (`ProfilsErpConnector` / `PodiumLeaderboard` / `ManagerPassportCard`,
  maquettes du 28-29/08) — exactement l'écran que le §9 interdit.
  Retiré le jour même (profils fictifs, rebuild ; FILE-ALERTES du
  29/08). C'est l'argument concret des mécanismes de M11 : une règle
  écrite dans un dépôt privé n'empêche rien, seul le mécanisme
  empêche.
- **Ce qui peut tuer le produit, et la parade en face de chaque mort**
  (pré-mortem de Claude, en attendant ceux de JB et Arthur — Q52) :
  1. le rituel de JB casse avant M9 → les gates existent pour ça : on
  gèle M9-M11, on répare le format, le produit perso continue ;
  2. la soirée artisanale révèle qu'un domaine coûte 10× l'espéré →
  le GO/NO-GO chiffré du §4 a lieu AVANT toute promesse à Arthur, et
  le repli est un domaine v1 réduit (30 cartes, boucle complète) ;
  3. la banque d'Arthur se remplit de cartes fausses parce que la
  double passe a été « allégée pour aller vite » → le statut
  `brouillon` bloque côté moteur (Q49), ce n'est pas une discipline,
  c'est le valideur ;
  4. le front extrait de l'ERP prend 5 sessions au lieu d'une et
  l'élan meurt dans la plomberie → l'inventaire des 16 composants
  (O6, entrée de chantier) chiffre AVANT d'ouvrir, et le chantier ne
  s'ouvre pas sans ce chiffrage ;
  5. personne ne publie de livraison après le premier mois et le
  produit est à sec en silence → **l'agent-compagnon** (§4) : l'à-sec
  interpelle le joueur dans l'app et propose le skill de relance —
  il ne se constate plus a posteriori.

## 6. Ce que ça change aux chantiers M9-M11 (la ROADMAP reste la carte)

- **M9 (extraction)** : les quatre briques « à nommer » sont
  nommées — auth = magic links ; hébergement = VPS actuel, vhost
  dédié, payeur JB (assumé, brief) ; clé tiers = supprimée (aucun
  appel IA serveur pour un tiers) ; flux fournisseur→produit = push
  volontaire + contrat versionné côté produit. Le coût d'extraction
  du front reste **à chiffrer en ouverture** (acquis pré-mortem).
  S'ajoute à M9 : SQLite + migration du journal JB (import), et le
  quiz de positionnement (il faut l'onboarding avant le premier
  compte tiers).
- **M7 (l'écran de progression) : réécrit** — l'arbre de compétence
  devient la **carte-monde de régions + boss-examens** du §3
  (BLUEPRINT §9 amendé). `SkillTree.jsx` (le composant actuel) est
  une maquette périmée par ce choix : il figure à l'inventaire « ce
  qui survit / ce qui se jette » d'O6, il ne se prolonge pas.
- **M10 (usine)** : redéfini §4 — un kit local guidé, pas un service.
  v1 artisanale avec Arthur, le guide d'agent en dérive.
- **M11 (social)** : garde-fous inchangés ; le carnet d'erreurs y est
  explicitement hors visibilité. À noter : plusieurs composants du
  front actuel (arène de défis, duels, podium) implémentent des bouts
  de M11 **avant son gate** — ce sont des maquettes, pas le chantier ;
  l'inventaire d'O6 tranche leur sort.
- **M2 gagne une brique venue de M8** (pré-mortem B1/B2) : le chemin
  d'écriture d'une révision — sans lui, `revues.jsonl` n'existe pas
  et AUCUN gate n'est mesurable. Détail : O1b au §7.
- **Les gates ne bougent pas** : rien de M9+ ne se CONSTRUIT avant le
  gate du rituel (bilan ~30 séances + 4 semaines à ≥4 séances/sem) —
  gate **mesurable seulement à partir du jour où O1b est posé**.
  Penser, spécifier, trier des sources n'est pas construire.

## 7. Le plan d'orchestration (les sessions Opus, dans l'ordre)

Routage modèle (CLAUDE.md) : **Opus** pour tout ce qui suit ; Sonnet
pour les sous-agents mécaniques (extraction, moissons) ; Fable jamais
par défaut. Chaque session : annoncer sa prise dans
`outputs/PORTEFEUILLE/FILE-ALERTES.md`, committer par chemins
explicites, `python3 tooling/examen.py` vert avant « fait » (il
inclut `app/tests.py`).

| # | Session | Charge en ouverture | Fini quand | Gate |
|---|---|---|---|---|
| O1a | **La banque au runtime** : le front lit `banque.json` par fetch, plus d'import de build (M2 reste n°1) | ROADMAP M2, `erp/react/src/**` (accroches listées M9), `academie/site/` | La séance servie change après le timer VPS, sans rebuild React | Aucun — priorité absolue |
| O1b | **Le chemin d'écriture d'une révision — il n'existe PAS aujourd'hui** (pré-mortem B1 : aucun localStorage, aucun appel réseau, `revues.jsonl` jamais créé ; les XP du front sont des valeurs en dur). Brique minimale sortie de M8 : localStorage + export JSON, ou route back par lots (le pattern jeton Bearer de R10 existe, `erp/app/serveur.py`) — écrire le contrat client pour que le passage à SQLite (M9) ne le change pas | ROADMAP M2/M8, `app/seance.py`, `erp/app/serveur.py` | **Une réponse jouée par JB le matin est relisible dans le journal le soir.** Sans O1b, aucun gate (M4, M9) n'est mesurable | Aucun — même priorité qu'O1a |
| O2 | **Finir M1** : lots équipements + procédure (`banque/procedure/` est vide, `banque/equipements/` n'existe pas), pilote pathologie AQC, rendu HTML de relecture, et `export_anki.py` (assurance-vie de réversibilité du CONTRAT §4 — pas un livrable joueur) | CONTRAT-CARTE-V1, CORPUS, `banque/` | **+30 cartes sur équipements et procédure, 0 carte `brouillon` restante** (3 au 29/08), JB a relu 20 cartes en HTML sans erreur | Aucun |
| O3 | **Finir M2** : registre RGPD (profil JB), écran de séance FSRS côté React | ROADMAP M2, `meta/2026-08-24-registre-traitements-rgpd.md`, `app/seance.py` | 7 séances réelles de JB sans lancement manuel | Aucun |
| O4 | **Le tri des sources d'Arthur** (cadrage, pas construction — autorisé avant tout gate) : inventaire de ses PDF, test de santé façon NotebookLM, liste virer/garder/télécharger, inventaire des référentiels publics du concours FPC IFSI (épreuve mars/avril 2027). Clôture : son premier lot de ~30 cartes `brouillon` au contrat carte-v1, prêtes pour la double passe — elles se jouent SUR L'APP dès que son compte existe | Ce fichier §4, `NOTEBOOKLM-A-RETIRER.md` (le modèle du geste), les documents qu'Arthur fournit | Arthur a sa liste triée, l'inventaire des sources fiables de sa première région, et un premier lot de cartes au contrat | Aucun (formalité RGPD envers Arthur levée par JB, §5) ; session locale avec ses fichiers, sur sa clé si possible |
| O5 | **M3 → M8 dans l'ordre de la ROADMAP** — avec les amendements du soir : M6 = copier-coller pour tous en v1 (§2) ; M7 = carte-monde + boss-examens (§3), plus d'arbre ; M8 = la sync vise le contrat client posé en O1b, cible SQLite à M9. L'arbitrage 4 du 29/08 reste : la réponse libre v1 peut avancer au gate de M4, jamais avant | ROADMAP (chaque M), ce fichier §3 | Leurs fini-quand, amendés pour M6/M7/M8 | Gate M4 = bilan ~30 séances (mesurable grâce à O1b) |
| O6 | **M9 : l'extraction** — EN OUVERTURE : l'inventaire « ce qui survit / ce qui se jette » des **16 composants** `components/academie/` (~5 200 lignes ; podium, duels, arène et `SkillTree` sont des maquettes, plusieurs implémentent M11 avant son gate) — c'est CE chiffrage qui autorise le chantier. Puis : repo produit, front hors châssis ERP, SQLite, magic links + fournisseur de mail (sous-traitant au registre), vhost, **réception des livraisons** (jeton, re-validation, quarantaine — §2 inv. 3), migration profil JB, quiz de positionnement | Ce fichier §2 §5 §6, ROADMAP M9 | JB joue sur la nouvelle adresse, historique intact, scanner + relecture prouvent zéro fuite | Gate M9 (rituel tenu, mesuré au journal d'O1b) + les « reste dû » RGPD/pré-mortem de la Partie 4 |
| O7 | **M10 : la soirée artisanale puis le kit** — étape 0 : installation du runtime chez Arthur (§4) ; génère son domaine avec lui, mesure le coût, GO/NO-GO, en dérive le gabarit de repo source + guide d'agent | Ce fichier §4, ROADMAP M10 | Arthur joue sa première séance sur un domaine que JB n'a pas écrit ; le kit rejouerait la soirée ; le coût réel est écrit | Après O6 |
| O8 | **M11 : amis, visibilité, défis** (carnet d'erreurs exclu de la visibilité, §3) | Ce fichier §3, ROADMAP M11 | JB et Arthur se voient avancer, un défi joué et comparé | Après O7 |

O1a, O1b, O2 et O3 peuvent s'enchaîner dès maintenant ; O4 est
parallélisable dès l'information RGPD d'Arthur faite. O6+ attendent
leurs gates — c'est la discipline qui a déjà sauvé ce chantier trois
fois (pré-mortems des 28 et 29/08, matin et soir).

**Le calendrier, calé sur la seule date dure** (mise à jour 29/08 au
soir, réponse de JB) : **l'épreuve d'Arthur est en mars/avril 2027**,
soit ~7 mois. Le plancher technique (journal O1b → ~30 séances ≈ 6-7
semaines → +4 semaines de rituel → O6 puis O7 ≈ ~3 mois avant
qu'Arthur joue) **tient dans ce délai avec de la marge** : Arthur
joue sur l'app, pas sur un détour (arbitrage JB : « arrête de me
parler Anki, le but c'est construire l'app » — l'export Anki reste au
contrat comme assurance-vie de réversibilité, il n'est le livrable de
personne). La marge n'autorise pas la flânerie : chaque mois de
retard sur O1-O3 mange la piste de révision d'Arthur avant l'épreuve.

**Le GO socle du 29/08 au soir** (second brief JB : « créer les
bases, les règles, les tests, les coquilles vides, les squelettes —
en mode orchestrateur ») : la construction du **socle
domaine-agnostique** est lancée sans attendre — moteur de progression
carte-monde (`app/progression.py`), quiz de positionnement
(`app/quiz.py`), carnet d'erreurs (`app/erreurs.py`), gabarit de
domaine (`gabarit-domaine/`), leurs règles dans `academie.json` et
leurs tests. Ce socle sert JB dès M2/M7 et sera extrait tel quel en
M9 : il ne viole pas les gates (qui portent sur le produit
multi-joueurs servi, pas sur le moteur), et c'est un ordre explicite
de JB, décideur des gates.

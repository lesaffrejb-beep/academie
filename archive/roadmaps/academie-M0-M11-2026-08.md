# ARCHIVE — Académie M0-M11 (août 2026)

> Archive de conception non pilotante depuis le 30/08/2026. La roadmap active
> est `../../ROADMAP.md`. Les états et chemins ci-dessous sont conservés comme
> trace des décisions et peuvent décrire l'ancien couplage avec ERP.

Écrite le 28/08/2026, révisée le même jour (second brief JB : nom
« L'Académie », ateliers ajoutés) puis RÉPARÉE après le pré-mortem par
agent frais du 28/08 (19 bloquants — rapport et réparations :
[`travail/relecture-2026-08-28-cadrage.md`](travail/relecture-2026-08-28-cadrage.md)).
Le produit est imaginé dans [`BLUEPRINT.md`](BLUEPRINT.md) (à lire
d'abord) ; ici les chantiers, dans l'ordre, chacun avec son « fini
quand ». Convention identique à la roadmap ERP (`erp/site/ROADMAP.md`) :
chantiers numérotés M*, une session reprend le flambeau sans rien
deviner. **M1 et tout ce qui suit ne démarrent qu'après le GO de JB
sur les arbitrages du BLUEPRINT §13** (formulation durcie au
pré-mortem : le GO porte sur les arbitrages, pas seulement sur l'envie
de commencer).

Règles transverses du repo qui s'appliquent à tout chantier M* :
banque de cartes anonyme (zéro fait copro nommé), toute carte sourcée
et datée (règle dure 3), `python3 tooling/examen.py` VERT avant de dire
« fait », commit par chemins explicites (sessions parallèles). Deux
conventions de lecture des chantiers : **« taille »** = sessions de
construction ; **« fini quand »** peut exiger en PLUS un délai
calendaire (des séances réelles de JB) — les deux ne se confondent
pas, un chantier peut être construit en deux sessions et validé trois
semaines plus tard. Troisième convention (29/08) : quand un chantier
porte un bloc d'avancement (« FAIT », « EN COURS ») ET un bloc
« (cadrage d'origine) », **le bloc d'avancement fait foi** ; le
cadrage d'origine reste pour mémoire, ses « fini quand » compris
seulement s'ils n'ont pas été remplacés.

## Révision du 29/08/2026 — L'Académie devient un produit autonome

Brief JB du 29/08 + quatre arbitrages rendus le même jour. Le cap
change en fin de trajectoire, pas au début : **hard focus sur JB
d'abord** (M1 à M8 inchangés), mais tout se construit dès maintenant
pour que le produit soit **déployable à d'autres ensuite**.

La vision élargie : l'Académie est **un produit à part entière, sur sa
propre adresse, dans son propre dépôt** — séparé du repo wiki-copro,
qui n'est plus que le fournisseur de contenu du domaine « copropriété »
de JB. Un ami (collègue gestionnaire, infirmier, sage-femme…) s'y
connecte, branche sa propre source documentaire (son NotebookLM, ses
documents), et l'IA lui génère son parcours complet : skill tree,
niveaux, cartes, QCM, exercices. Chacun avance dans son domaine et les
amis se voient avancer. JB garde un accès rapide depuis son ERP (un
simple lien vers la nouvelle adresse, rien de l'ERP n'est visible des
autres).

Les quatre arbitrages du 29/08 :

1. **Visibilité entre amis : totale.** Skill tree complet, heures de
   jeu, notions apprises, tout est visible des amis ajoutés — et ça
   ouvre les **défis** (un ami peut défier l'autre sur une notion).
   Nuance conservée du §9 : la transparence est *entre amis choisis* ;
   jamais d'usage managérial, jamais de profil lisible par un
   employeur.
2. **Nouveaux domaines : l'IA fait tout.** L'arrivant branche son
   NotebookLM ou dépose ses documents ; la génération du parcours
   (arbre, découpage en niveaux, cartes, QCM) est automatique, sans
   passer par JB. Le circuit qualité (brouillon → validation) reste,
   mais c'est l'arrivant qui valide son propre contenu.
3. **Coût de l'IA : chacun le sien.** Chaque joueur branche sa propre
   clé API. JB ne paie jamais l'IA des autres. Deux précisions posées
   au pré-mortem du 29/08 : (a) la piste « son propre abonnement »
   (Claude via Claude Code, Codex, Antigravity) est `[À VÉRIFIER]` —
   ces produits n'exposent pas d'endpoint qu'une app web peut appeler
   pour l'utilisateur, ce n'est pas une option d'architecture tant que
   ce n'est pas prouvé ; (b) l'INFRA (VPS, domaine, certificat) reste
   payée par quelqu'un — aujourd'hui JB — et « qui paie l'infra d'un
   produit multi-comptes » est un arbitrage M9, pas un acquis. Le
   stockage de la clé d'un tiers est un sujet de sécurité à part
   entière (M9 : jamais en clair, jamais dans un repo, conception à
   part).
4. **Ordre des modes d'exercice : la science décide** (arbitrage JB :
   « fais ce qui fait le plus apprendre d'abord »). Le
   CADRAGE-SCIENTIFIQUE est clair : la récupération effortful (rappel
   libre et indicé, g = 0.50-0.70) bat la reconnaissance (QCM
   simples). Conséquence sur la roadmap, PRÉCISE pour qu'une session
   qui reprend sache trancher : la **réponse libre v1** (rappel libre
   corrigé par LLM avec source citée, copier-coller sans
   infrastructure) peut être avancée **au même gate que M4** (le bilan
   des ~30 séances passé), avant M4/M5 si JB le préfère ; le jeu de
   rôle et la v2 restent à leur place (M6). Rien ne passe AVANT le
   gate : « dès que le rituel tient » = le gate, pas une impression.
   Les QCM existants restent valides (distracteurs expliqués =
   discrimination, pas reconnaissance simple), mais le mix de séance
   penche vers la génération de réponse. Le coût LLM récurrent d'une
   correction par carte (le mode devient dominant) se chiffre au
   moment d'avancer la v1, pas après.

Traduction en chantiers : M9 et M10 sont **réécrits** ci-dessous
(produit autonome + onboarding domaine par IA), et M11 (couche
sociale : amis, visibilité, défis) s'ajoute. L'ordre reste M1→M8
d'abord : rien de tout ça ne se construit avant que le rituel de JB
tienne (gate des ~30 séances).

**Complément du 29/08 au soir** : la séance de réponses JB × Arthur a
eu lieu (`CADRAGE-PRODUIT.md` Partie 4) et la spec en est dérivée :
[`SPEC-PRODUIT.md`](SPEC-PRODUIT.md) — elle précise les briques que
M9-M11 laissaient ouvertes et **fait foi sur ces points** : modèle A4
(un repo source par joueur, JB porte l'infra), aucun appel IA côté
serveur pour un tiers (la brique « clé tiers » de M9 disparaît),
auth par magic links, SQLite pour l'état, usine à domaine = kit local
guidé (M10), carte-monde de régions avec boss-examens à la place de
l'arbre (BLUEPRINT §9 amendé), quiz de positionnement, carnet
d'erreurs. Le plan de sessions est au §7 de la spec ; les gates
ci-dessous ne bougent pas.

**GO socle du 29/08 au soir** (second brief JB : « créer les bases,
les règles, les tests, les coquilles vides — en mode orchestrateur »,
plus « arrête de me parler Anki, le but c'est construire l'app ») :
le socle domaine-agnostique se construit sans attendre —
`app/progression.py` (carte-monde, XP dérivée, examens de région),
`app/quiz.py` (positionnement), `app/erreurs.py` (carnet d'erreurs),
`gabarit-domaine/` (la coquille d'un nouveau domaine), règles
chiffrées dans `academie.json` (blocs `progression` et `quiz`), tests
dédiés. Date dure enregistrée : **épreuve d'Arthur en mars/avril
2027**. Détail : SPEC-PRODUIT §7 (fin de section).

## Le risque numéro un, nommé avant de construire

Ce produit ne meurt pas d'un bug, il meurt d'un matin où JB ne l'ouvre
pas, puis d'un deuxième. Quatre parades structurelles, prises dès M2 :

1. **Zéro friction d'ouverture** : une URL, la séance déjà générée
   (Routine cloud 7h00 + timer de pull VPS, la chaîne complète est
   dans M2), prête en moins de 5 secondes, jouable même si la
   génération du matin a raté (repli sur la veille).
2. **Point de bilan à ~30 séances, usage ET savoir** : après un mois
   réel, on regarde les données d'usage (séances faites, abandons en
   cours, modes joués) ET un mini-test de rétention (20 cartes du
   premier lot rejouées à froid, score en clair) — le gate mesure si
   JB apprend, pas seulement s'il clique. On répare le FORMAT avant de
   construire M4 et au-delà.
3. **La séance dégrade bien** : pressé = 5 révisions et sortir (3
   minutes), c'est une séance valide. Une coupure de trois semaines
   (saison d'AG) se résorbe par plafond + ré-étalement automatique
   (BLUEPRINT §4/§8), jamais par une dette affichée. Le produit ne
   culpabilise jamais.
4. **Le neuf ne s'épuise pas en silence** : l'approvisionnement est
   une EXPLOITATION hebdomadaire chiffrée (BLUEPRINT §7 : lot de 15-20
   cartes/semaine, ~une session d'agent, ~10 min de validation JB),
   pas un stock M1 qu'on regarde fondre. Un matin sans neuf reste une
   séance valide (révisions seules).

## M0 — Cadrage — FAIT 28/08/2026

Ce dossier : README, BLUEPRINT (vision, science sourcée, modes,
ateliers, sources, moteur FSRS, arbres, architecture, généralisation),
la présente roadmap, pointeur dans CLAUDE.md, en-tête de la roadmap ERP
clarifié (deux roadmaps désormais : R* = ERP, M* = Académie).
Pré-mortem par agent frais passé le 28/08 (rapport dans `travail/`),
les 19 bloquants réparés dans les deux documents.

- **Fini quand** : JB a lu le BLUEPRINT et rendu les arbitrages du
  §13. ✓ docs / ⏳ arbitrages.

## M1 — Le contrat carte-v1 + la banque d'amorçage — EN COURS depuis le 28/08/2026

**GO donné par JB le 28/08/2026** (arbitrages : BLUEPRINT §12 bis).
Fait dans la foulée, le même soir :

- `CONTRAT-CARTE-V1.md` — le contrat, avec trois décisions qui
  s'écartent du blueprint et disent pourquoi : **JSON** plutôt que
  YAML+md (trois consommateurs, dont le front React, tous stdlib), un
  fichier **par branche** plutôt que par carte, et l'**id immuable**
  (c'est la clé de l'historique FSRS).
- `app/valide_banque.py` — le valideur, **écrit avant la première
  carte** (leçon batiment-v1). Refuse : carte sans source ou sans date,
  QCM sans distracteur expliqué, image sans licence, id dupliqué,
  prérequis fantôme, carte périmée encore `valide`, et tout nom de
  copro réel en couche partagée. Refus testés un par un.
- Deux champs que le blueprint n'avait pas : **`peremption`** (une
  carte de prix meurt toute seule — `energie-socle.md` était déjà
  périmé sans que rien ne le dise) et **`partage: interne`** (les
  supports employeur ne circulent pas comme Légifrance).
- `academie.json` — domaines, quotas et paramètres FSRS vérifiés.

Reste à faire sur M1 : le volume de cartes (en production par agents),
la vérification à la source des `brouillon`, le pilote pathologie AQC,
l'export Anki, et le rendu HTML de relecture pour JB. État réel de la
banque au 29/08 (pré-mortem) : 4 domaines servis (droit 28, compta 11,
pathologie 10, sinistres 10) — les domaines arbitrés **technique des
équipements** et **procédure** sont à zéro, et « sinistres » n'était
pas dans l'arbitrage §12.8 : à rééquilibrer dans les prochains lots.

### M1 (cadrage d'origine)

- **Quoi** : le schéma d'une carte (YAML + markdown : id, domaine,
  branche, type, question, réponse, distracteurs, image, explication
  pédagogique, source, verifie, statut, niveau, prérequis, origine),
  documenté comme un contrat indépendant du métier, **avec son export
  CSV Anki** (réversibilité, BLUEPRINT §2) ; puis **60 à 80 cartes
  d'amorçage irréprochables** (pas 150 médiocres : la qualité est le
  produit ; le rythme de croisière hebdo prend le relais dès M2) sur
  les domaines arbitrés (proposé : pathologie du bâtiment, technique
  des équipements, droit + procédure), tirées de la matière DÉJÀ
  vérifiée du repo (apprentissages-syndic, majorites-ag, références
  erp-juridique / erp-conseil, dépouillements de lab/ — jamais les
  bruts) et des référentiels publics liés (AQC, ANIL, Légifrance ;
  licence vérifiée source par source). Au passage : re-sourcer les
  références scientifiques du BLUEPRINT §3 (DOI/lien + date de
  vérification — la règle des cartes s'applique au blueprint).
- **Qualité** : chaque carte générée par LLM naît `brouillon` ; double
  passe par agent frais qui remonte à la source avant `valide` ;
  échantillon relu par JB (borné : 20 cartes max par lot, jamais une
  relecture de masse). Un valideur mécanique
  (`app/valide_banque.py`) refuse toute carte sans source ou hors
  schéma — leçon du contrat batiment-v1 (dérive mesurée le 26/08 faute
  de valideur) appliquée AVANT la première carte, pas après.
- **Fini quand** : le valideur passe sur toute la banque, 0 carte sans
  source, et JB a joué 20 cartes **rendues en HTML minimal** (jamais
  du .md brut : doctrine CLAUDE.md, on ne demande pas à JB de relire
  du markdown) sans y trouver une erreur. **Taille : une à deux
  sessions.**

## M2 — Le moteur v1 — LARGEMENT FAIT le 28/08/2026

Construit le soir même du GO, dans la foulée de M1 :

- **`app/planificateur.py`** — FSRS-6 porté en stdlib. Arbitrage tranché
  (le blueprint le laissait ouvert) : **portage plutôt que dépendance**,
  parce que la séance est servie par le VPS et qu'une dépendance de plus
  est un maillon qui peut manquer à 7 h. Les formules et les 21
  paramètres sont **repris de `py-fsrs`, lus, jamais écrits de mémoire**.
- **`app/tests_planificateur.py`** — compare le portage à `py-fsrs` sur
  6 séquences réelles (conforme au 10⁻⁴), et tourne **aussi sans elle**
  grâce aux valeurs figées, plus 6 invariants (un raté n'allonge jamais
  l'intervalle, dur ≤ bien ≤ facile, difficulté bornée sous 30 ratés).
- **`app/seance.py`** — la séance du jour : révisions dues, plafond de
  reprise, ré-étalement de l'arriéré, entrelacement des domaines, et le
  journal `etat/<profil>/revues.jsonl` append-only. **L'état se
  recalcule intégralement depuis le journal**, jamais stocké : on peut
  changer les paramètres FSRS ou corriger le moteur sans perdre
  l'historique, et deux appareils fusionnent par union horodatée.
- **`app/tests_seance.py`** — 7 tests qui protègent les promesses, pas
  le code : une carte `brouillon` n'est jamais servie, une ratée revient
  avant une sue, l'arriéré ne s'affiche jamais en dette, un journal
  corrompu est ignoré.
- **La chaîne du matin** — `tooling/back-deploy/academie-maj.{service,timer}`
  + `installe-academie.sh`. Timer systemd, 6h50 du lundi au vendredi,
  bornée à la banque de l'Académie. **Reste à lancer une fois** :
  `bash tooling/back-deploy/installe-academie.sh` (demande l'accès SSH
  au VPS, donc une session locale ou JB).

**Simplification assumée par rapport au cadrage** : le blueprint
prévoyait une routine cloud générant *la séance* à 7 h. Inutile — la
séance se COMPOSE à l'ouverture depuis la banque et le journal du
profil. Il suffit que la banque soit à jour. Un maillon fragile de
moins, et le pire cas devient « la banque d'hier » au lieu d'une page
blanche.

Reste sur M2, dans l'ordre :

0. **Le chemin d'écriture d'une révision n'existe pas** (pré-mortem du
   29/08 soir, B1 : aucun stockage local, aucun appel réseau,
   `revues.jsonl` jamais créé — JB n'a jamais pu enregistrer une
   révision, donc aucun gate n'est mesurable). Brique minimale sortie
   de M8, spécifiée en SPEC-PRODUIT §7 (O1b). Fini quand : une
   réponse jouée le matin est relisible dans le journal le soir.
1. **Le dernier maillon de la chaîne du matin est CASSÉ** (pré-mortem
   du 29/08, bloquant n°1 — le n°4 du 28/08 n'était réparé que sur le
   papier) : le timer VPS régénère `academie/site/banque.json`, mais
   l'écran que JB joue est le React de l'ERP, qui consomme
   `erp/react/src/data/academie-banque.json` **à la compilation**
   (import de build). Sans rebuild React + sync `erp/site/`, la
   séance servie ne bouge jamais. Réparation à arbitrer au chantier :
   faire lire `banque.json` **au runtime** (fetch) par le front —
   préférable, un maillon de moins — ou étendre le timer au rebuild.
   Tant que ce maillon n'est pas posé, le « fini quand » de M2 est
   inatteignable et la parade « zéro friction » ne tient pas.
2. Le registre RGPD avant la première écriture réelle de
   `revues.jsonl`.
3. L'écran de séance côté React (le composant lit aujourd'hui la
   banque, pas encore la séance FSRS).

### M2 (cadrage d'origine)

- **Quoi** : `app/genere.py` (même famille que `erp/app/genere.py`)
  assemble « la séance du jour » en page statique : révisions dues
  (FSRS, paramètres par défaut, sur `etat/<profil>/revues.jsonl`), une
  leçon nouvelle, modes Flash + QCM (l'écran d'ouverture est un menu
  simple tant qu'il n'y a que deux modes — la « machine à sous »
  attend M4). La clôture avec compteur cumulé. Thème nuit Sergic
  (tokens dérivés du front ERP). Plafond de reprise + ré-étalement
  d'arriéré + mode vacances (BLUEPRINT §4/§8) dès cette v1 : la saison
  d'AG arrive vite.
- **La chaîne du matin, maillon par maillon** (réparée au pré-mortem :
  la version initiale promettait un VPS à jour que rien ne mettait à
  jour) : Routine cloud à 7h00 lun-ven (AVANT la routine « Feuille de
  route du matin » de 7h30, sans la toucher) qui génère et pousse sur
  main ; **timer de pull côté VPS** (systemd : `git pull` +
  régénération bornée à `academie/site/`) — la seule brique d'infra
  nouvelle, GO JB requis (§13.8) ; repli documenté si un maillon casse
  (séance de la veille jouable, révisions recalculées côté client).
  Dépendances FSRS déclarées dans `tooling/requirements/` (ou portage
  pur Python, arbitrage au chantier — BLUEPRINT §8).
- **Avant la première écriture de `revues.jsonl`** : inscrire les
  traitements nouveaux au registre RGPD
  (`meta/2026-08-24-registre-traitements-rgpd.md`) — données
  d'apprentissage d'un salarié, lien carte↔copro (`contexte.jsonl`),
  pointeurs d'ateliers ; règle de lecture des profils gravée
  (BLUEPRINT §9 : propriétaire seul, jamais d'usage managérial).
- **L'exploitation démarre ici** : premier lot hebdo de cartes
  (rythme §7 du BLUEPRINT), fil du réel v0 rédigé à la main dans le
  lot (le digesteur attendra M5).
- **Fini quand** : construction = la chaîne complète tourne (génération
  7h00 → pull VPS → séance servie) ; validation (calendaire, ~2
  semaines après) = 7 séances réelles de JB SANS lancement manuel, et
  les cartes ratées un jour reviennent bien aux échéances FSRS.
  **Taille : deux sessions de construction + le délai de validation.**

## M1-bis — Capter Immocampus (le portail de formations de l'employeur)

> Placé ici dans le fil de lecture, mais son ordre réel est dit
> ci-dessous : après le pilote pathologie AQC de M1, pas après M2. Ce
> n'est PAS « le chantier suivant ».

- **Pourquoi ce chantier existe** : signalé par JB le 28/08/2026, ce
  portail SharePoint comble **exactement les deux trous majeurs** du
  CORPUS §2.3 — Replay Pathologie des bétons, Pathologie des balcons,
  Technique du bâtiment, Réussir une visite technique — plus une
  couverture large du droit, de la compta et de la procédure
  (inventaire complet : CORPUS §2.5).
- **Quoi** : (1) chiffrer avant de lancer — c'est un chantier, pas un
  scraping : pages SharePoint authentifiées, replays en vidéo, donc
  export puis transcription puis dépouillement ; (2) travail **depuis
  le poste local** (SharePoint ne se lit que de là, `cabinet.yaml`) ;
  (3) toute carte qui en dérive est une **paraphrase**, jamais une
  recopie, et naît en `partage: interne`.
- **Ordre** : après le pilote pathologie AQC de M1, qui aura donné le
  coût réel d'une carte de domaine visuel — on saura alors si capter
  Immocampus est moins cher que sourcer du public, ou l'inverse.
- **Fini quand** : un replay technique est transcrit, dépouillé, et a
  produit au moins 10 cartes `interne` validées. **Taille : à chiffrer
  au démarrage, la transcription est l'inconnue.**

## M3 — Les ateliers v1 : lire, analyser, corriger

- **Quoi** (BLUEPRINT §6) : les fiches de méthode (« comment lire un
  arrêt », « comment lire une annexe comptable », « la grille d'un
  devis ») + les trois premiers types d'atelier : **Auditer un devis**
  (proposé en premier), **Lire un arrêt** (Judilibre/Légifrance,
  textes publics, partageable), **Lire un bilan / une annexe** (grille
  erp-comptable). `app/atelier_prep.py` tourne en session LOCALE
  (le serveur ne se lit que du poste Windows) : une pièce réelle déjà
  convertie → un atelier dans `etat/<profil>/ateliers/` qui POINTE la
  pièce (jamais de copie — frontière reçu/produit). Stock cible : 3-4
  ateliers d'avance. Le « texte du bac » (philo/socio/urbanisme) entre
  ici comme quatrième type, cadence libre.
- **Règles** (durcies au pré-mortem) : le .md converti vaut la pièce
  (jamais reconverti ; re-OCR seulement pour une pièce jamais
  convertie) ; la pièce se choisit parmi les dossiers que JB n'a PAS
  traités lui-même, et le corrigé est produit et VALIDÉ (double passe,
  circuit carte) AVANT l'atelier — un corrigé non validé = l'atelier
  ne sort pas (BLUEPRINT §6.6) ; tout atelier se clôt par 2-3 cartes
  extraites qui entrent en rotation FSRS ; les révisions dues ne
  sautent jamais un jour d'atelier (compressées à 5) ; les ateliers
  sur pièces réelles n'entrent JAMAIS dans la distribution collègues.
- **Fini quand** : JB a fait un atelier devis complet (lecture,
  questions, corrigé validé, cartes extraites) sur un vrai devis du
  portefeuille qu'il n'avait pas traité, et un atelier arrêt sur une
  décision réelle. **Taille : deux sessions (une pour le cadre +
  devis, une pour arrêt + annexe) + les séances réelles.**

## M4 — Les modes visuels

- **Quoi** : photo-diagnostic (façon Tinder), relier, datation de
  façade — et avec eux le tirage au sort du menu qui devient une vraie
  machine à sous (4+ modes). La banque d'images : par défaut photos en
  couche PERSONNELLE ; une photo ne monte en banque partagée
  qu'anonymisée (cadrage serré sur le détail technique, aucune
  adresse, plaque, visage, rien d'identifiable) ET validée une à une
  par JB (BLUEPRINT §7) ; complétée par Wikimedia Commons / sources CC
  et des photos produites exprès. Chaque image porte sa licence et son
  crédit dans la banque.
- **Le verrou images est mesuré** (pilote du 28/08/2026, CORPUS
  §2.6 ter) : l'AQC interdit la reproduction de ses photos ET de ses
  schémas ; Wikimedia Commons ne porte que 150-200 fichiers non curés
  sur tout le domaine, dont aucun n'est légendé par un professionnel.
  **Le sourcing externe ne lèvera pas ce verrou.** Les deux voies
  restantes, à arbitrer par JB avant d'ouvrir M4 : les ~201 photos de
  VT du parc (anonymisées, légendées par JB — elles portent le bâti
  qu'il visite vraiment), ou des schémas SVG dessinés par nous depuis
  les mécanismes décrits par l'AQC. Quatre cartes du pilote portent
  déjà la description de ce qu'un schéma devrait montrer.
- **Fini quand** : une séance peut être 100 % visuelle sur la
  pathologie, et l'exemple canon du brief est jouable (une souche en
  toiture : cheminée ou ventilation primaire ?). Vérifié au pré-mortem
  du 29/08 : la carte de texte « souche » n'existe PAS encore dans la
  banque (contrairement à ce que cette roadmap affirmait) — elle est à
  produire avec l'image.
  **Taille : une à deux sessions.** **Gate d'entrée : le bilan des ~30
  séances (usage + rétention) est passé et les leçons intégrées.**

## M5 — La boucle terrain et actualité

- **Quoi** : `app/digesteur.py` — (1) la file d'alertes / la veille
  R14 d'hier → proposition de carte du lendemain, ou d'atelier « Lire
  un texte nouveau » quand le document le mérite ; (2) les JOURNAL et
  les questions que JB pose à Claude → détection de lacunes → cartes
  `brouillon` ; (3) le rituel de sortie de réunion dicté par JB
  lui-même (« je n'ai pas su répondre à X », sa parole à lui). **Pas
  de scan des transcriptions de réunions** (arbitrage §12.10 : la
  parole des tiers n'est pas à JB de la donner) sauf décision
  contraire explicite de JB en connaissance de cause. Tout passe par
  le statut `brouillon` + validation M1, rien n'entre en jeu tout
  seul. Anonymisation vérifiée mécaniquement (le scanner anti-fuite du
  générateur démo R16 sert de modèle : slugs OFF-, ICS, noms de copros
  → refus d'écrire).
- **Fini quand** : une alerte de veille réelle est devenue une carte
  jouée le lendemain matin, et une lacune détectée dans un JOURNAL a
  produit une carte que JB a validée. **Taille : deux sessions.**

## M6 — Réponse libre et jeu de rôle

> Amendé le 29/08/2026 au soir (SPEC-PRODUIT §2) : **un seul chemin
> LLM en v1, le copier-coller, pour tous les joueurs JB compris** —
> la « clé D20 côté serveur pour le profil JB » ne se construit pas ;
> l'appel navigateur avec clé locale est `[À VÉRIFIER]` et hors v1.

- **Quoi** : mode réponse libre (JB écrit ou dicte, correction LLM
  adossée aux sources de la carte) et mode jeu de rôle (prompt prêt à
  copier dans une conversation Claude dédiée : le chauffagiste et son
  P2, le président de CS remonté, le commissaire de justice qui
  explique le référé). v1 sans infrastructure (copier-coller). v2 via
  le back, **corrigée le 29/08 pour suivre l'arbitrage 3** : la clé
  D20 côté serveur ne vaut que pour le profil de JB tant que le
  produit est mono-joueur ; dès qu'il y a d'autres joueurs (M9+),
  chaque appel LLM part sur la clé DU joueur, jamais sur une clé
  mutualisée de JB. La v1 réponse libre peut être avancée au gate des
  ~30 séances (arbitrage 4, voir la révision du 29/08 en tête).
- **Fini quand** : un jeu de rôle complet joué et débriefé, et une
  réponse libre fausse corrigée AVEC la source citée. **Taille : une
  session (v1).**

## M7 — La carte-monde + le bilan (réécrit le 29/08/2026 au soir)

> L'arbre de compétence devient la **carte-monde de régions à
> conquérir** (séance JB × Arthur ; mécanique complète et formule de
> remplissage : SPEC-PRODUIT §3 ; BLUEPRINT §9 amendé). `SkillTree.jsx`
> est une maquette périmée par ce choix — inventaire O6.

- **Quoi** : l'écran carte-monde par domaine (régions remplies par la
  stabilité FSRS mesurée au journal, seuil d'ouverture ~75 %, liberté
  d'exploration, **boss-examen de région**, brouillard levé région
  par région), le tableau de bord (forces réelles, lacunes
  persistantes, le carnet d'erreurs et ses raisons récurrentes), le
  bilan mensuel généré par agent — la réponse complète au « dans 6
  mois j'ai rien appris ? » du brief. Règle de lecture des profils
  appliquée (§9 : propriétaire seul jusqu'à M11).
- **Fini quand** : la carte montre au moins un domaine avec des
  régions ouvertes et fermées d'après des données réelles de
  révision, un boss-examen a été joué, et un premier bilan mensuel
  est produit. **Taille : une à deux sessions.**

## M8 — Mobile : PWA + écriture via le back

- **Quoi** : PWA installable (manifest + icônes, comme R8) et **service
  worker propre à l'Académie** (ce que R8 a explicitement refusé pour
  l'ERP — justifié ici : la séance du jour est figée à 7h00, le
  contenu ne bouge pas sous les pieds du cache) ; révision hors ligne
  (moteur FSRS côté client, file locale) ; sync du `revues.jsonl` via
  une **route dédiée du back** (`POST /api/academie/revues`, écriture
  par LOTS : une séance = un envoi = un commit — le back R10 actuel
  est borné au JOURNAL des copros et committe par écriture, il ne se
  réutilise pas tel quel, on l'étend) — fusion par union horodatée du
  log, pas d'« état courant » à réconcilier.
- **Note du 29/08 au soir** (SPEC-PRODUIT §2, inv. 5) : la brique
  d'écriture minimale est SORTIE de M8 et posée en M2 (O1b) — sans
  elle aucun gate n'est mesurable ; et la cible de stockage devient
  SQLite à M9 : écrire la route de façon à ce que le changement de
  dépôt ne change pas le contrat client.
- **Fini quand** : une séance complète faite sur téléphone hors du
  bureau, et l'état retrouvé ensuite sur le poste. **Taille : deux
  sessions (le service worker et l'extension du back sont deux vrais
  morceaux).**

## M9 — Le produit autonome (réécrit le 29/08/2026)

- **Préalable absolu** (établi au pré-mortem, confirmé par le brief du
  29/08) : l'hébergement actuel ne cloisonne RIEN — basicauth partagé
  sur tout `erp/site`, clone complet du repo (outputs/ et coulisses/
  compris) sur le VPS. M9 est donc l'**extraction** : l'Académie sort
  du repo wiki-copro et devient **son propre dépôt** (moteur FSRS,
  contrat carte-v1, valideur, front, tests — zéro donnée copro), servi
  sur **sa propre adresse** avec ses propres comptes, jamais depuis le
  clone du repo. Le repo wiki-copro devient un fournisseur : il pousse
  la banque « copropriété » de JB (couche banque uniquement, scanner
  anti-fuite au passage) vers le produit. Les ateliers sur pièces
  réelles et la couche `interne` restent dans wiki-copro, jamais
  distribués.
- **Le coût réel de l'extraction, dit en face** (pré-mortem 29/08,
  recompté au pré-mortem du soir : « trois composants » était encore
  faux) : `academie/` n'est PAS isolé — le front vit DANS le React de
  l'ERP (`Academie.jsx` et **16 composants** `components/academie/`,
  ~5 200 lignes avec la vue, `lib/academie.js`, `data/academie.js`,
  plus les accroches dans `App.jsx`, `Barre.jsx`, `Rail.jsx`,
  `Palette.jsx`). Plusieurs sont des maquettes qui implémentent M11
  avant son gate (arène, duels, podium) ou que la carte-monde périme
  (`SkillTree.jsx`). Extraire, c'est reconstruire le front hors du
  châssis ERP (routing, thème, barre), pas déplacer un dossier —
  l'ouverture du chantier commence par l'**inventaire « ce qui
  survit / ce qui se jette »** des 16 (SPEC-PRODUIT §7, O6). La
  taille ci-dessous est donc **à chiffrer en ouverture de chantier**,
  pas promise.
- **Quatre briques que M9 doit NOMMER avant de coder** (aucune
  n'existe aujourd'hui) : (1) l'**authentification** — le seul
  mécanisme du repo est un basicauth à mot de passe PARTAGÉ, inapte à
  des comptes ; brique à choisir et à arbitrer avec JB ; (2)
  l'**hébergement et son payeur** — l'arbitrage 3 dit « JB ne paie
  jamais l'IA des autres », mais le VPS, le domaine et le certificat
  d'un produit multi-comptes, quelqu'un les paie et les maintient :
  arbitrage JB explicite ; (3) le **stockage de la clé API d'un
  tiers** — jamais en clair, jamais dans un repo, conception dédiée ;
  la piste « abonnement » (Claude Code, Codex, Antigravity) reste
  `[À VÉRIFIER]` : pas d'endpoint appelable par une app web connue à
  ce jour ; (4) le **flux fournisseur → produit** — wiki-copro pousse
  la banque « copropriété » : format, fréquence, versionnage du
  contrat carte-v1 des deux côtés, et qui corrige un bug du moteur une
  fois les dépôts séparés.
- **L'accès de JB** : un lien depuis son front ERP vers la nouvelle
  adresse (aller vite), et son profil migre avec son historique
  `revues.jsonl` complet (l'état se recalcule depuis le journal : la
  migration est une copie de fichier).
- **Comptes et profils** : profils multiples, chacun propriétaire de
  son état ; la clé API est **par personne**, jamais mutualisée sur le
  compte de JB (modalités : brique 3 ci-dessus).
- **Le RGPD est un PRÉALABLE, plus un sous-tiret** : dès M9, JB
  devient responsable de traitement de données d'apprentissage de
  TIERS, hébergées sur son infra. Avant le premier compte tiers : le
  registre (`meta/2026-08-24-registre-traitements-rgpd.md`, qui ne
  mentionne toujours pas l'Académie au 29/08) est mis à jour avec
  personnes concernées, base légale, information des personnes, durée
  de conservation, et la **suppression de compte** existe dans le
  produit (un ami part = son état s'efface). Pas de compte tiers sans
  ces cinq points.
- **Gate d'entrée mesurable** (remplace « plusieurs semaines », qui
  n'était ni un compteur ni un seuil) : le bilan des ~30 séances est
  passé ET le journal `revues.jsonl` montre 4 semaines supplémentaires
  de rituel tenu (≥ 4 séances/semaine) ; décideur : JB. **Ce gate
  n'est mesurable qu'à partir du jour où le chemin d'écriture d'une
  révision existe** (M2 reste n°0 / O1b — au 29/08 le journal n'a
  jamais reçu une ligne).
- **Fini quand** : JB fait sa séance du matin sur la nouvelle adresse
  depuis le lien ERP, avec son historique intact, et le scanner
  anti-fuite + une relecture prouvent qu'aucune donnée du portefeuille
  ni rien de l'ERP n'est visible du produit. **Taille : à chiffrer en
  ouverture (l'extraction du front est le morceau inconnu).**

## M10 — L'usine à domaines (réécrit le 29/08/2026)

- **Quoi** : le pipeline qui fait qu'un arrivant a son parcours **sans
  intervention humaine de JB** (arbitrage 2 du 29/08) : il branche sa
  source documentaire (**dépôt de documents en voie principale** ; le
  NotebookLM d'un tiers est une piste `[À VÉRIFIER]` — le « skill
  existant » est un skill de la session Claude de JB, pas une API
  qu'un produit web peut appeler pour un autre utilisateur), et l'IA
  génère le domaine complet — skill tree (branches, prérequis,
  niveaux), découpage de la matière, cartes, QCM à distracteurs
  expliqués, le tout au contrat carte-v1 et passé au valideur
  mécanique.
- **La qualité ne repose PAS sur l'arrivant seul** (pré-mortem 29/08 :
  un débutant ne peut pas valider un contenu qu'il ne maîtrise pas
  encore — c'est le mécanisme exact qui fait apprendre des faussetés,
  et le repo a déjà mesuré qu'un tampon `validated` + score de
  confiance ne protège de rien). Le circuit de M1 s'applique ENTIER à
  tout domaine généré : **la double passe par agent frais qui remonte
  aux sources reste obligatoire** (elle tourne sur la clé de
  l'arrivant, arbitrage 3) ; l'arrivant n'est que l'échantillonneur
  final, comme JB sur sa banque. Le bouton « carte fausse » existe dès
  la première séance, mais c'est un filet, pas le contrôle qualité.
- **Preuve par l'exemple** : un domaine étranger réel généré de bout
  en bout (le domaine infirmier ou maternité du brief, selon l'ami
  disponible ; sinon un domaine public de test), qui tourne sans
  toucher au moteur.
- **Le droit des sources s'applique à tous** : paraphrase + lien,
  jamais de recopie ; le NotebookLM d'un tiers peut contenir du
  matériel non redistribuable (le carnet de JB en contient : support
  interne Sergic) — la génération produit des cartes dérivées
  sourcées, pas des extraits.
- **Fini quand** : un vrai ami a son domaine généré, son skill tree,
  et a joué sa première séance sans que JB ait touché à son contenu.
  **Taille : deux à trois sessions.**

## M11 — La couche sociale : amis, visibilité, défis (ajouté le 29/08/2026)

- **Quoi** : l'ajout d'amis (invitation explicite, jamais de
  découverte publique), la **visibilité totale entre amis** (arbitrage
  1 : skill tree complet, heures de jeu, notions apprises, dernière
  activité — « JB est à l'étape X de copro niveau Y »), et les
  **défis** : un ami défie l'autre sur une notion (un mini-lot de
  cartes ou un QCM commun, chacun joue de son côté, les scores se
  comparent).
- **Ce que l'arbitrage 1 change au texte gravé, dit en face**
  (pré-mortem 29/08) : le §9 du BLUEPRINT interdisait « aucun écran
  comparatif entre profils, jamais » — M11 construit exactement cet
  écran. Le §9 est donc **amendé le 29/08** (pas contourné en
  silence) : l'interdit absolu devient « hors cercle d'amis
  mutuellement consentis » ; l'interdit managérial, lui, ne bouge pas.
  Une règle amendée sur brief tracé reste opposable ; une règle
  contredite sans trace ne l'est plus.
- **Le garde-fou managérial cesse d'être un vœu** : la doctrine seule
  n'empêche pas un manager de se faire « ajouter en ami » par un
  subordonné. Mécanismes minimums au chantier : ajout strictement
  mutuel ; retrait d'un clic, silencieux, sans notification ;
  visibilité désactivable **par domaine** ; avertissement explicite à
  l'ajout (« votre ami verra tout votre parcours — n'ajoutez pas
  votre hiérarchie ») ; et la règle écrite dans les conditions du
  produit, pas seulement dans un dépôt privé que l'employeur ne lit
  pas. Le risque résiduel (pression sociale à ajouter son manager)
  est nommé, pas résolu : il est dit à JB tel quel.
- **Défis vs Loi 7 (SDT)** : le cadrage scientifique classe les
  comparaisons extrinsèques parmi ce qui détruit la motivation
  intrinsèque — et un défi score-contre-score EST une comparaison
  extrinsèque, même sans ligue ni badge. On le construit quand même
  (arbitrage 1), mais sous condition mesurée : les défis sont
  optionnels, jamais proposés d'office dans la séance, et si les
  données d'usage montrent qu'ils dégradent le rituel (séances
  sautées après une défaite, mix de séance déformé vers les défis),
  **on les coupe** — le critère et le relevé se posent au chantier,
  avant la première partie.
- **Fini quand** : JB et un ami réel se voient mutuellement avancer
  chacun dans son domaine, et un défi complet a été joué et comparé.
  **Taille : deux sessions, après M10.**

---

## Ce qu'on n'oublie pas (risques nommés au cadrage et au pré-mortem)

- **La qualité avant la quantité** : 60 cartes justes battent 1 000
  cartes dont 5 % de fausses — une carte fausse apprise coûte plus
  cher qu'une carte absente (le brief le dit : « il ne faut pas me
  dire de bêtises »). D'où le valideur M1 et le bouton « carte
  fausse » dès M2.
- **Le rituel avant les features** : le bilan des ~30 séances (usage +
  mini-test de rétention) est un GATE d'entrée de M4. Pas de modes
  visuels au-dessus d'un rituel qui ne tient pas.
- **Le contenu est un flux, pas un stock** : sans le lot hebdo (M2,
  exploitation), le produit est à sec vers le 20e matin — c'est le
  bloquant n°2 du pré-mortem, la parade est chiffrée au BLUEPRINT §7.
- **Tant que M3 et M5 ne sont pas livrés, l'app maison n'a pas battu
  Anki** : c'est dit en face (BLUEPRINT §2), et l'export CSV Anki est
  l'assurance-vie du contenu quoi qu'il arrive.
- **Le droit des sources** : pas de scan de manuel dans la banque ;
  lien + paraphrase. À vérifier source par source en M1. Les décisions
  de justice et textes officiels sont publics : les ateliers qui s'y
  adossent sont les plus sûrs juridiquement.
- **Le RGPD n'attend pas M9** : registre mis à jour en M2 (données
  d'apprentissage d'un salarié, hébergées sur GitHub + VPS), règle de
  lecture des profils gravée avant le premier profil (§9). L'Académie
  n'est jamais un instrument d'évaluation.
- **Le serveur ne se lit pas depuis le cloud** : tout atelier sur
  pièce réelle se prépare en session locale, en batch, d'avance.
  Jamais « on ira chercher le devis le matin même ».
- **La charge de JB** : ~15 min par jour de séance + ~10 min de
  validation par semaine, point. Si ça déborde, on baisse le quota de
  neuf, on n'étire pas JB.
- **La dérive gadget** : chaque chantier M* sert la rétention mesurée
  ou n'existe pas ; le corpo et le cosmétique passent toujours après
  une branche de savoir métier.
- **La dérive de périmètre, version 29/08** : M9-M11 sont trois
  chantiers de produit grand public qui n'améliorent PAS la rétention
  de JB d'une seule carte. Ils n'ont le droit d'exister qu'après un
  rituel qui tient (gates M9) et ne passent jamais devant un chantier
  M1-M8 en retard. Si le temps manque, c'est M9-M11 qu'on gèle.
- **L'ami pilote peut abandonner** : les « fini quand » de M10 et M11
  exigent « un vrai ami » — une dépendance à une personne extérieure
  non engagée. Repli écrit d'avance : un domaine public de test
  (M10) et un second profil de JB (M11) valident la mécanique ; l'ami
  réel valide le produit, pas le chantier.
- **Le RGPD change de nature à M9** : jusqu'à M8, JB trace ses propres
  révisions ; à partir du premier compte tiers, il est responsable de
  traitement des données d'apprentissage d'autrui. Les cinq points du
  préalable M9 (registre, base légale, information, durée,
  suppression de compte) ne sont pas négociables.
- **Deux roadmaps, des sessions parallèles** : un chantier M* annonce
  sa prise dans la file d'alertes (leçon R16) et committe par chemins
  explicites. Attention (corrigé au pré-mortem du 29/08) : `academie/`
  n'est PAS isolé — le front de l'Académie vit dans
  `erp/react/src/**` (vue, composants, lib, data, accroches App /
  Barre / Rail / Palette) ; un chantier M* qui touche l'écran touche
  l'ERP, et se coordonne avec les chantiers R* comme tel.

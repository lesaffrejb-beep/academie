# Benchmark — ce qui se vole ailleurs pour l'Académie (30/08/2026)

Mission JB du 30/08 : « améliore tout ça en te basant sur des projets
open source ou des jeux existants, vois si tu peux choper des modèles,
des modules ou des fonctionnements ailleurs ».

**On vole des PATTERNS, jamais des plateformes.** Chaque entrée dit :
le mécanisme précis, où il atterrit chez nous (SPEC-PRODUIT §, chantier
O de la table d'orchestration), la licence **vérifiée à la source le
30/08/2026** avec son URL, et un verdict.

Trois verdicts :

- **VOLER LE PATTERN** — on reprend l'idée, on écrit notre code. Aucune
  question de licence (une mécanique de jeu ne se brevette pas ; on ne
  copie ni le nom, ni les visuels, ni le texte).
- **RÉUTILISER LE CODE-ASSET** — on branche le dépôt ou le fichier tel
  quel, licence permissive vérifiée.
- **IGNORER** — avec la raison écrite. Une licence introuvable ou
  douteuse est une raison suffisante et finale
  ([`wiki/patterns/licence-outil-avant-fonctionnalite.md`](../../wiki/patterns/licence-outil-avant-fonctionnalite.md)).

**Ce document n'installe rien.** Aucune dépendance npm n'a été ajoutée.
Le lot d'icônes est le seul livrable matériel de la session :
`erp/react/src/assets/academie/icones/` (33 SVG + `CREDITS.md`).

---

## Partie 1 — Les produits d'apprentissage

### 1.1 Anki : « mature card = intervalle ≥ 21 jours » — et notre seuil est le même

**Le pattern.** Anki appelle « mature » une carte dont l'intervalle
atteint 21 jours, et sa statistique de **true retention** ne compte que
la PREMIÈRE révision d'une carte dans la journée : `Again` = échec,
`Hard`/`Good`/`Easy` = réussite. C'est une convention vieille de quinze
ans, avec un corpus derrière.

**Ce que ça nous dit.** Le seuil de remplissage de région déjà arrêté à
la SPEC §3 (« % des cartes `valide` dont la stabilité FSRS est ≥ 21 j »)
tombe exactement sur la convention Anki. **Ce n'est pas une coïncidence
à laisser implicite : c'est un argument de défense du chiffre.** À
écrire dans `academie.json` à côté du paramètre, et dans MÉTHODE.

**Le second pattern, lui, nous manque** : la mesure de *true retention*
comme indicateur de santé du produit. On sait déjà mesurer la
rétrouvabilité prédite ; on ne mesure pas encore ce qu'on obtient
vraiment. C'est la métrique honnête du gate M4 (bilan ~30 séances) et
elle est calculable depuis `revues.jsonl` dès qu'O1b existe, sans une
ligne de code en plus dans le moteur.

**Où ça va.** `academie.json` (commentaire de source sur le seuil) ·
`app/progression.py` (fonction `retention_reelle()`) · le bilan mensuel ·
MÉTHODE §1. Chantier : **O1b puis O3**.

**Licence.** Anki : **AGPL-3.0** (avec des portions BSD-3 contribuées) —
<https://github.com/ankitects/anki/blob/main/LICENSE>, vérifié
30/08/2026. Copyleft fort : on lit la définition, la doctrine, le
manuel ; **on ne recopie pas une ligne de son code**.

**Verdict : VOLER LE PATTERN** (définition + métrique), pas le code.

---

### 1.2 Anki : la heatmap de révisions

**Le pattern.** Le calendrier-heatmap (une case par jour, intensité =
nombre de révisions, plus la série en cours et le total de l'année) est
l'écran que les utilisateurs d'Anki regardent en premier. Il montre la
régularité, pas la performance — exactement la variable qui compte chez
nous (« la seule chose qui compte vraiment, c'est le rituel »,
MÉTHODE §8).

**Où ça va.** Le calendrier de pastilles déjà prévu (SPEC §3, « le reste
confirmé »). La nuance à voler : **l'intensité, pas le binaire.** Une
pastille pleine/vide dit « fait / pas fait » et rouvre la porte à la
honte ; un dégradé dit « ce jour-là j'ai fait un peu », ce qui reste
compatible avec l'interdit de dette. Icône `calendrier.svg` livrée.

**Licence.** L'add-on de référence *Review Heatmap* (glutanimate) est en
**AGPL-3.0 + termes additionnels au titre de la section 7** —
<https://github.com/glutanimate/review-heatmap/blob/master/LICENSE>,
vérifié 30/08/2026. Copyleft fort **et** clauses maison en plus : on ne
touche pas au code.

**Alternative si on veut du code** : `simpleheat` (mourner) est en
**BSD-2-Clause** (<https://github.com/mourner/simpleheat>, vérifié
30/08/2026) mais c'est une heatmap de densité géographique, pas un
calendrier — inadapté. **Un calendrier-heatmap se dessine en ~40 lignes
de SVG** : ne rien installer.

**Verdict : VOLER LE PATTERN**, code écrit à la main.

---

### 1.3 Anki : le format de partage de decks (`.apkg`) — la réversibilité, sans Anki

**Le pattern.** Un deck Anki est un fichier unique, autonome, qu'on
s'envoie et qu'on ouvre partout. C'est ce qui a fait l'écosystème.
L'export Anki figure déjà au CONTRAT-CARTE-V1 §4 comme
**assurance-vie de réversibilité** (et JB a tranché : « arrête de me
parler Anki, le but c'est construire l'app » — donc l'export est une
assurance, le livrable de personne).

**La trouvaille concrète** : `genanki` écrit des `.apkg` en Python pur,
sans installer Anki. Notre `export_anki.py` (chantier O2) est un
script de ~80 lignes au lieu d'un chantier.

**Licence.** `genanki` : **MIT** —
<https://github.com/kerrickstaley/genanki/blob/main/LICENSE.txt>,
vérifié 30/08/2026 via l'API GitHub. Permissive, mention à conserver.

**Verdict : RÉUTILISER LE CODE** — mais **au moment d'O2**, pas avant :
c'est une dépendance Python de l'usine à cartes, jamais une dépendance
du produit joué. À vérifier une seconde fois à l'installation (une
licence porte sa date).

---

### 1.4 FSRS : l'écosystème est plus large que le planificateur

**Ce qu'on a déjà** : le portage maison FSRS-6, comparé à `py-fsrs`
à 10⁻⁴ près.

**Ce qu'on n'a pas regardé** : `fsrs-optimizer`, qui entraîne les 21
paramètres sur *un* historique personnel. Notre journal (`revues.jsonl`,
O1b) porte déjà le champ `origine` prévu par la SPEC §3 précisément pour
qu'un futur optimiseur ne s'entraîne pas sur les réponses de quiz. La
décision utile aujourd'hui n'est pas d'optimiser (il faut ~1000
révisions), c'est de **vérifier que notre journal contient les colonnes
que l'optimiseur exigera** — sinon on découvre le trou à 1000 révisions,
c'est-à-dire trop tard.

**Licences vérifiées le 30/08/2026 (API GitHub)** :

| Dépôt | Licence | URL |
|---|---|---|
| `open-spaced-repetition/py-fsrs` | MIT | <https://github.com/open-spaced-repetition/py-fsrs/blob/main/LICENSE> |
| `open-spaced-repetition/ts-fsrs` | MIT | <https://github.com/open-spaced-repetition/ts-fsrs/blob/main/LICENSE> |
| `open-spaced-repetition/fsrs4anki` | MIT | dépôt du planificateur |
| `open-spaced-repetition/fsrs-optimizer` | **BSD-3-Clause** | dépôt de l'optimiseur |
| `open-spaced-repetition/fsrs-rs` | **BSD-3-Clause** | implémentation Rust |

Toutes permissives. À noter pour plus tard : **`ts-fsrs` est en MIT** —
si un jour le front doit planifier hors ligne (mode avion, PWA), c'est
la brique, et elle ne pose aucune question de licence.

**Verdict : VOLER LE PATTERN** (le contrat de colonnes du journal, tout
de suite, chantier **O1b**) · **RÉUTILISER LE CODE** plus tard et
seulement si besoin (`fsrs-optimizer` au gate M4, `ts-fsrs` si offline).

---

### 1.5 WaniKani : la porte à 90 %, et la punition qui recule de plusieurs crans

**Le pattern, précisément.** Deux mécaniques distinctes, souvent
confondues :

1. **La porte de niveau** : on ne passe au niveau suivant que quand
   *tous* les radicaux et *90 %* des kanji du niveau courant ont atteint
   le stade « Guru ». C'est un seuil de **stabilité**, pas de volume.
2. **La rétrogradation asymétrique** : une erreur ne fait pas reculer
   d'un cran mais **de plusieurs**, d'autant plus qu'on était haut.

**Ce qu'on en prend.** La porte à 90 % valide notre seuil de ~75 % pour
ouvrir la région suivante — même famille de mécanique, calibrage plus
doux, ce qui est cohérent avec un adulte qui a 15 minutes le matin et
non un apprenant qui vise le kanji.

**Ce qu'on en refuse, et c'est le plus intéressant** : la
rétrogradation. FSRS gère déjà la baisse de stabilité, en continu et
mesuré. Rajouter une chute visible de « rang » par-dessus, ce serait
**une seconde comptabilité** — exactement ce que la SPEC §3 interdit
(« l'XP affichée est un habillage dérivé, jamais une seconde
comptabilité »). Et c'est punitif, ce que MÉTHODE §9 interdit.

**Où ça va.** SPEC §3 carte-monde (confirmation du seuil) ·
`app/progression.py`. Chantier **O5 (M7)**.

**Licence.** Produit commercial fermé, rien à réutiliser. Documentation
publique du fonctionnement :
<https://knowledge.wanikani.com/wanikani/srs-stages/> (vérifié
30/08/2026).

**Verdict : VOLER LE PATTERN** (la porte) · **IGNORER** (la
rétrogradation visible : incompatible avec nos invariants).

---

### 1.6 Khan Academy : quatre paliers nommés, et le palier haut n'est atteignable QU'EN examen

**Le pattern, précisément.** Une compétence traverse quatre états
nommés — *Attempted*, *Familiar*, *Proficient*, *Mastered* — et le
dernier n'est **atteignable que sur un test transverse** (unit test,
course challenge, mastery challenge), jamais sur l'exercice
d'entraînement lui-même. Les *Mastery Challenges* sont calibrées :
**6 questions sur 3 compétences**, déverrouillées après 3 compétences
« Familiar » + 1 « Proficient », et pas plus d'une toutes les 12 heures.

**Ce que ça valide et ce que ça ajoute.** Ça valide en plein notre
boss-examen (SPEC §3 : pas de 100 % sans examen à froid, plafond à
99 % sinon) — mécanique identique, chez un acteur qui l'a mesurée sur
des millions d'élèves. Ça **ajoute** trois choses qu'on n'a pas :

- **Nommer les paliers.** Notre remplissage est un pourcentage, donc
  illisible à l'œil. Quatre états nommés au-dessus du même calcul FSRS
  (0 / entamé / solide / conquis) rendent la carte lisible d'un regard,
  sans créer de comptabilité parallèle — c'est un **affichage**.
- **Le boss court et fréquent, pas seulement le boss final.** Une
  Mastery Challenge fait 6 questions sur 3 compétences. C'est
  exactement notre séance entrelacée, mais estampillée « épreuve ». Le
  boss de région (10-15 cartes) reste l'examen solennel.
- **Le verrou temporel** (une par 12 h). Notre équivalent naturel :
  **un boss de région ne se retente pas le jour même.** Sinon
  l'examen à froid n'est plus à froid, et la mesure ne vaut rien.

**Où ça va.** SPEC §3 (boss) · `app/progression.py` (les paliers
nommés) · MÉTHODE §10 (le verrou temporel, à justifier). Chantier
**O5 (M7)**.

**Licence.** Produit fermé ; documentation publique
<https://support.khanacademy.org/hc/en-us/articles/360037494231-What-are-Mastery-Challenges>
(vérifié 30/08/2026).

**Verdict : VOLER LE PATTERN** (les trois points).

---

### 1.7 Duolingo : le chemin linéaire — et le procès qu'on lui a fait

**Le fait, et il va à contre-courant de ce qu'on croit voler à
Duolingo.** En novembre 2022, Duolingo a remplacé son arbre par un
**chemin linéaire**, motif affiché : la clarté (« l'arbre ne disait pas
si on devait avancer, reculer ou monter »). Le retour terrain a été
franchement mitigé : le reproche principal, largement documenté, est
**la perte de liberté** — on ne pouvait plus sauter, ni revenir, ni
choisir.

**Ce que ça nous dit, et c'est la trouvaille la plus utile de la
partie 1.** La SPEC §3 a déjà tranché dans le bon sens sans le savoir :
« la région suivante s'ouvre à ~75 % de la précédente — **mais toute
région visible est explorable** ». C'est précisément la soupape que le
chemin de Duolingo a supprimée, et pour laquelle on lui est tombé
dessus. **Cette phrase de la SPEC est un invariant, pas un détail de
confort : à ne jamais optimiser au nom de la clarté.** À écrire comme
tel dans la spec, avec ce précédent.

**Le second pattern, celui qui se prend** : le **coffre de fin d'unité**
— une récompense visible sur le chemin, à quelques nœuds devant soi,
qui donne un objectif court quand l'objectif long (le concours de mars
2027) est trop loin pour tirer un matin de novembre. Chez nous, le
coffre ne peut pas contenir de monnaie (« jamais de boutique, jamais de
monnaie », SPEC §3) : **il contient le cosmétique de zone**, déjà arrêté
par JB le 30/08. Icône `coffre-ouvert.svg` livrée.

**Où ça va.** SPEC §3 (durcir la phrase d'exploration libre) · le
rendu de la carte-monde. Chantier **O5 (M7)**.

**Licence.** Produit fermé. Sources : annonce de refonte
<https://blog.duolingo.com/new-duolingo-home-screen-design> ; retour
d'usage secondaire <https://duoplanet.com/duolingo-new-learning-path-review/>
(consultés 30/08/2026).

**Verdict : VOLER LE PATTERN** (le coffre) · **IGNORER** (la linéarité,
et documenter pourquoi).

---

### 1.8 Duolingo : la recherche publiée, elle, est solide et réutilisable

**Le pattern.** Duolingo a publié en 2016 la *half-life regression*
(Settles & Meeder, ACL), avec **le jeu de données de 13 millions de
traces d'apprentissage** et le code. Annonces de l'article : +12 %
d'engagement quotidien et −45 % d'erreur de prédiction du rappel.

**Ce qu'on en fait, et surtout ce qu'on n'en fait pas.** On **ne change
pas de planificateur** : FSRS-6 est plus récent, entraîné sur ~700 M de
révisions, et il est déjà porté et testé chez nous. En revanche le
**jeu de données** est une ressource rare : il permettrait de tester
notre code de calcul de rétention sur des traces réelles massives avant
que JB en ait produit trente.

**Licence.** `duolingo/halflife-regression` : **MIT** —
<https://github.com/duolingo/halflife-regression/blob/master/LICENSE.md>,
vérifié 30/08/2026 via l'API GitHub. **Bonne surprise** : on s'attendait
à une clause non-commerciale sur les données d'un acteur privé, il n'y
en a pas.

**Verdict : IGNORER le modèle** (FSRS le remplace, et changer de
planificateur serait une régression documentée) · **RÉUTILISER LE JEU DE
DONNÉES** si un jour on veut valider un calcul statistique hors de nos
propres traces. Non prioritaire.

---

### 1.9 Duolingo : le streak freeze — et pourquoi on ne le prend pas

**Le pattern.** Le *streak freeze* protège la série sur un jour manqué ;
la *Streak Society* transforme le compteur en signe d'identité.

**Les chiffres qui circulent sont invérifiables.** Les écarts publiés
(séries en moyenne 48 % plus longues avec freeze, −21 % de churn) ne
viennent pas de Duolingo mais de blogs d'éditeurs d'outils de
gamification, qui vendent la fonctionnalité qu'ils mesurent.
**`[NON VÉRIFIÉ À LA SOURCE]`** — à ne pas citer dans MÉTHODE, où
chaque entrée porte une source relue.

**Et de toute façon, le mécanisme nous est inutile.** Un streak freeze
protège d'une punition ; **notre compteur ne descend jamais**
(MÉTHODE §9). On ne construit pas la rustine d'un problème qu'on n'a
pas. Le seul emprunt légitime est la *Streak Society* — un jalon
d'identité à 100 ou 365 jours — et il est déjà couvert par les
cosmétiques de zone.

**Verdict : IGNORER** (rustine d'une mécanique punitive qu'on n'a pas ;
chiffres non sourçables).

---

### 1.10 Exercism : le syllabus se fait pousser, il ne se dessine pas

**Le pattern.** Deux familles d'exercices : les *concept exercises* (un
concept, une leçon) et les *practice exercises*, ces dernières
**déverrouillées par la progression dans l'arbre de concepts** — un
exercice de pratique peut exiger plusieurs concepts, donc rester
verrouillé même après la leçon qui semblait le concerner. Et la
doctrine de construction, écrite noir sur blanc dans leur
documentation : **faire pousser l'arbre organiquement depuis les
concepts les plus simples, ne pas tout concevoir d'avance.**

**Ce que ça nous dit.** C'est la réponse au problème que la SPEC §3
pose sans le résoudre : « la carte est GIGANTESQUE en profondeur », le
bout de chaque branche visant l'état de l'art. Une carte de cette taille
ne se dessine pas d'avance — elle se **fait pousser**, région par
région, et le brouillard est précisément ce qui rend la croissance
invisible au joueur. Le `gabarit-domaine/` déjà posé doit donc porter
**la règle de croissance** (comment on ajoute une région à une carte
vivante sans casser les taux de remplissage déjà calculés), pas
seulement le squelette d'une carte finie. C'est un vrai risque de
conception : ajouter 40 cartes à une région conquise la fait retomber
à 60 %, et le joueur vit une régression qu'il n'a pas méritée. Il faut
la règle avant le contenu — soit une région conquise reste conquise et
l'ajout ouvre une **sous-région** neuve, soit on l'assume et on
l'explique.

**Où ça va.** `academie/gabarit-domaine/` · SPEC §4 (usine à domaine) ·
`app/progression.py`. Chantier **O2 puis O7**.

**Licence. Mauvaise surprise à noter** : `exercism/website` est en
**AGPL-3.0** (<https://github.com/exercism/website>, vérifié
30/08/2026) — copyleft fort, on ne lit que les idées. En revanche
`exercism/problem-specifications` est en **MIT** (même vérification).
La documentation de méthode (<https://exercism.org/docs/building/tracks/syllabus>)
est lisible sans réserve.

**Verdict : VOLER LE PATTERN** (la règle de croissance, urgent) ·
**IGNORER le code** (AGPL).

---

### 1.11 Brilliant : le pattern est déjà chez nous

**Le pattern** — on n'explique pas puis on interroge, on interroge et
l'explication naît de la réponse. C'est **exactement** MÉTHODE §2 et §7
(« on te fait répondre, jamais relire » ; « l'algo est le prof »).

**Verdict : rien à voler, tout est déjà pris.** Entrée conservée pour
que le prochain agent ne refasse pas la recherche.

---

## Partie 2 — Les jeux : la carte, la conquête, les cosmétiques

### 2.1 Le brouillard de guerre a DEUX couches, pas une (Civilization, Age of Empires)

**Le pattern, et c'est la trouvaille de la partie 2.** Les jeux de
stratégie ne connaissent pas « brouillard / pas brouillard ». Ils ont
**deux couches distinctes** :

1. le **shroud** — le non-exploré, noir opaque, on ne sait même pas
   quel terrain il y a. Il se lève définitivement et ne revient jamais ;
2. le **fog** — exploré mais hors de vue : **le terrain reste visible**,
   assombri, et on y voit la dernière information connue, périmée.

**Ce que ça change chez nous.** La SPEC §3 dit « le brouillard se lève
région par région » et « régions suivantes esquissées en silhouette ».
Ces deux phrases décrivent en fait déjà deux couches, sans le dire. Les
nommer donne trois états au lieu de deux, et chacun porte du sens
pédagogique :

| État de carte | Chez nous | Ce que le joueur voit |
|---|---|---|
| Shroud (noir) | Région non ouverte, pas encore à portée | Une silhouette, un nom, rien de plus |
| Fog (assombri) | Région ouverte, **information périmée** | Le dernier taux de remplissage connu, daté |
| Clair | Région travaillée récemment | Le remplissage à jour |

La couche « fog » est un cadeau : **une région qu'on n'a pas touchée
depuis six semaines a un remplissage périmé**, puisque la stabilité
FSRS y a baissé sans qu'on la mesure. Afficher un chiffre daté et
assombri au lieu d'un chiffre faux et net, c'est la règle dure n°3 du
repo (« un chiffre porte sa date de vérification, ou il ne se dit
pas ») rendue **littéralement visible dans un décor de jeu**. Un
mécanisme d'engagement qui dit la vérité sur l'incertitude : c'est le
meilleur dark pattern du lot.

**Où ça va.** SPEC §3 (carte-monde) · `app/progression.py` (fraîcheur
d'une région) · le rendu de la carte. Chantier **O5 (M7)**.

**Licence.** Aucune (mécanique de genre, présente dans des centaines de
jeux depuis 1990). Documentation :
<https://civilization.fandom.com/wiki/Fog_of_war> ·
<https://support.ageofempires.com/hc/en-us/articles/5722455564052-Creating-Fog-of-War-Areas>
(consultés 30/08/2026). Icône `brouillard.svg` livrée.

**Verdict : VOLER LE PATTERN** — première recommandation de la
courte liste.

---

### 2.2 Slay the Spire : la carte se génère, avec des contraintes dures

**Le pattern, précisément.** Un acte = une grille irrégulière 7×15, 17
étages. On tire un nœud de départ, on le relie à l'un des 3 nœuds les
plus proches de l'étage au-dessus, on recommence. Puis les contraintes,
qui font tout le sel :

- **au moins deux points de départ distincts** (le premier choix du
  joueur est réel dès le premier écran) ;
- **les chemins ne se croisent jamais** (lisibilité) ;
- **1 à 3 entrées et 1 à 3 sorties par nœud** (jamais d'impasse,
  jamais de bouillie) ;
- **tout est déterministe à partir d'une graine** — la même graine
  redonne la même carte.

**Ce qu'on en prend.** Pas la génération procédurale : nos régions sont
un contenu pédagogique écrit, pas un tirage. On prend **les
contraintes de lisibilité comme règles de validation du gabarit de
domaine** — pas d'impasse, au moins deux entrées possibles, degré
borné, pas de croisement. Quand un tiers dessinera sa carte dans
l'usine à domaine (SPEC §4, un humain qui ne sait pas coder), c'est
exactement le genre de règle qu'un valideur doit refuser
mécaniquement, comme le contrat de carte refuse déjà un QCM sans
distracteurs expliqués.

**Et la graine, elle, se prend telle quelle** : le tirage guidé
(« l'expédition aléatoire ») **doit** être déterministe et journalisé.
Sinon on ne peut pas rejouer une séance pour comprendre un bug, et
« pourquoi il m'a sorti ça ce matin » est sans réponse. Le contrat de
journal d'O1b doit donc porter la graine du jour. C'est une ligne de
code aujourd'hui, une reprise de schéma dans six mois.

**Où ça va.** `academie/gabarit-domaine/` (règles de validation) ·
`app/seance.py` (graine journalisée). Chantier **O1b puis O2**.

**Licence.** Le jeu est fermé ; les réimplémentations publiques de sa
génération de carte sont permissives, vérifiées 30/08/2026 via l'API
GitHub :

- `silverua/slay-the-spire-map-in-unity` — **MIT**
- `OrangeSensei06/SlayTheSpireMapGeneration` — **MIT**

Toutes deux en C#/Unity : **inutilisables telles quelles** dans un
front React. On lit l'algorithme, on n'importe rien.

**Verdict : VOLER LE PATTERN** (contraintes + graine déterministe) ·
**IGNORER le code** (mauvais runtime, pas mauvaise licence).

---

### 2.3 Super Mario World, Risk : ce qu'une carte-monde doit à ses voisins

**Le pattern (Mario World).** Une carte-monde tient debout avec trois
choses seulement : des **nœuds** posés sur un décor dessiné, des
**chemins** qui les relient, et un **avatar** qui se déplace de nœud en
nœud. La position de l'avatar EST la sauvegarde : on n'a pas besoin
d'un écran d'état, la carte est l'écran d'état. C'est le budget
technique minimal d'une carte qui n'est pas une liste — SVG, quelques
`<path>`, une transition de position. Rien à voir avec de la 3D.

**Le pattern (Risk).** Un territoire n'existe que par sa **liste
d'adjacences**. La carte est un graphe ; le dessin n'est qu'une
projection. Conséquence directe pour nous : le modèle de données d'une
région se réduit à `{ id, nom, voisins[], seuil_ouverture }`, le décor
est un habillage. **C'est ce qui rend le lieu-monde possible** : le même
graphe se dessine en archipel (v1) puis en coupe d'immeuble (v1.1) puis
en 3D, sans toucher `app/progression.py`. La SPEC §3 annonce cette
trajectoire ; le graphe d'adjacence est la pièce qui la rend vraie au
lieu de la promettre.

**Où ça va.** Le contrat de données de la carte, dans
`academie/gabarit-domaine/` — **avant** de dessiner quoi que ce soit.
Chantier **O2**, en amont d'O5.

**Licence.** Aucune (mécaniques de genre). **Attention à ne rien
emprunter d'autre** : les visuels, les noms et la musique de ces jeux
sont protégés.

**Verdict : VOLER LE PATTERN.**

---

### 2.4 Les cosmétiques qui ne s'achètent pas (Deep Rock Galactic, Halo: Campaign Evolved)

**Le pattern.** Deep Rock Galactic distribue des centaines de
cosmétiques par le jeu — assignations, caisses à réparer, événements —
et rien du contenu de jeu ne se monétise. Halo: Campaign Evolved annonce
qu'il n'y aura **aucune boutique** : chaque skin s'obtient par le jeu,
un événement ou un code, jamais avec une monnaie.

**Ce que ça confirme.** L'arbitrage de JB du 30/08 (cosmétiques de fin
de zone sur un avatar, « jamais de boutique, jamais de monnaie ») est
la position de studios qui en ont fait un argument de fidélité, pas une
coquetterie.

**Ce que ça ajoute, et c'est fin.** Chez DRG, le cosmétique **dit d'où
il vient** : il se lit comme une biographie. C'est exactement l'idée de
JB (« le chapeau d'étudiant en droit pour l'urbanisme copro, l'éclair
dans la main pour l'électricité des immeubles »). Le complément à
graver : **un cosmétique porte le nom de la zone qui l'a donné et sa
date**, visible au survol. Sans ça, c'est une décoration ; avec ça,
c'est une mémoire de parcours — et ça reste vrai pour quelqu'un qui
joue seul, avant tout M11.

**Où ça va.** SPEC §3 (« le reste, confirmé sans changement ») ·
`etat/<profil>/` (le cosmétique stocke sa provenance). Chantier
**O5**, matériel : `chapeau-etudiant.svg`, `eclair.svg`,
`coffre-ouvert.svg` livrés.

**Licence.** Aucune (mécanique). Sources :
<https://deeprockgalactic.wiki.gg/wiki/Character_Cosmetics> ·
<https://support.halowaypoint.com/hc/en-us/articles/50949231093268-Customization-Add-on-Support-for-Halo-Campaign-Evolved>
(consultés 30/08/2026).

**Verdict : VOLER LE PATTERN** (la provenance affichée).

---

## Partie 3 — Les projets open source : ce qui se branche vraiment

### 3.1 game-icons.net — **RÉUTILISER, c'est fait**

- **Licence : CC BY 3.0** — <https://creativecommons.org/licenses/by/3.0/>.
  Vérifiée **à deux sources concordantes** le 30/08/2026 : la page
  <https://game-icons.net/about.html> et le fichier
  <https://github.com/game-icons/icons/blob/master/license.txt>.
- Le dépôt précise « CC 3.0 BY **ou CC0 si mentionné** » : seuls
  Viscious Speed et Zeromancer sont en CC0. **Aucune icône retenue ne
  vient d'eux** — les 33 sont en CC BY, attribution obligatoire.
- **L'attribution est la condition de la licence** : elle doit être
  VISIBLE DANS L'APP, pas seulement dans le repo. Détail et mention
  exacte : `erp/react/src/assets/academie/icones/CREDITS.md`.
- Piège technique noté au CREDITS : les SVG sont blanc sur fond noir
  opaque, à retravailler en `currentColor` par la session front.

**Livré : 33 icônes**, couvrant le jeu (citadelle, drapeau, brouillard,
longue-vue, dé, sablier, éclair, parchemin, trophée, coffre, cerveau,
calendrier), le lieu-monde immeuble (maison, brique, casque, engrenages,
flamme, gouttes, vanne, ascenseur, clés, balance, marteau, pièces,
graphique) et le lieu-monde hôpital (hôpital, stéthoscope, cœur,
seringue, trousse).

---

### 3.2 Azgaar's Fantasy Map Generator — **RÉUTILISER L'ASSET, pas le code**

- **Licence : MIT** —
  <https://github.com/Azgaar/Fantasy-Map-Generator/blob/master/LICENSE>,
  fichier lu à la source le 30/08/2026.
- **Bonne surprise, et il faut la noter** : GitHub affiche « Other »
  parce que le fichier ajoute un paragraphe au texte MIT standard. Ce
  paragraphe **élargit** les droits au lieu de les restreindre : « You
  can produce, without restrictions, any derivative works from the
  original software and even reap commercial benefits from the sale of
  the secondary product. The derivates include created maps, map
  images, screenshots, videos, and other materials. » Autrement dit
  **les cartes produites par l'outil sont explicitement à nous**. Sans
  lire le fichier, on aurait classé ce dépôt en douteux et on serait
  passé à côté.
- **Ce qu'on en fait.** Le générateur est un monolithe SVG/JS de plus
  de dix ans, pensé pour un usage interactif, pas pour être importé
  dans React. On ne branche pas le code. On **génère une carte, on
  exporte le SVG, on le retravaille** comme fond de la carte 2,5D v1 —
  celle que la SPEC §3 veut « tout de suite », en attendant la coupe
  d'immeuble (v1.1). Coût : une soirée, zéro dépendance.

**Verdict : RÉUTILISER L'ASSET** (SVG exporté, fond de carte v1) ·
**IGNORER le code** (inintégrable). Chantier **O5**.

---

### 3.3 Red Blob Games (Amit Patel) — **RÉUTILISER LES ALGOS**

- **Licences vérifiées 30/08/2026 (API GitHub)** :
  `redblobgames/mapgen2` — **Apache-2.0** ;
  `redblobgames/1843-planet-generation` — **Apache-2.0**.
  Ses dépôts de code sont en MIT ou Apache 2.0, permissifs.
- **Réserve honnête** : le compte GitHub porte des licences claires,
  mais **le texte des articles sur redblobgames.com et le code inline
  des pages ne portent pas tous un fichier de licence visible**.
  Conduite : on prend les algorithmes depuis les **dépôts** (qui ont un
  LICENSE), on lit les articles comme explication, on ne copie-colle
  pas un extrait de page web sans licence attachée.
- **Ce qui nous sert précisément** : la génération de régions par
  **Voronoi** (des territoires irréguliers qui ressemblent à une carte,
  pas à une grille) et les algorithmes de terrain. C'est le savoir-faire
  qui manque pour que la carte « ne ressemble pas à un Quizlet »
  (critère de JB).

**Verdict : RÉUTILISER LES ALGOS** depuis les dépôts Apache-2.0,
mention d'attribution conservée. Chantier **O5**.

---

### 3.4 Les briques de rendu : ce qu'on ne doit PAS installer

Toutes vérifiées le 30/08/2026 via l'API GitHub. **Aucune n'a été
installée** (contrainte de la session) et, pour la plupart, aucune ne
devrait l'être.

| Brique | Licence | Verdict |
|---|---|---|
| `d3-geo` | **ISC** (+ MIT pour la part GeographicLib de C. Karney) | **IGNORER** — projection géographique ; nos régions sont un graphe abstrait, pas un globe |
| `d3-delaunay` | **ISC** | **RÉUTILISER si besoin** — Voronoi pour découper des régions irrégulières ; ~15 Ko, une seule fonction utile |
| `simplex-noise` (jwagner) | **MIT** | **RÉUTILISER si besoin** — bruit de terrain pour le relief 2,5D |
| `honeycomb` | **MIT** | **IGNORER** — grille hexagonale ; nos régions ne sont pas des hexagones et ne le deviendront pas |
| `rot.js` | **BSD-3-Clause** | **IGNORER** — champ de vision roguelike, à la case. Notre brouillard est par région : trois lignes, pas une bibliothèque |
| `leaflet` | **BSD-2-Clause** | **À CONSIDÉRER** — avec `CRS.Simple`, donne pan/zoom/calques sur une image de carte ; c'est le raccourci classique des visionneuses de cartes fantasy. À peser contre ~150 Ko et un modèle géographique dont on n'a pas besoin |
| `svg-pan-zoom` | **BSD-2-Clause** | **À CONSIDÉRER** — même service en ~10 Ko, sur du SVG. Le bon choix si la carte v1 est un SVG |
| `panzoom` (anvaka) | **MIT** | idem, alternative MIT |
| `konva` | **MIT** | **IGNORER** pour v1 — canvas 2D à scène-graphe ; utile seulement si le SVG sature |
| `pixi.js` | **MIT** | **IGNORER** pour v1 — WebGL 2D, surdimensionné avant d'avoir mesuré un problème de perf |
| `phaser` | **MIT** | **IGNORER** — moteur de jeu complet, hors sujet dans un front React |
| `excalibur` | **BSD-2-Clause** | **IGNORER** — idem |
| `lucide` | **ISC** | **RÉUTILISER si besoin** — icônes d'UI (flèches, croix, menu), complément propre de game-icons qui ne sert que le décor |
| `tabler-icons` | **MIT** | alternative MIT à lucide |

**La règle qui sort de ce tableau** : on n'installe pas une
bibliothèque pour un problème qu'on n'a pas encore mesuré (mémoire
`feedback_mesurer_avant_conclure`, 29/08). La carte v1
est du SVG écrit à la main ; `svg-pan-zoom` (BSD-2) est la seule
dépendance qui se discute vraiment, et seulement quand le zoom manquera.

---

### 3.5 Les packs 3D pour le chantier différé — **RÉUTILISER, licence idéale**

La SPEC §3 prévoit que le chantier 3D (three.js 0.180 déjà présent)
utilise « des packs d'assets .glb du commerce plutôt que de
modéliser — licence vérifiée AVANT de construire dessus ».
**Trois sources en CC0**, donc sans même d'obligation d'attribution :

| Source | Licence | Vérification |
|---|---|---|
| **Kenney** (kenney.nl) — packs isométriques, mobilier, prototypes | **CC0 1.0** | <https://kenney.nl/support> : « all game assets on the asset pages are public domain licensed (CC0). You're free to use them, even in commercial projects » — lu 30/08/2026 |
| **Poly Haven** — textures, HDRI, modèles | **CC0** | <https://polyhaven.com/license> — consulté 30/08/2026 |
| **Quaternius** — modèles low-poly game-ready | **CC0** | consulté 30/08/2026 |

CC0 = domaine public, usage commercial inclus, **attribution non
requise** (appréciée). À ne pas confondre avec les icônes
game-icons.net, qui l'imposent. Kenney a des kits isométriques
d'intérieurs et de mobilier : c'est **précisément** la matière du
lieu-monde immeuble.

**Verdict : RÉUTILISER LES ASSETS** — mais **au chantier 3D, pas
avant** : la SPEC dit v1 = 2,5D, et la 3D ne doit pas retarder le reste.
Entrée écrite ici pour que le prochain agent n'ait pas à refaire la
recherche de licence.

---

### 3.6 Watabou (générateurs de villes et donjons) — **IGNORER**

- Générateurs très beaux et très cités (Medieval Fantasy City
  Generator), mais **pas de licence formelle** : une phrase sur la page
  itch.io (« use maps as you like, attribution appreciated but not
  required ») que l'auteur **restreint ensuite dans les fils de
  discussion** de sa propre communauté, en désapprouvant certains
  usages commerciaux des SVG produits.
- Une permission qui se précise dans un forum n'est pas une licence.
  Elle n'a ni version, ni texte stable, ni date. Elle peut changer sans
  qu'on le sache, et elle n'est pas opposable.

**Verdict : IGNORER** — licence non formalisée et contredite par
l'auteur ailleurs. Azgaar (MIT, §3.2) rend le même service avec un
fichier LICENSE lisible. C'est exactement le cas d'école du pattern
`licence-outil-avant-fonctionnalite`.

---

## Partie 4 — Récapitulatif des licences vérifiées le 30/08/2026

Un fichier de licence lu à la source, ou une page officielle de
l'éditeur. Aucune ligne ne vient de la mémoire du modèle.

| Ressource | Licence | Conduite |
|---|---|---|
| game-icons.net | **CC BY 3.0** | Branché. **Attribution obligatoire et visible dans l'app** |
| Kenney / Poly Haven / Quaternius | **CC0** | Branchables au chantier 3D, sans attribution |
| Azgaar Fantasy Map Generator | **MIT** (élargi : cartes produites libres) | Asset exporté, pas le code |
| redblobgames/mapgen2, planet-generation | **Apache-2.0** | Algorithmes, mention conservée |
| genanki | **MIT** | À O2, pour `export_anki.py` |
| ts-fsrs, py-fsrs, fsrs4anki | **MIT** | Disponibles si besoin |
| fsrs-optimizer, fsrs-rs | **BSD-3-Clause** | Disponibles au gate M4 |
| duolingo/halflife-regression | **MIT** | Jeu de données seulement |
| d3-delaunay, lucide | **ISC** | Si besoin |
| simplex-noise, honeycomb, pixi, phaser, konva, tabler, panzoom | **MIT** | Non installés, la plupart inutiles |
| leaflet, svg-pan-zoom, rot.js, excalibur, simpleheat | **BSD-2 / BSD-3** | Non installés |
| exercism/problem-specifications | **MIT** | Documentation |
| **Anki** | **AGPL-3.0** | **Idées seulement, aucun code** |
| **Anki Review Heatmap** | **AGPL-3.0 + termes additionnels §7** | **Idées seulement** |
| **exercism/website** | **AGPL-3.0** | **Idées seulement** |
| **Watabou** | **aucune licence formelle** | **Écarté** |
| Duolingo, WaniKani, Khan Academy, Brilliant, Slay the Spire, Civ/AoE, Mario, Risk, DRG, Halo | produits fermés | Mécaniques seulement — jamais un visuel, un nom ou un texte |

**Aucune licence non commerciale ou « recherche seulement » n'a été
rencontrée** dans ce périmètre. Le piège du 29/08 (3DGS) ne s'est pas
reproduit : le risque ici est ailleurs, c'est **l'AGPL** — trois
ressources parmi les plus tentantes en sont porteuses.

---

## Partie 5 — La courte liste (5 recommandations, valeur/effort décroissant)

### 1. Le brouillard à deux couches : le chiffre périmé devient un décor

- **Le pattern.** Shroud (non exploré, silhouette) / fog (exploré,
  information périmée et datée) / clair (à jour) — la norme des jeux de
  stratégie depuis trente ans (§2.1).
- **La preuve.** Civilization et Age of Empires distinguent les deux
  couches ; c'est ce qui rend une carte lisible sans mentir sur ce
  qu'on sait.
- **Le premier pas.** Dans `app/progression.py`, ajouter la
  **fraîcheur** d'une région (date de dernière révision) à côté du
  remplissage, et rendre les trois états. Aucune donnée nouvelle : tout
  est dans le journal. **C'est la règle dure n°3 du repo rendue
  visible dans un décor de jeu.**

### 2. Nommer les paliers, et verrouiller le boss à 24 h

- **Le pattern.** Khan Academy : quatre états nommés au-dessus du même
  calcul, palier haut atteignable **uniquement en examen**, et une
  épreuve pas plus d'une fois toutes les 12 h (§1.6).
- **La preuve.** Mécanique servie à des millions d'élèves, et
  strictement identique à notre boss-examen — sauf le verrou temporel,
  qu'on n'a pas.
- **Le premier pas.** Un pourcentage est illisible : dériver quatre
  états nommés du remplissage déjà calculé (affichage, pas seconde
  comptabilité), et interdire de retenter un boss le jour même — sans
  ça, l'examen à froid n'est pas à froid et le score ne mesure rien.

### 3. La graine du jour, journalisée — à écrire dans O1b ou jamais

- **Le pattern.** Slay the Spire : toute la génération dérive d'une
  graine, la carte est rejouable à l'identique (§2.2).
- **La preuve.** C'est ce qui permet à ce jeu de se déboguer et de se
  discuter ; sans graine, aucune partie n'est reproductible.
- **Le premier pas.** Le contrat de journal d'O1b **n'est pas encore
  écrit** : y ajouter la graine du tirage guidé maintenant coûte une
  ligne. L'ajouter après le passage à SQLite (M9) coûte une migration.
  Sans elle, « pourquoi il m'a sorti ça ce matin » est sans réponse.

### 4. La règle de croissance de la carte, avant le contenu

- **Le pattern.** Exercism : le syllabus se fait pousser depuis les
  concepts simples, on ne dessine pas l'arbre entier d'avance (§1.10).
- **La preuve.** C'est leur doctrine écrite, sur des dizaines de
  parcours de langages construits par des bénévoles — le cas exact de
  notre usine à domaine (SPEC §4).
- **Le premier pas.** Trancher **avant** d'écrire les cartes : ajouter
  40 cartes à une région conquise la fait retomber à 60 % et inflige au
  joueur une régression qu'il n'a pas méritée. Soit une région conquise
  le reste et l'ajout ouvre une sous-région, soit on l'assume et on
  l'explique. La règle va dans `gabarit-domaine/`, chantier O2 — c'est
  la SPEC §3 (« la carte est GIGANTESQUE en profondeur ») qui la rend
  inévitable.

### 5. Le fond de carte d'Azgaar, et l'invariant Duolingo à graver

- **Le pattern.** Un fond de carte MIT exporté en SVG donne en une
  soirée le « mode jeu vidéo » que JB exige, sans trois semaines de
  direction artistique (§3.2). Et le procès fait au chemin linéaire de
  Duolingo (§1.7) dit quoi ne pas faire ensuite.
- **La preuve.** Licence MIT dont le paragraphe additionnel donne
  explicitement les cartes produites ; et le reproche public le plus
  constant fait à Duolingo depuis 2022 est la perte de liberté de
  navigation.
- **Le premier pas.** Générer une carte, exporter le SVG, le
  retravailler comme fond de la carte 2,5D v1. Et durcir dans la SPEC
  la phrase « toute région visible est explorable » en **invariant**,
  avec le précédent Duolingo comme motif — c'est la première chose
  qu'on optimisera par erreur au nom de la clarté.

---

## Partie 6 — Ce qu'on a regardé et écarté, avec le motif

| Écarté | Motif |
|---|---|
| Half-life regression (Duolingo) comme planificateur | FSRS-6 est postérieur, mieux entraîné, déjà porté et testé chez nous. Changer serait une régression |
| Streak freeze / Streak Society | Rustine d'une punition qu'on n'a pas (notre compteur ne descend jamais). Chiffres non sourçables : blogs d'éditeurs vendant la fonctionnalité |
| Rétrogradation de rang façon WaniKani | Seconde comptabilité (interdite SPEC §3) et punitive (interdite MÉTHODE §9) |
| Chemin linéaire façon Duolingo 2022 | Contredit « toute région visible est explorable », et c'est le reproche public constant qui lui est fait |
| Code d'Anki, de Review Heatmap, du site d'Exercism | **AGPL-3.0**, copyleft fort (Review Heatmap ajoute des termes §7) |
| Watabou | Aucune licence formelle, permission contredite par l'auteur en forum |
| rot.js, honeycomb, d3-geo | Résolvent des problèmes qu'on n'a pas (FOV à la case, hexagones, projections géo) |
| pixi.js, phaser, konva, excalibur | Moteurs de rendu surdimensionnés avant toute mesure de perf |
| Génération procédurale de carte | Nos régions sont un contenu pédagogique écrit, pas un tirage |

---

## Ce que cette session n'a pas fait, exprès

- **Aucune dépendance npm installée**, aucun `package.json` touché.
- **Aucun composant front modifié** : une autre session travaille sur
  le front. On livre le carquois (33 SVG + CREDITS), pas le tir.
- **Aucune modification de SPEC-PRODUIT, METHODE, ROADMAP ni
  academie.json** : les recommandations de la partie 5 sont des
  propositions d'arbitrage pour JB, pas des faits accomplis.
- **Rien n'est committé.**

*Toute reprise de ce benchmark revérifie les licences à leur date :
elles changent d'une version à l'autre.*

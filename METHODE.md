# LA MÉTHODE — pourquoi l'Académie fait apprendre comme ça

Livrable nommé par JB le 30/08/2026 : « tous nos choix sourcés et
documentés dans une méthode lisible par tout le monde ». Ce document
est la version LISIBLE du cadrage scientifique
([`CADRAGE-SCIENTIFIQUE.md`](CADRAGE-SCIENTIFIQUE.md), bibliographie
re-sourcée et vérifiée le 28/08/2026) : une entrée par mécanique du
produit — *ce qu'on fait*, *pourquoi*, *la source*. La règle est
gravée dans la spec : **une mécanique qui n'arrive pas à écrire son
entrée ici n'entre pas dans le produit.** L'app renvoie vers cette
page (« pourquoi cette mécanique ? »).

Une source marquée `[À VÉRIFIER]` signale une entrée dont le principe
est établi mais dont la référence précise n'a pas encore été relue à
la source par un agent — la mécanique concernée reste en retrait tant
que ce n'est pas fait (même règle que pour les cartes).

---

## 1. Les révisions reviennent à intervalles croissants (FSRS)

**Ce qu'on fait** : chaque carte revient juste avant le moment où tu
l'aurais oubliée ; l'intervalle s'allonge à chaque rappel réussi. Le
planificateur est FSRS-6 (21 paramètres, modèle
difficulté-stabilité-récupérabilité), pas le vieux SM-2 d'Anki.
**Pourquoi** : la répétition espacée est l'effet le plus robuste de la
littérature ; FSRS réduit de 20 à 30 % le volume de révisions pour la
même rétention (90 %), et transforme un retard de révision en
consolidation au lieu d'une punition.
**Source** : Ye et al., ACM KDD / IEEE (2022-2024), corpus de plus de
700 M de révisions — vérifié 28/08/2026 ; portage maison comparé à
`py-fsrs` à 10⁻⁴ près (`app/tests_planificateur.py`).

## 2. On te fait répondre, jamais relire

**Ce qu'on fait** : tout passe par la récupération — te faire sortir
la réponse de ta tête (rappel libre, indicé, diagnostic), jamais par
la relecture de fiches.
**Pourquoi** : récupérer une information l'encode bien mieux que la
réétudier (tailles d'effet g = 0,50-0,70 en méta-analyse) ; la
relecture et le surlignage donnent une illusion de maîtrise mesurée.
**Source** : Rowland (2014), *Psychological Bulletin* ; Adesope et
al. (2017), *Review of Educational Research* ; Dunlosky et al. (2013)
pour l'illusion de la relecture — vérifiés 28/08/2026.

## 3. Les QCM ont des pièges expliqués

**Ce qu'on fait** : un QCM de l'Académie n'a jamais de mauvaises
réponses « de remplissage » : chaque distracteur est plausible et
porte son explication (« pourquoi c'est faux »).
**Pourquoi** : un QCM évident ne demande que de la reconnaissance,
quasi inutile ; la discrimination entre options plausibles force la
reconstruction. Le contrat de carte l'impose mécaniquement (le
valideur refuse un QCM sans distracteurs expliqués).
**Source** : Rowland (2014) sur reconnaissance vs rappel — vérifié
28/08/2026.

## 4. Après une erreur : l'explication tout de suite, puis la carte revient

**Ce qu'on fait** : une erreur déclenche immédiatement la
micro-explication (3 lignes), la source de la carte, et le champ
optionnel « pourquoi je me suis trompé ? » (le carnet d'erreurs). La
carte ratée revient vite.
**Pourquoi** : l'effet d'hypercorrection — les erreurs commises avec
confiance sont les mieux corrigées, à condition d'un feedback
immédiat et explicatif ; la surprise crée un pic d'attention qu'il ne
faut pas gaspiller. Le feedback efficace porte sur le processus,
jamais sur la personne.
**Source** : Butterfield & Metcalfe (2001, 2006) ; Hattie &
Timperley (2007), d = 0,79 pour le feedback ciblé — vérifiés
28/08/2026.

## 5. Trois échecs sur la même carte = mini-leçon

**Ce qu'on fait** : une carte ratée 3 fois sort du simple cycle et
déclenche autre chose (mini-leçon, carte préalable) — la note du
carnet d'erreurs oriente quoi.
**Pourquoi** : répéter un échec à l'identique n'apprend rien ; c'est
le signal qu'un prérequis manque (échafaudage à reconstruire).
**Source** : Sweller (1988-2019), théorie de la charge cognitive et
exemples résolus — vérifié 28/08/2026.

## 6. Les matières s'entremêlent dans la séance

**Ce qu'on fait** : une séance mélange les domaines et les types au
lieu de faire des blocs (« tout droit », puis « tout technique »).
**Pourquoi** : la pratique en blocs donne une forte impression de
compétence et un transfert médiocre ; l'entrelacement force à
discriminer ce qui se ressemble.
**Source** : Bjork & Bjork (2011), difficultés désirables ; Carvalho
& Goldstone (2014) — vérifiés 28/08/2026.

## 7. L'algo est le prof : tu ne choisis jamais le format

**Ce qu'on fait** : tu cliques une zone (ou « au hasard »),
et le moteur enchaîne les formats — QCM, image, document à expliquer,
mise en situation — sans te demander ton avis.
**Pourquoi** : laisser l'élève choisir sa méthode produit exactement
les mauvais choix (relecture, blocs, QCM faciles : les stratégies les
plus agréables sont les moins efficaces, c'est mesuré). Le choix qui
te reste est celui qui motive sans nuire : OÙ aller sur la carte.
**Source** : Dunlosky et al. (2013) sur l'inefficacité des stratégies
auto-choisies ; Bjork & Bjork (2011) — vérifiés 28/08/2026.

## 8. Le matin, court ; le reste quand on a le temps (amendé le 02/09/2026)

**Ce qu'on fait** : la séance du matin vise 8 à 20 minutes, sans
verrou dur : la clôture est honorable à tout moment, cinq cartes valent
une séance. Deux formats longs existent, l'étude (45 à 90 min) et la
journée, avec **le neuf plafonné par jour** quel que soit le format
(`decisions/0005`).
**Pourquoi** : le rituel court est ce qui survit à une vie de bureau,
et c'est lui qui fait travailler l'espacement. La pratique massée est
inférieure à la pratique distribuée pour la rétention, donc une longue
journée ne doit pas bourrer de cartes neuves : elle dépense son temps
en compréhension et en production. La thèse de l'épuisement des
ressources exécutives, qui fondait le plafond dur de 15 minutes, a mal
survécu à sa réplication : elle ne justifie plus un verrou.
**Source** : Cepeda et al. (2006), *Psychological Bulletin*, 839
comparaisons, vérifié 28/08/2026 ; Pruessner, Lupien et al. (1997,
2007) sur la réponse cortisol du réveil, vérifié 28/08/2026 (le matin
reste un bon moment, pas une obligation) ; Hagger et al. (2016),
réplication multi-laboratoires préenregistrée de l'ego depletion,
*Perspectives on Psychological Science* `[À VÉRIFIER : référence
citée de mémoire le 02/09, à relire avant de la citer dans l'app]`.

## 9. La série ne casse jamais, la dette n'existe pas

**Ce qu'on fait** : le compteur monte, il ne descend jamais ; une
coupure (saison d'AG, vacances) se résorbe par ré-étalement
automatique, jamais par une pile de retard affichée.
**Pourquoi** : la gamification punitive détruit la motivation
intrinsèque (effet de surjustification) ; la honte du streak cassé
fait abandonner, elle ne fait pas revenir.
**Source** : Deci, Koestner & Ryan (1999), méta-analyse SDT — vérifié
28/08/2026.

## 10. L'épreuve de domaine est un examen à froid

**Ce qu'on fait** : le 100 % d'une région n'existe qu'après un examen
(cartes tirées à froid, score solennel) ; sans lui, plafond à 99 %.
**Pourquoi** : le test EST l'apprentissage (practice testing), et
l'examen à froid mesure la rétention réelle, pas la performance à
chaud de la séance — c'est la différence que les difficultés
désirables enseignent.
**Source** : Adesope et al. (2017) ; Bjork & Bjork (2011) — vérifiés
28/08/2026.

## 11. L'arbre est un lieu stable (amendé le 02/09/2026)

**Ce qu'on fait** : chaque savoir a une place fixe sur l'arbre du
métier (domaine, branche, nœud, distance au tronc) et cette place ne
bouge pas : on retrouve « la compta en bas à gauche, les majorités près
du tronc ». L'habillage « immeuble en coupe » (palais de mémoire) est
gravé comme idée et différé derrière l'arbre lui-même.
**Pourquoi** : l'ancrage spatial des connaissances exploite la mémoire
spatiale, très puissante chez l'humain ; une disposition stable est la
condition de cet ancrage, quel que soit le décor.
**Source** : Maguire et al. (2003), *Nature Neuroscience*, « Routes
to remembering » `[À VÉRIFIER, référence à relire à la source avant
de s'en réclamer dans l'app]`.

## 12. Certains exercices sont chronométrés, d'autres jamais

**Ce qu'on fait** : les automatismes (vocabulaire, réflexes de
diagnostic) se travaillent parfois en temps court ; l'analyse
(réponse libre, ateliers, documents) jamais.
**Pourquoi** : la fluence — produire vite et sans effort — est une
composante mesurable de l'expertise, distincte de la justesse ; mais
chronométrer l'analyse ne produit que du stress sans apprentissage.
**Source** : Binder (1996), « Behavioral fluency: evolution of a new
paradigm », *The Behavior Analyst* 19, 163-197, vérifié 02/09/2026 :
la fluence (justesse plus vitesse) prédit la rétention, l'endurance et
le transfert mieux que la justesse seule. Le chrono ne s'active que
sur des automatismes d'une branche déjà solide.

## 13. Les images montrent, le texte explique — jamais en double

**Ce qu'on fait** : les schémas (coupe de VMC, frise de procédure)
sont épurés, légendés au bon endroit, et la question porte sur ce que
l'image montre.
**Pourquoi** : la contiguïté spatiale (l'étiquette SUR le schéma, pas
dans un pavé à côté) et la signalisation réduisent la charge inutile
et améliorent le transfert (d = 0,38 pour la signalisation).
**Source** : Mayer & Fiorella (2021) ; Schneider et al. (2018) —
vérifiés 28/08/2026.

## 14. Le quiz de positionnement t'évite de retaper les bases

**Ce qu'on fait** : ~20 questions au premier lancement ; une bonne
réponse inscrit la carte comme déjà stabilisée (21 j, paramétré,
marquée `origine: quiz`), une mauvaise n'inscrit rien, et le quiz
ouvre des branches sans jamais écrire leur remplissage.
**Pourquoi** : évaluer le niveau réel avant de dérouler évite l'ennui
(le tueur de rituel n°1 chez quelqu'un qui sait déjà) sans jamais
« valider » : seule la mesure FSRS au fil des séances fait foi.
**Source** : mécanique dérivée du testing effect (Rowland 2014) ;
calibrage mesuré au pré-mortem du 29/08 (la stabilité standard d'une
première révision n'est que de ~2 jours — mesuré sur le moteur).

## 15. Les « dark patterns », assumés et bornés

**Ce qu'on fait** : brouillard de l'arbre, épreuves, tirage,
insignes — les mécaniques d'engagement des jeux, utilisées
délibérément pour ramener chaque matin.
**Pourquoi** : le rituel quotidien est la condition de tout le reste
(l'espacement ne marche que si on revient) ; on met l'engagement au
service de l'apprentissage, jamais l'inverse. Les bornes sont
gravées : jamais de culpabilisation, jamais de dette, jamais de
comparaison imposée, défis coupés si les données montrent qu'ils
dégradent le rituel, et la récompense qui compte ouvre du contenu.
**Source** : Deci, Koestner & Ryan (1999) pour les bornes — vérifié
28/08/2026 ; arbitrages JB des 29-30/08 pour le cap.

## 16. Le concret avant la théorie : l'amorce (ajouté le 02/09/2026)

**Ce qu'on fait** : un chapitre s'ouvre sur un problème à tenter
(« laquelle de ces trois fissures appelle un expert dans la semaine ? »)
avant toute leçon. Se tromper y est prévu.
**Pourquoi** : résoudre avant d'être instruit prépare l'encodage de la
leçon (on remarque ce qu'on ne savait pas) et améliore la compréhension
et le transfert, pas seulement la rétention.
**Source** : Sinha & Kapur (2021), *Review of Educational Research*,
méta-analyse de 53 études, g = 0,36 en faveur de « problème puis
instruction » ; vérifié 02/09/2026.

## 17. Le rappel bat l'élaboration, même pour comprendre (ajouté le 02/09/2026)

**Ce qu'on fait** : on ne remplace jamais les cartes par des schémas à
compléter ou des cartes mentales « pour comprendre » ; comprendre passe
aussi par répondre.
**Pourquoi** : le rappel produit plus d'apprentissage que l'étude
élaborative par carte conceptuelle, y compris sur des questions
d'inférence, et même quand le test final est une carte conceptuelle.
**Source** : Karpicke & Blunt (2011), *Science* 331, 772-775 ; vérifié
02/09/2026.

## 18. La synthèse : s'expliquer à soi-même (ajouté le 02/09/2026)

**Ce qu'on fait** : tout chapitre se clôt par une production (une
phrase, une explication, une note) relue contre une liste de contrôle.
À partir du niveau 3 la synthèse devient l'exercice dominant.
**Pourquoi** : inciter à s'auto-expliquer améliore l'apprentissage
substantiellement, dans des conditions très variées.
**Source** : Bisra et al. (2018), *Educational Psychology Review*,
méta-analyse, g = 0,55 ; Chi et al. (1989) pour l'effet initial ;
vérifiés 02/09/2026.

## 19. Expliquer à quelqu'un (ajouté le 02/09/2026)

**Ce qu'on fait** : la synthèse de niveau 2 est « explique-le à un
collègue en soixante secondes » ; les défis entre joueurs et, plus tard,
la contribution d'un chapitre en sont la version réelle.
**Pourquoi** : se préparer à enseigner aide à court terme ; enseigner
réellement ajoute un bénéfice qui dure.
**Source** : Fiorella & Mayer (2013), *Contemporary Educational
Psychology* 38, 281-288 ; vérifié 02/09/2026.

## 20. Le papier : dessiner, oui ; écrire à la main, pas prouvé (ajouté le 02/09/2026)

**Ce qu'on fait** : deux exercices sur papier, le dessin de mémoire
(un caisson de VMC, un circuit de recouvrement) et la feuille blanche
(rappel libre en temps borné), corrigés par liste de contrôle. Aucune
promesse sur « écrire à la main pour mieux retenir ».
**Pourquoi** : dessiner un item bat l'écrire, souvent du simple au
double en rappel libre ; la prise de notes manuscrite, elle, ne
réplique pas sa supériorité.
**Source** : Wammes, Meade & Fernandes (2016), *QJEP* ; Fernandes,
Wammes & Meade (2018), *Current Directions* ; Morehead, Dunlosky &
Rawson (2019), *Educational Psychology Review* ; vérifiés 02/09/2026.

## 21. La journée : du temps pour comprendre, pas pour bourrer (ajouté le 02/09/2026)

**Ce qu'on fait** : une demi-journée ou une journée enchaîne des études
sur deux ou trois domaines, avec des pauses, un rappel en fin de journée
sur les chapitres du matin, et un plafond de cartes neuves par jour.
**Pourquoi** : la pratique massée est inférieure à la pratique
distribuée pour la rétention ; c'est le neuf qui fabrique la dette de
révisions, pas la compréhension. Espacer les reprises dans la journée
et entrelacer les domaines garde ce que la science donne.
**Source** : Cepeda et al. (2006), *Psychological Bulletin* ; Rohrer &
Taylor (2007) pour l'entrelacement ; vérifiés 28/08/2026.

## 22. Dire sa confiance avant de répondre (ajouté le 02/09/2026)

**Ce qu'on fait** : sur un cas ou un QCM de niveau 2 et plus, le joueur
dit s'il est sûr avant de révéler. Le profil affiche sa calibration.
**Pourquoi** : une erreur confiante est mieux corrigée qu'une erreur
hésitante, à condition d'un retour immédiat ; et savoir quand on ne
sait pas est la compétence d'un professionnel qui vérifie.
**Source** : Butterfield & Metcalfe (2001, 2006), vérifiés 28/08/2026 ;
la calibration est mesurée au journal, elle n'est pas promise.

## 23. Le socle protégé, la liberté ailleurs (ajouté le 02/09/2026)

**Ce qu'on fait** : tant que le socle n'est pas validé, la moitié du
neuf d'une séance vient de la branche du socle la moins avancée ;
l'étude est libre ; on ne bloque jamais.
**Pourquoi** : le choix auto-régulé tend vers ce qu'on aime et vers les
illusions de maîtrise ; bloquer détruit l'autonomie, qui est un besoin
de base de la motivation. Pondérer sans bloquer respecte les deux.
**Source** : Dunlosky et al. (2013) sur les stratégies auto-choisies ;
Deci, Koestner & Ryan (1999) sur l'autonomie ; vérifiés 28/08/2026.

## 24. Les niveaux 4 et 5 : l'expertise n'est pas du drill (ajouté le 02/09/2026)

**Ce qu'on fait** : au-delà du praticien, l'arbre monte vers la
doctrine, les cas réels, la controverse et la contribution, pas vers
plus de cartes.
**Pourquoi** : la pratique délibérée explique une part de la
performance dans les jeux et la musique, mais très peu dans les
professions ; l'expertise professionnelle vient du jugement sur des cas
et de la connaissance du débat.
**Source** : Ericsson, Krampe & Tesch-Römer (1993) ; Macnamara,
Hambrick & Oswald (2014), méta-analyse (moins de 1 % de variance
expliquée dans les professions) ; vérifiés 02/09/2026.

## 25. La variété des formats (ajouté le 02/09/2026)

**Ce qu'on fait** : jamais deux formats identiques d'affilée quand la
matière le permet, au moins trois types par séance, et les formats
riches (cas, lecture, jeu de rôle) arrivent avec les niveaux.
**Pourquoi** : c'est une règle de conception, pas un effet mesuré en
laboratoire : elle prolonge l'entrelacement (§6) et se juge au journal
(abandons par format). Un format qui lasse se coupe.
**Source** : Bjork & Bjork (2011) pour l'entrelacement ; la mesure des
abandons par format est la source du reste (`rapport_rituel.py`).

## 26. Les épreuves transverses (ajouté le 02/09/2026)

**Ce qu'on fait** : un dossier en cinq pas qui mêle au moins trois
domaines, une décision à chaque pas ; l'épreuve du gestionnaire en
compte trois.
**Pourquoi** : sur le terrain les problèmes n'arrivent pas rangés par
matière ; tester le transfert, c'est tester dans un contexte qui ne
ressemble pas à l'entraînement.
**Source** : Bjork & Bjork (2011), difficultés désirables ; Barnett &
Ceci (2002) pour la taxonomie du transfert `[À VÉRIFIER : cité de
mémoire le 02/09]`.

## 27. Les points sont dérivés, la ligue compte des cartes stabilisées (ajouté le 02/09/2026)

**Ce qu'on fait** : une carte stabilisée vaut dix fois son niveau ; la
ligue hebdomadaire compte les cartes stabilisées × niveau ; jamais le
temps, jamais les clics ; jamais de monnaie.
**Pourquoi** : une mesure qu'on peut gagner sans apprendre devient un
objectif et cesse de mesurer (Goodhart) ; les récompenses extrinsèques
futiles détruisent la motivation intrinsèque ; ce qui ouvre du contenu
dure.
**Source** : Deci, Koestner & Ryan (1999), vérifié 28/08/2026 ;
`labor/wiki/patterns/mesure-objectif-goodhart.md`.

## 28. La semaine type (ajouté le 02/09/2026)

**Ce qu'on fait** : des jours colorés (fondations, cours, terrain,
exploration, étude, libre) qui pèsent sur le neuf et les formats ;
les révisions dues sont servies tous les jours.
**Pourquoi** : une habitude tient à un déclencheur stable ; un rythme
hebdomadaire lisible en est un, et la variété entre jours prolonge
l'entrelacement sans folklore.
**Source** : règle de conception ; Lally et al. (2010) sur la formation
des habitudes `[À VÉRIFIER : cité de mémoire le 02/09]` ; la mesure au
journal (`jour` sur chaque séance) tranchera.

## 29. Le professeur a un dossier, pas un diplôme (ajouté le 02/09/2026)

**Ce qu'on fait** : chaque carte dit qui l'a écrite (modèle ou humain,
date), combien de sources l'adossent, qui l'a relue, quand elle a été
vérifiée, et porte une note A, B ou C dérivée de tout ça. Chaque domaine
a sa page « Pourquoi croire ce professeur ? » avec ses chiffres, ses
erreurs connues et ses limites ; un second modèle, d'un autre
fournisseur, relit un échantillon chaque mois.
**Pourquoi** : un modèle n'a pas de diplôme ; ce qui se juge, c'est un
procédé et des résultats. Rendre visibles la provenance, le taux
d'erreur trouvé et le délai de correction est ce qui permet à un adulte
de décider de sa confiance, et de se méfier au bon endroit. Ce n'est
pas une mécanique d'apprentissage, c'est la condition pour qu'on
accepte d'apprendre.
**Source** : règle de conception (`decisions/0021`, `0022`) ; les
patterns de labor « validated sans lien ne vaut rien » et « un rapport
de LLM vaut par ses questions » (`labor/wiki/patterns/`).

## 30. La fiche se lit après, jamais avant (ajouté le 02/09/2026)

**Ce qu'on fait** : chaque chapitre a sa fiche de rappel (la leçon et la
liste question-réponse de ses cartes), lisible à tout moment depuis le
nœud, proposée quand un nœud passe « à revoir » et la veille d'une
épreuve ; elle n'ouvre jamais une séance et ne remplace jamais une
carte.
**Pourquoi** : relire n'apprend pas (§2), mais relire **après** avoir
tenté de se souvenir, ou pour réactiver un savoir périmé avant de le
tester, n'est pas de la relecture passive : c'est le retour d'information
qui suit le rappel. « Relis trois minutes, puis cinq cartes » est un
rappel avec feedback, pas une lecture.
**Source** : Roediger & Karpicke (2006) sur la relecture qui gagne au
test immédiat et perd au test différé ; Hattie & Timperley (2007) sur le
feedback ; vérifiés 28/08/2026.

## 31. Les petits leviers d'engagement, et leurs bornes (ajouté le 02/09/2026)

**Ce qu'on fait** : une mission par semaine qui donne un insigne ; une
notification par jour au plus, opt-in, silencieuse si la séance est
faite ; le calendrier du métier qui pèse en silence sur le neuf ; le
bilan du mois, privé, et sa carte partageable sans aucune erreur ; le
fil des jalons et les kudos dans le cercle.
**Pourquoi** : ce sont des déclencheurs et des signes de reconnaissance,
pas des récompenses ; ils soutiennent l'habitude sans créer de dette ni
de comparaison imposée. Chacun se coupe d'office pour un joueur dont il
dégrade le rituel mesuré, et aucun ne donne de points.
**Source** : Deci, Koestner & Ryan (1999) pour les bornes, vérifié
28/08/2026 ; la mesure au journal (`rapport_rituel.py`) pour le reste ;
`decisions/0014`, `0016`, `0020`.

## 32. Le pas à pas imposé et les points de sauvegarde (ajouté le 03/09/2026)

**Ce qu'on fait** : tout travail long d'un modèle (lire un document,
écrire un lot, coder un chantier) est découpé par un script en unités
que le modèle ne dimensionne pas ; chaque unité est jugée par la machine
contre un témoin (le texte extrait de la page) avant que la suivante
s'ouvre ; chaque unité validée est écrite sur disque avec un sceau, et
les contrôles sont rejoués à chaque reprise. Le modèle se déclare
(outil, modèle, classe) et la taille des unités suit ses résultats.
**Pourquoi** : la lecture d'un long contexte se dégrade avec la position
et la longueur, même quand la fenêtre annoncée suffit ; un résumé de
modèle ajoute un fait absent de la source dans environ un cas sur dix,
même pour les meilleurs ; et un modèle ne détecte pas ces deux défauts
de l'intérieur. Le pas à pas rend chaque erreur locale et visible, le
point de sauvegarde rend la coupure sans coût, la revérification rend
l'autovalidation inutile.
**Source** : Liu et al., « Lost in the Middle: How Language Models Use
Long Contexts », TACL 2024 (arXiv 2307.03172), vérifié 03/09/2026 ;
tableau Vectara des hallucinations (HHEM-2.3), mis à jour le
11/05/2026, lu le 03/09/2026 ; MRCR à huit aiguilles (rapport Google
Gemini 2.5, lu par yage.ai le 03/09/2026, `[À VÉRIFIER]` à la source) ;
`MODELES.md` §4 ; `decisions/0027`.

---

*Toute nouvelle mécanique ajoute son entrée ICI dans le même commit
que son code ; sinon elle n'existe pas.*

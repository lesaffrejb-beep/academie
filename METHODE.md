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

**Ce qu'on fait** : tu cliques une zone (ou l'expédition aléatoire),
et le moteur enchaîne les formats — QCM, image, document à expliquer,
mise en situation — sans te demander ton avis.
**Pourquoi** : laisser l'élève choisir sa méthode produit exactement
les mauvais choix (relecture, blocs, QCM faciles : les stratégies les
plus agréables sont les moins efficaces, c'est mesuré). Le choix qui
te reste est celui qui motive sans nuire : OÙ aller sur la carte.
**Source** : Dunlosky et al. (2013) sur l'inefficacité des stratégies
auto-choisies ; Bjork & Bjork (2011) — vérifiés 28/08/2026.

## 8. Le matin, 15 minutes, pas plus

**Ce qu'on fait** : la séance vise ~15 minutes vers 8h15, avec un
plafond dur ; le « mode 3 minutes » (5 révisions) est une séance
valide.
**Pourquoi** : le pic de cortisol du réveil optimise l'encodage
préfrontal et hippocampique ; au-delà d'un quart d'heure quotidien on
entame les ressources d'autorégulation de la journée — et on tue le
rituel, qui est la seule chose qui compte vraiment.
**Source** : Pruessner, Lupien et al. (1997, 2007) sur la réponse
cortisol du réveil ; Baumeister & Vohs (2016) sur l'épuisement
exécutif — vérifiés 28/08/2026.

## 9. La série ne casse jamais, la dette n'existe pas

**Ce qu'on fait** : le compteur monte, il ne descend jamais ; une
coupure (saison d'AG, vacances) se résorbe par ré-étalement
automatique, jamais par une pile de retard affichée.
**Pourquoi** : la gamification punitive détruit la motivation
intrinsèque (effet de surjustification) ; la honte du streak cassé
fait abandonner, elle ne fait pas revenir.
**Source** : Deci, Koestner & Ryan (1999), méta-analyse SDT — vérifié
28/08/2026.

## 10. Le boss de région est un examen à froid

**Ce qu'on fait** : le 100 % d'une région n'existe qu'après un examen
(cartes tirées à froid, score solennel) ; sans lui, plafond à 99 %.
**Pourquoi** : le test EST l'apprentissage (practice testing), et
l'examen à froid mesure la rétention réelle, pas la performance à
chaud de la séance — c'est la différence que les difficultés
désirables enseignent.
**Source** : Adesope et al. (2017) ; Bjork & Bjork (2011) — vérifiés
28/08/2026.

## 11. La carte est un lieu (l'immeuble, l'hôpital)

**Ce qu'on fait** : le savoir s'ancre dans un lieu navigable — pour
la copro, l'immeuble (la toiture = étanchéité, la chaufferie =
P1-P5…) ; chaque métier aura son lieu-monde.
**Pourquoi** : la méthode des lieux (palais de mémoire) — l'ancrage
spatial des connaissances exploite la mémoire spatiale, très
puissante chez l'humain ; c'est la technique des champions de
mémoire, documentée en imagerie.
**Source** : Maguire et al. (2003), *Nature Neuroscience*, « Routes
to remembering » `[À VÉRIFIER — référence à relire à la source avant
de construire l'habillage lieu-monde]`.

## 12. Certains exercices sont chronométrés, d'autres jamais

**Ce qu'on fait** : les automatismes (vocabulaire, réflexes de
diagnostic) se travaillent parfois en temps court ; l'analyse
(réponse libre, ateliers, documents) jamais.
**Pourquoi** : la fluence — produire vite et sans effort — est une
composante mesurable de l'expertise, distincte de la justesse ; mais
chronométrer l'analyse ne produit que du stress sans apprentissage.
**Source** : `[À VÉRIFIER — littérature fluence/automaticité à
sourcer proprement avant d'activer les niveaux chronométrés]`.

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
OUVRE des régions sans jamais écrire leur remplissage.
**Pourquoi** : évaluer le niveau réel avant de dérouler évite l'ennui
(le tueur de rituel n°1 chez quelqu'un qui sait déjà) sans jamais
« valider » : seule la mesure FSRS au fil des séances fait foi.
**Source** : mécanique dérivée du testing effect (Rowland 2014) ;
calibrage mesuré au pré-mortem du 29/08 (la stabilité standard d'une
première révision n'est que de ~2 jours — mesuré sur le moteur).

## 15. Les « dark patterns », assumés et bornés

**Ce qu'on fait** : brouillard de carte, citadelles de boss, tirage,
cosmétiques de zone — les mécaniques d'engagement des jeux, utilisées
délibérément pour ramener chaque matin.
**Pourquoi** : le rituel quotidien est la condition de tout le reste
(l'espacement ne marche que si on revient) ; on met l'engagement au
service de l'apprentissage, jamais l'inverse. Les bornes sont
gravées : jamais de culpabilisation, jamais de dette, jamais de
comparaison imposée, défis coupés si les données montrent qu'ils
dégradent le rituel, et la récompense qui compte ouvre du contenu.
**Source** : Deci, Koestner & Ryan (1999) pour les bornes — vérifié
28/08/2026 ; arbitrages JB des 29-30/08 pour le cap.

---

*Toute nouvelle mécanique ajoute son entrée ICI dans le même commit
que son code — sinon elle n'existe pas.*

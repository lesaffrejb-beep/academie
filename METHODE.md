# La méthode : pourquoi l’Académie propose ces exercices

Une entrée par mécanique : ce que le produit prévoit, la preuve disponible,
et ce qui reste un choix de conception. Cette méthode ne décrit pas à elle
seule l’état du logiciel livré ; `roadmap.json` et ses preuves font foi.
Les durées, quotas et seuils cités sont des paramètres produit, sauf source
explicite. Aucun effet moyen publié ne garantit un résultat individuel.

Révision critique du 05/09/2026, chantier `ACA-METHODE-2`. Les populations,
comparaisons et limites figurent dans [le cadrage](CADRAGE-SCIENTIFIQUE.md).
Les niveaux de consultation sont consignés dans
[le rapport](travail/relecture-science-2026-09-05.md). Une source retrouvée
n’est pas une lecture intégrale certifiée par l’usine. Les anciennes dates
ci-dessous sont historiques ; elles ne valent pas nouvelle vérification.
Une référence `[À VÉRIFIER]` ne fonde aucune promesse affichée dans l’app.

## 1. Les révisions sont planifiées avec FSRS

**Ce qu’on fait** : FSRS-6 estime un intervalle à partir de l’historique
et d’une cible de rappel. Il estime une probabilité, sans connaître le
moment exact de ton oubli.
**Pourquoi** : l’espacement est soutenu par la recherche sur la rétention.
La fidélité de notre portage à une implémentation de référence est une
preuve technique, pas un gain pédagogique mesuré. Aucun pourcentage de
révisions économisées n’est promis ; charge et rappel différé se mesurent.
**Source** : documentation des auteurs de [FSRS](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)
et Cepeda et al. (2006), sources R1/R2 du cadrage. Un retard réussi met à
jour l’estimation de stabilité ; il ne garantit pas une meilleure mémoire.

## 2. Répondre, puis comprendre et reprendre

**Ce qu’on fait** : une séance commence par une tentative ; la leçon,
les exemples et la correction aident à comprendre, puis vient un rappel.
**Pourquoi** : les tests de récupération bénéficient en moyenne à la
rétention par rapport à la réétude dans les comparaisons étudiées. Lire
reste utile pour acquérir une connaissance ou comprendre une explication.
La sensation de familiarité ne suffit pas à établir qu’on saura rappeler.
**Source** : Rowland (2014) et Dunlosky et al. (2013), R3/R4 du cadrage.

## 3. Les QCM ont des options plausibles et expliquées

**Ce qu’on fait** : chaque distracteur porte son explication ; la banque
passe les contrôles du contrat de carte.
**Pourquoi** : choisir entre des options permet aussi d’apprendre. Le
rappel généré bénéficie davantage au rappel ultérieur dans les études
synthétisées par Rowland ; cela ne rend pas la reconnaissance inutile.
Un QCM seul ne démontre ni rappel libre ni décision en situation nouvelle.
**Source** : Rowland (2014), R3 ; qualité des distracteurs : choix éditorial.

## 4. Après une erreur : une explication et un nouvel essai

**Ce qu’on fait** : correction, source et note privée facultative sur
l’erreur ; la carte revient. Le retour porte sur la réponse et la démarche.
**Pourquoi** : dans les expériences d’hypercorrection, les erreurs
confiantes ont été plus souvent corrigées au test suivant. Cela ne garantit
pas le résultat de chaque joueur ; le résumé ne démontre pas que seul un
retour immédiat et explicatif produit cet effet. Le retour immédiat est
notre choix pour rendre l’erreur compréhensible dans la séance.
**Source** : Butterfield & Metcalfe (2001), R5. Hattie & Timperley (2007),
référence complémentaire R15 ; aucun effet chiffré attribué à notre feedback.

## 5. Les erreurs répétées conduisent à une autre aide

**Ce qu’on fait** : trois échecs déclenchent une mini-leçon ou une carte
préalable dans la conception ; la note du carnet peut guider la reprise.
**Pourquoi** : un échec peut venir d’un prérequis, d’une formulation ou
d’une stratégie. Le seuil de trois est un choix à éprouver, pas un
résultat de la théorie de la charge cognitive.
**Source** : Sweller et al. (2019), référence complémentaire R16 pour le
guidage et les exemples ; le diagnostic reste à vérifier sur la carte.

## 6. Entrelacer ce qu’il faut apprendre à distinguer

**Ce qu’on fait** : la séance varie domaines et formats ; les contenus
proposent aussi des cas proches à comparer.
**Pourquoi** : le bénéfice de l’entrelacement dépend du matériel et de sa
similarité. Distinguer deux règles proches a une raison pédagogique ;
changer arbitrairement de sujet à chaque écran n’est pas le même test.
Une procédure peut demander une séquence suivie avant d’être mélangée.
**Source** : Brunmair & Richter (2019), R6 ; la diversité de la séance
reste un choix produit à observer.

## 7. Le moteur choisit le format, le joueur choisit sa direction

**Ce qu’on fait** : le joueur choisit où apprendre et le temps disponible ;
le moteur compose les formats conformément à `DOCTRINE.md` §3.5.
**Pourquoi** : c’est un arbitrage produit pour guider la séance. La revue
des stratégies d’étude ne prouve ni que chacun choisit mal, ni que retirer
le choix des formats améliore l’apprentissage. La recommandation doit
rester compréhensible et le guidage adapté aux prérequis.
**Source** : Dunlosky et al. (2013), R4, pour les stratégies ; doctrine
pour la répartition du choix. Aucun invariant n’est modifié ici.

## 8. Un créneau viable, des séances fractionnables

**Ce qu’on fait** : séance courte visée de 8 à 20 minutes ; étude de
45 à 90 minutes et journée quand on le souhaite, avec clôture possible
et plafond de neuf (`decisions/0005`). Ces durées sont des choix produit.
**Pourquoi** : espacer les reprises soutient la rétention. Le matin est
une préférence de rituel, sans preuve d’un horaire optimal dérivé du
cortisol. La réplication de Hagger ne justifie aucun verrou à quinze
minutes et ne démontre pas non plus que la fatigue n’existe pas.
**Source** : Cepeda et al. (2006), Pruessner et al. (1997), Hagger et al.
(2016), R2/R7/R8. Aucun gain local de régularité encore revendiqué.

## 9. La progression ne punit pas les absences

**Ce qu’on fait** : compteur cumulatif, reprises réétalées, aucune pile
de retard culpabilisante.
**Pourquoi** : « jamais de dette, jamais de honte » est une valeur de la
doctrine. Deci et al. étudient des récompenses précises ; ils ne démontrent
pas que chaque compteur interrompu provoque l’abandon de chaque adulte.
**Source** : `DOCTRINE.md` §3.9 ; Deci et al. (1999), R9, pour les limites
des récompenses, pas pour une causalité universelle des absences.

## 10. L’épreuve examine ce qui reste sans aide

**Ce qu’on fait** : un examen à froid conditionne le plein avancement
d’une région dans la conception ; sources après la réponse.
**Pourquoi** : différer le test distingue mieux la performance immédiate
de la rétention. Une épreuve échantillonne un contenu ; elle ne mesure pas
tout le métier. Les seuils de progression sont des conventions produit.
**Source** : Rowland (2014), R3 ; cas nouveaux et mesure distincte du
transfert dans `ACA-TRANSFERT-1`.

## 11. L’arbre garde des repères stables

**Ce qu’on fait** : domaines, branches et chapitres gardent une place
prévisible ; l’habillage spatial peut évoluer avec les décisions produit.
**Pourquoi** : aider à s’orienter est l’objectif ergonomique. L’étude de
Maguire concerne des experts de la mémoire utilisant des stratégies
spatiales ; un menu organisé ne reproduit pas cet entraînement.
**Source** : Maguire et al. (2003), R10. Le bénéfice mémoriel de notre
arbre n’est pas établi ; il ne sert pas d’argument à une promesse.

## 12. Distinguer vitesse et justesse

**Ce qu’on fait** : les automatismes peuvent être chronométrés après
acquisition ; l’analyse reste sans pression temporelle imposée.
**Pourquoi** : la vitesse et la justesse sont deux observations différentes.
Le retrait du chrono sur l’analyse est un choix de confort et de guidage,
pas la preuve que tout chronométrage empêche d’apprendre.
**Source** : Binder (1996), référence complémentaire R17. Le transfert
d’un automatisme rapide à une décision professionnelle doit être éprouvé.

## 13. Une image sert la question

**Ce qu’on fait** : schémas lisibles, légendes proches, indices utiles,
texte accessible et représentations adaptées à la notion.
**Pourquoi** : signalisation et contiguïté peuvent aider à relier les
éléments. Cela n’interdit ni photographie, ni légende séparée, ni animation ;
le choix dépend du contenu, de l’écran et de l’accessibilité. La qualité
graphique ne supprime pas toute charge cognitive et doit être examinée.
**Source** : Mayer & Fiorella (2021), Schneider et al. (2018), références
complémentaires R18/R19 ; aucun effet chiffré propre au front annoncé.

## 14. Le quiz de positionnement t'évite de retaper les bases

**Ce qu'on fait** : ~20 questions au premier lancement ; une bonne
réponse inscrit la carte comme déjà stabilisée (21 j, paramétré,
marquée `origine: quiz`), une mauvaise n'inscrit rien, et le quiz
ouvre des branches sans jamais écrire leur remplissage.
**Pourquoi** : éviter des répétitions perçues comme inutiles est l’objectif produit.
Une réponse juste ne suffit pas à établir le niveau réel ; le paramètre
d’initialisation reste une hypothèse à confronter aux rappels ultérieurs.
**Source** : mécanique dérivée du testing effect (Rowland 2014) ;
calibrage mesuré au pré-mortem du 29/08 (la stabilité standard d'une
première révision n'est que de ~2 jours — mesuré sur le moteur).

## 15. Un engagement qui sert l’apprentissage

**Ce qu’on fait** : progression, découverte, insignes et épreuves doivent
donner envie de revenir. Leur effet se juge sur l’usage et les acquis.
**Pourquoi** : la gamification peut aider, avec des résultats variables.
Une interface attrayante et une activité utile peuvent coexister. Ni
badges nécessairement nocifs, ni progression visuelle nécessairement efficace.
**Source** : Sailer & Homner (2020), R12 ; les bornes anti-honte sont
celles de `DOCTRINE.md`, sans dépendre d’un bénéfice expérimental garanti.

## 16. Une tentative avant l’explication, avec du guidage

**Ce qu’on fait** : un problème court ouvre le chapitre, puis viennent
l’explication, un exemple et un nouvel essai. Une aide reste possible.
**Pourquoi** : problème puis instruction obtient un avantage moyen dans
la synthèse de Sinha & Kapur, sous conditions de conception. L’ordre des
étapes seul ne suffit pas ; laisser un novice sans prise n’est pas le but.
**Source** : Sinha & Kapur (2021), R13. Les prérequis et la portée au
métier se vérifient dans le pilote, sans extrapoler une taille d’effet.

## 17. Articuler rappel et élaboration

**Ce qu’on fait** : répondre de mémoire, expliquer les liens, reconstruire
un schéma et confronter une analogie à ses limites peuvent se compléter.
**Pourquoi** : Karpicke & Blunt comparent des procédures précises de
rappel et de carte conceptuelle sur des textes scientifiques ; le rappel
y bénéficie aussi à la compréhension. Cette étude ne disqualifie pas
toutes les formes d’élaboration ni les cartes reconstruites de mémoire.
**Source** : Karpicke & Blunt (2011), R11. La variété des activités reste
subordonnée à l’objectif que la réponse permet d’observer.

## 18. La synthèse : s'expliquer à soi-même (ajouté le 02/09/2026)

**Ce qu'on fait** : tout chapitre se clôt par une production (une
phrase, une explication, une note) relue contre une liste de contrôle.
À partir du niveau 3 la synthèse devient l'exercice dominant.
**Pourquoi** : les synthèses citées rapportent un bénéfice moyen des incitations
à s’auto-expliquer, dans les tâches étudiées ; une liste de contrôle et
un nouvel essai servent à éprouver la qualité de l’explication dans ce produit.
**Source** : Bisra et al. (2018), référence complémentaire R20 ; Chi
et al. (1989), filiation historique. Sources non réexaminées dans ce lot,
aucune taille d’effet reprise comme attente pour le joueur.

## 19. Expliquer à quelqu'un (ajouté le 02/09/2026)

**Ce qu'on fait** : la synthèse de niveau 2 est « explique-le à un
collègue en soixante secondes » ; les défis entre joueurs et, plus tard,
la contribution d'un chapitre en sont la version réelle.
**Pourquoi** : l’étude citée compare préparation et enseignement dans un
dispositif déterminé. L’exercice destiné à un collègue en est une adaptation
produit ; sa durée et son bénéfice différé ne sont pas établis localement.
**Source** : Fiorella & Mayer (2013), référence complémentaire R21 ;
source historique non réexaminée dans ce lot.

## 20. Dessiner de mémoire, puis vérifier

**Ce qu’on fait** : dessin et feuille blanche, corrigés avec une liste
de contrôle ; aucune supériorité générale de l’écriture manuelle annoncée.
**Pourquoi** : les expériences de dessin portent notamment sur le rappel
d’items ; leur extension aux schémas techniques complexes reste à éprouver.
La réplication sur la prise de notes ne prouve pas l’égalité de tous les
supports dans toutes les conditions.
**Source** : Wammes et al. (2016), Morehead et al. (2019), références
complémentaires R22/R23 ; aucun doublement du rappel promis au joueur.

## 21. La journée laisse de la place à la compréhension

**Ce qu’on fait** : plusieurs études, pauses et reprises, avec plafond de
neuf. Ce rythme est une proposition éditoriale à adapter à la personne.
**Pourquoi** : l’espacement bénéficie à la rétention dans les tâches
étudiées ; il n’établit pas la meilleure dose de chapitres par jour.
Les cas et productions servent à travailler ce que les cartes seules
n’observent pas ; leur effet ne se déduit pas du temps passé.
**Source** : Cepeda et al. (2006), R2 ; paramètres et rythme : choix produit.

## 22. Dire sa confiance avant de révéler

**Ce qu’on fait** : sur les cas concernés, le joueur indique sa confiance
avant le corrigé ; l’accord entre confiance et réussite se mesure.
**Pourquoi** : l’hypercorrection motive l’attention portée aux erreurs
confiantes, sans prédire ce qui arrivera à chaque réponse. La calibration
permet de constater quand il faut vérifier ; elle n’est pas une maîtrise.
**Source** : Butterfield & Metcalfe (2001), R5 ; effet local non mesuré.

## 23. Le socle pèse dans la séance, l’exploration reste ouverte

**Ce qu’on fait** : la moitié du neuf vient du socle le moins avancé
tant qu’il n’est pas acquis ; l’étude reste ouverte dans la conception.
**Pourquoi** : c’est un compromis produit entre couverture et liberté.
Ni ce quota ni son effet sur la motivation ne viennent d’une expérience
citée. La revue des stratégies ne démontre pas que tout choix libre nuit.
**Source** : doctrine et `BLUEPRINT.md` pour l’arbitrage ; R4/R9 pour
les limites de l’interprétation scientifique.

## 24. L’expertise demande des situations variées

**Ce qu’on fait** : niveaux avancés avec cas, controverse, justification
et contribution, en conservant la pratique et son retour.
**Pourquoi** : Macnamara et al. observent des associations variables entre
pratique accumulée et performance selon les domaines. La faible variance
expliquée dans les professions n’est pas un effet causal de formation et
ne prouve ni l’inutilité de pratiquer, ni l’efficacité de lire la doctrine.
**Source** : Macnamara et al. (2014), R14. Ces formats doivent démontrer
un rappel autonome et un usage sur un cas nouveau.

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

## 27. Les points restent un indicateur de progression

**Ce qu’on fait** : points et ligue dérivés des cartes stabilisées et
du niveau, selon les paramètres produit ; aucune monnaie.
**Pourquoi** : les clics ne suffisent pas à mesurer un apprentissage ;
la stabilité estimée non plus. Les points rendent l’avancement visible,
sans remplacer les réponses différées ou les productions.
**Source** : choix produit ; Deci et al. (1999), R9, n’établissent pas
que tous les points détruisent la motivation ni que débloquer du contenu
la préserve automatiquement.

## 28. La semaine type (ajouté le 02/09/2026)

**Ce qu'on fait** : des jours colorés (fondations, cours, terrain,
exploration, étude, libre) qui pèsent sur le neuf et les formats ;
les révisions dues sont servies tous les jours.
**Pourquoi** : un rythme lisible vise à faciliter la reprise. Il s’agit d’une
hypothèse produit ; une semaine thématique n’est pas en elle-même la
preuve d’une habitude acquise ni d’un bénéfice d’entrelacement.
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

## 30. La fiche accompagne la tentative

**Ce qu’on fait** : fiche accessible depuis le chapitre, proposée en
reprise ; elle ne remplace pas la tentative qui ouvre la séance.
**Pourquoi** : lire une explication peut apprendre. Une fiche aide à
comprendre ou corriger ; seul un nouvel essai sans fiche permet de voir
ce qui est disponible mentalement. L’ordre de la séance est un choix
produit, sans interdiction scientifique générale de lire avant un test.
**Source** : Rowland (2014), Dunlosky et al. (2013), R3/R4.

## 31. Des invitations à revenir, à évaluer

**Ce qu’on fait** : invitation choisie, bilan privé, jalons et
reconnaissance entre pairs dans le périmètre des décisions produit.
**Pourquoi** : ces dispositifs peuvent soutenir ou gêner l’envie de
revenir selon la personne. Leur nom ne les soustrait pas aux effets des
récompenses. Les retirer si l’usage se dégrade reste une règle produit ;
un journal d’usage seul ne démontre pas leur causalité.
**Source** : Sailer & Homner (2020), R12 ; `decisions/0014`, `0016`,
`0020` pour les bornes et la confidentialité.

## 32. Provenance, contrôles et points de reprise

**Ce qu’on fait** : le modèle déclare outil et modèle ; pour une lecture,
l’usine distribue et juge les unités de document. Le code et les audits
conservent un point de reprise et des preuves adaptées à leur mission.
**Pourquoi** : contrôler les assertions contre une source et enregistrer
la reprise rendent le travail inspectable. Un sceau ne certifie ni vérité,
ni compréhension. Aucun nom de modèle ne limite le travail et aucun taux
général d’erreur des modèles n’est annoncé ici.
**Source** : `MODELES.md` et `decisions/0034`. Liu et al. (2024),
[Lost in the Middle](https://doi.org/10.1162/tacl_a_00638), reste une piste
historique sur des tâches et modèles particuliers, non réexaminée dans ce lot.

## 33. L'IFSI : objectifs distincts et approfondissement sans plafond (04/09/2026)

**Ce qu'on pose dans le programme** : l'étape de formation, la difficulté
de l'exercice et la criticité sont trois axes indépendants. Les objectifs
fins préparent le suivi des connaissances, du raisonnement, du calcul et
de la communication. Le geste en simulation et le geste clinique
supervisé demandent une appréciation distincte. Les spécialisations
réutilisent les acquis et ouvrent de nouveaux chapitres ; l'apprentissage
continue après le diplôme et après une spécialisation.

**Pourquoi** : une réussite à un exercice numérique ne démontre pas une
capacité à réaliser un soin dans une situation réelle. Le référentiel
prévoit une progression selon la complexité des situations et des
évaluations en stage. La difficulté cognitive est ici un choix éditorial
par objectif, sans prétendre reproduire une échelle clinique officielle.

**Source** : [arrêté du 20 février 2026, annexe III](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570499),
consulté le 04/09/2026 : complexité progressive, formation clinique et
évaluation. Les voies d'entrée suivent [l'article 12](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570385)
pour la FPC. L'ouverture après le diplôme est le cap demandé par JB,
consigné dans `decisions/0033-ifsi-referentiel-2026.md`.

**Portée de ce lot** : métadonnées et contrôles de programme. Les règles
de maîtrise par objectif, la remédiation d'erreur critique, la calibration
de confiance, les cas évolutifs et leurs mesures sont des spécifications
à éprouver dans un pilote. Aucun gain de rétention n'est revendiqué,
aucun score de maîtrise n'est inventé et aucun nouvel état joueur n'est
écrit par cette révision. Les formats et seuils seront éprouvés dans le
moteur avant de devenir des mécaniques actives.

Finition du 04/09 après relecture : les étapes restent des points d'appui
éditoriaux, avec reprises possibles ; leur ordre respecte les prérequis.
Les capacités sont conservées au niveau utile pour choisir un pilote.
Le détail par notion et les critères de réussite viendront avec ses
supports, sans utiliser le nombre d'objectifs comme preuve d'apprentissage.

*Toute nouvelle mécanique ajoute son entrée ICI dans le même commit
que son code ; sinon elle n'existe pas.*

## 34. L’étude relie tentative, principe, exercices et explication (05/09/2026)

**Ce qu’on fait** : une étude commence par une réponse personnelle ou une
demande de bases. Le principe et la leçon viennent ensuite, puis des
exercices et une synthèse personnelle. La grille de synthèse n’apparaît
qu’après écriture ; le joueur indique lui-même les critères présents dans
sa réponse. « Étude parcourue » décrit le parcours effectué, sans certifier
une compétence ni un transfert.

**Pourquoi** : ce parcours articule récupération et élaboration, avec
instruction après tentative [R3/R11/R13 du cadrage]. Ce rapprochement est
une conception pédagogique ; les travaux ne démontrent pas que ces quatre
écrans ou cet ordre exact sont optimaux pour nos métiers. L’indice sert à
reprendre quand les bases manquent, sans fabriquer une réussite autonome.

**Contrôles et limites** : la réponse et sa condition d’aide sont conservées
dans le journal. Un exercice assisté ne reçoit pas de note FSRS de rappel
autonome. Les essais sans indice restent des exercices pendant une étude,
avec le principe récemment consulté : ils ne sont pas un test à froid.
Leur format `etude` doit rester identifiable pour les mesures ultérieures.
Un choix QCM erroné est un rappel à reprendre ; une synthèse cochée reste
une autoévaluation. La reprise conserve l’étape et la version du contenu ;
un chapitre indisponible ou une carte retirée empêche de poursuivre sa
séquence, sans effacer les réponses déjà écrites.

**Source et état des preuves** : Rowland (2014), Karpicke & Blunt (2011),
Sinha & Kapur (2021), avec niveaux de consultation et limites dans
[le cadrage](CADRAGE-SCIENTIFIQUE.md). La conservation des réponses,
la séparation avec/sans aide et le retrait des cartes sont des garanties
logicielles à tester, pas des effets scientifiques. La rétention différée,
le transfert réel et l’envie de revenir restent à mesurer chez les joueurs.

## 35. Les formats interactifs spécialisés en séance (05/09/2026)

**Ce qu’on fait** : la salle de séance propose des interfaces dédiées selon
la nature cognitive de l’exercice :
- **Jeu de rôle (`role`)** : fiche de situation scénarisée avec interlocuteur,
  objectif de négociation et prompt exportable en un clic pour jeu immédiat.
- **Relier (`relier`)** : appariement tactile direct entre repères visuels
  d’un schéma et fonctions techniques.
- **Photo et plan (`photo`, `plan`)** : visualiseur avec loupe d’inspection
  tactile (niveaux de zoom) pour analyse d’organes techniques.
- **Chronologie (`datation`)** : frise procédurale jalonnée mettant en évidence
  l’étape ou le délai cible.
- **Synthèse (`synthese`)** : volet d’indice à la demande et liste de contrôle
  critériée des attendus après révélation pour guider l’auto-évaluation.

**Pourquoi** : diversifier les modes d’interaction permet d’aligner l’effort
cognitif sur l’activité cible (manipulation d’indices, analyse visuelle,
mise en situation relationnelle, structuration chronologique) plutôt que de
réduire toute réponse à une saisie textuelle indifférenciée.

**Contrôles et limites** : les saisies et choix tactiles sont synchronisés
dans le flux de réponse FSRS. L’usage d’une simulation IA ou l’auto-évaluation
par critères guidés ne dispense pas d’une confrontation ultérieure au terrain.
Aucun surcroît automatique de mémorisation n’est présumé ; les interactions
doivent rester sobres, sans surcharge cognitive superflue.

**Source et état des preuves** : Dunlosky et al. (2013), Bisra et al. (2018),
Hattie & Timperley (2007). Choix ergonomique et pédagogique documenté dans
`decisions/0039-modules-interactifs-salle-de-seance.md`.

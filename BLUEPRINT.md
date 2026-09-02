# BLUEPRINT v2, l'Académie telle qu'on l'imagine le 02/09/2026

Réécrit le 02/09/2026 sur le brief de JB et ses deux séries de questions
du même jour ([`travail/2026-09-02-brief-jb.md`](travail/2026-09-02-brief-jb.md),
[`travail/2026-09-02-dix-questions-oubliees.md`](travail/2026-09-02-dix-questions-oubliees.md)).
La version du 28/08 est archivée intacte
(`archive/conception-2026-08/BLUEPRINT-v1.md`) ; la table de concordance
est au §16. Ce document décrit **ce que le joueur vit**. Le pourquoi
pédagogique est dans [`METHODE.md`](METHODE.md), le quoi enseigner dans
[`PROGRAMME.md`](PROGRAMME.md), le comment construire dans
[`ARCHITECTURE.md`](ARCHITECTURE.md), l'apparence et les écrans dans
[`DIRECTION-ARTISTIQUE.md`](DIRECTION-ARTISTIQUE.md). Rien ici n'est
construit tant que `ROADMAP.md` ne le dit pas.

---

## 1. La vision en cinq lignes

Un gestionnaire de copropriété ouvre l'Académie dans le tram à 8h05. En
douze minutes il revoit neuf cartes que sa mémoire allait lâcher (une
fissure à qualifier, une majorité, une ligne d'annexe comptable), en
découvre deux nouvelles, et referme. Un autre matin il se dit « ce matin,
compta », touche le domaine et y va. Le samedi, il s'assoit pour une
étude d'une heure sur l'injonction de payer, ou pour une journée entière
sur l'énergie. Chaque question affiche d'où elle vient et qui l'a écrite.
L'arbre de son métier grandit devant lui, du primaire vers la frontière
de la science, et il n'a pas de fin.

## 2. Pour qui, dans quel ordre

1. **JB**, gestionnaire de copropriété. Son rituel réel est la mesure de
   tout ; rien de multi-joueur ne se construit avant qu'il tienne
   ([`ROADMAP.md`](ROADMAP.md), gate du rituel).
2. **Ses collègues**, même métier, même arbre, chacun son état.
3. **Arthur**, concours IFSI : autre banque, autre configuration, même
   moteur.
4. **Quiconque** tient un dépôt de sources et un abonnement à un modèle :
   location, vente, infirmiers, vétérinaires. Le produit ne leur demande
   jamais d'argent ([`decisions/0008`](decisions/0008-chacun-son-depot-et-son-abonnement.md)).

Téléphone et ordinateur sont **au même niveau** : tout se joue sur les
deux, même état, même arbre ; seuls les exercices sur papier attendent
que le joueur dise qu'il a de quoi écrire.

## 3. Les trois temps du joueur

Le joueur dit combien de temps il a et, s'il veut, où il va. Le moteur
compose. Il ne choisit jamais le format d'un exercice
([`decisions/0005`](decisions/0005-trois-formats-de-temps.md)).

### La séance (8 à 20 minutes)

1. **Ouverture en moins de trois secondes** : l'arbre s'affiche avec, en
   tête, le cap du jour (« Lundi, fondations : 9 cartes dues ») et un
   bouton. Une touche, la première question est là.
2. **Les révisions dues** : les cartes que FSRS prédit sur le point
   d'être oubliées, entrelacées entre domaines, plafonnées (reprise après
   trois semaines d'AG : jamais plus de vingt, le reste se ré-étale sans
   être montré). Elles ne se négocient pas, quel que soit le jour.
3. **Le neuf** : une à trois cartes du chapitre en cours du cap choisi,
   ou l'amorce d'un chapitre nouveau. Tant que le socle n'est pas validé,
   la moitié du neuf vient de la branche du socle la moins avancée (§6).
4. **La clôture** en un écran : ce qui est stabilisé, ce qui revient
   demain, le nœud qui a bougé, une phrase factuelle avec une action
   (« ton socle est à 62 %, la compta est ta branche la plus en retard,
   une étude de 45 minutes la fait passer à 70 % »). Le compteur de
   séances monte d'un.

S'arrêter à la troisième carte reste une séance. Il n'y a pas de bouton
« mode court » : la clôture est honorable à tout moment.

### « Ce matin, compta » : jouer un domaine

Le joueur touche un domaine sur l'arbre. L'écran du domaine propose, dans
cet ordre et selon l'état :

| Proposition | Quand | Ce qui se joue |
|---|---|---|
| **Réviser** | des cartes du domaine sont dues | les dues du domaine, puis au plus deux « rappels d'ailleurs » très en retard, annoncés comme tels |
| **Continuer** | un chapitre du domaine est en cours | le neuf du chapitre : amorce si jamais ouvert, puis trois à six cartes, la fiche en lien |
| **Étudier** | toujours | une étude de 45 à 90 minutes sur le chapitre suivant ou sur celui que le joueur touche |
| **Épreuve** | le domaine est solide et l'épreuve n'a pas été tentée aujourd'hui | douze à quinze cartes à froid, score solennel |
| **Au hasard** | toujours | un exercice tiré dans les nœuds ouverts du domaine |

Le domaine choisi l'emporte sur l'entrelacement : le joueur a demandé de
la compta, il a de la compta, et le moteur note le choix au journal.

### L'étude (45 à 90 minutes)

Un chapitre de bout en bout :

1. **L'amorce** : un problème concret à tenter avant toute explication
   (« voici trois photos de fissures ; laquelle appelle un expert dans la
   semaine ? »). Se tromper ici est prévu et productif.
2. **La leçon** : la fiche du chapitre, paraphrasée et sourcée, avec un
   exemple travaillé pas à pas. Huit minutes de lecture au plus.
3. **Les exercices** : dix à vingt cartes du chapitre, formats mélangés,
   feedback immédiat, capture de confiance avant la réponse sur les cas.
4. **La synthèse** : le joueur produit (une phrase, une explication de
   soixante secondes à un collègue imaginaire, un dessin de mémoire, une
   note). Relue par lui contre une liste de contrôle, ou par le modèle au
   niveau 3 et au-delà si le joueur a une clé.
5. **La sortie** : les cartes du chapitre entrent en rotation FSRS ; le
   nœud passe « en cours ».

### La journée (une demi-journée à une journée)

Un programme composé à partir du temps déclaré : les révisions dues
d'abord, puis trois à six études entrelacées sur deux ou trois domaines,
une pause de dix minutes toutes les cinquante, un rappel en fin de
journée sur les chapitres du matin, et une synthèse de journée
(« qu'est-ce que je saurai faire lundi que je ne savais pas faire
vendredi ? »). Le neuf est plafonné par jour : une journée dépense son
temps en compréhension et en production, jamais en bourrage.

### Le matin sans envie

« Au hasard » tire un exercice calibré dans les nœuds ouverts. Aucun
choix à faire, aucune culpabilité : cinq cartes valent une séance.

## 4. La semaine type

Pas de saisons, pas d'événements : une semaine qui a des couleurs
([`decisions/0016`](decisions/0016-semaine-type-pas-de-saisons.md)). Les
révisions dues sont servies tous les jours ; la couleur ne pèse que sur
le neuf et le mélange des formats. Elle est configurable par domaine et
par joueur ; le défaut :

| Jour | Couleur | Ce que la séance pèse |
|---|---|---|
| Lundi | **Fondations** | le socle d'abord, rattrapage du week-end, pas de neuf si plus de quinze cartes sont dues |
| Mardi | **Cours** | le chapitre en cours du cap choisi, neuf plein |
| Mercredi | **Terrain** | photo, plan, cas, diagnostic : les domaines techniques |
| Jeudi | **Cours** | comme mardi |
| Vendredi | **Exploration** | au hasard, satellites, épreuves éligibles, niveaux 4 et 5, culture |
| Samedi | **Étude** | une étude proposée sur la branche du socle la plus en retard, facultative |
| Dimanche | **Libre** | rien n'est proposé ; une lecture si envie ; jamais un rappel |

Le calendrier du métier pèse en silence sur les jours Cours et Terrain
(les assemblées au printemps, les budgets à l'automne, le chauffage en
novembre) ; le « pourquoi cette carte » le dit quand on le demande.

## 5. L'arbre

L'écran d'accueil **est** l'arbre du métier
([`decisions/0001`](decisions/0001-arbre-au-lieu-de-l-archipel.md)).

- **Le tronc** : le socle commun (§6), dessiné épais. Sa jauge est le
  chiffre de tête du profil.
- **Domaines** : les dix zones de compétence du gestionnaire
  ([`PROGRAMME.md`](PROGRAMME.md) §2), disposées autour du tronc, plus
  Culture, à part.
- **Branches** : à l'intérieur d'un domaine, ce qu'un professionnel nomme
  (« les majorités », « la VMC », « les cinq annexes »).
- **Chapitres** : les nœuds. Chacun porte un niveau de 1 à 5, dessiné
  comme une distance au tronc : les niveaux 1 et 2 près du tronc, les
  niveaux 4 et 5 vers la canopée, là où l'arbre n'a pas de bord.
- **Satellites** : les chapitres nés de la boîte (§9), en orbite d'une
  branche, jouables tout de suite.
- **Les liens** : un chapitre peut avoir plusieurs enfants (une branche
  se divise) et plusieurs parents (deux branches se rejoignent) ; c'est
  un graphe orienté, pas un arbre strict. Un prérequis dans un autre
  domaine se dessine en pointillé vers ce domaine.

### Ce qu'on voit, et jusqu'où

Le joueur voit **toute la forme** d'un domaine dès le premier jour : tous
les nœuds en silhouette, les divisions, la profondeur. Il ne voit pas
tout ce qu'ils contiennent :

| Distance au dernier nœud ouvert | Ce qui s'affiche |
|---|---|
| ouvert ou joué | titre, état, anneau de remplissage |
| +1 | titre lisible, anneau vide : « c'est la suite » |
| +2 | titre grisé |
| +3 et au-delà | silhouette sans titre |
| niveaux 4 et 5 | la canopée : silhouettes qui s'estompent vers le bord |

On voit la lumière au bout sans mesurer la distance, et on voit que
l'arbre est grand.

### Les états d'un nœud

| État | Ce que ça veut dire | Rendu |
|---|---|---|
| inconnu | jamais ouvert, hors de portée | silhouette |
| ouvert | à portée, jamais joué | titre, anneau vide |
| en cours | joué, remplissage < 75 % | anneau partiel |
| solide | remplissage ≥ 75 % | anneau presque plein |
| validé | épreuve de domaine réussie | anneau plein, insigne |
| à revoir | joué, mais pas revu depuis le seuil de fraîcheur | anneau grisé, daté (« vu il y a 47 j ») |

Le **remplissage** n'a qu'une définition : la part des cartes validées du
nœud dont la stabilité FSRS dépasse vingt et un jours (la convention
« mature » d'Anki, paramétrée). Tout ce qui s'affiche en dérive ; il
n'existe pas de seconde comptabilité.

### Les règles de l'arbre

1. **Tout nœud visible est jouable**, même loin devant. L'échec y est
   sans pénalité. Invariant, pas confort : le procès fait au chemin
   linéaire de Duolingo en 2022 est le précédent.
2. **La branche suivante s'ouvre à 75 %** de la précédente, ou par le
   quiz de positionnement, ou par l'épreuve.
3. **Un nœud validé le reste.** Ajouter des chapitres ouvre de nouveaux
   nœuds, il ne fait jamais retomber un acquis.
4. **Le brouillard a deux couches** : ce qu'on n'a jamais vu (silhouette)
   et ce qu'on a vu mais qui est périmé (grisé, daté). Un chiffre qui
   n'est plus sûr se montre comme tel.

## 6. Le socle et la liberté

([`decisions/0013`](decisions/0013-le-socle-et-la-liberte.md)) Le
**socle** est ce que tout gestionnaire doit tenir : niveau 2 dans les dix
domaines, niveau 3 en droit, en comptabilité et sur l'assemblée générale
(`PROGRAMME.md` §3). Au-delà, c'est la spécialisation, jamais imposée.

- **La séance protège le socle.** Tant qu'il n'est pas validé, la moitié
  du neuf vient de la branche du socle la moins avancée. Quand le joueur
  choisit un domaine, il l'a ; la pondération reprend le lendemain.
- **L'étude et la journée sont libres.** N'importe quel nœud ouvert, tout
  de suite, satellites compris.
- **Le rappel est une phrase et une action**, à la clôture, jamais une
  remontrance, jamais un verrou.
- **Le socle validé** par son épreuve (§8) éteint la pondération. Il
  reste entretenu par FSRS ; s'il pâlit, l'arbre le grise et la séance y
  revient d'elle-même.

## 7. Le chapitre : comment un cours est construit

Un chapitre ([`decisions/0002`](decisions/0002-le-chapitre-unite-de-contenu.md))
= amorce + leçon + cartes + synthèse. Ses cartes sont les unités de
mémoire ; FSRS ne connaît qu'elles.

### L'ordre des chapitres

- **Thématique par branche** : une branche est un sujet qu'un pro nomme,
  pas un chapitre de manuel.
- **Chronologique quand la matière l'est** : un circuit (le recouvrement,
  le cycle annuel, un sinistre) se suit dans l'ordre des étapes ; une
  histoire dans l'ordre des dates.
- **Du général au particulier, du fréquent au rare, du concret à
  l'abstrait** à l'intérieur d'une branche : la notion, puis la règle,
  puis l'exception, puis la controverse.
- **Les croisements sont explicites** : un chapitre cite ses ponts
  (« voir aussi ») vers d'autres domaines, et les cas transverses
  (§8) les font jouer ensemble au niveau 3. Le tronc commun n'est pas un
  empilement de matières, c'est un métier.

### La fiche de rappel

Chaque chapitre a sa **fiche** : la leçon, et sous elle la liste
question-réponse de ses cartes. Elle est lisible à tout moment depuis le
nœud, hors ligne, imprimable. Le moteur la propose quand un nœud passe
« à revoir » (« relis la fiche trois minutes, puis cinq cartes ») et à
la veille d'une épreuve. Elle n'ouvre jamais une séance : on répond
d'abord, on relit ensuite.

### Les types d'exercice

| Type | Le geste | Niveaux | Correction | Chrono |
|---|---|---|---|---|
| **flash** | question, réponse dans la tête, révélation, auto-note | 1-3 | soi-même (quatre notes FSRS) | jamais |
| **qcm** | quatre choix, chaque piège expliqué | 1-3 | exacte | parfois (fluence, niveau 1) |
| **photo** | une image, « qu'est-ce que c'est, à quoi ça sert, que faire ? » | 1-3 | exacte + fiche | parfois |
| **relier** | apparier termes, images, causes, époques | 1-2 | exacte | parfois |
| **datation** | remettre dans l'ordre un circuit ou une frise | 1-2 | exacte | jamais |
| **plan** | extrait de plan annoté, lire une abréviation, un niveau | 1-3 | exacte | jamais |
| **cas** | une situation en trois à cinq pas, une décision à chaque pas | 2-3 | exacte par pas | jamais |
| **libre** | écrire ou dicter, corrigé contre les sources de la carte | 3-4 | modèle (clé du joueur) ou liste de contrôle | jamais |
| **role** | un prompt prêt à copier pour une conversation dédiée | 3-4 | débrief par le modèle | jamais |
| **dessin** | dessiner de mémoire sur papier, puis liste de contrôle | 1-3 | soi-même par liste | jamais |
| **feuille-blanche** | rappel libre sur papier en temps borné, puis liste | 2-4 | soi-même par liste | oui, borne haute |
| **synthese** | produire : phrase, explication, note, commentaire | 1-5 | liste, modèle, ou pair | jamais |
| **lecture** | un document public avec sa fiche de méthode, questions, cartes extraites | 3-5 | exacte + modèle | jamais |
| **ecoute** | une situation audio (un appel, une réunion), puis décider | 2-4 | exacte | jamais |

Ce qui commande le type : le contenu et le niveau
([`decisions/0003`](decisions/0003-cinq-niveaux-et-la-synthese.md)).
Le joueur ne choisit jamais. Trois règles de variété : jamais deux
formats identiques d'affilée quand la matière le permet, au moins trois
types par séance, le concret avant la théorie. Les types `ecoute` et la
photothèque de terrain viennent **plus tard dans la roadmap**
([`decisions/0017`](decisions/0017-images-et-audio.md)) ; les schémas SVG
maison sont l'image de la v2.

### Le chrono

Un chrono ne mesure que la **fluence** d'un automatisme (nommer un organe,
donner une majorité, lire une abréviation). Il n'existe jamais sur
l'analyse, la réponse libre, la lecture, la synthèse. Aucune carte n'a de
chrono par défaut ; un chapitre l'active sur ses cartes de niveau 1 quand
la branche est solide.

### La confiance

Avant de révéler un cas ou un QCM de niveau 2 et plus, le joueur dit s'il
est sûr. Une erreur confiante déclenche la correction la plus longue :
c'est le moment où la mémoire se réécrit le mieux. Le profil montre sa
**calibration**, l'écart entre ce qu'il croit savoir et ce qu'il sait.

### Après une erreur

1. La micro-explication en trois lignes, la source, la vigilance.
2. Le champ « pourquoi je me suis trompé ? » du carnet d'erreurs,
   facultatif, une ligne.
3. La carte revient vite. Trois échecs sur la même carte : le moteur
   propose la carte préalable ou la fiche, guidé par la note du carnet.

Le carnet d'erreurs ne se partage jamais, avec personne.

## 8. Les épreuves

([`decisions/0014`](decisions/0014-competition-et-epreuves-transverses.md))

| Épreuve | Quand elle s'ouvre | Ce qu'elle contient | Ce qu'elle donne |
|---|---|---|---|
| **de domaine** | le domaine est solide | 12 à 15 cartes à froid tirées dans toutes ses branches, dont un cinquième venu des domaines prérequis | le domaine passe « validé », un insigne, la palette du domaine |
| **transverse** | au moins deux domaines concernés sont solides | un dossier en cinq pas (un dégât des eaux du 5e au 2e ; une fissure avant l'AG ; un impayé de 18 mois), une décision à chaque pas, expliquée | un insigne de dossier ; c'est le vrai test de la compréhension |
| **du gestionnaire** | tous les domaines du socle sont validés | trois dossiers transverses et vingt cartes à froid dans tout le socle | le titre « Confirmé », le socle validé, fin de la pondération |

Une épreuve ratée ne se retente pas le même jour, ne coûte rien, et
reste au journal comme mémoire. Une épreuve réussie l'est pour toujours.

## 9. La boîte

Le joueur croise un mot (« chaudière hybride »), un article, un dépôt
git, une capture d'écran, une vidéo. Il le glisse dans la boîte, depuis
le téléphone ou l'ordinateur ([`boite/README.md`](boite/README.md)). Sur
sa machine, l'agent en tire un **chapitre satellite** : sources triées,
leçon paraphrasée, cartes brouillon, trous nommés, rattachement proposé
à la branche la plus proche. Après double passe et valideur, le
satellite apparaît sur l'arbre, en orbite, jouable tout de suite
([`decisions/0009`](decisions/0009-la-boite-et-les-chapitres-satellites.md)).

La boîte est aussi le chemin des niveaux 4 et 5 : un article ou un arrêt
commenté glissé dans la boîte devient une lecture, puis une contribution
à la banque.

## 10. Les sources à l'écran

Chaque question porte, sous la réponse et en un tap depuis la question :

- la ou les sources, avec leur **nature** et leur **parti** quand il
  existe (« défend les syndics », « vend la prestation décrite ») ;
- la date de vérification et, s'il y en a une, la date de péremption ;
- la **ligne de provenance** : qui a écrit (« Généré par Claude Opus le
  21/01/2026 » ou « Écrit par JB »), combien de sources retrouvées et
  concordantes, qui a relu et quand, la dernière vérification
  ([`decisions/0021`](decisions/0021-le-modele-ecrit-la-provenance-s-affiche.md)) ;
- la mention **« sans source retrouvée »** quand le modèle n'a rien
  trouvé et l'a dit : la carte se joue, sans chiffre ni date, et sera
  vérifiée en priorité ;
- le marqueur **« à recouper »** si la carte ne repose que sur un
  éditeur, une organisation professionnelle ou une association, ou sur
  rien ;
- la **note de confiance**, une lettre discrète, A, B ou C, dérivée du
  nombre et de la qualité des sources, de la relecture et de la
  fraîcheur de la vérification ([`decisions/0022`](decisions/0022-le-modele-pose-le-cadre-les-sources-corroborent-l-audit-mesure.md)) ;
  elle se lit aussi sur le nœud de l'arbre ;
- le **dossier de la carte** : qui l'a vérifiée et quand, l'historique
  de ses statuts, l'empreinte de la source ;
- le lien vers **« Pourquoi croire ce professeur ? »**, la page de
  confiance du domaine : qui a écrit, comment c'est vérifié et avec
  quels chiffres, ce que des humains ont contrôlé, les erreurs connues
  et leur traitement, les limites ;
- le bouton **« cette carte est fausse »** : la carte sort de la rotation
  du signaleur immédiatement ; le retrait pour tous attend le
  propriétaire du domaine.

([`decisions/0004`](decisions/0004-la-source-porte-sa-nature-et-son-parti.md))

## 11. Le quiz de positionnement

Au premier lancement d'un domaine, une vingtaine de questions réparties
sur ses branches. Une bonne réponse inscrit la carte au journal comme
déjà stabilisée (stabilité initiale explicite, origine « quiz ») ; une
mauvaise n'inscrit rien. Le quiz **ouvre** des branches, il n'écrit jamais
leur remplissage. Puis le joueur joue cinq cartes tout de suite ; la
première séance dure moins de dix minutes.

## 12. Points, titres, insignes : ce qui récompense, ce qui est interdit

([`decisions/0014`](decisions/0014-competition-et-epreuves-transverses.md),
[`decisions/0015`](decisions/0015-l-arbre-est-l-avatar.md))

- **Les points de savoir** : une carte stabilisée vaut dix fois son
  niveau. Deux chiffres : le cumulé, qui ne descend jamais, et l'à jour,
  qui peut pâlir. Aucun point n'est stocké : tout se recalcule depuis le
  journal.
- **Le niveau du joueur** en dérive par une courbe douce, et son **titre**
  dépend du socle et des épreuves, jamais des points seuls : Apprenti,
  Junior, Gestionnaire, Confirmé (socle validé), Expert en X (domaine X
  validé et un chapitre de niveau 4 solide), Référent X (une
  contribution de niveau 5 validée).
- **Le compteur de séances** monte et ne descend jamais. Une coupure se
  ré-étale, elle ne s'affiche pas en dette.
- **Le calendrier de régularité** en dégradé, jamais en binaire.
- **La mission de la semaine** (« stabilise quinze cartes de compta »,
  « réussis l'épreuve procédure ») donne un insigne, pas des points.
- **Le brouillard qui recule** est la récompense visuelle. Un domaine
  validé débloque un **insigne** sobre, daté, qui dit d'où il vient, et
  une **palette** de couleurs pour l'outil. Pas d'avatar : l'arbre est
  l'avatar, sa forme c'est toi.
- **Une citation sourcée** aux moments de conquête, jamais de confettis.
- **Le bilan du mois** : une page qu'on peut partager, façon récap
  annuel : cartes stabilisées, domaines qui ont bougé, calibration,
  erreurs récurrentes et leur raison, le nœud le plus dur.
- Interdits : boutique, monnaie, vies, série qui casse, coffres
  aléatoires, urgence factice. Les mécaniques d'engagement se coupent
  d'office pour un joueur dont elles dégradent le rituel mesuré.

## 13. Les cercles et le partage

([`decisions/0010`](decisions/0010-cercles-visibilite-et-aucun-reporting.md))

**Tous les joueurs d'une même Académie se voient par défaut** : l'arbre,
le titre, les insignes, le compteur (amendement de JB du 02/09 au soir).
Chacun peut masquer un domaine ou se masquer d'un geste. Ensuite :

- **Le cercle** : des amis ajoutés mutuellement. Un **fil des jalons**
  (domaine validé, épreuve réussie, titre gagné : jamais une séance,
  jamais un score), des **kudos** d'un tap, des **défis** : dix cartes
  d'un chapitre commun, même tirage, chacun à son heure dans les
  quarante-huit heures, comparaison à la fin.
- **Le profil d'un autre** : sa carte de visite (titre, socle, insignes
  affichés), son arbre en miniature (tous les domaines, sauf ceux qu'il
  a masqués), son compteur. Jamais son carnet, ses réponses, ses temps.
- **La bibliothèque** : les domaines livrés par les uns sont adoptables
  par les autres. Le travail de digestion fait par un joueur, à ses
  frais, sert au suivant s'il le veut ; seule la couche `banque`, sous
  licence de partage, y entre.
- **L'équipe** : une agence, un service, une classe. Un cercle avec un
  domaine commun, une **ligue hebdomadaire facultative** (score : cartes
  stabilisées dans la semaine × niveau, sur le tronc commun ; sa propre
  ligne mise en avant, le podium pas plus gros que le reste) et un
  **tuteur** que chacun accepte ou non, en voyant qu'il est vu.
- **Le partage est manuel.** À un jalon, le produit fabrique une carte
  image et texte (« JB a validé Comptabilité de copropriété, 143 cartes
  stabilisées »). Le joueur l'envoie lui-même, par mail ou Teams, s'il
  veut. Le produit n'envoie jamais rien à personne.
- **Jamais** : le carnet d'erreurs, un export pour un tiers, un
  classement imposé, un profil public.

## 14. Ce qui vient du travail réel

L'Académie est un cours sur un savoir qui existe indépendamment de JB.
Le terrain est un condiment. Ce qui peut passer de labor à l'Académie :

- un **atelier sur pièce publique** équivalente (une décision Judilibre
  sur le même contentieux qu'un dossier réel) ;
- un **cas d'école réécrit** (copropriété renommée, montants arrondis,
  détails gommés, mécanisme conservé), validé par JB carte par carte ;
- une **photo de terrain** cadrée serré, sans adresse ni visage, validée
  une à une (plus tard, `decisions/0017`) ;
- un « fil du réel » occasionnel : l'actualité de la veille devenue carte
  ou lecture ;
- le **rituel de sortie de réunion**, trente secondes dictées (« je n'ai
  pas su répondre à X »), qui atterrit dans la boîte.

Jamais : un nom de copropriété, un montant réel, une personne, un mail,
une transcription de réunion.

## 15. Un autre métier, et l'agent-compagnon

Donner l'Académie à Arthur ou à un vétérinaire = une autre banque, une
autre configuration (domaines, branches, socle, semaine type, quotas),
le même moteur, le même client, la même méthode. Le guide est
[`gabarit-domaine/USINE.md`](gabarit-domaine/USINE.md).

Le produit ne s'assèche jamais en silence : quand il n'y a plus de neuf
dans une branche ouverte, quand une source est douteuse, quand un
satellite attend son rattachement, un message court s'affiche avec un
bouton qui lance le geste correspondant sur la machine du joueur. Le
serveur ne fait aucun appel à un modèle ; il parle, le joueur agit chez
lui.

## 16. Table de concordance v1 → v2

| BLUEPRINT v1 | Ici |
|---|---|
| §1 vision | §1 |
| §2 c'est / ce n'est pas | `DOCTRINE.md` §1-2 |
| §3 socle scientifique | `METHODE.md`, `CADRAGE-SCIENTIFIQUE.md` |
| §4 boucle quotidienne | §3 |
| §5 modes d'exercice | §7 |
| §6 ateliers | §7 (type `lecture`), `PROGRAMME.md` |
| §7 sources de contenu, garde-fous | §10, §14, `CORPUS.md` |
| §7 bis recadrage cours magistral | §7, `decisions/0002` |
| §8 moteur FSRS | `ARCHITECTURE.md` §4 |
| §9 arbres de compétence, règle des profils | §5, §13, `decisions/0010` |
| §10 architecture | `ARCHITECTURE.md` |
| §11 généralisation | §15 |
| §12-13 arbitrages | `decisions/` |
| SPEC-PRODUIT §2 modèle A4 | `ARCHITECTURE.md` §2, `decisions/0008` |
| SPEC-PRODUIT §3 carte-monde, quiz, carnet | §5, §11, §7 |
| SPEC-PRODUIT §4 usine | `gabarit-domaine/USINE.md`, `ARCHITECTURE.md` §7 |
| SPEC-PRODUIT §5 sécurité, RGPD | `ARCHITECTURE.md` §8 |
| SPEC-PRODUIT §7 sessions O1-O8 | `ROADMAP.md` |

## 17. Ce qui reste à trancher par JB

1. Les noms des dix domaines tels qu'il les dirait à un collègue
   (`PROGRAMME.md` §2 propose).
2. Le premier collègue invité, et quand.
3. La semaine type par défaut (§4) : garder, ou décaler l'étude au
   dimanche.

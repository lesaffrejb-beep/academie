# 0014, La compétition compte des cartes stabilisées ; les épreuves transverses testent la compréhension

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur les questions de JB (« compétition sur quoi ?
  temps passé ? notions validées ? comment vérifier la compréhension
  profonde ? comment compter les points ? »)

## Décision

1. **Jamais sur le temps passé, jamais sur les clics.** Une mesure qu'on
   peut gagner en traînant ou en tapotant est une mauvaise mesure
   (Goodhart, `labor/wiki/patterns/mesure-objectif-goodhart.md`).
2. **La ligue compte les cartes stabilisées dans la semaine, pondérées
   par leur niveau** (une carte de niveau 3 vaut trois), sur le tronc
   commun par défaut. Elle est facultative, hebdomadaire, et ne
   s'affiche pas plus gros que la ligne du joueur.
3. **Les points de savoir** : une carte stabilisée (stabilité ≥ seuil)
   vaut dix fois son niveau. Deux chiffres : le cumulé (ne descend
   jamais) et l'à jour (peut pâlir). Aucun point n'est stocké.
4. **Le niveau du joueur** dérive des points par une courbe douce ; **le
   titre** dérive du socle et des épreuves, jamais des points seuls :
   Apprenti, Junior, Gestionnaire, Confirmé (socle validé), Expert en X,
   Référent X.
5. **Les épreuves transverses** : un dossier en cinq pas mêlant au moins
   trois domaines, une décision à chaque pas, expliquée. Elles s'ouvrent
   quand les domaines concernés sont solides. L'épreuve du gestionnaire
   = trois dossiers plus vingt cartes à froid dans tout le socle.
6. **Les défis** : dix cartes d'un chapitre commun, même graine, chacun
   à son heure dans les quarante-huit heures.
7. **Les missions de la semaine** donnent un insigne, jamais des points.

## Contexte

Les jeux comptent l'XP, les quêtes, les saisons, les classements ; la
littérature de la motivation dit que la récompense qui ne change rien
au jeu s'use en deux semaines et que la comparaison imposée détruit la
motivation intrinsèque (Deci, Koestner & Ryan 1999). Ce qui dure : ce
qui ouvre du contenu, ce qui mesure du vrai, ce qu'on choisit.

## Conséquences

- `points.py` et `epreuves.py` (chantier `ACA-EXAMEN-1`) ; les dossiers
  transverses sont des chapitres de la branche `cabinet.cas-transverses`
  avec prérequis multi-domaines (`programme/copro.json`).
- `METHODE.md` §26 et §27.

## Réouverture

Si la ligue fait baisser la fréquence des séances d'un joueur sur
quatre semaines, elle lui est coupée d'office (décision 0010).

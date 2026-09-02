# 0002, Le chapitre est l'unité de contenu

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur le brief de JB (« chaque chapitre fini, on a le
  chapitre d'après », « je veux un chapitre dessus »)

## Décision

Le contenu s'organise en **chapitres**. Un chapitre = une amorce (un
problème à tenter avant la leçon), une leçon (fiche de cours paraphrasée
et sourcée, 300 à 800 mots, avec un exemple travaillé), ses cartes
(les unités de mémoire, contrat carte-v1 puis v2), et une synthèse (ce
que le joueur produit à la fin). Il porte un niveau (1 à 5), une branche,
des prérequis (d'autres chapitres) et ses sources. La **carte reste
l'unité de mémoire** : FSRS ne connaît que des cartes ; le chapitre est ce
qu'on ouvre, la carte est ce qui revient.

## Contexte

Au 02/09 la banque est un tableau de cartes par branche (84 cartes copro,
40 IFSI), sans leçon, sans amorce, sans synthèse. Le recadrage du 28/08
demandait « du cours magistral de haute qualité, avec récursivité ». Le
brief du 02/09 demande des chapitres qui s'enchaînent sans fin et des
chapitres à la demande.

## Conséquences

- Le contrat carte-v2 ajoute un champ `chapitre` à la carte ; un fichier
  de chapitre porte la leçon, l'amorce et la synthèse (`ARCHITECTURE.md`
  §5). La migration des cartes existantes est une assignation, jamais un
  renumérotage d'id.
- La leçon ne s'affiche **jamais en ouverture** d'une séance (invariant 4
  de la doctrine) : en séance, on joue les cartes et la leçon est un lien
  après la réponse ; en étude, la leçon vient après l'amorce et avant les
  exercices.
- Un chapitre naît `brouillon`, passe la double passe et le valideur
  comme une carte ; il ne se joue que `valide`.
- La règle de croissance vaut pour les chapitres : ajouter un chapitre à
  une branche validée ouvre un nouveau nœud, il ne fait jamais retomber
  un remplissage acquis.

## Réouverture

Si les leçons ne sont pas lues (mesure : ouverture de la fiche après
réponse < 5 % sur un mois), on rouvre le format de la leçon, pas
l'unité.

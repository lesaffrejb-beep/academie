# 0011, Le papier est un mode d'exercice

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur la question de JB (« est-ce qu'il ne faudrait pas
  parfois passer sur papier ? »)

## Décision

Le papier entre dans le produit comme **exercice**, jamais comme support
de cours. Deux types de cartes :

- **`dessin`** : « dessine de mémoire la coupe d'un caisson de VMC et
  légende-le », puis l'écran montre le schéma de référence et une liste
  de contrôle (les éléments attendus) ; le joueur coche ce qu'il avait,
  la note FSRS en découle. Photo du dessin facultative, jamais envoyée
  au serveur.
- **`feuille-blanche`** : « sur une feuille, écris tout ce que tu sais du
  circuit de recouvrement d'une charge impayée, en 4 minutes », puis
  liste de contrôle des points attendus, même mécanique.

Ces cartes sont proposées en **étude** et en **journée**, jamais en séance
sur téléphone (sauf si le joueur déclare avoir de quoi écrire).

## Contexte

La science est plus nuancée que l'intuition. Dessiner ce qu'on apprend
améliore nettement le rappel (Wammes, Meade & Fernandes 2016, effet
robuste sur sept expériences ; synthèse Fernandes, Wammes & Meade 2018).
Écrire à la main plutôt qu'au clavier, en revanche, ne tient pas la
réplication (Morehead, Dunlosky & Rawson 2019 : effets petits et non
significatifs). Le rappel libre sur feuille blanche, lui, est du
« testing effect » pur, robuste (Rowland 2014). Donc : le dessin pour
les schémas et mécanismes, la feuille blanche pour le rappel libre, et
aucune promesse sur « écrire à la main pour mieux retenir ».

## Conséquences

- Contrat carte-v2 : types `dessin` et `feuille-blanche`, avec un champ
  `attendus` (liste de contrôle, 3 à 10 éléments) obligatoire.
- `METHODE.md` §20 porte l'entrée avec ses sources vérifiées le
  02/09/2026.
- Le programme marque les chapitres où le dessin est le bon exercice
  (pathologie, équipements, plans, circuits de procédure et de
  comptabilité).

## Réouverture

Si la note auto-attribuée sur `dessin` diverge de la rétention mesurée à
l'épreuve de domaine de plus de 20 points, on revoit la liste de
contrôle, pas le type.

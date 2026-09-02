# 0001, L'arbre de compétences remplace l'archipel

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« pourquoi pas abandonner le bateau, c'est trop enfantin
  pour mes collègues »), arbitrage d'exécution par l'agent

## Décision

L'habillage « archipel » (îles en forme de sujet, bateaux, phare, dé,
brume marine) est abandonné. Le produit affiche un **arbre de
compétences** : des domaines, des branches, des chapitres reliés par des
liens de prérequis, dessinés comme une planche technique adulte. Le
graphe qui vit dessous (`app/progression.py` : régions, remplissage
mesuré par FSRS, ouverture à seuil, épreuve pour le 100 %, exploration
libre partout) ne change pas de principe ; il descend au niveau du
chapitre et de la branche par le chantier `ACA-ARBRE-1` (états de nœud,
fraîcheur, ouverture de branche).

## Contexte

Le 30/08, l'archipel SVG était jouable et déployé. Le brief du 02/09
vise les collègues de JB et « n'importe qui » : le vocabulaire maritime
et les silhouettes d'îles ont été jugés enfantins, et le produit doit
être neutre en genre et en âge. Le mot de JB est « skill tree ».

## Conséquences

- `client/` (l'archipel) reste servi jusqu'à ce que le nouveau front le
  remplace (chantier `ACA-FRONT-2`). `tooling/check.py` vérifie encore
  les marqueurs de l'archipel : il sera mis à jour dans le même chantier.
- Le vocabulaire change : « domaine, branche, chapitre, épreuve, séance,
  au hasard » remplacent « île, phare, dé, expédition, boss ». Les clés de
  configuration (`domaines`, `progression`) ne bougent pas.
- Les patterns volés au benchmark du 30/08 restent valables : brouillard à
  deux couches, paliers nommés, verrou 24 h de l'épreuve, graine
  journalisée, règle de croissance, exploration libre gravée.
- Les 33 icônes game-icons (CC BY) restent utilisables comme glyphes de
  chapitre, attribution visible.

## Réouverture

Si trois joueurs adultes disent spontanément que l'arbre est froid ou
illisible, on rouvre l'habillage, jamais le graphe.

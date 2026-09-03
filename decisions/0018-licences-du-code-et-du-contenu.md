# 0018, Les licences du code et du contenu

- Statut : acceptée par délégation le 03/09/2026 (`decisions/0023`) ; question oubliée n° 3
- Date : 02/09/2026
- Décideur : JB

## Décision proposée

1. **Le code** (moteur, serveur, client, outils) : licence **MIT**. Un
   copain peut reprendre tout le dépôt, l'héberger, le modifier ; c'est
   le brief. Le dépôt reste privé tant que JB le veut ; la licence dit
   ce qui est permis le jour où il l'ouvre ou le partage.
2. **Le contenu de la couche `banque`** (chapitres, cartes, schémas
   maison) : **CC BY-SA 4.0**. Attribution à l'Académie et à l'auteur
   du domaine ; partage aux mêmes conditions. C'est ce qui rend la
   bibliothèque commune légale : ce qu'un joueur livre peut être repris
   par le suivant.
3. **La couche `interne`** : aucune licence de redistribution ; elle
   dérive de supports acquis. Elle ne quitte jamais son propriétaire.
4. **Les images** : chacune porte sa licence ; les schémas maison sont
   CC BY-SA ; les icônes game-icons restent CC BY 3.0 avec attribution
   visible.
5. **Les sources** ne sont jamais relicenciées : on paraphrase et on
   lie ; le droit de courte citation s'applique.

## Contexte

Le brief du 02/09 veut que « quelqu'un puisse reprendre tout le repo »
et que « le travail de digestion fait par les autres » serve aux
suivants. Sans licence écrite, rien de tout ça n'est permis.

## Conséquences

- Un fichier `LICENCE` (code) et une mention dans `banque/README` (à
  créer) au chantier `ACA-BIBLIOTHEQUE-1`.
- Le manifeste de livraison porte la licence de la banque livrée ; le
  serveur refuse une livraison `banque` sans CC BY-SA.

## Réouverture

Si JB veut un jour vendre une formation : ce serait une autre décision,
sur un autre contenu ; celle-ci ne s'annule pas rétroactivement.

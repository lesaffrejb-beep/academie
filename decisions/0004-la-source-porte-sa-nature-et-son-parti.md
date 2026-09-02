# 0004, Une source porte sa nature et son parti

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« qu'on voie afficher la source sur la question, comme ça
  on peut se méfier si telle source est biaisée politiquement »)

## Décision

Chaque entrée de `source` porte, en plus du texte et de l'URL, une
**nature** parmi une liste fermée et, quand il existe, un **parti** :

| `nature` | Exemples |
|---|---|
| `texte-officiel` | Légifrance, Journal officiel, un arrêté municipal |
| `jurisprudence` | Judilibre, une décision citée avec sa référence |
| `institution` | ANIL, ADEME, ANAH, HAS, Santé publique France, Cerema |
| `norme` | DTU, norme NF, fiche AQC, guide CSTB |
| `doctrine` | manuel universitaire, revue juridique, thèse |
| `presse-pro` | presse spécialisée signée |
| `organisation-pro` | fédération ou syndicat de professionnels |
| `association` | association de consommateurs ou de copropriétaires |
| `editeur` | éditeur de logiciel, cabinet, courtier, blog commercial |
| `support-interne` | support de formation d'un employeur, non redistribuable |
| `terrain` | observation anonymisée validée par le propriétaire du domaine |

`parti` est une chaîne courte et honnête : « défend les syndics »,
« défend les copropriétaires », « vend la prestation décrite », ou absent.
Le registre du domaine (`sources/REGISTRE.md`) pose ces deux valeurs
**une fois par source** ; les cartes héritent.

Le front affiche sur chaque question la source, sa nature et son parti.
Une carte dont la seule source est `editeur` ou `organisation-pro` ou
`association` porte un marqueur « à recouper » visible tant qu'une source
`texte-officiel`, `jurisprudence`, `institution` ou `norme` ne la
confirme pas.

## Contexte

L'inventaire NotebookLM du 29/08 a montré que 157 des 189 sources web du
carnet de JB sont commerciales, et qu'une réponse « juste » y était
sourcée sur un vendeur. Le contrat carte-v1 exige une source, pas sa
nature.

## Conséquences

- Contrat carte-v2 et valideur : `nature` obligatoire par source, valeurs
  fermées, `parti` libre. Migration des 84 cartes : assignation par
  domaine d'URL puis relecture (chantier `ACA-SOURCES-1`).
- Le tri des sources de l'usine (étape 3) remplit désormais `nature` et
  `parti` au lieu du seul lot fiable/commercial/douteux/doublon.
- Le brouillard « à recouper » est un état de carte visible, pas un
  refus : une carte `editeur` bien faite se joue, marquée.

## Réouverture

Si la liste fermée refuse une source légitime trois fois, on l'étend par
une décision, pas par une valeur libre.

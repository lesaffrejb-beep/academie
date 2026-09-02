# 0021, Le modèle peut écrire, à condition de dire d'où ça vient et de se faire relire

- Statut : acceptée
- Date : 02/09/2026 (soir)
- Décideur : JB (« on pourrait accepter qu'un LLM complète les trous,
  voire génère des chapitres, tant qu'il crawle des sources fiables,
  cite ses sources, note que c'est généré par tel modèle à telle date,
  vérifié par X et Y ; si pas de source, le reconnaître ; et de temps en
  temps des runs de vérif vont voir si les choses ont changé »)

## Décision

1. **Le modèle a le droit d'écrire un chapitre ou une carte**, y
   compris pour combler un trou du programme, à condition de chercher
   ses sources sur la liste blanche et sur des domaines fiables
   (`sources/LISTE-BLANCHE.md`, registre), de les citer, et de les
   croiser quand c'est possible. Chercher, citer, croiser : la manière
   de faire des outils de recherche assistée, sans en faire une
   dépendance.
2. **Toute carte et tout chapitre portent un tampon de provenance**,
   affiché au joueur : le modèle, la date de génération, le nombre de
   sources retrouvées et concordantes, qui a relu (agent frais, date),
   et l'historique des vérifications. Par exemple : « Généré par Claude
   Opus le 21/01/2026 · 2 sources concordantes · relu le 22/01 ».
3. **Sans source retrouvée, on le dit.** Une carte peut exister avec
   zéro source si le modèle l'écrit explicitement (`sans_source: true`)
   et si elle ne porte **aucun chiffre, date, délai, seuil ni montant** :
   pour ces choses-là, la règle dure de labor tient, une valeur sans
   source ne se dit pas. Une carte sans source est servie avec la
   mention « sans source retrouvée », marquée « à recouper », et passe
   en tête de la file de vérification.
4. **La double passe par agent frais reste obligatoire** avant `valide`,
   pour tout ce qui est généré, sans exception.
5. **Des runs de vérification tournent périodiquement** (chantier
   `ACA-VERIF-1`) : un tirage de cartes (les sans-source d'abord, puis
   les plus anciennes, les plus révisées, celles de nature juridique),
   une recherche sur les sources fiables pour voir si quelque chose a
   changé, une ligne d'historique par carte, et un statut qui bouge si
   besoin (`verifie` rafraîchi, ou `signale`, ou `perime`). Ils tournent
   chez le propriétaire du domaine, à son coût, jamais sur le serveur.
6. **L'humilité est écrite** : toutes les sources sont imparfaites, les
   manuels et les professeurs aussi. Ce que l'Académie garantit n'est
   pas la vérité, c'est la transparence : qui a écrit, quand, avec quoi,
   vérifié comment, et un bouton pour dire que c'est faux.

## Contexte

La doctrine du matin interdisait toute carte sans source et faisait de
tout sujet non couvert un trou nommé. JB a tranché le soir : les modèles
de dernière génération, avec un pipeline de garde-fous (recherche
citée, relecture par agent frais, valideur, runs de vérification),
disent assez peu de bêtises pour qu'on préfère un chapitre tamponné et
relu à un trou. Le trou reste écrit dans l'inventaire ; il ne bloque
plus la génération.

## Conséquences

- `DOCTRINE.md` invariant 1 réécrit ; `AGENTS.md` règle 3 amendée.
- Contrat v2 : bloc `provenance` obligatoire (`modele`, `genere_le`,
  `session`, `sources_retrouvees`, `sans_source`), `historique` alimenté
  par les runs ; le valideur refuse une carte sans source qui contient
  un chiffre ou une date.
- `gabarit-domaine/USINE.md` : le refus 1 et la règle du trou nommé
  sont amendés ; l'étape 4 gagne la recherche sur sources fiables.
- `BLUEPRINT.md` §10 : la ligne de provenance à l'écran.
- `ROADMAP.md` : `ACA-VERIF-1` ; `ACA-CONTENT-2` génère avec crawl et
  tampon.
- `METHODE.md` §29.

## Réouverture

Si les runs de vérification trouvent plus de 5 % de cartes fausses sur
un lot généré, le lot repasse en `brouillon` entier et le prompt de
génération se corrige avant tout nouveau lot.

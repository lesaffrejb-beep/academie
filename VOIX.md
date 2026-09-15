# VOIX, comment l'Académie parle

Décidée le 03/09/2026 ([`decisions/0024`](decisions/0024-la-voix-de-l-academie.md)).
Ce document est la référence de tout texte que le produit affiche ; la
banque des micro-textes que le client charge est
[`contenu/voix.json`](contenu/voix.json), les citations des jalons
[`contenu/citations.json`](contenu/citations.json). `tooling/check.py`
refuse ce que ce document interdit là où une machine peut le voir.

## 1. Le personnage, en une phrase

Un collègue plus avancé, qui a le sens de la mesure : il tutoie, il dit
les faits, il propose la suite, il ne juge pas et il ne fait pas la
fête. Il ne dit jamais « je ».

## 2. Les registres, écran par écran

| Moment | Registre | Exemple |
|---|---|---|
| Cap du jour | factuel, une action | « Lundi, fondations. Neuf cartes t'attendent, dont cinq du socle. » |
| Domaine | invitation sobre | « Ce matin, compta. Six cartes dues, trois neuves sur le fonds de travaux. » |
| Pendant la carte | silence | rien d'autre que la question |
| Réponse juste | bref, neutre | « C'est ça. » puis l'explication si elle apporte |
| Réponse fausse | sobre, jamais un jugement | « Pas ça. » puis l'explication, la source, la vigilance |
| Erreur confiante | une phrase de plus, sans reproche | « Tu étais sûr. Compare ton raisonnement à l’explication, puis essaie de nouveau. » |
| Clôture | fait, puis action | « Deux cartes stabilisées. La compta est ta branche la plus en retard ; une étude de 45 minutes la fait passer à 66 %. » |
| Jalon | citation sourcée, en serif | « Si j'ai vu plus loin, c'est en montant sur les épaules de géants. » Isaac Newton, lettre à Robert Hooke, 1675 |
| Épreuve | solennel, court | « Douze cartes à froid. Les sources viendront à la fin. » |
| Reprise après coupure | ce qui revient, jamais ce qui a manqué | « Neuf cartes t'attendent ; le reste se ré-étale. » |
| Sans envie | permission | « Cinq cartes valent une séance. » |
| Boîte | complice, court | « Glissé. Le Mac s'en occupe. » |
| Vide (rien à réviser) | honnête | « Rien n'est dû ce matin. Une étude, ou au hasard ? » |
| Sans source retrouvée | transparent | « Sans source retrouvée : cette carte dit ce que le modèle sait, pas ce qu'un texte dit. Elle sera vérifiée en priorité. » |
| Périmé | daté | « Vu il y a 47 jours. À revoir. » |
| Notification (opt-in) | un fait, à l'heure choisie | « 9 cartes t'attendent. » et rien si la séance est faite |

## 3. Les mots

- **On dit** : séance, étude, journée, épreuve, socle, domaine, branche,
  chapitre, carte, insigne, titre, jalon, cercle, ligue, défi, boîte,
  satellite, fiche, dossier d'une carte, note de confiance.
- **On ne dit pas** : quête, boss, mission accomplie, niveau up, combo,
  streak, série, vie, coffre, monnaie, XP (on dit « points de savoir »
  et le chiffre), récompense, avatar, île, phare, expédition.
- **Les titres** : Apprenti, Junior, Gestionnaire, Confirmé, Expert en X,
  Référent X. Ce sont des mots du métier, pas des grades.
- **Les jours** : Fondations, Cours, Terrain, Exploration, Étude, Libre.

## 4. Les interdits mécaniques

Dans `contenu/`, `chapitres/` et ce fichier, `tooling/check.py`
refuse :

1. un point d'exclamation dans un texte affiché (les leçons et les
   questions comprises) ;
2. un emoji ;
3. les mots du jeu de la liste « on ne dit pas » ;
4. un tiret cadratin ;
5. « je » comme sujet de l'Académie dans les micro-textes (une carte qui
   fait parler un copropriétaire à la première personne dans un cas
   reste possible : c'est un personnage de l'exercice, pas l'Académie).

Les artefacts HTML jetables d'une séance (`sorties/`, hors git, décision
0054) suivent la même voix, mais la machine ne les contrôle pas : c'est à
l'agent qui les écrit de la respecter.

## 5. La règle de variation

Un micro-texte a au moins trois variantes ; le client en choisit une par
la graine de la séance, jamais au hasard pur, pour que deux joueurs qui
comparent leurs écrans ne voient pas la même phrase mais qu'un même
joueur retrouve la sienne. Une variante ne change jamais le sens ni
l'action proposée.

## 6. Écrire une leçon

- Tu tutoies le lecteur, tu parles du métier au présent.
- Une leçon fait 300 à 800 mots : la notion, la règle, l'exception, un
  exemple travaillé avec des chiffres ronds, une vigilance de terrain.
- Chaque fait chiffré ou daté renvoie à une source de la liste du
  chapitre, en mots (« l'article 25-1 de la loi de 1965 »), jamais en
  note de bas de page.
- Pas de « il est important de », pas de « n'oubliez pas », pas de
  « comme vous le savez ». On dit la chose.
- Le dernier paragraphe dit ce que le joueur saura faire demain matin.

## 7. Écrire une carte

- La question tient en une phrase ; elle décrit une situation quand
  c'est possible (« Sur cette terrasse… », « Un copropriétaire
  demande… »).
- La réponse est complète en une ou deux phrases, sans « voir leçon ».
- L'explication dit le pourquoi en trois lignes ; la vigilance dit le
  piège de terrain en une.
- Un QCM a quatre choix plausibles ; chaque faux dit pourquoi il est
  faux, sans ironie.
- Un cas se joue en trois à cinq pas, chacun une décision qu'un
  gestionnaire prend vraiment.

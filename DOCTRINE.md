# DOCTRINE, l'Académie en une page et demie

Écrite le 02/09/2026 sur le brief de JB
([`travail/2026-09-02-brief-jb.md`](travail/2026-09-02-brief-jb.md)). C'est
la constitution du dépôt : ce que l'Académie est, ce qu'elle refuse, et
dans quel ordre on lit le reste. Une règle qui change ici passe par une
décision datée dans [`decisions/`](decisions/README.md).

## 1. Ce que c'est

L'Académie est **l'école d'un métier, jouée tous les jours**. Elle
transforme des sources vérifiées en un arbre de compétences qu'on
conquiert par des exercices de rappel, de diagnostic et de synthèse,
planifiés par un algorithme de mémoire. Elle est conçue pour un adulte
qui travaille : quinze minutes le matin dans le tram, une journée entière
quand il décide d'apprendre son métier.

Le premier métier est **gestionnaire de copropriété** ; le premier joueur
est JB ; les suivants sont ses collègues (même arbre), puis Arthur (autre
métier, même moteur), puis quiconque tient un dépôt de sources et un
abonnement à un modèle.

## 2. Ce que ce n'est pas

- **Pas un chatbot.** Le modèle fabrique et corrige, il n'est jamais
  l'écran d'accueil.
- **Pas un produit vendu.** Aucun paiement demandé à un joueur, jamais.
  Chacun apporte son dépôt et son abonnement ; JB porte le serveur pour
  son cercle ; tout le monde peut héberger le sien.
- **Pas un instrument d'évaluation.** Les joueurs d'une même Académie se
  voient par défaut (arbre, titre, insignes, compteur), comme sur une
  application de sport, et chacun peut se masquer d'un geste. Mais
  personne ne reçoit jamais le carnet d'erreurs, les réponses ni les
  temps de quelqu'un d'autre, et il n'existe ni agrégat, ni export, ni
  classement imposé pour un manager ou un tuteur.
- **Pas un jeu pour enfants.** Ni genre, ni âge, ni bateau : une direction
  artistique adulte, sobre et vivante ([`DIRECTION-ARTISTIQUE.md`](DIRECTION-ARTISTIQUE.md)).
- **Pas un miroir de labor.** Aucune donnée client, aucun immeuble nommé,
  aucun mail, aucune pièce du portefeuille n'entre ici. Ce qui vient du
  travail réel arrive anonymisé, validé, et avec sa provenance.

## 3. Les dix invariants

1. **Toute carte dit d'où elle vient.** Elle porte ses sources (nature,
   date de vérification, péremption si un chiffre bouge) et son tampon
   de provenance : quel modèle ou quelle personne l'a écrite, quand,
   combien de sources ont été retrouvées et croisées, qui l'a relue. Le
   modèle a le droit d'écrire, à condition de chercher ses sources sur
   les domaines fiables, de les citer, et d'avouer quand il n'en a pas
   trouvé : une carte « sans source retrouvée » existe, se dit comme
   telle, et passe en tête de la file de vérification ; mais **un
   chiffre, une date, un délai, un seuil ou un montant sans source ne se
   dit pas**. Le trou s'écrit dans l'inventaire, il ne bloque plus le
   chapitre ([`decisions/0021`](decisions/0021-le-modele-ecrit-la-provenance-s-affiche.md)).
2. **La source s'affiche, avec son parti.** Le joueur voit sur chaque
   question d'où elle vient et si l'émetteur défend un intérêt (syndics,
   copropriétaires, vendeur d'une prestation). Il peut se méfier en
   connaissance de cause. Seule exception : pendant une épreuve, les
   sources apparaissent à la fin, pas pendant.
3. **Le valideur fait foi.** Rien de rouge n'est servi. Un contrat qui
   diverge du valideur se corrige ; un valideur ne s'affaiblit jamais pour
   faire passer une carte.
4. **Tout est question.** On fait répondre avant d'expliquer ; la leçon
   arrive après la tentative, et se termine par du rappel. Aucune
   mécanique n'entre sans son entrée sourcée dans
   [`METHODE.md`](METHODE.md).
5. **L'algorithme est le professeur.** Le joueur choisit où aller sur
   l'arbre et combien de temps il a ; il ne choisit jamais le format de
   l'exercice ni le moment du rappel.
6. **L'état joueur est un journal append-only, séparé de la banque.** Il
   se recalcule toujours depuis le journal, se synchronise par union, et
   s'exporte à tout moment. La banque de connaissances ne contient jamais
   un état joueur.
7. **Le dépôt de sources reste chez le joueur.** Le serveur ne voit que
   des fiches JSON validées, dérivées par paraphrase et lien. Le
   traitement par modèle tourne chez le joueur, à son coût.
8. **Le moteur ne connaît aucun métier.** Domaines, branches, chapitres,
   quotas et habillage vivent dans la configuration et la banque du
   domaine. Changer de métier, c'est changer de banque.
9. **Jamais de dette, jamais de honte.** Le compteur monte, il ne descend
   pas ; une coupure se ré-étale ; la comparaison n'est jamais imposée ;
   tout mécanisme d'engagement se coupe s'il dégrade le rituel mesuré.
10. **Les actes irréversibles sont humains.** Envoi, publication, dépense,
    suppression, migration : un agent prépare et prouve, JB tranche.

Et une humilité écrite : toutes les sources sont imparfaites, les manuels
et les professeurs aussi. L'Académie ne garantit pas la vérité ; elle
garantit la transparence (qui a écrit, quand, avec quoi, vérifié
comment), la relecture par un agent qui n'a pas écrit, des runs de
vérification qui retournent voir si les choses ont changé, et un bouton
pour dire que c'est faux.

## 4. La hiérarchie des documents

Quand deux documents divergent, le plus haut fait foi et le plus bas se
corrige.

| Rang | Document | Ce qu'il porte |
|---|---|---|
| 1 | ce fichier | ce qu'on est, ce qu'on refuse |
| 2 | [`CONTRAT-CARTE-V1.md`](CONTRAT-CARTE-V1.md) et `app/valide_banque.py` | le format d'une carte ; le valideur prime sur le texte. [`CONTRAT-CARTE-V2.md`](CONTRAT-CARTE-V2.md) et [`contrats/`](contrats/README.md) prendront ce rang le jour où leur valideur existe ; d'ici là ce sont des propositions de rang 6 |
| 3 | [`BLUEPRINT.md`](BLUEPRINT.md) | le produit tel qu'il est imaginé le 02/09/2026 |
| 4 | [`PROGRAMME.md`](PROGRAMME.md) | ce qu'on enseigne au gestionnaire de copropriété, dans quel ordre |
| 5 | [`METHODE.md`](METHODE.md), [`CADRAGE-SCIENTIFIQUE.md`](CADRAGE-SCIENTIFIQUE.md) | pourquoi chaque mécanique existe, avec sa source |
| 6 | [`ARCHITECTURE.md`](ARCHITECTURE.md) | comment c'est construit et où c'est stocké |
| 7 | [`DIRECTION-ARTISTIQUE.md`](DIRECTION-ARTISTIQUE.md) | à quoi ça ressemble et comment ça bouge |
| 8 | [`ROADMAP.md`](ROADMAP.md), `roadmap.json` | ce qu'on fait ensuite, avec la preuve attendue |
| 9 | [`decisions/`](decisions/README.md) | pourquoi on a tranché comme ça, daté |
| 10 | [`gabarit-domaine/`](gabarit-domaine/README.md), [`CORPUS.md`](CORPUS.md), [`boite/`](boite/README.md), [`sources/`](sources/README.md), [`programme/`](programme/README.md), [`serveur/`](serveur/README.md), [`web/`](web/README.md) | les guides opérationnels et les squelettes |
| 11 | [`archive/`](archive/roadmaps/README.md) | l'histoire, non pilotante |

## 5. Qui fait quoi

- **JB** décide des gates, des dépenses, de ce qui se publie, et joue.
  Son rituel réel est la mesure de tout.
- **Un agent** lit `AGENTS.md`, cette doctrine, puis uniquement les
  documents que sa mission exige. Il travaille par résultat prouvé
  (`ROADMAP.md`), écrit ses arbitrages dans `decisions/`, ajoute une
  entrée à `METHODE.md` pour toute mécanique nouvelle, et laisse
  `python3 app/tests.py` puis `python3 tooling/check.py` verts.
- **Un joueur invité** joue la banque partagée avec son compte et son
  état. Il ne fabrique rien pour les autres et personne ne fabrique
  pour lui : s'il veut un domaine, il tient son dépôt-domaine
  ([`gabarit-domaine/USINE.md`](gabarit-domaine/USINE.md)).

## 6. Ce qui tue le produit, et la parade

| La mort | La parade, en place ou à construire |
|---|---|
| JB n'ouvre plus l'app le matin | le rituel est le gate de tout le reste ; on répare le format, jamais la culpabilité |
| Une carte fausse est apprise | valideur, double passe par agent frais, source affichée, bouton « fausse » qui sort la carte |
| Le front absorbe tout l'effort et le fond stagne | le front est déclaré jetable ; le moteur, la banque et le programme sont la valeur |
| Un collègue se sent surveillé | visibilité symétrique et consentie, carnet d'erreurs privé, aucun export pour un tiers |
| L'arbre est fini, l'ennui s'installe | l'arbre pousse par chapitres satellites (la boîte) et par niveaux 4 et 5 sans fin |
| Le stock de neuf s'assèche en silence | l'agent-compagnon interpelle et propose la fabrication ; les trous sont nommés |

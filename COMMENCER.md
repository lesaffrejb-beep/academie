# COMMENCER : un pseudo, un parcours

Ce que vit quelqu'un qui arrive à l'Académie, et ce qu'il fait s'il veut
son propre parcours. Écrit le 03/09/2026 ; l'écran correspondant est le
chantier `ACA-ONBOARDING-1`, après le client v2. D'ici là, cette page est
l'accueil, et les prompts de [`prompts/`](prompts/README.md) sont les
boutons.

## 1. Un pseudo

Tu choisis un pseudo. Il est visible de tous les joueurs de ton cercle
par défaut ([`decisions/0010`](decisions/0010-les-cercles-et-la-visibilite.md)) :
un prénom, un surnom, ce que tu veux, pas forcément ton nom. Ton carnet
d'erreurs n'est jamais visible, ton arbre l'est. Tu peux masquer un
domaine entier à ton cercle, jamais une carte. Personne ne reçoit de
rapport sur toi.

Le pseudo est ton identifiant de journal : il ne change pas. Ce que tu
apprends est à toi (`etat/`, jamais dans git, jamais chez un tiers).

## 2. Le catalogue

Le catalogue vit dans [`programme/catalogue.json`](programme/catalogue.json).
Au 03/09/2026, il tient en une ligne :

| Parcours | État | Ce qu'on peut faire aujourd'hui |
|---|---|---|
| Gestion de copropriété | squelette : dix domaines, 387 chapitres, cinq niveaux, parcours de treize semaines ([`SYLLABUS.md`](SYLLABUS.md)) ; 84 cartes v1 jouables, 2 chapitres v2 témoins | lire le programme, jouer les cartes existantes ; les chapitres se remplissent chantier par chantier (`ACA-CONTENT-2`) |
| Entrer en IFSI, puis devenir infirmier | squelette : dix domaines, 310 chapitres, cinq niveaux, douze semaines vers l'entrée ([`SYLLABUS-IFSI.md`](SYLLABUS-IFSI.md)) ; aucune carte encore | lire le programme ; les chapitres arrivent avec le kit de domaine (`ACA-DOMAIN-KIT-1`) |

Tu prends un parcours du catalogue : il est à tous, personne ne paie
rien, et ce que tu fais remonter (une carte fausse signalée, une fiche
de ta boîte adoptée) profite aux suivants.

## 3. Créer le vôtre

Tu n'as pas ton métier ou ta matière dans le catalogue. Tu crées ton
parcours, avec ton outil et ton abonnement ; le produit ne te demande
rien ([`decisions/0008`](decisions/0008-chacun-son-depot-et-son-abonnement.md)).

**Étape A, rassembler.** Mets dans un dossier de ta machine (par
exemple `~/Academie/<mon-metier>/sources/`) ce que tu as : cours,
référentiels, textes officiels, annales, PDF publics. Copie, ne déplace
rien. Mets à part, dans `sources/interne/`, ce qui est interne à ton
employeur ou porte des noms : ça ne sortira jamais de ta machine. Ne
mets rien qui contienne des données de clients, de patients, de
collègues.

**Étape B, l'outil.** Il te faut un agent de code avec accès au disque et
à git : Claude Code, Codex, Antigravity, Cursor ou un autre. Une session
web sans accès aux fichiers ne peut pas faire ce parcours. Il te faut
aussi `git`, Python 3 et poppler (`brew install poppler` sur Mac,
`apt install poppler-utils` sur Linux).

**Étape C, coller.** Ouvre ton outil dans un dossier vide et colle le
contenu de [`prompts/creer-un-parcours.md`](prompts/creer-un-parcours.md).
Le prompt dit à l'agent qui il est, quoi cloner, quoi lire, quelles
questions te poser, et il l'oblige à travailler par petites unités que
la machine vérifie ([`MODELES.md`](MODELES.md), [`decisions/0027`](decisions/0027-pas-a-pas-impose-points-de-sauvegarde-classes-de-modeles.md)).

**Étape D, répondre.** L'agent te pose une question à la fois : ton
métier, pourquoi tu apprends et pour quand, combien de temps par jour,
où tu en es, où sont tes documents, quelles sources ton métier tient
pour fiables. Réponds court ; il n'a pas besoin de plus.

**Étape E, laisser faire, sans lâcher.** L'agent prépare tes documents
un par un, les relit par unités, écrit une fiche par document, puis
propose le squelette de ton programme (domaines, branches, chapitres,
niveaux) sans rédiger de cours. À la fin, il te montre un sommaire et
s'arrête : tu valides, tu corriges, tu retires. Si la session coupe,
colle [`prompts/reprendre.md`](prompts/reprendre.md) : tout ce qui est
fait est sur disque.

**Ce que tu obtiens.** Un dépôt-domaine à toi (copie du
[`gabarit-domaine/`](gabarit-domaine/README.md)), tes sources et leurs
fiches, un registre, un programme en données et son sommaire lisible.
Les chapitres viennent ensuite, écrits par un grand modèle, relus, et
ce que tu livres au serveur profite aux suivants sous licence ouverte
([`decisions/0018`](decisions/0018-licences.md)).

## 4. Ajouter tes documents à un parcours qui existe

Tu suis le parcours copropriété et tu as un PDF, une formation, un
rapport qui pourrait servir. Même outil, même méthode : colle
[`prompts/ajouter-des-documents.md`](prompts/ajouter-des-documents.md).
Le document devient une source de la bibliothèque, pas un chapitre
([`decisions/0026`](decisions/0026-un-document-n-est-pas-un-chapitre.md)) :
il nourrit l'arbre par une contribution, une lecture, un satellite ou
une correction, et l'agent te dit lesquels il propose.

## 5. Ce que l'écran fera (chantier `ACA-ONBOARDING-1`)

Trois écrans, dans la voix de [`VOIX.md`](VOIX.md), textes dans
`contenu/voix.json` (`arrivee.*`) :

1. **Le pseudo** : un champ, la règle de visibilité en une phrase, le
   bouton « C'est moi ».
2. **Le catalogue** : une carte par parcours du catalogue (titre, état,
   nombre de chapitres, ce qu'on peut faire aujourd'hui) et une carte
   « Créer le vôtre ».
3. **Créer le vôtre** : les étapes A à E ci-dessus, un bouton « Copier
   le prompt » par prompt, et rien d'autre. Aucune saisie de documents
   dans l'app : ils restent sur la machine de l'élève.

Le quiz de positionnement ([`BLUEPRINT.md`](BLUEPRINT.md) §11) vient
après le choix du parcours, pas avant.

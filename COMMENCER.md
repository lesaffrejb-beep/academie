# COMMENCER : un pseudo, un parcours

Ce que vit quelqu'un qui arrive à l'Académie, et ce qu'il fait s'il veut
son propre parcours. Écrit le 03/09/2026, actualisé le 21/09/2026. Le
front est retiré
([`decisions/0054`](decisions/0054-plus-de-front-le-depot-est-l-interface.md)) :
l'accueil est ce dépôt, discuté par un agent, et les prompts de
[`prompts/`](prompts/README.md) sont les boutons. Les écrans décrits au
§5 sont historiques.

## 0. Un poste neuf

Ouvre l'agent de code à la racine du dépôt et demande-lui de démarrer.
Sur Windows, le premier geste est PowerShell, dans ce dossier, même si
tu crois avoir Python : le script est le seul à dire quel interpréteur
répond vraiment.

```powershell
powershell -ExecutionPolicy Bypass -File demarrer.ps1
```

Ce script détecte `py -3`, `python3` ou `python` pour de vrai, retient
celui qui répond en 3.12 ou plus, transmet cet interpréteur au
diagnostic complet et reste muet s'il n'en trouve aucun. Même quand un
`python` répond déjà, il l'interroge avant de conclure : un alias
Microsoft Store ou une version trop ancienne ne compte pas. Il installe
les manquants avec `winget --scope user` si on le lui demande
(`-Installer`), sans élévation automatique, et vérifie le résultat
avant de dire quoi que ce soit.

Sur macOS ou Linux, ou après le script Windows, le diagnostic est le
même en Python :

```sh
python3 app/demarrer.py --json
```

Il vérifie que Git répond, que Python atteint 3.12, que le dossier est
bien la racine d'un clone et que le hook pre-commit est posé.
`demarrer.py` seul ne fait que diagnostiquer ; pour installer les outils
manquants, c'est `python3 app/demarrer.py --installer` (autorisation
déjà donnée, pas de confirmation à répéter). Un dossier reçu en ZIP suit
`--guide-zip` : on clone à côté, on ne réécrit jamais le dossier
existant.

## 0 bis. Chaque matin

Avant de jouer, sur un clone propre, sans modification locale :

```sh
git pull --ff-only
```

Jamais `git reset`, `git clean` ni `git pull --autostash` ici : l'état
du joueur et tes notes locales ne doivent pas être réécrits. Si le
réseau est coupé, le moteur, la banque et le journal locaux restent
utilisables et seule la mise à jour Git attend. Une séance menée par un
agent dont le modèle vit en ligne demande, lui, une connexion : hors
ligne, tu peux lire l'état local et l'export, mais pas faire tourner un
agent distant.

## 1. Un pseudo

Tu choisis un pseudo : un prénom, un surnom, ce que tu veux, pas
forcément ton nom. Ce parcours local ne le publie nulle part : il nomme
ton dossier `etat/<pseudo>/` et aucun autre joueur ne le voit par ce
chemin. Les cercles et la visibilité décrits par la
[`décision 0010`](decisions/0010-les-cercles-et-la-visibilite.md)
visaient un serveur et un front retirés
([`décision 0054`](decisions/0054-plus-de-front-le-depot-est-l-interface.md)).
L'état réel d'un éventuel déploiement distant n'est pas audité ici : ce
document décrit le parcours local et ne garantit rien sur un service
qui tournerait encore ailleurs.

Le pseudo est ton identifiant de journal : il ne change pas. Ce que tu
apprends est à toi, sur ta machine (`etat/`, jamais dans git). Ce
parcours-ci n'ouvre aucun compte distant et ne synchronise rien depuis
`etat/` : ce qui s'y écrit reste un fichier local.

La nuance qui compte : quand un agent lit un de tes documents ou une
partie de ton journal pour te répondre, ce texte passe par le modèle que
tu as choisi et par son fournisseur, selon son contrat et sa
configuration. La confidentialité locale du fichier ne veut pas dire que
rien ne quitte jamais la machine pendant une session d'agent. Range dans
`sources/interne/a-preparer/` ce qui ne doit pas sortir, lis le contrat
de ton fournisseur, et ne fais lire à un agent que ce que tu acceptes de
lui confier.

L'état d'un pseudo ne voyage pas d'une machine à l'autre par `git pull` :
sans transfert explicite, le Mac et le poste de travail tiennent deux
copies indépendantes de la progression de la même personne, qui
divergent sans prévenir. Le profil actif d'une machine se choisit avec
`python3 app/academie.py profil --activer <pseudo>` ; le transfert se
fait par `python3 app/academie.py exporter <fichier>` puis `importer`.

## 2. Le catalogue

Le catalogue vit dans [`programme/catalogue.json`](programme/catalogue.json)
et `python3 app/academie.py accueil` le sert tel qu'il est, avec les
compteurs du moment. Ne recopie pas de nombres ici : ils datent vite.
Aujourd'hui la commande liste la gestion de copropriété et le parcours
IFSI, chacune avec son état éditorial et ce qui est jouable
([`SYLLABUS.md`](SYLLABUS.md),
[`SYLLABUS-IFSI.md`](SYLLABUS-IFSI.md)).

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
aussi `git` et Python 3.12+ (`python3 app/demarrer.py` vérifie et
installe les manquants). Poppler ne sert qu'à extraire le texte de PDF
quand tu prépares tes propres documents (`brew install poppler` sur Mac,
`apt install poppler-utils` sur Linux) : jouer une séance n'en a pas
besoin et le démarrage ne l'installe pas.

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
Les chapitres viennent ensuite, écrits par un modèle, relus, et
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

## 5. Ce que l'écran aurait fait (historique, chantier `ACA-ONBOARDING-1`)

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

Ces trois écrans visaient le client web retiré par
[`décision 0054`](decisions/0054-plus-de-front-le-depot-est-l-interface.md).
Ils ne sont ni construits ni au programme : ce qui les remplace est la
surface `python3 app/academie.py accueil` et
`python3 app/academie.py profil`, décrite au §0 et dans
[`prompts/arriver.md`](prompts/arriver.md). Aucune visibilité entre
joueurs n'existe tant qu'un service n'est pas rouvert et consenti.

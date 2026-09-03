# USINE — le guide d'agent pour fabriquer un domaine

Squelette du futur SKILL de M10. Écrit le 29/08/2026, **avant** la
soirée artisanale : ce qui suit fixe la structure, les portes et les
refus. Le contenu fin de plusieurs étapes ne peut pas être inventé
d'avance, il viendra de la première fabrication réelle (O7) — ces
endroits portent la marque **[À COMPLÉTER PAR M10]**.

Lecteur visé : **un agent IA** qui déroule le parcours avec un humain
qui ne code pas. Le ton du guide est celui d'un accompagnateur : une
question à la fois, jamais deux étapes en parallèle.

Source de vérité du parcours : [`../ARCHITECTURE.md`](../ARCHITECTURE.md)
§7 et [`../decisions/0008`](../decisions/0008-chacun-son-depot-et-son-abonnement.md)
(le `SPEC-PRODUIT` d'août, archivé, en est l'origine). Si ce guide et
l'architecture divergent, l'architecture fait foi et ce fichier se
corrige. Depuis le 02/09/2026, l'étape 3 remplit aussi `nature`, `parti`
et fiabilité par source (`decisions/0004`, `sources/README.md`) et
s'appuie sur `sources/LISTE-BLANCHE.md` pour dire au joueur quoi
déposer et où trouver le reste ; les entrées PDF scanné (OCR), vidéo
(sous-titres ou transcription locale) et capture d'écran (vision, chez
le joueur) sont admises à l'étape 1.

---

## Comment ce guide se déroule

Le parcours est une **suite de portes**, pas une liste de courses. À
chaque étape :

- un **objectif** en une phrase, dit au joueur avant de commencer ;
- un **livrable** : un fichier écrit sur le disque, pas une réponse
  dans le fil de conversation ;
- des **garde-fous** : ce qui fait échouer l'étape ;
- une **porte** : la condition pour passer à la suivante. Tant que la
  porte est fermée, on ne passe pas. On le dit au joueur, on ne
  contourne pas.

L'agent ne décide jamais seul de forcer une porte. S'il pense qu'une
porte est trop stricte pour ce domaine, il le dit et attend un
arbitrage humain.

---

## Les cinq refus (hors du déroulé, valables à toutes les étapes)

Ils sont sortis des étapes exprès : une règle citée dans une seule
étape se dilue à la troisième heure de session.

1. **Aucune carte sans provenance, aucun chiffre sans source.** (Amendé
   le 02/09/2026, `decisions/0021`.) Une source, c'est un texte
   identifiable et, quand elle existe, une URL. Le modèle a le droit
   d'écrire s'il a cherché sur les domaines fiables
   (`sources/LISTE-BLANCHE.md`), cité ce qu'il a trouvé, et dit
   combien ; s'il n'a rien trouvé, il l'écrit (`sans_source: true`) et
   la carte ne porte alors ni chiffre, ni date, ni délai, ni montant.
   Un « c'est bien connu » n'est toujours pas une source.
2. **Aucune donnée personnelle réelle, dans aucune couche.** Pour un
   domaine santé, cela veut dire : **aucune donnée patient, aucune
   photo clinique non publiée sous licence** — les cas, tracés et
   images viennent de banques pédagogiques publiées, ou sont fictifs
   et annoncés comme tels. Le scanner anti-fuite est calibré sur un
   autre métier : il ne détectera pas une donnée de santé. Ici la
   barrière est cette règle et le contrôle de licence, rien d'autre.
3. **Aucune image sans licence.** Le contrat exige `licence` et
   `credit` sur toute image. Une image trouvée sans licence identifiée
   n'entre pas, même « juste pour illustrer ».
4. **Aucune recopie, aucun scraping.** On dérive : paraphrase plus
   lien. Pas de robot qui « sort le cours » d'un site (conditions
   d'utilisation et droit d'auteur). Un cours PDF obtenu par une
   connaissance sert à **dériver** des cartes dans le dépôt du joueur ;
   il n'est jamais redistribué ni poussé au serveur tel quel.
5. **Aucune publication sans valideur vert.** Le valideur mécanique
   est le dernier juge, y compris contre l'avis de l'agent et du
   joueur (étape 6).

## La règle du trou nommé

Elle mérite son propre titre parce qu'elle est contre-intuitive et
que c'est elle qui tient la promesse « il ne faut pas me dire de
bêtises ».

> Si le plan de région réclame un sujet et qu'**aucune source fiable
> sous la main ne le couvre**, on cherche d'abord sur les domaines de
> la liste blanche. Si la recherche rend quelque chose, on écrit les
> fiches avec leur tampon de provenance. Si elle ne rend rien, on écrit
> le trou dans `sources/INVENTAIRE.md` (« sujet X : à sourcer, rien de
> fiable trouvé le AAAA-MM-JJ »), on propose où chercher, **et on peut
> tout de même écrire une fiche conceptuelle avouée « sans source
> retrouvée »**, sans aucun chiffre ni date, qui sera vérifiée en
> priorité (`decisions/0021`, amendement du 02/09/2026).

**Écrire un trou est un livrable, pas un échec.** Un domaine qui rend
30 cartes solides et 12 trous nommés est en bon état ; un domaine qui
rend 42 cartes dont 12 inventées est cassé, et on ne le saura que le
jour où le joueur redira une bêtise à voix haute.

Corollaire pour l'agent : quand il se surprend à écrire une carte de
mémoire, il s'arrête et ouvre l'inventaire.

---

## Étape 0 — L'installation

**Objectif.** Que la machine du joueur puisse faire tourner un agent
avec accès au disque et à git. Faite une fois, ensemble, avant tout
travail de contenu.

**Ce qu'il faut, nommé :**

| Élément | Pourquoi |
|---|---|
| un compte GitHub | héberger le dépôt source privé du joueur |
| `git` installé | versionner l'inventaire, la config et les fiches |
| **Claude Code**, ou Claude Desktop avec accès fichiers | une session web n'a **ni accès disque ni git** : elle ne peut pas faire ce parcours |
| un abonnement ou une clé API | le traitement tourne chez le joueur, à son coût |
| Node et Python 3 | valideur et outils du gabarit |
| une copie de ce gabarit | `cp -R` puis renommage (voir `README.md`) |

**Garde-fous.** Ne pas commencer l'étape 1 « en attendant » que
l'installation soit finie : un inventaire fait dans une session sans
disque est à refaire.

**Le repli honnête, écrit d'avance.** Si l'installation coince, le
joueur **dépose ses fichiers et la fabrique tourne sur la machine de
celui qui porte l'infra**. Le dépôt source du joueur est l'état
**cible**, pas le prérequis de sa première séance. Ce repli est borné
à la v1 et se dit au joueur, il ne se subit pas en silence.

**Porte.** L'agent lit et écrit un fichier de test dans le dossier du
joueur, et `git status` répond. Sinon : repli.

**[À COMPLÉTER PAR M10]** — la liste des commandes exactes,
système par système, et les trois pannes réellement rencontrées le
soir de la première installation. Tout ce qui est écrit ici est
prévisionnel tant que personne ne l'a fait.

---

## Étape 1 — Où sont tes documents ?

**Objectif.** Savoir ce que le joueur a déjà, sans rien déplacer.

**Livrable.** La section « Le tas » de `sources/INVENTAIRE.md` : un
tableau des dossiers et fichiers repérés, avec leur volume et leur
nature apparente.

**Garde-fous.**
- On **n'ouvre pas** tout, on **ne déplace rien**, on **ne renomme
  rien** à cette étape. Un tri fait avant de savoir ce qu'on trie est
  un tri à refaire.
- Les fichiers lourds ne rentrent pas dans git : `sources/` est ignoré
  par git, seul l'inventaire est versionné. Vérifier que c'est bien le
  cas **avant** de déposer quoi que ce soit.
- Demander explicitement s'il existe un tas ailleurs (drive, clé,
  boîte mail, un carnet type NotebookLM). Le joueur oublie toujours un
  gisement.

**Le pivot** (`decisions/0026`, 03/09/2026) : chaque document retenu
devient un Markdown par page (`sources/<empreinte>.md`, ancres `[p. n]`,
titres, tableaux, figures décrites) avec ses pages à figures rendues en
image à côté ; c'est ce pivot que l'agent lit et que les chapitres
citent, jamais le PDF. Outils : `pdftotext`, `pdftohtml -xml`,
`pdftoppm`, `pdfimages` ; la vision du modèle pour les figures ; l'OCR
seulement pour un PDF sans couche texte. Le tout tourne sur l'abonnement
du joueur, aucune clé d'API.

**Porte.** Le joueur reconnaît son propre tas dans l'inventaire.

---

## Étape 2 — Quel métier, quel objectif ?

**Objectif.** Fixer le domaine exact, la **première** région et
l'échéance réelle.

**Livrable.** `academie.json` renseigné : `metier`, `profil_defaut`,
et les régions avec leur `ordre`.

**Garde-fous.**
- **Une seule région pour commencer.** La v1 d'un domaine est bornée à
  environ **30 cartes** : une boucle complète et jouable vaut mieux que
  300 cartes qu'on ne finit pas.
- Une échéance datée (un concours, un examen, une prise de poste)
  change l'ordre des régions. La demander, ne pas la deviner.
- Les blocs `quotas`, `fsrs`, `progression` et `quiz` sont **les
  règles du jeu, pas du métier** : on n'y touche pas à cette étape.
- Une région `culture` avec `"arbre": false` est prévue dans la
  coquille : c'est la région sans prérequis, celle où l'on range ce
  qui n'entre dans aucune progression. La garder ou la retirer, mais
  décider.

**Le cadre est écrit par l'agent** (`decisions/0022`, 02/09/2026) : à
partir de ce que le joueur dit de son métier et de son objectif, l'agent
propose le programme (domaines, branches, chapitres, niveaux, socle)
calibré sur les ancres publiques du métier (le diplôme d'entrée, le
référentiel de compétences, la formation continue), et le joueur le
relit et le corrige. Les documents du joueur viennent ensuite
corroborer, compléter ou contredire chapitre par chapitre ; ils ne
dessinent pas la carte.

**Porte.** Le joueur sait dire en une phrase ce qu'il saura faire
quand la première région sera pleine.

---

## Étape 3 — Le test de santé des sources

**Objectif.** Séparer ce qui peut fonder une carte de ce qui ne le
peut pas, **source par source**, et dire ce qui manque.

**Livrable.** `sources/INVENTAIRE.md` complet : le tableau de tri
rempli et la section « Les trous nommés » ouverte.

**Le classement, en quatre lots.**

| Lot | Ce que c'est | Verdict par défaut |
|---|---|---|
| **fiable** | référentiel public, texte officiel, institution, doctrine signée | garder |
| **commercial** | éditeur, prestataire, courtier : vend quelque chose sur la page | virer, sauf motif écrit |
| **douteux** | contenu manifestement généré, blog anonyme, autre pays ou autre droit, page trop ancienne | virer |
| **doublon** | déjà présent sous un autre nom | virer, gain sec |

**Garde-fous.**
- Le classement automatique (sur le nom de domaine, sur le type de
  fichier) est un **premier tri mécanique**, pas un verdict. Le verdict
  se pose **source par source** et se conteste. Une part du lot
  « commercial » est en réalité de la doctrine sérieuse mal étiquetée.
- Un piège vérifié : **même vocabulaire, autre droit** (ou autre pays,
  autre référentiel, autre édition). C'est le cas où la réponse paraît
  juste et est fausse. Il se traque à la main.
- Chaque ligne porte sa **licence ou son droit de dériver** et sa
  **date de vérification**. Sans ces deux colonnes, l'inventaire ne
  sert à rien six mois plus tard.
- Dire **ce qui manque et où le télécharger légalement** fait partie
  de l'étape : les référentiels publics du métier sont la voie sûre.

**Modèle du geste.** Voir
[`../NOTEBOOKLM-A-RETIRER.md`](../NOTEBOOKLM-A-RETIRER.md) : un
compte par lot, puis la liste nommée, puis ce qu'on garde et
pourquoi. Rien n'est supprimé par l'agent — la suppression est un
geste humain.

**Porte.** Chaque source du tas a un verdict daté, et la liste des
trous existe (même vide, la section est écrite).

---

## Étape 4 — La génération

**Objectif.** Produire les cartes au contrat carte-v1, région par
région.

**Livrable.** `banque/<region>/<branche>.json` : un tableau de cartes,
toutes en `"statut": "brouillon"`.

**Garde-fous.**
- **Paraphrase plus lien, jamais de recopie** (refus 4).
- **La règle du trou nommé s'applique ici en premier** : le plan de
  région dit ce qu'il faudrait couvrir, les sources disent ce qu'on
  peut couvrir. L'écart s'écrit dans l'inventaire, il ne se comble pas
  à l'imagination.
- **Une carte générée naît `brouillon`**, sans exception. Le générateur
  ne sert que du `valide` ; c'est son défaut, et un test le verrouille.
- La couche `partage` se décide **à la source**, pas à la relecture :
  source publique → `banque` ; support interne paraphrasé → `interne`
  (jamais de distribution externe) ; pièce réelle → `perso` (le
  propriétaire du profil seul).
- Un QCM sans distracteurs expliqués n'apprend rien : chaque choix
  faux porte son `pourquoi_faux`, et il y a **exactement une** bonne
  réponse.
- **Un chiffre qui bouge porte sa date de mort** (`peremption`) :
  prix, plafond, seuil indexé, barème. Passé la date, la carte sort de
  la rotation toute seule au lieu d'enseigner du faux en silence.
- Aucune donnée personnelle réelle, aucune image sans licence
  (refus 2 et 3).

**Porte.** Le nombre de cartes est cohérent avec le nombre de sources
gardées. Beaucoup de cartes pour peu de sources est un signal
d'invention, pas de productivité : on rouvre.

**[À COMPLÉTER PAR M10]** — le découpage en branches qui marche
vraiment (combien de cartes par branche, quel grain), les tournures de
question qui donnent de bonnes cartes, et les prompts de génération
mesurés le soir de la fabrication. Écrire ça d'avance serait de la
décoration.

---

## Étape 5 — La double passe par agent frais

**Objectif.** Qu'un agent **qui n'a pas écrit les cartes** remonte aux
sources et vérifie, carte par carte.

**Livrable.** Les cartes vérifiées passent en `"statut": "valide"` ;
les autres restent `brouillon` ou passent `signale`, avec le motif.

**Garde-fous.**
- **Obligatoire, quel que soit le domaine.** Ce n'est pas une option
  de confort : c'est la seule étape qui attrape une carte plausible et
  fausse.
- **Agent frais** veut dire : session neuve, sans le fil de la
  génération. Un agent qui relit son propre travail confirme son
  propre travail.
- La passe **remonte à la source**, elle ne juge pas la vraisemblance.
  Une carte dont la source ne dit pas ce que la carte affirme est
  fausse, même si elle est juste par ailleurs.
- **Le joueur échantillonne, il ne valide pas seul.** Il tire quelques
  cartes au hasard et vérifie qu'il retrouve ce qu'il connaît. Son
  accord ne remplace pas la double passe.
- La règle du trou nommé s'applique aussi ici : une carte sans source
  retrouvable ne se répare pas en cherchant une source qui lui
  ressemble. Elle sort, et le sujet devient un trou.

**Porte.** Aucune carte ne reste en `brouillon` sans motif écrit.

**[À COMPLÉTER PAR M10]** — le taux de rejet observé à la première
fabrication (c'est le chiffre qui dira si l'étape 4 est bien réglée),
et le coût mesuré de la passe.

---

## Étape 6 — Le valideur mécanique

**Objectif.** Que la machine refuse ce qui ne respecte pas le contrat,
sans discussion.

**Livrable.** Une sortie verte.

```
ACADEMIE_RACINE=<dossier du joueur> python3 <chemin>/valide_banque.py
```

**Ce qu'il refuse, sans dérogation :** une carte sans source ou sans
date de vérification ; un fait nominatif dans une couche partagée ; un
QCM sans distracteurs expliqués ; une image sans licence ; un id
dupliqué ; un prérequis qui pointe dans le vide ; une carte périmée
encore marquée `valide`.

**Garde-fous.**
- **Le valideur fait foi.** Quand il contredit le contrat écrit, c'est
  le contrat qui se corrige, pas le valideur.
- On ne **jamais** affaiblit le valideur pour faire passer une carte.
  Si une carte légitime est refusée, on corrige la carte, ou on ouvre
  une discussion sur la règle — hors session de fabrication.
- Un id ne se renumérote pas : il est la clé de tout l'historique de
  révision. Une carte fausse se corrige ou se retire.

**Porte.** Sortie verte. C'est tout.

---

## Étape 7 — « Je publie ma livraison »

**Objectif.** Envoyer au serveur de jeu les seules fiches validées.

**Livrable.** Une livraison acceptée, ou un refus tracé.

**Garde-fous.**
- **Geste humain, jamais un hook de commit.** On publie parce qu'on a
  décidé de publier.
- Le filtre se fait **par couche**, mécaniquement : une distribution
  externe ne sert que `banque`. Il n'y a pas de relecture humaine à
  refaire à chaque publication, et c'est ce qui la rend sûre.
- **Les sources ne partent jamais.** Ni les PDF, ni les cours, ni les
  annales, ni les notes de contexte. Si un fichier de `sources/` se
  retrouve dans la livraison, la livraison est cassée.
- Côté serveur, la réception **re-passe le valideur** et met en
  quarantaine avant mise en jeu. Deux barrières, deux dépôts : un
  refus à la réception n'est pas un bug, c'est le dispositif qui
  fonctionne.

**Porte.** La livraison est visible côté serveur, ou le refus est lu
et compris.

**[À COMPLÉTER PAR M10]** — le geste concret côté joueur
(téléversement depuis le produit), le jeton par joueur, et le message
de refus tel qu'il est réellement affiché. Rien de tout cela n'existe
au 29/08/2026.

---

## Ce que la première fabrication doit mesurer

Le guide se termine sur une mesure, pas sur une promesse.

- Le **coût réel** de la fabrication (tokens et euros), séparé du coût
  d'usage. La fabrication est ponctuelle et se chiffre en dizaines
  d'euros ; l'usage est proche de zéro.
- Le **temps** passé par étape, et là où ça a coincé.
- Le **taux de rejet** de la double passe.

Un GO/NO-GO écrit suit la mesure. **Aucun prix ne s'annonce à un
joueur avant qu'elle existe.**

**[À COMPLÉTER PAR M10]** — le déroulé de la soirée artisanale est le
brouillon du vrai guide. Ce fichier sera réécrit après, avec les mots
qui ont marché.

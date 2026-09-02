# CADRAGE PRODUIT — L'Académie hors du repo : les options, et les questions à trancher avec Arthur

Écrit le 29/08/2026 sur demande de JB (« est-ce qu'on prépare pas un
autre repo ? quel lien entre les deux projets ? pose-moi 30 questions,
je répondrai avec Arthur, et tu écriras la technique sur cette base »).
**Rien ne se code depuis ce fichier** : c'est le questionnaire d'avant
la technique. JB et Arthur répondent inline (sous chaque question, ou
en vrac par numéros), puis un agent écrit la spec technique depuis les
réponses et la fait relire par pré-mortem avant la première ligne.

**RÉPONDU le 29/08/2026 au soir** : la séance JB × Arthur a eu lieu
(transcription fournie par JB), complétée d'un brief écrit de JB qui
tranche l'architecture. Les réponses et les arbitrages rendus sont en
**Partie 4** ci-dessous, la spec technique qui en découle est
[`SPEC-PRODUIT.md`](SPEC-PRODUIT.md). Les Parties 1 à 3 restent pour
mémoire du raisonnement.

Note : le « grand md des génies » (réflexes de cadrage) n'est pas dans
ce clone — s'il vit en `coulisses/`, le rapatrier ou le citer au moment
des réponses. En attendant, ce document en reprend l'esprit : pré-mortem
avant plan, squelette qui marche avant features, boucle de jeu avant
contenu, critères de mort écrits d'avance.

---

## PARTIE 1 — Les options, expliquées avant les questions

### A. Le lien entre les deux dépôts (la question « un autre repo ? »)

| Option | Ce que c'est | Pour | Contre |
|---|---|---|---|
| **A1. Statu quo monorepo** | L'Académie reste dans wiki-copro, servie depuis le clone VPS | Zéro travail, tout le tooling existant | Impossible d'accueillir quiconque : le clone porte `outputs/` et `coulisses/` ; basicauth partagé ; c'est le préalable absolu de M9 qui l'interdit |
| **A2. Extraction totale, zéro lien** | Nouveau repo `academie` (moteur + front + contrat carte-v1), plus AUCUN échange avec wiki-copro ; JB y saisit son contenu comme n'importe quel joueur | Frontière parfaite, sécurité maximale, produit vraiment générique | JB perd sa chaîne de production de cartes (les agents du repo, le wiki, les skills) ; double saisie ; le meilleur atout du produit (le contenu copro déjà usiné) est débranché |
| **A3. Produit séparé + wiki-copro FOURNISSEUR** (recommandé par la roadmap actuelle, M9) | Nouveau repo pour le produit ; wiki-copro garde la fabrication du domaine « copropriété » de JB et POUSSE la banque validée (couche partagée seulement, scanner anti-fuite au passage) vers le produit, comme un éditeur livre un manuel | JB garde son usine à cartes ; le produit ne voit jamais une donnée copro ; le pipeline de push est petit (un fichier JSON versionné) | Deux dépôts à maintenir ; le contrat carte-v1 doit être versionné des deux côtés ; le flux est à sens unique (une correction faite côté produit doit remonter à la main) |
| **A4. Produit séparé + « chaque joueur a son repo source »** | Comme A3, mais généralisé : le pattern « un repo privé qui fabrique, un produit qui joue » devient LE modèle d'onboarding — Arthur a son propre repo/dossier source, l'IA y fabrique son domaine, le produit le consomme | Symétrique et honnête (JB n'est pas un joueur spécial) ; prépare M10 proprement | Le plus ambitieux : il faut outiller la fabrication pour quelqu'un qui n'a ni Claude Code ni la culture du repo — probablement la v2 de A3, pas la v1 |

**Ce que ça implique dans tous les cas sauf A1** : le front doit sortir
du châssis React de l'ERP (il y est tissé — vue, composants, barre,
palette), l'hébergement a besoin d'une vraie auth (le basicauth partagé
ne fait pas des comptes), et le nouveau repo a son propre CI/tooling.
C'est le coût d'entrée, quel que soit le choix.

### B. Quel contenu passe la frontière (le « aucun ? un petit ? tout ? »)

| Option | Contenu transféré au produit | Verdict rapide |
|---|---|---|
| **B1. Rien** | Le produit démarre vide, chaque joueur fabrique tout | Cohérent avec A2, mais l'Académie de JB régresse |
| **B2. La banque anonyme seule** | Les cartes `partage: banque` (déjà zéro fait copro par construction du valideur) | Le minimum viable — c'est ce que M9 prévoit |
| **B3. Banque + ateliers publics** | B2 + fiches de méthode + ateliers sur textes PUBLICS (arrêts, décrets) | Le bon niveau probable : les ateliers publics sont le différenciateur pédagogique et sont juridiquement les plus sûrs |
| **B4. Tout sauf l'interne** | B3 + cas d'école dérivés du terrain (voir C) | À n'ouvrir que si C est tranché proprement |

Ce qui ne passe JAMAIS, quelle que soit l'option : la couche
`partage: interne` (supports employeur), les ateliers sur pièces
réelles, `contexte.jsonl`, tout ce qui porte un nom de copro.

### C. Les cas IRL de JB (« si je dois reprendre des cas de moi ? »)

Trois régimes possibles, cumulables :

1. **Couche perso** (existe déjà) : le cas réel reste chez JB
   (`etat/<profil>/`), jamais distribué. Zéro risque, zéro partage.
2. **Cas d'école réécrit** : un vrai dossier devient un exercice
   FICTIF — montants arrondis, copro renommée « Résidence des
   Lilas », détails identifiants gommés, mais le mécanisme (le piège
   du devis, l'erreur d'imputation) conservé. C'est la tradition des
   cas de fac de droit : le réel anonymisé est le meilleur matériau
   pédagogique. Circuit : réécriture par agent → scanner anti-fuite →
   validation JB carte par carte → `partage: banque`.
3. **Atelier sur pièce publique équivalente** : plutôt que d'anonymiser
   la pièce de JB, chercher la pièce PUBLIQUE qui enseigne la même
   chose (une décision Judilibre sur le même contentieux). Plus de
   travail de sourcing, zéro risque juridique.

La question à trancher n'est pas « oui ou non » mais **le curseur** :
combien de cas d'école par mois, qui fait la réécriture, et est-ce que
le jeu vaut la chandelle face au régime 3.

### D. Accueillir d'autres sujets (le domaine d'Arthur, et au-delà)

L'architecture le prévoit déjà (BLUEPRINT §11 : le moteur ne sait rien
de la copropriété, un domaine = une banque + une config). Les vraies
questions sont ailleurs : qui FABRIQUE le domaine d'Arthur (M10 dit
« l'IA, sans JB », mais la v1 peut être « JB et Arthur ensemble, un
soir, pour apprendre ce que coûte un domaine »), qui le VALIDE (la
double passe agent frais reste obligatoire — un débutant ne peut pas
valider sa propre matière), et sur quelles SOURCES (le domaine
infirmier a ses référentiels publics : HAS, Vidal ? à inventorier
comme on a inventorié AQC/ANIL/Légifrance).

---

## PARTIE 2 — Le questionnaire (répondre avec Arthur, inline ou par numéros)

Répondre court, franchement, « je ne sais pas » est une réponse
valable (elle devient un arbitrage à défaut ou une expérience à
mener). Les questions marquées **[ARTHUR]** sont pour lui d'abord.

### I. Vision et ambition (ce qu'on construit vraiment)

1. Dans un an, l'Académie est un succès si… quoi, concrètement ?
   (JB sait nommer une souche en toiture ? Arthur a tenu 100 séances ?
   5 amis jouent ? le produit rapporte un euro ?) Une phrase chacun.
2. C'est quoi le produit, au fond : (a) TON école du matin, que des
   amis squattent ; (b) un produit d'amis, à 3-6 joueurs, sans
   ambition au-delà ; (c) un vrai produit qu'un inconnu pourrait
   utiliser un jour ? Le choix change TOUT (auth, RGPD, support,
   design).
3. Y a-t-il un horizon commercial, même lointain, même flou ?
   (Réponse « non jamais » = on simplifie beaucoup ; « peut-être » =
   licences des sources et CGU à penser dès maintenant.)
4. Combien d'heures par mois JB accepte-t-il de mettre dans le
   PRODUIT (pas dans son propre apprentissage) une fois lancé ?
   C'est le budget de maintenance réel, tout le reste doit tenir
   dedans.
5. Critère de mort, écrit d'avance (réflexe pré-mortem) : à quelle
   condition on ARRÊTE le produit multi-joueurs et on replie sur
   l'Académie perso ? (ex. : « si Arthur décroche deux fois », « si
   la maintenance dépasse X h/mois »)

### II. Arthur, le joueur pilote

6. **[ARTHUR]** Ton domaine exact ? (« infirmier » est trop large :
   quelles branches, quel niveau de départ, quel manque le plus
   coûteux dans ton quotidien — l'équivalent de la souche en toiture
   de JB ?)
7. **[ARTHUR]** Tes sources : quels référentiels publics font foi
   dans ton métier (l'équivalent de Légifrance/AQC) ? En as-tu déjà
   une bibliothèque (NotebookLM, PDF, cours) ? Qui a le droit d'en
   dériver des cartes ?
8. **[ARTHUR]** Ton rituel réaliste : quel créneau, combien de
   minutes, combien de jours par semaine, sur quel appareil
   (téléphone ? ordi ?) ? Sois pessimiste, pas motivé.
9. **[ARTHUR]** As-tu déjà utilisé Anki, Duolingo, ou équivalent ?
   Tenu combien de temps ? Pourquoi arrêté ? (La réponse dit ce qui
   te fera décrocher ici.)
10. **[ARTHUR]** Une clé API payante à ton nom (~qq €/mois selon
    usage), tu es prêt à la créer et la payer ? Sinon, quel serait
    ton maximum acceptable ?
11. **[ARTHUR]** Qu'est-ce que tu acceptes que JB voie de ton
    parcours, et inversement ? (Tout ? Le skill tree sans les échecs ?
    Les heures de jeu ?) — la « visibilité totale » arbitrée le 29/08
    est-elle vraiment ce que TU veux ?
12. **[ARTHUR]** Le défi (un mini-duel sur une notion, chacun dans son
    domaine ou sur un tronc commun de culture générale) : envie
    réelle, ou politesse ? Serais-tu vexé/démotivé de perdre ?
13. À deux : combien d'autres joueurs dans les 12 mois, nommables
    aujourd'hui ? (Des noms, pas « on verra » — c'est le vrai test de
    l'ambition de la question 2.)

### III. La frontière entre les deux projets

14. Option A2, A3 ou A4 (Partie 1) ? Et si A3 : le push de la banque
    est-il automatique (chaque commit wiki-copro déclenche) ou un
    geste volontaire de JB (« je publie la livraison de la semaine ») ?
15. Le nouveau repo : privé GitHub sur ton compte perso ? Un compte
    d'organisation dédié (plus propre si d'autres contribuent un
    jour) ? Qui d'autre que toi a les droits d'écriture ?
16. Quand un bug du moteur FSRS est découvert côté produit, qui le
    corrige et sous quel délai « acceptable » ? (Toi via Claude Code ?
    N'importe quel joueur peut ouvrir une issue ?)
17. Le jour où tu changes d'employeur : qu'est-ce qui doit survivre
    tel quel ? (Réponse attendue : tout le produit + ta banque ; à
    vérifier que rien dans la banque « copropriété » ne dérive de
    supports Sergic `interne`.)
18. L'accès depuis ton front ERP : un simple lien sortant suffit-il,
    ou veux-tu un aperçu (streak, cartes dues) affiché DANS l'ERP ?
    (L'aperçu recrée un couplage qu'on vient de couper — à décider en
    conscience.)

### IV. Contenu : les cas IRL et le reste

19. Le curseur de la Partie 1-C : régime 1 (perso seulement), 2 (cas
    d'école réécrits), 3 (équivalents publics), ou un mix ? Si le 2 :
    combien par mois, et acceptes-tu que CHAQUE cas d'école passe par
    ta validation nominale (c'est incompressible) ?
20. Y a-t-il des dossiers dont tu sais DÉJÀ qu'ils feraient des cas
    d'école en or (un contentieux fini, un devis piégeux, une AG qui a
    mal tourné) ? Liste-en 3-5 de tête : ils calibreront le format.
21. La branche « Culture » (le texte du bac) : partagée entre tous les
    joueurs quel que soit leur métier (tronc commun), ou par domaine ?
    (Un tronc commun est le terrain naturel des défis JB-Arthur.)
22. Les 59 cartes actuelles : elles restent le noyau du domaine copro
    du produit, ou on repart propre au moment de l'extraction ?

### V. Pédagogie : exercices, exemples, réflexes

23. Classer ces modes du plus envie au moins envie (chacun son
    classement) : Flash / QCM / photo-diagnostic / relier / datation /
    réponse libre corrigée / jeu de rôle / lecture de plan / atelier
    de lecture. Le podium de chacun oriente la v1 de son domaine.
24. **[ARTHUR]** Quels seraient les équivalents dans ton domaine ?
    (photo-diagnostic → reconnaître une plaie/un tracé ECG ? lecture
    de plan → lire une prescription ? jeu de rôle → l'annonce à un
    patient, la famille difficile ?) Donne 3 exemples concrets
    d'exercices dont tu rêves.
25. La correction par LLM (réponse libre) : indispensable dès la v1 de
    chaque domaine, ou luxe qui attend ? (Elle coûte par carte et par
    joueur — question 10.)
26. Le réflexe « boucle avant contenu » (game design) : accepte-t-on
    que la v1 du domaine d'Arthur n'ait que 30 cartes mais une boucle
    quotidienne complète (tirage → révisions → clôture), plutôt que
    300 cartes sans rituel ? (Réponse recommandée : oui.)
27. L'hypercorrection (le cadrage scientifique l'appuie) : après une
    erreur, préférez-vous la correction sèche immédiate, ou une
    micro-explication de 3 lignes + la source ? Et une erreur répétée
    3 fois doit-elle déclencher quelque chose de spécial (mini-leçon,
    carte préalable) ?
28. Que doit-il se passer un matin SANS envie : le produit propose-t-il
    un « mode 3 minutes » explicite (5 révisions et sortie honorable),
    et c'est tout ?

### VI. Game design : XP, arbres, motivation

29. L'XP : qu'est-ce qui en donne, et pour quoi faire ? (débloquer des
    branches ? cosmétique ? rien d'autre qu'un chiffre qui monte ?)
    Attention au réflexe des génies du genre : une récompense qui ne
    change rien au jeu s'use en deux semaines ; celle qui ouvre du
    contenu dure.
30. Les trois boucles (réflexe game design) : la boucle COURTE
    (une carte, 20 s), on l'a ; la boucle MOYENNE (la séance, 15 min),
    on l'a ; la boucle LONGUE (la semaine, le mois : qu'est-ce que
    j'attends avec impatience ?) — qu'est-ce que c'est chez vous ?
    (le bilan mensuel ? une branche qui s'ouvre ? un boss de fin de
    niveau — un « examen » de branche ?)
31. Un « examen de branche » (10 cartes mélangées, à froid, score
    solennel) pour valider un niveau et ouvrir le suivant : envie, ou
    trop scolaire ?
32. La première séance d'un nouveau joueur (onboarding) : que doit-il
    se passer dans les 5 premières minutes pour qu'Arthur revienne le
    lendemain ? (jouer immédiatement 5 cartes faciles de son domaine ?
    voir son arbre vide mais prometteur ? paramétrer son quota ?)
33. Les streaks : le compteur cumulé doux est arbitré, mais faut-il un
    affichage de régularité (calendrier de pastilles façon GitHub) ou
    même ça culpabilise ?
34. Le tirage « machine à sous » du menu : sonore et visuel assumé
    (3 s d'animation), ou sobre (le menu apparaît, point) ?
35. Avatar / niveau / titre (« Compagnon pathologie niveau 3 ») :
    envie de cosmétique léger, ou zéro chrome ?

### VII. Technique (les choix qui engagent)

36. Le front extrait : (a) on re-fait léger (HTML/JS vanilla généré,
    comme l'ERP d'origine) ; (b) on garde React mais dans un build
    propre au produit ; (c) autre envie ? Le (b) réutilise les
    composants Académie existants, le (a) simplifie la maintenance
    décennale.
37. Hébergement : le VPS OVH actuel avec un vhost + domaine dédié
    (~12 €/an le domaine), ou un hébergeur séparé pour étanchéifier
    complètement (le VPS actuel porte le clone wiki-copro) ?
    Réponse structurante pour la sécurité.
38. L'auth : des comptes classiques email + mot de passe (il faut une
    base et du reset), des magic links par mail, ou des passkeys ?
    Pour 2-6 joueurs connus, le magic link est le meilleur rapport
    simplicité/sécurité — avis ?
39. Le stockage serveur : rester sur la philosophie fichiers
    (`revues.jsonl` par profil, git) ou passer à une vraie base
    (SQLite) maintenant qu'il y a plusieurs écrivains ? (SQLite
    recommandé dès 2 joueurs : l'append-only par fichier ne survit pas
    bien à la concurrence + suppression de compte RGPD.)
40. Hors ligne / PWA : indispensable dès la v1 du produit séparé
    (Arthur joue dans les transports ?) ou M8 reste à sa place ?
41. La clé API d'un joueur : stockée chiffrée côté serveur (le serveur
    appelle l'IA pour lui), ou jamais côté serveur (les appels IA
    partent du navigateur du joueur) ? La seconde est plus saine mais
    contraint les features (pas de génération nocturne pour lui).

### VIII. IA : rôle et coûts

42. Pour la GÉNÉRATION d'un domaine (M10) : v1 artisanale assumée
    (JB + Arthur + une session Claude, un soir, pour le domaine
    d'Arthur — on apprend le vrai coût) avant toute automatisation ?
    (Recommandé : oui — « do things that don't scale ».)
43. Quel budget IA mensuel chacun juge-t-il « évidemment ok » /
    « limite » / « non » ? (donne trois chiffres chacun ; ça calibre
    le mix de modes par défaut)
44. Si un joueur n'a pas de clé : le produit doit-il rester 100 %
    jouable en dégradé (tous les modes à correction exacte, pas de
    réponse libre ni de génération) ? (Recommandé : oui, c'est le mode
    de survie du produit.)

### IX. Social et RGPD

45. La suppression de compte : un bouton qui efface tout (état,
    historique, clé) sous 48 h — on est d'accord que c'est
    non négociable avant le premier compte tiers ?
46. **[ARTHUR]** Es-tu d'accord pour figurer au registre RGPD de JB
    comme personne concernée (données d'apprentissage, hébergées sur
    son infra) ? — c'est une formalité mais elle doit être réelle.
47. Les invitations : sur lien privé envoyé à la main par un joueur
    existant (pas de page d'inscription publique) — suffisant pour
    les 12 prochains mois ?
48. Un joueur peut-il avoir plusieurs domaines à la fois (JB : copro +
    culture ; Arthur : infirmier + autre chose) et le mix de séance
    les entrelace-t-il ?

### X. Qualité et exploitation

49. La règle « aucune carte ne devient jouable sans double passe par
    agent frais remontant aux sources » s'applique à TOUS les
    domaines, y compris celui d'Arthur (sur sa clé) : on la grave dans
    le produit (le statut `brouillon` est bloquant côté moteur) ?
50. Qui produit le lot hebdo de cartes d'Arthur les 3 premiers mois :
    lui seul avec l'IA, ou une passe JB « qualité du format » (pas du
    fond, qu'il ne connaît pas) par-dessus ?
51. Le bouton « carte fausse » : la carte sort de rotation
    immédiatement chez TOUS les joueurs du domaine, ou seulement chez
    celui qui a signalé, en attendant l'arbitrage ?
52. Dernier réflexe pré-mortem, chacun répond séparément puis on
    compare : « Nous sommes en août 2027, le produit est mort. Raconte
    en 5 lignes ce qui l'a tué. » — les deux récits écrivent la vraie
    liste des risques.

---

## PARTIE 3 — Ce qui se passe après les réponses

1. Les réponses s'écrivent ICI, sous les questions (ou en vrac datées
   en fin de fichier), avec Arthur, sans se censurer.
2. Un agent en dérive la **spec technique** (architecture du nouveau
   repo, auth, stockage, pipeline de banque, plan de chantiers qui
   remplace/raffine M9-M11) — un document, pas du code.
3. La spec passe le **pré-mortem par agent frais** (protocole
   habituel) avant tout GO.
4. Seulement ensuite : la première ligne de code, en commençant par le
   squelette qui marche (un joueur, un domaine, une séance de bout en
   bout sur la nouvelle adresse) avant toute feature.

Rappel de la roadmap, inchangé : rien de M9+ ne se construit avant que
le rituel de JB tienne (gate des ~30 séances). Ce questionnaire, lui,
peut se remplir dès ce week-end : penser n'est pas construire.

---

## PARTIE 4 — Les réponses du 29/08/2026 (séance JB × Arthur) et les arbitrages rendus

Sources : la transcription de la séance du 29/08 (fournie par JB) + le
brief écrit de JB le même jour. Marquage : **[JB]** / **[ARTHUR]** =
réponse en séance ; **[BRIEF]** = tranché par écrit par JB après la
séance ; **[ARBITRÉ]** = décidé par Claude sur délégation de JB
(« arbitre toutes les questions, décide de tout le reste »), donc
révocable d'un mot. L'attribution des voix dans la transcription est
parfois incertaine : les réponses ci-dessous ne retiennent que ce qui
est net.

### I. Vision et ambition

1. **Succès dans un an** — [JB] le produit vit tant qu'« il y a
   toujours un truc derrière à apprendre » : du contenu et des
   objectifs qui ne s'épuisent pas, et devenir « un pro qui a de très
   bonnes connaissances techniques ». [ARTHUR] avoir conquis sa
   première région : être prêt au concours d'entrée en IFSI.
2. **Nature du produit** — [JB] « une vraie appli, conçue comme une
   vraie appli, mais que pour nous deux — une vraie appli quand même,
   qui scale. » Donc : produit d'amis (b), construit aux standards
   d'un vrai produit (c), sans jamais viser l'inconnu.
3. **Horizon commercial : NON**, catégorique ([JB] en séance). Seul
   usage élargi imaginé, lointain et interne : la formation d'équipes
   si JB a un jour son agence (« le premier quart d'heure vous êtes
   payés »). Conséquence : pas de CGU commerciales, pas de licence de
   vente à penser ; le droit des sources reste, lui, entier.
4. **Heures/mois de JB dans le produit** — [JB] « infini, ça m'éclate
   de construire ça ». [ARBITRÉ] le garde-fou de la roadmap reste
   malgré l'enthousiasme : si le temps manque un jour, c'est M9-M11
   qu'on gèle, jamais le rituel.
5. **Critère de mort du multijoueur** — [JB] « si Arthur s'en
   branle ». [ARBITRÉ] rendu mesurable : Arthur sans aucune séance
   pendant 4 semaines consécutives (hors indisponibilité annoncée),
   ou sur sa demande → la couche multi se gèle, l'Académie perso de
   JB continue telle quelle. Réversible si Arthur revient.

### II. Arthur, le joueur pilote

6. **Domaine exact** — [ARTHUR] la **préparation du concours d'entrée
   en IFSI par la voie FPC** (formation professionnelle continue —
   pas Parcoursup : il n'est pas encore admis). C'est sa première
   région ; les suivantes sont déjà en vue (études IFSI, puis cadre de
   santé), exactement le modèle « régions à conquérir » du §VI.
7. **Sources** — [ARTHUR] une bibliothèque en vrac (« des milliers de
   PDF téléchargés », ex. Santé publique France), un site de cours en
   ligne repéré en séance (nom incertain dans la transcription), et la
   piste de récupérer les cours PDF de l'année 1 d'IFSI via une
   connaissance. Rien de trié : **le tri IA des sources (le « test de
   santé », façon `NOTEBOOKLM-A-RETIRER.md`) est la première étape de
   son onboarding**, dite en séance par JB lui-même. Référentiels
   publics à inventorier : annales du concours FPC, référentiels de
   formation IFSI, HAS, Santé publique France.
8. **Rituel réaliste** — pessimiste : ~1 h/semaine ; motivé : 3-4
   jours/semaine × 15-20 min (attribution des deux chiffres incertaine
   entre les deux voix ; le produit se calibre sur le pessimiste).
   Appareils : **ordi et téléphone** — le mobile n'est pas optionnel.
9. **Anki/Duolingo** — [ARTHUR] jamais utilisés. Aucun historique de
   décrochage à copier… ni de réflexe acquis : l'onboarding part de
   zéro.
10. **Clé API payante** — [ARTHUR] oui, **maximum 10 €/mois**. C'est
    le budget qui calibre le mix de modes de son domaine.
11. **Visibilité mutuelle** — [ARTHUR] « tout », avec enthousiasme.
    L'arbitrage 1 du 29/08 (visibilité totale entre amis) est confirmé
    par l'intéressé.
12. **Défis** — [ARTHUR] envie réelle (« ce serait énorme »), y
    compris le droit de choisir un thème dans le domaine de l'autre et
    les taquineries (« guerre de clan »). Pas de crainte de
    démotivation exprimée ; le garde-fou M11 (coupure si dégradation
    mesurée du rituel) reste en place tel quel.
13. **Joueurs à 12 mois** — [JB+ARTHUR] **2 pendant ~6 mois**, le
    temps que « le début un peu bugué » passe. Ensuite Agnès, « une
    fois que ça marchera très très bien » (jamais en bêta-testeuse),
    horizon ~4 joueurs. Pas de noms au-delà : l'ambition réelle est
    (b), le « qui scale » est une exigence de qualité, pas de volume.

### III. La frontière entre les deux projets

14. **Option A4, retenue** — [BRIEF] « mon double repo est le truc de
    base : Arthur pourrait aussi avoir son repo avec les choses de son
    métier + l'espace learning academy ; moi je porte le côté archi
    VPS. » Le pattern « un repo source privé qui fabrique, un produit
    qui joue » devient LE modèle d'onboarding. Push banque → produit :
    [ARBITRÉ] **geste volontaire** (« je publie ma livraison »),
    jamais un hook automatique — un humain regarde ce qui part.
15. [ARBITRÉ] Repo produit : privé, sur le compte GitHub perso de JB
    pour commencer ; migration vers un compte d'organisation seulement
    le jour où un tiers doit écrire dedans. Repo source d'Arthur : sur
    SON compte, privé, JB sans droit d'écriture par défaut.
16. [ARBITRÉ] Bug moteur découvert côté produit : JB corrige via
    Claude Code, meilleur effort sans délai promis ; un joueur signale
    par le canal amis (pas d'issues publiques — repo privé).
17. **Changement d'employeur** — tout survit (produit + banques). La
    garantie existe déjà par construction : la couche `interne` ne
    passe jamais la frontière, le valideur refuse un nom de copro en
    couche partagée.
18. [ARBITRÉ] Accès depuis l'ERP : **un simple lien sortant**, aucun
    aperçu embarqué (streak, cartes dues) — on ne recrée pas le
    couplage qu'on vient de couper.

### IV. Contenu : les cas IRL et le reste

19. [ARBITRÉ, non couvert en séance] Curseur des cas IRL : régimes
    1 + 3 par défaut (couche perso + équivalents publics) ; le régime
    2 (cas d'école réécrits) au compte-goutte, après M3, chaque cas
    passant par la validation nominale de JB.
20. **Reste dû par JB** : ses 3-5 dossiers « en or » de tête, pour
    calibrer le format des cas d'école. À répondre quand M3 s'ouvre.
21. **Branche Culture : tronc commun** partagé entre tous les joueurs
    quel que soit leur métier — confirmé en séance (« marrant…
    complètement »), terrain naturel des défis, jamais dominant
    (« mon but c'est pas non plus de faire ça »).
22. [ARBITRÉ] Les cartes actuelles (59+ au 29/08) restent le noyau du
    domaine copro du produit : elles passent déjà le valideur,
    l'extraction M9 les emporte telles quelles.

### V. Pédagogie

23-24. **Modes** — [ARTHUR] « un peu tout, ce qui est marrant », et
    ses équivalents nommés en séance : **tracé ECG à lire, tension à
    repérer sur un scope, photo de plaie → quel soin, cas patient
    déroulé**. Le photo-diagnostic et le cas guidé se transposent tels
    quels ; le contrat carte-v1 couvre déjà ces types.
25. [ARBITRÉ] Correction LLM (réponse libre) : pas dans la v1 du
    domaine d'Arthur — un concours se prépare d'abord aux QCM et aux
    annales, et ça tient son budget sous les 10 €. S'active quand son
    rituel tient, sur sa clé, jamais sur celle de JB.
26. **Boucle avant contenu : OUI** (recommandation acceptée). La v1
    du domaine d'Arthur peut n'avoir que 30 cartes si la boucle
    quotidienne est complète.
27. **Après une erreur** — [ARBITRÉ] micro-explication de 3 lignes +
    source (l'hypercorrection du cadrage scientifique) ; 3 échecs sur
    la même carte → mini-leçon ou carte préalable. **Et le CARNET
    D'ERREURS** [BRIEF : « pouvoir noter questions fausses et
    pourquoi »] : à chaque erreur, le joueur peut noter en une ligne
    pourquoi il s'est trompé ; la note vit dans son état
    (`etat/<profil>/erreurs.jsonl`), nourrit le bilan mensuel et la
    fabrication de cartes préalables. Spec : SPEC-PRODUIT §3.
28. [ARBITRÉ] Mode 3 minutes explicite : oui — 5 révisions et sortie
    honorable, déjà dans la parade « la séance dégrade bien ».

### VI. Game design

29-30. **Le modèle change : la CARTE-MONDE remplace l'arbre** —
    [JB+ARTHUR] pas un arbre de compétences qu'on finit, des
    **régions à conquérir** façon open world / Risk : chaque région se
    remplit de 0 à 100 %, la suivante s'ouvre à un seuil (~75 %),
    mais on a **le droit d'aller se frotter partout** (« le boss de
    là-bas est trop dur, mais t'as le droit d'y aller ») — parce que
    « c'est pas parce que j'ai pas compris ce qu'est une lézarde que
    je peux pas comprendre une courroie de VMC ». L'XP remplit les
    régions et les débloque, rien d'autre. L'horizon : « une lumière
    au bout » qu'on voit sans mesurer la distance — l'immensité se
    révèle région par région, jamais d'un coup (ne pas décourager).
    Amendement tracé du BLUEPRINT §9 ; spec : SPEC-PRODUIT §3.
31. **Boss de fin de région : OUI, enthousiaste** — un examen de
    branche à froid (« examen blanc » qui pioche dans les annales pour
    Arthur), sans lequel le 100 % de la région n'existe pas.
32. **Onboarding : le quiz de positionnement** — [JB] ~20 questions au
    premier lancement pour évaluer le niveau réel et ne pas « se
    retaper tout depuis le début » ; puis jouer immédiatement quelques
    cartes de son domaine. [ARBITRÉ] mécanique précisée en spec.
33. [ARBITRÉ] Régularité : calendrier de pastilles doux (façon
    GitHub), cohérent avec le streak cumulé déjà arbitré — jamais de
    série qui casse, jamais de dette affichée.
34. **Chemin guidé automatique : OUI** — [JB] « si le matin t'as pas
    envie de choisir, un tirage au hasard qui correspond à ton niveau
    et t'avances ». [ARBITRÉ] l'habillage machine à sous reste sobre
    (< 1,5 s), ça se règle en M4.
35. [ARBITRÉ] Cosmétique : léger — titres liés aux régions conquises,
    rien de plus. Zéro boutique, zéro monnaie.

### VII-VIII. Technique et IA (le brief tranche l'essentiel)

36. [ARBITRÉ] Front : **React dans un build propre au produit**
    (option b) — les composants Académie existants se réutilisent, et
    le produit a un mainteneur outillé (JB + Claude Code).
37. [ARBITRÉ] Hébergement : **le VPS OVH actuel**, vhost + domaine
    dédié, process et racine servie hors du clone wiki-copro
    (étanchéité par construction, pas par mot de passe). Migration
    possible plus tard sans rien casser (tout est fichiers + SQLite).
38. [ARBITRÉ] Auth : **magic links par mail** — pour 2-6 joueurs
    connus et invités à la main, le meilleur rapport
    simplicité/sécurité. Pas de mot de passe à stocker.
39. [ARBITRÉ] Stockage serveur : **SQLite** pour comptes, état de jeu
    et journal de révisions (plusieurs écrivains + effacement RGPD) ;
    les **banques de domaine restent des JSON** au contrat carte-v1,
    versionnés — le contrat ne change pas.
40. PWA/mobile : Arthur joue « ordi et téléphone » → le produit
    séparé naît responsive ; la PWA hors-ligne reste M8, avant M9
    dans l'ordre de construction.
41. **Aucune clé de tiers côté serveur — mieux : aucun appel IA côté
    serveur pour un tiers** — [BRIEF] « le traitement se fait en
    local au prix de leur abonnement ou API, pas le mien. » Toute la
    fabrication (tri de sources, génération, double passe) tourne
    chez le joueur ; le serveur ne reçoit que des fiches JSON
    validées. La brique 3 de M9 (stockage de clé tiers) est résolue
    **par suppression**. Détail : SPEC-PRODUIT §2 et §4.
42. **v1 artisanale : OUI** — [JB en séance] le domaine d'Arthur se
    fabrique une première fois JB + Arthur + une session Claude, un
    soir ; le déroulé de cette soirée DEVIENT le script de l'usine
    (M10). « Do things that don't scale. »
43. Budgets IA : Arthur max 10 €/mois (Q10). JB : non chiffré en
    séance ; [ARBITRÉ] même ordre de grandeur pour la part produit.
44. **Sans clé : 100 % jouable en dégradé** (modes à correction
    exacte, pas de réponse libre ni de génération). OUI — gravé ; ça
    répond à la question ouverte n°1 du pré-mortem du 29/08.

### IX-X. Social, RGPD, qualité

45. Suppression de compte sous 48 h avant le premier compte tiers :
    **non négociable, confirmé**.
46. **Reste dû** : l'inscription d'Arthur au registre RGPD
    (personne concernée, base légale, information) — formalité réelle
    à acter avec lui avant son premier compte, pas couverte en séance.
47. Invitations sur lien privé envoyé à la main : oui, suffisant pour
    12 mois.
48. Multi-domaines par joueur + entrelacement en séance : oui (JB :
    copro + culture ; Arthur : concours + culture).
49. **Double passe par agent frais obligatoire pour TOUS les
    domaines** : oui, gravée — le statut `brouillon` bloque côté
    moteur, quel que soit le domaine et quelle que soit la clé.
50. [ARBITRÉ] Les 3 premiers mois d'Arthur : une passe JB « qualité
    du format » (pas du fond, qu'il ne connaît pas) sur ses lots.
51. [ARBITRÉ] Bouton « carte fausse » : la carte sort de rotation
    immédiatement **chez le signaleur seulement** ; le retrait global
    attend l'arbitrage du propriétaire du domaine (JB pour le tronc
    commun Culture).
52. **Reste dû** : le pré-mortem personnel (« août 2027, le produit
    est mort : raconte en 5 lignes »), chacun séparément puis
    comparaison. La spec porte en attendant la version de Claude
    (SPEC-PRODUIT §6).

### Les « reste dû » (à sonner au bon moment ; révisés au pré-mortem du 29/08 soir)

| Quoi | Qui | Quand |
|---|---|---|
| ~~La date du concours FPC d'Arthur~~ **RÉPONDU le 29/08 au soir : épreuve en mars/avril 2027** | — | ~7 mois de piste : le plan O6/O7 tient, Arthur joue SUR L'APP (arbitrage JB : pas de détour Anki, « le but c'est construire l'app ») |
| ~~Information RGPD d'Arthur (Q46)~~ **TRANCHÉ par JB le 29/08 au soir** : « Arthur est comme mon frère », cercle familial, pas de formalité — JB assume et l'informera de vive voix | — | La machinerie RGPD du PRODUIT (registre, suppression de compte 48 h, sous-traitant mail) reste entière pour M9 : c'est le formalisme envers Arthur qui est levé, pas les protections |
| 3-5 dossiers « en or » pour les cas d'école (Q20) | JB | À l'ouverture de M3 |
| Pré-mortem personnel en 5 lignes (Q52) | JB et Arthur, séparément | Avant le GO d'O6 — déclencheur : la session qui prépare l'ouverture de M9 le réclame et ne s'ouvre pas sans |
| Budget de JB pour la soirée artisanale (elle tourne sur SON abonnement, §2 de la spec) | JB | Avant O7 |

# DIRECTION ARTISTIQUE, à quoi ressemble l'Académie et comment elle bouge

Écrite le 02/09/2026 sur le brief de JB (« beau, sexy, Dribbble,
Awwwards, jolies animations, agréable comme Duolingo, ni genre ni âge,
pas de petit bateau »). Ce document remplace le `DESIGN.md` d'août
(archivé). Le front est déclaré jetable ([`decisions/0007`](decisions/0007-stack-front-et-dependances.md)) ;
ce qui ne l'est pas, c'est cette direction. La maquette cliquable du
02/09 vit dans `travail/maquette-2026-09-02.html`.

---

## 1. L'intention en trois mots : la planche

Une **planche** d'encyclopédie, de carnet d'architecte, d'atlas : un
fond profond, des lignes fines, des anneaux, une typographie qui a du
caractère. Adulte sans être froid, vivant sans être enfantin. Pas de
mascotte, pas de bateau, pas d'avatar : **l'arbre est l'avatar**, et ce
qui bouge à l'écran, c'est le savoir qui se dessine.

Trois références de ton, pour situer sans copier : les outils de
productivité haut de gamme (densité calme, transitions courtes), les
applications de sport (le journal, la régularité, les jalons qu'on
partage soi-même), les atlas et cartes anciennes (les lignes, les
hachures, le grain).

Ce qu'on refuse : les couleurs primaires saturées partout, les
personnages, les confettis, les sons par défaut, les compteurs qui
rougissent, les modales qui supplient.

## 2. Les tokens

### Couleurs

Deux thèmes, choisis par le système ou par le joueur : **Papier** (défaut)
et **Nuit**. Aucun hexadécimal dans un composant : tout passe par les
variables.

| Rôle | Nuit | Papier |
|---|---|---|
| fond | bleu nuit très profond, légèrement chaud | blanc cassé, grain léger |
| surface | un cran plus clair que le fond | blanc |
| encre (texte) | ivoire | anthracite |
| encre secondaire | ivoire à 62 % | anthracite à 62 % |
| trait (lignes, anneaux vides) | ivoire à 14 % | anthracite à 14 % |
| accent du domaine | la palette du domaine (ci-dessous) | idem, assombrie |
| succès | vert mousse | idem |
| erreur | terre brûlée, jamais rouge vif | idem |
| brouillard | fond à 70 % avec flou | idem |

**Une palette par domaine**, attribuée au rang du domaine (jamais à son
nom, pour qu'un autre métier hérite sans rien coder) : ocre, cuivre,
sauge, lavande, bleu acier, brique, olive, prune, sable, ardoise.
Chaque domaine validé débloque sa palette comme thème d'accent de
l'outil ([`BLUEPRINT.md`](BLUEPRINT.md) §12).

### Typographie

- **Titres** : une serif à empattements marqués, à axe variable
  (Fraunces, licence OFL, auto-hébergée). Elle donne le côté planche.
- **Texte et interface** : une sans humaniste lisible petite, avec de
  vrais chiffres tabulaires (Source Sans 3, OFL, auto-hébergée ; la
  maquette du 02/09 l'utilise).
- **Chiffres** : toujours en chiffres tabulaires (`font-variant-numeric:
  tabular-nums`) pour les scores, dates, comptes et surtout la
  comptabilité (méthode §13).
- Corps 17 px sur téléphone, 16 sur ordinateur ; interligne 1,5 ;
  longueur de ligne 60 à 70 caractères pour les leçons.

### Espace, formes, relief

- Grille de 4 px ; marges 16 sur téléphone, 24 sur ordinateur.
- Rayons imbriqués : extérieur 20, intérieur 12 (rayon intérieur = rayon
  extérieur moins le padding).
- Une seule ombre, douce et large, réservée aux surfaces qui flottent
  (feuille de sources, carte en cours) ; le reste est plat.
- Le **grain** : un bruit très léger sur le fond, comme du papier ;
  désactivable.

## Amendement du 05/09 : couleurs et vue globale

La demande explicite de JB et la décision 0037 reprennent la palette et
la géométrie : Papier rosé, encre prune, accent framboise sourd ; Nuit
prune conservé. Les valeurs exactes vivent dans `web/src/index.css`.
La vue globale devient un index de domaines avec branches et disponibilité
réelles, sans orbites, zoom ni rotation. Les paragraphes radiaux ci-dessous
restent l'intention historique ; cet amendement les remplace pour la vue
globale. Les fiches et prérequis restent accessibles dans la vue domaine.

## 3. L'arbre

### Rendu

- SVG. Chaque chapitre est un **nœud** : un disque avec un anneau de
  remplissage (le pourcentage FSRS), un glyphe (game-icons, CC BY,
  attribution dans l'écran Crédits), un titre. Un satellite est un
  nœud plus petit, en pointillé, en orbite de son nœud d'attache.
- Les **liens** sont des courbes fines, pleines entre nœuds ouverts,
  pointillées vers un prérequis d'un autre domaine, à peine visibles
  vers un nœud en silhouette.
- Le **tronc** (le socle) est une colonne au centre de la vue globale ;
  les domaines s'ordonnent autour comme des branches maîtresses, dans
  l'ordre du programme.
- Le **brouillard** : silhouettes sans titre pour l'inconnu (flou et
  fond à 70 %), grisé daté pour le périmé.
- La **canopée** : les nœuds de niveau 4 et 5 s'estompent vers le bord
  de la vue ; il n'y a pas de bord net.

### Disposition

- Vue globale : radiale, dix branches maîtresses, lisible en un écran
  sur ordinateur, à faire pivoter au doigt sur téléphone.
- Vue domaine : verticale, du tronc (haut) vers la canopée (bas), une
  colonne par branche, les divisions et les rejoints dessinés. Sur
  téléphone elle se parcourt en défilant ; les positions sont écrites
  dans `programme/<metier>.json` (bloc `disposition`) et un placement
  automatique sert de repli.
- Zoom et déplacement au doigt et à la molette, sans inertie longue.

### Interactions

- Tap sur un nœud : la **fiche du nœud** monte en feuille (titre,
  niveau, état, ce que tu sauras faire, prérequis, sources, boutons
  Réviser / Continuer / Étudier / Épreuve selon l'état).
- Tap sur un domaine (vue globale) : la vue domaine, avec le bandeau
  « ce matin, compta » et ses propositions.
- Appui long : rien. Aucune interaction cachée.

## 4. Les écrans et la navigation

### La barre

- **Téléphone** : barre basse à quatre entrées, dans la zone du pouce :
  **Arbre** (accueil), **Cercle**, **Boîte**, **Profil**. L'action du
  jour est un bouton flottant en bas à droite de l'arbre (« Séance »),
  jamais dans la barre.
- **Ordinateur** : rail gauche avec les mêmes quatre entrées et le
  bouton Séance en haut du rail ; l'arbre occupe tout le reste. Une
  séance, une étude ou une épreuve ouvrent une **salle** en plein
  écran, sans rail, avec une sortie évidente en haut à gauche.

### Les écrans

| Écran | Ce qu'il montre | Ce qu'on y fait |
|---|---|---|
| **Arbre** | la vue globale, le cap du jour en bandeau (jour coloré, cartes dues), le bouton Séance | choisir un domaine, lancer la séance, au hasard |
| **Domaine** | la vue domaine, le bandeau « ce matin, X » avec Réviser / Continuer / Étudier / Épreuve / Au hasard | choisir un nœud |
| **Fiche du nœud** | feuille : niveau, état, objectifs, prérequis, sources, la fiche de rappel | lancer, lire la fiche |
| **Salle : séance** | une carte à la fois, barre de progression fine en haut, en-tête domaine + type | répondre, révéler, noter |
| **Salle : étude** | quatre étapes en fil (amorce, leçon, exercices, synthèse) avec un rail d'étapes | dérouler |
| **Salle : épreuve** | la même carte, une ambiance plus sobre, pas de sources avant la fin | répondre à froid |
| **Clôture** | un écran : stabilisé, revient demain, nœud qui a bougé, la phrase, une citation aux jalons | fermer, partager un jalon |
| **Profil** | carte de visite (titre, socle, calibration, compteur), heatmap, insignes, bilan du mois, carnet d'erreurs (privé), réglages, export | régler, exporter, lire son bilan |
| **Profil d'un autre** | carte de visite, arbre miniature limité aux domaines visibles, insignes affichés, compteur ; rien d'autre | kudos, défi |
| **Cercle** | trois onglets : Fil (jalons, kudos), Ligue (facultative, sa ligne en avant), Défis | suivre, défier |
| **Boîte** | une zone de dépôt (texte, lien, photo, fichier), la file d'attente et son état (à traiter sur le Mac, chapitre proposé, rattaché) | glisser |
| **Crédits** | licences des icônes, polices, sources scientifiques (la MÉTHODE) | lire |

## 5. La carte d'exercice

Anatomie, de haut en bas :

1. **En-tête** : pastille du domaine (sa couleur), type d'exercice avec
   son glyphe et son mot (« QCM », « Photo », « Cas »), niveau en
   chiffre romain discret.
2. **Corps** : la question, l'image si elle existe (pleine largeur,
   légende sur l'image, jamais à côté), les choix ou la zone de réponse.
3. **Zone du pouce** (téléphone) : les boutons de réponse ou de
   révélation, hauts de 48 px au moins, dans le tiers inférieur.
4. **Après réponse** : le retour (juste ou faux, en une ligne, ton
   neutre), l'explication en trois lignes, la vigilance, puis la ligne
   **source** (note de confiance en lettre, nature, parti, vérifié le,
   « à recouper » ou « sans source retrouvée » s'il y a lieu) puis la
   ligne de **provenance** en encre tertiaire (« Généré par Claude Opus le
   21/08/2026 · 2 sources concordantes · relu le 22/08 »), qui s'ouvre en
   feuille pour le dossier complet, le bouton « cette carte est fausse »
   et le lien « Pourquoi croire ce professeur ? ». En épreuve, cette
   ligne n'apparaît qu'à la fin.
5. **Notes FSRS** (flash) : quatre boutons, mots adultes : À revoir,
   Difficile, Bien, Évident.

**Chaque type a sa personnalité** : un glyphe, une teinte de fond très
légère tirée de l'accent du domaine, une disposition. Un QCM ne
ressemble pas à une photo qui ne ressemble pas à un cas en pas. La
sobriété revient pour l'erreur : le moment de l'hypercorrection est
sérieux.

## 6. Le mouvement

- Durées : 120 ms pour un retour (pression, sélection), 200 à 260 ms
  pour une transition d'écran, 400 à 600 ms pour une conquête (anneau
  qui se remplit, brouillard qui recule). Jamais plus d'une seconde.
- Courbes : sortie rapide, entrée douce (`cubic-bezier(0.2, 0, 0, 1)`
  et ses variantes) ; pas de rebond, pas d'élastique.
- Ce qui bouge : l'anneau d'un nœud quand une carte se stabilise ; le
  brouillard qui se dissipe sur un nœud qui s'ouvre ; le lien qui se
  trace vers le nœud suivant ; la carte qui glisse latéralement à la
  suivante ; la feuille qui monte. Ce qui ne bouge jamais : le texte
  qu'on lit, les chiffres de comptabilité, l'écran d'erreur.
- **Ouverture** : moins de trois secondes jusqu'à la première question,
  aucune animation d'entrée.
- **Mouvement réduit** respecté : les transitions deviennent des fondus
  de 120 ms.
- **Haptique** sur téléphone : une impulsion brève à la réponse, une
  double à la conquête, jamais à l'erreur. **Son** : coupé par défaut,
  activable, quatre sons discrets au plus.
- Les célébrations : l'anneau qui se ferme, le brouillard qui recule,
  une citation sourcée en serif, un insigne qui se dessine trait par
  trait. Aucun confetti, nulle part.

## 7. Accessibilité

- Contraste AA partout, y compris sur les palettes de domaine.
- Jamais une information portée par la couleur seule : l'état d'un nœud
  se lit aussi à l'anneau, au titre, au glyphe.
- Cibles tactiles de 44 px au moins ; clavier complet sur ordinateur
  (espace révèle, 1 à 4 notent, Échap sort).
- Étiquettes de lecteur d'écran sur l'arbre (chaque nœud annonce titre,
  niveau, état) et sur les images (`image.alt` obligatoire au contrat
  v2).
- Taille de texte du système respectée ; mise en page qui tient à
  200 %.

## 8. Les mots

- Ton complice, adulte, court. Jamais infantile, jamais culpabilisant,
  jamais d'exclamation.
- La clôture dit un fait et une action : « Socle à 62 %. La compta est
  ta branche la plus en retard ; une étude de 45 minutes la fait passer
  à 70 %. »
- Après une erreur : « Pas ça. » puis l'explication. Jamais « Dommage ! ».
- Les titres du joueur sont des mots du métier (Apprenti, Junior,
  Gestionnaire, Confirmé, Expert, Référent), jamais des grades de jeu.
- Les citations aux jalons sont attribuées et sourcées (banque dans le
  client, une entrée = auteur, œuvre, date).

## 8 bis. Où va le regard, et combien de stimulation

Chaque écran a **un point où le regard arrive** et un niveau de
stimulation voulu. Le reste se tait.

| Écran | Le regard arrive sur | Stimulation | Ce qui se tait |
|---|---|---|---|
| Arbre | le bandeau du jour (« Lundi, fondations · 9 cartes ») puis le tronc | moyenne : l'arbre vit un peu (anneaux, brouillard), rien ne clignote | les chiffres du profil, la barre |
| Domaine | le bandeau « ce matin, compta » et son premier bouton | moyenne | les autres domaines |
| Séance | la question, seule, au tiers supérieur ; les réponses dans la zone du pouce | **basse** : c'est le moment de récupération, aucune distraction, aucun compteur en gros | la barre (masquée), les sources (repliées) |
| Après réponse | la ligne de retour (« Pas ça. »), puis l'explication | basse, plus sobre encore en cas d'erreur | tout mouvement |
| Clôture | la phrase du jour, puis l'anneau qui a bougé | **haute mais brève** : c'est ici que le plaisir se dépense, une fois par séance | |
| Épreuve | la question ; aucune source, aucun retour avant la fin | basse, solennelle | tout |
| Profil | le socle en chiffre de tête, puis la carte de visite | moyenne | |
| Cercle | le dernier jalon du fil | moyenne | la ligue (un onglet, pas la page) |

Règle : **une seule chose en avant par écran**. Ce qui est en avant est
grand et coloré ; tout le reste est en encre secondaire. Le mouvement
n'a lieu qu'aux moments de stimulation haute.

## 8 ter. Clavier, souris, pouce

- **Téléphone** : tout se fait d'une main. Les réponses sont dans le
  tiers inférieur ; glisser vers la gauche révèle, vers la droite passe
  à la suite (avec les boutons, jamais à la place). La barre est basse.
  Jamais un geste caché.
- **Ordinateur** : `Espace` révèle, `1` à `4` notent, `Entrée` valide,
  `Échap` sort d'une salle, `?` liste les raccourcis. La souris n'est
  jamais nécessaire dans une salle. Sur l'arbre : molette pour zoomer,
  glisser pour déplacer, clic sur un nœud.
- **Bento** : le profil est une grille de tuiles inégales (le socle
  large, la heatmap longue, les insignes en mosaïque, le bilan en
  carte), la seule page qui a le droit d'être dense. L'arbre et les
  salles ne sont jamais en grille.
- **Bordures et boutons** : un trait à 14 % d'encre, jamais d'ombre sur
  un bouton ; le bouton principal est plein de l'accent du domaine, les
  autres sont creux ; hauteur 48 px sur téléphone, 40 sur ordinateur ;
  état pressé à 98 % d'échelle, 120 ms.

## 9. Checklist avant de committer un écran

- [ ] Aucun hexadécimal, aucune couleur hors tokens.
- [ ] Chiffres en tabulaire.
- [ ] Téléphone à 375 px, ordinateur à 1280, texte à 200 % : rien ne
  déborde, pas de défilement horizontal.
- [ ] Nuit et Papier.
- [ ] Mouvement réduit testé.
- [ ] Clavier et lecteur d'écran sur le chemin principal.
- [ ] Première question en moins de trois secondes sur un téléphone de
  milieu de gamme, réseau coupé.
- [ ] Aucun confetti, aucune exclamation, aucune culpabilisation.

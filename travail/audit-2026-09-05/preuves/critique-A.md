# Assessment A — critique indépendante du rendu Académie

Date : 05/09/2026. Cible : `web/src/ecrans/`, rendu local `http://127.0.0.1:4173/academie/`. Aucun résultat du détecteur ni de l’assessment B consulté. Aucune modification produit.

Lecture : DOCTRINE.md, README.md, web/AGENTS.md, DIRECTION-ARTISTIQUE.md ; skill Impeccable 4.1.3 et reference/critique.md. Mode : Operate, avec lecture pédagogique dans la salle. Le script context a confirmé une implémentation existante sans PRODUCT.md/DESIGN.md ; la doctrine et la DA constituent ici le cadre explicite, leur absence n’a pas bloqué la critique.

## Verdict de spécificité

La composition est identifiable et cohérente avec Académie : Fraunces, tons minéraux, lignes fines, constellation de métiers autour du socle, surfaces ouvertes. Ce n’est pas une landing page générique à cartes. Le problème principal est que cette planche représente mieux la promesse de programme que le chemin réellement apprenable. La séance possède une véritable sobriété adulte ; elle n’a pas encore la cadence lisible ni le retour de progression nécessaires au rituel demandé.

## Preuves observées

- 1280 × 900 : accueil Nuit, domaine droit, ouverture du premier chapitre vide, début de séance, profil Papier.
- 375 × 812 : accueil Nuit, question avec frise, correction, dossier de sources, profil DOM.
- Captures : `/tmp/academie-audit-design-A/01-arbre-1280.png`, `02-domaine-1280.png`, `03-seance-1280.png`, `04-seance-375.png`, `05-arbre-375.png`, `06-profil-papier-1280.png`.
- La première séance observée le 5 septembre sert une seule carte neuve de niveau III « Lecture de plan », en procédure, alors que le profil indique zéro réponse. Elle demande trois raisonnements sur une frise judiciaire.
- Le domaine droit affiche 60 chapitres, 26 cartes ; tous les chapitres listés portent « À écrire ». Le premier ouvre une feuille sans carte, avec Réviser désactivé. Les 26 cartes jouables sont regroupées après toute la liste sous « Cartes en cours de rattachement ».
- Le profil signale explicitement la synchronisation indisponible et le journal conservé sur l’appareil. C’est une observation sur le serveur preview, pas un constat de panne VPS.

## Trois forces à préserver

1. **Une identité adulte déjà réelle.** Le duo typographique, le dessin radial, les accents mesurés et le thème Papier tiennent ensemble. Le rendu ordinateur évite l’empilement de panneaux et donne une impression de livre de travail soigné. Preuves : captures 01, 02, 06 ; `web/src/index.css:19`, `:215`, `:376` ; `web/src/ecrans/Arbre.tsx:39`.
2. **La salle sait retirer la navigation.** Le titre métier et le compteur restent discrets, la question prend le premier rôle, les sources se replient. Les boutons de réponse et notes ont des libellés adultes. Les raccourcis Échap, Espace/Entrée et 1–4 existent dans le code ; le titre reçoit le focus. Preuves : capture 03 ; `web/src/ecrans/Seance.tsx:104`, `:134`, `:136`, `:244`.
3. **Les états vides et la conservation locale sont dits.** Le chapitre ne simule pas un contenu disponible ; le profil prévient de l’absence de synchronisation et propose une reprise. Sources officielles consultables après la réponse, lien Confiance et signalement présents. Preuves : DOM du premier chapitre et du profil, dossier de sources ; `web/src/ecrans/Noeud.tsx:24`, `web/src/ecrans/Profil.tsx:51`, `web/src/ecrans/Seance.tsx:248`.

## Cinq défauts prioritaires

### A1 — P1 : le parcours principal expose les trous avant le premier apprentissage

L’accueil met 389 chapitres en avant, puis Explorer mène à 60 chapitres « À écrire ». Le novice choisit « Qu’est-ce qu’une copropriété », ouvre une feuille, découvre zéro carte et un bouton désactivé. Le programme est honnête, mais l’organisation exige de comprendre la différence entre programme, banque et rattachement avant de savoir où apprendre. La voie directe Séance sert immédiatement une carte avancée de procédure, sans expliquer le choix ni proposer un commencement adapté au novice.

Preuves : captures 01–03 ; `web/src/ecrans/Arbre.tsx:30`, `:81`, `:86` ; `web/src/ecrans/Domaine.tsx:30`, `:37`, `:42` ; `web/src/ecrans/Noeud.tsx:24`, `:28` ; `web/src/ecrans/Seance.tsx:28`.

Correction proposée : rendre le premier chemin jouable explicite dès l’accueil, afficher l’objectif concret et la disponibilité avant les destinations vides, conserver le programme complet comme vue d’exploration. Relier la banque aux chapitres avec les preuves de contenu requises ; préparer un vrai parcours de départ/positionnement, sans déclarer qu’il existe déjà. Aucun besoin de changer la DA pour cette hiérarchie.

Acceptation : un nouvel utilisateur atteint une première question adaptée depuis l’accueil ; chaque chapitre proposé comme « à commencer » contient une séquence réellement jouable ; un chapitre vide présente un prochain chemin utile et ses objectifs. Vérification comportementale avec un novice, distincte des tests de navigation. Commandes pertinentes : clarify / onboard / shape.

### A2 — P1 : la question longue et la frise deviennent impraticables sur téléphone

À 375 pixels, l’intitulé occupe 526 pixels de haut dans une colonne de 295 pixels. Le premier écran ne montre pratiquement que la question ; l’image et toute réponse passent en dessous. La frise complète est comprimée à environ 295 × 113 pixels sans agrandissement dédié dans le composant. Après révélation, la correction observée mesure 1 462 pixels de haut ; les quatre notes arrivent après ce bloc. La question domine bien, mais sa taille et son contenu repoussent l’exercice réel de plusieurs écrans. La frise sert à répondre tout en devenant difficile à lire.

Preuves : captures 03 et 04 ; mesures DOM après révélation ; `web/src/index.css:303`, `:305`, `:327`, `:331`, `:334`, `:335` ; `web/src/ecrans/Seance.tsx:160`, `:161`, `:191`.

Correction proposée : un énoncé principal court, des sous-questions séquencées lorsque pédagogiquement approprié, une image consultable à taille lisible, une correction structurée avec réponse essentielle puis développement. Garder les commandes atteignables au pouce sans masquer le texte. Toute nouvelle mécanique pédagogique doit avoir son cahier et son entrée METHODE.

Acceptation : sur les cartes réellement les plus longues, à 375 pixels et texte à 200 %, une personne peut lire tous les labels nécessaires de la figure, trouver la saisie/révélation et comprendre comment passer à la suite ; pas de défilement horizontal de page. La réduction du titre ne suffit pas à prouver cette réussite. Commandes : adapt / typeset / distill.

### A3 — P2 : l’arbre mobile impose de deviner dix pictogrammes

Les dix domaines conservent leurs icônes, mais tous leurs noms disparaissent à 375 pixels. Seul le domaine sélectionné est nommé sous l’arbre. Un novice doit essayer une icône puis lire le panneau, ou parcourir les flèches une à une. Une poignée de main et un livre ne permettent pas d’identifier spontanément « Le cabinet » ou « Propriété, immobilier et urbanisme ». Les noms ARIA sont présents : le défaut porte sur la reconnaissance visuelle, pas une absence totale de nom accessible.

Preuves : capture 05 ; `web/src/index.css:237`, `:418` ; `web/src/ecrans/Arbre.tsx:61`, `:76`.

Correction proposée : conserver l’atlas, lui ajouter une sélection textuelle lisible et groupée ou des libellés courts suffisamment distincts. Le choix du métier/domaine ne doit pas dépendre de la mémorisation des glyphes.

Acceptation : sur 375 pixels, un novice retrouve un domaine nommé sans essais successifs ; mêmes noms et état sélectionné accessibles au clavier/lecteur d’écran. Commandes : clarify / adapt.

### A4 — P2 : le profil raconte des compteurs, pas ce que l’élève sait faire

Le profil rend Niveau 1, points, pourcentage global, révisions, cartes et jours joués, puis une heatmap et les réglages. Il ne dit pas quelle capacité concrète commence à être acquise, ce qui mérite une prochaine séance ou quel jalon professionnel approche. Le vide affiche six valeurs nulles ou initiales sans chemin d’entrée. Le composant de clôture, lu mais non joué jusqu’au bout, expose surtout des comptes du jour et un retour à l’arbre ; aucun anneau de chapitre réellement déplacé n’y est rendu. Les données manquantes ne doivent évidemment pas être inventées.

Preuves : capture 06 ; `web/src/ecrans/Profil.tsx:41`, `:42`, `:50` ; clôture uniquement par code : `web/src/ecrans/Cloture.tsx:22`.

Correction proposée : donner la priorité à une capacité mesurée et un prochain pas ; expliquer ce que mesure le pourcentage. Quand rien n’est mesuré, montrer le point de départ concret. Réserver la satisfaction visuelle à une progression réellement calculée, cohérente avec l’anneau et la voix existants.

Acceptation : après une séance connue, le joueur peut nommer ce qu’il a travaillé, distinguer activité et maîtrise, et expliquer le prochain pas sans lire le dépôt. Au premier lancement, aucune progression fictive et une invitation utile. Commandes : clarify / delight, après disponibilité des données de maîtrise.

### A5 — P2 : l’autoévaluation et la confiance restent peu explicites pour un premier utilisateur

« J’étais sûr » apparaît avant même la réponse. Après lecture, quatre notes « À revoir / Difficile / Bien / Évident » sont présentées sans explication visible de ce qu’elles mesurent ou de leur effet. Le même code rend ces quatre notes pour les QCM après avoir affiché juste/faux : le novice peut confondre la correction objective avec son sentiment de facilité. Le dossier Sources de la carte observée donne références, nature et date, mais pas de ligne de provenance auteur/relecteur, faute de données affichables. Une interface qui demande de s’évaluer gagne à expliquer sa règle et ses limites au moment utile.

Preuves : DOM séance/correction/sources ; `web/src/ecrans/Seance.tsx:181`, `:200`, `:224`, `:258`. Absence de provenance constatée sur cette carte uniquement, pas extrapolée à toute la banque.

Correction proposée : une explication brève et reconsultable des quatre réponses lors du premier usage, vocabulaire de confiance au présent avant la tentative, séparation claire entre résultat et facilité. Afficher explicitement les champs de provenance manquants plutôt que laisser croire que le dossier est complet.

Acceptation : un novice choisit une note selon le critère voulu ; le QCM distingue résultat et autoévaluation ; chaque dossier expose auteur/relecteur ou « non renseigné » sans fabrication. Commandes : clarify / onboard.

## Heuristiques de Nielsen, évaluation A

Scores de qualité de 0 (absent/défaillant) à 4 (excellent). Ce sont des jugements d’expert fondés sur les parcours observés, pas une mesure d’acceptation utilisateur.

| Heuristique | Score / 4 | Justification |
|---|---:|---|
| Visibilité de l’état | 3 | Compteur de salle, disponibilité, sélection et erreur de synchronisation lisibles ; signification du progrès peu claire. |
| Langage du monde réel | 2 | Noms de métier naturels ; « À écrire », rattachement et autoévaluation demandent des explications. |
| Contrôle et liberté | 3 | Quitter, fermer la feuille, Échap, thèmes et export ; reprise d’une saisie interrompue non vérifiée. |
| Cohérence et standards | 3 | Navigation et surfaces cohérentes ; noms de domaines disparaissant sur mobile. |
| Prévention des erreurs | 2 | Chapitre vide désactivé ; risques de mauvais choix de difficulté/autoévaluation non guidés. |
| Reconnaissance plutôt que mémorisation | 1 | Dix icônes muettes sur mobile, nombreuses destinations sans apprentissage immédiat. |
| Flexibilité et efficacité | 2 | Raccourcis codés, recherche de chapitre ; consultation répétée du catalogue et absence de guidance de départ. |
| Esthétique et sobriété | 3 | Identité forte et calme ; énoncé mobile trop volumineux. |
| Récupération après erreur | 3 | Message local rassurant et action Réessayer ; autres pannes non provoquées. |
| Aide et documentation | 1 | Sources et Confiance présents ; pas d’aide contextuelle observée au premier choix ou à la notation. |
| Total | 23 / 40 | Base visuelle solide, parcours pédagogique encore incomplet. |

## Charge cognitive et trajet émotionnel

Charge modérée à forte selon l’écran. Points de décision dépassant quatre options : dix domaines sur l’accueil ; neuf chapitres dans la première branche, soixante dans le domaine observé ; cinq niveaux dans le filtre plus Tous. La quantité seule n’est pas une preuve d’échec : les branches organisent le domaine. Les échecs concrets sont l’absence de recommandation jouable, le rappel nécessaire du sens des pictogrammes, le passage obligé entre catalogue et contenu pour comprendre leur relation et la correction non découpée. Dans la salle, une action de révélation puis quatre notes restent un nombre raisonnable de choix.

Émotion : l’accueil donne envie d’explorer un univers professionnel sérieux ; la première feuille vide crée un creux ; la première question avancée et très longue augmente l’effort avant le premier succès. Les sources et la conservation locale rassurent. La fin de séance n’a pas été jouée : son effet émotionnel reste une hypothèse issue du composant, à vérifier avec des séances réelles.

## Personas : risques concrets

- **Jordan, première visite** : ouvre le premier chapitre logique, trouve un bouton désactivé ; ne sait pas pourquoi Séance commence directement par une lecture de plan niveau III.
- **Casey, téléphone dans le tram** : ne reconnaît pas le domaine parmi dix icônes ; doit défiler pour accéder à la figure et aux commandes ; la figure réduite ne permet pas aisément de lire les éléments demandés.
- **Sam, accessibilité** : étiquettes ARIA de domaines et focus explicitement présents ; alt de la frise observée répète la question au lieu de décrire le contenu nécessaire. Parcours VoiceOver, clavier intégral et texte 200 % non exécutés dans A, donc non certifiés.

## Détails secondaires

- Les contrôles de zoom de l’arbre ont une largeur CSS de 36 pixels (`web/src/index.css:239`), inférieure aux 44 pixels fixés par la DA ; la hauteur est 44.
- « 1 lignes de journal » manque le singulier (`web/src/ecrans/Profil.tsx:51`).
- La heatmap expose les nombres quotidiens via title ; consultation au toucher ou lecteur d’écran non vérifiée.
- Les raccourcis existent dans le code de la salle, mais aucune liste accessible avec « ? » n’y est implémentée.

## Questions de conception à soumettre dans la synthèse

Quel premier accomplissement métier doit survenir durant la première séance d’un novice ? Quelle part du programme doit-on montrer avant d’avoir rendu ce premier accomplissement possible ? Quand une carte demande trois raisonnements et une figure, appartient-elle au rituel court ou à une séquence d’étude guidée ?

## Limites et nettoyage

Pas de test sur téléphone physique, pas de preuve d’acceptation humaine, pas de test réseau hors ligne ni zoom texte 200 %, pas de lecteur d’écran. Aucun constat de disponibilité VPS. Tests produit et gates laissés à l’agent parent qui consolide l’audit. Aucune note d’exercice, réponse écrite ou signalement envoyé ; entrer en séance a automatiquement ajouté un événement local d’ouverture, visible au profil en attente. Thème Papier testé puis Nuit restauré ; viewport réinitialisé. Serveur du parent laissé actif. Captures conservées comme preuves temporaires. Aucun détecteur lancé dans A, conformément à l’indépendance prescrite.

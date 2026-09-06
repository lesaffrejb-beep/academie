# Candidat Fragilité : preuves et relecture à faire

Préparé le 06/09/2026 par Codex, GPT-6, agent `/root/acces_profils`.
Le fichier `diagnostic-partage-fragilite.brouillon.json` est un candidat
distinct : neuf cartes, cinq formats, une leçon de 681 mots, une amorce et une
synthèse finale. Aucune promotion ni relecture indépendante n'est revendiquée.

## Source et limite de couverture

Source de fond unique : Anah, *Gérer et accompagner les copropriétés fragiles*,
édition 2026, copie locale `sources/0a7537d478616271.pdf`, 195 pages.
[Notice officielle](https://www.anah.gouv.fr/anatheque/gerer-accompagner-coproprietes-fragiles),
[PDF lié par cette notice](https://www.anah.gouv.fr/sites/default/files/2026-08/082026_guide_gerer-coproprietes-fragiles.pdf).
Le lien public a été retrouvé dans cette passe ; le fond du candidat vient du
pivot local et des rendus existants, pas d'une nouvelle ingestion distante.
La concordance binaire entre copie locale et URL actuelle n'a pas été mesurée.

Commandes rejouées :

```text
python3 app/usine/usine.py etat 0a7537d478616271
python3 app/usine/usine.py suivant 0a7537d478616271
```

L'usine indique 195/195 pages relues, dix unités, 31 chiffres lus en vision à
faire vérifier, dernier événement « fiche validée » le 06/09 à 17:00:35 +02:00.
`suivant` indique que toutes les pages sont relues, avec son rappel générique
de fiche/registre. La présente passe ne ferme aucune unité et ne modifie aucun
état. Les 31 chiffres restent une réserve globale ; aucun n'est repris dans le
candidat. La date de préparation du champ obligatoire `verifie` ne vaut pas
validation indépendante : `statut=brouillon`, sans `verifie_par`, partout.

Unités pertinentes déjà acceptées par l'usine :

| Unité | Pages PDF | Validation enregistrée | Sceau observé |
|---|---|---|---|
| 1 | 1-12 | Gemini 3.8 Flash, 06/09 à 16:18:02 +02:00 | `487737078fecf91d1124006a6ac1ed1d6311da880029fc9d85120a583f9392a6` |
| 2 | 13-24 | Gemini 3.8 Flash, 06/09 à 16:26:06 +02:00 | `cde4c80a0ce591add29e43ffe588135d5ec3050f8f96b69f1e173e3683636358` |

Cette passe consulte les sections du pivot p.8, 10, 11, 12, 13, 14, 15, 16 et
22. Elle examine visuellement les rendus existants `p-0008.png`, `p-0016.png`
et `p-0022.png` sous `sources/0a7537d478616271.figures/`. Elle ne prétend pas
avoir relu les 195 pages ni démontrer les règles juridiques évoquées p.14.

## Ce que les trois schémas montrent effectivement

| Page | Observation directe du rendu | Utilisation et limite |
|---|---|---|
| 8 | Axe vertical urgence/planification et axe horizontal agir seul/chercher du soutien/trouver un relais ; acteurs et difficultés positionnés | Sert à distinguer temporalité et besoin de soutien. Aucune position du dessin ne devient une compétence juridique, un seuil ou une procédure automatique. |
| 16 | Gouvernance au centre ; structure juridique, environnement, gestion comptable et financière, personnes concernées, bâti et équipement autour | Six axes d'intervention, découpage différent des quatre dimensions p.10. Les liens graphiques n'établissent pas une chaîne causale déterministe dans notre cas. Crédit du schéma : PUCA, Eva Simon. |
| 22 | Gestion/situation financière ; gouvernance/fonctionnement ; état du bâti, réseau et équipements ; situation socioéconomique des ménages ; environnement urbain ; caractéristiques structurelles | Six catégories de suivi. Les quatre dimensions d'entrée ne dispensent pas d'examiner structure et environnement. Ce n'est ni un score, ni une liste de conditions légales. |

Pas de reproduction du schéma dans le candidat : ses droits ne sont pas
établis par sa disponibilité publique. Aucune image de remplacement inventée.
Le raisonnement du dossier est textuel ; les formats photo/plan ne sont pas
revendiqués. Le valideur v2 exige encore un objet image pour `relier` et
`datation` : aucun objet factice n'est ajouté pour contourner cette exigence.

## Matrice des assertions et de leurs limites

Les repères A désignent des assertions paraphrasées du guide ; les repères P
désignent une transposition pédagogique. Une citation du guide sur une carte
étaye son principe, jamais la réalité du cas fictif ni chacune de ses
hypothèses particulières.

| Repère | Assertion ou choix | Preuve/page | Portée conservée |
|---|---|---|---|
| A1 | Gouvernance, finances, bâti et solvabilité/situation sociale doivent être distingués | Énumération p.10 | Quatre dimensions d'entrée, pas nomenclature exhaustive ou score. |
| A2 | Des facteurs extérieurs peuvent aggraver des dysfonctionnements | Texte p.10 | Pas de diagnostic par adresse, quartier ou âge du bâtiment. |
| A3 | Niveau socioéconomique, localisation et époque constructive ne suffisent pas à expliquer la difficulté | Développement p.12, en regard des symptômes p.11 | Aucune assimilation entre ménage modeste, mauvais payeur et copropriété en difficulté. |
| A4 | Différents problèmes peuvent concerner instances, technique, finances, social ou gestion | Exemples p.15 | Ces catégories n'établissent pas les causes particulières de nos soldes ou reports. Les qualifications de personnes du guide ne sont pas reprises. |
| A5 | Une difficulté sur un axe ne condamne pas la copropriété à un état général de difficulté | Texte p.16 + schéma consulté | Interdépendance sans fatalité ni garantie de réussite d'une intervention. |
| A6 | La grille de suivi ajoute structure et environnement aux catégories de fonctionnement, finances, bâti, ménages | Rendu et questions p.22 | Demander les informations adaptées au dossier ; aucun calcul de gravité. |
| A7 | Temporalité et type d'appui constituent deux questions distinctes | Rendu p.8 | Cadre d'orientation ; pas de séquence obligatoire ni d'attribution juridique de pouvoirs. |
| P1 | Le dossier possède un relevé incomplet, un report faute de pièces, une trace humide signalée, une baisse de ressources déclarée | Construction fictive explicite | Aucune copropriété réelle, aucun montant, aucune observation ou intention présentée comme terrain. |
| P2 | Solde inexpliqué : difficulté de paiement, contestation ou anomalie de compte sont des possibilités à départager | Transposition de A1/A4, pas liste fournie telle quelle par le guide | Aucun mécanisme n'est tenu pour démontré ; la pièce discriminante est exigée. |
| P3 | Distinguer ce qu'atteste une pièce et ce qu'on lui fait dire | Consigne de raisonnement de l'étude | Le procès-verbal confirme le report et le motif consigné ; il ne prouve pas toutes leurs causes. |
| P4 | Qualifier nature/urgence du désordre tout en examinant les autres dimensions | Proposition conditionnelle fondée sur A5/A7 | Aucun diagnostic technique, ordre de travaux, urgence supposée ou calendrier réglementaire. |
| P5 | Associer syndic, conseil, interlocuteur technique ou social aux demandes pertinentes | Transposition de A1/A6/A7 ; rôles de base prérequis | Pas de transfert de pouvoir au conseil, pas d'accès annoncé à une aide, pas de procédure décidée. |
| P6 | Conserver avis initial, pièce nouvelle, modification et inconnues restantes | Consigne pédagogique ; mécanismes déjà présents dans METHODE.md | Pas une obligation issue du guide ni une efficacité mesurée de ce module. |

## Matrice par carte

Les identifiants ci-dessous portent tous le préfixe `fragilite-`.

| Carte | Format | Pages et repères | Preuve d'apprentissage visée |
|---|---|---|---|
| dimensions | flash | 10, A1 | Expliquer pourquoi compte collectif et situation des personnes ne s'équivalent pas. |
| report-decision | QCM | 10/16, A1/A5/P1/P3 | Refuser une cause technique supposée et une exclusion absolue du problème de gouvernance. |
| soldes-hypotheses | libre | 10/15, A1/A4/P2 | Relier chaque hypothèse à une pièce capable de la démentir, pas seulement dresser une liste. |
| contre-stereotype | QCM | 12, A3 | Conserver l'inconnu sans faire du profil des habitants une explication. |
| priorite-conditionnelle | libre | 8/16, A5/A7/P4 | Distinguer démarches parallèles et priorité modifiée par un constat. |
| angles-manquants | libre | 10/16/22, A1/A5/A6 | Élargir les quatre dimensions sans confondre les trois représentations du guide. |
| conseil-partage | rôle | 10/15-16, A1/A4/A5/P3/P5 | Répondre au lien causal allégué et expliquer ce qui permettrait de le tester. |
| menage-inconnu | rôle | 10/12, A1/A3/P5 | Accueillir une déclaration sans décider d'une intention ni promettre un droit. |
| revision-avis | synthèse | 10/16/22, A1/A5/A6/P6 | Réviser séparément finances, technique, décision collective et situation des personnes. |

L'amorce combine P1-P4 ; la leçon développe A1-A7 et explicite les adaptations.
La synthèse finale est un cas fictif distinct : une visite limitée rassurante
ne clôt pas des soldes confirmés ou des pièces manquantes pour voter. Les
attendus évaluent la qualité du raisonnement écrit, pas une décision juridique
ou une compétence professionnelle certifiée.

## Compétences et arbre proposés, sans modification du programme

Identifiant du candidat : `satellite.droit.diagnostic-partage-fragilite`.
Rattachement proposé existant :
`droit.organes.administrateur-provisoire-et-procedure-d-alerte`.
Il prépare la qualification des faits en amont ; il **ne couvre pas** les
conditions des outils du juge annoncés par ce nœud. Niveau déclaré 3
(Praticien) : raisonnement appliqué approfondi, aucune acquisition de niveau
attribuée à un joueur.

| Clé existante | Relation proposée | Raison |
|---|---|---|
| droit.organes.le-syndicat-des-coproprietaires | Prérequis, niveau 1 | Distinguer le collectif des situations individuelles. |
| droit.organes.le-syndic-et-ses-missions | Prérequis, niveau 1 | Savoir à qui adresser les demandes de pièces et repérer les limites du gestionnaire. |
| droit.organes.le-conseil-syndical | Prérequis, niveau 1 | Préparer une discussion avec le conseil sans lui attribuer tous les pouvoirs. |
| comptabilite.budget.le-budget-previsionnel | Prérequis, niveau 2 | Comprendre le périmètre collectif des dépenses et des décisions financières. |
| comptabilite.impayes.le-plan-de-recouvrement | Pont, niveau 3 | Approfondissement après clarification des soldes et situations ; aucune stratégie de recouvrement n'est enseignée ici. |
| immobilier.local.les-fragilites-observees | Pont, niveau 3 | Approfondissement du repérage local ; aucune donnée territoriale ni radar du 49 n'est importé dans ce cas. |

Toutes ces clés ont été contrôlées dans `programme/copro.json`. Leur existence
ne démontre pas que leur chapitre est actuellement servi : une intégration
doit vérifier le chemin jouable et présenter les prérequis absents honnêtement.
Compétences visées, sans ajouter de clés au programme : qualifier un signal,
faire dialoguer les quatre dimensions, chercher une preuve contraire,
prioriser sous condition, partager puis réviser un avis.

## Relecture indépendante nécessaire

- Confronter chaque correction attendue aux pages précises et distinguer
  rigoureusement A1-A7 des adaptations P1-P6.
- Vérifier que les neuf exercices exigent des réponses suffisamment
  différentes ; les rôles doivent exercer l'explication et le recueil de
  besoins, sans promettre une conversation automatique.
- Éprouver la synthèse avec une réponse argumentée différente de la réponse
  proposée : aucune hypothèse alternative compatible avec le dossier ne doit
  être pénalisée pour son seul écart au libellé.
- Vérifier la priorité conditionnelle : qualifier une urgence potentielle
  sans en affirmer l'existence, sans rendre toute autre démarche dépendante
  de la fin de l'examen technique.
- Confirmer le rattachement à l'arbre et les prérequis réellement jouables ;
  le module ne remplace pas le cours sur les dispositifs judiciaires.
- Avant service : relecteur distinct et tampon, essai du parcours complet,
  sources ouvrables, reprise des réponses et de la grille, éventuels critères
  cochés et synthèse finale persistés. Aucun de ces essais d'usage n'est
  revendiqué dans cette préparation de contenu.

Le candidat n'a pas de score de certification, d'évaluation automatique du
raisonnement, de chiffre métier à appliquer, d'éligibilité à une aide ou de
procédure légale. L'ancien brouillon `coproprietes-fragiles.json` est inchangé.

## Contrôles exécutés

`CONTROLES.json` conserve l'empreinte du candidat et le résultat de
`app.valide_chapitres.valide_chapitre` appliqué explicitement au fichier de
travail avec les identifiants du programme courant : zéro erreur, neuf cartes,
cinq types, leçon de 4 492 caractères/681 mots, brouillon partout, aucune
relecture indépendante déclarée. Le scan utilise un parc vide : motifs
généraux contrôlés, aucune donnée client consultée.

Les commandes obligatoires ont ensuite été exécutées séquentiellement :

- `python3 app/tests.py` : 21 entrées vertes et une suite en échec,
  « serveur d'état ». Cette suite compte 43 tests en 2,622 s, avec une erreur
  `PermissionError: [Errno 1] Operation not permitted` sur `socket.bind`,
  ouverture du port local interdite par le bac à sable. Le résultat global
  n'est donc pas vert ; log dans `app-tests.log`.
- `python3 tooling/check.py` : « Académie : 0 erreur(s) », log dans
  `tooling-check.log`.

Le coordinateur a reçu ce résultat pour compléter, dans son contexte autorisé,
la seule preuve serveur manquante. Aucun contournement du bac à sable ni essai
d'usage du candidat n'a été effectué ici. Les compteurs du log global portent
sur le dépôt partagé au moment du contrôle, pas sur une promotion de ce
fichier resté sous `travail/`.

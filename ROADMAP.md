# Roadmap Académie, 05/09/2026

## Actualisation du 15/09 : plus de front (décision 0054)

Le client web est retiré et archivé (`archive/conception-2026-09-web/`),
son workflow supprimé. L'interface est désormais le dépôt discuté par un
agent ; le moteur reste le professeur et l'état reste un journal local,
hors git ([décision 0054](decisions/0054-plus-de-front-le-depot-est-l-interface.md)).
Nouveau chantier : `ACA-SANS-FRONT-1`, cahier
[chantiers/ACA-SANS-FRONT-1.md](chantiers/ACA-SANS-FRONT-1.md). Livré le
15/09 : surface `app/academie.py`, tests `app/tests_academie.py`, skill
`skills/academie/SKILL.md`, prompt `prompts/jouer.md` ; `tests.py`,
`check.py` et `--mutation` verts. Reste l'observation humaine : une
première séance réelle jouée et un QCM affiché. `ACA-SANS-FRONT-2` est
livré aussi : carnet d'erreurs (`erreur`, `erreurs`) et quiz de
positionnement (`quiz`) dans la surface, 16 tests verts et une mutation
du carnet détectée. `ACA-SANS-FRONT-3` ferme les aides de séance :
`prevue` (l'échéance selon la note) et `mini-lecons` (les cartes ratées
plusieurs fois), 19 tests verts et une mutation d'intervalle détectée.
`ACA-SANS-FRONT-4` met le journal de la surface au contrat `journal-v1`
(ouverture `seance`, réponses `revision` avec format et nonce) et expose
`rituel` : l'habitude devient mesurable et la synchronisation serveur
possible. 22 tests verts et deux mutations nouvelles.
`ACA-SANS-FRONT-5` et `ACA-SANS-FRONT-6` rendent la surface multi-cursus
et complète : `--cursus` isole copro et IFSI, `cursus <cle>` journalise
le choix, et la surface charge aussi les chapitres v2 (92 cartes, dont
34 IFSI restées invisibles jusqu'ici). 26 tests verts et deux mutations
nouvelles.
Les items
qui pointaient vers `ACA-FRONT-2` s'y raccrochent. La comparaison des
dépôts existants (apprendre en chat, répétition espacée) est faite dans
[travail/veille-2026-09-15-comparatif-depots.md](travail/veille-2026-09-15-comparatif-depots.md),
licences lues à la source.

## Actualisation du 06/09 : ambition expertise

La demande de JB ouvre `ACA-EXPERTISE-1` : [cahier](chantiers/ACA-EXPERTISE-1.md),
[cartographie et compteurs](travail/expertise-2026-09-06/COUVERTURE.md),
[fabrication reproductible](travail/expertise-2026-09-06/PROTOCOLE.md).
Passe du 06/09 : cinq approfondissements relus et jouables localement ;
[chemin depuis la demande et exemple électrique](travail/preuve-concrete-2026-09-06/LIVRAISON.md). Les cursus experts restent à construire.
Les dossiers avancés et l'exploitation intégrale des sources restent ouverts.
Ce chantier n'autorise ni publication ni envoi de documents internes.

Cap : une école de métier qui donne envie de revenir et rend capable de
comprendre, rappeler, expliquer et agir, y compris sans IA. L'arbre reste
vaste ; la prochaine livraison doit être petite et complète.

L'[audit](travail/audit-2026-09-05/AUDIT.md) fonde cet ordre. La
[revue scientifique](travail/audit-2026-09-05/SCIENCE.md) distingue résultats,
limites et propositions. `roadmap.json` contient les dépendances ; chaque
chantier a son cahier avant le code. Les anciens jalons restent historiques,
leurs chiffres ne sont pas des compteurs actuels.

## État local après la demande autonome

La décision 0036 autorise la fabrication maintenant. Les preuves de cette
livraison sont dans [LIVRAISON.md](travail/experience-2026-09-05/LIVRAISON.md).
L'audit initial reste daté ; ses compteurs décrivent l'avant.

- Deux parcours : AG (trois chapitres, 17 cartes) et IFSI sécurité et
  communication (deux chapitres, 10 cartes), avec relecture indépendante.
- 103 cartes publiées localement : 93 copro et 10 IFSI. Les 76 cartes v1
  sont conservées ; les cinq leçons v2 sont reliées au programme.
- Accueil orienté apprentissage, salle Étude, reprise, brouillons, deux
  thèmes, séparation des métiers et des réponses avec/sans aide.
- Journal : ordre UTC exact, émission locale ordonnée et acquittements
  contrôlés ; preuves de régression et contre-relecture dans la livraison.
- Les surinterprétations scientifiques ciblées sont corrigées et leurs
  limites documentées. Les références non recontrôlées restent nommées.
- 389 chapitres copro et 375 IFSI restent l'horizon éditorial. Cinq leçons
  jouables ne démontrent ni sa couverture, ni une formation validée.
- Publication distante, trajet physique téléphone/Mac, appréciation
  esthétique de JB, usage sur quatre semaines et transfert : non mesurés
  dans cette livraison. Aucun résultat humain reconstruit par un agent.
- Classes de modèles retirées des consignes actives et du code par le lot
  précédent, conservé avec ses contrôles de reprise et de provenance.

## Ordre de référence de l’audit, puis actualisation

Ordre : **préserver les réponses et la fiabilité**, rendre l'existant
utilisable, mesurer l'usage, démontrer un apprentissage, puis étendre.
À priorité égale, choisir le lot qui retire une dépendance avec le moins
de travail. Aucun score RICE artificiel faute de données d'usage/coût.

Les charges ci-dessous sont des enveloppes de planification, pas des mesures
ni des promesses de calendrier. Une unité termine un livrable vérifiable ;
le temps d'agent ne remplace pas les jours d'observation humaine. Les
`budget` JSON bornent une passe de travail, pas tout un chantier.

| Ordre | Chantiers et résultat concret | Preuve de sortie | Charge indicative |
|---|---|---|---|
| P0, maintenant | `ACA-JOURNAL-SYNC-1` : ordre temporel correct et acquittement serveur strict | Tests rouges puis verts sur offsets, fractions, égalités, reprise et réponses 200 invalides ; aucun événement désynchronisé silencieusement | 2 à 3 unités de code/revue |
| P0, en parallèle | `ACA-COPRO-1` : clôturer les relectures restantes ; `ACA-METHODE-2` : corriger les surinterprétations scientifiques | Table assertion/source/périmètre et avis indépendant ; chaque règle scientifique distingue preuve et choix produit | 1 unité copro, 2 unités méthode |
| P1 | `ACA-FRONT-2` : première séance évidente, départ novice adapté, mobile lisible, brouillon conservé, focus correct, tests web en CI | Revue rendue indépendante, vérifications téléphone/tablette/ordinateur, tests incluant les défauts observés ; appréciation visuelle JB encore distincte | 3 à 4 unités ciblées, sans refonte générale imposée |
| P1, après correctifs | `ACA-PUBLICATION-2` : rendre le client réellement accessible et synchronisé | SHA servi, HTTPS authentifié, téléphone hors-ligne puis Mac et trajet inverse, retour arrière documenté ; validation humaine de publication | 1 unité de préparation puis essai réel |
| P1, dès accès utilisable | `ACA-RITUAL-1` : sept séances d'acceptation incluses dans environ trente, puis bilan | Usage réel sur au moins quatre semaines, test différé, calibration et verbatim ; aucune séance de robot comptée | Temps humain, pas estimable en tokens |
| P2, contrat préparable avant le bilan | `ACA-PILOTE-CONTRAT-1` puis `ACA-ETUDE-1` : une séquence AG cohérente sur trois chapitres | Contrat du pilote, sources et relecture vérifiables, tentative/aides/explication/cas inédit/rappel ; jeu pilote après bilan du rituel | 1 à 2 unités contrat, 3 à 5 unités éditoriales et produit |
| P2, après le pilote | `ACA-TRANSFERT-1` : montrer ce qui reste et ce qui se transfère | Cas parallèles sans IA et avec outils, mesures différées distinctes des points et de FSRS ; décision documentée | Préparation 1 à 2 unités, observations différées |
| P3, sur preuve | `ACA-CONTRAT-2`, `ACA-CONTENT-2`, étude/cas IFSI, réponses libres, boîte et extensions | Migration entière sans provenance inventée ; lots plafonnés par le coût et le besoin observés ; aucune promesse de formation clinique validée par des cartes | Recalibrer avec le premier pilote |

La fabrication locale anticipée est autorisée par 0036 ; son observation
humaine reste distincte. Les cases de la table ci-dessus décrivent les
preuves attendues, pas une absence de code. Aucune nouvelle mécanique
n'entre dans un lot déjà mesuré en cours de rituel. Un défaut bloquant se corrige, sa version et
la rupture éventuelle de mesure se consignent.

## Le premier parcours qui doit donner envie d'apprendre

**AG : préparer une décision, la défendre, puis la mettre en œuvre.**
Trois chapitres rapprochés, issus du programme existant, plutôt qu'une
carte solitaire suivie de sujets sans lien. La sélection livrée est : syndic et missions, article 24, préparation
du procès-verbal. Le chapitre PV ne couvre pas encore toutes les
modalités de notification annoncées par le programme.

1. Comprendre les acteurs, pouvoirs, documents et informations manquantes.
2. Qualifier une décision, expliquer son raisonnement et comparer un cas
   proche où la conclusion change.
3. Produire une courte note de décision, repérer une limite de mandat et
   répondre à la pression d'un interlocuteur avec des options explicites.

Le pilote exerce les fondations aussi bien que le terrain : définir un
principe, le rappeler, l'expliquer simplement, l'utiliser. Il distingue
ce qui est sûr, ce qui dépend du contexte, ce qui exige une vérification
et ce qui appelle une aide professionnelle. Aucun exemple de cette page
ne constitue une réponse juridique validée.

Après ce pilote : dégât des eaux pour varier les situations, puis systèmes
du bâtiment (dont VMC) et sécurité/mandat selon le besoin constaté. IFSI :
premier lot transversal diabète, traitement, calcul, alerte, communication
et domicile, sur sources adaptées au niveau. Les gestes et la compétence
clinique demandent une observation supervisée distincte de l'application.

La migration globale reste prévue dans `ACA-CONTRAT-2`, avec les
assignations de 0030. Elle n'est plus le prérequis des trois premiers
chapitres : le générateur accepte déjà v1 et v2 ensemble. Le petit contrat
pilote doit prouver cette coexistence sans doublons, sans fausse étiquette
v2 globale et sans réécrire le journal. Décision de séquencement : 0035.

## Ce qu'on mesure

| Dimension | Mesure utile | Ce qu'elle ne prouve pas |
|---|---|---|
| Usage | Retours, séances interrompues, temps disponible, envie de reprendre | Acquisition d'un métier |
| Mémoire | Rappel différé, sans corrigé, des connaissances cibles | Traitement d'un cas nouveau |
| Compréhension | Explication causale, contre-exemple, analogie et sa limite | Exécution correcte sur le terrain |
| Transfert | Cas inédit et production avec grille annoncée | Généralisation à tout le métier |
| Jugement | Informations demandées, risques reconnus, options et justification, confiance avant retour | Autorisation juridique ou clinique donnée par l'IA |
| Assistance | Même objectif avec outils et sources, temps et vérifications observés | Connaissance disponible sans téléphone |
| Fabrication | Temps réel, corrections factuelles, relecture humaine et coût par chapitre | Capacité illimitée de production |

Le test à froid de vingt cartes prévu pour le rituel reste un premier
signal. `ACA-TRANSFERT-1` ajoute un protocole borné au pilote ; ni vingt
cartes ni un joueur ne constituent un essai causal sur l'efficacité générale.

## IA, groupe et horizon

Faire progresser le professeur IA par capacités observées : fabriquer une
séquence sourcée, proposer des indices, discuter une justification, jouer
un interlocuteur, puis adapter le parcours sur des résultats différés.
Le même modèle peut écrire et effectuer une passe indépendante dans une
autre session ; changer son nom ne prouve aucune indépendance.

`ACA-RESPONSE-1` porte l'expérience bornée de correction. `ACA-TUTEUR-1`
concerne le rôle social consenti ; le professeur IA adaptatif reste à
cadrer après les résultats de l'expérience de correction. Celle-ci
n'attend pas les cercles. L'architecture sans appel LLM serveur reste
en vigueur ; une première expérimentation peut utiliser l'abonnement local.

Un binôme peut discuter un cas après réponse individuelle, puis chacun
résoudre une variante seul. Cette expérience consentie n'exige pas encore
un réseau social. Les cercles et la ligue restent après le rituel et les
décisions de comptes. Pas de classement imposé ni de reporting hiérarchique.

Conserver Python, SQLite, journal append-only, client PWA et données par
métier. Différer nouvelle infrastructure, catalogue massif, médias coûteux,
optimisation FSRS sans historique suffisant et automatisation large de la
publication. L'effort va d'abord à une expérience de bout en bout.

## Prochaine reprise

Lire `chantiers/ACA-JOURNAL-SYNC-1.md`, écrire les régressions manquantes,
corriger et faire relire. `tooling/roadmap.py next` ne choisit que les
items automatisables sans revue ; son absence de résultat ne signifie
pas qu'il n'y a aucun travail. Les P0 avec revue se prennent explicitement
depuis cette page et leur cahier.

## Sortie de cette livraison

ACA-JOURNAL-SYNC-1, ACA-COPRO-1, ACA-METHODE-2, ACA-FRONT-2,
ACA-PILOTE-CONTRAT-1 et ACA-EXPERIENCE-1 sont clos à leur périmètre local.
La livraison porte les preuves exactes et leurs limites. La prochaine
preuve à obtenir est l'accès publié et la synchronisation physique
(ACA-PUBLICATION-2), puis les observations réelles du rituel et du pilote.
ACA-ETUDE-1 reste ouvert pour son étude humaine observée ; sa fabrication
locale anticipée est désormais disponible. Rien n'est bloqué sur une
question de design ou de contenu adressée à JB dans cette passe.

## Essai comptes préparé le 05/09

ACA-ONBOARDING-1 est intégré sur main pour l’essai autorisé (0042, 0043) :
mail/mot de passe, pseudo, cursus unique, sauvegardes par compte et annuaire
minimal masquable. [Preuves et limites](travail/onboarding/LIVRAISON.md).
Publication VPS constatée le soir (code 6c9c6bc) ; [contrôles et limites](travail/onboarding/PUBLICATION-VPS.md). Le parcours joueur public, le trajet physique et dix heures humaines par cursus restent à constater.

## Accès local à préparer

ACA-ACCES-LOCAL-1 remplace l'accès par mail par un pseudo unique, une
phrase secrète et une clé de récupération à conserver localement. La clé
est affichée une seule fois. Sans phrase ni clé, il n'y a aucune
récupération. Les comptes d'essai actuels ne seront effacés du VPS
qu'après publication contrôlée et commande locale confirmée.
Le stock est de trois études copro et deux IFSI ; les programmes ne sont
pas des cours déjà fabriqués. [Prompt PDF et préparation de l’essai](prompts/essai-10h-et-pdf.md).

## Base écrite du programme copro

`ACA-COURS-COPRO-1` : [cours bruts](cours/copro/README.md),
[index](cours/copro/INDEX.md) et [compléments demandés par JB](cours/copro/complements/COUVERTURE-JB.md).
La rédaction couvre les identifiants du programme avec cas, transferts et sources
qualifiées. Le [rapport](travail/cours-copro-2026-09-06/LIVRAISON.md) distingue
présence des textes, contrôles et examen de fond borné. Les brouillons ne sont
pas automatiquement servis comme études.

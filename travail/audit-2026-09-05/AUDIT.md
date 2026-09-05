# Audit Académie, fond, forme et roadmap

Date : 05/09/2026. Outil : Codex. Modèle : GPT-6 Astra, provenance de
l'exécution, sans catégorie de capacité. Dépôt audité après synchronisation :
`main`, `3ecbc77`, dernier commit du 04/09 à 18:36:54, heure de Paris.
Le dépôt était propre ; `git pull --ff-only` n'a apporté aucun changement.

## Verdict

**Académie a une architecture exploitable et une ambition pédagogique
documentée ; elle n'a pas encore démontré une école de métier jouable.**
L'écart principal est entre ce que les documents promettent et ce qu'un
débutant peut effectivement apprendre, pratiquer et retenir aujourd'hui.

Le meilleur investissement est une boucle complète : première séance
compréhensible, connaissance fiable, cas concret, explication personnelle,
retour utile, reprise et vérification différée. Augmenter le catalogue avant
cette preuve accroîtrait surtout la charge éditoriale et l'attente du joueur.

Les choix de JB sont pris au sérieux : comprendre sans téléphone, relier
des idées, exercer un jugement pragmatique, aimer revenir, apprendre tout
au long du métier, utiliser l'IA sans lui céder toute la connaissance. Le
produit doit mesurer ces capacités séparément. Les points et la stabilité
FSRS ne suffisent pas à les représenter.

La [roadmap active](../../ROADMAP.md) et `../../roadmap.json` ont été
réordonnées. Cet audit n'a pas refait l'interface, promu de carte, publié
sur le VPS ni importé de contenu de Labor. Le seul changement de code
fonctionnel effectué ici est la suppression des classes de modèles,
explicitement demandée ensuite par JB.

## Méthode et limites

Trois couches examinées : ce qui est décidé, ce qui est implémenté, ce qui
a été observé. Une réussite dans une couche ne clôt pas les autres.

- Doctrine, README, méthode, cadrage scientifique, architecture, programme,
  roadmap, cahiers et décisions pertinentes lus ; code et tests des chemins
  sensibles examinés.
- Rapports d'hier retrouvés avec leurs originaux : IFSI, copro et stratégie,
  organisés dans [le dossier existant](../rapports-chatgpt-pro/README.md).
  Les variantes copro A/B ne sont pas deux validations indépendantes.
- Cinq pièces jointes lues ; identité et empreinte dans [pieces.json](pieces.json).
  Ce sont des orientations, pas des sources scientifiques de même force.
- Inventaire des données et échantillonnage ciblé des contenus ; il ne s'agit
  pas d'une contre-expertise métier exhaustive des 764 chapitres de programme.
- Recherche bibliographique ciblée sur onze publications, en privilégiant
  revues, méta-analyses et essais ; profondeur de consultation et accès
  manquants indiqués dans [SCIENCE.md](SCIENCE.md). Ce n'est pas une revue
  systématique exhaustive arrêtée en septembre 2026.
- Interface construite localement, inspectée à 375 et 1280 px, thèmes
  Papier/Nuit ; deux critiques indépendantes selon Impeccable, dont une
  avant toute lecture du détecteur. Tests existants relancés.
- Aucune nouvelle inspection du VPS ni observation de JB apprenant. Les
  indications de déploiement sont celles du rapport daté du 04/09.

Les screenshots montrent un profil local d'essai. Une ouverture de séance
a été créée localement pendant l'inspection ; aucune réponse ni note n'a
été jouée par un agent pour produire une prétendue preuve d'apprentissage.

## 1. État réel du produit

| Couche | Vérifié ici | Limite déterminante |
|---|---|---|
| Programme copro | 389 chapitres, 81 branches, 11 domaines, 398 liens de prérequis | Cadrage éditorial ; pas 389 leçons |
| Programme IFSI | 375 chapitres, 58 branches, 11 domaines, 600 capacités de cadrage | Aucune carte IFSI jouable |
| Banque v1 | 84 cartes : 76 valides, 4 signalées, 4 brouillons | 76 servables au build local, pas preuve de service distant |
| Formats servables | 41 flash, 27 QCM, 2 rôle, 2 libre, 4 autres visuels | 68/76 sont flash ou QCM ; les cas longs restent marginaux |
| Chapitres et provenance | Aucune des 76 cartes servables n'a de rattachement chapitre ni de provenance structurée v2 | Des sources existent ; source et tampon de fabrication ne sont pas la même chose |
| Pilotes v2 | Deux chapitres, onze cartes, tous brouillons | Pas encore de séquence Étude publiée |
| Moteur | Python de référence, FSRS, progression et miroir TypeScript testés | Deux implémentations peuvent partager le même défaut |
| État | Journal append-only, SQLite, file locale et synchronisation | Ordre temporel et réponse serveur invalide à corriger |
| Apprentissage | Outils de mesure du rituel présents | Rétention autonome et transfert réels non mesurés |
| Fabrication | Usine de documents avec unités, reprise et contrôles | Coût réel d'un chapitre pédagogique complet non établi |

Chiffres reproductibles et empreintes : [inventaire.json](inventaire.json).
Dans ce fichier, `capacites_cadrage: 0` pour copro compte l'absence de la
liste fine `objectifs`, pas une absence de compétences : les chapitres
ont bien un champ de compétence. Ne pas tirer une conclusion abusive du
seul nom d'une clé.

## 2. Fond pédagogique : préserver l'ambition, préciser les preuves

### Ce qui est bien fondé

Séances fractionnables, rappel actif, révisions espacées, sources visibles,
refus de servir une carte périmée, place du diagnostic et de la synthèse,
absence de honte après interruption : cet ensemble donne une base cohérente.
L'autonomie des dépôts et la séparation Labor/Académie protègent aussi la
différence entre apprendre un principe et recopier un dossier professionnel.

La méthode est déjà documentée. Son défaut n'est pas l'absence de science :
plusieurs conclusions ont été transformées en prescriptions plus absolues
que les travaux cités. La table complète des corrections se trouve dans
[SCIENCE.md](SCIENCE.md), avec les publications et leurs limites.

### Ce qui doit évoluer

| Besoin de JB | Entraînement à viser | Preuve attendue |
|---|---|---|
| Savoir sans chercher immédiatement | Acquisition guidée puis rappel libre et espacement | Réponse correcte différée, sans aide |
| Croiser les connaissances | Mécanisme causal, comparaison, analogie et contre-exemple | Expliquer pourquoi le parallèle fonctionne et où il échoue |
| Comprendre la VMC | Système, circulation, indices, causes concurrentes | Schéma expliqué et diagnostic sur une situation nouvelle |
| Arbitrer en AG ou avec le CS | Documents, acteurs, règles applicables, marges et limites | Note de décision argumentée, informations manquantes et options |
| Être pragmatique | Cas incomplet, contrainte de temps, désaccord, réponse proportionnée | Distinguer ce qui se sait, se vérifie et se décide |
| Utiliser l'IA efficacement | Vérifier une réponse et ses sources, comparer des hypothèses | Production assistée fiable, mesurée séparément du savoir autonome |
| Continuer à apprendre | Socle utile, exploration et nouveaux cas reliés | Retour choisi et progrès local documenté, sans diplôme fictif |

Ces situations sont des spécifications de futurs exercices. L'audit ne
donne pas une réponse juridique sur l'enregistrement d'une AG ou une
autorisation d'agir hors mandat ; les sources exactes, contexte et date
doivent être établis dans les cartes concernées.

Il faut articuler savoir et action. Une collection de microfaits n'apprend
pas à conduire un dossier ; des cas sans bases poussent le novice à deviner.
La boucle proposée est : **situation, tentative, principe explicatif,
exemple contrasté, exercice, explication personnelle, cas inédit, rappel
différé**. Donner un indice ou un exemple résolu lorsque les prérequis
manquent ; retirer progressivement l'aide. Cette proposition ne modifie
pas silencieusement les invariants de DOCTRINE.

La difficulté utile n'est pas la douleur. La méta-analyse de Shields et al.
distingue plusieurs effets du stress selon le moment et le processus
mémoriel. On peut se souvenir vivement d'une erreur sans avoir appris à
résoudre la suivante. Une simulation tendue demande préparation et débriefing ;
l'humiliation ou la surcharge ne sont pas des objectifs pédagogiques.
[Source primaire](https://researchworks.laverne.edu/esploro/outputs/journalArticle/The-effects-of-acute-stress-on/991004113765106311).

Le jeu peut soutenir l'apprentissage, avec des résultats variables selon
les dispositifs. Le plaisir à viser ici est aussi celui de comprendre,
réussir une mission et percevoir une compétence nouvelle. Ni supprimer
toute récompense au nom d'une loi universelle, ni copier les ligues de
Duolingo sans tester leur effet.
[Méta-analyse Sailer et Homner](https://link.springer.com/article/10.1007/s10648-019-09498-w).

**Temps proposé :** garder les quinze minutes déjà décidées comme point de
départ adaptable, et réserver un créneau plus long aux cas, calculs,
documents et productions. Il n'existe pas dans les sources examinées un
ratio universel théorie/terrain ou une dose quotidienne optimale applicable
à ces métiers. Mesurer temps disponible, effort, rappel différé et abandon ;
ne pas interpréter le temps passé comme une compétence.

**Groupe :** réponse individuelle, discussion à deux, puis variante
individuelle. Cela éprouve l'explication et la confrontation des modèles
mentaux avant de construire une infrastructure de cercle.
[L'expérience de Smith et al.](https://doi.org/10.1126/science.1165919)
porte sur un dispositif précis ; elle ne valide pas n'importe quel chat social.

## 3. Les deux cursus

### Copro : une carte large, une entrée trop diffuse

Les corrections du 04/09 ne doivent pas être refaites : 389 chapitres
conservés, objectifs ciblés précisés, cinq cartes v1 AG contre-lues, quatre
cartes IRSI/CIDRE signalées, chapitre article 24 v2 encore brouillon.
Le [rapport de révision](../2026-09-04-revision-copro.md) sépare ces états.

Le programme vise 2 990 cartes et 23 085 minutes d'étude ; le socle seul
compte 333 chapitres et 18 645 minutes. Ce sont des estimations éditoriales,
pas une mesure de charge ni une promesse de niveau BAC+5. Le socle pondère
la séance, il n'interdit pas actuellement l'exploration.

398 prérequis pour sept ponts déclarés : le graphe exprime davantage une
progression qu'un travail explicite de mise en relation. Ce ratio ne prouve
pas l'absence de liens implicites ; il invite à concevoir les contrastes
et transferts dans le premier parcours, sans ajouter des arêtes décoratives.

Recommandation : conserver le catalogue, sélectionner un noyau d'entrée
et relier trois chapitres AG en une mission complète. Ajouter ensuite
dégât des eaux, VMC et sécurité/mandat selon l'usage. Tester lecture d'un
document, calcul utile, formulation écrite et explication orale ; ne pas
réduire le métier à la reconnaissance de majorités.

Le référentiel du BTS Professions immobilières a été consulté comme point
de comparaison des activités, pas comme certification du programme maison.
[Texte officiel](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000048530487).

### IFSI : la correction de cadrage existe, la formation reste à produire

La révision du 04/09 a déjà distingué le référentiel 2026 et l'historique,
les voies d'entrée, les étapes, la difficulté et la criticité. Elle conserve
310 identifiants anciens et ajoute 65 chapitres ; les 600 capacités remplacent
un inventaire gonflé par des objectifs génériques. Les anciennes données
2009 sont préservées. Ce progrès est réel, limité au cadrage.

L'article 60 consulté confirme la distinction de rentrée entre nouvelles
dispositions et cursus antérieurs ; toutes les correspondances détaillées
aux annexes n'ont pas été réauditées ici.
[Texte officiel](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570487).

Les 375 chapitres sont encore à écrire. Les niveaux historiques I à V ne
constituent ni une qualification ni une échelle de sécurité clinique.
Priorité pédagogique : un petit parcours transversal diabète, médicaments,
calcul, alerte, communication, retour à domicile, avec difficulté adaptée
au public. Séparer connaissances, raisonnement clinique sur cas, geste
observé et pratique supervisée. Les deux dernières preuves ne peuvent pas
être remplacées par un QCM ou une note de tuteur IA.

## 4. Forme : une identité existe, l'entrée dans l'apprentissage reste difficile

La direction adulte tient : typographies, thèmes Papier/Nuit, surface calme,
arbre stable, question centrale, sources accessibles et états vides honnêtes.
Il n'est pas nécessaire de jeter cette direction pour produire un meilleur
résultat. L'acceptation esthétique par JB reste ouverte.

| Observation locale | Conséquence | Priorité et destination |
|---|---|---|
| En droit, 60 chapitres « À écrire » avant la section des 26 cartes disponibles | Le novice parcourt d'abord ce qu'il ne peut pas apprendre | P1, ACA-FRONT-2 : accès immédiat au jouable, programme à explorer séparément |
| Sur le profil vierge et la graine observés, première séance réduite à un schéma de procédure de niveau III | Les premiers gestes n'expliquent pas comment entrer dans le métier | P1, départ novice à éprouver ; ne pas extrapoler cette séance à toutes les graines |
| À 375 px, schéma d'environ 295 × 113 px ; correction très longue, actions éloignées | Lecture et comparaison coûteuses au téléphone | P1, consultation agrandie, hiérarchie et commandes accessibles |
| Dix pictogrammes de domaines sans libellé visible sur mobile | Leur nom accessible existe, mais le novice voyant doit deviner | P1, libellés et orientation |
| Brouillon saisi dans Boîte, navigation Profil puis retour : texte vide | Une intention d'apprendre se perd | P1, conservation locale et abandon explicite |
| Échap ferme le dialogue mais laisse le focus sur BODY ; navigation sans focus sur le contenu nouveau | Le clavier perd le fil | P2, restitution et déplacement de focus |
| Profil orienté activité/points ; résultat QCM et autoévaluation peu distingués | L'effort et la confiance risquent d'être confondus avec la compétence | P2, états et limites explicites, sans inventer de KPI |

Captures conservées : [arbre ordinateur](preuves/arbre-1280.png),
[arbre mobile](preuves/arbre-375.png), [séance mobile](preuves/seance-375.png).

Deux inspections indépendantes concordent sur l'écart entre catalogue et
jeu. Le détecteur automatique ne trouve rien ; cela n'invalide pas les
défauts observés. Aucun débordement horizontal global constaté aux deux
largeurs. VoiceOver, zoom 200 %, tablette et vraie utilisation mobile
restent à vérifier ; cet audit n'est pas une certification WCAG.

## 5. Architecture, intégrité et IA

### Constats techniques reproductibles

| ID | Preuve et chemin | Effet | Suite |
|---|---|---|---|
| T1, P0 | `app/seance.py:60`, `web/src/moteur/etats.ts:48` et autres lecteurs trient les dates comme du texte. À la fin de l'heure d'été, notes réelles [4,1], ordre lu [1,4] | Dernière note et calcul FSRS changent ; parité des deux moteurs insuffisante | ACA-JOURNAL-SYNC-1 réouvert, tous lecteurs, égalités et fractions inclus |
| T2, P0 | Vraies fonctions TS avec transport HTTP 200 `{}` : [preuve](preuves/api-200-vide.json). `web/src/donnees/api.ts` caste le corps ; `web/src/moteur/journal.ts` retire les éléments du lot | Journal local conservé, mais file d'envoi vidée sans preuve de réception ; reprise compromise | Valider schéma et cohérence de l'acquittement avant retrait |
| T3, P1 | Une copie en mémoire de carte brouillon passée à `valide`, avec même auteur/session dans `verifie_par`, donne zéro erreur : [preuve](preuves/relecture-meme-session.json). `app/valide_chapitres.py:239` vérifie surtout la présence | La double passe promise n'est pas opposable comme indépendance ; aucune carte réelle modifiée par ce test | ACA-PILOTE-CONTRAT-1, attestation structurée et audit des assertions |
| T4, P1 | `.github/workflows/check.yml` exécute les contrôles Python sans les suites client/build/E2E | La CI ne protège pas toute la surface actuellement construite | Extension bornée de ACA-FRONT-2 |
| T5, P1 | Rapport VPS du 04/09 : Caddy ne traverse pas le chemin de publication | Build transféré ne signifie pas interface utilisable ; état distant actuel non vérifié | ACA-PUBLICATION-2, préparation limitée puis autorisation de publication |

La reproduction T2 utilise les modules applicatifs transpillés, un stockage
de test et un transport simulé ; elle ne prétend pas montrer que le vrai
serveur produit actuellement ce corps. C'est une vulnérabilité du contrat
de reprise à un succès mal formé, pas une perte totale du journal local.

T3 ne démontre pas qu'une fausse carte est actuellement servie. Il démontre
que le valideur accepte une attestation qui ne satisfait pas la promesse
d'indépendance. Même un meilleur schéma ne prouvera pas automatiquement que
la source implique chaque assertion. Une note A/B/C doit rester un état
documentaire, jamais une probabilité de vérité inventée.

### Architecture à conserver

Python de référence, SQLite, synchronisation par union, PWA et séparation
des données par métier suffisent à poursuivre. Aucun besoin démontré d'un
graphe serveur, d'une nouvelle base, d'une ferme d'agents ou de microservices.
FSRS reste un calendrier de mémoire d'items ; les compétences demandent
des observations supplémentaires.

Une correction de sens doit garder la trace du contenu appris et de la
version évaluée. Les identifiants et le journal historique se préservent ;
la compétence n'est pas automatiquement reconduite parce que l'ID survit.
Spécifier ce contrat avant de fabriquer beaucoup de contenu.

### Professeurs hybrides puis IA

L'ambition est crédible comme direction d'expérimentation. L'essai de Kestin
et al. montre des résultats encourageants pour un tuteur IA soigneusement
conçu sur deux leçons de physique ; il ne démontre pas le remplacement de
toute formation ni la rétention professionnelle à long terme.
[Publication](https://www.nature.com/articles/s41598-025-97652-6).

Progression proposée : séquence sourcée, indices gradués, analyse d'une
justification, simulation d'interlocuteur, adaptation fondée sur résultats
différés. Évaluer le professeur sur la réussite ultérieure de l'élève sans
aide, la qualité de ses corrections et ses abstentions pertinentes.

La correction libre bornée peut être essayée avec l'abonnement local
existant. L'intégration produit et sociale vient ensuite ; pas de nouvelle
facturation ou d'appels serveur imposés par cet audit. Un humain apporte
au besoin une observation du terrain, une contradiction ou la validation
d'un geste ; son nom dans un champ ne suffit pas non plus comme preuve.

## 6. Agents et fabrication : suppression des classes effectuée

La demande explicite de JB a conduit à `ACA-MODELES-2` et la décision 0034.

- Retrait des tableaux et règles petit/moyen/grand dans les consignes actives.
  Nom du modèle et outil conservés uniquement comme provenance.
- Suppression de la classification par motifs de noms dans l'usine.
  Taille initiale et plafond communs à tous, adaptation selon les contrôles.
- Anciennes configurations et états reprenables ; unités ouvertes et sceaux
  préservés. L'ancien argument CLI `--classe` est seulement toléré et ignoré,
  masqué de l'aide, afin de ne pas casser les commandes historiques.
- Contrôle de cohérence de la configuration réellement raccordé à
  `tooling/check.py`, qui ne l'appelait auparavant pas.
- Tests rouges avant code, puis verts ; revue indépendante ayant détecté
  une incompatibilité des anciennes configurations, corrigée et retestée.
  Le doublement au-delà de l'ancien plafond a été reproduit indépendamment.

Les unités de document sont un mécanisme de reprise et de contrôle, pas
une façon de limiter un audit au nom de la capacité supposée du modèle.
Elles ne garantissent pas la compréhension sémantique d'un document.
Les anciens textes de décisions restent historiques et explicitement
amendés ; ils ne constituent plus la politique active.

## 7. Ordre de livraison et critères d'arrêt

La [roadmap](../../ROADMAP.md) détaille les lots, dépendances, preuves et
enveloppes de travail. Les changements structurants sont tracés en 0035.

1. Corriger le journal ; terminer les relectures copro ; corriger les
   surinterprétations de méthode.
2. Rendre l'entrée et la séance mobile utilisables ; prouver le service
   authentifié et la synchronisation entre vrais appareils.
3. Observer le rituel sur l'existant stable. Les sept séances d'acceptation
   font partie des trente, elles ne s'y ajoutent pas.
4. Préparer le contrat pendant le rituel, puis fabriquer et jouer les trois
   chapitres AG après le bilan, avec protocole et mesure initiale avant étude. La migration des 84 cartes et la fabrication des 54 chapitres
   manquants du candidat ne doivent pas bloquer ce premier essai borné.
5. Mesurer rappel et transfert avec cas comparables et délai ; étendre si les
   résultats et le coût le justifient. L'IFSI reste un second pilote métier,
   avec sa propre validation.
6. Étendre tuteur, groupe, contenus et médias selon les besoins observés.

Décisions de poursuite : si personne ne revient, corriger l'expérience ;
si l'on revient sans progrès différé, corriger l'entraînement ; si le rappel
progresse sans les cas, travailler guidage, contrastes et productions ; si
la relecture coûte trop, réduire le lot. Aucun faux seuil statistique ne
remplace ces observations sur un très petit effectif.

## 8. Vérifications et ce qui reste ouvert

Les [preuves de vérification](VERIFICATIONS.md) séparent suites existantes,
reproductions adverses, revue du changement et observations humaines.

Les défauts T1/T2/T3 sont documentés et planifiés, **pas corrigés par cet
audit**. Les changements de pédagogie sont des cahiers, pas des mécaniques
déjà implémentées. La validité de chaque contenu juridique/clinique, la
publication réelle, l'acceptation visuelle JB et le bénéfice d'apprentissage
restent des preuves distinctes à obtenir.

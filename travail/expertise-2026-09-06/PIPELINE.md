# Du document au cours : contrat de fabrication et de contrôle

06/09/2026 — Codex / GPT-6. Demande de JB : coût contenu, pipeline ouvert,
reprise par d'autres agents, tests et vérifications aléatoires.
Décision : `decisions/0047-pipeline-documentaire-econome-et-auditable.md`.
Complément visuel : décision 0048 et `VISUELS.md`. L'extraction doit livrer
les supports, leurs légendes et les données d'exercice, pas seulement du texte.

## Ce qui est acté, ce qui existe, ce qui manque

**Acté :** extraction locale d'abord ; escalade par page ou passage ; source
originale conservée ; vérification des faits séparée de la fidélité ; cours
construits à partir de compétences observables ; correction propre à chaque
exercice ; audit indépendant et sondages reproductibles.

**Disponible :** usine par unités, pivots par page, sceaux de contrôle,
registre, formats de chapitre, tests produit. Le banc `benchmark_pdf.py`
compare des extracteurs ; il ne remplace pas l'usine. Il n'appelle aucune API.

**Non automatisé :** routage par page, OCR des pages mixtes, arbitrage entre
extracteurs, contrôles de relations dans toutes les tables, registre des
assertions, blocage automatique des descendants d'une assertion rétractée.
Les contrats ci-dessous s'exécutent donc manuellement avec des preuves
explicites, sans inventer un état logiciel qui n'existe pas.

**Non livré par ce protocole :** les cours experts de toutes les spécialités,
les supports de tous les formats visuels, un correcteur sémantique IA. Un
scénario de rôle et sa correction prédéfinie ne sont pas une IA qui comprend
la réponse. Les coûts de lecture de cette conversation restent non mesurés.

## Ordre de travail et portes de sortie

| Étape | Pourquoi cet ordre | Sortie minimale | Condition de passage |
|---|---|---|---|
| 0. Objectif | Éviter de convertir des bibliothèques sans usage | compétence, production attendue, prérequis, spécialité | objectif observable, pas « connaître tout » |
| 1. Réception | Conserver une preuve et les droits avant transformation | original, SHA-256 complet, titre/éditeur/date, droits, périmètre | document autorisé ; pas de donnée client |
| 2. Diagnostic | Un PDF peut mélanger texte, scans et figures | carte des pages et risques, nombre de pages, extraction native témoin | pages manquantes/inconnues visibles |
| 3. Extraction graduée | Réserver le travail cher aux échecs | textes bruts par moteur, versions/options, durée, rendus | aucune écriture sur l'original ; couverture physique explicite |
| 4. Pivot contrôlé | Ne pas apprendre à partir d'une extraction fausse | Markdown par page, tables, figures, anomalies | unité acceptée par usine **et** réserves consignées |
| 5. Instruction des faits | Un texte fidèlement copié peut être faux ou périmé | assertions reliées aux passages, portée, date, contradictions | sources retrouvées ; faits critiques corroborés ou exclus |
| 6. Conception pédagogique | Le cours sert une épreuve, pas le plan du PDF | grille, cas, leçon, exemples, exercices, transfert | toutes les attentes ont une explication et une preuve |
| 7. Relecture | L'auteur ne s'auto-certifie pas | retour aux pages par un autre agent, corrections et réserves | aucune erreur critique ouverte dans le contenu proposé |
| 8. Intégration locale | Un texte écrit n'est pas un module jouable | chapitre/carte au format réel, données visuelles propres, tests | rendu et interactions contrôlés sur les routes concernées |
| 9. Publication | Séparer fabrication et diffusion | autorisation, paquet/version, retour arrière, essai authentifié | validation humaine ; état joueur préservé |
| 10. Apprentissage | Séparer disponibilité et compétence | tentative sans aide, correction, nouveau cas, rappel différé | progrès observé, jamais diplôme ou habilitation déduit |

Pas de saut de 3 à 8. Une citation de NotebookLM sert à retrouver une source,
pas à valider une assertion. Une donnée absente reste absente.

## Réception et diagnostic page par page

Utiliser `preparer` pour conserver les originaux et retrouver les doublons.
Deux éditions différentes ne se fusionnent pas. Conserver à la fois la page
physique du fichier (base 1) et, si elle existe, la pagination imprimée.
Un titre dans le carnet ne prouve ni téléchargement ni lecture intégrale.

Sur chaque page : quantité et emplacement du texte natif, images, tableaux,
colonnes, rotation, équations, chiffres/unités, notes et légendes. Une page
avec seulement un pied de page natif n'est pas une page textuelle complète.
Les rendus sont la référence pour le **visible**, pas l'ordre interne du PDF.

Défauts observés dans les documents de JB :

- Angers p. 1 : cartouche scanné absent de l'extraction native ;
- Angers p. 9 et 12 : contenu masqué et mélange des colonnes ;
- PDHH p. 6 : arrêté scanné dans une page qui possède déjà du texte natif ;
- Focus p. 26 : chiffres de la discussion et du tableau contradictoires ;
- Focus p. 32 : texte d'un autre document masqué derrière le pied de page.

Le moteur actuel marque `ocr_requis` au niveau du document par un ratio
global très faible de mots et la présence d'images. Cela ne couvre pas le
cas PDHH p. 6. `pdfimages` compte aussi des logos et masques : son compteur
n'est ni un nombre de schémas utiles ni une preuve de leur compréhension.

## Routage économe retenu

1. **Texte natif lisible, page simple :** Poppler comme témoin, sans LLM de
   transcription. Conserver les sauts de page et ne pas fusionner les nombres.
2. **Colonnes ou ordre douteux :** comparer une autre extraction sur les
   seules pages concernées. Pypdf, pdfplumber ou MarkItDown sont candidats
   légers ; ne pas choisir selon la longueur du texte produit. PyMuPDF est
   ici un comparateur hors produit, pas une nouvelle dépendance distribuée.
3. **Tables complexes / structure perdue :** essayer un moteur de structure
   local évalué (premiers essais Docling dans `BENCHMARK-STRUCTURE.md`). Garder cellules,
   en-têtes, unités, notes et coordonnées ; Markdown seul peut être insuffisant.
4. **Scan ou texte natif absent/incomplet/parasite :** OCR de la zone ou page
   rendue dans un dérivé distinct. OCRmyPDF/Tesseract ou moteur OCR de Docling
   restent à qualifier pour la production ; certains modes Docling ont été
   essayés, sans réussite complète des témoins. Éviter l'OCR
   systématique de tout le PDF ; ne jamais remplacer l'original signé.
5. **Figure, équation, conflit non résolu :** vision ciblée par un agent,
   transcription littérale puis relecture indépendante des éléments critiques.
   Si la lecture reste incertaine, marquer l'inconnu ; ne pas compléter au jugé.

Un second extracteur ne constitue pas à lui seul une source indépendante :
plusieurs bibliothèques peuvent lire la même couche défectueuse. Un modèle
visuel peut inventer un raccord plausible. Ni l'un ni l'autre ne remplace
la comparaison avec le rendu.

**Arrêt de l'escalade :** dès que les témoins critiques et le contrôle visuel
du passage utile passent, ne pas faire tourner tous les moteurs pour gagner
une jolie mise en page. Un deuxième essai qui reproduit le même défaut
déclenche le changement de famille (structure/OCR/vision), pas une boucle.
Ce seuil est une règle de coût du projet, pas une garantie scientifique.

Ne pas assimiler `--skip-text` d'OCRmyPDF à « toutes les images seront OCRisées » :
une page mixte peut déjà contenir du texte. Le mode et la zone doivent être
choisis selon le défaut ; `force` rasterise, `redo` vise la couche OCR.
Les options changent selon version : vérifier l'aide locale et épingler.
[Documentation OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/cookbook.html).

## Fidélité, vérité et fiabilité : trois contrôles différents

### Fidélité au document

Contrôler ordre de lecture, négations, décimales, signes, unités, intitulés,
notes, liens figure/légende et cellule/en-tête. Conserver une transcription
des erreurs visibles de la source avec une annotation externe : ne pas
« corriger » silencieusement son auteur.

`usine valider` contrôle ancres, chevauchement lexical, mots ajoutés,
nombres présents dans la page ou ses voisines et description de figures.
Il ne prouve pas l'ordre des mots, la compréhension d'un schéma, la bonne
association d'un chiffre à une ligne, ni l'exactitude d'une règle juridique.
Un sceau est une preuve d'intégrité contre une version, pas un certificat
de vérité. Il peut accepter un texte qui reproduit fidèlement le parasite
de l'extracteur ; les anomalies doivent donc rester visibles hors du score.

### Validité de l'assertion

Pour chaque affirmation destinée à être enseignée, conserver une ligne :

| Champ | Exemple de contenu attendu |
|---|---|
| `id` | identifiant stable de l'assertion |
| `enonce` | une seule proposition contrôlable |
| `preuve` | SHA document, page physique, titre/paragraphe ou coordonnées, extrait court |
| `nature` | texte opposable / recommandation / étude / hypothèse / observation / cas fictif |
| `portee` | territoire, époque, population, exclusions et hypothèses |
| `risque` | ordinaire / critique : sécurité, droit, argent, seuil, unité |
| `corroboration` | autre source primaire consultée, ou manque explicite |
| `verdict` | étayée / contradictoire / périmée / sans source retrouvée / à instruire |
| `relecteur` | outil, modèle, date, résultat et emplacement de la preuve |
| `descendants` | leçon, carte, question, corrigé, schéma concernés |

Ce tableau est un contrat éditorial, pas encore un schéma imposé par le code.
Ne pas fabriquer une corroboration avec deux reprises de la même source.
Les lois se vérifient dans leurs versions officielles pertinentes ; les
normes payantes non consultées restent manquantes. Une recommandation locale
datée ne devient pas une règle universelle. Une mention de traitement du bois
ne devient pas un protocole de diagnostic ou de sécurité au travail.

### Fiabilité du procédé

Mesurer les erreurs sur une référence établie indépendamment, par catégorie.
Sur une transcription de référence complète : CER/WER pour le texte ;
exactitude numérique et unités ; ordre ; cellules/en-têtes et notes pour
les tables ; éléments/relations pour les figures. Mesurer aussi omissions
et ajouts : plus de texte n'est pas toujours mieux.

Notre premier test ne calcule **pas** ces taux : il ne possède que des témoins
ciblés sur des pages difficiles. « 20 témoins passés » signifierait seulement
que ces 20 assertions de test passent, pas « PDF fiable à 100 % ».
Les benchmarks publics servent à présélectionner ; corpus, langue, versions,
matériel et métriques diffèrent. Aucun classement de modèles n'est déduit.

## Des passages aux cours et aux exercices

Pour les visuels, suivre `VISUELS.md` : preuve locale → support pédagogique
qualifié → exercice avec données et corrigé. Une figure décrite ne compte
pas comme support disponible, et une image affichée ne prouve pas un exercice
jouable. Les scores du banc textuel ne mesurent pas cette chaîne.

Concevoir d'abord une production et sa grille : ce que l'élève doit décider,
justifier, mesurer, reconnaître ou faire vérifier. Rattacher aux branches
et spécialités, puis combler les prérequis réellement nécessaires.

Un lot de cours contient :

- un problème professionnel et ses limites ;
- une leçon qui explique les mécanismes et les arbitrages, avec sources ;
- un exemple raisonné, un contre-exemple plausible et les erreurs typiques ;
- une tentative sans correction visible, des aides graduées, un corrigé
  expliqué et une grille qui accepte plusieurs formulations justes ;
- un cas de transfert dont les faits changent assez pour empêcher la récitation ;
- une reprise différée, distincte du résultat immédiat ;
- le registre d'assertions et la relecture indépendante.

| Format | Données indispensables | Contrôle qui manque si on n'a que le moteur |
|---|---|---|
| Question / rappel | question précise, réponse, variantes, source | paraphrase correcte acceptée ; faux ami expliqué |
| QCM | choix, justification de chaque distracteur, bonne réponse | pas de réponse déductible de la forme seule |
| Relier | paires propres au sujet, justification des liens | pas de paires VMC réutilisées pour un autre thème |
| Reconnaître | image autorisée ou schéma original, labels/zones, limites | l'image permet réellement la reconnaissance demandée |
| Plan / schéma | fichier, légende, repères, consigne, corrigé spatial | zones cliquables et solution correspondent au support |
| Calcul | données fictives déclarées, unités, formule, arrondi, résultat indépendant | signe, ordre de grandeur et cas limite vérifiés |
| Jeu de rôle | rôle, dossier, informations accessibles, objectif, grille, relances | une réponse libre n'est pas comprise par une correction statique |
| Expertise contradictoire | hypothèses concurrentes, pièces en tension, investigations discriminantes | absence de preuve ne vaut pas preuve d'absence |

Pour une réponse libre, indiquer le mode réel : auto-appréciation, comparaison
à une grille, relecture humaine, ou futur correcteur IA autorisé. Ne pas
présenter un simple clic comme une évaluation du raisonnement.

Les niveaux élevés exigent une synthèse d'indices incertains, des contraintes
en conflit et une décision conditionnelle défendable. Allonger un QCM de
vocabulaire ne le rend pas expert. Les métiers réglementés et les gestes
dangereux nécessitent leurs formations, habilitations et pratiques supervisées.

## Audit par un autre agent : ciblage + hasard

Deux ensembles se cumulent, ils ne se remplacent pas :

1. **Imposés :** toutes les assertions critiques utilisées, toutes les anomalies
   connues, toutes les nouvelles tables/formules et tous les supports visuels
   du lot enseigné. Retour au rendu, pas seulement au Markdown.
2. **Sondage :** sélection de pages parmi le reste, et d'exercices parmi le lot.
   Le relecteur choisit une graine après gel des empreintes du lot. Conserver
   la graine, la population, les exclusions, l'algorithme, le tirage et le verdict.

Le banc fournit le tirage des **pages**. Le tirage des assertions/exercices
utilise le même principe sur leurs identifiants mais reste manuel dans ce lot.
La graine d'exemple est publique ; elle sert à reproduire, pas à empêcher
l'auteur d'anticiper le contrôle. Pour un audit indépendant, en choisir une
nouvelle après réception du manifeste et ne pas retirer les résultats gênants.

Huit pages par document est le paramètre pratique de départ du script, pas
une assurance statistique. Un document court sera contrôlé intégralement si
le tirage dépasse sa population. Sur une estimation statistique, annoncer
population, nombre vérifié, mode de tirage et intervalle, pas une confiance
intuitive ; les erreurs corrélées par mise en page limitent l'extrapolation.

Une erreur critique : suspendre les usages descendants concernés, corriger
la cause, contrôler toutes les pages du même type puis refaire les contrôles
critiques et un nouveau sondage. Une erreur mineure : consigner, corriger,
vérifier les pages voisines et élargir si elle se répète. L'audit ne certifie
jamais la totalité des pages qu'il n'a pas vues.

## Coût, reprise et attribution

Enregistrer par lot : outil/modèle/version/options, SHA entrée/sortie,
pages traitées, pages rendues/OCRisées, nombre de reprises, durée machine,
temps de revue disponible, consommation de tokens **si fournie par l'outil**,
coût API éventuel et mode abonnement/local. Inconnu reste `null`.
Un nombre de caractères n'est pas un nombre de tokens facturés. L'absence
d'appel API ne signifie ni calcul gratuit ni abonnement gratuit.

Cache : clé composée du SHA original, de la version du moteur, des options
et de la plage de pages. Un nouvel outil n'écrase ni extraction précédente
ni pivot scellé. Les sorties de benchmark vont dans un répertoire neuf.
Ne pas retraiter un document complet pour une correction locale.

Chaque agent reçoit : cahier, manifeste, prochain `suivant`, anomalies,
sorties à livrer, critères de refus. Il rend : diff, verdicts des scripts,
preuves de lecture, erreurs non résolues et point de reprise exact.
L'agent chargé de la relecture n'a pas écrit le contenu et repart de la source.

## Exécuter et reprendre

Voir `BENCHMARK.md` pour les versions et commandes mesurées.

```sh
python3 travail/expertise-2026-09-06/test_benchmark_pdf.py
python3 travail/expertise-2026-09-06/benchmark_pdf.py --help
python3 travail/expertise-2026-09-06/benchmark_pdf.py --audit-seed MA-GRAINE --audit-size 8
python3 app/usine/usine.py etat
python3 app/usine/usine.py suivant 707940074f138868
```

Pour une unité de lecture : déclarer outil/modèle, lire l'unité distribuée,
regarder les figures, corriger le pivot via patch, demander `valider`.
Une page retirée à cause de texte masqué garde sa preuve et son anomalie.
Les contrôles ne sont pas abaissés pour faire passer une extraction.

Pour un cours : suivre son cahier et son format réel, contrôle des assertions,
relecture, tests spécifiques, `python3 app/tests.py`, puis
`python3 tooling/check.py`. Éprouver ensuite les routes concernées.
Pas de publication, de purge de comptes ou de migration impliquée par ces commandes.

## Prochain lot précisément borné

1. Relecture indépendante des témoins et du contrat ; conserver les objections.
2. Tester OCR local et structure sur les mêmes pages difficiles, sans nouveau
   grand téléchargement ou fournisseur distant implicite.
3. Automatiser le diagnostic par page et le signalement des pages mixtes dans
   un cahier usine distinct ; tests rouges PDHH p. 6 et Angers p. 1.
4. Reprendre Angers unité p. 1-12 : transcriptions intermédiaires sauvegardées,
   p. 9/10/12 à nettoyer, ensemble à recontrôler ; aucune unité acceptée.
5. Reprendre PDHH p. 1-12 via l'usine, avec traitement OCR des scans requis.
6. Achever les dossiers patrimoine/désordre/copropriété fragile, puis seulement
   les intégrer comme enseignements jouables après leur propre acceptation.

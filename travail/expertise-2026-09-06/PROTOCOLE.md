# Fabrication reproductible des spécialisations

06/09/2026. Outil Codex, modèle GPT-6. Première unité de `ACA-EXPERTISE-1`.
Complément demandé ensuite par JB : `PIPELINE.md` est le mode opératoire
détaillé, `BENCHMARK.md` porte les essais et `COMPARATIF-OUTILS.md` distingue
les mesures des capacités documentées. Décision 0047.
La demande porte sur un jugement professionnel exceptionnel, pas seulement
sur une connaissance des textes. L'audit indépendant a confirmé le défaut
de profondeur. Cette unité ne termine pas le chantier.

## Ce qui fait foi

1. `programme/genere_copro.py` porte les données historiques de l'arbre ;
   `programme/copro.json` et `SYLLABUS.md` en sont les sorties. Ne pas éditer
   ces sorties pour gonfler artificiellement les niveaux.
2. `programme/specialisations/copro.json` porte les spécialisations demandées,
   leurs objectifs, les productions attendues et les limites. Les branches
   communes servent plusieurs métiers ; aucune équivalence de diplôme.
3. Les chapitres et cartes effectivement écrits sont confrontés à l'artefact
   local dans `COUVERTURE.md`. Aucun compteur ne mesure l'apprentissage humain.

## Du document à un enseignement

| Étape | Sortie conservée | Preuve et limite |
|---|---|---|
| Repérage | titre, origine, date, nature, droits, disponibilité | Un titre NotebookLM ne prouve pas l'accès au texte |
| Préparation locale | PDF, empreinte, pages machine, pivot, rendus | Extraction seulement, pas lecture |
| Lecture par unités | pivot corrigé, descriptions, état scellé | Verdict `usine valider`, pas certification du fond |
| Instruction | fiche, anomalies, passages, propositions de rattachement | Une contradiction de source reste visible |
| Écriture | leçon, pièces fictives, questions, corrigés et grilles | Brouillon tant que source et relecture manquent |
| Relecture indépendante | assertions examinées, sources et réserves | L'auteur ne s'auto-certifie pas |
| Intégration locale | formats pris en charge, tests, artefact | Aucun défaut de format masqué par un exemple générique |
| Publication autorisée | paquet, SHA, retour arrière, test authentifié | Distincte de la fabrication et de la réception utilisateur |
| Apprentissage | tentative, aide, transfert et rappel différé | Pas de certification d'un geste par une note numérique |

## Reprendre les documents

Depuis la racine, consulter d'abord les états, puis demander l'unité. Ne
jamais boucler automatiquement sur `valider` ; chaque unité se lit et ses
figures se regardent avant le contrôle.

```sh
python3 app/usine/usine.py etat
python3 app/usine/usine.py suivant 707940074f138868
python3 app/usine/usine.py suivant 8760dfb3f168df2d
```

Le Focus `322a2f5e843f45b9` a atteint la fin du pas à pas dans cette unité.
Sa première unité provenait du travail antérieur ; les suivantes ont été
reprises ici. Les incohérences du document et les réserves de relecture
restent dans `SOURCES.md`. Relancer `suivant` recontrôle les sceaux.

Pour un nouveau PDF : `preparer CHEMIN`, puis `declarer EMPREINTE --outil
OUTIL --modele MODELE`, `suivant`, édition du pivot, `valider`, et ainsi de
suite ; terminer par `fiche`. Les commandes complètes sont dans
`app/usine/usine.py --help`. Ne jamais modifier les états à la main.

Le registre canonique est `sources/registre.json`. Ne pas employer
`usine registre --ecrire` : cette ancienne commande ajoute au Markdown
généré sans mettre à jour le JSON canonique. Réconcilier la fiche avec
l'entrée existante avant de régénérer le registre ; aucun doublon de source
ne doit être créé pour masquer une lecture partielle.

## Construire les dossiers de spécialité

Pour chaque objectif, écrire une production observable et une grille avant
de rédiger la leçon. La grille doit distinguer : données établies,
hypothèses, inconnues, investigation qui départage, décision conditionnelle,
source et limite. Préparer une pièce contradictoire et un second cas de
transfert, sans donner leur correction avant la tentative.

Le prochain lot de production relie trois dossiers :

- rénovation patrimoniale : façade, humidité, énergie, urbanisme, économie,
  financement, action collective et AMO ;
- désordre technique : observation, hypothèses, mesures, contrat, assurance,
  expertise contradictoire et communication ;
- copropriété fragile : comptes, trésorerie, impayés, habitat, accompagnement,
  recouvrement et stratégie de redressement.

`DOSSIER-PILOTE-ENERGIE.md` est un premier exercice rédigé de lecture critique,
pas encore une étude jouable dans l'application. Il teste les limites d'un
modèle avant tout conseil de travaux. Le reste des dossiers doit être écrit,
pas seulement nommé.

## Réponses libres et IA : contrat de vérité

Le client actuel n'a pas de correcteur sémantique IA branché sur les réponses
libres. Une correction prédéfinie et une auto-appréciation ne démontrent pas
qu'une réponse a été comprise. Aucun correcteur IA n'est ajouté par ce lot.
Avant tout ajout : préciser les réponses transmises, le destinataire, le
coût, le consentement et la conservation ; tester réponses exactes formulées
autrement, faux raisonnements plausibles, refus et incertitudes. Le jugement
doit renvoyer à une grille et à une source, sans verdict de compétence absolu.

Les exercices visuels exigent un schéma ou une image pertinents, des zones ou
paires propres au contenu et une correction correspondante. Un moteur qui
affiche le format ne prouve pas l'existence de ces supports.

## Vérifier et rendre compte

```sh
python3 app/tests_expertises.py
python3 app/couverture_expertises.py --write
python3 app/couverture_expertises.py --check
python3 app/tests.py
python3 tooling/check.py
```

Le rapport est déterministe et expose les empreintes de ses entrées.
`site/banque.json` absent donne « inconnu » : un clone sans artefact ne devient
pas une banque vide certifiée. Un programme seul ne produit aucune carte.
Les cartes sans chapitre ne sont pas distribuées artificiellement entre les
spécialités. Les rattachements multiples ne s'additionnent pas.

Consigner à chaque lot : sources réellement parcourues, formats rédigés,
verdicts, réserves, coût mesuré disponible et prochaine unité exacte.
Cette session ne dispose pas d'un décompte de tokens fiable par document :
coût non mesuré, aucun chiffre inventé. Pas d'appel à une API payante ajouté.

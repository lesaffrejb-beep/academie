# Révision du programme infirmier, 04/09/2026

## POINT DE REPRISE : intégration IFSI terminée localement

Le « go » de JB a lancé la finition. Son troisième rapport a d'abord
été [archivé et analysé](rapports-chatgpt-pro/STRATEGIE.md), puis le lot
`ACA-IFSI-1` a été terminé selon le périmètre de son cahier. Le
[plan commun](rapports-chatgpt-pro/PLAN.md) donne désormais priorité aux
corrections, à l'usage réel et aux petits pilotes avant généralisation.

### Résultat courant

- 375 chapitres, 310 identifiants historiques conservés, copie 2009
  toujours identique. Les 65 ajouts ont un historique explicitement vide,
  accepté uniquement avec l'action `ajouter`.
- 1 123 déclinaisons « Associer la notion » retirées ; les notions restent
  dans leur champ. Les 32 chapitres ainsi vidés reçoivent une capacité
  réelle : **600 objectifs de cadrage** au total, à affiner avec les
  supports du pilote. Aucune carte IFSI produite ou rendue jouable.
- 19 premiers points d'appui déplacés pour respecter les prérequis ;
  un lien de préparation orale devient un pont facultatif. Aucun prérequis
  n'est annoncé à une étape ultérieure. Les années restent indicatives,
  sans équilibrage artificiel : 187, 86 et 42 chapitres.
- Formulations sensibles et dimensions corrigées : observations sur
  dossier fictif, alerte et traçabilité sourcées, calcul distinct de sa
  justification, communication distincte de la saisie numérique.
- Syllabus régénéré : trois exemples au plus par étape, liens vers les
  univers, tous les chapitres conservés. Catalogue IFSI mis à jour.

### Preuves de sortie

| Contrôle | Résultat |
|---|---|
| Tests rouges avant correctif | Ajout sans historique et prérequis d'étape ultérieure détectés |
| `python3 app/tests_ifsi.py` | 21 tests passent |
| `python3 app/valide_programme.py --json` | Les deux programmes passent |
| `python3 programme/genere_ifsi.py --check` | Conforme ; source inchangée |
| `python3 app/tests.py`, avec socket locale autorisée | Toutes les suites, banque réelle et chapitres passent |
| `python3 tooling/check.py` | Zéro erreur |
| Trois mutations IFSI sur copie isolée | Toutes détectées : certification clinique, historique inventé, prérequis tardif |
| `git diff --check` | Passe |
| Contre-relecture indépendante du cadrage | Avis favorable de `revue_pedagogique_ifsi`, dernière réserve sur l'erreur médicamenteuse corrigée et levée |

La contre-relecture ne constitue pas une validation clinique. Les
objectifs, difficulté et criticité restent un cadrage éditorial ; les
sources, réponses et critères des futurs cas seront contrôlés à leur
fabrication. La suite ne demande pas de produire tous les cours avant
le premier usage.

Les modifications restent locales et non committées. Journaux
temporaires : `/tmp/academie-ifsi-reprise-{rouge,tests,global,check}.log`,
rapport des changements `/tmp/academie-ifsi-finition-changements.json`.
Cette section constitue la preuve durable si ces fichiers disparaissent.

### Où repartir

Lire le plan commun et le tri copro pour préparer le cahier L2. Pour
l'usage, les défauts front/journal restent dans leurs cahiers existants
et `travail/audit-froid-2026-09-04.md`. Le lot IFSI ne les clôture pas.
Le cap reste : **entrée en IFSI, formation infirmière, approfondissements
sans plafond**. JB a explicitement confirmé que l'apprentissage doit
continuer après le diplôme et les spécialisations.

Le dépôt contenait déjà beaucoup de modifications avant cette session,
notamment programme copro, banque, serveur et front. Ne pas les annuler
ni les inclure dans un commit IFSI par un ajout global.

## Historique de la pause initiale, conservé pour traçabilité

Les chiffres et défauts ci-dessous décrivent l'arrêt précédent. Ils
sont remplacés pour l'état courant par les preuves de sortie ci-dessus.

### Sur disque à cette pause

- `programme/ifsi.json`, version 0.2 : **375 chapitres**, dont les
  **310 identifiants anciens conservés** et **65 ajouts** ; **1 691
  objectifs** d'inventaire, **2 794 cartes cibles éditoriales**. Ce ne
  sont ni des cartes produites ni des acquis prouvés. Les objectifs
  incluent des déclinaisons générées à partir des notions et demandent
  encore une revue de granularité et de pertinence.
- Trois préparations de douze semaines, huit étapes de trajectoire,
  sept surcouches de spécialisation ; pédagogie et pilote diabète
  explicitement `specification-non-implementee` / `a-construire`.
- Copie historique intacte : `programme/versions/ifsi-2009.json`.
  SHA-256 vérifié :
  `056163e3e865a65c70fa3176a1ccb18d7a4475bd87b34783e9af4d051bc4a6f7`.
- `programme/genere_ifsi.py` remplacé : lit le JSON, contrôle et rend
  uniquement le syllabus ; option `--check` sans écriture.
- `app/valide_ifsi.py` et `app/tests_ifsi.py` ajoutés ; extension reliée
  dans `app/valide_programme.py`, suite et mutation ciblée ajoutées dans
  `app/tests.py` en préservant les modifications préexistantes.
- Décision `0033`, cahier `ACA-IFSI-1`, méthode §33, guides et roadmap
  mis à jour. Le statut roadmap reste `ready`, jamais `done`.
- Sources primaires de la réforme recherchées et recoupées par un autre
  agent ; nuances conservées plus bas. La revue finale du JSON complet
  **n'a pas été menée**, l'arrêt utilisateur est arrivé juste après
  son écriture.

### État exact des contrôles à la pause

| Contrôle exécuté | Résultat |
|---|---|
| Lecture JSON et `git diff --check` | Passent |
| Copie historique et conservation des anciens identifiants | Passent séparément |
| Tests unitaires IFSI | 14 passent ; un autre test d'intégration sur le marqueur passe |
| Suite `python3 app/tests_ifsi.py` | 18 tests, 3 échecs d'intégration |
| `python3 app/valide_programme.py --json` | 65 erreurs, toutes « niveau ou titre legacy absent » |
| `python3 app/tests.py` | Deux suites en échec : IFSI, et serveur d'état pour ouverture de socket interdite par le sandbox ; toutes les autres suites et banques passent |
| `python3 tooling/check.py` | 9 lignes d'erreur : extrait des erreurs IFSI ci-dessus et 14 tirets cadratins dans le JSON |
| Mutation ciblée de certification clinique | Le retrait du refus est détecté sur une fixture valide |

Les journaux temporaires sont `/tmp/academie-ifsi-pause-tests.log`,
`/tmp/academie-ifsi-pause-detail.log` et
`/tmp/academie-ifsi-pause-check.log`. Ils peuvent disparaître ; le
résumé ci-dessus est le point de sauvegarde durable.

### Ancienne liste de finition L1, désormais traitée

1. **Accorder le contrat des nouveaux chapitres.** Les 65 ajouts ont
   `legacy: {niveau: null, titre: null, ue_ids: []}`, puisqu'ils n'ont
   aucun prédécesseur. Le valideur exige actuellement niveau et titre
   anciens pour tous. Ajouter d'abord un test : les nulls sont admis
   uniquement pour `revision.action == "ajouter"` ; un chapitre
   historique conserve obligatoirement ses métadonnées. Ne pas inventer
   un passé aux ajouts pour rendre les tests verts.
2. Retirer les **14 tirets cadratins** du JSON courant, dans le titre de
   l'oral facultatif, ses objectifs et les libellés des sources et
   référentiels. Le contrôle de voix reste inchangé.
3. Faire la **revue indépendante du JSON** : objectifs réellement
   évaluables, granularité des déclinaisons par notion, cohérence
   étapes/difficulté/criticité, formulations gestuelles, correspondances
   de compétences, séparation des voies. Les années sont très
   déséquilibrées (199 chapitres année 1, 80 année 2, 36 année 3) :
   vérifier que c'est justifié. Le rattachement UE courant est laissé
   vide et explicitement non établi ; ne pas présenter le mapping comme
   une équivalence réglementaire officielle.
4. Exécuter `python3 programme/genere_ifsi.py` seulement après accord
   des données et du valideur. **`SYLLABUS-IFSI.md` est encore l'ancien
   syllabus**, volontairement laissé ainsi à la pause. Puis
   `python3 programme/genere_ifsi.py --check`.
5. Vérifier la lisibilité du rendu : le continuum utilise tous les
   identifiants par étape et peut devenir trop long en « points
   d'appui ». Réduire cette présentation si nécessaire sans perdre le
   parcours ni les branches après le diplôme.
6. Mettre à jour uniquement l'entrée IFSI de
   `programme/catalogue.json` : elle annonce encore **310 chapitres**
   et le précédent texte de préparation. Conserver zéro carte jouable.
   Ajuster la note de `ACA-DOMAIN-KIT-1`, encore fondée sur le squelette
   précédent, dans `roadmap.json`.
7. Relancer `python3 app/tests_ifsi.py`, puis `python3 app/tests.py`,
   puis `python3 tooling/check.py`. Le test serveur HTTP a besoin d'un
   environnement permettant une socket locale ; ne pas modifier son
   assertion pour contourner le sandbox. Rejouer la mutation ciblée.
8. Consigner les résultats réels, mettre à jour le statut du chantier
   uniquement après ses preuves et préparer un diff par chemins.
   Aucune publication n'a été demandée dans cette session.

Le moteur de cas, la mesure de maîtrise et la fabrication des cours
sont les lots suivants, après ce programme. Le plan commun les ordonne
désormais avec la révision copro et un contrat pédagogique partagé.
Ils ne doivent pas être confondus avec la finition technique de cette
révision. Le reste de ce document conserve le cadrage de la première
session ; le plan commun fait foi pour l'ordre des travaux entre métiers.

---

Cap confirmé par JB : entrer en école infirmière, devenir infirmier,
puis continuer à approfondir sans plafond. Le chantier
`ACA-IFSI-1` applique la critique au programme et à ses contrôles.
Il ne transforme pas un inventaire en banque jouable par déclaration.

## Ce qui change

| Point de la critique | Traitement dans ce lot |
|---|---|
| Référentiel ancien | Cadre DEI-2026 courant, sources officielles datées, copie exacte du squelette précédent en `programme/versions/ifsi-2009.json` |
| Voies d'accès confondues | Trois préparations avec diagnostic et semaines distinctes ; entretien et écrit FPC séparés du dossier Parcoursup |
| Sujet tiré au sort | Entraînement facultatif, absent du parcours obligatoire ; aucune présentation comme épreuve nationale actuelle |
| Niveaux ambigus | Étape de formation, difficulté, criticité et modes distincts ; niveau historique conservé pour compatibilité |
| Taxonomie administrative | Univers lisibles conservés, correspondance pédagogique avec les compétences officielles, distinction entre domaines d'enseignement A–E et domaines de compétences 1–5 |
| Matières trop larges | Objectifs fins et révision éditoriale par chapitre ; la maîtrise future doit porter sur ces objectifs |
| Contenus insuffisants | Renforcement du numérique, de l'environnement, de la consultation/prescription, du leadership et de la pédiatrie |
| Formulations gestuelles | Objectifs numériques de préparation, analyse, surveillance et alerte ; simulation et pratique supervisée distinctes |
| Constantes rigides | Contexte, évolution et fiabilité de mesure ; aucune table de normes clinique inventée |
| Stages | Situations du cadre 2026, préparation, analyse et consolidation ; un exercice ne délivre aucune validation de stage |
| Spécialités et expertise | Surcouches du socle, nouvelles questions, recherche et extensions par la boîte ; aucune fin globale du parcours |
| Graphe | Identifiants stables, prérequis et ponts préservés et contrôlés ; pas de relation clinique « contre-indique » générée sans source |
| Générateur qui écrase les corrections | JSON éditable unique ; génération et contrôle du syllabus sans réécriture de la source |

## Ce que les textes ont corrigé dans la critique

- Les domaines A–E sont des domaines d'enseignement. Les annexes I et
  II emploient des domaines de compétences numérotés. Le rapprochement
  est explicite ; les rattachements détaillés de nos chapitres restent
  des choix pédagogiques.
- Pour la FPC, l'article 12 fixe deux épreuves et un seuil total, en
  plus de la note éliminatoire. « Sans calculatrice » peut être un
  exercice pédagogique ; aucune interdiction nationale générale n'a
  été retrouvée dans cet article. Le règlement local reste à consulter.
- L'ancienne condition générale d'expérience ne doit pas être
  reconduite sans texte. L'accès adapté aide-soignant a ses propres
  conditions et ne décrit pas tous les accès spécifiques.
- La première année ne se résume pas à « un seul patient » : l'annexe
  III parle de situations simples ou stabilisées. Le programme ne
  transforme pas une progression pédagogique en limite d'exercice.
- L'abrogation du texte de 2009 ne périme pas automatiquement les
  connaissances apprises ; elle concerne le cadre de formation.

Sources consultées le 04/09/2026 :
[texte complet](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000053568913/),
[annexe I](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570495),
[annexe III](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570499),
[article 12](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570385),
[article 60](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053570487),
[Parcoursup](https://www.parcoursup.gouv.fr/contenus/test-d-auto-positionnement-ifsi-1812).

## La suite est ouverte et concrète

Le prochain lot est un pilote vertical : diabète, traitement, calcul,
situation préoccupante, transmission, éducation et retour à domicile.
Il réutilise les identifiants du programme et sert à éprouver la boucle
complète avant d'étendre toutes les branches.

| Brique | Exigence pour le pilote | État de ce lot |
|---|---|---|
| Maîtrise | Par objectif et contexte ; connaissance, raisonnement, calcul et communication distincts | Spécification, aucun score calculé |
| Erreur critique | Remédiation puis nouvel essai ; aucune compensation par des points sur un autre sujet | Spécification, pas de blocage général de l'arbre |
| Calcul | Valeur et unité saisies, estimation, dimension, vraisemblance, détection d'information manquante | Spécification, aucun dosage clinique produit |
| Cas | Situations fictives, progression temporelle et variantes dont les réponses attendues sont sourcées | Pilote à construire |
| Provenance sensible | Assertion, source exacte, nature, territoire, vérification et portée ; sources locales ou incertaines signalées | Exigence de fabrication à appliquer aux futures cartes |
| Revue | Contrôles automatiques, relecture indépendante, revue professionnelle adaptée à la criticité | Aucune validation clinique revendiquée |
| Mesures | Rétention différée, transfert à un cas inédit, erreurs critiques, confiance et justesse, évolution après remédiation | À mesurer depuis des usages réels et privés |
| Extensions | Spécialités, recommandations nouvelles, articles et questions du joueur alimentent de nouveaux objectifs | Arbre extensible, sans dernier niveau |

La demande de progression sans fin ne se réduit pas à répéter les mêmes
questions avec d'autres nombres. De nouvelles branches et de nouveaux
contenus peuvent entrer, avec les exigences de source et de relecture
de la doctrine. Les formations et diplômes spécialisés restent des
formations réelles, pas des titres attribués par l'application.

## Preuves et limites

La critique a été préparée par `app/usine/usine.py` sous l'empreinte
`f34fc8af2597118f`. Déclaration Codex, modèle `gpt-5.6-sol` lu dans la
configuration locale, classe grand. Le script a accepté les deux unités
de lecture (pages machine 1–12 et 13–20) et la fiche. Cette validation
prouve la fidélité du pivot, pas l'exactitude des affirmations du LLM.
La recherche réglementaire indépendante a précédé leur adoption.

Les tests rouges ont été observés avant les changements de code et de
données : absence du contrôle IFSI, disparition silencieuse du marqueur
de référentiel et absence des trois préparations dans le syllabus.
L'historique est verrouillé par son SHA-256 et les anciens identifiants
doivent subsister. Les contrôles de structure ne prouvent pas que les
objectifs sont cliniquement justes ou qu'un élève les maîtrise.

Les résultats à l'arrêt et le travail restant sont consignés dans le
point de reprise en tête de ce document. Le chantier n'est pas déclaré
terminé.

# OCR : références publiques et budget conditionnel

Recherche du 06/09/2026, Codex / GPT-6. Sources primaires consultées en ligne.
Tarifs en dollars US, hors taxes ; estimations, pas factures ni appels API.
**Périmètre du prix : transcription, pas cours multimédia prêt à jouer.**
Récupération des figures, légendes, géométrie d'exercice, adaptation, revue
et tests produit sont des postes distincts encore non chiffrés : `VISUELS.md`.
Méthode OpenAI Docs appliquée : pages officielles modèles, tarifs, vision,
fichiers, Batch et abonnement ouvertes avant recommandation.

## Nous ne partons pas de zéro

[OmniDocBench](https://github.com/opendatalab/OmniDocBench) fournit jeu de
données, scripts et classements par texte, tableaux, formules et ordre de
lecture. Le tableau v1.6_full consulté affiche notamment PaddleOCR-VL-1.6,
MinerU2.5-Pro et GLM-OCR en tête du score global. Ce score combine trois
mesures ; ce n'est pas un taux de vérité. Les catégories linguistiques
documentées sont anglais/chinois : aucune garantie de transfert aux PDF
français patrimoniaux. Toujours noter version du jeu, du modèle et configuration.

[olmOCR-Bench](https://github.com/allenai/olmocr/blob/main/olmocr/bench/README.md)
teste des propriétés simples d'une page : texte attendu, ordre, relations de
tableau et éléments à exclure. Son protocole combine annotations et revue
humaine. Son classement distingue résultats reproduits et résultats rapportés
par les auteurs. Notre banc de témoins relève de cette famille d'approche,
sans prétendre exécuter ce benchmark public. Un caractère erroné dans une
équation peut compter davantage qu'une longue différence de mise en forme.

Décision : compléter nos témoins ciblés par des références intégrales sur un
lot français, avec erreurs de caractères/mots, ordre des blocs, cellules et
valeurs-unités. Garder un lot de test non utilisé pour ajuster les prompts.
Un meilleur score public sert à sélectionner un candidat, pas à le qualifier
pour Académie. Les noms du classement sont de nouveaux candidats à examiner,
pas des outils déjà testés sur ce Mac.

## Coût d'une passe OpenAI sur les trois PDF

54 + 32 + 180 = **266 pages** (manifeste vérifié par le banc).
Luna accepte les images ; modèle API `gpt-5.6-luna`, pas un moteur OCR spécialisé
dont nous aurions mesuré la fidélité. [Fiche officielle](https://developers.openai.com/api/docs/models/gpt-5.6-luna).

Hypothèse A : une requête indépendante par page, **3 500 tokens d'entrée**
(image comprise + consigne) et **1 500 tokens de sortie facturés** (raisonnement
éventuel compris). Aucun outil payant, cache, nouvelle tentative ni revue.

| Modèle API | Entrée / million | Sortie / million | Une page A | 266 pages A |
|---|---:|---:|---:|---:|
| GPT-5.6 Luna | 0,20 $ | 1,20 $ | 0,0025 $ | 0,665 $ |
| GPT-5.6 Terra | 2,00 $ | 12,00 $ | 0,025 $ | 6,65 $ |
| GPT-5.6 Sol | 4,00 $ | 20,00 $ | 0,044 $ | 11,704 $ |

[Tarifs officiels standard, contexte court](https://developers.openai.com/api/docs/pricing).
Formule : `pages × (tokens_entree × prix_entree + tokens_sortie × prix_sortie) / 1_000_000`.
Le tableau suppose des requêtes courtes distinctes, pas un contexte cumulant
les 266 pages. Ne pas utiliser le tarif standard pour une exécution Fast.

L'hypothèse d'entrée est compatible avec une image `detail: high` : plafond
de 2 500 patches, multiplicateur 1,2, donc environ 3 000 tokens image au plus,
plus une consigne de 500 tokens. Mais le redimensionnement peut rendre les
petits caractères illisibles. `original` ou des recadrages coûtent davantage ;
`auto` suit `original` sur ces modèles, ne pas le laisser implicite dans un
budget fondé sur `high`. [Règles de vision](https://developers.openai.com/api/docs/guides/images-vision).

Hypothèse B plus chargée : 12 000 tokens d'entrée et 6 000 de sortie facturés
par page donnent **2,554 $ avec Luna** pour 266 pages. A et B sont deux scénarios,
pas des bornes garanties. Mesurer `usage`, sorties tronquées, tokens de
raisonnement et reprises sur le pilote avant d'autoriser le lot complet.

[Batch](https://developers.openai.com/api/docs/guides/batch) annonce une réduction
de 50 % avec traitement sous 24 heures ; vérifier l'accès effectif modèle et
endpoint sur le compte. Luna A reviendrait alors à 0,333 $ environ, sans les
coûts de revue. Ne pas lancer un lot avant d'avoir évalué un pilote synchrone.

## Abonnement ou API ?

Un agent Luna dans Codex connecté au compte ChatGPT consomme l'enveloppe du
plan ; ce n'est ni gratuit ni un forfait garanti de pages. Contexte, outils,
raisonnement et reprises affectent la consommation. Codex avec une clé API
est facturé aux tarifs API. Le calcul ci-dessus ne décrit donc pas le débit
de l'abonnement et ne transforme pas celui-ci en crédits API.
[Documentation des offres et de l'usage](https://learn.chatgpt.com/docs/pricing).

Pas de nouvelle souscription recommandée pour ces trois PDF sans essai.
Pour un pipeline ouvert, les requêtes API courtes sont plus faciles à mesurer
et rejouer. Pour quelques unités avec l'abonnement existant, un agent dédié
peut suffire, à condition d'enregistrer modèle, consigne, empreinte, page,
sortie et verdict. Aucun besoin d'un agent autonome complet par page : un
worker simple évite de recopier tout l'historique du projet.

## Astuces retenues et ordre proposé

1. Figer les originaux/empreintes et rendre les pages. Extraction native
   d'abord, mais contrôle page par page des PDF mixtes : une page avec un titre
   sélectionnable peut contenir tout son corps sous forme de scan.
2. Tester les extracteurs structurés et OCR local sur les mêmes cas difficiles.
   Conserver texte brut et géométrie ; Markdown seul perd des relations.
3. Pilote Luna de transcription littérale sur les images visibles : ne rien
   compléter, garder les incertitudes, unités et contradictions. Pas de cours
   ni correction juridique dans cette passe. Ne pas lui donner les témoins
   attendus : ce serait une fuite du jeu de test.
4. Comparer les variantes `high` et `original` sur les petits caractères ;
   recadrer les tableaux suspects avec repérage de page/bloc. Une image évite
   d'injecter directement le texte PDF parasite ; le modèle peut néanmoins
   omettre ou inventer du contenu. Un PDF envoyé comme `input_file` apporte
   **texte et images**, donc aussi une couche native éventuellement polluée.
   [Comportement officiel des entrées PDF](https://developers.openai.com/api/docs/guides/file-inputs).
5. Revoir tous les chiffres/relations critiques et un sondage tiré après gel
   des sorties. Un second agent doit comparer aux images, pas seulement donner
   son accord à la transcription du premier. Même modèle ≠ erreur indépendante.
6. Réserver un modèle plus coûteux aux échecs et arbitrages. Cacher les
   résultats par empreinte PDF/page/rendu/moteur/version/consigne afin de ne
   pas repayer les pages inchangées. Journaliser coût par page et coût de reprise.
7. Seulement ensuite : unités usine, assertions sourcées, objectifs, cours,
   exercices, corrigés et revue indépendante selon `PIPELINE.md`. Une page
   correctement transcrite n'est ni une règle actuelle ni un cours expert.

Le routage local puis Luna est une **hypothèse de production à évaluer**.
Luna n'a encore été testé sur aucune de ces pages ; aucun appel API payant
n'a été effectué. L'autorisation d'envoi et le plafond de dépense restent
nécessaires pour le pilote cloud. Les moteurs locaux n'envoient pas les PDF
à une API de conversion ; téléchargement de poids et calcul local sont
distincts, avec leurs propres coûts de stockage et de temps.

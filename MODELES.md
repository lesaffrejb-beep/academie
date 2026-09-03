# MODELES, ce qu'un modèle peut et ne peut pas faire ici

Lu par tout modèle avant un travail long : lire un document, écrire des
chapitres, coder un chantier. Écrit le 03/09/2026 sur les tableaux de
résultats lus ce jour-là ; **à relire le 03/12/2026** (les modèles
changent tous les trois mois). Un chiffre porte sa date et sa source ;
ce qui n'a pas pu être lu à la source porte `[À VÉRIFIER]`. Ce fichier
ne classe pas les modèles par prestige : il dit ce qu'on leur confie
ici, et ce qu'on ne leur confie pas ([`decisions/0027`](decisions/0027-pas-a-pas-impose-points-de-sauvegarde-classes-de-modeles.md)).

## 1. Pourquoi un modèle doit lire ce fichier

Un modèle ne connaît pas ses limites de l'intérieur. Trois faits mesurés
en 2026 décident de tout ce qui suit :

- **Une fenêtre n'est pas une mémoire.** Les trois familles annoncent un
  million de jetons, mais sur les épreuves à plusieurs aiguilles (MRCR),
  la lecture se dégrade bien avant : le rapport technique de Google
  donnait 54 à 58 % pour Gemini 2.5 Pro à huit aiguilles sous 128 k
  (lu le 03/09/2026 sur yage.ai, `[À VÉRIFIER]` à la source). Les cent
  premières pages d'un document s'effacent pendant qu'on lit les cent
  suivantes : d'où les unités courtes et l'état sur disque.
- **Résumer ajoute quelque chose une fois sur dix.** Sur le tableau de
  Vectara (HHEM-2.3, mis à jour le 11/05/2026), les meilleurs modèles
  généralistes introduisent dans un résumé un fait absent de la source
  entre 7 et 12 % du temps. D'où : le pivot **recopie**, il ne résume
  pas, et chaque chiffre est vérifié par la machine.
- **Lire un PDF est un métier d'outil, pas de modèle.** Sur
  OmniDocBench (v1.7, avril 2026), les têtes de classement sont des
  modèles d'OCR spécialisés, pas des modèles de conversation. D'où :
  poppler pour le texte, la vision seulement pour les figures, l'OCR
  avant tout PDF scanné.

## 2. Se déclarer : qui êtes-vous ?

Avant la première unité de travail, le modèle se déclare à l'usine :

```bash
python3 app/usine/usine.py declarer <empreinte> --outil <outil> --modele <modèle> --classe <petit|moyen|grand>
```

| Outil | Comment savoir quel modèle vous êtes | Où l'outil lit les règles du dépôt |
|---|---|---|
| Claude Code | le modèle est nommé dans le contexte de session ; `/model` l'affiche et le change | `CLAUDE.md` (renvoie à `AGENTS.md`) |
| Codex (OpenAI) | `/model` dans la session ; la clé `model` de `~/.codex/config.toml` | `AGENTS.md`, de la racine au dossier courant, 32 Kio au plus |
| Antigravity (Google) | le sélecteur de modèle du panneau agent ; « Auto » n'est pas un nom | `.agents/rules/academie.md` (renvoie à `AGENTS.md`), `~/.gemini/GEMINI.md` en global, 12 000 caractères par fichier de règles |
| Cursor | le menu du modèle dans la conversation ; « Auto » n'est pas un nom | `AGENTS.md` et `.cursor/rules/academie.mdc` |
| Gemini CLI | `/model` | `GEMINI.md` (renvoie à `AGENTS.md`) |

**Si vous ne pouvez pas nommer votre modèle avec certitude, vous êtes
« inconnu », classe petit.** Un nom de petit modèle déclaré en classe
grand est ramené à petit par le script (motif `modeles_petits` dans
`academie.json`). Une classe qu'on s'attribue trop haut se paie au
premier refus : la taille des unités est divisée par deux.

## 3. Les trois classes

Elles se définissent par ce qu'on leur confie ici, pas par un score.

| Classe | Ce qu'elle fait ici | Unités (pages) | Ce qu'elle ne fait pas |
|---|---|---|---|
| **grand** | lit un document entier par unités, écrit des chapitres en `brouillon` à tous les niveaux, code un chantier depuis son cahier, relit en agent frais le travail d'un autre modèle | 12, jusqu'à 25 | valider son propre travail ; écrire un chiffre sans source ; pousser sans tests verts |
| **moyen** | lit par unités, écrit fiches, lignes de registre et cartes de niveaux 1 à 3 en `brouillon`, code une étape numérotée d'un cahier | 5, jusqu'à 10 | une leçon de niveau 4 ou 5 ; relire un contenu écrit par un modèle moyen ; élargir un périmètre |
| **petit** (et inconnu) | relit le pivot **pré-rempli** par unités courtes, décrit les figures, écrit la fiche, propose la ligne de registre | 2, jusqu'à 4 | un chapitre, une carte, un chiffre ; du code hors d'une étape nommée ; continuer après deux refus de suite sans le dire à l'humain |

Classement des noms lus le 03/09/2026 (un nom absent d'ici est petit
tant qu'un humain n'a pas tranché) :

| Classe | Modèles |
|---|---|
| grand | Claude Fable 5.1 et Fable 5 ; Claude Opus 5 ; Claude Opus 4.7 et 4.6 (en mode réflexion « high ») ; GPT-5.6 (variantes « sol » et « terra ») ; GPT-5.5 et GPT-5.5-pro ; Gemini 3.1 Pro |
| moyen | Claude Sonnet 5 et Sonnet 4.6 ; GPT-5.3-Codex `[À VÉRIFIER]` (encore servi ?) ; Gemini 3.5, 3.6, 3.7 et 3.8 Flash ; Muse Spark 1.x (Meta), Qwen 3.8 Max, Ernie 5.1, Grok 4.5 : bien classés en arène, `[À VÉRIFIER]` sur nos épreuves, et absents des outils de JB |
| petit | Claude Haiku 4.5 ; GPT-5.x mini et nano ; Gemini Flash-Lite ; GPT-OSS-120B (dans Antigravity) ; tout modèle local ; « Auto » ; inconnu |

## 4. Les épreuves qui nous intéressent, et ce qu'elles disent

| Ce qu'on demande au modèle | Épreuve publique | Ce qu'on a lu (date, source) | Ce qu'on en conclut |
|---|---|---|---|
| coder un chantier au cahier, tests d'abord | SWE-bench Verified, SWE-bench Pro, Terminal-Bench 2.x | Fable 5 : 95,0 % Verified, 80,0 % Pro ; Opus 5 : 89,1 % Terminal-Bench 2.1, 79,2 % Pro ; Sonnet 5 : 80,4 % Terminal-Bench 2.1, Verified `[À VÉRIFIER]` (72,7 et 85,2 selon la page) ; GPT-5.5 (23/04/2026) : 82,7 % Terminal-Bench 2.0, 58,6 % Pro ; Gemini 3.5 Flash (19/05/2026) : 76,2 % Terminal-Bench 2.1 ; Haiku 4.5 : 73,3 % Verified (10/2025). Lus le 03/09/2026 sur morphllm, OpenAI, DataCamp ; les pages Anthropic et OpenAI n'ont pas répondu ce jour-là | les grands codent un chantier ; les moyens une étape ; les petits exécutent une étape sous tests rouges. Un score de 80 % dit qu'une tâche sur cinq échoue : les tests ne sont pas optionnels |
| tenir un long document sans perdre le début | MRCR v2 (8 aiguilles), Fiction.LiveBench, « lost in the middle » | fenêtres annoncées : 1 M (Opus 5, Sonnet 5, Gemini), 400 k dans Codex (GPT-5.5) ; Gemini 3.1 Pro devance 3.5 Flash de 7,6 points sur MRCR v2 à 128 k ; Gemini 2.5 Pro à 8 aiguilles sous 128 k : 54 à 58 % (rapport Google, lu sur yage.ai le 03/09/2026) | on ne charge jamais un document entier ; on lit par unités et on écrit sur disque après chacune ; la reprise se fait depuis l'état, pas depuis la mémoire |
| recopier sans rien ajouter | tableau Vectara des hallucinations (HHEM-2.3) | mis à jour le 11/05/2026 : GPT-5.5 9,3 % ; Haiku 4.5 9,8 % ; Sonnet 4 10,3 % ; Opus 4.1 11,8 % ; Gemini 2.5 Pro 7,0 % ; Gemini 2.5 Flash 7,8 % ; GPT-5.4-nano 3,1 % ; o3-pro 23,3 %. Claude 5 et Gemini 3 pas encore mesurés | le pivot est une copie, pas un résumé ; la couverture et les chiffres sont contrôlés par la machine ; un petit modèle n'écrit pas de résumé sans fiche vérifiée |
| lire un PDF | OmniDocBench v1.7 (04/2026) | les têtes de classement sont des modèles d'OCR (GLM-OCR, PaddleOCR-VL, MinerU) et non des modèles généralistes `[À VÉRIFIER]` à la source | poppler extrait, le modèle relit ; un PDF sans couche texte passe par `ocrmypdf` avant tout |
| lire un graphique ou une figure | CharXiv Reasoning | Gemini 3.5 Flash : 84,2 % (05/2026) | même le meilleur se trompe sur une figure sur six : un chiffre lu en vision est compté « à vérifier » par le script et relu par un humain ou un agent frais |
| suivre un protocole de dix étapes sans en sauter | IFEval, IFBench | aucun chiffre relevé le 03/09/2026 `[À VÉRIFIER]` | la parade n'est pas le score : c'est le script qui donne une unité à la fois et refuse la suivante |
| répondre sans source | SimpleQA, FACTS Grounding | aucun chiffre relevé `[À VÉRIFIER]` | un chiffre, une date, un délai, un montant sans source ne s'écrivent pas (`decisions/0021`), quel que soit le modèle |

## 4 bis. Les arènes (préférence humaine, pas vérité)

JB a apporté le 03/09/2026 quatre tableaux d'arena.ai, où des personnes
comparent deux réponses à l'aveugle et votent. Une arène mesure une
**préférence**, pas une exactitude : un modèle qui écrit bien et se
trompe peut y gagner. Elle dit en revanche qui tient la route sur des
tâches réelles, et l'écart de rang (« rank spread ») dit combien le
classement est sûr. Lecture faite sur les captures, dix premiers
seulement, scores arrondis :

| Arène (date, votes, modèles) | Ce qu'elle mesure pour nous | Tête de classement le jour de la capture |
|---|---|---|
| Document Arena (26/07/2026, 322 650 votes, 39 modèles) | analyse de documents et raisonnement sur un long contenu : le plus proche de l'usine | 1 Claude Opus 5 (high) ; 2 Opus 4.6 ; 3 Opus 4.6 (high) ; 4 Fable 5 ; 5 Opus 4.7 ; 6 Opus 4.7 (high) ; 7 GPT-5.5 (high) ; 8 Sonnet 4.6 ; 9 GPT-5.5 ; 10 GPT-5.6 terra (xhigh) ; 11 GPT-5.6 sol (xhigh). Les quatre premiers sont à un rang près les uns des autres |
| Vision Arena (27/08/2026, 1 258 468 votes, 148 modèles) | lire une page rendue, une figure, une capture | 1 Claude Fable 5 ; 2 Opus 4.7 (high) ; 3 Qwen 3.8 Max ; 4 Opus 4.7 ; 5 Opus 4.6 (high) ; 6 Muse Spark (Meta) ; 7 Opus 4.6 ; 8 Muse Spark 1.2 (xhigh) ; 9 Opus 5 (high) ; 10 Gemini 3 Pro. Catégories utiles : Diagram, OCR, Entity Recognition |
| Search Arena (24/08/2026, 1 110 523 votes, 34 modèles) | chercher sur le web et répondre avec des sources : ce que fait un modèle qui écrit un chapitre | 1 GPT-5.6 sol (xhigh) ; 2 Claude Opus 4.6 (search) ; 3 GPT-5.5 (search) ; 4 Opus 4.7 ; 5 Fable 5 ; 6 Ernie 5.1 ; 7 Sonnet 4.6 (search) ; 8 Grok 4.5 ; 9 Gemini 3.1 Pro (grounding) ; 10 Gemini 3 Pro (grounding). L'arène propose un réglage « Factuality » : à activer avant de lire |
| Text Arena (02/09/2026, 7 999 020 votes, 400 modèles) | l'ensemble : rédaction, code, suivi de consigne | 1 Claude Fable 5 ; 2 Opus 4.6 (high) ; 3 Fable 5.1 (max) ; 4 Opus 4.7 (high) ; 5 Muse Spark 1.2 (xhigh) ; 6 Opus 4.6 ; 7 Opus 4.7 ; 8 Gemini 3.8 Flash (high) ; 9 Opus 5 (high) ; 10 Muse Spark 1.1 ; 11 Gemini 3.7 Flash (high). Catégories utiles : Instruction Following, Hard Prompts |

Ce qu'on en retient pour l'usine : sur les documents et la vision, les
modèles Claude en mode réflexion et GPT-5.5 ou 5.6 tiennent le haut ;
un modèle Flash (Gemini 3.7 ou 3.8) entre dans les dix du texte, pas du
document ni de la vision, ce qui confirme sa classe moyen. Les noms
absents de ces tableaux (Haiku, mini, nano, lite, locaux) restent petits.
Les arènes changent chaque mois : on ne copie pas un rang dans une
carte, on relit le tableau à la date du travail.

## 5. Faiblesses connues, parade en place

| Faiblesse | Où elle frappe | Parade (vérifiée par la machine) |
|---|---|---|
| oubli du début d'un long contexte | lecture d'un document, longue session de code | unités courtes, état sur disque, `suivant` relit l'état, rien en mémoire |
| résumé qui glisse vers l'invention | pivot, fiche, leçon | couverture minimale et invention maximale par page (`academie.json`, `usine`) |
| chiffre inventé ou déplacé | pivot, fiche, carte | tout chiffre du pivot doit se lire sur la page ou ses voisines ; tout chiffre de la fiche doit se lire dans le pivot ; toute carte : `valide_chapitres.py` |
| paresse : consigne laissée en place, page « décrite » en trois mots | pages à figures | consigne de départ détectée ; description de six mots au moins |
| s'autovalider | tout | c'est le script qui valide ; sceau par unité ; contrôles rejoués à chaque `suivant` |
| se déclarer plus grand qu'on est | déclaration | noms de petits modèles ramenés à petit ; unités divisées par deux au premier refus |
| confiance en vision | figures, tableaux | chiffres des lignes `[figure]` et `[tableau]` comptés « à vérifier » dans l'état |
| nom d'une personne dans une transcription | formations internes | `sources/interne/` ne sort jamais de la machine ; fiche et chapitres sans nom ; le script retire locuteurs et horodatages, pas les noms cités dans la parole : relecture humaine |
| coupure, plafond de jetons, session fermée | tout travail long | chaque unité validée est un point de sauvegarde ; `prompts/reprendre.md` |

## 6. Ce que la classe change ailleurs qu'à l'usine

- **Chapitres et cartes** : un petit modèle n'en écrit pas ; un moyen
  écrit des cartes de niveaux 1 à 3 en `brouillon` ; un grand écrit à
  tout niveau, en `brouillon`. Le passage à `valide` exige `verifie_par`
  (un humain ou un agent frais de classe moyen au moins, différent de
  l'auteur) : `valide_chapitres.py` le refuse sinon.
- **Code** : un petit exécute une étape numérotée d'un cahier, tests
  rouges d'abord, et s'arrête ; un moyen prend un cahier ; un grand
  peut écrire un cahier, que JB valide. Personne ne code sans cahier
  (`CONTRIBUER.md`).
- **Abonnement d'abord** : tout ce qui précède tourne dans l'outil de
  l'élève, sur son abonnement ; aucune clé d'API n'est jamais requise
  (`decisions/0026`).

## 7. Renouveler ce fichier

Tous les trois mois, ou dès qu'une famille change de génération : relire
les tableaux nommés au §4, dater chaque chiffre, marquer `[À VÉRIFIER]`
tout ce qui n'a été lu que sur un site secondaire, mettre à jour le
tableau des noms du §3 et le motif `modeles_petits` d'`academie.json`,
ajouter une ligne dans `lab/VEILLE.md`. Un chiffre sans date se retire.

## Sources lues le 03/09/2026

- OpenAI, « Introducing GPT-5.5 » (23/04/2026), lu par une page de
  recherche ; la page elle-même a refusé la lecture ce jour-là.
- morphllm.com, « Claude Benchmarks (2026) », lu par une page de
  recherche ; la page elle-même a refusé la lecture ce jour-là.
- Vectara, « hallucination-leaderboard » sur GitHub, mis à jour le
  11/05/2026, lu directement.
- Google DeepMind, fiche modèle Gemini 3.5 Flash, et DataCamp.
- OmniDocBench (opendatalab) et CodeSOTA.
- yage.ai, « Long Context Benchmarks: All Three Hit 1M » (15/03/2026).
- arena.ai, tableaux Document (26/07/2026), Vision (27/08/2026), Search
  (24/08/2026) et Text (02/09/2026), captures apportées par JB le
  03/09/2026.
- Antigravity, « Rules and Workflows » (antigravity.google/docs), lu
  directement ; OpenAI, « Custom instructions with AGENTS.md » ;
  Cursor, règles et AGENTS.md ; Anthropic, Haiku 4.5 (10/2025).

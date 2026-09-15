# Veille du 15/09/2026, comparatif des dépôts « apprendre avec un agent »

Recherche menée à la demande de JB, dans la foulée de
[`decisions/0054`](../decisions/0054-plus-de-front-le-depot-est-l-interface.md)
(plus de front, le dépôt est l'interface) et du cahier
[`ACA-SANS-FRONT-1`](../chantiers/ACA-SANS-FRONT-1.md).

Question posée : « Ça se trouve, faut juste prendre un dépôt existant et
arrêter de faire le nôtre ? » Réponse courte : **non**, aucun dépôt ne
couvre l'intersection qui fait notre valeur, mais plusieurs apportent des
patterns précis qu'on reprend. Détail ci-dessous.

## 1. Méthode et limites

Quatre explorations en lecture seule, licences lues au fichier quand il
existe. Aucun dépôt cloné, aucune dépendance installée (règle de
`ACA-REUSE-1`). Quand la licence n'a pas été lue à la source, la fiche le
dit (« non vérifié »). Les étoiles et dates ne sont pas un critère : la
plupart de ces dépôts datent de 2026 et sont très jeunes.

## 2. Le paysage se sépare en deux pôles qui ne se rejoignent pas

| Pôle | Ce qu'il a | Ce qu'il n'a pas | Exemples |
|---|---|---|---|
| Tuteurs agentiques | l'agent, le chat, parfois FSRS | pas de provenance par carte, pas de journal append-only séparé, pas d'usine de contenu validé | DeepTutor (Apache-2.0), OpenTutor (MIT), Tutor MCP (MIT), Smart-Study-Agent (MIT), learning-mcp (MIT) |
| Bases sourcées / RAG | des citations, une traçabilité | pas de moteur de révision quotidien déterministe | Lunaris (AGPL-3.0), Anchor (MIT), groundly (MIT), SourceLens (MIT), Groundmap (Apache-2.0) |
| SRS classiques | un moteur mûr (FSRS-6) | ni agent, ni provenance, ni usine | Anki (AGPL-3.0), RemNote et Mochi (fermés), Obsidian Spaced Repetition (MIT) |

Aucun projet ne réunit les quatre invariants d'Académie : moteur
déterministe sans LLM, banque de cartes à provenance tamponnée, journal
d'état append-only séparé du contenu, usine locale documents vers unités
relues.

## 3. Les cinq candidats qui comptent, et ce qu'on en prend

| Dépôt | Licence (lue à la source) | Ce qui est vraiment réutilisable |
|---|---|---|
| [`wpwilson10/spacedrep`](https://github.com/wpwilson10/spacedrep) | MIT | La **boucle agent** : `get_next_card` puis notation 1-4 **choisie par l'agent, jamais demandée au joueur** ; `due_remaining` renvoyé à chaque carte (pacing) ; les 3 dernières revues (`user_answer` + `feedback`) renvoyées inline ; **enterrement automatique des cartes sœurs** clozes/reversed 24 h ; `preview_review` pour trancher hard/good ; erreurs JSON `{error, message, suggestion}` |
| [`ChenChenyaqi/learn-anything`](https://github.com/ChenChenyaqi/learn-anything) | MIT | Le **générateur d'adaptateurs multi-outils** (interface + registre + un formateur par outil) et un schéma `state.json` compact (domaines/concepts/statut/confiance/dernières dates) comme inspiration, à réécrire avec nos champs de provenance |
| [`vesperchinn/learn-anything-skill`](https://github.com/vesperchinn/learn-anything-skill) | MIT | La séparation **snapshot court + journal append-only** (`progress.md` + `progress-log.md`) et la **couche sources** : `claim_ledger`, `claims_to_verify`, `freshness_log`, marque `[unverified]`. Le plus proche de nos règles 3 et 4, mais sans script de verdict |
| [`Bhala-Srinivash/agent-tutor-skill`](https://github.com/Bhala-Srinivash/agent-tutor-skill) | MIT | Le **quiz sans indice** (quatre options, distracteurs qui sont de vrais concepts du domaine), le **séquençage des prérequis** avant d'avancer, et les **notes d'erreur** « Confusion / Point clé / Source » |
| [`FavioVazquez/agentic-learning`](https://github.com/FavioVazquez/agentic-learning) | MIT | Le **vocabulaire pédagogique** : `explain-first` (le joueur parle d'abord), `struggle` (échelle d'indices que le joueur déclenche), `interleave`, `cognitive-load` ; le feedback formatif et la citation honnête des sources primaires |

Deux autres à connaître sans copier : **Tutor MCP**
([`ArnaudGuiovanna/tutor-mcp`](https://github.com/ArnaudGuiovanna/tutor-mcp),
MIT) est le plus proche de notre philosophie « le moteur décide, le LLM ne
planifie pas » (FSRS + BKT + IRT côté moteur, en Go, alpha) ; et
**learning-mcp** ([`ryantthomas/learning-mcp`](https://github.com/ryantthomas/learning-mcp),
MIT) formule bien « la logique d'enseignement est une lib Python pure
servie par MCP », mais reste en SM-2 et sans banque sourcée.

## 4. À écarter, et pourquoi

- **AGPL-3.0** (contamination si on lie ou sert en réseau) : Anki, Logseq,
  Lunaris, vestige. Idées seulement, comme déjà noté pour Anki.
- **CC BY-SA 4.0** (copyleft sur le texte) : `GarethManning/education-agent-skills`.
  On re-dérive depuis les sources primaires, on ne copie pas le texte.
- **Apache-2.0** : carlosceja27/ai-tutor, DeepTutor, Groundmap. Compatible
  en principe, mais on n'en prend que des idées, pas du code.
- **Sans licence lisible** (à ne pas copier avant vérification à la
  source) : `johwiebe/anki-mcp`, `koganei/learn-anything-skill`,
  `YusenZhang0601/tutor`, `RoundTable02/tutor-skills`,
  `arashbehmand/learners-mcp`, `Yggdrasil Forge`, `Math Frontier`,
  `Sapient`.
- **Redondant** : toute implémentation FSRS parallèle (agent-tutor-skill,
  tylerbittner, SRSA) : nous avons déjà `app/planificateur.py`, et
  `py-fsrs` (MIT) reste l'oracle de comparaison.

## 5. Réponse à la question stratégique

Prendre un dépôt et arrêter reviendrait à sacrifier soit la provenance
tamponnée des cartes, soit le moteur déterministe, soit le journal
append-only. Ces trois-là sont l'intersection que personne n'implémente,
et c'est précisément ce qui distingue l'Académie. En revanche, l'interface
en chat est un problème déjà résolu ailleurs : on en reprend les patterns
(section 3) au lieu de l'inventer, et on publie notre propre consignes au
**standard AgentSkills** (`agentskills.io`, installable via `skills.sh`)
pour couvrir Claude Code, Cursor, Codex, Gemini, OpenCode et Antigravity
avec un seul fichier, plutôt que d'écrire trente formateurs.

## 6. Suite

Les reprises concrètes (adaptateurs, consignes sans indice, notes
d'erreur, couche sources, boucle agent) sont rattachées au cahier
[`ACA-SANS-FRONT-1`](../chantiers/ACA-SANS-FRONT-1.md). Les licences
restent à confirmer depuis le Mac avant toute copie de code, comme
l'exige `ACA-REUSE-1`.

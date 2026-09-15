# VEILLE — academie

Même format que `labor/lab/VEILLE.md` : une ligne par lien, quatre verdicts (PRIS, À ESSAYER, À CONNAÎTRE, ÉCARTÉ), append-only, verdict motivé en une phrase.

| Date | Ce que c'est | Verdict | Pourquoi / où |
|---|---|---|---|
| 03/09/2026 | Khan Academy Perseus (MIT) | À CONNAÎTRE | La notation par widget et la réponse partielle ; le rendu est couplé à leur contrat, pas au nôtre (ACA-REUSE-1) |
| 03/09/2026 | H5P, h5p-php-library | ÉCARTÉ | Licence lue à la source : GPL-3.0, pas MIT comme annoncé le 02/09. Idées seulement |
| 03/09/2026 | Oppia (Apache-2.0) | À CONNAÎTRE | L'exercice en pas avec relance sur l'erreur |
| 03/09/2026 | Kolibri (MIT) | À CONNAÎTRE | Le hors-ligne d'abord et la synchronisation par lots ; notre serveur fait déjà l'union |
| 03/09/2026 | Anki (AGPL-3.0), AnkiDroid (GPL-3.0) | ÉCARTÉ | Idées seulement, aucun code. Confirmé à la source |
| 03/09/2026 | ts-fsrs (MIT), py-fsrs (MIT), fsrs-optimizer (BSD-3) | PRIS | ts-fsrs en usage ; py-fsrs comme oracle ; l'optimiseur attend ACA-OPTIMISEUR-1 |
| 03/09/2026 | genanki (MIT) | PRIS | Outil d'usine pour ACA-EXPORT-1, jamais lié au client |
| 03/09/2026 | xyflow / React Flow (MIT) | ÉCARTÉ | C'est un éditeur de graphe ; l'arbre de l'Académie ne s'édite pas, il se conquiert |
| 03/09/2026 | d3-zoom, d3-hierarchy, d3-shape (ISC) | PRIS | Les briques de l'arbre maison : zoom, disposition de repli, courbes des liens |
| 03/09/2026 | elkjs (EPL-2.0, npm en double avec GPL-3.0), dagre (MIT) | ÉCARTÉ | 8 Mo et 845 Ko pour un placement que le programme porte déjà |
| 03/09/2026 | svg-pan-zoom (BSD-2), panzoom (MIT) | ÉCARTÉ | d3-zoom fait la même chose pour 87 Ko |
| 03/09/2026 | Plyr, Vidstack (MIT), wavesurfer.js (BSD-3) | À ESSAYER | Le type ecoute, pas avant ACA-MEDIA-1 |
| 03/09/2026 | Video.js (Apache-2.0), pdf.js (Apache-2.0), Excalidraw (MIT) | ÉCARTÉ | Hors budget client ; le PDF se lit à l'usine, le dessin se fait sur papier |
| 03/09/2026 | OCRmyPDF (MPL-2.0), tesseract (Apache-2.0), yt-dlp (Unlicense), faster-whisper (MIT) | PRIS | Outils d'usine sur le Mac, jamais liés au produit, aucun tiers appelé |
| 03/09/2026 | react-activity-calendar (MIT), cal-heatmap (MIT) | ÉCARTÉ | La heatmap tient en quarante lignes de SVG et la DA veut nos couleurs |
| 03/09/2026 | Tiptap (MIT), Milkdown (MIT) | À ESSAYER | La synthèse écrite commence en texte simple ; décidé à ACA-RESPONSE-1 |
| 03/09/2026 | Radix Primitives (MIT), shadcn/ui (MIT) | PRIS | Radix à la carte pour Ui.tsx, sans leur style ; shadcn se copie avec en-tête de provenance |
| 03/09/2026 | Lucide (ISC) | PRIS | Glyphes d'interface, import nommé seulement |
| 03/09/2026 | Phosphor, Iconoir, Tabler (MIT) | ÉCARTÉ | Une seule famille d'interface suffit |
| 03/09/2026 | game-icons (CC BY 3.0, CC0 pour certains contributeurs) | PRIS | Confirmé dans license.txt du dépôt ; attribution visible dans Crédits |
| 03/09/2026 | Rive, runtimes web et React (MIT) | À ESSAYER | Runtimes libres, éditeur propriétaire, les fichiers .riv restent à nous |
| 03/09/2026 | GSAP, Lottie | À CONNAÎTRE | Licences NON LUES : gsap.com et lottiefiles.com sont injoignables depuis le Cloud, et GSAP n'a pas de LICENSE dans son dépôt. À lire depuis le Mac avant tout usage |
| 03/09/2026 | Playwright (Apache-2.0) | À ESSAYER | Les tests de bout en bout qui manquent à web/ (ACA-FRONT-2) |
| 15/09/2026 | ChenChenyaqi/learn-anything, ZYQIO (MIT) | À ESSAYER | Le générateur d'adaptateurs multi-outils et un state.json compact ; ni provenance ni FSRS (ACA-SANS-FRONT-1) |
| 15/09/2026 | vesperchinn/learn-anything-skill (MIT) | À ESSAYER | Snapshot plus journal append-only et couche sources (claim_ledger, freshness_log) ; le plus proche de nos règles 3 et 4 |
| 15/09/2026 | Bhala-Srinivash/agent-tutor-skill (MIT) | À ESSAYER | Quiz sans indice, notes d'erreur Confusion/Point clé/Source, gate de prérequis ; FSRS artisanal à ignorer |
| 15/09/2026 | FavioVazquez/agentic-learning (MIT) | À ESSAYER | Vocabulaire explain-first, struggle en échelle d'indices, interleave, cognitive-load |
| 15/09/2026 | wpwilson10/spacedrep (MIT) | À ESSAYER | Boucle agent get_next_card puis notation, pacing, cartes sœurs enterrées, preview_review |
| 15/09/2026 | ArnaudGuiovanna/tutor-mcp (MIT), ryantthomas/learning-mcp (MIT) | À CONNAÎTRE | Le moteur décide et le LLM ne planifie pas ; lib Python pure servie par MCP ; alpha, sans banque sourcée |
| 15/09/2026 | OpenTutor, Smart-Study-Agent (MIT), DeepTutor (Apache-2.0) | À CONNAÎTRE | FSRS ou BKT côté app LLM-centrée ; ni provenance-contrat ni append-only |
| 15/09/2026 | Lunaris (AGPL-3.0), Anchor, groundly, SourceLens, Groundmap | ÉCARTÉ | Sourcing fort mais pas de SRS déterministe ; Lunaris AGPL |
| 15/09/2026 | GarethManning/education-agent-skills (CC BY-SA 4.0) | ÉCARTÉ | Copyleft sur le texte ; re-dériver depuis Cepeda 2006 |
| 15/09/2026 | johwiebe/anki-mcp, koganei/learn-anything-skill, YusenZhang0601/tutor, RoundTable02/tutor-skills, learners-mcp, Yggdrasil, Math Frontier, Sapient | ÉCARTÉ | Sans licence lisible ; ne rien copier avant vérification à la source |
| 15/09/2026 | Anki, Logseq, vestige (AGPL-3.0) | ÉCARTÉ | Copyleft réseau ; idées seulement, confirmé à la source |

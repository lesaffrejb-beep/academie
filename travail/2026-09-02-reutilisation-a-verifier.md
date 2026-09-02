# Réutilisation : les dépôts à regarder avant d'écrire du code (02/09/2026)

Brief JB : « aller voir si on peut s'appuyer sur des repos open source
qui feraient des choses déjà faites ; reprendre le code pour en être
maître, l'adapter à nos besoins et à notre esprit ». Ce fichier est la
**liste des candidats**, pas le benchmark : chaque licence ci-dessous
est **à vérifier à la source le jour de l'adoption**
(`labor/wiki/patterns/licence-outil-avant-fonctionnalite.md`). Le
benchmark du 30/08 (`benchmark-2026-08-30.md`) a déjà vérifié une
partie ; le chantier `ACA-REUSE-1` fait le reste et rend un verdict par
ligne : **reprendre le code**, **voler le pattern**, **écarter**.

Règle de reprise : on copie avec un en-tête de provenance
(`// repris de <dépôt>@<sha> le AAAA-MM-JJ, licence X`), on adapte au
contrat et à la direction artistique, on n'importe jamais un framework
d'apprentissage entier. AGPL et GPL : idées seulement.

## Exercices et rendu d'apprentissage

| Candidat | Ce qu'il fait | Licence annoncée (à vérifier) | Intérêt |
|---|---|---|---|
| Khan Academy Perseus | moteur de rendu et d'édition d'exercices : choix multiples, appariement, tri, numérique, avec notation | MIT | le plus proche de nos types `qcm`, `relier`, `datation` ; à lire pour les patterns d'interaction et de notation, peut-être reprendre des widgets |
| H5P (core et types de contenu) | glisser-déposer, texte à trous, appariement, questions sur image, « hotspots » | MIT (core), types variés | patterns pour `photo` (zones sur image), `relier`, `plan` |
| Oppia | plateforme d'« explorations » interactives | Apache-2.0 | pattern de l'exercice en pas (`cas`) |
| Kolibri (Learning Equality) | plateforme d'apprentissage hors-ligne | MIT | pattern hors-ligne d'abord, synchronisation |
| Anki, AnkiDroid | répétition espacée, formats de cartes | AGPL / GPL | **idées seulement** (déjà tranché le 30/08) |
| ts-fsrs, py-fsrs, fsrs-optimizer | FSRS | MIT / MIT / BSD-3 | **reprendre** (déjà vérifié le 30/08) |
| genanki | export `.apkg` | MIT | **reprendre** à `ACA-EXPORT-1` |

## Le graphe, l'arbre, les cartes

| Candidat | Ce qu'il fait | Licence annoncée | Intérêt |
|---|---|---|---|
| xyflow (React Flow) | graphes de nœuds interactifs, zoom, mini-carte | MIT | base possible de l'arbre ; à peser contre du SVG maison (DA §3) |
| d3 (d3-zoom, d3-hierarchy, d3-shape) | zoom, disposition d'arbres, courbes | ISC | les briques de l'arbre maison |
| elkjs, dagre | disposition automatique de graphes orientés | EPL-2.0 / MIT | le placement de repli quand `disposition` manque |
| svg-pan-zoom, panzoom | zoom et déplacement SVG | BSD-2 / MIT | déjà notés le 30/08 |

## Lecteurs et médias

| Candidat | Ce qu'il fait | Licence annoncée | Intérêt |
|---|---|---|---|
| Plyr, Vidstack, Video.js | lecteur vidéo et audio accessible | MIT / MIT / Apache-2.0 | le type `ecoute` et les replays (plus tard) |
| wavesurfer.js | forme d'onde audio | BSD-3 | l'écoute avec repères |
| pdf.js | rendu de PDF dans le navigateur | Apache-2.0 | le type `lecture` sur un document public |
| Excalidraw | dessin à main levée dans le navigateur | MIT | option pour `dessin` sur ordinateur, à peser contre le papier |
| ocrmypdf, tesseract, poppler | OCR et extraction de texte | MPL-2.0 / Apache-2.0 / GPL (outil, pas lié) | l'usine |
| yt-dlp, faster-whisper | sous-titres, transcription locale | Unlicense / MIT | l'usine |

## Profil, régularité, journal, éditeur

| Candidat | Ce qu'il fait | Licence annoncée | Intérêt |
|---|---|---|---|
| react-activity-calendar, cal-heatmap | calendrier de régularité | MIT | la heatmap du profil (ou 40 lignes de SVG, déjà noté le 30/08) |
| Tiptap, Milkdown | éditeur de texte riche | MIT | la synthèse écrite et la réponse libre |
| Radix Primitives, shadcn/ui | composants accessibles (feuilles, onglets, dialogues) | MIT | la base d'`Ui/` sans reprendre leur style |
| Motion | animations | MIT | déjà tranché |
| Dexie | IndexedDB | Apache-2.0 | déjà tranché |

## Classement, cercles, ligue

Rien de convaincant en open source qui ne soit pas un réseau social
entier ; la ligue est trois requêtes SQL et un tableau. **Voler le
pattern** de Strava (fil de jalons, kudos, partage manuel) et de Duolingo
(ligue hebdomadaire, sa propre ligne en avant), écrire le code.

## Contenu et données

| Candidat | Ce qu'il fait | Licence | Intérêt |
|---|---|---|---|
| API PISTE Légifrance, API Judilibre | textes et arrêts | ouvertes (compte) | l'usine, la veille (déjà câblées dans labor) |
| Duolingo halflife-regression (jeu de données) | 13 M de traces | MIT | valider les calculs statistiques avant d'avoir nos propres traces (noté le 30/08) |
| game-icons.net | glyphes | CC BY 3.0 | déjà repris, attribution visible |
| Kenney, Poly Haven, Quaternius | assets 3D | CC0 | seulement si la 3D revient un jour |

## Ce que le chantier `ACA-REUSE-1` doit rendre

Un tableau par ligne avec la licence lue à la source et sa date, le
verdict, et pour chaque « reprendre le code » : le fichier de
provenance, la taille ajoutée au bundle, et ce qu'on a adapté. Rien
n'est installé avant ce tableau.

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

---

# VERDICTS, chantier `ACA-REUSE-1` (03/09/2026)

Chaque licence ci-dessous a été **lue dans le fichier `LICENSE` du dépôt
lui-même**, à l'URL donnée, le 03/09/2026. Aucun badge GitHub, aucune
mémoire de modèle, aucune page d'agrégateur. Les licences déclarées dans
le registre npm ont servi de contre-épreuve : quand les deux divergent,
c'est écrit.

**Poids** : la colonne donne le **paquet npm décompressé**
(`registry.npmjs.org`, version courante du 03/09/2026). Ce n'est pas la
taille ajoutée au bundle gzippé : ce cahier interdit `npm install` et
toute écriture dans `web/`. Le poids gzippé réel se mesure au moment de
l'adoption, dans `ACA-FRONT-2`, contre le budget de 400 Ko
(`decisions/0007`). Le paquet décompressé sert à écarter d'emblée ce qui
est manifestement hors budget.

## Deux corrections à la liste des candidats

1. **H5P n'est pas MIT.** `h5p/h5p-php-library/LICENSE.txt` est la **GNU
   GPL version 3**. La ligne « MIT (core) » du 02/09 était fausse. H5P
   passe donc en **idées seulement**, au même rang qu'Anki. C'est la
   raison d'être de la règle « pas de verdict de mémoire ».
2. **wavesurfer.js est BSD-3-Clause** (le fichier le dit en toutes
   lettres), et **AnkiDroid est GPL-3.0**, pas AGPL. **elkjs** est en
   double licence : son `LICENSE.md` est l'**EPL-2.0**, son paquet npm
   déclare `EPL-2.0 OR GPL-3.0-or-later`.

## Exercices et rendu d'apprentissage

| Candidat | Licence lue le 03/09 | URL lue | Poids npm | Verdict |
|---|---|---|---|---|
| Khan Academy Perseus | MIT | `raw.githubusercontent.com/Khan/perseus/main/LICENSE` | monorepo | **voler le pattern** : la notation par widget et la validation d'une réponse partielle. Le rendu est couplé à leur contrat de contenu, pas au nôtre |
| H5P (h5p-php-library) | **GPL-3.0** | `.../h5p/h5p-php-library/master/LICENSE.txt` | PHP | **idées seulement** : zones sur image et appariement. Aucun code |
| Oppia | Apache-2.0 | `.../oppia/oppia/master/LICENSE` | plateforme | **voler le pattern** : l'exercice en pas, avec relance sur l'erreur |
| Kolibri | MIT | `.../learningequality/kolibri/master/LICENSE` | plateforme | **voler le pattern** : hors-ligne d'abord, synchronisation par lots. Notre `serveur/` fait déjà l'union |
| Anki | **AGPL-3.0 ou ultérieure** | `.../ankitects/anki/main/LICENSE` | app | **idées seulement** (déjà tranché le 30/08) |
| AnkiDroid | **GPL-3.0** | `.../ankidroid/Anki-Android/main/COPYING` | app | **idées seulement** |
| ts-fsrs | MIT | `.../open-spaced-repetition/ts-fsrs/main/LICENSE` | 706 Ko | **repris** : déjà dans `web/LICENCES.md`. Le miroir écrit à la main dans `web/src/moteur/fsrs.ts` reste la référence, la parité est testée |
| py-fsrs | MIT | `.../open-spaced-repetition/py-fsrs/main/LICENSE` | PyPI | **écarter de la production** : `app/planificateur.py` est maison et testé. Gardé comme oracle de comparaison |
| fsrs-optimizer | BSD-3-Clause | `.../open-spaced-repetition/fsrs-optimizer/main/LICENSE` | PyPI | **à connaître**, pour `ACA-OPTIMISEUR-1` seulement (quatre cents révisions) |
| genanki | MIT | `.../kerrickstaley/genanki/main/LICENSE.txt` | PyPI | **reprendre** à `ACA-EXPORT-1`. Outil d'usine, jamais lié au client |

## Le graphe, l'arbre, les cartes

L'arbre est **dessiné**, pas disposé à l'exécution : le programme porte
déjà la disposition. Ce qu'on cherche ici, c'est le zoom et les courbes,
pas un moteur de graphe.

| Candidat | Licence lue le 03/09 | URL lue | Poids npm | Verdict |
|---|---|---|---|---|
| xyflow (React Flow) | MIT | `.../xyflow/xyflow/main/LICENSE` | 1,2 Mo | **écarter** : c'est un éditeur de graphe (nœuds déplaçables, poignées, mini-carte). L'arbre de l'Académie ne s'édite pas, il se conquiert |
| d3-zoom | ISC | `.../d3/d3-zoom/main/LICENSE` | 87 Ko | **reprendre** : le zoom et le déplacement de l'arbre |
| d3-hierarchy | ISC | `.../d3/d3-hierarchy/main/LICENSE` | 136 Ko | **reprendre** : disposition de repli quand une branche n'a pas de `disposition` |
| d3-shape | ISC | `.../d3/d3-shape/main/LICENSE` | 247 Ko | **reprendre** : les courbes des liens entre nœuds |
| elkjs | **EPL-2.0** (npm : `EPL-2.0 OR GPL-3.0-or-later`) | `.../kieler/elkjs/master/LICENSE.md` | 8,0 Mo | **écarter** : 8 Mo pour un placement qu'on ne calcule pas à l'exécution |
| dagre | MIT | `.../dagrejs/dagre/master/LICENSE` | 845 Ko | **écarter** : même motif ; `d3-hierarchy` suffit au repli |
| svg-pan-zoom | BSD-2-Clause | `.../bumbu/svg-pan-zoom/master/LICENSE` | 2,0 Mo | **écarter** : `d3-zoom` fait la même chose pour 87 Ko |
| panzoom | MIT | `.../anvaka/panzoom/main/LICENSE` | 719 Ko | **écarter** : même motif |

## Lecteurs et médias

Rien de tout cela n'entre avant `ACA-MEDIA-1`. Les licences sont lues
maintenant pour que le chantier n'ait plus à le faire.

| Candidat | Licence lue le 03/09 | URL lue | Poids npm | Verdict |
|---|---|---|---|---|
| Plyr | MIT | `.../sampotts/plyr/master/LICENSE.md` | 5,3 Mo | **à connaître** : candidat du type `ecoute` |
| Vidstack | MIT | `.../vidstack/player/main/LICENSE` | monorepo | **à connaître** : même case, plus moderne |
| Video.js | Apache-2.0 | `.../videojs/video.js/main/LICENSE` | lourd | **écarter** : trop gros pour de l'audio de chapitre |
| wavesurfer.js | **BSD-3-Clause** | `.../katspaugh/wavesurfer.js/main/LICENSE` | 1,4 Mo | **à connaître** : l'écoute avec repères, si le podcast de chapitre existe un jour |
| pdf.js | Apache-2.0 | `.../mozilla/pdf.js/master/LICENSE` | 34,8 Mo | **écarter du client** : l'usine lit les PDF sur le Mac et le type `lecture` sert le pivot Markdown, pas le PDF |
| Excalidraw | MIT | `.../excalidraw/excalidraw/master/LICENSE` | 46,8 Mo | **écarter** : le `dessin` se fait sur papier (`ACA-PAPIER-1`), pas dans le navigateur |
| OCRmyPDF | **MPL-2.0** | `.../ocrmypdf/OCRmyPDF/main/LICENSE` | PyPI | **pris pour l'usine**, sur le Mac, jamais lié au produit |
| tesseract | Apache-2.0 | `.../tesseract-ocr/tesseract/main/LICENSE` | binaire | **pris pour l'usine**, même conduite |
| yt-dlp | Unlicense | `.../yt-dlp/yt-dlp/master/LICENSE` | binaire | **pris pour l'usine** |
| faster-whisper | MIT | `.../SYSTRAN/faster-whisper/master/LICENSE` | PyPI | **pris pour l'usine** : transcription locale, aucun tiers |

## Profil, régularité, journal, éditeur

| Candidat | Licence lue le 03/09 | URL lue | Poids npm | Verdict |
|---|---|---|---|---|
| react-activity-calendar | MIT | `.../grubersjoe/react-activity-calendar/main/LICENSE` | 178 Ko | **écarter** : la heatmap tient en quarante lignes de SVG (déjà noté le 30/08), et la DA veut nos couleurs |
| cal-heatmap | MIT | `.../wa0x6e/cal-heatmap/master/LICENCE` | 6,9 Mo | **écarter** : hors budget pour un carré par jour |
| Tiptap | MIT | `.../ueberdosis/tiptap/main/LICENSE.md` | 2,9 Mo (core seul) | **à connaître**, décidé à `ACA-RESPONSE-1` : la synthèse écrite commence en texte simple |
| Milkdown | MIT | `.../Milkdown/milkdown/main/LICENSE` | monorepo | **écarter** : même case que Tiptap, sans avantage |
| Radix Primitives | MIT | `.../radix-ui/primitives/main/LICENSE` | 99 Ko par primitive | **reprendre à la carte** : seulement les primitives dont `web/src/ecrans/Ui.tsx` a besoin (dialogue, onglets), jamais le paquet entier, jamais leur style |
| shadcn/ui | MIT | `.../shadcn-ui/ui/main/LICENSE.md` | copier-coller | **voler le pattern** : c'est du code à copier par construction, pas une dépendance. En-tête de provenance obligatoire |
| Motion | MIT | `.../motiondivision/motion/main/LICENSE.md` | 718 Ko | **repris** (déjà tranché) |
| Dexie | Apache-2.0 | `.../dexie/Dexie.js/master/LICENSE` | 3,2 Mo | **repris** (déjà tranché, en usage dans `web/src/moteur/journal.ts`) |

## Icônes et animation

| Candidat | Licence lue le 03/09 | URL lue | Poids npm | Verdict |
|---|---|---|---|---|
| Lucide | ISC | `.../lucide-icons/lucide/main/LICENSE` | 31,8 Mo (paquet entier, import par icône) | **repris** : les glyphes d'interface. Import nommé seulement, jamais le paquet |
| Phosphor Icons | MIT | `.../phosphor-icons/core/main/LICENSE` | 33,0 Mo | **écarter** : une seule famille d'interface |
| Iconoir | MIT | `.../iconoir-icons/iconoir/main/LICENSE` | 6,4 Mo | **écarter** : même motif |
| Tabler Icons | MIT | `.../tabler/tabler-icons/main/LICENSE` | 66,0 Mo | **écarter** : même motif |
| game-icons | **CC BY 3.0, ou CC0 pour certains contributeurs** | `.../game-icons/icons/master/license.txt` | assets | **repris** : les glyphes de chapitre, attribution visible dans Crédits |
| Rive (rive-react, rive-wasm) | MIT (les deux runtimes) | `.../rive-app/rive-react/main/LICENSE` et `.../rive-app/rive-wasm/master/LICENSE` | 48 Ko (react) | **à connaître** : les runtimes sont libres, l'éditeur est propriétaire et les `.riv` sont à nous |
| GSAP | **à vérifier** | non lue : le dépôt `greensock/GSAP` n'a pas de fichier `LICENSE` à sa racine, et `gsap.com` est injoignable depuis l'environnement Cloud (proxy, 403) | 6,3 Mo | **suspendu** : le registre npm déclare « Standard 'no charge' license: https://gsap.com/standard-license », ce n'est pas une licence OSI et le texte n'a pas été lu. À lire depuis le Mac avant tout usage. Motion (MIT) couvre le besoin en attendant |
| Lottie / LottieFiles | **à vérifier** | non lue : `lottiefiles.com` injoignable depuis le Cloud | assets | **suspendu**, même motif. Chaque fichier porterait sa mention |

## Outillage du client, déjà en place

| Candidat | Licence lue le 03/09 | URL lue | Verdict |
|---|---|---|---|
| vite-plugin-pwa | MIT | `.../vite-pwa/vite-plugin-pwa/main/LICENSE` | **repris** (en usage) |
| Workbox | MIT | `.../GoogleChrome/workbox/main/LICENSE` | **repris** (via le plugin) |
| Playwright | Apache-2.0 | `.../microsoft/playwright/main/LICENSE` | **à prendre** pour les tests de bout en bout qui manquent à `web/` |

## Ce qui reste à faire à la main, hors Cloud

Deux licences n'ont pas pu être lues à leur source depuis cet
environnement : **GSAP** et **Lottie**. Le proxy sortant refuse
`gsap.com` et `lottiefiles.com`, et GSAP ne publie pas de fichier de
licence dans son dépôt. Elles restent « à vérifier », pas « libres ».
Tant que le texte n'est pas lu depuis le Mac, ni l'une ni l'autre
n'entre dans `web/`.

## Aucune AGPL en code

Vérifié sur les 48 dépôts lus ce jour : la seule AGPL est **Anki**
(les deux autres AGPL du domaine, Anki Review Heatmap et
exercism/website, avaient été relevées le 30/08 et sont déjà écartées).
**H5P** et **AnkiDroid** sont GPL, ce qui est le même refus pour du code
lié. Aucune de ces quatre n'est retenue autrement qu'en idées, et aucun
« reprendre » de ce tableau n'est sous une licence à contamination.

## Banques d'éléments 2026 (ajouté le 03/09/2026, licences lues en ligne le jour même)

| Candidat | Ce que c'est | Licence lue le 03/09 | Verdict |
|---|---|---|---|
| GSAP (et ses plugins ScrollTrigger, SplitText, MorphSVG, DrawSVG) | animation JavaScript | gratuit pour tout usage y compris commercial depuis avril 2025 (licence « no charge » de GSAP, pas une licence OSI) | **utilisable** pour les moments de conquête (anneau, brouillard, insigne qui se dessine) ; Motion reste la base ; ne pas empiler les deux |
| Rive (runtimes web, React) | animations vectorielles interactives | runtimes MIT ; éditeur propriétaire | **à considérer** pour les insignes animés ; les fichiers .riv sont à nous |
| Lottie / LottieFiles | animations vectorielles JSON | Lottie Simple License sur les animations du site : usage commercial libre, attribution encouragée, dérivés sous les mêmes termes, pas de compilation en bibliothèque concurrente | **utilisable** au cas par cas, chaque fichier avec sa mention ; préférer nos propres SVG animés |
| Phosphor, Iconoir, Tabler, Lucide | icônes d'interface | MIT, MIT, MIT, ISC | **reprendre** l'une d'elles pour l'interface ; game-icons (CC BY) reste pour les glyphes de chapitre |
| Open Peeps (Pablo Stanley) | illustrations de personnages | CC0 | écarté par la DA (pas de personnage) ; noté pour un autre métier scolaire |
| unDraw | illustrations | licence propre : gratuit, sans attribution, pas de redistribution en bibliothèque, pas d'entraînement de modèle | **écarté** : style générique, contraire à « la planche » |
| Radix Primitives, Base UI, Ark UI | composants accessibles sans style | MIT | **reprendre** l'un d'eux pour `Ui/` (feuilles, onglets, dialogues) |
| auto-animate (FormKit) | transitions de listes en une ligne | MIT | **utilisable** pour les listes (file de la boîte, fil du cercle) |
| Fraunces, Source Sans 3, JetBrains Mono | polices | OFL | **reprendre**, auto-hébergées |
| Kenney (sons d'interface) | sons | CC0 | quatre sons discrets au plus, coupés par défaut |

## Outils d'ingestion (ajouté le 03/09/2026, à vérifier à la source au chantier ACA-INGESTION-1)

| Candidat | Ce qu'il fait | Licence annoncée (à vérifier) | Verdict provisoire |
|---|---|---|---|
| poppler (`pdftotext`, `pdftohtml`, `pdftoppm`, `pdfimages`) | texte, structure, rendu, images | GPL, utilisé en ligne de commande, jamais lié | **la base**, testée le 03/09 |
| ocrmypdf, tesseract | OCR d'un PDF sans couche texte | MPL-2.0, Apache-2.0 | **à installer** le jour d'un PDF scanné |
| docling (IBM) | mise en page, tableaux, figures vers Markdown | MIT | **à essayer** si poppler plus vision ne suffit pas sur les tableaux |
| marker, MinerU, PyMuPDF | conversion PDF vers Markdown | GPL / AGPL / AGPL | idées seulement ; pas dans le produit |
| pdfplumber, pypdf | extraction Python | MIT, BSD | admis si un script en a besoin |
| faster-whisper, yt-dlp | transcription locale, sous-titres | MIT, Unlicense | l'usine, pour les vidéos |
| Firecrawl | crawl et extraction web | AGPL (cœur), API payante | **écarté** : pas de crawl ; lecture directe des domaines fiables |
| L'entrée PDF native de l'API Claude (600 pages, citations par page) | lecture par le modèle | service | **à titre indicatif** : JB travaille sur abonnement ; dans Claude Code, la lecture de PDF par pages rendues fait le même travail |

# Comparaison des outils : capacité documentée ≠ résultat sur nos PDF

06/09/2026 — Codex / GPT-6. Sources primaires consultées à cette date.
Le mot « top » ne désigne pas un classement universel : extraction native,
OCR, structure de tableaux et compréhension d'une figure sont des tâches
différentes. `BENCHMARK.md` et `BENCHMARK-STRUCTURE.md` décrivent les
performances mesurées ici. `RECHERCHE-ET-COUTS.md` ajoute benchmarks publics
et budget conditionnel Luna/API/abonnement.

## Extracteurs effectivement essayés

| Outil / famille | Rôle utile | Limite décisive | Place retenue |
|---|---|---|---|
| Poppler `pdftotext -layout` / `-raw` | Lire la couche texte, conserver une extraction témoin locale | L'ordre PDF peut être mauvais ; texte masqué et texte dans une image ne sont pas correctement distingués dans tous nos cas | Première passe rapide, pas arbitre du visible |
| PyMuPDF, texte brut / trié | Extraction et accès aux pages ; autre ordre de lecture | Aucun OCR activé dans l'essai ; le tri peut dégrader certaines relations ; licence distincte à traiter avant intégration | Comparateur hors produit |
| pypdf, `plain` / `layout` | Extraction Python, manipulation de pages pour l'essai | Ce n'est pas un OCR ; ordre et espacements restent dépendants du PDF | Second avis léger sur pages signalées |
| pdfplumber | Texte et objets géométriques ; extraction de tables configurable | Les réglages et la structure réelle comptent ; ne donne pas la vérité du document | Candidat de diagnostic/cellules ; seul `extract_text()` a été mesuré ici |
| Microsoft MarkItDown 0.1.7 | Conversion de formats vers Markdown, tables selon son convertisseur | Notre essai sans plugin ni client LLM conserve des parasites, invente une structure tabulaire sur une page et manque les scans | Candidat, pas nouveau défaut global |

Documentation : [PyMuPDF, texte et ordre](https://pymupdf.readthedocs.io/en/latest/recipes-text.html),
[pypdf, limites de l'extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html),
[pdfplumber](https://github.com/jsvine/pdfplumber),
[MarkItDown](https://github.com/microsoft/markitdown).
Pour Poppler, les options et la version proviennent du binaire local et de
`app/usine/pivot.py` ; le comportement rapporté provient des fichiers d'essai.

MarkItDown est un outil Microsoft open source, pas le service Azure Document
Intelligence. Le README actuel documente un plugin OCR utilisant un client
LLM ; sans client il peut rester sans OCR. Il décrit aussi des intégrations
Azure facturées. Ces variantes ne sont pas celles mesurées. La version
installée localement s'appuie dans son convertisseur PDF sur pdfplumber et
pdfminer ; ce n'est donc pas un avis totalement indépendant de ces moteurs.
[README et options](https://github.com/microsoft/markitdown).

## Moteurs de structure / OCR : documentation et état des essais

Extension après la demande de JB : PyMuPDF4LLM 1.28.2, Docling 2.126.0 avec
RapidOCR 3.9.2 (hybride et pleine page) et pdf-inspector 1.17.0 sans OCR ont
été exécutés sur les six pages. Résultats et options dans
`BENCHMARK-STRUCTURE.md`. Les autres lignes ci-dessous restent non mesurées.

| Outil | Ce que sa documentation décrit | Pourquoi le considérer | Pourquoi ne pas le déclarer gagnant |
|---|---|---|---|
| Docling, initié chez IBM | Ordre de lecture, structure, tableaux, exports JSON/Markdown et OCR ; exécution locale possible | OCR et structure essayés sur Angers/PDHH | Les deux options testées manquent encore des témoins ; pleine page ne garantit pas suppression de toute couche native parasite |
| OCRmyPDF + moteur OCR (dont Tesseract selon configuration) | Création/réparation d'une couche OCR ; modes skip/redo/force | Traiter un scan ou une couche OCR défectueuse dans un dérivé | Ce n'est ni un moteur pédagogique ni un lecteur fiable de toutes les tables ; attention aux pages mixtes et à la rasterisation |
| Marker | Conversion structurée, OCR et options hybrides ; plusieurs modes | Candidat pour tableaux, formules et pages complexes | Code et poids ont des licences différentes ; appels LLM optionnels et environnement d'inférence à maîtriser |
| MinerU / PDF-Extract-Kit | Conversion de documents pour MinerU ; boîte de modèles de mise en page/OCR/formules pour PDF-Extract-Kit | Candidat de traitement spécialisé | Boîte de composants ≠ produit prêt à intégrer ; lire la licence exacte et celle des poids, mesurer sur le français du corpus |
| Microsoft Table Transformer (TATR) | Détection et structure de tables ; texte fourni séparément par extraction/OCR | Référence spécialisée pour les cellules et leur structure | Ce n'est pas un convertisseur PDF complet ni un OCR autonome |
| olmOCR / olmOCR-bench | Linéarisation de documents et banc de tests de phénomènes PDF | Référence pour construire des épreuves plus riches que la présence de mots | Matériel et modèle non installés ; benchmark public ≠ certification de nos documents |

Sources : [Docling](https://docling-project.github.io/docling/),
[OCR pleine page Docling](https://docling-project.github.io/docling/_generated/examples/full_page_ocr/),
[OCRmyPDF](https://ocrmypdf.readthedocs.io/en/latest/cookbook.html),
[Marker](https://github.com/datalab-to/marker),
[MinerU](https://github.com/opendatalab/mineru),
[PDF-Extract-Kit](https://github.com/opendatalab/PDF-Extract-Kit),
[TATR](https://github.com/microsoft/table-transformer),
[olmOCR](https://github.com/allenai/olmocr).

Les chiffres de performance des README ne sont pas recopiés comme nos
résultats. Code ouvert ne signifie ni poids sans restriction, ni calcul
gratuit, ni qualité prouvée en français. L'environnement structuré et les
poids locaux occupent environ 2 Go au relevé ; ils sont dans un répertoire
temporaire dédié, pas dans les dépendances du produit. Environ 10 Gio libres
sur le Mac : ne pas multiplier les poids lourds sans vérifier la place.

## Firecrawl : utile, mais à la bonne étape

Firecrawl documente la collecte web et un endpoint de parsing de documents,
avec Markdown par page, blocs de mise en page et OCR de secours. Les sorties
par page/bloc sont pertinentes pour une attribution vérifiable. Il faut
contrôler `numPages` contre `totalPages` : un plafond peut tronquer la sortie.
[Documentation Parse](https://docs.firecrawl.dev/features/parse).

Pour nos trois fichiers déjà locaux, un upload supplémentaire n'est pas
nécessaire. Aucun PDF envoyé au cloud Firecrawl, aucun crédit
consommé par le banc. Son composant local
[pdf-inspector](https://github.com/firecrawl/pdf-inspector) a été essayé
séparément, sans activer son OCR. Le parsing cloud documenté et une installation
auto-hébergée ne doivent pas être présumés équivalents sans vérifier leurs
composants. Pas de classement de fiabilité de Firecrawl sur ce corpus.

## « pdf2… » : préciser le moteur, pas seulement l'extension de sortie

PDF→texte, PDF→Markdown, PDF→Word et PDF→image ne sont pas la même promesse.
« pdf2 » ne suffit pas à identifier un produit ou une version. Le banc est
ouvert à un autre convertisseur : lui faire produire une sortie par page,
enregistrer version/options/temps et la passer sur **les mêmes témoins**,
puis sur un échantillon neuf avec une référence indépendante.

Un outil PDF→Markdown peut sortir un tableau syntaxiquement valide mais
faux. Une image correctement rendue n'a encore ni texte OCR ni interprétation.
Une sortie plus longue peut contenir davantage de parasites. Le choix se
fait par défaut à traiter et coût de reprise, pas par nom à la mode.

## Choix opérationnel

Garder Poppler comme extraction témoin déjà disponible. Comparer à faible
coût les pages signalées. Les premiers essais Docling/OCR sont désormais
effectués, mais insuffisants pour remplacer une étape globalement. Réserver la vision générale aux
figures, chiffres litigieux et cas non résolus. Distinguer ce choix de
présélection d'une victoire générale de Docling, que nous n'avons pas.

La vision utilisée dans cette conversation est une lecture par le modèle,
pas un moteur OCR versionné et benchmarké. Sa durée de lecture et son coût
tokens ne sont pas mesurés. Elle sert à établir les premiers témoins,
lesquels exigent eux aussi une revue indépendante.

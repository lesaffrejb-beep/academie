# Complément local : structure et OCR

06/09/2026 — Codex / GPT-6. Suite réelle du premier banc, pas une comparaison
des seuls README. Même manifeste : six pages difficiles et vingt témoins.
Ce ne sont ni vingt pages, ni des pourcentages de fiabilité générale.

| Configuration | Version | Témoins satisfaits / 20 | Limite constatée |
|---|---|---:|---|
| PyMuPDF4LLM, modèle de layout, `use_ocr=False` | 1.28.2 | 16 | Les témoins de parasites passent, mais tampon et corps scannés restent manquants |
| Docling + RapidOCR, mode DEFAULT, tables activées | 2.126.0 / 3.9.2 | 16 | Retrouve les témoins scannés ; conserve des parasites sur Angers 9/12 et Focus 32 |
| Docling + RapidOCR, mode FULL_PAGE, tables activées | 2.126.0 / 3.9.2 | 17 | Mélange une phrase sur Angers 12 ; conserve les parasites Focus 32 |
| Firecrawl pdf-inspector, `extract_pages_markdown`, sans OCR | 1.17.0 | 8 | Ordre/parasites encore présents et sortie vide sur PDHH 6 |

Les vingt-quatre extractions ont abouti. Une sortie vide est conservée avec
ses témoins en échec, pas considérée comme une page correcte. Ces variantes
s'ajoutent aux huit configurations natives de `BENCHMARK.md` ; elles ne sont
pas indépendantes statistiquement. Aucun outil n'est déclaré gagnant global.

Point important : **FULL_PAGE est le nom d'une option de Docling, pas la
preuve d'une chaîne exclusivement fondée sur le visible.** Le PDF original
est toujours l'entrée. Pour tester cette autre hypothèse, il faudra un dérivé
rasterisé contrôlé, sans couche native, ou un OCR direct de l'image.

## Preuves et reproduction

Rapports intégraux et Markdown par page, hors git :

- `sources/benchmark-pdf/2026-09-06-structure-pymupdf4llm-02/`
- `sources/benchmark-pdf/2026-09-06-structure-docling-02/`
- `sources/benchmark-pdf/2026-09-06-structure-docling-ocr-02/`
- `sources/benchmark-pdf/2026-09-06-structure-firecrawl-01/`

Ces passes finales conservent une copie du script, du comparateur et des
témoins ainsi que leurs empreintes. Les premiers essais `01` sont conservés
également ; avant l'ajout de l'archivage du code, leurs scripts n'étaient pas
copiés dans le dossier. Ne pas confondre leurs hashes avec le script actuel.
Résumé partageable : `benchmark-structure-resultats.json`.

```sh
python3 travail/expertise-2026-09-06/test_benchmark_structure.py
HF_HOME=CHEMIN-CACHE-HF XDG_CACHE_HOME=CHEMIN-CACHE-LOCAL OMP_NUM_THREADS=2 \
  CHEMIN-PYTHON-STRUCTURE travail/expertise-2026-09-06/benchmark_structure.py \
  --moteur docling-hybride --out sources/benchmark-pdf/NOUVEL-ESSAI
```

Remplacer les chemins ; moteurs possibles : `pymupdf4llm`, `docling-hybride`,
`docling-ocr`, `pdf-inspector`. `HF_HUB_OFFLINE=1` a été ajouté aux passes
Docling finales, après chargement des poids. Les modèles RapidOCR sont
présents dans l'environnement installé ; le script interdit services
distants et plugins externes Docling. Aucun PDF n'est envoyé à une API.

Environnement : `/private/tmp/academie-pdf-bench.uNpd2O/structure/bin/python`,
Python 3.12, venv avec runtime Codex de base partagé en lecture. Principales
dépendances : PyMuPDF/layout 1.28.2, docling-core 2.95.0, docling-ibm-models
4.0.2, docling-parse 7.17.0, RapidOCR 3.9.2, ONNX Runtime 1.29.0,
Torch 2.14.0, Transformers 5.16.1. RapidOCR charge PP-OCRv6 det/rec small et
le classifieur ch_ppocr_mobile_v2.0. Paramètres français non optimisés :
configuration OCR livrée par défaut, pas un essai du meilleur réglage français.

Les durées par page sont dans les rapports. Une initialisation par moteur,
poids téléchargés à la première conversion Docling puis cache chaud : **ne
pas comparer ces temps au banc natif qui relance un processus par page**.
Pas de répétitions suffisantes pour annoncer un débit. Les poids ne sont
pas tous inventoriés par hash : une réinstallation future peut différer ;
il faut figer cet inventaire avant une qualification de production.

Garde-fous : sources SHA-256 contrôlées avant calcul ; répertoire de sortie
neuf ; erreur d'import/exécution signalée, code de sortie non nul si erreur ;
réserve de 8 Gio libres contrôlée avant moteur puis chaque page. Ce contrôle
n'est pas un quota pendant téléchargement. Pas de dépendance applicative,
original, état joueur ou sceau usine modifié. Trois tests rouges puis verts
couvrent résultat absent, résultat vide et réserve disque.

## Ce qui reste réellement à tester

Marker, MinerU, PaddleOCR-VL, GLM-OCR, olmOCR, Tesseract/OCRmyPDF, TATR et
l'OCR de pdf-inspector : **non exécutés sur ce lot**. API Luna/Terra/Sol,
Mistral OCR, Azure Document Intelligence et Firecrawl cloud : **non appelées**.
Il serait faux de dire « toutes les meilleures options testées ».

Les environnements et poids d'essai occupent environ 2 Go ; environ 10 Gio
restaient libres lors du contrôle. Éviter d'accumuler les modèles lourds sur
ce Mac. Pour les candidats suivants : vérifier licence des poids, taille,
backend disponible et budget avant installation ; conserver la cause exacte
si une exécution est impossible. Ne pas transformer une absence d'installation
en échec de qualité du moteur.

Prochaine preuve utile : lot français neuf annoté, OCR sur rendu seul et
pilote Luna à coût plafonné après autorisation. Voir `RECHERCHE-ET-COUTS.md`.
Le protocole de passage des pages aux cours demeure `PIPELINE.md` : ces
essais n'ont pas produit ni validé de nouveaux cours experts.

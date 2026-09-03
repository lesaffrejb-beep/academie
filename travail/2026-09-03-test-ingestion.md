# Test d'ingestion sur de vrais documents métier (03/09/2026)

Demande de JB : « avoir une idée du coût, de la méthode, des techniques,
et essayer avec de vrais docs métier ; PDF vers quoi ? les images, les
schémas ? périmé ? quels textes restent en lecture ? dispo depuis l'app ?
moi j'utilise des abonnements, jamais d'API ; testons deux ou trois trucs
et arbitrons sur un cas réel ». Ce rapport consigne ce qui a été fait,
mesuré et décidé. La décision qui en sort est
[`decisions/0026`](../decisions/0026-un-document-n-est-pas-un-chapitre.md).

## 1. Les quatre documents

| Document | Nature | Pages | Mots | Images | Ce qu'il vaut pour l'arbre |
|---|---|---|---|---|---|
| Cahier de recommandations du PSMV d'Angers (10 fiches-conseil, 2023) | institution (Angers Loire Métropole, DRAC) | 54, A3 | 45 850 | 912 | **le plus riche** : vocabulaire de la toiture (souche, lucarne, rive, solin, chéneau, noue, faîtage, arêtier, dalle nantaise, dauphin), pathologies du bâti ancien, règles du site patrimonial ; exactement le trou d'origine de JB (la souche sur la terrasse) |
| Focus n° 106 du Conseil d'analyse économique, rénovation énergétique (juin 2024) | institution, doctrine économique | 32, A4 | 17 433 | 0 raster, figures vectorielles | niveau IV : « rénovation performante contre par gestes », coûts, valeur inobservée ; une lecture de doctrine |
| Plan départemental de l'habitat et de l'hébergement 49, 2020-2025 | institution (État, Département) | 180, A4 | 51 467 | 65 | faible pour le socle : deux chapitres locaux (habitat indigne, précarité énergétique, copropriétés fragiles) ; le reste hors métier ; période close |
| Transcription d'une formation interne (espaces clients) | support-interne | 2 457 lignes VTT | 5 302 | 0 | couche `interne` seulement ; un locuteur nommé ; une notion générique (l'accès en ligne obligatoire) va au chapitre public |

Les trois PDF sont copiés dans `sources/` (hors git) sous leur empreinte ;
la transcription dans `sources/interne/`. Lignes ajoutées au registre et
au journal de la boîte.

## 2. Trois techniques testées, mesurées

| Technique | Outil | Temps | Ce que ça donne | Verdict |
|---|---|---|---|---|
| **A. Texte brut** | `pdftotext -layout` (poppler) | < 1 s par document | tout le texte, colonnes préservées ; perd les titres, les figures, les tableaux deviennent des colonnes d'espaces | **la base** : suffit pour le PDHH et pour tout document surtout textuel |
| **B. Structure par tailles de police** | `pdftohtml -xml` + 20 lignes de Python | 0,3 s | les titres retrouvés (corps 15 pt, titres 18 à 23 pt sur le Focus) ; bruit : en-têtes de page, numéros, à filtrer par répétition | **utile** pour reconstituer le plan d'un rapport et ancrer les pages |
| **C. Pages rendues en image, lues en vision** | `pdftoppm -r 90` (A3) ou `-r 110` (A4) puis lecture par le modèle | 1 s par page ; 600 à 800 Ko par page A3, 200 à 350 Ko par page A4 | **excellent** : sur la fiche 1 du PSMV, chaque étiquette du schéma de toiture a été lue et comprise ; sur le Focus, le tableau 4 et la figure 2 sont lus avec leurs valeurs | **la voie pour les figures** ; coûteuse en tokens si on l'applique à tout, donc réservée aux pages à figures |
| **D. Pré-digestion par abonnement** | NotebookLM (carnet « Copropriété » de JB, skill `notebooklm`) | 83 s la question | une réponse structurée sur les tranches IRSI avec les documents nommés (`convention-irsi.pdf`, dont l'article 1.9 date l'application au 1er juin 2018) et un document interne non daté | **utile pour trouver où chercher** ; jamais une source ; le carnet mélange documents publics et internes (déjà noté le 29/08) |

L'OCR (`ocrmypdf`, `tesseract`) n'est pas installé sur le Mac ; aucun des
quatre documents n'en avait besoin (couche texte présente). Il entre au
cahier `ACA-INGESTION-1` pour les PDF scannés.

## 3. PDF vers quoi : le pivot

**Markdown par page**, `sources/<empreinte>.md` : le texte de A, les
titres de B, chaque page ancrée `[p. n]`, les tableaux remis en tableaux
quand B les repère, et pour chaque page à figure une phrase de
description écrite par le modèle depuis C, à sa place dans le texte. À
côté, `sources/<empreinte>.figures/` garde les pages rendues. Une fiche
JSON (registre) porte titre, éditeur, date d'édition, période de
validité, licence, pages, mots.

Pourquoi ce pivot : un chapitre cite « PSMV, fiche 1, p. 4 » et un agent
frais peut rouvrir exactement cet endroit ; le PDF n'est jamais la
matière de travail, seulement la preuve ; le Markdown se relit, se
diffe, se cherche.

## 4. Les images et les schémas

- **Lire** : la vision lit les schémas légendés et les tableaux mieux
  que l'extraction de texte ; c'est la seule voie pour un dessin.
- **Réutiliser** : les dessins de l'agence d'architectes et les photos
  du PSMV sont à droits réservés (mention en pied de page) : on décrit
  et on redessine en SVG maison, comme pour l'AQC. **Exception vérifiée
  sur pièce** : les planches de Viollet-le-Duc reproduites dans la fiche
  1 sont du domaine public ; elles se réutilisent avec leur mention.
- **Décrire** : la description d'une figure par le modèle devient le
  cahier des charges du schéma maison (« coupe d'une toiture ardoise :
  souche, lucarne, rive, solin, chéneau, noue, faîtage, arêtier, dalle
  nantaise, descente EP, dauphin »). Quatre schémas de ce genre couvrent
  la branche toitures.

## 5. Ce qu'on garde, ce qu'on abrège, ce qu'on coupe

| Document | Lecture intégrale | Abrégé | Coupé |
|---|---|---|---|
| PSMV | les fiches 1 à 7 (restaurer le bâti traditionnel), une par une, comme lectures de niveau III sur le bâti angevin | les fiches 8 à 10 en un résumé | le réglementaire pur, renvoyé au règlement du PSMV |
| Focus CAE | l'encadré 1 (les six postes de travaux) et l'encadré 2 (valeur inobservée), en lecture de niveau IV | le reste en une page : coûts, bénéfices, barrières | les annexes méthodologiques |
| PDHH | rien | deux pages : orientations 2-1 et 2-2 (habitat indigne, précarité énergétique) avec les chiffres datés | tout le reste, hors métier |
| Formation interne | rien (jamais servie) | une paraphrase en couche `interne` pour JB : qui a accès à l'espace client, ce qu'il faut pour qu'un compte marche, les trois bonnes pratiques | les noms, l'outil, les captures |

Un document ne dicte pas l'ordre du programme : il alimente les
chapitres où il tombe. Le PSMV nourrit six chapitres de trois domaines ;
il n'en crée aucun.

## 6. Le périmé

La ligne de registre porte la date d'édition et la période de validité.
Le PDHH 2020-2025 est une source de méthode, plus une source de
chiffres. Le Focus date de juin 2024 : ses coûts unitaires portent une
péremption d'un an, ses raisonnements non. Le PSMV de 2023 est
réglementaire : il vaut jusqu'à sa révision, surveillée par un run de
vérification annuel.

## 7. Disponible depuis l'app

La ligne source d'une carte mène à la page officielle du document. Le
produit n'héberge un document que sous licence ouverte ou avec l'accord
de l'éditeur ; le pivot Markdown d'un document public peut être servi en
lecture avec sa page et sa licence. Un document interne n'est jamais
servi depuis le serveur.

## 8. Coûts : abonnement d'abord, l'API à titre indicatif

JB travaille sur abonnement (Claude Code, Codex, NotebookLM) : le coût
marginal d'une lecture est nul, la contrainte est la fenêtre de
contexte d'une session et le quota. Les ordres de grandeur en tokens,
et leur prix si quelqu'un passait par l'API (grille Claude du
24/06/2026 en cache dans la skill `claude-api`, à revérifier) :

| Lecture | Tokens | Opus 5 (5 $/M en entrée) | Sonnet 5 (2 $/M) |
|---|---|---|---|
| PSMV en texte | ~65 000 | 0,33 $ | 0,13 $ |
| PSMV en vision, 54 pages A3 à 90 dpi | ~113 000 | 0,57 $ | 0,23 $ |
| PDHH en texte | ~75 000 | 0,38 $ | 0,15 $ |
| Focus CAE en texte + 8 pages à figures | ~38 000 | 0,19 $ | 0,08 $ |
| Transcription | ~8 000 | 0,04 $ | 0,02 $ |
| Écrire un chapitre (sortie) | ~4 000 à 5 000 | 0,10 à 0,13 $ (25 $/M en sortie) | 0,05 $ |
| Double passe d'un chapitre (lecture des sources et du chapitre) | ~30 000 à 60 000 | 0,15 à 0,30 $ | 0,06 à 0,12 $ |

Un chapitre complet, sources lues, écrit, relu : **0,5 à 1 $** par
l'API ; les 387 chapitres du programme : **200 à 400 $** à Opus 5, la
moitié à Sonnet 5, une fois. Sur abonnement : le temps de session. Le
cache de prompt et les lots asynchrones divisent encore ces chiffres
(le corpus lu une fois en cache, les lots à moitié prix).

## 9. Les modèles en 2026, et la suite probable

Ce qui existe le 03/09/2026 (grille en cache de la skill, vérifiée le
24/06/2026) : Claude Opus 5, Sonnet 5, Fable 5.1 avec un million de
tokens de contexte et 128 000 en sortie ; l'entrée PDF native jusqu'à
600 pages, les citations avec numéro de page, la recherche et la lecture
web côté serveur, les lots asynchrones à moitié prix, le cache de
prompt, les agents gérés avec exécution planifiée. Ce qui change vite :
le prix de la vision, la taille des contextes, l'autonomie des agents.

Ce que ça impose à l'usine, et qui ne change pas : un pivot indépendant
du modèle (Markdown, pages, figures rendues), un tampon de provenance
qui nomme le modèle et la date, une relecture par un autre modèle, et
le principe de `labor/domaine/doctrine-harnais.md` : le harnais est
périssable, on le re-teste à chaque génération de modèle. Aucune
fonction du produit ne dépend d'un fournisseur ; l'usine tourne dans
n'importe quel outil d'agent sur abonnement.

## 10. Ce que le test change

- `decisions/0026` : un document n'est pas un chapitre ; le pivot ; les
  outils ; l'abonnement d'abord ; les images du domaine public.
- `ACA-INGESTION-1` (ready, cahier écrit) : le script de pivot et les
  quatre documents traités de bout en bout.
- `boite/GLISSER.md` : la lecture des PDF par pivot et pages rendues.
- Le programme : le PSMV a fait ajouter le chapitre « Le site
  patrimonial remarquable et le PSMV », la sous-branche
  « couvertures » et les notions de la toiture angevine ; le PDHH, le
  chapitre « Le plan départemental de l'habitat » ; la formation
  interne, le chapitre « L'espace client en ligne » ; le Focus, la
  notion de « valeur inobservée » au niveau IV.
- Reste dû : installer l'OCR le jour d'un PDF scanné ; décider si le
  carnet NotebookLM, marqué public, doit perdre ses documents internes.

# Test d’une page scannée — 6 septembre 2026

**Un vrai scan a été trouvé, mais le texte capturé dans le panneau NotebookLM
ne restitue pas son corps.** La récupération du panneau ne remplace donc
pas, sur cet exemple, un OCR des images du document. Cela ne mesure pas
les capacités internes de recherche ou de réponse multimodale de NotebookLM.

Outil : Codex, modèle GPT-6 ; lecture locale avec Poppler `pdftotext`
26.07.0, `pdfinfo`, `pdfimages`, Python et inspection d’un rendu déjà présent.
Aucune requête au modèle du carnet, aucun import, nouveau rendu, OCR,
achat ou publication. Aucun document client ou interne consulté.

## Recherche bornée du candidat

Les quatre PDF publics déjà présents ont été sondés par extraction native.
Une page contenant moins de 100 caractères hors espaces sert seulement
de signal de recherche : couvertures, séparateurs et pages blanches peuvent
produire le même signal. Ce seuil ne diagnostique pas un scan.

| PDF local | Pages | Extraction complète, un passage | Pages sous le seuil |
|---|---:|---:|---:|
| PDHH Maine-et-Loire 2020-2025, `8760dfb3f168df2d.pdf` | 180 | 0,346 s | 29 |
| CAE Focus 106, `322a2f5e843f45b9.pdf` | 32 | 0,287 s | 0 |
| Guide Anah, `0a7537d478616271.pdf` | 195 | 0,319 s | 19 |
| Cahier Angers, `707940074f138868.pdf` | 54 | 0,400 s | 0 |

Ce sont des durées locales observées, avec démarrage du processus inclus,
sans répétition statistique. Elles ne mesurent ni une lecture humaine ni
l’ingestion NotebookLM. Le Focus est un contrôle local ; son titre exact
n’est pas identifié dans l’inventaire du carnet.

## Page contrôlée : arrêté du PDHH, page PDF 6

Le PDF est mixte, pas entièrement scanné. Sur cette page, `pdfimages -list`
identifie deux images JPEG : 1440 × 1248 et 1440 × 623 pixels, à 220 ppp
selon les métadonnées. Le rendu existant montre le texte de l’arrêté dans
ces images, avec l’en-tête, les visas et des marques de numérisation.

Une extraction isolée de cette page prend **0,017 s** et rend seulement
**75 caractères hors espaces** : « Arrêté », le numéro de page et le pied
de page du plan. Le corps visible ne possède pas de couche texte native
exploitable par cette commande.

La capture NotebookLM existante porte le titre UI exact
`bat_brochure_PDHH_A4.pdf`, entrée **66**, occurrence 0, capturée le
6 septembre à 16:32:20 UTC. Son fichier `0066.txt` contient 377 430
caractères. Son empreinte correspond au manifeste. Le titre intérieur,
le sommaire, l’entrée « Arrêté … 6 », puis la section I et son contenu
rattachent fortement cette capture au même document éditorial.
L’identité binaire du PDF importé dans NotebookLM reste non démontrée.

Dans cette capture, après le sommaire, « Arrêté » est suivi directement
de « I. Calendrier et méthodologie d’élaboration du PDHH ». Six repères
lus sur le rendu de la page 6 sont absents à la fois de la couche native
de cette page et de **tout le texte NotebookLM capturé** :

| Repère visible dans le scan | Texte natif p. 6 | Capture NotebookLM |
|---|---|---|
| ARRÊTÉ PORTANT APPROBATION | absent | absent |
| CHEVALIER DE LA LÉGION D’HONNEUR | absent | absent |
| OFFICIER DE L’ORDRE NATIONAL DU MÉRITE | absent | absent |
| 2019-016 | absent | absent |
| L. 302-10 | absent | absent |
| BIDAL | absent | absent |

Recherche insensible à la casse, aux accents, aux espaces et à la
ponctuation. Ces six repères et la rupture de section établissent une
omission du corps de cette page dans le texte collecté. Ils ne constituent
pas une transcription de référence complète ni un taux d’erreur OCR.

## Temps, images et limites de la comparaison

La lecture du fichier NotebookLM déjà sauvegardé prend 0,00049 s. **Ce
temps n’est pas comparable aux 0,017 s d’extraction PDF** : il ne mesure
que l’accès disque à un résultat antérieur. Aucun temps d’ingestion,
d’OCR, d’ouverture du panneau ou d’extraction navigateur n’a été remesuré
sur ce document. Aucun coût marginal n’a été constaté ; cela ne prouve
pas la gratuité d’une chaîne complète ni les limites de l’abonnement.

La capture possède aussi **225 références d’images**, dont les champs
`alt` contiennent des URL, sans transcription de l’arrêté. Ces références
ne sont ni 225 téléchargements vérifiés ni 225 pages. Les images de cette
source n’ont pas été ouvertes ou téléchargées dans cette passe : le scan
peut être préservé en tant qu’image sans devenir du texte sélectionnable.

Contrôle visuel limité à **une page du PDF local**, sur son rendu existant ;
pas de comparaison pixel à pixel avec une image exportée de NotebookLM.
La fidélité des tableaux, l’ordre de lecture du reste du document et la
qualité de réponses générées ne sont pas évalués. Aucun verdict usine
de lecture intégrale ou de validation documentaire n’est revendiqué.

Pour la chaîne envisagée, cette page impose donc de conserver les images
et de détecter les zones textuelles absentes du panneau. L’outil peut
économiser une récupération de texte natif, mais le gain OCR n’est pas
démontré ici : **le texte de ce scan reste à transcrire ou à OCRiser**.

## Preuves conservées hors dépôt

Les sorties brutes, mesures JSON, métadonnées et copie du rendu existant
sont dans
`/Users/jb/.codex/visualizations/2026/09/06/01a07779-1d3c-7203-a4f5-f7ddc4deb94e/notebooklm-benchmark-scan/`.
La capture source et son manifeste restent dans le dossier frère
`notebooklm-collecte/` (`0066.txt`, `0066-images.json`, `manifest.json`).
Copie temporaire des mesures : `/private/tmp/academie-benchmark-notebooklm/scan/`.

- PDF local SHA-256 : `8760dfb3f168df2df451b23dbab92e88fdeda4575334989953fb1e002ea36d3c`.
- Capture NotebookLM SHA-256 : `9b8570844218e314eb5552ccb57e95581b9db88986e4b172b3bf4664f4de5b55`.
- Rendu p. 6 SHA-256 : `4eb89ae1f010d002de9aa4e3b7dbfd6d924dee1ace2d9e41f195df725d2ac39a`.

`measurements.json` contient les compteurs par PDF et toutes les pages
sous le seuil ; `comparison.json` contient les six recherches, les
empreintes et les durées. Les PDF bruts n’ont pas été recopiés dans le
dépôt par cette passe.

# Lien public du cahier façade : correspondance établie

Contrôle Codex / GPT-6, sous-tâche `/root/graphe`, le 06/09/2026.
Cette preuve complète PREUVES-ET-LIMITES.md : le téléchargement direct du
PDF public a désormais abouti, après la limite de taille de l'outil web.
Elle ne modifie ni la source locale scellée ni les statuts du candidat.

## Verdict utilisable pour la relecture

Le [PDF officiel du Géoportail de l'urbanisme](https://data.geopf.fr/annexes/gpu/documents/PSMV_244900015/e4859efbaa6a6b73f60a338e11f14048/244900015_cahier_recommandations_20241016.pdf)
est consultable et contient **la même pagination des passages utilisés** :
page PDF 2 pour le statut des recommandations ; pages PDF 11 à 14 pour la
fiche façades en pierre, feuillets imprimés 3.1, 3.2, 3.3 et 3.4.

Les extractions `pdftotext -layout` des pages 11, 12, 13 et 14 sont
**strictement identiques**, espaces et retours de ligne compris, entre
copie locale et PDF public. Les rendus publics de ces quatre pages ont
également été affichés et confrontés aux rendus locaux déjà consultés :
mêmes photographies, schémas, légendes et organisation des passages étudiés.
Cette comparaison n'est pas une autorisation de reproduire leurs images.

Page 2, la phrase sur le règlement déplace la parenthèse relative aux pièces
écrite et graphique ; quelques titres changent de casse dans l'extraction.
La distinction entre recommandations et prescriptions réglementaires est
conservée. Le rendu public de cette page a été consulté. Le candidat peut
continuer à pointer `#page=2` pour cette distinction, sans en tirer une
obligation juridique actuelle.

## Les fichiers restent distincts

| Propriété | Copie locale scellée | PDF public téléchargé |
|---|---|---|
| Pages PDF | 54 | 54 |
| Taille | 12 570 504 octets | 47 648 818 octets |
| SHA-256 | `707940074f1388686398dd795457acbf3ab30d6bcd2ae2a65c3a88f3888b1fba` | `37599e98bfa1d90b13aa7ee1b7ca54e26f700b3614c2e9cc74a94e1c55ae4ea3` |
| Producteur PDF | iLovePDF | Adobe PDF Library 10.0.1 |
| Métadonnée modification | 05/05/2023 | 16/10/2024 |

La couverture publique ajoute une mention de document approuvé et son
horodatage imprimé diffère de quelques minutes. Les PNG produits aux mêmes
réglages ne sont pas identiques octet pour octet. Aucun pourcentage de
fiabilité n'est déduit des comparaisons de texte ou d'images. Les autres
pages du PDF public n'ont pas été confrontées dans cette unité : aucune
identité intégrale de contenu ni lecture intégrale du fichier public n'est
revendiquée, et son sceau n'est pas celui de la copie locale.

## Référence proposée pour le candidat

Conserver le lien officiel ci-dessus avec les ancres de pages vérifiées.
La référence peut dire : « Cahier de recommandations du PSMV d'Angers,
fiche façades en pierre, pages PDF 11 à 14 ; passages confrontés entre la
copie locale édition 2023 et le document officiel diffusé sous le nom
20241016. Recommandations, sans prescription juridique actuelle. »

Si le champ `empreinte` désigne le fichier accessible à l'URL, utiliser
l'empreinte publique `37599e98…` ; conserver l'empreinte `70794007…` comme
preuve de la copie locale consultée dans ce dossier. Ne pas annoncer les
deux fichiers comme identiques. L'auteur du candidat n'en modifie pas les
sources pendant la relecture distincte du coordinateur.

## Traces conservées hors dépôt

- Brut public : `/private/tmp/academie-angers-cahier-public-20241016.pdf`.
- Textes par page, diffs et rendus 72 dpi : `/private/tmp/academie-angers-comparaison/`.
- Résultat et empreintes des rendus : `Lien-public.json` dans ce dossier.
- Téléchargement `curl --fail --location`, sortie 0 ; aucune authentification,
  aucun appel NotebookLM, aucune utilisation du navigateur partagé.

Les commandes `pdfinfo`, `pdftotext` et `pdftoppm` ont été utilisées en
lecture seule. Poppler signale « Invalid Font Weight » pendant certaines
extractions ; les commandes aboutissent et les passages sont lisibles,
ce signal est conservé comme limite d'outil et n'a pas été effacé par une
modification du PDF.

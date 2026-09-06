# Médias AQC récupérés depuis NotebookLM

06/09/2026. Outil : Chrome browser-client, capacité pageAssets, Codex / GPT-6.
Carnet : https://notebook.google.com/notebook/567a033f-6a53-4321-a741-912f722403ea
Les onglets agents utilisés étaient 530438735 et 530438741 ; l'onglet du
coordinateur 530438679 n'a pas été contrôlé par cet agent.

## Résultat du corpus canonique

| Fiche, titre exact observé dans l'interface | Occurrence UI choisie (index zéro) | Images DOM chargées | Fichiers récupérés |
|---|---:|---:|---:|
| Fiche-Pathologie-Batiment-G05-Entretien-Maintenance-Pac-Aerothermiques-AQC.pdf | 0 | 11 | 11 |
| Fiche-Pathologie-Batiment-G06-Entretien-Maintenance-VMC-Simple-Double-Flux-AQC.pdf | 1 | 9 | 9 |
| Fiche-Pathologie-Batiment-G07-Entretien-Maintenance-Plomberie-Sanitaire-AQC.pdf | 0 | 5 | 5 |

Dossiers canoniques : `G05/`, `G06-occurrence-2/`, `G07/`.
25 fichiers, 23 empreintes SHA-256 distinctes. Un même fichier se trouve dans
les trois fiches (G05 no 7, G06 occurrence 2 no 8, G07 no 4). Il est conservé
dans chaque occurrence : aucune déduplication destructive.

33 téléchargements sont conservés au total : les huit fichiers de la première
tentative VMC figurent aussi dans `G06/`. Ces huit empreintes sont identiques
à huit fichiers de la seconde occurrence, malgré des URLs d'images différentes.
La seconde occurrence fournit une neuvième image. Les deux boutons homonymes
PAC et les deux boutons homonymes plomberie n'ont pas tous été ouverts : le
relevé ne prouve pas l'identité complète des six occurrences du carnet.

## Méthode et écarts conservés

Les titres proviennent des boutons de la liste de sources. Après ouverture,
les éléments `img` du panneau source ont été recensés avec URL effectivement
chargée, largeur/hauteur naturelles et état de chargement. La navigation a
atteint le bas du conteneur déroulant ; le nombre d'images est resté inchangé.
Aucune image différée supplémentaire n'a été observée par ce contrôle.

L'inventaire pageAssets a été filtré par correspondance exacte avec les URLs
du panneau source avant téléchargement. Aucun logo de l'application, avatar,
favicon, autre source ou média Studio n'a été collecté. Les fichiers sont
issus du navigateur, sans requête HTTP lancée depuis le shell ou un client
alternatif, sans transformation d'URL pour demander une meilleure résolution.

La première occurrence VMC avait neuf images DOM mais seulement huit dans
l'inventaire exportable. Dans cet onglet, la fiche plomberie avait ensuite
cinq images DOM mais aucune correspondance dans l'inventaire cumulatif.
Cette tentative de bundle a été refusée avec le motif « Asset bundle request
matched no discovered assets ». Aucun téléchargement n'en est compté.
Un onglet neuf a permis de récupérer les cinq images plomberie, puis les
neuf images de la deuxième occurrence VMC. La cause interne de la divergence
d'inventaire n'a pas été établie ; aucune limite logicielle supposée n'est
présentée comme diagnostic certain.

Plusieurs observations Chrome ont expiré alors que l'action précédente avait
abouti. L'état du même onglet a été relu avant toute action suivante ; aucun
clic de source n'a été répété sans constater la liste ou le panneau courant.

## Preuves locales

- `manifest.json` : titres, fichiers, MIME, dimensions locales, octets,
  empreintes, doublons, corpus canonique et limites.
- `*-observation*.json`, `*-fin.json` : état DOM restreint aux médias sources
  et géométrie de défilement ; `*-bundle.json` : résultat de l'export navigateur.
- Quatre `*-fin-panneau.png` : captures recadrées au panneau documentaire,
  témoignant de la navigation en fin de source. Ces captures ne sont pas
  comptées dans les 25 fichiers média et ne sont pas des rendus PDF complets.
- `sips` a décodé les dimensions des 33 fichiers récupérés. Une photographie
  G05 a également été affichée pour constater qu'il s'agit d'une image réelle,
  sans interprétation technique de son contenu.
- `python3 verifier.py` : vérification des octets et empreintes sur disque.

## Limites de preuve

Il s'agit de toutes les images DOM recensées pour les trois occurrences
canoniques, pas d'une preuve d'exhaustivité contre les PDF originaux. Les
PDF eux-mêmes n'ont pas été récupérés. Les dimensions conservées sont celles
servies par NotebookLM ; elles ne prouvent pas la résolution des originaux.
Des logos ou petits éléments graphiques font partie des images du document :
25 fichiers ne signifient pas 25 schémas pédagogiques distincts.

Aucune transcription textuelle nouvelle, interprétation métier, carte,
qualification juridique ni publication. Les mentions AQC ou l'accessibilité
du carnet n'accordent pas à elles seules un droit de redistribution. Tous les
fichiers de ce lot sont hors dépôt dans ce dossier temporaire local.

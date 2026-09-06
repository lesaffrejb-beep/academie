# Collecte → notions → application : contre-lecture des preuves

Observation locale du 06/09/2026 à 20:34 +02:00. Codex, GPT-6,
agent `/root/acces_profils`. Lecture des manifests, recalcul des empreintes,
lecture de la banque et des chapitres ; aucun navigateur, collecte, test
global, génération ou accès VPS.

**La chaîne fonctionne sur une sélection éditoriale de trois documents, pas
sur l'ensemble du carnet. La collecte est beaucoup plus large que les cours
produits ; son passage automatique en notions puis en cours n'est pas démontré.**

## Collecte constatée sur disque

Racine hors dépôt :
`/Users/jb/.codex/visualizations/2026/09/06/01a07779-1d3c-7203-a4f5-f7ddc4deb94e/`.
Manifests lus : `notebooklm-collecte/manifest.json`,
`notebooklm-medias-corpus/lot-1/manifest.json` et `lot-2/manifest.json`.

| Unité | Compte exact | Ce qu'elle prouve |
|---|---:|---|
| Occurrences du carnet recensées | 200 | Entrées de liste, dont des doublons |
| Titres distincts | 188 | Libellés distincts, pas identité des documents |
| Textes capturés | 181 fichiers | Tous présents, SHA-256 recalculés conformes |
| Textes distincts par empreinte | 169 | Déduplication binaire, pas correction OCR |
| Réserves / source vide | 18 / 1 | Non assimilées à des textes exploitables |
| Volume texte / références image | 11 513 261 caractères / 7 816 | Ni pages relues, ni figures récupérées |
| Occurrences portant des références image | 71 | Périmètre prévu des deux lots médias |
| Lot 1 | 1 311 fichiers, 1 074 empreintes distinctes | 35 occurrences prévues |
| Lot 2 | 126 fichiers, 125 empreintes distinctes | 36 occurrences prévues |
| Deux lots réunis | 1 437 fichiers, 1 183 empreintes distinctes | Tous présents, SHA-256 conformes |

Les 71 occurrences médias se répartissent en 27 `captured_dom_images`, deux
réemplois d'une capture antérieure, sept partielles, trois bloquées/en erreur
et 32 non tentées. **36 occurrences ont au moins un fichier**, dont les sept
partielles. Un statut DOM complet ne prouve pas l'exhaustivité face au PDF.
Les petits éléments, logos, répétitions et fragments sont comptés comme
fichiers ; 1 437 fichiers ne sont pas 1 437 illustrations pédagogiques.

Le premier essai AQC annonçait 25 fichiers canoniques, 23 empreintes et
33 téléchargements avec reprises. Il est antérieur aux deux lots et comporte
des réemplois : ne pas additionner ces nombres aux 1 437 sans déduplication.
Le résumé `collecte-stats.json` décrit encore cet essai AQC, pas les deux lots
actuels. Les textes sources complets et médias collectés restent hors dépôt.

## Ce qui atteint réellement l'application locale

`site/banque.json` : **137 cartes, neuf études, cinq parcours**.
Les 137 cartes se décomposent en 76 cartes anciennes sans chapitre v2 et
61 cartes appartenant aux neuf études. Les trois nouvelles familles
documentaires produisent quatre études/extensions et 34 de ces cartes :

| Document de fond | Passages utilisés dans les preuves éditoriales | Descendants locaux |
|---|---|---|
| CAE, Focus 106 sur la rénovation | Pages PDF 13-22, approfondissement 14-18 | Rénovation rentable : 8 cartes ; contre-expertise : 8 |
| Anah, guide copropriétés fragiles | Pages 8, 10-16 et 22 | Diagnostic partagé : 9 cartes |
| Angers, cahier de recommandations | Pages 2 et 11-14 ; version publique confrontée par le coordinateur | Façade avant devis : 9 cartes |

Les cinq autres études préexistaient : trois sur l'assemblée et ses organes
(17 cartes), deux IFSI (10 cartes). Les fichiers de `chapitres/` comptent
11 chapitres : neuf au statut valide, deux brouillons exclus des études,
soit 61 cartes valides et 12 brouillons. Les neuf études présentes dans la
banque correspondent aux neuf chapitres valides observés.

Les titres du carnet permettent de repérer le Focus à l'occurrence 41,
l'Anah aux occurrences 14/15, et un document PSMV Angers à l'occurrence 42.
Cette correspondance bibliographique **ne prouve pas l'identité binaire**
des documents importés. Les preuves de fabrication renvoient aux PDF locaux,
aux passages examinés et aux relectures. Elles ne démontrent pas que les
181 fichiers texte NotebookLM ont été consommés automatiquement. Trois
documents exploités ne signifie pas trois documents intégralement enseignés.

Neuf cartes servies référencent une image, avec **cinq chemins SVG distincts**
dans la banque. Aucun chemin des médias NotebookLM collectés n'est utilisé
par ces cartes. Le grand lot d'images n'a donc pas encore produit une banque
de supports pédagogiques dans cet artefact.

## Couverture : les nombres à ne pas confondre

| Cursus | Cartes jouables locales | Études | Chapitres du programme de base couverts par une étude | Sans étude complète |
|---|---:|---:|---:|---:|
| Copropriété | 127 | 7 = 3 socle + 4 extensions | 3 / 389 | 386 |
| IFSI | 10 | 2 | 2 / 375 | 373 |

`programme/catalogue.json` annonce sept `chapitres_ecrits` pour copro avec
389 chapitres au programme. Le numérateur inclut quatre extensions hors de
ce programme : **ce n'est pas sept chapitres du socle couverts**. L'arbre
complet copro contient 393 nœuds parce qu'il ajoute ces quatre extensions ;
ce nombre mesure la structure de navigation, pas la quantité de cours.
Les statuts bruts du programme (`a-ecrire`, etc.) sont également distincts
des chapitres effectivement servis et ne constituent pas un inventaire à jour
des études.

« Sans étude complète » ne veut pas dire absence totale de connaissances :
les 76 cartes anciennes apportent du rappel, mais n'établissent pas une
couverture complète de ces chapitres. Ni les compteurs, ni la réussite des
parcours de test ne démontrent une compétence professionnelle acquise.

## Conclusion de preuve

Collecter, sélectionner des passages, écrire des notions avec leurs limites,
faire relire, intégrer et jouer fonctionne sur ces quatre extensions. Le
passage éditorial reste délibéré et traçable, pas une conversion automatique
de tout le carnet. Les preuves de parcours locales existent séparément dans
`travail/modules-experts-2026-09-06/`, `travail/fragilite-2026-09-06/E2E.md`
et `travail/facade-2026-09-06/E2E.md` ; elles ne sont pas rejouées ici.

Restent ouverts : qualification des textes collectés, 32 occurrences médias
non tentées, trois blocages et sept collectes partielles, droits et utilité
des illustrations, transformation pédagogique du reste du corpus, couverture
du programme et preuve d'apprentissage. **Aucun état courant du VPS n'est
établi par cet audit.**

Empreinte SHA-256 de la banque observée :
`3b8edfac22602145548cf17ff291f0ef93138cb50775447fc42efc89eafce3de`.

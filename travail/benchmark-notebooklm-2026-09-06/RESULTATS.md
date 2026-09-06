# Extraction locale et NotebookLM — essai du 6 septembre 2026

Outil d'observation : Codex, GPT-6. Extracteur local : Poppler, sans modèle. Extracteur interne de NotebookLM : inconnu. Essai mécanique, sans ingestion éditoriale ni validation de lecture du guide.

Source commune : `082026_guide_gerer-coproprietes-fragiles.pdf`, PDF local dans Downloads, 195 pages, empreinte SHA-256 abrégée `0a7537d478616271`. Le panneau du carnet présente le même nom et un texte très proche ; identité binaire du fichier importé non vérifiée.

| Mesure | Local | NotebookLM |
|---|---|---|
| Extraction du texte | 0,365 s | lecture du panneau déjà préparé : 0,077 s |
| Volume brut | 468 128 caractères | 298 688 caractères |
| Caractères hors espaces | 253 703 | 253 031 |
| Mots normalisés | 47 507 | 47 366 |
| Images | inventaire PDF : 0,251 s | 2 téléchargements réussis en 23,17 s |
| Illustration | rendu d'une page à 1 200 px : 0,232 s | un schéma téléchargé de 435 × 400 px, lisible |
| Facturation supplémentaire de l'extraction | aucun appel payant ; calcul local | aucun achat ni appel API payant déclenché ; abonnement de JB, facture et quotas non vérifiés |

Les temps ne sont pas équivalents : l'import et le traitement initial NotebookLM sont exclus, de même que la connexion, les reprises et les interactions Codex. Un rendu de page local n'est pas la même opération que télécharger deux images. Un seul passage mesuré, aucune extrapolation à un corpus.

## Divergences constatées

Après normalisation Unicode, casse et tokenisation, l'intersection des multiensembles contient 47 290 occurrences : 99,54 % des occurrences locales. Ce score ignore l'ordre, le sens et les associations entre valeurs et libellés. Ce n'est ni une exactitude OCR ni une validation du contenu.

Le sommaire local conserve la géométrie de deux colonnes ; une lecture linéaire mélange leurs lignes. NotebookLM replace les sections dans un ordre plus exploitable. À l'inverse, la formule de couverture « Expertise de l'habitat privé », lisible localement, devient une suite de fragments dans NotebookLM. Des ruptures de lignes persistent.

L'inventaire local dénombre 2 049 objets image sur 28 pages ; le panneau comporte 1 158 éléments image et l'inventaire navigateur n'en exposait que 67 de NotebookLM lors de la collecte. Ces unités diffèrent (objets, fragments, rendus, ressources chargées) : aucun taux de récupération des figures ne peut être déduit. Deux fichiers JPEG ont été téléchargés sans erreur, dont un schéma examiné visuellement. Exhaustivité et résolution d'origine non établies.

## Décision proposée

Pour ce PDF avec couche texte, garder l'extraction locale comme témoin paginé, rapide et reproductible. NotebookLM fournit une autre représentation utile pour l'ordre de lecture et des illustrations récupérables. Ne pas remplacer le témoin local sur la seule base de cet essai.

Un second essai a maintenant porté sur une vraie page scannée du PDHH :
le corps de l’arrêté visible sur la page 6 est absent du texte NotebookLM
récupéré. Voir [le test du scan](SCAN.md). Cet exemple ne démontre aucun gain
OCR du panneau et impose de conserver la référence PDF et les images. Les deux chemins laissent à faire la compréhension des schémas, les références de pages, le contrôle des assertions et la fabrication pédagogique. Aucune économie monétaire globale chiffrable sans temps complet et consommation d'abonnement observés.

Preuves brutes temporaires : `/private/tmp/academie-benchmark-notebooklm/` (textes local et NotebookLM, différences de séquence, rendu page 8). Les textes source restent hors du dépôt. Aucun contenu pédagogique modifié.

Recontrôle indépendant du scan par le coordinateur : rendu page6 examiné,
six repères recherchés à nouveau dans toute la capture ; mêmes absences.
Le détail des médias AQC effectivement récupérés est dans [MEDIAS-AQC.md](MEDIAS-AQC.md).

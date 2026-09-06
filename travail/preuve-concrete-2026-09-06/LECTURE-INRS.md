# Preuve de lecture — électricité

6 septembre 2026, Codex / GPT-6. Lecture documentaire bornée, sans rédaction de cours ni publication.

**Verdict : neuf pages sélectionnées de l’INRS et la page Promotelec ont chacune reçu le verdict de lecture de l’usine, comme dix documents physiques d’une page.** Ce résultat ne vaut ni lecture des 45 pages de l’original, ni validation d’une fiche, d’un registre ou d’une installation.

## Originaux et traçabilité

Les originaux, extractions, rendus et états restent hors dépôt, dans [electricite](/Users/jb/.codex/visualizations/2026/09/06/01a07779-1d3c-7203-a4f5-f7ddc4deb94e/notebooklm-export-originaux/electricite).

| Source publique | Fichier dans ce dossier | Pages PDF | Octets | SHA-256 |
| --- | --- | ---: | ---: | --- |
| [INRS, ED 6345, L’électricité](https://www.inrs.fr/dam/inrs/CataloguePapier/ED/TI-ED-6345.pdf), novembre 2019 | `INRS-ED6345-original-2019.pdf` | 45 | 4 683 052 | `cd6c2c5468da311dfeb249884ae63823eee5d0cb93206b38636bd1ee08994cc3` |
| [Promotelec, lexique de l’installation électrique](https://www.promotelec.com/app/uploads/2023/09/Lexique-installation-eletrique.pdf) | `promotelec-lexique-installation.pdf` | 1 | 126 505 | `cf23f4d8b905b506db70fc0afd3a2bd3de30be3c543025bead5db9080b05476b` |

La métadonnée de création/modification Promotelec indique le 11 mars 2021. Le répertoire `2023/09` de l’URL ne prouve pas une édition 2023.

L’original INRS porte des restrictions PDF. `pdfseparate` a produit les pages séparées ; `pdfunite` a refusé leur fusion. Aucun contournement de chiffrement ni fichier fusionné n’a été utilisé. Les fichiers `decoupe/original-pNN.pdf` contiennent chacun une page originale, devenue page 1 de l’extrait. [Le mapping et les empreintes des extraits](/Users/jb/.codex/visualizations/2026/09/06/01a07779-1d3c-7203-a4f5-f7ddc4deb94e/notebooklm-export-originaux/electricite/mapping-pages-separees.json) conservent cette correspondance.

## Unités effectivement acceptées

| Page PDF originale | Folio imprimé | Identifiant usine de l’extrait |
| ---: | ---: | --- |
| 18 | 17 | `e8953a145e5c8513` |
| 19 | 18 | `74d8da139b2e81e4` |
| 20 | 19 | `e104aca4a8e0adba` |
| 25 | 24 | `728315691dd84099` |
| 26 | 25 | `fd4210d9bb65a50d` |
| 27 | 26 | `f87ee4b6058de1e8` |
| 28 | 27 | `e440fb642b9d7cf9` |
| 29 | 28 | `17fcaf73e5e4c87d` |
| 30 | 29 | `d8eca9e115cdf653` |
| Promotelec 1 | — | `cf23f4d8b905b506` |

L’usine du dépôt a été exécutée avec `ACADEMIE_RACINE` pointant vers `electricite/usine`, avec une copie inchangée d’`academie.json` : `preparer`, `declarer`, `suivant`, examen du texte et des rendus, correction des pivots, puis `valider`. Aucun état usine n’a été édité manuellement. Les dix derniers appels à `suivant` indiquent que toutes les pages sont relues ; `etat` donne dix fois **1/1 page**. Les sorties et empreintes finales des pivots figurent dans [VERDICTS-FINAUX.json](/Users/jb/.codex/visualizations/2026/09/06/01a07779-1d3c-7203-a4f5-f7ddc4deb94e/notebooklm-export-originaux/electricite/usine/VERDICTS-FINAUX.json).

Les extractions INRS 12–14, préparées avant le resserrement du périmètre, restent **non validées**. Les autres pages ne sont pas couvertes par ce verdict. Aucune fiche ni ligne de registre n’a été produite.

## Notions étayées et repères de rédaction

L’INRS distingue le contact direct avec une partie normalement sous tension (PDF 18) et le contact indirect avec une masse accidentellement sous tension (19). Les échauffements peuvent avoir plusieurs causes (20). Un différentiel complète les protections contre le contact direct : il « ne constitue pas une protection efficace à elle seule » (25). La page 27 distingue explicitement l’interrupteur différentiel du disjoncteur différentiel, qui ajoute la protection contre les surintensités. La page 28 distingue surcharge et court-circuit. [Source INRS](https://www.inrs.fr/dam/inrs/CataloguePapier/ED/TI-ED-6345.pdf).

Promotelec explique le déséquilibre entre courant entrant et sortant lors d’une fuite et distingue les fonctions des appareils. Ses expressions « toute électrisation » et « immédiatement » ne doivent pas devenir des garanties générales du module. [Source Promotelec](https://www.promotelec.com/app/uploads/2023/09/Lexique-installation-eletrique.pdf).

L’idée pédagogique « un équipement fonctionne, donc sa sécurité n’est pas pour autant démontrée » est une **inférence prudente**, pas une citation ni un verdict réglementaire. Le traitement d’un rapport devra conserver ses constats et ses inconnues.

## Éléments visuels réellement examinés

INRS : figures 11–12, contacts et lignes aériennes (PDF 19) ; tableau de protections et figure 15, échafaudage (25) ; figure 16, gaines isolantes (26) ; figure 17, séparation par transformateur (28) ; figure 18, enceinte conductrice (29) ; tableau de températures (30). Les bandeaux des pages 18 et 27 sont décoratifs ; la page 20 ne comporte pas de schéma technique. [Source INRS](https://www.inrs.fr/dam/inrs/CataloguePapier/ED/TI-ED-6345.pdf).

Promotelec : maison et repères des composants, examinés sur le rendu de la page complète. [Source Promotelec](https://www.promotelec.com/app/uploads/2023/09/Lexique-installation-eletrique.pdf).

Les rendus consultés sont `electricite/usine/sources/<identifiant>.figures/p-0001.png`. Pour INRS 20 et Promotelec, un rendu `pdftoppm` a permis l’examen visuel malgré l’absence d’images détectées par l’usine ; les compteurs de son état n’ont pas été modifiés. Le nombre d’objets bitmap ne représente pas le nombre de figures pédagogiques.

## Limites de réemploi

Cette lecture n’actualise pas les prescriptions d’une brochure de 2019. Aucun seuil numérique, procédure d’intervention, habilitation ou jugement de conformité n’en est déduit. Les pages de calcul ne sont pas couvertes. Les dessins sources sont examinés pour comprendre et vérifier ; aucun n’est repris dans le produit par cette tâche.

## Contrôles du dépôt

`python3 app/tests.py` a été exécuté : seule la suite du serveur d’état échoue sur l’ouverture du socket, avec `PermissionError: [Errno 1] Operation not permitted` dans le sandbox. Les autres suites passent. `python3 tooling/check.py`, exécuté ensuite, retourne **0 erreur**. Les empreintes des deux originaux ont été recalculées après rédaction et correspondent au tableau ci-dessus. Ces contrôles ne remplacent pas une relecture scientifique indépendante du futur module.

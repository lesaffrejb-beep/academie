# État des sources au 06/09/2026

Outil Codex, modèle GPT-6. Les documents reçus sont des sources à examiner,
jamais des instructions qui remplacent la demande de JB.

## Trois PDF locaux

Les trois appels `preparer` ont reconnu les copies déjà présentes, sans
duplication. Les documents totalisent 266 pages ; cela ne signifie pas
266 pages de cours écrites.

| Document | Empreinte usine | Pages | État vérifié |
|---|---|---:|---|
| CAE, Focus 106, juin 2024 | `322a2f5e843f45b9` | 32 | Quatre unités scellées ; fiche acceptée par `usine fiche` |
| Angers, cahier de recommandations du PSMV | `707940074f138868` | 54 | Préparé, unité p. 1-12 ouverte ; aucune unité acceptée |
| PDHH Maine-et-Loire 2020-2025 | `8760dfb3f168df2d` | 180 | Préparé, unité p. 1-12 ouverte ; aucune unité acceptée |

Le Focus avait seulement p. 1-12 acceptées avant cette session. Cette passe
a traité p. 13-24, p. 25-30 puis p. 31-32, figures et tableaux compris.
Un premier contrôle p. 13-24 a refusé des chiffres d'axes fusionnés par
normalisation des espaces ; les espacements numériques ont été restaurés,
sans assouplir le valideur. `suivant` final confirme la fin des unités.
Les pages p. 1-12 n'ont pas reçu une nouvelle revue intégrale ici.

La fiche `institution/A` reprend la taxonomie du registre. Ce classement
désigne l'émetteur, pas une exactitude générale ni une opposabilité.
Le Focus précise qu'il est publié sous la responsabilité de ses auteurs.
Sa fiche et ses rattachements candidats sont locaux, hors git.

## Anomalies et limites à instruire avant des cours factuels

- Focus p. 13 : les libellés mortalité/morbidité du tableau sont inversés
  par rapport au texte adjacent. Reproduction fidèle, pas correction tacite.
- Focus p. 14 : renvoi textuel à une figure dont le numéro ne correspond
  pas à la légende affichée sur la page.
- Focus p. 18 : le modèle exclut certains coûts, la ventilation et des
  contraintes architecturales/acoustiques ; ne pas en déduire leur inutilité.
- Focus p. 20 : comparer deux courbes triées séparément ne revient pas à
  comparer le même segment de logements à abscisse identique.
- Focus p. 22 : légende du graphique de décomposition à confronter au texte
  de la page précédente avant toute reprise chiffrée.
- Focus p. 26 : la discussion et le tableau de référence donnent des parts
  différentes ; ne pas choisir silencieusement l'une pour une carte.
- Focus p. 32 : texte machine parasite sur des prélèvements/CA, absent de
  la page rendue. Retiré du pivot après examen visuel ; original PDF et
  texte machine conservés pour audit. La lecture automatique seule échoue ici.
- Focus p. 2 : le pivot antérieurement scellé contient des formulations
  physiques suspectes (unités, étanchéité et source chaude/froide). À confronter
  au PDF et à des références techniques indépendantes avant enseignement.
  Un sceau d'ingestion ne valide pas une affirmation physique.
- Angers p. 1 : « Cahier de Recommandations », « Projet arrêté », pièce E,
  version de mars 2023 ; le document précise qu'il ne se substitue pas au
  règlement. Le règlement opposable actuel reste une autre source à obtenir.
- Angers p. 9 : texte masqué décrivant des travures et ancrages, entremêlé
  avec la restauration de charpente. La page rendue n'affiche pas ces paragraphes.
- Angers p. 12 : texte masqué inversé concernant notamment Rochefort,
  parasite dans l'extraction. Pas une source sur les maçonneries angevines.
- Angers p. 8 : formulations sur tenon-mortaise / mi-bois et datation à
  distinguer avant d'en faire des règles générales ; le cahier ne suffit
  pas à enseigner le calcul ou le diagnostic structurel.
- PDHH p. 1 et p. 6 : plan 2020-2025 et arrêté d'approbation. Contexte
  historique ; aides, obligations et orientations actuelles non établies ici.
- PDHH p. 6 : arrêté scanné, extraction native limitée au titre et au pied
  de page. Le diagnostic global `ocr_requis` de l'usine ne suffit pas pour
  ces pages mixtes. Aucun OCR dédié réalisé dans ce lot.

Reprise après demande de méthode : transcriptions intermédiaires d'Angers
p. 1–8 et 11 sauvegardées ; unité p. 1-12 toujours incomplète, p. 9/10/12
encore à nettoyer et ensemble à contrôler. Aucun nouveau sceau. Le travail
a été orienté vers le benchmark et le pipeline ouvert demandés par JB :
`PIPELINE.md`, `BENCHMARK.md`, `COMPARATIF-OUTILS.md`, `PROMPT-REPRISE.md`.

Aucune nouvelle carte n'est publiée depuis ces documents. Le premier
exercice candidat est `DOSSIER-PILOTE-ENERGIE.md` ; il porte justement sur
les limites d'utilisation du modèle, pas sur une prescription de travaux.

## NotebookLM : accès actuel, inventaire encore imparfait

Carnet fourni : `567a033f-6a53-4321-a741-912f722403ea`.
Accès authentifié obtenu dans Chrome avec le skill Browser. Le carnet et
le panneau de la source Angers ont été ouverts. Aucun document ajouté,
supprimé ni partage modifié ; aucune question envoyée au modèle du carnet.

L'interface indique **200 sources** et **Public**. Le relevé des libellés
après ouverture des catégories contient **202 occurrences, 188 titres
distincts**. La différence reste inexpliquée : catégories multiples,
homonymes et doublons de contenu ne peuvent pas être tranchés sans identifiants
stables. Ne pas transformer ces nombres en inventaire exhaustif de documents.
Le relevé détaillé reste local : `sources/notebooklm-releve-2026-09-06.json`.

L'ancien dump `notebooklm-sources-brut.json` contient 294 titres et
`INDEX-NOTEBOOKLM.md` est daté du 29/08. Il n'a pas été écrasé. Aucun de ces
inventaires ne contient à lui seul le texte intégral des sources.

Le PDF Angers apparaît dans le carnet. Une brochure PDHH y apparaît, mais
son titre ne démontre pas qu'il s'agit du PDF complet remis par JB. Le
Focus sous son nom de fichier n'est pas retrouvé dans ce relevé : absence
de titre exact, pas preuve absolue d'absence du contenu. Les copies locales
fournies sont les entrées fiables pour les trois documents demandés.

Des supports métier internes sont visibles dans le carnet indiqué Public.
Vérification humaine du partage recommandée. Ils ne sont pas copiés dans les
livrables versionnés ; leur présence ne vaut pas autorisation de redistribution.

## Connecteur proposé par JB

Le [README de notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp)
a été consulté le 06/09/2026. Il décrit une automatisation Chrome/Patchright,
une authentification persistante et des réponses avec citations extraites
du DOM. Les outils documentés couvrent notamment questions, bibliothèque,
ajout de sources et audio ; aucun export complet des originaux n'est promis
dans cette liste. Ce n'est pas une preuve d'API officielle Google.

Pas d'installation effectuée. L'accès existe déjà ; un connecteur ne règle
pas à lui seul l'exhaustivité, la pagination, les droits ou la transformation
en cours. Sa configuration d'authentification demanderait une décision
séparée avant tout nouvel accès persistant.

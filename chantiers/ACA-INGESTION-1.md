# Cahier ACA-INGESTION-1 : l'usine lit un document réel

Résultat attendu : un script local transforme un document (PDF texte,
PDF image, transcription) en pivot Markdown par page avec figures
rendues et fiche de source ; un agent, sur abonnement, en tire la ligne
de registre, les rattachements aux chapitres, les lectures candidates,
les satellites, les corrections, et écrit le coût (`decisions/0026`).
Fini quand : les quatre documents du test du 03/09 traversent la chaîne
de bout en bout avec leurs pivots dans `sources/` (hors git), leurs
lignes de registre et de journal, et un rapport de coût ; un test
compare le pivot d'un PDF de fixture à un attendu.
Dépend de : ACA-DOC-2. Bloque : ACA-BOITE-1, ACA-CONTENT-2.

## État au 03/09/2026 au soir (decisions/0027)

Existe : `app/usine/` (`pivot.py`, `transcription.py`, `etat.py`,
`fiche.py`, `usine.py`), `app/tests_usine.py` (40 tests) et quatre
mutations dans `app/tests.py` ; la clé `usine` d'`academie.json` ; les
quatre documents du test préparés (pivots bruts, pages machine, pages
rendues) ; la première unité du Focus du CAE relue et validée. Reste :
les étapes 4 et 5 ci-dessous (les quatre documents relus de bout en
bout, fiches, lignes de registre, rattachements, rapport de coût).

## Et pourquoi le Cloud ne peut pas le finir (03/09/2026)

Les étapes 4 et 5 demandent de relire **les quatre documents** de bout
en bout. Or ces documents, leurs pivots et leurs pages rendues vivent
dans `sources/`, qui est hors git par construction (`sources/README.md`,
`ARCHITECTURE.md` §3) : un clone n'en contient aucun, et c'est voulu.

Vérifié le 03/09 dans l'environnement Cloud : `sources/` ne porte que
ses quatre fichiers versionnés. Il n'y a rien à relire.

Ce qui peut se faire en Cloud sur ce chantier : le code de l'usine et
ses tests, qui existent déjà et sont verts. Ce qui ne le peut pas : la
traversée des documents réels. **À finir depuis le Mac**, où les
documents sont.

## Périmètre

Peut créer ou modifier : `app/usine/` (`pivot.py` qui appelle
`pdftotext`, `pdftohtml -xml`, `pdftoppm`, `pdfimages` ; `etat.py`, le
pas à pas revérifiable ; `fiche.py`, la fiche et la ligne de registre ;
`transcription.py` pour un `.vtt`, `.srt`, `.txt` : retrait des
locuteurs et des horodatages ; `usine.py`, la ligne de commande),
`app/tests_usine.py`, `app/tests.py` (suite et mutations), la clé
`usine` d'`academie.json` et du gabarit, `tooling/requirements-usine.txt`
(outils externes attendus, avec leur licence), `sources/README.md`,
`gabarit-domaine/USINE.md` (étapes 1 et 4), `boite/GLISSER.md`
(l'appel au pivot).
Ne touche pas : le moteur, les contrats, `chapitres/`, le serveur.

## Déjà tranché (ne pas rouvrir)

- Le pivot : Markdown par page, ancres `[p. n]`, titres par taille de
  police, tableaux, figures décrites en place, pages à figures rendues
  en image à côté (`decisions/0026`).
- Outils : poppler en ligne de commande ; aucune bibliothèque AGPL
  importée ; aucun service tiers ; OCR (`ocrmypdf`, `tesseract`) admis
  en outil local quand un PDF n'a pas de couche texte, licence lue.
- L'abonnement d'abord : le script prépare, l'agent lit et écrit dans
  Claude Code ; aucune clé d'API.
- Les figures : décrites et redessinées ; domaine public réutilisable ;
  agences, associations, éditeurs jamais (`decisions/0017`, `0026`).
- Une transcription interne ne sort de `sources/interne/` que sous forme
  de paraphrase en couche `interne` ; jamais un nom.
- Le registre reçoit une ligne par document, avec date d'édition,
  période de validité, licence, « on en tire », « on n'en tire pas ».

## Étapes, dans l'ordre

1. Tests rouges : un PDF de fixture de trois pages (texte, un titre, un
   tableau, une figure) donne un pivot attendu ; un PDF sans couche
   texte est signalé « OCR requis » ; un `.vtt` de fixture donne un
   texte sans horodatage ni locuteur.
2. `pivot.py` : texte par page, titres, tableaux simples, liste des
   pages à figures, rendu de ces pages en PNG à 110 dpi, empreinte du
   document, écriture de `sources/<empreinte>.md` et `.figures/`.
3. `fiche.py` : la fiche JSON (empreinte, titre, éditeur, date
   d'édition, période de validité, licence connue ou « à vérifier »,
   pages, mots).
4. Rejouer les quatre documents du test ; mesurer le temps, la taille des
   pivots, les tokens lus par l'agent pour en tirer registre et
   rattachements ; écrire le rapport.
5. Mettre à jour `USINE.md` et `GLISSER.md`.

## Ce qu'on ne fait pas

- Pas de chapitre ici (ACA-CONTENT-2), pas de satellite (ACA-BOITE-1).
- Pas d'appel d'API, pas de service d'extraction en ligne.
- Pas de copie d'image d'agence dans `banque/images/`.

## Annexe du 21/09/2026 : le dépôt ne perd plus l'original (lot borné)

Constat, reproduit par le QA du parent sur une fixture `.md`
(`# Cours`, `2026`, `Objectif : comprendre la source.`) : `preparer`
recopiait l'original vers `sources/<empreinte>.md`, c'est-à-dire vers le
pivot lui-même, puis écrasait ce fichier par le pivot. L'original n'était
plus retrouvable nulle part, et `Document.source()` ne rendait rien. Deux
défauts voisins ont été relevés dans la foulée : un `.txt` ou un `.md`
subissait le nettoyage de transcription (perte des lignes numériques et
des préfixes avant deux-points, `Niveau : 3` par exemple) ; un échec au
milieu d'un `deposer` interrompait le lot et le bilan ne distinguait ni
les succès, ni les documents déjà préparés, ni les échecs.

Résultat attendu : l'original d'un document préparé reste sur disque,
exactement, sous un nom qui ne peut pas heurter le pivot
(`<empreinte>.source.md` pour un Markdown, `<empreinte><extension>`
sinon, nom inchangé pour les documents déjà préparés) ; le texte machine
d'un `.txt` ou d'un `.md` est le document tel qu'il est écrit ; `deposer`
traverse tout le dossier, nomme les échecs et sort non nul s'il en
reste un.

Périmètre : `app/usine/usine.py`, `app/usine/transcription.py`,
`app/usine/etat.py` (chemins et recherche de la source),
`app/usine/pivot.py` (constantes d'extension), `app/tests_usine.py`,
`app/tests.py` (la seule mutation qui cite `deposer`), `sources/README.md`,
cette annexe. Rien d'autre.

Deux points de contrat que la revue a fixés. La recherche de la source
énumère les noms exacts que l'usine archive (`<empreinte>.source.md`,
puis `<empreinte><extension>` pour PDF, `.vtt`, `.srt`, `.txt`) et ne
globe rien : un fichier dérivé déposé à la main près du pivot ne passe
jamais pour l'original. Et `deposer` rend un échec attendu (outil absent,
PDF illisible, archive étrangère, état `.json` corrompu) au lieu de le
propager : le lot continue, le bilan nomme l'échec et la source du
fichier refusé reste sur disque.

Étapes : tests rouges d'abord (`scenario_document_texte`,
`scenario_reparation_archive_source`, `scenario_archive_etrangere`,
`scenario_source_derivee`, `scenario_depot_partiel`), puis le code, puis
`python3 app/tests.py`, `python3 app/tests_usine.py` et
`python3 tooling/check.py`.

Ce qu'on ne fait pas : aucune migration destructive d'un dépôt existant.
Un document préparé avant ce lot garde son état et son pivot ; relancer
`preparer` sur le fichier d'origine réarchive celui-ci à côté du pivot,
sans jamais réécrire le pivot. Aucun document réel n'est préparé ici, et
aucun scellé fictif n'est posé.

Preuve :

```bash
python3 app/tests_usine.py && python3 app/tests.py && python3 tooling/check.py
```

## Preuve

```bash
python3 app/usine/pivot.py sources/322a2f5e843f45b9.pdf && python3 app/tests.py && python3 tooling/check.py
```

JB voit : le pivot Markdown du Focus du CAE, ses pages à figures, sa
fiche, et le coût en tokens d'un rattachement.

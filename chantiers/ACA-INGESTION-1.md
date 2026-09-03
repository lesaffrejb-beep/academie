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

## Périmètre

Peut créer ou modifier : `app/usine/` (nouveau : `pivot.py` qui appelle
`pdftotext`, `pdftohtml -xml`, `pdftoppm`, `pdfimages` ; `fiche.py`
qui écrit la fiche JSON de source ; `transcription.py` pour un `.vtt`
ou un `.srt` : nettoyage, retrait des locuteurs et des horodatages,
jamais un nom dans la sortie), `app/tests_usine.py`, `app/tests.py`
(ajout de la suite), `tooling/requirements-usine.txt` (outils
externes attendus, avec leur licence), `sources/README.md`,
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

## Preuve

```bash
python3 app/usine/pivot.py sources/322a2f5e843f45b9.pdf && python3 app/tests.py && python3 tooling/check.py
```

JB voit : le pivot Markdown du Focus du CAE, ses pages à figures, sa
fiche, et le coût en tokens d'un rattachement.

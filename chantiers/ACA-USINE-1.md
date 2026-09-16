# Cahier ACA-USINE-1 : déposer un PDF, récupérer ses images

Résultat attendu : un dossier de dépôt `sources/a-preparer/` où l'on
jette un PDF ; la commande `deposer` prépare tout ce qui s'y trouve (le
PDF copié sous son empreinte, le texte par page, les pages à figures
rendues, l'extraction des images réelles), saute ce qui est déjà préparé,
et dit quoi faire si l'OCR manque. Le pas à pas de relecture ne change
pas.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : rien. Bloque : rien (facilite `ACA-INGESTION-1`).

## Périmètre

Peut créer ou modifier : `app/usine/usine.py` (commande `deposer`),
`app/usine/pivot.py` (`extraire_images`, un champ de structure),
`app/tests_usine.py` (un scénario), `app/tests.py` (une mutation),
`sources/.gitignore`, `sources/a-preparer/.gitkeep`, `sources/README.md`,
`prompts/ajouter-des-documents.md`.
Ne touche pas : `app/usine/etat.py`, `fiche.py`, le valideur, la banque.

## Déjà tranché (ne pas rouvrir)

- L'usine est locale et pas à pas (decisions/0026, 0027) : `preparer`,
  `declarer`, `suivant`, `valider`, `fiche`, `registre`. `deposer` ne
  fait qu'appeler `preparer` sur un lot.
- Les sources ne sont jamais versionnées (`sources/.gitignore`), sauf le
  registre et la liste blanche.
- Un PDF scanné sans couche texte est signalé (`ocr_requis`) ; l'OCR est
  un outil externe (`ocrmypdf`, tesseract), pas une dépendance du dépôt.
- Rien n'appelle de modèle ni de service.

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_usine.py` (scénario sauté si poppler
   absent) : un PDF déposé dans `sources/a-preparer/` est préparé par
   `deposer`, la structure porte `images_extraites`, un second `deposer`
   saute le document déjà préparé.
2. `pivot.extraire_images` : `pdfimages -png -p` vers
   `<empreinte>.figures/img-*`, à côté des pages rendues ; compté dans la
   structure.
3. `usine.py deposer [--interne]` : prépare chaque fichier du dossier,
   saute les déjà préparés, rappelle la commande OCR si besoin.
4. `sources/a-preparer/` créé et versionné par un `.gitkeep` ; le
   `.gitignore` l'exempte.
5. Une phrase dans `sources/README.md` et dans
   `prompts/ajouter-des-documents.md`.
6. La mutation qui prouve que `deposer` prépare vraiment.

## Ce qu'on ne fait pas

- Aucun OCR automatique qui installe un outil en silence.
- Aucune réécriture du pas à pas ni du valideur.
- Aucune image extraite qui entre dans git.

## Preuve

```bash
python3 app/tests_usine.py && python3 app/tests.py && python3 tooling/check.py
cp ~/Documents/mon-guide.pdf sources/a-preparer/
python3 app/usine/usine.py deposer
```

JB voit : un PDF déposé devient un texte par page, des pages rendues et
des images extraites, prêt pour la relecture et les rattachements.

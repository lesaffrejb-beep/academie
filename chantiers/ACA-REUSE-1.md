# Cahier ACA-REUSE-1 : la réutilisation, licences lues à la source

Résultat attendu : chaque candidat de
`travail/2026-09-02-reutilisation-a-verifier.md` a sa licence lue à la
source et un verdict (reprendre le code, voler le pattern, écarter) ;
rien n'est installé avant.
Fini quand : tableau daté avec URL de licence par ligne ; taille ajoutée
au bundle estimée pour chaque reprise ; aucune AGPL en code.
Dépend de : ACA-DOC-2. Bloque : ACA-FRONT-2.

## Périmètre

Peut créer ou modifier : `travail/2026-09-02-reutilisation-a-verifier.md`
(le tableau des verdicts, daté), `travail/benchmark-2026-08-30.md`
partie 4 (registre des licences vérifiées, étendu), `lab/VEILLE.md`
(une ligne par dépôt avec son verdict).
Ne touche pas : `package.json` (il n'existe pas), `web/`, `serveur/`,
aucun code.

## Déjà tranché (ne pas rouvrir)

- On vole des patterns, on reprend du code permissif avec en-tête de
  provenance, on n'importe jamais un framework d'apprentissage entier ;
  AGPL et GPL : idées seulement (`decisions/0007`,
  `travail/benchmark-2026-08-30.md`).
- Le client est jetable ; ce qui entre doit pouvoir sortir.
- Budget : bundle client < 400 Ko gzippé, première question < 3 s
  (`decisions/0007`).

## Étapes, dans l'ordre

1. Pour chaque ligne : ouvrir le fichier LICENSE du dépôt (pas le badge
   GitHub, pas la mémoire), noter l'URL et la date.
2. Pour chaque « reprendre » : nommer le ou les fichiers à reprendre, la
   taille, et ce qu'on adaptera (contrat, DA, voix).
3. Pour chaque « écarter » : le motif en une phrase.
4. Compléter avec les banques d'éléments (icônes, animation, UI,
   illustrations, polices, sons) déjà notées le 03/09/2026 en fin de
   fichier, en confirmant chaque licence à sa source.
5. Une ligne par dépôt dans `lab/VEILLE.md` avec le verdict.

## Ce qu'on ne fait pas

- Pas d'installation, pas de `npm init`, pas de code.
- Pas de verdict de mémoire : une licence non lue est « à vérifier »,
  pas « MIT ».

## Preuve

```bash
python3 tooling/check.py
```

JB voit : le tableau final, et pour chaque « reprendre », ce qu'on
prend et ce que ça pèse.

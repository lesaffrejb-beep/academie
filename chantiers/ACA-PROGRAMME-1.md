# Cahier ACA-PROGRAMME-1 : le programme validé et branché

Résultat attendu : `app/valide_programme.py` valide
`programme/<metier>.json` (prérequis existants et de niveau ≤, pas de
cycle, clés cohérentes), `academie.json` aligné (`plans` → `travaux`,
`immobilier` et `cabinet` ajoutés, ordre du programme), niveaux calibrés
par un agent frais contre `PROGRAMME.md` §5.
Fini quand : valideur vert en CI sur `programme/copro.json` ; rapport de
calibrage listant les chapitres reclassés et pourquoi ; tests existants
verts avec les nouvelles clés.
Dépend de : ACA-DOC-2. Bloque : ACA-CONTRAT-2, ACA-ARBRE-1,
ACA-SEMAINE-1, ACA-FRONT-2.

## Périmètre

Peut créer ou modifier : `app/valide_programme.py`,
`app/tests_programme.py`, `app/tests.py` (ajout de la suite et d'une
mutation), `tooling/check.py` (remplacer le contrôle inline du programme
par un appel au valideur), `academie.json` (clés, titres, ordre),
`programme/copro.json` (niveaux reclassés, `disposition` si le calibrage
la produit), `banque/**/*.json` **seulement** pour renommer le domaine
`plans` s'il y a des cartes (il n'y en a pas au 03/09), `PROGRAMME.md`
§2 et §5 si le calibrage change une ligne.
Ne touche pas : le moteur (`seance.py`, `progression.py`), les
contrats, `chapitres/`.

## Déjà tranché (ne pas rouvrir)

- Les clés et l'ordre : `PROGRAMME.md` §2, `decisions/0023`.
- L'échelle 1-5 et ses ancres : `decisions/0003`, `PROGRAMME.md` §5.
- Le socle : niveau 2 partout, 3 en droit, comptabilité, cabinet
  (`decisions/0013`, `PROGRAMME.md` §3).
- Le JSON fait foi sur le texte (`programme/README.md`).
- Le calibrage est fait par un agent frais qui n'a pas écrit le
  programme, contre la grille et les ancres publiques
  (`decisions/0022`).

## Étapes, dans l'ordre

1. Tests rouges (`app/tests_programme.py`) : identifiant dupliqué,
   prérequis inconnu, prérequis de niveau supérieur, cycle, domaine ou
   branche non déclarés, clé de `academie.json` absente du programme et
   l'inverse, `socle.niveaux` hors 1-5, semaine type incomplète.
2. `app/valide_programme.py` : stdlib, `ACADEMIE_RACINE`, sortie 0 ou 1,
   `--json`.
3. Aligner `academie.json` ; lancer `app/tests.py` (la banque réelle et
   `progression.py` lisent les clés : rien ne doit casser ; la région
   `plans` sans carte devient `travaux`).
4. Calibrage par agent frais : un rapport `travail/calibrage-programme-AAAA-MM-JJ.md`
   avec, par chapitre reclassé, le niveau avant, après, et la raison
   (grille de `decisions/0003`, ancre BTS PI / RNCP / doctrine).
   Appliquer dans le JSON ; ne pas toucher aux identifiants.
5. `tooling/check.py` appelle le valideur ; mutation ajoutée à
   `tests.py`.

## Ce qu'on ne fait pas

- Pas de contenu, pas de chapitre.
- Pas de renumérotation d'identifiant de chapitre : un identifiant
  publié est immuable.
- Pas de nouvelle règle de socle sans décision.

## Preuve

```bash
python3 app/valide_programme.py && python3 app/tests.py && python3 tooling/check.py
```

JB voit : le rapport de calibrage, lisible, et `academie.json` avec les
onze clés dans l'ordre du programme.

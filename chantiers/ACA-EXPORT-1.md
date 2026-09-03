# Cahier ACA-EXPORT-1 : l'export Anki, assurance-vie de réversibilité

Résultat attendu : `app/export_anki.py` produit un `.apkg` de n'importe
quel sous-ensemble de la banque (v1 aujourd'hui, chapitres v2 dès qu'ils
existent).
Fini quand : un paquet importé dans Anki sans erreur ; licence de
`genanki` vérifiée à la date ; test qui compare le nombre de notes au
nombre de cartes servies.
Dépend de : ACA-ENGINE-1. Bloque : rien.

## Périmètre

Peut créer ou modifier : `app/export_anki.py`, `app/tests_export.py`,
`app/tests.py` (ajout de la suite), `tooling/requirements-usine.txt`
(nouveau : les dépendances de l'usine, jamais du produit),
`CONTRAT-CARTE-V1.md` §4 (mise à jour de la phrase « à construire »).
Ne touche pas : `genere.py`, le client, le serveur.

## Déjà tranché (ne pas rouvrir)

- L'export est une assurance-vie, le livrable de personne
  (`CONTRAT-CARTE-V1.md` §4, `decisions/0008`).
- `genanki` (MIT, vérifié le 30/08/2026) est une dépendance de l'usine,
  pas du produit joué (`travail/benchmark-2026-08-30.md` §1.3).
- Colonnes : question, réponse (explication et vigilance incluses),
  source, tags `domaine::branche`.

## Étapes, dans l'ordre

1. Test rouge : export d'une banque de fixture de trois cartes → trois
   notes, tags corrects, source dans le champ arrière.
2. `export_anki.py` : lit `banque/` via `valide_banque.charge_banque`
   (cartes `valide` seulement par défaut, `--avec-brouillons` explicite),
   filtre `--domaine`, `--couches`, écrit un `.apkg` ; modèle Anki avec
   trois champs (Recto, Verso, Source).
3. Relire la licence de `genanki` à la date, noter l'URL dans le
   registre.
4. Import manuel dans Anki par JB (preuve humaine).

## Ce qu'on ne fait pas

- Pas d'import depuis Anki vers l'Académie.
- Pas d'export de l'état joueur (c'est `/journal/export`).

## Preuve

```bash
python3 app/export_anki.py --domaine droit --sortie /tmp/droit.apkg && python3 app/tests.py
```

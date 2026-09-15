# Cahier ACA-SANS-FRONT-4 : le journal de la surface est au contrat v1

Résultat attendu : la surface écrit un journal conforme à
`contrats/journal-v1.schema.json` : une ligne `mode: seance` qui ouvre la
séance (format, graine, banque_version, moteur_version, cartes) et des
lignes `mode: revision` avec `format` et `nonce`. Le rapport
`app/rituel.py` lit alors le journal sans ligne écartée, et le serveur
pourra l'unionner. La commande `rituel` est exposée.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-SANS-FRONT-3. Bloque : la synchronisation réelle
(`ACA-PUBLICATION-2`, `ACA-RITUAL-1`).

## Périmètre

Peut créer ou modifier : `app/seance.py` (deux fonctions ajoutées, la
fonction existante `note` inchangée), `app/academie.py` (`repondre` en
v1, `seance --journaliser`, commande `rituel`), `app/tests_academie.py`,
`app/tests.py` (une mutation), `prompts/jouer.md`,
`skills/academie/SKILL.md`.
Ne touche pas : `app/seance.py:note` (le mode `flash` reste pour les
appelants existants), `app/rituel.py`, la banque, `serveur/` (qui sait
déjà unir du v1), `web/` (archivé).

## Déjà tranché (ne pas rouvrir)

- Le contrat des lignes est `contrats/journal-v1.schema.json` : `quand`,
  `mode`, `nonce` obligatoires ; `format`, `graine`, `banque_version`,
  `moteur_version` obligatoires pour `mode: seance` ; `carte`, `note`,
  `format` pour `mode: revision`.
- `app/rituel.py` ne lit que les modes v1 et ne se modifie pas : c'est
  la surface qui se met au contrat, jamais le lecteur qui s'assouplit.
- La migration v0 (`mode: flash` vers `revision`) est celle de
  `serveur/importer_journal.py` ; les anciens journaux restent lisibles
  par `seance.etats_cartes`, qui ignore le mode.
- L'état reste local et append-only ; `note` reste en place pour ne rien
  casser.

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_academie.py` :
   - `repondre` écrit une ligne `mode: revision` avec `format` et
     `nonce` ;
   - `seance --journaliser` écrit une ouverture `mode: seance` qui
     annonce ses cartes ;
   - `rituel` sur le journal ainsi produit ne compte aucune ligne
     écartée, voit une séance finie, et sort vide sur un journal absent.
2. `seance.note_v1` et `seance.ouvre_seance` dans `app/seance.py`.
3. `app/academie.py` : `repondre` appelle `note_v1`, `seance` accepte
   `--journaliser`, commande `rituel` qui appelle `rituel.rapport`.
4. Les versions : `banque_version` = empreinte courte des identifiants
   jouables servis, `moteur_version` = un identifiant de surface assumé
   comme provisoire, écrits tels quels dans la ligne d'ouverture.
5. Une phrase dans `prompts/jouer.md` et `skills/academie/SKILL.md`.
6. La mutation qui prouve qu'une ligne de révision sans `format` est vue.

## Ce qu'on ne fait pas

- Aucune réécriture de l'ancien journal.
- Aucun assouplissement de `app/rituel.py`.
- Aucun vrai schéma de version inventé : une empreinte et un identifiant
  provisoire, nommés comme tels.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py seance --journaliser
python3 app/academie.py rituel
```

JB voit : le journal produit par la surface est lisible par le rapport du
rituel, donc l'habitude devient mesurable et la synchronisation possible.

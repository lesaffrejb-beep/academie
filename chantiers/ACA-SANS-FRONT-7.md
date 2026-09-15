# Cahier ACA-SANS-FRONT-7 : sauvegarder et transférer l'état local

Résultat attendu : `exporter <fichier>` produit une sauvegarde lisible
du journal et du carnet du profil ; `importer <fichier>` les fusionne par
union, sans jamais écraser ni dupliquer. C'est la réponse locale à deux
appareils : le Mac écrit, le portable importe, rien ne se perd.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-SANS-FRONT-6. Bloque : rien (le serveur reste la voie de
synchronisation continue, `ACA-PUBLICATION-2`).

## Périmètre

Peut créer ou modifier : `app/academie.py` (`exporter`, `importer`, un
helper d'union, les clés de déduplication), `app/tests_academie.py`,
`app/tests.py` (une mutation), `skills/academie/SKILL.md`.
Ne touche pas : le moteur, la banque, `serveur/` (qui a déjà son union),
`web/`.

## Déjà tranché (ne pas rouvrir)

- L'état est append-only et hors git : `etat/<profil>/revues.jsonl` et
  `erreurs.jsonl`. L'écriture à chaque réponse EST la sauvegarde continue.
- L'union se fait sur une clé stable : `nonce` pour une ligne de journal,
  `(quand, carte, mode, raison)` pour le carnet qui n'en porte pas.
- On n'écrase jamais : un import ajoute ce qui manque, rien d'autre.
- Le format de sauvegarde est versionné (`academie-sauvegarde-1`) pour
  qu'un futur changement ne casse pas un fichier ancien.

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_academie.py` :
   - exporter puis importer dans un état neuf rend le même nombre de
     lignes ; réimporter n'ajoute rien (idempotence) ;
   - un import n'efface pas les lignes déjà présentes : l'union s'ajoute ;
   - un fichier illisible ou d'un autre format est un trou nommé.
2. `cmd_exporter`, `cmd_importer`, `_union_append` dans `app/academie.py`.
3. Une phrase dans `skills/academie/SKILL.md`.
4. La mutation qui prouve que l'import déduplique.

## Ce qu'on ne fait pas

- Aucune synchronisation en ligne : c'est le rôle du serveur, plus tard.
- Aucune réécriture ni tri des fichiers locaux : on ajoute des lignes.
- Aucun secret : la sauvegarde ne contient que le journal et le carnet.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py exporter ~/academie-sauvegarde.json
python3 app/academie.py importer ~/academie-sauvegarde.json
```

JB voit : un fichier de sauvegarde, un import qui s'ajoute à ce qu'il a
déjà, et un second import qui ne crée rien.

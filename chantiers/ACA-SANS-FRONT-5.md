# Cahier ACA-SANS-FRONT-5 : le cursus actif et l'isolation

Résultat attendu : la surface joue UN cursus à la fois. `--cursus <cle>`
choisit le programme de `programme/catalogue.json`, les cartes sont
isolées à ses domaines (une carte IFSI ne tombe plus dans une séance
copro), et `cursus <cle>` inscrit le choix au journal (`mode: cursus`).
Sans `--cursus`, le dernier choix journalisé fait foi, sinon le premier
parcours du catalogue.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-SANS-FRONT-4. Bloque : l'entrée réelle d'Arthur et de
tout second cursus.

## Périmètre

Peut créer ou modifier : `app/academie.py` (helpers de cursus, option
`--cursus`, commande `cursus`, contexte filtré), `app/tests_academie.py`,
`app/tests.py` (une mutation), `prompts/jouer.md`,
`skills/academie/SKILL.md`.
Ne touche pas : `programme/` (les cursus existent déjà), `academie.json`
(la config moteur commune), le moteur, la banque, `serveur/`, `web/`.

## Déjà tranché (ne pas rouvrir)

- Les programmes vivent dans le repo : `programme/catalogue.json` liste
  les cursus, chacun avec son fichier `programme/*.json` (domaines,
  branches, chapitres, socle, semaine type). Tout le monde les a en
  clonant ; aucun cursus n'est privé.
- L'état joueur reste local et par pseudo : `etat/<pseudo>/`. Deux
  personnes sur une machine = deux dossiers ; deux machines = deux
  journaux locaux, jamais dans git.
- L'événement `mode: cursus` porte `cursus` (contrat `journal-v1`) ; le
  serveur le connaît déjà (0045, 0053). On l'écrit localement ici.
- `charge_programme()` reste le repli quand il n'y a pas de catalogue
  (racines de test sans programme).

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_academie.py` :
   - deux cursus A (domaines droit) et B (domaines entree) sur une
     racine jetable : `seance --cursus A` ne sert que des cartes droit,
     `--cursus B` que des cartes entree ;
   - sans `--cursus`, le premier parcours du catalogue fait foi ;
   - `cursus B` écrit un `mode: cursus`, et la séance suivante sans
     `--cursus` sert alors le cursus B ;
   - un cursus inconnu est un trou nommé, aucune carte servie.
2. Helpers dans `app/academie.py` : `charge_catalogue`, `charge_cursus`,
   `cursus_actif`, `config_du_cursus`, `_ecrit_cursus`.
3. `charge_contexte` filtre les cartes aux domaines du cursus et
   remplace `domaines`/`socle`/`semaine_type` par ceux du programme.
4. `--cursus` sur les options communes ; commande `cursus [<cle>]`.
5. La mutation qui prouve que l'isolation mord.

## Ce qu'on ne fait pas

- Aucun cursus recopié dans `academie.json` : le programme fait foi.
- Aucun état de cursus stocké ailleurs que dans le journal.
- Aucun déplacement de carte entre cursus.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py cursus
python3 app/academie.py cursus ifsi
python3 app/academie.py seance --profil arthur
```

JB voit : sa séance ne contient que du copro ; Arthur choisit l'IFSI une
fois (`cursus ifsi`) et ses séances suivantes ne contiennent que de
l'IFSI ; leurs journaux sont séparés.

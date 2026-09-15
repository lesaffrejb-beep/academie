# Cahier ACA-SANS-FRONT-6 : la surface charge aussi les chapitres v2

Résultat attendu : la surface joue les cartes v1 de `banque/` ET les
cartes v2 de `chapitres/`, par le même chemin que `app/genere.py` (les
deux valideurs, couches banque et interne, sans brouillon). Sans ce
chargement, 92 cartes valides dont les 34 IFSI restaient invisibles, et
Arthur n'avait aucune carte à jouer.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-SANS-FRONT-5. Bloque : l'entrée réelle d'Arthur.

## Périmètre

Peut créer ou modifier : `app/academie.py` (un helper de chargement, le
contexte), `app/tests_academie.py`, `app/tests.py` (une mutation).
Ne touche pas : `app/genere.py`, `app/valide_chapitres.py`, la banque,
les chapitres, `serveur/`, `web/`.

## Déjà tranché (ne pas rouvrir)

- `app/genere.py` sert déjà les deux dispositions : `banque/` par
  `charge_banque`, `chapitres/` par `valide_chapitres` et la règle de
  transition. La surface fait le même geste, elle ne réinvente rien.
- Les deux valideurs font foi : une erreur d'un côté arrête la surface.
- Aucun identifiant n'est servi deux fois (genere refuse un doublon).

## Étapes, dans l'ordre

1. Test rouge : sur le dépôt réel, `seance --cursus ifsi` sert au moins
   une carte d'un domaine IFSI ; avant le correctif, aucune.
2. `charge_cartes_du_depot` dans `app/academie.py` : `charge_banque`
   plus `genere.charge_cartes_v2({"banque","interne"}, False, today)`,
   erreurs cumulées.
3. La mutation qui prouve que le v2 est bien chargé.

## Ce qu'on ne fait pas

- Aucun accès au fichier publié `site/banque.json` : la source reste la
  banque et les chapitres, pas un artefact.
- Aucune inclusion de la couche `perso` ni des brouillons.
- Aucun changement au valideur.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py seance --cursus ifsi --json
```

JB voit : sa séance copro inclut désormais les cartes v2 ; Arthur a des
cartes IFSI à jouer.

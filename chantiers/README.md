# chantiers/

Un cahier par item de `roadmap.json` qu'un agent peut prendre. Sans
cahier, pas de code (`CONTRIBUER.md`, `decisions/0025`) ; `check.py`
refuse un item `ready` sans cahier.

Le gabarit d'un cahier :

```
# Cahier <ID> : <titre>

Résultat attendu : (copié de roadmap.json)
Fini quand : les tests nommés ici sont verts, plus tests.py et check.py.
Dépend de : … Bloque : …

## Périmètre
Peut créer ou modifier : …
Ne touche pas : …

## Déjà tranché (ne pas rouvrir)
- … (renvoi vers la décision ou le document)

## Étapes, dans l'ordre
1. Écrire les tests rouges : …
2. …

## Ce qu'on ne fait pas
- …

## Preuve
Commandes à lancer ; ce que JB doit voir.
```

Cahiers écrits le 03/09/2026 : les six items `ready` et les cinq qui
suivent. Un item qui passe `ready` sans cahier bloque `check.py` : on
écrit le cahier d'abord.

# 0025, Le cadre d'exécution : un LLM ne code pas sans cahier, et la machine le vérifie

- Statut : acceptée
- Date : 03/09/2026
- Décideur : agent, sur demande de JB (« poser les bases pour qu'on ne
  puisse plus dévier ; que tout soit tellement cadré qu'un autre LLM ne
  puisse pas dévier en codant »)

## Décision

1. **Aucun chantier ne se code sans son cahier** dans `chantiers/<id>.md`.
   Le cahier dit le résultat attendu, la preuve exécutable de « fini »,
   les fichiers qu'on a le droit de toucher, ceux qu'on n'a pas le droit
   de toucher, ce qui est déjà tranché avec ses renvois, les étapes dans
   l'ordre, et ce qu'on ne fait pas. `tooling/check.py` refuse un item
   `ready` de `roadmap.json` sans cahier.
2. **Les règles vivent dans des contrôles, pas dans la prose.** Tout ce
   qu'un document interdit et qu'une machine peut vérifier est vérifié
   par `tooling/check.py` ou par un test d'`app/tests.py` : vocabulaire,
   voix, tirets, JSON des contrats, cohérence programme et roadmap,
   décisions indexées, chapitres v2 au contrat, aucun import de labor,
   aucun hôte tiers dans le client. Une règle qu'on ne sait pas vérifier
   s'écrit quand même, et son contrôle est un chantier.
3. **Une définition exécutable de « fini » avant de commencer** : les
   tests nommés dans le cahier s'écrivent d'abord, rouges, puis le code
   les fait passer. Un chantier sans test rouge au départ n'a pas
   commencé.
4. **Le périmètre est fermé** : un chantier qui a besoin de toucher un
   fichier hors de son périmètre s'arrête et le dit ; il n'élargit pas
   tout seul. Un agent qui découvre une contradiction entre deux
   documents la règle par la précédence de `DOCTRINE.md` §4 et laisse
   une ligne dans `decisions/`, il ne choisit pas en silence.
5. **Le contrat avant le code** : une frontière (banque publiée, journal,
   livraison, API) se code contre son schéma de `contrats/` ou contre
   `serveur/API.md` ; un écart se règle en changeant le contrat par
   décision, jamais en adaptant le code au coup par coup.
6. **La relecture par un agent qui n'a pas écrit** reste obligatoire pour
   tout livrable à enjeu (contenu, contrat, sécurité) ; « aucun
   bloquant » est un verdict recevable.
7. **Le tout est écrit dans `CONTRIBUER.md`**, la constitution
   d'exécution, lue par tout agent avant sa première ligne, en plus de
   `AGENTS.md`.

## Contexte

Le 02/09, la conception v2 a été écrite en une journée, puis relue :
4 red paths et 16 bloquants sont venus de documents qui se
contredisaient ou promettaient ce que le code ne faisait pas. Une
doctrine en prose ne tient pas seule ; ce que dit `labor/domaine/doctrine-harnais.md`
(« vérification mécanique, hors modèle ; contrat avant action ») est
la réponse.

## Conséquences

- `CONTRIBUER.md`, `chantiers/`, `tooling/check.py` étendu,
  `app/valide_chapitres.py` et `app/tests_chapitres.py` écrits le
  03/09/2026.
- `AGENTS.md` règle 8 : « tu ne codes pas sans cahier ».

## Réouverture

Si les contrôles bloquent un chantier légitime plus d'une fois par
semaine, on relit le contrôle, pas la règle.

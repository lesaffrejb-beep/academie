# Cahier ACA-ONBOARDING-2 : l'arrivée d'un élève, sans front

Écrit le 16/09/2026 sur la demande de JB. Succède à
[`ACA-ONBOARDING-1`](ACA-ONBOARDING-1.md), qui visait le client web
retiré par [`decisions/0054`](../decisions/0054-plus-de-front-le-depot-est-l-interface.md).

Résultat attendu : au premier message, l'agent lit un seul document
local, `etat/<pseudo>/profil.json` (hors git), pour savoir qui joue,
quel cursus, quelle voix et quel niveau d'exigence. Si ce document
n'existe pas, l'agent conduit l'arrivée une fois : choisir un cursus
(copropriété, infirmier, ou « aucun, il m'en faut un autre »), dire le
pseudo et où l'état vit sur la machine, indiquer où déposer des
documents, présenter les choix disponibles, choisir une voix de
professeur et un niveau d'exigence, puis écrire le profil.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : `ACA-SANS-FRONT-1` à `ACA-SANS-FRONT-7`. Bloque : rien.

Décision de référence : [`decisions/0056`](../decisions/0056-arrivee-locale-et-profil-du-joueur.md).

## Périmètre

Peut créer ou modifier : `contenu/arrivee.json` (nouveau : voix,
exigences, zones de dépôt), `app/academie.py` (commandes `accueil` et
`profil`, exigence appliquée au moteur), `app/tests_academie.py`,
`app/tests.py` (une mutation), `skills/academie/SKILL.md`,
`prompts/arriver.md` (nouveau), `prompts/README.md`.
Ne touche pas : le moteur (`planificateur.py`, `seance.py`,
`progression.py`, `quiz.py`, `erreurs.py`), la banque, les valideurs,
`serveur/`, `web/`, le format du journal.

## Déjà tranché (ne pas rouvrir)

- Les préférences vivent dans `etat/<pseudo>/profil.json`, hors git, à
  côté du journal (`decisions/0056`). La progression reste un journal
  append-only ; un profil est une préférence, pas une mesure.
- Trois registres de voix, tous dans le cadre de `VOIX.md` (pas
  d'exclamation, pas d'emoji, pas de mot du jeu, jamais « je »).
- Trois niveaux d'exigence qui pilotent le moteur (rétention FSRS,
  cartes neuves par séance, seuil de reprise) et le ton des corrections.
- Le cursus reste un événement du journal (`mode: cursus`) ; le profil
  sert de repli quand aucun choix n'est encore journalisé.
- Le dépôt de documents existe déjà : `sources/a-preparer/` (public) et
  `sources/interne/a-preparer/` (privé), traités par
  `python3 app/usine/usine.py deposer [--interne]`. L'arrivée le nomme,
  elle n'en invente pas un second.
- « Créer le vôtre » reste `CHEMINS.md` et
  `prompts/creer-un-parcours.md`. Aucun envoi vers un tiers.

## Étapes, dans l'ordre

1. Tests rouges (`app/tests_academie.py`) :
   - sans profil, `accueil --json` dit `profil_existe` faux, nomme le
     trou et sert le catalogue, les voix, les exigences et le dépôt ;
   - `profil` sans profil écrit est un trou nommé ;
   - `profil --pseudo jb --cursus a --voix sobre --exigence standard`
     écrit `etat/<pseudo>/profil.json` et se relit à l'identique ;
   - une voix inconnue, une exigence inconnue ou un pseudo vide sont
     refusés sans rien écrire ;
   - sans événement `cursus` au journal, la séance suit le cursus du
     profil ; un événement `cursus` journalisé l'emporte ;
   - un profil `exigeant` change les intervalles de `prevue` par rapport
     au même profil `detendu`, et la parité sans profil avec le moteur
     reste exacte.
2. `contenu/arrivee.json` : voix, exigences, dépôt.
3. `app/academie.py` : `accueil`, `profil`, repli de cursus, exigence
   appliquée à `config["fsrs"]["retention_souhaitee"]`,
   `config["quotas"]["nouveau_par_seance"]` et
   `config["erreurs"]["seuil_echecs"]`.
4. `skills/academie/SKILL.md` et `prompts/arriver.md` : le geste du
   premier message, sans nouvelle mécanique.
5. `app/tests.py` : la mutation qui prouve que l'exigence est bien
   appliquée.

## Ce qu'on ne fait pas

- Aucun écran, aucun serveur, aucune dépendance graphique.
- Aucun compte, aucun mail, aucun mot de passe : le pseudo suffit.
- Aucune écriture du moteur : la surface applique la config, elle ne
  recompose ni FSRS ni la séance.
- Aucun fichier du joueur dans git : `etat/` reste hors versionnement.
- Aucune voix hors `VOIX.md`, aucun classement de modèles.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py accueil --json
python3 app/academie.py profil --pseudo jb --cursus copro --voix sobre --exigence standard
```

JB voit : sur une racine neuve, `accueil` propose copro, ifsi et
« créer le vôtre », nomme la zone de dépôt, écrit un profil et le
relit ; l'exigence choisie change la prochaine échéance sans toucher au
moteur ; `check.py` reste vert.

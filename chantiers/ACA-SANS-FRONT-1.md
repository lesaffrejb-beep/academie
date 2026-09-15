# Cahier ACA-SANS-FRONT-1 : jouer dans le dépôt, sans écran

Résultat attendu : plus de client web ; l'agent est l'écran, le moteur
reste le professeur. Une surface mince (commandes Python et consignes par
outil) joue une séance de bout en bout, journalise en local et ouvre les
artefacts HTML jetables.
Fini quand : les tests nommés ici sont verts, plus `app/tests.py` et
`tooling/check.py`.
Dépend de : ACA-ENGINE-1, ACA-JOURNAL-SYNC-1. Bloque : la reprise des
items qui pointaient vers `ACA-FRONT-2` (ACA-ETUDE-1, ACA-EXAMEN-1,
ACA-CERCLE-1, ACA-SELFHOST-1).

Décision de référence : [`decisions/0054`](../decisions/0054-plus-de-front-le-depot-est-l-interface.md).

## Périmètre

Peut créer ou modifier : `app/academie.py` (nouveau, la surface en
ligne de commande), `app/tests_academie.py` (nouveau), `app/tests.py`
(ajout de la suite et d'une mutation), `skills/` (un fichier de consignes
par outil : OpenCode, Claude Code, Codex, Gemini, Antigravity),
`prompts/jouer.md` (nouveau), `AGENTS.md` et adaptateurs si un renvoi
manque, `.gitignore` (`sorties/`).
Ne touche pas : le moteur (`planificateur.py`, `seance.py`,
`progression.py`, `quiz.py`, `erreurs.py`) qui fait foi sans changement,
la banque, les valideurs, `serveur/` (conservé, non branché par défaut),
`web/` (déjà archivé par 0054).

## Déjà tranché (ne pas rouvrir)

- Le moteur est la référence et ne dépend d'aucun modèle : l'agent lit
  ses sorties, il ne recompose jamais une séance (`decisions/0007`,
  invariant 5).
- Le journal est append-only, se rejoue, n'est jamais dans git
  (invariant 6). Un fichier par joueur : `etat/<pseudo>/journal.jsonl`.
- Aucune branche par joueur : le dépôt partagé porte le code et la
  banque ; le carnet reste local.
- Rien de rouge n'est servi : seules les cartes validées et leur
  provenance entrent dans la conversation (`app/valide_banque.py`).
- L'état local est le défaut ; `serveur/` reste la voie de
  synchronisation quand deux appareils l'exigeront (0054).
- La comparaison des dépôts existants (`spacedrep`, `learn-anything`,
  `agent-tutor-skill`) est une étape suivante, licences lues à la source
  (`ACA-REUSE-1`).

## Étapes, dans l'ordre

1. Tests rouges (`app/tests_academie.py`) :
   - depuis un journal fixture, `academie seance` rend exactement la
     séance de `app/seance.py` (mêmes cartes, même ordre, même graine) ;
   - `academie repondre` ajoute une ligne au journal sans écraser
     l'existant, et la rejoue à l'identique ;
   - `academie progression` recalcule le même état que
     `app/progression.py` ;
   - sans banque ni réseau, la surface sort un trou nommé au lieu d'une
     carte inventée.
2. `app/academie.py` : la surface. Sous-commandes au minimum `etat`,
   `seance`, `carte`, `repondre`, `progression`, `qcm`, `schema`. Sortie
   lisible pour un humain et `--json` pour l'agent. Aucune dépendance
   nouvelle.
3. `skills/` : une consigne par outil qui dit à l'agent de lire
   `AGENTS.md`, d'appeler la surface, de présenter une carte à la fois,
   de journaliser la réponse, et de ne jamais inventer un fait. Renvois
   dans les adaptateurs existants (`CLAUDE.md`, `GEMINI.md`,
   `.agents/rules/academie.md`, `.cursor/rules/academie.mdc`).
4. `prompts/jouer.md` : le geste d'une séance de quinze minutes, collable
   dans n'importe quel outil, dans la voix de `VOIX.md`.
5. Artefacts `qcm` et `schema` : écrire un HTML autonome dans `sorties/`
   (`sorties/` gitignored), l'ouvrir, ne rien garder. Le QCM respecte
   `VOIX.md` §7 (quatre choix plausibles, chaque faux dit pourquoi).
6. Micro : une phrase dans les consignes qui encourage la dictée de la
   machine, sans coder aucun moteur audio.
7. Brancher la suite dans `app/tests.py` et ajouter la mutation qui
   prouve que la surface retombe bien sur `app/seance.py`.

## Ce qu'on ne fait pas

- Aucun nouvel écran, aucune dépendance graphique, aucun serveur.
- Aucune écriture du moteur : la surface appelle, elle ne réimplémente
  pas FSRS, la composition ni la progression.
- Aucun appel de modèle côté dépôt : le modèle est celui de l'outil que
  le joueur a ouvert, à son coût (`decisions/0020`).
- Aucun état ni artefact dans git : `etat/` et `sorties/` restent hors
  versionnement.
- Rien qui rouvre `web/` ou `client/`.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/academie.py seance --journal etat/jb/journal.jsonl
python3 app/academie.py qcm <carte> --ouvrir
```

JB voit : depuis un dépôt cloné, sans navigateur ni serveur, une séance
proposée par le moteur, une carte répondue et journalisée, un QCM HTML
affiché, et `check.py` qui refuse le retour du front.

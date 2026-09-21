# Cahier ACA-PORTABILITE-1 : l'installation tient sur un poste Windows

Écrit le 21/09/2026 sur la demande de JB : le dépôt sera cloné sur son
Windows de travail (Antigravity ou Codex) et chez Arthur, autre joueur
sur une autre machine. Ce cahier borne la portabilité de l'installation
du hook et des vérifications du dépôt. Il ne touche ni le moteur, ni la
banque, ni l'arrivée d'un élève.

Résultat attendu : `python app/installation_precommit.py` (ou `python3`)
pose un hook qui fonctionne dans le `sh` de Git pour Windows, dans le
dépôt comme dans un worktree, sans dépendre d'un interpréteur figé ;
`tooling/check.py` retrouve le hook par `git` et lit les sorties en
UTF-8 ; un clone neuf sans hook dit quoi faire, et la CI installe le
hook avant de vérifier.

Fini quand : `app/tests_garde.py` vert avec les cas worktree et
interpréteur, puis `app/tests.py` et `tooling/check.py` verts, et la CI
déclare le job Windows.

Dépend de : `ACA-PRECOMMIT-1` (le hook et son garde), `ACA-ONBOARDING-2`
(l'arrivée d'un élève). Bloque : rien.

## Périmètre

Peut créer ou modifier : `app/installation_precommit.py`,
`app/tests_garde.py`, `app/tests.py` (encodage du lanceur et une
mutation), `tooling/check.py`, `.github/workflows/check.yml`,
`chantiers/ACA-PORTABILITE-1.md`, `roadmap.json` (cet item),
`app/garde_confidentialite.py` (encodage de `git diff` seulement).
Ne touche pas : la détection du garde et ses motifs, `app/academie.py`,
`contenu/arrivee.json`, `prompts/arriver.md`, `skills/academie/`, le
moteur, la banque, les valideurs, `serveur/`.

## Déjà tranché (ne pas rouvrir)

- Le hook reste un script `sh` : Git pour Windows exécute les hooks
  avec le `sh` qu'il embarque.
- L'interpréteur est cherché à l'exécution (`python3`, puis `python`,
  puis le chemin absolu enregistré à l'installation). Un joueur Windows
  tape `python`, un joueur mac ou Linux tape `python3`.
- Le hook retrouve la racine par `git rev-parse --show-toplevel` : un
  worktree utilise donc son propre `app/`, pas celui du dépôt principal.
- Le dossier du hook se trouve par `git rev-parse --git-path
  hooks/pre-commit` : dans un worktree, `.git` est un fichier, pas un
  dossier, et les hooks sont partagés avec le dépôt principal.
- Un hook inconnu (non vide, sans la marque `academie-precommit`) n'est
  jamais écrasé ; un hook déjà académique est réécrit à l'identique
  (idempotence).
- Les sous-processus qui lisent git ou Python déclarent leur encodage
  UTF-8 ; le garde lit `git diff --cached` en UTF-8.
- La CI installe le hook avant `check.py` : un clone neuf ne porte
  jamais `.git/hooks/`, puisque les hooks ne sont pas versionnés. Le job
  Windows est ajouté en preuve d'exécution, sans promettre un poste
  Windows réel avant sa première exécution.

## Étapes, dans l'ordre

1. Tests rouges dans `app/tests_garde.py` :
   - le hook généré nomme l'interpréteur détecté et la racine, sans
     `python3` en dur comme seul chemin ;
   - le hook exécuté bloque un commit porteur de motif même quand aucun
     `python3` n'est dans le `PATH` ;
   - `installation_precommit.py` pose le hook depuis un worktree et
     `check.py` le retrouve là (`git rev-parse --git-path hooks`) ;
   - un hook inconnu reste intact et l'installation sort en erreur ;
   - `check.py` ne se signale plus lui-même quand le dépôt est atteint
     par un chemin symbolique (`/tmp` vers `/private/tmp`).
2. `app/installation_precommit.py` : recherche de l'interpréteur,
   racine et dossier de hooks par `git`, contenu de hook portable.
3. `tooling/check.py` : chemin du hook par `git`, encodage UTF-8 des
   sous-processus, sortie en UTF-8, comparaison des chemins résolus.
4. `app/tests.py` et `app/garde_confidentialite.py` : encodage UTF-8
   des sous-processus et de la sortie.
5. `.github/workflows/check.yml` : étape d'installation du hook avant
   `check.py`, job `windows-latest`.
6. Preuve : tests, `check.py`, clone neuf sans hook, worktree.

## Ce qu'on ne fait pas

- Aucune promesse d'un Windows constaté : seul le job CI ou un poste
  réel le dira.
- Aucune réécriture de la détection du garde, aucun nouveau motif.
- Aucun hook versionné dans le dépôt : il reste local par conception
  (`ACA-PRECOMMIT-1`).
- Aucune dépendance nouvelle, aucun `--no-verify` automatique, aucun
  acte irréversible.
- Aucune reprise de l'arrivée d'un élève : elle appartient à
  `ACA-ONBOARDING-2` et à l'agent qui la tient. Ce cahier lui laisse la
  commande à appeler au premier message.

## Preuve

```bash
python3 app/tests_garde.py
python3 app/tests.py
python3 tooling/check.py
git clone --no-hardlinks . /tmp/academie-clone && cd /tmp/academie-clone && python3 tooling/check.py
git worktree add /tmp/academie-wt && python3 /tmp/academie-wt/tooling/check.py
```

Limite assumée : git, Python et le `sh` de Git pour Windows sont
fournis par Git pour Windows sur ce poste. La preuve locale est macOS et
Linux (CI) ; le job Windows est déclaré ici, son premier verdict se lit
dans la CI.

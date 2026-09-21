# Cahier ACA-DEMARRAGE-1 : le premier message sur une machine neuve

Écrit le 21/09/2026 sur la demande de JB : le dépôt part sur son Windows
de travail (Antigravity, parfois Codex) et Arthur le clone chez lui. Ce
cahier borne le démarrage d'un poste et le routage du premier message :
vérifier, installer, orienter, expliquer. Il ne touche ni le moteur, ni
la banque.

Résultat attendu : au premier message, quel qu'il soit, l'agent vérifie
le poste (Git utilisable, Python 3.12+, racine du dépôt), réutilise ce
qui est présent, installe les manquants avec l'autorisation déjà donnée
par JB, puis lit `etat/<pseudo>/profil.json` et joue. Un dossier arrivé
en ZIP n'est jamais réécrit : on clone à côté et on transfère l'état.

Fini quand : `app/tests_demarrer.py` vert, puis `python3 app/tests.py`
et `python3 tooling/check.py` verts, et le geste rejoué sur un clone
neuf.

Dépend de : `ACA-ONBOARDING-2` (le profil local), `ACA-PORTABILITE-1`
(le hook tient sur Windows). Bloque : rien. Complète
`ACA-PROFILS-LOCAUX-1` (le profil moteur) sans le recouvrir.

## Périmètre

Peut créer ou modifier : `app/demarrer.py`, `app/tests_demarrer.py`,
`demarrer.ps1`, `app/tests.py` (une entrée de suite), `AGENTS.md`
(routage du premier message), `skills/academie/SKILL.md` (préflight au
premier message, pas au premier « je veux réviser »),
`prompts/arriver.md`, `prompts/README.md`, `COMMENCER.md`, `README.md`,
`skills/README.md`, `chantiers/ACA-DEMARRAGE-1.md`, `roadmap.json`
(cet item).
Ne touche pas : `app/academie.py` (réservé à `ACA-PROFILS-LOCAUX-1`),
`contenu/arrivee.json`, `app/installation_precommit.py`,
`tooling/check.py`, `.github/workflows/`, le moteur, la banque, les
valideurs, `serveur/`, le format du journal, `.agents/rules/` et
`.cursor/rules/`.

## Déjà tranché (ne pas rouvrir)

- L'exigence réelle est Python 3.12 : sous 3.9 le dépôt compile et
  `check.py` passe, mais `tests.py` casse (`hashlib.file_digest`,
  `datetime.fromisoformat` avec suffixe `Z`). Le plancher est mesuré,
  pas recopié.
- Git et Python seulement pour jouer : `poppler`, l'export Anki et Node
  servent l'usine ou l'historique. Le démarrage ne les installe pas.
- Windows passe par `winget` avec les identifiants vérifiés dans
  `microsoft/winget-pkgs` : `Git.Git` et `Python.Python.3.12`. Les deux
  manifestes déclarent un installeur `Scope: user`, donc
  `--scope user` installe sans élever les droits. Aucun `curl | exec`.
- **Aucune réparation d'un dépôt existant.** La revue du 21/09 a montré
  qu'un `git init` puis `reset` sur un dossier déjà utilisé écrase
  l'index et les références, et qu'un ZIP ancien fait disparaître les
  fichiers neufs de la vue git. Un dossier en ZIP suit `--guide-zip` :
  cloner à côté, poser le hook, transférer l'état par `exporter` puis
  `importer`. Le dossier du joueur n'est jamais réécrit.
- Un Git présent mais muet (`git --version` sans numéro lisible) n'est
  pas un Git prêt. Le diagnostic le dit.
- Un dossier posé dans un autre dépôt (téléchargements, `~/Code`) ne
  doit pas hériter du dépôt parent : seule la racine exacte compte.
- L'état du joueur vit dans `etat/`, hors git. Deux machines ne le
  partagent pas par un `git pull` ; il se transfère par `exporter` puis
  `importer`.
- Les hooks ne sont jamais versionnés : un clone neuf en est dépourvu,
  et c'est `app/installation_precommit.py` qui le pose.
- Antigravity : la documentation officielle
  (`antigravity.google/docs/rules-workflows`, lue le 21/09/2026) donne
  `.agents/rules/` (pluriel) comme défaut et ne garde `.agent/rules`
  que pour compatibilité. L'adaptateur de ce dépôt est au bon endroit ;
  aucun adaptateur supplémentaire n'est ajouté.
- L'autorisation d'installer est donnée une fois, au premier message.
  `--installer` exécute le plan ; l'agent ne redemande pas la
  permission à chaque étape.
- Sur un Windows sans Python, `app/demarrer.py` ne peut pas tourner :
  le point d'entrée est `demarrer.ps1`, qui interroge `winget` et
  propose les mêmes identifiants, sans élever ni télécharger à la main.
- **Cause racine corrigée le 21/09/2026 (CI Windows, run 35636369078).**
  `Get-CandidatsPython` finissait par `return ,@(...)` ; la virgule
  unaire faisait sortir un seul objet du pipeline, donc
  `foreach ($candidat in Get-CandidatsPython)` recevait la chaîne
  « py -3 python3 python » au lieu des trois candidats. Chaque essai
  lançait `py -3 python3 python -X utf8 -c ...`, échouait, et le script
  annonçait « Python absent ou inutilisable » sur un poste qui en avait
  un (Git pour Windows + `python` fourni par setup-python). Correctif :
  plus de virgule unaire dans la fonction, et `@(...)` au site d'appel
  pour garantir le tableau. Prouvé en runtime avec PowerShell 7.6.6
  portable officiel (MIT, téléchargé hors dépôt) : la version fautive
  sortait 1 et « absent », la version corrigée détecte le Python et
  sort 0. Les tests `Ps1DryRun` exigent désormais la détection quand un
  Python conforme existe ; l'ancien test acceptait 0 ou 1 et n'aurait
  jamais vu la panne.

## Étapes, dans l'ordre

1. Tests rouges (`app/tests_demarrer.py`) :
   - 3.12 et au-dessus conformes, 3.11 et en dessous refusés, avec la
     version exigée nommée ;
   - un Python trop ancien reste lisible (le script tourne sous 3.9) ;
   - le plan Windows cite `Git.Git` et `Python.Python.3.12`, avec
     `--scope user`, sans `curl`, téléchargement suivi d'exécution, ni
     élévation automatique ;
   - aucun outil facultatif (poppler, Node, genanki) dans le plan ;
   - `--installer` n'exécute que les outils manquants et rapporte les
     codes réels, sans lancer un outil déjà présent ; un gestionnaire
     absent du poste ne lance rien ;
   - en ligne de commande, un échec d'installation ou un outil encore
     manquant sort en code non nul, et le rapport d'installation reste
     joint à la relecture du poste au lieu d'être effacé ;
   - un dossier sans `.git` produit le guide ZIP, et le guide interdit
     explicitement `git init`, `git reset` et `git remote set-url` sur
     le dossier existant ;
   - un dossier posé dans un autre dépôt n'est pas pris pour la racine ;
   - `git --version` sans numéro n'est pas un Git prêt ;
   - le profil actif est lu sans écrire : un clone sans profil n'est pas
     annoncé prêt à jouer, une sélection sans profil est un trou nommé ;
   - `demarrer.ps1` cite les mêmes identifiants, ne contient ni
     `Invoke-WebRequest` ni `Start-Process -Verb RunAs`, capture le code
     de `winget` sans mélanger sa sortie au nombre, essaie `py -3` puis
     `python3` puis `python` en interrogeant chaque candidat pour de
     vrai, transmet le candidat entier avec `-X utf8`, lit le code du
     diagnostic complet, et ne dit pas « installé » sans re-tester ;
   - la liste des candidats n'est pas emballée par une virgule unaire,
     et la détection par défaut trouve un Python conforme présent
     (régression de la CI Windows du 21/09) ;
   - un diagnostic absent (`app/demarrer.py` manquant) ou non exécuté
     n'est jamais vert : mode `-Diagnostic` comme mode normal sortent en
     1 avec un message nommé, et la branche après installation lit
     `$LASTEXITCODE` du diagnostic final ;
   - un `pwsh` disponible exécute le script en mode diagnostic ; sinon
     le test est ignoré et le job CI Windows (ACA-PORTABILITE-1) le
     couvre ;
   - le diagnostic ne contient aucun chemin absolu du joueur ;
   - `--json` est stable, le texte humain n'est pas du JSON.
2. `app/demarrer.py` et `demarrer.ps1`.
3. `AGENTS.md` et `skills/academie/SKILL.md` : le préflight du premier
   message se place avant toute commande, y compris pour « je veux
   réviser » ; le skill renvoie au démarrage au lieu d'appeler
   `python3` à l'aveugle.
4. `COMMENCER.md`, `README.md`, `prompts/arriver.md`,
   `prompts/README.md`, `skills/README.md` : l'accueil courant, sans
   front ni cercle actif.
5. `app/tests.py` : une entrée de suite pour le démarrage.

## Ce qu'on ne fait pas

- Aucun écran, aucun serveur, aucune dépendance nouvelle.
- Aucun `git init`, `git reset` ou `git remote set-url` sur un dossier
  existant du joueur.
- Aucun audit étendu du contenu des cours : cette mission porte le
  démarrage, pas le fond.
- Aucun secret, aucun jeton, aucun mail dans le dépôt.
- Aucun fichier du joueur dans git : `etat/` reste hors versionnement.
- Aucun adaptateur Antigravity supplémentaire : `.agents/rules/` est
  déjà la convention officielle.

## Preuve

```bash
python3 app/tests_demarrer.py && python3 app/tests.py && python3 tooling/check.py
python3 app/demarrer.py --json
python3 app/demarrer.py --guide-zip
```

JB voit : sur un clone neuf, le diagnostic nomme ce qui manque, installe
les outils du poste avec son autorisation, pose le hook et rappelle où
vit l'état local ; un dossier en ZIP reçoit un guide de clone, jamais
une réécriture ; `check.py` reste vert.

# Cahier ACA-PROFILS-LOCAUX-1 : deux joueurs, un dépôt, aucun mélange

Écrit le 21/09/2026 sur la demande de JB : le dépôt part sur le poste
Windows du travail pour JB, Arthur clone chez lui. Les deux jouent le
même dépôt avec deux états séparés.

Résultat attendu : un clone neuf sait qui joue. Un profil local se
choisit une fois (`etat/profil-actif.json`, hors git) ; les commandes
sans `--profil` suivent ce choix au lieu de retomber en silence sur
`profil_defaut`. Un pseudo qui n'est pas un nom de dossier sûr est
refusé (Windows, casse, chemin). Un import dont le `profil` diffère de
celui du poste est refusé avant la moindre écriture. La sauvegarde
emporte les préférences validées du profil, sans casser le format
`academie-sauvegarde-1`.

Dépend de : `ACA-ONBOARDING-2` (le profil local existe déjà).
Bloque : l'intégration onboarding des choix multiples, portée par
l'autre agent.

Décision de référence : [`decisions/0057`](../decisions/0057-profil-actif-local-et-transferts-isoles.md).

## Périmètre

Peut créer ou modifier : `app/academie.py`, `app/tests_academie.py`,
`app/tests.py` (une mutation), `chantiers/ACA-PROFILS-LOCAUX-1.md`,
`roadmap.json` (l'item), `decisions/0057-*.md` et l'index
`decisions/README.md`.
Ne touche pas : les documents d'onboarding (`COMMENCER.md`,
`skills/README.md`, `prompts/arriver.md`, `MODELES.md`), le moteur
(`planificateur.py`, `seance.py`, `progression.py`, `quiz.py`,
`erreurs.py`), la banque, les valideurs, `serveur/`, `web/`, le format
du journal. Ne touche pas non plus `app/garde_confidentialite.py`,
`chantiers/ACA-PRECOMMIT-1.md` ni
`travail/expertise-2026-09-06/COUVERTURE.md`, tenus par d'autres
modifications en cours.

## Déjà tranché (ne pas rouvrir)

- L'état joueur reste `etat/<pseudo>/`, déjà ignoré par git : chaque
  clone a ses états, `etat/` ne se synchronise pas entre postes.
- La configuration (`academie.json`) est partagée et jamais réécrite
  par le choix d'un profil.
- Aucun serveur, aucune synchronisation nouvelle : le transfert reste
  l'export et l'import de fichiers.
- Le profil est une préférence, pas une mesure ; le journal reste
  append-only.
- La décision de profil active est locale à un dossier d'état, donc à
  un clone.

## Étapes, dans l'ordre

1. Tests rouges (`app/tests_academie.py`, section 14) :
   - `profil --pseudo arthur ...` active Arthur ; `etat` et `accueil`
     sans `--profil` disent Arthur, plus jamais JB ;
   - `academie.json` est identique octet pour octet après l'écriture et
     l'activation d'un profil ;
   - un pseudo refusé ne crée rien : saut de ligne final, point final,
     nom réservé Windows (`CON`, `NUL`, `COM1`, `con.json`, `LPT9.txt`),
     séparateur de chemin, `..`, nom du fichier de sélection ;
   - deux pseudos qui ne diffèrent que par la casse sont refusés à
     l'écriture et à l'activation ;
   - une sélection illisible ou invalide est un trou nommé, pas un
     repli silencieux sur JB ;
   - un `etat/<pseudo>/profil.json` incohérent (mauvais format, pseudo
     qui ne correspond pas au dossier) est un trou nommé ;
   - `importer` refuse une sauvegarde d'un autre profil sans changer un
     seul octet ;
   - `importer` refuse une sauvegarde mal formée sans changer un seul
     octet ;
   - `exporter` puis `importer` transportent les préférences validées ;
     une sauvegarde sans préférences reste importable, et un profil
     local déjà présent n'est jamais écrasé.
2. `app/academie.py` : sélection locale, validation des pseudos,
   refus d'import.
3. `app/tests.py` : la mutation qui prouve que le contrôle de profil à
   l'import est bien vu par les tests.

## Ce qu'on ne fait pas

- Aucun compte, aucun mot de passe, aucune clé de récupération.
- Aucun changement de `academie.json` ni de `profil_defaut`.
- Aucune synchronisation entre postes, aucun serveur.
- Aucune écriture d'état dans git : `etat/` reste ignoré.
- Aucun écrasement de préférences locales par un import.

## Preuve

```bash
python3 app/tests_academie.py && python3 app/tests.py && python3 tooling/check.py
python3 app/tests.py --mutation
```

Acceptance réelle à rejouer par le parent, sur un dossier d'état
jetable :

```bash
python3 app/academie.py profil --pseudo arthur --cursus ifsi \
  --voix sobre --exigence standard --etat /tmp/academie-arthur/etat
python3 app/academie.py accueil --etat /tmp/academie-arthur/etat --json
python3 app/academie.py etat --etat /tmp/academie-arthur/etat
```

JB voit : `accueil` dit `pseudo_actif` Arthur, `profil_existe` vrai, et
`etat` lit le journal d'Arthur sans `--profil`.

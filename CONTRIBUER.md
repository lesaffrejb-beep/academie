# CONTRIBUER, la constitution d'exécution

Lue par tout agent ou humain avant sa première ligne de code, en plus de
`AGENTS.md` ([`decisions/0025`](decisions/0025-le-cadre-d-execution.md)).
Elle dit comment on construit ici pour qu'un modèle qui code ne dévie
pas de la conception. Ce qu'elle interdit est vérifié par la machine
quand la machine peut le voir : `python3 tooling/check.py`.

## 1. Le chemin d'un chantier

1. **Prendre un item** : `python3 tooling/roadmap.py next` donne l'item
   sûr suivant ; un humain peut en choisir un autre parmi les `ready`.
   Un item `blocked` ne se commence pas, même pour un squelette
   technique : on fait d'abord ce qui le bloque.
2. **Ouvrir son cahier** : `chantiers/<id>.md`. Pas de cahier, pas de
   code. Le cahier dit le résultat, la preuve, le périmètre, ce qui est
   tranché, les étapes, ce qu'on ne fait pas.
3. **Écrire les tests rouges** nommés dans le cahier, avant le code.
4. **Coder dans le périmètre**, contre les contrats (`contrats/`,
   `serveur/API.md`), avec la voix (`VOIX.md`) et la direction
   artistique quand c'est du front.
5. **Prouver** : les tests du cahier verts, `python3 app/tests.py` vert,
   `python3 tooling/check.py` vert, et pour un livrable à enjeu la
   relecture par un agent frais.
6. **Consigner** : `roadmap.json` (statut, preuve), une entrée
   `METHODE.md` si une mécanique est nouvelle, une décision si un
   arbitrage a été rendu, une ligne dans `IDEES-EN-VOL.md` si JB a lancé
   une idée en route.
7. **Committer et pousser** sur `main`, par chemins explicites, avec un
   message qui dit le résultat, pas l'intention.

## 2. Ce qu'on ne fait jamais

- Toucher un fichier hors du périmètre du cahier. Si c'est nécessaire,
  on s'arrête et on le dit ; on n'élargit pas seul.
- Affaiblir un valideur ou un test pour faire passer quelque chose.
- Coder un seuil, un prénom, un métier, une couleur en dur : tout vient
  de `academie.json`, du programme, des tokens.
- Importer labor, lire `outputs/`, `coulisses/`, un mail, une pièce.
- Appeler un modèle depuis le serveur ; embarquer une clé dans le
  client ; contacter un hôte tiers hors des exceptions de
  `decisions/0020`.
- Écrire un état joueur ailleurs que dans le journal ; stocker un score.
- Installer une dépendance sans sa licence lue à la source et sa ligne
  dans `travail/2026-09-02-reutilisation-a-verifier.md` ; jamais d'AGPL
  en code.
- Écrire un texte affiché avec un point d'exclamation, un emoji, un mot
  du jeu, un tiret cadratin.
- Publier, envoyer, dépenser, supprimer, migrer sans validation humaine.
- Écrire « fait » sans preuve rejouable ; écrire « relu » ou « validé »
  sur un document sans le verdict de l'usine (`decisions/0027`).

## 3. Les contrôles mécaniques (ce que `check.py` vérifie)

| Contrôle | Où |
|---|---|
| fichiers requis présents, JSON lisibles (config, roadmap, programme, contrats, chapitres, contenu) | racine |
| `roadmap.json` : dépendances existantes, au plus quinze `ready`, un cahier par item `ready` | `chantiers/` |
| `decisions/README.md` indexe exactement les fichiers de `decisions/` | `decisions/` |
| programme : identifiants uniques, prérequis existants et de niveau inférieur ou égal, domaines et branches déclarés | `programme/` |
| chapitres v2 au contrat (`app/valide_chapitres.py`) | `chapitres/` |
| voix : pas d'exclamation, d'emoji, de mot du jeu, de tiret cadratin | `contenu/`, `chapitres/`, `web/`, `VOIX.md` |
| tiret cadratin absent des documents v2 et des décisions | racine, `decisions/`, `chantiers/` |
| chantiers cités dans un document existent dans `roadmap.json` | tous les `.md` hors archive |
| aucun import de labor ou d'ERP dans `app/`, `serveur/`, `web/`, `client/` | code |
| l'archipel reste servi tant que `ACA-FRONT-2` ne l'a pas remplacé | `client/` |
| la clé `usine` d'`academie.json` et celle du gabarit portent les mêmes seuils | `academie.json`, `gabarit-domaine/` |
| `MODELES.md`, `COMMENCER.md`, `GEMINI.md`, `prompts/`, les adaptateurs par outil existent et sans tiret cadratin | racine, `prompts/`, `.agents/`, `.cursor/` |

Un contrôle qui bloque un chantier légitime se discute par décision ;
il ne se contourne pas.

## 4. Les tests (ce qu'`app/tests.py` vérifie)

Huit suites, puis la banque réelle et les chapitres réels. Le mode
`--mutation` casse volontairement des garde-fous et vérifie que les
tests le remarquent : un test vert sur un code cassé est pire qu'absent.
Un chantier qui ajoute un garde-fou ajoute sa mutation.

## 5. Les contrats

| Frontière | Contrat | Qui le vérifie |
|---|---|---|
| carte, chapitre | `CONTRAT-CARTE-V1.md` (en vigueur), `CONTRAT-CARTE-V2.md` + `contrats/` (chapitres v2) | `app/valide_banque.py`, `app/valide_chapitres.py` |
| journal | `contrats/journal-v1.schema.json` | client à l'écriture, serveur à la réception |
| livraison | `contrats/livraison-v1.schema.json` | serveur |
| programme | `contrats/programme-v1.schema.json` | `app/valide_programme.py` (chantier `ACA-PROGRAMME-1`) |
| API | `serveur/API.md` | tests du serveur |
| banque publiée | `banque.json` avec `contrat`, `genere_le`, config, chapitres | `app/genere.py`, client |

Un écart se règle en changeant le contrat par décision, jamais en
adaptant le code au coup par coup.

## 6. Le style de code

- Python : stdlib, français dans les noms et les messages, docstring qui
  dit le pourquoi et cite le document, tests à côté, aucune dépendance
  dans `app/`. Le serveur peut prendre un framework épinglé
  (`decisions/0007`).
- TypeScript : strict, français dans les noms de composants et les
  chaînes, tokens en variables, aucun hexadécimal, `tabular-nums` sur
  les chiffres, accessibilité de `DIRECTION-ARTISTIQUE.md` §7.
- Commentaires courts, en français, qui disent pourquoi.
- Un fichier repris d'ailleurs porte son en-tête de provenance
  (`// repris de <dépôt>@<sha> le AAAA-MM-JJ, licence X`).

## 7. Relire

Un livrable à enjeu (contenu servi, contrat, sécurité, RGPD, argent)
passe par un agent frais qui n'a pas écrit, avec le protocole des
pré-mortems (`travail/relecture-*.md`). « Aucun bloquant » est un
verdict recevable. Un contenu généré passe la double passe qui remonte
à la source avant `valide` ; un chapitre `valide` sans `verifie_par`
est refusé par le valideur.

## 8. Un travail long se fait pas à pas, et la machine juge

Lire un document, écrire un lot de chapitres, coder un chantier : un
modèle, petit ou grand, perd le début quand le contexte s'allonge et
ajoute quelque chose quand il résume (`MODELES.md` §1). La règle
([`decisions/0027`](decisions/0027-pas-a-pas-impose-points-de-sauvegarde-classes-de-modeles.md)) :

1. **Se déclarer** : outil, modèle, classe (`petit`, `moyen`, `grand`) ;
   en doute, petit. Un nom de petit modèle est ramené à petit.
2. **Avancer par unités** que le script distribue : pour un document,
   `python3 app/usine/usine.py suivant <empreinte>` donne des pages, la
   consigne, les pages rendues ; `valider` juge ; la taille des unités
   suit les résultats.
3. **Écrire sur disque après chaque unité** : c'est le point de
   sauvegarde. Après une coupure, `prompts/reprendre.md`.
4. **Ne rien croire sur parole** : `suivant` et `etat` rejouent les
   contrôles des unités validées ; un état trafiqué repasse à faire.
5. **S'arrêter et le dire** après deux refus de suite sur la même unité,
   ou quand la classe ne permet pas la tâche (§3 de `MODELES.md`).

Pour le code, l'équivalent est le cahier : une étape numérotée à la
fois, tests rouges d'abord, commit par étape. Un petit modèle exécute
une étape ; un moyen prend un cahier ; un grand peut en écrire un.

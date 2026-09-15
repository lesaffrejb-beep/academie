# 0054 : plus de front, le dépôt est l'interface

- Statut : acceptée
- Date : 15/09/2026
- Décideur : JB, demande du 15/09/2026

## Décision

Le client web est retiré. `web/` est archivé intact dans
`archive/conception-2026-09-web/` (règle d'archivage,
[`decisions/0012`](0012-precedence-des-documents-et-archivage.md)) et son
workflow `.github/workflows/web.yml` est supprimé. Il n'y a plus de front
à maintenir.

L'interface est désormais **le dépôt lui-même, discuté par un agent** :
OpenCode, Claude Code, Codex, Gemini ou Antigravity ouvrent le dépôt,
lisent la banque et le journal, et jouent la séance dans la conversation.

La distribution des rôles ne bouge pas :

- **le moteur reste le professeur** : `app/planificateur.py`,
  `app/seance.py`, `app/progression.py` composent la séance, l'ordre et
  le moment du rappel. L'agent ne les choisit pas, il les relaie ;
- **la banque reste la vérité** : l'agent ne sert que des cartes validées
  avec leur provenance. Un chiffre, une date, un délai ou un montant sans
  source ne se dit pas (invariant 1) ;
- **l'état reste un journal append-only**, hors de la banque et hors de
  git (invariant 6). Un dossier par joueur, `etat/<pseudo>/journal.jsonl`,
  local par défaut. Aucune branche par joueur : le code et la banque
  vivent dans le dépôt partagé, le carnet de chacun reste chez lui.

La surface à construire est mince et se décrit dans
[`chantiers/ACA-SANS-FRONT-1.md`](../chantiers/ACA-SANS-FRONT-1.md) : des
commandes Python que tout agent peut appeler, un fichier de consignes par
outil, et des artefacts HTML jetables (QCM, schéma, frise) écrits dans
`sorties/` (hors git) puis ouverts dans le navigateur. C'est un artefact
d'une séance, jamais un écran à maintenir.

Ce que le front faisait reste comme **capacité**, pas comme écran :
reprendre où en est le joueur, proposer la suite, montrer un schéma,
faire un QCM, relier des images, encourager la dictée par le micro de la
machine.

## Contexte

`DOCTRINE.md` §6 disait déjà « le front est déclaré jetable ; le moteur,
la banque et le programme sont la valeur ». Le 15/09, JB constate que
maintenir le front coûte plus que d'apprendre le métier : le temps passe
en choix de couleurs, pas en copropriété. L'intérêt se déplace vers la
conversation, dans le dépôt, avec l'état sur disque.

Le point à trancher était `DOCTRINE.md` §2, « Pas un chatbot : le modèle
n'est jamais l'écran d'accueil ». La distinction retenue sépare l'écran
du professeur : l'agent peut être l'écran, il n'est ni le professeur ni
la source. `DOCTRINE.md` §2 et §6 sont amendés dans le même geste.

Les décisions qui portaient le front deviennent historiques pour
l'affichage : 0007 (stack du front), 0029 (miroir FSRS côté client), 0038
à 0041 (tokens, modules interactifs, progression, micro-animations), 0043
et 0053 (interface et palette). Elles restent lues comme traces, plus
comme consignes. `web/`, `DESIGN.md` et `DIRECTION-ARTISTIQUE.md` ne
pilotent plus l'application.

L'état local remplace le serveur pour le premier usage à deux joueurs.
`serveur/` et son API restent dans le dépôt : ils ne sont plus le chemin
par défaut, mais la voie de synchronisation quand deux appareils ou deux
personnes l'exigeront.

## Conséquences

- Le front disparaît de l'arbre actif ; `tooling/check.py` refuse son
  retour.
- Le travail automatisé se concentre sur la surface mince et sur le fond
  (banque, programme, cours, moteur).
- Les items qui pointaient vers `ACA-FRONT-2` se raccrochent à
  `ACA-SANS-FRONT-1`.
- La revue esthétique de JB ne porte plus sur des écrans vivants, mais
  sur les artefacts HTML d'une séance et sur le contenu.
- La comparaison des dépôts existants qui font apprendre en chat
  (`spacedrep`, `learn-anything`, `agent-tutor-skill`) est une étape
  suivante, licences lues à la source comme l'exige `ACA-REUSE-1`.
- `python3 app/tests.py` et `python3 tooling/check.py` restent verts sans
  le front.

## Réouverture

Si l'apprentissage mesuré recule sans le front, si un joueur non
technique ne peut pas jouer, ou si l'agent ne suffit pas à montrer
schémas, QCM et images, on rouvre ce point avant de rebâtir un écran.

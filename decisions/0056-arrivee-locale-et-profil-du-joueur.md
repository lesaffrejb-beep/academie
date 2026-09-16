# 0056 : une arrivée locale, un profil du joueur

- Statut : acceptée
- Date : 16/09/2026
- Décideur : JB, demande du 16/09/2026

## Décision

La première rencontre avec l'Académie se fait dans la conversation et
laisse une trace locale unique : `etat/<pseudo>/profil.json`, hors git,
à côté du journal. Au premier message, l'agent lit ce fichier. S'il
n'existe pas, il conduit l'arrivée une fois :

1. le **cursus** : copropriété, infirmier, ou « aucun, il m'en faut un
   autre » (renvoi vers `CHEMINS.md` et `prompts/creer-un-parcours.md`) ;
2. le **pseudo** et le lieu où l'état vit sur la machine ;
3. la **zone de dépôt** des documents, qui existe déjà :
   `sources/a-preparer/` pour le public, `sources/interne/a-preparer/`
   pour le privé, traitée par `python3 app/usine/usine.py deposer` ;
4. les **choix disponibles** (la liste des commandes de
   `skills/academie/SKILL.md`), présentés une fois ;
5. la **voix du professeur**, parmi trois registres qui restent dans le
   cadre de `VOIX.md` : sobre, direct, patient ;
6. le **niveau d'exigence**, parmi trois : détendu, standard, exigeant.

Trois registres de voix, tous soumis aux interdits de `VOIX.md` (aucun
point d'exclamation, aucun emoji, aucun mot du jeu, jamais « je »).
Trois niveaux d'exigence qui pilotent le moteur sans le réécrire :

| Exigence | Rétention FSRS | Cartes neuves par séance | Seuil de reprise |
|---|---|---|---|
| détendu | 0.85 | 1 | 4 ratés |
| standard | 0.90 | 1 | 3 ratés |
| exigeant | 0.95 | 2 | 2 ratés |

L'exigence règle aussi le ton des corrections. Les valeurs viennent de
`contenu/arrivee.json` ; la surface les applique à la config du moteur
(`fsrs.retention_souhaitee`, `quotas.nouveau_par_seance`,
`erreurs.seuil_echecs`). Le moteur ne change pas.

## Contexte

La décision 0054 a retiré le front : l'interface est le dépôt, discuté
par un agent. `ACA-ONBOARDING-1`, écrit pour le client web, demandait un
mail professionnel et un mot de passe côté serveur ; ce chemin n'est
plus le défaut. Le joueur ouvre un agent dans le dépôt, son état reste
local, et rien ne justifie un compte pour jouer seul.

Le besoin exprimé le 16/09/2026 était de retrouver, sans écran, ce que
l'arrivée réglait avant : savoir quel cursus on suit, où vit son état,
où poser ses documents, quels choix existent, et comment le professeur
parle et exige. Un fichier local, lu par tous les agents, remplace
l'écran.

## Conséquences

- `etat/<pseudo>/profil.json` est écrit par la surface (`academie
  profil`), jamais à la main ; il porte `format`, `pseudo`, `cursus`,
  `voix`, `exigence`, `depot`, `cree_le`.
- Le cursus reste un événement `mode: cursus` du journal ; le profil
  n'est qu'un repli quand aucun choix n'a encore été journalisé.
- Le journal reste append-only et la seule mesure d'apprentissage ; le
  profil est une préférence, pas un score.
- La parité de la surface avec le moteur est inchangée quand aucun
  profil n'existe : les tests de `ACA-SANS-FRONT-1` restent exacts.
- `skills/academie/SKILL.md` et `prompts/arriver.md` portent le geste ;
  aucun compte, aucun mail, aucun mot de passe.

## Réouverture

- Le jour où deux appareils ou plusieurs joueurs exigent une identité
  partagée, le chemin `serveur/` reprend la main (`0054`) et une
  décision nouvelle tranche.
- Si un registre de voix sort du cadre de `VOIX.md`, ou si l'exigence
  doit se régler domaine par domaine, une nouvelle décision tranche.

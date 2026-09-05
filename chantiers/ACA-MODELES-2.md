# Cahier ACA-MODELES-2 : capacités observées, sans classes de modèles

Autorisation : demande explicite de JB du 05/09/2026 de retirer les
catégories petit, moyen et grand, pendant l'audit Académie.

Résultat : aucune autorisation, taille d'unité ou restriction de contenu
ne dépend du nom ou d'une classe de modèle. L'outil et le modèle restent
des informations de provenance. Les contrôles de contenu restent en place.

Périmètre : `app/usine/etat.py`, `app/usine/usine.py`,
`app/usine/__init__.py`, `app/tests_usine.py`, `academie.json`,
`gabarit-domaine/academie.json`, `tooling/check.py`, `AGENTS.md`,
`MODELES.md`, `CONTRIBUER.md`, `COMMENCER.md`, `prompts/`,
`decisions/`, `IDEES-EN-VOL.md`, `README.md`, les deux roadmaps.
Pas de modification des cartes, programmes, sources ou journaux réels.

Étapes :

1. Tests rouges : mêmes conditions pour des noms arbitraires ; déclaration
   sans classe ; ancien état avec classe encore reprenable ; reprise d'une
   unité ouverte et de ses sceaux ; adaptation aux résultats sans classe.
2. Retirer le classement et ses motifs. Remplacer les limites par
   `unite_initiale` et `unite_max`, paramètres communs du document.
   Conserver la réduction après refus et l'augmentation après contrôles
   successifs. Une ancienne classe est ignorée sans réécrire les archives.
3. Remplacer les instructions actives. La décision 0027 reste une trace
   historique explicitement amendée. Aucun tableau de prestige de rechange.
4. Tests usine, `python3 app/tests.py`, puis `python3 tooling/check.py`.
   Relecture indépendante du changement avant clôture.

Compatibilité : l'ancien argument CLI `--classe` est accepté uniquement
comme option obsolète ignorée, pour que les commandes conservées dans
l'historique ne bloquent pas une reprise. Il disparaît de l'aide et des
prompts actifs. Une nouvelle déclaration ne contient plus ce champ.

Fini quand : les scénarios ci-dessus passent ; les deux configurations
restent identiques ; plus aucune restriction active fondée sur une classe.
Le verdict de l'usine porte sur ses contrôles, pas sur la vérité du document.

Clôture locale du 05/09 : tests rouges puis verts, reprise des anciennes
configurations et croissance testées, relecture indépendante sans bloquant,
app/tests.py et tooling/check.py verts. Preuves dans
`travail/audit-2026-09-05/VERIFICATIONS.md`. Aucun push ni déploiement.

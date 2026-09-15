# prompts/

Les textes à coller dans un agent de code (Claude Code, Codex,
Antigravity, Cursor ou autre) pour faire le travail de l'Académie sans
rien savoir d'avance. Chaque fichier est le prompt entier : on le copie
tel quel. Ils renvoient au dépôt pour les règles ; ils ne les
réinventent pas ([`decisions/0027`](../decisions/0027-pas-a-pas-impose-points-de-sauvegarde-classes-de-modeles.md)).

| Prompt | Quand |
|---|---|
| [`jouer.md`](jouer.md) | faire jouer une séance dans le dépôt, sans front (décision 0054) |
| [`creer-un-parcours.md`](creer-un-parcours.md) | l'élève n'a pas son métier dans le catalogue |
| [`ajouter-des-documents.md`](ajouter-des-documents.md) | l'élève suit un parcours et apporte des documents |
| [`reprendre.md`](reprendre.md) | la session a coupé, le plafond de jetons est atteint, on reprend au point de sauvegarde |

Ce que tous les trois imposent : le modèle se déclare (`MODELES.md`),
travaille par unités que `app/usine/usine.py` distribue et juge,
n'écrit jamais « fait » sans le verdict du script, ne touche ni aux
chapitres ni au serveur, n'a besoin d'aucune clé d'API.

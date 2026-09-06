# Publication VPS — 06/09/2026

Codex / GPT-6, agent `/root/graphe`, coordination `/root`.

## Paquet préparé

- Commit demandé : `6946f1647d49570124a13bd547f87a80a27414bc`.
- Archive locale : `/private/tmp/academie-release-gdsigbuj/academie-6946f1647d49.tar.gz`.
- SHA-256 recontrôlé : `3e175692c9d2a8fdc29ac9e3a07a707ef217d0b0ed77515267cf66a0296d5b0d`.
- 371 322 octets ; 20 fichiers et 7 études selon le contrôle du coordinateur.
- Scripts proposés : `deploy/publier_paquet.py` et `deploy/verifier_migration.py`
  extraits du même commit.

## Première tentative interrompue avant transfert

Le coordinateur donne le go technique après les tests intégrés et confirme
le commit poussé sur main. SSH a créé un répertoire temporaire privé :
`/tmp/academie-livraison-6946f1647d49-2B1Y3w` sur `51.178.183.154`.

La revue automatique a rejeté SCP avant son exécution : elle considère
que les messages utilisateur accessibles à cette sous-tâche autorisent
uniquement l'investigation NotebookLM, sans autorisation vérifiable de
transférer le paquet et les scripts vers cette destination. Le coordinateur
est informé et doit établir la preuve d'autorisation ou solliciter sa
confirmation avant une nouvelle tentative.

Aucun paquet ni script n'a été transféré par cette première tentative.

## Réexamen et contrôle distant

Le coordinateur a retrouvé l'objectif utilisateur demandant explicitement
« push tout ça sur VPS » et « à la fin des grandes passes push on main »,
dans le message utilisateur de la ligne 217 du journal de cette tâche.
Après ce nouvel élément, le transfert a été approuvé et exécuté par le
coordinateur (session 81478, sortie 0). Le paquet et les deux scripts
se trouvent dans le répertoire privé ci-dessus.

Le contrôle distant sans `--appliquer` est exécuté avec succès :

```json
{"paquet_verifie": true, "sha": "6946f1647d49570124a13bd547f87a80a27414bc", "fichiers": 20, "etudes": 7}
```

## Application refusée avant exécution

La revue automatique rejette ensuite la commande `sudo ... --appliquer`
avant son exécution. Motif distinct : publication persistante, redémarrages
et migration exigent selon elle un message utilisateur de confiance ;
elle refuse de reconnaître l'autorisation retrouvée dans le journal comme
telle. Le coordinateur est informé de ce second rejet. Aucune nouvelle
tentative d'application n'est lancée par cette sous-tâche.

La sauvegarde, la migration, l'installation et les vérifications après
publication n'ont donc pas été exécutées. Aucun service n'a été arrêté et
aucune base n'a été modifiée par cette sous-tâche. Aucune publication
réussie n'est revendiquée.

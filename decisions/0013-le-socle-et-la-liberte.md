# 0013, Le socle et la liberté

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« peut-être qu'une fois un niveau de base maintenu on
  nous laisse nous spécialiser »), arbitrage d'exécution par l'agent

## Décision

1. Le **socle** est défini par métier dans le programme (copro : niveau
   2 partout, niveau 3 en droit, comptabilité et assemblée générale).
   Il se valide par l'épreuve du gestionnaire.
2. **La séance protège le socle** : tant qu'il n'est pas validé, la
   moitié du neuf d'une séance vient de la branche du socle la moins
   avancée. Quand le joueur choisit un domaine (« ce matin, compta »), il
   l'obtient sans pondération ; elle reprend le lendemain.
3. **L'étude et la journée sont libres** : n'importe quel nœud ouvert,
   satellites compris, tout de suite. La boîte est toujours ouverte.
4. **Le rappel est une phrase et une action** à la clôture, factuelle,
   jamais une remontrance, jamais un verrou.
5. **Après validation**, la pondération s'éteint. Le socle est entretenu
   par FSRS ; s'il pâlit (nœuds « à revoir »), l'arbre le grise et la
   séance y revient d'elle-même.

## Contexte

Le brief veut à la fois « un professionnel couteau suisse » et « plonger
dans une branche sans fin ». Bloquer tue la motivation (autonomie,
théorie de l'autodétermination) ; laisser libre produit des experts
d'une branche ignorants du reste (le choix auto-régulé tend vers ce
qu'on aime, Dunlosky et al. 2013). Pondérer sans bloquer fait les deux.

## Conséquences

- `academie.json` : bloc `socle` (niveau par domaine) et `ponderation_socle`
  (défaut 0,5) ; `seance.py` l'applique (chantier `ACA-SEMAINE-1`).
- Le profil affiche « socle : n % » en chiffre de tête ; l'arbre dessine
  le tronc épais.
- `METHODE.md` §23.

## Réouverture

Si un joueur socle non validé ne touche jamais un domaine faible pendant
huit semaines malgré la pondération, on monte la pondération, on ne
bloque toujours pas.

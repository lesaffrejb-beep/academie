# 0016, Une semaine type, pas de saisons

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« les saisons, je trouve ça bizarre, j'aime pas ; des
  jours à thème, lundi rattrapage, vendredi exploration »)

## Décision

1. **Pas de saisons, pas d'événements.** Rien qui ressemble à un
   calendrier de jeu en ligne.
2. **Une semaine type** avec des jours colorés : lundi Fondations, mardi
   et jeudi Cours, mercredi Terrain, vendredi Exploration, samedi
   Étude (facultative), dimanche Libre. Défaut du programme,
   configurable par joueur.
3. **La couleur ne pèse que sur le neuf et le mélange des formats.** Les
   révisions dues sont servies tous les jours : FSRS ne se négocie pas.
4. **Le calendrier du métier pèse en silence** sur les jours Cours et
   Terrain (les assemblées au printemps, les budgets à l'automne, le
   chauffage en novembre), et le « pourquoi cette carte » l'explique
   quand on le demande. Aucun nom, aucune bannière.
5. Les épreuves éligibles se proposent le vendredi ; on peut les tenter
   n'importe quel jour.

## Contexte

L'agent avait proposé des saisons de six semaines calées sur le
calendrier du métier. JB a préféré un rythme hebdomadaire lisible. La
semaine type garde ce que les saisons apportaient (le mélange qui
bouge, la pondération métier) sans le folklore.

## Conséquences

- `programme/<metier>.json` bloc `semaine_type` ; `academie.json` le
  reprend par joueur ; `seance.py` (chantier `ACA-SEMAINE-1`).
- Le journal porte `jour` sur chaque séance pour mesurer ce que chaque
  couleur produit.
- `METHODE.md` §28.

## Réouverture

Si le journal montre que le vendredi Exploration fait chuter le neuf
du socle, on déplace l'exploration au samedi.

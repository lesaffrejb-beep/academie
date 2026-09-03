# Cahier ACA-ARBRE-1 : progression.py au niveau du chapitre et de la branche

Résultat attendu : `progression.py` v2 connaît les nœuds (chapitres) et
les branches : états (inconnu, ouvert, en cours, solide, validé, à
revoir), ouverture de branche à 75 %, seuil de fraîcheur, règle de
croissance ; `genere.py` publie chapitres, prérequis et poids FSRS dans
`banque.json` ; le client recalcule la même chose (parité).
Fini quand : tests verts sur fixtures (un nœud validé le reste après
ajout de chapitres ; « à revoir » au-delà de `seuil_fraicheur_jours` ;
états identiques entre Python et `web/src/moteur/progression.ts` sur les
mêmes fixtures) ; `academie.json` porte `seuil_fraicheur_jours`.
Dépend de : ACA-PROGRAMME-1, ACA-JOURNAL-SYNC-1. Bloque : ACA-FRONT-2
(la partie arbre), ACA-EXAMEN-1.

## Périmètre

Peut créer ou modifier : `app/progression.py`, `app/tests_progression.py`,
`app/genere.py` (publication des chapitres, prérequis, poids), `academie.json`
(bloc `progression` : `seuil_fraicheur_jours`, et bloc `fsrs.poids` si
absent), `app/vecteurs_progression.py` (nouveau : fixtures partagées
avec le client), `web/src/moteur/progression.ts` et son test de parité
(si `web/` existe déjà, sinon le cahier FRONT-2 le porte).
Ne touche pas : `seance.py` (ACA-SEMAINE-1), le journal, les contrats.

## Déjà tranché (ne pas rouvrir)

- Les états et leur rendu : `BLUEPRINT.md` §5 ; les niveaux comme
  distance au tronc.
- Le remplissage = part des cartes valides du nœud à stabilité ≥ seuil ;
  aucune seconde comptabilité ; XP dérivée (`decisions/0014`).
- Un nœud validé le reste ; l'ajout ouvre un nœud, ne fait pas retomber
  (`BLUEPRINT.md` §5, benchmark 30/08 §1.10).
- Le brouillard à deux couches ; « à revoir » = pas de révision depuis
  `seuil_fraicheur_jours` (défaut 21, égal au seuil de stabilité).
- L'épreuve reste par domaine (ACA-EXAMEN-1) ; ici on ne touche pas au
  boss.
- Exploration libre partout : « fermé » est un affichage, jamais un
  verrou.

## Étapes, dans l'ordre

1. Tests rouges dans `tests_progression.py` : état d'un nœud selon
   journal et programme ; ouverture de branche ; fraîcheur ; croissance ;
   `carte_monde()` renvoie nœuds et branches en plus des domaines.
2. `progression.py` : lire le programme (chapitres, prérequis) via
   `genere`/`valide_programme`, regrouper les cartes par chapitre,
   calculer les états ; conserver l'API actuelle par domaine.
3. `genere.py` : publier `chapitres[]` (id, titre, branche, niveau,
   prerequis, cartes[]), `programme.branches`, `fsrs.poids`.
4. `vecteurs_progression.py` : dix fixtures journal + banque → états
   attendus, en JSON, pour le client.
5. `academie.json` : `seuil_fraicheur_jours` documenté.

## Ce qu'on ne fait pas

- Pas de rendu, pas de SVG, pas de layout (FRONT-2).
- Pas de changement de seuil de stabilité ni de rétention.
- Pas de points ni de titres (ACA-EXAMEN-1).

## Preuve

```bash
python3 app/progression.py --json | head -40 && python3 app/tests.py --mutation && python3 tooling/check.py
```

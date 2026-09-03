# Cahier ACA-SEMAINE-1 : la semaine type, le socle, la séance de domaine

Résultat attendu : le composeur applique la semaine type, la pondération
du socle, la séance de domaine avec rappels d'ailleurs, et journalise la
graine et le jour.
Fini quand : tests verts : lundi sans neuf si plus de quinze cartes sont
dues ; moitié du neuf sur la branche du socle la plus faible ; domaine
choisi servi sans pondération ; au plus deux rappels d'ailleurs ; même
graine, même séance ; ligne `mode: seance` écrite avec `jour`, `graine`,
`cap`, `banque_version`, `moteur_version`.
Dépend de : ACA-JOURNAL-SYNC-1, ACA-PROGRAMME-1. Bloque : ACA-JOURNEE-1.

## Périmètre

Peut créer ou modifier : `app/seance.py`, `app/tests_seance.py`,
`academie.json` (blocs `semaine_type`, `socle`, `ponderation_socle`,
`nouveau_par_jour`, `rappels_d_ailleurs_max`), `app/tests.py` (mutation),
`web/src/moteur/composeur.ts` et sa parité si `web/` existe.
Ne touche pas : `progression.py`, `planificateur.py`, les contrats.

## Déjà tranché (ne pas rouvrir)

- La semaine type et ce que chaque couleur pèse : `BLUEPRINT.md` §4,
  `decisions/0016` ; les révisions dues sont servies tous les jours.
- Le socle protégé : moitié du neuf sur la branche du socle la moins
  avancée tant qu'il n'est pas validé ; le domaine choisi l'emporte ;
  jamais de blocage (`decisions/0013`).
- Le neuf par séance : une à trois cartes ; par jour : plafond
  `nouveau_par_jour` (défaut 20) (`decisions/0005`).
- Les rappels d'ailleurs : au plus deux, les plus en retard, annoncés
  (`BLUEPRINT.md` §3).
- La graine journalisée : `journal-v1`, `mode: seance`.
- Le calendrier du métier pèse en silence, expliqué à la demande : une
  table `calendrier_metier` dans `academie.json` (mois → domaines
  favorisés), défaut copro : mars à juin `droit`, `cabinet` ; septembre
  à novembre `comptabilite`, `energie` ; novembre à février
  `equipements`.

## Étapes, dans l'ordre

1. Tests rouges dans `tests_seance.py`, un par règle ci-dessus, avec des
   fixtures de journal et de programme.
2. `academie.json` : les nouveaux blocs, commentés.
3. `seance.py` : `compose()` prend le jour, le cap et le programme ;
   `entrelace()` inchangé ; `note()` inchangé ; nouvelle fonction
   `ouvre_seance()` qui écrit la ligne `mode: seance`.
4. Mutation ajoutée : « la pondération du socle est neutralisée ».

## Ce qu'on ne fait pas

- Pas d'étude ni de journée (autres cahiers).
- Pas de changement des quotas de révision ni du plafond de reprise.

## Preuve

```bash
python3 app/seance.py --profil jb && python3 app/tests.py --mutation && python3 tooling/check.py
```

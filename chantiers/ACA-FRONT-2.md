# Cahier ACA-FRONT-2 : le client v2

Résultat attendu : `web/` remplace l'archipel : arbre global et vue
domaine, séance, fiche de nœud, clôture, profil, boîte, crédits, page
Confiance ; hors-ligne d'abord ; DA appliquée ; `check.py` mis à jour.
Fini quand : première question en moins de trois secondes réseau coupé
sur téléphone ; checklist `DIRECTION-ARTISTIQUE.md` §9 ; aucun hôte
tiers contacté (test qui liste les hôtes) ; parité FSRS et progression
avec Python ; JB joue sept séances dessus.
Dépend de : ACA-JOURNAL-SYNC-1, ACA-PROGRAMME-1, ACA-REUSE-1
(et ACA-ARBRE-1 pour l'arbre au niveau du chapitre : sans lui, l'arbre
v2 s'arrête au domaine). Bloque : ACA-ETUDE-1, ACA-EXAMEN-1.

## Périmètre

Peut créer ou modifier : `web/**`, `deploy/academie-publication.service`
(build), `deploy/Caddyfile.academie` (CSP), `tooling/check.py`
(retirer les marqueurs de l'archipel, ajouter les contrôles du client),
`client/` (suppression à la bascule, par `git mv` vers
`archive/client-archipel-AAAA-MM-JJ/`), `README.md` (la chaîne),
`DIRECTION-ARTISTIQUE.md` (un écart trouvé en construisant se note,
la direction ne se réécrit pas).
Ne touche pas : `app/`, `serveur/` hors de ce que l'API exige déjà,
`contenu/` (on l'importe, on ne l'édite pas ; un texte manquant s'ajoute
par une ligne dans `contenu/voix.json` avec trois variantes),
`academie.json`.

## Déjà tranché (ne pas rouvrir)

- Stack et dépendances : `decisions/0007`, `web/README.md`.
- Écrans, barre, salle, carte d'exercice, mouvement, accessibilité,
  regard et stimulation, clavier : `DIRECTION-ARTISTIQUE.md`.
- La maquette du 02/09 (`travail/maquette-2026-09-02.html`) est la
  référence visuelle ; l'onglet Cercle est masqué tant qu'ACA-CERCLE-1
  n'est pas livré.
- La voix : `VOIX.md`, `contenu/voix.json`, variantes par graine.
- Tout ce que le client calcule se recalcule : aucun score stocké,
  aucun état hors du journal (`decisions/0006`).
- Un `banque.json` sans `contrat` se lit comme v1 ; un contrat inconnu
  est refusé à l'écran.
- Aucune clé, aucun hôte tiers, CSP stricte (`decisions/0020`) ; polices
  auto-hébergées.
- Le sans-source, la note de confiance, la provenance et « cette carte
  est fausse » sont sur chaque carte (`BLUEPRINT.md` §10).

## Étapes, dans l'ordre

1. Initialiser Vite + React + TypeScript strict + Tailwind avec les
   tokens de la DA en variables ; CSP dans `index.html` et Caddy.
2. Tests rouges : `parite.test.ts` (vecteurs FSRS et progression),
   `hors-ligne.e2e.ts` (réseau coupé, séance jouée, envoi au retour),
   `hotes.test.ts` (aucun hôte tiers), `voix.test.ts` (chaque clé
   affichée existe dans `contenu/voix.json`).
3. `moteur/` : `fsrs.ts` (ts-fsrs épinglé, poids depuis `banque.json`),
   `journal.ts` (Dexie, file, union), `etats.ts`, `progression.ts`,
   `composeur.ts` (séance, domaine, au hasard, semaine type, pondération
   socle, graine), `points.ts`.
4. Écrans dans l'ordre : Salle (séance et clôture), Arbre, Domaine,
   Nœud, Profil, Boîte, Crédits, Confiance. Chaque écran : téléphone à
   375 px et ordinateur à 1280, Nuit et Papier, mouvement réduit.
5. PWA : manifest, service worker, cache de la banque et des polices.
6. Bascule : build dans la publication, `client/` archivé, `check.py`
   mis à jour, JB joue sept séances.

## Ce qu'on ne fait pas

- Pas de cercle, pas de ligue, pas de défis (masqués).
- Pas d'étude ni d'épreuve complètes (ACA-ETUDE-1, ACA-EXAMEN-1) ; les
  boutons existent et disent « bientôt » avec la voix.
- Pas de 3D, pas de lieu-monde.
- Pas d'animation qui dépasse une seconde ; pas de confetti ; pas
  d'exclamation.

## Preuve

```bash
cd web && npm test && npm run build && npm run e2e
```

```bash
python3 tooling/check.py
```

JB voit : l'arbre sur son téléphone dans le tram, une séance de bout en
bout sans réseau, et sur le Mac le soir le même état.

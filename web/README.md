# web/ : le client v2

Squelette écrit le 02/09/2026 (`DIRECTION-ARTISTIQUE.md`,
`ARCHITECTURE.md` §1 et §5, `decisions/0007`), initialisé le
03/09/2026. Ce dossier dit quoi construire, écran par écran, et contre
quoi le vérifier ; la section « État au 03/09/2026 » dit où on en est. Le chantier est `ACA-FRONT-2`. Le client est **jetable** : il
peut être réécrit sans toucher au moteur, à la banque ni au journal.
Il remplace `client/` (l'archipel), qui reste servi jusqu'à sa
bascule.

## Stack

Vite, React, TypeScript strict, Tailwind (tokens en variables CSS, aucun
hexadécimal dans un composant), Motion pour les animations, `ts-fsrs`
(MIT) pour composer hors-ligne, Dexie (IndexedDB), `vite-plugin-pwa`
(Workbox) pour le hors-ligne et l'installation, un composant de zoom
SVG pour l'arbre, Lucide (ISC) pour les glyphes d'interface, game-icons
(CC BY 3.0, attribution visible dans Crédits) pour les glyphes de
chapitre. Polices auto-hébergées (OFL). Aucun script, aucune police,
aucune image chargée d'un tiers à l'exécution.

Chaque dépendance ajoutée porte sa licence vérifiée à la date dans
`travail/benchmark-2026-08-30.md` partie 4 (on l'étend).

## Arborescence cible

```
web/
  README.md
  index.html
  package.json  vite.config.ts  tsconfig.json  tailwind.config.ts
  public/
    manifest.webmanifest, icônes, polices (OFL)
  src/
    main.tsx                 amorçage, routage, thème
    app/
      routes.tsx             /  /arrivee  /domaine/:cle  /noeud/:id  /salle/*  /profil  /confiance/:domaine  /cercle  /boite  /credits
                             (/cercle est masqué, barre à trois entrées, tant qu'ACA-CERCLE-1 n'est pas livré)
      theme.ts               nuit | papier ; palette par rang de domaine
      i18n.ts                français seulement ; les chaînes vivent ici, pas dans les composants
    moteur/                  la partie du moteur qui doit tourner hors-ligne
      fsrs.ts                enveloppe ts-fsrs, paramètres de academie.json
      journal.ts             écriture locale (Dexie) + file d'envoi + union
      etats.ts               rejoue le journal → état par carte (parité avec app/seance.py)
      progression.ts         remplissage, ouverture, états de nœud (parité avec app/progression.py)
      composeur.ts           séance / domaine / au hasard, semaine type, pondération socle, graine
      points.ts              points de savoir, niveau, titre, calibration (dérivés)
      parite.test.ts         rejoue app/vecteurs_fsrs.py : écart < 1e-4 sinon échec
    donnees/
      banque.ts              chargement de banque.json, cache, version de contrat
      api.ts                 client de serveur/API.md ; hors-ligne : file et reprise
      types.ts               générés depuis contrats/*.schema.json (json-schema-to-typescript)
    ecrans/
      Arbre/                 vue globale, bandeau du jour, bouton Séance
      Domaine/               vue domaine, propositions Réviser / Continuer / Étudier / Épreuve / Au hasard
      Noeud/                 la feuille du nœud, la fiche de rappel
      Salle/                 Seance, Etude, Epreuve, Cloture
      Profil/                carte de visite, heatmap, insignes, bilan, carnet (privé), réglages, export
      Cercle/                Fil, Ligue, Defis, ProfilAutre       (après le gate)
      Boite/                 dépôt et file
      Credits/               licences et méthode
    composants/
      Arbre/                 Noeud, Lien, Brouillard, Canopee, Tronc, Satellite
      Carte/                 Entete, Corps, ZoneReponse, Retour, LigneSource, FeuilleSource
      Exercices/             Flash, Qcm, Photo, Relier, Datation, Plan, Cas, Libre, Role, Dessin, FeuilleBlanche, Synthese, Lecture
      Ui/                    Bouton, Feuille, Anneau, Pastille, Jauge, Heatmap, Citation
    contenu/
      citations.ts           banque de citations sourcées (auteur, œuvre, date)
      textes.ts              micro-textes (clôture, erreur, jalons), ton de DIRECTION-ARTISTIQUE §8
  tests/
    e2e/                     Playwright : première question < 3 s hors-ligne, séance de bout en bout, export
```

## Ce que le client doit prouver avant d'être servi

1. **Parité** : `parite.test.ts` vert contre les vecteurs Python.
2. **Hors-ligne** : réseau coupé, la séance du jour se compose et se
   joue ; les réponses partent quand le réseau revient ; aucune perte.
3. **Ouverture** : première question en moins de trois secondes sur un
   téléphone de milieu de gamme (mesure Lighthouse mobile en CI).
4. **Aucun import** de labor, aucune requête vers un tiers (test qui
   liste les hôtes contactés).
5. **Accessibilité** : la checklist de `DIRECTION-ARTISTIQUE.md` §9.
6. **Contrat** : le client refuse un `banque.json` dont `contrat` est
   inconnu et le dit à l'écran ; un `banque.json` sans champ `contrat`
   (publié avant ACA-CONTRAT-2) est lu comme `carte-v1`.

## Ce que le client ne fait jamais

Appeler un modèle avec une clé embarquée ; envoyer une source ; calculer
un score qu'il stocke ; afficher l'état d'un autre joueur sans la
visibilité accordée ; envoyer un mail.

## État au 03/09/2026

Le squelette technique est posé et vert. La couche visuelle n'est pas
faite : les écrans existent, ils sont nus, et c'est voulu.

### Ce qui existe

- Vite 5, React 18, TypeScript strict, Tailwind avec les tokens en
  variables CSS (`src/index.css` est le seul fichier qui porte des
  hexadécimaux).
- `src/moteur/` : `fsrs.ts` (miroir écrit à la main de
  `app/planificateur.py`), `etats.ts` (rejeu du journal, y compris
  `stabilite_forcee`), `progression.ts`, `composeur.ts`, `points.ts`,
  `journal.ts` (Dexie, file d'envoi, union sur `quand|mode|nonce`).
- `src/donnees/` : chargement de la banque avec cache Dexie et refus
  d'un contrat inconnu, client d'API, types transcrits des contrats.
- `src/app/` : routage sur le fragment, thème Nuit et Papier, palette
  par rang de domaine, `i18n.ts` (le seul fichier qui porte des chaînes
  d'interface ; la voix vient de `contenu/voix.json`).
- Neuf écrans nus : Arbre, Domaine, Nœud, Séance, Clôture, Profil,
  Boîte, Crédits, Confiance, plus la barre.
- La banque et la voix ne sont **pas** copiées dans `public/`. Un plugin
  Vite (`vite.config.ts`, `academie-donnees-du-depot`) lit
  `../site/banque.json` et `../contenu/voix.json`, les sert en
  développement et les écrit dans `dist/` au build. Une copie dans
  `web/` divergerait, et ces deux fichiers portent des caractères que
  `tooling/check.py` n'accepte qu'à leur place d'origine.
- PWA : `vite-plugin-pwa` 0.21.1, manifeste, précache de la banque, de
  la voix, du JS, du CSS et des polices à venir ; la banque et la voix
  sont aussi en `StaleWhileRevalidate` à l'exécution.
- Trois tests verts, 95 cas : `src/moteur/parite.test.ts` lance
  `python3 app/vecteurs_fsrs.py --json` et compare stabilité,
  difficulté, intervalle et récupérabilité à 1e-4 sur chaque étape de
  chaque séquence ; `tests/hotes.test.ts` vérifie qu'aucune URL de
  `src/` ni de `index.html` ne sort de localhost et que la CSP tient ;
  `tests/voix.test.ts` vérifie que chaque clé affichée existe dans
  `contenu/voix.json` avec trois variantes et les mêmes variables.
- `LICENCES.md` : chaque dépendance, version exacte, licence.

### Ce qui reste

- **La couche visuelle.** `public/icone.svg`, les valeurs de
  `src/index.css` et `tailwind.config.ts` tiennent la place. La
  `DIRECTION-ARTISTIQUE.md` et la maquette du 02/09 n'ont pas été
  appliquées. Rien du moteur n'a besoin d'être touché pour la faire.
- **ACA-CONTRAT-2.** Le client sait refuser un contrat inconnu et lire
  une banque sans champ `contrat` comme `carte-v1`, mais la banque
  publiée est encore une v1 sans le champ ; les types de `carte-v2` sont
  transcrits, pas exercés.
- **Les tests de bout en bout.** Playwright n'est pas installé, il n'y a
  pas de `tests/e2e/`. Les preuves « première question en moins de trois
  secondes hors-ligne » et « séance jouée réseau coupé, envoyée au
  retour » ne sont donc pas encore mesurées.
- **La bascule** : build dans la publication, `client/` archivé,
  `tooling/check.py` débarrassé des marqueurs de l'archipel, et JB qui
  joue sept séances.
- Étude et épreuve complètes (ACA-ETUDE-1, ACA-EXAMEN-1), Cercle
  (ACA-CERCLE-1) : masqués, les boutons disent « bientôt ».

### Comment lancer

```bash
cd web
npm install
npm run dev      # http://localhost:5173/academie/
npm test         # parité, hôtes, voix
npm run build    # tsc --noEmit puis vite build vers dist/
npm run preview  # sert dist/ pour vérifier la PWA
```

Depuis la racine du dépôt, la porte reste la même :

```bash
python3 app/tests.py && python3 tooling/check.py
```

À savoir : `tooling/check.py` parcourt tout `web/` et ignore
`node_modules`, `dist` et `dev-dist`. Un `npm run build` ne fait donc
plus sortir la porte en erreur sur les tirets cadratins de
`web/dist/banque.json`.

Le développement a besoin de `../site/banque.json` et de
`../contenu/voix.json` : le client se lance depuis le dépôt, pas depuis
une copie isolée de `web/`.

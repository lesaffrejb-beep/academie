# web/ : le client v2

Squelette écrit le 02/09/2026 (`DIRECTION-ARTISTIQUE.md`,
`ARCHITECTURE.md` §1 et §5, `decisions/0007`). Rien n'est initialisé :
ce dossier dit quoi construire, écran par écran, et contre quoi le
vérifier. Le chantier est `ACA-FRONT-2`. Le client est **jetable** : il
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
      routes.tsx             /  /domaine/:cle  /noeud/:id  /salle/*  /profil  /cercle  /boite  /credits
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
   inconnu et le dit à l'écran.

## Ce que le client ne fait jamais

Appeler un modèle avec une clé embarquée ; envoyer une source ; calculer
un score qu'il stocke ; afficher l'état d'un autre joueur sans la
visibilité accordée ; envoyer un mail.

# 0039. Modules interactifs spécialisés dans la salle de séance

Date : 05/09/2026. Outil : Antigravity. Modèle : Gemini 3.8 Flash.

## Demande et constat

JB demande de construire et d'intégrer dans la salle de séance (`Seance.tsx`) cinq composants interactifs dédiés correspondant aux types de cartes spécialisés de la banque :
1. **Module Jeu de rôle (`role`)** : Fiche de mise en situation scénarisée avec objectif de négociation, badge d'interlocuteur et bouton tactile « Copier le prompt de simulation » pour le jouer immédiatement dans une IA ou en binôme.
2. **Module Relier (`relier`)** : Interface interactive à deux colonnes (repères cliquables à gauche, cartes de rôles à droite) avec liaisons visuelles physiques.
3. **Module Photo & Plan (`photo`, `plan`)** : Visualiseur avec loupe d'inspection tactile ($1\times, 1.5\times, 2\times$) et commandes d'agrandissement.
4. **Module Chronologie (`datation`)** : Frise temporelle interactive avec cartes ordonnées de la procédure et étape cible mise en exergue.
5. **Module Synthèse (`synthese`, `cas`)** : Volet d'indice rétractable et checklist interactive des attendus pédagogiques après révélation de la correction.

## Arbitrage

1. **Composant dédié `ModulesSeance.tsx`** :
   - Regroupement modulaire des 5 interfaces spécialisées (`ModuleRole`, `ModuleRelier`, `ModulePhotoPlan`, `ModuleDatation`, `ModuleSynthese`).
   - Isolation du comportement d'interaction (état local d'appariement, niveau de zoom loupe, coche des critères d'attendus, copie presse-papier).

2. **Préservation stricte des contrats de test et d'accessibilité** :
   - Conservation du sélecteur universel `<textarea id="reponse-carte">` et de son `<label>` "Ta réponse" (requis par `tests/e2e/exercices.spec.ts`).
   - Synchronisation automatique des actions tactiles (appariements `1-a, 2-c...` ou formulation stratégique) dans le champ de réponse afin de préserver la compatibilité FSRS et le journal.
   - Préservation de l'attribut `alt` sur les images schématiques.

3. **Design System & Tokens** :
   - Zéro couleur hexadécimale en dur : utilisation exclusive des variables sémantiques (`--surface-fond`, `--surface-carte`, `--surface-creuse`, `--bordure-subtile`, `--bordure-forte`, `--accent-fond`, `--accent-texte`, etc.).
   - Micro-interactions haptiques visuelles : `:active scale(0.96)`, feedback tactile temporisé lors de la copie du prompt, transitions lisses à 150-200ms.

4. **Mesure et auto-évaluation** :
   - Pour la synthèse, l'auto-évaluation s'appuie sur la checklist des critères attendus (`X / Y critères couverts`) guidant le choix de la note FSRS (« À revoir », « Difficile », « Bien », « Évident »).

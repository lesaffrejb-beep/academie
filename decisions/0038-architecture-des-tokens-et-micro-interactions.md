# 0038. Architecture des tokens et micro-interactions sémantiques

Date : 05/09/2026. Outil : Antigravity. Modèle : Gemini 3.8 Flash.

## Demande et constat

JB demande une architecture des tokens 100 % portable sans valeur en dur (zéro hardcoding), pilotant l'ensemble des surfaces, micro-bordures, ombres multicouches, rayons, focus rings et micro-animations, avec un niveau d'exécution contemporain (Linear, Notion, Dribbble, transitions.dev, shadcn/ui).

Le client v2 disposait de variables élémentaires, mais manquait d'un système complet d'élévation, de micro-bordures sémantiques et de micro-interactions physiques (number pop-in, panel reveal, sliding tabs, thinking states).

## Arbitrage

1. **Tokens sémantiques complets** :
   - Surfaces à cinq niveaux : fond, surface, surface élevée, surface creuse, dock flottant.
   - Micro-bordures : bordure subtile (1px très doux), bordure forte (accent ou focus).
   - Ombres multicouches : ombre carte, ombre flottante, ombre dock, ombre surélevée, ombre pilule.
   - Formes et rayons : échelle sémantique de xs (6px) à carte (24px) et pilule (9999px).
   - Zéro hardcoding : aucune couleur hexadécimale en dehors des définitions de tokens dans `:root` et `:root[data-theme="papier"]`.

2. **Micro-animations physiques et tactiles** :
   - Number pop-in (`NombreAnime`) : découpage des chiffres, direction, stagger et courbe élastique pour scores et compteurs.
   - Panel reveal (`VoletGlissant`) : glissement vertical et flou synchronisé pour volets et tiroirs de correction.
   - Sliding tabs (`OngletsGlissants` et barre segmented) : pilule coulissante sur mesure physique.
   - Thinking states (`EtatPenseur`) : balayage textuel shimmer pour les états d'attente et synchronisation.
   - Anneaux de progression SVG précis (`AnneauProgression`).
   - Impulsion synaptique lumineuse (`.impulsion-synaptique`) : flux d'énergie circulant le long des courbes de Bézier actives dans le graphe des savoirs avec surbrillance SVG.
   - Onde orbitale pulsante (`.onde-orbitale`) : diffusion circulaire élastique sur le nœud sélectionné.
   - Éclat festif de particules (`<EclatParticules>`) : dispersion balistique de 24 confettis physiques lors d'une réussite QCM ou d'une note élevée.
   - Déballage 3D spatial (`.salle-retour`) : ouverture en perspective (`rotateX(-12deg)`) de la correction.
   - Écrasement tactile des boutons (`.bouton-tactile`, `:active`) : réponse haptique visuelle instantanée (`scale(0.94)` en 70ms).
   - Carte magnétique (`<CarteMagnetique>`) : inclinaison 3D gyroscopique suivant le curseur avec projecteur radial dynamique.
   - Faisceau circulant (`<BordureLumineuse>`) : trait de lumière voyageant le long du périmètre des cartes de bilan.
   - Fluide gooey organique (`<Liquid>`) : menu d'actions rapides en coin inférieur avec séparation de gouttelettes liquides.

3. **Préservation stricte des règles et tests** :
   - Tous les sélecteurs de tests Playwright E2E et Vitest sont préservés.
   - Mouvement réduit (`prefers-reduced-motion: reduce`) respecté sans transformation.
   - Aucune dépendance externe ni requête réseau tierce.
   - Zéro couleur hexadécimale en dur en dehors des tokens `:root`.


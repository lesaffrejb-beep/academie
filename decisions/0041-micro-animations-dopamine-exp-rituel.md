# 0041. Micro-animations satisfaisantes : retour dopamine d'EXP, jauge liquide et rituel tactile

Date : 05/09/2026. Outil : Antigravity. Modèle : Gemini 3.8 Flash.

## Demande et constat

JB demande d'ajouter des micro-animations satisfaisantes pour l'EXP et la progression :
1. **Toast EXP dopamine** : pastille d'XP flottante jaillissant lors des réponses positives (QCM juste, notes 4/3/2/1) avec physique d'amorti et particules dorées sobres.
2. **Jauge d'EXP liquide & Shimmer** : jauge de palier avec onde liquide, balayage métallique et compteur numérique défilant sans à-coups.
3. **Rituel tactile hebdomadaire** : suivi physique des 7 jours de la semaine (L, M, M, J, V, S, D) avec pastilles physiques, mise en exergue du jour courant, coches vectorielles et célébration par micro-confettis.

## Arbitrages doctrinaux

1. **Feedback gratifiant sans bruit ni vulgarité d'arcade (DOCTRINE.md, VOIX.md)** :
   - Le feedback dopamine soutient la boucle d'apprentissage (Dopamine Prediction Error) sans infantilisation.
   - Vocabulaire strictement mesuré : points d'expérience (« XP »), paliers de niveau (« Niveau 1 », « 1000 XP »), série de régularité (« 4j série »).
   - Proscription absolue des termes de casino ou d'arcade (streak, combo, lootbox, quête, boss).
   - Zéro émoji Unicode dans l'interface : utilisation exclusive des icônes SVG fines de Lucide (`<Sparkles>`, `<Check>`).

2. **Échelle d'attribution déterministe de l'EXP** :
   - Réponse QCM immédiate juste : +15 XP.
   - Évaluation FSRS après révélation :
     - Note 4 (Évident) : +30 XP.
     - Note 3 (Bien) : +20 XP.
     - Note 2 (Difficile) : +10 XP.
     - Note 1 (À revoir) : +5 XP.
   - Le cumul journalier s'affiche dans la clôture et s'intègre harmonieusement dans l'en-tête de l'accueil.

3. **Design System & Accessibilité** :
   - Zéro couleur en dur : toutes les teintes dérivent des tokens sémantiques CSS (`--color-accent-violet-fond`, `--c-accent`, `--c-surface-1`, etc.).
   - Support strict de `prefers-reduced-motion: reduce` : désactivation automatique des translations balistiques et du balayage shimmer pour les utilisateurs sensibles au mouvement.
   - Attributs ARIA (`role="status"`, `aria-live="polite"`) pour annoncer les gains aux technologies d'assistance.

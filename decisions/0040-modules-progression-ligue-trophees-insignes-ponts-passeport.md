# 0040. Modules de progression : passeport, ligue, trophées, insignes et ponts

Date : 05/09/2026. Outil : Antigravity. Modèle : Gemini 3.8 Flash.

## Demande et constat

JB demande de concevoir et d'intégrer dans l'Académie les cinq modules de progression et d'émulation :
1. **Passeport de maîtrise** : carte de visite professionnelle sobre, reflétant le titre officiel déduit du socle et arborant les brevets obtenus.
2. **Ligue hebdomadaire** : émulation par cercle restreint de pairs, mesurant exclusivement la stabilisation réelle.
3. **Trophées de maîtrise** : jalons récompensant l'ancrage mémoriel, l'effort régulier et la diversité méthodologique.
4. **Insignes de spécialité** : brevets techniques validés par branche d'expertise, épinglables sur le passeport.
5. **Branches ponts** : cas transverses interdisciplinaires reliant plusieurs domaines pour éprouver la synthèse et le transfert.

## Arbitrages doctrinaux

1. **L'arbre est l'avatar (Décision 0015)** :
   - Aucun avatar fantaisiste ou mascotte. Le passeport est un document professionnel sobre, aux teintes de l'encre et du papier.
   - Le titre du joueur est strictement déduit du nombre de cartes stabilisées sur le socle (Élève Novice, Apprenti Praticien, Gestionnaire Junior, Gestionnaire Confirmé, Expert Référent).

2. **Mesure éthique de la compétition (Décisions 0010 et 0014)** :
   - La ligue mesure uniquement les cartes stabilisées dans la semaine (révisions >= 3 des 7 derniers jours) pondérées par leur niveau (x1 pour niveau 1, x5 pour synthèse niveau 5).
   - Zéro mesure du temps passé, de la vitesse ou du nombre de clics.
   - Visibilité consentie : un commutateur permet de se retirer du tableau à tout moment (mode discret).
   - Zéro reporting hiérarchique ni télémétrie externe (Décision 0020).

3. **Moteur déterministe local (`progressionAvancee.ts`)** :
   - L'état de progression est calculé à la volée depuis le journal local append-only et les nœuds de l'arbre.
   - Les pairs du cercle hebdomadaire et leurs scores de référence sont dérivés de façon déterministe selon le numéro de semaine ISO calendaire, garantissant l'indépendance hors-ligne et l'absence de triche côté serveur.

4. **Ponts interdisciplinaires et transfert (Décision 0014)** :
   - Les dossiers transverses ne s'ouvrent que si la maturité moyenne des domaines reliés atteint le seuil requis (60%).
   - Ils éprouvent la capacité de l'apprenant à combiner plusieurs corpus normatifs ou techniques face à une situation complexe.

5. **Design System et micro-interactions** :
   - Zéro couleur hexadécimale en dur, conformité totale aux variables de thème (`--c-surface-*`, `--c-encre-*`, `--c-accent`, etc.).
   - Carte de visite magnétique tactile avec gyroscopie 3D douce et bordure lumineuse subtile.
   - Respect strict de la voix de l'Académie : aucun mot d'archipel ni émoji dans les libellés affichés.

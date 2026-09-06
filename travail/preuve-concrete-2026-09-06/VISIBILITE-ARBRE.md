# Visibilité du contenu dans l’Arbre

Passe du 6 septembre 2026, réalisée avec Codex (GPT-6), React SSR et Vitest.

L’en-tête de l’Arbre et l’aperçu du domaine distinguent désormais les
chapitres prévus du socle des études disponibles. Chaque total d’études
est décomposé en études du socle et approfondissements. Aucun ratio ne
compare les études satellites au seul socle. Le compteur de la miniature
`GrapheMindmap` distingue également ses nœuds du socle et ses extensions.

Au moment de cette passe, la banque copro contient 389 chapitres du socle,
4 extensions et 7 leçons correspondantes : 3 du socle et 4 approfondissements.
Ces nombres ne sont pas codés dans le client. L’affichage des études utilise
`etudeDisponible` avec le programme reçu, les cartes, le journal et la date
du joueur. Une étude périmée, en brouillon, privée d’une carte ou dont une
carte est signalée n’entre pas dans le total disponible. Une leçon étrangère
aux nœuds du programme reçu n’y entre pas non plus.

## Preuves

- Deux tests SSR échouaient avant correction : distinction des compteurs
  absente et absence de prise en compte du signalement.
- Après correction de l’en-tête et de l’aperçu, le test a encore détecté le
  total mélangé dans la miniature. Le libellé a été corrigé après extension
  explicite du cahier à `GrapheSavoir.tsx`.
- `npx vitest run src/ecrans/Arbre.test.ts src/ecrans/GraphePrerequis.test.ts src/moteur/graphe.test.ts` : 8/8 passent.
- `npx tsc --noEmit` : passe.
- Aucun navigateur, build, test global ou déploiement exécuté pour cette passe.

Les tests vérifient le rendu et les conditions de disponibilité. Ils ne
prouvent ni l’apprentissage, ni la publication VPS, ni le rendu sur appareil
réel. Aucun programme, contenu de cours ou état joueur n’a été modifié.

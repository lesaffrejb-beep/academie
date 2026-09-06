# Relecture indépendante du graphe, 06/09/2026

Outil : Codex ; modèle : GPT-6. Agent : acces_profils, qui n'a pas écrit
les fichiers du graphe. Revue du code et contrôles ciblés, sans nouveau
contrôle visuel ni appel au VPS. Le rapport PREUVES.md de l'auteur a été
consulté ; ses preuves navigateur ne sont pas présentées ici comme rejouées.

## Périmètre et verdict

Fichiers inspectés : `Arbre.tsx`, `GraphePrerequis.tsx`,
`graphePrerequis.css`, `moteur/graphe.ts`, puis les frontières magasin,
serviceabilité et étude dont dépendent les accès.

Aucun défaut bloquant trouvé dans les relations, le choix de cursus ou
les liens vers le contenu. Un défaut mineur de texte a été transmis à
l'auteur : un chapitre dont tous les prérequis sont introuvables affiche
« Aucun prérequis déclaré » dans Les bases puis nomme les références
absentes plus bas. Le premier message doit distinguer absence de déclaration
et absence dans le programme. Correction demandée au parent et autorisée.

## Constat par exigence

- Les arêtes viennent exclusivement des identifiants de `prerequis`.
  Entrées : prérequis vers centre ; sorties : centre vers suites directes.
  Aucun lien de branche ou de rang n'est transformé en prérequis.
- Les références introuvables sont gardées dans `absents`, sans fabriquer
  de nœud. Les liens interdomaines restent identifiés dans la projection
  puis affichés en pointillés et avec le nom de domaine voisin.
- Arbre reçoit banque et monde du magasin. Le compte fixe le métier actif ;
  la banque de ce métier filtre les cartes et fournit son programme avant
  construction du monde. Le composant de graphe ne recharge aucun programme
  global. Les leçons, conservées globalement dans la banque, ne sont cherchées
  que pour l'identifiant du chapitre sélectionné du monde courant.
- Les états viennent du moteur. Un nœud sans cartes est « Au programme » ;
  il ne reçoit ni pourcentage ni niveau de compétence inventé.
- Les cartes disponibles sont recalculées par `cartesServiables` avec le
  journal et le jour. Réviser est désactivé quand il n'en reste aucune.
  L'accès à l'étude exige `etudeDisponible`, qui vérifie le statut de la
  leçon, ses dates et toutes ses cartes. Les routes sont les routes réelles
  de salle d'étude et de révision du chapitre.
- Les contrôles HTML natifs gardent des labels et des cibles de taille utile.
  Les SVG sont décoratifs et les relations sont également lisibles sous
  Les bases, Ce chapitre et Pour aller plus loin. Le CSS prévoit une colonne
  sur mobile, les retours à la ligne et des actions de hauteur minimale.
  Ce constat de code ne remplace pas un essai lecteur d'écran ou physique.

## Contrôles rejoués

Commande depuis `web/` :

```sh
npx vitest run src/moteur/graphe.test.ts src/app/magasin.metier.test.ts src/moteur/serviceabilite.test.ts src/moteur/etude.test.ts
```

Résultat : **19 tests verts**, à 18:37 heure de Paris. Ils couvrent la
projection orientée, les références manquantes, recherche et filtres,
l'isolation des indicateurs par métier, les cartes périmées ou signalées
et l'accès aux études. Aucune suite globale n'a été relancée dans cette revue.

## Confirmation de la correction

Le texte de `GraphePrerequis.tsx` distingue désormais `graphe.absents.length` :
« Aucun prérequis disponible dans ce programme » si les références manquent,
« Aucun prérequis déclaré » sinon. Correction constatée dans le code courant.
Aucun constat ouvert de cette relecture du graphe.

# Reprise visuelle du 05/09

Outil : Codex. Modèle : GPT-6. Demande de JB : améliorer le front avec
références réelles, puis correction explicite contre les recettes visuelles IA.

## Références regardées

- [Thinkers, Niccolò Miranda pour Awwwards](https://www.niccolomiranda.com/work/thinkers) : hiérarchie portée par les contenus, navigation et composants communs. Le visuel de cours a été ouvert et inspecté.
- [Made in Platform, page éditoriale](https://www.awwwards.com/inspiration/article-page-made-in-platform) : titres de vrais sujets, colonnes ouvertes, contrastes de densité. Le visuel a été ouvert et inspecté.
- [Learning Mobile, Purrweb](https://dribbble.com/shots/19783203-Learning-Mobile-IOS-App) : relation typographie de lecture et navigation compacte ; illustrations et cartes non reprises.
- [Learning Platform, Windmill](https://dribbble.com/shots/20829569-Learning-platform) : visuel regardé ; grille pastel et illustrations écartées pour cette surface.
- [Carbon, espacement](https://carbondesignsystem.com/elements/spacing/overview/) : regroupements et rythme cohérent des espaces.

Les références orientent la composition ; aucun de leurs assets n'est intégré.
Les captures locales de l'audit du 05/09 et le rendu avant modification ont
été inspectés. Les captures d'inspiration mentionnées par JB n'étaient pas
jointes au contexte disponible : aucune conformité à ces images n'est revendiquée.

## Résultat local

Le vrai parcours remplace le slogan et l'italique décoratif. Le cas affiché
est l'amorce exacte du prochain chapitre disponible. L'orbite et ses accès
doublonnés sont retirés de l'accueil ; l'atlas du programme est conservé.
Les lignes de chapitre exposent ordre, titre, objectif et état réel, y compris
au clavier et dans leur nom accessible. Le thème se choisit dans l'en-tête,
persiste après rechargement et suit aussi les changements depuis le profil.

Sur mobile, les étapes précèdent l'aperçu. Premier chapitre observé vers
579 px, contre environ 920 px dans la première passe. Numéros indivisibles,
flèches internes horizontales, un seul bouton principal d'étude.

Direction : cahier de travail, modes Operate/Read. Fraunces et Source Sans 3
locales, tokens Nuit/Papier et accent par rang conservés. Pas de nouvelle
mécanique d'apprentissage ni de modification de la banque ou du journal.
DFII de travail : impact 3, adéquation 5, faisabilité 5, performance 5,
risque de cohérence 3, soit 15 selon la formule du skill. Ce jugement interne
ne mesure pas l'acceptation esthétique de JB.

## Contrôles et limites

- Test du thème exécuté avant implémentation : rouge, contrôle absent.
- `npm test` : 271 tests Vitest et 5 tests de publication passent.
- Build TypeScript/Vite : passe.
- Sélection E2E accueil, étude, relecture étude et direction artistique :
  29/30 d'abord, puis 30/30 après correction de l'attente du changement de
  carte dans le test clavier. Ce test lisait l'ancienne question pendant
  l'écriture IndexedDB ; l'assertion clavier n'a pas été retirée.
- Contrôles Python et dépôt : verts.
- Détecteur Impeccable sur les trois fichiers UI : aucune alerte.
- Inspection groupée, revue indépendante `/root/revue_front`, corrections,
  puis confirmation à 375/1280, Nuit/Papier. Aucune nouvelle boucle de finition.
- Aucun débordement observé sur ces quatre variantes, y compris texte à 200 %.

[Ordinateur Nuit](preuves/front/1280-nuit.png),
[téléphone Nuit](preuves/front/375-nuit.png),
[ordinateur Papier](preuves/front/1280-papier.png),
[téléphone Papier](preuves/front/375-papier.png).

Les captures pleine page placent la barre fixe à la position du viewport
initial : cela ne représente pas un élément intercalé dans le contenu.
La revue indépendante a demandé le déplacement du cas mobile, la préservation
de l'état dans le nom accessible et des flèches internes cohérentes ; ces
corrections sont intégrées. Elle ne certifie pas le goût de JB.

Travail local, non publié, non committé avec les nombreux changements
préexistants du dépôt. La publication VPS et l'acceptation utilisateur ne
sont pas établies par ces tests. Le sidecar Impeccable conserve son relevé
antérieur ; DESIGN.md décrit la composition présente.

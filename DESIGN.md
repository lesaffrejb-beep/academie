---
name: Académie — la planche vivante
description: Système visuel observé de l’école d’un métier, jouée tous les jours.
colors:
  nuit-fond: "#0a092d"
  nuit-surface: "#131642"
  nuit-encre: "#f6f7fb"
  nuit-encre-secondaire: "#a6b0cf"
  nuit-trait: "#282e66"
  nuit-bleu: "#7786ff"
  nuit-succes: "#4ade80"
  nuit-erreur: "#f87171"
  papier-fond: "#f6f7fb"
  papier-surface: "#ffffff"
  papier-encre: "#1a1d28"
  papier-encre-secondaire: "#586380"
  papier-trait: "#e2e6f0"
  papier-bleu: "#4255ff"
  papier-succes: "#157c3b"
  papier-erreur: "#c43838"
typography:
  display:
    fontFamily: '"Source Sans 3 Variable", system-ui, sans-serif'
    fontSize: "clamp(2.8rem, 4.8vw, 4.7rem)"
    fontWeight: 440
    lineHeight: 1.08
    letterSpacing: "-.035em"
  question:
    fontFamily: '"Source Sans 3 Variable", system-ui, sans-serif'
    fontSize: "clamp(1.6rem, 2.5vw, 2.2rem)"
    fontWeight: 400
    lineHeight: 1.3
    letterSpacing: "-.02em"
  body:
    fontFamily: '"Source Sans 3 Variable", system-ui, -apple-system, "Segoe UI", sans-serif'
    fontSize: "1rem"
    lineHeight: 1.5
rounded:
  ext: "20px"
  int: "12px"
  bouton: "8px"
  action-etude: "8px"
spacing:
  marge-mobile: "16px"
  marge-desktop: "24px"
components:
  action-etude-nuit:
    backgroundColor: "{colors.nuit-bleu}"
    textColor: "{colors.nuit-fond}"
    rounded: "{rounded.action-etude}"
    padding: "15px 20px"
  action-etude-papier:
    backgroundColor: "{colors.papier-bleu}"
    textColor: "{colors.papier-fond}"
    rounded: "{rounded.action-etude}"
    padding: "15px 20px"
  reponse-etude-nuit:
    backgroundColor: "{colors.nuit-surface}"
    textColor: "{colors.nuit-encre}"
    rounded: "{rounded.int}"
    padding: "18px"
---

# Design System: Académie

## Overview

**Creative North Star: "La planche vivante"**

Une planche d’encyclopédie adulte : papier blanc froid ou fond bleu profond, traits
fins et titres humanistes. Les surfaces ouvertes et la densité calme
laissent le contenu du métier conduire la lecture. Le savoir réel fournit
les noms, les liens et les états du dessin.

Ce relevé actualise le DESIGN.md de cette demande. Il décrit le client local
au 05/09/2026 ; [DIRECTION-ARTISTIQUE.md](DIRECTION-ARTISTIQUE.md) garde
l’autorité visuelle. Sources : `web/src/index.css`, `web/src/experience.css`,
`web/src/polices.css`, `web/src/app/theme.ts`, `Accueil.tsx`, `Etude.tsx`
et `Arbre.tsx`. La [décision 0037](decisions/0037-exploration-lisible-et-preuves-durables.md)
amende la palette et la vue globale.
La composition des surfaces reste dans
[le cahier de surface](travail/experience-2026-09-05/SURFACE.md).

**Key Characteristics:**

- Fraunces pour les titres ; Source Sans 3 pour lire et agir.
- Papier par défaut et Nuit conservé, avec un accent attribué au rang du domaine.
- Traits fins, formes circulaires et surfaces majoritairement plates.
- États explicites, sources accessibles, aucune progression inventée.

## Colors

Papier associe fond rosé très clair, encre prune et framboise sourd. Nuit
associe fond prune profond, encre claire rosée et accent rose. Une préférence
de thème déjà enregistrée reste respectée.

### Primary

L’accent porte l’action principale, l’étape active et les liens du parcours.
Le rose et le framboise relevés dans le frontmatter correspondent au rang 1. Les dix palettes de
rang restent définies dans `index.css` ; `accentDuRang` les choisit sans
connaître le nom du métier. Ne pas figer tous les domaines sur l’accent du rang 1.

### Secondary

Le vert mousse et la terre brûlée indiquent succès et erreur. Leur valeur
change avec le thème, sans transformer une erreur en alarme rouge vive.

### Neutral

Fond pour l’espace ouvert, surface pour la saisie et les feuilles, encre
pour le contenu, encre secondaire pour le contexte, trait pour les séparations.
Le texte posé sur un accent reprend le fond du thème. Les valeurs du
frontmatter sont un relevé ; les composants continuent d’utiliser les variables CSS.

## Typography

**Display Font:** Fraunces Variable, avec replis Georgia et Times New Roman.
**Body Font:** Source Sans 3 Variable, avec replis système.

Les deux polices sont auto-hébergées. Les chiffres sont tabulaires. Le corps
vaut 17 px sur téléphone et 16 px à partir de 768 px, avec un interligne de 1,5.
Le titre reprend le vrai parcours, sans slogan ni italique décoratif. La question garde une échelle plus contenue.

Sous 768 px, le titre utilise `clamp(2.3rem,8.8vw,3.4rem)` et la
question d’étude 1,3 rem, interligne 1,35. Les leçons conservent
1,08 rem / 1,8 sur ordinateur, 1 rem / 1,75 sur téléphone.

## Layout

Le cadre garde la navigation basse sur téléphone et le rail de 96 px sur
ordinateur. L'accueil utilise des marges de 40 px, puis 20 px sous 768 px,
et une largeur maximale de 1240 px. Le thème est accessible dans l'en-tête.

Sur ordinateur, le titre du parcours dialogue avec l'amorce du prochain
chapitre disponible. Le texte provient du contenu servi. Sous ce duo, une
liste ouverte présente numéro d'étape, titre, objectif et état réel.
Sur téléphone, l'action et les étapes précèdent l'aperçu du cas. La salle
retire le rail, limite le corps à 710 px et préserve les actions accessibles.

L’exploration globale présente un index de domaines nommés. Sur ordinateur,
la sélection actualise un aperçu latéral avec les branches et un accès au
domaine. Sous 768 px, toucher une ligne ouvre directement le domaine ;
l’aperçu latéral est masqué et l’action Séance reste dans le flux.

## Elevation & Depth

Le relief vient surtout du contraste des surfaces et des traits. Une ombre
ambiante est réservée aux feuilles flottantes et aux cartes de séance ;
son token et sa variante Papier sont définis dans `web/src/index.css`. Le grain SVG de
fond est léger et désactivable avec `data-grain="non"`. Il ne porte aucune
information.

## Shapes

Les rayons extérieur et intérieur du frontmatter servent les feuilles et
les champs. Les boutons d’étude possèdent leur rayon propre, déjà présent
dans le client. Les numéros et étapes sont circulaires ; leurs anneaux fins
se distinguent des contours des zones de saisie.

## Components

### Buttons

L’action d’étude est pleine, en accent, avec un texte de la couleur du fond,
une hauteur minimale de 52 px et une graisse 600. Le survol éclaircit par
filtre ; l’indisponibilité réduit l’opacité. L’aide et la sortie restent des
actions de texte accompagnées d’icônes SVG.

Le focus des contrôles utilise un contour d’accent de 2 px décalé de 2 px.
La pression réduit l’échelle à 98 % ; la préférence de mouvement réduit
supprime cette transformation. Les durées observées sont dans le sidecar.

### Cards / Containers

Les chapitres sont des lignes ouvertes : numéro de séquence, titre, objectif,
état et flèche. Le titre suit directement le numéro. Les séparations relient
les chapitres sans multiplier les panneaux. Les feuilles flottantes gardent
leur surface, leur rayon extérieur et l’unique famille d’ombre.

### Inputs / Fields

La réponse libre repose sur une surface légèrement distincte, une bordure
fine et le rayon intérieur. Le texte indicatif conserve l’encre secondaire.
Sur mobile, le champ initial à quatre lignes mesure 110 px et reçoit 12 px
de padding. Un choix sélectionné prend le trait d’accent et la surface.

### Navigation

Icône SVG et libellé restent associés. L’entrée active utilise l’accent ;
le survol ajoute une teinte légère. La barre basse respecte la zone sûre du
téléphone. Le fil d’étude associe numéros, noms d’étapes et état courant.

### Aperçu du cas et étapes

L'aperçu reprend la question exacte du prochain chapitre disponible ; il
n'expose aucun corrigé. Un seul bouton principal démarre ou reprend l'étude.
Les lignes des chapitres restent des accès directs et conservent leur état
dans le nom accessible. Les flèches horizontales indiquent une navigation
interne.

### Index des domaines

Chaque ligne présente le nom du domaine, le nombre de cartes disponibles
ou « Au programme », et les deux premières branches réelles. La sélection
de bureau est signalée ; l’aperçu donne les branches complètes, les comptes
de chapitres et de cartes, et les commandes précédent/suivant. Sur mobile,
la ligne est un accès direct. Aucun pourcentage n’est inventé pour un domaine
vide. La vue globale n’emploie plus d’orbites décoratives ; l’exploration
détaillée reste dans la vue domaine.

## Do's and Don'ts

### Do:

- **Do** conserver Papier par défaut, la préférence enregistrée et les deux thèmes.
- **Do** utiliser les vrais chapitres et états pour les parcours dessinés.
- **Do** garder les sources et les limites de progression lisibles.
- **Do** distinguer une étude parcourue d’une compétence démontrée.

### Don't:

- **Don't** ajouter de mascotte, confettis ou couleurs saturées omniprésentes.
- **Don't** réintroduire les petites étiquettes décoratives au-dessus des titres de chapitre.
- **Don't** transformer l’ombre flottante en relief de chaque section.

La revue [de l’exploration](travail/experience-2026-09-05/REVUE-EXPLORATION.md)
conclut `ship` pour trois corrections bornées : accès mobile au domaine,
action Séance dans le flux et retrait du surtitre générique. Les captures
375/1280 dans les deux thèmes ne certifient ni tous les parcours interactifs,
ni la publication VPS, ni l’acceptation esthétique de l’utilisateur.

La composition ancienne avec slogan en italique et orbite décorative est
retirée de l’accueil ; la [reprise visuelle](travail/experience-2026-09-05/REPRISE-VISUELLE.md)
en conserve le contexte. Le sidecar `.impeccable/design.json` reste un relevé
antérieur, non actualisé par cette passe ; ses palettes ne font pas référence
pour le client actuel.

## Actualisation du 05/09 au soir

Décision 0043 : références bleues fournies par JB, titres et corps Source
Sans 3 auto-hébergée. Le fichier CSS porte les valeurs exactes, dont les
accents de domaine ajustés pour la lisibilité dans les deux thèmes.

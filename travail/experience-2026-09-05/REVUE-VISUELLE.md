disposition: fix

Entrées hors captures absentes : aucun contrat séparé THESIS/OWN-WORLD/STORY/FIRST VIEWPORT/FORM ni QUALITY BAR ; les documents de direction fournis servent de référence. Aucun comp, roll, seed ou raster attendu pour cette extension du monde existant. Lecture du code limitée aux cinq fichiers primaires fournis ; aucune interaction exécutée.

## persistence

Pass pour la persistance de la direction : PRODUCT.md et DESIGN.md existent et désignent DIRECTION-ARTISTIQUE.md comme référence. SURFACE.md borne la nouvelle composition à l’accueil et à l’étude. L’absence de pipeline de reproduction de comp n’est pas un défaut dans cette construction directement en code.

Les six captures requises existent et sont valides : desktop.png, mobile.png, desktop-papier.png, mobile-papier.png, etude-desktop.png, etude-mobile.png, sous `.impeccable/review/`. Elles montrent respectivement les premiers écrans annoncés, sans région noire ni assemblage incohérent : 1280 × 900 et 375 × 812. Ce sont des captures de viewport ; le contenu sous le premier écran, les états interactifs et les autres étapes d’étude n’ont pas de preuve visuelle ici. Le détecteur fourni a retourné `[]` ; aucun second passage effectué.

## fidelity

| Élément ou promesse | Verdict | Constat et autorité |
|---|---|---|
| TYPE | match | La serif expressive, son italique et la sans humaniste gardent le caractère éditorial de la planche décrit dans DIRECTION-ARTISTIQUE.md. Le titre d’accueil domine clairement ; les questions gardent le premier rôle dans la salle. |
| MATERIAL | match | Traits, anneaux, géométrie vectorielle et surfaces plates appartiennent au monde prescrit. Aucune simulation de métal, peinture ou photographie. Aucun raster requis. |
| GROUND | adaptation | Les variantes profond sombre / blanc cassé et l’accent ocre restent cohérentes entre accueil et salle observée. DIRECTION-ARTISTIQUE.md donne des noms de couleurs, sans cible colorimétrique exacte ; une égalité de teinte ne peut pas être certifiée. La couleur Nuit observée tire vers le vert sombre plutôt que vers un bleu net. |
| Invitation et action d’accueil | match | Le premier écran montre la promesse, les deux métiers et « Commencer l’étude », également sur mobile. Les nombres sont calculés depuis les leçons disponibles dans Accueil.tsx. |
| Signature du parcours réel | contradicted | SURFACE.md promet une planche dont les étapes sont les chapitres réellement disponibles. Le dessin montre trois notions génériques codées en dur ; il ne représente ni les chapitres, ni leur disponibilité, ni leur reprise. Sur mobile, il devient trois mots entre des traits. La signature raconte une méthode abstraite au lieu du parcours annoncé. |
| Navigation et salle | adaptation | L’accueil « Apprendre » et l’atlas séparé sont explicitement permis par DESIGN.md et SURFACE.md. Le rail disparaît dans la salle ; la sortie reste visible. La barre mobile laisse apparaître l’entrée active. |
| Lecture et action mobile de l’étude | contradicted | La question prend six lignes, avec un point-virgule isolé en début de dernière ligne. À 375 × 812, le champ et l’indice sont visibles mais aucune action pour avancer ne l’est. La hiérarchie et l’espacement repoussent le contrôle principal hors de la zone du pouce prescrite dans DIRECTION-ARTISTIQUE.md. |
| Étiquettes de chapitre | contradicted | « Les pouvoirs », visible en bas de la capture desktop, est une petite étiquette au-dessus du titre. Accueil.tsx confirme le motif `chapitre-role` précédant `strong` : c’est l’eyebrow refusé par le craft floor. |
| Vérité des états | match pour le contenu inspecté | Le cas est nommé fictif. Le code distingue indisponible, reprise, attente d’écriture, erreur et étude parcourue ; il ne transforme pas la clôture en certification. Les états autres que la tentative vide ne sont pas validés visuellement par ce packet. |

Les cinq promesses de direction se lisent dans les documents existants, sans exiger un nouveau formulaire : intention d’école adulte tenue ; monde de la planche tenu ; récit des chapitres réels non tenu dans la signature ; premier écran d’accueil lisible et actionnable ; forme directement en code autorisée. Le test de mémoire retient le grand titre et l’ocre sur fond sombre, mais aucun trait propre au parcours sélectionné.

## ceiling

La demande Dribbble/Awwwards ne peut pas être considérée comme atteinte sur la seule propreté de cette composition. Le dispositif natif laissé inutilisé est le chemin de savoir réel : noms de chapitres, relations et états pourraient donner à la planche sa nécessité et sa singularité. Le diagramme générique et sa réduction mobile à trois mots restent en deçà de cette ambition. L’ornement supplémentaire, les effets de matière et un nouveau monde ne sont pas nécessaires pour corriger ce point. Le mouvement, le focus clavier, les retours, les erreurs et la clôture ne sont pas évaluables sur ces images fixes.

## material_fixes

1. **Signature / SURFACE.md :** relier la planche aux chapitres réellement disponibles et à leurs états, avec une forme compacte lisible sur mobile ; ses libellés et ses liens doivent appartenir au métier sélectionné, en conservant les traits fins et l’action dominante.
2. **Lecture et action / DIRECTION-ARTISTIQUE.md §§5 et 8 ter :** recomposer le premier écran mobile de l’étude pour rendre l’action d’avancement visible dans la zone basse sans écraser la question ni la réponse ; empêcher le point-virgule français de commencer une ligne. Vérifier de nouveau à 375 × 812 avec le texte réel.
3. **Floor / eyebrow :** supprimer la petite étiquette `chapitre-role` placée avant chaque titre, ou intégrer son information utile au texte descriptif après le titre, sans la déplacer en une autre eyebrow.

## keep

Conserver Fraunces et Source Sans 3, Nuit/Papier, l’ocre, les surfaces ouvertes, la dominance de l’action d’accueil, la salle sans rail, les cas fictifs explicites et la séparation entre étude parcourue et compétence démontrée.

---

## verdict

Second passage sur les trois corrections demandées ; les six captures ont été rouvertes aux mêmes chemins et restent valides.

1. **resolved — Signature du parcours réel :** les captures Nuit/Papier montrent maintenant « Les pouvoirs », « Le vote » et « La trace », avec leur ordre et un centre propre à l’assemblée. Le mobile conserve ces trois entrées lisibles. La lecture ciblée d’Accueil.tsx confirme que les boutons proviennent des leçons du parcours, ouvrent leur identifiant et dérivent disponibilité et coche du journal. Les captures ne montrent pas de parcours terminé ni la variante IFSI ; ces états ne sont pas certifiés visuellement.
2. **resolved — Lecture et action mobile :** à 375 × 812, la question et le champ restent lisibles, le point-virgule reste avec le mot précédent et « Confronter ma réponse » apparaît entièrement dans la zone basse. La question demeure le point d’entrée de la salle ; la réduction des espacements n’introduit pas de collision visible.
3. **resolved — Eyebrow de chapitre :** dans les deux captures desktop, « Le syndic et ses missions » suit directement le numéro. L’étiquette au-dessus du titre a disparu ; le code confirme la suppression du motif pour la liste.

## remaining

clear. Aucune régression matérielle visible introduite par ces trois corrections. Ce ship couvre uniquement les corrections évaluées, pas l’ensemble des surfaces, les interactions, l’acceptation utilisateur ni l’efficacité d’apprentissage. Les limites du premier écran restent applicables.

disposition: ship

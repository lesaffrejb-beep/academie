# Formats du parcours de contre-expertise, 06/09/2026

Outil : Codex ; modèle : GPT-6. Agent acces_profils. Extension autorisée
par JB pour l'essai des différentes formes et consignée dans
`chantiers/ACA-FRONT-2.md` et `chantiers/ACA-EXPERTISE-1.md` avant code.

## Comportement implémenté

L'étude de contre-expertise est la deuxième étude du parcours rénovation.
Le premier pilote propose Continuer le parcours après sa synthèse finale.
Les sept exercices de contre-expertise sont : rappel écrit, QCM, lecture
visuelle, association, deux réponses libres et rôle, puis la synthèse finale.

Étude réutilise désormais les modules interactifs Relier, Rôle et Datation.
Relier écrit les associations dans la première ligne de la réponse, puis
conserve l'explication libre sur les lignes suivantes. La réponse est le
brouillon existant de l'étude ; ses associations valides reconstruisent
l'affichage après rechargement. Un identifiant inconnu, une syntaxe ambiguë
ou un commentaire ne crée pas de paire et son texte reste conservé.

Les photos et plans gardent SupportEtude, son zoom et son contrôle de
chargement. Une image explicitement déclarée mais nulle ou invalide bloque
le retour ; aucun second visualiseur n'est ajouté. Une association ou
chronologie sans image peut utiliser ses données textuelles structurées.

La copie du rôle confirme uniquement un presse-papier réussi. Aucun moteur
de dialogue vocal, enregistrement audio, vidéo ou correction experte
automatique n'est ajouté. Les textes libres restent des productions de
l'élève à comparer au corrigé. Les critères ne certifient pas une compétence.

## Preuves de cette passe

- Trois tests de rendu du vrai composant Étude échouaient avant branchement :
  association, rôle à copier et datation absents. Les trois passent ensuite.
- Le test de restitution des liens depuis `1-a` échouait avant correction,
  puis passe ; le commentaire contenant `2-b` ne fabrique pas de deuxième lien.
- Dix tests ciblés passent, incluant absence de contenu inventé, fidélité des
  décimales, données structurées et formats d'étude. TypeScript passe.
- `web/tests/e2e/contre-expertise.spec.ts` parcourt le pilote puis l'étude,
  vérifie la source et le schéma réel, relie des paires, recharge l'écran,
  conserve le commentaire et contrôle la synthèse finale dans IndexedDB.
  Le compte et l'API y sont simulés ; cela ne prouve pas la sauvegarde VPS.
- L'exécution navigateur par cet agent a été rejetée par l'approbation
  automatique, qui considère les messages fiables limités à NotebookLM.
  Aucun succès E2E de ce nouveau fichier n'est revendiqué ici ; l'intégration
  parent doit consigner son résultat exécuté séparément.

## Premier rejeu intégré

Le rejeu parent a retrouvé la production initiale après rechargement dans
les deux captures d'échec, mais le sélecteur `getByLabel` exact ne trouvait
plus le champ dont le textarea restauré porte un contenu textuel dans le
DOM. La capture accessible montre le textbox nommé « Ta réponse » et le
texte complet attendu. Le test utilise désormais ce rôle accessible exact,
en conservant la même assertion `toHaveValue` intégrale. Aucune correction
de l'application ni suppression de contrôle de reprise n'a été faite pour
ce constat ; le trajet complet doit encore être rejoué.

## Limites de saisie et remise à zéro

La relecture indépendante a reproduit deux défauts : une association ajoutée
à un commentaire de 5 000 caractères dépassait le contrat ; effacer les liens
pouvait réinterpréter un commentaire littéral `2-b` comme une association.
Deux tests rouges ont reproduit ces états avant correction. La composition
refuse désormais les réponses trop longues sans appeler la sauvegarde ni
tronquer le texte, avec une erreur visible. La première ligne vide conserve
la séparation du commentaire après réinitialisation. Les tests contrôlent
aussi l'acceptation à exactement 5 000 caractères et le retour des liens
sans altérer le commentaire.

## Reprise de la grille de synthèse

Le premier rechargement immédiatement après Comparer à la grille interrompait
une écriture IndexedDB non encore terminée. Le test attend maintenant le
rendu qui suit cette écriture, puis recharge sans retirer son assertion de
reprise. Il a ensuite révélé une perte réelle des critères encore non
confirmés : le rejeu parent 29997 retrouvait le critère initial décoché.

Les choix sont désormais conservés par le même brouillon de compte, chapitre,
version et étape que les autres saisies. Seuls les indices entiers présents
dans la grille sont interprétés à la lecture, ordonnés et sans doublons.
Le journal reste append-only et Garder cette étape enregistre les critères
explicitement choisis. Le test exige deux cases cochées et une case non cochée
après rechargement avant d'enregistrer la clôture et de recharger à nouveau.

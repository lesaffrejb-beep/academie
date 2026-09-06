# Contre-lecture indépendante du dernier diff interface

Codex / GPT-6, agent `/root/graphe`, 06/09/2026. Relecture du code écrit
par le coordinateur, distincte de la rédaction du candidat façade.
Fichiers : `ModulesSeance.tsx`, `Etude.tsx`, `donnees/types.ts`,
`Etude.formats.test.ts`. Aucun contenu pédagogique n'est certifié par
cette passe. Aucun code, navigateur ni test global modifié ou exécuté.

## Verdict

Aucun défaut bloquant trouvé dans le diff examiné. Les changements de rôle
préservent la question entière, et ceux des sources cessent de transformer
une nature absente ou différente en « Institution ». Une réserve mineure
sur les clés héritées de la table de libellés est décrite ci-dessous.

## Rôle, contexte et aide

`scenario` référence directement `carte.question`, sans extraction ni
normalisation. Le paragraphe l'affiche avec conservation des retours à la
ligne, même en l'absence de citation. Le bouton écrit exactement cette
variable dans le presse-papier. Les extraits entre guillemets ne servent
plus qu'à tenter d'identifier un interlocuteur ; ils ne remplacent ni le
scénario affiché ni la chaîne copiée. L'objectif éventuel est extrait de
la question déjà visible, pas d'un corrigé ou de l'aide cachée.

Le composant ne lit pas `carte.aide`. Le panneau Étude ne l'affiche qu'après
le passage de `aide` à vrai par le bouton dédié. Ce changement passe par le
brouillon existant, de même que la réponse. À l'enregistrement, la trace
`aide_utilisee` est conservée et `noteCarte` produit le mode `synthese`
sans note de rappel autonome si une aide a été demandée. Ce chemin n'a
pas été réécrit par le dernier diff et aucune aide gratuite supplémentaire
n'y a été introduite. La copie seule n'est pas assimilée à une réponse
produite : l'élève doit toujours saisir sa réponse avant de voir le retour.

L'échec du presse-papier reste une alerte sans message de succès. La saisie
reste contrôlée, limitée à 5 000 caractères et non modifiable après
révélation ; les clés de brouillon, callbacks et événements du journal
ne changent pas dans ce diff.

## Provenance affichée

`Source.parti` devient un champ optionnel de type chaîne. Le dossier affiche
le texte déclaré lorsqu'il contient autre chose que des espaces ; aucune
position n'est fabriquée lorsque le champ est absent. Les onze natures du
valideur actuel ont un libellé correspondant. Une nature absente ou blanche
est affichée comme non renseignée ; une valeur inconnue ordinaire est
conservée telle quelle. Les textes passent par l'échappement React. Les
liens restent limités à HTTPS et ouverts avec `rel=noreferrer`.

Le remplacement de la phrase qui présentait les sources comme établissant
systématiquement des règles évite de traiter une recommandation ou une
analyse comme un texte normatif. Il ne change pas la qualification des
sources ni leur disponibilité dans la banque.

Réserve P3 : la table `natures` est un objet JavaScript ordinaire et
`natures[s.nature]` peut donc trouver une propriété héritée pour des valeurs
inconnues telles que `constructor` ou `toString`. Le rendu ne conserverait
alors pas la chaîne attendue. Le contrat actuel borne les natures servies,
ce qui limite l'exposition ; si le fallback doit accepter toute chaîne
inconnue, employer une recherche de propriété propre et un cas ciblé.
Cette réserve a été transmise au coordinateur avant sa vérification finale.

## Preuves et limites

Les tests ajoutés couvrent la présence du contexte après une citation,
la question sans citation, l'absence d'aide dans le rôle, l'affichage du
parti et l'absence de substitution « Institution » pour un éditeur ou une
nature manquante. Les autres formats restent exercés par les tests
existants du même fichier. Le coordinateur annonce sept tests ciblés verts
après rouge, puis sa suite npm verte ; cette sous-tâche ne les a pas rejoués.

Ces tests SSR ne déclenchent pas le clic de copie : le contenu effectivement
écrit au presse-papier est établi ici par lecture du callback, sans nouvelle
preuve navigateur. Ils ne démontrent pas non plus la persistance de l'aide,
la synchronisation d'un compte ou le parcours téléphone/Mac. Les preuves
antérieures de ces comportements restent distinctes.

Limite de périmètre existante : ce dossier reçoit `lecon.sources`, y compris
après un exercice. La présente passe n'ajoute pas un dossier propre aux
sources de chaque carte. Si une carte dispose d'une source différente de
celles du chapitre, il faut traiter séparément sa traçabilité dans Étude.
Aucun défaut nouveau de ce type n'est introduit par le diff examiné.

## Suite du coordinateur après la revue

La réserve sur les propriétés héritées a été reproduite : la nature
`constructor` produisait une valeur non textuelle. Le rendu utilise
maintenant `Object.hasOwn` et conserve la valeur inconnue littérale.
Deux tests portent sur une nature externe ordinaire et `constructor` :
rouge sur ce dernier, puis neuf tests de rendu tous verts. Le scénario
Façade a depuis compilé et passé ses quatre E2E sur ce même client.

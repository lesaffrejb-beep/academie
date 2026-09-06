# Relecture indépendante des modules de séance, 06/09/2026

Relecteur : Codex / GPT-6, agent `/root/graphe`, distinct de l'auteur
`/root/acces_profils`. Périmètre : diff de Seance.tsx, ModulesSeance.tsx,
supportSeance.ts, tests SSR et nouveaux E2E d'exercices. Vérification contre
le journal-v1 et les contrôles serveur existants. Pas de nouvelle lecture
ou promotion de contenu source.

Les champs `reponse_libre` et `attendus_coches` remontent au composant qui
écrit l'événement de révision. Les boutons et raccourcis transmettent les
mêmes valeurs. Le verrou d'écriture reste en place. Le schéma et le serveur
acceptent ces champs et limitent la réponse à 5 000 caractères. Les saisies
spécialisées ont cette borne. Un refus du presse-papier montre une erreur,
sans message de copie réussie.

La disparition des modèles fictifs de ventilation et de recouvrement est
confirmée : sans repères explicites, la saisie libre conserve la question
et son support. Les données structurées gardent leurs identifiants. Les
critères cochés restent une autoévaluation, pas une correction automatique.

Un P2 a été trouvé dans les regex d'extraction : `2.5` devenait `2` avant
affichage. L'auteur a ajouté un test rouge puis conservé les points suivis
d'un chiffre dans les trois extracteurs. Relecture du delta et du test
`2.5` / `1.2` : le défaut reproduit est corrigé.

Preuve navigateur exécutée indépendamment :

```sh
CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' npm --prefix web run e2e -- exercices.spec.ts --grep 'synthèse conserve|refus du presse'
```

Résultat : **6 tests verts en 14,6 s**, trois comportements sur ordinateur
et téléphone. La réponse multiligne et le tableau `[1]` sont relus dans
IndexedDB après clic ou touche 3. Le refus du presse-papier reste une erreur.
Build TypeScript/Vite inclus. Les tests SSR ciblés ont été réexécutés après
correction des décimales.

Verdict sur ce diff : aucun bloquant restant trouvé. Ces tests utilisent
une API et un profil fictifs ; ils ne prouvent pas la synchronisation d'un
compte réel sur VPS. La trace d'une réponse est écrite lors de sa notation :
cette passe ne promet pas la reprise d'une saisie de séance non soumise.
L'analyse ne certifie pas le contenu pédagogique des cartes ni l'efficacité
mesurée des formes d'exercice.

## Complément Étude et reprise des associations, vers 19:00

Périmètre supplémentaire : Etude.tsx branche Relier, Rôle et Datation dans
le parcours servi. Les champs continuent à passer par le brouillon privé
lié au compte, au chapitre, à la version et à l'étape. Les photos/plans et
les images explicitement déclarées conservent le contrôle SupportEtude.
Une association ou chronologie textuelle ne reçoit pas d'image inventée.

La relecture a relevé deux problèmes dans la nouvelle conservation des
commentaires : un ajout de lien après une saisie de 5 000 caractères faisait
dépasser le contrat ; un commentaire commençant littéralement par `2-b`
pouvait devenir une association à l'effacement du dernier lien. L'auteur
a ajouté deux tests rouges, puis un assembleur qui refuse explicitement
le dépassement sans modifier le texte et conserve une première ligne vide
pour séparer les commentaires littéraux. Le composant expose l'erreur et
n'appelle pas le changement de réponse si l'assembleur refuse.

Lecture indépendante du delta et réexécution des tests : **12 tests verts**
dans supportSeance.test.ts, ModulesSeance.test.ts et Etude.formats.test.ts ;
TypeScript vert. Le graphe, la sélection par indices connus et le contrôle
des supports n'introduisent pas de blocage supplémentaire trouvé dans ce
diff. La preuve navigateur du parcours contre-expertise appartient au run
intégré du coordinateur et n'est pas déduite de ces tests SSR. Le contenu
et l'alignement de chaque correspondance avec la réponse source restent
la responsabilité de la revue éditoriale distincte.

## Dernières jointures avant paquet

La conservation des coches dans le brouillon Étude utilise la même clé
privée compte/chapitre/version/étape/index. La reprise filtre les indices
entiers dans la grille courante, les déduplique et les trie. Les cases
passent par l'écriture du brouillon et le journal final garde le tableau.
Lecture indépendante du delta : aucun défaut supplémentaire trouvé ; la
preuve de rechargement navigateur appartient au run du coordinateur.

La relecture du transport `paires` / `etapes` dans le générateur a trouvé
un contrat machine divergent : il décrivait des objets element/cible et
des étapes chaînes, alors que les données et le client utilisent
gauche/droite et num/titre/cible. Sur arbitrage du coordinateur, le contrat
est aligné et le valideur refuse désormais les supports facultatifs
malformés. Les tests de chaîne du coordinateur couvrent le transport ;
19 nouveaux cas du valideur ont échoué avant le correctif puis passent.
Les listes vides, anciens formats, éléments non objets, textes blancs,
plus de 26 paires, numéros d'étapes non entiers positifs représentables
exactement par JavaScript, numéros dupliqués et cibles non booléennes
sont refusés sans crash. Les 9 chapitres / 55 cartes actuels passent le
valideur, et `tooling/check.py` ne relève aucune erreur. Ce dernier delta
est écrit par le relecteur de l'interface ; sa relecture indépendante
appartient donc au coordinateur.

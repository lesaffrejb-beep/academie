# Preuve E2E du parcours Fragilité

Test : `web/tests/e2e/fragilite.spec.ts`. Outil Codex, modèle GPT-6,
agent `/root/acces_profils`, préparation du 06/09/2026 dans le cahier
ACA-EXPERTISE-1 étendu par le coordinateur. Pas de modification du contenu.

## Rouge avant intégration

Commande exécutée avec permission d'ouvrir le serveur local :

```sh
cd web
CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' npm run e2e -- tests/e2e/fragilite.spec.ts --project=ordinateur --grep 'garde la tentative'
```

Résultat : un test en échec, code de sortie 1. L'échec intervient au clic
sur « Ouvrir Qualifier une copropriété fragile », absent de l'accueil avant
intégration. Le build et le démarrage du navigateur ont réussi. Log :
`travail/fragilite-2026-09-06/e2e-rouge.log`. Le contexte d'erreur et la trace
Playwright sont dans `web/test-results/fragilite-le-parcours-frag-6d8dd-it-exercices-et-la-synthèse-ordinateur/`.

## Assertions préparées pour le rejeu après génération

- Ouverture depuis l'accueil copro, titre et identifiant du chapitre.
- Première réponse conservée après reload, puis retrouvée dans le principe.
- Source Anah regroupée par la relecture indépendante : libellé couvrant les
  pages 8, 10-16 et 22, lien vers le PDF officiel à la page 10.
- Huit questions non synthèse : réponses libres, choix et identifiants exacts
  retrouvés dans les huit événements de révision.
- Deux rôles proposés à un binôme, avec saisie libre et sans bouton de
  conversation automatique ; copie du premier scénario comprenant motif du
  procès-verbal et consigne. L'indice non demandé reste absent de la copie et
  de l'écran pour conserver le statut de rappel autonome. Le presse-papier est simulé dans le contexte
  navigateur, sans échange externe.
- Reprise d'une réponse libre et d'une réponse de rôle après reload.
- Synthèse finale conservée, huit critères, cases 0/3/7 reprises après reload
  et retrouvées dans l'événement terminal ; autres cases restées décochées.
- Clôture persistée et absence de débordement horizontal.
- Compte IFSI : absence du parcours à l'accueil et refus de servir son contenu
  par URL directe.

Captures prévues pour chaque projet : `role-ordinateur.png`,
`role-telephone.png`, `grille-ordinateur.png`, `grille-telephone.png`, dans ce
dossier. Elles ne sont produites qu'après que le parcours les atteint.

## Vert après intégration

Commande : même environnement Chromium, puis
`npm run e2e -- tests/e2e/fragilite.spec.ts` sans filtre de projet.
Le premier rejeu s'est arrêté sur l'attente devenue obsolète de trois liens
source : la relecture indépendante avait regroupé ces pages dans une seule
référence Anah. La source du chapitre et celle de `site/banque.json` ont été
comparées ; le test vérifie désormais cette référence unique, ses pages
explicites et son lien précis, sans relâcher le contrôle des sources.

Rejeu final, code de sortie 0 : **4 passed (14.4s)**.

| Projet | Parcours complet | Exclusion IFSI |
|---|---|---|
| ordinateur | 3,0 s | 330 ms |
| telephone | 3,2 s | 354 ms |

Log final : `e2e-vert-rejeu.log`. Les assertions listées ci-dessus passent,
y compris la copie du scénario complet sans indice non demandé, les huit
productions de révision et les cases 0/3/7 de la synthèse finale. Le build
utilisé contient l'intégration du coordinateur et sa correction de ModuleRole.
L'auteur du test n'a modifié ni contenu, ni banque, ni composant pour ce rejeu.

Captures inspectées après réussite :

- `role-telephone.png` : scénario lisible dans le bloc de copie ; bouton
  placé sous le texte, sans recouvrement. La répétition avec l'énoncé allonge
  l'écran, mais aucun libellé n'est coupé.
- `grille-ordinateur.png` et `grille-telephone.png` : huit critères lisibles,
  cases 0/3/7 visibles cochées, autres décochées, bouton de conservation
  accessible, aucun débordement horizontal constaté.
- `role-ordinateur.png` est également produit par le test, sans inspection
  visuelle spécifique revendiquée dans cette passe.

## Limites

Le profil, le presse-papier et l'API journal sont simulés. Le vert porte sur le
vrai build et le stockage du navigateur, pas sur un compte réel, un échange
avec un modèle ou une synchronisation VPS. Les captures téléphone utilisent
le projet Playwright de 375 × 812 pixels, pas un téléphone physique. Les tests
globaux sont centralisés par le coordinateur et n'ont pas été relancés ici.

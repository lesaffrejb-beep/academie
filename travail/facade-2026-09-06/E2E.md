# Preuve E2E du parcours Façade

Préparation le 06/09/2026 par Codex, modèle GPT-6, agent `/root/acces_profils`,
dans le cahier ACA-EXPERTISE-1 étendu par le coordinateur. Périmètre :
`web/tests/e2e/facade.spec.ts` et preuves dans ce dossier, aucun changement de
contenu ou de composant.

## Rouge avant intégration

Commande exécutée avec permission du serveur local :

```sh
cd web
CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' npm run e2e -- tests/e2e/facade.spec.ts --project=ordinateur --grep 'garde la tentative'
```

Un test en échec, code de sortie 1 : après dix secondes, le bouton
« Ouvrir Comprendre une façade ancienne » est absent de l'accueil. L'échec
est situé sur l'assertion de visibilité précédant son clic. Build et
navigateur démarrés. Log : `e2e-rouge.log`.

## Assertions préparées

- Entrée depuis l'accueil copro et titre exact du chapitre.
- Première réponse conservée après reload et dans le journal du principe.
- Source publique unique après relecture, pages 2/11-14 dans le libellé,
  URL précise du PDF sur data.geopf.fr à la page 11 ; nature Institution et
  limite des recommandations face au règlement visibles.
- Huit questions non synthèse et huit identifiants exacts dans le journal ;
  toutes les productions, y compris les choix, comparées au texte conservé.
- Deux rôles offerts avec bouton de copie ; le premier, sans citation dans
  l'énoncé, doit copier exactement la question complète sans l'indice masqué.
- Réponses au rôle et à l'exercice de révision de l'avis reprises après reload.
- Synthèse finale, sept critères, cases 1/5 cochées et reprises après reload,
  autres critères décochés, texte et indices retrouvés dans l'événement final.
- Clôture persistée, contrôle du débordement horizontal.
- Compte IFSI : absence du parcours à l'accueil et de contenu par accès direct.

Captures pour ordinateur et téléphone : `role-<projet>.png`,
`grille-<projet>.png` et `source-<projet>.png`.

## Vert après intégration et génération

Commande : même environnement Chromium, puis
`npm run e2e -- tests/e2e/facade.spec.ts`, les deux projets sans filtre.
Le libellé de la source a été aligné avant lancement sur la version intégrée
du coordinateur : « pages PDF 2 et 11-14 ». L'URL précise reste contrôlée.

Résultat : **4 passed (16.1s)**, code de sortie 0.

| Projet | Parcours complet | Exclusion IFSI |
|---|---|---|
| ordinateur | 3,6 s | 375 ms |
| telephone | 3,3 s | 402 ms |

Log : `e2e-vert.log`. Toutes les assertions préparées passent, y compris le
texte exact de la copie du rôle sans guillemets, l'absence d'indice non demandé,
les huit identifiants et productions de révision, les sept critères et les
indices 1/5 enregistrés avec la synthèse terminale.

Captures examinées : source et rôle sur ordinateur et téléphone, grille sur
téléphone. La source affiche « Institution », les pages, le lien, la réserve
sur le règlement et les mentions de fabrication. Le rôle conserve la question
complète dans le bloc de copie ; le bouton se situe sous le texte sans le
recouvrir. La grille téléphone présente les sept critères et les cases 1/5
cochées. Aucun texte tronqué ou débordement observé. La capture de grille
ordinateur est produite mais n'a pas été inspectée visuellement dans cette
passe.

Le test Fragilité n'a pas été relancé : ses assertions de parcours et de
persistance restent couvertes par sa preuve précédente. L'ajout d'affichage
de nature/parti est maintenant éprouvé par le parcours Façade et les contrôles
unitaires du coordinateur.

## Limites

Le profil, l'API journal et le presse-papier sont simulés. Le test porte sur
le vrai build et la persistance du navigateur, sans preuve de compte réel,
de synchronisation VPS ou d'efficacité pédagogique. Le projet téléphone est
un viewport Playwright de 375 × 812 pixels, pas un appareil physique. Aucun
contenu, banque ou composant n'a été modifié par l'auteur du test ; les tests
globaux restent centralisés par le coordinateur.

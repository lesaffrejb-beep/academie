# Cahier ACA-FRONT-2 : le client v2

Résultat attendu : `web/` remplace l'archipel : arbre global et vue
domaine, séance, fiche de nœud, clôture, profil, boîte, crédits, page
Confiance ; hors-ligne d'abord ; DA appliquée ; `check.py` mis à jour.
Fini quand : première question en moins de trois secondes réseau coupé
sur téléphone ; checklist `DIRECTION-ARTISTIQUE.md` §9 ; aucun hôte
tiers contacté (test qui liste les hôtes) ; parité FSRS et progression
avec Python ; revue rendue indépendante. La publication réelle relève de
ACA-PUBLICATION-2 ; les sept séances d'acceptation sont conservées dans
ACA-RITUAL-1 parmi les trente (décision 0035).
Dépend de : ACA-JOURNAL-SYNC-1, ACA-PROGRAMME-1, ACA-REUSE-1
(et ACA-ARBRE-1 pour l'arbre au niveau du chapitre : sans lui, l'arbre
v2 s'arrête au domaine). Bloque : ACA-ETUDE-1, ACA-EXAMEN-1.

## Périmètre

Peut créer ou modifier : `web/**`, `deploy/academie-publication.service`
(build), `deploy/Caddyfile.academie` (CSP), `tooling/check.py`
(retirer les marqueurs de l'archipel, ajouter les contrôles du client),
`client/` (suppression à la bascule, par `git mv` vers
`archive/client-archipel-AAAA-MM-JJ/`), `README.md` (la chaîne),
`DIRECTION-ARTISTIQUE.md` (un écart trouvé en construisant se note,
la direction ne se réécrit pas).
Ne touche pas : `app/`, `serveur/` hors de ce que l'API exige déjà,
`contenu/` (on l'importe, on ne l'édite pas ; un texte manquant s'ajoute
par une ligne dans `contenu/voix.json` avec trois variantes),
`academie.json`.

## Déjà tranché (ne pas rouvrir)

- Stack et dépendances : `decisions/0007`, `web/README.md`.
- Écrans, barre, salle, carte d'exercice, mouvement, accessibilité,
  regard et stimulation, clavier : `DIRECTION-ARTISTIQUE.md`.
- La maquette du 02/09 (`travail/maquette-2026-09-02.html`) est la
  référence visuelle ; l'onglet Cercle est masqué tant qu'ACA-CERCLE-1
  n'est pas livré.
- La voix : `VOIX.md`, `contenu/voix.json`, variantes par graine.
- Tout ce que le client calcule se recalcule : aucun score stocké,
  aucun état hors du journal (`decisions/0006`).
- Un `banque.json` sans `contrat` se lit comme v1 ; un contrat inconnu
  est refusé à l'écran.
- Aucune clé, aucun hôte tiers, CSP stricte (`decisions/0020`) ; polices
  auto-hébergées.
- Le sans-source, la note de confiance, la provenance et « cette carte
  est fausse » sont sur chaque carte (`BLUEPRINT.md` §10).

## Étapes, dans l'ordre

1. Initialiser Vite + React + TypeScript strict + Tailwind avec les
   tokens de la DA en variables ; CSP dans `index.html` et Caddy.
2. Tests rouges : `parite.test.ts` (vecteurs FSRS et progression),
   `hors-ligne.e2e.ts` (réseau coupé, séance jouée, envoi au retour),
   `hotes.test.ts` (aucun hôte tiers), `voix.test.ts` (chaque clé
   affichée existe dans `contenu/voix.json`).
3. `moteur/` : `fsrs.ts` (ts-fsrs épinglé, poids depuis `banque.json`),
   `journal.ts` (Dexie, file, union), `etats.ts`, `progression.ts`,
   `composeur.ts` (séance, domaine, au hasard, semaine type, pondération
   socle, graine), `points.ts`.
4. Écrans dans l'ordre : Salle (séance et clôture), Arbre, Domaine,
   Nœud, Profil, Boîte, Crédits, Confiance. Chaque écran : téléphone à
   375 px et ordinateur à 1280, Nuit et Papier, mouvement réduit.
5. PWA : manifest, service worker, cache de la banque et des polices.
6. Bascule : build dans la publication, `client/` archivé, `check.py`
   mis à jour, JB joue sept séances.

État du 05/09 : l'archipel a déjà été archivé. La publication et les séances
de cette ancienne étape 6 sont désormais attestées dans les deux chantiers
ci-dessus, sans refaire l'archivage ni les considérer acquises.

## Ce qu'on ne fait pas

- Pas de cercle, pas de ligue, pas de défis (masqués).
- Pas d'étude ni d'épreuve complètes (ACA-ETUDE-1, ACA-EXAMEN-1) ; les
  boutons existent et disent « bientôt » avec la voix.
- Pas de 3D, pas de lieu-monde.
- Pas d'animation qui dépasse une seconde ; pas de confetti ; pas
  d'exclamation.

## Preuve

```bash
cd web && npm test && npm run build && npm run e2e
```

```bash
python3 tooling/check.py
```

JB voit : l'arbre sur son téléphone dans le tram, une séance de bout en
bout sans réseau, et sur le Mac le soir le même état.

## Corrections ciblées issues de l'audit du 05/09

Lire `travail/audit-2026-09-05/AUDIT.md` et ses captures. Aucune nouvelle
refonte visuelle n'a été demandée ou réalisée pendant l'audit.

1. Montrer ce qui se joue avant les dizaines de chapitres « À écrire » ;
   distinguer explorer le programme et commencer à apprendre. L'arrivée
   générale et les comptes restent ACA-ONBOARDING-1.
2. Éprouver un départ novice : la séance observée commence par un schéma de
   procédure de niveau III. Si le correctif touche le composeur, extension
   bornée du périmètre à `app/seance.py`, composeurs Python/TS et tests de
   parité ; ne pas modifier les paramètres FSRS ni inventer des prérequis.
3. Rendre les schémas consultables à 375 px et la correction parcourable avec
   actions accessibles ; donner des libellés aux pictogrammes de domaines.
4. Conserver le brouillon de la boîte quand on change d'onglet ; tester aussi
   abandon explicite et reprise, sans produire d'envoi non demandé.
5. Restaurer le focus au déclencheur à la fermeture du dialogue, et guider
   le focus vers le nouvel écran après navigation. Ne pas confondre un test
   clavier avec une certification WCAG ; éprouver lecteur d'écran et zoom.
6. Distinguer résultat de la réponse, confiance et autoévaluation. Montrer
   provenance/absence de provenance sans fabriquer de preuve de maîtrise.
7. Ajouter les tests web, build et E2E appropriés à `.github/workflows/` ;
   extension bornée à la CI. Les tests doivent échouer sur les régressions
   observées avant correction. Revue rendue Impeccable selon `web/AGENTS.md`.

## Reprise autorisée du 05/09, couleurs et graphe

JB demande explicitement de reprendre les couleurs et le graphe, avec
arbitrages réversibles et publication. Le périmètre inclut cette fois
la DA, DESIGN.md et une décision : Papier par défaut, encre prune et
rose sourd, Nuit conservé ; exploration par domaines lisibles et branches
réelles, sans orbites décoratives. Aucun calcul de progression modifié.
Mode de surface : Operate / Read. Le premier écran doit permettre de
choisir un domaine par son nom et distinguer cartes disponibles et
chapitres prévus. Interaction : sélection au clavier ou au toucher, puis
aperçu des branches et ouverture du domaine. Sur mobile, liste compacte
et aperçu adjacent dans le flux, sans déplacement de canevas.
Preuves avant code : défaut Papier, préférence conservée, domaines nommés
et absence de faux graphe. Puis E2E existants, rendu 375/1280 dans les deux
thèmes, contraste calculé, revue indépendante et contrôles du dépôt.

## Finition autorisée du 05/09 au soir

Intégrer la palette bleue montrée par JB (références Quizlet et diff fourni),
avec Source Sans 3 auto-hébergée, sans dépendre de la police propriétaire
absente. Garder les modules et animations existants ; corriger les contrastes
des textes et boutons dans les deux thèmes, puis vérifier le rendu mobile
et ordinateur du trajet compte → cursus → étude → élèves. Décision 0043.

## Restauration autorisée du 06/09 : le graphe des prérequis

Demande de JB : retrouver le graphe des cursus pendant la préparation de
l'essai de lundi. Outil : Codex ; modèle : GPT-6. Mode : Operate / Read.
La vue Domaines reste disponible. La vue Graphe expose tous les chapitres
du cursus courant dans un index filtrable et les vrais liens immédiats
prérequis → chapitre sélectionné → suites. Les liens interdomaines sont
identifiés. Aucun lien de hiérarchie n'est présenté comme prérequis.

Périmètre borné : `web/src/ecrans/Arbre.tsx`, nouveau composant et styles
`GraphePrerequis`, projection pure de graphe et ses tests, E2E dédiés,
preuve dans `travail/graphe-2026-09-06/`. Pas de nouveau moteur de
progression, de mécanique pédagogique, de dépendance, d'authentification
ou de donnée joueur. Les états restent ceux du moteur existant et les
accès aux études reprennent son contrôle de serviceabilité.

Tests rouges avant code : exactitude et orientation des liens, prérequis
interdomaines, référence absente conservée comme inconnue, recherche
accentuée, séparation du cursus et absence de progression fictive.
Navigateur : recherche et clavier, sélection d'un prérequis, ouverture
réelle d'une étude, chapitre sans carte, rendu 375/1280 Papier/Nuit et texte
agrandi, absence de débordement de page. Contrôles du dépôt ensuite.

## Fiabilité des exercices autorisée du 06/09

Outil : Codex ; modèle : GPT-6. Mode Operate / Read. La préparation de
l'essai du lundi inclut la correction des quatre défauts constatés dans
la salle de révision, sans nouvelle mécanique ni modification du contrat.

Périmètre : `Seance.tsx`, `ModulesSeance.tsx`, leurs fonctions de support,
les tests unitaires et `web/tests/e2e/exercices.spec.ts`. Les appariements
et chronologies reprennent seulement les données explicites de la carte ;
sans données suffisantes, la question et la réponse libre restent visibles.
Aucun exemple de ventilation ni délai de recouvrement n'est ajouté.
La révision conserve le texte saisi et les critères cochés dans les champs
existants `reponse_libre` et `attendus_coches` du journal. La confirmation
« Copié » dépend de la réussite du presse-papier ; un refus reste explicite.

Tests rouges : rendu de cartes sans paires ni étapes, extraction de trois
repères explicites sans ajout, conservation du texte et des critères au
clic comme au clavier, refus du presse-papier sans succès affiché. Puis
contrôles unitaires, E2E intégrés, tests applicatifs et contrôle du dépôt.

### Branchement des formats dans l'étude, 06/09

Le trajet d'étude réutilise les modules Relier, Rôle et Datation ; photo et
plan conservent SupportEtude et son contrôle de chargement/zoom. Une seule
image est rendue. La réponse reste contrôlée par le brouillon d'étude.
Les associations de Relier sont dérivées de la première ligne de réponse
structurée, avec contrôle des identifiants affichés ; un commentaire ne
crée pas d'association. Le texte libre après cette ligne reste conservé.
Périmètre : Etude.tsx, supportSeance.ts, ModuleRelier dans ModulesSeance.tsx,
preuves et tests de contre-expertise. Test avant code : associations absentes
dans Étude ; puis clic, rechargement, explication conservée et fin du parcours.

La reprise de la grille de synthèse conserve aussi les critères cochés dans
le brouillon isolé par compte, chapitre, version, étape et index. La lecture
n'interprète que les indices entiers des critères existants, sans doublons,
et les ordonne. Le journal reste écrit lors de Garder cette étape. Le test
attend la fin de l'écriture avant rechargement puis contrôle séparément la
reprise de l'étape, du texte et des choix de la grille avant validation finale.

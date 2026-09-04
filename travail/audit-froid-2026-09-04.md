# Audit froid et point de reprise, 04/09/2026

**Reprise du 04/09, publication demandée par JB :** [état livré, limites et suite](2026-09-04-publication-et-suite.md). Ce point actualise les mentions historiques de pause et de publication ci-dessous.

Arrêt demandé par JB pendant la finition. Ce document est le point de
reprise, pas une déclaration de livraison. Outil : Codex,
gpt-5.6-sol, effort ultra, classe grand ; trois agents de travail et de
contre-relecture. Aucun commit, push, déploiement, archivage de banque
ou migration du journal effectué par cette session.

Lire d'abord `DOCTRINE.md`, `README.md`, puis ce document et le cahier
du chantier repris. Les changements restent dans le worktree.
Des changements IFSI provenant d'une autre tâche sont apparus pendant
le travail ; ils ont été conservés, sans reprise de leur responsabilité.
Les trois agents ont arrêté leur travail. Les serveurs locaux de cette
session (ports 4173 et 5180) sont arrêtés ; aucun listener ne subsiste
sur ces ports. Les fichiers restent enregistrés, sans commit automatique.

## Conclusion froide

Le client n'est plus le squelette nu : il a son atlas, ses branches,
sa salle et ses états utiles dans la DA prévue. Plusieurs défauts de
conservation et de synchronisation ont des tests de régression.
Ce n'est pas encore un produit publiable sans réserve : un défaut
chronologique est reproduit mais non corrigé, la migration manque de
preuves éditoriales, et le trajet réel téléphone–Mac n'est pas prouvé.

## Modifications conservées

| Lot | Fichiers principaux | Résultat observable |
|---|---|---|
| Règles de goût | `web/AGENTS.md` | Impeccable installé et appliqué sous la DA ; gpt-taste installé comme référence, recettes incompatibles explicitement exclues. |
| Interface | `web/src/ecrans/`, `web/src/index.css`, `web/src/main.tsx` | Atlas SVG issu du programme, rail/bas de page, branches, modale native, Nuit/Papier, anneaux réels, profil sans activité inventée. |
| Salle | `Seance.tsx`, `Cloture.tsx` | Images réellement affichées, sources après réponse, QCM expliqué, signalement sans note, reprise après panne de stockage, protection contre double note et double ouverture. |
| Cartes servies | `web/src/moteur/serviceabilite.ts`, `donnees/banque.ts`, `composeur.ts`, `app/magasin.tsx` | Statut, péremption, signalements et passage de minuit pris en compte, cache inclus. |
| Journal | `web/src/moteur/journal.ts`, `serveur/academie_etat/journal.py`, `serveur/API.md` | Lecture distante avec file vide, borne de curseur inclusive, lots refusés précisément, 401/5xx conservant la file, requêtes concurrentes et demande tardive reprises. |
| Import | `serveur/importer_journal.py` | Champs canoniques et nonce v1 conservés ; importer de nouveau ne recompte plus le même événement. |
| Boîte/profil | `Boite.tsx`, `Profil.tsx`, `app/magasin.tsx` | Liste conforme à la vraie réponse API, texte saisi pendant un dépôt lent conservé, erreurs de synchronisation visibles et reprise manuelle. |
| Médias/build | `web/vite.config.ts`, `web/package*.json`, `web/LICENCES.md` | Lucide installé ; banque/voix/images injectées depuis les sources, pas dupliquées dans public. |
| Publication préparée | `web/preparer-publication.mjs`, `deploy/academie-publication.service` | Construction hors du dépôt en lecture seule, manifeste complet SHA-256, assets avant index, SW en dernier ; aucune action VPS. |
| Migration préparée | `app/migre_banque.py`, `app/tests_migration.py` | Simulation et candidat isolé seulement ; inventaire et empreintes refusent une modification concurrente de source. |
| Programme copro | `programme/genere_copro.py`, `programme/copro.json`, `SYLLABUS.md` | Décision 0030 appliquée : notification, déchéance du terme, P1 à P5 ; 389 chapitres. |
| Sources des domaines | cinq `travail/sources-*-2026-09-04.md`, `sources/registre.json` | 34 branches inventoriées ; 21 N1 existants proposés ; repérage public, pas lecture intégrale ni carte fabriquée. |

Les règles externes et leurs commits précis sont dans `web/AGENTS.md`.
Impeccable ne remplace ni Fraunces/Source Sans 3, ni l'atlas, ni la voix.
Le détecteur anti-patterns n'a signalé aucun motif sur les écrans visés ;
ce résultat automatique ne prouve pas la qualité visuelle à lui seul.

## Dernières preuves au point d'arrêt

- `npm test` : **197 cas Vitest + 5 tests Node de publication passent**.
- `npm run build` : TypeScript et Vite passent. JS 311,78 ko brut,
  100,97 ko gzip ; CSS 29,13 ko ; 13 entrées précachées, 766,42 Kio.
- `npm run e2e` : **54 scénarios passent**, ordinateur et téléphone.
  Cela comprend tablette 768/1024, Nuit/Papier, texte agrandi, clavier,
  hors-ligne, reprise, images, sources, refus de session et dépôt lent.
- Rendu regardé dans le navigateur : atlas mobile 375, atlas et branches
  Papier à 1280, salle Papier ; contre-relecture indépendante à 320 et
  768. Le dernier correctif tablette a son test géométrique vert mais
  mérite encore une capture de confirmation et une vérification à 200 %.
- `python3 app/tests.py` : toutes les suites hors IFSI passent ; la
  suite concurrente IFSI échoue avec **2 échecs et 1 erreur** à cet instant
  (`référentiels doit être un objet`, données et valideur en changement).
  Ce n'est donc pas une porte globale verte. Refaire le contrôle après
  stabilisation de l'autre tâche, sans écraser ses fichiers.
- `python3 tooling/check.py` : **9 erreurs**, toutes liées à l'état
  IFSI concurrent lors du contrôle : six nouveaux chapitres sans niveau
  ou titre legacy, résumé de validation en échec, tiret cadratin dans
  `programme/ifsi.json`. Ne pas confondre ce snapshot avec une conclusion
  définitive sur le travail IFSI encore en cours.
- Migration : **15 tests** et **3 mutations ciblées** détectées ; import :
  **7 tests** et mutation du nonce détectée. La campagne globale de
  mutations n'a pas été relancée sur le worktree final partagé.
- `npm audit --omit=dev` : zéro vulnérabilité de production signalée.
  Audit complet : **4 dépendances de développement signalées**, dont
  Vitest critique, Vite/PostCSS élevées et esbuild modérée. Aucun
  `npm audit fix` aveugle ni mise à niveau majeure lancé.

Les tests navigateur simulent téléphone et serveur ; ils ne sont pas
une preuve de téléphone physique, de session authentifiée sur le VPS,
de sept séances de JB ou de résultat d'apprentissage.

## À reprendre en premier

### 1. Ordre réel des révisions, défaut confirmé

Les nouvelles dates portent le décalage local, mais les lecteurs
Python/TypeScript trient encore les chaînes. Le 25/10/2026, une note 4
à `02:50+02:00`, suivie d'une note 1 à `02:10+01:00`, est rejouée dans
l'ordre inverse par les deux moteurs. La parité reste verte car leur
erreur est commune. Mélanger anciennes dates UTC et nouvelles dates
locales peut déclencher le même problème sans changement d'heure.

**Aucun correctif DST commencé.** La reproduction et le périmètre de
sept lecteurs sont consignés en fin de
`chantiers/ACA-JOURNAL-SYNC-1.md`. Commencer par tests rouges, tri par
instant et départage canonique identique, y compris fractions de seconde.
Conserver la date portée pour le jour d'apprentissage, le nonce et les
identités ; ne jamais réécrire le journal. Le curseur `recu_le` du
transport reste distinct.

### 2. Front et protocole, finition encore ouverte

- Confirmer visuellement le dernier rendu tablette, les petits écrans,
  le texte à 200 %, la modale, les thèmes et les images dans une même passe.
- Ajouter un test de réponse API **HTTP 200 malformée** : `api.ts`
  considère actuellement le JSON nul comme succès typé ; un objet vide
  de journal peut aussi être traité comme acquittement. Hypothèse issue
  de lecture du code, pas encore reproduite par test. Exiger la forme
  du contrat avant de retirer quoi que ce soit de la file locale.
- Examiner le changement direct de paramètre de route pendant une
  salle montée : besoin éventuel d'une clé de remontage, non testé.
- Harmoniser si nécessaire les noms d'images acceptés : le plugin Vite
  est plus restrictif que le générateur pour points et sous-dossiers.
  Aucun des deux médias actuels n'est touché.
- Mettre à niveau la chaîne de développement de façon bornée : lire
  les avis exacts, choisir des versions corrigées compatibles, garder
  le lockfile et refaire les portes. Ne pas exposer le serveur dev.

### 3. Contrat v2, blocage éditorial mesuré

Le candidat conservé est dans
`/private/tmp/academie-contrat-v2-20260904-revue/rapport-migration.json`.
Ce dossier temporaire peut disparaître ; `app/migre_banque.py --help`
donne les commandes de régénération. Ne pas le promouvoir.

| Mesure du candidat | Nombre |
|---|---:|
| Cartes v1, identifiants conservés | 84 |
| Cartes pilotes v2 déjà présentes | 11 |
| Changements de domaine réellement calculés | 19 |
| Chapitres du candidat | 56 |
| Chapitres nécessitant du contenu | 54 |
| Auteurs structurés manquants | 84 |
| Cartes valides sans relecteur renseigné | 80 |
| Niveaux de carte dépassant le chapitre assigné | 19 |
| Alternatives textuelles d'image manquantes | 4 |

Le rapport comprend 433 messages du valideur, **pas 433 problèmes
indépendants**. Les 21 changements annoncés historiquement dans le
cahier ne sont pas les 19 calculés par la table finalement retenue.
L'assignation est arbitrée ; la provenance et la relecture ne deviennent
pas mécaniques pour autant. Ne pas inventer auteur, modèle, relecteur,
leçon ou baisse de niveau pour obtenir du vert. Aucune carte v1 n'a été
déplacée, supprimée ou renumérotée. La banque servie reste 80 cartes v1,
sans rattachement chapitre ; les 11 pilotes restent brouillons.

Une incohérence éditoriale reste à relire sur
`equipements-vmc-composants-roles` : la vigilance parle d'un schéma
incorrect et d'un brouillon, l'origine d'un schéma corrigé, le statut
est valide. Ce signal ne tranche pas la justesse réelle du dessin.

### 4. Sources et ingestion

Lire les cinq inventaires datés : énergie, travaux, immobilier, cabinet,
culture. Le registre distingue repérage et vérification ; un hôte
repéré n'a pas reçu une date de lecture intégrale fictive. Culture n'a
qu'un N1 dans le programme, pas les cinq demandés par le cahier :
quatre emplacements restent un trou nommé, pas des chapitres inventés.

Trois PDF publics préparés existent localement : `322a2f5e843f45b9`
(32 pages, 20 figures machine), `707940074f138868` (54/53),
`8760dfb3f168df2d` (180/67). Les pivots et états usine existent ; aucune
fiche finale constatée pour ces trois. Le premier est identifié : CAE,
Focus n°106, juin 2024, « Analyse socio-économique de la rénovation
énergétique des logements », Giraudet et Vivier.

État exact à l'arrêt dans `sources/322a2f5e843f45b9.etat.json` :
déclaration Codex/gpt-5.6-sol/grand enregistrée ; unité 1 pages 1–12
déjà validée avant cette session ; unité 2 pages 13–24 ouverte. L'agent
a examiné le texte et ses dix rendus, mais n'a ni modifié le pivot ni
demandé `valider` pour cette unité. Pages 25–32 non parcourues,
aucune fiche créée. Tokens et coût financier exacts indisponibles.

Reprendre avec `python3 app/usine/usine.py suivant 322a2f5e843f45b9`,
puis normaliser les seules pages 13–24 du pivot et décrire les figures
depuis leurs rendus avant de demander le verdict du script. Préserver
les contradictions de la source, notamment mortalité/morbidité dans
le tableau 6a ; ne pas les corriger silencieusement.
Ne pas déclarer les documents lus sur la seule existence d'un pivot.
Le quatrième document interne n'a pas été inspecté ni assimilé à une
autre fiche. Respecter les cloisonnements du cahier ingestion.

### 5. Publication et preuve humaine

Lire la section finale de `web/README.md`. Les cinq tests de préparation
passent avec sources réellement en lecture seule et échec de build
laissant l'ancien index. Ils ne prouvent pas systemd/Linux, les chemins
Node/Python, les dépendances ou permissions du VPS. La distribution est
atomique fichier par fichier, pas comme dossier entier : une erreur E/S
pendant la copie peut laisser des ressources partiellement actualisées.

Avant toute bascule : autorisation de JB, sauvegarde de publication et
d'unité, préflight de la machine, exécution, contrôle authentifié et
retour arrière préparé. `deploy/README.md` est encore à aligner avec la
nouvelle préparation. Ensuite seulement : vraie réponse hors-ligne sur
téléphone, reprise sur Mac dans les deux sens, sept séances ; puis le
rituel de trente séances. Aucun gate humain n'a été inventé.

## Commandes de reprise

Depuis `/Users/jb/Code/academie`, inspecter d'abord `git status` et les
modifications IFSI concurrentes. Ne pas nettoyer le worktree par reset.

```bash
python3 app/tests.py
python3 tooling/check.py
cd web
npm test
npm run build
npm run preview -- --host 127.0.0.1 --port 4173 --strictPort
```

Dans un autre terminal, avec le Chromium actuellement installé sur ce Mac :

```bash
cd /Users/jb/Code/academie/web
CHROMIUM_PATH='/Users/jb/Library/Caches/ms-playwright/chromium_headless_shell-1234/chrome-headless-shell-mac-arm64/chrome-headless-shell' npm run e2e
```

Le preview sert le dernier `dist/` : reconstruire avant de juger une
modification. Relancer la campagne de mutations dans une copie isolée
si d'autres tâches écrivent encore : `app/tests.py --mutation` modifie
temporairement ses sources. `roadmap.py next` ne sélectionne que les
items sûrs automatiques ; une réponse vide ne signifie pas que les
chantiers `agent-review` sont terminés. Recaler leurs statuts sur les
preuves effectives après la reprise, pas sur le volume de code écrit.

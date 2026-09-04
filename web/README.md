# web/ : le client v2

Squelette écrit le 02/09/2026 (`DIRECTION-ARTISTIQUE.md`,
`ARCHITECTURE.md` §1 et §5, `decisions/0007`), initialisé le
03/09/2026. Ce dossier dit quoi construire, écran par écran, et contre
quoi le vérifier. Le chantier est `ACA-FRONT-2`. Le client est **jetable** : il
peut être réécrit sans toucher au moteur, à la banque ni au journal.
Il remplace l'archipel, archivé le 04/09 dans
`archive/client-archipel-2026-09-04` ; rien n'est servi en attendant.

## État au 04/09/2026

L'arbre radial, les branches, la fiche de chapitre, la salle de révision,
la clôture, le profil et la boîte ont leur rendu Nuit/Papier. Les règles
de finition sont dans `AGENTS.md` : Impeccable appliqué dans la DA,
pas une nouvelle direction tirée d'un skill. Lucide est installé ;
Motion, ts-fsrs et game-icons ne le sont pas. Le moteur FSRS reste le
miroir Python décidé dans `decisions/0029`.

La banque, la voix et les images sont injectées depuis leurs sources
au build. Les cartes invalides, périmées ou signalées sont écartées du
service, y compris après minuit dans une salle ouverte. Le journal
attend honnêtement une API indisponible et ne transforme plus une panne
HTTP en rejet de toutes les réponses.

Les tests navigateur couvrent ordinateur et téléphone, Nuit/Papier,
texte agrandi, clavier, réseau coupé, reprise, images et panne de stockage.
Cela ne remplace pas l'essai sur un vrai téléphone ni la preuve de
synchronisation avec le VPS. Le détail actuel et les limites figurent
dans l'[audit](../travail/audit-froid-2026-09-04.md). Les sections datées
du 03/09 ci-dessous sont un état historique, pas le reste à faire actuel.

## Stack prévue (voir l'état actuel ci-dessus)

Vite, React, TypeScript strict, Tailwind (tokens en variables CSS, aucun
hexadécimal dans un composant), Motion pour les animations, `ts-fsrs`
(MIT) pour composer hors-ligne, Dexie (IndexedDB), `vite-plugin-pwa`
(Workbox) pour le hors-ligne et l'installation, un composant de zoom
SVG pour l'arbre, Lucide (ISC) pour les glyphes d'interface, game-icons
(CC BY 3.0, attribution visible dans Crédits) pour les glyphes de
chapitre. Polices auto-hébergées (OFL). Aucun script, aucune police,
aucune image chargée d'un tiers à l'exécution.

Chaque dépendance ajoutée porte sa licence vérifiée à la date dans
`travail/benchmark-2026-08-30.md` partie 4 (on l'étend).

## Arborescence cible

```
web/
  README.md
  index.html
  package.json  vite.config.ts  tsconfig.json  tailwind.config.ts
  public/
    manifest.webmanifest, icônes, polices (OFL)
  src/
    main.tsx                 amorçage, routage, thème
    app/
      routes.tsx             /  /arrivee  /domaine/:cle  /noeud/:id  /salle/*  /profil  /confiance/:domaine  /cercle  /boite  /credits
                             (/cercle est masqué, barre à trois entrées, tant qu'ACA-CERCLE-1 n'est pas livré)
      theme.ts               nuit | papier ; palette par rang de domaine
      i18n.ts                français seulement ; les chaînes vivent ici, pas dans les composants
    moteur/                  la partie du moteur qui doit tourner hors-ligne
      fsrs.ts                enveloppe ts-fsrs, paramètres de academie.json
      journal.ts             écriture locale (Dexie) + file d'envoi + union
      etats.ts               rejoue le journal → état par carte (parité avec app/seance.py)
      progression.ts         remplissage, ouverture, états de nœud et branches (parité avec app/progression.py)
      composeur.ts           séance / domaine / au hasard, semaine type, pondération socle, graine
      points.ts              points de savoir, niveau, titre, calibration (dérivés)
      parite.test.ts         rejoue app/vecteurs_fsrs.py : écart < 1e-4 sinon échec
    donnees/
      banque.ts              chargement de banque.json, cache, version de contrat
      api.ts                 client de serveur/API.md ; hors-ligne : file et reprise
      types.ts               générés depuis contrats/*.schema.json (json-schema-to-typescript)
    ecrans/
      Arbre/                 vue globale, bandeau du jour, bouton Séance
      Domaine/               vue domaine, propositions Réviser / Continuer / Étudier / Épreuve / Au hasard
      Noeud/                 la feuille du nœud, la fiche de rappel
      Salle/                 Seance, Etude, Epreuve, Cloture
      Profil/                carte de visite, heatmap, insignes, bilan, carnet (privé), réglages, export
      Cercle/                Fil, Ligue, Defis, ProfilAutre       (après le gate)
      Boite/                 dépôt et file
      Credits/               licences et méthode
    composants/
      Arbre/                 Noeud, Lien, Brouillard, Canopee, Tronc, Satellite
      Carte/                 Entete, Corps, ZoneReponse, Retour, LigneSource, FeuilleSource
      Exercices/             Flash, Qcm, Photo, Relier, Datation, Plan, Cas, Libre, Role, Dessin, FeuilleBlanche, Synthese, Lecture
      Ui/                    Bouton, Feuille, Anneau, Pastille, Jauge, Heatmap, Citation
    contenu/
      citations.ts           banque de citations sourcées (auteur, œuvre, date)
      textes.ts              micro-textes (clôture, erreur, jalons), ton de DIRECTION-ARTISTIQUE §8
  tests/
    e2e/                     Playwright : première question < 3 s hors-ligne, séance de bout en bout, export
```

## Ce que le client doit prouver avant d'être servi

1. **Parité** : `parite.test.ts` vert contre les vecteurs Python.
2. **Hors-ligne** : réseau coupé, la séance du jour se compose et se
   joue ; les réponses partent quand le réseau revient ; aucune perte.
3. **Ouverture** : première question en moins de trois secondes sur un
   téléphone de milieu de gamme (mesure Lighthouse mobile en CI).
4. **Aucun import** de labor, aucune requête vers un tiers (test qui
   liste les hôtes contactés).
5. **Accessibilité** : la checklist de `DIRECTION-ARTISTIQUE.md` §9.
6. **Contrat** : le client refuse un `banque.json` dont `contrat` est
   inconnu et le dit à l'écran ; un `banque.json` sans champ `contrat`
   (publié avant ACA-CONTRAT-2) est lu comme `carte-v1`.

## Ce que le client ne fait jamais

Appeler un modèle avec une clé embarquée ; envoyer une source ; calculer
un score qu'il stocke ; afficher l'état d'un autre joueur sans la
visibilité accordée ; envoyer un mail.

## État au 03/09/2026

Le squelette technique est posé et vert. La **fondation** de la couche
visuelle l'est aussi depuis le soir du 03/09 (polices, tokens, mouvement,
mots, clavier) ; ce qui la surmonte (l'arbre, les anneaux, la
personnalité des cartes) n'est pas fait, et les écrans restent nus.

### Ce qui existe

- Vite 5, React 18, TypeScript strict, Tailwind avec les tokens en
  variables CSS (`src/index.css` est le seul fichier qui porte des
  hexadécimaux, et `tests/e2e/direction-artistique.spec.ts` le vérifie
  dans le CSS servi, pas dans les sources).
- Deux polices auto-hébergées, OFL, sous-ensemble latin seulement :
  Fraunces (titres) et Source Sans 3 (texte, chiffres tabulaires),
  65 ko à elles deux, précachées avec le reste.
- `src/moteur/` : `fsrs.ts` (miroir écrit à la main de
  `app/planificateur.py`), `etats.ts` (rejeu du journal, y compris
  `stabilite_forcee`), `progression.ts`, `composeur.ts`, `points.ts`,
  `journal.ts` (Dexie, file d'envoi, union sur `quand|mode|nonce`).
- `src/donnees/` : chargement de la banque avec cache Dexie et refus
  d'un contrat inconnu, client d'API, types transcrits des contrats.
- `src/app/` : routage sur le fragment, thème Nuit et Papier, palette
  par rang de domaine, `i18n.ts` (le seul fichier qui porte des chaînes
  d'interface ; la voix vient de `contenu/voix.json`).
- Neuf écrans nus : Arbre, Domaine, Nœud, Séance, Clôture, Profil,
  Boîte, Crédits, Confiance, plus la barre.
- La banque et la voix ne sont **pas** copiées dans `public/`. Un plugin
  Vite (`vite.config.ts`, `academie-donnees-du-depot`) lit
  `../site/banque.json` et `../contenu/voix.json`, les sert en
  développement et les écrit dans `dist/` au build. Une copie dans
  `web/` divergerait, et ces deux fichiers portent des caractères que
  `tooling/check.py` n'accepte qu'à leur place d'origine.
- PWA : `vite-plugin-pwa` 0.21.1, manifeste, précache de la banque, de
  la voix, du JS, du CSS et des polices à venir ; la banque et la voix
  sont aussi en `StaleWhileRevalidate` à l'exécution.
- Cinq tests verts, 159 cas : `src/moteur/parite.test.ts` lance
  `python3 app/vecteurs_fsrs.py --json` et compare stabilité,
  difficulté, intervalle et récupérabilité à 1e-4 sur chaque étape de
  chaque séquence ; `tests/hotes.test.ts` vérifie qu'aucune URL de
  `src/` ni de `index.html` ne sort de localhost et que la CSP tient ;
  `tests/voix.test.ts` vérifie que chaque clé affichée existe dans
  `contenu/voix.json` avec trois variantes et les mêmes variables ;
  `src/moteur/parite-arbre.test.ts` (ACA-ARBRE-1) lance
  `python3 app/vecteurs_progression.py --json` et exige l'égalité
  **stricte** des états de nœud, des branches et des drapeaux de
  fraîcheur sur dix scènes, dont les deux pièges de `decisions/0028` :
  un nœud validé qui le reste quand on lui ajoute des cartes, et un
  nœud mûr revu il y a trente jours qui n'est pas « à revoir » ;
  `src/moteur/parite-semaine.test.ts` (ACA-SEMAINE-1) compare la couleur
  du jour, le quota de neuf et la branche du socle visée. Le tirage,
  lui, n'est pas comparé : Python tire avec Mersenne Twister, le client
  avec un mulberry32, et comparer l'ordre ferait un test du générateur
  plutôt que du produit. Depuis le 03/09 au soir, ce fichier compare
  aussi la **composition elle-même** sur cinq scènes (couleur du jour,
  cap, branche du socle, nombre de révisions, de neuf, de rappels
  d'ailleurs, arriéré). C'est ce qui manquait : les règles étaient
  comparées une par une, leur emploi dans `compose()` ne l'était pas.
- `LICENCES.md` : chaque dépendance, version exacte, licence.

### La couche visuelle : la fondation est posée (03/09 au soir)

La `DIRECTION-ARTISTIQUE.md` n'est pas appliquée en entier : les écrans
n'ont ni arbre en SVG, ni anneaux, ni feuilles qui montent, ni
personnalité par type de carte. Mais sa **fondation** l'est, et c'est
elle qui décide de tout le reste :

- **Les deux polices, auto-hébergées** (DA §2) : Fraunces pour les
  titres, Source Sans 3 pour le texte et les chiffres tabulaires, OFL
  toutes les deux. Sous-ensemble `latin` seulement, deux fichiers,
  65 ko ; `src/polices.css` dit pourquoi. Rien n'est chargé d'un tiers.
- **Les tokens en entier** : le brouillard, l'ombre unique des surfaces
  qui flottent, le grain de papier (désactivable par
  `data-grain="non"`), les marges 16/24, les trois durées et la courbe
  du §6, et la palette de domaine **assombrie** en Papier pour tenir le
  contraste AA du §7.
- **Le mouvement du §6, et lui seul.** Le blocage général des
  animations du matin est levé ; à sa place, une politique : l'état
  pressé d'un bouton (98 %, 120 ms, §8 ter), aucune animation
  d'entrée, et `prefers-reduced-motion` qui ramène tout à des fondus de
  120 ms. Rien d'autre ne bouge parce que rien d'autre n'existe encore.
- **Les mots du §8** : les libellés portent leurs accents, et les
  quatre notes FSRS sont celles de la DA (À revoir, Difficile, Bien,
  Évident) au lieu des mots du moteur.
- **Le clavier du §8 ter** : Espace révèle, 1 à 4 notent, Échap sort.
  « La souris n'est jamais nécessaire dans une salle » est une promesse
  d'accessibilité, pas un confort ; elle est tenue avant les jolis
  écrans.
- **La ligne de source et de provenance du §5** : la note de confiance
  en lettre, la nature de chaque source, et « Généré par … · N sources
  concordantes · relu le … » construite sur les vrais champs du contrat
  v2, que `genere.py` publie depuis ce soir.

Ce qui reste de la couche visuelle : l'arbre (§3), la personnalité par
type de carte (§5), les célébrations de clôture (§6), les glyphes
(Lucide, game-icons) et le bento du profil (§8 ter). Rien du moteur n'a
besoin d'être touché pour les faire.

### Ce qui reste ailleurs

- **ACA-CONTRAT-2.** Le client sait refuser un contrat inconnu et lire
  une banque sans champ `contrat` comme `carte-v1`, mais la banque
  publiée est encore une v1 sans le champ ; les types de `carte-v2` sont
  transcrits, pas exercés.
- ~~**Les tests de bout en bout.**~~ Faits le 03/09 au soir :
  `tests/e2e/hors-ligne.spec.ts`, quatre preuves sur deux tailles
  d'écran (375 et 1280). Mesuré : **première question en 530 ms réseau
  coupé**, budget 3 000 ms ; une séance jouée hors-ligne s'écrit dans
  IndexedDB avec sa ligne d'ouverture et attend en file ; au retour du
  réseau la file part en entier vers `POST /journal` et se vide ; aucun
  hôte tiers n'est contacté.

  Ils tournent sur le **vrai build** servi par `vite preview` : sans
  service worker, « hors-ligne » ne voudrait rien dire.

  ```bash
  npm run e2e              # les deux tailles d'écran
  npm run e2e:telephone    # 375 px seulement
  ```

  Depuis le 03/09 au soir s'y ajoute `tests/e2e/direction-artistique.spec.ts`,
  qui prend la moitié **mesurable** de la checklist §9 : aucun
  hexadécimal hors des tokens dans le CSS servi, rien qui déborde à 375,
  à 1280 ni à 200 % de texte, les deux thèmes rendus, le mouvement
  réduit respecté, le clavier de bout en bout dans une salle, le focus
  visible. Vingt cas sur deux tailles d'écran. L'autre moitié de la
  checklist est du jugement et n'a rien à faire dans un test.

  Ils ne sont **pas** dans `npm test` ni dans la porte du dépôt : ils
  demandent un navigateur et un build, la CI n'installe ni l'un ni
  l'autre. Le chemin de Chromium se règle par `CHROMIUM_PATH` ; à
  défaut, `/opt/pw-browsers/chromium`.
- **La bascule** : build dans la publication, `client/` archivé,
  `tooling/check.py` débarrassé des marqueurs de l'archipel, et JB qui
  joue sept séances.
- Étude et épreuve complètes (ACA-ETUDE-1, ACA-EXAMEN-1), Cercle
  (ACA-CERCLE-1) : masqués, les boutons disent « bientôt ».

### Comment lancer

```bash
cd web
npm install
npm run dev      # http://localhost:5173/academie/
npm test         # parité, hôtes, voix
npm run build    # tsc --noEmit puis vite build vers dist/
npm run preview  # sert dist/ pour vérifier la PWA
```

Depuis la racine du dépôt, la porte reste la même :

```bash
python3 app/tests.py && python3 tooling/check.py
```

À savoir : `tooling/check.py` parcourt tout `web/` et ignore
`node_modules`, `dist` et `dev-dist`. Un `npm run build` ne fait donc
plus sortir la porte en erreur sur les tirets cadratins de
`web/dist/banque.json`.

Le développement a besoin de `../site/banque.json` et de
`../contenu/voix.json` : le client se lance depuis le dépôt, pas depuis
une copie isolée de `web/`.

### Préparation de la publication

Le script `preparer-publication.mjs` prépare le client complet, et pas
seulement `banque.json`. Sa présence dans le dépôt ne prouve pas que le
service correspondant a été installé ou exécuté sur le VPS.

Prérequis : Node 20 ou plus, Python 3.12, et les dépendances de construction
installées par `npm ci --include=dev` dans `web/`. Leur installation est
une opération préalable : le service ne lance ni `npm install` ni un
téléchargement. Il faut notamment TypeScript, Vite et le générateur PWA.
Les chemins de Node et Python du service sont `/usr/bin/node` et
`/usr/bin/python3` ; ils doivent être vérifiés sur la machine cible avant
toute activation humaine.

Pour préparer seulement une sortie locale jetable, depuis le dépôt :

```bash
node web/preparer-publication.mjs --sortie /tmp/academie-publication-locale
cd web
npm run test:publication
```

La préparation utilise un dossier de travail hors du dépôt, choisi avec
`--travail` ou, par défaut, le dossier temporaire du système. Elle copie
les sources du client et les seules familles de données nécessaires
(`academie.json`, `banque/`, `chapitres/`, `programme/`, `contenu/voix.json`).
Les tests TypeScript font partie de la copie car `tsconfig.json` les
inclut. Les dépendances installées sont consultées par lien, sans copie
ni écriture. Aucun état joueur n'entre dans la construction.

Le générateur tourne avec `--couches banque` et `-B`, puis TypeScript et
Vite construisent dans ce dossier temporaire. Cela fonctionne avec les
sources en lecture seule : Vite peut y écrire sa configuration compilée
et Python peut recopier une image partagée sans modifier le dépôt.

Avant de changer la destination, le script contrôle l'inventaire SHA-256
complet, les fichiers indispensables à la PWA, les références du
manifeste Vite et toutes les images des cartes publiées. Un échec de
génération, de build ou de contrôle laisse la publication existante
intacte. Les ressources passent ensuite avant `index.html`, remplacé par
renommage atomique ; `sw.js` vient en dernier. Les anciens assets hachés
restent disponibles pour les onglets encore ouverts. Ce n'est pas un
remplacement atomique de tout le dossier : une erreur d'E/S pendant la
distribution peut laisser une partie des ressources actualisée.

Le service préparé dans `deploy/academie-publication.service` conserve
`ProtectSystem=strict` et crée son atelier sous
`/run/academie-publication`. Seuls cet atelier et la destination
`/var/lib/academie/publication` sont déclarés inscriptibles. L'installation
du service, sa relance, l'archivage de `client/` et toute bascule du VPS
restent soumis à validation humaine.

Retour arrière à préparer avant une bascule : conserver une copie
complète de la publication précédente et de l'unité systemd installée.
Un humain suspend le timer, rétablit les ressources sauvegardées avant
l'ancien `index.html`, puis l'ancien `sw.js`, et remet l'unité précédente.
Il vérifie ensuite l'ouverture en ligne et hors ligne avant de réactiver
le timer. Le script n'efface ni anciens assets ni sauvegardes ; leur
nettoyage est une opération distincte, jamais implicite.

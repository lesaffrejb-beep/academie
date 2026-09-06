# Graphe des prérequis, 06/09/2026

Outil : Codex ; modèle : GPT-6. Périmètre autorisé : reprise du graphe
demandée par JB, cahier `chantiers/ACA-FRONT-2.md` amendé avant code.

## Résultat observable

Dans Arbre, le bouton visible « Graphe des prérequis » ouvre un index de
tous les chapitres du cursus chargé, avec recherche sans distinction
d'accents, domaine et branche. L'index affiche trente résultats à la fois
et une commande pour poursuivre. La sélection dessine son voisinage :
prérequis, chapitre, suites directes. Les références manquantes restent
nommées comme absentes ; un lien pointillé indique un autre domaine.

Le graphe précédent existe toujours dans `GrapheSavoir.tsx` pour les vues
qui l'importent, mais sa vue radiale n'est plus branchée depuis Arbre.
Elle reliait la hiérarchie et non les prérequis, proposait des cibles SVG
sans activation clavier et assimilait certains comptes de branches à des
comptes de cartes. L'index Domaines antérieur reste utilisable.

Les états du nouveau graphe viennent des nœuds du moteur. Un chapitre sans
carte affiche « Au programme », sans pourcentage. Les boutons de révision
comptent les cartes encore serviables ; les études passent par
`etudeDisponible`. Une étude parcourue n'est pas une compétence démontrée.

## Preuves exécutées

- Avant projection : Vitest échoue car `moteur/graphe` n'existe pas.
- Avant branchement : E2E échoue en attendant le bouton « Graphe des
  prérequis » absent (20 s). Le premier lancement a rencontré l'interdiction
  des sockets du sandbox ; la relance autorisée a produit le rouge attendu.
- Projection : 3 tests unitaires verts, orientation exacte, interdomaines,
  références manquantes, conservation des états et filtrage du programme reçu.
- Navigateur : `CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' npm --prefix web run e2e -- graphe.spec.ts atlas.spec.ts`
  produit **14 tests verts** le 06/09 à 18:33 heure de Paris, en 19,5 s.
  Les deux projets éprouvent 375 et 1280 px, clavier Entrée/Espace,
  recherche et filtres, cursus IFSI séparé du copro, ouverture d'une vraie
  étude, chapitre vide, deux thèmes et texte à 200 %, sans débordement de page.
- Build TypeScript/Vite inclus dans la preuve navigateur : vert.
- Détecteur Impeccable sur les trois fichiers UI modifiés : tableau vide.
- Inspection groupée des captures ordinateur et téléphone, puis correction
  des liens mobiles et de la hiérarchie des actions. Confirmation visuelle
  finale conservée dans les quatre PNG de ce dossier.

La première passe navigateur a attrapé une mauvaise route du bouton Étudier
(qui revenait à l'accueil). Elle est corrigée vers `/salle/etude/<id>` et
le test exige maintenant le champ de première réponse de l'étude ouverte.
Sur mobile, les connexions passent sur les côtés des cibles, pour éviter
qu'un lien traversant les cases fasse croire à une relation entre frères.

Les tests de contenu emploient le profil fictif `e2e-copro` / `e2e-ifsi`.
L'API de journal était absente pendant ce test graphique : les traces
ECONNREFUSED sont conservées dans la sortie du test. Cette preuve porte
sur le front et ne prouve ni synchronisation VPS, ni compte réel, ni
acceptation esthétique ou essai sur un appareil physique.

## Fichiers de cette passe

- `web/src/ecrans/Arbre.tsx`
- `web/src/ecrans/GraphePrerequis.tsx`
- `web/src/ecrans/graphePrerequis.css`
- `web/src/moteur/graphe.ts`
- `web/src/moteur/graphe.test.ts`
- `web/tests/e2e/graphe.spec.ts`
- extension du cahier et ce dossier de preuves.

Aucune dépendance, nouvelle mécanique pédagogique ou donnée joueur ajoutée.
`METHODE.md` §11 reste la règle existante d'orientation dans le programme.
Le relevé Impeccable `.impeccable/design.json` est signalé plus ancien que
DESIGN.md ; cette passe conserve les tokens CSS actuels et ne réécrit pas
le relevé historique.

## Relecture indépendante et contrôles finaux

L'agent `/root/acces_profils` a relevé un libellé contradictoire lorsque tous
les prérequis référencés sont absents : « Aucun prérequis déclaré » côtoyait
leur liste. Test SSR ajouté et constaté rouge avant correction ; le texte
dit maintenant « Aucun prérequis disponible dans ce programme » dans ce cas.
La référence absente reste affichée. Aucun autre défaut remonté par cette
relecture sur les liens, le cursus ou le contrôle des études.

`python3 app/tests.py` a terminé TOUT VERT après relance autorisée pour les
sockets localhost. Le contrôle global `tooling/check.py` avait rencontré
le mot interdit d'un test ModulesSeance en cours d'écriture par l'autre
agent ; ce mot a ensuite été corrigé par son auteur. Le coordinateur
exécute la porte finale sur le lot intégré avant publication.

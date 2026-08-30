# academie — L'Académie, l'apprentissage du matin

Chantier posé le 28/08/2026 (brief dicté de JB : « 15 minutes
d'apprentissage tous les matins avant le boulot, cadre l'idée, imagine
le produit mais ne le construis pas encore ») ; renommé « L'Académie »
et enrichi des ateliers le même jour (second brief JB). Le nom est
« pour l'instant » : s'il change encore, le dossier suit.

**L'Académie** est l'école du matin du gestionnaire : chaque matin vers
8h15, avant le travail, une séance de ~15 minutes qui rend JB meilleur
professionnel — cartes à répétition espacée (FSRS) sur la pathologie du
bâtiment, le droit, la comptabilité, la procédure, la technique des
équipements ; et des ateliers de lecture et d'analyse (un arrêt de
cassation avec sa méthode de lecture, un vrai devis du portefeuille à
auditer, une annexe comptable, un texte de fond « comme au bac »),
alimentés par son travail réel de la veille.

## La chaîne : d'une donnée brute à l'écran du matin

```
  banque/<domaine>/<branche>.json      la donnée brute, versionnée
        │                              une carte = source + date + statut + couche
        ▼
  app/valide_banque.py                 LE FILTRE — refuse et n'écrit rien si :
        │                              pas de source ou pas de date de vérification,
        │                              QCM sans distracteur expliqué, image sans licence,
        │                              id dupliqué, prérequis fantôme, carte périmée,
        │                              nom de copropriété réelle en couche partagée
        ▼
  app/genere.py                        le tri de sortie : --production ne sert que
        │                              les cartes `valide`, --couches filtre ce qui
        │                              a le droit de circuler (banque / interne / perso)
        ▼
  app/seance.py  ◄── etat/<profil>/revues.jsonl     FSRS décide de ce qui revient
        │                              (journal append-only, l'état se RECALCULE)
        ▼
  un client autorisé       le pont vers le front
                                       ← MAILLON CASSÉ au 29/08 : import
                                       de build, pas un fetch (O1a de
                                       SPEC-PRODUIT §7, priorité absolue)
        │
        ▼
  l'écran                              avec le statut affiché : une carte non
                                       vérifiée se présente comme telle
```

**Tout vérifier en une commande** (inclus dans `tooling/examen.py`) :

```bash
python3 app/tests.py
```

Six étages : le moteur FSRS (comparé à `py-fsrs`), la composition de
séance, la carte-monde (`app/progression.py` : régions, seuils,
boss-examens, XP dérivée — GO socle du 29/08), le quiz de
positionnement + le carnet d'erreurs (`app/quiz.py`,
`app/erreurs.py`), la chaîne donnée → écran, et la validation de la
banque réelle. La coquille d'un nouveau domaine (modèle A4) vit dans
[`gabarit-domaine/`](gabarit-domaine/README.md).

**Vérifier que les tests mordent vraiment** :

```bash
python3 app/tests.py --mutation
```

Casse huit garde-fous un par un et vérifie qu'un test s'en aperçoit. Un
test qui reste vert pendant que le code est cassé donne confiance à
tort : ce mode a trouvé, le 28/08/2026, que la vérification des champs
obligatoires n'était couverte par aucun cas.

---

Les documents :

- [`BLUEPRINT.md`](BLUEPRINT.md) — le produit imaginé : vision, socle
  scientifique sourcé, modes d'exercice, ateliers, arbres de
  compétence, architecture technique, généralisation à d'autres
  métiers. **À lire en premier.**
- [`ROADMAP.md`](ROADMAP.md) — les chantiers M0 à M11 (+ M1-bis), dans l'ordre,
  chacun avec son « fini quand », et le risque numéro un (le rituel
  qui ne tient pas) traité en tête.
- [`CADRAGE-SCIENTIFIQUE.md`](CADRAGE-SCIENTIFIQUE.md) — cadrage
  neuroscientifique et sciences cognitives d'un système d'apprentissage
  quotidien d'élite : les 7 lois fondamentales, tableau comparatif des
  stratégies, architecture chronométrée de la séance de 15 min, matrice
  de transposition par matière et bibliographie complète.
- [`CORPUS.md`](CORPUS.md) — le contrat wiki → banque (28/08/2026) :
  routage par type de matière (faits, images, news, articles, études,
  sources), inventaire du gisement réel du repo (~100-120 cartes
  extractibles, trous nommés), références scientifiques du BLUEPRINT
  re-sourcées et vérifiées.
- [`DESIGN.md`](DESIGN.md) — charte & architecture Design System de l'interface React : tokens stricts, règles ergonomiques, micro-interactions et checklist de contribution.
- [`CONTRAT-CARTE-V1.md`](CONTRAT-CARTE-V1.md) — le format d'une carte,
  engagé et opposable : champs obligatoires, les trois couches de
  partage, la péremption, l'export Anki. Le valideur en est
  l'application mécanique et **fait foi** en cas de divergence.
- [`CADRAGE-PRODUIT.md`](CADRAGE-PRODUIT.md) — le questionnaire du
  produit autonome (52 questions), **répondu le 29/08/2026** avec
  Arthur (Partie 4 : réponses + arbitrages).
- [`SPEC-PRODUIT.md`](SPEC-PRODUIT.md) — l'architecture arrêtée du
  produit autonome (modèle A4 : un repo source par joueur, usine
  locale, serveur de jeu VPS ; carte-monde, boss, quiz de
  positionnement, carnet d'erreurs) et le **plan des sessions Opus**
  (§7). Fait foi sur les briques de M9-M11.
- [`METHODE.md`](METHODE.md) — la pédagogie lisible par tous : une
  entrée par mécanique (ce qu'on fait / pourquoi / la source datée).
  Une mécanique sans entrée n'entre pas dans le produit.
- [`IDEES-EN-VOL.md`](IDEES-EN-VOL.md) — le registre append-only des
  idées de JB lancées en route : gravée / différée / à creuser /
  écartée, avec le pointeur. Rien ne se perd.
- [`gabarit-domaine/DESSINER-LA-CARTE.md`](gabarit-domaine/DESSINER-LA-CARTE.md)
  — la méthode réutilisable pour cartographier un nouveau métier
  (régions, lieu-monde, difficulté, tri des sources, coûts mesurés).
- Ce README — la porte d'entrée.

Le pré-mortem du cadrage (agent frais, protocole
`.agents/skills/erp-complete/references/pre-mortem.md` adapté) est dans
`travail/relecture-2026-08-28-cadrage.md`.

Règles héritées du repo qui s'appliquent ici sans exception : aucune
donnée copro nommée dans la banque de cartes partagée (anti-pollution,
AGENTS.md) — les ateliers sur pièces réelles vivent dans la couche
personnelle ; toute carte porte sa source et sa date de vérification
(règle dure 3 étendue) ; markdown + git, jamais de SaaS propriétaire
(doctrine ERP, « on vole les patterns des géants, jamais leurs
plateformes »).

Statut (30/08/2026) : **l'espace de jeu est jouable et déployé sur le
VPS** — depuis l'ERP, un clic sur L'Académie ouvre l'archipel plein
écran (O1a fetch runtime et O1b journal auto-save : faits ; les 7
types de cartes se jouent ; banque copro 80 valide / 4 brouillon
après double passe Légifrance ; domaine test `domaines/arthur-ifsi`
40 cartes). Les choix sont documentés : SPEC-PRODUIT (les décisions),
METHODE (la pédagogie sourcée), `DESIGN.md`
§2bis-2ter (la peau de l'espace de jeu et ses pièges techniques),
`travail/benchmark-2026-08-30.md` (ce qu'on a volé et sous quelle
licence), CREDITS des icônes affichés dans l'app. Prochains gestes :
le rituel réel de JB (c'est lui le gate de tout), O2 (remplir les 5
îles vides), la couleur d'île qui descend dans les exercices, puis le
lieu-monde immeuble (v1.1).

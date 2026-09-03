# CONTRAT carte-v1 — le format d'une carte de l'Académie

Écrit le 28/08/2026 (chantier M1), après les arbitrages de JB. Ce
fichier est un **contrat** : il engage le format, pas une intention.
Le valideur [`app/valide_banque.py`](app/valide_banque.py) en est
l'application mécanique — quand les deux divergent, **le valideur fait
foi** et ce document se corrige.

Leçon appliquée d'avance : le contrat `batiment-v1` a dérivé faute de
valideur (constaté le 26/08/2026). Ici le valideur naît **avec** le
contrat, avant la première carte.

---

## 1. Trois décisions de format, et pourquoi

**JSON, pas YAML+md** (écart assumé au BLUEPRINT §10, qui disait
« un bloc YAML+md »). Trois consommateurs veulent lire une carte : le
valideur Python, le front React, l'export Anki. Le JSON est parsable
par les trois en stdlib, sans dépendance et sans ambiguïté
d'indentation. Le repo fait déjà ce choix pour ses données
structurées (`batiment.json`, `majorites-ag.json`, `parc-v1`). Le
markdown reste pour la prose (fiches de méthode d'atelier).
Contre-argument écarté : « le JSON est pénible à écrire à la main » —
les cartes sont produites par agent et relues **en HTML**, jamais dans
leur format de stockage (doctrine CLAUDE.md : on ne fait pas relire du
brut à JB).

**Un fichier par branche**, pas un par carte :
`banque/<domaine>/<branche>.json` contenant un tableau de cartes. 80
fichiers pour M1 seraient déjà ingérables, et une branche est l'unité
naturelle de révision. Le diff reste lisible (une carte = un bloc).

**L'id ne change jamais.** Il est la clé de tout l'historique FSRS
(`etat/<profil>/revues.jsonl`). Renommer un id, c'est effacer la
mémoire de la carte. Une carte fausse se corrige ou se retire ; elle
ne se renumérote pas.

## 2. Le schéma

```json
{
  "id": "droit-majorites-passerelle-25-1",
  "domaine": "droit",
  "branche": "majorites",
  "niveau": 1,
  "prerequis": ["droit-majorites-article-25"],

  "type": "qcm",
  "question": "Un projet relevant de l'article 25 est refusé…",
  "reponse": "Au moins le tiers des voix de tous les copropriétaires.",
  "choix": [
    {"texte": "Le tiers des voix de tous les copropriétaires",
     "correct": true},
    {"texte": "La moitié des présents et représentés",
     "correct": false,
     "pourquoi_faux": "C'est la majorité de l'article 24, celle du second vote, pas le seuil qui l'ouvre."}
  ],
  "explication": "Le seuil se calcule sur TOUS les copropriétaires…",
  "vigilance": "Le second vote a lieu immédiatement, en séance.",

  "source": [
    {"texte": "Art. 25-1 loi du 10 juillet 1965",
     "url": "https://www.legifrance.gouv.fr/…"}
  ],
  "verifie": "2026-08-28",
  "peremption": null,
  "statut": "valide",
  "origine": "templates/majorites-ag.md",
  "partage": "banque"
}
```

### Champs obligatoires, toujours

| Champ | Règle |
|---|---|
| `id` | kebab-case, unique dans TOUTE la banque, immuable |
| `domaine` | une clé déclarée dans `academie.json` (les 8 de BLUEPRINT §9) |
| `branche` | kebab-case, libre dans le domaine |
| `type` | `flash` \| `qcm` \| `photo` \| `relier` \| `datation` \| `libre` \| `role` \| `plan` |
| `question` | non vide |
| `reponse` | non vide |
| `source` | **au moins une entrée** avec `texte` non vide (règle dure 3) |
| `verifie` | date `AAAA-MM-JJ` de la vérification à la source |
| `statut` | `brouillon` \| `valide` \| `signale` \| `perime` |
| `partage` | `banque` \| `interne` \| `perso` — voir §2 bis |

### Champs conditionnels

- `choix` : obligatoire si `type: qcm` — au moins 3 entrées, **exactement
  une** `correct: true`. Chaque entrée fausse porte `pourquoi_faux` :
  un QCM sans explication des distracteurs n'apprend rien.
- `image` : obligatoire si `type` vaut `photo`, `relier`, `datation` ou
  `plan`. Toujours `{fichier, licence, credit, source}` — **une image
  sans licence n'entre pas** (BLUEPRINT §7, droit des sources).
- `etapes` : optionnel, pour `type: datation` — la liste ordonnée des
  étapes DANS LE BON ORDRE (le front les mélange pour le jeu
  d'ordonnancement). Sans ce champ, une carte `datation` se joue en
  lecture guidée de son image, jamais en ordonnancement inventé
  depuis la prose (ajout du 30/08/2026, demandé par le rendu des
  types : deviner l'ordre en découpant une phrase produit un exercice
  faux).
- `paires` : optionnel, pour `type: relier` — la liste des paires
  `{element, cible}` structurées ; lue en priorité sur le parsing de
  la prose (même ajout du 30/08/2026).
- `prerequis` : liste d'ids existants ; sert au déblocage de l'arbre (§9).
- `niveau` : entier 1 à 3, défaut 1.

### `partage` : trois couches, parce que la source commande la diffusion

Ajouté le 28/08/2026, quand JB a signalé le portail de formations de
l'employeur (Immocampus, CORPUS §2.5). Deux couches ne suffisaient
plus : une carte tirée de Légifrance et une carte paraphrasée d'un
support interne n'ont pas le même droit de circuler.

| Valeur | Source admise | Diffusion possible |
|---|---|---|
| `banque` | publique (Légifrance, AQC, ADEME, Wikimedia) | tout le monde, y compris un autre métier (BLUEPRINT §10-M10) |
| `interne` | paraphrase d'un support employeur | JB et ses collègues Sergic — **jamais** une distribution externe |
| `perso` | pièce réelle du portefeuille, photo VT non anonymisée | le propriétaire du profil seul |

La règle qui rend ça sûr : le générateur de distribution filtre **par
couche**, pas par relecture. Une distribution externe ne sert que
`banque` ; il n'y a pas de jugement humain à refaire à chaque publication.

Le scan anti-fuite s'applique à `banque` **et** à `interne` : même
entre collègues, une carte pédagogique n'a jamais besoin du nom d'une
copropriété réelle. Seul `perso` y échappe, par construction.

### `peremption` : le champ que le blueprint n'avait pas

`peremption: "AAAA-MM-JJ"` ou `null`. **Obligatoire dès que la carte
porte un chiffre qui bouge** (prix de l'énergie, plafond d'aide, seuil
indexé). Passé la date, le valideur bascule la carte en `perime` et
elle **sort de la rotation toute seule**.

Pourquoi ce champ existe : l'inventaire du 28/08/2026 (CORPUS §2) a
trouvé `energie-socle.md` vérifié le 02/07/2026 et déjà périmé (les
révisions CRE sont passées). Sans ce champ, ces cartes-là auraient
enseigné des prix faux en silence — précisément le « il ne faut pas me
dire de bêtises » du brief. La règle dure 3 du repo dit qu'un chiffre
porte sa date ; ici on ajoute qu'il porte sa **date de mort**.

## 3. Les invariants que le valideur fait respecter

1. **Aucune carte sans source ni date de vérification.** Règle dure 3,
   mécanisée. Pas de dérogation, pas de `[À VÉRIFIER]` en banque.
2. **Aucun fait copro nommé dans une carte `partage: banque`.** Scanner
   anti-fuite de même nature que la capacité bornée d'ERP : slugs `OFF-*`,
   immatriculations, ICS, et les noms réels du parc. Une correspondance
   et le valideur refuse — rien n'est écrit. C'est ce qui rendra la
   distribution M9 sûre par construction, pas par relecture.
3. **Une carte LLM naît `brouillon`.** Seule une double passe à la
   source la fait passer `valide`. Le générateur ne sert que les cartes
   `valide` — c'est son comportement **par défaut**, pas une option :
   servir du non-recoupé demande `--avec-brouillons`, explicitement, et
   le statut voyage alors jusqu'au front qui doit l'afficher. (Le défaut
   était inverse jusqu'au 28/08/2026 ; corrigé, et verrouillé par un
   test qui échoue si le défaut redevient permissif.)
4. **`signale` sort immédiatement de la rotation.** Le bouton « cette
   carte est fausse » écrit ce statut ; la correction est un chantier
   d'agent, pas une urgence de séance.
5. **Un id dupliqué casse la validation.** Deux cartes partageant un id
   corrompent l'historique FSRS des deux.
6. **Un prérequis inexistant casse la validation.** L'arbre ne doit pas
   pointer dans le vide.

## 4. L'export Anki (l'assurance-vie)

`app/export_anki.py` (écrit le 03/09/2026, chantier `ACA-EXPORT-1`)
produit un paquet lisible par Anki (`.apkg` via `genanki`, MIT, lue à
la source le 03/09/2026) depuis n'importe quel sous-ensemble de la
banque. Trois champs : `Recto` (la question), `Verso` (la réponse,
explication et vigilance incluses, plus les distracteurs d'un QCM avec
leur `pourquoi_faux`), `Source` (les sources avec leur nature et leur
parti, l'URL, la date de vérification, et le statut quand la carte
n'est pas `valide`). Étiquettes : `domaine::branche`, plus
`chapitre::<id>` et `statut::<statut>` quand ils s'appliquent.

Par défaut, seule la couche `banque` et les cartes `valide` partent ;
`--couches` et `--avec-brouillons` sont explicites. Le `guid` d'une
note est dérivé de l'identifiant de carte : réimporter un export mis à
jour remplace la note, il n'en crée pas une deuxième.

Ce qui ne part pas : **les images**. Les cartes `photo`, `relier`,
`datation` et `plan` sortent avec leur texte seul, parce que les images
de la banque ont des licences par fichier (`decisions/0017`) et qu'un
paquet parti chez un tiers ne les respecte pas par construction. La
question se rouvrira si le besoin se présente.

`genanki` est une dépendance d'**usine**, jamais du produit joué :
elle vit dans `tooling/requirements-usine.txt`, le moteur ne la charge
pas, et `app/tests_export.py` passe sans elle (la mise en forme est de
la stdlib pure ; seul l'empaquetage est sauté, et le dit).

Contrat de réversibilité du BLUEPRINT §2 : si l'app maison s'arrête, le
contenu se joue ailleurs le lendemain. L'inverse n'est pas vrai et
c'est assumé : Anki ne saura pas rejouer les ateliers ni la boucle
terrain.

## 5. Indépendance du métier (BLUEPRINT §11)

Rien dans ce contrat ne connaît la copropriété. Les domaines, leurs
libellés et les quotas vivent dans `academie.json` ; `app/` n'écrit
jamais « copro », « Sergic » ni un prénom en dur (même règle que pour
les skills). Donner l'Académie à un autre métier = une autre banque et
une autre config.

## 6. Ce qui reste hors contrat pour l'instant

Les **ateliers** (BLUEPRINT §6) ne sont pas des cartes : ils vivent en
markdown (`banque/ateliers/` pour les publics,
`etat/<profil>/ateliers/` pour ceux qui pointent une pièce réelle), et
leur seul lien avec ce contrat est qu'un atelier se clôt en produisant
2-3 cartes conformes. Leur format se fixera en M3.

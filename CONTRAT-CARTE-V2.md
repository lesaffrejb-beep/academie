# CONTRAT carte-v2 et chapitre-v1 (proposition à instruire, 02/09/2026)

**Statut : proposition.** Le contrat en vigueur est
[`CONTRAT-CARTE-V1.md`](CONTRAT-CARTE-V1.md) et son valideur
`app/valide_banque.py`. Ce fichier décrit ce que le chantier
`ACA-CONTRAT-2` doit livrer **avec** son valideur, dans le même commit,
sinon il n'existe pas (leçon du contrat `batiment-v1`, qui a dérivé faute
de valideur). Les schémas machine sont dans
[`contrats/carte-v2.schema.json`](contrats/carte-v2.schema.json) et
[`contrats/chapitre-v1.schema.json`](contrats/chapitre-v1.schema.json).

## 1. Ce qui ne change pas

- `id` immuable, kebab-case, unique dans toute la banque.
- `source` : au moins une entrée, **sauf** si `provenance.sans_source`
  vaut vrai (`decisions/0021`) ; dans ce cas la question et la réponse
  ne peuvent contenir aucun chiffre, date, délai, seuil ni montant (le
  valideur le contrôle par motif), la carte est servie avec la mention
  « sans source retrouvée » et `a_recouper` vaut vrai. `verifie`
  obligatoire ; `peremption` obligatoire dès qu'un chiffre bouge ;
  `statut` parmi `brouillon`, `valide`, `signale`, `perime` ; `partage`
  parmi `banque`, `interne`, `perso`.
- Un QCM porte au moins trois choix, exactement un vrai, chaque faux
  avec `pourquoi_faux`. Une image porte `fichier`, `licence`, `credit`,
  `source`.
- Un prérequis pointe vers un identifiant existant ; le scan anti-fuite
  s'applique aux couches `banque` et `interne`.

## 2. Ce que la carte gagne

| Champ | Règle | Pourquoi |
|---|---|---|
| `provenance` | obligatoire : `{auteur: "modele" \| "humain", modele, genere_le, session, sources_retrouvees, sans_source}` ; affiché au joueur (« Généré par Claude Opus le 21/01/2026 · 2 sources concordantes ») | le modèle écrit, la provenance s'affiche (`decisions/0021`) |
| `chapitre` | obligatoire ; identifiant d'un chapitre existant | le chapitre est l'unité de contenu (`decisions/0002`) |
| `niveau` | entier 1 à 5 ; ne peut pas dépasser le niveau du chapitre | échelle 1-5 (`decisions/0003`) |
| `source[].nature` | obligatoire ; valeur fermée : `texte-officiel`, `jurisprudence`, `institution`, `norme`, `doctrine`, `presse-pro`, `organisation-pro`, `association`, `editeur`, `support-interne`, `terrain` | la source affiche sa nature (`decisions/0004`) |
| `source[].parti` | facultatif ; chaîne courte | idem |
| `source[].empreinte` | facultatif ; SHA-256 de la copie locale | les liens meurent (`ARCHITECTURE.md` §3) |
| `type` | ajoute `cas`, `dessin`, `feuille-blanche`, `synthese`, `lecture`, `ecoute` | `BLUEPRINT.md` §7 |
| `pas` | obligatoire si `type: cas` : liste ordonnée de `{situation, choix[], correct, pourquoi}` | le cas en pas |
| `attendus` | obligatoire si `type` vaut `dessin`, `feuille-blanche` ou `synthese` : 3 à 10 éléments de contrôle | l'auto-correction par liste (`decisions/0011`) |
| `document` | obligatoire si `type: lecture` : `{titre, url, nature, methode}` | la lecture guidée |
| `audio` | obligatoire si `type: ecoute` : `{fichier, empreinte_texte, licence}` | l'écoute (plus tard) |
| `chrono` | facultatif ; secondes ; interdit sur `libre`, `lecture`, `synthese`, `dessin`, `cas` | la fluence seulement |
| `confiance` | facultatif ; booléen, défaut vrai pour `qcm` et `cas` de niveau ≥ 2 | l'hypercorrection |
| `image.alt` | obligatoire si `image` | accessibilité |
| `verifie_par` | facultatif ; libellé de la session ou de la personne | le dossier de la carte |
| `historique` | facultatif ; liste de `{date, statut, motif, par}` ajoutée par les outils et les runs de vérification, jamais éditée à la main | auditabilité, `decisions/0019` et `0021` |
| `a_recouper` | dérivé par le valideur, jamais écrit à la main : vrai si aucune source n'est `texte-officiel`, `jurisprudence`, `institution` ou `norme`, ou si `sans_source` | le marqueur à l'écran |
| `confiance` | dérivée par le valideur, jamais écrite à la main : **A** si au moins deux sources de fiabilité A ou B concordantes, relue par un agent frais (`verifie_par`), vérifiée depuis moins de douze mois ; **B** si une source A ou B, relue ; **C** sinon (sources C seulement, sans source, relecture manquante ou vérification trop ancienne). Affichée en lettre sur la carte et le nœud | le dossier du professeur (`decisions/0022`) |

## 3. Le chapitre

Un fichier `banque/<domaine>/<branche>/<chapitre>.json` :

| Champ | Règle |
|---|---|
| `id` | `domaine.branche.chapitre`, immuable, présent dans `programme/<metier>.json` |
| `titre`, `domaine`, `branche` | cohérents avec le programme |
| `niveau` | 1 à 5 |
| `prerequis` | identifiants de chapitres existants, tous de niveau ≤ au sien |
| `objectifs` | 2 à 5 phrases « à la fin, tu sais… » |
| `amorce` | `{question, aide, reponse_attendue}` : le problème à tenter avant la leçon |
| `lecon` | Markdown, 300 à 800 mots, paraphrase et liens, avec un exemple travaillé |
| `synthese` | `{consigne, attendus[]}` |
| `cartes` | tableau de cartes v2 (ou `cartes_fichier` pointant un fichier v1 pendant la migration) |
| `sources` | même format que celles d'une carte ; le chapitre hérite au valideur |
| `provenance` | comme une carte : modèle ou personne, date, session, sources retrouvées, `sans_source` |
| `ponts` | identifiants de chapitres « voir aussi » |
| `satellite` | booléen ; si vrai, `rattachement_propose` et `rattache_le` |
| `statut`, `partage`, `verifie`, `version`, `remplace` | comme une carte |

Un chapitre naît `brouillon` ; il ne se joue que `valide`, et ses cartes
aussi. Un chapitre `valide` dont une carte passe `signale` reste
jouable sans elle.

## 4. Le journal (journal-v1)

Une ligne par événement, append-only, JSON :

| `mode` | Champs | Écrit par |
|---|---|---|
| `revision` | `quand`, `carte`, `note` 1-4, `format` (séance, étude, journée, domaine, épreuve), `duree_ms`, `confiance`, `nonce` | le client |
| `quiz` | `quand`, `carte`, `note`, `stabilite_forcee`, `origine: quiz` | le client |
| `examen` | `quand`, `region` ou `dossier`, `score`, `cartes[]` | le client |
| `erreur` | `quand`, `carte`, `raison` | le client (carnet, privé) |
| `seance` | `quand`, `format`, `jour`, `graine`, `banque_version`, `moteur_version`, `cap` | le client |
| `synthese` | `quand`, `chapitre`, `attendus_coches[]` | le client |

Le serveur n'écrit jamais dans le journal d'un joueur. L'état se
recalcule toujours depuis ces lignes.

## 5. La migration

1. Chaque carte v1 reçoit `chapitre` (assignation depuis
   `programme/copro.json`) et `source[].nature` (assignation par domaine
   d'URL, puis relecture).
2. Les fichiers `banque/<domaine>/<branche>.json` sont éclatés en
   fichiers de chapitre ; les identifiants ne bougent pas.
3. Le valideur v2 lit les deux dispositions pendant la migration et
   refuse une carte sans `chapitre` passée la date fixée par le chantier.
4. Le générateur publie `banque.json` v2 avec `contrat: "carte-v2"` ; le
   client refuse une version qu'il ne connaît pas.

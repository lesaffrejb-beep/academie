# INVENTAIRE DES SOURCES — [MÉTIER]

**COQUILLE VIDE.** Gabarit d'inventaire : les lignes d'exemple sont à
effacer, pas à compléter. Rempli aux étapes 1 et 3 de
[`../USINE.md`](../USINE.md), relu à chaque génération.

> **Ce dossier `sources/` ne quitte JAMAIS la machine du joueur.**
> Ni le serveur de jeu, ni un autre joueur, ni un dépôt public ne voit
> les PDF, cours, annales ou notes qui s'y trouvent. **Seul ce fichier
> `INVENTAIRE.md` est versionné** — c'est un tableau de verdicts, pas
> du contenu. Vérifier le `.gitignore` du dossier avant de déposer
> quoi que ce soit.

Dernière revue : [AAAA-MM-JJ] · Sources tenues : [N] · Trous ouverts : [N]

---

## 1. Le tas (étape 1)

Ce qu'on a repéré, sans rien déplacer ni renommer.

| Emplacement | Nature apparente | Volume | Repéré le |
|---|---|---|---|
| `[dossier / drive / clé / carnet]` | `[cours PDF / annales / captures / notes]` | `[N fichiers]` | `[AAAA-MM-JJ]` |

Gisements à vérifier avant de clore l'étape : disque, drive partagé,
boîte mail, clé USB, carnet de recherche type NotebookLM. **Le joueur
oublie toujours un gisement.**

## 2. Le tri (étape 3)

Un verdict par source, posé à la main. Le classement mécanique (sur le
nom de domaine, sur le type de fichier) est un premier tri, **pas un
verdict** : une part du lot commercial est de la doctrine sérieuse mal
étiquetée, et elle se récupère ligne par ligne.

Fiabilité : `fiable` · `commercial` · `douteux` · `doublon`.
Verdict : `garder` · `virer`.

| Source (titre exact) | Type | Fiabilité | Licence / droit de dériver | Verdict | Vérifié le |
|---|---|---|---|---|---|
| `[titre tel qu'il apparaît]` | `[PDF / page web / annale]` | `[fiable]` | `[public / interne, dérivable, jamais redistribué / inconnu]` | `[garder]` | `[AAAA-MM-JJ]` |

**Le compte**, à tenir à jour comme un solde :

| Lot | Sources |
|---|---|
| Doublons | [N] |
| Autre droit, autre pays, autre édition | [N] |
| Contenu manifestement généré | [N] |
| Hors sujet ou pur marketing | [N] |
| Commercial récupérable (doctrine mal étiquetée) | [N] |
| **Total à retirer** | **[N]** |

Trois pièges vérifiés, à retraquer à chaque revue :

- **Même vocabulaire, autre droit** (ou autre pays, autre référentiel,
  autre édition) : le cas où la réponse paraît juste et est fausse.
- **Contenu généré par IA** : faire citer par une IA du texte écrit par
  une IA, pour en tirer une carte, c'est empiler trois étages sans
  jamais toucher une source.
- **Licence inconnue** : tant que la colonne licence est vide, la
  source ne fonde aucune carte. Une image sans licence n'entre jamais.

**Rien n'est supprimé par un agent.** La suppression est un geste
humain, faite depuis l'outil qui héberge les sources.

## 3. Les trous nommés

**La section la plus importante du fichier.** Un sujet que le plan de
région réclame et qu'aucune source fiable ne couvre **ne devient pas
une carte** : il devient une ligne ici. Écrire un trou est un
livrable, pas un échec — une carte inventée pour combler un trou ne se
voit que le jour où le joueur redit une bêtise à voix haute.

| Sujet à couvrir | Pourquoi il manque | Où chercher (légalement) | Ouvert le |
|---|---|---|---|
| `[le sujet, formulé comme une question du métier]` | `[aucune source sous la main / seule source trouvée non fiable / licence inconnue / source périmée]` | `[référentiel public, institution, annales officielles — nommer, pas « chercher sur internet »]` | `[AAAA-MM-JJ]` |

Un trou se ferme en ajoutant la source au tableau du § 2, puis en
générant les cartes. Il ne se ferme jamais en écrivant les cartes
d'abord.

## 4. Ce qu'on garde et pourquoi

Trois à cinq lignes de prose : les piliers du domaine, ceux sur
lesquels la majorité des cartes s'appuiera, et la raison de leur
confiance. C'est ce paragraphe qu'on relit dans six mois pour savoir
si l'inventaire tient encore.

[À REMPLIR]

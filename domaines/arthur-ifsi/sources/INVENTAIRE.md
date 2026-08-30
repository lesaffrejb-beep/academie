# INVENTAIRE DES SOURCES — Arthur, concours IFSI voie FPC

Rempli le 29/08/2026, première exécution réelle de l'usine à domaine
(étapes 1 et 3 de [`../../../gabarit-domaine/USINE.md`](../../../gabarit-domaine/USINE.md)).
Relu à chaque génération.

> **Ce dossier `sources/` ne quitte JAMAIS la machine du joueur.**
> Au 29/08/2026 il est **vide et le reste** : les fichiers d'Arthur
> vivent dans `~/Downloads/IFSI S1` sur le Mac et **n'ont pas été
> copiés dans le dépôt**. Seul ce fichier `INVENTAIRE.md` est
> versionné — c'est un tableau de verdicts, pas du contenu. Le
> `.gitignore` du dossier est en place et vérifié.

> **Support de cours acquis, non redistribuable.** Tout ce qui en
> dérive est en couche `interne` : paraphrase seulement, jamais de
> recopie, jamais de publication en distribution externe, jamais de
> dépôt du fichier source sur un serveur.

Dernière revue : 2026-08-29 · Sources tenues : 18 · Trous ouverts : 11

---

## 0. Le fait qui date cet inventaire : la transcription tourne en direct

Relevé pendant la séance, à noter avant tout le reste parce qu'il
périme la moitié des chiffres ci-dessous :

| Heure | Fichiers `.txt` présents |
|---|---|
| 17:56 (brief de mission) | 13 |
| 18:06 (relevé du tas) | 17 puis 18 |
| 18:22 (fin de génération) | 46 |

Un traitement de transcription par lot **tourne sur le Mac pendant la
fabrication**, à raison d'environ un fichier par minute. Conséquences,
dites en clair :

1. **Les 35 cartes de ce domaine sont dérivées du lot de 18
   transcriptions disponibles à 18:10** (UE1.1 ×6, UE1.3 ×8, UE2.1 ×4).
   Rien d'autre n'a été lu.
2. Les transcriptions arrivées après 18:10 (UE2.1 complétée, UE2.10
   bactériologie / parasitologie / virologie / mycologie…) sont de la
   **matière pour le prochain lot**, pas pour celui-ci. Les compter
   comme sources de cette livraison serait faux.
3. Le compte de « fichiers à transcrire » ci-dessous est une **cible
   mobile**. Il se recompte au début de la prochaine séance, il ne se
   déduit pas de ce fichier.

## 1. Le tas (étape 1)

Repéré sans rien déplacer, renommer ni copier.

| Emplacement | Nature apparente | Volume | Repéré le |
|---|---|---|---|
| `~/Downloads/IFSI S1` | audio de cours narré, une piste par fiche numérotée | 128 fichiers `.mp4`, ~319 Mo | 2026-08-29 |
| `~/Downloads/IFSI S1` | transcriptions automatiques des mêmes fiches | 18 fichiers `.txt` à 18:10, 46 à 18:22 | 2026-08-29 |

Les 128 audios couvrent neuf UE du semestre 1, numérotées en continu
de la fiche 001 à la fiche 128 :

| UE | Intitulé apparent | Audios | Transcrits à 18:10 |
|---|---|---|---|
| UE1.1 | Psychologie, sociologie, anthropologie | 6 (fiches 001-006) | **6** |
| UE1.3 | Législation, éthique, déontologie | 8 (fiches 007-014) | **8** |
| UE2.1 | Biologie fondamentale | 16 (fiches 015-030) | **4** |
| UE2.2 | Cycles de la vie et grandes fonctions | 23 (fiches 031-053) | 0 |
| UE2.4 | Processus traumatiques | 27 (fiches 054-080) | 0 |
| UE2.10 | Infectiologie et hygiène | 17 (fiches 081-097) | 0 |
| UE2.11 | Pharmacologie et thérapeutiques | 13 (fiches 098-110) | 0 |
| UE3.1 | Raisonnement et démarche clinique | 8 (fiches 111-118) | 0 |
| UE4.1 | Soins de confort et de bien-être | 10 (fiches 119-128) | 0 |

**Gisements non vérifiés, à demander à Arthur avant de clore
l'étape 1** : un drive ou un espace de l'organisme de formation, une
clé USB, la boîte mail (envois de promotion), des polycopiés papier,
un carnet de recherche type NotebookLM, et surtout **tout ce qui
concerne le concours lui-même** — convocation, notice d'inscription,
annales, sujets d'entraînement. Le tas actuel n'en contient rien.

## 2. Le tri (étape 3)

Un verdict par source, posé à la main après lecture.

Fiabilité : `fiable` · `commercial` · `douteux` · `doublon`.
Verdict : `garder` · `virer`.

| Source | Type | Fiabilité | Licence / droit de dériver | Verdict | Vérifié le |
|---|---|---|---|---|---|
| UE1.1 Fiches 001 à 006 (psychologie) | transcription auto d'audio de cours | fiable sous réserve (voir § 2 bis) | support acquis, dérivable en couche `interne`, jamais redistribué | garder | 2026-08-29 |
| UE1.3 Fiches 007 à 014 (législation, éthique, droits) | transcription auto d'audio de cours | fiable sous réserve | idem | garder | 2026-08-29 |
| UE2.1 Fiches 015 à 018 (biochimie, nutriments) | transcription auto d'audio de cours | **dégradée** sur le vocabulaire chimique | idem | garder partiellement | 2026-08-29 |
| Les 110 audios non transcrits au 18:10 | audio, non lu | non jugeable | idem | **en attente** — voir § 3 | 2026-08-29 |

**Le compte**, tenu comme un solde :

| Lot | Sources |
|---|---|
| Doublons | 0 |
| Autre droit, autre pays, autre édition | 0 identifié |
| Contenu manifestement généré | 0 (voix humaine transcrite par machine, ce n'est pas la même chose) |
| Hors sujet ou pur marketing | 0 |
| Commercial récupérable | 0 |
| **Total à retirer** | **0** |

Rien à retirer : le tas est homogène, issu d'une seule et même
production pédagogique. C'est un cas facile, et il ne dit rien de la
difficulté du tri sur un tas hétérogène.

### 2 bis. Le test de santé, dit sans ménagement

**Ce sont des transcriptions automatiques, pas des fiches de cours.**
La distinction n'est pas cosmétique et elle change le régime de
confiance :

- **La structure est excellente.** Chaque fiche annonce son plan, pose
  les définitions dans l'ordre, et énumère proprement. C'est un cours
  magistral bien construit : la matière se découpe en cartes presque
  sans effort.
- **La couche « concepts » est solide.** Définitions, oppositions de
  notions, listes fermées (les six émotions, les dix compétences, les
  quatre modes d'hospitalisation, les trois responsabilités) : c'est
  là que les cartes de cette livraison ont été prises.
- **La couche « références » n'est pas fiable.** Numéros d'articles,
  dates de lois et formules chimiques passent mal la reconnaissance
  vocale. Trois erreurs vérifiées, sur exactement le type de détail
  qu'un QCM teste :

  | Fiche | Ce que dit la transcription | Le problème |
  |---|---|---|
  | UE1.3 / 008 | « article R43-11 du code de la santé publique » | numérotation impossible telle quelle ; la référence réelle est à relever sur Légifrance |
  | UE1.3 / 010 | « loi du 11 février **2007** » pour l'égalité des droits des personnes handicapées | la loi handicap connue porte une autre année ; contradiction non résolue sans le texte |
  | UE2.1 / 016 | « CO2, monoxyde de carbone » | le monoxyde de carbone n'est pas CO2 ; la fiche donne deux fois la même formule pour deux gaz différents |

- **Le vocabulaire technique est abîmé** quand il est rare :
  « périliminant » pour péril imminent, « liaison oseydique » pour
  liaison osidique, « dioloside » pour diholoside, « PO3-4 » pour un
  ion phosphate. Corrigé silencieusement dans les cartes **uniquement**
  là où la déformation est orthographique et sans ambiguïté ; jamais
  là où elle porte sur un fait.
- **Chaque fichier se termine par des artefacts de fin de piste**
  (« Merci. Merci. », « C'est parti ! », « Montage client »,
  répétitions de la dernière phrase). Sans conséquence, mais c'est la
  signature d'une transcription automatique non relue : personne
  n'a ouvert ces fichiers après leur production.

**Verdict d'ensemble.** Bonne source pour le fond conceptuel, source
**non citable** pour toute référence normative. Règle de travail
retenue pour ce domaine et à reconduire : *on dérive la notion, on ne
dérive jamais la référence.* Toute date, tout numéro d'article et
toute formule chimique passe par un texte publié avant d'entrer dans
une carte — ou devient un trou.

## 3. Les trous nommés

**La section la plus importante du fichier.** Onze trous ouverts.
Les cinq premiers sont ceux qui comptent.

| # | Sujet à couvrir | Pourquoi il manque | Où chercher (légalement) | Ouvert le |
|---|---|---|---|---|
| 1 | **Le concours FPC lui-même : nature des épreuves, durée, coefficients, attendus du jury** | **Aucune source dans le tas.** Le dossier ne contient que du contenu de semestre 1, c'est-à-dire ce qui s'enseigne APRÈS l'admission. La région `concours`, qui porte pourtant l'échéance de mars/avril 2027, est vide par manque total de matière | Notice d'inscription de l'IFSI ou du groupement où Arthur candidate (source n° 1, à réclamer) ; arrêté relatif à l'admission en formation infirmière sur Légifrance `[À VÉRIFIER]` — la voie FPC ne passe pas par Parcoursup et ses modalités lui sont propres | 2026-08-29 |
| 2 | **Annales et sujets d'entraînement du concours** | Aucune annale, aucun sujet blanc, aucun corrigé. Impossible de calibrer une carte sur ce qui est réellement demandé | IFSI concernés (sujets des sessions passées) ; centres de documentation. Les recueils d'éditeurs existent mais relèvent du lot commercial et ne se dérivent pas sans vérifier le droit | 2026-08-29 |
| 3 | **110 des 128 audios, soit six UE entières** (UE2.2, UE2.4, UE2.10, UE2.11, UE3.1, UE4.1) et 12 des 16 fiches d'UE2.1 | Non transcrits au moment de la génération. Les régions `soins-et-pathologies` et `pratique-professionnelle` sont déclarées et **vides** pour cette seule raison | Le lot de transcription tourne déjà sur le Mac. Trou en cours de fermeture, à recompter au début de la prochaine séance | 2026-08-29 |
| 4 | **Les références normatives de l'exercice infirmier** : article du code de la santé publique définissant la profession, formulation officielle des dix compétences, code de déontologie | Les numéros d'article sont illisibles dans la transcription (trou n° 1 du § 2 bis). Une carte les citant serait fausse à coup sûr | Légifrance (code de la santé publique, partie réglementaire consacrée à la profession d'infirmier) `[À VÉRIFIER]` ; arrêté relatif au diplôme d'État d'infirmier et ses annexes `[À VÉRIFIER]` ; Ordre national des infirmiers pour le code de déontologie | 2026-08-29 |
| 5 | **Les dates et intitulés exacts des lois sur les droits des patients et des personnes handicapées** | Une contradiction identifiée (loi handicap datée 2007 par le cours) et aucun moyen de contrôler les autres dates. Les cartes existantes portent l'objet des textes, jamais un article | Légifrance pour chaque loi citée ; le portail du ministère chargé de la santé pour la circulaire portant charte de la personne hospitalisée `[À VÉRIFIER]` | 2026-08-29 |
| 6 | Culture sanitaire et sociale : organisation du système de santé, grands enjeux, actualité | Aucune source. La région `culture` est déclarée et vide | Santé publique France ; DREES pour les chiffres du système de santé et la démographie des professions ; HAS pour les recommandations `[À VÉRIFIER pour les trois]` | 2026-08-29 |
| 7 | Modes d'hospitalisation sans consentement : durées des mesures, contrôle du juge, articles applicables | Passage le plus dégradé de tout le tas. Une carte a été écrite sur la seule répartition des certificats, qui est cohérente ; le reste ne s'en tire pas | Code de la santé publique, dispositions sur les soins psychiatriques `[À VÉRIFIER]` | 2026-08-29 |
| 8 | Sanctions pénales de la violation du secret professionnel et de la non-dénonciation | Les montants et durées figurent dans la transcription et paraissent plausibles, mais aucune carte ne les porte : un quantum de peine ne se dérive pas d'une transcription automatique | Code pénal sur Légifrance `[À VÉRIFIER]` | 2026-08-29 |
| 9 | Macronutriments et micronutriments : classification et exemples | Les exemples donnés par la fiche 017 mélangent des niveaux de classification différents. Fond douteux, aucune carte écrite | Programme national nutrition santé ; ANSES `[À VÉRIFIER]` | 2026-08-29 |
| 10 | Gaz du sang et molécules du vivant : formules exactes | Erreur vérifiée sur le monoxyde de carbone, formules ioniques déformées. Le chapitre n'est pas dérivable en l'état | Manuel de biochimie de la formation, ou la fiche audio réécoutée à la main | 2026-08-29 |
| 11 | Développement cognitif de l'enfant (stades et âges) | La fiche 004 mentionne le développement cognitif en une phrase sans nommer les stades. Trop peu pour une carte | Support de cours complet de l'UE1.1, s'il existe en version écrite | 2026-08-29 |

Un trou se ferme en ajoutant la source au tableau du § 2, puis en
générant les cartes. Jamais en écrivant les cartes d'abord.

## 4. Ce qu'on garde et pourquoi

Le domaine repose sur **une seule famille de sources** : la
transcription automatique d'un cours audio d'année 1, acquis, non
redistribuable, exploité en couche `interne`. On la garde parce que
sa structure pédagogique est bonne et que son fond conceptuel se
recoupe avec ce qu'un candidat doit maîtriser. On la garde **sous
condition** : elle fonde des définitions et des distinctions de
notions, jamais une référence normative, jamais un chiffre, jamais
une formule. Cette limite est la raison d'être de la moitié des trous
ci-dessus.

Le déséquilibre à ne pas perdre de vue : **la seule région adossée à
une échéance datée est aussi la seule qui n'a aucune source.** Un
domaine bien rempli sur les sciences humaines et vide sur le concours
prépare correctement le semestre 1 d'une formation dans laquelle
Arthur n'est pas encore admis. Fermer le trou n° 1 passe avant
d'ajouter la moindre carte.

## 5. Statut des cartes produites, dit honnêtement

Les 35 cartes de la livraison du 29/08/2026 sont **toutes en
`statut: "brouillon"`**. La double passe par agent frais (étape 5 de
l'USINE) **n'a pas eu lieu** : elle était hors du périmètre de la
séance. En conséquence, et par construction du moteur, **le générateur
ne les sert pas** — il ne sert que les cartes `valide`, et servir des
brouillons demande une option explicite.

Ce n'est pas un travail inachevé qu'on cacherait : c'est l'état
correct d'une banque qui n'a pas encore été recoupée à la source.
Elles passeront `valide` une par une, et seulement celles dont la
source dit bien ce que la carte affirme.

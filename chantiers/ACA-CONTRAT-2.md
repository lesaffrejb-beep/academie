# Cahier ACA-CONTRAT-2 : le contrat v2 opposable et la banque migrée

Résultat attendu : le contrat carte-v2 et chapitre-v1 sont opposables :
valideur unique, banque migrée à la disposition par chapitre sans
renumérotage, péremption par défaut du droit, `a_recouper` et
`note_confiance` dérivés et publiés.
Fini quand : `app/valide_chapitres.py` (déjà écrit le 03/09) devient le
valideur de toute la banque ; les 84 cartes v1 vivent dans des
chapitres v2 avec `chapitre`, `provenance` et `source[].nature` ;
`genere.py` publie `contrat: "carte-v2"`, les chapitres, les prérequis,
les dérivés et les poids FSRS ; l'archipel joue la banque v2 ou est
retiré au même moment (ACA-FRONT-2) ; tests de mutation étendus.
Dépend de : ACA-PROGRAMME-1, ACA-SOURCES-1. Bloque : ACA-ETUDE-1,
ACA-BOITE-1, ACA-EXAMEN-1, ACA-PAPIER-1, ACA-AUDIT-1, ACA-CONTENT-2,
ACA-BIBLIOTHEQUE-1, ACA-VERIF-1.

## Point d'arrêt du 04/09/2026 : candidat préparé, non promouvable

`app/migre_banque.py` applique la table de 0030 dans une simulation ou
un nouveau dossier isolé. Aucun mode de promotion ni archivage. Les
15 tests et trois mutations ciblées passent. Le rapport mesure
19 changements de domaine, et non les 21 annoncés avant application
de la table finale ; 84 auteurs structurés manquent, 80 cartes valides
n'ont pas de relecteur renseigné, 19 niveaux dépassent leur chapitre,
quatre images manquent d'alternative textuelle. Il reste 54 chapitres
à écrire dans le candidat. L'audit
`travail/audit-froid-2026-09-04.md` donne le point de reprise complet.

L'assignation est tranchée, pas la provenance : le « reste mécanique »
annoncé ci-dessous est un état historique invalidé par la simulation.
Ne pas inventer auteur, modèle, relecteur ou contenu pour migrer ;
aucun archivage sans candidat vert et validation humaine.

## État antérieur au 04/09/2026 : l'étape 2 arbitrée

Les trois questions sont tranchées dans `decisions/0030` (21 changements
acceptés, premier choix partout, deux chapitres neufs, P1 à P5). Il
reste à recopier la table dans `app/migre_banque.py`, régénérer le
programme, migrer, archiver `banque/`.

## État au 03/09/2026 : l'étape 2 attendait un arbitrage de JB

L'étape 2 demande « une table d'assignation écrite à la main (une
carte, un chapitre) ». Elle a été préparée en entier :
[`travail/assignation-cartes-chapitres-2026-09-03.md`](../travail/assignation-cartes-chapitres-2026-09-03.md).

Elle n'a pas été appliquée, et voici pourquoi. Les fichiers de la
banque v1 ont été écrits par thème de travail, pas par domaine du
programme. Conséquence mesurée sur les 84 cartes :

- **21 cartes changent de domaine.** `droit/conformite-annuelle.json`
  disperse à lui seul huit de ses quinze cartes vers `comptabilite`,
  `energie`, `pathologie` et `cabinet`.
- 56 assignations sont sûres, 24 sont défendables autrement, 4 n'ont
  pas de chapitre qui les porte.

Changer le `domaine` d'une carte change la carte-monde : le
remplissage des régions, l'ouverture de la suivante, la branche du
socle que la séance protège (`ACA-ARBRE-1`, `ACA-SEMAINE-1`). Une
carte mal rangée ne casse aucun test et déplace pourtant ce que JB
révise le matin. C'est un arbitrage de contenu, pas une migration.

Trois questions à JB, listées en fin du document de travail : les
changements de domaine, les quatre cartes sans chapitre, et trois
trous du programme que l'assignation a révélés (la notification n'a
pas de chapitre, la déchéance du terme non plus, et le chapitre des
marchés d'exploitation s'appelle « P1 à P4 » alors que les cartes vont
jusqu'à P5).

**Une fois ces réponses données, le reste du chantier est mécanique** :
la table se recopie dans `app/migre_banque.py`, les fichiers de
chapitre s'écrivent, le valideur v2 juge le résultat, et `banque/`
s'archive.

## État au 03/09/2026 au soir : les étapes 1, 3 et 4 sont faites

Ce qui ne dépendait pas de l'arbitrage a été livré pendant qu'il
attend. `genere.py` lit maintenant `chapitres/`, le fait juger par
`valide_chapitres.py`, dérive `a_recouper` et `note_confiance`, et sert
les cartes v2 à côté des v1, avec leur `chapitre` et leur `provenance`.

Deux choix méritent d'être dits, parce qu'ils changent la suite :

- **Le champ `contrat` bascule par construction, pas par drapeau.** Il
  vaut `carte-v2` quand plus aucune carte ne vient de `banque/`, et
  reste absent avant (le client lit alors `carte-v1`,
  `CONTRAT-CARTE-V2.md` §5.4). Le champ dit au client ce qu'il peut
  supposer de CHAQUE carte du lot : l'annoncer v2 sur un lot mixte
  serait un mensonge payé à l'écran. Conséquence pratique : l'étape 2,
  le jour où elle se fera, fera basculer le contrat toute seule.
- **Un identifiant présent des deux côtés arrête la publication.** La
  migration doit déplacer, jamais copier : deux cartes de même
  identifiant, c'est un état de joueur rejoué sur deux contenus
  différents. Le garde-fou est en place avant la migration, pas après.

Effet mesuré le jour même : **la banque servie n'a pas changé d'un
octet**. Les 11 cartes des deux chapitres pilotes sont `brouillon`, donc
écartées en production ; elles se jouent en `--avec-brouillons`. La
machinerie est là, elle attend le contenu.

Reste de l'étape 3 et 4 : rien côté publication. `valide_banque.py` ne
se retirera qu'à la fin de l'étape 2, quand `banque/` sera vide.

## Périmètre

Peut créer ou modifier : `app/valide_chapitres.py`, `app/valide_banque.py`
(retrait ou délégation), `app/genere.py`, `app/migre_banque.py`
(nouveau, à usage unique), `app/tests_*.py`, `app/tests.py`,
`banque/**` (déplacement des cartes dans des fichiers de chapitre sous
`chapitres/`, puis `banque/` ne garde que `images/` et `satellites/`),
`chapitres/**`, `CONTRAT-CARTE-V1.md` (statut « remplacé par v2 »),
`CONTRAT-CARTE-V2.md` (statut « en vigueur »), `contrats/*.json` (par
décision seulement), `DOCTRINE.md` §4 rang 2 (le v2 prend le rang),
`tooling/check.py`, `deploy/academie-publication.service` si le chemin
de sortie change.
Ne touche pas : `app/planificateur.py`, `app/seance.py`,
`app/progression.py` (ACA-ARBRE-1), les identifiants de cartes.

## Déjà tranché (ne pas rouvrir)

- Tout `CONTRAT-CARTE-V2.md` et `contrats/` ; les décisions 0002, 0003,
  0004, 0019, 0021, 0022.
- Disposition : `chapitres/<domaine>/<branche>/<slug>.json`, un objet par
  fichier ; les identifiants de cartes ne bougent jamais.
- Une carte v1 migrée reçoit une `provenance` `auteur: "modele"` ou
  `"humain"` selon son `origine`, `genere_le` = sa date `verifie`,
  `sources_retrouvees` = nombre de sources, `sans_source: false`.
- Une carte v1 sans `nature` sur une source : ACA-SOURCES-1 l'a
  assignée avant ; s'il en reste, `editeur` par défaut et « à recouper ».
- Les cartes migrées sont rattachées aux chapitres de
  `programme/copro.json` par une table d'assignation écrite à la main
  dans `app/migre_banque.py` (une carte, un chapitre) ; un chapitre qui
  ne reçoit que des cartes v1 porte une leçon `[à écrire]` et reste
  `brouillon` jusqu'à ACA-CONTENT-2 : **il ne se joue pas**. Pour ne pas
  priver JB des 80 cartes valides pendant la migration, `genere.py`
  sert aussi les cartes `valide` d'un chapitre `brouillon` quand la
  carte elle-même est `valide` et relue (règle de transition, datée,
  retirée à la fin d'ACA-CONTENT-2).

## Étapes, dans l'ordre

1. Tests rouges : `tests_chaine.py` étendu (une banque v2 de fixture
   traverse `genere.py` et sort `contrat: "carte-v2"`, dérivés présents,
   chapitres et prérequis publiés, poids FSRS publiés) ; `tests_chapitres.py`
   étendu (règle de transition).
2. `app/migre_banque.py` : lit `banque/`, écrit les fichiers de chapitre
   sous `chapitres/`, table d'assignation, ne supprime rien avant que le
   valideur v2 soit vert sur le résultat ; puis `git mv` des anciens
   fichiers vers `archive/banque-v1-AAAA-MM-JJ/`.
3. `genere.py` v2 : lit `chapitres/`, dérive, publie ; `--couches` et
   `--avec-brouillons` inchangés.
4. `valide_banque.py` : délègue au v2 ou se retire ; `tests.py` et
   `check.py` suivent.
5. Vérifier que l'archipel joue la banque v2 (les champs qu'il lit
   existent encore) ou basculer sur `web/` si ACA-FRONT-2 est livré.
6. Mettre à jour `DOCTRINE.md` §4, les deux contrats, la CI.

## Ce qu'on ne fait pas

- Pas de nouveau contenu (ACA-CONTENT-2), pas d'arbre (ACA-ARBRE-1).
- Pas de suppression d'une carte ; une carte inassignable va dans
  `chapitres/_a-rattacher/` et bloque le valideur jusqu'à décision.
- Pas de changement de schéma sans décision.

## Preuve

```bash
python3 app/valide_chapitres.py --rapport && python3 app/genere.py --couches banque && python3 app/tests.py --mutation && python3 tooling/check.py
```

JB voit : la même banque jouable le lendemain matin, et sur chaque
carte la nature de ses sources et sa note.

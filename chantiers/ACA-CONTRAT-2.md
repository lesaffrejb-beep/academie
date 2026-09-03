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

# Livraison des cours copro — 6 septembre 2026

**389 chapitres écrits, 13 dossiers complémentaires et les 61 demandes de JB
rattachées à leur contenu.** Tous restent des brouillons éditoriaux. Les
exemples et exercices sont fictifs et situés en copropriété. Aucun visuel produit.

## Accéder au résultat

- [Table de tes 61 sujets](../../cours/copro/complements/COUVERTURE-JB.md)
- [Index de tous les cours](../../cours/copro/INDEX.md)
- [Bibliographie et limites de consultation](../../cours/copro/SOURCES.md)
- [Sujets voisins et manques restants](../../cours/copro/complements/MANQUES-ET-EXTENSIONS.md)
- [Mode d'étude](../../cours/copro/README.md) et [chemin du professeur](../../CHEMINS.md)

## Couverture mesurée

Le contrôleur retrouve exactement les 389 identifiants du programme dans
81 branches et 11 domaines. Il compte 209,990 mots dans ces chapitres et
11,878 dans les compléments, selon sa segmentation ; ces
quantités ne mesurent pas la profondeur pédagogique. Les niveaux du programme
sont conservés : 117 N1, 193 N2, 58 N3, 19 N4, 2 N5.

| Domaine | Chapitres |
|---|---:|
| cabinet | 42 |
| comptabilite | 41 |
| culture | 7 |
| droit | 60 |
| energie | 29 |
| equipements | 38 |
| immobilier | 32 |
| pathologie | 46 |
| procedure | 33 |
| sinistres | 29 |
| travaux | 32 |

Les 13 compléments développent les interfaces juridiques, les factures et
assurances, l'enveloppe et les sols, le climat et l'autonomie, la comparaison
internationale, les ménages, les groupes d'intérêt et les politiques du logement.
Le mot recherché par JB est explicité : UPEC, dont usure et poinçonnement.
Les prestations P1–P5 sont distinguées des composantes d'une facture EDF.

Les registres contiennent 400 déclarations de sources, dont certaines
URLs partagées entre domaines ; ce n'est pas un nombre de livres intégralement
lus. Chaque entrée décrit nature, date, portée et limites. Une notice, un extrait
indexé ou une présentation commerciale ne devient pas une norme complète.

## Contrôles et examens

- `python3 app/cours_copro.py indexer` : 389/389, aucune erreur ni alerte ;
  13 compléments et 61 demandes contrôlés, références internes existantes.
- `python3 app/tests.py` : suite complète verte ; le contrôleur de cours comprend
  12 tests, avec erreurs provoquées puis corrections documentées.
- `python3 tooling/check.py` : 0 erreur ; résultat conservé dans [check.log](check.log).
- [Examen travaux](EXAMEN-TRAVAUX.md),
  [immobilier et contrôleur](RELECTURE-INVENTAIRE-VENTE-ASL-SCI.md),
  [culture](EXAMEN-CULTURE.md), [énergie](EXAMEN-ENERGIE.md) et
  [examen transversal](EXAMEN-RACINE.md) : périmètres bornés et corrections tracées.

Ces contrôles ne valent pas revue de fond intégrale. Ils ne transforment pas
les niveaux visés en niveaux acquis. Les cours ne sont pas automatiquement
intégrés dans les cartes, les études jouables, Notion ou le VPS.

## Ce qui reste à approfondir

Les normes et DTU complets, la convention IRSI et ses avenants applicables,
plusieurs manuels spécialisés, des sources historiques originales et certains
travaux de sciences sociales restent à instruire. Les comparaisons étrangères
sont un échantillon nommé. Le dossier présidentiel est un état daté du
6 septembre 2026 : il distingue textes nationaux, municipaux, annonces et
programmes non retrouvés ; il n'invente pas les programmes définitifs de 2027.

La progression exige désormais des productions de l'élève et des évaluations
différées sur cas nouveaux. La rédaction fournit une base utilisable ; elle ne
prouve ni autonomie professionnelle ni rang parmi les gestionnaires français.

## Reproductibilité

Le cahier ACA-COURS-COPRO-1, la décision 0052, les règles de rédaction et le
prompt partagé fixent le procédé. Les textes Markdown sont les originaux
éditoriaux. `indexer` régénère inventaire, index, bibliographie et table de
rattachement sans réécrire les cours. Les journaux de tests et les rapports
restent dans ce dossier. La sauvegarde Git suit les chemins de ce chantier ;
le répertoire préexistant `.vite/` est exclu. Aucune installation VPS dans ce lot.

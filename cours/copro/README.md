# Étudier la copropriété en profondeur

Cette base écrite couvre le programme de copropriété et ses ramifications.
Les cours expliquent les mécanismes, les décisions difficiles et des cas
fictifs corrigés. Toutes les applications restent dans l’immeuble collectif.
Les niveaux indiquent la capacité visée par le programme, pas ton niveau acquis.

[Ouvrir tous les cours](INDEX.md) · [Retrouver ta liste de sujets](complements/COUVERTURE-JB.md) · [Consulter les sources](SOURCES.md)

## Partir d’un problème qui t’intéresse

Choisis une demande concrète : comprendre une fissure, contester une facture,
préparer une rénovation, expliquer une majorité ou améliorer un contrat.
Le [chemin du professeur](../../CHEMINS.md) organise le diagnostic des acquis,
les prérequis, le choix des sources et les preuves de transfert.

1. Formule le résultat attendu : quelle décision ou production veux-tu savoir réaliser ?
2. Cherche le chapitre central dans l’index, puis ses prérequis dans le programme.
3. Essaie le cas avant de lire sa correction. Note ton hypothèse et la pièce qui te manque.
4. Lis l’explication, puis vérifie les assertions décisives dans leur source et leur contexte.
5. Résous l’exercice de transfert en changeant une hypothèse. Explique ce qui ferait changer ta réponse.
6. Reprends plus tard un cas différent, avec les mêmes critères. Une bonne réponse aidée ne prouve pas encore une maîtrise autonome.

Par exemple, « comprendre ce que paie la copropriété pour son chauffage »
relie les contrats P1 à P5, les organes de chaufferie, la physique énergétique,
la lecture d’une facture, le budget et la comparaison des offres. Le même
principe n’est pas réécrit intégralement dans chaque branche : les renvois
indiquent le chapitre qui le porte.

## Lire les références et les limites

`[S:id]` renvoie à la source du **domaine du cours**, dans [SOURCES.md](SOURCES.md).
Les dossiers complémentaires indiquent explicitement leur domaine de sources.
La nature, la date, la portée consultée et les limites sont conservées. Un
résumé de recherche, une notice bibliographique, une page commerciale et une
règle juridique n’apportent pas la même preuve. Un PDF repéré n’est pas déclaré
intégralement lu.

`[C:id]` renvoie à un chapitre du programme, retrouvable dans [INDEX.md](INDEX.md).
« Schéma à faire » désigne un support à produire ultérieurement ; aucun visuel
n’a été créé dans ce lot. Les lacunes explicites restent visibles dans les
textes et dans [l’inventaire](INVENTAIRE.json).

## État du contenu

**Brouillons éditoriaux.** Le nombre de chapitres prouve leur présence, pas une
relecture intégrale de leurs sources, une validation professionnelle ou une
compétence acquise. Les points examinés et les contrôles sont décrits dans le
[rapport de livraison](../../travail/cours-copro-2026-09-06/LIVRAISON.md).
La banque de cartes et les études jouables ont leur procédure distincte.
Ces fichiers sont lisibles localement ; ils ne sont pas automatiquement
transformés en études, publiés sur le VPS ou synchronisés dans Notion.

Les N4 et N5 doivent apprendre à comparer des hypothèses, défendre une décision,
identifier une preuve insuffisante et corriger un raisonnement. Certaines sources
approfondies restent à instruire. Le texte est une base de travail importante,
à éprouver sur des productions et des situations variées, sans promettre un rang
professionnel à partir d’un volume de lecture.

## Reprendre la rédaction avec un agent

[Règles partagées](REGLES.md) · [Prompt de rédaction](../../prompts/rediger-cours-copro.md)

```sh
python3 app/cours_copro.py verifier
python3 app/cours_copro.py indexer
```

L’index et la bibliographie sont régénérables ; les textes de cours sont les
sources éditoriales. Les compléments à la liste de JB sont comptés séparément
des identifiants du programme. Aucun changement de niveau ni crédit de lecture
n’est déduit d’un contrôle automatique.

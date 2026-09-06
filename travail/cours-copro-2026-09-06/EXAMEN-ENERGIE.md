# Examen indépendant borné — aides et lecture du DPE

Relecteur : Codex / GPT-6 / cours-copro-20260906/graphe.
Auteur des cours : contenu_expert. Date : 6 septembre 2026.
Statut : revue bornée de brouillons éditoriaux, sans promotion de contenu.

## Verdict

Aucun blocage de fond trouvé dans les cinq sections examinées. Une correction
précise de métadonnée est nécessaire ; une clarification de l'assiette de
l'exercice financier est souhaitable avant réutilisation pédagogique.
Aucun fichier de cours ni registre de l'auteur n'a été modifié par cette revue.

Périmètre : les trois chapitres de `cours/copro/energie/aides.md`, puis
`energie.dpe.la-methode-de-calcul` et `energie.dpe.les-etiquettes` dans
`cours/copro/energie/dpe.md`. Registre des sources concernées consulté.
Les autres chapitres DPE, décence, contrats et audit ne font pas partie de
ce verdict.

## Corrections concrètes proposées

1. `energie/sources.json`, entrée `dila-mpr-copro`, champ `portee` : remplacer
   « syndic bénéficiaire » par « syndicat bénéficiaire, demande portée par
   le syndic en son nom ». Le corps du cours effectue déjà correctement cette
   distinction. La [DILA](https://www.service-public.gouv.fr/particuliers/vosdroits/F37827),
   rubriques objet et démarche, confirme explicitement les deux rôles. La
   métadonnée actuelle pourrait réintroduire la confusion dans SOURCES.md.
2. Exercice MPR : les 700 000 euros sont décrits comme coût de travaux, sans
   préciser leur relation à l'assiette subventionnable ni HT/TTC. Le résultat
   mathématique est exact **sous l'hypothèse d'une assiette admissible au moins
   égale à 500 000 euros**. Ajouter cette hypothèse explicitement rend le cas
   entièrement déterminé : « Supposons une assiette de dépenses admissibles
   d'au moins 500 000 euros avant application du plafond, les vingt logements
   retenus et toutes les autres conditions remplies. » Ne pas attribuer une
   qualification HT/TTC à un coût global sans préciser le régime de dépenses
   utilisé. Les pages HTML bornées consultées ne suffisent pas ici à régler
   toutes les composantes de cette assiette ; aucune règle fiscale nouvelle
   n'est proposée par la revue.

## Constats sur les aides et les prêts

Le [régime MPR présenté par la DILA](https://www.service-public.gouv.fr/particuliers/vosdroits/F37827),
page vérifiée le 1er janvier 2026, a été effectivement relu pour bénéficiaire,
conditions, AMO, paliers et plafonds. Les taux 30/45 %, gains 35/50 % et plafond
par logement sont fidèles au régime métropolitain général présenté. Le cas
20 × 25 000 × 30 % = 150 000 est exact avec l'hypothèse précisée ci-dessus.
L'AMO n'est pas confondue avec la maîtrise d'œuvre. Les régimes ultramarins,
petites copropriétés et cumuls ne sont pas transformés en règles générales.

Le [ministère de l'Économie](https://www.economie.gouv.fr/particuliers/faire-des-economies-denergie/maprimerenov-copropriete-tout-savoir-sur-laide-la-renovation-des-parties-communes),
passages travaux et AMO effectivement relus, confirme la distinction entre
prise en compte d'une chaudière gaz dans le gain énergétique et financement
de son coût. Le cours conserve cette distinction sans promettre un financement
du gaz ni reprendre un régime transitoire périmé.

CEE : pas de montant, fiche, délai ou bonification non étayé annoncé. Le cas
évite de compter une prime déjà incluse dans le devis une seconde fois dans
les ressources. L'économie conventionnelle et l'économie réelle demeurent
séparées. La lecture porte sur le mécanisme ; aucune fiche opérationnelle
particulière n'a été ouverte pour cette revue puisqu'aucune n'est prescrite.

La [DILA éco-PTZ Copropriétés](https://www.service-public.gouv.fr/particuliers/vosdroits/F38064),
introduction et champ effectivement relus, confirme le prêt sans intérêts et
son objet collectif sous conditions. Le cours n'assimile pas prêt, aide et
avance ; il n'annonce ni accord bancaire, ni mensualité, ni coût de garantie
inventé. Le cas 500 000 − 150 000 − 100 000 = 250 000 décrit correctement le
reste final, sans le prendre pour le besoin maximal de trésorerie. Les modalités
du prêt à adhésion automatique sont renvoyées à leur régime propre, sans délai
ou pouvoir de retrait improvisé.

## Constats sur la méthode et les étiquettes DPE

La conversion fictive 100 kWh finaux électriques × 1,9 = 190 kWh primaires
est correcte ; elle est explicitement distinguée du DPE complet, du rendement
et du prix. Le cours ne confond pas données physiques, conventions, facture et
résultat réel. L'exemple de l'isolant exige une preuve de travaux effectivement
réalisés et ne permet pas d'améliorer les entrées pour obtenir une lettre.

Les valeurs temporelles 1,9 en 2026 et 1,7 à partir de 2027 ont été retrouvées
par l'auteur et l'agent racine dans les sources primaires du registre. Cette
revue vérifie leur séparation dans le texte ; elle **ne revendique pas une
nouvelle lecture indépendante intégrale de l'arrêté de 2027**. Aucun basculement
anticipé de la valeur future n'apparaît dans les cinq sections relues.

La règle du critère le moins favorable est correctement expliquée : énergie C
et émissions E conduisent à un classement global limité par E. Le cours ne
reconstruit pas une classe à partir d'une consommation réelle déclarée. Les
unités et la différence avec l'indicateur de confort d'été sont explicites.

L'[arrêté du 25 mars 2024](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000049446315),
annexe 1, début de l'annexe 5 et passages sur les seuils selon surface/altitude/
zone climatique, a été ouvert en HTML pour vérifier la réserve sur les tableaux.
Elle est fondée ; aucune grille simplifiée n'est présentée comme universelle.
Pas de lecture intégrale des annexes 3CL, pas de rendu ou production d'image,
pas de diagnostic réglementaire d'un logement réel.

## Trace de l'état examiné

Empreintes relevées à la fin de la lecture, avant éventuelles corrections auteur :
- aides.md : `e71391fbc9d9339a55aa819feb79a7c55a6e48cf559a65793fa5e945b9dc49e5`
- dpe.md : `f965aa5f51fd102e10ba6338cb6bbfa71d92fae56dfbf9ed20817f76373adf2d`

Aucun test global, build, indexation ni publication exécuté pour cet examen.
L'absence de blocage repéré dans ce périmètre ne valide pas le corpus complet,
les disponibilités budgétaires futures ni le financement d'un projet réel.

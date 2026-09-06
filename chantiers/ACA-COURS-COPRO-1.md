# ACA-COURS-COPRO-1 : première base écrite de tout le programme copro

Demande de JB du 06/09/2026 : rédiger tous les cours bruts, niveau exigeant,
sans produire aucune image ni aucun schéma. L’ambition est l’excellence
professionnelle. Mentionner les supports manquants et garder sources,
cohérence, reproductibilité, règles communes et liens transversaux.

## Résultat et périmètre

Une première rédaction des 389 chapitres du programme courant, avec un
index navigable et un inventaire rejouable. Les niveaux du programme ne
sont pas modifiés pour afficher artificiellement de l’expertise. Même les
repères doivent expliquer leur utilité, leurs limites et un piège réel.
Les auteurs écrivent du texte original, pas des fiches remplies à partir
des titres ni une répétition de formules de prudence.

Périmètre : `cours/copro/**`, `app/cours_copro.py`,
`app/tests_cours_copro.py`, `app/tests.py`, `prompts/rediger-cours-copro.md`,
`decisions/0052-cours-bruts-complets-et-exigence-editoriale.md`,
`decisions/README.md`, `AGENTS.md` (routage uniquement), `README.md`,
`ROADMAP.md`, `roadmap.json`, `travail/cours-copro-2026-09-06/**`.
Le programme, la banque jouable, ses validateurs et le journal restent
hors de cette fabrication de cours bruts.

## Méthode commune

Lire `cours/copro/REGLES.md` avant rédaction. Domaine attribué explicitement
à un auteur ; pas d’écriture simultanée dans le même cours. Sources publiques
et sources locales dont le périmètre de lecture est établi. Pour tout nouvel
original PDF, utiliser l’usine, avec unités et pages bornées. Pour le droit,
les dates, seuils et montants, vérifier les pages officielles pertinentes.
Ne jamais présenter un lien simplement trouvé comme une source lue.

Les répétitions de notions fondamentales sont remplacées par un lien au
chapitre qui les porte ; conserver la nuance spécifique à chaque usage.
Les cas sont fictifs. Pas de données client, pas de contact, pas de dépense,
pas d’image ni de génération graphique. Les besoins de supports sont des
phrases « Schéma à faire pour… », accompagnées d’un objectif pédagogique.

Le contrôle compte les chapitres réellement présents, références et liens,
repère absences et duplication substantielle ; il ne délivre pas une note
d’expertise. Les cours restent des brouillons éditoriaux tant qu’une
relecture de fond distincte n’est pas documentée. Pas de promotion globale
`valide` et pas d’intégration automatique dans les cartes de l’application.

## Preuves

Tests rouges puis verts du contrôle : chapitre absent, doublon, identifiant
inconnu, source ou renvoi inconnu, contenu fictivement validé sans revue,
image interdite. Index régénérable sans écraser les cours écrits.
Vérifier une correspondance exacte avec les 389 identifiants et conserver
les trous de sources ou développements, distincts de cette couverture.
Relecture croisée bornée des parties les plus risquées et des interfaces
entre domaines ; nommer exactement la couverture de cette revue.
`python3 app/tests.py`, puis `python3 tooling/check.py` avant livraison.
Sauvegarder sur main selon CONTRIBUER ; aucune installation VPS dans ce lot.

Précision de JB pendant le lancement : tous les domaines, exemples et
exercices restent ancrés dans la copropriété. La généralisation vers un
autre métier ne vient que plus tard si une discipline l’intéresse.

## Extension demandée en cours de rédaction

JB a soumis une liste détaillée de sujets métier et transversaux le
06/09/2026 : audit de leur présence effective, approfondissements des
chapitres canoniques et dossiers complémentaires si le programme ne
porte pas encore le sujet. `cours/copro/complements/themes/*.md` reçoit
ces dossiers, sans inventer d’identifiants de programme. Un tableau de
couverture relie chaque demande au texte qui l’enseigne ; une simple
occurrence lexicale ne compte pas comme un cours. Le contrôle et l’index
intègrent ces compléments séparément des 389 chapitres du programme.
Les politiques électorales portent une date, une campagne et un état de
publication ; aucun programme futur n’est inventé. Les termes ambigus
(P1–P5, UPEC, désenfumage) sont explicités avec leur portée.

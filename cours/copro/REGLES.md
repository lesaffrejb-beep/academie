# Règles communes de rédaction

Cette base vise une compréhension professionnelle approfondie du programme
copro. Une couverture complète en brouillon reste distincte d’une formation
validée ou d’une expertise démontrée chez l’élève. Outil : Codex ; modèle :
GPT-6, identifiant précis non exposé ; date : 2026-09-06.

## Organisation

Un fichier par branche : `<domaine>/<branche>.md`. Chaque chapitre du
programme est une section `## <identifiant> | <titre exact>` ; les titres
et identifiants proviennent de `programme/copro.json`. Les sous-sections
utilisent `###`. Chaque fichier commence par un titre et la ligne
`Statut : brouillon éditorial` et `Auteur : Codex / GPT-6 / <session>`.
Chaque domaine a un `sources.json`, liste d’objets avec `id`, `titre`,
`url`, `nature`, `consulte_le`, `portee`, `limites`. Un lien simplement
repéré porte `consulte_le: null` et `etat: a_verifier`. Le champ `etat`
vaut `consultee` lorsque la page est effectivement consultée. Un original
PDF n’est dit lu que pour les pages couvertes par le verdict usine.

Citations locales au domaine : `[S:identifiant-source]` au plus près de
l’assertion ou du développement soutenu. Liens transversaux :
`[C:identifiant-chapitre]`, transformables par l’index. Aucun identifiant
inventé. Les références peuvent être répétées ; les explications centrales
ont un chapitre propriétaire. Les références de sources sont publiées
comme liens dans le fichier, en complément des balises si utile à la lecture.

## Un cours doit enseigner

Entrer par un problème, expliquer le mécanisme ou le raisonnement, puis
mettre le lecteur à l’épreuve avec une correction. Le fil doit être propre
au sujet. Ne pas fabriquer 389 variations du même texte.

Chaque chapitre comporte :
- sa capacité cible et le niveau existant, sans requalifier la personne ;
- une explication substantielle des concepts et de leur articulation ;
- une décision délicate, un contre-exemple ou une erreur séduisante ;
- un cas fictif concret avec résolution argumentée ;
- une question de transfert et des critères ou une correction ;
- un ou plusieurs liens utiles, avec la relation expliquée, si pertinents ;
- les limites ou manques réels, sans avertissement passe-partout.

Visez généralement 450 à 900 mots par chapitre, davantage si le problème
le demande. C’est une indication de travail, jamais une preuve automatique
ou un quota à remplir par des répétitions. Un chapitre plus court doit
encore porter un véritable enseignement ; un simple résumé de 100 mots
ne répond pas à la demande. Les textes de niveaux 4 et 5 examinent les
hypothèses rivales, la portée des preuves et l’effet d’un changement de
contexte. Écrire “consulter un expert” n’explique pas la question que cet
expert doit résoudre.

Les calculs pédagogiques sont permis sur données explicitement fictives,
avec formule, unités, hypothèses et interprétation. Ne pas inventer un
seuil normatif, un tarif courant, une majorité, une échéance ou une règle.
Une source juridique est située dans son contexte et sa version consultée.
Une convention d’assureurs ne devient pas la loi. Un fabricant n’est pas
un arbitre désintéressé. Une notice bibliographique ne prouve pas la lecture
d’un ouvrage. Un fait incertain reste précisément incertain.

## Répartition des notions centrales

- Droit : qualification des parties, organes, autorisations, majorités,
  répartition des charges, mutations et responsabilité du syndicat.
- Comptabilité : engagement, trésorerie, comptes, affectations, budgets,
  annexes et contrôle comptable. Procédure porte les voies de recouvrement.
- Pathologie : matériaux, mécanismes des désordres et raisonnement diagnostic.
  Équipements : fonctionnement, organes, défaillances et maintenance.
- Travaux : formulation du besoin, comparaison, contrat, exécution, réception.
  Énergie : physique, diagnostic énergétique, scénarios, exploitation et aides.
- Sinistres : garanties, exclusions, mécanismes d’indemnisation et expertise.
  Procédure : preuve, demandes, voies, acteurs et limites des décisions.
- Immobilier : propriété hors seuls mécanismes copro, vente, bail, urbanisme.
- Cabinet : organisation, conduite des échanges, négociation, données et
  arbitrage transversal. Les cas y mobilisent les autres cours, sans recopier
  leurs développements juridiques ou comptables.
- Culture : analyse d’idées, histoire et lecture critique, sources et portée.

## Images et état des connaissances

Ne créer ni image, ni schéma, ni SVG, ni Mermaid. Si un support manque,
écrire « Schéma à faire pour X : il devra permettre de comprendre Y. »
Le texte doit déjà expliquer ce qu’on peut apprendre sans ce support.
Nommer précisément toute lacune : `À approfondir : ...` ou
`Source à retrouver : ...`, avec l’incidence sur l’usage du cours.

Les auteurs ne signent pas leur propre relecture. Une revue croisée cite
les fichiers et sections examinés, les corrections et les limites.
Le cours brut n’est ni une carte validée, ni un programme professionnel
certifiant ; le compteur de couverture ne mesure pas le niveau acquis.

## Ancrage copro obligatoire, précision de JB

TOUS les domaines sont enseignés pour et dans la copropriété. Les bases
de plomberie, de physique, de droit ou d’histoire restent rigoureuses,
mais tous les cas, exemples chiffrés, exercices et décisions prennent
place dans un immeuble collectif, ses parties privatives/communes, ses
occupants, son syndicat, son conseil syndical ou son cabinet. Pas de cas
de maison individuelle, d’usine, d’hôpital ou d’entreprise générique en
remplacement. Même une notion abstraite explique quelle question d’une
copropriété elle permet de résoudre. Une culture générale peut éclairer
l’habitat collectif, l’architecture de l’immeuble ou la propriété partagée.

L’exploration générale d’un autre métier est une extension ultérieure,
selon l’intérêt de l’élève ; cette première base ne dilue pas l’ancrage
copro. Enseigner un mécanisme physique précis n’oblige pas à quitter ce
contexte. Les comparaisons externes, si nécessaires à une explication,
restent brèves et reviennent au problème de copropriété.

## Dossiers complémentaires demandés par JB

Les thèmes supplémentaires sans chapitre propre vont dans
`complements/themes/<famille>-<sujet>.md`, avec titre lisible, statut
brouillon, auteur, sources et ancrage copro identiques. Préciser
`Domaine sources : <domaine>` pour résoudre les références `[S:...]`
dans le registre concerné. Ne pas créer de faux identifiant programme.
Un cas corrigé et un exercice de transfert restent nécessaires.
La couverture de ces dossiers est comptée séparément des 389 chapitres.

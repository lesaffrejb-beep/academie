# Modèles : provenance et preuves

Révisé le 05/09/2026 à la demande de JB. La
[décision 0034](decisions/0034-capacites-sans-classes-de-modeles.md)
retire les catégories de modèles et les restrictions qui en découlaient.

## 1. Ce qui détermine le travail

La demande humaine fixe l'objectif et les limites. Un agent conduit le
travail autorisé jusqu'au résultat vérifiable. Son nom, son fournisseur,
un classement public ou son absence d'une liste ne restreignent ni ses
missions, ni les niveaux de contenu qu'il peut proposer.

Lire `AGENTS.md`, puis les documents nécessaires à la mission. Les
instructions spécifiques à une ingestion ne s'appliquent pas à une
correction de texte ou à un audit de code. Aucun palmarès de modèles
n'est requis avant de travailler.

## 2. Dire qui a produit le résultat

Indiquer l'outil et le modèle lorsqu'ils sont connus ; sinon écrire
« inconnu », sans inventer d'identité ni en déduire une incapacité.
Pour un document traité par l'usine :

```bash
python3 app/usine/usine.py declarer <empreinte> --outil <outil> --modele <modele>
```

Cette déclaration conserve la provenance. Elle ne délivre pas un permis
et n'attribue aucun rang. Pour le code ou l'audit, la déclaration dans le
point de travail suffit ; l'usine distribue des pages, pas des chantiers.

## 3. Vérifier le résultat à l'endroit où il peut échouer

| Travail | Preuve attendue |
|---|---|
| Lecture d'un document | Extraction, contrôle des pages et figures utiles, état de reprise, limites explicites |
| Carte ou chapitre | Sources retrouvées, assertion contextualisée, valideur, relecture distincte avant service |
| Code | Cahier de la mission, tests pertinents, vérification du contrat et du comportement observable |
| Interface | Parcours et rendu examinés ; les tests ne remplacent pas l'acceptation de JB |
| Publication | Artefact identifié, état réel du serveur et consultation effective ; autorisation humaine |

Une nouvelle capacité s'éprouve sur un travail représentatif et borné.
Consigner réussite, défauts, coût disponible et limites. Ne pas construire
un registre de scores avant qu'un besoin concret le justifie.

## 4. Reprendre et adapter l'effort

L'usine conserve ses unités, sceaux et contrôles. Les paramètres communs
`unite_initiale` et `unite_max` viennent d'`academie.json`. La taille
évolue après les contrôles du document, indépendamment de l'identité du
modèle. Les valeurs sont des choix opératoires, pas des seuils scientifiques.

Les anciens états restent lisibles sans migration des sources. Une
ancienne classe n'a plus d'effet. L'ancien argument CLI correspondant
est toléré avec un message d'obsolescence ; les nouveaux prompts ne
l'utilisent plus. Une unité ouverte est reprise, jamais abandonnée à
cause d'un changement de modèle.

Après des refus répétés, examiner la cause, corriger ou changer d'approche.
Signaler le blocage concret si l'information ou l'autorisation manque.
Le protocole ne demande pas une permission supplémentaire pour une
correction réversible déjà autorisée.

## 5. Ce que les contrôles ne prouvent pas

Un sceau prouve le résultat des contrôles exécutés. Il ne prouve ni la
compréhension du document, ni l'exactitude d'une source, ni l'indépendance
réelle d'un relecteur. Une relecture doit préciser son auteur, sa session,
le contenu examiné et ses réserves. Deux modèles peuvent partager une erreur.

Le modèle fabrique dans l'outil du joueur ; les limites de publication,
dépense, données client et appels côté serveur restent celles de la doctrine.

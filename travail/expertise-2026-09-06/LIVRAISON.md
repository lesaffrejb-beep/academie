# Première unité expertise, 06/09/2026

Compléments du même jour : [pipeline ouvert](PIPELINE.md),
[premier banc natif](BENCHMARK.md), [essais structurés/OCR](BENCHMARK-STRUCTURE.md),
[benchmarks publics et budget Luna/API/abonnement](RECHERCHE-ET-COUTS.md).
Ces compléments n'achèvent pas les unités Angers/PDHH ni les cours experts.

La profondeur disponible ne correspondait pas à l'ambition demandée. Les
389 chapitres prévus ne sont pas 389 cours. L'artefact local contient 93
cartes copro, aucune N4/N5 ; seules trois études complètes copro sont
déclarées valides, toutes juridiques. Les dix autres cartes sont IFSI.

## Changements locaux

- [34 spécialisations](COUVERTURE.md), chacune avec objectifs, production
  attendue, sources à instruire et limites. Toutes restent à construire.
- [Processus reproductible](PROTOCOLE.md), cahier et décision 0046, état
  source distinct de l'état éditorial, priorités transversales nommées.
- Rapport déterministe, empreintes et contrôles : programme seul, artefact
  absent, mauvais rattachement, autre cursus et champs vides ne fabriquent
  pas de preuve de couverture.
- [Focus](SOURCES.md) : fin du pas à pas, fiche acceptée, tableaux structurés,
  figures décrites et anomalies conservées ; première unité antérieure,
  vingt pages supplémentaires traitées ici. Les deux autres PDF restent
  préparés, sans unité acceptée.
- [Exercice candidat énergétique](DOSSIER-PILOTE-ENERGIE.md) rédigé :
  situation, contradiction, production, corrigé et grille. Hors application,
  sans correction IA, pièces résumées seulement.
- Accès authentifié au carnet NotebookLM et ouverture d'une source obtenus.
  Relevé local conservé ; son exhaustivité n'est pas démontrée. Connecteur
  suggéré par JB examiné, pas installé.

## Relecture indépendante

Agent `audit_expertise`, lecture seule, conformément à `CONTRIBUER.md` §7.
Il a identifié un mélange possible des cursus sur un domaine commun et
des champs malformés acceptés. Deux tests rouges ont reproduit les défauts,
puis les corrections les ont rendus verts. Les branches majorités/organes
ont été ajoutées au rattachement juridique.

Avis final favorable à l'unité de cartographie et à la cohérence du candidat
avec le pivot. La réserve sur les pièces simplement résumées est maintenant
explicite. Il n'a pas revérifié les PDF originaux ni leurs références, les
figures ou l'accès au carnet. Pas de promotion en cours validé.

## Limites et reprise exacte

Contrôles finaux exécutés : dix tests spécifiques verts ; `python3
app/tests.py` retourne « TOUT VERT » après autorisation des sockets HTTP
locaux ; puis `python3 tooling/check.py` retourne zéro erreur.
`python3 app/couverture_expertises.py --check` confirme la fraîcheur du
rapport ; `git diff --check` ne signale aucun défaut. Ces contrôles ne
constituent pas une validation pédagogique ni un test de déploiement.

`ACA-EXPERTISE-1` reste ouvert. Prochain travail éditorial : unité Angers
p. 1-12, puis suite du document ; unité PDHH p. 1-12, puis suite ; compléter
les fiches et les rattachements par passage. Instruire les anomalies Focus
avant de publier des affirmations techniques ou des données chiffrées.

Produire ensuite les pièces complètes, les chapitres et les exercices des
dossiers rénovation patrimoniale, désordre technique et copropriété fragile,
et les intégrer aux formats réellement pris en charge. Le catalogue de
spécialités ne remplace pas cette fabrication.

Les changements d'accès aux comptes déjà présents sont conservés, hors de
cette unité : aucune purge, migration distante ou publication effectuée ici.
Les PDF, pivots, rendus et relevé détaillé du carnet restent locaux, hors git.

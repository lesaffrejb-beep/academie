# AGENTS.md — Académie

Académie est un dépôt autonome d'apprentissage gamifié. Lis d'abord
`context/giverny.md`, `README.md`, `METHODE.md`, puis le document spécialisé
nécessaire à la mission.

Règles dures :

1. Aucun contact, immeuble, contrat, mail, réunion ou document client ne doit entrer dans ce dépôt.
2. ERP n'est jamais importé. Un contenu ERP n'arrive que sous forme anonymisée, validée et accompagnée de sa provenance.
3. Une carte non sourcée, périmée ou invalide n'est pas servie en production.
4. L'état joueur est append-only et séparé de la banque de connaissances.
5. Les envois, publications, dépenses et migrations irréversibles demandent une validation humaine.
6. Avant de conclure : `python3 app/tests.py` puis `python3 tooling/check.py`.

La roadmap exécutable est `roadmap.json`; la vision produit détaillée reste dans
`ROADMAP.md` et `SPEC-PRODUIT.md`.

# AGENTS.md — Académie

Académie est un dépôt autonome d'apprentissage gamifié : l'école d'un
métier, jouée tous les jours. Lis d'abord `DOCTRINE.md`, puis `README.md`,
puis uniquement le document que ta mission exige (`DOCTRINE.md` §4 donne
la précédence ; en cas de divergence, le plus haut fait foi et le plus
bas se corrige).

Règles dures :

1. Aucun contact, immeuble, contrat, mail, réunion ou document client ne doit entrer dans ce dépôt.
2. labor n'est jamais importé. Un contenu de labor n'arrive que sous forme anonymisée, validée et accompagnée de sa provenance.
3. Une carte périmée ou invalide n'est pas servie. Toute carte porte son tampon de provenance (modèle ou personne, date, sources retrouvées, relecteur) et ses sources avec leur nature ; le modèle peut écrire s'il cherche sur les domaines fiables, cite, et avoue quand il n'a rien trouvé (« sans source retrouvée », servie marquée, vérifiée en priorité). Un chiffre, une date, un délai ou un montant sans source ne se dit pas. Le trou s'écrit dans l'inventaire, il ne bloque plus (`decisions/0021`).
4. L'état joueur est append-only, séparé de la banque de connaissances, jamais versionné.
5. Les envois, publications, dépenses, suppressions et migrations irréversibles demandent une validation humaine.
6. Une mécanique nouvelle ajoute son entrée sourcée dans `METHODE.md` dans le même commit ; un arbitrage structurant ajoute un fichier dans `decisions/`.
7. Avant de conclure : `python3 app/tests.py` puis `python3 tooling/check.py`.

La roadmap exécutable est `roadmap.json` ; la roadmap lisible, `ROADMAP.md`.
Le domaine (carte des dépôts, décisions transverses, modèles) vit dans
`labor/domaine/` sur le Mac ; `context/giverny.md` en est le paquet
historique. La veille se note dans `lab/VEILLE.md`, format des quatre
verdicts ; ce qu'on veut apprendre se glisse dans `boite/`.

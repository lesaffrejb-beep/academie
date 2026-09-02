# contrats/

Les frontières de l'Académie, en JSON Schema (brouillon 2020-12). Un
contrat est **opposable** quand un valideur l'applique en CI ; jusque-là
c'est une proposition instruite.

| Schéma | Ce qu'il décrit | Valideur | État |
|---|---|---|---|
| `carte-v2.schema.json` | une carte (`CONTRAT-CARTE-V2.md` §2) | `app/valide_banque.py` v2, chantier ACA-CONTRAT-2 | proposition |
| `chapitre-v1.schema.json` | un chapitre et ses cartes (`CONTRAT-CARTE-V2.md` §3) | idem | proposition |
| `journal-v1.schema.json` | une ligne du journal (`CONTRAT-CARTE-V2.md` §4) | `serveur/` à la réception, client à l'écriture | proposition |
| `livraison-v1.schema.json` | le manifeste d'une livraison de banque | `serveur/` à la réception | proposition |
| `programme-v1.schema.json` | `programme/<metier>.json` | `app/valide_programme.py`, chantier ACA-PROGRAMME-1 | proposition |

Règles :

1. Un schéma se versionne dans son nom ; on n'édite jamais une version
   publiée, on en ajoute une.
2. Le valideur Python fait foi sur le schéma quand ils divergent, et le
   schéma se corrige.
3. Un artefact publié (`banque.json`, une livraison) annonce la version
   de contrat qu'il respecte ; le serveur et le client refusent ce qu'ils
   ne connaissent pas.
4. Les schémas décrivent la forme, pas la vérité : une carte peut être
   conforme et fausse. La double passe et le valideur sémantique
   (anti-fuite, péremption, prérequis) restent obligatoires.

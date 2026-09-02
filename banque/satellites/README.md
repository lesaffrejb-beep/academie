# banque/satellites/

Les chapitres satellites nés de la boîte (`decisions/0009`), au contrat
chapitre-v1 avec `satellite: true`. Un fichier par chapitre,
`<slug>.json`. Ils sont validés comme tout chapitre (double passe,
valideur) et jouables dès `valide`, quel que soit l'état de l'arbre.

Quand un satellite est rattaché (`rattache_le`), le fichier est déplacé
dans `banque/<domaine>/<branche>/` par le chantier de rattachement ;
son identifiant ne change pas.

Vide au 02/09/2026 : le premier satellite sort du chantier `ACA-BOITE-1`.

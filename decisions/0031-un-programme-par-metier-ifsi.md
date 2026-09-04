# 0031. Un programme par métier : `programme/ifsi.json`, l'arbre de l'infirmier

Date : 04/09/2026. Brief de JB : « un arbre qui aille jusqu'au concours
d'infirmier d'Arthur, mais que s'ils veulent avancer ils puissent faire
sa formation, et aller beaucoup plus loin dans chaque domaine ».

## Décision

1. `programme/` porte un fichier par métier, chacun généré par son
   script (`genere_copro.py`, `genere_ifsi.py`). Le catalogue
   (`programme/catalogue.json`) les liste tous.
2. `academie.json` reste le fichier de l'Académie de JB : le valideur
   ne l'aligne qu'avec le programme dont le `metier` est le sien. Les
   autres programmes se valident seuls (structure, prérequis, socle,
   semaine type). Une Académie d'Arthur aura son propre `academie.json`
   dans son dépôt (`0008`).
3. L'arbre infirmier a dix domaines et Culture, calqués sur les
   familles d'unités d'enseignement de l'arrêté du 31 juillet 2009,
   plus un domaine « L'entrée en IFSI ». Les niveaux disent le chemin :
   I et II = ce que la sélection d'entrée attend (le socle, niveau II
   partout) ; III = la formation (unités, dix compétences, gestes,
   stages, cas transverses) ; IV et V = au-delà du diplôme.
4. Le parcours des douze premières semaines vise l'entrée en IFSI :
   quatre séances, une étude le samedi qui prépare l'écrit puis l'oral.
5. Le squelette ne porte aucun chiffre (durée d'épreuve, taux, dose,
   norme) : ils n'entrent qu'avec leur source, dans les chapitres
   (`0021`). Les modalités d'admission changent souvent : le domaine
   « entrée » se périme à douze mois comme le droit (`0019`).

## Contexte

Le programme copro a montré la forme (`ACA-PROGRAMME-1`). Arthur a un
premier semestre d'IFSI en sources (`gabarit-domaine/DESSINER-LA-CARTE.md`),
donc ce squelette sera confronté à de la matière réelle dès le kit de
domaine (`ACA-DOMAIN-KIT-1`). Écrit de tête par un modèle, sans
recherche : les titres et notions sont des repères, pas des faits.

## Conséquences

- 310 chapitres à écrire, tous `a-ecrire` ; aucun n'est joué avant
  d'avoir sa leçon sourcée.
- Un agent frais calibre les niveaux comme pour la copro
  (`travail/calibrage-programme-2026-09-03.md`), avant le premier lot.
- `SYLLABUS-IFSI.md` est le programme lisible ; `ifsi.json` fait foi.

## Réouverture

Si Arthur, en jouant, trouve que l'entrée en IFSI demande autre chose
que le socle II, on ajuste le socle ; si le référentiel de formation
est réformé, on ajoute les chapitres, on ne renumérote pas.

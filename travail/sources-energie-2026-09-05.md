# Sources : complément DILA du 05/09/2026

Unité ACA-CONTENT-MAP-1. Outil : Codex ; modèle : GPT-6.
Complète les inventaires énergie, travaux, immobilier et cabinet du 04/09.
Repérage de pages publiques et de droits ; aucune fiche métier déclarée
lue intégralement, aucune carte créée.

## Droit de réutilisation retrouvé

La page officielle [Mise à disposition des données](https://www.service-public.gouv.fr/P10004),
datée du 03/03/2026 et consultée le 05/09, renvoie aux données sous licence
ouverte. Les [mentions légales](https://www.service-public.gouv.fr/P10025)
distinguent liens autorisés, photos et marques réservées. Leur clause sur
les marques ne doit pas être attribuée aux fiches.

Le [jeu Particuliers de la DILA](https://www.data.gouv.fr/datasets/fiches-pratiques-et-ressources-de-service-public-gouv-fr-particuliers)
annonce la Licence Ouverte 2.0. Pour une extraction future, conserver
l'attribution Service-Public.gouv.fr / DILA, l'URL de téléchargement, le
nom du fichier et sa date ; suivre les mises à jour annoncées. La date
affichée pour le catalogue, 17/08/2026, ne date pas chaque fiche.

## Application aux quatre inventaires

| Domaine | Sources concernées dans l'inventaire du 04/09 |
|---|---|
| énergie | E3, plan pluriannuel de travaux |
| travaux | T9 et T11, déclaration préalable et PPT |
| immobilier | I4 à I7 et I9, propriété, vente et bail |
| cabinet | C5, syndic |

L'incertitude sur le canal de réutilisation de ces informations est levée.
Cela ne valide ni leur contenu juridique ni leurs références actuelles.
Avant fabrication : retrouver la fiche dans le jeu, dater sa version,
ouvrir ses textes de référence, puis suivre le contrôle documentaire.
Abandonner un fichier retiré, remplacé ou impossible à dater. Les images,
marques et documents externes gardent leurs droits propres.

Le registre reçoit une ligne spécifique au jeu, sans rattacher tout
data.gouv.fr à cette licence. Les anciens repérages restent datés du 04/09.
La colonne `verifie` reste vide : aucune lecture métier intégrale achevée.

## Suite bornée

ACA-CONTENT-MAP-1 reste ouvert : les lacunes scientifiques et techniques
des inventaires persistent et Culture ne possède qu'un chapitre N1.
Ce complément retire une incertitude commune sans élargir le programme.

## Contrôles locaux du lot

Comparaison des inventaires du 04/09 à `programme/copro.json` par assertions :
34 branches présentes et 21 identifiants N1 exactement dans l'ordre attendu
(cinq par domaine, un pour Culture). Les deux lignes ajoutées portent le
registre à 35 entrées, sans modifier les rattachements existants des cartes.

`python3 app/tests.py` : TOUT VERT ; puis `python3 tooling/check.py` :
zéro erreur. Ces contrôles vérifient le dépôt local, pas l'exactitude
juridique ou historique de documents non encore traités. Aucun code
d'application ni contenu servi modifié par ce lot.

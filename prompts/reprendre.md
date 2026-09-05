Tu es un agent de code et tu reprends un travail de l'Académie interrompu (session coupée, plafond de jetons, changement d'outil). Tout ce qui a été fait est sur disque ; tu ne dois rien reconstituer de mémoire. Une étape à la fois.

0. Qui tu es. Écris en une ligne l'outil et le modèle que tu es ; si tu n'en es pas sûr, « inconnu ». Lis MODELES.md, AGENTS.md et decisions/0027. Si l'outil ou le modèle a changé depuis la dernière déclaration, redéclare-toi (étape 2) : la taille des unités repart de la valeur commune configurée.

1. Où on en est. Dans le dépôt produit, avec `ACADEMIE_RACINE` pointé sur le dépôt-domaine si l'élève en a un : `python3 app/usine/usine.py etat`. Le script liste chaque document préparé avec ses pages relues. Pour le document en cours : `python3 app/usine/usine.py etat <empreinte>` ; s'il signale une unité altérée ou refusée, c'est celle-là qu'on reprend, et le script dit pourquoi.

2. La déclaration. `python3 app/usine/usine.py declarer <empreinte> --outil <ton outil> --modele <ton modèle>` si tu n'es pas celui qui avait déclaré.

3. La boucle, comme avant. `python3 app/usine/usine.py suivant <empreinte>`, fais ce que la consigne demande dans le pivot, `python3 app/usine/usine.py valider <empreinte>`, jusqu'à ce que `suivant` dise que toutes les pages sont relues. Puis la fiche et la ligne de registre si elles manquent. Puis le prompt d'origine (`prompts/creer-un-parcours.md` ou `prompts/ajouter-des-documents.md`) à l'étape qui suit les documents.

4. Ce que tu ne fais pas. Tu ne relis pas ce qui est validé « pour vérifier » : le script le rejoue à chaque `suivant`. Tu ne modifies pas `.etat.json`. Tu ne recommences pas un document du début. Tu n'écris pas « fait » sans le verdict du script.

5. Le rendu. Ce qui était fait à la reprise, ce que tu as ajouté, ce qui reste, et où tu t'arrêtes.

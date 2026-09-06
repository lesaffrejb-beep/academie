# 0049 : pilote hybride de dix pages jusqu'à une étude jouable

Date : 06/09/2026. Statut : accepté pour ce pilote, à la demande de JB.

## Contexte

Le benchmark de moteurs ne prouve ni la fidélité des visuels, ni la qualité
du cours, ni son usage. JB demande un essai de bout en bout publié.

## Options et décision

Retenir les pages 13 à 22 du Focus 106 (juin 2024), déjà scellées par l'usine.
Croiser le texte natif Poppler avec Docling/RapidOCR pour la structure, puis
arbitrer face au rendu PyMuPDF. Un vote entre extracteurs, ou un OCR total
par défaut, n'est pas retenu : la source contient elle-même des contradictions.
Pas d'API payante ; cette décision ne proclame pas un meilleur moteur universel.

Récupérer les régions figures/tableaux localement avec coordonnées et empreintes.
Conserver la page entière quand la région coupe une légende ou une note.
Ne publier que nos schémas originaux et des formulations pédagogiques originales,
avec renvois aux pages du PDF, faute de droits établis sur les figures sources.

Le cours est un satellite de lecture critique, pas la couverture de la branche
ni une expertise acquise. Relecture indépendante avant activation. Le client
affiche les supports, bloque un exercice dont le support manque et rend les
parcours supplémentaires accessibles. Aucun nouveau système de notation IA.

## Conséquences et preuves

Le produit garde des liens source → assertion → exercice, plutôt qu'un résumé
opaque. Extraction, arbitrage sémantique, auteur, relecteur, test et publication
sont des étapes distinctes. Dossier : `travail/pilote-renovation-10p/`.

Publication isolée des modifications de comptes en cours ; sauvegarde statique
et source du générateur cohérente avec le timer. Aucune migration joueur.
Les résultats de tests et la diffusion ne prouvent pas le transfert pédagogique.

Références : décisions 0027, 0047 et 0048 ; documentation primaire Docling,
https://docling-project.github.io/docling/examples/export_figures/ ; source
https://www.cae-eco.fr/staticfiles/pdf/focus-106-modelisation-reno-240625.pdf.

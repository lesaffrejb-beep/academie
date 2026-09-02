# 0008, Chacun son dépôt-domaine et son abonnement ; aucun paiement demandé

- Statut : acceptée (confirme le modèle A4 du 29/08)
- Date : 02/09/2026
- Décideur : JB (« sans demander d'argent, chacun avec son repo, son
  abonnement ; si un copain peut reprendre tout le repo, faire ses fiches
  JSON avec son propre LLM et que ça rentre dans mon truc, pourquoi pas »)

## Décision

1. **Aucun joueur ne paie jamais rien.** Pas d'abonnement, pas de
   boutique, pas de monnaie, pas de « premium ».
2. **Chaque domaine est un dépôt** (`gabarit-domaine/`) tenu par celui qui
   le fabrique, sur son compte, avec son abonnement au modèle. Le
   traitement (tri des sources, génération, double passe) tourne chez lui.
3. **JB porte le serveur pour son cercle** (VPS OVH, sous `/academie/`).
   Le serveur reçoit des **livraisons** : un JSON validé, poussé par un
   geste humain, re-validé à la réception, mis en quarantaine, puis servi.
4. **Tout le monde peut héberger le sien.** Le dépôt produit s'installe
   en une commande sur n'importe quel Linux avec Python et Caddy
   (`ARCHITECTURE.md` §9). Un copain qui reprend tout le dépôt a son
   Académie, et peut aussi livrer sa banque au serveur de JB s'il le
   souhaite.
5. **Les coûts se disent.** La fabrication d'un domaine se mesure en
   tokens et en euros (`gabarit-domaine/DESSINER-LA-CARTE.md` §6) ; aucun
   chiffre ne se promet avant mesure.

## Contexte

Le modèle A4 (un dépôt source par joueur, un serveur de jeu) est arbitré
depuis le 29/08. Le brief du 02/09 le confirme et ajoute le cas du
copain qui reprend tout, et l'entrée PDF / OCR / vidéo.

## Conséquences

- L'usine (`USINE.md`) gagne les entrées PDF scanné (OCR), vidéo (sous-
  titres ou transcription locale) et capture d'écran (lecture par modèle
  de vision, chez le joueur).
- La couche `interne` reste le domicile de tout ce qui dérive d'un
  support acquis (cours d'Arthur, Immocampus) : jamais servi à un tiers.
- Une livraison sans registre de sources (`sources/REGISTRE.md`) est
  refusée à la réception dès le contrat v2.

## Réouverture

Le jour où l'infrastructure coûte plus que ce que JB accepte de porter
seul : on rouvre le partage des frais d'hébergement, jamais un prix
d'usage.

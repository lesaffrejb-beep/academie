# 0032. L'arrivée : compte par mail et mot de passe, un cursus à la fois, demande de nouveau cursus à JB

Date : 04/09/2026. Arbitrage de JB, rendu oralement.

## Décision

1. **Un compte se crée avec une adresse mail professionnelle et un mot
   de passe.** Pas d'onboarding qui traîne : on dépose ses deux
   informations, on entre. Le lien magique (`serveur/API.md`) reste
   pour l'ajout d'un appareil et le mot de passe oublié.
2. **Ensuite, on choisit un cursus** dans le catalogue
   (`programme/catalogue.json`) : aujourd'hui Gestionnaire de
   copropriété ou Infirmier.
3. **« Nouveau cursus » n'est plus un bouton vers des prompts** : c'est
   une demande adressée à Jean-Baptiste. L'élève explique sa situation
   et pourquoi ; la demande est enregistrée côté serveur et JB la lit.
   Rien ne part vers un tiers sans son geste (règle 5). Les prompts de
   `prompts/` restent pour qui fabrique son domaine à la main
   (`COMMENCER.md`), mais ils ne sont plus l'entrée principale.
4. **Un cursus commencé est relié au profil.** Un seul cursus à la fois
   pour l'instant ; l'état se sauve tout seul (le journal, `0006`).
   Plusieurs cursus en parallèle : plus tard, quand on aura vu.

## Contexte

Le cahier `ACA-ONBOARDING-1` du 03/09 prévoyait pseudo seul, catalogue,
et « Créer le vôtre » vers les prompts, en laissant les comptes à
`ACA-MULTI-DECISION-1`. Le second programme (`0031`) rend le choix de
cursus réel, et JB tranche l'entrée dès maintenant.

## Conséquences

- `ACA-ONBOARDING-1` se réécrit : mail, mot de passe, pseudo, cursus,
  demande de cursus, puis quiz de positionnement.
- Le serveur doit accepter un mot de passe (haché, jamais en clair,
  même règle que les jetons de `auth.py`) et une table de demandes de
  cursus : étape ajoutée au cahier, périmètre `serveur/` ouvert pour ça.
- Le journal porte le cursus choisi (une ligne d'événement) ; le client
  n'affiche que l'arbre de ce cursus.
- Le point « comptes » d'`ACA-MULTI-DECISION-1` est tranché ici ; y
  restent le fournisseur de mail, le RGPD et la suppression.

## Réouverture

Quand un joueur réel demande un second cursus en parallèle, on rouvre
le point 4, pas les autres.

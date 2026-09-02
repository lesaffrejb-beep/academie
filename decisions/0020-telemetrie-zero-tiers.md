# 0020, Télémétrie : le journal, et rien d'autre, chez personne d'autre

- Statut : acceptée (question oubliée n° 8)
- Date : 02/09/2026
- Décideur : agent

## Décision

1. **Ce qu'on mesure est dans le journal du joueur**, et il peut le
   lire et l'exporter : révisions, formats, durées, confiance, graines,
   erreurs (son carnet), épreuves, synthèses.
2. **Aucun service tiers**, à deux exceptions nommées : pas d'analytique
   externe, pas de police ni de script chargé d'un autre domaine, pas de
   rapport de plantage envoyé ailleurs que sur le VPS de JB. La
   politique de sécurité de contenu (CSP) du client l'interdit
   mécaniquement. Exception 1 : le fournisseur d'envoi de mail, pour les
   magic links et la confirmation de suppression, inscrit au registre
   comme sous-traitant. Exception 2, plus tard et opt-in : le fournisseur
   de modèle que le joueur choisit lui-même pour la correction libre,
   avec sa clé, déclaré dans ses réglages ; l'appel part de son
   navigateur vers ce seul hôte, et la CSP l'admet uniquement quand le
   joueur l'a activé (R4 du pré-mortem du 02/09).
3. **Les mesures produit** (fréquence des séances, abandons, durée,
   formats qui lassent, rétention réelle) se calculent depuis le
   journal, côté serveur, par `rapport_rituel.py`, **sans lire le
   contenu des réponses**, et se lisent par JB dans un rapport, jamais
   dans un tableau de bord tiers.
4. **Les notifications** (question oubliée n° 6) : une par jour au plus,
   à l'heure choisie par le joueur, opt-in, silencieuse si la séance est
   faite, formulée en fait (« 9 cartes t'attendent »), jamais en
   reproche. PWA seulement ; aucun mail de relance.

## Contexte

Le brief vise des collègues et une classe : la confiance dans l'outil
tient à ce qu'il ne parle de personne à personne. Le journal est déjà
append-only et exportable ; il suffit de ne rien ajouter à côté.

## Conséquences

- `web/` : CSP stricte, test qui liste les hôtes contactés.
- `serveur/` : aucune dépendance réseau sortante.
- Registre RGPD : une seule finalité de mesure, décrite.

## Réouverture

Aucune prévue.

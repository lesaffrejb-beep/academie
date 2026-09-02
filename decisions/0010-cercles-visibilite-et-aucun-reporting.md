# 0010, Cercles, visibilité consentie, aucun reporting hiérarchique

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur le brief de JB (« compétition avec les collègues,
  savoir où ils en sont, le même arbre par métier ; à l'échelle d'une
  agence, d'un service copro, de juste moi, d'une classe d'élèves
  infirmiers »)

## Décision

Trois cercles, du plus petit au plus grand :

| Cercle | Qui | Ce qui se voit | Ce qui ne se voit jamais |
|---|---|---|---|
| **Solo** | un joueur | tout, par lui seul | |
| **Cercle** | amis ajoutés mutuellement | l'arbre (par domaine, débrayable), le compteur de séances, les insignes, les défis joués | le carnet d'erreurs, les réponses, les temps par carte |
| **Équipe** | une agence, un service, une classe : un cercle avec un domaine commun | idem cercle, plus une ligue hebdomadaire **facultative** et un rôle **tuteur** consenti | idem ; et aucun agrégat, aucun export, aucun classement obligatoire |

Règles :

1. **Symétrie** : je vois de toi ce que tu vois de moi, domaine par
   domaine. Un tuteur ne voit que ceux qui l'ont accepté, et chacun voit
   qu'il est vu (« X voit ta progression sur Droit »). Retrait d'un clic,
   silencieux.
2. **La ligue mesure des cartes stabilisées, pas des clics** : le score
   hebdomadaire est le nombre de cartes passées au-dessus du seuil de
   stabilité dans la semaine. On ne peut pas la gagner en bourrant.
3. **Aucun reporting hiérarchique.** Il n'existe pas d'écran, d'export ni
   d'API qui donne l'état d'une personne à quelqu'un qu'elle n'a pas
   accepté. Le jour où un manager le demande, la réponse est non, et
   elle est écrite ici.
4. **Rien n'est public.** Pas de profil public, pas de classement public.
   Une banque `partage: banque` peut être ouverte comme un manuel, par
   décision du propriétaire du domaine.
5. **Coupure mesurée** : si la ligue ou les défis font baisser la
   fréquence des séances d'un joueur sur quatre semaines, ils lui sont
   coupés d'office, et il peut les rallumer.

## Contexte

Le pré-mortem du 29/08 a trouvé dans le front un podium de collègues
réels nommés avec des métriques inventées : une règle écrite ne tient
pas sans mécanisme. Les cercles n'existent pas encore ; ils attendent
le gate du rituel et les comptes (`ACA-MULTI-DECISION-1`).

## Conséquences

- Chantiers `ACA-CERCLE-1`, `ACA-LIGUE-1`, `ACA-TUTEUR-1`, dans cet ordre,
  après authentification et suppression de compte sous 48 h.
- Le registre RGPD nomme chaque cercle comme un traitement à part.

## Amendement du 02/09/2026 au soir : tous les joueurs se voient par défaut

JB : « je veux que tous les joueurs se voient ». La règle 1 devient :

- **Par défaut, tous les joueurs d'une même Académie se voient** : arbre
  (tous les domaines), titre, insignes affichés, compteur de séances.
  C'est le modèle des applications de sport : la visibilité est la
  norme, la discrétion un réglage.
- **Chacun peut masquer un domaine, ou se masquer entièrement**, d'un
  geste, sans le dire à personne.
- **Ce qui ne se voit jamais ne change pas** : le carnet d'erreurs, les
  réponses, les temps par carte, et aucun agrégat, export ni classement
  imposé pour un tiers. La ligue reste facultative.
- Le rôle tuteur reste consenti par chacun : voir un arbre n'est pas
  la même chose que suivre quelqu'un, et le suivi se demande.

Le reste de la décision tient.

## Réouverture

Si une classe ou une agence a besoin d'un suivi collectif, on conçoit un
agrégat **anonyme et à seuil** (jamais sous 8 personnes), par décision
nouvelle.

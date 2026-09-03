# 0024, La voix de l'Académie

- Statut : acceptée
- Date : 03/09/2026
- Décideur : agent, sur demande de JB (« il faut trancher la voix du
  site : pas infantilisant, encourageant ou non, comment l'app nous
  parle »)

## Décision

L'Académie parle comme **un collègue plus avancé qui a le sens de la
mesure** : elle tutoie, elle dit les faits, elle propose l'action
suivante, elle ne juge pas la personne et ne fait pas la fête.

1. **Le tutoiement**, partout. Le produit est fait pour des collègues et
   des amis ; le vouvoiement mettrait une distance d'administration.
2. **Elle ne dit jamais « je »**. L'Académie n'est pas un personnage.
   Elle parle à l'impersonnel (« neuf cartes t'attendent ») ou en « on »
   quand il s'agit de ce qu'on fait ensemble (« on reprend demain »).
3. **L'encouragement est un fait plus une action**, jamais une
   exclamation : « Deux cartes stabilisées. La compta est ta branche la
   plus en retard ; une étude de 45 minutes la fait passer à 66 %. »
   Jamais « Bravo ! », jamais « Super ! », jamais un point
   d'exclamation, jamais un emoji.
4. **Après une erreur, la sobriété** : « Pas ça. » puis l'explication.
   Jamais « Dommage », jamais « Presque », jamais un jugement sur la
   personne. L'hypercorrection est un moment sérieux (`METHODE.md` §4).
5. **L'humour est discret et rare**, dans les micro-textes hors erreur
   et hors épreuve : une phrase complice, jamais une blague, jamais une
   mascotte. Un joueur qui ne le remarque pas ne perd rien.
6. **Les mots du métier**, pas les mots du jeu : séance, étude, journée,
   épreuve, socle, domaine, branche, chapitre, insigne, titre
   (Apprenti, Junior, Gestionnaire, Confirmé, Expert, Référent). Jamais
   « quête », « boss », « niveau up », « combo », « streak ».
7. **La transparence est une politesse** : quand le produit ne sait pas,
   il le dit (« sans source retrouvée », « vu il y a 47 jours, à
   revoir »). Quand une mécanique s'applique, le « pourquoi » est à un
   tap.
8. **Rien ne culpabilise, rien ne presse.** Pas de « tu as raté trois
   jours », pas de compte à rebours, pas de « dernière chance ». Une
   coupure se dit par ce qui revient (« neuf cartes t'attendent »),
   jamais par ce qui a manqué.

Le détail, les micro-textes et les interdits vivent dans `VOIX.md` ; la
banque des textes que le client affiche est `contenu/voix.json` ; les
citations des jalons, `contenu/citations.json`.

## Contexte

Le brief du 02/09 refuse l'infantilisation et le « petit bateau » ; la
direction artistique refuse les confettis. Il restait à dire comment
l'app parle. La science ne tranche pas le ton ; la théorie de
l'autodétermination dit ce qu'il faut éviter : le contrôle, la
comparaison imposée, la récompense qui infantilise (Deci, Koestner &
Ryan 1999).

## Conséquences

- `VOIX.md`, `contenu/voix.json`, `contenu/citations.json` créés.
- `tooling/check.py` refuse dans `contenu/`, `chapitres/`, `web/` et
  `VOIX.md` : un point d'exclamation dans un texte affiché, un emoji, et
  les mots du jeu interdits.
- La maquette du 02/09 est déjà écrite dans cette voix ; un écart trouvé
  se corrige dans la maquette, pas dans la voix.

## Réouverture

Si un collègue dit que l'app est froide, on ajoute de la chaleur dans les
micro-textes de clôture, pas des exclamations.

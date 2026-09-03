# Cahier ACA-ONBOARDING-1 : l'arrivée d'un élève

Résultat attendu : dans le client v2, un nouvel élève choisit un pseudo,
voit le catalogue (`programme/catalogue.json`) et la carte « Créer le
vôtre », copie un prompt de `prompts/` en un geste, puis passe au quiz de
positionnement ; tout dans la voix de `VOIX.md` (`contenu/voix.json`,
clés `arrivee.*`) ; aucune saisie de document dans l'app (`COMMENCER.md`).
Fini quand : les tests nommés ici sont verts, plus tests.py et check.py.
Dépend de : ACA-FRONT-2, ACA-PROGRAMME-1. Bloque : rien.

## Périmètre

Peut créer ou modifier : `web/src/ecrans/Arrivee/` (pseudo, catalogue,
créer le vôtre), la route `/arrivee` dans `web/src/app/routes.tsx`,
`contenu/voix.json` (clés `arrivee.*` seulement), `programme/catalogue.json`
(les compteurs), `web/README.md`.
Ne touche pas : le moteur, le journal, le serveur, les prompts (ils se
lisent tels quels), `COMMENCER.md` hors des compteurs.

## Déjà tranché (ne pas rouvrir)

- Le pseudo est visible par défaut dans le cercle ; le carnet d'erreurs
  jamais ; pas d'avatar (`decisions/0010`, `0015`).
- Le catalogue est un fichier de données ; « Créer le vôtre » est un
  bouton fixe vers les prompts ; les documents restent sur la machine de
  l'élève (`decisions/0026`, `0027`, `COMMENCER.md` §5).
- Le quiz de positionnement vient après le choix du parcours
  (`BLUEPRINT.md` §11).
- Aucun hôte tiers ; la copie du prompt se fait dans le presse-papiers,
  rien n'est envoyé.

## Étapes, dans l'ordre

1. Tests rouges : un pseudo vide est refusé avec le texte `arrivee.pseudo`
   ; le catalogue affiche autant de cartes que `programme/catalogue.json`
   plus une ; le bouton copie le contenu exact du prompt ; la route mène
   au quiz avec le parcours choisi.
2. Les trois écrans, tokens de `DIRECTION-ARTISTIQUE.md`, clavier et
   lecteur d'écran (§7).
3. Compteurs du catalogue calculés depuis `programme/copro.json` et les
   chapitres au build, pas à la main.

## Ce qu'on ne fait pas

- Pas de compte, pas de mot de passe : le lien magique est
  `ACA-JOURNAL-SYNC-1`.
- Pas d'import de fichier dans le navigateur.

## Preuve

```bash
python3 app/tests.py && python3 tooling/check.py
```

JB voit : il entre un pseudo, voit le parcours copropriété et « Créer le
vôtre », copie un prompt, arrive au quiz.

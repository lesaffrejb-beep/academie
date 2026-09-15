# 0055 : le dépôt devient public, Arthur est collaborateur

- Statut : acceptée
- Date : 15/09/2026
- Décideur : JB, demande du 15/09/2026

## Décision

Le dépôt `lesaffrejb-beep/academie` passe de privé à **public**. Arthur
Charrier (`arthurcharrier37@gmail.com`) est ajouté comme collaborateur.

Conséquences voulues : n'importe qui peut cloner le dépôt et installer le
skill sans jeton (`npx skills add`), et Arthur peut jouer son cursus IFSI
depuis son téléphone via l'agent distant de son outil. Le dépôt de
sources reste chez chaque joueur : `sources/` n'est pas versionné, et
l'état joueur `etat/<pseudo>/` reste local et hors git.

La licence ne change pas : code MIT, contenu `banque` CC BY-SA 4.0,
couche `interne` non redistribuable ([`LICENSE.md`](../LICENSE.md),
[`decisions/0018`](0018-licences-du-code-et-du-contenu.md)).

## Contexte

[`decisions/0018`](0018-licences-du-code-et-du-contenu.md) disait « le
dépôt reste privé tant que JB le veut ». Le 15/09, après le retrait du
front ([`decisions/0054`](0054-plus-de-front-le-depot-est-l-interface.md)),
JB veut qu'Arthur et d'autres jouent : un dépôt privé obligerait à un
jeton partout et bloquerait les agents distants.

Un audit de pré-publication a été mené avant le basculement. Aucun
secret, aucune clé, aucun jeton, aucun téléphone, aucun email personnel
(le seul trouvé, `i@izs.me`, est une métadonnée de dépendance), aucune
donnée client. Les PDF de `sources/` ne sont ni suivis ni présents dans
l'historique : seuls `sources/README.md`, `REGISTRE.md`,
`LISTE-BLANCHE.md`, `registre.json` et un `.gitignore` le sont. Aucun
fichier de plus d'un mégaoctet n'est suivi. Le seul fichier jamais
supprimé est l'ancien workflow du front.

## Conséquences

- `project.yaml` passe `classification` à `public`.
- `README.md`, `ARCHITECTURE.md`, `LICENSE.md` et `skills/README.md`
  cessent de dire « privé ».
- L'ajout d'un collaborateur par email se fait dans l'interface GitHub ;
  l'API n'accepte qu'un nom d'utilisateur. Tant que le nom d'Arthur
  n'est pas connu, le dépôt public suffit à le laisser cloner et jouer.
- La CI publique (`.github/workflows/check.yml`) tourne sans secret.

## Réouverture

Si une donnée sensible apparaît dans l'historique, si un usage abusif
justifie de refermer, ou si la licence du contenu change, on rouvre ce
point avant toute nouvelle publication.

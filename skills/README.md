# skills/

Les consignes que l'agent lit pour faire jouer une séance. Un skill est
un dossier avec un `SKILL.md` (frontmatter `name` et `description`), au
standard AgentSkills (`agentskills.io`), repris par les outils de code
et le CLI `npx skills`.

## Ce qu'il y a

| Skill | Quand |
|---|---|
| [`academie/`](academie/SKILL.md) | faire jouer, réviser, se positionner, montrer un QCM (décision 0054) |

## Le point important : le skill n'est pas autonome

Le skill appelle `python3 app/academie.py` et lit `banque/`,
`chapitres/`, `programme/`. Il suppose **le dépôt sous la main** et le
répertoire de travail à sa racine. Installé dans un autre projet, il ne
trouve rien. C'est voulu : l'interface est le dépôt, pas un paquet
détaché.

Le geste normal, pour un collègue :

1. Le dépôt est public depuis le 15/09/2026 : il clone directement.
2. `git clone https://github.com/lesaffrejb-beep/academie.git`
3. Il ouvre l'agent dans ce dossier. La plupart des outils découvrent
   `skills/academie/SKILL.md` tout seuls.

Pour **écrire** dans le dépôt (pas pour jouer), il faut être
collaborateur, ce que JB ajoute depuis l'interface GitHub.

Sur téléphone, on passe par l'agent distant de l'outil (Codex, Claude,
Antigravity) : il faut que cet agent ait accès au dépôt. Le skill est
alors lu depuis le dépôt, sans installation locale.

## Pour les outils qui demandent une installation explicite

Le CLI public est `npx skills` (Vercel). Depuis la racine du dépôt :

    npx skills add lesaffrejb-beep/academie --list
    npx skills add lesaffrejb-beep/academie --skill academie

La première commande liste ce que le dépôt expose sans rien installer ;
la seconde installe le skill dans le dossier de skills de l'agent
(`.agents/skills/`, ou l'équivalent de l'outil). Le dépôt étant public,
aucun jeton n'est nécessaire. Pour tous les agents d'un coup, ajouter
`--all` ; pour un usage sur toute la machine, `-g`.

Après installation, ouvrir une nouvelle session pour que l'agent
redécouvre le skill.

## Licence

Le code, dont ce skill, est MIT ; le contenu de `banque/` est CC BY-SA
4.0 ; la couche `interne` ne se redistribue pas. Détail :
[`LICENSE.md`](../LICENSE.md) et
[`decisions/0018`](../decisions/0018-licences-du-code-et-du-contenu.md).

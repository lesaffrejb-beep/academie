# DESSINER LA CARTE D'UN MÉTIER — la méthode, documentée en la faisant

Créé le 30/08/2026 (brief JB : « tout ce qu'on devra refaire pour
chaque user qui arrive, autant documenter ce qu'on a fait »). Ce
document capitalise la méthode RÉELLEMENT employée pour les deux
premières cartes — copropriété (JB) et concours IFSI (Arthur) — pour
que le prochain domaine se dessine en suivant les pas, pas en
réinventant. Il complète [`USINE.md`](USINE.md) (le parcours guidé
outillé) : USINE dit QUOI faire étape par étape, ce fichier dit
COMMENT ON A TRANCHÉ les choix de conception.

## 1. Trouver les régions (le découpage du territoire)

**La question à poser** : « quelles sont les 5 à 9 grandes zones de
compétence que le métier reconnaît lui-même ? » — pas le sommaire
d'un manuel, les zones qu'un pro nomme quand il parle de son travail.

**Ce qu'on a fait** :
- Copro : 8 régions + Culture, prises du brief terrain de JB (là où
  les manques coûtent : pathologie, équipements, droit, procédure,
  compta, énergie, plans) — PAS du plan de la loi de 1965.
- IFSI : le piège évité — la première région n'est PAS le semestre 1
  du programme, c'est **l'objectif réel du joueur** (le concours,
  échéance mars/avril 2027) ; les UE du S1 deviennent les régions
  suivantes, regroupées (législation-éthique, biologie fondamentale…),
  jamais neuf régions squelettiques.

**Règles qui en sortent** :
1. La région 1 = l'objectif le plus proche du joueur, pas le début
   logique de la matière.
2. Regrouper plutôt qu'éparpiller : une région sans matière est un
   trou de motivation (elle affiche 0 % pour toujours).
3. Culture toujours en `arbre: false`, hors carte.
4. L'ordre (`ordre` de la config) raconte une progression défendable,
   mais la carte reste explorable partout (le moteur le garantit).

## 2. Choisir le lieu-monde (l'habillage)

Chaque métier ancre sa carte dans un LIEU navigable (palais de
mémoire, METHODE §11) : l'immeuble pour la copro (toiture =
étanchéité, chaufferie = P1-P5, la rue = cabinet d'avocat, étude,
mairie), l'hôpital pour l'infirmier (urgences, bloc, pharmacie…).
**La question à poser au joueur** : « quel est LE lieu où ton métier
se passe, et quelles pièces correspondent à quelles compétences ? »
La réponse dessine l'habillage ; le moteur, lui, ne voit que des
régions.

## 3. Calibrer la difficulté et la profondeur

- `niveau` 1-3 aujourd'hui (1 = base, 3 = praticien) ; l'échelle
  s'étendra 1-5 (4 = doctrine/controverse, 5 = recherche/frontière) —
  le bout de chaque branche vise « théoriquement top 5 mondial du
  sujet » (SPEC §3) : on ne déclare jamais une branche « finie » au
  niveau du manuel.
- Les `prerequis` se posent AVEC PARCIMONIE (seulement quand rater la
  carte sans l'autre est certain) : trop de prérequis = un couloir,
  plus une carte.
- Premier lot : ~30 cartes avec une boucle complète battent 300
  cartes sans rituel (arbitrage Q26).

## 4. Le tri des sources (le geste fondateur)

Documenté en vrai deux fois :
- NotebookLM de JB : 278 sources, tri fiable/commercial/douteux, cf.
  `academie/NOTEBOOKLM-A-RETIRER.md` — le modèle du geste.
- IFSI S1 d'Arthur : 141 fichiers, 13 transcriptions exploitables,
  128 audios = trous nommés « à transcrire », support commercial →
  tout dérivé en couche `interne` ; inventaire dans
  `academie/domaines/arthur-ifsi/sources/INVENTAIRE.md`.

**Règles** : la règle du trou nommé (pas de source fiable = pas de
carte, le trou s'écrit) ; paraphrase + article/référentiel cité,
jamais le blog ni la mémoire du modèle ; la couche de partage se
décide PAR SOURCE (public → `banque`, support acquis → `interne`,
vécu → `perso`).

## 5. La fabrication des cartes (mesuré sur les deux premières fois)

- Tous les types dès le premier lot si la matière le permet (flash,
  qcm à distracteurs expliqués, libre, role ; photo/relier/datation/
  plan dès qu'un schéma JUSTE est dessinable — les schémas se
  dessinent en SVG maison, licence interne, jamais volés).
- Tout naît `brouillon`. La double passe par agent frais qui remonte
  aux sources (Légifrance pour le droit, référentiels publics pour la
  technique) est ce qui fait passer en `valide` — le moteur ne sert
  jamais un brouillon en production.
- Le valideur mécanique est le juge de paix : on s'adapte à lui, on
  ne l'affaiblit jamais.

## 6. Ce que ça a coûté (à compléter à chaque domaine)

| Domaine | Sources triées | Cartes lot 1 | Sessions | Coût mesuré |
|---|---|---|---|---|
| Copro (JB) | 278 (NotebookLM, tri fait avant) | 84 (les 8 types) | ~3 sessions d'agents | sur abonnement JB, non chiffré finement |
| IFSI (Arthur) | 141 fichiers (13 exploitables) | 40 | ~2 sessions d'agents | sur abonnement JB (exception bornée, SPEC §2) — la soirée artisanale O7 fera LA mesure |

*Chaque nouveau domaine ajoute sa ligne — c'est cette table qui
transformera un jour la promesse de prix en chiffre honnête.*

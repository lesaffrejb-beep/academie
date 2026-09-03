# 0028, L'état d'un nœud, et la fraîcheur qui ne déclasse pas

- Statut : acceptée
- Date : 03/09/2026
- Décideur : par délégation, au chantier `ACA-ARBRE-1`, sur la doctrine
  de `BLUEPRINT.md` §5 (JB arbitre s'il n'est pas d'accord)

## Le problème

`BLUEPRINT.md` §5 donne six états de nœud dans un tableau, et quatre
règles d'arbre juste en dessous. Deux d'entre elles se contredisent si
on les lit vite :

- l'état **« à revoir »** : « joué, mais pas revu depuis le seuil de
  fraîcheur » ;
- la règle 3 : **« un nœud validé le reste »**.

Un nœud validé le mois dernier et non revu depuis est-il « validé » ou
« à revoir » ? Et si on ajoute des cartes à un nœud validé, son
remplissage tombe : redevient-il « en cours » ?

## Décision

**1. L'état d'un nœud est une seule valeur, calculée dans cet ordre :**

| État | Condition |
|---|---|
| `inconnu` | le nœud n'a aucune carte servie (chapitre `a-ecrire`) |
| `valide` | le nœud a été joué **et** l'épreuve de son domaine est réussie |
| `a-revoir` | joué, jamais validé, et rien de revu depuis `seuil_fraicheur_jours` |
| `solide` | remplissage ≥ `seuil_ouverture_region` |
| `en-cours` | joué, remplissage en dessous |
| `ouvert` | des cartes, jamais joué |

**2. `valide` ne se calcule pas sur le remplissage, mais sur l'épreuve
du domaine**, comme le tableau de `BLUEPRINT.md` §5 le dit
(« validé = épreuve de domaine réussie »). C'est ce qui rend la règle 3
vraie par construction, sans stocker quoi que ce soit : une épreuve
réussie est une ligne du journal append-only, elle ne s'efface jamais.
Ajouter des cartes ou des chapitres ne peut donc pas déclasser un nœud
validé, puisque son état ne dépend pas de son remplissage.

**2 bis. « À revoir » demande deux conditions, pas une.** Le cahier
disait « pas de révision depuis `seuil_fraicheur_jours` ». Pris au pied
de la lettre, ce seuil plat grise au vingt-deuxième jour un nœud dont
les cartes ont un intervalle FSRS de quatre mois : exactement le
contraire de ce que la répétition espacée promet. Un nœud est donc
`a_revoir` quand **le seuil de fraîcheur est dépassé ET qu'au moins une
de ses cartes déjà vue est échue** au sens de FSRS (`du_le` passé). Une
carte jamais vue n'est pas échue : elle est à découvrir.

**3. La fraîcheur ne déclasse jamais un nœud validé.** Elle s'affiche à
côté : chaque nœud porte `a_revoir` (booléen) et
`jours_depuis_derniere_revue`, quel que soit son état. Un nœud validé
et périmé reste `valide` avec `a_revoir: true` : l'écran le grise et le
date (le brouillard à deux couches, règle 4), il ne lui reprend pas son
insigne. L'état `a-revoir` n'est le mot affiché que pour un nœud joué
qui n'a jamais été validé.

**4. Un nœud sans carte est `inconnu`, jamais `ouvert`.** Un chapitre
que personne n'a encore écrit n'est pas « à portée » : c'est une
silhouette. Les 387 chapitres du programme sont dans ce cas aujourd'hui.

**5. Rien de tout cela n'est un verrou.** `jouable` vaut `true` sur tous
les nœuds, sans exception (règle 1). « Fermé », « inconnu », « hors de
portée » sont des mots d'affichage.

## Le rattachement des cartes aux nœuds

Une carte appartient à un nœud par son champ `chapitre` (contrat
carte-v2). Les 84 cartes v1 ne le portent pas encore, et les branches
qu'elles déclarent ne sont pas celles du programme : une seule des dix
correspond. Le rattachement est donc **vide aujourd'hui**, et c'est
`ACA-CONTRAT-2` qui le remplira.

Conséquence assumée : `carte_monde()` compte les cartes non rattachées
et l'écrit (`cartes_sans_chapitre`). Le trou se voit, il ne se devine
pas et il ne bloque pas (`decisions/0021`). Les régions, elles,
continuent de se mesurer par `domaine` comme avant : la carte-monde v1
ne perd rien.

## Conséquences

- `app/progression.py` gagne `etat_noeud`, `noeuds`, `branches`, et
  `carte_monde()` rend `noeuds` et `branches` en plus des `regions`.
- `academie.json` gagne `progression.seuil_fraicheur_jours` (21 jours,
  la même valeur que le seuil de stabilité : ce qui n'est plus mûr est
  ce qu'on n'a pas revu depuis qu'il aurait dû l'être).
- `app/vecteurs_progression.py` fige ces états en fixtures partagées, et
  `web/src/moteur/progression.ts` doit rendre exactement les mêmes.
- L'épreuve de domaine reste hors de ce chantier (`ACA-EXAMEN-1`) : ici
  on lit son résultat au journal, on ne la fabrique pas.

## Réouverture

Si JB, en jouant, trouve qu'un nœud validé mais périmé devrait perdre
son insigne, le point 3 se rouvre : c'est un choix de produit, pas une
contrainte technique. Le bilan de `ACA-RITUAL-1` est le bon moment.

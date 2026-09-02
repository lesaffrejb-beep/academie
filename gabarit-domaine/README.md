# Gabarit de domaine — la coquille vide d'une Académie

Créé le 29/08/2026 (GO de JB, chantier M10 « usine à domaine »).
**Coquilles vides : rien ici n'est du contenu, tout est à remplir.**

Ce dossier est le squelette qu'un nouveau joueur clone pour fabriquer
**son** domaine (un métier, une matière, un concours). Il ne connaît
aucun métier : partout où le vrai contenu manquera, on trouve un
placeholder en majuscules — `[MÉTIER]`, `[RÉGION-1]`, `[URL du
référentiel public]`. Un placeholder laissé en place est un travail
non fait, jamais un défaut acceptable.

Référence : [`../ARCHITECTURE.md`](../ARCHITECTURE.md) §1 (les quatre
pièces, le modèle A4) et §7 (l'usine et la boîte) ;
[`../decisions/0008`](../decisions/0008-chacun-son-depot-et-son-abonnement.md).
Contrat de format des cartes : [`../CONTRAT-CARTE-V1.md`](../CONTRAT-CARTE-V1.md)
(en vigueur) et [`../CONTRAT-CARTE-V2.md`](../CONTRAT-CARTE-V2.md)
(proposé). Les sources de confiance par métier :
[`../sources/LISTE-BLANCHE.md`](../sources/LISTE-BLANCHE.md).

---

## Le modèle A4, en cinq lignes

1. **Tes sources restent chez toi.** Les PDF, cours et annales que tu
   déposes dans `sources/` ne quittent jamais ta machine : ni le
   serveur de jeu, ni un autre joueur ne les voit.
2. **Seules les fiches JSON validées partent** vers le serveur de jeu,
   et seulement quand tu cliques « je publie ma livraison ». Une
   fiche, c'est une paraphrase plus un lien, jamais une recopie.
3. **Le traitement IA tourne chez toi, à ton coût** : l'agent qui lit
   tes sources et fabrique les fiches tourne sur ton abonnement ou ta
   clé. Le serveur n'a aucune clé IA et n'appelle aucun modèle pour toi.
4. **Deux barrières, pas une relecture** : le scanner anti-fuite au
   moment où tu publies, le valideur mécanique à la réception. Rien de
   rouge n'entre en jeu.
5. **Ton état de jeu vit sur le serveur** (deux appareils), ton
   journal de révisions est exportable à tout moment : si l'app
   s'arrête, ton contenu se rejoue ailleurs le lendemain.

## L'ordre des fichiers

| Ordre | Fichier | Ce qu'il porte |
|---|---|---|
| 1 | ce `README.md` | à quoi sert le gabarit, le modèle A4 |
| 2 | [`USINE.md`](USINE.md) | **le guide** : l'étape 0 puis les 7 étapes du parcours. C'est le fichier qu'on déroule avec l'agent. |
| 3 | [`academie.json`](academie.json) | la config du domaine : métier, régions, règles du jeu |
| 4 | [`sources/INVENTAIRE.md`](sources/INVENTAIRE.md) | le tri des sources et **les trous nommés** |
| 5 | [`banque/exemple/exemple.json`](banque/exemple/exemple.json) | une carte d'exemple fictive, à **remplacer**, jamais à publier |
| 6 | `etat/` | vide : le journal de révisions du joueur, jamais versionné |

## Ce qu'on fait de ce dossier

On le **copie** ailleurs (dans son propre dépôt privé), on le renomme,
et on le remplit. On ne travaille pas dedans : ici c'est le moule, pas
la pièce.

```
cp -R academie/gabarit-domaine ~/mon-domaine
```

Trois gestes de renommage à ne pas oublier une fois la copie faite :

- `academie.json` : remplacer `[MÉTIER]`, les `[RÉGION-N]` et le
  profil par défaut par les vraies valeurs ;
- `banque/exemple/` : renommer le dossier avec la clé de la région
  (`banque/region-1/` par exemple). Le nom du dossier n'est qu'une
  convention de rangement ; **c'est le champ `domaine` de chaque carte
  que le valideur contrôle**, et il doit exister dans `academie.json` ;
- `sources/` : y déposer les documents, et vérifier que le
  `.gitignore` du dossier les tient bien hors de git.

## Le valideur

Le gabarit ne contient pas de copie du moteur : on fait pointer le
valideur du dépôt sur son propre dossier, avec `ACADEMIE_RACINE`.

```
ACADEMIE_RACINE=~/mon-domaine python3 app/valide_banque.py
```

Tant que cette commande n'est pas verte, **rien ne se publie**. C'est
le dernier juge, et il n'a pas de dérogation (§ « Les cinq refus » de
`USINE.md`).

> Le gabarit vit **hors** du périmètre de scan de la banque réelle
> (le valideur ne lit que `academie/banque/`). La carte d'exemple ne
> peut donc pas polluer la banque du domaine copro, et c'est voulu.

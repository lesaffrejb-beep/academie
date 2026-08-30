# Domaine « Arthur — concours IFSI, voie FPC »

Première instance réelle du gabarit de domaine, fabriquée le
**29/08/2026** au GO de JB (chantier M10, « usine à domaine »).
Échéance du joueur : **concours d'entrée en IFSI par la voie de la
formation professionnelle continue, mars/avril 2027.**

Ce dossier n'est pas une copie du guide : **le guide reste
[`../../gabarit-domaine/USINE.md`](../../gabarit-domaine/USINE.md)**,
et le modèle A4 reste
[`../../gabarit-domaine/README.md`](../../gabarit-domaine/README.md).
On les ouvre là où ils vivent ; les dupliquer ici garantirait deux
versions divergentes dans six mois.

## Ce qu'il y a dedans

| Fichier | Ce qu'il porte |
|---|---|
| [`academie.json`](academie.json) | la config du domaine : métier, profil, **sept régions**, règles du jeu reprises du gabarit |
| [`sources/INVENTAIRE.md`](sources/INVENTAIRE.md) | le tri des sources, le test de santé, et **les onze trous nommés**. À lire avant toute génération |
| `banque/<region>/<branche>.json` | 35 cartes au contrat carte-v1, **toutes en `brouillon`** |
| `sources/` | vide et versionné vide : les fichiers d'Arthur restent dans `~/Downloads/IFSI S1` |
| `etat/` | vide : le journal de révisions du joueur, jamais versionné |

## Trois choses à savoir avant d'y toucher

1. **Couche `interne`, sans exception.** Les cartes dérivent d'un
   support de cours acquis et non redistribuable : paraphrase
   seulement, jamais de recopie, jamais de distribution externe. Le
   filtre se fait par couche, mécaniquement.
2. **Aucune carte n'est validée.** La double passe par agent frais
   (étape 5 de l'USINE) n'a pas eu lieu. Le générateur ne sert que du
   `valide` : en l'état, ce domaine ne se joue pas encore.
3. **La région qui porte l'échéance est vide.** `concours` n'a aucune
   source dans le tas d'Arthur — c'est le trou n° 1 de l'inventaire,
   et il passe avant l'ajout de toute nouvelle carte.

## Le valideur

```
ACADEMIE_RACINE=academie/domaines/arthur-ifsi python3 academie/app/valide_banque.py
```

Tant que cette commande n'est pas verte, rien ne se publie. Elle est
verte au 29/08/2026 sur 35 cartes.

> Ce domaine vit **hors** du périmètre de scan de la banque du domaine
> copro (le valideur sans `ACADEMIE_RACINE` ne lit que
> `academie/banque/`). Les deux banques ne se polluent pas, et c'est
> voulu.

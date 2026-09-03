# Cahier ACA-CONTENT-MAP-1 : la carte des sources des domaines vides

Résultat attendu : énergie, travaux, immobilier, cabinet et culture
disposent chacun d'une carte de sources primaires, licences,
péremptions et premier lot de chapitres proposé.
Fini quand : inventaire sourcé sans création de carte et sans contenu
labor, avec critères d'abandon de chaque source, lignes ajoutées au
registre.
Dépend de : ACA-PORT-1. Bloque : ACA-CONTENT-2.

## Périmètre

Peut créer ou modifier : `travail/sources-<domaine>-AAAA-MM-JJ.md` (un
par domaine), `sources/REGISTRE.md` et `sources/registre.json` (lignes
ajoutées), `sources/LISTE-BLANCHE.md`, `PROGRAMME.md` §9 (trous nommés
mis à jour), `programme/copro.json` **seulement** pour ajouter un trou
nommé ou une source attendue sur un chapitre.
Ne touche pas : `banque/`, `chapitres/`, le moteur.

## Déjà tranché (ne pas rouvrir)

- Les sources primaires par domaine : `PROGRAMME.md` §2 et §6,
  `sources/LISTE-BLANCHE.md`.
- Une source commerciale n'est pas interdite, elle est `editeur` avec
  son parti ; une carte qui n'a que ça est « à recouper »
  (`decisions/0004`).
- Aucune image d'éditeur ; schémas maison d'abord (`decisions/0017`).
- Le modèle peut chercher sur les domaines fiables et le dire
  (`decisions/0021`).

## Étapes, dans l'ordre

1. Par domaine : lister les branches du programme, et pour chaque
   branche les deux ou trois sources primaires qui la couvrent, avec
   licence, dernière mise à jour connue, et péremption probable.
2. Dire ce qui manque et où le chercher légalement ; écrire les trous
   nommés.
3. Proposer le premier lot : cinq chapitres de niveau 1 par domaine, dans
   l'ordre du programme, avec les sources qui les fonderaient.
4. Ajouter les sources au registre (nature, parti, fiabilité, date).

## Ce qu'on ne fait pas

- Pas de carte, pas de chapitre, pas de leçon.
- Pas de téléchargement en masse ; pas de scraping.
- Pas d'Immocampus ici (couche `interne`, chantier à part).

## Preuve

```bash
python3 tooling/check.py
```

JB voit : cinq inventaires lisibles et, au registre, les nouvelles
lignes.

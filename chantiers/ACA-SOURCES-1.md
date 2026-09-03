# Cahier ACA-SOURCES-1 : le registre des sources et la nature sur chaque carte

Résultat attendu : chaque source des 84 cartes a une ligne au registre
(nature, parti, fiabilité, date) ; chaque carte porte `source[].nature` ;
la liste blanche copro est complète en v1 ; la forme machine
`sources/registre.json` existe.
Fini quand : `sources/REGISTRE.md` sans ligne vide ; zéro carte de
`banque/` sans nature ; `sources/registre.json` valide et cohérent avec
le Markdown ; `app/valide_banque.py` toujours vert (la nature est
tolérée par le contrat v1, exigée par le v2).
Dépend de : ACA-DOC-2. Bloque : ACA-CONTRAT-2.

## Périmètre

Peut créer ou modifier : `sources/REGISTRE.md`, `sources/registre.json`,
`sources/LISTE-BLANCHE.md`, `banque/**/*.json` (ajout du champ `nature`
et, si connu, `parti` sur chaque entrée de `source` ; rien d'autre ne
change dans une carte), `app/valide_banque.py` **seulement** pour
tolérer les champs `nature`, `parti`, `fiabilite`, `empreinte` sur une
source (pas pour les exiger : c'est le v2).
Ne touche pas : les identifiants de cartes, les statuts, les textes des
cartes, `chapitres/`.

## Déjà tranché (ne pas rouvrir)

- La liste fermée des natures et la règle du parti : `decisions/0004`.
- Fiabilité A, B, C : `sources/README.md`.
- Les cartes fondées sur `editeur`, `organisation-pro` ou `association`
  seules porteront « à recouper » (dérivé, pas écrit ici).
- Le tri NotebookLM du 29/08 est la première matière du registre
  (`NOTEBOOKLM-A-RETIRER.md`).

## Étapes, dans l'ordre

1. Test rouge : un script `app/tests_sources.py` qui échoue tant qu'une
   carte a une source sans `nature`, ou qu'une source de carte n'a pas
   de ligne au registre (par domaine web ou par référence).
2. Extraire les sources des 84 cartes (URL, texte), les grouper par
   domaine web, proposer nature et fiabilité par table de domaines,
   relire à la main les cas ambigus (une page d'avocat est `doctrine`,
   un courtier est `editeur`).
3. Écrire `sources/registre.json` (`{source, domaine_web, nature, parti,
   fiabilite, verifie, on_en_tire, on_n_en_tire_pas}`) et régénérer le
   tableau de `REGISTRE.md` depuis le JSON (le JSON fait foi).
4. Assigner `nature` sur chaque source de carte, sans toucher au reste.
5. Compléter `LISTE-BLANCHE.md` avec ce que l'extraction a révélé.

## Ce qu'on ne fait pas

- Pas de jugement sur le fond des cartes : une carte fausse se signale,
  elle ne se corrige pas ici.
- Pas de suppression de source ; une source douteuse reste, notée C.
- Pas de scraping ; pas de téléchargement de sources ici.

## Preuve

```bash
python3 app/tests_sources.py && python3 app/tests.py && python3 tooling/check.py
```

JB voit : le registre lisible, et sur une carte de la banque, la nature
de chaque source.

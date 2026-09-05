# Cahier ACA-RITUAL-1 : les trente séances de JB

Résultat attendu : JB réalise environ trente séances réelles et un test
de rétention à froid de vingt cartes, sans dette ni culpabilisation, et
le bilan est écrit. C'est **le gate** : rien de multi-joueur, rien de
social, aucune décision de comptes ne se prend avant lui
(`ROADMAP.md`, garde-fous de produit).
Fini quand : le bilan `travail/bilan-rituel-AAAA-MM-JJ.md` existe, il
cite la sortie de `python3 app/rituel.py` sur le journal réel, il porte
le score à froid, le verbatim de JB et la décision : continuer,
corriger ou geler.
Dépend de : ACA-PUBLICATION-2 et ACA-RITUAL-METRICS-1. Les sept premières
séances portent aussi l'acceptation réelle du front ; elles font partie
des trente, sans double comptage (0035).
Bloque : ACA-CONTENT-2, ACA-MULTI-DECISION-1, ACA-DOMAIN-KIT-1,
ACA-RESPONSE-1, ACA-OPTIMISEUR-1.

## Mode : `human-only`

Aucun agent ne peut faire ce chantier, et aucun ne doit prétendre
l'avancer. Ce qui se mesure ici, c'est si **une personne ouvre
l'Académie le matin**. Un agent peut préparer l'instrument, lire le
journal et écrire le bilan à partir des chiffres ; il ne peut pas jouer
les séances.

## Ce que la machine fournit déjà

- L'état synchronisé : `serveur/` sur le VPS, le journal append-only,
  l'union par lots, la parité FSRS des deux côtés
  (`ACA-JOURNAL-SYNC-1`).
- Le tableau de bord : `python3 app/rituel.py <journal.jsonl>`
  (`ACA-RITUAL-METRICS-1`). Il donne séances ouvertes, menées au bout,
  laissées en route et à quel rang, durées, formats, jours de la
  semaine, séances par semaine, plus longue coupure. Il ne lit pas le
  contenu des réponses.
- Le journal se sort par `GET /journal/export` (`serveur/API.md`).
- JB a demandé le 04/09 un client v2 propre avant de jouer. Le client
  corrigé et sa mise en service sont donc des prérequis. Un ancien statut
  `done` ou un test local ne prouve pas ce service.

## Périmètre

Peut créer ou modifier : `travail/bilan-rituel-AAAA-MM-JJ.md` (nouveau),
`ROADMAP.md` (le verdict du gate), `lab/VEILLE.md` (ce que le terrain a
appris). Un agent qui aide au dépouillement ne touche à rien d'autre.
Ne touche pas : le journal (lecture seule, jamais réécrit), la banque,
le moteur, le client.

## Déjà tranché (ne pas rouvrir)

- Pas de dette, pas de série qui casse, pas de culpabilisation après
  une coupure (`ROADMAP.md`, garde-fous). Une coupure de trois semaines
  est une donnée du bilan, pas un échec du joueur.
- La preuve recherchée : au moins quatre séances par semaine, une
  séance jouable en moins de trois secondes, terminable à tout moment,
  une réponse jouée dans le tram relisible sur le Mac le soir.
- Aucune télémétrie sortante, aucun tiers (`decisions/0020`) : le bilan
  se fait sur le fichier, à la main.

## Étapes, dans l'ordre

1. JB joue. Environ trente séances, sur quatre semaines au moins, sans
   forcer la régularité pour faire joli : un trou est une donnée.
2. Sortir le journal (`GET /journal/export`) et lancer
   `python3 app/rituel.py journal.jsonl` puis `--json`.
3. Le test de rétention à froid : vingt cartes tirées parmi celles qui
   n'ont pas été revues depuis au moins trois semaines, jouées d'un
   coup, score noté. C'est la mesure du savoir, celle que
   `app/rituel.py` refuse de faire.
4. Écrire `travail/bilan-rituel-AAAA-MM-JJ.md` : les chiffres du
   rapport, le score à froid, la calibration (ce que JB croyait savoir
   contre ce qu'il savait), trois verbatims, et ce qui a fait rater les
   séances manquées.
5. La décision, écrite noir sur blanc : **continuer**, **corriger** (et
   quoi), ou **geler**. Elle ouvre ou ferme `ACA-MULTI-DECISION-1`.

## Ce qu'on ne fait pas

- Pas de séance jouée par un agent, pas de journal fabriqué, pas de
  chiffre estimé : trente séances réelles ou rien.
- Pas de gate déclaré atteint sur une impression. Le rapport fait foi.
- Pas de nouvelle mécanique pendant la mesure : on mesure ce qui est
  servi, on ne le change pas en cours de route.

## Preuve

```bash
python3 app/rituel.py journal.jsonl
python3 app/rituel.py journal.jsonl --json > travail/rituel-AAAA-MM-JJ.json
```

JB voit : ses séances par semaine, sa plus longue coupure, son score à
froid, et la décision qu'il a signée.

# chapitres/

Les chapitres v2 (`CONTRAT-CARTE-V2.md`, `contrats/chapitre-v1.schema.json`),
un objet par fichier, `chapitres/<domaine>/<branche>/<slug>.json`,
l'identifiant du chapitre étant `domaine.branche.slug` et devant exister
dans `programme/copro.json`.

Jugés par `app/valide_chapitres.py` (écrit le 03/09/2026), lancé par
`app/tests.py` et `tooling/check.py`. Un chapitre ou une carte ne se joue
que `valide`, et `valide` exige `verifie_par` (double passe par un agent
frais qui n'a pas écrit).

La banque v1 (`banque/`, tableaux de cartes) reste jugée par
`app/valide_banque.py` et servie par `genere.py` ; les deux dispositions
coexistent jusqu'au chantier `ACA-CONTRAT-2`, qui migre v1 dans v2 et
fait de ce dossier la seule banque. D'ici là, `genere.py` ne lit pas ce
dossier : les chapitres qui s'y trouvent sont écrits, relus et prêts,
pas encore servis.

Premiers chapitres écrits le 03/09/2026 par le modèle (provenance sur
chaque carte), relus par des agents frais le même jour : voir
`travail/lot-pilote-2026-09-03.md`.

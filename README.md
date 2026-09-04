# academie, l'école d'un métier jouée tous les jours

**Reprise du 04/09, publication demandée par JB :** [état livré, limites et suite](travail/2026-09-04-publication-et-suite.md). Ce point actualise les mentions historiques de pause et de publication ci-dessous.

L'Académie transforme des sources vérifiées en un **arbre de
compétences** qu'on conquiert par des exercices de rappel, de
diagnostic et de synthèse, planifiés par un algorithme de mémoire
(FSRS). Premier métier : gestionnaire de copropriété. Premier joueur :
JB. Puis ses collègues, puis Arthur (entrée en IFSI, formation infirmière
et approfondissements sans plafond), puis quiconque
tient un dépôt de sources et un abonnement à un modèle. Personne ne
paie jamais rien.

Conception v2 posée le **02/09/2026** sur le brief de JB
([`travail/2026-09-02-brief-jb.md`](travail/2026-09-02-brief-jb.md)).
La conception d'août est archivée intacte dans
[`archive/conception-2026-08/`](archive/conception-2026-08/README.md).

## Lire, dans cet ordre

| Ordre | Document | Ce qu'il porte |
|---|---|---|
| 1 | [`DOCTRINE.md`](DOCTRINE.md) | ce qu'on est, ce qu'on refuse, les dix invariants, la précédence des documents |
| 2 | [`BLUEPRINT.md`](BLUEPRINT.md) | ce que le joueur vit : séance, étude, journée, l'arbre, le chapitre, les épreuves, la boîte, les cercles |
| 3 | [`PROGRAMME.md`](PROGRAMME.md) et [`programme/copro.json`](programme/copro.json) | ce qu'on enseigne au gestionnaire : dix domaines, branches, 389 chapitres, cinq niveaux, le socle ; l'infirmier a le sien, [`programme/ifsi.json`](programme/ifsi.json) et [`SYLLABUS-IFSI.md`](SYLLABUS-IFSI.md) |
| 4 | [`METHODE.md`](METHODE.md) et [`CADRAGE-SCIENTIFIQUE.md`](CADRAGE-SCIENTIFIQUE.md) | pourquoi chaque mécanique existe, avec sa source vérifiée |
| 5 | [`ARCHITECTURE.md`](ARCHITECTURE.md) | les quatre pièces, où est stocké quoi, le moteur, les contrats, le serveur, l'usine, l'archivage, l'audit, le déploiement |
| 6 | [`DIRECTION-ARTISTIQUE.md`](DIRECTION-ARTISTIQUE.md) | à quoi ça ressemble, les écrans, la barre, le mouvement, l'accessibilité ; maquette : `travail/maquette-2026-09-02.html` |
| 7 | [`ROADMAP.md`](ROADMAP.md) et `roadmap.json` | ce qu'on fait ensuite, avec la preuve attendue |
| 8 | [`decisions/`](decisions/README.md) | les décisions datées et leurs amendements |
| 9 | [`CONTRAT-CARTE-V1.md`](CONTRAT-CARTE-V1.md) (en vigueur), [`CONTRAT-CARTE-V2.md`](CONTRAT-CARTE-V2.md) (proposé), [`contrats/`](contrats/README.md) | les formats, le valideur fait foi |
| 10 | [`gabarit-domaine/`](gabarit-domaine/README.md), [`sources/`](sources/README.md), [`boite/`](boite/README.md), [`CORPUS.md`](CORPUS.md) | fabriquer un domaine, trier ses sources, glisser une idée |
| 11 | [`IDEES-EN-VOL.md`](IDEES-EN-VOL.md), [`lab/VEILLE.md`](lab/VEILLE.md), [`travail/`](travail/) | ce qui n'est pas perdu |
| 12 | [`MODELES.md`](MODELES.md), [`COMMENCER.md`](COMMENCER.md), [`prompts/`](prompts/README.md) | ce qu'un modèle peut et ne peut pas faire ici ; l'arrivée d'un élève et les prompts à coller dans Claude Code, Codex, Antigravity ou Cursor |

## Ce qui existe et ce qui reste à prouver (04/09/2026)

```
  banque/<domaine>/<branche>.json    84 cartes copro (76 valides, 4 signalées, 4 brouillons), contrat carte-v1
        │
  app/valide_banque.py               refuse tout ce qui sort du contrat
        │
  app/genere.py                      publie banque.json (cartes valides, couche banque)
        │
  web/ : build Vite → dist/          client React, arbre, salle, profil, boîte
        │
  VPS à jour                         client transféré ; accès Caddy bloqué par les droits
```

Le moteur Python (`app/`) est la référence : FSRS-6 comparé à
`py-fsrs`, composition de séance, carte de progression, quiz de
positionnement, carnet d'erreurs, tests de contrats et de mutation.

L'usine (`app/usine/`, 03/09/2026) lit un document réel pas à pas :
`preparer` extrait le texte par page et rend les pages à figures,
`declarer` enregistre l'outil et le modèle, `suivant` et `valider`
distribuent et jugent des unités de pages, `fiche` et `registre`
ferment le document. Rien n'est cru sur parole : chaque `suivant`
rejoue les contrôles (`decisions/0027`, `MODELES.md`).

Le serveur d'état, la synchronisation locale, les contrats et valideurs
v2, le programme et le client sont implémentés. Les tests locaux ne
prouvent ni la publication actuelle, ni le trajet réel téléphone–Mac,
ni les sept séances attendues. L'archipel a été archivé le 04/09.

La banque jouable locale reste v1 : aucun de ses 76 éléments n'est encore
rattaché à un chapitre. La préparation de migration est disponible,
mais elle refuse d'inventer auteurs et relecteurs manquants ou de
promouvoir un candidat invalide. Les 11 cartes v2 pilotes sont des
brouillons. Étude, épreuves, journée et cercles restent à construire.

L'[audit du 04/09](travail/audit-froid-2026-09-04.md) donne les preuves,
les écarts et la prochaine unité de chaque chantier. L'ordre exécutable
reste dans `roadmap.json`, expliqué par `ROADMAP.md`.

Les [rapports IFSI, copro et stratégie](travail/rapports-chatgpt-pro/README.md)
sont classés avec leurs originaux locaux, un tri des recommandations et
un plan commun recentré sur l'usage. L'intégration IFSI est terminée
localement : 375 chapitres, 600 capacités de cadrage, syllabus régénéré,
contrôles verts. La [révision copro](travail/2026-09-04-revision-copro.md)
conserve 389 chapitres, précise 34 objectifs et corrige les cartes
concernées ; quatre cartes IRSI/CIDRE sont signalées en attente de source.
Les cinq retouches v1 AG ont été contre-lues avant le push et la banque
a été régénérée. Restent la relecture du chapitre v2 brouillon et la
clôture générale du lot copro.
Les pilotes suivent les gates de rituel et de contenu existants.

## Vérifier

```bash
python3 app/tests.py
```

```bash
python3 tooling/check.py
```

```bash
python3 app/tests.py --mutation
```

## Règles qui ne bougent pas

Aucune donnée client de labor. Aucune carte sans provenance ni nature de source ; aucun chiffre sans source.
Rien de rouge n'est servi. L'état joueur est un journal append-only,
séparé de la banque, jamais dans git. Les actes irréversibles sont
humains. Le détail : `DOCTRINE.md` §3.

# 0007, Le front est jetable et outillé ; le moteur Python reste la référence

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur le brief de JB (« le front peut être fragile mais
  beau, Dribbble, Awwwards, animations » ; « pas peur des dépendances »)

## Décision

- **Moteur de référence** : Python stdlib, tel qu'il existe
  (`app/planificateur.py`, `seance.py`, `progression.py`, `quiz.py`,
  `erreurs.py`, `valide_banque.py`, `genere.py`), avec ses 47 tests et
  ses tests de mutation. Aucune dépendance n'y entre.
- **Serveur d'état** : Python avec un framework HTTP léger accepté
  (FastAPI ou équivalent, épinglé), SQLite en mode WAL, servi par systemd
  derrière Caddy. Justification : cookies, jetons, validation d'entrée et
  erreurs propres sont plus sûrs dans un framework maintenu que réécrits
  en stdlib.
- **Client** : Vite, React, TypeScript, Tailwind, Motion (animations),
  `ts-fsrs` (planification hors-ligne), Dexie (IndexedDB), PWA (Workbox),
  un composant de zoom SVG pour l'arbre, icônes Lucide (ISC) et
  game-icons (CC BY, attribution visible). Le client est **déclaré
  jetable** : il peut être réécrit sans toucher au moteur, à la banque ni
  au journal.
- **Usine** (fabrication locale) : Python + outils libres installés chez
  le joueur : `pdftotext` (poppler), `ocrmypdf`/`tesseract`, `yt-dlp`,
  `faster-whisper`, `genanki`. Aucun de ces outils ne tourne sur le
  serveur.

## Contexte

Le client du 30/08 est 258 lignes de JavaScript sans dépendance. La
roadmap d'août recommandait déjà React + TypeScript + Vite. Le brief du
02/09 lève la réserve sur les dépendances et exige une qualité visuelle
qu'un canvas vanilla n'atteindra pas à coût raisonnable.

## Conséquences

- Toute dépendance porte sa licence vérifiée à la date d'installation
  (`travail/benchmark-2026-08-30.md`, partie 4, sert de registre ; on
  l'étend). AGPL : idées seulement, jamais de code.
- Le contrat entre client et moteur est le JSON publié (`banque.json`),
  le journal (`ARCHITECTURE.md` §5) et l'API d'état. Le client ne lit
  jamais un fichier Python.
- `tooling/check.py` cesse de vérifier l'archipel et vérifie que le
  client compilé n'importe rien de labor.

## Réouverture

Si le bundle client dépasse 400 Ko gzippé ou si le temps jusqu'à la
première question dépasse 3 s sur un téléphone de milieu de gamme, on
coupe des dépendances.

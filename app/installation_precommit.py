#!/usr/bin/env python3
"""Installe le hook pre-commit du garde-fou (ACA-PRECOMMIT-1).

Idempotent : écrit le hook s'il est absent, le remplace s'il a été posé
par ce même script (marque `academie-precommit`), et refuse d'écraser un
hook inconnu. Le hook appelle le garde, qui lit le diff stágé et bloque
sur un motif de donnée client (règle 1, AGENTS.md).

Le dépôt est clone sur un Windows de travail et chez un autre joueur :
le hook est donc un script `sh` sans chemin de machine en dur, il
cherche l'interpréteur à l'exécution (`python3`, puis `python`, puis le
`py` de Windows, puis l'interpréteur qui a posé le hook), il retrouve sa
racine par `git rev-parse --show-toplevel` pour qu'un worktree utilise
son propre `app/`, et le dossier de hooks par `git rev-parse
--git-path` puisque `.git` est un fichier dans un worktree
(chantiers/ACA-PORTABILITE-1.md).
"""

from __future__ import annotations

import argparse
import shutil
import stat
import subprocess
import sys
from pathlib import Path

APPEL = "# academie-precommit\n"
MARQUEUR = "academie-precommit"
INTERPRETEURS = ("python3", "python", "py")

# Windows : une console en cp1252 ne doit pas faire mourir le message
# d'installation sur un accent (ACA-PORTABILITE-1).
for flux in (sys.stdout, sys.stderr):
    if hasattr(flux, "reconfigure"):
        flux.reconfigure(encoding="utf-8", errors="replace")

# Le dépôt documente Python 3.12 (ARCHITECTURE.md, CI). La sonde du hook
# vérifie la version avant d'exécuter le garde : sous Windows, l'alias du
# Microsoft Store porte le nom `python3` sans être un Python utilisable.
VERSION_MINIMALE = (3, 12)
SONDE = ("import sys; raise SystemExit(0 if sys.version_info >= %r else 1)"
         % (VERSION_MINIMALE,))


def citer_sh(texte: str) -> str:
    """Cite une chaîne pour `sh` (les chemins Windows peuvent contenir
    des espaces et des apostrophes)."""
    return "'" + texte.replace("'", "'\\''") + "'"


def chemin_sh(chemin: str | Path) -> str:
    """Un chemin d'interpréteur lisible par Git pour Windows : ses
    barres obliques inverses sont des échappements pour `sh`."""
    return str(chemin).replace("\\", "/")


def interpretes() -> list[str]:
    """Interpréteurs essayés par le hook, du plus portable au plus précis.

    Un nom présent dans le `PATH` ne prouve pas un Python utilisable : le
    hook sonde chaque candidat avant de l'exécuter. Le lanceur `py` de
    Windows n'est pas une commande Python directe ; il est résolu ici en
    un chemin réel.
    """
    trouves = []
    for nom in INTERPRETEURS:
        chemin = shutil.which(nom)
        if not chemin or nom in trouves:
            continue
        if nom == "py":
            reel = interpreteur_du_lanceur(chemin)
            if not reel:
                continue
            chemin = chemin_sh(reel)
        trouves.append(nom if nom != "py" else chemin)
    if sys.executable:
        exact = chemin_sh(sys.executable)
        if exact not in trouves:
            trouves.append(exact)
    return trouves or ["python3", "python"]


def interpreteur_du_lanceur(lanceur: str) -> str:
    """Chemin réel derrière le lanceur `py` de Windows, qui n'accepte pas
    les mêmes arguments qu'un interpréteur."""
    res = subprocess.run([lanceur, "-3", "-c", "import sys; print(sys.executable)"],
                         capture_output=True, text=True, encoding="utf-8",
                         errors="replace")
    return res.stdout.strip() if res.returncode == 0 else ""


def contenu_hook(racine: Path, garde: Path | None = None) -> str:
    """Hook `sh` relogeable : racine et interpréteur résolus au commit."""
    garde = garde or Path(__file__).resolve().parent / "garde_confidentialite.py"
    secours = chemin_sh(garde)
    candidats = " ".join(citer_sh(i) for i in interpretes())
    return ("#!/bin/sh\n"
            + APPEL
            + "# Garde-fou de confidentialité (règle 1, AGENTS.md).\n"
            + "# La racine est relue à chaque commit : un worktree a la sienne.\n"
            + "racine=$(git rev-parse --show-toplevel 2>/dev/null) || racine=''\n"
            + 'garde="$racine/app/garde_confidentialite.py"\n'
            + f"if [ ! -f \"$garde\" ]; then garde={citer_sh(secours)}; fi\n"
            + f"for python in {candidats}; do\n"
            + '  command -v "$python" >/dev/null 2>&1 || continue\n'
            # Un nom qui existe ne prouve pas un Python utilisable : sous
            # Windows, l'alias du Microsoft Store s'ouvre au lieu de
            # répondre. La sonde écarte les leurres et les versions trop
            # anciennes avant tout exec.
            + f'  "$python" -X utf8 -c {citer_sh(SONDE)} >/dev/null 2>&1 || continue\n'
            # exec remplace le processus : un refus du garde (code 1, un
            # motif trouvé) n'est jamais rejoué avec un autre interpréteur.
            + '  PYTHONUTF8="${PYTHONUTF8:-1}" exec "$python" -X utf8 "$garde" "$@"\n'
            + "done\n"
            + 'echo "academie-precommit : aucun interpréteur Python trouvé'
            + ' (python3, python)." >&2\n'
            + "exit 1\n")


def chemin_hook(depot: Path) -> Path | None:
    """Dossier des hooks selon git : dans un worktree, `.git` est un
    fichier et les hooks vivent dans le dépôt principal."""
    res = subprocess.run(["git", "rev-parse", "--git-path", "hooks/pre-commit"],
                         cwd=depot, capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if res.returncode != 0 or not res.stdout.strip():
        return None
    chemin = Path(res.stdout.strip())
    return chemin if chemin.is_absolute() else (depot / chemin)


def installer(depot: Path | None = None) -> int:
    racine = (depot or Path.cwd()).resolve()
    cible = chemin_hook(racine)
    if cible is None:
        print("pas de dépôt git ici", file=sys.stderr)
        return 1
    if cible.is_file():
        texte = cible.read_text(encoding="utf-8", errors="replace")
        if MARQUEUR not in texte and texte.strip():
            print("pre-commit existant non académique : non touché",
                  file=sys.stderr)
            return 1
    if (Path(__file__).resolve().parent / "garde_confidentialite.py").is_file():
        texte = contenu_hook(racine)
    else:
        texte = ("#!/bin/sh\n" + APPEL
                 + "echo 'academie-precommit : garde introuvable' >&2\n"
                 + "exit 1\n")
    cible.parent.mkdir(parents=True, exist_ok=True)
    # Écriture en octets : sous Windows, `write_text` traduirait les
    # sauts de ligne en CRLF et casserait le `#!/bin/sh` du hook.
    cible.write_bytes(texte.encode("utf-8"))
    cible.chmod(cible.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP
                | stat.S_IXOTH)
    print(f"hook installé : {cible}")
    return 0


def main() -> int:
    analyseur = argparse.ArgumentParser(
        description="Installe le hook pre-commit du garde de confidentialité.")
    analyseur.add_argument("--depot", type=Path, default=None,
                           help="racine du dépôt (défaut : dossier courant)")
    args = analyseur.parse_args()
    return installer(args.depot)


if __name__ == "__main__":
    raise SystemExit(main())

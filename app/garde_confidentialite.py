#!/usr/bin/env python3
"""Garde-fou de confidentialité (chantier ACA-PRECOMMIT-1).

La règle 1 d'AGENTS.md interdit tout contact, immeuble, contrat, mail,
réunion ou document client dans ce dépôt. Ce module en fait un filet
mécanique : il lit un diff git (produit par `git diff --cached`) et
signale toute ligne ajoutée qui porte un motif de donnée client. Il
détecte, il ne certifie pas ; un nom d'immeuble ou un scénario sans motif
passe à travers, et l'avoué reste la responsabilité de l'agent.

Usage en hook : `python3 app/precommit_garde.py` (exit 1 et message si
alerte, exit 0 sinon). Voir `app/tests_garde.py`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RE_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,}")
RE_TEL_FR = re.compile(
    r"(?<!\d)(?:0|\+33\s?|33\s?)[1-9](?:[\s.-]?\d{2}){4}(?!\d)")
RE_SIRET = re.compile(r"(?<!\d)\d{3}[\s]?\d{3}[\s]?\d{3}[\s]?\d{5}(?!\d)")
RE_IBAN = re.compile(r"\bFR\d{2}(?:[\s]?\d{4}){5}[\s]?\d{3}\b")
RE_LABOR = re.compile(r"\blabor/(?:outputs|coulisses|domaine)\b|Code/labor\b")

MOTIFS = ("mail", "téléphone", "SIRET", "IBAN", "mention de labor")


def alertes(diff_texte: str) -> list[str]:
    """Liste les alertes d'un texte de diff : lignes ajoutées seulement.

    Chaque alerte dit la règle enfreinte (règle 1, AGENTS.md) et le
    fichier ajouté, pour qu'un blocage s'avoue sans détour.
    """
    fichier = "?"
    m_f = re.match(r"--- a/(\S+)", diff_texte or "")
    if m_f:
        fichier = m_f.group(1)
    trouvées = []
    for ligne in diff_texte.splitlines():
        if not ligne.startswith("+") or ligne.startswith("+++"):
            continue
        corps = ligne[1:]
        heur = None
        if RE_MAIL.search(corps):
            heur = "mail"
        elif RE_TEL_FR.search(corps):
            heur = "téléphone français"
        elif RE_SIRET.search(corps):
            heur = "SIRET"
        elif RE_IBAN.search(corps):
            heur = "IBAN"
        elif RE_LABOR.search(corps):
            heur = "mention de labor"
        if heur:
            trouvées.append(f"règle 1 : {heur} dans {fichier} ({corps.strip()[:50]})")
    return trouvées


def alertes_par_fichier(diff_texte: str) -> list[tuple[str, str]]:
    """(fichier, alerte) pour chaque ligne ajoutée du diff stágé.

    Les fichiers du garde et de ses tests parlent des motifs de la
    règle sans porter de donnée réelle : ils ne se scannent pas
    eux-mêmes, sinon aucun commit du garde ne passerait.
    """
    fichier = "?"
    resultat = []
    exclus = ("app/garde_confidentialite.py", "app/tests_garde.py",
              "app/installation_precommit.py")
    for ligne in diff_texte.splitlines():
        m = re.match(r"\+\+\+ b/(.*)", ligne)
        if m:
            fichier = m.group(1)
            continue
        if fichier in exclus:
            continue
        if ligne.startswith("+") and not ligne.startswith("+++"):
            corps = ligne[1:]
            motifs = [MOTIFS[i] for i, re_ in enumerate(
                (RE_MAIL, RE_TEL_FR, RE_SIRET, RE_IBAN, RE_LABOR))
                if re_.search(corps)]
            for motif in motifs:
                resultat.append((fichier, motif))
    return resultat


def lire_diff_stagé(depot: str | None = None) -> str:
    argv = ["git", "diff", "--cached"]
    return subprocess.run(argv, cwd=depot, capture_output=True,
                          text=True).stdout


def scan_stage(depot: str | None = None) -> int:
    """Sort 1 et imprime les alertes si le diff stágé porte un motif."""
    fichier, paires = "?", alertes_par_fichier(lire_diff_stagé(depot))
    if paires:
        print("ACADÉMIE — règle 1 : une donnée client ne doit pas entrer"
              " dans ce dépôt (AGENTS.md §1).", file=sys.stderr)
        for f, motif in paires:
            print(f"  {motif} repéré dans {f} (ajout)", file=sys.stderr)
        print("Committer quand même : git commit --no-verify (choix humain,",
              file=sys.stderr)
        print("à avouer ensuite). Sinon : modifier le contenu avant commit.",
              file=sys.stderr)
        return 1
    return 0


def main() -> int:
    return scan_stage()


if __name__ == "__main__":
    raise SystemExit(main())

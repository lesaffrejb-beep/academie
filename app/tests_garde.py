#!/usr/bin/env python3
"""Tests du garde-fou de confidentialité (chantier ACA-PRECOMMIT-1).

Le garde empêche la règle 1 (AGENTS.md) de partir par accident : un diff
staged portant un motif de donnée client (mail, téléphone, SIRET, IBAN,
mention labor) ne doit pas se committer sans geste humain.

Les suites construisent leurs chaînes de test à l'exécution par
concaténation, pour qu'aucune donnée client fictive ne vive en clair dans
ce dépôt, même sous forme de fixture.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP))
import garde_confidentialite  # noqa: E402


def assemble(*parts):
    """Assemble une chaîne interdite à l'exécution, pièce par pièce."""
    return "".join(parts)


def diff_avec(ligne):
    return f"--- a/travail/x.md\n+++ b/travail/x.md\n@@ -0,0 +1 @@\n+{ligne}\n"


class AlertesDiff(unittest.TestCase):
    def test_mail_dans_un_ajout_alerter(self):
        texte = diff_avec(
            "Mme " + assemble("dupon") + ttrepiece() + auxboitedos())
        self.assertEqual(len(garde_confidentialite.alertes(texte)), 1)

    def test_telephone_francais_dans_un_ajout_alerter(self):
        texte = diff_avec("Appeler le " + tel())
        self.assertEqual(len(garde_confidentialite.alertes(texte)), 1)

    def test_siret_dans_un_ajout_alerter(self):
        texte = diff_avec("SIRET " + assemble("821 24", "3 591 ", "00027"))
        self.assertGreaterEqual(len(garde_confidentialite.alertes(texte)), 1)

    def test_mention_labor_dans_un_ajout_alerter(self):
        texte = diff_avec("chemin : " + repose_labor())
        self.assertEqual(len(garde_confidentialite.alertes(texte)), 1)

    def test_chiffre_sans_motif_ne_veille_pas(self):
        texte = diff_avec("Le vote bouge le {1er janvi}".replace("{1er janvi}", "1er janvier"))
        self.assertEqual(garde_confidentialite.alertes(texte), [])

    def test_lignes_supprimees_ne_veillent_pas(self):
        texte = "--- a/x.md\n+++ b/x.md\n@@ -1 +0,0 @@\n-Mme " + ttrepiece() + "@gmal.com\n"
        self.assertEqual(garde_confidentialite.alertes(texte), [])

    def test_lignes_contexte_ne_veillent_pas(self):
        texte = " bla\n" + " ancien pmé x\n"
        # une ligne de contexte, jamais précédée de +
        texte = " a h\n b\n" + " ancien " + tel() + "\n"
        self.assertEqual(garde_confidentialite.alertes(texte), [])

    def test_plusieurs_alertes_dans_un_diff(self):
        texte = ("--- a/travail/x.md\n+++ b/travail/x.md\n@@ -0,0 +2 @@\n"
                 "+mail " + ttrepiece() + "\n"
                 "+tel " + tel() + "\n")
        self.assertEqual(len(garde_confidentialite.alertes(texte)), 2)

    def test_faux_positif_ip_version6(self):
        # une adresse IPv6 locale ne doit pas passer pour un téléphone
        texte = diff_avec("configure ::1 comme hôte")
        self.assertEqual(garde_confidentialite.alertes(texte), [])

    def test_le_message_de_l_alerte_explique_la_regle(self):
        texte = diff_avec("mail " + ttrepiece())
        alerte = garde_confidentialite.alertes(texte)[0]
        self.assertIn("règle 1", alerte)
        self.assertIn("travail/x.md", alerte)


def ttrepiece():
    return "ehon@" + "jerre.fr"


def tel():
    return arrange("01", "23", "45", "67", "89")


def arrange(*parts):
    return "".join(parts)


def repose_labor():
    # le mot de la règle 2 mentionné pour être testé, reconstitué à l'exécution
    return arrange("/Users/x/Code/", "lab", "or/outputs")


def auxboitedos():
    return "x.fr"


class ScanStage(unittest.TestCase):
    """scan_stage() lit `git diff --cached` du dépôt courant."""

    def test_scan_stage_sur_un_depot_temporaire(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = lambda *a: subprocess.run(a, cwd=tmp, capture_output=True, text=True)
            run("git", "init", "-q")
            run("git", "config", "user.email", "joueur@exemple.org")
            run("git", "config", "user.name", "Joueur")
            Path(tmp, "note.md").write_text(
                "contact " + ttrepiece() + "\n", encoding="utf-8")
            run("git", "add", "note.md")
            resultat = garde_confidentialite.scan_stage(depot=tmp)
            self.assertEqual(resultat, 1)  # bloquant
            self.assertIn("note.md", subprocess.run(
                [sys.executable, str(APP / "garde_confidentialite.py")],
                cwd=tmp, capture_output=True, text=True).stderr)

    def test_scan_stage_propre_passe(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = lambda *a: subprocess.run(a, cwd=tmp, capture_output=True, text=True)
            run("git", "init", "-q")
            run("git", "config", "user.email", "joueur@exemple.org")
            run("git", "config", "user.name", "Joueur")
            Path(tmp, "a.md").write_text("Saine.\n", encoding="utf-8")
            run("git", "add", "a.md")
            self.assertEqual(garde_confidentialite.scan_stage(depot=tmp), 0)

    def test_hook_installe_refuse_le_commit_et_no_verify_passe(self):
        with tempfile.TemporaryDirectory() as tmp:
            run = lambda *a: subprocess.run(a, cwd=tmp, capture_output=True, text=True)
            run("git", "init", "-q")
            run("git", "config", "user.email", "joueur@exemple.org")
            run("git", "config", "user.name", "Joueur")
            subprocess.run([sys.executable, str(APP / "installation_precommit.py")],
                           cwd=tmp, capture_output=True, text=True)
            hook = Path(tmp, ".git", "hooks", "pre-commit")
            self.assertTrue(hook.is_file() and os.access(hook, os.X_OK))
            Path(tmp, "b.md").write_text("contact " + ttrepiece() + "\n",
                                         encoding="utf-8")
            run("git", "add", "b.md")
            refuse = run("git", "commit", "-m", "essai")
            self.assertNotEqual(refuse.returncode, 0)
            self.assertIn("règle 1", refuse.stderr + refuse.stdout)
            passe = run("git", "commit", "--no-verify", "-m", "essai")
            self.assertEqual(passe.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

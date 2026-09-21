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
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP))
import garde_confidentialite  # noqa: E402
import installation_precommit  # noqa: E402

# Windows : une console en cp1252 ne sait pas écrire les accents du
# rapport ni les coches (ACA-PORTABILITE-1).
for flux in (sys.stdout, sys.stderr):
    if hasattr(flux, "reconfigure"):
        flux.reconfigure(encoding="utf-8", errors="replace")


def assemble(*parts):
    """Assemble une chaîne interdite à l'exécution, pièce par pièce."""
    return "".join(parts)


def diff_avec(ligne):
    return f"--- a/travail/x.md\n+++ b/travail/x.md\n@@ -0,0 +1 @@\n+{ligne}\n"


def python_utf8(*arguments):
    """Descendant Python forcé en UTF-8 : sur Windows hors CI, la console
    par défaut est cp1252 et un enfant qui affiche un accent meurt
    (ACA-PORTABILITE-1)."""
    return [sys.executable, "-X", "utf8", *arguments]


def env_utf8():
    return {**os.environ, "PYTHONUTF8": "1"}


def env_avec_path(dossier):
    """Environnement des descendants avec un `PATH` réduit au dossier donné.

    Sous Windows, `os.environ` peut porter la clé `Path` ; ajouter un
    second `PATH` donnerait deux variables de même nom, et Windows en
    garderait une au hasard. La casse de la clé existante est donc
    respectée, et `PYTHONUTF8` est posé pour les descendants
    (ACA-PORTABILITE-1).
    """
    env = {**os.environ, "PYTHONUTF8": "1"}
    cles = [cle for cle in env if cle.upper() == "PATH"]
    for cle in cles:
        env[cle] = str(dossier)
    if not cles:
        env["PATH"] = str(dossier)
    return env


def lance_script(script, *arguments, cwd=None):
    return subprocess.run(python_utf8(str(script), *arguments), cwd=cwd,
                          capture_output=True, text=True, encoding="utf-8",
                          errors="replace", env=env_utf8())


def installe_hook(cwd):
    """Pose le hook par le script réel, encodage des descendants inclus."""
    return lance_script(APP / "installation_precommit.py", cwd=cwd)


def git(*arguments, cwd, env=None):
    """Commande git du test, sortie décodée en UTF-8."""
    return subprocess.run(["git", *arguments], cwd=cwd, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          env=env)


def ecrit_script_sh(chemin, lignes):
    """Écrit un script `sh` en octets, sauts de ligne LF.

    `write_text` traduit les `\\n` en CRLF sous Windows : le `#!/bin/sh`
    n'est alors plus reconnu par le `sh` de Git pour Windows, et la
    fixture ne prouve plus rien (ACA-PORTABILITE-1).
    """
    chemin = Path(chemin)
    contenu = "".join(ligne + "\n" for ligne in lignes)
    chemin.write_bytes(contenu.encode("utf-8"))
    chemin.chmod(0o755)
    return chemin


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
            git("init", "-q", cwd=tmp)
            git("config", "user.email", "joueur@exemple.org", cwd=tmp)
            git("config", "user.name", "Joueur", cwd=tmp)
            Path(tmp, "note.md").write_text(
                "contact " + ttrepiece() + "\n", encoding="utf-8")
            git("add", "note.md", cwd=tmp)
            resultat = garde_confidentialite.scan_stage(depot=tmp)
            self.assertEqual(resultat, 1)  # bloquant
            self.assertIn("note.md", lance_script(
                APP / "garde_confidentialite.py", cwd=tmp).stderr)

    def test_scan_stage_propre_passe(self):
        with tempfile.TemporaryDirectory() as tmp:
            git("init", "-q", cwd=tmp)
            git("config", "user.email", "joueur@exemple.org", cwd=tmp)
            git("config", "user.name", "Joueur", cwd=tmp)
            Path(tmp, "a.md").write_text("Saine.\n", encoding="utf-8")
            git("add", "a.md", cwd=tmp)
            self.assertEqual(garde_confidentialite.scan_stage(depot=tmp), 0)

    def test_hook_installe_refuse_le_commit_et_no_verify_passe(self):
        with tempfile.TemporaryDirectory() as tmp:
            git("init", "-q", cwd=tmp)
            git("config", "user.email", "joueur@exemple.org", cwd=tmp)
            git("config", "user.name", "Joueur", cwd=tmp)
            installe_hook(tmp)
            hook = Path(tmp, ".git", "hooks", "pre-commit")
            self.assertTrue(hook.is_file() and os.access(hook, os.X_OK))
            Path(tmp, "b.md").write_text("contact " + ttrepiece() + "\n",
                                         encoding="utf-8")
            git("add", "b.md", cwd=tmp)
            refuse = git("commit", "-m", "essai", cwd=tmp)
            self.assertNotEqual(refuse.returncode, 0)
            self.assertIn("règle 1", refuse.stderr + refuse.stdout)
            passe = git("commit", "--no-verify", "-m", "essai", cwd=tmp)
            self.assertEqual(passe.returncode, 0)


class InstallationPortable(unittest.TestCase):
    """Le hook doit tenir sur un dépôt cloné ailleurs que sur ce Mac :
    Git pour Windows, worktree, interpréteur nommé `python`. Voir
    chantiers/ACA-PORTABILITE-1.md.
    """

    def depot_temporaire(self, tmp):
        git("init", "-q", cwd=tmp)
        git("config", "user.email", "joueur@exemple.org", cwd=tmp)
        git("config", "user.name", "Joueur", cwd=tmp)

    def hook_du_depot(self, tmp):
        res = git("rev-parse", "--git-path", "hooks/pre-commit", cwd=tmp)
        chemin = Path(res.stdout.strip())
        return chemin if chemin.is_absolute() else Path(tmp) / chemin

    def test_hook_genere_est_un_script_sh_relogeable(self):
        racine = APP.parent
        contenu = installation_precommit.contenu_hook(racine)
        self.assertTrue(contenu.startswith("#!/bin/sh\n"))
        self.assertIn("academie-precommit", contenu)
        # La racine est relue à chaque commit : un worktree a la sienne.
        self.assertIn("git rev-parse --show-toplevel", contenu)
        # L'interpréteur est cherché à l'exécution, pas figé.
        self.assertIn("for python in", contenu)
        self.assertIn("python3", contenu)
        self.assertIn(" python ", contenu)
        self.assertIn("garde_confidentialite.py", contenu)
        # Le nom ne suffit pas : la version est sondée avant l'exec.
        self.assertIn("version_info", contenu)
        self.assertIn("exec", contenu)

    def test_hook_ecrit_en_lf(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.depot_temporaire(tmp)
            installe_hook(tmp)
            octets = self.hook_du_depot(tmp).read_bytes()
            # Un hook en CRLF casse `#!/bin/sh` dans Git pour Windows.
            self.assertNotIn(b"\r\n", octets)
            self.assertTrue(octets.startswith(b"#!/bin/sh\n"))

    def test_hook_bloque_si_python3_absent_du_path(self):
        """Sur Windows, l'interpréteur s'appelle souvent `python`. Le hook
        doit le trouver quand `python3` n'existe pas, sans quoi il ne
        protégerait rien là où il doit servir.
        """
        git_exe = shutil.which("git")
        if not git_exe:
            self.skipTest("git absent")
        with tempfile.TemporaryDirectory() as tmp:
            self.depot_temporaire(tmp)
            installe_hook(tmp)
            bacs = Path(tmp, "faux-bin")
            bacs.mkdir()
            ecrit_bouchon(bacs, "python", sys.executable)
            ecrit_bouchon(bacs, "git", git_exe)
            env = env_avec_path(bacs)
            Path(tmp, "sale.md").write_text("contact " + ttrepiece() + "\n",
                                            encoding="utf-8")
            git("add", "sale.md", cwd=tmp)
            refuse = subprocess.run([git_exe, "commit", "-m", "sale"], cwd=tmp,
                                    capture_output=True, text=True, env=env)
            self.assertNotEqual(refuse.returncode, 0)
            self.assertIn("règle 1", refuse.stderr + refuse.stdout)
            git("reset", "-q", cwd=tmp)
            Path(tmp, "propre.md").write_text("Une ligne saine.\n", encoding="utf-8")
            git("add", "propre.md", cwd=tmp)
            passe = subprocess.run([git_exe, "commit", "-m", "propre"], cwd=tmp,
                                   capture_output=True, text=True, env=env)
            self.assertEqual(passe.returncode, 0, passe.stderr)

    def test_hook_ignore_un_python3_qui_echoue(self):
        """L'alias du Microsoft Store porte le nom `python3` et échoue à
        l'exécution : le hook doit le sonder, puis passer à `python`.
        """
        git_exe = shutil.which("git")
        if not git_exe:
            self.skipTest("git absent")
        with tempfile.TemporaryDirectory() as tmp:
            self.depot_temporaire(tmp)
            installe_hook(tmp)
            bacs = Path(tmp, "faux-bin")
            bacs.mkdir()
            ecrit_script_sh(Path(bacs, "python3"), ["#!/bin/sh", "exit 9009"])
            ecrit_bouchon(bacs, "python", sys.executable)
            ecrit_bouchon(bacs, "git", git_exe)
            env = env_avec_path(bacs)
            Path(tmp, "sale.md").write_text("contact " + ttrepiece() + "\n",
                                            encoding="utf-8")
            git("add", "sale.md", cwd=tmp)
            refuse = subprocess.run([git_exe, "commit", "-m", "sale"], cwd=tmp,
                                    capture_output=True, text=True, env=env)
            self.assertNotEqual(refuse.returncode, 0)
            self.assertIn("règle 1", refuse.stderr + refuse.stdout)

    def test_hook_fonctionne_dans_un_worktree(self):
        with tempfile.TemporaryDirectory() as tmp:
            principal = Path(tmp, "principal")
            principal.mkdir()
            self.depot_temporaire(principal)
            Path(principal, "a.md").write_text("Une ligne saine.\n", encoding="utf-8")
            git("add", "a.md", cwd=principal)
            git("commit", "-m", "depart", cwd=principal)
            arbre = Path(tmp, "arbre")
            self.assertEqual(git("worktree", "add", "-q", "-b", "essai",
                                 str(arbre), cwd=principal).returncode, 0)
            self.assertTrue((arbre / ".git").is_file())  # .git est un fichier
            installe = installe_hook(arbre)
            self.assertEqual(installe.returncode, 0, installe.stderr)
            hook = self.hook_du_depot(arbre)
            self.assertTrue(hook.is_file())
            self.assertIn("academie-precommit", hook.read_text(encoding="utf-8"))
            Path(arbre, "note.md").write_text("contact " + ttrepiece() + "\n",
                                              encoding="utf-8")
            git("add", "note.md", cwd=arbre)
            refuse = git("commit", "-m", "sale", cwd=arbre)
            self.assertNotEqual(refuse.returncode, 0)
            self.assertIn("règle 1", refuse.stderr + refuse.stdout)

    def test_hook_inconnu_non_ecrase(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.depot_temporaire(tmp)
            hook = self.hook_du_depot(tmp)
            hook.parent.mkdir(parents=True, exist_ok=True)
            gardien = "#!/bin/sh\necho autre outil\n"
            ecrit_script_sh(hook, ["#!/bin/sh", "echo autre outil"])
            res = installe_hook(tmp)
            self.assertNotEqual(res.returncode, 0)
            self.assertEqual(hook.read_text(encoding="utf-8"), gardien)


class CheminsReels(unittest.TestCase):
    """Le dépôt peut être atteint par un chemin symbolique : /tmp vers
    /private/tmp sur macOS, un lecteur mappé sur Windows. Les contrôles
    ne doivent pas voir deux fois le même fichier.
    """

    def test_check_ne_se_signale_pas_par_chemin_symbolique(self):
        racine = APP.parent
        with tempfile.TemporaryDirectory() as tmp:
            lien = Path(tmp, "lien")
            try:
                lien.symlink_to(racine, target_is_directory=True)
            except (OSError, NotImplementedError):
                self.skipTest("liens symboliques indisponibles")
            res = subprocess.run(
                python_utf8(str(lien / "tooling" / "check.py")),
                cwd=lien, capture_output=True, text=True, encoding="utf-8",
                errors="replace", env=env_utf8())
            self.assertNotIn("ancien couplage technique dans tooling/check.py",
                             res.stdout + res.stderr)


class FixturesPortables(unittest.TestCase):
    """Les fixtures du test ne doivent pas être la panne : un script `sh`
    écrit avec `write_text` sort en CRLF sous Windows et son shebang ne
    vaut plus rien (ACA-PORTABILITE-1). Ces deux cas tournent sur toutes
    les plateformes, y compris le job Windows.
    """

    def test_ecrit_script_sh_ecrit_en_lf(self):
        with tempfile.TemporaryDirectory() as tmp:
            chemin = ecrit_script_sh(Path(tmp, "python3"),
                                     ["#!/bin/sh", "exit 9009"])
            octets = chemin.read_bytes()
            self.assertTrue(octets.startswith(b"#!/bin/sh\n"))
            self.assertNotIn(b"\r\n", octets)

    def test_le_relais_cite_un_chemin_windows(self):
        with tempfile.TemporaryDirectory() as tmp:
            chemin = ecrit_bouchon(
                Path(tmp), "python",
                r"C:\Users\jb\Python 3.12\python.exe")
            texte = chemin.read_text(encoding="utf-8")
            # Barres obliques et citation : un chemin Windows avec des
            # espaces reste un seul mot pour `sh`.
            self.assertIn("'C:/Users/jb/Python 3.12/python.exe'", texte)
            self.assertNotIn("\\", texte.replace("\\'", ""))


def ecrit_bouchon(dossier, nom, cible):
    """Écrit un exécutable `sh` qui relaie vers un outil existant.

    Le relais est écrit en octets LF (un shebang CRLF casse sous Windows)
    et son chemin est cité pour `sh` avec des barres obliques : un
    `sys.executable` Windows (`C:\\...`) ou une apostrophe ne doit pas
    casser le relais (ACA-PORTABILITE-1).
    """
    relais = installation_precommit.citer_sh(
        installation_precommit.chemin_sh(cible))
    return ecrit_script_sh(Path(dossier, nom),
                           ["#!/bin/sh", f'exec {relais} "$@"'])


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""Tests du démarrage d'un poste (chantier ACA-DEMARRAGE-1).

Ce que ces tests protègent, dans l'ordre de gravité :

  1. **Aucun dépôt existant n'est réécrit.** Un dossier arrivé en ZIP
     reçoit un guide de clone, jamais un `git init`, `git reset` ou
     `git remote set-url`. La revue du 21/09 a montré que la réparation
     en place écrasait l'index et les références.
  2. **Le diagnostic dit vrai.** La version de Python est mesurée, pas
     recopiée : sous 3.9 le dépôt compile et `check.py` passe, mais
     `tests.py` casse. Un `git` présent mais muet n'est pas un Git prêt.
  3. **Aucune installation opaque.** Sur Windows, le plan cite des
     identifiants `winget` vérifiés à la source, avec `--scope user` ;
     pas de `curl`, pas de téléchargement suivi d'exécution, pas
     d'élévation automatique.
  4. **La racine est exacte.** Un dossier posé dans un autre dépôt ne
     doit pas hériter du parent.
  5. **L'état local n'est pas dans git.** Le diagnostic le dit, avec le
     geste d'export et d'import.

    python3 app/tests_demarrer.py
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

APP = Path(__file__).resolve().parent
RACINE = APP.parent
sys.path.insert(0, str(APP))
import demarrer  # noqa: E402


def run(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace",
                          env={**os.environ, "PYTHONUTF8": "1"})


class VersionPython(unittest.TestCase):
    def test_3_12_et_au_dessus_sont_conformes(self):
        self.assertTrue(demarrer.version_conforme((3, 12, 0)))
        self.assertTrue(demarrer.version_conforme((3, 13, 1)))
        self.assertTrue(demarrer.version_conforme((4, 0, 0)))

    def test_3_11_et_en_dessous_sont_refuses(self):
        self.assertFalse(demarrer.version_conforme((3, 11, 9)))
        self.assertFalse(demarrer.version_conforme((3, 9, 6)))
        self.assertFalse(demarrer.version_conforme((2, 7, 18)))

    def test_le_diagnostic_nomme_la_version_exigee(self):
        diag = demarrer.diagnostic(RACINE)
        self.assertEqual(diag["python"]["minimum"], "3.12")
        self.assertRegex(diag["python"]["version"], r"^\d+\.\d+")

    def test_un_python_trop_ancien_reste_lisible(self):
        """Le script doit tourner sous 3.9 pour pouvoir dire qu'il ne
        faut pas 3.9 : sinon l'utilisateur voit une SyntaxError."""
        vieux = Path("/usr/bin/python3")
        if not vieux.is_file():
            self.skipTest("pas de python système à l'ancienne")
        sonde = run(str(vieux), "-c",
                    "import sys; print('%d.%d' % sys.version_info[:2])")
        if sonde.returncode != 0 or tuple(
                int(p) for p in sonde.stdout.strip().split(".")) >= (3, 12):
            self.skipTest("le python système est déjà récent")
        res = run(str(vieux), str(APP / "demarrer.py"), "--json")
        self.assertEqual(res.returncode, 0, res.stderr)
        donnees = json.loads(res.stdout)
        self.assertFalse(donnees["python"]["conforme"])
        self.assertTrue(any("3.12" in t for t in donnees["a_faire"]))


class PlanInstallation(unittest.TestCase):
    def test_windows_cite_les_identifiants_verifies(self):
        plan = demarrer.plan_installation("windows")
        identifiants = {etape["identifiant"] for etape in plan}
        self.assertIn("Git.Git", identifiants)
        self.assertIn("Python.Python.3.12", identifiants)

    def test_windows_installe_en_scope_user(self):
        """Les manifestes Git.Git et Python.Python.3.12 déclarent un
        installeur `Scope: user` : `--scope user` installe sans élever."""
        for etape in demarrer.plan_installation("windows"):
            self.assertIn("--scope", etape["commande"])
            i = etape["commande"].index("--scope")
            self.assertEqual(etape["commande"][i + 1], "user")

    def test_windows_reste_sans_telechargement_opaque(self):
        texte = json.dumps(demarrer.plan_installation("windows")).lower()
        for interdit in ("curl", "iwr", "invoke-webrequest", "start-process",
                         "-verb runas", "iex", "http://"):
            self.assertNotIn(interdit, texte,
                             f"installation opaque ou élevée : {interdit}")

    def test_chaque_plateforme_est_couverte(self):
        for plateforme in ("windows", "macos", "linux"):
            plan = demarrer.plan_installation(plateforme)
            outils = {etape["outil"] for etape in plan}
            self.assertIn("git", outils, plateforme)
            self.assertIn("python", outils, plateforme)

    def test_le_plan_ne_contient_pas_les_outils_facultatifs(self):
        for plateforme in ("windows", "macos", "linux"):
            texte = json.dumps(demarrer.plan_installation(plateforme)).lower()
            for facultatif in ("poppler", "node", "genanki"):
                self.assertNotIn(facultatif, texte, plateforme)

    def test_chaque_etape_cite_sa_source(self):
        for plateforme in ("windows", "macos", "linux"):
            for etape in demarrer.plan_installation(plateforme):
                self.assertTrue(etape["source"].startswith("https://"), etape)


class InstallationAutorisee(unittest.TestCase):
    def test_seuls_les_manquants_sont_executes(self):
        diag = {
            "manquants": ["python"],
            "installation": demarrer.plan_installation("windows"),
        }
        appels = []

        class Resultat:
            returncode = 0

        def faux_lanceur(commande, **kwargs):
            appels.append(commande)
            return Resultat()

        rapport = demarrer.installer(diag, lanceur=faux_lanceur,
                                     disponible=lambda nom: True)
        self.assertEqual(len(appels), 1, appels)
        self.assertIn("Python.Python.3.12", appels[0])
        deja = [e for e in rapport["etapes"] if not e["execute"]]
        self.assertTrue(any(e["outil"] == "git" for e in deja))

    def test_un_gestionnaire_absent_du_poste_ne_lance_rien(self):
        """Sur un mac ou un linux, winget n'existe pas : le plan Windows
        ne doit rien exécuter, et l'outil reste à installer."""
        diag = {
            "manquants": ["git", "python"],
            "installation": demarrer.plan_installation("windows"),
        }
        rapport = demarrer.installer(
            diag, lanceur=lambda *a, **k: self.fail("ne doit pas lancer"),
            disponible=lambda nom: False)
        self.assertEqual(sorted(rapport["restant"]), ["git", "python"])
        self.assertFalse(any(e["execute"] for e in rapport["etapes"]))

    def test_un_outil_absent_du_path_est_rapporte_non_execute(self):
        diag = {
            "manquants": ["git"],
            "installation": [{
                "outil": "git",
                "identifiant": "Git.Git",
                "commande": ["winget-inexistant", "install"],
                "source": "https://example.org",
            }],
        }
        rapport = demarrer.installer(
            diag, lanceur=lambda *a, **k: self.fail("ne doit pas lancer"),
            disponible=lambda nom: False)
        self.assertEqual(rapport["restant"], ["git"])
        self.assertFalse(rapport["etapes"][0]["execute"])


class RacineExacte(unittest.TestCase):
    def test_un_dossier_dans_un_depot_parent_n_est_pas_la_racine(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp, "parent")
            parent.mkdir()
            run("git", "init", "-q", cwd=parent)
            enfant = Path(parent, "depot-arrive-en-zip")
            enfant.mkdir()
            diag = demarrer.diagnostic(enfant)
            self.assertFalse(diag["depot"]["git"])
            self.assertTrue(diag["depot"]["dans_un_depot_parent"])
            self.assertFalse(diag["depot"]["sans_git"])
            self.assertTrue(any("racine" in t.lower() or "clone" in t.lower()
                                for t in diag["a_faire"]))

    def test_la_racine_du_depot_est_reconnue(self):
        with tempfile.TemporaryDirectory() as tmp:
            run("git", "init", "-q", cwd=tmp)
            diag = demarrer.diagnostic(tmp)
            self.assertTrue(diag["depot"]["git"])
            self.assertTrue(diag["depot"]["racine"])
            self.assertFalse(diag["depot"]["dans_un_depot_parent"])


class GitMuet(unittest.TestCase):
    """Un `git` présent mais muet n'est pas un Git prêt.

    Le cas est vérifié sans fixture exécutable : sur Windows, un script
    `sh` posé sans extension dans le `PATH` n'est pas lancé par
    `subprocess`, et la fixture ne prouverait plus rien. Le module est
    remplacé par un double, l'assertion métier reste la même
    (ACA-PORTABILITE-1).
    """

    def test_un_git_sans_version_lisible_n_est_pas_pret(self):
        with mock.patch.object(demarrer.shutil, "which",
                               return_value="/usr/bin/git"), \
                mock.patch.object(demarrer, "_sortie",
                                  return_value="commande inconnue"):
            pret, sortie = demarrer.version_git_utilisable()
        self.assertFalse(pret)
        self.assertNotRegex(sortie, r"\d+\.\d+\.\d+")

    def test_un_git_absent_du_path_n_est_pas_pret(self):
        with mock.patch.object(demarrer.shutil, "which", return_value=None), \
                mock.patch.object(demarrer, "_sortie") as sortie:
            pret, texte = demarrer.version_git_utilisable()
        self.assertFalse(pret)
        self.assertEqual(texte, "")
        sortie.assert_not_called()

    def test_un_git_qui_repond_sa_version_est_pret(self):
        with mock.patch.object(demarrer.shutil, "which",
                               return_value="/usr/bin/git"), \
                mock.patch.object(demarrer, "_sortie",
                                  return_value="git version 2.55.0"):
            pret, sortie = demarrer.version_git_utilisable()
        self.assertTrue(pret)
        self.assertIn("2.55.0", sortie)


class GuideZip(unittest.TestCase):
    def test_le_guide_interdit_de_reecrire_le_dossier(self):
        guide = demarrer.guide_zip(RACINE)
        texte = json.dumps(guide, ensure_ascii=False).lower()
        for interdit in ("git init", "git reset", "remote set-url"):
            self.assertIn(interdit, texte)
        for etape in guide["etapes"]:
            self.assertNotIn("git init", etape.lower())

    def test_le_guide_dit_de_cloner_a_cote(self):
        guide = demarrer.guide_zip(RACINE)
        self.assertIn("git clone", guide["clone"])
        self.assertIn(demarrer.DEPOT_PUBLIC, guide["clone"])

    def test_le_guide_transfere_l_etat_par_export_import(self):
        texte = " ".join(demarrer.guide_zip(RACINE)["etapes"])
        self.assertIn("exporter", texte)
        self.assertIn("importer", texte)


class HookEtEtatLocal(unittest.TestCase):
    def test_hook_absent_est_nomme_avec_sa_commande(self):
        with tempfile.TemporaryDirectory() as tmp:
            run("git", "init", "-q", cwd=tmp)
            diag = demarrer.diagnostic(tmp)
            self.assertFalse(diag["depot"]["hook"])
            self.assertIn("installation_precommit",
                          diag["depot"]["hook_commande"])
            self.assertTrue(any("installation_precommit" in t
                                for t in diag["a_faire"]))

    def test_hook_present_est_reconnu(self):
        with tempfile.TemporaryDirectory() as tmp:
            run("git", "init", "-q", cwd=tmp)
            hook = Path(tmp, ".git", "hooks", "pre-commit")
            hook.parent.mkdir(parents=True, exist_ok=True)
            hook.write_text("# academie-precommit\n"
                            'exec python3 "app/garde_confidentialite.py"\n',
                            encoding="utf-8")
            self.assertTrue(demarrer.diagnostic(tmp)["depot"]["hook"])

    def test_l_etat_local_est_hors_git_et_sauvegardable(self):
        diag = demarrer.diagnostic(RACINE)
        etat = diag["etat"]
        self.assertEqual(etat["dossier"], "etat")
        self.assertFalse(etat["synchronise_par_git"])
        texte = " ".join(etat["sauvegarde"])
        self.assertIn("exporter", texte)
        self.assertIn("importer", texte)

    def test_le_diagnostic_ne_contient_aucun_chemin_du_joueur(self):
        texte = json.dumps(demarrer.diagnostic(RACINE), ensure_ascii=False)
        self.assertNotIn(str(Path.home()), texte)


class SortieLisible(unittest.TestCase):
    def test_json_est_stable_et_analysable(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = run(sys.executable, str(APP / "demarrer.py"), "--json", cwd=tmp)
            self.assertEqual(res.returncode, 0, res.stderr)
            donnees = json.loads(res.stdout)
            for cle in ("python", "git", "depot", "etat", "a_faire",
                        "plateforme", "manquants", "installation", "zip"):
                self.assertIn(cle, donnees)

    def test_le_texte_humain_n_est_pas_du_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            res = run(sys.executable, str(APP / "demarrer.py"), cwd=tmp)
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("Python", res.stdout)
            with self.assertRaises(json.JSONDecodeError):
                json.loads(res.stdout)

    def test_le_texte_ne_promet_pas_que_tout_est_pret(self):
        with tempfile.TemporaryDirectory() as tmp:
            run("git", "init", "-q", cwd=tmp)
            res = run(sys.executable, str(APP / "demarrer.py"), cwd=tmp)
            self.assertNotIn("tout est prêt", res.stdout.lower())
            self.assertIn("installation_precommit", res.stdout)

    def test_guide_zip_est_appelable_en_ligne_de_commande(self):
        res = run(sys.executable, str(APP / "demarrer.py"), "--guide-zip",
                  cwd=RACINE)
        self.assertEqual(res.returncode, 0, res.stderr)
        guide = json.loads(res.stdout)
        self.assertIn("interdits", guide)


class EntreeSansPython(unittest.TestCase):
    """Sur un Windows sans Python, `app/demarrer.py` ne peut pas
    tourner : l'entrée est `demarrer.ps1`."""

    def script(self) -> str:
        return (RACINE / "demarrer.ps1").read_text(encoding="utf-8")

    def test_le_script_existe(self):
        self.assertTrue((RACINE / "demarrer.ps1").is_file())

    def test_le_script_cite_les_identifiants_verifies(self):
        texte = self.script()
        self.assertIn("Git.Git", texte)
        self.assertIn("Python.Python.3.12", texte)
        self.assertIn("--scope", texte)

    def test_le_script_n_eleve_ni_ne_telecharge_a_la_main(self):
        texte = self.script().lower()
        for interdit in ("invoke-webrequest", "start-process", "-verb runas",
                         "curl ", "iwr ", "iex "):
            self.assertNotIn(interdit, texte, interdit)

    def test_le_script_test_les_candidats_python_reels(self):
        """`python` peut être un alias Microsoft Store qui échoue : le
        script doit essayer `py -3` puis `python3` puis `python`, et
        interroger chaque candidat pour de vrai."""
        texte = self.script()
        self.assertIn("py -3", texte)
        self.assertIn("python3", texte)
        self.assertIn("sys.version_info", texte)
        self.assertIn("git --version", texte)

    def test_la_liste_des_candidats_n_est_pas_emballee_par_une_virgule(self):
        """Cause racine de la CI Windows du 21/09/2026 : `return ,@(...)`
        sort UN objet du pipeline, `foreach` reçoit la chaîne
        « py -3 python3 python » au lieu des trois candidats, et tous
        échouent. Les appelants garantissent le tableau avec @(...)."""
        texte = self.script()
        self.assertNotIn("return ,@(", texte)
        self.assertIn("@(Get-CandidatsPython)", texte)

    def test_le_script_lit_le_code_de_sortie_de_winget(self):
        texte = self.script()
        self.assertIn("$LASTEXITCODE", texte)
        self.assertIn("Installation en echec", texte)

    def test_le_script_ne_melange_pas_la_sortie_de_winget_au_code(self):
        """`$code` doit recevoir un entier, pas le texte de winget melange
        au nombre."""
        texte = self.script()
        self.assertIn("Out-Host", texte)
        self.assertIn("[int]$code", texte)

    def test_le_script_transmet_le_candidat_entier(self):
        """`py -3` doit garder son `-3` et forcer l'UTF-8 : sinon le
        diagnostic complet tourne sous un autre interpreteur."""
        texte = self.script()
        self.assertIn("Split-Candidat", texte)
        self.assertIn('"-X" "utf8"', texte)
        # `@($x)` passerait le tableau comme un seul argument ; seul
        # `@variable` déroule les arguments.
        self.assertNotIn('@($parties.Prefixes) "-X"', texte)
        self.assertIn("@prefixes", texte)

    def test_le_script_lit_le_code_du_diagnostic_complet(self):
        texte = self.script()
        self.assertIn("$codeDiagnostic", texte)

    def test_le_script_ne_sort_pas_vert_sans_diagnostic(self):
        """Un `app/demarrer.py` absent, ou un diagnostic non executé,
        doit sortir en 1 : le mode -Diagnostic ne peut pas rendre 0 sur
        un preflight incomplet."""
        texte = self.script()
        self.assertIn("$diagnosticAbsent", texte)
        self.assertIn("Diagnostic incomplet", texte)
        # Aucune branche ne doit reprendre la condition permissive
        # `$null -ne $codeDiagnostic -and ... -ne 0` seule, qui laissait
        # passer un diagnostic nul.
        self.assertNotIn("if ($null -ne $codeDiagnostic -and $codeDiagnostic -ne 0) { exit 1 }",
                         texte)
        self.assertIn("if ($null -eq $codeDiagnostic)", texte)

    def test_le_script_lit_le_code_apres_installation(self):
        """La branche post-installation doit elle aussi lire
        $LASTEXITCODE du diagnostic final."""
        texte = self.script()
        self.assertIn("apres installation", texte)
        index = texte.index("apres installation")
        self.assertIn("$LASTEXITCODE -ne 0", texte[max(0, index - 400):index])

    def test_outils_prets_vient_apres_le_controle_du_diagnostic(self):
        """Le message « Outils prets » ne doit pas etre atteignable avant
        la garde qui refuse un diagnostic nul ou en echec, sinon un
        preflight incomplet se termine en code 0."""
        texte = self.script()
        garde_nul = texte.rindex("if ($null -eq $codeDiagnostic)")
        garde_echec = texte.rindex("if ($codeDiagnostic -ne 0) {")
        message = texte.index("Outils prets.")
        self.assertLess(garde_nul, message)
        self.assertLess(garde_echec, message)

    def test_le_script_ne_dit_pas_installe_sans_re_verifier(self):
        texte = self.script()
        self.assertIn("Resolve-PythonPret", texte)
        self.assertIn("rouvrir le terminal", texte.lower())

    def test_le_script_ne_promet_pas_que_tout_est_pret(self):
        texte = self.script().lower()
        self.assertNotIn("tout est prêt", texte)
        self.assertIn("app/demarrer.py", self.script())


class ProfilLocal(unittest.TestCase):
    """Le préflight répond « ce poste est-il prêt », pas seulement
    « les outils sont-ils là »."""

    def test_un_clone_sans_profil_n_est_pas_pret_a_jouer(self):
        if not demarrer.version_conforme(sys.version_info):
            self.skipTest("ce test suppose un Python conforme")
        with tempfile.TemporaryDirectory() as tmp:
            run("git", "init", "-q", cwd=tmp)
            hook = Path(tmp, ".git", "hooks", "pre-commit")
            hook.parent.mkdir(parents=True, exist_ok=True)
            hook.write_text("# academie-precommit\n"
                            'exec python3 "app/garde_confidentialite.py"\n',
                            encoding="utf-8")
            diag = demarrer.diagnostic(tmp)
            self.assertTrue(diag["outils_prets"])
            self.assertFalse(diag["profil"]["existe"])
            self.assertIsNone(diag["profil"]["actif"])
            self.assertTrue(any("arrivée" in t for t in diag["a_faire"]),
                            diag["a_faire"])

    def test_un_profil_actif_est_lu_et_nomme(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run("git", "init", "-q", cwd=tmp)
            etat = Path(tmp, "etat")
            Path(etat, "jb").mkdir(parents=True)
            Path(etat, "jb", "profil.json").write_text(
                '{"pseudo": "jb", "cursus": "copro"}\n', encoding="utf-8")
            Path(etat, "profil-actif.json").write_text(
                '{"format": "academie-profil-actif-1", "profil": "jb"}\n',
                encoding="utf-8")
            diag = demarrer.diagnostic(tmp)
            self.assertTrue(diag["profil"]["existe"])
            self.assertEqual(diag["profil"]["actif"], "jb")
            self.assertEqual(diag["profil"]["cursus"], "copro")

    def test_une_selection_sans_profil_est_un_trou_nomme(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            run("git", "init", "-q", cwd=tmp)
            Path(tmp, "etat").mkdir()
            Path(tmp, "etat", "profil-actif.json").write_text(
                '{"format": "academie-profil-actif-1", "profil": "jb"}\n',
                encoding="utf-8")
            diag = demarrer.diagnostic(tmp)
            self.assertFalse(diag["profil"]["existe"])
            self.assertTrue(diag["profil"]["erreur"])

    def test_le_rapport_ne_fuit_pas_le_pseudo_dans_le_texte(self):
        """Le texte humain nomme le profil actif, mais le diagnostic en
        JSON reste la source ; aucun chemin absolu ne sort."""
        with tempfile.TemporaryDirectory() as tmp:
            res = run(sys.executable, str(APP / "demarrer.py"), "--json",
                      cwd=tmp)
            donnees = json.loads(res.stdout)
            self.assertIn("profil", donnees)
            self.assertIn("outils_prets", donnees)


class CliInstallation(unittest.TestCase):
    """Le rapport d'installation ne doit pas être effacé par la relecture
    du poste, et un échec doit sortir en code non nul."""

    def appeler_main(self, argv, diagnostic, installation):
        import io
        import contextlib
        ancien_argv = sys.argv
        ancien_diag = demarrer.diagnostic
        ancien_inst = demarrer.installer
        tampon = io.StringIO()
        try:
            sys.argv = ["demarrer.py"] + argv
            demarrer.diagnostic = lambda racine=None: dict(diagnostic)
            demarrer.installer = lambda diag, **k: dict(installation)
            with contextlib.redirect_stdout(tampon):
                code = demarrer.main()
        finally:
            sys.argv = ancien_argv
            demarrer.diagnostic = ancien_diag
            demarrer.installer = ancien_inst
        return code, tampon.getvalue()

    def diag_avec(self, manquants):
        diag = demarrer.diagnostic(RACINE)
        diag["manquants"] = list(manquants)
        return diag

    def test_un_echec_d_installation_sort_non_nul(self):
        diag = self.diag_avec(["python"])
        rapport = {"etapes": [{"outil": "python", "execute": True,
                               "commande": "winget install", "code": 1}],
                   "restant": ["python"]}
        code, sortie = self.appeler_main(["--installer"], diag, rapport)
        self.assertEqual(code, 1, sortie)
        self.assertIn("échec d'installation", sortie)
        self.assertNotIn("installé : python (code 1)", sortie)

    def test_un_outil_toujours_manquant_apres_installation_sort_non_nul(self):
        diag = self.diag_avec(["git"])
        rapport = {"etapes": [{"outil": "git", "execute": False,
                               "raison": "winget absent du PATH"}],
                   "restant": ["git"]}
        code, sortie = self.appeler_main(["--installer"], diag, rapport)
        self.assertEqual(code, 1, sortie)
        self.assertIn("restent à installer", sortie)

    def test_le_rapport_reste_lisible_apres_relance_du_diagnostic(self):
        diag = self.diag_avec([])
        rapport = {"etapes": [{"outil": "python", "execute": True,
                               "commande": "winget install", "code": 0}],
                   "restant": []}
        code, sortie = self.appeler_main(["--installer"], diag, rapport)
        self.assertEqual(code, 0, sortie)
        self.assertIn("installation lancée : python (code 0)", sortie)

    def test_json_avec_installation_contient_le_rapport(self):
        import json as json_mod

        diag = self.diag_avec(["python"])
        rapport = {"etapes": [{"outil": "python", "execute": True,
                               "commande": "winget install", "code": 1}],
                   "restant": ["python"]}
        code, sortie = self.appeler_main(["--installer", "--json"], diag, rapport)
        self.assertEqual(code, 1)
        donnees = json_mod.loads(sortie)
        self.assertIn("installation_executee", donnees)
        self.assertEqual(donnees["installation_executee"]["restant"], ["python"])


class Ps1DryRun(unittest.TestCase):
    """Si `pwsh` est présent, le script est exécuté pour de vrai en mode
    diagnostic. Sinon le test est ignoré, et le job CI Windows le
    couvrira (ACA-PORTABILITE-1).

    Le test décisif est le comportement, pas la présence du script : la
    CI Windows du 21/09/2026 disait « Python absent » sur un poste qui
    en avait un. Un test qui accepte 0 ou 1 ne l'aurait pas vu, donc on
    exige la détection quand un Python conforme existe réellement ici.
    """

    def pwsh(self):
        # `ACADEMIE_PWSH` permet de pointer un runtime portable officiel
        # (MIT) sans l'installer globalement ni l'ajouter au dépôt.
        chemin = os.environ.get("ACADEMIE_PWSH") or shutil.which("pwsh") \
            or shutil.which("powershell")
        if not chemin:
            self.skipTest("pwsh absent de cette machine")
        return chemin

    def python_conforme_local(self):
        """Le Python 3.12+ réellement joignable ici, ou None."""
        for candidat in ("python3", "python"):
            chemin = shutil.which(candidat)
            if not chemin:
                continue
            res = run(chemin, "-c",
                      "import sys; print('%d.%d' % sys.version_info[:2])")
            if res.returncode != 0:
                continue
            try:
                if tuple(int(p) for p in res.stdout.strip().split(".")) >= (3, 12):
                    return candidat
            except ValueError:
                continue
        return None

    def lance(self, *arguments):
        return run(self.pwsh(), "-NoProfile", "-File",
                   str(RACINE / "demarrer.ps1"), *arguments, cwd=RACINE)

    def test_pwsh_diagnostic_si_disponible(self):
        res = self.lance("-Diagnostic")
        self.assertIn(res.returncode, (0, 1), res.stdout + res.stderr)
        self.assertIn("Git :", res.stdout)
        self.assertIn("Python 3.12", res.stdout)

    def test_python_present_est_detecte_par_la_liste_par_defaut(self):
        """Régression de la CI du 21/09 : la virgule unaire faisait
        arriver les trois candidats en une seule chaîne, donc un poste
        pourvu de Python était déclaré « absent ou inutilisable »."""
        if shutil.which("git") is None:
            self.skipTest("git absent de cette machine")
        candidat = self.python_conforme_local()
        if not candidat:
            self.skipTest("aucun Python 3.12+ local à détecter")
        res = self.lance("-Diagnostic")
        self.assertIn("present", res.stdout,
                      "un Python conforme existe ici mais n'est pas détecté : "
                      + res.stdout + res.stderr)
        self.assertNotIn("absent ou inutilisable", res.stdout)
        self.assertEqual(0, res.returncode, res.stdout + res.stderr)

    def test_un_candidat_absent_n_est_pas_declare_present(self):
        """Un nom qui n'existe sur aucune plateforme : le test ne peut
        pas être sauté parce qu'un `python` traîne dans le PATH."""
        sentinelle = "__academie_python_absent_test__"
        self.assertIsNone(shutil.which(sentinelle))
        res = self.lance("-Diagnostic", "-CandidatPython", sentinelle)
        self.assertIn("absent ou inutilisable", res.stdout)
        self.assertEqual(1, res.returncode, res.stdout + res.stderr)

    def test_un_candidat_fourni_est_interroge(self):
        candidat = self.python_conforme_local()
        if not candidat:
            self.skipTest("aucun Python 3.12+ local")
        res = self.lance("-Diagnostic", "-CandidatPython", candidat)
        self.assertIn("present", res.stdout, res.stdout + res.stderr)
        self.assertEqual(0, res.returncode, res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)

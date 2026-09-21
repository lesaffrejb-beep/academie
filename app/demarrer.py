#!/usr/bin/env python3
"""Le démarrage d'un poste : vérifier, installer, expliquer.

Chantier ACA-DEMARRAGE-1. Le dépôt part sur un Windows de travail
(Antigravity, parfois Codex) et chez un second joueur : au premier
message, l'agent doit savoir ce qui est déjà là, ce qui manque, et
pose le geste. Trois principes :

  1. **On mesure, on ne recopie pas.** L'exigence est Python 3.12.
     Sous 3.9 le dépôt compile et `tooling/check.py` passe, mais
     `app/tests.py` casse (`hashlib.file_digest`, `datetime.fromisoformat`
     avec suffixe `Z`). Le diagnostic lit la version réelle, et un Git
     présent mais muet n'est pas un Git prêt.
  2. **L'humain a déjà dit oui, une fois.** JB a autorisé l'installation
     au premier message : `--installer` exécute le plan du poste. Ce qui
     reste interdit, c'est le téléchargement opaque et l'élévation
     automatique : sur Windows on passe par `winget --scope user`, qui
     installe pour l'utilisateur sans élever les droits.
  3. **Le dépôt du joueur n'est jamais réécrit.** Un dossier arrivé en
     ZIP n'est pas « réparé » en place : on clone le dépôt à côté et on
     transfère l'état privé par `exporter` puis `importer`. Aucun
     `git init`, `git reset` ou `git remote set-url` ne touche un
     dossier existant.

Ce fichier reste lisible par Python 3.9 : un poste trop ancien doit
lire la raison, pas une `SyntaxError`. Sur un Windows sans Python, le
point d'entrée est `demarrer.ps1`, à la racine du dépôt.

    python3 app/demarrer.py
    python3 app/demarrer.py --json
    python3 app/demarrer.py --installer
    python3 app/demarrer.py --guide-zip
"""

from __future__ import annotations

import argparse
import json
import platform as plateforme_mod
import re
import shutil
import subprocess
import sys
from pathlib import Path

VERSION_MINIMUM = (3, 12)
VERSION_MINIMUM_TEXTE = "3.12"
MARQUE_HOOK = "academie-precommit"
COMMANDE_HOOK = "python3 app/installation_precommit.py"
DEPOT_PUBLIC = "https://github.com/lesaffrejb-beep/academie.git"
NOM_SELECTION = "profil-actif.json"
COMMANDE_ACCUEIL = "python3 app/academie.py accueil --json"

# Identifiants lus dans microsoft/winget-pkgs le 21/09/2026 :
#   manifests/g/Git/Git/2.55.0/Git.Git.installer.yaml
#     PackageIdentifier: Git.Git, avec un installeur `Scope: user`.
#   manifests/p/Python/Python/3/12/3.12.9/Python.Python.3.12.installer.yaml
#     PackageIdentifier: Python.Python.3.12, avec un installeur `Scope: user`.
SOURCE_GIT = "https://github.com/microsoft/winget-pkgs/tree/master/manifests/g/Git/Git"
SOURCE_PYTHON = ("https://github.com/microsoft/winget-pkgs/tree/master/"
                 "manifests/p/Python/Python/3/12")
SOURCE_MANUEL_PYTHON = "https://www.python.org/downloads/windows/"

RE_VERSION_GIT = re.compile(r"(\d+)\.(\d+)\.(\d+)")


def version_conforme(version_info) -> bool:
    """Python 3.12+ est le plancher réel du dépôt, pas un confort."""
    return tuple(version_info)[:2] >= VERSION_MINIMUM


def plateforme_courante() -> str:
    nom = plateforme_mod.system().lower()
    if nom.startswith("win"):
        return "windows"
    if nom == "darwin":
        return "macos"
    return "linux"


def plan_installation(plateforme: str) -> list:
    """Le plan d'installation d'un poste.

    Chaque étape porte son identifiant vérifié à la source et sa
    commande exacte. Sur Windows, `--scope user` évite l'élévation ;
    on ne télécharge jamais un exécutable pour le lancer ensuite. Les
    outils facultatifs de l'usine (poppler, Node, l'export Anki) n'y
    figurent pas : jouer une séance n'en a besoin d'aucun.
    """
    if plateforme == "windows":
        return [
            {
                "outil": "git",
                "identifiant": "Git.Git",
                "commande": ["winget", "install", "--id", "Git.Git",
                             "--scope", "user", "--source", "winget",
                             "--accept-package-agreements",
                             "--accept-source-agreements"],
                "source": SOURCE_GIT,
            },
            {
                "outil": "python",
                "identifiant": "Python.Python.3.12",
                "commande": ["winget", "install", "--id",
                             "Python.Python.3.12", "--scope", "user",
                             "--source", "winget",
                             "--accept-package-agreements",
                             "--accept-source-agreements"],
                "source": SOURCE_PYTHON,
            },
        ]
    if plateforme == "macos":
        return [
            {
                "outil": "git",
                "identifiant": "git",
                "commande": ["brew", "install", "git"],
                "source": "https://formulae.brew.sh/formula/git",
            },
            {
                "outil": "python",
                "identifiant": "python@3.12",
                "commande": ["brew", "install", "python@3.12"],
                "source": "https://formulae.brew.sh/formula/python@3.12",
            },
        ]
    return [
        {
            "outil": "git",
            "identifiant": "git",
            "commande": ["sudo", "apt", "install", "-y", "git"],
            "source": "https://git-scm.com/download/linux",
        },
        {
            "outil": "python",
            "identifiant": "python3.12",
            "commande": ["sudo", "apt", "install", "-y", "python3.12"],
            "source": "https://docs.python.org/3/using/unix.html",
        },
    ]


def _sortie(*commande, cwd=None) -> str:
    try:
        res = subprocess.run(list(commande), cwd=cwd, capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    except OSError:
        return ""
    if res.returncode != 0:
        return ""
    return (res.stdout or "").strip()


def version_git_utilisable() -> tuple:
    """Un `git` dans le PATH ne suffit pas : il doit répondre.

    Un binaire cassé, un alias de coquille ou un `git` masqué rendent
    une version vide. Sans numéro lisible, Git n'est pas prêt.
    """
    if shutil.which("git") is None:
        return False, ""
    sortie = _sortie("git", "--version")
    if not RE_VERSION_GIT.search(sortie):
        return False, sortie
    return True, sortie


def racine_depot(racine: Path) -> str:
    """La racine du dépôt, et elle seule.

    Un dossier peut être posé dans un autre dépôt (téléchargements,
    `~/Code`) : `--show-toplevel` renverrait alors le parent, et le
    diagnostic parlerait du mauvais projet. On ne considère le dossier
    comme dépôt que si la racine rendue est bien celle demandée.
    """
    sommet = _sortie("git", "rev-parse", "--show-toplevel", cwd=racine)
    if not sommet:
        return ""
    try:
        return str(Path(sommet).resolve())
    except OSError:
        return ""


def chemin_hook(racine: Path):
    """Le fichier de hook du dépôt, worktree compris.

    Dans un worktree `.git` est un fichier, pas un dossier : seul
    `git rev-parse --git-path` sait où vit le hook.
    """
    chemin = _sortie("git", "rev-parse", "--git-path", "hooks/pre-commit",
                     cwd=racine)
    if chemin:
        p = Path(chemin)
        return p if p.is_absolute() else Path(racine) / p
    return Path(racine) / ".git" / "hooks" / "pre-commit"


def hook_present(racine: Path) -> bool:
    fichier = chemin_hook(racine)
    try:
        texte = fichier.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return MARQUE_HOOK in texte and "garde_confidentialite" in texte


def profil_local(racine: Path) -> dict:
    """Le profil actif de la machine, lu sans rien écrire.

    Le préflight répond à « ce poste est-il prêt », pas seulement
    « les outils sont-ils là » : un clone neuf avec Git et Python mais
    sans profil n'a pas encore d'arrivée, et le dire évite de confondre
    outils prêts et joueur prêt. Aucun chemin absolu ne sort d'ici.
    """
    etat = Path(racine) / "etat"
    fichier = etat / NOM_SELECTION
    actif = None
    erreur = ""
    if fichier.is_file():
        try:
            donnees = json.loads(fichier.read_text(encoding="utf-8"))
            actif = donnees.get("profil")
        except (OSError, json.JSONDecodeError, AttributeError):
            erreur = "sélection locale illisible"
    if not actif:
        return {
            "actif": None,
            "existe": False,
            "cursus": None,
            "erreur": erreur,
            "commande": COMMANDE_ACCUEIL,
        }
    prefs = etat / str(actif) / "profil.json"
    if not prefs.is_file():
        return {
            "actif": str(actif),
            "existe": False,
            "cursus": None,
            "erreur": "profil actif sans profil.json",
            "commande": COMMANDE_ACCUEIL,
        }
    try:
        donnees = json.loads(prefs.read_text(encoding="utf-8"))
        cursus = donnees.get("cursus")
    except (OSError, json.JSONDecodeError, AttributeError):
        return {
            "actif": str(actif),
            "existe": True,
            "cursus": None,
            "erreur": "profil local illisible",
            "commande": COMMANDE_ACCUEIL,
        }
    return {
        "actif": str(actif),
        "existe": True,
        "cursus": cursus,
        "erreur": "",
        "commande": "python3 app/academie.py profil --json",
    }


def guide_zip(racine=None) -> dict:
    """Ce qu'on dit à un dossier arrivé en ZIP.

    On ne réécrit jamais ce dossier : un `git init` suivi d'un `reset`
    écraserait l'index et les références de quelqu'un qui a déjà
    travaillé, et un ZIP ancien ferait disparaître les fichiers neufs de
    la vue git. On clone le dépôt à côté et on transfère l'état privé.
    """
    racine = Path(racine) if racine is not None else Path.cwd()
    return {
        "dossier": "à côté, jamais dans le dossier existant",
        "etapes": [
            "cloner le dépôt public dans un dossier voisin",
            "poser le hook dans le clone : " + COMMANDE_HOOK,
            "transférer l'état privé depuis le dossier existant : "
            "python3 app/academie.py exporter <fichier>",
            "réimporter dans le clone : python3 app/academie.py importer <fichier>",
        ],
        "clone": "git clone %s academie" % DEPOT_PUBLIC,
        "interdits": [
            "git init dans le dossier existant",
            "git reset ou git remote set-url dans le dossier existant",
            "git pull dans un dossier qui n'est pas un clone du dépôt",
        ],
        # Chemin relatif seulement : le rapport se relit sans exposer
        # l'arborescence du joueur.
        "etat_conserve": "etat/",
        "raison": "le dossier du joueur n'est jamais réécrit par un outil",
    }


def diagnostic(racine=None) -> dict:
    """Ce que l'agent doit savoir avant de promettre quoi que ce soit.

    Aucun chemin absolu du poste ne sort d'ici : le rapport se relit
    sans exposer le nom du joueur ni son arborescence.
    """
    racine = Path(racine) if racine is not None else Path.cwd()
    try:
        racine = racine.resolve()
    except OSError:
        pass
    plateforme = plateforme_courante()
    version = "%d.%d.%d" % sys.version_info[:3]
    conforme = version_conforme(sys.version_info)
    git_pret, git_version = version_git_utilisable()
    sommet = racine_depot(racine) if git_pret else ""
    est_racine = bool(sommet) and Path(sommet) == racine
    dans_un_depot = bool(sommet) and not est_racine
    hook = hook_present(racine) if est_racine else False
    profil = profil_local(racine) if est_racine else {
        "actif": None, "existe": False, "cursus": None, "erreur": "",
        "commande": COMMANDE_ACCUEIL,
    }

    manquants = []
    if not git_pret:
        manquants.append("git")
    if not conforme:
        manquants.append("python")

    outils_prets = not manquants
    a_faire = []
    if not git_pret:
        a_faire.append("installer Git puis rouvrir le terminal")
    if not conforme:
        a_faire.append(
            "installer Python %s ou plus récent (version trouvée : %s)"
            % (VERSION_MINIMUM_TEXTE, version))
    # La liste est additive : sur un poste trop ancien, le hook et
    # l'arrivée restent nommés. Un rapport qui tait une action à cause
    # d'une autre ferait croire à un poste plus prêt qu'il ne l'est.
    if not est_racine:
        if dans_un_depot:
            a_faire.append(
                "ce dossier n'est pas la racine du dépôt : se placer à "
                "la racine d'un clone de l'Académie (un dépôt parent a "
                "été trouvé et n'est pas utilisé)")
        else:
            a_faire.append(
                "ce dossier n'est pas un clone git : cloner le dépôt "
                "public dans un dossier voisin, jamais réparer celui-ci "
                "en place (voir --guide-zip)")
    else:
        if not hook:
            a_faire.append("poser le hook pre-commit : " + COMMANDE_HOOK)
        if not profil["existe"]:
            a_faire.append(
                "faire l'arrivée une fois (pseudo, cursus, voix, exigence) : "
                + COMMANDE_ACCUEIL)

    return {
        "version": 1,
        "plateforme": plateforme,
        "outils_prets": bool(outils_prets),
        "python": {
            "nom": "python3",
            "version": version,
            "minimum": VERSION_MINIMUM_TEXTE,
            "conforme": conforme,
        },
        "git": {
            "present": git_pret,
            "version": git_version,
        },
        "depot": {
            "git": est_racine,
            "racine": est_racine,
            "dans_un_depot_parent": dans_un_depot,
            "sans_git": not sommet,
            "hook": bool(hook),
            "hook_commande": COMMANDE_HOOK,
        },
        "etat": {
            "dossier": "etat",
            "synchronise_par_git": False,
            "sauvegarde": [
                "python3 app/academie.py exporter <fichier>",
                "python3 app/academie.py importer <fichier>",
            ],
            "raison": "l'état du joueur vit hors git et ne suit pas un git pull",
        },
        "profil": profil,
        "manquants": manquants,
        "a_faire": a_faire,
        "installation": plan_installation(plateforme),
        "zip": guide_zip(racine),
    }


def texte(diag: dict) -> str:
    """Le même rapport, pour un humain. Il ne dit jamais que tout est
    prêt quand une action précise reste à faire."""
    lignes = []
    lignes.append("Démarrage de l'Académie")
    etat_python = "conforme" if diag["python"]["conforme"] else "trop ancien"
    lignes.append("Python %s : %s (minimum %s)"
                  % (diag["python"]["version"], etat_python,
                     diag["python"]["minimum"]))
    if diag["git"]["present"]:
        lignes.append("Git : %s" % (diag["git"]["version"] or "présent"))
    else:
        lignes.append("Git : absent ou sans réponse")
    if diag["depot"]["git"]:
        lignes.append("Dépôt git : oui, à la racine")
        lignes.append("Hook pre-commit : %s"
                      % ("posé" if diag["depot"]["hook"] else "à poser"))
    elif diag["depot"]["dans_un_depot_parent"]:
        lignes.append("Dépôt git : non (dossier posé dans un autre dépôt)")
    else:
        lignes.append("Dépôt git : non (dossier arrivé en ZIP)")
    lignes.append("État local : %s/ (hors git, non synchronisé entre "
                  "machines)" % diag["etat"]["dossier"])
    for commande in diag["etat"]["sauvegarde"]:
        lignes.append("  sauvegarde : %s" % commande)
    profil = diag.get("profil", {})
    if profil.get("existe"):
        lignes.append("Profil actif : %s (cursus %s)"
                      % (profil.get("actif"),
                         profil.get("cursus") or "aucun"))
    elif diag["outils_prets"]:
        lignes.append("Profil actif : aucun (l'arrivée n'a pas encore été faite)")
    if diag["a_faire"]:
        lignes.append("À faire :")
        for action in diag["a_faire"]:
            lignes.append("  - %s" % action)
    else:
        lignes.append("Préflight terminé : outils, hook et profil sont "
                      "en place.")
        lignes.append("Prochain geste : python3 app/academie.py etat")
    return "\n".join(lignes) + "\n"


def installer(diag: dict, lanceur=None, disponible=None) -> dict:
    """Exécuter le plan du poste pour les outils manquants.

    L'autorisation est explicite : JB a demandé que les outils
    s'installent au premier message. On n'exécute que les étapes dont
    l'outil manque, avec les identifiants vérifiés à la source, et on
    rapporte le code de sortie réel. Sur Windows `--scope user` évite
    l'élévation ; ailleurs une étape qui a besoin de `sudo` le dit.
    """
    lanceur = lanceur or subprocess.run
    disponible = disponible or (lambda nom: shutil.which(nom) is not None)
    rapport = {"etapes": [], "restant": []}
    manquants = set(diag["manquants"])
    for etape in diag["installation"]:
        if etape["outil"] not in manquants:
            rapport["etapes"].append(
                {"outil": etape["outil"], "execute": False,
                 "raison": "déjà installé"})
            continue
        commande = etape["commande"]
        if not disponible(commande[0]):
            rapport["etapes"].append(
                {"outil": etape["outil"], "execute": False,
                 "raison": "%s absent du PATH" % commande[0]})
            rapport["restant"].append(etape["outil"])
            continue
        res = lanceur(commande, capture_output=True, text=True,
                      encoding="utf-8", errors="replace")
        rapport["etapes"].append(
            {"outil": etape["outil"], "execute": True,
             "commande": " ".join(commande), "code": res.returncode})
        if res.returncode != 0:
            rapport["restant"].append(etape["outil"])
    return rapport


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Vérifier le poste avant de jouer (ACA-DEMARRAGE-1).")
    ap.add_argument("--json", action="store_true", help="rapport lisible par un agent")
    ap.add_argument("--racine", default=".", help="dépôt à inspecter")
    ap.add_argument("--installer", action="store_true",
                    help="installer les outils manquants (autorisé au premier message)")
    ap.add_argument("--guide-zip", action="store_true",
                    help="les étapes pour un dossier arrivé en ZIP, sans le réécrire")
    args = ap.parse_args()
    if args.guide_zip:
        print(json.dumps(guide_zip(Path(args.racine)),
                         ensure_ascii=False, indent=1))
        return 0
    donnees = diagnostic(Path(args.racine))
    installation = None
    if args.installer:
        installation = installer(donnees)
        # On relit le poste après l'installation : un gestionnaire de
        # paquets qui sort 0 sans rien poser doit se voir ici, pas dans
        # une promesse. Le rapport d'installation reste joint.
        donnees = diagnostic(Path(args.racine))
        donnees["installation_executee"] = installation
    if args.json:
        print(json.dumps(donnees, ensure_ascii=False, indent=1))
    else:
        sys.stdout.write(texte(donnees))
        if installation is not None:
            for etape in installation["etapes"]:
                if not etape.get("execute"):
                    continue
                if etape.get("code") == 0:
                    print("installation lancée : %s (code 0)"
                          % etape["outil"])
                else:
                    print("échec d'installation : %s (code %s)"
                          % (etape["outil"], etape.get("code")))
            if installation["restant"]:
                print("restent à installer : %s"
                      % ", ".join(installation["restant"]))
            elif donnees["manquants"]:
                print("outils encore manquants après installation : %s"
                      % ", ".join(donnees["manquants"]))
    if installation is not None and (
            installation["restant"] or donnees["manquants"]):
        # Un code de sortie nul ferait croire que le poste est prêt.
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

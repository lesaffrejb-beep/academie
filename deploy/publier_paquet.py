#!/usr/bin/env python3
"""Livraison Académie construite sur Mac, VPS sans Node (ACA-PUBLICATION-2).

Sans --appliquer, contrôle seulement l'archive dans un répertoire temporaire.
Avec --appliquer, exécuter en root sur le VPS après revue du SHA et du paquet.
Ne modifie aucune unité systemd ni configuration Caddy. Ne restaure jamais SQLite.
"""
from __future__ import annotations
from contextlib import closing
from datetime import datetime, timezone
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import sqlite3
import subprocess
import tarfile
import tempfile
import time
import urllib.request
from verifier_migration import compare

REPO = Path("/home/academie/repo")
PUBLICATION = Path("/var/lib/academie/publication")
BASE = Path("/var/lib/academie/etat.sqlite")
SAUVEGARDES = Path("/var/lib/academie/sauvegardes")
VERROU = Path("/run/lock/academie-publication-20260905.lock")
REQUIS = {"index.html", "sw.js", "registerSW.js", "manifest.webmanifest", "icone.svg",
          "banque.json", "voix.json", "catalogue.json", "cours.json", "reprise.html", "reprise.js", ".vite/manifest.json", "version-source.json"}


def empreinte(chemin: Path) -> str:
    h = hashlib.sha256()
    with chemin.open("rb") as fichier:
        for morceau in iter(lambda: fichier.read(1024 * 1024), b""):
            h.update(morceau)
    return h.hexdigest()


def relatif(nom: str) -> str:
    if not isinstance(nom, str) or not nom or "\\" in nom or "\x00" in nom or nom.startswith("/"):
        raise ValueError("Chemin de paquet refusé")
    if any(p in ("", ".", "..") for p in nom.split("/")):
        raise ValueError("Chemin de paquet refusé")
    return nom


def extraire(archive: Path, cible: Path, digest: str) -> None:
    if empreinte(archive) != digest:
        raise ValueError("Digest de l'archive différent")
    with tarfile.open(archive, "r:*") as tar:
        entrees = []
        connus = set()
        for membre in tar.getmembers():
            nom = membre.name[2:] if membre.name.startswith("./") else membre.name
            if nom in ("", ".") and membre.isdir():
                continue
            nom = relatif(nom.rstrip("/") if membre.isdir() else nom)
            if nom in connus or membre.size < 0 or not (membre.isfile() or membre.isdir()):
                raise ValueError("Lien, doublon ou fichier spécial refusé dans l'archive")
            connus.add(nom)
            entrees.append((nom, membre))
        tailles = sum(m.size for _, m in entrees if m.isfile())
        if tailles * 2 > shutil.disk_usage(cible.parent).free:
            raise ValueError("Espace temporaire insuffisant pour extraire et contrôler")
        # Toutes les entrées sont contrôlées avant la première création.
        cible.mkdir(mode=0o700)
        for nom, membre in entrees:
            chemin = cible / nom
            if membre.isdir():
                chemin.mkdir(parents=True, exist_ok=True)
            else:
                chemin.parent.mkdir(parents=True, exist_ok=True)
                with closing(tar.extractfile(membre)) as source, chemin.open("xb") as sortie:
                    shutil.copyfileobj(source, sortie)


def verifier(source: Path, sha: str, expected_lessons: int, *, exact: bool = True) -> list[str]:
    manifeste = json.loads((source / "publication-manifeste.json").read_text())
    if manifeste.get("version") != 1 or not isinstance(manifeste.get("fichiers"), list):
        raise ValueError("Manifeste invalide")
    noms = [relatif(f["chemin"]) for f in manifeste["fichiers"]]
    if len(noms) != len(set(noms)) or not REQUIS.issubset(noms):
        raise ValueError("Manifeste incomplet ou doublonné")
    presents = {str(p.relative_to(source)) for p in source.rglob("*") if p.is_file() and p.relative_to(source) != Path("publication-manifeste.json")}
    if any(p.is_symlink() for p in source.rglob("*")) or (exact and presents != set(noms)):
        raise ValueError("Fichiers non déclarés ou liens dans le paquet")
    for ligne in manifeste["fichiers"]:
        if empreinte(source / ligne["chemin"]) != ligne["sha256"]:
            raise ValueError(f"Empreinte différente : {ligne['chemin']}")
    if json.loads((source / "version-source.json").read_text()).get("commit") != sha:
        raise ValueError("Le paquet n'annonce pas le commit demandé")
    vite = json.loads((source / ".vite/manifest.json").read_text())
    for entree in vite.values():
        if any(relatif(n) not in noms for n in [entree["file"], *entree.get("css", []), *entree.get("assets", [])]):
            raise ValueError("Ressource Vite manquante")
        if any(cle not in vite for cle in [*entree.get("imports", []), *entree.get("dynamicImports", [])]):
            raise ValueError("Import Vite manquant")
    banque = json.loads((source / "banque.json").read_text())
    cartes = {c["id"] for c in banque.get("cartes", [])}
    lecons = banque.get("etudes", {}).get("lecons", {})
    if len(lecons) != expected_lessons:
        raise ValueError("Nombre d'études différent du paquet attendu")
    for lecon in lecons.values():
        if lecon.get("statut") != "valide" or not lecon.get("cartes") or not set(lecon["cartes"]).issubset(cartes):
            raise ValueError("Une étude n'a pas ses cartes publiées")
    for carte in banque.get("cartes", []):
        if (carte.get("image") or {}).get("fichier") and relatif(carte["image"]["fichier"]) not in noms:
            raise ValueError("Support image absent")
    return noms


def commande(*args: str, acceptable: tuple[int, ...] = (0,)) -> str:
    resultat = subprocess.run(args, text=True, capture_output=True)
    if resultat.returncode not in acceptable:
        # Les journaux d'une commande peuvent contenir du contexte privé.
        raise RuntimeError(f"Commande refusée ({resultat.returncode}) : {args[0]}")
    return resultat.stdout.strip()


def git(*args: str) -> str:
    return commande("sudo", "-u", "academie", "git", "-C", str(REPO), *args)


def actif(unite: str) -> bool:
    return commande("systemctl", "is-active", unite, acceptable=(0, 3)) == "active"


def copie_atomique(source: Path, cible: Path) -> None:
    compte = pwd.getpwnam("academie")
    dossier = PUBLICATION
    for segment in cible.parent.relative_to(PUBLICATION).parts:
        dossier = dossier / segment
        if not dossier.exists():
            dossier.mkdir(mode=0o750)
            os.chown(dossier, compte.pw_uid, compte.pw_gid)
            commande("setfacl", "-m", "u:caddy:r-x,d:u:caddy:r-x", str(dossier))
    fd, temporaire = tempfile.mkstemp(prefix=".academie-livraison-", dir=cible.parent)
    try:
        with os.fdopen(fd, "wb") as sortie, source.open("rb") as entree:
            shutil.copyfileobj(entree, sortie)
            sortie.flush()
            os.fsync(sortie.fileno())
        os.chown(temporaire, compte.pw_uid, compte.pw_gid)
        os.chmod(temporaire, 0o644)
        commande("setfacl", "-m", "u:caddy:r--", temporaire)
        os.replace(temporaire, cible)
    finally:
        if os.path.exists(temporaire):
            os.unlink(temporaire)


def distribuer(source: Path, noms: list[str]) -> None:
    # Les cibles existantes doivent rester de vrais chemins dans publication.
    for nom in noms:
        chemin = PUBLICATION / relatif(nom)
        courant = chemin
        while True:
            if courant.is_symlink():
                raise ValueError("Lien existant refusé dans publication")
            if courant == PUBLICATION:
                break
            courant = courant.parent
    ordre = [n for n in noms if n not in ("index.html", "sw.js")]
    ordre += ["publication-manifeste.json", "index.html", "sw.js"]
    for nom in dict.fromkeys(ordre):
        copie_atomique(source / nom, PUBLICATION / nom)


def sante() -> None:
    for _ in range(30):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8790/academie/api/v1/sante", timeout=1) as reponse:
                if json.load(reponse).get("ok"):
                    return
        except (OSError, ValueError):
            pass
        time.sleep(.2)
    raise ValueError("Santé API incorrecte après attente du démarrage")


def publier(source: Path, noms: list[str], args) -> None:
    if os.geteuid() != 0:
        raise ValueError("L'application distante exige root")
    if git("status", "--porcelain"):
        raise ValueError("Clone distant modifié : aucune livraison")
    precedent = git("rev-parse", "HEAD")
    if not actif("academie-etat.service") or actif("academie-publication.service"):
        raise ValueError("API inactive ou génération en cours : réexaminer avant livraison")
    taille = sum(p.stat().st_size for p in PUBLICATION.rglob("*") if p.is_file())
    taille += sum(p.stat().st_size for p in source.rglob("*") if p.is_file()) * 2 + BASE.stat().st_size * 3
    if shutil.disk_usage(SAUVEGARDES).free < taille + args.reserve_mib * 1024 * 1024:
        raise ValueError("Espace insuffisant pour conserver le retour arrière et la réserve")
    git("fetch", "origin", "main")
    git("cat-file", "-e", args.sha + "^{commit}")
    git("merge-base", "--is-ancestor", precedent, args.sha)
    git("merge-base", "--is-ancestor", args.sha, "origin/main")
    timer = actif("academie-publication.timer")
    sauvegarde = SAUVEGARDES / ("avant-" + args.sha[:12] + "-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    sauvegarde.mkdir(mode=0o700)
    commande("systemctl", "stop", "academie-publication.timer")
    if actif("academie-publication.service"):
        raise ValueError("Une génération a commencé : timer suspendu, réexaminer")
    api_ouverte = False
    code_change = False
    sauvegarde_prete = False
    try:
        commande("systemctl", "stop", "academie-etat.service")
        with closing(sqlite3.connect(BASE)) as origine, closing(sqlite3.connect(sauvegarde / "etat.sqlite")) as copie:
            origine.backup(copie)
        compare(sauvegarde / "etat.sqlite", BASE)
        shutil.copytree(PUBLICATION, sauvegarde / "publication", symlinks=False)
        (sauvegarde / "ancien-sha.txt").write_text(precedent + "\n")
        (sauvegarde / "timer-actif.txt").write_text(str(timer) + "\n")
        (sauvegarde / "acl.txt").write_text(commande("getfacl", "-R", "-p", str(PUBLICATION), str(BASE), str(PUBLICATION.parent)))
        for unite in ("academie-etat.service", "academie-publication.service", "academie-publication.timer"):
            (sauvegarde / unite).write_text(commande("systemctl", "cat", unite))
        shutil.copy2("/etc/caddy/Caddyfile", sauvegarde / "Caddyfile")
        sauvegarde_prete = True
        code_change = True
        git("merge", "--ff-only", args.sha)
        if git("rev-parse", "HEAD") != args.sha or git("status", "--porcelain"):
            raise ValueError("Clone différent de la version demandée")
        with closing(sqlite3.connect(BASE)) as conn:
            migrations = {r[0] for r in conn.execute("SELECT nom FROM migrations")}
        attendues = {p.name for p in (REPO / "serveur/migrations").glob("[0-9][0-9][0-9][0-9]_*.sql")}
        if not migrations.issubset(attendues) or attendues - migrations - {"0003_acces_local.sql"}:
            raise ValueError("Migration autre que 0003 : examen spécifique requis")
        commande("sudo", "-u", "academie", "env", "PYTHONDONTWRITEBYTECODE=1", "PYTHONPATH=" + str(REPO / "serveur"),
                 "python3", "-c", "from academie_etat.db import connecter; c=connecter('/var/lib/academie/etat.sqlite'); c.close()")
        comptes = compare(sauvegarde / "etat.sqlite", BASE)
        with closing(sqlite3.connect(BASE)) as conn:
            if {r[0] for r in conn.execute("SELECT nom FROM migrations")} != attendues:
                raise ValueError("Migrations non conformes au code")
        distribuer(source, noms)
        verifier(PUBLICATION, args.sha, args.expected_lessons, exact=False)
        for nom in noms:
            commande("sudo", "-u", "caddy", "test", "-r", str(PUBLICATION / nom))
        for voisin in (BASE, Path(str(BASE) + "-wal"), Path(str(BASE) + "-shm"), SAUVEGARDES):
            if voisin.exists() and subprocess.run(["sudo", "-u", "caddy", "test", "-r", str(voisin)], capture_output=True).returncode == 0:
                raise ValueError("Un voisin privé est lisible par Caddy")
        # Dès cet appel, de nouvelles écritures sont possibles : aucun retour automatique.
        api_ouverte = True
        commande("systemctl", "start", "academie-etat.service")
        sante()
        with urllib.request.urlopen("http://127.0.0.1:8790/academie/api/v1/auth/comptes", timeout=5) as reponse:
            if not isinstance(json.load(reponse).get("comptes"), list):
                raise ValueError("Le point d'entrée des comptes n'est pas disponible")
        if timer:
            commande("systemctl", "start", "academie-publication.timer")
        print(json.dumps({"sha": args.sha, "fichiers": len(noms), "etudes": args.expected_lessons,
                          "tables_conservees": comptes, "sauvegarde": str(sauvegarde),
                          "api": "active", "https_authentifie": "à vérifier au navigateur"}, ensure_ascii=False))
    except Exception:
        commande("systemctl", "stop", "academie-publication.timer")
        if api_ouverte:
            print("Échec après ouverture API : conserver nouveau code/client/base et timer suspendu ; diagnostiquer sans restaurer SQLite.")
        elif sauvegarde_prete and code_change:
            # 0003 ajoute seulement des colonnes ; les anciennes données doivent rester identiques.
            compare(sauvegarde / "etat.sqlite", BASE)
            if git("rev-parse", "HEAD") != args.sha or git("status", "--porcelain"):
                raise RuntimeError("Modification concurrente : retour automatique refusé")
            git("checkout", "--detach", precedent)
            anciens = [str(p.relative_to(sauvegarde / "publication")) for p in (sauvegarde / "publication").rglob("*") if p.is_file()]
            distribuer(sauvegarde / "publication", anciens)
            commande("systemctl", "start", "academie-etat.service")
            sante()
            print("Ancien code/client rétablis ; base courante conservée, timer suspendu pour diagnostic.")
        else:
            commande("systemctl", "start", "academie-etat.service")
            print("Aucun nouveau code servi ; timer suspendu pour diagnostic.")
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--digest", required=True)
    parser.add_argument("--expected-lessons", type=int, required=True)
    parser.add_argument("--reserve-mib", type=int, default=128, help="Réserve opérationnelle, pas une promesse de capacité")
    parser.add_argument("--appliquer", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.sha) or not re.fullmatch(r"[a-f0-9]{64}", args.digest) or args.expected_lessons < 1 or args.reserve_mib < 1:
        parser.error("SHA, digest, nombre d'études ou réserve invalides")
    os.umask(0o077)
    try:
        with tempfile.TemporaryDirectory(prefix="academie-livraison-") as travail:
            source = Path(travail) / "paquet"
            extraire(args.archive, source, args.digest)
            noms = verifier(source, args.sha, args.expected_lessons)
            if not args.appliquer:
                print(json.dumps({"paquet_verifie": True, "sha": args.sha, "fichiers": len(noms), "etudes": args.expected_lessons}))
                return 0
            with VERROU.open("a") as verrou:
                fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
                publier(source, noms, args)
        return 0
    except Exception as erreur:
        print(f"Livraison interrompue : {type(erreur).__name__} : {erreur}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

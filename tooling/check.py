#!/usr/bin/env python3
"""Contrôles structurels du dépôt Académie : ce que la doctrine interdit et
qu'une machine peut voir (CONTRIBUER.md §3, decisions/0025).

Chaque contrôle est une fonction qui ajoute des erreurs à une liste. Le
script sort 1 dès qu'une erreur existe. Un contrôle qui bloque un chantier
légitime se discute par décision ; il ne se contourne pas.
"""
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RE_OLD_REPO = re.compile(r"erp/app/etude|wiki-copro-sergic|\.claude/skills")
# Vocabulaire du jeu et de l'archipel, interdit dans ce que le produit affiche (VOIX.md §3).
RE_MOTS_INTERDITS = re.compile(
    r"\b(quête|quêtes|boss|combo|streak|streaks|niveau up|coffre|coffres|monnaie|avatar|avatars"
    r"|île|îles|phare|phares|archipel|expédition|expéditions|bateau|bateaux)\b", re.I)
RE_EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F900-\U0001F9FF]")
RE_CHANTIER = re.compile(r"\bACA-[A-Z]+(?:-[A-Z]+)*-\d+\b")
RE_IMPORT_LABOR = re.compile(r"(?:^|\n)\s*(?:from|import)\s+(?:labor|erp)\b|['\"](?:\.\./)+(?:labor|erp)/", re.M)

# Documents v2 où le tiret cadratin est interdit (règle de la maison).
DOCS_V2 = ["DOCTRINE.md", "BLUEPRINT.md", "PROGRAMME.md", "ARCHITECTURE.md", "DIRECTION-ARTISTIQUE.md",
           "ROADMAP.md", "README.md", "AGENTS.md", "CONTRIBUER.md", "VOIX.md", "CONTRAT-CARTE-V2.md", "SYLLABUS.md"]
DOSSIERS_V2 = ["decisions", "chantiers", "contenu", "chapitres", "sources", "boite", "serveur", "web",
               "programme", "contrats"]
# Ce que le produit affiche : voix contrôlée (exclamation, emoji, mots interdits).
DOSSIERS_VOIX = ["contenu", "chapitres", "web"]


def fichiers(dossiers, suffixes):
    for d in dossiers:
        p = ROOT / d
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if f.is_file() and f.suffix in suffixes and "node_modules" not in f.parts:
                yield f


def lit(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def controle_fichiers_requis(errors):
    for required in ("AGENTS.md", "CLAUDE.md", "DOCTRINE.md", "CONTRIBUER.md", "VOIX.md", "project.yaml",
                     "ROADMAP.md", "roadmap.json", "context/giverny.md", "decisions/README.md",
                     "client/index.html", "client/style.css", "client/app.js", "client/sw.js",
                     "deploy/academie-publication.service", "deploy/academie-publication.timer",
                     "contenu/voix.json", "contenu/citations.json", "programme/copro.json"):
        if not (ROOT / required).is_file():
            errors.append(f"fichier requis absent : {required}")


def controle_json(errors):
    cibles = ["project.yaml", "roadmap.json", "academie.json"]
    cibles += [rel(f) for f in fichiers(["contrats", "programme", "contenu", "chapitres"], {".json"})]
    for r in cibles:
        try:
            json.loads((ROOT / r).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{r} invalide : {exc}")


def controle_ancien_couplage(errors):
    for path in ROOT.rglob("*"):
        if path == Path(__file__) or not path.is_file() or ".git" in path.parts or "node_modules" in path.parts:
            continue
        if path.suffix not in {".md", ".py", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js"}:
            continue
        if RE_OLD_REPO.search(lit(path)):
            errors.append(f"ancien couplage technique dans {rel(path)}")
    tracked = subprocess.run(["git", "ls-files", ".claude"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if tracked:
        errors.append(".claude ne doit pas être versionné")


def controle_client_archipel(errors):
    """L'archipel reste servi tant qu'ACA-FRONT-2 ne l'a pas remplacé (cahier)."""
    client = "\n".join(lit(ROOT / "client" / n) for n in ("index.html", "style.css", "app.js", "sw.js"))
    if re.search(r"(?:^|[/'\"])(?:erp|etude)(?:[/'\"]|$)", client, re.MULTILINE | re.IGNORECASE):
        errors.append("le client Académie ne doit importer ni ERP ni Etude")
    for marker in ('id="archipel"', 'id="phare"', 'id="routes"', 'id="iles"'):
        if marker not in client:
            errors.append(f"archipel autonome incomplet : marqueur absent {marker}")
    if "academie-v2" not in lit(ROOT / "client" / "sw.js"):
        errors.append("le cache du client n'a pas été invalidé pour l'archipel")


def controle_roadmap(errors):
    try:
        data = json.loads((ROOT / "roadmap.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    items = data.get("items", [])
    ids = {i["id"] for i in items}
    for i in items:
        for d in i.get("depends_on", []):
            if d not in ids:
                errors.append(f"roadmap : {i['id']} dépend d'un item inconnu {d}")
        if i.get("status") == "ready" and not (ROOT / "chantiers" / f"{i['id']}.md").is_file():
            errors.append(f"roadmap : {i['id']} est ready sans cahier chantiers/{i['id']}.md (decisions/0025)")
    prets = [i["id"] for i in items if i.get("status") == "ready"]
    if len(prets) > 15:
        errors.append(f"roadmap : {len(prets)} items ready, quinze au plus")
    # Chantiers cités dans les documents : ils existent.
    cites = set()
    for f in ROOT.rglob("*.md"):
        if ".git" in f.parts or "archive" in f.parts or "node_modules" in f.parts:
            continue
        cites |= set(RE_CHANTIER.findall(lit(f)))
    for c in sorted(cites - ids):
        errors.append(f"chantier cité sans item dans roadmap.json : {c}")


def controle_decisions(errors):
    index = lit(ROOT / "decisions" / "README.md")
    fichiers_dec = sorted(p.name for p in (ROOT / "decisions").glob("[0-9][0-9][0-9][0-9]-*.md"))
    for nom in fichiers_dec:
        if f"({nom})" not in index:
            errors.append(f"decisions/README.md n'indexe pas {nom}")
    for lien in re.findall(r"\]\((\d{4}-[^)]+\.md)\)", index):
        if not (ROOT / "decisions" / lien).is_file():
            errors.append(f"decisions/README.md indexe un fichier absent : {lien}")


def controle_programme(errors):
    for f in (ROOT / "programme").glob("*.json"):
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        chapitres = p.get("chapitres", [])
        ids = {}
        for ch in chapitres:
            if ch["id"] in ids:
                errors.append(f"{rel(f)} : identifiant de chapitre dupliqué {ch['id']}")
            ids[ch["id"]] = ch
        domaines = p.get("domaines", {})
        branches = p.get("branches", {})
        for ch in chapitres:
            if ch["domaine"] not in domaines:
                errors.append(f"{rel(f)} : {ch['id']} dans un domaine non déclaré")
            if ch["branche"] not in {b["cle"] for b in branches.get(ch["domaine"], [])}:
                errors.append(f"{rel(f)} : {ch['id']} dans une branche non déclarée")
            for pre in ch.get("prerequis", []):
                if pre not in ids:
                    errors.append(f"{rel(f)} : {ch['id']} a un prérequis inconnu {pre}")
                elif ids[pre]["niveau"] > ch["niveau"]:
                    errors.append(f"{rel(f)} : {ch['id']} a un prérequis de niveau supérieur ({pre})")
        # pas de cycle
        etat = {}
        def visite(cid, pile):
            if etat.get(cid) == 1:
                errors.append(f"{rel(f)} : cycle de prérequis via {cid}")
                return
            if etat.get(cid) == 2:
                return
            etat[cid] = 1
            for pre in ids.get(cid, {}).get("prerequis", []):
                if pre in ids:
                    visite(pre, pile + [cid])
            etat[cid] = 2
        for cid in ids:
            visite(cid, [])


def controle_tirets(errors):
    cibles = [ROOT / d for d in DOCS_V2 if (ROOT / d).is_file()]
    cibles += list(fichiers(DOSSIERS_V2, {".md", ".json", ".sql", ".ts", ".tsx"}))
    for f in cibles:
        txt = lit(f)
        if "—" in txt:
            n = txt.count("—")
            errors.append(f"tiret cadratin dans {rel(f)} ({n})")


def controle_voix(errors):
    """Ce que le produit affiche : pas d'exclamation, pas d'emoji, pas de mot du jeu (VOIX.md §4)."""
    cibles = list(fichiers(DOSSIERS_VOIX, {".json", ".ts", ".tsx", ".md"})) + [ROOT / "VOIX.md"]
    for f in cibles:
        if f.name == "README.md":
            continue
        txt = lit(f)
        if f.suffix == ".json":
            try:
                data = json.loads(txt)
            except json.JSONDecodeError:
                continue
            # On ne juge que les chaînes affichées, pas les clés ni les URL.
            def chaines(o):
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k in ("_", "url", "fichier", "empreinte", "id", "chapitre", "session", "modele"):
                            continue
                        yield from chaines(v)
                elif isinstance(o, list):
                    for v in o:
                        yield from chaines(v)
                elif isinstance(o, str):
                    yield o
            txt = "\n".join(chaines(data))
        if "!" in txt and f.suffix in {".json"}:
            errors.append(f"point d'exclamation dans un texte affiché : {rel(f)}")
        if RE_EMOJI.search(txt):
            errors.append(f"emoji dans un texte affiché : {rel(f)}")
        m = RE_MOTS_INTERDITS.search(txt)
        if m and f.name != "VOIX.md":
            errors.append(f"mot du jeu ou de l'archipel « {m.group(0)} » dans {rel(f)} (VOIX.md §3)")


def controle_contenu(errors):
    try:
        voix = json.loads((ROOT / "contenu" / "voix.json").read_text(encoding="utf-8"))
        for cle, variantes in voix.get("textes", {}).items():
            if not isinstance(variantes, list) or len(variantes) < 3:
                errors.append(f"contenu/voix.json : la clé {cle} n'a pas trois variantes (VOIX.md §5)")
        cit = json.loads((ROOT / "contenu" / "citations.json").read_text(encoding="utf-8"))
        for c in cit.get("citations", []):
            for champ in ("texte", "auteur", "oeuvre", "date"):
                if not c.get(champ):
                    errors.append(f"contenu/citations.json : citation sans {champ} : {c.get('texte', '?')[:40]}")
    except (OSError, json.JSONDecodeError):
        pass


def controle_imports(errors):
    for f in fichiers(["app", "serveur", "web", "client"], {".py", ".ts", ".tsx", ".js"}):
        if "node_modules" in f.parts:
            continue
        if RE_IMPORT_LABOR.search(lit(f)):
            errors.append(f"import de labor ou d'ERP dans {rel(f)}")


def controle_chapitres(errors):
    res = subprocess.run([sys.executable, str(ROOT / "app" / "valide_chapitres.py")],
                         cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        for l in (res.stdout + res.stderr).splitlines()[-8:]:
            errors.append(f"chapitres : {l}")


def main() -> int:
    errors: list[str] = []
    for controle in (controle_fichiers_requis, controle_json, controle_ancien_couplage, controle_client_archipel,
                     controle_roadmap, controle_decisions, controle_programme, controle_tirets, controle_voix,
                     controle_contenu, controle_imports, controle_chapitres):
        controle(errors)
    for error in errors:
        print(f"ERREUR: {error}")
    print(f"Académie : {len(errors)} erreur(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

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
           "ROADMAP.md", "README.md", "AGENTS.md", "CONTRIBUER.md", "VOIX.md", "CONTRAT-CARTE-V2.md", "SYLLABUS.md",
           "MODELES.md", "COMMENCER.md", "GEMINI.md", "CLAUDE.md"]
DOSSIERS_V2 = ["decisions", "chantiers", "contenu", "chapitres", "sources", "boite", "serveur", "web",
               "programme", "contrats", "prompts", ".agents", ".cursor", "app/usine"]
# Ce que le produit affiche : voix contrôlée (exclamation, emoji, mots interdits).
DOSSIERS_VOIX = ["contenu", "chapitres", "web"]


def fichiers(dossiers, suffixes):
    for d in dossiers:
        p = ROOT / d
        if not p.exists():
            continue
        for f in p.rglob("*"):
            if f.is_file() and f.suffix in suffixes and not {"node_modules", "dist", "dev-dist", "test-results", "playwright-report"} & set(f.parts):
                yield f


def lit(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


REQUIS = ("AGENTS.md", "CLAUDE.md", "DOCTRINE.md", "CONTRIBUER.md", "VOIX.md", "project.yaml",
          "ROADMAP.md", "roadmap.json", "context/giverny.md", "decisions/README.md",
          "deploy/academie-publication.service", "deploy/academie-publication.timer",
          "contenu/voix.json", "contenu/citations.json", "programme/copro.json",
          "MODELES.md", "COMMENCER.md", "GEMINI.md", ".agents/rules/academie.md", ".cursor/rules/academie.mdc",
          "prompts/README.md", "prompts/creer-un-parcours.md", "prompts/ajouter-des-documents.md",
          "prompts/reprendre.md", "programme/catalogue.json", "app/usine/usine.py", "app/tests_usine.py",
          "sources/README.md", "sources/REGISTRE.md", "sources/LISTE-BLANCHE.md", "sources/registre.json")


def controle_fichiers_requis(errors):
    for required in REQUIS:
        if not (ROOT / required).is_file():
            errors.append(f"fichier requis absent : {required}")


def controle_fichiers_suivis(errors):
    """Un fichier requis qui existe sur le disque mais qu'aucun commit ne
    porte est un piège : la porte est verte en local et rouge partout
    ailleurs. `sources/.gitignore` masque tout son dossier par défaut,
    et c'est exactement là que le cas s'est produit le 03/09/2026.
    """
    res = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        return  # hors dépôt git : rien à vérifier
    suivis = set(res.stdout.split("\0"))
    for required in REQUIS:
        if (ROOT / required).is_file() and required not in suivis:
            errors.append(f"fichier requis présent mais non versionné : {required} "
                          f"(un .gitignore le masque ; il n'existera pas en CI)")


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
        if path == Path(__file__) or not path.is_file() or ".git" in path.parts or {"node_modules", "dist", "dev-dist", "test-results", "playwright-report"} & set(path.parts):
            continue
        if path.suffix not in {".md", ".py", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js"}:
            continue
        if RE_OLD_REPO.search(lit(path)):
            errors.append(f"ancien couplage technique dans {rel(path)}")
    tracked = subprocess.run(["git", "ls-files", ".claude"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    if tracked:
        errors.append(".claude ne doit pas être versionné")


def controle_client_archipel(errors):
    """L'archipel est archivé depuis le 04/09 (archive/client-archipel-2026-09-04) : il ne revient pas."""
    if (ROOT / "client").exists():
        errors.append("client/ ne doit pas revenir : l'archipel est archivé, le client v2 est web/ (ACA-FRONT-2)")


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
        if ".git" in f.parts or "archive" in f.parts or {"node_modules", "dist", "dev-dist", "test-results", "playwright-report"} & set(f.parts):
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
    """Le programme et son alignement avec academie.json : app/valide_programme.py (ACA-PROGRAMME-1)."""
    res = subprocess.run([sys.executable, str(ROOT / "app" / "valide_programme.py")],
                         capture_output=True, text=True)
    if res.returncode != 0:
        for l in (res.stdout + res.stderr).splitlines()[-8:]:
            errors.append(f"programme : {l}")


def controle_tirets(errors):
    cibles = [ROOT / d for d in DOCS_V2 if (ROOT / d).is_file()]
    cibles += list(fichiers(DOSSIERS_V2, {".md", ".json", ".sql", ".ts", ".tsx"}))
    for f in cibles:
        if "sources" in f.parts and re.fullmatch(r"[0-9a-f]{16}", f.name.split(".")[0] or ""):
            continue  # un pivot ou une fiche cite le document tel quel ; ses tirets ne sont pas les nôtres
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


def controle_usine(errors):
    """Les seuils du pas à pas vivent dans academie.json et dans le gabarit, identiques (decisions/0027)."""
    try:
        a = json.loads((ROOT / "academie.json").read_text(encoding="utf-8")).get("usine")
        g = json.loads((ROOT / "gabarit-domaine" / "academie.json").read_text(encoding="utf-8")).get("usine")
    except (OSError, json.JSONDecodeError):
        return
    if not a or not g:
        errors.append("clé `usine` absente d'academie.json ou du gabarit (decisions/0027)")
        return
    for cle in ("unite_initiale", "unite_max", "serie_pour_doubler", "couverture_min",
                "invention_max", "mots_page_texte", "mots_min_description", "lignes_par_page_transcription", "dpi_rendu", "resume_max"):
        if cle not in a:
            errors.append(f"academie.json : usine.{cle} manquant")
        elif a.get(cle) != g.get(cle):
            errors.append(f"usine.{cle} diffère entre academie.json et gabarit-domaine/academie.json")
    for cle in ("classes", "classe_par_defaut", "modeles_petits"):
        if cle in a or cle in g:
            errors.append(f"usine.{cle} : ancien classement de modèles interdit")
    bornes = [a.get("unite_initiale"), a.get("unite_max"), a.get("serie_pour_doubler")]
    if any(type(n) is not int or n < 1 for n in bornes):
        errors.append("usine : tailles et série doivent être des entiers positifs")
    elif bornes[0] > bornes[1]:
        errors.append("usine.unite_initiale dépasse unite_max")
    try:
        cat = json.loads((ROOT / "programme" / "catalogue.json").read_text(encoding="utf-8"))
        for parcours in cat.get("parcours", []):
            for cle in ("programme", "sommaire"):
                if not (ROOT / parcours.get(cle, "")).is_file():
                    errors.append(f"catalogue : {parcours.get('cle')} renvoie à un fichier absent ({cle})")
        for prompt in cat.get("creer_le_votre", {}).get("prompts", []):
            if not (ROOT / prompt).is_file():
                errors.append(f"catalogue : prompt absent {prompt}")
    except (OSError, json.JSONDecodeError):
        pass


def controle_chapitres(errors):
    res = subprocess.run([sys.executable, str(ROOT / "app" / "valide_chapitres.py")],
                         cwd=ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        for l in (res.stdout + res.stderr).splitlines()[-8:]:
            errors.append(f"chapitres : {l}")


def main() -> int:
    errors: list[str] = []
    for controle in (controle_fichiers_requis, controle_fichiers_suivis,
                     controle_json, controle_ancien_couplage, controle_client_archipel,
                     controle_roadmap, controle_decisions, controle_programme, controle_tirets, controle_voix,
                     controle_contenu, controle_imports, controle_usine, controle_chapitres):
        controle(errors)
    for error in errors:
        print(f"ERREUR: {error}")
    print(f"Académie : {len(errors)} erreur(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

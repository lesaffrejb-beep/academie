"""L'état revérifiable d'un document en cours de lecture (decisions/0027).

Le fichier `<empreinte>.etat.json` retient les unités (des tranches de
pages), la déclaration du modèle, les sceaux des unités validées et un
journal. Rien n'y est cru sur parole : `suivant` et `etat` rejouent les
contrôles de chaque unité validée contre le texte machine, donc un état
modifié à la main est détecté comme une altération. La taille des unités
suit les contrôles du document, indépendamment du nom du modèle.
Les anciennes déclarations restent lisibles ; leur classe est ignorée.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from usine.pivot import EXTENSIONS_PDF, EXTENSIONS_TRANSCRIPTION, RE_MOT, lire_page, mots

RE_ANCRE = re.compile(r"^## \[p\. (\d+)\]\s*$", re.M)
RE_NOMBRE = re.compile(r"\d+(?:[ \u00a0\u202f\u2009\u2007\u2008]\d{3})*(?:[.,]\d+)?")
RE_LIGNE_META = re.compile(
    r"^\s*\[(figure|tableau|sch[ée]ma|photo|carte|dessin|plan|graphique|page vide|ocr requis|encadr[ée]|l[ée]gende|logo)\b", re.I)
CONSIGNES_DE_DEPART = ("à décrire depuis la page rendue", "à décrire en une phrase chacune depuis la page rendue")
STATUTS_A_REPRENDRE = {"a-faire", "refusee", "alteree"}


def maintenant() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def racine() -> Path:
    return Path(os.environ.get("ACADEMIE_RACINE") or Path(__file__).resolve().parents[2])


def config(rac: Path) -> dict:
    conf = json.loads((rac / "academie.json").read_text(encoding="utf-8"))
    if "usine" not in conf:
        raise RuntimeError("academie.json n'a pas de clé `usine` (decisions/0027)")
    cfg = dict(conf["usine"])
    # Les dépôts-domaines existants peuvent encore porter l'ancien schéma.
    # Leurs classes ne sont jamais lues : seules les bornes communes du
    # dépôt qui fournit ce code servent de défaut, sans écriture du domaine.
    manquantes = [cle for cle in ("unite_initiale", "unite_max") if cle not in cfg]
    if manquantes:
        origine = Path(__file__).resolve().parents[2] / "academie.json"
        communes = json.loads(origine.read_text(encoding="utf-8"))["usine"]
        for cle in manquantes:
            if cle not in communes:
                raise RuntimeError(f"configuration de l'usine à actualiser : {cle} manquant")
            cfg[cle] = communes[cle]
    return cfg


class Document:
    """Les chemins d'un document : source, pages machine, pivot, figures, état, fiche."""

    # Le pivot s'appelle `<empreinte>.md` : l'original d'un document Markdown
    # ne peut donc pas porter ce nom, il vit en `<empreinte>.source.md`.
    MARQUE_SOURCE = ".source"
    EXTENSIONS_SOURCE = tuple(sorted(EXTENSIONS_PDF | EXTENSIONS_TRANSCRIPTION))

    def __init__(self, rac: Path, empreinte: str, interne: bool = False):
        self.racine = rac
        self.empreinte = empreinte
        self.interne = interne
        self.base = rac / "sources" / "interne" if interne else rac / "sources"
        self.etat = self.base / f"{empreinte}.etat.json"
        self.pivot = self.base / f"{empreinte}.md"
        self.pages = self.base / f"{empreinte}.pages"
        self.figures = self.base / f"{empreinte}.figures"
        self.structure = self.base / f"{empreinte}.structure.json"
        self.fiche = self.base / f"{empreinte}.fiche.json"

    def chemin_source(self, suffixe: str) -> Path:
        """Où archiver l'original, sans jamais viser le nom du pivot."""
        if self.base / f"{self.empreinte}{suffixe}" == self.pivot:
            return self.base / f"{self.empreinte}{self.MARQUE_SOURCE}{suffixe}"
        return self.base / f"{self.empreinte}{suffixe}"

    def source(self) -> Path | None:
        """Le fichier d'origine, aux noms exacts que l'usine archive.

        Aucun glob : un fichier dérivé déposé à la main (`<empreinte>.html`,
        `<empreinte>.notes.md`) ne doit pas passer pour la source. Les noms
        des versions antérieures (`<empreinte><extension>`) restent lus.
        """
        candidats = [self.base / f"{self.empreinte}{self.MARQUE_SOURCE}.md"]
        candidats += [self.base / f"{self.empreinte}{ext}" for ext in self.EXTENSIONS_SOURCE]
        for c in candidats:
            if c != self.pivot and c.is_file():
                return c
        return None

    def rel(self, p: Path) -> str:
        try:
            return str(p.relative_to(self.racine))
        except ValueError:
            return str(p)


def trouver(rac: Path, cle: str) -> Document:
    """Retrouve un document par son empreinte (ou un préfixe) dans sources/ et sources/interne/."""
    cle = Path(cle).name.split(".")[0]
    for interne in (False, True):
        base = rac / "sources" / "interne" if interne else rac / "sources"
        if not base.exists():
            continue
        candidats = sorted(base.glob(f"{cle}*.etat.json"))
        if len(candidats) == 1:
            return Document(rac, candidats[0].name[: -len(".etat.json")], interne)
        if len(candidats) > 1:
            raise RuntimeError(f"plusieurs documents commencent par {cle} : précise l'empreinte")
    raise RuntimeError(f"aucun document préparé pour « {cle} » (lance `preparer` d'abord)")


def charger(doc: Document) -> dict:
    return json.loads(doc.etat.read_text(encoding="utf-8"))


def sauver(doc: Document, etat: dict) -> None:
    doc.etat.write_text(json.dumps(etat, ensure_ascii=False, indent=1), encoding="utf-8")


def journaliser(etat: dict, evenement: str, detail: str = "") -> None:
    etat.setdefault("journal", []).append({"quand": maintenant(), "evenement": evenement, "detail": detail})


def etat_initial(doc: Document, info: dict, cfg: dict) -> dict:
    return {
        "_": "État revérifiable d'un document (app/usine, decisions/0027). Modifier ce fichier à la main ne sert à rien : chaque `suivant` rejoue les contrôles.",
        "empreinte": doc.empreinte, "fichier": doc.source().name if doc.source() else "", "interne": doc.interne,
        "type": info["type"], "prepare_le": maintenant(), "pages": info["pages"],
        "mots_machine": info["mots_machine"], "images_par_page": info.get("images_par_page", {}),
        "figures_par_page": info.get("figures_par_page", {}),
        "ocr_requis": bool(info.get("ocr_requis")), "declaration": None,
        "taille_unite": cfg["unite_initiale"], "serie": 0,
        "a_verifier": 0, "unites": [], "journal": [],
    }


# ---- déclaration ----------------------------------------------------------

def declarer(doc: Document, etat: dict, cfg: dict, outil: str, modele: str) -> list[str]:
    """Consigne la provenance ; aucune capacité n'est déduite du nom."""
    if not outil.strip() or not modele.strip():
        raise RuntimeError("outil et modèle sont obligatoires (MODELES.md §2)")
    ancienne = etat.get("declaration")
    etat["declaration"] = {"outil": outil.strip(), "modele": modele.strip(), "declare_le": maintenant()}
    etat["taille_unite"] = cfg["unite_initiale"]
    etat["serie"] = 0
    journaliser(etat, "déclaration", f"{outil} / {modele}" + (" (changement)" if ancienne else ""))
    return [f"déclaré : {outil}, {modele} ; unités de {etat['taille_unite']} page(s) pour commencer"]


# ---- lecture du pivot -----------------------------------------------------

def sections(texte: str) -> tuple[dict[int, str], list[str]]:
    """Les sections par page du pivot, et les défauts de structure (doublon, désordre)."""
    erreurs = []
    positions = [(m.start(), m.end(), int(m.group(1))) for m in RE_ANCRE.finditer(texte)]
    result: dict[int, str] = {}
    precedent = 0
    for i, (debut, fin, n) in enumerate(positions):
        suite = positions[i + 1][0] if i + 1 < len(positions) else len(texte)
        if n in result:
            erreurs.append(f"ancre [p. {n}] en double")
        if n <= precedent:
            erreurs.append(f"ancre [p. {n}] hors ordre après [p. {precedent}]")
        precedent = max(precedent, n)
        result[n] = texte[fin:suite]
    return result, erreurs


def normaliser_nombre(s: str) -> str:
    s = re.sub(r"[ \u00a0\u202f\u2009\u2007\u2008]", "", s).replace(",", ".")
    return s.strip(".")


def nombres(texte: str) -> set[str]:
    return {normaliser_nombre(m) for m in RE_NOMBRE.findall(texte) if normaliser_nombre(m)}


def _sha(texte: str) -> str:
    return hashlib.sha256(texte.encode("utf-8")).hexdigest()


def controles_page(n: int, section: str, machine: str, voisins: str, figures: int, cfg: dict) -> tuple[list[str], int]:
    """Ce qu'une machine peut voir d'une page relue ; renvoie (erreurs, chiffres à vérifier en vision)."""
    err: list[str] = []
    a_verifier = 0
    if not section.strip():
        return [f"p. {n} : section vide"], 0
    for consigne in CONSIGNES_DE_DEPART:
        if consigne in section:
            err.append(f"p. {n} : la consigne de départ est encore là ; décris la figure ou écris [page vide]")
            break
    lignes = section.splitlines()
    meta = [l for l in lignes if RE_LIGNE_META.match(l)]
    page_texte = len(RE_MOT.findall(machine.lower())) >= int(cfg["mots_page_texte"])
    if page_texte:
        mots_m = mots(machine)
        mots_s = mots(section)
        couverture = len(mots_m & mots_s) / len(mots_m) if mots_m else 1.0
        if couverture < float(cfg["couverture_min"]):
            err.append(f"p. {n} : couverture {couverture:.0%} du texte machine (minimum {float(cfg['couverture_min']):.0%}) ; le pivot reprend le texte, il ne le résume pas")
        invention = len(mots_s - mots_m) / len(mots_s) if mots_s else 0.0
        if invention > float(cfg["invention_max"]):
            err.append(f"p. {n} : {invention:.0%} des mots ne sont pas sur la page (maximum {float(cfg['invention_max']):.0%}) ; le pivot reprend, il n'explique pas")
    if not page_texte or figures > 0:
        if not meta:
            err.append(f"p. {n} : page à figures ou sans texte ; il faut une ligne [figure : …], [tableau : …] ou [page vide]")
        for l in meta:
            if re.match(r"^\s*\[(page vide|ocr requis)", l, re.I):
                continue
            if len(RE_MOT.findall(l.lower())) < int(cfg["mots_min_description"]):
                err.append(f"p. {n} : description trop courte « {l.strip()[:60]} » ({cfg['mots_min_description']} mots au moins)")
    connus = nombres(machine) | nombres(voisins)
    for l in lignes:
        if RE_LIGNE_META.match(l):
            a_verifier += len(nombres(l) - connus)
            continue
        absents = sorted(nombres(l) - connus)
        if absents:
            err.append(f"p. {n} : chiffre absent de la page : {', '.join(absents[:5])} ; un chiffre qu'on ne lit pas dans le document ne s'écrit pas")
    return err, a_verifier


def _voisins(doc: Document, n: int, total: int) -> str:
    return "\n".join(lire_page(doc.pages, k) for k in (n - 1, n + 1) if 1 <= k <= total)


def controler_unite(doc: Document, etat: dict, cfg: dict, unite: dict) -> tuple[list[str], str, int]:
    """Rejoue tous les contrôles d'une unité ; renvoie (erreurs, sceau, chiffres à vérifier)."""
    if not doc.pivot.exists():
        return [f"pivot absent : {doc.rel(doc.pivot)}"], "", 0
    texte = doc.pivot.read_text(encoding="utf-8")
    secs, err = sections(texte)
    a_verifier = 0
    morceaux = []
    for n in range(unite["de"], unite["a"] + 1):
        if n not in secs:
            err.append(f"p. {n} : ancre « ## [p. {n}] » absente du pivot")
            continue
        e, av = controles_page(n, secs[n], lire_page(doc.pages, n), _voisins(doc, n, etat["pages"]),
                               int((etat.get("figures_par_page") or etat.get("images_par_page", {})).get(str(n), 0)), cfg)
        err += e
        a_verifier += av
        morceaux.append(secs[n])
    return err, _sha("\n".join(morceaux)), a_verifier


# ---- unités ---------------------------------------------------------------

def reverifier(doc: Document, etat: dict, cfg: dict) -> list[str]:
    """Rejoue les contrôles de chaque unité validée : un état trafiqué ou un pivot abîmé se voit ici."""
    messages = []
    for u in etat["unites"]:
        if u["statut"] != "valide":
            continue
        err, sceau, _ = controler_unite(doc, etat, cfg, u)
        if err:
            u["statut"] = "alteree"
            u["erreurs"] = err
            journaliser(etat, "altération détectée", f"unité {u['n']} (p. {u['de']}-{u['a']}) : " + " | ".join(err[:3]))
            messages.append(f"unité {u['n']} (p. {u['de']}-{u['a']}) : les contrôles ne passent plus, elle repasse à faire")
        elif sceau != u.get("sceau"):
            u["sceau"] = sceau
            journaliser(etat, "unité modifiée après validation, revalidée", f"unité {u['n']}")
    return messages


def suivant(doc: Document, etat: dict, cfg: dict) -> tuple[dict | None, list[str]]:
    """L'unité à faire maintenant ; refuse d'avancer tant que la précédente n'est pas validée."""
    messages = []
    if not etat.get("declaration"):
        raise RuntimeError("aucun modèle déclaré : `usine.py declarer <empreinte> --outil … --modele …` (MODELES.md §2)")
    if etat.get("ocr_requis"):
        raise RuntimeError("ce PDF n'a pas de couche texte : `ocrmypdf --language fra <pdf> <pdf-ocr>` puis `preparer` à nouveau")
    messages += reverifier(doc, etat, cfg)
    for u in etat["unites"]:
        if u["statut"] in STATUTS_A_REPRENDRE:
            journaliser(etat, "unité reprise", f"unité {u['n']} ({u['statut']})")
            messages.append(f"unité {u['n']} (p. {u['de']}-{u['a']}) est {u['statut']} : on la reprend avant d'avancer")
            return u, messages
    derniere = etat["unites"][-1]["a"] if etat["unites"] else 0
    if derniere >= etat["pages"]:
        messages.append("toutes les pages sont relues ; reste la fiche (`usine.py fiche`) puis la ligne de registre")
        return None, messages
    de = derniere + 1
    a = min(etat["pages"], de + int(etat["taille_unite"]) - 1)
    u = {"n": len(etat["unites"]) + 1, "de": de, "a": a, "statut": "a-faire", "cree_le": maintenant(), "refus": 0}
    etat["unites"].append(u)
    journaliser(etat, "unité ouverte", f"unité {u['n']} (p. {de}-{a})")
    return u, messages


def valider(doc: Document, etat: dict, cfg: dict) -> tuple[bool, list[str]]:
    """Valide l'unité en cours ; adapte la taille des unités suivantes au résultat."""
    if not etat.get("declaration"):
        raise RuntimeError("aucun modèle déclaré")
    en_cours = [u for u in etat["unites"] if u["statut"] in STATUTS_A_REPRENDRE]
    if not en_cours:
        return False, ["aucune unité en cours : lance `suivant`"]
    u = en_cours[0]
    err, sceau, a_verifier = controler_unite(doc, etat, cfg, u)
    bornes = cfg
    if err:
        u["statut"] = "refusee"
        u["refus"] = int(u.get("refus", 0)) + 1
        u["erreurs"] = err
        etat["serie"] = 0
        etat["taille_unite"] = max(1, int(etat["taille_unite"]) // 2)
        journaliser(etat, "unité refusée", f"unité {u['n']} : {len(err)} défaut(s) ; unités de {etat['taille_unite']} page(s) désormais")
        return False, err + [f"unité {u['n']} refusée ; corrige le pivot puis relance `valider` (les unités passent à {etat['taille_unite']} page(s))"]
    u["statut"] = "valide"
    u["valide_le"] = maintenant()
    u["par"] = etat["declaration"]["modele"]
    u["sceau"] = sceau
    u["a_verifier"] = a_verifier
    u.pop("erreurs", None)
    etat["a_verifier"] = sum(int(x.get("a_verifier", 0)) for x in etat["unites"])
    messages = [f"unité {u['n']} (p. {u['de']}-{u['a']}) validée ; point de sauvegarde écrit"]
    if int(u.get("refus", 0)) == 0:
        etat["serie"] = int(etat.get("serie", 0)) + 1
        if etat["serie"] >= int(cfg["serie_pour_doubler"]) and int(etat["taille_unite"]) < int(bornes["unite_max"]):
            etat["taille_unite"] = min(int(bornes["unite_max"]), int(etat["taille_unite"]) * 2)
            etat["serie"] = 0
            messages.append(f"trois unités propres d'affilée : les unités passent à {etat['taille_unite']} page(s)")
    else:
        etat["serie"] = 0
    if a_verifier:
        messages.append(f"{a_verifier} chiffre(s) lus en vision dans des lignes [figure] ou [tableau] : à faire vérifier par un relecteur")
    journaliser(etat, "unité validée", f"unité {u['n']} (p. {u['de']}-{u['a']})")
    return True, messages


# ---- ce qu'on montre -------------------------------------------------------

def pages_relues(etat: dict) -> int:
    return sum(u["a"] - u["de"] + 1 for u in etat["unites"] if u["statut"] == "valide")


def consigne(doc: Document, etat: dict, unite: dict) -> str:
    """La tâche, écrite pour un modèle qui n'a rien d'autre en mémoire."""
    lignes = [
        f"Document {doc.empreinte} ({etat.get('fichier', '')}), unité {unite['n']} : pages {unite['de']} à {unite['a']} sur {etat['pages']}.",
        f"Fichier à modifier : {doc.rel(doc.pivot)} ; seulement les sections « ## [p. {unite['de']}] » à « ## [p. {unite['a']}] ».",
        "Ce qu'on attend, et rien d'autre :",
        "  1. garder le texte de la page tel qu'il est écrit dans le document ; recoller les mots coupés, remettre les colonnes dans l'ordre de lecture, rien de plus ;",
        "  2. remettre les titres en « ### » (le fichier .structure.json propose des candidats par taille de police) ;",
        "  3. remettre un tableau en tableau Markdown quand la page en a un ;",
        "  4. décrire chaque figure en une ligne « [figure : …] » d'au moins six mots, depuis la page rendue ; une page sans rien : « [page vide] » ;",
        "  5. ne rien résumer, ne rien expliquer, n'ajouter aucun chiffre qui ne se lit pas sur la page.",
    ]
    rendus = []
    if doc.figures.exists():
        for n in range(unite["de"], unite["a"] + 1):
            rendus += [doc.rel(p) for p in sorted(doc.figures.glob(f"p-{n:04d}*.png"))]
    if rendus:
        lignes.append("Pages rendues à regarder : " + ", ".join(rendus))
    if doc.structure.exists():
        try:
            struct = json.loads(doc.structure.read_text(encoding="utf-8"))
            titres = [t for t in struct.get("titres_candidats", []) if unite["de"] <= int(t.get("page", 0)) <= unite["a"]]
            if titres:
                lignes.append("Titres candidats : " + " | ".join(f"p. {t['page']} : {t['texte'][:60]}" for t in titres[:12]))
        except (OSError, json.JSONDecodeError, ValueError):
            pass
    lignes += [
        f"Puis : python3 app/usine/usine.py valider {doc.empreinte}",
        "Point de sauvegarde : rien n'est à garder en mémoire ; après une coupure, relance `suivant` et l'état reprend au disque.",
    ]
    return "\n".join(lignes)


def resume(doc: Document, etat: dict) -> str:
    decl = etat.get("declaration") or {}
    total = etat["pages"]
    relues = pages_relues(etat)
    lignes = [
        f"{doc.empreinte} ({etat.get('fichier', '')}) : {relues}/{total} page(s) relues, {len(etat['unites'])} unité(s), unités de {etat['taille_unite']} page(s)",
        f"modèle : {decl.get('outil', 'non déclaré')} / {decl.get('modele', '')}".rstrip(" /"),
    ]
    if etat.get("ocr_requis"):
        lignes.append("OCR requis avant toute lecture")
    if etat.get("a_verifier"):
        lignes.append(f"{etat['a_verifier']} chiffre(s) lus en vision à faire vérifier")
    for u in etat["unites"]:
        if u["statut"] != "valide":
            lignes.append(f"unité {u['n']} (p. {u['de']}-{u['a']}) : {u['statut']}")
    if etat.get("journal"):
        j = etat["journal"][-1]
        lignes.append(f"dernier événement : {j['quand']} {j['evenement']} {j.get('detail', '')}".rstrip())
    return "\n".join(lignes)

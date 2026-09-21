#!/usr/bin/env python3
"""Tests de l'usine pas à pas (app/usine, decisions/0026 et 0027).

Chaque scénario construit une racine jetable (academie.json copié,
sources/ vide) et pilote l'usine par sa ligne de commande, comme le fera
un modèle. Les promesses protégées : l'unité suivante ne s'ouvre pas tant
que la précédente n'est pas validée ; un résumé, un chiffre inventé, une
consigne laissée en place sont refusés ; un état trafiqué est détecté ;
la taille des unités suit les résultats ; la fiche ne porte aucun chiffre
absent du document ; une transcription perd horodatages et locuteurs.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent
RACINE = APP.parent
USINE = APP / "usine" / "usine.py"
sys.path.insert(0, str(APP))
from usine import etat as E  # noqa: E402
from usine import transcription  # noqa: E402

ECHECS: list[str] = []

# Un PDF demande les quatre outils de poppler ; `pdftotext` seul ne suffit
# pas (ACA-INGESTION-1, ACA-PORTABILITE-1).
OUTILS_PDF = ("pdfinfo", "pdftotext", "pdfimages", "pdftoppm")


def outils_pdf_absents() -> list[str]:
    return [nom for nom in OUTILS_PDF if shutil.which(nom) is None]


def verifie(nom: str, condition: bool, detail: str = "") -> None:
    print(f"{'✓' if condition else '✗'} {nom}")
    if not condition:
        ECHECS.append(nom)
        if detail:
            print("\n".join("    " + l for l in detail.splitlines()[-8:]))


def racine_test(lignes_par_page: int = 3, mots_page_texte: int = 5) -> Path:
    rac = Path(tempfile.mkdtemp(prefix="academie-usine-"))
    conf = json.loads((RACINE / "academie.json").read_text(encoding="utf-8"))
    conf["usine"]["lignes_par_page_transcription"] = lignes_par_page
    conf["usine"]["mots_page_texte"] = mots_page_texte
    conf["usine"]["unite_initiale"] = 2
    conf["usine"]["unite_max"] = 4
    (rac / "academie.json").write_text(json.dumps(conf, ensure_ascii=False), encoding="utf-8")
    (rac / "sources").mkdir()
    (rac / "sources" / "REGISTRE.md").write_text("# Registre\n\n| Source | Réf | Nature | Parti | Fiab | Vérifié | On en tire | On n'en tire pas |\n|---|---|---|---|---|---|---|---|\n", encoding="utf-8")
    return rac


def lance(rac: Path, *args: str) -> tuple[int, str]:
    env = dict(os.environ, ACADEMIE_RACINE=str(rac))
    res = subprocess.run([sys.executable, str(USINE), *args], capture_output=True, text=True, env=env, cwd=str(rac))
    return res.returncode, res.stdout + res.stderr


PHRASES = [
    "La loi du 10 juillet 1965 organise la copropriété des immeubles bâtis.",
    "Le décret du 17 mars 1967 précise la convocation et le procès-verbal.",
    "Le syndic convoque l'assemblée générale au moins 21 jours avant la séance.",
    "Les charges se répartissent selon les tantièmes fixés par le règlement.",
    "Le conseil syndical contrôle la gestion et assiste le syndic.",
    "Les travaux d'amélioration relèvent de la majorité de l'article 25.",
    "Le budget prévisionnel se vote chaque année avant l'exercice.",
    "Le fonds de travaux représente au moins 5 pour cent du budget.",
    "L'immatriculation au registre national est obligatoire depuis 2017.",
]


def transcription_fixture(n_lignes: int = 45) -> str:
    lignes = ["WEBVTT", "", "1", "00:00:01.000 --> 00:00:04.000", "<v Formateur>Bonjour à toutes et à tous.", ""]
    for i in range(n_lignes):
        lignes += [str(i + 2), f"00:0{i % 10}:10.000 --> 00:0{i % 10}:14.000", f"Intervenant : {PHRASES[i % len(PHRASES)]}", ""]
    return "\n".join(lignes)


def pdf_fixture(pages: list[list[str]]) -> bytes:
    """Un PDF minimal écrit à la main : une police standard, une page par liste de lignes."""
    objs: list[tuple[int, bytes]] = []
    kids = []
    num = 4
    for lignes in pages:
        page_num, contenu_num = num, num + 1
        num += 2
        kids.append(page_num)
        flux = ["BT", "/F1 12 Tf", "72 740 Td", "14 TL"]
        for l in lignes:
            esc = l.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            flux.append(f"({esc}) Tj T*")
        flux.append("ET")
        octets = "\n".join(flux).encode("cp1252", "replace")
        objs.append((page_num, f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents {contenu_num} 0 R /Resources << /Font << /F1 3 0 R >> >> >>".encode()))
        objs.append((contenu_num, b"<< /Length %d >>\nstream\n" % len(octets) + octets + b"\nendstream"))
    objs = [(1, b"<< /Type /Catalog /Pages 2 0 R >>"),
            (2, ("<< /Type /Pages /Kids [" + " ".join(f"{k} 0 R" for k in kids) + f"] /Count {len(pages)} >>").encode()),
            (3, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")] + objs
    out = bytearray(b"%PDF-1.4\n")
    offsets = {}
    for n, corps in objs:
        offsets[n] = len(out)
        out += f"{n} 0 obj\n".encode() + corps + b"\nendobj\n"
    xref = len(out)
    total = len(objs) + 1
    out += f"xref\n0 {total}\n".encode() + b"0000000000 65535 f \n"
    for n in range(1, total):
        out += f"{offsets[n]:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {total} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    return bytes(out)


def empreinte_de(rac: Path) -> str:
    return sorted((rac / "sources").glob("*.etat.json"))[0].name.split(".")[0]


def sha16(fichier: Path) -> str:
    return hashlib.sha256(fichier.read_bytes()).hexdigest()[:16]


def etat_de(rac: Path, emp: str) -> dict:
    return json.loads((rac / "sources" / f"{emp}.etat.json").read_text(encoding="utf-8"))


def remplace_section(rac: Path, emp: str, page: int, nouveau: str) -> None:
    pivot = rac / "sources" / f"{emp}.md"
    texte = pivot.read_text(encoding="utf-8")
    motif = re.compile(rf"(## \[p\. {page}\]\n)(.*?)(?=\n## \[p\. |\Z)", re.S)
    assert motif.search(texte), f"section {page} introuvable"
    pivot.write_text(motif.sub(lambda m: m.group(1) + "\n" + nouveau + "\n", texte, count=1), encoding="utf-8")


def scenario_transcription_et_pas_a_pas() -> None:
    rac = racine_test()
    src = rac / "formation.vtt"
    src.write_text(transcription_fixture(), encoding="utf-8")
    code, sortie = lance(rac, "preparer", str(src))
    verifie("une transcription se prépare", code == 0 and "préparé" in sortie, sortie)
    emp = empreinte_de(rac)
    etat = etat_de(rac, emp)
    verifie("les pseudo-pages sont découpées (46 lignes, 3 par page)", etat["pages"] == 16, json.dumps(etat)[:300])
    pivot = (rac / "sources" / f"{emp}.md").read_text(encoding="utf-8")
    verifie("le pivot brut porte une ancre par page", pivot.count("## [p. ") == 16 and re.search(r"\d\d:\d\d:\d\d", pivot) is None and "Intervenant :" not in pivot, pivot[:300])

    code, sortie = lance(rac, "suivant", emp)
    verifie("sans déclaration, pas d'unité", code == 1 and "déclar" in sortie, sortie)

    for nom in ("gpt-6-astra", "modele-inconnu", "local-mini", "claude-haiku-4-5"):
        code, sortie = lance(rac, "declarer", emp, "--outil", "codex", "--modele", nom)
        declaration = etat_de(rac, emp)["declaration"] or {}
        verifie(f"{nom} garde les mêmes conditions sans classe",
                code == 0 and "classe" not in declaration
                and declaration.get("modele") == nom
                and etat_de(rac, emp)["taille_unite"] == 2, sortie)
    code, sortie = lance(rac, "declarer", emp, "--outil", "codex", "--modele", "claude-haiku-4-5", "--classe", "grand")
    verifie("l'ancien argument est ignoré sans créer une classe",
            code == 0 and "ignor" in sortie and "classe" not in etat_de(rac, emp)["declaration"]
            and etat_de(rac, emp)["taille_unite"] == 2, sortie)

    code, sortie = lance(rac, "suivant", emp)
    verifie("la première unité couvre les pages 1 à 2", code == 0 and "pages 1 à 2" in sortie and "Point de sauvegarde" in sortie, sortie)
    code, sortie = lance(rac, "suivant", emp)
    verifie("suivant sans valider redonne la même unité", code == 0 and "pages 1 à 2" in sortie and "on la reprend" in sortie, sortie)
    verifie("aucune deuxième unité n'est ouverte", len(etat_de(rac, emp)["unites"]) == 1)

    code, sortie = lance(rac, "valider", emp)
    verifie("le pivot brut, fidèle, est validé", code == 0 and "validée" in sortie and "sauvegarde" in sortie, sortie)
    verifie("un sceau est posé sur l'unité", bool(etat_de(rac, emp)["unites"][0].get("sceau")))

    code, sortie = lance(rac, "suivant", emp)
    verifie("l'unité 2 couvre les pages 3 à 4", "pages 3 à 4" in sortie, sortie)
    remplace_section(rac, emp, 3, "Résumé : la loi organise la copropriété.")
    code, sortie = lance(rac, "valider", emp)
    verifie("un résumé à la place du texte est refusé", code == 1 and "couverture" in sortie, sortie)
    verifie("un refus réduit les unités à 1 page", etat_de(rac, emp)["taille_unite"] == 1)
    machine = (rac / "sources" / f"{emp}.pages" / "p-0003.txt").read_text(encoding="utf-8")
    remplace_section(rac, emp, 3, machine.strip() + "\nEn 2031, 45 pour cent des immeubles seront concernés.")
    code, sortie = lance(rac, "valider", emp)
    verifie("un chiffre absent de la page est refusé", code == 1 and "chiffre absent" in sortie and "2031" in sortie, sortie)
    remplace_section(rac, emp, 3, machine.strip())
    code, sortie = lance(rac, "valider", emp)
    verifie("le texte rétabli est validé", code == 0, sortie)

    # Altération : on trafique l'état pour marquer valide une unité dont le pivot a été résumé.
    code, sortie = lance(rac, "suivant", emp)
    verifie("l'unité 3 fait 1 page (p. 5)", "pages 5 à 5" in sortie, sortie)
    remplace_section(rac, emp, 5, "Trois mots seulement.")
    e = etat_de(rac, emp)
    e["unites"][-1]["statut"] = "valide"
    e["unites"][-1]["sceau"] = "faux"
    (rac / "sources" / f"{emp}.etat.json").write_text(json.dumps(e), encoding="utf-8")
    code, sortie = lance(rac, "suivant", emp)
    verifie("un état trafiqué est détecté et l'unité repasse à faire", "ne passent plus" in sortie and "pages 5 à 5" in sortie, sortie)
    machine5 = (rac / "sources" / f"{emp}.pages" / "p-0005.txt").read_text(encoding="utf-8")
    remplace_section(rac, emp, 5, machine5.strip())
    code, sortie = lance(rac, "valider", emp)
    verifie("l'unité altérée, réparée, se valide", code == 0, sortie)

    # Série : trois unités propres d'affilée doublent la taille (1 → 2 → 4, plafond commun de la fixture).
    tailles = []
    for _ in range(6):
        code, sortie = lance(rac, "suivant", emp)
        if "toutes les pages" in sortie:
            break
        code, sortie = lance(rac, "valider", emp)
        tailles.append(etat_de(rac, emp)["taille_unite"])
    verifie("la taille des unités grandit sur une série propre, sans dépasser le plafond", 4 in tailles and max(tailles) <= 4, str(tailles))

    code, sortie = lance(rac, "etat", emp)
    verifie("l'état se lit", code == 0 and "page(s) relues" in sortie and "claude-haiku-4-5" in sortie, sortie)


def scenario_pdf() -> None:
    absents = outils_pdf_absents()
    if absents:
        # Poppler incomplet (le runner Windows peut porter `pdftotext`
        # sans `pdfinfo`, `pdfimages` ni `pdftoppm`) : l'absence doit être
        # dite et refusée nommément, pas contournée par un IndexError sur
        # un état qui n'existe pas (ACA-PORTABILITE-1).
        rac = racine_test(mots_page_texte=5)
        src = rac / "guide.pdf"
        src.write_bytes(pdf_fixture([["La loi du 10 juillet 1965 fixe les majorites."]]))
        code, sortie = lance(rac, "preparer", str(src))
        verifie("poppler incomplet : le PDF est refusé en nommant l'outil absent",
                code == 1 and "outil absent" in sortie and absents[0] in sortie, sortie)
        verifie("poppler incomplet : aucun état n'est écrit",
                not list((rac / "sources").glob("*.etat.json")), sortie)
        print(f"~ poppler incomplet ({', '.join(absents)}) : scénario PDF remplacé par le refus attendu")
        return
    rac = racine_test(mots_page_texte=5)
    src = rac / "guide.pdf"
    src.write_bytes(pdf_fixture([
        ["Guide des majorites", "La loi du 10 juillet 1965 fixe les majorites.", "Le syndic convoque au moins 21 jours avant."],
        ["Le budget se vote chaque annee.", "Le fonds de travaux est obligatoire.", "Graphique 1 : evolution des charges depuis 2010"],
        [],
    ]))
    code, sortie = lance(rac, "preparer", str(src))
    verifie("un PDF se prépare avec poppler", code == 0 and "3 page(s)" in sortie, sortie)
    emp = empreinte_de(rac)
    etat = etat_de(rac, emp)
    verifie("le texte machine de la page 1 est extrait", "10 juillet 1965" in (rac / "sources" / f"{emp}.pages" / "p-0001.txt").read_text(encoding="utf-8"))
    verifie("la page vide est rendue en image", any((rac / "sources" / f"{emp}.figures").glob("p-0003*.png")), str(list((rac / "sources").iterdir())))
    verifie("une figure vectorielle est repérée par sa légende et sa page rendue",
            etat["figures_par_page"].get("2") == 1 and any((rac / "sources" / f"{emp}.figures").glob("p-0002*.png")), json.dumps(etat["figures_par_page"]))
    verifie("le PDF n'est pas marqué OCR requis", etat["ocr_requis"] is False)
    conf = json.loads((rac / "academie.json").read_text())
    conf["usine"]["unite_initiale"] = 3
    (rac / "academie.json").write_text(json.dumps(conf))
    lance(rac, "declarer", emp, "--outil", "claude-code", "--modele", "claude-sonnet-5")
    code, sortie = lance(rac, "suivant", emp)
    verifie("le document utilise les 3 pages configurées", "pages 1 à 3" in sortie and "Pages rendues" in sortie, sortie)
    code, sortie = lance(rac, "valider", emp)
    verifie("la consigne de départ laissée sur la page vide est refusée", code == 1 and "consigne de départ" in sortie, sortie)
    remplace_section(rac, emp, 3, "[page vide]")
    code, sortie = lance(rac, "valider", emp)
    verifie("la figure de la page 2 doit encore être décrite", code == 1 and "p. 2" in sortie, sortie)
    machine2 = (rac / "sources" / f"{emp}.pages" / "p-0002.txt").read_text(encoding="utf-8").strip()
    remplace_section(rac, emp, 2, "[figure : courbe de l'évolution des charges depuis 2010, en hausse]\n" + machine2)
    code, sortie = lance(rac, "valider", emp)
    verifie("« [page vide] » et une figure décrite suffisent", code == 0, sortie)

    fiche = rac / "sources" / f"{emp}.fiche.json"
    base = {"titre": "Guide des majorités", "editeur": "Éditeur de test", "date_edition": "2024", "nature": "institution",
            "parti": "", "fiabilite": "A", "licence": "à vérifier", "periode_validite": "2024 et après", "pages": 3,
            "on_en_tire": "les règles de majorité", "on_n_en_tire_pas": "rien", "resume": "Un guide court sur les majorités.", "interne": False}
    fiche.write_text(json.dumps(dict(base, nature="blog")), encoding="utf-8")
    code, sortie = lance(rac, "fiche", emp)
    verifie("une nature inconnue est refusée", code == 1 and "nature inconnue" in sortie, sortie)
    fiche.write_text(json.dumps(dict(base, resume="Le guide annonce 48 pour cent de copropriétés en difficulté.")), encoding="utf-8")
    code, sortie = lance(rac, "fiche", emp)
    verifie("un chiffre du résumé absent du document est refusé", code == 1 and "chiffre absent" in sortie, sortie)
    fiche.write_text(json.dumps(dict(base, nature="editeur", fiabilite="A")), encoding="utf-8")
    code, sortie = lance(rac, "fiche", emp)
    verifie("une fiabilité au-dessus de la nature est refusée", code == 1 and "au-dessus" in sortie, sortie)
    fiche.write_text(json.dumps(base), encoding="utf-8")
    code, sortie = lance(rac, "fiche", emp)
    verifie("une fiche juste est validée et signée par le script", code == 0 and json.loads(fiche.read_text(encoding="utf-8")).get("par") == "claude-sonnet-5", sortie)
    code, sortie = lance(rac, "registre", emp, "--ecrire")
    registre = (rac / "sources" / "REGISTRE.md").read_text(encoding="utf-8")
    verifie("la ligne de registre s'écrit depuis la fiche", code == 0 and "Guide des majorités (Éditeur de test, 2024)" in registre and "| institution |" in registre, sortie)
    code, sortie = lance(rac, "registre", emp, "--ecrire")
    verifie("la ligne ne s'écrit pas deux fois", registre.count("Guide des majorités") == (rac / "sources" / "REGISTRE.md").read_text(encoding="utf-8").count("Guide des majorités"))


def scenario_depot() -> None:
    absents = outils_pdf_absents()
    if absents:
        # Même refus honnête que `scenario_pdf`, vu par le lot : le bilan
        # nomme l'échec, le fichier reste dans le dépôt de départ
        # (ACA-INGESTION-1).
        rac = racine_test(mots_page_texte=5)
        depot = rac / "sources" / "a-preparer"
        depot.mkdir()
        (depot / "guide.pdf").write_bytes(pdf_fixture([["Le fonds de travaux est obligatoire."]]))
        code, sortie = lance(rac, "deposer")
        verifie("poppler incomplet : le dépôt nomme l'échec et sort non nul",
                code == 1 and "1 échec" in sortie and "échec : guide.pdf" in sortie
                and absents[0] in sortie, sortie)
        verifie("poppler incomplet : le PDF refusé reste dans le dépôt",
                (depot / "guide.pdf").is_file(), sortie)
        print(f"~ poppler incomplet ({', '.join(absents)}) : scénario dépôt remplacé par le refus attendu")
        return
    rac = racine_test(mots_page_texte=5)
    depot = rac / "sources" / "a-preparer"
    depot.mkdir()
    (depot / "guide.pdf").write_bytes(pdf_fixture([
        ["Guide du depot", "Le fonds de travaux est obligatoire.", "Graphique 1 : evolution des charges"],
        [],
    ]))
    code, sortie = lance(rac, "deposer")
    verifie("le dossier de dépôt prépare le PDF",
            code == 0 and "1 fichier(s)" in sortie and "préparé :" in sortie, sortie)
    emp = empreinte_de(rac)
    structure = json.loads((rac / "sources" / f"{emp}.structure.json").read_text(encoding="utf-8"))
    verifie("la structure retient les images extraites",
            "images_extraites" in structure, json.dumps(structure)[:200])
    verifie("les pages à figures sont rendues",
            any((rac / "sources" / f"{emp}.figures").glob("p-*.png")), "")
    code, sortie = lance(rac, "deposer")
    verifie("un document déjà préparé est sauté", "déjà préparé" in sortie, sortie)
    verifie("le fichier reste dans le dossier de dépôt", (depot / "guide.pdf").is_file())


def scenario_reprise_ancien_etat() -> None:
    rac = racine_test()
    src = rac / "ancien.vtt"
    src.write_text(transcription_fixture(), encoding="utf-8")
    lance(rac, "preparer", str(src))
    emp = empreinte_de(rac)
    lance(rac, "declarer", emp, "--outil", "codex", "--modele", "modele-anonyme")
    lance(rac, "suivant", emp)
    lance(rac, "valider", emp)
    lance(rac, "suivant", emp)
    e = etat_de(rac, emp)
    unites_avant = json.loads(json.dumps(e["unites"]))
    conf = json.loads((rac / "academie.json").read_text())
    conf["usine"].pop("unite_initiale")
    conf["usine"].pop("unite_max")
    conf["usine"].update({"classes": {"petit": {"unite_initiale": 2, "unite_max": 4}},
                          "classe_par_defaut": "petit", "modeles_petits": ".*"})
    (rac / "academie.json").write_text(json.dumps(conf))
    e["declaration"]["classe"] = "ancienne-valeur-inconnue"
    (rac / "sources" / f"{emp}.etat.json").write_text(json.dumps(e))
    code, sortie = lance(rac, "suivant", emp)
    verifie("un ancien état reprend son unité sans consulter sa classe",
            code == 0 and etat_de(rac, emp)["unites"] == unites_avant, sortie)
    code, sortie = lance(rac, "valider", emp)
    verifie("un ancien état se valide sans migration de classe", code == 0, sortie)
    verifie("le sceau de l'unité antérieure est conservé",
            etat_de(rac, emp)["unites"][0]["sceau"] == unites_avant[0]["sceau"])
    lance(rac, "suivant", emp)
    ouverte = etat_de(rac, emp)["unites"][-1]
    lance(rac, "declarer", emp, "--outil", "codex", "--modele", "nouveau-nom")
    code, sortie = lance(rac, "suivant", emp)
    verifie("changer de modèle conserve l'unité ouverte", code == 0 and etat_de(rac, emp)["unites"][-1] == ouverte, sortie)
    conf_avant = (rac / "academie.json").read_bytes()
    code, sortie = lance(rac, "declarer", emp, "--outil", "codex", "--modele", "local-mini")
    bornes_courantes = json.loads((RACINE / "academie.json").read_text())["usine"]
    verifie("un ancien dépôt adopte les unités communes sans classer son modèle",
            code == 0 and etat_de(rac, emp)["taille_unite"] == bornes_courantes["unite_initiale"], sortie)
    e = etat_de(rac, emp)
    e["serie"] = bornes_courantes["serie_pour_doubler"] - 1
    (rac / "sources" / f"{emp}.etat.json").write_text(json.dumps(e))
    code, sortie = lance(rac, "valider", emp)
    verifie("ancien dépôt : le doublement dépasse effectivement l'ancien plafond",
            code == 0 and etat_de(rac, emp)["taille_unite"] == min(
                2 * bornes_courantes["unite_initiale"], bornes_courantes["unite_max"]), sortie)
    for _ in range(4):
        code, sortie = lance(rac, "suivant", emp)
        if "toutes les pages" in sortie:
            break
        code, sortie = lance(rac, "valider", emp)
        verifie("ancien dépôt : l'adaptation se poursuit sans ancien plafond", code == 0, sortie)
    verifie("la compatibilité ne réécrit pas la configuration du domaine", (rac / "academie.json").read_bytes() == conf_avant)


def scenario_transcription_unitaire() -> None:
    lignes = transcription.nettoyer(transcription_fixture(3))
    verifie("horodatages, numéros et locuteurs disparaissent",
            all("-->" not in l and not l.startswith("Intervenant") and "<v" not in l for l in lignes) and lignes[0].startswith("Bonjour"), "\n".join(lignes))
    verifie("les pseudo-pages respectent la taille demandée", [len(p.splitlines()) for p in transcription.pseudo_pages(lignes, 2)] == [2, 2])


TEXTE_MD = "# Cours\n\n2026\nObjectif : comprendre la source.\nNiveau : 3\n"


def scenario_document_texte() -> None:
    """Un .md ou un .txt n'est pas une transcription : ni son original, ni son texte ne se perdent."""
    rac = racine_test(lignes_par_page=10, mots_page_texte=3)
    src = rac / "cours.md"
    src.write_text(TEXTE_MD, encoding="utf-8")
    code, sortie = lance(rac, "preparer", str(src))
    verifie("un Markdown se prépare", code == 0 and "préparé" in sortie, sortie)
    emp = empreinte_de(rac)
    archive = rac / "sources" / f"{emp}.source.md"
    pivot = rac / "sources" / f"{emp}.md"
    verifie("l'original est archivé à part du pivot",
            archive.is_file() and archive.read_bytes() == src.read_bytes(),
            str(sorted(p.name for p in (rac / "sources").iterdir())))
    verifie("l'archive retrouve l'empreinte du document",
            archive.is_file() and sha16(archive) == emp, emp)
    verifie("le pivot reste distinct de l'original",
            pivot.is_file() and pivot.read_bytes() != archive.read_bytes()
            and "## [p. 1]" in pivot.read_text(encoding="utf-8"),
            pivot.read_text(encoding="utf-8")[:200])
    machine = (rac / "sources" / f"{emp}.pages" / "p-0001.txt").read_text(encoding="utf-8")
    verifie("un document n'est pas nettoyé comme une transcription",
            "2026" in machine and "Objectif : comprendre la source." in machine and "Niveau : 3" in machine,
            machine)
    verifie("l'état porte le chemin de la source",
            etat_de(rac, emp)["fichier"] == f"{emp}.source.md")

    src_txt = rac / "notes.txt"
    src_txt.write_text("Niveau : 3\n2026\nObjectif : comprendre la source.\n", encoding="utf-8")
    code, sortie = lance(rac, "preparer", str(src_txt))
    emp_txt = sha16(src_txt)
    machine_txt = (rac / "sources" / f"{emp_txt}.pages" / "p-0001.txt").read_text(encoding="utf-8")
    verifie("un .txt garde son nom d'archive d'origine", (rac / "sources" / f"{emp_txt}.txt").is_file(), sortie)
    verifie("un .txt garde ses lignes numériques et ses deux-points",
            code == 0 and "2026" in machine_txt and "Niveau : 3" in machine_txt
            and "Objectif : comprendre la source." in machine_txt, machine_txt)


def scenario_reparation_archive_source() -> None:
    """Un document préparé par la version fautive (archive écrasée par le pivot) se répare sans perdre le pivot."""
    rac = racine_test(lignes_par_page=10, mots_page_texte=3)
    src = rac / "cours.md"
    src.write_text(TEXTE_MD, encoding="utf-8")
    lance(rac, "preparer", str(src))
    emp = empreinte_de(rac)
    archive = rac / "sources" / f"{emp}.source.md"
    pivot = rac / "sources" / f"{emp}.md"
    pivot_avant = pivot.read_bytes()
    archive.unlink()
    code, sortie = lance(rac, "preparer", str(src))
    verifie("un document déjà préparé réarchive sa source sans toucher au pivot",
            code == 0 and "déjà préparé" in sortie and archive.read_bytes() == src.read_bytes()
            and pivot.read_bytes() == pivot_avant, sortie)


def scenario_archive_etrangere() -> None:
    """Une archive qui ne porte pas l'empreinte du document n'est jamais écrasée."""
    rac = racine_test(lignes_par_page=10, mots_page_texte=3)
    src = rac / "cours.md"
    src.write_text(TEXTE_MD, encoding="utf-8")
    emp = sha16(src)
    etrangere = rac / "sources" / f"{emp}.source.md"
    etrangere.write_text("un autre document\n", encoding="utf-8")
    code, sortie = lance(rac, "preparer", str(src))
    verifie("une archive étrangère n'est pas écrasée",
            code == 1 and "étrangère" in sortie
            and etrangere.read_text(encoding="utf-8") == "un autre document\n", sortie)
    verifie("un refus n'écrit aucun état", not (rac / "sources" / f"{emp}.etat.json").exists())


def scenario_source_derivee() -> None:
    """Un fichier dérivé posé près du pivot ne passe pas pour la source du document."""
    rac = racine_test(lignes_par_page=10, mots_page_texte=3)
    src = rac / "cours.md"
    src.write_text(TEXTE_MD, encoding="utf-8")
    emp = sha16(src)
    derive = rac / "sources" / f"{emp}.notes.md"
    derive.write_text("des notes prises à la main\n", encoding="utf-8")
    doc = E.Document(rac, emp)
    verifie("aucune source tant que l'original n'est pas archivé", doc.source() is None, str(doc.source()))
    code, sortie = lance(rac, "preparer", str(src))
    verifie("l'archive exacte devient la source, pas le dérivé",
            code == 0 and doc.source() is not None and doc.source().name == f"{emp}.source.md"
            and doc.source().read_bytes() == src.read_bytes(), sortie)


def scenario_depot_partiel() -> None:
    """Un fichier qui échoue (PDF cassé, format refusé, état corrompu) n'arrête plus le dépôt."""
    rac = racine_test(lignes_par_page=10, mots_page_texte=3)
    depot = rac / "sources" / "a-preparer"
    depot.mkdir()
    (depot / "aa-casse.pdf").write_bytes(b"%PDF-1.4\npas un vrai PDF\n")
    (depot / "ab-mauvais.docx").write_bytes(b"un format non pris en charge")
    casse = depot / "ac-etat-casse.txt"
    casse.write_text("Niveau : 3\n2026\nObjectif : comprendre la source.\n", encoding="utf-8")
    emp_casse = sha16(casse)
    (rac / "sources" / f"{emp_casse}.etat.json").write_text('{"unites": [', encoding="utf-8")
    (depot / "zz-bon.md").write_text(TEXTE_MD, encoding="utf-8")
    code, sortie = lance(rac, "deposer")
    emp = sha16(depot / "zz-bon.md")
    verifie("le lot traverse un PDF cassé, un format refusé et un état corrompu",
            (rac / "sources" / f"{emp}.etat.json").is_file() and (rac / "sources" / f"{emp}.source.md").is_file(),
            sortie)
    verifie("le dépôt sort non nul quand un fichier échoue", code == 1, sortie)
    verifie("le bilan sépare les succès, les documents déjà présents et les échecs",
            "1 préparé" in sortie and "3 échec" in sortie and "échec : aa-casse.pdf" in sortie
            and "échec : ab-mauvais.docx" in sortie and "échec : ac-etat-casse.txt" in sortie, sortie)
    verifie("les fichiers refusés restent dans le dépôt de départ",
            (depot / "aa-casse.pdf").is_file() and (depot / "ab-mauvais.docx").is_file()
            and casse.is_file(), sortie)
    verifie("la source d'un fichier refusé est quand même conservée",
            (rac / "sources" / f"{emp_casse}.txt").is_file(), sortie)
    (depot / "aa-casse.pdf").unlink()
    (depot / "ab-mauvais.docx").unlink()
    casse.unlink()
    (rac / "sources" / f"{emp_casse}.etat.json").unlink()
    code, sortie = lance(rac, "deposer")
    verifie("un dépôt entièrement préparé sort à zéro et compte les documents déjà présents",
            code == 0 and "0 préparé" in sortie and "1 déjà" in sortie, sortie)


def main() -> int:
    scenario_transcription_et_pas_a_pas()
    scenario_pdf()
    scenario_depot()
    scenario_transcription_unitaire()
    scenario_document_texte()
    scenario_reparation_archive_source()
    scenario_archive_etrangere()
    scenario_source_derivee()
    scenario_depot_partiel()
    scenario_reprise_ancien_etat()
    if ECHECS:
        print(f"\n{len(ECHECS)} test(s) en échec : {', '.join(ECHECS)}")
        return 1
    print("\nTOUT VERT (usine).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

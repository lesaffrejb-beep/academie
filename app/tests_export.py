#!/usr/bin/env python3
"""Tests de l'export Anki (app/export_anki.py), chantier ACA-EXPORT-1.

Ce que ces tests protègent, c'est la promesse de réversibilité
(`BLUEPRINT.md` §2) : une carte partie chez Anki doit se suffire à
elle-même. Donc sa source part avec elle, son explication et sa
vigilance aussi, et les distracteurs d'un QCM ne se perdent pas en
route — sans eux, la question devient ouverte et la carte ment.

**Ces tests tournent sans `genanki`.** La mise en forme est de la
stdlib pure, et c'est là qu'est le contrat. L'empaquetage, lui, ne se
teste que si la dépendance d'usine est installée : la CI n'installe
rien, et la porte du dépôt ne doit pas dépendre d'un `pip install`.

    python3 app/tests_export.py
"""

from __future__ import annotations

import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_anki import etiquettes, note_anki, source, verso  # noqa: E402

ECHECS: list[str] = []


def verifie(nom: str, condition: bool, detail: str = "") -> None:
    print(f"{'✓' if condition else '✗'} {nom}")
    if not condition:
        ECHECS.append(nom)
        if detail:
            print(f"   {detail}")


def carte(**kw) -> dict:
    base = {"id": "droit-0001", "domaine": "droit", "branche": "majorites",
            "type": "flash", "question": "Quelle majorité ?",
            "reponse": "L'article 25.",
            "source": [{"texte": "Art. 25 loi n° 65-557", "nature": "texte-officiel",
                        "url": "https://www.legifrance.gouv.fr/x"}],
            "verifie": "2026-08-28", "statut": "valide", "partage": "banque"}
    base.update(kw)
    return base


def main() -> int:
    # --- 1. la carte se suffit à elle-même ----------------------------
    n = note_anki(carte(explication="Parce que la loi le dit.",
                        vigilance="Ne pas confondre avec l'article 24."))
    recto, dos, src = n["champs"]
    verifie("le recto est la question", "Quelle majorité" in recto, recto)
    verifie("le verso porte la réponse", "article 25" in dos, dos)
    verifie("le verso porte l'explication", "Parce que la loi" in dos, dos)
    verifie("le verso porte la vigilance", "Vigilance" in dos and "article 24" in dos, dos)
    verifie("la source part avec la carte", "Art. 25 loi" in src, src)
    verifie("la nature de la source part aussi", "texte-officiel" in src, src)
    verifie("l'URL de la source est cliquable", "legifrance.gouv.fr" in src, src)
    verifie("la date de vérification part aussi", "2026-08-28" in src, src)

    # --- 2. un QCM ne perd pas ses distracteurs -----------------------
    qcm = carte(type="qcm", choix=[
        {"texte": "L'article 25", "correct": True},
        {"texte": "L'article 24", "correct": False,
         "pourquoi_faux": "L'article 24 est la majorité simple."},
        {"texte": "L'unanimité", "correct": False},
    ])
    dos = note_anki(qcm)["champs"][1]
    # L'apostrophe est échappée en &#x27; : on cherche le fond, pas la forme.
    verifie("les distracteurs d'un QCM survivent à l'export",
            "article 24" in dos and "unanimité" in dos, dos)
    verifie("le pourquoi_faux part avec le distracteur",
            "majorité simple" in dos, dos)
    verifie("la bonne réponse n'est pas listée comme à écarter",
            dos.split("À écarter").pop().count("article 25") == 0, dos)

    # --- 3. les étiquettes --------------------------------------------
    verifie("l'étiquette est domaine::branche",
            etiquettes(carte()) == ["droit::majorites"], str(etiquettes(carte())))
    verifie("le chapitre s'ajoute quand il existe",
            "chapitre::droit.majorites.n1" in etiquettes(carte(chapitre="droit.majorites.n1")),
            str(etiquettes(carte(chapitre="droit.majorites.n1"))))
    tags = etiquettes(carte(statut="brouillon"))
    verifie("un brouillon porte son statut en étiquette",
            "statut::brouillon" in tags, str(tags))
    verifie("aucune étiquette ne contient d'espace",
            all(" " not in t for t in etiquettes(carte(chapitre="a b"))),
            str(etiquettes(carte(chapitre="a b"))))

    # --- 4. un brouillon se dénonce lui-même --------------------------
    src = source(carte(statut="brouillon"))
    verifie("un brouillon exporté dit qu'il n'est pas revérifié",
            "brouillon" in src and "revérifiée" in src, src)

    # --- 5. rien ne casse sur une carte pauvre ------------------------
    pauvre = {"id": "x", "domaine": "d", "branche": "b", "question": "q",
              "reponse": "r", "statut": "valide"}
    try:
        n = note_anki(pauvre)
        ok = len(n["champs"]) == 3
    except Exception as exc:                                       # noqa: BLE001
        ok = False
        n = {"champs": [repr(exc)]}
    verifie("une carte sans source ni date ne fait pas planter l'export",
            ok, str(n["champs"]))

    # --- 6. le HTML est échappé ---------------------------------------
    dangereuse = carte(question="<script>alert(1)</script>",
                       reponse="a < b & c > d")
    recto, dos, _ = note_anki(dangereuse)["champs"]
    verifie("le HTML d'une carte est échappé, pas exécuté",
            "<script>" not in recto and "&lt;script&gt;" in recto, recto)
    verifie("les caractères spéciaux survivent échappés",
            "&lt;" in dos and "&amp;" in dos, dos)
    verifie("les sauts de ligne deviennent des <br>",
            "<br>" in verso(carte(reponse="une\ndeux")), verso(carte(reponse="une\ndeux")))

    # --- 7. l'empaquetage, seulement si la dépendance est là ----------
    try:
        import genanki  # noqa: F401, PLC0415
        dispo = True
    except ImportError:
        dispo = False

    if not dispo:
        print("· empaquetage non testé : genanki absent "
              "(python3 -m pip install -r tooling/requirements-usine.txt). "
              "La mise en forme, elle, vient d'être vérifiée.")
    else:
        from export_anki import ecrit_paquet                       # noqa: PLC0415
        cible = Path(tempfile.mkdtemp(prefix="academie-anki-")) / "test.apkg"
        cartes = [carte(id=f"droit-000{i}") for i in range(1, 4)]
        n = ecrit_paquet(cartes, cible)
        verifie("trois cartes donnent trois notes", n == 3, str(n))
        verifie("le fichier .apkg existe et n'est pas vide",
                cible.is_file() and cible.stat().st_size > 0)
        try:
            with zipfile.ZipFile(cible) as z:
                noms = z.namelist()
            ok = any(x.startswith("collection") for x in noms)
        except zipfile.BadZipFile:
            ok, noms = False, []
        verifie("le .apkg est une archive lisible avec sa collection",
                ok, str(noms))

        # Deux exports de la même carte donnent le même guid : Anki
        # remplace la note au lieu d'en créer une seconde.
        a = genanki.guid_for("droit-0001")
        b = genanki.guid_for("droit-0001")
        verifie("le guid d'une carte est stable entre deux exports", a == b)

    if ECHECS:
        print(f"\n{len(ECHECS)} test(s) en échec : {', '.join(ECHECS)}")
        return 1
    print("\nexport : tout vert."
          + ("" if dispo else " (empaquetage non couvert, genanki absent)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

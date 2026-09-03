#!/usr/bin/env python3
"""L'export Anki : l'assurance-vie de la réversibilité.

Chantier `ACA-EXPORT-1`. Contrat de réversibilité du `BLUEPRINT.md` §2 :
si l'application maison s'arrête, le contenu se joue ailleurs le
lendemain. L'inverse n'est pas vrai et c'est assumé — Anki ne saura
rejouer ni les ateliers ni la boucle terrain.

Ce fichier est un **outil d'usine**, pas du produit. `genanki` (MIT,
lue à la source le 03/09/2026, `travail/benchmark-2026-08-30.md`
partie 4) est déclaré dans `tooling/requirements-usine.txt` et n'est
jamais chargé par le moteur, le serveur ni le client.

Deux moitiés, volontairement séparées :

  1. **La mise en forme** (`note_anki`) est de la stdlib pure. Elle
     décide ce qui va dans le recto, le verso, la source et les
     étiquettes. C'est là qu'est le contrat, donc c'est là qu'est le
     test, et il tourne partout — y compris en CI, qui n'installe rien.
  2. **L'empaquetage** (`ecrit_paquet`) a besoin de `genanki`. Il est
     importé au dernier moment : sans la dépendance, le script le dit
     et sort proprement, il ne casse pas la porte du dépôt.

Ce que l'export NE porte PAS, et qu'il faut savoir avant d'y compter :
les **images**. Les quatre cartes à image de la banque (`photo`,
`relier`, `datation`, `plan`) partent avec leur texte seul. Embarquer
un média dans un `.apkg` est possible, mais les images de la banque ont
des licences par fichier (`decisions/0017`) et rien ne garantit qu'un
paquet parti chez un tiers les respecte. Tant que la question n'est pas
tranchée, l'export est textuel et le dit.

Usage :
    python3 app/export_anki.py --sortie /tmp/academie.apkg
    python3 app/export_anki.py --domaine droit --sortie /tmp/droit.apkg
    python3 app/export_anki.py --couches banque --avec-brouillons ...

Installation de la dépendance d'usine :
    python3 -m pip install -r tooling/requirements-usine.txt
"""

from __future__ import annotations

import argparse
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from valide_banque import charge_banque  # noqa: E402

# Identifiants Anki, tirés une fois et gravés : un paquet réimporté doit
# se ranger dans le même modèle et le même deck, sinon Anki duplique
# tout à chaque export. Ils ne changent plus.
MODELE_ID = 1607392319
PAQUET_ID = 2059400110
NOM_PAQUET = "Académie"

CHAMPS = ("Recto", "Verso", "Source")


def _echappe(texte: str) -> str:
    """Le HTML d'Anki : on échappe, puis on rend les sauts de ligne."""
    return html.escape(str(texte or "")).replace("\n", "<br>")


def verso(carte: dict) -> str:
    """La réponse, augmentée de l'explication et de la vigilance.

    Le contrat v1 §4 le dit : « réponse (explication et vigilance
    incluses) ». Une carte exportée doit se suffire à elle-même, sinon
    l'assurance-vie ne couvre rien.
    """
    morceaux = [_echappe(carte.get("reponse"))]
    if carte.get("explication"):
        morceaux.append("<p><i>" + _echappe(carte["explication"]) + "</i></p>")
    if carte.get("vigilance"):
        morceaux.append("<p><b>Vigilance</b> : " + _echappe(carte["vigilance"]) + "</p>")
    # Un QCM perd ses boutons en partant, mais pas ses distracteurs :
    # sans eux, la carte exportée devient une question ouverte.
    faux = [c for c in (carte.get("choix") or []) if not c.get("correct")]
    if faux:
        lignes = "".join(
            f"<li>{_echappe(c.get('texte'))}"
            + (f" — {_echappe(c.get('pourquoi_faux'))}" if c.get("pourquoi_faux") else "")
            + "</li>"
            for c in faux)
        morceaux.append(f"<p>À écarter :</p><ul>{lignes}</ul>")
    return "\n".join(morceaux)


def source(carte: dict) -> str:
    """Les sources, avec leur nature, et la date de vérification.

    Une carte servie sans sa source viole la règle dure 3 ; une carte
    exportée sans sa source la violerait tout autant, chez quelqu'un
    d'autre et sans personne pour s'en apercevoir.
    """
    lignes = []
    for s in (carte.get("source") or []):
        texte = _echappe(s.get("texte"))
        nature = s.get("nature")
        if nature:
            texte += f" <i>({_echappe(nature)}"
            if s.get("parti"):
                texte += f", {_echappe(s['parti'])}"
            texte += ")</i>"
        if s.get("url"):
            texte += f'<br><a href="{html.escape(str(s["url"]), quote=True)}">'
            texte += f'{_echappe(s["url"])}</a>'
        lignes.append(f"<li>{texte}</li>")
    corps = f"<ul>{''.join(lignes)}</ul>" if lignes else ""
    if carte.get("verifie"):
        corps += f"<p>Vérifié le {_echappe(carte['verifie'])}"
        if carte.get("peremption"):
            corps += f", périme le {_echappe(carte['peremption'])}"
        corps += ".</p>"
    if carte.get("statut") != "valide":
        corps += (f"<p><b>Statut {_echappe(carte.get('statut'))}</b> : cette carte "
                  f"n'a pas été revérifiée à la source.</p>")
    return corps


def etiquettes(carte: dict) -> list[str]:
    """`domaine::branche`, plus le statut quand il n'est pas `valide`.

    Anki coupe une étiquette sur l'espace : on ne met que des clés, qui
    sont en kebab-case par contrat.
    """
    tags = [f"{carte.get('domaine')}::{carte.get('branche')}"]
    if carte.get("chapitre"):
        tags.append(f"chapitre::{carte['chapitre']}")
    if carte.get("statut") != "valide":
        tags.append(f"statut::{carte.get('statut')}")
    return [t.replace(" ", "-") for t in tags]


def note_anki(carte: dict) -> dict:
    """Une carte de la banque vue comme une note Anki. Stdlib pure."""
    return {
        "id": carte.get("id"),
        "champs": [_echappe(carte.get("question")), verso(carte), source(carte)],
        "tags": etiquettes(carte),
    }


def ecrit_paquet(cartes: list[dict], sortie: Path, nom: str = NOM_PAQUET) -> int:
    """Écrit le `.apkg`. Rend le nombre de notes. Demande `genanki`."""
    try:
        import genanki  # noqa: PLC0415
    except ImportError as exc:                                     # pragma: no cover
        raise SystemExit(
            "genanki absent : python3 -m pip install -r tooling/requirements-usine.txt"
        ) from exc

    modele = genanki.Model(
        MODELE_ID, "Académie (recto, verso, source)",
        fields=[{"name": c} for c in CHAMPS],
        templates=[{
            "name": "Recto vers verso",
            "qfmt": "{{Recto}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Verso}}'
                    '<hr><div class="source">{{Source}}</div>',
        }],
        css=".card{font-family:Georgia,serif;font-size:18px;text-align:left;}"
            ".source{font-size:13px;color:#555;}",
    )
    paquet = genanki.Deck(PAQUET_ID, nom)
    for carte in cartes:
        n = note_anki(carte)
        # `guid` sur l'identifiant de carte : réimporter un export mis à
        # jour remplace la note au lieu d'en créer une deuxième.
        note = genanki.Note(model=modele, fields=n["champs"], tags=n["tags"],
                            guid=genanki.guid_for(n["id"]))
        paquet.add_note(note)
    sortie.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(paquet).write_to_file(str(sortie))
    return len(paquet.notes)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Export Anki de la banque (assurance-vie, BLUEPRINT §2).")
    ap.add_argument("--sortie", type=Path, required=True, help="le fichier .apkg")
    ap.add_argument("--domaine", help="n'exporter qu'un domaine")
    ap.add_argument("--couches", nargs="*", default=["banque"],
                    help="couches de partage exportées (défaut : banque seule)")
    ap.add_argument("--avec-brouillons", action="store_true",
                    help="exporter aussi les cartes non revérifiées")
    ap.add_argument("--nom", default=NOM_PAQUET, help="nom du paquet dans Anki")
    args = ap.parse_args(argv)

    paires, erreurs = charge_banque()
    if erreurs:
        print(f"banque illisible ({len(erreurs)} erreur(s)) : "
              f"python3 app/valide_banque.py", file=sys.stderr)
        return 1

    couches = set(args.couches or [])
    retenues = []
    ecartees = {"couche": 0, "statut": 0, "domaine": 0}
    for carte, _ in paires:
        if carte.get("partage") not in couches:
            ecartees["couche"] += 1
        elif carte.get("statut") != "valide" and not args.avec_brouillons:
            ecartees["statut"] += 1
        elif args.domaine and carte.get("domaine") != args.domaine:
            ecartees["domaine"] += 1
        else:
            retenues.append(carte)

    if not retenues:
        print("aucune carte à exporter (voir --couches, --domaine, "
              "--avec-brouillons)", file=sys.stderr)
        return 1

    n = ecrit_paquet(retenues, args.sortie, args.nom)
    print(f"{n} note(s) → {args.sortie}")
    print(f"  couches : {', '.join(sorted(couches))}")
    if any(ecartees.values()):
        print(f"  écartées : {ecartees['couche']} hors couche, "
              f"{ecartees['statut']} par statut, {ecartees['domaine']} hors domaine")
    brouillons = sum(1 for c in retenues if c.get("statut") != "valide")
    if brouillons:
        print(f"  dont {brouillons} non revérifiée(s) : elles portent leur statut "
              f"en étiquette et dans le champ Source")
    return 0


if __name__ == "__main__":
    sys.exit(main())

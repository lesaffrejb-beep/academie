#!/usr/bin/env python3
"""Tests du tableau de bord du rituel (app/rituel.py), chantier
ACA-RITUAL-METRICS-1.

Quatre fixtures, celles que `roadmap.json` exige :

  1. séance complète       toutes les cartes annoncées ont leur réponse
  2. arrêt après 3 minutes  une partie seulement : abandon, à quel rang
  3. coupure de 3 semaines  la plus longue coupure est trouvée
  4. journal corrompu       ligne illisible, sans `quand`, hors contrat,
                            réponse orpheline : le rapport sort quand même

Plus la promesse qui compte autant que les chiffres : **le rapport ne
lit pas le contenu des réponses**. Une ligne empoisonnée (raison, motif,
attendus_coches, note) ne doit laisser aucune trace dans la sortie.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

APP = Path(__file__).resolve().parent
sys.path.insert(0, str(APP))

import rituel  # noqa: E402

ECHECS: list[str] = []


def verifie(nom: str, condition: bool, detail: str = "") -> None:
    print(f"{'✓' if condition else '✗'} {nom}")
    if not condition:
        ECHECS.append(nom)
        if detail:
            print(f"   {detail}")


def ouverture(quand: str, cartes: list[str], format_: str = "seance", **kw) -> dict:
    return {"quand": quand, "mode": "seance", "nonce": "n" + quand,
            "format": format_, "graine": 1, "cartes": cartes,
            "banque_version": "v", "moteur_version": "v", **kw}


def reponse(quand: str, carte: str, duree_ms: int = 5000, **kw) -> dict:
    return {"quand": quand, "mode": "revision", "nonce": "r" + quand + carte,
            "carte": carte, "note": 3, "format": "seance", "duree_ms": duree_ms, **kw}


def rapport(lignes: list) -> dict:
    """Écrit les lignes dans un JSONL jetable et rend le rapport."""
    tmp = Path(tempfile.mkdtemp(prefix="academie-rituel-")) / "journal.jsonl"
    tmp.write_text("\n".join(l if isinstance(l, str) else json.dumps(l, ensure_ascii=False)
                             for l in lignes) + "\n", encoding="utf-8")
    return rituel.rapport(rituel.lit(tmp))


def main() -> int:
    # --- 1. séance complète -------------------------------------------
    complet = [
        ouverture("2026-09-01T07:00:00+00:00", ["a", "b", "c"]),
        reponse("2026-09-01T07:00:20+00:00", "a", 8000),
        reponse("2026-09-01T07:00:50+00:00", "b", 12000),
        reponse("2026-09-01T07:01:30+00:00", "c", 9000),
    ]
    r = rapport(complet)
    verifie("une séance dont toutes les cartes ont leur réponse est finie",
            r["seances"]["commencees"] == 1 and r["seances"]["finies"] == 1
            and r["seances"]["abandonnees"] == 0, json.dumps(r["seances"]))
    s = r["detail_seances"][0]
    verifie("la durée d'horloge de la séance est la bonne",
            s["duree_horloge_s"] == 90, str(s))
    verifie("la durée des réponses est la somme des duree_ms",
            s["duree_reponses_s"] == 29, str(s))
    verifie("les cartes répondues sont comptées, pas listées",
            s["cartes_repondues"] == 3 and s["cartes_annoncees"] == 3
            and "cartes" not in s, str(s))

    # --- 2. arrêt après trois minutes ---------------------------------
    arret = [
        ouverture("2026-09-02T07:00:00+00:00", ["a", "b", "c", "d", "e", "f"]),
        reponse("2026-09-02T07:00:30+00:00", "a"),
        reponse("2026-09-02T07:01:20+00:00", "b"),
        reponse("2026-09-02T07:03:00+00:00", "c"),
    ]
    r = rapport(arret)
    verifie("une séance interrompue compte abandonnée",
            r["seances"]["commencees"] == 1 and r["seances"]["finies"] == 0
            and r["seances"]["abandonnees"] == 1, json.dumps(r["seances"]))
    s = r["detail_seances"][0]
    verifie("le rang d'abandon est dit, pas la carte",
            s["abandon_au_rang"] == 3 and s["cartes_annoncees"] == 6, str(s))
    verifie("la durée d'horloge d'un arrêt à trois minutes est 180 s",
            s["duree_horloge_s"] == 180, str(s))

    # --- 3. coupure de trois semaines ---------------------------------
    coupure = (
        [ouverture("2026-08-03T07:00:00+00:00", ["a"]), reponse("2026-08-03T07:00:10+00:00", "a")]
        + [ouverture("2026-08-24T07:00:00+00:00", ["a"]), reponse("2026-08-24T07:00:10+00:00", "a")]
    )
    r = rapport(coupure)
    verifie("la plus longue coupure est trouvée en jours",
            r["regularite"]["plus_longue_coupure_jours"] == 21,
            json.dumps(r["regularite"]))
    verifie("les semaines sans séance sont comptées",
            r["regularite"]["semaines_sans_seance"] == 2,
            json.dumps(r["regularite"]))
    verifie("le rapport lisible ne reproche rien",
            not any(m in rituel.rend(r).lower()
                    for m in ("retard", "raté", "perdu", "dette", "rattrap")),
            rituel.rend(r))

    # --- 4. journal corrompu ------------------------------------------
    corrompu = [
        "{ceci n'est pas du JSON",
        json.dumps({"mode": "seance", "nonce": "x"}),                    # sans quand
        json.dumps({"quand": "2026-09-01T07:00:00+00:00", "mode": "danse", "nonce": "y"}),
        json.dumps(["une liste, pas un objet"]),
        json.dumps(reponse("2026-09-01T09:00:00+00:00", "z")),           # orpheline
        json.dumps(ouverture("2026-09-01T10:00:00+00:00", ["a"])),
        json.dumps(reponse("2026-09-01T10:00:10+00:00", "a")),
    ]
    r = rapport(corrompu)
    verifie("un journal corrompu rend quand même un rapport",
            r["seances"]["commencees"] == 1 and r["seances"]["finies"] == 1,
            json.dumps(r["seances"]))
    verifie("les lignes écartées sont comptées, par motif",
            r["ecartees"]["illisible"] == 1 and r["ecartees"]["sans_quand"] == 1
            and r["ecartees"]["mode_inconnu"] == 1 and r["ecartees"]["pas_un_objet"] == 1,
            json.dumps(r["ecartees"]))
    verifie("une réponse hors séance est comptée orpheline",
            r["ecartees"]["reponse_orpheline"] == 1, json.dumps(r["ecartees"]))

    # --- 5. formats et jours de la semaine -----------------------------
    varie = [
        ouverture("2026-09-01T07:00:00+00:00", ["a"], "seance"),          # mardi
        reponse("2026-09-01T07:00:10+00:00", "a"),
        ouverture("2026-09-05T07:00:00+00:00", ["b"], "hasard"),          # samedi
        reponse("2026-09-05T07:00:10+00:00", "b"),
        ouverture("2026-09-08T07:00:00+00:00", ["c"], "seance"),          # mardi
        reponse("2026-09-08T07:00:10+00:00", "c"),
    ]
    r = rapport(varie)
    verifie("les formats sont comptés",
            r["formats"] == {"seance": 2, "hasard": 1}, json.dumps(r["formats"]))
    verifie("les jours de la semaine sont comptés",
            r["jours_semaine"]["mardi"] == 2 and r["jours_semaine"]["samedi"] == 1,
            json.dumps(r["jours_semaine"]))
    verifie("les séances par semaine sont données",
            r["regularite"]["seances_par_semaine_moyenne"] == 1.5,
            json.dumps(r["regularite"]))

    # --- 6. le rapport ne lit pas le contenu ---------------------------
    poison = "CONTENU-SECRET-QUI-NE-DOIT-PAS-SORTIR"
    empoisonne = [
        ouverture("2026-09-01T07:00:00+00:00", ["a"], cap=poison),
        reponse("2026-09-01T07:00:10+00:00", "a", raison=poison, motif=poison,
                attendus_coches=[1, 2], origine=poison),
        {"quand": "2026-09-01T07:05:00+00:00", "mode": "erreur", "nonce": "e1",
         "carte": "a", "raison": poison},
    ]
    r = rapport(empoisonne)
    verifie("aucun contenu de réponse ne ressort du rapport",
            poison not in json.dumps(r, ensure_ascii=False) and poison not in rituel.rend(r),
            "le rapport laisse fuir le contenu")
    # La promesse tient au chargement, pas seulement à la sortie : une
    # ligne lue ne doit porter que la liste blanche. Sans ce test, on
    # pourrait charger tout le journal en mémoire sans qu'aucun chiffre
    # ne bouge, et la garantie ne serait plus qu'une intention.
    tmp = Path(tempfile.mkdtemp(prefix="academie-rituel-")) / "journal.jsonl"
    tmp.write_text("\n".join(json.dumps(l, ensure_ascii=False) for l in empoisonne) + "\n",
                   encoding="utf-8")
    charge = rituel.lit(tmp)
    trop = sorted({c for l in charge["lignes"] for c in l} - set(rituel.CHAMPS_LUS) - {"_instant"})
    verifie("une ligne chargée ne porte que les champs de la liste blanche",
            not trop, f"champs chargés en trop : {trop}")

    verifie("la liste blanche des champs lus est explicite et fermée",
            set(rituel.CHAMPS_LUS) == {"quand", "mode", "format", "duree_ms",
                                       "cartes", "carte", "jour"},
            str(sorted(rituel.CHAMPS_LUS)))

    # --- 7. le vide n'est pas une erreur -------------------------------
    r = rapport([])
    verifie("un journal vide rend un rapport vide, sans planter",
            r["seances"]["commencees"] == 0 and r["periode"]["de"] is None,
            json.dumps(r["seances"]))

    if ECHECS:
        print(f"\n{len(ECHECS)} test(s) en échec : {', '.join(ECHECS)}")
        return 1
    print("\nrituel : tout vert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

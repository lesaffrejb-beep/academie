#!/usr/bin/env python3
"""Le tableau de bord du rituel : ce que le journal dit de l'habitude.

    python3 app/rituel.py <journal.jsonl>
    python3 app/rituel.py <journal.jsonl> --json

Chantier `ACA-RITUAL-METRICS-1`. Ce rapport est l'instrument du gate de
`ACA-RITUAL-1` : sans lui, « au moins quatre séances par semaine »
(`ROADMAP.md`) reste une intention. Il mesure **l'habitude**, jamais le
savoir : combien de séances, combien finies, combien abandonnées et à
quel rang, combien de temps, quels formats, quels jours, quelles
coupures.

Trois règles qui tiennent ce fichier :

1. **Il ne lit pas le contenu des réponses.** Chaque ligne est projetée
   sur `CHAMPS_LUS`, une liste blanche fermée, avant tout traitement. Ni
   `raison`, ni `motif`, ni `attendus_coches`, ni `note` n'existent pour
   lui : la mesure du savoir est le bilan de `ACA-RITUAL-1`, pas ceci.
2. **Il n'écrit rien et n'appelle personne.** Lecture seule d'un fichier
   local, aucune requête (`decisions/0020`).
3. **Un journal abîmé ne l'arrête pas.** Une ligne illisible, sans date,
   de mode inconnu ou orpheline est comptée par motif et le rapport
   sort. Un journal est une matière de terrain, pas une base propre.

Une séance s'ouvre par une ligne `mode: seance` (contrat
`contrats/journal-v1.schema.json`) qui annonce ses cartes ; les lignes
`revision`, `quiz` et `examen` qui suivent, jusqu'à la prochaine
ouverture, sont ses réponses. Une séance est **finie** quand toutes les
cartes annoncées ont leur réponse, **abandonnée** sinon, et
**indéterminée** quand l'ouverture n'annonce pas ses cartes (un journal
v0 migré, par exemple).

Le ton du rapport suit `VOIX.md` : il constate, il ne reproche pas. Une
coupure de trois semaines est une ligne du rapport, pas une faute.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# Liste blanche fermée. Tout autre champ d'une ligne de journal est
# écarté à la lecture : le rapport ne peut pas laisser fuir ce qu'il
# n'a jamais chargé.
CHAMPS_LUS = ("quand", "mode", "format", "duree_ms", "cartes", "carte", "jour")

MODES = {"revision", "quiz", "examen", "erreur", "seance", "synthese", "signalement"}
MODES_REPONSE = {"revision", "quiz", "examen"}
JOURS = ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")

# Les motifs d'écart, dans l'ordre où ils se produisent.
MOTIFS = ("illisible", "pas_un_objet", "sans_quand", "date_illisible",
          "mode_inconnu", "reponse_orpheline")


def _instant(quand: str) -> datetime | None:
    try:
        return datetime.fromisoformat(str(quand).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def lit(chemin: Path | str) -> dict:
    """Le journal projeté sur la liste blanche, trié, avec ses écarts.

    Rend `{"lignes": [...], "ecartees": Counter}`. Une ligne gardée ne
    porte que les champs de `CHAMPS_LUS`, plus `_instant` (la date
    analysée). Rien d'autre du journal n'entre en mémoire.
    """
    chemin = Path(chemin)
    ecartees: Counter[str] = Counter({m: 0 for m in MOTIFS})
    gardees: list[dict] = []
    brut = chemin.read_text(encoding="utf-8") if chemin.is_file() else ""
    for texte in brut.splitlines():
        texte = texte.strip()
        if not texte:
            continue
        try:
            ligne = json.loads(texte)
        except json.JSONDecodeError:
            ecartees["illisible"] += 1
            continue
        if not isinstance(ligne, dict):
            ecartees["pas_un_objet"] += 1
            continue
        if not ligne.get("quand"):
            ecartees["sans_quand"] += 1
            continue
        instant = _instant(ligne["quand"])
        if instant is None:
            ecartees["date_illisible"] += 1
            continue
        if ligne.get("mode") not in MODES:
            ecartees["mode_inconnu"] += 1
            continue
        propre = {c: ligne[c] for c in CHAMPS_LUS if c in ligne}
        propre["_instant"] = instant
        gardees.append(propre)
    gardees.sort(key=lambda l: l["_instant"])
    return {"lignes": gardees, "ecartees": ecartees}


def _decoupe(lignes: list[dict], ecartees: Counter) -> list[dict]:
    """Les séances, une par ligne `mode: seance`, avec leurs réponses."""
    seances: list[dict] = []
    for ligne in lignes:
        mode = ligne["mode"]
        if mode == "seance":
            seances.append({"ouverture": ligne, "reponses": []})
        elif mode in MODES_REPONSE:
            if not seances:
                ecartees["reponse_orpheline"] += 1
            else:
                seances[-1]["reponses"].append(ligne)
    return seances


def _mesure(seance: dict) -> dict:
    """Les chiffres d'une séance. Aucun identifiant de carte n'en sort."""
    ouverture, reponses = seance["ouverture"], seance["reponses"]
    annoncees = ouverture.get("cartes")
    annoncees = list(annoncees) if isinstance(annoncees, list) else None
    repondues = [str(r["carte"]) for r in reponses if r.get("carte")]
    distinctes = list(dict.fromkeys(repondues))

    debut = ouverture["_instant"]
    fin = reponses[-1]["_instant"] if reponses else debut
    horloge = int((fin - debut).total_seconds())
    somme = sum(int(r.get("duree_ms") or 0) for r in reponses)

    if annoncees is None:
        statut = "indeterminee"
        rang = None
    elif set(annoncees).issubset(set(distinctes)):
        statut = "finie"
        rang = None
    else:
        statut = "abandonnee"
        # Le rang de la dernière carte annoncée qui a reçu une réponse.
        # On dit le rang, jamais la carte : la mesure est de l'habitude.
        rangs = [annoncees.index(c) + 1 for c in distinctes if c in annoncees]
        rang = max(rangs) if rangs else 0

    return {
        "quand": debut.isoformat(),
        "jour_semaine": JOURS[debut.weekday()],
        "format": ouverture.get("format") or "inconnu",
        "statut": statut,
        "cartes_annoncees": len(annoncees) if annoncees is not None else None,
        "cartes_repondues": len(distinctes),
        "abandon_au_rang": rang,
        "duree_horloge_s": horloge,
        "duree_reponses_s": round(somme / 1000),
    }


def _regularite(mesures: list[dict]) -> dict:
    """Semaines couvertes, séances par semaine, plus longue coupure."""
    if not mesures:
        return {"semaines_couvertes": 0, "semaines_avec_seance": 0,
                "semaines_sans_seance": 0, "seances_par_semaine_moyenne": 0.0,
                "plus_longue_coupure_jours": 0}
    jours = sorted({datetime.fromisoformat(m["quand"]).date() for m in mesures})
    coupure = max((int((b - a).days) for a, b in zip(jours, jours[1:])), default=0)

    # Une semaine est ancrée sur son lundi : le lundi et le samedi
    # suivants comptent pour une, et le compte ne dépend pas du
    # découpage ISO au passage d'une année.
    lundi = lambda d: d.toordinal() - d.weekday()  # noqa: E731
    semaines = {lundi(d) for d in jours}
    couvertes = (lundi(jours[-1]) - lundi(jours[0])) // 7 + 1

    return {
        "semaines_couvertes": couvertes,
        "semaines_avec_seance": len(semaines),
        "semaines_sans_seance": couvertes - len(semaines),
        "seances_par_semaine_moyenne": round(len(mesures) / couvertes, 2),
        "plus_longue_coupure_jours": coupure,
    }


def rapport(journal: dict) -> dict:
    """Le rapport complet, sérialisable, sans contenu de réponse."""
    lignes, ecartees = journal["lignes"], journal["ecartees"]
    seances = _decoupe(lignes, ecartees)
    mesures = [_mesure(s) for s in seances]
    statuts = Counter(m["statut"] for m in mesures)

    finies = [m for m in mesures if m["statut"] == "finie"]
    return {
        "periode": {
            "de": lignes[0]["_instant"].isoformat() if lignes else None,
            "a": lignes[-1]["_instant"].isoformat() if lignes else None,
            "lignes_lues": len(lignes),
        },
        "seances": {
            "commencees": len(mesures),
            "finies": statuts["finie"],
            "abandonnees": statuts["abandonnee"],
            "indeterminees": statuts["indeterminee"],
        },
        "duree": {
            "horloge_mediane_s": _mediane([m["duree_horloge_s"] for m in finies]),
            "reponses_medianes_s": _mediane([m["duree_reponses_s"] for m in finies]),
            "horloge_totale_s": sum(m["duree_horloge_s"] for m in mesures),
        },
        "formats": dict(Counter(m["format"] for m in mesures)),
        "jours_semaine": {j: n for j, n in
                          sorted(Counter(m["jour_semaine"] for m in mesures).items(),
                                 key=lambda kv: JOURS.index(kv[0]))},
        "regularite": _regularite(mesures),
        "ecartees": dict(ecartees),
        "detail_seances": mesures,
    }


def _mediane(valeurs: list[int]) -> int:
    if not valeurs:
        return 0
    tri = sorted(valeurs)
    milieu = len(tri) // 2
    return tri[milieu] if len(tri) % 2 else (tri[milieu - 1] + tri[milieu]) // 2


def rend(r: dict) -> str:
    """Le rapport en clair. Il constate, il ne reproche pas (VOIX.md)."""
    if not r["periode"]["de"]:
        return "Journal vide : aucune séance à mesurer."
    s, reg = r["seances"], r["regularite"]
    lignes = [
        f"Du {r['periode']['de'][:10]} au {r['periode']['a'][:10]}, "
        f"{r['periode']['lignes_lues']} ligne(s) lue(s).",
        "",
        f"Séances ouvertes : {s['commencees']}. "
        f"Menées au bout : {s['finies']}. "
        f"Laissées en route : {s['abandonnees']}."
        + (f" Sans cartes annoncées : {s['indeterminees']}." if s["indeterminees"] else ""),
        f"Durée d'une séance menée au bout, en médiane : "
        f"{r['duree']['horloge_mediane_s']} s d'horloge, "
        f"{r['duree']['reponses_medianes_s']} s de réponses.",
        "",
        f"Régularité : {reg['seances_par_semaine_moyenne']} séance(s) par semaine "
        f"sur {reg['semaines_couvertes']} semaine(s) couverte(s), dont "
        f"{reg['semaines_avec_seance']} avec au moins une séance.",
        f"Plus longue coupure : {reg['plus_longue_coupure_jours']} jour(s). "
        "Une coupure se constate, elle ne se paie pas.",
        "",
        "Formats : " + (", ".join(f"{k} {v}" for k, v in r["formats"].items()) or "aucun"),
        "Jours : " + (", ".join(f"{k} {v}" for k, v in r["jours_semaine"].items()) or "aucun"),
    ]
    ecarts = {k: v for k, v in r["ecartees"].items() if v}
    if ecarts:
        lignes += ["", "Lignes écartées : "
                   + ", ".join(f"{k.replace('_', ' ')} {v}" for k, v in ecarts.items())
                   + ". Le journal reste tel quel : rien n'a été réécrit."]
    return "\n".join(lignes)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Le tableau de bord du rituel, depuis un journal-v1 en JSONL.")
    ap.add_argument("journal", help="chemin d'un journal-v1 en JSONL (serveur/API.md, GET /journal/export)")
    ap.add_argument("--json", action="store_true", help="la sortie machine")
    args = ap.parse_args(argv)

    chemin = Path(args.journal)
    if not chemin.is_file():
        print(f"journal introuvable : {chemin}", file=sys.stderr)
        return 2
    r = rapport(lit(chemin))
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else rend(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())

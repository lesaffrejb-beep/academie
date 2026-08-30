#!/usr/bin/env python3
"""La séance du jour : ce que l'Académie propose ce matin.

Assemble, dans l'ordre du BLUEPRINT §4 : les révisions dues (FSRS), le
neuf, puis la clôture. Deux principes portés ici et pas ailleurs :

  1. **On ré-étale, on ne jette jamais.** Après trois semaines de
     saison d'AG, l'arriéré ne s'affiche pas en entier : la séance
     plafonne (`plafond_reprise`) et le reste revient les jours
     suivants. Revenir doit ressembler à une séance normale un peu
     dense, jamais à une dette de 200 cartes.
  2. **L'état se recalcule depuis le journal**, jamais depuis un « état
     courant » stocké. `revues.jsonl` est append-only : deux appareils
     qui écrivent chacun leur bout fusionnent par union horodatée, sans
     conflit possible. C'est la même philosophie que le JOURNAL des
     copros.

Usage :
    python3 app/seance.py                    # la séance du jour
    python3 app/seance.py --profil jb --json
    python3 app/seance.py --noter <id> <1-4> # enregistre une réponse
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from planificateur import Planificateur  # noqa: E402
from valide_banque import charge_banque, charge_config  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
ETAT = RACINE / "etat"


def chemin_revues(profil: str) -> Path:
    return ETAT / profil / "revues.jsonl"


def lit_journal(profil: str) -> list[dict]:
    """Le journal append-only, trié par horodatage."""
    p = chemin_revues(profil)
    if not p.is_file():
        return []
    revues = []
    for n, ligne in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        ligne = ligne.strip()
        if not ligne:
            continue
        try:
            revues.append(json.loads(ligne))
        except json.JSONDecodeError:
            print(f"⚠ {p.name}:{n} illisible, ignorée", file=sys.stderr)
    return sorted(revues, key=lambda r: r.get("quand", ""))


def etats_cartes(journal: list[dict], sched: Planificateur) -> dict[str, dict]:
    """Rejoue tout le journal pour retrouver l'état FSRS de chaque carte.

    Recalculé à chaque fois, jamais stocké : c'est ce qui permet de
    changer les paramètres FSRS (ou de corriger un bug du moteur) sans
    perdre l'historique.

    Une entrée peut porter `stabilite_forcee` : la stabilité vaut alors
    cette valeur au lieu de celle que FSRS aurait calculée (la
    difficulté, elle, reste celle du moteur). Un seul écrivain
    aujourd'hui, le quiz de positionnement (`quiz.py`), dont les bonnes
    réponses sont des postulats de départ et non des révisions
    observées. Champ optionnel : un journal qui ne le porte pas se
    rejoue exactement comme avant.
    """
    etats: dict[str, dict] = {}
    for revue in journal:
        cid, note = revue.get("carte"), revue.get("note")
        quand = revue.get("quand")
        if not cid or note not in (1, 2, 3, 4) or not quand:
            continue
        jour = datetime.fromisoformat(quand).date()
        ancien = etats.get(cid)
        if ancien is None:
            s, d = sched.premiere(note)
        else:
            ecoules = (jour - ancien["vu_le"]).days
            s, d = sched.revise(ancien["stabilite"], ancien["difficulte"],
                                note, max(0, ecoules))
        forcee = revue.get("stabilite_forcee")
        if forcee is not None:
            try:
                valeur = float(forcee)
            except (TypeError, ValueError):
                valeur = 0.0               # valeur illisible : FSRS garde la main
            if valeur > 0:
                s = valeur
        etats[cid] = {"stabilite": s, "difficulte": d, "vu_le": jour,
                      "du_le": jour.toordinal() + sched.intervalle(s),
                      "revues": (ancien["revues"] + 1) if ancien else 1,
                      "dernière_note": note}
    return etats


def compose(cartes: list[dict], etats: dict, config: dict, aujourdhui: date,
            sched: Planificateur, graine: int | None = None) -> dict:
    """Choisit ce qui se joue ce matin."""
    quotas = config["quotas"]
    jouables = [c for c in cartes if c.get("statut") == "valide"]

    dues, neuves = [], []
    for carte in jouables:
        etat = etats.get(carte["id"])
        if etat is None:
            neuves.append(carte)
        elif etat["du_le"] <= aujourdhui.toordinal():
            dues.append((carte, etat))

    # Les plus en retard d'abord : ce sont celles qui s'effacent.
    dues.sort(key=lambda ce: ce[1]["du_le"])
    plafond = quotas.get("plafond_reprise", 20)
    arriere = max(0, len(dues) - plafond)
    dues = dues[:plafond]

    # Entrelacement (§3.5) : on mélange les domaines plutôt que de
    # servir quinze minutes d'un seul. Le tri par retard est conservé
    # en gros, mais on évite les blocs monothématiques.
    rng = random.Random(graine if graine is not None else aujourdhui.toordinal())
    dues = entrelace([c for c, _ in dues], rng)

    rng.shuffle(neuves)
    neuves = neuves[:quotas.get("nouveau_par_seance", 1)]

    return {
        "date": aujourdhui.isoformat(),
        "revisions": [carte_seance(c, etats.get(c["id"]), sched) for c in dues],
        "nouveau": [carte_seance(c, None, sched) for c in neuves],
        "arriere_reetale": arriere,
        "total_jouable": len(jouables),
        "jamais_vues": sum(1 for c in jouables if c["id"] not in etats),
    }


def entrelace(cartes: list[dict], rng: random.Random) -> list[dict]:
    """Alterne les domaines autant que possible (interleaving, §3.5)."""
    paquets: dict[str, list[dict]] = {}
    for c in cartes:
        paquets.setdefault(c["domaine"], []).append(c)
    ordre, restants = [], list(paquets.values())
    while restants:
        rng.shuffle(restants)
        for paquet in list(restants):
            if paquet:
                ordre.append(paquet.pop(0))
            if not paquet:
                restants.remove(paquet)
    return ordre


def carte_seance(carte: dict, etat: dict | None, sched: Planificateur) -> dict:
    """La carte telle que la séance la présente."""
    sortie = dict(carte)
    if etat:
        sortie["_etat"] = {
            "revues": etat["revues"],
            "stabilite_jours": round(etat["stabilite"], 1),
            "retard_jours": max(0, date.today().toordinal() - etat["du_le"]),
        }
    return sortie


def note(profil: str, carte_id: str, valeur: int, mode: str = "flash") -> dict:
    """Écrit une réponse au journal. Append-only, jamais de réécriture."""
    if valeur not in (1, 2, 3, 4):
        raise ValueError("note attendue entre 1 (raté) et 4 (facile)")
    p = chemin_revues(profil)
    p.parent.mkdir(parents=True, exist_ok=True)
    ligne = {"quand": datetime.now(timezone.utc).isoformat(timespec="seconds"),
             "carte": carte_id, "note": valeur, "mode": mode}
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    return ligne


def main() -> int:
    ap = argparse.ArgumentParser(description="La séance du jour.")
    ap.add_argument("--profil")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--noter", nargs=2, metavar=("CARTE", "NOTE"))
    ap.add_argument("--sortie", type=Path)
    args = ap.parse_args()

    config = charge_config()
    profil = args.profil or config.get("profil_defaut", "jb")

    if args.noter:
        ligne = note(profil, args.noter[0], int(args.noter[1]))
        print(f"noté : {ligne['carte']} → {ligne['note']}")
        return 0

    sched = Planificateur(retention=config["fsrs"]["retention_souhaitee"])
    paires, erreurs = charge_banque()
    if erreurs:
        print(f"banque illisible ({len(erreurs)} erreur(s)) : "
              f"python3 app/valide_banque.py", file=sys.stderr)
        return 1
    cartes = [c for c, _ in paires]
    journal = lit_journal(profil)
    etats = etats_cartes(journal, sched)
    seance = compose(cartes, etats, config, date.today(), sched)

    if args.sortie:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        args.sortie.write_text(
            json.dumps(seance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(seance, ensure_ascii=False, indent=2))
        return 0

    print(f"Séance du {seance['date']} — profil {profil}")
    print(f"  {len(seance['revisions'])} révision(s) due(s), "
          f"{len(seance['nouveau'])} nouvelle(s)")
    if seance["arriere_reetale"]:
        print(f"  {seance['arriere_reetale']} carte(s) ré-étalée(s) sur les "
              f"jours suivants (jamais affichées en dette)")
    print(f"  banque : {seance['total_jouable']} carte(s) jouable(s), "
          f"{seance['jamais_vues']} jamais vue(s)")
    if not seance["total_jouable"]:
        print("\n  Aucune carte `valide` : la banque n'est pas encore vérifiée.")
        print("  Les cartes `brouillon` ne se jouent jamais (contrat carte-v1 §3.3).")
    for c in seance["revisions"][:5]:
        etat = c.get("_etat", {})
        print(f"    · [{c['domaine']}] {c['question'][:60]}… "
              f"(vue {etat.get('revues', 0)}×)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

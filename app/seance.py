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
import hashlib
import json
import random
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chronologie import cle_chronologique
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
    return sorted(revues, key=cle_chronologique)


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
    for revue in sorted(journal, key=cle_chronologique):
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


# --- la semaine type et le socle (ACA-SEMAINE-1) ----------------------
#
# La couleur du jour ne pèse QUE sur le neuf et sur l'ordre : les
# révisions dues sont servies tous les jours, dimanche compris
# (BLUEPRINT §4, decisions/0016). Rien ici ne bloque quoi que ce soit.

JOURS_SEMAINE = ("lundi", "mardi", "mercredi", "jeudi", "vendredi",
                 "samedi", "dimanche")
COULEURS = ("fondations", "cours", "terrain", "exploration", "etude", "libre")


def couleur_du_jour(config: dict, jour: date) -> str:
    """La couleur d'un jour selon `semaine_type`. Par défaut : cours."""
    table = config.get("semaine_type") or {}
    return table.get(JOURS_SEMAINE[jour.weekday()], "cours")


def branche_socle_la_plus_faible(cartes: list[dict], etats: dict, config: dict,
                                 programme: dict) -> str | None:
    """`<domaine>.<branche>` du socle la moins avancée, ou None.

    Réutilise `progression.noeuds_et_branches` : une seule mesure de
    remplissage dans tout le moteur (BLUEPRINT §5). Rend None quand le
    socle est déjà tenu partout, ou qu'il n'y a rien à mesurer.
    """
    if not programme or not config.get("socle"):
        return None
    from progression import noeuds_et_branches, reglages  # noqa: PLC0415

    domaines_socle = set((config["socle"].get("niveaux") or {}))
    if not domaines_socle:
        return None
    _, branches = noeuds_et_branches(cartes, [], config, programme, etats,
                                     set(), date.today())
    candidates = [b for b in branches if b["domaine"] in domaines_socle
                  and b["noeuds_servis"]]
    if not candidates:
        return None
    faible = min(candidates, key=lambda b: (b["remplissage"], b["domaine"], b["cle"]))
    # Socle tenu partout : la pondération s'éteint, FSRS entretient
    # (`decisions/0013` §5). Elle reprendra d'elle-même si une branche
    # pâlit, puisque tout se recalcule depuis le journal.
    if faible["remplissage"] >= reglages(config)["seuil_ouverture_region"]:
        return None
    return f"{faible['domaine']}.{faible['cle']}"


def quota_de_neuf(config: dict, couleur: str, dues: int, deja_du_jour: int
                  ) -> tuple[int, list[str]]:
    """Combien de cartes neuves ce matin, et pourquoi.

    Fonction pure, sans tirage : c'est la partie de la composition que
    le client doit reproduire à l'identique (`web/src/moteur/composeur.ts`).
    Le tirage, lui, n'est pas comparable — les deux générateurs
    pseudo-aléatoires diffèrent, et c'est assumé.
    """
    quotas = config["quotas"]
    pourquoi: list[str] = []
    quota = quotas.get("nouveau_par_seance", 1)
    if couleur in ("cours", "terrain"):
        quota = quotas.get("nouveau_par_seance_max", quota)
    if couleur == "libre":
        quota = 0
        pourquoi.append("dimanche libre : rien de neuf n'est poussé")
    if couleur == "fondations":
        seuil = quotas.get("fondations_dues_sans_neuf", 15)
        if dues > seuil:
            quota = 0
            pourquoi.append(f"lundi fondations : {dues} cartes dues, plus de "
                            f"{seuil}, on rattrape avant d'ouvrir du neuf")
    par_jour = quotas.get("nouveau_par_jour", 20)
    reste = max(0, par_jour - deja_du_jour)
    if reste < quota:
        pourquoi.append(f"plafond de {par_jour} cartes neuves par jour atteint"
                        if reste == 0 else
                        "plafond de neuf du jour presque atteint")
    return min(quota, reste), pourquoi


def _neuf_du_jour(journal: list[dict] | None, jour: date) -> int:
    """Combien de cartes neuves ont déjà été introduites aujourd'hui."""
    if not journal:
        return 0
    prefixe = jour.isoformat()
    return sum(1 for e in journal
               if str(e.get("quand", "")).startswith(prefixe)
               and e.get("origine") == "nouveau")


def compose(cartes: list[dict], etats: dict, config: dict, aujourdhui: date,
            sched: Planificateur, graine: int | None = None,
            cap: str | None = None, programme: dict | None = None,
            journal: list[dict] | None = None) -> dict:
    """Choisit ce qui se joue ce matin.

    `cap` est le domaine choisi par le joueur (« ce matin, compta ») :
    il l'obtient sans pondération, et la pondération reprend le
    lendemain (`decisions/0013`). `programme` sert à trouver la branche
    du socle la moins avancée ; sans lui, la séance est exactement celle
    d'avant `ACA-SEMAINE-1`.
    """
    quotas = config["quotas"]
    jouables = [c for c in cartes if c.get("statut") == "valide"]
    couleur = couleur_du_jour(config, aujourdhui)
    pourquoi: list[str] = []

    dues, neuves = [], []
    for carte in jouables:
        etat = etats.get(carte["id"])
        if etat is None:
            neuves.append(carte)
        elif etat["du_le"] <= aujourdhui.toordinal():
            dues.append((carte, etat))

    # Les plus en retard d'abord : ce sont celles qui s'effacent.
    dues.sort(key=lambda ce: ce[1]["du_le"])

    # Séance de domaine : le cap tient la séance, et au plus
    # `rappels_d_ailleurs_max` révisions d'ailleurs s'y glissent, les
    # plus en retard, annoncées (BLUEPRINT §3).
    rappels: list[str] = []
    if cap:
        du_cap = [ce for ce in dues if ce[0].get("domaine") == cap]
        ailleurs = [ce for ce in dues if ce[0].get("domaine") != cap]
        maxi = quotas.get("rappels_d_ailleurs_max", 2)
        ailleurs = ailleurs[:maxi]
        rappels = [c["id"] for c, _ in ailleurs]
        dues = du_cap + ailleurs
        dues.sort(key=lambda ce: ce[1]["du_le"])
        if rappels:
            pourquoi.append(f"{len(rappels)} rappel(s) d'ailleurs, les plus en retard")

    plafond = quotas.get("plafond_reprise", 20)
    arriere = max(0, len(dues) - plafond)
    dues_avant_plafond = len(dues)
    dues = dues[:plafond]

    # Entrelacement (§3.5) : on mélange les domaines plutôt que de
    # servir quinze minutes d'un seul. Le tri par retard est conservé
    # en gros, mais on évite les blocs monothématiques.
    rng = random.Random(graine if graine is not None else aujourdhui.toordinal())
    dues = entrelace([c for c, _ in dues], rng)

    # --- combien de neuf, ce matin -------------------------------------
    quota_neuf, raisons = quota_de_neuf(
        config, couleur, dues_avant_plafond, _neuf_du_jour(journal, aujourdhui))
    pourquoi += raisons

    # --- lesquelles ---------------------------------------------------
    branche_socle = None
    rng.shuffle(neuves)
    if cap:
        neuves = [c for c in neuves if c.get("domaine") == cap]
        pourquoi.append(f"domaine choisi : {cap}, la pondération du socle se tait")
    else:
        favoris = (config.get("calendrier_metier") or {}).get(str(aujourdhui.month), [])
        if favoris and couleur in ("cours", "terrain"):
            neuves.sort(key=lambda c: c.get("domaine") not in favoris)
            pourquoi.append("calendrier du métier : "
                            + ", ".join(favoris) + " passent devant ce mois-ci")
        branche_socle = branche_socle_la_plus_faible(cartes, etats, config,
                                                     programme or {})
        if branche_socle and quota_neuf:
            part = quotas.get("ponderation_socle", 0.5)
            # « la moitié du neuf » s'arrondit vers le haut : sur trois
            # cartes, deux vont au socle, pas une (decisions/0013).
            vises = max(1, int(quota_neuf * part + 0.5))
            du_socle = [c for c in neuves
                        if str(c.get("chapitre") or "").startswith(branche_socle + ".")]
            autres = [c for c in neuves if c not in du_socle]
            neuves = du_socle[:vises] + autres + du_socle[vises:]
            if du_socle:
                pourquoi.append(f"socle : {min(vises, len(du_socle))} carte(s) neuve(s) "
                                f"sur la branche la moins avancée ({branche_socle})")

    if not any(c["id"] in etats for c in jouables) and neuves:
        niveau_entree = min(c.get("niveau", 1) for c in neuves)
        neuves = [c for c in neuves if c.get("niveau", 1) == niveau_entree]
        pourquoi.append("première séance : commencer par les fondations disponibles")
    neuves = neuves[:quota_neuf]

    return {
        "date": aujourdhui.isoformat(),
        "jour": couleur,
        "cap": cap,
        "graine": graine if graine is not None else aujourdhui.toordinal(),
        "branche_socle": branche_socle,
        "rappels_d_ailleurs": rappels,
        "pourquoi": pourquoi,
        "revisions": [carte_seance(c, etats.get(c["id"]), sched) for c in dues],
        "nouveau": [carte_seance(c, None, sched) for c in neuves],
        "arriere_reetale": arriere,
        "total_jouable": len(jouables),
        "jamais_vues": sum(1 for c in jouables if c["id"] not in etats),
    }


def ligne_ouverture(seance: dict, banque_version: str, moteur_version: str,
                    quand: str | None = None) -> dict:
    """La ligne `mode: seance` de `journal-v1` qui ouvre une séance.

    Elle dit ce qu'il faut pour rejouer la séance à l'identique : la
    graine, la couleur du jour, le cap, les versions, et les cartes
    servies. Elle ne porte ni note ni réponse : c'est une ouverture.
    """
    quand = quand or datetime.now(timezone.utc).isoformat(timespec="seconds")
    cartes = [c["id"] for c in seance["revisions"] + seance["nouveau"]]
    graine = seance["graine"]
    empreinte = hashlib.sha256(
        f"{quand}|{graine}|{','.join(cartes)}".encode("utf-8")).hexdigest()[:16]
    ligne = {
        "quand": quand,
        "mode": "seance",
        "nonce": empreinte,
        "format": "domaine" if seance.get("cap") else "seance",
        "graine": graine,
        "jour": seance["jour"],
        "banque_version": banque_version,
        "moteur_version": moteur_version,
        "cartes": cartes,
    }
    if seance.get("cap"):
        ligne["cap"] = seance["cap"]
    return ligne


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
    ap.add_argument("--cap", help="le domaine choisi pour ce matin (decisions/0013)")
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
    from genere import charge_programme  # noqa: PLC0415
    seance = compose(cartes, etats, config, date.today(), sched,
                     cap=args.cap, programme=charge_programme() or None,
                     journal=journal)

    if args.sortie:
        args.sortie.parent.mkdir(parents=True, exist_ok=True)
        args.sortie.write_text(
            json.dumps(seance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(seance, ensure_ascii=False, indent=2))
        return 0

    print(f"Séance du {seance['date']} — profil {profil} "
          f"— jour {seance['jour']}"
          + (f", cap {seance['cap']}" if seance.get("cap") else ""))
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
    for raison in seance.get("pourquoi", []):
        print(f"  · {raison}")
    for c in seance["revisions"][:5]:
        etat = c.get("_etat", {})
        print(f"    · [{c['domaine']}] {c['question'][:60]}… "
              f"(vue {etat.get('revues', 0)}×)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

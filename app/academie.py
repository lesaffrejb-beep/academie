#!/usr/bin/env python3
"""La surface de jeu du dépôt, pour un agent.

Depuis la décision 0054 il n'y a plus de front : l'interface est ce
dépôt, discuté par un agent (OpenCode, Claude Code, Codex, Gemini,
Antigravity). Ce fichier est la seule surface que l'agent appelle.

Trois principes, et rien d'autre :

  1. **Le moteur décide.** La séance, l'ordre et le moment du rappel
     viennent de `seance.py`, `progression.py` et `planificateur.py`.
     Cette surface les relaie, elle ne recompose jamais une séance.
  2. **La banque est la vérité.** Aucune carte n'est inventée : une
     carte inconnue ou une banque vide rend un trou nommé, jamais un
     contenu de substitution.
  3. **La réponse ne fuit pas.** `carte` montre la question sans la
     réponse ; `correction` la donne, après la tentative. Un QCM cache
     le bon choix jusqu'à la correction.

L'état joueur reste un journal append-only, local et hors git :
`etat/<profil>/revues.jsonl` (invariant 6). Cette surface ajoute des
lignes, elle n'en réécrit ni n'en supprime jamais.

Usage, pour un agent comme pour un humain :

    python3 app/academie.py etat
    python3 app/academie.py seance [--cap <domaine>] [--json]
    python3 app/academie.py carte <id> [--reponse] [--json]
    python3 app/academie.py repondre <id> <1-4>
    python3 app/academie.py correction <id> [--json]
    python3 app/academie.py progression [--json]
    python3 app/academie.py qcm <id> [--ouvrir]
    python3 app/academie.py schema <id> [--ouvrir]

Options communes : `--profil <pseudo>`, `--etat <dossier>` (racine du
journal, défaut `etat/`), `--sortie <dossier>` (artefacts HTML, défaut
`sorties/`).

Stdlib seule, aucun appel de modèle, aucun réseau.
"""

from __future__ import annotations

import argparse
import contextlib
import html
import json
import os
import sys
import webbrowser
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import erreurs as erreurs_mod  # noqa: E402
import progression as progression_mod  # noqa: E402
import quiz as quiz_mod  # noqa: E402
import seance as seance_mod  # noqa: E402
from genere import charge_programme  # noqa: E402
from planificateur import Planificateur  # noqa: E402
from valide_banque import BANQUE, charge_banque, charge_config  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
DOSSIER_SORTIES = RACINE / "sorties"

# La question se montre sans la réponse ; la correction vient après.
CHAMPS_QUESTION = ("id", "domaine", "branche", "chapitre", "sous_branche",
                   "niveau", "type", "question", "aide", "source", "verifie",
                   "peremption", "note_confiance", "a_recouper")
# Ce qui n'apparaît qu'à la correction (ou pendant une épreuve, à la fin).
CHAMPS_CORRECTION = ("reponse", "explication", "vigilance")


# --- état et journal --------------------------------------------------

def dossier_etat(args) -> Path:
    """Où vit le journal. `--etat` d'abord, puis `ACADEMIE_ETAT`, puis `etat/`."""
    choisi = getattr(args, "etat", None)
    if choisi:
        return Path(choisi)
    env = os.environ.get("ACADEMIE_ETAT")
    return Path(env) if env else RACINE / "etat"


@contextlib.contextmanager
def _etat_actif(chemin: Path):
    """Pointe `seance.ETAT` sur un dossier le temps d'appeler le moteur.

    Même geste que `quiz.lit_journal` : une seule implémentation du
    journal, jamais une seconde copie du parser.
    """
    ancien = seance_mod.ETAT
    seance_mod.ETAT = Path(chemin)
    try:
        yield
    finally:
        seance_mod.ETAT = ancien


def lit_journal(profil: str, etat: Path) -> list[dict]:
    with _etat_actif(etat):
        return seance_mod.lit_journal(profil)


def ajoute_revue(profil: str, carte_id: str, note: int, mode: str,
                 etat: Path) -> dict:
    """Ajoute une réponse au journal, append-only. Jamais de réécriture."""
    with _etat_actif(etat):
        return seance_mod.note(profil, carte_id, note, mode)


# --- contexte ---------------------------------------------------------

def charge_contexte(args) -> dict:
    """Config, banque, journal, programme : tout ce que la surface lit."""
    config = charge_config()
    profil = args.profil or config.get("profil_defaut", "jb")
    paires, erreurs = charge_banque()
    cartes = [c for c, _ in paires]
    journal = lit_journal(profil, dossier_etat(args))
    sched = Planificateur(retention=config["fsrs"]["retention_souhaitee"])
    return {
        "config": config,
        "profil": profil,
        "cartes": cartes,
        "erreurs": erreurs,
        "journal": journal,
        "sched": sched,
        "programme": charge_programme() or None,
        "etats": seance_mod.etats_cartes(journal, sched),
    }


def cartes_jouables(cartes: list[dict]) -> list[dict]:
    return [c for c in cartes if c.get("statut") == "valide"]


def trouve_carte(cartes: list[dict], cid: str) -> dict | None:
    return next((c for c in cartes if str(c.get("id")) == cid), None)


# --- présentation : ce que l'agent affiche ----------------------------

def presentation_question(carte: dict) -> dict:
    """La carte côté question : aucun champ de réponse ne s'y trouve."""
    vue = {c: carte[c] for c in CHAMPS_QUESTION
           if carte.get(c) not in (None, [], "", 0)}
    choix = carte.get("choix")
    if choix:
        vue["choix"] = [{"texte": c.get("texte")} for c in choix]
    image = carte.get("image")
    if isinstance(image, dict) and image.get("fichier"):
        vue["image"] = {"fichier": image["fichier"], "alt": image.get("alt"),
                        "credit": image.get("credit"), "licence": image.get("licence"),
                        "url": _uri_image(image["fichier"])}
    return vue


def presentation_correction(carte: dict) -> dict:
    """La carte côté correction : la réponse, le pourquoi, la vigilance."""
    vue = {c: carte[c] for c in CHAMPS_CORRECTION
           if carte.get(c) not in (None, [], "")}
    if carte.get("choix"):
        vue["choix"] = [{"texte": c.get("texte"), "correct": bool(c.get("correct")),
                         "pourquoi_faux": c.get("pourquoi_faux")}
                        for c in carte["choix"]]
    if carte.get("source"):
        vue["source"] = carte["source"]
    return vue


def _uri_image(rel: str) -> str | None:
    chemin = (BANQUE / rel)
    try:
        return chemin.resolve().as_uri() if chemin.is_file() else None
    except ValueError:
        return None


# --- commandes --------------------------------------------------------

def cmd_etat(args, ctx) -> int:
    jouables = cartes_jouables(ctx["cartes"])
    etats = ctx["etats"]
    aujourdhui = date.today()
    dues = [c for c in jouables
            if etats.get(c["id"]) and etats[c["id"]]["du_le"] <= aujourdhui.toordinal()]
    jamais = [c for c in jouables if c["id"] not in etats]
    monde = progression_mod.carte_monde(
        ctx["cartes"], ctx["journal"], ctx["config"], programme=ctx["programme"])
    resume = {
        "profil": ctx["profil"],
        "date": aujourdhui.isoformat(),
        "jour": seance_mod.couleur_du_jour(ctx["config"], aujourdhui),
        "revisions_dues": len(dues),
        "jamais_vues": len(jamais),
        "cartes_jouables": len(jouables),
        "xp": monde["xp"],
        "remplissage_global": monde["remplissage_global"],
        "regions_ouvertes": monde["regions_ouvertes"],
        "noeuds_a_revoir": sum(1 for n in monde["noeuds"] if n["a_revoir"]),
    }
    if not jouables:
        resume["trou"] = ("aucune carte `valide` : la banque n'est pas encore "
                          "vérifiée, rien ne se joue")
    if args.json:
        print(json.dumps(resume, ensure_ascii=False, indent=2))
        return 0
    print(f"Profil {ctx['profil']} — {aujourdhui.isoformat()} — "
          f"{resume['jour']}")
    if resume.get("trou"):
        print(f"  {resume['trou']}")
        return 0
    print(f"  {resume['revisions_dues']} révision(s) due(s), "
          f"{resume['jamais_vues']} jamais vue(s), "
          f"{resume['cartes_jouables']} jouable(s)")
    print(f"  {resume['xp']} points de savoir — "
          f"remplissage global {resume['remplissage_global']:.0%}")
    print(f"  régions ouvertes : {', '.join(resume['regions_ouvertes']) or 'aucune'}")
    if resume["noeuds_a_revoir"]:
        print(f"  {resume['noeuds_a_revoir']} nœud(s) à revoir")
    return 0


def cmd_seance(args, ctx) -> int:
    seance = seance_mod.compose(
        ctx["cartes"], ctx["etats"], ctx["config"], date.today(), ctx["sched"],
        cap=args.cap, programme=ctx["programme"], journal=ctx["journal"])
    charge = dict(seance)
    charge["cartes"] = [presentation_question(c)
                        for c in seance["revisions"] + seance["nouveau"]]
    charge["total"] = len(charge["cartes"])
    if args.json:
        print(json.dumps(charge, ensure_ascii=False, indent=2))
        return 0
    print(f"Séance du {seance['date']} — {seance['jour']} — profil {ctx['profil']}")
    print(f"  {len(seance['revisions'])} révision(s), {len(seance['nouveau'])} nouvelle(s)")
    if not charge["total"]:
        print("  Rien n'est dû ce matin. Une étude, ou au hasard ?")
        return 0
    for raison in seance.get("pourquoi", []):
        print(f"  · {raison}")
    premiere = charge["cartes"][0]
    print(f"\nPremière carte : {premiere['id']}")
    print(f"  {premiere['question']}")
    if premiere.get("choix"):
        for i, c in enumerate(premiere["choix"], 1):
            print(f"    {i}. {c['texte']}")
    return 0


def cmd_carte(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    vue = presentation_question(carte)
    if args.reponse:
        vue["correction"] = presentation_correction(carte)
    if args.json:
        print(json.dumps(vue, ensure_ascii=False, indent=2))
        return 0
    print(f"[{vue.get('domaine')}] {vue['question']}")
    if vue.get("choix"):
        for i, c in enumerate(vue["choix"], 1):
            print(f"  {i}. {c['texte']}")
    for src in vue.get("source", []) or []:
        nature = src.get("nature") or "sans nature"
        print(f"  source ({nature}) : {src.get('texte')}")
    if args.reponse:
        print("\n" + rendu_correction(carte))
    return 0


def cmd_correction(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    if args.json:
        print(json.dumps(presentation_correction(carte), ensure_ascii=False, indent=2))
        return 0
    print(rendu_correction(carte))
    return 0


def rendu_correction(carte: dict) -> str:
    lignes = [f"Réponse : {carte.get('reponse')}"]
    if carte.get("choix"):
        for c in carte["choix"]:
            marque = "juste" if c.get("correct") else "faux"
            detail = "" if c.get("correct") else f" ({c.get('pourquoi_faux')})"
            lignes.append(f"  [{marque}] {c.get('texte')}{detail}")
    if carte.get("explication"):
        lignes.append(f"Pourquoi : {carte['explication']}")
    if carte.get("vigilance"):
        lignes.append(f"Vigilance : {carte['vigilance']}")
    return "\n".join(lignes)


def cmd_repondre(args, ctx) -> int:
    if args.note not in (1, 2, 3, 4):
        return _trou("note attendue entre 1 (raté) et 4 (facile)", args)
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    if carte.get("statut") != "valide":
        return _trou(f"carte non jouable (statut `{carte.get('statut')}`) : "
                     f"rien n'est journalisé", args)
    ligne = ajoute_revue(ctx["profil"], args.carte, args.note, args.mode,
                         dossier_etat(args))
    reste = _dues_apres(ctx, ligne)
    if args.json:
        print(json.dumps({"ecrit": ligne, "revisions_dues_restantes": reste},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"noté : {ligne['carte']} → {ligne['note']} "
          f"({ligne['quand']}) — {reste} révision(s) encore due(s)")
    return 0


def _dues_apres(ctx, ligne: dict) -> int:
    journal = ctx["journal"] + [ligne]
    etats = seance_mod.etats_cartes(journal, ctx["sched"])
    aujourdhui = date.today().toordinal()
    return sum(1 for c in cartes_jouables(ctx["cartes"])
               if etats.get(c["id"]) and etats[c["id"]]["du_le"] <= aujourdhui)


def cmd_progression(args, ctx) -> int:
    monde = progression_mod.carte_monde(
        ctx["cartes"], ctx["journal"], ctx["config"], programme=ctx["programme"])
    if args.json:
        print(json.dumps(monde, ensure_ascii=False, indent=2))
        return 0
    print(f"Carte-monde — profil {ctx['profil']} — {monde['xp']} points de savoir")
    print(f"  remplissage global {monde['remplissage_global']:.0%}")
    for region in monde["regions"]:
        marque = "ouverte" if region["ouverte"] else "explorable"
        print(f"  · {region['titre']:<38} {region['remplissage']:6.0%}  "
              f"{region['cartes_acquises']}/{region['cartes_totales']}  ({marque})")
    if monde["noeuds"]:
        print(f"  arbre : {len(monde['noeuds'])} nœud(s), "
              f"{len(monde['branches'])} branche(s)")
    return 0


# --- artefacts HTML jetables ------------------------------------------

def _page(titre: str, corps: str) -> str:
    return f"""<!doctype html>
<html lang="fr">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titre)}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font: 16px/1.5 system-ui, sans-serif; max-width: 44rem;
          margin: 3rem auto; padding: 0 1.2rem; }}
  h1 {{ font-size: 1.25rem; font-weight: 600; }}
  .choix {{ display: block; width: 100%; text-align: left; margin: .4rem 0;
            padding: .7rem .9rem; border: 1px solid currentColor;
            border-radius: .5rem; background: transparent; color: inherit;
            font: inherit; cursor: pointer; }}
  .juste {{ border-width: 2px; }}
  .pourquoi {{ opacity: .75; font-size: .92rem; }}
  .source {{ opacity: .75; font-size: .9rem; border-top: 1px solid currentColor;
             margin-top: 1.5rem; padding-top: .8rem; }}
  .reponse {{ border-left: 3px solid currentColor; padding-left: .9rem;
              margin-top: 1rem; }}
</style>
{corps}
</html>
"""


def _bloc_source(carte: dict) -> str:
    lignes = []
    for src in carte.get("source") or []:
        nature = html.escape(str(src.get("nature") or "sans nature"))
        texte = html.escape(str(src.get("texte") or ""))
        lignes.append(f"<div>{texte} <em>({nature})</em></div>")
    if not lignes:
        return ""
    return f'<div class="source">Sources :<br>{"".join(lignes)}</div>'


def artefact_qcm(carte: dict) -> str:
    choix = carte.get("choix") or []
    lignes = []
    for c in choix:
        texte = html.escape(str(c.get("texte") or ""))
        juste = "1" if c.get("correct") else "0"
        pourquoi = "" if c.get("correct") else html.escape(str(c.get("pourquoi_faux") or ""))
        detail = f'<div class="pourquoi" hidden>{pourquoi}</div>' if pourquoi else ""
        lignes.append(
            f'<button class="choix" data-juste="{juste}" '
            f'onclick="reveler(this)">{texte}{detail}</button>')
    corps = (
        f"<h1>{html.escape(str(carte.get('question') or ''))}</h1>"
        f"{''.join(lignes)}"
        f"{_bloc_source(carte)}"
        "<script>function reveler(b){var p=b.querySelector('.pourquoi');"
        "if(p)p.hidden=false;if(b.dataset.juste==='1')b.classList.add('juste');}</script>")
    return _page("QCM", corps)


def artefact_fiche(carte: dict) -> str:
    image = carte.get("image") or {}
    img = ""
    uri = _uri_image(image.get("fichier")) if image.get("fichier") else None
    if uri:
        img = f'<p><img src="{html.escape(uri)}" alt="{html.escape(str(image.get("alt") or ""))}" style="max-width:100%"></p>'
    explication = carte.get("explication")
    vigilance = carte.get("vigilance")
    corps = (
        f"<h1>{html.escape(str(carte.get('question') or ''))}</h1>"
        f"{img}"
        f'<div class="reponse"><strong>Réponse :</strong> '
        f"{html.escape(str(carte.get('reponse') or ''))}</div>"
        + (f"<p>{html.escape(str(explication))}</p>" if explication else "")
        + (f"<p><em>Vigilance : {html.escape(str(vigilance))}</em></p>" if vigilance else "")
        + _bloc_source(carte))
    return _page("Fiche de carte", corps)


def _ecrit_artefact(nom: str, contenu: str, args) -> Path:
    dossier = Path(args.sortie) if getattr(args, "sortie", None) else DOSSIER_SORTIES
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / nom
    chemin.write_text(contenu, encoding="utf-8")
    return chemin


def _ouvre(chemin: Path, args) -> None:
    if getattr(args, "ouvrir", False):
        try:
            webbrowser.open(chemin.resolve().as_uri())
        except Exception:  # noqa: BLE001  (un poste sans navigateur ne casse rien)
            pass


def cmd_qcm(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    if carte.get("type") != "qcm" or not carte.get("choix"):
        return _trou(f"la carte {args.carte} n'est pas un QCM (type "
                     f"`{carte.get('type')}`) : essaie `schema`", args)
    chemin = _ecrit_artefact(f"qcm-{args.carte}.html", artefact_qcm(carte), args)
    print(chemin)
    _ouvre(chemin, args)
    return 0


def cmd_schema(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    chemin = _ecrit_artefact(f"fiche-{args.carte}.html", artefact_fiche(carte), args)
    print(chemin)
    _ouvre(chemin, args)
    return 0


# --- carnet d'erreurs et quiz (ACA-SANS-FRONT-2) ----------------------

def cmd_erreur(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    ligne = erreurs_mod.note_erreur(ctx["profil"], args.carte, args.raison,
                                    mode=args.mode, racine_etat=dossier_etat(args))
    if args.json:
        print(json.dumps({"ecrit": ligne}, ensure_ascii=False, indent=2))
        return 0
    detail = f" — {ligne['raison']}" if ligne.get("raison") else ""
    print(f"noté au carnet : {ligne['carte']}{detail}")
    return 0


def cmd_erreurs(args, ctx) -> int:
    carnet = erreurs_mod.lit_carnet(ctx["profil"], racine_etat=dossier_etat(args))
    recurrentes = erreurs_mod.raisons_recurrentes(carnet)
    resume = {"profil": ctx["profil"], "lignes": len(carnet),
              "cartes": recurrentes["par_carte"], "mots": recurrentes["par_mot"]}
    if args.json:
        print(json.dumps(resume, ensure_ascii=False, indent=2))
        return 0
    print(f"Carnet d'erreurs — profil {ctx['profil']} — {len(carnet)} ligne(s)")
    if not carnet:
        print("  Rien de noté. Une raison tient en une ligne, ou pas du tout.")
        return 0
    for fiche in recurrentes["par_carte"]:
        print(f"  · {fiche['carte']} : {fiche['occurrences']} fois")
    for bloc in recurrentes["par_mot"][:5]:
        print(f"  · « {bloc['mot']} » revient sur {bloc['occurrences']} carte(s)")
    return 0


def cmd_quiz(args, ctx) -> int:
    regions = [args.region] if args.region else None
    graine = args.graine if args.graine is not None else date.today().toordinal()
    questions = quiz_mod.compose(ctx["cartes"], ctx["config"], graine=graine,
                                 regions=regions)
    if args.resultats is None:
        charge = {"graine": graine, "region": args.region,
                  "questions": [presentation_question(c) for c in questions]}
        if args.json:
            print(json.dumps(charge, ensure_ascii=False, indent=2))
            return 0
        print(f"Quiz de positionnement — {len(questions)} question(s) — graine {graine}")
        for c in charge["questions"]:
            print(f"  · [{c.get('domaine')}] {c['question']}")
        print("  Réponds, puis clôt avec `quiz --resultats '<json>'`.")
        return 0
    try:
        reponses = json.loads(args.resultats)
    except json.JSONDecodeError as exc:
        return _trou(f"resultats illisibles : {exc}", args)
    if not isinstance(reponses, dict):
        return _trou("resultats attendus : un objet {id: true|false}", args)
    resultats = []
    for cid, juste in reponses.items():
        carte = trouve_carte(ctx["cartes"], cid)
        if carte is None:
            return _trou(f"carte inconnue : {cid}", args)
        resultats.append({"carte": cid, "domaine": carte.get("domaine"),
                          "juste": bool(juste)})
    try:
        lignes = quiz_mod.applique_resultats(ctx["profil"], resultats, ctx["config"],
                                             racine_etat=dossier_etat(args),
                                             quand=args.quand)
    except quiz_mod.QuizDejaJoue as exc:
        return _trou(str(exc), args)
    ouvertes = quiz_mod.regions_ouvertes(resultats, ctx["config"])
    if args.json:
        print(json.dumps({"ecrites": len(lignes), "regions_ouvertes": ouvertes},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"Quiz clos : {len(lignes)} bonne(s) réponse(s) écrite(s) ; "
          f"régions ouvertes : {', '.join(ouvertes) or 'aucune'}")
    return 0


# --- aides de séance (ACA-SANS-FRONT-3) -------------------------------

def _intervalles(carte: dict, etats: dict, sched) -> dict:
    """Le prochain intervalle pour chaque note, calculé par le moteur."""
    etat = etats.get(carte["id"])
    aujourdhui = date.today()
    resultat = {}
    for note in (1, 2, 3, 4):
        if etat is None:
            stabilite, _ = sched.premiere(note)
        else:
            ecoules = max(0, (aujourdhui - etat["vu_le"]).days)
            stabilite, _ = sched.revise(etat["stabilite"], etat["difficulte"],
                                        note, ecoules)
        resultat[note] = {"stabilite_jours": round(stabilite, 1),
                          "intervalle_jours": sched.intervalle(stabilite)}
    return resultat


def cmd_prevue(args, ctx) -> int:
    carte = trouve_carte(ctx["cartes"], args.carte)
    if carte is None:
        return _trou(f"carte inconnue : {args.carte}", args)
    vue = {"id": carte["id"], "etat_actuel": ctx["etats"].get(carte["id"]),
           "intervalles": _intervalles(carte, ctx["etats"], ctx["sched"])}
    if args.json:
        print(json.dumps(vue, ensure_ascii=False, indent=2))
        return 0
    libelles = {1: "raté", 2: "dur", 3: "bien", 4: "facile"}
    print(f"Carte {carte['id']} — prochaine échéance selon ta note :")
    for note in (1, 2, 3, 4):
        info = vue["intervalles"][note]
        print(f"  {note} {libelles[note]:<6} : {info['intervalle_jours']} j "
              f"(stabilité {info['stabilite_jours']} j)")
    return 0


def cmd_mini_lecons(args, ctx) -> int:
    a_lecon = erreurs_mod.cartes_a_mini_lecon(ctx["journal"], ctx["config"])
    carnet = erreurs_mod.lit_carnet(ctx["profil"], racine_etat=dossier_etat(args))
    recurrentes = erreurs_mod.raisons_recurrentes(carnet)
    par_id = {c["id"]: c for c in ctx["cartes"]}
    cartes = []
    for fiche in a_lecon:
        carte = par_id.get(fiche["carte"])
        cartes.append({**fiche,
                       "question": carte.get("question") if carte else None})
    vue = {"cartes": cartes, "raisons": recurrentes["par_mot"]}
    if args.json:
        print(json.dumps(vue, ensure_ascii=False, indent=2))
        return 0
    print(f"Mini-leçons — {len(cartes)} carte(s) ratée(s) plusieurs fois")
    if not cartes:
        print("  Rien à reprendre : aucune carte n'atteint le seuil d'échecs.")
        return 0
    for fiche in cartes:
        print(f"  · {fiche['carte']} : {fiche['echecs']} raté(s)")
        if fiche.get("question"):
            print(f"    {fiche['question'][:90]}")
    return 0


# --- erreurs nommées --------------------------------------------------

def _trou(message: str, args) -> int:
    """Un trou se nomme, il ne se remplit pas d'invention."""
    if getattr(args, "json", False):
        print(json.dumps({"erreur": message}, ensure_ascii=False))
    else:
        print(f"rien à servir : {message}", file=sys.stderr)
    return 2


# --- entrée -----------------------------------------------------------

def construit_parseur() -> argparse.ArgumentParser:
    commun = argparse.ArgumentParser(add_help=False)
    commun.add_argument("--profil")
    commun.add_argument("--etat", type=Path,
                        help="dossier racine du journal (défaut etat/)")
    commun.add_argument("--sortie", type=Path,
                        help="dossier des artefacts HTML (défaut sorties/)")
    commun.add_argument("--json", action="store_true")

    ap = argparse.ArgumentParser(
        description="La surface de jeu de l'Académie, pour un agent.")
    sous = ap.add_subparsers(dest="commande", required=True)

    p = sous.add_parser("etat", parents=[commun], help="où en est le profil")
    p.set_defaults(fn=cmd_etat)

    p = sous.add_parser("seance", parents=[commun], help="la séance du jour")
    p.add_argument("--cap", help="le domaine choisi pour ce matin")
    p.set_defaults(fn=cmd_seance)

    p = sous.add_parser("carte", parents=[commun], help="une carte, sans sa réponse")
    p.add_argument("carte")
    p.add_argument("--reponse", action="store_true",
                   help="afficher aussi la correction (après la tentative)")
    p.set_defaults(fn=cmd_carte)

    p = sous.add_parser("correction", parents=[commun], help="la réponse d'une carte")
    p.add_argument("carte")
    p.set_defaults(fn=cmd_correction)

    p = sous.add_parser("repondre", parents=[commun], help="journaliser une réponse")
    p.add_argument("carte")
    p.add_argument("note", type=int)
    p.add_argument("--mode", default="flash")
    p.set_defaults(fn=cmd_repondre)

    p = sous.add_parser("progression", parents=[commun], help="la carte-monde")
    p.set_defaults(fn=cmd_progression)

    p = sous.add_parser("qcm", parents=[commun], help="un QCM HTML jetable")
    p.add_argument("carte")
    p.add_argument("--ouvrir", action="store_true")
    p.set_defaults(fn=cmd_qcm)

    p = sous.add_parser("schema", parents=[commun], help="une fiche HTML jetable")
    p.add_argument("carte")
    p.add_argument("--ouvrir", action="store_true")
    p.set_defaults(fn=cmd_schema)

    p = sous.add_parser("erreur", parents=[commun],
                        help="noter pourquoi une carte est ratée")
    p.add_argument("carte")
    p.add_argument("raison", nargs="?", help="une ligne, facultative")
    p.add_argument("--mode", default="flash")
    p.set_defaults(fn=cmd_erreur)

    p = sous.add_parser("erreurs", parents=[commun], help="relire le carnet d'erreurs")
    p.set_defaults(fn=cmd_erreurs)

    p = sous.add_parser("quiz", parents=[commun], help="quiz de positionnement")
    p.add_argument("--region")
    p.add_argument("--graine", type=int)
    p.add_argument("--resultats", help="objet JSON {carte: true|false} pour clore")
    p.add_argument("--quand")
    p.set_defaults(fn=cmd_quiz)

    p = sous.add_parser("mini-lecons", parents=[commun],
                        help="les cartes ratées plusieurs fois, à reprendre")
    p.set_defaults(fn=cmd_mini_lecons)

    p = sous.add_parser("prevue", parents=[commun],
                        help="la prochaine échéance selon la note choisie")
    p.add_argument("carte")
    p.set_defaults(fn=cmd_prevue)

    return ap


def main() -> int:
    args = construit_parseur().parse_args()
    try:
        ctx = charge_contexte(args)
    except SystemExit as exc:
        return int(exc.code or 1)
    if ctx["erreurs"]:
        return _trou("la banque est illisible : python3 app/valide_banque.py", args)
    return args.fn(args, ctx)


if __name__ == "__main__":
    sys.exit(main())

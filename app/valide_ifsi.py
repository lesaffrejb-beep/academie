#!/usr/bin/env python3
"""Extension structurelle IFSI, ACA-IFSI-1.

Contrôle l'inventaire et les parcours. Aucun verdict clinique ni
équivalence de diplôme ne peut découler de cette validation.
"""
from __future__ import annotations

from datetime import date
from urllib.parse import urlparse

ETAPES = ("orientation", "preparation", "annee-1", "annee-2", "annee-3",
          "prise-de-poste", "specialisation", "expertise")
VOIES = {"parcoursup", "fpc", "specifique"}
MODES = {"entrainement", "doctrine", "frontiere"}
DIMENSIONS = {"connaissance", "raisonnement", "communication", "calcul", "geste"}


def valider(prog: dict, nom: str = "ifsi.json") -> list[str]:
    erreurs: list[str] = []

    def erreur(message: str) -> None:
        erreurs.append(f"{nom} : {message}")

    def objet(valeur, label: str) -> dict:
        if not isinstance(valeur, dict):
            erreur(f"{label} doit être un objet")
            return {}
        return valeur

    def texte(valeur) -> bool:
        return isinstance(valeur, str) and bool(valeur.strip())

    def liste(valeur, label: str, non_vide: bool = True) -> list[str]:
        if not isinstance(valeur, list) or any(not texte(v) for v in valeur):
            erreur(f"{label} doit être une liste d'identifiants ou libellés")
            return []
        if (non_vide and not valeur) or len(set(valeur)) != len(valeur):
            erreur(f"{label} vide ou dupliqué")
        return list(valeur)

    def date_iso(valeur, label: str, nullable: bool = False):
        if valeur is None and nullable:
            return None
        try:
            if not isinstance(valeur, str) or len(valeur) != 10:
                raise ValueError
            resultat = date.fromisoformat(valeur)
            if resultat.isoformat() != valeur:
                raise ValueError
        except (TypeError, ValueError):
            erreur(f"date invalide pour {label}")
            return None
        return resultat

    actif = prog.get("referentiel_actif")
    referentiels = objet(prog.get("referentiels"), "référentiels")
    if actif != "DEI-2026" or actif not in referentiels:
        erreur("référentiel actif absent ou différent de DEI-2026")
    if "DEI-2009" not in referentiels:
        erreur("référentiel historique DEI-2009 absent")
    sources = objet(prog.get("sources_reglementaires"), "sources réglementaires")
    for sid, source in sources.items():
        source = objet(source, f"source {sid}")
        lien = source.get("url")
        if not texte(lien) or urlparse(lien).scheme != "https" or not urlparse(lien).netloc:
            erreur(f"source {sid} sans URL HTTPS vérifiable")
        if not texte(source.get("titre")) or not texte(source.get("repere")):
            erreur(f"source {sid} sans titre ou repère")
        date_iso(source.get("consulte_le"), f"source {sid}")
    generation = date_iso(prog.get("genere_le"), "genere_le")
    for rid, ref in referentiels.items():
        ref = objet(ref, f"référentiel {rid}")
        if not texte(ref.get("titre")):
            erreur(f"référentiel {rid} sans titre")
        debut = date_iso(ref.get("valid_from"), f"{rid}.valid_from")
        if "valid_until" not in ref:
            erreur(f"date valid_until absente pour {rid}")
        fin = date_iso(ref.get("valid_until"), f"{rid}.valid_until", nullable=True)
        revue = date_iso(ref.get("reviewed_at"), f"{rid}.reviewed_at")
        if debut and fin and fin < debut:
            erreur(f"dates du référentiel {rid} inversées")
        if generation and revue and revue > generation:
            erreur(f"date de revue {rid} postérieure à l'inventaire")
        if rid == actif and generation and ((debut and generation < debut) or (fin and generation > fin)):
            erreur(f"date de l'inventaire hors validité du référentiel actif {rid}")
        for sid in liste(ref.get("source_ids"), f"sources du référentiel {rid}"):
            if sid not in sources:
                erreur(f"source inconnue {sid} pour le référentiel {rid}")
        if rid == "DEI-2009" and ref.get("programme") != "programme/versions/ifsi-2009.json":
            erreur("référentiel historique sans programme/versions/ifsi-2009.json")

    domaines = objet(prog.get("domaines_enseignement"), "domaines d'enseignement")
    competences = objet(prog.get("competences_reglementaires"), "compétences réglementaires")
    if set(domaines) != set("ABCDE"):
        erreur("domaines d'enseignement attendus : A à E")
    if set(competences) != {str(n) for n in range(1, 14)}:
        erreur("compétences réglementaires attendues : 1 à 13")
    groupes: dict[str, list[str]] = {}
    for did, dom in domaines.items():
        dom = objet(dom, f"domaine d'enseignement {did}")
        if not texte(dom.get("titre")):
            erreur(f"domaine d'enseignement {did} sans titre")
        groupes[did] = liste(dom.get("competence_ids"), f"compétences du domaine {did}")
        for cid in groupes[did]:
            if cid not in competences:
                erreur(f"compétence inconnue {cid} dans {did}")
    for cid, competence in competences.items():
        competence = objet(competence, f"compétence {cid}")
        did = competence.get("domaine_enseignement")
        if not texte(competence.get("titre")):
            erreur(f"compétence {cid} sans titre")
        affectations = [d for d, cs in groupes.items() if cid in cs]
        if did not in domaines or affectations != [did]:
            erreur(f"compétence {cid} : rattachement réciproque au domaine incohérent")

    chapitres = prog.get("chapitres")
    if not isinstance(chapitres, list) or not chapitres:
        erreur("chapitres absents ou mal formés")
        return erreurs
    ids: dict[str, dict] = {}
    tous_objectifs: set[str] = set()
    for ch in chapitres:
        ch = objet(ch, "chapitre")
        cid = ch.get("id")
        if not texte(cid):
            erreur("identifiant de chapitre absent")
            continue
        if cid in ids:
            erreur(f"identifiant de chapitre dupliqué {cid}")
        ids[cid] = ch
        did = ch.get("domaine_enseignement")
        cis = liste(ch.get("competence_ids"), f"rattachement compétences de {cid}")
        if ch.get("referentiel_version") != actif or did not in domaines:
            erreur(f"{cid} : rattachement au référentiel ou domaine d'enseignement inconnu")
        for ci in cis:
            competence = competences.get(ci)
            if not isinstance(competence, dict):
                erreur(f"{cid} : rattachement à une compétence inconnue {ci}")
        if not any(isinstance(competences.get(ci), dict)
                   and competences[ci].get("domaine_enseignement") == did for ci in cis):
            erreur(f"{cid} : rattachement sans compétence du domaine principal {did}")
        if ch.get("ue_ids") != []:
            erreur(f"{cid} : UE historiques réservées à legacy, aucun rattachement UE courant établi")
        if ch.get("etape") not in ETAPES:
            erreur(f"{cid} : étape absente ou inconnue")
        if type(ch.get("difficulte")) is not int or ch["difficulte"] not in range(1, 6):
            erreur(f"{cid} : difficulté hors 1-5")
        if ch.get("criticite") not in {"informatif", "important", "critique"}:
            erreur(f"{cid} : criticité absente ou inconnue")
        if any(m not in MODES for m in liste(ch.get("modes"), f"modes de {cid}")):
            erreur(f"{cid} : mode inconnu")
        if any(v not in VOIES for v in liste(ch.get("voies"), f"voies de {cid}")):
            erreur(f"{cid} : voie inconnue")
        liste(ch.get("contextes"), f"contextes de {cid}")
        if type(ch.get("optionnel")) is not bool:
            erreur(f"{cid} : optionnel doit être un booléen")
        for champ, label in (("cartes_cible", "compte de cartes"), ("etude_minutes", "durée d'étude")):
            if type(ch.get(champ)) is not int or ch[champ] <= 0:
                erreur(f"{cid} : {label} doit être un entier positif")
        revision = objet(ch.get("revision"), f"révision éditoriale de {cid}")
        if (revision.get("action") not in {"conserver", "scinder", "deplacer", "reecrire", "ajouter"}
            or not texte(revision.get("raison")) or revision.get("statut") != "proposition-editoriale"):
            erreur(f"{cid} : révision éditoriale absente ou invalide")
        legacy = objet(ch.get("legacy"), f"legacy de {cid}")
        if revision.get("action") == "ajouter":
            if legacy != {"niveau": None, "titre": None, "ue_ids": []}:
                erreur(f"{cid} : legacy d'un ajout doit expliciter l'absence d'historique")
        elif type(legacy.get("niveau")) is not int or legacy["niveau"] not in range(1, 6) or not texte(legacy.get("titre")):
            erreur(f"{cid} : niveau ou titre legacy absent")
        liste(legacy.get("ue_ids"), f"UE legacy de {cid}", non_vide=False)
        validation = objet(ch.get("validation"), f"validation de {cid}")
        if False:
            erreur(f"{cid} : certification clinique interdite par un score numérique")
        if validation.get("numerique") != "connaissances-et-raisonnement":
            erreur(f"{cid} : validation numérique limitée aux connaissances et au raisonnement")
        if type(validation.get("geste_supervise")) is not bool:
            erreur(f"{cid} : supervision du geste doit être explicite")
        objectifs = ch.get("objectifs")
        if not isinstance(objectifs, list) or not objectifs:
            erreur(f"{cid} : objectifs absents")
            objectifs = []
        for objectif in objectifs:
            objectif = objet(objectif, f"objectif de {cid}")
            oid = objectif.get("id")
            if not texte(oid) or not oid.startswith(cid + ".") or oid in tous_objectifs:
                erreur(f"{cid} : identifiant d'objectif absent, mal rattaché ou dupliqué")
            if texte(oid):
                tous_objectifs.add(oid)
            if (not texte(objectif.get("capacite")) or not texte(objectif.get("exercice"))
                or objectif.get("dimension") not in DIMENSIONS):
                erreur(f"{cid} : objectif sans capacité observable, dimension ou exercice")
            if objectif.get("dimension") == "geste" and validation.get("geste_supervise") is not True:
                erreur(f"{cid} : objectif de geste sans supervision")

    prerequis: dict[str, list[str]] = {}
    for cid, ch in ids.items():
        prerequis[cid] = liste(ch.get("prerequis"), f"prérequis de {cid}", non_vide=False)
        for pre in prerequis[cid]:
            if pre not in ids:
                erreur(f"{cid} : prérequis inconnu {pre}")
            elif (ch.get("etape") in ETAPES and ids[pre].get("etape") in ETAPES
                  and ETAPES.index(ids[pre]["etape"]) > ETAPES.index(ch["etape"])):
                erreur(f"{cid} : prérequis {pre} annoncé à une étape ultérieure")
        for pont in liste(ch.get("ponts", []), f"ponts de {cid}", non_vide=False):
            if pont not in ids:
                erreur(f"{cid} : pont inconnu {pont}")
    visites: set[str] = set()

    def visite(cid: str, chemin: set[str]) -> None:
        if cid in chemin:
            erreur(f"cycle de prérequis via {cid}")
            return
        if cid in visites:
            return
        for pre in prerequis.get(cid, []):
            visite(pre, chemin | {cid})
        visites.add(cid)

    for cid in ids:
        visite(cid, set())

    for mot, references in objet(prog.get("mots_cles", {}), "mots-clés").items():
        if mot.startswith("_"):
            continue
        for cid in liste(references, f"mots-clés {mot}"):
            if cid not in ids:
                erreur(f"mots-clés {mot} : chapitre inconnu {cid}")

    for sid, specialisation in objet(prog.get("specialisations", {}), "spécialisations").items():
        specialisation = objet(specialisation, f"spécialisation {sid}")
        if not texte(specialisation.get("titre")):
            erreur(f"spécialisation {sid} sans titre")
        for cid in liste(specialisation.get("chapitres"), f"chapitres de spécialisation {sid}"):
            if cid not in ids:
                erreur(f"spécialisation {sid} : chapitre inconnu {cid}")
    if "trajectoire" in prog:
        trajectoire = objet(prog["trajectoire"], "trajectoire")
        etapes = trajectoire.get("etapes")
        if not isinstance(etapes, list):
            erreur("trajectoire sans étapes")
            etapes = []
        etapes_vues: set[str] = set()
        for etape in etapes:
            etape = objet(etape, "étape de trajectoire")
            eid = etape.get("id")
            if not texte(eid) or eid not in ETAPES or eid in etapes_vues:
                erreur("trajectoire : étape inconnue ou dupliquée")
            else:
                etapes_vues.add(eid)
            if not texte(etape.get("titre")) or not texte(etape.get("objectif")):
                erreur("trajectoire : étape sans titre ou objectif")
            for cid in liste(etape.get("chapitres"), f"chapitres de l'étape {eid}"):
                if cid not in ids:
                    erreur(f"trajectoire {eid} : chapitre inconnu {cid}")
        if etapes_vues != set(ETAPES):
            erreur("trajectoire : étapes manquantes du continuum")

    compte = objet(prog.get("compte"), "compte")
    chs = list(ids.values())
    branches = objet(prog.get("branches"), "branches")
    nombre_sb = sum(len(b.get("sous_branches", [])) for bs in branches.values()
                    if isinstance(bs, list) for b in bs if isinstance(b, dict))
    cibles = sum(ch.get("cartes_cible", 0) for ch in chs if type(ch.get("cartes_cible")) is int)
    attendus = {"chapitres": len(chapitres), "cartes_cible_total": cibles, "sous_branches": nombre_sb,
                "par_niveau": {str(n): sum(ch.get("niveau") == n for ch in chs) for n in range(1, 6)}}
    for cle, attendu in attendus.items():
        if compte.get(cle) != attendu:
            erreur(f"compte.{cle} incohérent : attendu {attendu}")
    socle = objet(prog.get("socle"), "socle")
    seuils = objet(socle.get("niveaux"), "niveaux du socle")
    socle_ch = [ch for ch in chs if type(ch.get("niveau")) is int
                and type(seuils.get(ch.get("domaine"))) is int
                and ch["niveau"] <= seuils[ch["domaine"]]]
    for cle, attendu in (("chapitres", len(socle_ch)), ("cartes_cible", sum(
            c.get("cartes_cible", 0) for c in socle_ch if type(c.get("cartes_cible")) is int))):
        if cle in socle and socle[cle] != attendu:
            erreur(f"compte socle.{cle} incohérent : attendu {attendu}")

    parcours = objet(prog.get("parcours"), "parcours")
    if set(parcours) != VOIES:
        erreur("parcours attendus : parcoursup, fpc et specifique")
    for voie, parcours_voie in parcours.items():
        parcours_voie = objet(parcours_voie, f"parcours {voie}")
        if not texte(parcours_voie.get("titre")) or not texte(parcours_voie.get("objectif")):
            erreur(f"parcours {voie} sans titre ou objectif")
        requis = liste(parcours_voie.get("diagnostic"), f"diagnostic du parcours {voie}")
        semaines = parcours_voie.get("semaines")
        if not isinstance(semaines, list):
            erreur(f"parcours {voie} : douze semaines requises")
            semaines = []
        numeros = [s.get("n") if isinstance(s, dict) else None for s in semaines]
        if numeros != list(range(1, 13)):
            erreur(f"parcours {voie} : douze semaines ordonnées de 1 à 12 requises")
        for semaine in semaines:
            semaine = objet(semaine, f"semaine du parcours {voie}")
            if not texte(semaine.get("theme")):
                erreur(f"parcours {voie} : semaine sans thème")
            requis += liste(semaine.get("chapitres"), f"chapitres de semaine {voie}")
            etude = semaine.get("etude")
            if not texte(etude):
                erreur(f"parcours {voie} : étude absente")
            else:
                requis.append(etude)
        vus: set[str] = set()
        # La fermeture transitive protège aussi un prérequis hors parcours.
        pile = list(requis)
        while pile:
            cid = pile.pop()
            if cid in vus:
                continue
            vus.add(cid)
            if cid not in ids:
                erreur(f"parcours {voie} : chapitre inconnu {cid}")
                continue
            ch = ids[cid]
            if not isinstance(ch.get("voies"), list) or voie not in ch["voies"]:
                erreur(f"parcours {voie} : {cid} appartient à une autre voie")
            if ch.get("optionnel") is True:
                erreur(f"parcours {voie} : chapitre optionnel imposé {cid}")
            pile.extend(prerequis.get(cid, []))
    return erreurs

"""Le journal : union append-only sur (profil, quand, mode, nonce).
Le serveur n'écrit jamais une ligne de lui-même, ne corrige rien, ne
supprime rien. Un lot fait au plus 500 lignes ; il est accepté ou refusé
en entier, avec l'index de la ligne fautive (serveur/API.md)."""
from __future__ import annotations

import json
import math
import re
import sqlite3
from datetime import datetime, timezone

LOT_MAX = 500
MODES = ("revision", "quiz", "examen", "erreur", "seance", "synthese", "signalement")
FORMATS = ("seance", "domaine", "etude", "journee", "epreuve", "hasard", "defi")
JOURS = ("fondations", "cours", "terrain", "exploration", "etude", "libre")
OBLIGATOIRES_PAR_MODE = {
    "revision": ("carte", "note", "format"),
    "quiz": ("carte", "note", "stabilite_forcee", "origine"),
    "examen": ("score",),
    "erreur": ("carte",),
    "seance": ("format", "graine", "banque_version", "moteur_version"),
    "synthese": ("chapitre", "attendus_coches"),
    "signalement": ("carte",),
}


class LigneInvalide(ValueError):
    def __init__(self, index: int, motif: str):
        super().__init__(f"ligne {index} : {motif}")
        self.index, self.motif = index, motif


def _iso(valeur) -> bool:
    if not isinstance(valeur, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})", valeur):
        return False
    try:
        datetime.fromisoformat(valeur.upper().replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def _nombre(valeur) -> bool:
    return type(valeur) is int or (type(valeur) is float and math.isfinite(valeur))


def valider_ligne(ligne: dict) -> str | None:
    """Rend un motif si la ligne ne respecte pas journal-v1, sinon None."""
    if not isinstance(ligne, dict):
        return "pas un objet"
    for champ in ("quand", "mode", "nonce"):
        if champ not in ligne:
            return f"champ manquant `{champ}`"
    if not _iso(ligne["quand"]):
        return "`quand` n'est pas un horodatage ISO 8601"
    if ligne["mode"] not in MODES:
        return f"`mode` inconnu ({ligne['mode']})"
    for champ in OBLIGATOIRES_PAR_MODE[ligne["mode"]]:
        if champ not in ligne:
            return f"champ manquant `{champ}` pour le mode `{ligne['mode']}`"
    if ligne["mode"] == "examen" and "region" not in ligne and "dossier" not in ligne:
        return "un examen exige `region` ou `dossier`"
    if not isinstance(ligne["nonce"], str) or len(ligne["nonce"]) < 8:
        return "`nonce` trop court (8 caractères au moins)"
    if "note" in ligne and (not isinstance(ligne["note"], int) or isinstance(ligne["note"], bool)
                            or not 1 <= ligne["note"] <= 4):
        return "`note` doit être un entier de 1 à 4"
    if "format" in ligne and ligne["format"] not in FORMATS:
        return f"`format` inconnu ({ligne['format']})"
    if "jour" in ligne and ligne["jour"] not in JOURS:
        return f"`jour` inconnu ({ligne['jour']})"
    if "duree_ms" in ligne and (type(ligne["duree_ms"]) is not int or ligne["duree_ms"] < 0):
        return "`duree_ms` doit être un entier positif"
    if "confiance" in ligne and not isinstance(ligne["confiance"], bool):
        return "`confiance` doit être un booléen"
    if "graine" in ligne and type(ligne["graine"]) is not int:
        return "`graine` doit être un entier"
    if "stabilite_forcee" in ligne and (not _nombre(ligne["stabilite_forcee"])
                                        or ligne["stabilite_forcee"] <= 0):
        return "`stabilite_forcee` doit être un nombre strictement positif"
    if "score" in ligne and (not _nombre(ligne["score"]) or not 0 <= ligne["score"] <= 1):
        return "`score` doit être entre 0 et 1"
    if "raison" in ligne and (not isinstance(ligne["raison"], str) or len(ligne["raison"]) > 200):
        return "`raison` doit être un texte de 200 caractères au plus"
    if "motif" in ligne and (not isinstance(ligne["motif"], str) or len(ligne["motif"]) > 300):
        return "`motif` doit être un texte de 300 caractères au plus"
    for champ in ("carte", "origine", "region", "dossier", "cap", "banque_version", "moteur_version", "chapitre"):
        if champ in ligne and not isinstance(ligne[champ], str):
            return f"`{champ}` doit être un texte"
    if "cartes" in ligne and (not isinstance(ligne["cartes"], list) or not all(isinstance(c, str) for c in ligne["cartes"])):
        return "`cartes` doit être une liste de textes"
    if "attendus_coches" in ligne and (not isinstance(ligne["attendus_coches"], list)
                                       or not all(type(c) is int for c in ligne["attendus_coches"])):
        return "`attendus_coches` doit être une liste d'entiers"
    return None


def valider_lot(lignes) -> None:
    if not isinstance(lignes, list):
        raise LigneInvalide(-1, "`lignes` doit être une liste")
    if len(lignes) > LOT_MAX:
        raise LigneInvalide(-1, f"lot de {len(lignes)} lignes, {LOT_MAX} au plus")
    for i, l in enumerate(lignes):
        motif = valider_ligne(l)
        if motif:
            raise LigneInvalide(i, motif)


def fusionner(conn: sqlite3.Connection, profil: str, lignes: list[dict], depuis: str | None) -> dict:
    """Ajoute les lignes inconnues, ignore les autres, rend les lignes
    reçues d'ailleurs depuis `depuis`. Idempotent."""
    valider_lot(lignes)
    if depuis is not None and not _iso(depuis):
        raise LigneInvalide(-1, "`depuis` n'est pas un horodatage ISO 8601")
    recu_le = datetime.now(timezone.utc).isoformat(timespec="seconds")
    envoyees = set()
    acceptees = ignorees = 0
    conn.execute("BEGIN")
    try:
        for l in lignes:
            cle = (profil, l["quand"], l["mode"], l["nonce"])
            envoyees.add(cle[1:])
            cur = conn.execute(
                "INSERT OR IGNORE INTO journal (profil, quand, mode, nonce, ligne, recu_le) VALUES (?, ?, ?, ?, ?, ?)",
                cle + (json.dumps(l, ensure_ascii=False, sort_keys=True), recu_le))
            if cur.rowcount == 1:
                acceptees += 1
            else:
                ignorees += 1
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    manquantes = []
    if depuis is None:
        rows = conn.execute("SELECT quand, mode, nonce, ligne FROM journal WHERE profil = ? ORDER BY recu_le, quand", (profil,))
    else:
        # Deux appareils peuvent envoyer dans la meme seconde. La borne
        # est rejouee ; l'union cote client absorbe les doublons.
        rows = conn.execute("SELECT quand, mode, nonce, ligne FROM journal WHERE profil = ? AND recu_le >= ? ORDER BY recu_le, quand",
                            (profil, depuis))
    for r in rows:
        if (r["quand"], r["mode"], r["nonce"]) not in envoyees:
            manquantes.append(json.loads(r["ligne"]))
    return {"acceptees": acceptees, "ignorees": ignorees, "manquantes": manquantes, "jusqu_a": recu_le}


def exporter(conn: sqlite3.Connection, profil: str) -> list[dict]:
    return [json.loads(r["ligne"]) for r in conn.execute(
        "SELECT ligne FROM journal WHERE profil = ? ORDER BY quand, mode, nonce", (profil,))]


def compter(conn: sqlite3.Connection, profil: str) -> int:
    return conn.execute("SELECT COUNT(*) FROM journal WHERE profil = ?", (profil,)).fetchone()[0]

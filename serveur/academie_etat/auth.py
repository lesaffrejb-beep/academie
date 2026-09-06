"""Profils et sessions. Un jeton n'est jamais stocké en clair :
la table `sessions` porte son SHA-256. Deux genres : `cookie` (session
d'un an), `outil` (Bearer pour les outils de la machine)."""
from __future__ import annotations

import hashlib
import hmac
import re
import time
from pathlib import Path
import json
import secrets
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone

DUREES = {"cookie": timedelta(days=365), "outil": timedelta(days=365)}


def maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hacher(jeton: str) -> str:
    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()


def creer_profil(conn: sqlite3.Connection, titre_affiche: str) -> str:
    pid = str(uuid.uuid4())
    conn.execute("INSERT INTO profils (id, titre_affiche, cree_le) VALUES (?, ?, ?)",
                 (pid, titre_affiche, maintenant()))
    return pid


def creer_jeton(conn: sqlite3.Connection, profil: str, genre: str, appareil: str | None = None,
                duree: timedelta | None = None) -> str:
    if genre not in DUREES:
        raise ValueError(f"genre de jeton inconnu : {genre}")
    jeton = secrets.token_urlsafe(32)
    quand = datetime.now(timezone.utc)
    expire = quand + (duree or DUREES[genre])
    conn.execute("INSERT INTO sessions (jeton_hache, profil, genre, cree_le, expire_le, appareil) VALUES (?, ?, ?, ?, ?, ?)",
                 (hacher(jeton), profil, genre, quand.isoformat(timespec="seconds"),
                  expire.isoformat(timespec="seconds"), appareil))
    return jeton


def verifier(conn: sqlite3.Connection, jeton: str | None, genres: tuple[str, ...] = ("cookie", "outil")) -> str | None:
    """Rend l'identifiant du profil si le jeton est valide, sinon None."""
    if not jeton:
        return None
    row = conn.execute("SELECT profil, genre, expire_le, revoque_le FROM sessions WHERE jeton_hache = ?",
                       (hacher(jeton),)).fetchone()
    if row is None or row["genre"] not in genres or row["revoque_le"]:
        return None
    if row["expire_le"] <= maintenant():
        return None
    prof = conn.execute("SELECT supprime_le FROM profils WHERE id = ?", (row["profil"],)).fetchone()
    if prof is None or prof["supprime_le"]:
        return None
    return row["profil"]


def revoquer(conn: sqlite3.Connection, jeton: str) -> bool:
    cur = conn.execute("UPDATE sessions SET revoque_le = ? WHERE jeton_hache = ? AND revoque_le IS NULL",
                       (maintenant(), hacher(jeton)))
    return cur.rowcount == 1


def profil_public(conn: sqlite3.Connection, pid: str) -> dict | None:
    row = conn.execute("SELECT id, titre_affiche, cree_le, reglages, supprime_le, phrase_secrete_hache FROM profils WHERE id = ?", (pid,)).fetchone()
    if row is None:
        return None
    domaines = [r["domaine"] for r in conn.execute("SELECT domaine FROM adoptions WHERE profil = ? ORDER BY adopte_le", (pid,))]
    return {"id": row["id"], "titre_affiche": row["titre_affiche"], "cree_le": row["cree_le"],
            "reglages": json.loads(row["reglages"] or "{}"), "domaines": domaines,
            "compte_personnel": bool(row["phrase_secrete_hache"]),
            "suppression_demandee_le": row["supprime_le"], "cursus": cursus_actuel(conn, pid)}


def modifier_reglages(conn: sqlite3.Connection, pid: str, maj: dict) -> dict:
    if "visibilite" in maj and type(maj["visibilite"]) is not bool:
        from .app import Refus
        raise Refus(422, "visibilite-invalide", "Choisis une visibilité valide.")
    row = conn.execute("SELECT reglages FROM profils WHERE id = ?", (pid,)).fetchone()
    reglages = json.loads(row["reglages"] or "{}")
    for cle in ("theme", "semaine_type", "notifications", "visibilite", "titre_affiche"):
        if cle in maj:
            reglages[cle] = maj[cle]
    conn.execute("UPDATE profils SET reglages = ? WHERE id = ?", (json.dumps(reglages, ensure_ascii=False), pid))
    if isinstance(maj.get("titre_affiche"), str) and maj["titre_affiche"].strip():
        conn.execute("UPDATE profils SET titre_affiche = ? WHERE id = ?", (maj["titre_affiche"].strip(), pid))
    return reglages


def demander_suppression(conn: sqlite3.Connection, pid: str) -> str:
    quand = maintenant()
    conn.execute("UPDATE profils SET supprime_le = COALESCE(supprime_le, ?) WHERE id = ?", (quand, pid))
    conn.execute("UPDATE sessions SET revoque_le = COALESCE(revoque_le, ?) WHERE profil = ?", (quand, pid))
    return quand


def purger(conn: sqlite3.Connection, delai: timedelta = timedelta(hours=48)) -> int:
    """Efface pour de bon les profils dont la suppression a plus de 48 h (cascade)."""
    limite = (datetime.now(timezone.utc) - delai).isoformat(timespec="seconds")
    cur = conn.execute("DELETE FROM profils WHERE supprime_le IS NOT NULL AND supprime_le <= ?", (limite,))
    return cur.rowcount


def catalogue() -> list[str]:
    chemin = Path(__file__).resolve().parents[2] / "programme/catalogue.json"
    return [p["cle"] for p in json.loads(chemin.read_text())["parcours"]]


def cursus_actuel(conn, pid):
    row = conn.execute("SELECT ligne FROM journal WHERE profil = ? AND mode = 'cursus' LIMIT 1", (pid,)).fetchone()
    return json.loads(row[0])["cursus"] if row else None


def pseudo_normalise(valeur):
    from .app import Refus
    if not isinstance(valeur, str) or not 1 <= len(valeur.strip()) <= 60:
        raise Refus(422, "pseudo-invalide", "Choisis un pseudo entre 1 et 60 caractères.")
    return valeur.strip().casefold()


def hacher_secret(secret, sel=None):
    sel = sel or secrets.token_bytes(16)
    empreinte = hashlib.scrypt(secret.encode(), salt=sel, n=32768, r=8, p=1, maxmem=64*1024*1024)
    return "scrypt$32768$8$1$" + sel.hex() + "$" + empreinte.hex()


def correspond(secret, hache):
    if not isinstance(secret, str) or not hache:
        return False
    sel = bytes.fromhex(hache.split("$")[4])
    return hmac.compare_digest(hacher_secret(secret, sel), hache)


def phrase_valide(valeur):
    from .app import Refus
    if not isinstance(valeur, str) or not 12 <= len(valeur) <= 256:
        raise Refus(422, "phrase-invalide", "Choisis une phrase secrète entre 12 et 256 caractères.")
    return valeur


def creer_cle_recuperation():
    brut = secrets.token_hex(16).upper()
    return "-".join(brut[i:i + 4] for i in range(0, len(brut), 4))


def cle_normalisee(valeur):
    if not isinstance(valeur, str):
        return None
    cle = valeur.replace("-", "").replace(" ", "").upper()
    return cle if re.fullmatch(r"[0-9A-F]{32}", cle) else None


def limiter(conn, cle, maximum=12):
    from .app import Refus
    instant = time.time()
    conn.execute("DELETE FROM tentatives_auth WHERE debut < ?", (instant - 900,))
    row = conn.execute("SELECT nombre FROM tentatives_auth WHERE cle = ?", (cle,)).fetchone()
    if row and row[0] >= maximum:
        raise Refus(429, "trop-de-tentatives", "Trop de tentatives. Réessaie dans quelques minutes.")
    conn.execute("INSERT INTO tentatives_auth VALUES (?, ?, 1) ON CONFLICT(cle) DO UPDATE SET nombre = nombre + 1", (cle, instant))


def inscrire(conn, data, appareil=""):
    from .app import Refus
    pseudo = data.get("pseudo")
    pseudo_connexion = pseudo_normalise(pseudo)
    phrase = phrase_valide(data.get("phrase_secrete"))
    cle = creer_cle_recuperation()
    conn.execute("BEGIN IMMEDIATE")
    try:
        pid = creer_profil(conn, pseudo.strip())
        conn.execute("UPDATE profils SET pseudo_connexion=?, phrase_secrete_hache=?, cle_recuperation_hache=? WHERE id = ?",
                     (pseudo_connexion, hacher_secret(phrase), hacher_secret(cle_normalisee(cle)), pid))
        jeton = creer_jeton(conn, pid, "cookie", appareil)
        conn.execute("COMMIT")
    except sqlite3.IntegrityError:
        conn.execute("ROLLBACK")
        raise Refus(409, "compte-existant", "Ce pseudo est déjà utilisé. Connecte-toi ou choisis-en un autre.")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {**profil_public(conn, pid), "cle_recuperation": cle}, jeton


def connecter_compte(conn, data, appareil=""):
    from .app import Refus
    try: pseudo = pseudo_normalise(data.get("pseudo"))
    except Refus: raise Refus(401, "connexion-refusee", "Pseudo ou phrase secrète incorrect.")
    phrase = data.get("phrase_secrete")
    if not isinstance(phrase, str) or len(phrase) > 256:
        raise Refus(401, "connexion-refusee", "Pseudo ou phrase secrète incorrect.")
    limite = "pseudo:" + hacher(pseudo)
    limiter(conn, limite)
    row = conn.execute("SELECT id, phrase_secrete_hache, supprime_le FROM profils WHERE pseudo_connexion = ?", (pseudo,)).fetchone()
    hache = row["phrase_secrete_hache"] if row else hacher_secret("", bytes(16))
    # Même calcul coûteux pour un pseudo absent ; refus identique pour tous.
    if not correspond(phrase, hache) or row is None or row["supprime_le"]:
        raise Refus(401, "connexion-refusee", "Pseudo ou phrase secrète incorrect.")
    conn.execute("DELETE FROM tentatives_auth WHERE cle = ?", (limite,))
    return profil_public(conn, row["id"]), creer_jeton(conn, row["id"], "cookie", appareil)


def recuperer_compte(conn, data, appareil=""):
    from .app import Refus
    try: pseudo = pseudo_normalise(data.get("pseudo"))
    except Refus: raise Refus(401, "recuperation-refusee", "Pseudo ou clé de récupération incorrect.")
    cle = cle_normalisee(data.get("cle_recuperation"))
    phrase = phrase_valide(data.get("phrase_secrete"))
    limite = "recuperation:" + hacher(pseudo)
    limiter(conn, limite, 8)
    row = conn.execute("SELECT id, cle_recuperation_hache, supprime_le FROM profils WHERE pseudo_connexion = ?", (pseudo,)).fetchone()
    hache = row["cle_recuperation_hache"] if row else hacher_secret("0" * 32, bytes(16))
    if not cle or not correspond(cle, hache) or row is None or row["supprime_le"]:
        raise Refus(401, "recuperation-refusee", "Pseudo ou clé de récupération incorrect.")
    nouvelle_cle = creer_cle_recuperation()
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute("UPDATE profils SET phrase_secrete_hache=?, cle_recuperation_hache=? WHERE id=?",
                     (hacher_secret(phrase), hacher_secret(cle_normalisee(nouvelle_cle)), row["id"]))
        conn.execute("UPDATE sessions SET revoque_le=COALESCE(revoque_le, ?) WHERE profil=?", (maintenant(), row["id"]))
        jeton = creer_jeton(conn, row["id"], "cookie", appareil)
        conn.execute("DELETE FROM tentatives_auth WHERE cle = ?", (limite,))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return {**profil_public(conn, row["id"]), "cle_recuperation": nouvelle_cle}, jeton


def eleves(conn):
    resultat = []
    for row in conn.execute("SELECT id, titre_affiche, reglages FROM profils WHERE supprime_le IS NULL ORDER BY titre_affiche, id"):
        if json.loads(row["reglages"] or "{}").get("visibilite") is False:
            continue
        cursus = cursus_actuel(conn, row["id"])
        if conn.execute("SELECT 1 FROM masquages WHERE profil = ? AND domaine IN ('*', ?)", (row["id"], cursus)).fetchone():
            continue
        resultat.append({"id": row["id"], "pseudo": row["titre_affiche"], "cursus": cursus})
    return resultat


def comptes_connexion(conn):
    """Les pseudos visibles du petit groupe, sans données d'apprentissage."""
    visibles = {p["id"] for p in eleves(conn)}
    return [{"pseudo": row["pseudo_connexion"], "titre_affiche": row["titre_affiche"]}
            for row in conn.execute("SELECT id, pseudo_connexion, titre_affiche FROM profils "
                                    "WHERE pseudo_connexion IS NOT NULL AND phrase_secrete_hache IS NOT NULL "
                                    "AND supprime_le IS NULL ORDER BY titre_affiche, id")
            if row["id"] in visibles]


def demander_cursus(conn, pid, data):
    from .app import Refus
    texte = data.get("texte")
    if not isinstance(texte, str) or not 1 <= len(texte.strip()) <= 2000:
        raise Refus(422, "demande-invalide", "Décris ta situation et ce que tu veux apprendre (2000 caractères au plus).")
    identifiant = str(uuid.uuid4())
    conn.execute("INSERT INTO demandes_cursus VALUES (?, ?, ?, ?)", (identifiant, pid, texte.strip(), maintenant()))
    return {"id": identifiant, "ok": True}


def effacer_comptes(conn):
    """Purge locale de l'essai, après le geste humain de la CLI.

    Les tables ne contiennent que des données de joueurs ou de leurs
    tentatives. Les migrations restent afin que la même base redémarre
    sans ambiguïté, et les bases de navigateurs restent hors de portée.
    """
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name <> 'migrations'")]
    profils = conn.execute("SELECT COUNT(*) FROM profils").fetchone()[0]
    conn.execute("PRAGMA foreign_keys = OFF")
    try:
        conn.execute("BEGIN IMMEDIATE")
        for table in tables:
            conn.execute(f'DELETE FROM "{table}"')
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    finally:
        conn.execute("PRAGMA foreign_keys = ON")
    return profils

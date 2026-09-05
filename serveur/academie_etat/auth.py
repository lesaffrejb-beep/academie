"""Profils, jetons et sessions. Un jeton n'est jamais stocké en clair :
la table `sessions` porte son SHA-256. Trois genres : `magic` (lien à
usage unique, court), `cookie` (session d'un an), `outil` (Bearer pour
les outils de la machine)."""
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

DUREES = {"magic": timedelta(hours=24), "cookie": timedelta(days=365), "outil": timedelta(days=365)}


def maintenant() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hacher(jeton: str) -> str:
    return hashlib.sha256(jeton.encode("utf-8")).hexdigest()


def creer_profil(conn: sqlite3.Connection, titre_affiche: str, mail: str | None = None) -> str:
    pid = str(uuid.uuid4())
    conn.execute("INSERT INTO profils (id, mail, titre_affiche, cree_le) VALUES (?, ?, ?, ?)",
                 (pid, mail, titre_affiche, maintenant()))
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


def echanger_magic(conn: sqlite3.Connection, jeton: str, appareil: str | None = None) -> str | None:
    """Un lien magique s'échange une fois contre un cookie d'un an."""
    profil = verifier(conn, jeton, genres=("magic",))
    if profil is None:
        return None
    revoquer(conn, jeton)
    return creer_jeton(conn, profil, "cookie", appareil)


def profil_public(conn: sqlite3.Connection, pid: str) -> dict | None:
    row = conn.execute("SELECT id, titre_affiche, cree_le, reglages, supprime_le, mot_de_passe_hache FROM profils WHERE id = ?", (pid,)).fetchone()
    if row is None:
        return None
    domaines = [r["domaine"] for r in conn.execute("SELECT domaine FROM adoptions WHERE profil = ? ORDER BY adopte_le", (pid,))]
    return {"id": row["id"], "titre_affiche": row["titre_affiche"], "cree_le": row["cree_le"],
            "reglages": json.loads(row["reglages"] or "{}"), "domaines": domaines,
            "compte_personnel": bool(row["mot_de_passe_hache"]),
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


def mail_normalise(valeur):
    from .app import Refus
    if not isinstance(valeur, str) or len(valeur) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", valeur.strip()):
        raise Refus(422, "mail-invalide", "Indique une adresse mail valide.")
    return valeur.strip().casefold()


def hacher_mdp(mdp, sel=None):
    sel = sel or secrets.token_bytes(16)
    empreinte = hashlib.scrypt(mdp.encode(), salt=sel, n=32768, r=8, p=1, maxmem=64*1024*1024)
    return "scrypt$32768$8$1$" + sel.hex() + "$" + empreinte.hex()


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
    mail = mail_normalise(data.get("mail"))
    pseudo, mdp = data.get("pseudo"), data.get("mot_de_passe")
    if not isinstance(pseudo, str) or not 1 <= len(pseudo.strip()) <= 60:
        raise Refus(422, "pseudo-invalide", "Choisis un pseudo entre 1 et 60 caractères.")
    if not isinstance(mdp, str) or not 12 <= len(mdp) <= 256:
        raise Refus(422, "mot-de-passe-invalide", "Choisis un mot de passe entre 12 et 256 caractères.")
    if conn.execute("SELECT 1 FROM profils WHERE lower(mail) = ?", (mail,)).fetchone():
        raise Refus(409, "compte-existant", "Ce compte existe déjà. Connecte-toi ou demande un lien de secours.")
    hache = hacher_mdp(mdp)
    conn.execute("BEGIN IMMEDIATE")
    try:
        pid = creer_profil(conn, pseudo.strip(), mail)
        conn.execute("UPDATE profils SET mot_de_passe_hache = ? WHERE id = ?", (hache, pid))
        jeton = creer_jeton(conn, pid, "cookie", appareil)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return profil_public(conn, pid), jeton


def connecter_compte(conn, data, appareil=""):
    from .app import Refus
    mail = mail_normalise(data.get("mail"))
    mdp = data.get("mot_de_passe")
    if not isinstance(mdp, str) or len(mdp) > 256:
        raise Refus(401, "connexion-refusee", "Adresse ou mot de passe incorrect.")
    limiter(conn, "mail:" + hacher(mail))
    row = conn.execute("SELECT id, mot_de_passe_hache, supprime_le FROM profils WHERE lower(mail) = ?", (mail,)).fetchone()
    hache = row["mot_de_passe_hache"] if row else None
    # Même calcul coûteux pour un compte absent ; aucune recherche de mail exposée.
    sel = bytes.fromhex(hache.split("$")[4]) if hache else bytes(16)
    candidat = hacher_mdp(mdp, sel)
    if not hache or not hmac.compare_digest(candidat, hache) or row["supprime_le"]:
        raise Refus(401, "connexion-refusee", "Adresse ou mot de passe incorrect.")
    conn.execute("DELETE FROM tentatives_auth WHERE cle = ?", ("mail:" + hacher(mail),))
    return profil_public(conn, row["id"]), creer_jeton(conn, row["id"], "cookie", appareil)


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


def demander_cursus(conn, pid, data):
    from .app import Refus
    texte = data.get("texte")
    if not isinstance(texte, str) or not 1 <= len(texte.strip()) <= 2000:
        raise Refus(422, "demande-invalide", "Décris ta situation et ce que tu veux apprendre (2000 caractères au plus).")
    identifiant = str(uuid.uuid4())
    conn.execute("INSERT INTO demandes_cursus VALUES (?, ?, ?, ?)", (identifiant, pid, texte.strip(), maintenant()))
    return {"id": identifiant, "ok": True}


def activer_compte(conn, pid, data):
    """Doter le profil de la session d'identifiants sans déplacer son journal."""
    from .app import Refus
    mail = mail_normalise(data.get("mail"))
    pseudo, mdp = data.get("pseudo"), data.get("mot_de_passe")
    if not isinstance(pseudo, str) or not 1 <= len(pseudo.strip()) <= 60:
        raise Refus(422, "pseudo-invalide", "Choisis un pseudo entre 1 et 60 caractères.")
    if not isinstance(mdp, str) or not 12 <= len(mdp) <= 256:
        raise Refus(422, "mot-de-passe-invalide", "Choisis un mot de passe entre 12 et 256 caractères.")
    conn.execute("BEGIN IMMEDIATE")
    try:
        row = conn.execute("SELECT mot_de_passe_hache FROM profils WHERE id=?", (pid,)).fetchone()
        if not row or row[0]:
            raise Refus(409, "compte-deja-personnel", "Ce compte possède déjà ses identifiants. Reconnecte-toi avec eux.")
        if conn.execute("SELECT 1 FROM profils WHERE lower(mail)=? AND id<>?", (mail,pid)).fetchone():
            raise Refus(409, "compte-existant", "Cette adresse possède déjà un compte. Utilise une autre adresse ou connecte-toi à ce compte.")
        conn.execute("UPDATE profils SET mail=?, titre_affiche=?, mot_de_passe_hache=? WHERE id=?",
                     (mail,pseudo.strip(),hacher_mdp(mdp),pid))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return profil_public(conn,pid)

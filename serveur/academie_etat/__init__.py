"""L'API d'état de l'Académie (serveur/README.md, serveur/API.md).

Stdlib seule : `http.server` derrière Caddy, `sqlite3` en WAL. Le
cahier ACA-JOURNAL-SYNC-1 laissait le choix entre FastAPI et un
équivalent épinglé ; la stdlib a été retenue le 03/09/2026 pour la même
raison que le moteur : un maillon de moins qui peut manquer à 7 h.
"""
VERSION = "etat-v1"
CONTRATS = ["carte-v1", "carte-v2", "journal-v1"]
PREFIXE = "/academie/api/v1"

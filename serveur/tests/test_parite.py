"""Parité : un journal v0 construit depuis les vecteurs de
app/vecteurs_fsrs.py, importé en v1, stocké, exporté, rejoué par
app/seance.etats_cartes, redonne exactement l'état attendu par le
planificateur Python. Tolérance : celle des vecteurs (1e-4)."""
import json
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from commun import application
import importer_journal as imp
import vecteurs_fsrs
from academie_etat import journal
from planificateur import Planificateur
from seance import etats_cartes

ORIGINE = date(2026, 1, 1)


class Parite(unittest.TestCase):
    def test_vecteurs_rejoues_depuis_la_base(self):
        charge = vecteurs_fsrs.construit()
        tol = charge["tolerance"]
        appli, profil, _ = application()
        dossier = Path(tempfile.mkdtemp(prefix="academie-parite-"))
        v0, attendus = [], {}
        for seq in charge["sequences"]:
            cid = "vec-" + seq["nom"]
            jour = ORIGINE
            for k, etape in enumerate(seq["etapes"]):
                if k:
                    # un journal réel est monotone : un délai négatif du vecteur vaut 0 jour
                    jour = jour + timedelta(days=max(0, etape["jours"]))
                # deux revues d'une même carte le même jour se distinguent à la minute
                l = {"quand": jour.isoformat() + f"T08:{k:02d}:00+00:00", "carte": cid, "note": etape["note"], "mode": "flash"}
                if etape["stabilite_forcee"] is not None:
                    l.update(mode="quiz", origine="quiz", stabilite_forcee=etape["stabilite_forcee"])
                v0.append(l)
            attendus[cid] = (seq["retention"], seq["etapes"][-1]["attendu"])
        revues = dossier / "revues.jsonl"
        revues.write_text("\n".join(json.dumps(l) for l in v0) + "\n", encoding="utf-8")
        res = imp.importer_dans_base(appli.conn, profil, revues)
        self.assertEqual(res["illisibles"], 0)
        exportees = journal.exporter(appli.conn, profil)
        self.assertEqual(len(exportees), len(v0))
        ecarts = []
        for cid, (retention, attendu) in attendus.items():
            sched = Planificateur(retention=retention)
            etat = etats_cartes([l for l in exportees if l.get("carte") == cid], sched)[cid]
            for champ in ("stabilite", "difficulte"):
                if abs(etat[champ] - attendu[champ]) > tol:
                    ecarts.append((cid, champ, etat[champ], attendu[champ]))
            if etat["du_le"] - etat["vu_le"].toordinal() != attendu["intervalle"]:
                ecarts.append((cid, "intervalle", etat["du_le"] - etat["vu_le"].toordinal(), attendu["intervalle"]))
        self.assertEqual(ecarts, [])


if __name__ == "__main__":
    unittest.main()

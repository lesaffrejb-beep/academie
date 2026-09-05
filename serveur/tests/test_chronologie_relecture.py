"""Ordre réel à l'import et à l'export, sans modifier l'identité."""
import json
import tempfile
import unittest
from pathlib import Path
from commun import application, ligne
from academie_etat import journal
import importer_journal

class RelectureChronologieServeur(unittest.TestCase):
    def test_import_et_export_offsets_fractions_unicode(self):
        attendu = [
            ligne(1, quand="2026-10-25T02:50:00+02:00"),
            ligne(2, quand="2026-10-25T02:10:00+01:00", nonce="\ue000aaaaaaa"),
            ligne(3, quand="2026-10-25T02:10:00+01:00", nonce="\U00010000aaaaaaa"),
            ligne(4, quand="2026-10-25T01:10:00.0000001Z"),
            ligne(5, quand="2026-10-25T01:10:00.0000002Z"),
        ]
        inverse = list(reversed(attendu))
        with tempfile.TemporaryDirectory() as dossier:
            source = Path(dossier)/"revues.jsonl"
            brut = "\n".join(json.dumps(l) for l in inverse)
            source.write_text(brut)
            migrees, illisibles = importer_journal.migrer_fichier(source)
            self.assertEqual(illisibles, 0)
            self.assertEqual(migrees, attendu)
            self.assertEqual(source.read_text(), brut)
        appli, profil, _ = application()
        try:
            journal.fusionner(appli.conn, profil, inverse, None)
            self.assertEqual(journal.exporter(appli.conn, profil), attendu)
            bilan = journal.fusionner(appli.conn, profil, attendu, None)
            self.assertEqual((bilan["acceptees"],bilan["ignorees"]),(0,5))
            self.assertEqual(journal.exporter(appli.conn, profil), attendu)
        finally:
            appli.conn.close()

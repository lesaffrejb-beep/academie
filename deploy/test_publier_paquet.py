"""Archive et manifeste malformés doivent échouer avant toute publication."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).parent))
import publier_paquet as module

SHA = "a" * 40

class Paquet(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / "source"
        self.source.mkdir()
        contenus = {nom: "contenu" for nom in module.REQUIS}
        contenus.update({"version-source.json": json.dumps({"commit": SHA}),
            "banque.json": json.dumps({"cartes":[{"id":"c"}], "etudes":{"lecons":{"l":{"statut":"valide","cartes":["c"]}}}}),
            ".vite/manifest.json": json.dumps({"index.html":{"file":"assets/index.js"}}),
            "assets/index.js": "code"})
        for nom, contenu in contenus.items():
            chemin = self.source / nom
            chemin.parent.mkdir(parents=True, exist_ok=True)
            chemin.write_text(contenu)
        self.manifeste()

    def manifeste(self):
        fichiers = [{"chemin":str(p.relative_to(self.source)),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in self.source.rglob("*") if p.is_file() and p.name != "publication-manifeste.json"]
        (self.source / "publication-manifeste.json").write_text(json.dumps({"version":1,"fichiers":fichiers}))

    def test_archive_valide_rejouee_jusqu_au_manifeste(self):
        archive = self.base / "publication.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(self.source, arcname=".")
        cible = self.base / "extrait"
        module.extraire(archive, cible, hashlib.sha256(archive.read_bytes()).hexdigest())
        self.assertEqual(set(module.verifier(cible, SHA, 1)), set(module.verifier(self.source, SHA, 1)))

    def test_paquet_identifie(self):
        self.assertIn("assets/index.js", module.verifier(self.source, SHA, 1))

    def test_sha_et_compte_etudes_differents(self):
        with self.assertRaises(ValueError): module.verifier(self.source, "b"*40, 1)
        with self.assertRaises(ValueError): module.verifier(self.source, SHA, 2)

    def test_fichier_altere(self):
        (self.source / "index.html").write_text("altéré")
        with self.assertRaises(ValueError): module.verifier(self.source, SHA, 1)

    def test_fichier_non_declare(self):
        (self.source / "inattendu.json").write_text("{}")
        with self.assertRaises(ValueError): module.verifier(self.source, SHA, 1)

    def test_etude_sans_carte_refusee(self):
        (self.source / "banque.json").write_text(json.dumps({"cartes":[],"etudes":{"lecons":{"l":{"statut":"valide","cartes":["absente"]}}}}))
        self.manifeste()
        with self.assertRaises(ValueError): module.verifier(self.source, SHA, 1)

    def test_traversee_et_liens_archive(self):
        for nom, lien in [("../sortie",False),("/absolu",False),("valide",True)]:
            archive = self.base / "paquet.tar"
            with tarfile.open(archive,"w") as tar:
                entree=tarfile.TarInfo(nom)
                if lien: entree.type=tarfile.SYMTYPE; entree.linkname="/etc/passwd"
                else: entree.size=1
                tar.addfile(entree,None if lien else io.BytesIO(b"x"))
            cible=self.base / ("extrait"+str(lien))
            with self.assertRaises(ValueError): module.extraire(archive,cible,hashlib.sha256(archive.read_bytes()).hexdigest())
            self.assertFalse(cible.exists())

    def test_distribution_garde_les_anciens_assets_et_termine_par_entrees(self):
        publication = self.base / "publication"
        publication.mkdir()
        ancien = publication / "ancien.js"
        ancien.write_text("onglet existant")
        ordre = []
        with patch.object(module, "PUBLICATION", publication), patch.object(module, "copie_atomique", side_effect=lambda src, dst: ordre.append(dst.name)):
            module.distribuer(self.source, module.verifier(self.source, SHA, 1))
        self.assertEqual(ordre[-2:], ["index.html", "sw.js"])
        self.assertTrue(ancien.exists())

    def test_lien_destination_refuse_avant_premiere_copie(self):
        publication = self.base / "publication"
        publication.mkdir()
        (publication / "assets").symlink_to(self.source, target_is_directory=True)
        with patch.object(module, "PUBLICATION", publication), patch.object(module, "copie_atomique") as copie:
            with self.assertRaises(ValueError): module.distribuer(self.source, module.verifier(self.source, SHA, 1))
            copie.assert_not_called()

    def test_digest_refuse_avant_extraction(self):
        archive=self.base / "paquet.tar"
        archive.write_bytes(b"invalide")
        with self.assertRaises(ValueError): module.extraire(archive,self.base/"extrait","0"*64)
        self.assertFalse((self.base/"extrait").exists())

if __name__ == "__main__": unittest.main()

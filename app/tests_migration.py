#!/usr/bin/env python3
"""ACA-CONTRAT-2 : une preparation conserve les faits et refuse de publier le rouge."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests_chapitres import chapitre, carte

APP = Path(__file__).resolve().parent
RACINE = APP.parent
SCRIPT = APP / "migre_banque.py"
CID = "droit.majorites.l-article-24"
KID = "droit-majorites-article-24"


def empreintes(racine: Path) -> dict[str, str]:
    return {str(f.relative_to(racine)): hashlib.sha256(f.read_bytes()).hexdigest()
            for f in racine.rglob("*") if f.is_file()}


class MigrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="academie-migration-test-")
        self.addCleanup(self.tmp.cleanup)
        self.racine = Path(self.tmp.name) / "source"
        self.racine.mkdir()
        self.carte = carte(id=KID, chapitre=CID, statut="valide", verifie_par="agent frais, fixture")
        self.carte.pop("chapitre")
        self.carte["origine"] = "fixture sans donnee metier"
        self.chapitre = chapitre(id=CID, cartes=[carte(id="droit-majorites-pilote", chapitre=CID)])
        self.ecris("programme/copro.json", json.loads((RACINE / "programme/copro.json").read_text()))
        self.ecris("academie.json", json.loads((RACINE / "academie.json").read_text()))
        self.ecris("banque/droit/majorites.json", [self.carte])
        self.ecris("chapitres/droit/majorites/l-article-24.json", self.chapitre)

    def ecris(self, chemin, valeur):
        cible = self.racine / chemin
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(json.dumps(valeur, ensure_ascii=False), encoding="utf-8")

    def lance(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), "--racine", str(self.racine),
                               "--json", *map(str, args)], capture_output=True, text=True)

    def test_simulation_ne_touche_pas_a_la_source(self):
        avant = empreintes(self.racine)
        res = self.lance()
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertEqual(empreintes(self.racine), avant)
        rapport = json.loads(res.stdout)
        self.assertEqual(rapport["cartes_v1"], 1)
        self.assertEqual(rapport["erreurs_validation"], [])

    def refuse_changement_apres_preparation(self, changement):
        from migre_banque import prepare, staging
        rapport, chapitres, non_assignees = prepare(self.racine)
        self.assertTrue(rapport["pret_pour_revue"])
        changement()
        cible = Path(self.tmp.name) / "source-changee"
        staging(self.racine, cible, rapport, chapitres, non_assignees)
        self.assertFalse(rapport["source_inchangee"])
        self.assertFalse(rapport["pret_pour_revue"])
        self.assertFalse((cible / "site/banque.json").exists())

    def test_ajout_source_apres_preparation_bloque_la_generation(self):
        self.refuse_changement_apres_preparation(lambda: self.ecris(
            "banque/droit/ajout-concurrent.json", [dict(self.carte, id="droit-majorites-article-25")]))

    def test_modification_source_apres_preparation_bloque_la_generation(self):
        self.refuse_changement_apres_preparation(lambda: self.ecris(
            "banque/droit/majorites.json", [dict(self.carte, question="Question corrigee.")]))

    def test_suppression_source_apres_preparation_bloque_la_generation(self):
        self.refuse_changement_apres_preparation(lambda: (self.racine / "banque/droit/majorites.json").unlink())

    def test_candidat_conserve_pilote_contenu_et_publie_v2(self):
        avant = empreintes(self.racine)
        cible = Path(self.tmp.name) / "candidat"
        res = self.lance("--staging", cible)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertEqual(empreintes(self.racine), avant)
        ch = json.loads((cible / "chapitres/droit/majorites/l-article-24.json").read_text())
        self.assertEqual(ch["lecon"], self.chapitre["lecon"])
        self.assertEqual(ch["provenance"], self.chapitre["provenance"])
        self.assertEqual(ch["cartes"][0], self.chapitre["cartes"][0])
        migree = next(c for c in ch["cartes"] if c["id"] == KID)
        self.assertEqual(migree, dict(self.carte, chapitre=CID))
        self.assertEqual(list((cible / "banque").rglob("*.json")), [])
        publiee = json.loads((cible / "site/banque.json").read_text())
        self.assertEqual(publiee["contrat"], "carte-v2")
        self.assertEqual([c["id"] for c in publiee["cartes"]], [KID])
        self.assertIn("note_confiance", publiee["cartes"][0])

    def test_les_absences_et_niveaux_ne_sont_pas_inventes(self):
        self.carte.pop("provenance")
        self.carte.pop("verifie_par")
        self.carte["niveau"] = 3
        self.ecris("banque/droit/majorites.json", [self.carte])
        cible = Path(self.tmp.name) / "rouge"
        res = self.lance("--staging", cible)
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        rapport = json.loads(res.stdout)
        self.assertEqual(rapport["relecteurs_manquants"], [KID])
        self.assertEqual(rapport["auteurs_manquants"], [KID])
        self.assertEqual(rapport["niveaux_incompatibles"][0]["carte"], KID)
        ch = json.loads((cible / "chapitres/droit/majorites/l-article-24.json").read_text())
        migree = next(c for c in ch["cartes"] if c["id"] == KID)
        self.assertEqual(migree["niveau"], 3)
        self.assertEqual(migree["statut"], "valide")
        self.assertNotIn("verifie_par", migree)
        self.assertNotIn("auteur", migree["provenance"])
        self.assertNotIn("modele", migree["provenance"])
        self.assertFalse((cible / "site/banque.json").exists())

    def test_une_origine_en_texte_ne_devient_pas_un_relecteur(self):
        self.carte.pop("verifie_par")
        self.carte["origine"] = "texte corrige et verifie en double passe, sans nom de session"
        self.ecris("banque/droit/majorites.json", [self.carte])
        res = self.lance()
        self.assertEqual(res.returncode, 1)
        self.assertEqual(json.loads(res.stdout)["relecteurs_manquants"], [KID])

    def test_destination_source_et_destination_existante_refusees(self):
        avant = empreintes(self.racine)
        for cible in (self.racine, self.racine / "chapitres/nouveau", Path(self.tmp.name)):
            res = self.lance("--staging", cible)
            self.assertNotEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertEqual(empreintes(self.racine), avant)

    def test_doublon_et_carte_sans_assignation_ne_disparaissent_pas(self):
        autre = dict(self.carte, id="carte-sans-decision")
        self.ecris("banque/droit/majorites.json", [self.carte, self.carte, autre])
        res = self.lance()
        self.assertEqual(res.returncode, 1)
        rapport = json.loads(res.stdout)
        self.assertEqual(rapport["sans_assignation"], ["carte-sans-decision"])
        self.assertEqual(rapport["doublons"], [KID])

    def test_collision_avec_un_pilote_est_refusee(self):
        self.chapitre["cartes"][0]["id"] = KID
        self.ecris("chapitres/droit/majorites/l-article-24.json", self.chapitre)
        cible = Path(self.tmp.name) / "collision"
        res = self.lance("--staging", cible)
        self.assertEqual(res.returncode, 1)
        self.assertEqual(json.loads(res.stdout)["doublons"], [KID])
        self.assertFalse((cible / "site/banque.json").exists())

    def test_le_squelette_ne_masque_pas_les_cartes_invalides(self):
        self.carte["id"] = "droit-majorites-article-25"
        self.carte.pop("verifie_par")
        self.ecris("banque/droit/majorites.json", [self.carte])
        res = self.lance()
        self.assertEqual(res.returncode, 1)
        rapport = json.loads(res.stdout)
        self.assertIn("droit.majorites.l-article-25-et-la-passerelle", rapport["chapitres_a_ecrire"])
        self.assertTrue(any("verifie_par" in e for e in rapport["erreurs_validation"]))

    def test_un_programme_cyclique_ne_peut_pas_produire_un_candidat_vert(self):
        programme = json.loads((self.racine / "programme/copro.json").read_text())
        programme["chapitres"][0]["prerequis"] = [programme["chapitres"][0]["id"]]
        self.ecris("programme/copro.json", programme)
        res = self.lance()
        self.assertEqual(res.returncode, 1)
        self.assertTrue(any("cycle" in e for e in json.loads(res.stdout)["erreurs_validation"]))

    def test_table_explicite_applique_les_exceptions_arbitrees(self):
        from migre_banque import ASSIGNATIONS
        self.assertEqual(len(ASSIGNATIONS), 84)
        self.assertEqual(ASSIGNATIONS["droit-veille-notification-electronique-principe"], "droit.assemblee.la-notification")
        self.assertEqual(ASSIGNATIONS["droit-veille-pieces-espace-en-ligne"], "droit.assemblee.les-pieces-jointes-obligatoires")
        self.assertEqual(ASSIGNATIONS["procedure-recouvrement-datation-decheance"], "procedure.recouvrement.la-decheance-du-terme")
        self.assertEqual(ASSIGNATIONS["equipements-chauffage-libre-expliquer-p3-au-cs"], "equipements.chauffage.les-contrats-p1-a-p5")

    def test_nature_de_secours_est_editeur(self):
        self.carte["source"][0].pop("nature")
        self.ecris("banque/droit/majorites.json", [self.carte])
        cible = Path(self.tmp.name) / "editeur"
        res = self.lance("--staging", cible)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        publiee = json.loads((cible / "site/banque.json").read_text())
        self.assertEqual(publiee["cartes"][0]["source"][0]["nature"], "editeur")
        self.assertTrue(publiee["cartes"][0]["a_recouper"])

    def test_programme_applique_la_decision_0030(self):
        programme = json.loads((RACINE / "programme/copro.json").read_text())
        ids = {c["id"]: c for c in programme["chapitres"]}
        notification = ids.get("droit.assemblee.la-notification", {})
        decheance = ids.get("procedure.recouvrement.la-decheance-du-terme", {})
        self.assertEqual(notification.get("niveau"), 2)
        self.assertEqual(notification.get("sous_branche"), "preparer")
        self.assertIn("droit.assemblee.la-convocation-forme-et-delai", notification["prerequis"])
        self.assertEqual(decheance.get("niveau"), 2)
        self.assertIn("procedure.avant-le-proces.mise-en-demeure-recommande-sommation", decheance["prerequis"])
        self.assertIn(decheance["id"], ids["procedure.recouvrement.choisir-la-voie"]["prerequis"])
        self.assertNotIn("equipements.chauffage.les-contrats-p1-a-p4", ids)
        self.assertIn("P5", ids["equipements.chauffage.les-contrats-p1-a-p5"]["notions"])


if __name__ == "__main__":
    unittest.main()

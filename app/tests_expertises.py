"""Le catalogue de spécialités ne fabrique pas de preuve d'expertise."""
import copy
import io
import unittest
import json
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch
from pathlib import Path

import couverture_expertises
from couverture_expertises import (SEMANTIQUE_FILTRE, construire, filtrer, main,
                                   markdown, verifier)


class CouvertureTests(unittest.TestCase):
    def setUp(self):
        self.programme = {"domaines": {"droit": {"titre": "Droit"}},
                          "branches": {"droit": [{"cle": "statut"}]},
                          "chapitres": [{"id": "droit.statut.a", "domaine": "droit", "niveau": 5}]}
        self.catalogue = {"specialites": [{"id": "juriste", "titre": "Juriste",
            "branches": ["droit.statut"], "objectifs": ["Arbitrer"],
            "production": "Note contradictoire", "sources_a_instruire": ["Textes"],
            "limite": "Pas une qualification", "statut": "a-construire"}]}

    def test_branche_inconnue_refusee(self):
        c = copy.deepcopy(self.catalogue)
        c["specialites"][0]["branches"] = ["droit.invente"]
        self.assertTrue(verifier(c, self.programme))

    def test_production_et_limite_obligatoires(self):
        for champ in ("production", "limite", "sources_a_instruire", "objectifs"):
            c = copy.deepcopy(self.catalogue)
            del c["specialites"][0][champ]
            self.assertTrue(verifier(c, self.programme), champ)

    def test_pas_de_couverture_inventee(self):
        r = construire(self.catalogue, self.programme, {"cartes": []}, [])
        self.assertEqual(r["domaines"][0]["chapitres_prevus"], 1)
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 0)
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 0)

    def test_autre_cursus_exclu_et_v1_non_attribuee(self):
        cartes = {"cartes": [
            {"id": "copro", "domaine": "droit", "niveau": 1, "statut": "valide"},
            {"id": "ifsi", "domaine": "pharmaco", "niveau": 5, "statut": "valide"},
            {"id": "draft", "domaine": "droit", "niveau": 5, "statut": "brouillon"}]}
        r = construire(self.catalogue, self.programme, cartes, [])
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 1)
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 0)
        self.assertEqual(r["cartes_sans_chapitre"], 1)

    def test_artefact_absent_reste_inconnu(self):
        r = construire(self.catalogue, self.programme, None, [])
        self.assertIsNone(r["domaines"][0]["cartes_artefact"])
        self.assertIsNone(r["specialites"][0]["cartes_rattachees"])

    def test_doublon_specialite_refuse(self):
        c = copy.deepcopy(self.catalogue)
        c["specialites"] *= 2
        self.assertTrue(verifier(c, self.programme))

    def test_rattachement_exact_sans_couverture_competence(self):
        cartes = {"cartes": [{"id": "a", "domaine": "droit", "niveau": 4,
                            "chapitre": "droit.statut.a", "statut": "valide"}]}
        r = construire(self.catalogue, self.programme, cartes, [])
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 1)
        self.assertEqual(r["specialites"][0]["statut"], "a-construire")
        self.assertEqual(r, construire(self.catalogue, self.programme, cartes, []))

    def test_catalogue_reel(self):
        racine = Path(__file__).resolve().parents[1]
        catalogue = json.loads((racine / "programme/specialisations/copro.json").read_text())
        programme = json.loads((racine / "programme/copro.json").read_text())
        self.assertEqual(verifier(catalogue, programme), [])
        r = construire(catalogue, programme, None, [])
        self.assertEqual(len(r["specialites"]), len(catalogue["specialites"]))

    def test_domaine_commun_ne_melange_pas_les_cursus(self):
        artefact = {"cartes": [{"id": "autre", "domaine": "droit", "statut": "valide",
                               "niveau": 5, "chapitre": "droit.autre-cursus.a"}]}
        r = construire(self.catalogue, self.programme, artefact, [])
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 0)

    def test_champs_malformes_refuses_sans_exception(self):
        for champ, valeur in [("production", "   "), ("limite", 5), ("branches", [[]]),
                              ("id", []), ("titre", None)]:
            c = copy.deepcopy(self.catalogue)
            c["specialites"][0][champ] = valeur
            self.assertTrue(verifier(c, self.programme), (champ, valeur))


def programme_deux_domaines():
    return {"domaines": {"droit": {"titre": "Droit"}, "travaux": {"titre": "Travaux"}},
            "branches": {"droit": [{"cle": "statut"}], "travaux": [{"cle": "chantier"}]},
            "chapitres": [
                {"id": "droit.statut.a", "domaine": "droit", "niveau": 5,
                 "titre": "Statut A", "statut": "a-ecrire"},
                {"id": "travaux.chantier.b", "domaine": "travaux", "niveau": 2,
                 "titre": "Chantier B", "statut": "a-ecrire"}]}


def catalogue_deux_specialites():
    return {"specialites": [
        {"id": "juriste", "titre": "Juriste", "branches": ["droit.statut"],
         "objectifs": ["Arbitrer"], "production": "Note contradictoire",
         "sources_a_instruire": ["Textes"], "limite": "Pas une qualification",
         "statut": "a-construire"},
        {"id": "chantier", "titre": "Chantier", "branches": ["travaux.chantier"],
         "objectifs": ["Lire un chantier"], "production": "Dossier de chantier",
         "sources_a_instruire": ["DTU sous licence"], "limite": "Pas une habilitation",
         "statut": "a-construire"}]}


def rapport_deux_domaines(cartes=None):
    return construire(catalogue_deux_specialites(), programme_deux_domaines(),
                      {"cartes": [] if cartes is None else cartes}, [])


class FiltreCouvertureTests(unittest.TestCase):
    def setUp(self):
        self.programme = programme_deux_domaines()
        self.cartes = [{"id": "a", "domaine": "droit", "niveau": 4,
                        "chapitre": "droit.statut.a", "statut": "valide"}]

    def test_filtre_domaine_reduit_et_laisse_le_global_intact(self):
        global_ = rapport_deux_domaines(self.cartes)
        extrait = filtrer(global_, self.programme, domaine="droit")
        self.assertEqual(extrait["filtre"]["type"], "domaine")
        self.assertEqual(extrait["filtre"]["id"], "droit")
        self.assertEqual([d["id"] for d in extrait["domaines"]], ["droit"])
        self.assertEqual(extrait["domaines"][0]["cartes_artefact"], 1)
        self.assertEqual([s["id"] for s in extrait["specialites"]], ["juriste"])
        self.assertEqual([c["id"] for c in extrait["chapitres"]], ["droit.statut.a"])
        self.assertEqual(len(global_["domaines"]), 2)
        self.assertEqual(len(global_["specialites"]), 2)

    def test_filtre_specialite_garde_ses_compteurs_seulement(self):
        global_ = rapport_deux_domaines(self.cartes)
        extrait = filtrer(global_, self.programme, specialite="chantier")
        self.assertEqual(extrait["filtre"]["type"], "specialite")
        self.assertEqual([s["id"] for s in extrait["specialites"]], ["chantier"])
        self.assertEqual(extrait["specialites"][0]["cartes_rattachees"], 0)
        self.assertEqual([d["id"] for d in extrait["domaines"]], ["travaux"])
        self.assertEqual([c["id"] for c in extrait["chapitres"]], ["travaux.chantier.b"])

    def test_filtre_inconnu_refuse_avec_les_identifiants_utilisables(self):
        global_ = rapport_deux_domaines(self.cartes)
        with self.assertRaises(ValueError) as domaine:
            filtrer(global_, self.programme, domaine="energie")
        message = str(domaine.exception)
        self.assertIn("energie", message)
        self.assertIn("droit", message)
        self.assertIn("travaux", message)
        with self.assertRaises(ValueError) as specialite:
            filtrer(global_, self.programme, specialite="travaux")
        self.assertIn("juriste", str(specialite.exception))
        self.assertIn("chantier", str(specialite.exception))

    def test_filtre_exclusif_et_obligatoire(self):
        global_ = rapport_deux_domaines(self.cartes)
        for appel in (lambda: filtrer(global_, self.programme),
                      lambda: filtrer(global_, self.programme, specialite="juriste",
                                      domaine="droit")):
            with self.assertRaises(ValueError):
                appel()

    def test_extrait_ne_renseigne_aucun_total_global(self):
        extrait = filtrer(rapport_deux_domaines(self.cartes), self.programme, domaine="droit")
        self.assertNotIn("cartes_sans_chapitre", extrait)
        self.assertIn("cartes_sans_chapitre", extrait["hors_extrait"])
        self.assertIn("Extrait ciblé", markdown(extrait))

    def test_portee_precise_le_perimetre_du_socle(self):
        r = rapport_deux_domaines(self.cartes)
        for mot in ("cartes sans chapitre", "rattachement exact au socle",
                    "satellites sont exclues", "ne signifie pas absence de contenu"):
            self.assertIn(mot, r["portee"])
        extrait = filtrer(r, self.programme, specialite="juriste")
        self.assertEqual(extrait["portee"], r["portee"])
        rendu = markdown(extrait)
        self.assertIn("cartes sans chapitre", rendu)
        self.assertIn("ne signifie pas absence de contenu", rendu)

    def test_note_de_portee_decrit_les_compteurs_reels(self):
        cartes = {"cartes": [
            {"id": "socle", "domaine": "droit", "niveau": 2,
             "chapitre": "droit.statut.a", "statut": "valide"},
            {"id": "sans-chapitre", "domaine": "droit", "niveau": 2, "statut": "valide"}]}
        r = construire(catalogue_deux_specialites(), self.programme, cartes, [])
        self.assertEqual(r["domaines"][0]["cartes_artefact"], 2)
        self.assertEqual(r["specialites"][0]["cartes_rattachees"], 1)
        self.assertEqual(r["cartes_sans_chapitre"], 1)
        note = r["portee"]
        self.assertIn("Les compteurs de domaines incluent les cartes du socle et les cartes sans chapitre.", note)
        self.assertIn("Les compteurs de spécialités exigent un rattachement exact au socle.", note)
        self.assertIn("Les études et cartes satellites sont exclues", note)
        self.assertIn("zéro dans une spécialité ne signifie pas absence de contenu sur le thème", note)

    def test_extrait_absent_reste_inconnu_et_deterministe(self):
        r = construire(catalogue_deux_specialites(), self.programme, None, [])
        extrait = filtrer(r, self.programme, specialite="juriste")
        self.assertIsNone(extrait["specialites"][0]["cartes_rattachees"])
        self.assertIsNone(extrait["domaines"][0]["cartes_artefact"])
        self.assertEqual(extrait, filtrer(construire(catalogue_deux_specialites(),
                                                     self.programme, None, []),
                                          self.programme, specialite="juriste"))
        domaine = filtrer(r, self.programme, domaine="droit")
        self.assertIsNone(domaine["domaines"][0]["cartes_artefact"])
        self.assertIn("inconnu (artefact absent)", markdown(domaine))
        self.assertNotIn("0 carte valide de l'artefact", markdown(domaine))

    def test_json_extrait_porte_filtre_et_portee(self):
        global_ = rapport_deux_domaines(self.cartes)
        extrait = filtrer(global_, self.programme, domaine="droit")
        self.assertEqual(extrait["filtre"]["semantique"], SEMANTIQUE_FILTRE)
        self.assertEqual(extrait["portee"], global_["portee"])
        self.assertNotIn("cartes_sans_chapitre", extrait)
        self.assertEqual(extrait["hors_extrait"], ["cartes_sans_chapitre"])

    def test_specialite_transversale_previent_des_totaux_de_domaine(self):
        catalogue = catalogue_deux_specialites()
        catalogue["specialites"][0]["branches"] = ["droit.statut", "travaux.chantier"]
        r = construire(catalogue, self.programme, {"cartes": self.cartes}, [])
        rendu = markdown(filtrer(r, self.programme, specialite="juriste"))
        self.assertIn("## Compteurs des domaines touchés", rendu)
        self.assertIn("portent le domaine entier", rendu)
        self.assertIn("ne démontre pas la couverture des objectifs", rendu)

    def test_rendu_ne_promet_pas_de_contenu_servi(self):
        r = rapport_deux_domaines(self.cartes)
        for rendu in (markdown(r), markdown(filtrer(r, self.programme, domaine="droit")),
                      markdown(filtrer(r, self.programme, specialite="juriste"))):
            self.assertNotIn("servies localement", rendu)
            self.assertIn("Cartes artefact N4/N5", rendu)
        self.assertIn("contenu actuellement servi", markdown(r))

    def test_extrait_lisible_commence_par_un_resume(self):
        r = rapport_deux_domaines(self.cartes)
        rendu = markdown(filtrer(r, self.programme, domaine="droit"))
        specialite = markdown(filtrer(r, self.programme, specialite="juriste"))
        lignes = rendu.splitlines()
        self.assertTrue(lignes[0].startswith("# "))
        self.assertIn("droit", lignes[0])
        self.assertIn("domaine `droit`, Droit", lignes[0])
        self.assertIn("spécialité `juriste`, Juriste", specialite.splitlines()[0])
        for texte in (rendu, specialite):
            self.assertIn("## En bref", texte.splitlines())
        self.assertLess(rendu.index("## En bref"), rendu.index("## Chapitres prévus"))
        self.assertLess(specialite.index("## En bref"), specialite.index("## Chapitres thématiquement"))
        self.assertIn("1 chapitre prévu", rendu)
        self.assertIn("1 carte valide de l'artefact", rendu)
        self.assertIn("1 spécialité", rendu)
        self.assertIn("1 carte rattachée à un chapitre", specialite)


class CliCouvertureTests(unittest.TestCase):
    def setUp(self):
        racine = Path(__file__).resolve().parents[1]
        self.rapport = racine / "travail/expertise-2026-09-06/COUVERTURE.md"
        self.avant = self.rapport.read_bytes()

    def lancer(self, *arguments):
        sortie, erreur = io.StringIO(), io.StringIO()
        with redirect_stdout(sortie), redirect_stderr(erreur):
            code = main(list(arguments))
        return code, sortie.getvalue(), erreur.getvalue()

    def test_check_et_write_filtres_refuses(self):
        for arguments in (("--domaine", "droit", "--check"),
                          ("--specialite", "juriste-copro", "--check"),
                          ("--domaine", "droit", "--write")):
            code, _, erreur = self.lancer(*arguments)
            self.assertEqual(code, 2, arguments)
            self.assertTrue(erreur.strip(), arguments)
        self.assertEqual(self.rapport.read_bytes(), self.avant)

    def test_sortie_ecrit_l_extrait_sans_toucher_le_rapport_global(self):
        with tempfile.TemporaryDirectory() as dossier:
            cible = Path(dossier) / "sous-dossier" / "electricite.md"
            code, _, _ = self.lancer("--specialite", "electricite", "--sortie", str(cible))
            self.assertEqual(code, 0)
            rendu = cible.read_text(encoding="utf-8")
            self.assertIn("# Couverture éditoriale copro", rendu)
            self.assertIn("electricite", rendu)
            self.assertEqual(self.rapport.read_bytes(), self.avant)

    def test_identifiant_inconnu_refuse_en_listant_les_utilisables(self):
        code, sortie, erreur = self.lancer("--domaine", "inexistant")
        self.assertEqual(code, 2)
        self.assertEqual(sortie, "")
        self.assertIn("droit", erreur)
        self.assertIn("travaux", erreur)

    def test_json_filtre_reste_du_json(self):
        code, sortie, _ = self.lancer("--domaine", "droit", "--json")
        self.assertEqual(code, 0)
        extrait = json.loads(sortie)
        self.assertEqual(extrait["filtre"]["id"], "droit")
        self.assertEqual([d["id"] for d in extrait["domaines"]], ["droit"])

    def test_write_json_sans_sortie_refuse_sans_toucher_le_rapport(self):
        code, sortie, erreur = self.lancer("--write", "--json")
        self.assertEqual(code, 2)
        self.assertEqual(sortie, "")
        self.assertIn("Markdown", erreur)
        self.assertEqual(self.rapport.read_bytes(), self.avant)
        self.assertTrue(self.rapport.read_text(encoding="utf-8")
                        .startswith("# Couverture éditoriale copro"))

    def test_write_json_refuse_avant_toute_ecriture(self):
        with tempfile.TemporaryDirectory() as dossier:
            faux = Path(dossier) / "sous-dossier" / "COUVERTURE.md"
            with patch.object(couverture_expertises, "RAPPORT_GLOBAL", faux):
                code, _, _ = self.lancer("--write", "--json")
            self.assertEqual(code, 2)
            self.assertFalse(faux.exists())

    def test_sortie_sur_le_rapport_global_refusee(self):
        equivalent = self.rapport.parent / ".." / "expertise-2026-09-06" / "COUVERTURE.md"
        for arguments in (("--specialite", "electricite", "--sortie", str(self.rapport)),
                          ("--domaine", "droit", "--sortie", str(equivalent)),
                          ("--json", "--sortie", str(self.rapport))):
            code, sortie, erreur = self.lancer(*arguments)
            self.assertEqual(code, 2, arguments)
            self.assertEqual(sortie, "", arguments)
            self.assertIn("rapport global", erreur, arguments)
            self.assertEqual(self.rapport.read_bytes(), self.avant, arguments)

    def test_write_seul_ecrit_le_markdown_canonique(self):
        with tempfile.TemporaryDirectory() as dossier:
            faux = Path(dossier) / "sous-dossier" / "COUVERTURE.md"
            with patch.object(couverture_expertises, "RAPPORT_GLOBAL", faux):
                code, sortie, _ = self.lancer("--write")
                self.assertEqual(code, 0)
                self.assertEqual(sortie.strip(), str(faux))
                texte = faux.read_text(encoding="utf-8")
            self.assertTrue(texte.startswith("# Couverture éditoriale copro"))
            self.assertNotIn('"portee"', texte)
            self.assertEqual(self.rapport.read_bytes(), self.avant)

    def test_json_reste_possible_sur_une_sortie_distincte(self):
        with tempfile.TemporaryDirectory() as dossier:
            cible = Path(dossier) / "extrait.json"
            code, _, _ = self.lancer("--domaine", "droit", "--json", "--sortie", str(cible))
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(cible.read_text(encoding="utf-8"))["filtre"]["id"], "droit")
            self.assertEqual(self.rapport.read_bytes(), self.avant)

    def test_extrait_electricite_porte_la_note_de_perimetre_socle(self):
        code, sortie, _ = self.lancer("--specialite", "electricite")
        self.assertEqual(code, 0)
        self.assertIn("cartes sans chapitre", sortie)
        self.assertIn("satellites sont exclues", sortie)
        code, sortie, _ = self.lancer("--specialite", "electricite", "--json")
        self.assertEqual(code, 0)
        portee = json.loads(sortie)["portee"]
        self.assertIn("cartes sans chapitre", portee)
        self.assertIn("rattachement exact au socle", portee)
        self.assertIn("0", sortie)


if __name__ == "__main__":
    unittest.main()

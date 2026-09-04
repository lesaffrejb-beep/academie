#!/usr/bin/env python3
"""Contrat structurel IFSI 2026 et mutations, ACA-IFSI-1.

Les petits exemples ne sont pas du contenu clinique. L'intégration réelle
vérifie séparément l'inventaire et le rendu reproductible.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SHA_HISTORIQUE = "056163e3e865a65c70fa3176a1ccb18d7a4475bd87b34783e9af4d051bc4a6f7"
VOIES = ("parcoursup", "fpc", "specifique")


def charger(nom: str, chemin: Path):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def exemple() -> dict:
    cid = "entree.reperes.premier"
    chapter = {
        "id": cid, "domaine": "entree", "branche": "reperes", "titre": "Premier repère",
        "niveau": 1, "prerequis": [], "ponts": [], "cartes_cible": 6,
        "etude_minutes": 30, "statut": "a-ecrire", "referentiel_version": "DEI-2026",
        "domaine_enseignement": "A", "competence_ids": ["1"], "ue_ids": [],
        "etape": "orientation", "difficulte": 3, "criticite": "informatif",
        "modes": ["entrainement"], "contextes": ["orientation"], "voies": list(VOIES),
        "optionnel": False,
        "validation": {"numerique": "connaissances-et-raisonnement", "geste_supervise": False,
                       "certification_clinique": False},
        "revision": {"action": "reecrire", "raison": "Rattacher au référentiel courant.",
                     "statut": "proposition-editoriale"},
        "objectifs": [{"id": cid + ".o1", "capacite": "Distinguer les voies d'entrée",
                       "dimension": "raisonnement", "exercice": "qcm"}],
        "legacy": {"niveau": 1, "ue_ids": [], "titre": "Premier repère"},
    }
    competences = {str(n): {"titre": f"Compétence {n}", "domaine_enseignement": "ABCDE"[(n-1) % 5]}
                   for n in range(1, 14)}
    return {
        "metier": "infirmier", "genere_le": "2026-09-04", "referentiel_actif": "DEI-2026",
        "referentiels": {
            "DEI-2026": {"titre": "Référentiel courant", "valid_from": "2026-09-01",
                         "valid_until": None, "reviewed_at": "2026-09-04", "source_ids": ["arrete"]},
            "DEI-2009": {"titre": "Référentiel historique", "valid_from": "2009-09-01",
                         "valid_until": "2030-06-30", "reviewed_at": "2026-09-04",
                         "source_ids": ["arrete"], "programme": "programme/versions/ifsi-2009.json"},
        },
        "sources_reglementaires": {"arrete": {"titre": "Texte de référence",
            "url": "https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000000000",
            "repere": "Annexe", "consulte_le": "2026-09-04"}},
        "competences_reglementaires": competences,
        "domaines_enseignement": {d: {"titre": f"Domaine {d}", "competence_ids":
            [k for k, c in competences.items() if c["domaine_enseignement"] == d]} for d in "ABCDE"},
        "domaines": {"entree": {"titre": "Entrée", "ordre": 1}},
        "branches": {"entree": [{"cle": "reperes", "titre": "Repères", "ordre": 1,
                                    "sous_branches": []}]},
        "socle": {"niveaux": {}, "chapitres": 0, "cartes_cible": 0},
        "semaine_type": {j: "cours" for j in ("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche")},
        "chapitres": [chapter],
        "compte": {"chapitres": 1, "cartes_cible_total": 6, "sous_branches": 0,
                   "par_niveau": {str(n): int(n == 1) for n in range(1, 6)}},
        "parcours": {v: {"titre": v, "objectif": "Préparer son entrée.", "diagnostic": [cid],
            "semaines": [{"n": n, "theme": "Repères", "chapitres": [cid], "etude": cid}
                         for n in range(1, 13)]} for v in VOIES},
    }


class ContratIFSI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.extension = charger("valide_ifsi_test", RACINE / "app/valide_ifsi.py")

    def refuse(self, p, fragment):
        erreurs = self.extension.valider(p, "exemple.json")
        self.assertTrue(any(fragment in e for e in erreurs), erreurs)

    def test_exemple_valide_et_difficulte_independante_du_niveau(self):
        p = exemple(); avant = copy.deepcopy(p)
        self.assertEqual(self.extension.valider(p), [])
        self.assertEqual(p, avant, "le valideur ne modifie pas son inventaire")

    def test_referentiel_actif_obligatoire_et_declare(self):
        for valeur in (None, "DEI-2099", "DEI-2009"):
            p = exemple(); p["referentiel_actif"] = valeur
            self.refuse(p, "référentiel")

    def test_dates_et_sources_verifiables(self):
        for champ in ("valid_from", "reviewed_at"):
            p = exemple(); p["referentiels"]["DEI-2026"][champ] = "2026-99-99"
            self.refuse(p, "date")
        p = exemple(); p["referentiels"]["DEI-2026"]["source_ids"] = ["inconnue"]
        self.refuse(p, "source")
        p = exemple(); p["sources_reglementaires"]["arrete"]["url"] = "pas-un-lien"
        self.refuse(p, "source")
        p = exemple(); p["referentiels"]["DEI-2026"]["valid_until"] = "2020-01-01"
        self.refuse(p, "date")

    def test_mapping_chapitre_et_reciprocite_competences(self):
        for champ, valeur in (("competence_ids", ["99"]), ("domaine_enseignement", "Z"),
                              ("competence_ids", ["2"]), ("referentiel_version", "DEI-2009")):
            p = exemple(); p["chapitres"][0][champ] = valeur
            self.refuse(p, "rattachement")
        p = exemple(); p["domaines_enseignement"]["A"]["competence_ids"] = []
        self.refuse(p, "compétence")

    def test_competences_transversales_et_domaine_principal(self):
        p = exemple(); p["chapitres"][0]["competence_ids"] = ["1", "2"]
        self.assertEqual(self.extension.valider(p), [])

    def test_references_du_continuum_et_des_specialisations(self):
        p = exemple(); p["specialisations"] = {"exemple": {"titre": "Exemple", "chapitres": ["inconnu"]}}
        self.refuse(p, "inconnu")
        p = exemple(); p["trajectoire"] = {"etapes": [{"id": "orientation", "titre": "Repères",
            "objectif": "S'orienter", "chapitres": ["inconnu"]}]}
        self.refuse(p, "inconnu")

    def test_axes_et_proposition_editoriale(self):
        for champ, valeur, fragment in (("etape", "automatique", "étape"),
            ("difficulte", 0, "difficulté"), ("criticite", "faible", "criticité"),
            ("modes", ["certification"], "mode"), ("voies", ["concours"], "voie"),
            ("optionnel", "oui", "optionnel")):
            p = exemple(); p["chapitres"][0][champ] = valeur
            self.refuse(p, fragment)
        p = exemple(); p["chapitres"][0]["revision"]["statut"] = "valide-par-ifsi"
        self.refuse(p, "éditoriale")
        p = exemple(); p["chapitres"][0]["voies"] = None
        self.refuse(p, "voie")

    def test_un_score_ne_certifie_pas_un_geste(self):
        p = exemple(); p["chapitres"][0]["validation"]["certification_clinique"] = True
        self.refuse(p, "certification clinique")
        p = exemple(); p["chapitres"][0]["objectifs"][0]["dimension"] = "geste"
        self.refuse(p, "supervis")
        p["chapitres"][0]["validation"]["geste_supervise"] = True
        self.assertEqual(self.extension.valider(p), [])

    def test_ajout_sans_historique_explicite(self):
        p = exemple(); chapitre = p["chapitres"][0]
        chapitre["revision"]["action"] = "ajouter"
        chapitre["legacy"] = {"niveau": None, "titre": None, "ue_ids": []}
        self.assertEqual(self.extension.valider(p), [])
        for legacy in ({}, {"niveau": None, "titre": None, "ue_ids": ["UE inventée"]},
                       {"niveau": 1, "titre": "Passé inventé", "ue_ids": []}):
            chapitre["legacy"] = legacy
            self.refuse(p, "legacy")

    def test_historique_obligatoire_hors_ajout(self):
        for action in ("conserver", "reecrire", "deplacer", "scinder"):
            p = exemple(); chapitre = p["chapitres"][0]
            chapitre["revision"]["action"] = action
            chapitre["legacy"] = {"niveau": None, "titre": None, "ue_ids": []}
            self.refuse(p, "legacy")

    def test_prerequis_accessible_a_l_etape_annoncee(self):
        p = exemple(); chapitre = p["chapitres"][0]
        suivant = copy.deepcopy(chapitre)
        suivant["id"] = "entree.reperes.suivant"
        suivant["objectifs"][0]["id"] = suivant["id"] + ".o1"
        suivant["etape"] = "annee-2"
        p["chapitres"].append(suivant)
        p["compte"].update(chapitres=2, cartes_cible_total=12)
        p["compte"]["par_niveau"]["1"] = 2
        chapitre["etape"] = "annee-1"
        chapitre["prerequis"] = [suivant["id"]]
        self.refuse(p, "étape ultérieure")
        chapitre["etape"] = "annee-2"
        self.assertEqual(self.extension.valider(p), [])

    def test_objectifs_uniques_et_observables(self):
        p = exemple(); p["chapitres"][0]["objectifs"] *= 2
        self.refuse(p, "objectif")
        p = exemple(); p["chapitres"][0]["objectifs"][0]["capacite"] = ""
        self.refuse(p, "objectif")
        p = exemple(); p["chapitres"][0]["objectifs"] = []
        self.refuse(p, "objectif")

    def test_compteurs_calcules(self):
        for cle in ("chapitres", "cartes_cible_total", "sous_branches"):
            p = exemple(); p["compte"][cle] += 1
            self.refuse(p, "compte")
        p = exemple(); p["compte"]["par_niveau"]["1"] = 0
        self.refuse(p, "compte")
        p = exemple(); p["chapitres"][0]["etude_minutes"] = -1
        self.refuse(p, "durée")

    def test_trois_parcours_complets(self):
        p = exemple(); del p["parcours"]["fpc"]
        self.refuse(p, "parcours")
        p = exemple(); p["parcours"]["fpc"]["semaines"].pop()
        self.refuse(p, "douze")
        p = exemple(); p["parcours"]["fpc"]["semaines"][1]["n"] = 1
        self.refuse(p, "douze")
        p = exemple(); p["parcours"]["fpc"]["diagnostic"] = []
        self.refuse(p, "diagnostic")

    def test_parcours_sans_reference_inconnue_option_ni_melange(self):
        p = exemple(); p["parcours"]["fpc"]["semaines"][0]["etude"] = "inconnu"
        self.refuse(p, "inconnu")
        p = exemple(); p["chapitres"][0]["voies"] = ["fpc"]
        self.refuse(p, "voie")
        p = exemple(); p["chapitres"][0]["optionnel"] = True
        self.refuse(p, "optionnel")
        p = exemple(); p["mots_cles"] = {"entrée": ["inconnu"]}
        self.refuse(p, "inconnu")

    def test_prerequis_indirects_et_cycles(self):
        p = exemple(); base = p["chapitres"][0]
        for suffixe in ("second", "troisieme"):
            c = copy.deepcopy(base); c["id"] = "entree.reperes." + suffixe
            c["objectifs"][0]["id"] = c["id"] + ".o1"
            p["chapitres"].append(c)
        p["compte"].update(chapitres=3, cartes_cible_total=18)
        p["compte"]["par_niveau"]["1"] = 3
        p["chapitres"][0]["prerequis"] = [p["chapitres"][1]["id"]]
        p["chapitres"][1]["prerequis"] = [p["chapitres"][2]["id"]]
        self.assertEqual(self.extension.valider(p), [])
        p["chapitres"][2]["voies"] = ["fpc"]
        self.refuse(p, "voie")
        p["chapitres"][2]["voies"] = list(VOIES)
        p["chapitres"][2]["optionnel"] = True
        self.refuse(p, "optionnel")
        p["chapitres"][2]["optionnel"] = False
        p["chapitres"][2]["prerequis"] = [base["id"]]
        self.refuse(p, "cycle")
        p["chapitres"][2]["prerequis"] = ["inconnu"]
        self.refuse(p, "prérequis inconnu")

    def test_pas_d_ue_historique_obligatoire_dans_le_courant(self):
        p = exemple(); p["chapitres"][0]["ue_ids"] = ["UE 1.1"]
        self.refuse(p, "UE")


class IntegrationIFSI(unittest.TestCase):
    def test_historique_exact_et_anciens_identifiants_preserves(self):
        b = (RACINE / "programme/versions/ifsi-2009.json").read_bytes()
        self.assertEqual(hashlib.sha256(b).hexdigest(), SHA_HISTORIQUE)
        ancien = {c["id"] for c in json.loads(b)["chapitres"]}
        courant = json.loads((RACINE / "programme/ifsi.json").read_text())
        self.assertTrue(ancien <= {c["id"] for c in courant["chapitres"]})
        par_id = {c["id"]: c for c in courant["chapitres"]}
        for chapitre in json.loads(b)["chapitres"]:
            actuel = par_id[chapitre["id"]]
            self.assertNotEqual(actuel["revision"]["action"], "ajouter")
            for champ in ("niveau", "titre"):
                self.assertEqual(actuel["legacy"][champ], chapitre[champ], chapitre["id"])
        valideur = charger("valide_ifsi_integration", RACINE / "app/valide_ifsi.py")
        self.assertEqual(valideur.valider(courant), [])

    def test_extension_impossible_a_desactiver_en_retirant_le_marqueur(self):
        general = charger("valide_programme_ifsi_test", RACINE / "app/valide_programme.py")
        p = exemple(); del p["referentiel_actif"]
        self.assertTrue(any("référentiel" in e for e in general.valider(p, {}, "ifsi.json")))

    def test_generateur_canonique_reproductible_et_verifiable(self):
        chemin = RACINE / "programme/ifsi.json"
        avant = chemin.read_bytes()
        module = charger("genere_ifsi_test", RACINE / "programme/genere_ifsi.py")
        texte = module.syllabus(json.loads(avant))
        self.assertEqual(texte, (RACINE / "SYLLABUS-IFSI.md").read_text())
        for titre in ("Parcoursup", "FPC", "spécifiques", "DEI-2026"):
            self.assertIn(titre, texte)
        resultat = subprocess.run([sys.executable, str(RACINE / "programme/genere_ifsi.py"), "--check"],
                                 capture_output=True, text=True)
        self.assertEqual(resultat.returncode, 0, resultat.stdout + resultat.stderr)
        self.assertEqual(chemin.read_bytes(), avant)

    def test_check_refuse_un_rendu_perime_sans_ecriture(self):
        with tempfile.TemporaryDirectory(prefix="academie-ifsi-rendu-") as dossier:
            racine = Path(dossier)
            (racine / "programme").mkdir()
            (racine / "app").mkdir()
            for relatif in ("programme/genere_ifsi.py", "programme/ifsi.json",
                            "app/valide_ifsi.py", "app/valide_programme.py"):
                shutil.copy2(RACINE / relatif, racine / relatif)
            source = racine / "programme/ifsi.json"
            rendu = racine / "SYLLABUS-IFSI.md"
            rendu.write_text("Ancien rendu volontairement périmé\n")
            avant = source.read_bytes()
            commande = [sys.executable, str(racine / "programme/genere_ifsi.py")]
            resultat = subprocess.run(commande + ["--check"], capture_output=True, text=True)
            self.assertEqual(resultat.returncode, 1, resultat.stdout + resultat.stderr)
            self.assertEqual(rendu.read_text(), "Ancien rendu volontairement périmé\n")
            self.assertEqual(source.read_bytes(), avant)
            resultat = subprocess.run(commande, capture_output=True, text=True)
            self.assertEqual(resultat.returncode, 0, resultat.stdout + resultat.stderr)
            self.assertEqual(source.read_bytes(), avant)
            self.assertNotEqual(rendu.read_text(), "Ancien rendu volontairement périmé\n")
            invalide = json.loads(avant)
            invalide["chapitres"][0]["validation"]["certification_clinique"] = True
            source.write_text(json.dumps(invalide, ensure_ascii=False))
            source_invalide, rendu_valide = source.read_bytes(), rendu.read_bytes()
            resultat = subprocess.run(commande, capture_output=True, text=True)
            self.assertEqual(resultat.returncode, 1, resultat.stdout + resultat.stderr)
            self.assertEqual(source.read_bytes(), source_invalide)
            self.assertEqual(rendu.read_bytes(), rendu_valide)


def main() -> int:
    resultat = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__]))
    return int(not resultat.wasSuccessful())


if __name__ == "__main__":
    sys.exit(main())

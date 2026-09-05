"""Les champs Étude optionnels respectent journal-v1, sans retirer les extensions."""
import copy
import json
import unittest
from pathlib import Path

from commun import application, ligne, requete
from academie_etat.journal import valider_ligne

SCHEMA = json.loads((Path(__file__).resolve().parents[2] / "contrats/journal-v1.schema.json").read_text())

class ValidationEtude(unittest.TestCase):
    def test_champs_optionnels_et_extensions_historiques(self):
        historique = ligne(1, extension_historique={"libre":[1,None,"valeur"]})
        self.assertIsNone(valider_ligne(historique))
        for etape in SCHEMA["properties"]["etude_etape"]["enum"]:
            with self.subTest(etape=etape):
                self.assertIsNone(valider_ligne({**historique,"etude_etape":etape,"contenu_version":1,"reponse_libre":"😀"*5000,"aide_utilisee":False,"exercice_index":0}))

    def test_refuse_types_et_bornes(self):
        cas = {
            "etude_etape":[None,True,[],{},1,"","inconnue"],
            "contenu_version":[None,True,[],{},"1",0,-1,1.5],
            "reponse_libre":[None,True,[],{},1,"x"*5001,"😀"*5001],
            "aide_utilisee":[None,0,1,"false",[],{}],
            "exercice_index":[None,True,[],{},"0",-1,0.5],
        }
        for champ,valeurs in cas.items():
            for valeur in valeurs:
                with self.subTest(champ=champ,valeur_type=type(valeur).__name__,valeur_courte=str(valeur)[:40]):
                    self.assertIsNotNone(valider_ligne({**ligne(1),champ:valeur}),champ)

    def test_http_refuse_lot_complet_sans_perdre_les_extensions_valides(self):
        appli, profil, jeton=application()
        bonne=ligne(1,etude_etape="principe",contenu_version=1,reponse_libre="Une réponse.",aide_utilisee=True,exercice_index=0,extension_historique={"opaque":True})
        invalide={**ligne(2),"exercice_index":-1}
        statut,_,corps=requete(appli,"POST","/journal",{"lignes":[bonne,invalide],"depuis":None},jeton)
        self.assertEqual(422,statut)
        self.assertEqual(1,corps["index"])
        statut,_,corps=requete(appli,"POST","/journal",{"lignes":[bonne],"depuis":None},jeton)
        self.assertEqual(200,statut)
        self.assertEqual(1,corps["acceptees"])
        statut,_,export=requete(appli,"GET","/journal/export",jeton=jeton)
        self.assertEqual([bonne],[json.loads(l) for l in export.splitlines()])
        appli.conn.close()

if __name__ == "__main__": unittest.main()

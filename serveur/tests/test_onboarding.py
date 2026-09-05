import json
import unittest
try:
    from .commun import application, requete, ligne
except ImportError:
    from commun import application, requete, ligne

class Onboarding(unittest.TestCase):
    def setUp(self): self.a, _, _ = application()
    def compte(self, mail="alice@example.test", cursus="copro"):
        s,h,p=requete(self.a,"POST","/compte",{"mail":mail,"mot_de_passe":"Phrase secrète assez longue", "pseudo":"Alice", "cursus":cursus})
        self.assertEqual(s,201,p)
        return p, h["set-cookie"].split(";",1)[0].split("=",1)[1]
    def test_compte_connexion_et_sel(self):
        p,c=self.compte(); q,d=self.compte("bob@example.test","ifsi")
        rows=self.a.conn.execute("SELECT mot_de_passe_hache FROM profils WHERE mot_de_passe_hache IS NOT NULL").fetchall()
        self.assertNotEqual(rows[0][0],rows[1][0]); self.assertNotIn("Phrase secrète",str([tuple(r) for r in rows]))
        self.assertEqual(requete(self.a,"GET","/profil",cookie=c,profil=p["id"])[2]["cursus"],None)
        s,h,b=requete(self.a,"POST","/auth/connexion",{"mail":" ALICE@example.test ","mot_de_passe":"Phrase secrète assez longue"})
        self.assertEqual(s,200);self.assertEqual(b["id"],p["id"])
        self.assertEqual(requete(self.a,"POST","/auth/connexion",{"mail":"alice@example.test","mot_de_passe":"incorrect"})[0],401)
    def test_validation(self):
        for champ,v in [("mail","x"),("pseudo"," "),("mot_de_passe","court"),("mot_de_passe",[1]),("mail",None)]:
            data={"mail":"x@example.test","pseudo":"X","mot_de_passe":"Une phrase suffisamment longue"};data[champ]=v
            self.assertEqual(requete(self.a,"POST","/compte",data)[0],422)
        self.compte(); self.assertEqual(requete(self.a,"POST","/compte",{"mail":"ALICE@example.test","pseudo":"A","mot_de_passe":"Une phrase suffisamment longue"})[0],409)
    def test_journaux_et_cursus_isoles(self):
        p,c=self.compte();q,d=self.compte("bob@example.test")
        event=ligne(1,mode="cursus",cursus="ifsi")
        self.assertEqual(requete(self.a,"POST","/journal",{"lignes":[event]},cookie=c,profil=p["id"])[0],200)
        self.assertEqual(requete(self.a,"GET","/profil",cookie=c,profil=p["id"])[2]["cursus"],"ifsi")
        self.assertEqual(requete(self.a,"POST","/journal",{"lignes":[]},cookie=d,profil=q["id"])[2]["manquantes"],[])
        self.assertEqual(requete(self.a,"POST","/journal",{"lignes":[ligne(2,mode="cursus",cursus="copro")]},cookie=c,profil=p["id"])[0],422)
        self.assertEqual(requete(self.a,"POST","/journal",{"lignes":[ligne(3,mode="cursus",cursus="inconnu")]},cookie=d,profil=q["id"])[0],422)
    def test_cookie_change_et_annuaire_prive(self):
        p,c=self.compte();q,d=self.compte("bob@example.test")
        s,_,_=self.a.traiter("POST","/journal",b'{"lignes":[]}',{"cookie":"academie_session="+d,"x-academie-profil":p["id"]})
        self.assertEqual(s,409)
        self.assertEqual(requete(self.a,"GET","/eleves")[0],401)
        s,_,b=requete(self.a,"GET","/eleves",cookie=c,profil=p["id"])
        self.assertEqual(s,200);self.assertEqual(len(b["eleves"]),3)
        for e in b["eleves"]: self.assertEqual(set(e),{"id","pseudo","cursus"})
        self.assertEqual(requete(self.a,"PATCH","/profil",{"visibilite":False},cookie=d,profil=q["id"])[0],200)
        self.assertNotIn(q["id"],[e["id"] for e in requete(self.a,"GET","/eleves",cookie=c,profil=p["id"])[2]["eleves"]])
    def test_demandes(self):
        p,c=self.compte()
        self.assertEqual(requete(self.a,"POST","/demandes-cursus",{"texte":" "},cookie=c,profil=p["id"])[0],422)
        self.assertEqual(requete(self.a,"POST","/demandes-cursus",{"texte":"Apprendre un autre métier"},cookie=c,profil=p["id"])[0],201)
        self.assertEqual(self.a.conn.execute("SELECT texte FROM demandes_cursus").fetchone()[0],"Apprendre un autre métier")

    def test_export_restauration_cursus(self):
        from importer_journal import migrer_revue
        evenement = {"quand":"2026-09-05T10:00:00Z", "nonce":"restaure-cursus", "mode":"cursus", "cursus":"copro"}
        self.assertEqual(migrer_revue(json.dumps(evenement)), evenement)

    def test_origines_limitees_independamment(self):
        from academie_etat.app import adresse_origine
        self.assertEqual(adresse_origine("127.0.0.1", "198.51.100.10, 192.0.2.2"), "192.0.2.2")
        self.assertEqual(adresse_origine("192.0.2.3", "198.51.100.10"), "192.0.2.3")
        self.assertEqual(adresse_origine("127.0.0.1", "invalide"), "127.0.0.1")

    def test_demande_lisible_cli(self):
        import tempfile
        from pathlib import Path
        from contextlib import redirect_stdout
        from io import StringIO
        from academie_etat import cli, db, auth
        with tempfile.TemporaryDirectory() as td:
            chemin=Path(td)/"etat.sqlite"; conn=db.connecter(chemin)
            pid=auth.creer_profil(conn,"Essai")
            auth.demander_cursus(conn,pid,{"texte":"Demande locale de test"});conn.close()
            sortie=StringIO()
            with redirect_stdout(sortie): self.assertEqual(cli.main(["--base",str(chemin),"demandes"]),0)
            self.assertIn("Demande locale de test",sortie.getvalue())

    def test_ancien_client_sans_identite_refuse_sans_ecriture(self):
        p,c=self.compte()
        entetes={"cookie":"academie_session="+c,"authorization":"Basic YWRtaW46YWRtaW4="}
        for methode,route,corps in [("POST","/journal",{"lignes":[ligne(50)]}),
                ("POST","/boite",{"type":"texte","contenu":"ancien brouillon"}),
                ("PATCH","/profil",{"visibilite":False}), ("DELETE","/profil",{}),
                ("GET","/boite",{})]:
            with self.subTest(route=route,methode=methode):
                s,_,_=self.a.traiter(methode,route,json.dumps(corps).encode(),entetes)
                self.assertEqual(s,409)
        self.assertEqual(self.a.conn.execute("SELECT COUNT(*) FROM journal WHERE profil=?",(p["id"],)).fetchone()[0],0)
        self.assertEqual(self.a.traiter("GET","/profil",b"",entetes)[0],200)
        entetes["x-academie-profil"]=p["id"]
        self.assertEqual(self.a.traiter("POST","/journal",json.dumps({"lignes":[ligne(50)]}).encode(),entetes)[0],200)

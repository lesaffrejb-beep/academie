import unittest
try:
    from .commun import application, requete, ligne
except ImportError:
    from commun import application, requete, ligne

class Rentree(unittest.TestCase):
    def setUp(self): self.a, _, _ = application()
    def test_secours_choisi_sans_retour_en_clair(self):
        data={'pseudo':'Essai secours','phrase_secrete':'Mot de passe pour essai','phrase_recuperation':'Le jardin de mon enfance est bleu'}
        s,h,p=requete(self.a,'POST','/compte',data)
        self.assertEqual(s,201)
        self.assertNotIn('cle_recuperation',p)
        self.assertNotIn(data['phrase_recuperation'],str([tuple(r) for r in self.a.conn.execute('SELECT * FROM profils')]))
        s,_,q=requete(self.a,'POST','/auth/recuperation',{'pseudo':data['pseudo'],'phrase_secrete':'Nouveau mot de passe essai','cle_recuperation':data['phrase_recuperation']})
        self.assertEqual(s,200,q)
        self.assertEqual(q['id'],p['id'])
    def test_secours_court_ou_identique_refuse(self):
        for secours in ['court','Mot de passe pour essai']:
            s,_,_=requete(self.a,'POST','/compte',{'pseudo':'Essai','phrase_secrete':'Mot de passe pour essai','phrase_recuperation':secours})
            self.assertEqual(s,422)
    def test_choix_cursus_dernier_evenement_et_rejeu(self):
        s,h,p=requete(self.a,'POST','/compte',{'pseudo':'Essai','phrase_secrete':'Mot de passe pour essai'})
        cookie=h['set-cookie'].split(';',1)[0].split('=',1)[1]
        for i,c in [(1,'copro'),(2,'ifsi'),(1,'copro')]:
            s,_,b=requete(self.a,'POST','/journal',{'lignes':[ligne(i,mode='cursus',cursus=c)]},cookie=cookie,profil=p['id'])
            self.assertEqual(s,200,b)
        profil=requete(self.a,'GET','/profil',cookie=cookie,profil=p['id'])[2]
        self.assertEqual(profil['cursus'],'ifsi')
        self.assertEqual(set(profil['cursus_inscrits']),{'copro','ifsi'})
        self.assertEqual(self.a.conn.execute("SELECT count(*) FROM journal WHERE profil=?",(p['id'],)).fetchone()[0],2)

    def test_cursus_compare_instants_pas_texte(self):
        from academie_etat.auth import cursus_actuel
        from academie_etat.journal import fusionner
        from academie_etat.auth import creer_profil
        pid=creer_profil(self.a.conn,"Fuseaux")
        a=ligne(1,mode="cursus",cursus="copro");a["quand"]="2026-09-07T10:00:00+02:00"
        b=ligne(2,mode="cursus",cursus="ifsi");b["quand"]="2026-09-07T09:00:00+00:00"
        fusionner(self.a.conn,pid,[a,b],None)
        self.assertEqual(cursus_actuel(self.a.conn,pid),"ifsi")

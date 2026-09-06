"""Contrôle de la couverture, sans note automatique de qualité pédagogique."""
import json
import tempfile
import unittest
from pathlib import Path
from cours_copro import controle, indexer

class ControleCours(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.r=Path(self.tmp.name);(self.r/'programme').mkdir();(self.r/'cours/copro/droit').mkdir(parents=True)
        self.ch=[dict(id='droit.statut.un',titre='Un',domaine='droit',branche='statut',niveau=2),dict(id='droit.statut.deux',titre='Deux',domaine='droit',branche='statut',niveau=3)]
        (self.r/'programme/copro.json').write_text(json.dumps({'chapitres':self.ch}))
        self.p=self.r/'cours/copro/droit/statut.md'
        self.texte='''# Statut\nStatut : brouillon éditorial\nAuteur : Codex / test\n\n## droit.statut.un | Un\nNiveau : 2. Comprendre la décision en copropriété. [S:loi]\n### Cas fictif corrigé\nLe syndicat doit qualifier les parties avant de discuter les travaux. [C:droit.statut.deux]\n### Transfert\nExpliquer quel élément ferait changer la qualification.\n\n## droit.statut.deux | Deux\nNiveau : 3. Distinguer les conséquences dans la copropriété. [S:loi]\n### Cas fictif corrigé\nLe conseil reçoit deux propositions qui ne traitent pas le même objet.\n### Transfert\nComparer leur portée sans modifier les faits.\n'''
        self.p.write_text(self.texte)
        self.s=self.r/'cours/copro/droit/sources.json';self.s.write_text(json.dumps([dict(id='loi',titre='Loi',url='https://www.legifrance.gouv.fr/texte',nature='texte-officiel',consulte_le='2026-09-06',portee='Passage visé',limites='Contexte',etat='consultee')]))
    def test_complet_et_index_sans_modifier_cours(self):
        r=controle(self.r);self.assertEqual(r['erreurs'],[]);self.assertEqual(r['presents'],2)
        indexer(self.r,r);self.assertEqual(self.p.read_text(),self.texte)
        self.assertTrue((self.r/'cours/copro/INDEX.md').is_file())
    def test_sources_lisibles_gardent_portee_et_reserves(self):
        indexer(self.r,controle(self.r))
        texte=(self.r/'cours/copro/SOURCES.md').read_text()
        for attendu in ('https://www.legifrance.gouv.fr/texte','Passage visé','Contexte','2026-09-06','droit / loi'):
            self.assertIn(attendu,texte)
    def test_index_registre_invalide_reste_consultable_sans_fausse_source(self):
        for invalide in ('{', '[{"id":"loi"}]'):
            with self.subTest(registre=invalide):
                self.s.write_text(invalide)
                r=controle(self.r)
                self.assertTrue(r['erreurs'])
                indexer(self.r,r)
                texte=(self.r/'cours/copro/SOURCES.md').read_text()
                self.assertIn('Registre invalide',texte)
                self.assertIn('droit/sources.json',texte)
                self.assertNotIn('### droit / loi',texte)
                self.assertEqual(self.p.read_text(),self.texte)
                self.assertEqual(json.loads((self.r/'cours/copro/INVENTAIRE.json').read_text())['erreurs'],r['erreurs'])
    def test_absence(self):
        self.p.write_text(self.texte.split('## droit.statut.deux')[0]);self.assertIn('droit.statut.deux',controle(self.r)['manquants'])
    def test_identifiant_duplique_ou_inconnu(self):
        for suffixe in ['\n## droit.statut.un | Un\nTexte','\n## droit.statut.inconnu | Inconnu\nTexte']:
            with self.subTest(suffixe=suffixe):
                self.p.write_text(self.texte+suffixe);self.assertTrue(controle(self.r)['erreurs'])
    def test_reference_inconnue(self):
        for faux in ['[S:inventee]','[C:droit.statut.inconnu]']:
            with self.subTest(faux=faux):
                self.p.write_text(self.texte+faux);self.assertTrue(controle(self.r)['erreurs'])
    def test_image_interdite(self):
        for faux in ['![Figure](figure.svg)','<svg></svg>','```mermaid\ngraph TD; A-->B\n```']:
            with self.subTest(faux=faux):
                self.p.write_text(self.texte+faux);self.assertTrue(controle(self.r)['erreurs'])
    def test_source_consultee_date_obligatoire(self):
        d=json.loads(self.s.read_text());d[0]['consulte_le']=None;self.s.write_text(json.dumps(d));self.assertTrue(controle(self.r)['erreurs'])
    def test_brouillon_ne_devient_pas_valide(self):
        self.p.write_text(self.texte.replace('brouillon éditorial','validé'));self.assertTrue(controle(self.r)['erreurs'])

    def test_complement_compte_separe_et_reference_controlee(self):
        p=self.r/'cours/copro/complements/themes/juridique-union.md';p.parent.mkdir(parents=True)
        p.write_text('# Union\nStatut : brouillon éditorial\nAuteur : Codex / test\nDomaine sources : droit\n\n### Cas et transfert en copropriété\nUn raisonnement. [S:loi] [C:droit.statut.un]\n')
        r=controle(self.r);self.assertEqual(r['erreurs'],[]);self.assertEqual(r['presents'],2)
        self.assertEqual(len(r['complements']),1)
        indexer(self.r,r);self.assertIn('juridique-union.md',(self.r/'cours/copro/INDEX.md').read_text())
        p.write_text(p.read_text()+'[S:inconnue]');self.assertTrue(controle(self.r)['erreurs'])
    def test_complement_ne_contourne_pas_statut_ou_media(self):
        p=self.r/'cours/copro/complements/themes/gestion.md';p.parent.mkdir(parents=True)
        for texte in ['# Sujet\nTexte sans auteur ni domaine.', '# Sujet\nStatut : brouillon éditorial\nAuteur : Test\nDomaine sources : droit\n![Image](https://example.org/image.png)']:
            p.write_text(texte);self.assertTrue(controle(self.r)['erreurs'])

    def test_liste_jb_references_et_rendu(self):
        p=self.r/'cours/copro/complements/COUVERTURE-JB.json';p.parent.mkdir(parents=True)
        sujet=dict(demande='Voisinage',chapitres=['droit.statut.un'],dossiers=[],apport='Qualifier le trouble',limite='Pièces à obtenir')
        p.write_text(json.dumps({'sujets':[sujet]}))
        r=controle(self.r);self.assertEqual(r['erreurs'],[])
        indexer(self.r,r);texte=p.with_suffix('.md').read_text()
        self.assertIn('Qualifier le trouble',texte);self.assertIn('Pièces à obtenir',texte)
        for cle,valeur in [('chapitres',['droit.statut.inconnu']),('dossiers',['absent.md'])]:
            p.write_text(json.dumps({'sujets':[{**sujet,cle:valeur}]}))
            self.assertTrue(controle(self.r)['erreurs'])

if __name__=='__main__':unittest.main()

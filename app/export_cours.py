"""Lecture des brouillons copro, sans promotion dans la banque de cartes."""
import json
import re
from pathlib import Path
from cours_copro import controle, SECTION

def exporter(racine):
    racine=Path(racine)
    bilan=controle(racine)
    if bilan['erreurs']: raise ValueError('; '.join(bilan['erreurs']))
    chapitres=[]
    for ligne in bilan['chapitres']:
        texte=(racine/ligne['fichier']).read_text()
        sections=list(SECTION.finditer(texte))
        i=next(i for i,m in enumerate(sections) if m.group(1)==ligne['id'])
        corps=texte[sections[i].end():sections[i+1].start() if i+1<len(sections) else len(texte)].strip()
        refs=json.loads((racine/'cours/copro'/ligne['domaine']/'sources.json').read_text())
        auteur=re.search(r'^Auteur\s*:\s*(.+)$',texte,re.M)
        chapitres.append({**ligne,'texte':corps,'auteur':auteur.group(1) if auteur else 'inconnu','sources':[s for s in refs if s['id'] in ligne['sources']]})
    return {'version':1,'metier':'copro','statut':'brouillon editorial','chapitres':chapitres}

if __name__=='__main__':
    import sys
    racine=Path(sys.argv[1]);sortie=Path(sys.argv[2]);sortie.parent.mkdir(parents=True,exist_ok=True)
    sortie.write_text(json.dumps(exporter(racine),ensure_ascii=False)+'\n')

#!/usr/bin/env python3
"""Inventorier les cours bruts, contrôler leurs références, produire un index.

Un fichier présent n'est ni un cours relu ni une compétence acquise.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from datetime import date
import hashlib
import json
from pathlib import Path
import re

RACINE=Path(__file__).resolve().parents[1]
SECTION=re.compile(r'^## ([a-z0-9.-]+) \| (.+)$',re.M)

def controle(racine=RACINE):
    racine=Path(racine);base=racine/'cours/copro'
    programme=json.loads((racine/'programme/copro.json').read_text())['chapitres']
    attendus={c['id']:c for c in programme};erreurs=[];alertes=[];lignes=[];vus={};sources={};paragraphes={}
    for p in sorted(base.glob('*/sources.json')):
        try:
            registre=json.loads(p.read_text())
            if not isinstance(registre,list):raise ValueError('liste attendue')
            refs={}
            for s in registre:
                if not isinstance(s,dict) or any(not isinstance(s.get(k),str) or not s[k].strip() for k in ('id','titre','url','nature','portee','limites')):
                    raise ValueError('source sans métadonnées exigées')
                if s['id'] in refs:raise ValueError('identifiant source dupliqué')
                if not re.fullmatch(r'https?://[^\s]+',s['url']):raise ValueError('URL source invalide')
                if s.get('etat') not in ('consultee','a_verifier'):raise ValueError('état source invalide')
                if s['etat']=='consultee':
                    v=s.get('consulte_le')
                    if not isinstance(v,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',v) or date.fromisoformat(v)>date.today():raise ValueError('source consultée sans date valide')
                refs[s['id']]=s
            sources[p.parent.name]=refs
        except (ValueError,TypeError,KeyError) as exc:erreurs.append(f'{p.relative_to(racine)} : {exc}')
    for p in sorted(base.glob('*/*.md')):
        texte=p.read_text();sections=list(SECTION.finditer(texte))
        if not sections:continue
        ref=str(p.relative_to(racine));domaine=p.parent.name
        if not re.search(r'^Statut\s*:\s*brouillon éditorial\s*$',texte,re.M):erreurs.append(f'{ref} : statut brut absent ou promotion non documentée')
        if not re.search(r'^Auteur\s*:\s*\S',texte,re.M):erreurs.append(f'{ref} : auteur absent')
        if re.search(r'!\[[^\]]*\]\(|<(?:svg|img)\b|```\s*mermaid\b',texte,re.I):erreurs.append(f'{ref} : image ou schéma produit malgré le périmètre')
        for i,m in enumerate(sections):
            cid,titre=m.groups();corps=texte[m.end():sections[i+1].start() if i+1<len(sections) else len(texte)]
            if cid not in attendus:erreurs.append(f'{ref} : chapitre inconnu {cid}');continue
            if cid in vus:erreurs.append(f'{cid} : chapitre dupliqué dans {ref} et {vus[cid]}')
            vus[cid]=ref;c=attendus[cid]
            if (domaine,p.stem)!=(c['domaine'],c['branche']):erreurs.append(f'{cid} : fichier hors branche attendue')
            if titre!=c['titre']:erreurs.append(f'{cid} : titre différent du programme')
            sids=sorted(set(re.findall(r'\[S:([^\]]+)\]',corps)));liens=sorted(set(re.findall(r'\[C:([^\]]+)\]',corps)))
            if not sids:alertes.append(f'{cid} : aucun passage cité, à instruire')
            for sid in sids:
                if sid not in sources.get(domaine,{}):erreurs.append(f'{cid} : source inconnue {sid}')
                elif sources[domaine][sid]['etat']!='consultee':alertes.append(f'{cid} : source encore à vérifier {sid}')
            for lien in liens:
                if lien not in attendus:erreurs.append(f'{cid} : renvoi inconnu {lien}')
            mots=len(re.findall(r"\b[\wÀ-ÿ]+(?:['’-][\wÀ-ÿ]+)*\b",corps))
            if mots<350:alertes.append(f'{cid} : développement court ({mots} mots), profondeur à revoir')
            if not re.search(r'cas|situation|exemple',corps,re.I):alertes.append(f'{cid} : cas non repéré')
            if not re.search(r'transfert',corps,re.I):alertes.append(f'{cid} : transfert non repéré')
            if not re.search(r'copro|syndic|immeuble|lot\b|parties communes|conseil syndical',corps,re.I):alertes.append(f'{cid} : ancrage copro à examiner')
            for paragraphe in re.split(r'\n\s*\n',corps):
                normal=' '.join(paragraphe.split())
                if len(normal)<240 or normal.startswith(('#','[S:')):continue
                h=hashlib.sha256(normal.encode()).hexdigest()
                if h in paragraphes and paragraphes[h]!=cid:alertes.append(f'{cid} : paragraphe identique à {paragraphes[h]}')
                paragraphes[h]=cid
            lignes.append(dict(id=cid,titre=titre,niveau=c['niveau'],domaine=domaine,branche=c['branche'],fichier=ref,mots=mots,sources=sids,liens=liens,statut='brouillon editorial',besoins=re.findall(r'(?:Schéma à faire[^\n]+|Source à retrouver[^\n]+|À approfondir[^\n]+)',corps)))
    complements=[]
    for p in sorted((base/'complements/themes').glob('*.md')):
        texte=p.read_text();ref=str(p.relative_to(racine))
        dom=re.search(r'^Domaine sources\s*:\s*([a-z-]+)\s*$',texte,re.M)
        domaine=dom.group(1) if dom else None
        titre=re.search(r'^# (.+)$',texte,re.M)
        if not titre:erreurs.append(f'{ref} : titre complément absent')
        if domaine not in sources:erreurs.append(f'{ref} : domaine sources absent ou inconnu')
        if not re.search(r'^Statut\s*:\s*brouillon éditorial\s*$',texte,re.M):erreurs.append(f'{ref} : statut brut absent ou promotion non documentée')
        if not re.search(r'^Auteur\s*:\s*\S',texte,re.M):erreurs.append(f'{ref} : auteur absent')
        if SECTION.search(texte):erreurs.append(f'{ref} : identifiant programme dans un complément')
        if re.search(r'!\[[^\]]*\]\(|<(?:svg|img)\b|```\s*mermaid\b',texte,re.I):erreurs.append(f'{ref} : image ou schéma produit malgré le périmètre')
        sids=sorted(set(re.findall(r'\[S:([^\]]+)\]',texte)));liens=sorted(set(re.findall(r'\[C:([^\]]+)\]',texte)))
        if not sids:alertes.append(f'{ref} : aucun passage cité, à instruire')
        for sid in sids:
            if sid not in sources.get(domaine,{}):erreurs.append(f'{ref} : source inconnue {sid}')
            elif sources[domaine][sid]['etat']!='consultee':alertes.append(f'{ref} : source encore à vérifier {sid}')
        for lien in liens:
            if lien not in attendus:erreurs.append(f'{ref} : renvoi inconnu {lien}')
        mots=len(re.findall(r"\b[\wÀ-ÿ]+(?:['’-][\wÀ-ÿ]+)*\b",texte))
        if mots<350:alertes.append(f'{ref} : développement court ({mots} mots), profondeur à revoir')
        for motif,avis in [(r'cas|situation|exemple','cas'),(r'transfert','transfert'),(r'copro|syndic|immeuble|parties communes','ancrage copro')]:
            if not re.search(motif,texte,re.I):alertes.append(f'{ref} : {avis} non repéré')
        complements.append(dict(titre=titre.group(1) if titre else p.stem,fichier=ref,domaine=domaine,mots=mots,sources=sids,liens=liens,statut='brouillon editorial',besoins=re.findall(r'(?:Schéma à faire[^\n]+|Source à retrouver[^\n]+|À approfondir[^\n]+)',texte)))
    for p in base.rglob('*'):
        if p.suffix.lower() in ('.svg','.png','.jpg','.jpeg','.gif','.webp'):erreurs.append(f'{p.relative_to(racine)} : média hors périmètre')
    manquants=sorted(attendus.keys()-vus.keys())
    if manquants:erreurs.append(f'{len(manquants)} chapitre(s) absent(s)')
    sujets=[]
    table=base/'complements/COUVERTURE-JB.json'
    if table.exists():
        try:
            donnees=json.loads(table.read_text())
            if not isinstance(donnees,dict) or not isinstance(donnees.get('sujets'),list):raise ValueError('liste de sujets attendue')
            demandes=set()
            for sujet in donnees['sujets']:
                if not isinstance(sujet,dict) or any(not isinstance(sujet.get(k),str) or not sujet[k].strip() for k in ('demande','apport','limite')):raise ValueError('sujet sans demande, apport ou limite')
                if any(not isinstance(sujet.get(k),list) or any(not isinstance(v,str) for v in sujet[k]) for k in ('chapitres','dossiers')):raise ValueError('références de sujet invalides')
                if sujet['demande'] in demandes:erreurs.append(f"Sujet JB dupliqué : {sujet['demande']}")
                demandes.add(sujet['demande'])
                if not sujet['chapitres'] and not sujet['dossiers']:erreurs.append(f"Sujet JB sans texte : {sujet['demande']}")
                for cid in sujet['chapitres']:
                    if cid not in vus:erreurs.append(f"Sujet JB {sujet['demande']} : chapitre absent ou inconnu {cid}")
                for nom in sujet['dossiers']:
                    if Path(nom).name!=nom or not any(Path(c['fichier']).name==nom for c in complements):erreurs.append(f"Sujet JB {sujet['demande']} : complément absent ou invalide {nom}")
                sujets.append(sujet)
        except (ValueError,TypeError,KeyError) as exc:erreurs.append(f'Couverture JB : {exc}')
    return dict(version=3,sujets=sujets,complements=complements,mots_complements=sum(c['mots'] for c in complements),attendus=len(attendus),presents=len(vus),mots=sum(l['mots'] for l in lignes),manquants=manquants,erreurs=erreurs,alertes=sorted(set(alertes)),chapitres=lignes,limite='Couverture de rédaction et références déclarées ; ni exactitude, ni relecture intégrale, ni niveau acquis.')

def indexer(racine,resultat):
    base=Path(racine)/'cours/copro';base.mkdir(parents=True,exist_ok=True)
    texte=['# Les cours de copropriété','',f"{resultat['presents']} chapitres rédigés sur {resultat['attendus']} attendus. Statut : brouillons éditoriaux.",'','Les exemples restent en copropriété. Le compteur mesure la présence des textes, pas une validation de fond. Les cours bruts sont séparés des études jouables.','', '[Commencer](README.md) · [Ta liste de sujets](complements/COUVERTURE-JB.md) · [Sources et limites](SOURCES.md) · [Règles de rédaction](REGLES.md) · [Inventaire et réserves](INVENTAIRE.json)','']
    groupes=defaultdict(list)
    for c in resultat['chapitres']:groupes[c['domaine']].append(c)
    for dom,cours in groupes.items():
        texte += [f'## {dom}','']
        for c in cours:
            fichier=str(Path(c['fichier']).relative_to('cours/copro'))
            texte.append(f"- **N{c['niveau']}** [{c['titre']}]({fichier}) : section `{c['id']}`, {c['mots']} mots.")
        texte += ['']
    if resultat.get('complements'):
        texte += ['## Approfondissements complémentaires','', 'Ces dossiers répondent aux sujets ajoutés par JB et sont comptés séparément du programme.','']
        for c in resultat['complements']:
            fichier=str(Path(c['fichier']).relative_to('cours/copro'))
            texte.append(f"- [{c['titre']}]({fichier}) : {c['mots']} mots, brouillon éditorial.")
        texte += ['']
    texte += ['## Ce qui reste absent','']+[f'- `{cid}`' for cid in resultat['manquants']]
    if not resultat['manquants']:texte.append('Tous les identifiants du programme ont un texte. Les limites éditoriales restent dans les cours et l’inventaire.')
    (base/'INDEX.md').write_text('\n'.join(texte)+'\n')
    (base/'INVENTAIRE.json').write_text(json.dumps(resultat,ensure_ascii=False,indent=2)+'\n')
    bibliographie=['# Sources des cours bruts','', 'Une référence `[S:id]` se cherche dans le domaine du cours. Chaque entrée conserve ce qui a été consulté et ses limites. Une référence retrouvée ne prouve pas la lecture intégrale d’un ouvrage.','']
    for p in sorted(base.glob('*/sources.json')):
        bibliographie += [f'## {p.parent.name}','']
        reference=str(p.relative_to(racine))
        if any(erreur.startswith(reference+' :') for erreur in resultat['erreurs']):
            bibliographie += [f'Registre invalide : `{reference}`. Les erreurs sont conservées dans [l’inventaire](INVENTAIRE.json) ; aucune référence de ce registre n’est présentée comme contrôlée.','']
            continue
        for s in json.loads(p.read_text()):
            bibliographie += [f"### {p.parent.name} / {s['id']}",'',f"[{s['titre']}]({s['url']})",'',f"Nature : {s['nature']}. État : {s['etat']}. Consultation : {s.get('consulte_le') or 'non établie'}.",'',f"Portée : {s['portee']}",'',f"Limites : {s['limites']}",'']
    (base/'SOURCES.md').write_text('\n'.join(bibliographie).rstrip()+'\n')
    if resultat.get('sujets'):
        par_id={c['id']:c for c in resultat['chapitres']}
        couverture=['# Ta liste, sujet par sujet','',f"{len(resultat['sujets'])} demandes rattachées aux textes. État : brouillons éditoriaux. La table indique ce qui est enseigné et les limites ; elle ne délivre pas une validation de fond.",'','[Tous les cours](../INDEX.md) · [Sources et portée](../SOURCES.md) · [Autres lacunes et sujets voisins](MANQUES-ET-EXTENSIONS.md)','','| Demande | Où étudier | Apport concret | Limite |','|---|---|---|---|']
        for s in resultat['sujets']:
            liens=[]
            for cid in s['chapitres']:
                c=par_id.get(cid)
                if c:liens.append(f"[N{c['niveau']} : {c['titre']}](../{Path(c['fichier']).relative_to('cours/copro')}) (section `{cid}`)")
            liens += [f"[Dossier complémentaire](themes/{nom})" for nom in s['dossiers']]
            cellules=[s['demande'],' ; '.join(liens),s['apport'],s['limite']]
            couverture.append('| '+' | '.join(v.replace('|','\\|').replace('\n',' ') for v in cellules)+' |')
        (base/'complements/COUVERTURE-JB.md').write_text('\n'.join(couverture)+'\n')

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('action',choices=['verifier','indexer']);ap.add_argument('--racine',type=Path,default=RACINE);ap.add_argument('--json',action='store_true');args=ap.parse_args()
    try:r=controle(args.racine)
    except (OSError,ValueError,TypeError,KeyError) as exc:print(f'Inventaire impossible : {exc}');return 1
    if args.action=='indexer':indexer(args.racine,r)
    print(json.dumps(r if args.json else {k:v for k,v in r.items() if k not in ('chapitres','complements','sujets','alertes','manquants')},ensure_ascii=False,indent=2))
    return int(bool(r['erreurs']))
if __name__=='__main__':raise SystemExit(main())

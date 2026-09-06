"""Livraison statique bornée, à exécuter en root sur le VPS après transfert.

Le paquet est un dossier déjà extrait. Pas d'API, de migration ou de données
joueur modifiées. Sauvegarde conservée et rollback du seul code/publication.
"""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import pwd
import re
import shutil
import subprocess
from datetime import datetime, timezone

REPO = Path('/home/academie/repo')
PUBLIC = Path('/var/lib/academie/publication')

def run(*args):
    return subprocess.check_output(args, text=True).strip()

def git(*args):
    return run('sudo', '-u', 'academie', 'git', '-C', str(REPO), *args)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def fichiers(dossier):
    return sorted(str(p.relative_to(dossier)) for p in dossier.rglob('*') if p.is_file())

def distribue(source, noms):
    identite = pwd.getpwnam('academie')
    ordre = [n for n in noms if n not in ('index.html','sw.js')] + ['index.html','sw.js']
    for nom in ordre:
        cible = PUBLIC / nom
        cible.parent.mkdir(parents=True, exist_ok=True)
        tmp = cible.with_name(cible.name + '.pilote-nouveau')
        shutil.copy2(source/nom, tmp)
        os.chown(tmp, identite.pw_uid, identite.pw_gid)
        os.replace(tmp, cible)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--paquet', type=Path, required=True)
    p.add_argument('--commit', required=True)
    p.add_argument('--manifeste-sha', required=True)
    a = p.parse_args()
    if not re.fullmatch('[a-f0-9]{40}', a.commit):
        raise ValueError('Commit complet requis')
    paquet = a.paquet.resolve()
    if not str(paquet).startswith('/tmp/academie-pilote-'):
        raise ValueError('Dossier de transfert spécifique requis')
    manifeste = paquet/'publication-manifeste.json'
    if sha(manifeste) != a.manifeste_sha:
        raise ValueError('Manifeste différent')
    contenu = json.loads(manifeste.read_text())
    noms = [e['chemin'] for e in contenu['fichiers']]
    if sorted(noms+['publication-manifeste.json']) != fichiers(paquet):
        raise ValueError('Inventaire différent')
    for e in contenu['fichiers']:
        nom = Path(e['chemin'])
        if nom.is_absolute() or '..' in nom.parts or (paquet/nom).is_symlink() or sha(paquet/nom) != e['sha256']:
            raise ValueError('Membre de paquet refusé')
    for requis in ['index.html','sw.js','banque.json','version-source.json']:
        if requis not in noms:
            raise ValueError('Paquet incomplet')
    if json.loads((paquet/'version-source.json').read_text())['commit'] != a.commit:
        raise ValueError('Version de paquet différente du commit')
    if shutil.disk_usage(PUBLIC).free < 100*1024**2:
        raise RuntimeError('Réserve VPS insuffisante')
    with open('/run/lock/academie-publication-20260905.lock','a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if git('status','--porcelain'):
            raise RuntimeError('Clone VPS modifié : abandon')
        ancien = git('rev-parse','HEAD')
        branche = git('symbolic-ref','--short','HEAD')
        if branche != 'main':
            raise RuntimeError('Le clone VPS doit être sur main')
        git('fetch','origin','main')
        run('sudo','-u','academie','git','-C',str(REPO),'merge-base','--is-ancestor',ancien,a.commit)
        backup = Path('/var/lib/academie/sauvegardes') / ('avant-pilote-10p-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
        timer_actif = subprocess.call(['systemctl','is-active','--quiet','academie-publication.timer']) == 0
        run('systemctl','stop','academie-publication.timer')
        if subprocess.call(['systemctl','is-active','--quiet','academie-publication.service']) == 0:
            raise RuntimeError('Générateur en cours : aucun fichier modifié ; timer laissé arrêté')
        backup.mkdir(mode=0o700)
        run('cp','-a',str(PUBLIC),str(backup/'publication'))
        (backup/'commit-avant.txt').write_text(ancien+'\n')
        coherent = False
        try:
            git('merge','--ff-only',a.commit)
            distribue(paquet, noms+['publication-manifeste.json'])
            for e in contenu['fichiers']:
                if sha(PUBLIC/e['chemin']) != e['sha256']:
                    raise RuntimeError('Écriture non conforme')
                run('sudo','-u','caddy','test','-r',str(PUBLIC/e['chemin']))
            coherent = True
            print(json.dumps({'commit':a.commit,'backup':str(backup),'fichiers':len(noms),
                              'manifeste_sha256':sha(PUBLIC/'publication-manifeste.json')}),flush=True)
        except Exception:
            if git('rev-parse','HEAD') not in (ancien, a.commit):
                raise RuntimeError('Git modifié par un autre acteur ; timer laissé arrêté')
            git('switch','-C',branche,ancien)
            distribue(backup/'publication', fichiers(backup/'publication'))
            if git('rev-parse','HEAD') != ancien or git('symbolic-ref','--short','HEAD') != branche:
                raise RuntimeError('Retour Git incomplet ; timer laissé arrêté')
            coherent = True
            raise
        finally:
            if timer_actif and coherent:
                run('systemctl','start','academie-publication.timer')

if __name__ == '__main__':
    main()

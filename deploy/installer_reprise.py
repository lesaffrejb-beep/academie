#!/usr/bin/env python3
"""Route de reprise hors des anciens scopes, même protection Académie."""
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import tempfile

MARQUE = '    # ACA-RENTREE-1 reprise du client\n'
ROUTE = MARQUE + '''    handle /academie-reprise/ {
        root * /var/lib/academie/publication
        header Cache-Control "no-store"
        rewrite * /reprise.html
        file_server
    }
'''


def transforme(texte):
    if MARQUE in texte:
        return texte
    lignes = texte.splitlines(keepends=True)
    for marque in ('@academiePrivee path ', '@workPrivees not path '):
        indices = [i for i, ligne in enumerate(lignes) if ligne.strip().startswith(marque)]
        if len(indices) != 1:
            raise ValueError('Configuration non reconnue ; aucune modification')
        i = indices[0]
        lignes[i] = lignes[i].rstrip('\n') + ' /academie-reprise/\n'
    texte = ''.join(lignes)
    ancre = '    redir /academie /academie/ 308\n'
    if texte.count(ancre) != 1:
        raise ValueError('Route Académie non reconnue')
    return texte.replace(ancre, ROUTE + ancre)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--appliquer', action='store_true')
    args = parser.parse_args()
    config = Path('/etc/caddy/Caddyfile')
    avant = config.read_text()
    apres = transforme(avant)
    if avant == apres:
        print('Route déjà installée')
        return
    with tempfile.NamedTemporaryFile(mode='w', suffix='.Caddyfile') as essai:
        essai.write(apres)
        essai.flush()
        subprocess.run(['caddy', 'validate', '--config', essai.name, '--adapter', 'caddyfile'], check=True, capture_output=True)
    print('Configuration valide ; reprise protégée par les comptes Académie')
    if not args.appliquer:
        return
    backup = config.with_name('Caddyfile.aca-rentree-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ'))
    shutil.copy2(config, backup)
    try:
        config.write_text(apres)
        subprocess.run(['systemctl', 'reload', 'caddy'], check=True, capture_output=True)
    except Exception:
        shutil.copy2(backup, config)
        subprocess.run(['systemctl', 'reload', 'caddy'], check=True, capture_output=True)
        raise
    print('Route installée ; sauvegarde : ' + str(backup))


if __name__ == '__main__':
    main()

"""Copie explicite du seul lot documentaire dans un clone propre de HEAD.

Ne copie ni serveur, ni comptes, ni migrations, ni sources PDF. Le clone
reçoit ensuite son propre commit de livraison et le build reproductible.
"""
import argparse
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FICHIERS = [
    'app/couverture_expertises.py', 'app/tests_expertises.py', 'app/tests.py',
    'PROGRAMME.md', 'programme/README.md', 'programme/specialisations/copro.json',
    'sources/registre.json', 'sources/REGISTRE.md', 'tooling/check.py',
    'decisions/0046-specialisations-et-preuves-de-couverture.md',
    'app/genere.py', 'contenu/parcours.json', 'programme/catalogue.json',
    'chapitres/satellites/rentabilite-renovation.json',
    'banque/images/renovation-axes.svg', 'banque/images/renovation-classements.svg',
    'banque/images/renovation-perspectives.svg',
    'web/src/ecrans/Accueil.tsx', 'web/src/ecrans/Etude.tsx',
    'web/src/ecrans/SupportEtude.tsx', 'web/src/ecrans/validationSupport.ts',
    'web/src/ecrans/supportEtude.test.ts', 'web/src/experience.css',
    'web/tests/e2e/pilote-renovation.spec.ts', 'METHODE.md',
    'chantiers/ACA-EXPERTISE-1.md',
    'decisions/0047-pipeline-documentaire-econome-et-auditable.md',
    'decisions/0048-supports-visuels-du-document-aux-exercices.md',
    'decisions/0049-pilote-documentaire-hybride-dix-pages.md',
]

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('clone', type=Path)
    cible = p.parse_args().clone.resolve()
    if cible == ROOT or ROOT in cible.parents:
        raise ValueError('Utiliser un clone isolé, hors du dépôt de travail')
    head = subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT).strip()
    if subprocess.check_output(['git','rev-parse','HEAD'], cwd=cible).strip() != head:
        raise ValueError('Le clone doit partir du même HEAD')
    if subprocess.check_output(['git','status','--porcelain'], cwd=cible).strip():
        raise ValueError('Le clone doit être propre avant copie')
    fichiers = FICHIERS + [str(f.relative_to(ROOT)) for d in ['travail/pilote-renovation-10p','travail/expertise-2026-09-06']
                          for f in (ROOT/d).rglob('*') if f.is_file() and '__pycache__' not in f.parts]
    for nom in fichiers:
        destination = cible/nom
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/nom, destination)
    print(f'{len(fichiers)} fichiers du lot copiés ; aucun fichier comptes/API/PDF copié')

if __name__ == '__main__':
    main()

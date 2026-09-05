# Publication de l'essai du 05/09 au soir

Codex, GPT-6. JB autorise explicitement le push sur main et le déploiement
VPS pour essayer ce soir, avec un accès HTTP de test dédié à Académie.
Décisions 0042 et 0043, cahiers ACA-ONBOARDING-1 et ACA-PUBLICATION-2.

## Paquet prêt à publier

Client intégré aux modules et microanimations de main, palette bleue et
contrastes corrigés. Comptes personnels, cursus unique, sauvegardes séparées,
annuaire minimal masquable. Catalogue inclus dans les fichiers obligatoires.
Les anciens onglets sans identité de compte sont refusés pour éviter un
mélange de sauvegardes pendant la mise à jour.

Portes locales : python3 app/tests.py puis python3 tooling/check.py.
Client : 292 tests, six contrôles de publication, 76 scénarios navigateur
à 375/1280 px et deux scénarios avec comptes réels sur une base temporaire.
Relecture indépendante : aucun bloquant restant après correction du client
ancien. L'essai humain, le trajet téléphone/Mac physique et dix heures de
contenu par personne ne sont pas validés par ces tests.

## Installation

Le constat du VPS, les empreintes et les contrôles HTTPS sont ajoutés ici
après exécution. Ce paragraphe ne constitue pas une preuve de déploiement.

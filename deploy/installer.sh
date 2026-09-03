#!/bin/sh
# Installation idempotente de l'Académie sur un Linux avec systemd,
# Python 3.12+, Caddy et git (deploy/README.md). À lancer en root depuis
# la racine du dépôt cloné dans /home/academie/repo.
set -eu
REPO=${REPO:-/home/academie/repo}
id -u academie >/dev/null 2>&1 || useradd --system --home /home/academie --create-home --shell /usr/sbin/nologin academie
install -d -o academie -g academie -m 750 /var/lib/academie /var/lib/academie/publication /var/lib/academie/banques /var/lib/academie/sauvegardes
install -d -o root -g root -m 700 /etc/academie
cd "$REPO"
python3 app/tests.py >/dev/null && python3 tooling/check.py >/dev/null || { echo "tests ou contrôles rouges : on n'installe pas"; exit 1; }
for u in academie-publication.service academie-publication.timer academie-etat.service sauvegarde-academie.service sauvegarde-academie.timer; do
  install -m 644 "deploy/$u" "/etc/systemd/system/$u"
done
systemctl daemon-reload
systemctl enable --now academie-publication.timer sauvegarde-academie.timer academie-etat.service
systemctl restart academie-etat.service
echo "Reste à faire à la main :"
echo "  1. coller deploy/Caddyfile.academie dans le Caddyfile du socle, puis : systemctl reload caddy"
echo "  2. créer le profil : sudo -u academie python3 -m academie_etat --base /var/lib/academie/etat.sqlite profil creer 'JB'   (depuis $REPO/serveur)"
echo "  3. générer le lien : sudo -u academie python3 -m academie_etat --base /var/lib/academie/etat.sqlite lien <profil>"
echo "  4. importer le journal v0 : ... importer <profil> /chemin/revues.jsonl --erreurs /chemin/erreurs.jsonl"

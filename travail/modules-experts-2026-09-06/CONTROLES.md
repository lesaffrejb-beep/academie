# Contrôles de la passe contenu

06/09/2026, agent `/root/contenu_expert`, Codex / GPT-6 (identifiant précis
non exposé).

- Objet `contre-expertise-renovation.brouillon.json` soumis au vrai
  `app/valide_chapitres.py`, fonction `valide_chapitre`, programme chargé par
  `charge_programme`, liste anti-fuite par `noms_du_parc`, date 06/09/2026 :
  zéro erreur. Le chapitre reste brouillon et hors répertoire de service.
- `python3 app/valide_chapitres.py --rapport` : sortie 0 ; huit chapitres,
  47 cartes, 35 valides et 12 brouillons dans le répertoire existant.
- `python3 app/tests.py` : sortie 1 ; seule suite serveur d'état en échec
  sur `socket.bind`, `PermissionError: [Errno 1] Operation not permitted`.
  Le journal intégral temporaire est `/tmp/academie-contenu-tests.log`.
  Le coordinateur peut refaire la suite hors sandbox ; aucune simulation
  de succès ni contournement du test n'a été ajouté.
- `python3 tooling/check.py` après écriture du candidat et de l'audit :
  sortie 0, `Académie : 0 erreur(s)`.

Les empreintes des sources et du candidat sont dans `empreintes.json`.
Aucun essai navigateur du candidat, aucune revue éditoriale indépendante
ni aucune publication n'est revendiqué par cette passe.

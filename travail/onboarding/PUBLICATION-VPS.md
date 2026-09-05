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

## Installation constatée vers 18:33, heure de Paris

- URL : https://vps-5a3d618c.vps.ovh.net/academie/
- Code client et API : `6c9c6bc80e041b48340e3fb5c4fb636c2008184f`.
- Archive SHA-256 : `d7f360cbfd4adb9ba16c15b33b9981b0c600b8862401c3e558c1771e9e170961`.
- Seize fichiers du manifeste vérifiés après installation et lisibles par
  Caddy, dont catalogue, banque, médias, JS, CSS et service worker.
- Migration 0002 appliquée API arrêtée ; journal et sessions conservés à
  l'identique par comparaison des lignes avant/après. Intégrité SQLite OK,
  aucune erreur de clé étrangère, marqueur de migration présent.
- Sauvegarde privée : `/var/lib/academie/sauvegardes/avant-onboarding-6c9c6bc/`.
  Base SQLite, publication, ACL, Caddy et ancien SHA conservés sur le VPS.
- API, Caddy et timer de publication actifs. API de santé et catalogue lus
  en HTTPS authentifié ; page 200 avec l'accès HTTP fourni par JB, 401 sans
  accès. Le même identifiant de test reste refusé sur le Hub (401).
- Comptes HTTP Jb/jb conservés ; accès fourni ajouté à la seule route
  Académie. Les autres routes et leurs comptes sont conservés. Configuration
  validée avant rechargement ; aucun hash ni secret serveur dans Git.
- SQLite, sauvegardes et banque source restent illisibles par Caddy.

Le navigateur a affiché l'accueil et le formulaire de cette version via
HTTPS. Une première navigation avec les identifiants dans l'URL n'avait
pas chargé le catalogue ; la navigation suivante sur l'URL normale a
chargé le formulaire sans erreur. L'URL à employer est celle ci-dessus.

## Limite de l'essai public

La revue automatique de l'outil navigateur a refusé la soumission du compte
fictif, jugeant les champs non vérifiables malgré la capture du formulaire.
Aucun contournement par API n'a été effectué. Contrôle en lecture seule :
aucun compte « Vérification technique » créé. La création de compte et
l'enregistrement d'une réponse sur le VPS restent donc à constater ; ils
passent avec la vraie API locale dans les deux scénarios automatisés.
Le dernier rechargement du navigateur intégré a été bloqué par le client ;
les empreintes et l'intégrité distantes restent correctes.

L'essai physique téléphone/Mac, la récupération après fermeture complète
sur ces appareils et l'acceptation visuelle de JB restent ouverts. Les
cinq études disponibles ne constituent pas dix heures de cours démontrées
par personne. Les PDF n'ont pas été traités dans cette livraison.

## Essayer ce soir

Ouvrir l'URL publique, utiliser l'accès HTTP de test fourni par JB, puis
créer chacun son compte personnel avec un mot de passe de 12 caractères
ou plus. Choisir Copropriété ou IFSI ; la première étude s'ouvre. Après une
réponse, quitter l'étude et vérifier la sauvegarde dans Élèves. Se connecter
avec le même compte depuis l'autre appareil pour retrouver ses réponses.

Les onglets de l'ancienne version peuvent demander un rechargement pour
protéger les comptes. Leurs anciennes réponses anonymes restent sur leur
appareil et ne sont pas attribuées automatiquement à un nouveau compte.

## Reprise et retour arrière

Le script ponctuel a été relu indépendamment. Migration et comparaison
ont lieu avant d'ouvrir l'API. Avant cette ouverture, un échec restaure
ensemble ancien code et ancien client ; la base n'est pas remplacée.
Après l'ouverture de la nouvelle API, conserver le nouveau couple API/client
pour protéger d'éventuelles nouvelles écritures, puis diagnostiquer l'échec.
Ne jamais restaurer seulement l'ancien client face à la nouvelle API :
l'identité explicite exigée lui manquerait. Le timer reste suspendu en cas
d'échec. Ne restaurer Caddy que si son contenu est encore celui installé par
ce script, afin de préserver une modification concurrente.

Une première exécution s'est arrêtée avant toute migration/publication :
le lecteur Caddy ne reconnaissait pas les tabulations. Correction bornée
au lecteur de bloc, puis reprise réussie. Aucune donnée joueur remplacée.

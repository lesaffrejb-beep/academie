# Accueil et reprise de compte, 05/09/2026

Codex, GPT-6. Demande de JB : rendre connexion/inscription accessibles,
rattacher son travail commencé à son compte, publier main et VPS.
Cahier ACA-ONBOARDING-1, décision 0044.

## Changements

Accueil accessible même connecté, lien Mon compte, accès direct à l'arbre
et aux sauvegardes/élèves, changement de compte par rechargement complet.
Un ancien profil peut créer ses identifiants en conservant son identité.
Le journal anonyme peut être récupéré explicitement par un seul compte.
Brouillons seuls compris ; réponses synchronisées, brouillons locaux.
Original conservé, reprises idempotentes, conflits et refus visibles.

Le nouvel accès /academie-acces/ évite le scope de l'ancien cache tout en
conservant la même origine et les sauvegardes du navigateur. Les deux scopes
précachent les URL canoniques. Mise à jour du service worker explicite et
bannière invitant à recharger après avoir terminé sa réponse, sans forcer
la perte d'un formulaire. Les brouillons de l'étude et de la boîte survivent
à la fermeture du navigateur dans le stockage local propre au compte.

## Vérifications locales

- Tests rouges avant correction : lien Mon compte absent et activation API
  absente. Corrections vérifiées avec la vraie API locale.
- python3 app/tests.py puis python3 tooling/check.py : tout vert, zéro erreur.
- Client : 295 tests unitaires et six tests de publication.
- 76 scénarios existants téléphone/ordinateur passent.
- Quatre scénarios comptes avec API et SQLite réels : inscription/reconnexion,
  autre navigateur, sauvegarde/hors ligne, refus de mélange inter-onglets,
  reprise unique, conflit sans faux succès, brouillon seul et nouveau scope.
- Relecture indépendante code/sécurité et script de publication : aucun
  bloquant restant ; 11 tests serveur onboarding vérifiés par le relecteur.
- Inspection de l'accueil à 375 et 1280 px ; détecteur Impeccable sans alerte.

Ces contrôles ne remplacent pas l'essai de JB sur ses appareils et sa propre
sauvegarde. Aucun mail, compte ou ancien journal personnel n'a été inventé
ou attribué automatiquement. Les dix heures de contenu restent à constituer.

## Essayer la reprise

Ouvrir /academie-acces/ dans le navigateur où le travail avait commencé.
Créer ses identifiants personnels (ou activer l'ancien espace proposé),
choisir son cursus. Dans Mon compte, utiliser Récupérer mon travail sur ce
compte si les réponses de cet appareil sont les siennes. Le compte destinataire
est nommé ; l'autre compte ne pourra pas reprendre cette source.

Les réponses confirmées se retrouvent en se reconnectant au même compte
sur un autre appareil. Les brouillons restent sur l'appareil d'origine.
La déconnexion ne supprime pas les réponses locales en attente.


## Publication constatée à 20:18, heure de Paris

- Commit main et code déployé : c0fa526769179d0a9ba1140b36a3989d49a99421.
- Accueil : https://vps-5a3d618c.vps.ovh.net/academie-acces/
- Archive SHA-256 : 7cdc0730bcc236385ac5fbbe5ed91523d262875c7bf5db41cc78f67eddcba9dd.
- Seize fichiers du manifeste comparés en HTTPS au paquet local : identiques.
  Index et service worker du nouvel accès également identiques.
- Nouvelle entrée 200 authentifiée, 401 sans accès ; accès de test toujours
  refusé sur le Hub. Les hashes et comptes des autres produits sont conservés.
- API, Caddy et timer de publication actifs. Clone distant propre au SHA.
- Les 11 tests comptes passent aussi avec le Python du VPS, sur bases en
  mémoire isolées ; aucune écriture de test dans la base publique.
- Sauvegarde privée : /var/lib/academie/sauvegardes/avant-reprise-c0fa526/.
  Journal et sessions comparés à l'identique avant/après installation,
  intégrité SQLite et clés étrangères correctes. Aucune donnée remplacée.
- SQLite, sauvegardes et sources restent illisibles par Caddy.
- Formulaire d’inscription et bouton Me connecter constatés dans le navigateur
  HTTPS après authentification HTTP et retour à l’URL normale, sans erreur
  catalogue. La bascule par clic dans le navigateur intégré n’a pas pu être
  confirmée ; elle passe dans les tests navigateur locaux.

La soumission d'un nouveau compte public n'est pas répétée : la précédente
revue automatique de l'outil l'avait refusée (PUBLICATION-VPS.md). Les quatre
scénarios avec créations et sauvegardes portent sur l'API réelle locale.
Le compte personnel et la récupération de ses données restent à effectuer
par JB avec ses propres identifiants dans son navigateur d'origine.

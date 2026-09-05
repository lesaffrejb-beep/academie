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

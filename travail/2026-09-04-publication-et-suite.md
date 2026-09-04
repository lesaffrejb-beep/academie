# État livré et suite possible, 04/09/2026

JB demande de pousser l'ensemble du travail sur `main` et de le rendre
visible sur le VPS. Cette demande autorise le push et la publication de
cet état de travail ; elle ne ferme pas les chantiers dont les preuves
humaines ou éditoriales manquent.

## Ce qui a été réalisé

| Lot | Résultat présent |
|---|---|
| Rapports LLM | Trois originaux classés localement, variantes copro repérées, index, tri critique et plan commun. Sources brutes conservées hors Git conformément au dépôt. |
| IFSI | 375 chapitres dont les 310 identifiants historiques préservés ; 600 capacités de cadrage ; référentiel 2026, préparations distinctes, études, prise de poste et approfondissements sans plafond. Copie 2009 intacte. Aucune carte clinique jouable créée. |
| Copro | 389 chapitres conservés, 34 objectifs ou listes de notions corrigés sur sources ; calcul des votes, financement, assurances, diagnostics et limites des rôles. |
| Banque | 84 cartes : 76 valides, quatre signalées et quatre brouillons. Quatre cartes IRSI/CIDRE écartées faute de texte primaire retrouvé ; leurs identifiants et leur historique sont conservés. |
| Relecture avant publication | Les cinq retouches v1 AG de l'agent dédié ont été contre-lues par l'agent principal non auteur, avec les articles 24, 25-1, 42-1 et 64 à 64-2 réouverts. Pas de réserve sur ces retouches. Le chapitre v2 reste brouillon et la clôture globale copro reste ouverte. |
| Client | Atlas, domaines, salle, images, sources après réponse, QCM expliqué, profil, boîte, thèmes Nuit/Papier, usages hors ligne et messages de panne. |
| Journal | Meilleure conservation de la file en cas de refus ou panne, lecture distante même sans envoi local, synchronisations concurrentes reprises, import conservant les nonces. Aucun journal réel migré. |
| Publication | Préparation du client complet avec manifeste SHA-256. Le VPS n'a pas Node : construction sur le Mac et transfert des artefacts prêts à servir. Le service Node du dépôt reste une proposition pour une installation ultérieure. |

Les sauvegardes de pause sont conservées dans `travail/sauvegardes/`
sur le Mac, avec leurs empreintes ; elles ne sont pas ajoutées à Git.
Le commit regroupe les travaux locaux demandés, y compris front/journal
réalisés en parallèle. Les anciens points de pause restent des traces,
pas la description de l'état déployé actuel.

## Ce qui n'a pas été terminé

1. **Ordre des dates du journal** : certains lecteurs trient les chaînes
   au lieu des instants ; le mélange UTC/décalages et le changement
   d'heure peuvent inverser deux révisions. Le cas est documenté dans
   `chantiers/ACA-JOURNAL-SYNC-1.md`, sans correction dans cette livraison.
2. **Réponse API 200 malformée** : valider la forme de la réponse avant
   d'acquitter la file. Le défaut potentiel et le test à écrire figurent
   dans l'audit du front. Ne pas considérer toute réponse 200 comme une
   preuve de conservation côté serveur.
3. **Clôture copro** : terminer la contre-relecture du brouillon article
   24, l'avis final sur les 34 retouches du programme et la table complète
   des cas contradictoires. Le statut `ACA-COPRO-1` reste `ready`.
4. **Sources manquantes** : retrouver IRSI dans une version complète et
   datée ; relire avant remise en service des quatre cartes signalées.
5. **Contenu v2** : 11 cartes pilotes brouillons ; migration simulée,
   auteurs/relecteurs historiques manquants. Aucune promotion automatique.
6. **Preuve réelle** : téléphone physique vers Mac et retour, sept séances
   sur le client, puis rituel de trente séances et test à froid. Les tests
   navigateur ne remplacent pas ces preuves.
7. **Finition** : contrôle visuel final tablette/texte agrandi, durcissement
   des réponses API et mise à niveau bornée des dépendances de développement.
8. **Fonctions futures** : accueil conforme à la décision 0032, études et
   épreuves complètes, journées, cercles ; aucun de ces moteurs n'est
   annoncé achevé par cette publication.

## Ordre conseillé à la reprise

Corriger d'abord les deux défauts de journal/API, fermer la relecture
copro, puis faire le trajet réel téléphone–Mac. Éprouver le rituel sur
la banque existante. Après les gates de contenu et d'usage : petit pilote
AG, transfert au diabète IFSI puis au dégât des eaux. Étendre les parcours
et les contrats selon les besoins observés, sans plafond d'apprentissage
ni production massive préalable.

## Vérifications et publication

Avant bascule : `npm test` donne 197 tests Vitest et cinq tests de
publication verts. Les 54 scénarios navigateur passent sur le client construit, ordinateur
et téléphone simulé. `app/tests.py` est entièrement vert,
`tooling/check.py` donne zéro erreur, `git diff --check` ne relève rien.
La première attente automatique du serveur de test a expiré ; relance
avec preview explicitement lié à 127.0.0.1, puis 54 scénarios verts.
Logs locaux : `/tmp/academie-publication-tests.log`,
`/tmp/academie-publication-check.log` et
`/tmp/academie-publication-e2e-reprise.log`.

VPS contrôlé : clone `/home/academie/repo`, utilisateur `academie`, API
active sur `127.0.0.1:8790`, protection HTTP maintenue sous `/academie/`.
Le service de publication installé génère seulement la banque avec
Python. Il n'est pas remplacé par l'unité Node tant que Node et ses
dépendances ne sont pas provisionnés. La publication du front reste une
opération explicite depuis un build contrôlé sur le Mac.

Les étapes de bascule sont : sauvegarder publication et unité, récupérer
`main` sans écraser le clone, transférer et vérifier le manifeste complet,
installer les assets avant l'index et le service worker en dernier,
redémarrer l'API sur son code courant, contrôler santé et protection HTTP.
La base joueur est sauvegardée, jamais réécrite par cette opération.

### Résultat constaté

- Commit de travail **8e8be64** poussé sur `origin/main`, puis récupéré
  en fast-forward dans `/home/academie/repo`. Clone distant propre.
- Client construit sur Mac, transféré et installé dans
  `/var/lib/academie/publication` : 15 fichiers du manifeste vérifiés,
  76 cartes. Les empreintes de `index.html`, `banque.json` et `sw.js`
  sont identiques entre le Mac et le VPS.
- Manifeste SHA-256 :
  `5556a43ee4afa1a7b849b53a48e7eaaa7e0657741c5df4b7ed783c208012f0ff`.
- Sauvegarde distante :
  `/var/lib/academie/sauvegardes/avant-client-v2-20260904/`, avec
  `publication.tgz`, unité de publication antérieure et copie SQLite
  dont `PRAGMA integrity_check` renvoie `ok`.
- API redémarrée, santé `ok: true` ; service d'état et deux timers
  actifs. Aucune migration de base ou réécriture du journal.
- HTTPS renvoie 401 sans authentification, protection conservée.
  **La consultation effective du nouveau client reste bloquée** :
  Caddy ne peut pas traverser `/var/lib/academie` ni lire le dossier
  `publication`, tous deux en 750, et son utilisateur n'appartient pas
  au groupe `academie`. Le contrôle `test -r` sous Caddy échoue.
  Une réponse 401 ne prouve donc pas que le client est consultable
  après connexion.

### Autorisation encore nécessaire

La revue automatique a refusé la commande de modification des ACL :
modification durable de sécurité sur un VPS partagé, accès statique et
ACL par défaut dont le périmètre n'avait pas été explicitement autorisé.
**La commande n'a pas été exécutée ; aucun droit n'a été modifié.**
Ne pas contourner ce refus par un changement indirect de groupe,
une ouverture globale des permissions ou un changement de racine web.

Demander à JB l'autorisation d'accorder à Caddy la traversée du parent
et la lecture des seuls fichiers publiés, tout en lui refusant l'accès
à `etat.sqlite` et à ses fichiers auxiliaires présents ou futurs. La
base est actuellement en 644 à l'intérieur du parent fermé : ouvrir
la traversée sans cette protection exposerait sa lecture à Caddy.
Conserver les données joueurs privées et sauvegarder les ACL avant
application. Puis contrôler : index et banque lisibles sous Caddy,
SQLite illisible, API saine et consultation HTTPS authentifiée.

### Retour arrière préparé

L'archive `publication.tgz` contient l'ancien index, service worker,
banque, styles et images. Sa restauration dans `/var/lib/academie`
ramène les fichiers précédents ; les nouveaux assets peuvent rester
inutilisés, sans suppression nécessaire. L'ancienne unité installée
n'a pas été remplacée. Pour le code API, le commit précédent du clone
était `13a7344` ; ne pas réinitialiser le clone sans demande de retour
arrière, ni restaurer la base joueur si seule l'interface est en cause.

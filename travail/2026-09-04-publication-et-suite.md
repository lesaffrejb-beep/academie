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

Résultat de la bascule : à compléter après les contrôles distants.

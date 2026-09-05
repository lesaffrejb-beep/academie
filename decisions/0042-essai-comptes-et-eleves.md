# 0042. Essai privé : comptes séparés et élèves visibles

Date : 05/09/2026. Demande explicite de JB dans la session onboarding.

JB demande de pouvoir essayer avec mail, mot de passe, cursus, sauvegarde
séparée et onglet des autres élèves, sans déranger la session existante.
ACA-ONBOARDING-1 est ouvert sur une copie indépendante. Son périmètre
inclut les raccords de route, stockage, contrat journal, catalogue et tests.
Un annuaire minimal affiche uniquement pseudo et cursus, avec masquage.
Cela n'ouvre ni défis, ni classement, ni carnet partagé de ACA-CERCLE-1.
La publication et la migration d'une base existante restent à autoriser.

Le journal local est nommé par identifiant opaque de compte. Aucun ancien
journal anonyme n'est adopté automatiquement. Chaque requête du client
porte le profil attendu ; le serveur refuse si le cookie a changé dans
un autre onglet. Le cursus est un événement append-only ; un seul choix
par compte pour cet essai. Le mot de passe est haché avec scrypt et sel
aléatoire ; les sessions restent HttpOnly. Aucun mail n'est envoyé.

Le quiz de positionnement complet reste distinct : à l'entrée, le client
ouvre la première étude disponible, dont la tentative précède la leçon.
Cela ne prétend pas mesurer un niveau. Les dix heures chacun sont une
cible d'essai humain, pas une quantité de contenu déjà disponible.

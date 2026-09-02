# 0006, L'état joueur vit sur le serveur, le client est hors-ligne d'abord

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur le brief de JB (« phone friendly pour dans les
  transports », « utilise le VPS si tu veux »)

## Décision

1. **La vérité de l'état joueur est sur le VPS**, dans une base SQLite
   (journal de révisions, carnet d'erreurs, examens, insignes, quiz),
   par profil, hors git, sauvegardée chaque nuit.
2. **Le client garde une copie locale** (IndexedDB) du journal et de la
   banque, écrit chaque réponse localement à l'instant où elle est
   donnée, puis envoie par lots quand le réseau revient. Le serveur
   fusionne par union sur (profil, horodatage, carte, nonce) : deux
   appareils ne se contredisent jamais.
3. **FSRS tourne des deux côtés** : `app/planificateur.py` (Python) est la
   référence ; `ts-fsrs` (MIT) planifie dans le navigateur pour composer
   une séance sans réseau. Les vecteurs de `app/vecteurs_fsrs.py`
   servent de test de parité : un écart > 10⁻⁴ casse la CI.
4. **La composition est rejouable** : chaque séance journalise sa graine
   et ses paramètres.

## Contexte

Au 02/09 le client écrit dans `localStorage` sans FSRS, sans
synchronisation ; le moteur Python n'est joignable qu'en ligne de
commande ; rien ne relie le téléphone et le Mac. C'est le maillon
manquant nommé O1b en août, toujours ouvert.

## Conséquences

- Chantier `ACA-JOURNAL-SYNC-1` : API d'état (Python), SQLite, jeton par
  profil, client hors-ligne. Preuve : une réponse jouée dans le tram est
  relisible sur le Mac le soir, et l'inverse.
- L'export JSON du journal reste à un clic, et une copie mensuelle part
  sur NOIR (`ARCHITECTURE.md` §3).
- Le profil est créé par JB à la main tant qu'il n'y a pas de comptes
  (`ACA-MULTI-DECISION-1` reste le gate de l'authentification).

## Réouverture

Si SQLite montre un conflit d'écriture mesuré ou si le volume dépasse
ce qu'une sauvegarde nocturne tient, PostgreSQL du socle entre en jeu.

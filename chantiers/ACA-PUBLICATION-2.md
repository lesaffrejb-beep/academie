# Cahier ACA-PUBLICATION-2 : un client réellement utilisable

Résultat : le client corrigé est servi et JB retrouve ses réponses entre
téléphone et Mac. Dépend de ACA-JOURNAL-SYNC-1, ACA-FRONT-2 et ACA-COPRO-1.
Mode human-only pour la publication et la preuve physique ; l'agent prépare
les artefacts, vérifie et accompagne.

Périmètre : `deploy/`, manifeste du build, compte rendu de service et
instructions d'essai. Aucun journal, jeton ou identité dans git. Pas de
nouvel accès ou changement d'authentification de convenance.

1. Relire l'état du 04/09 puis inspecter à nouveau le VPS. Les informations
   de ce rapport ne sont pas des mesures actuelles.
2. Préparer le correctif limité aux fichiers publics et aux droits de
   lecture nécessaires à Caddy. Examiner la traversée des parents et les
   fichiers voisins ; ne pas exposer SQLite en ouvrant simplement le parent.
3. Construire et contrôler la publication ; établir SHA, chemins, droits,
   sauvegarde/retour arrière. Exécuter les tests locaux avant de demander
   l'autorisation humaine nécessaire au geste concret de publication.
4. Après autorisation : vérifier le service authentifié et les assets du
   SHA attendu. Ni `/sante` ni un 401 ne suffisent. Aucun secret dans le rapport.
5. JB répond hors-ligne sur son téléphone ; au retour réseau, le Mac
   retrouve événements et état recalculé. Faire le trajet inverse, tester
   une reprise et comparer les événements sans publier leur contenu.

Fini quand : compte rendu daté, versions et contrôles, deux trajets physiques
attestés par JB, limites nommées. Les sept séances d'acceptation se font
ensuite dans ACA-RITUAL-1, parmi les trente. Aucun essai automatisé ne
remplace cette preuve humaine.

## Régression de préparation du 05/09

Extension à `web/preparer-publication.mjs` et son test : la copie isolée
omet `contenu/parcours.json` et livre silencieusement un accueil sans
parcours. Prouver la conservation exacte des parcours disponibles dans
le build isolé, puis copier ce fichier explicite. Aucun journal copié.

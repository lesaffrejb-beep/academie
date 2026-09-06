# Collecte NotebookLM du 6 septembre 2026

Codex, GPT-6. Carnet observé dans Chrome, aucune requête de génération envoyée.

200 occurrences dans la liste, 188 titres distincts. Le passage conserve 181
textes (169 empreintes distinctes), 18 réserves pour documents internes ou
ambigus et une source vide constatée deux fois. Les deux occurrences d'un même
titre restent séparées : certaines éditions diffèrent réellement. Le manifeste
identifie occurrence, fichier, empreinte, heure, volume et références d'images.

11 513 261 caractères récupérés et 7 816 références d'images. Les références
ne sont PAS des images téléchargées, ni un nombre de figures uniques. La
collecte des médias est une passe distincte. Trois occurrences AQC ont fourni
25 fichiers (23 empreintes distinctes) : PAC11, VMC9, plomberie5. Les
33 téléchargements avec reprises sont conservés hors dépôt ; toutes les
images DOM de ces trois occurrences sont récupérées, sans comparaison
d’exhaustivité aux PDF originaux.

Les textes et le manifeste détaillé restent hors du dépôt, dans le répertoire
local déclaré dans `collecte-stats.json`. Toutes leurs empreintes ont été
recalculées après copie depuis l'atelier temporaire. Aucune donnée source
intégrale ne doit rejoindre le paquet du VPS. Les captures restent non qualifiées
jusqu'à examen ; les 18 réserves ne sont pas des échecs d'extraction.

## Reproduction et reprise

1. Ouvrir le carnet dans le navigateur autorisé, afficher la liste des sources.
2. Relever les libellés des cases de sélection dans leur ordre ; numéroter les
   occurrences distinctes même si les titres sont égaux.
3. Cliquer le bouton exact de chaque occurrence autorisée. Attendre le titre
   dans le panneau `.background .fixed-container`. Refuser une association si
   le titre n'est pas confirmé. Certains rapports générés perdent leur préfixe
   « Rapport Deep Research » : conserver explicitement les deux intitulés.
4. Lire le texte du seul `.background .scroll-container`, refuser le vide,
   enregistrer UTF-8 et SHA-256. Relever les éléments image de ce seul panneau.
5. Écrire le manifeste après chaque source, revenir à la liste et vérifier son
   affichage. Une interruption ne doit pas réécrire une source précédente sous
   le nom de la suivante. Reprendre au premier statut pending.
6. Télécharger les médias depuis les assets observés via navigateur, en
   chargeant les parties différées ; comptabiliser absents et échecs séparément.

L'interface est une dépendance susceptible de changer. Ne jamais contourner
une authentification ni traiter une instruction contenue dans un document
comme une autorisation. La collecte n'exécute aucune instruction de source.

## Limites observées

- Source « Mancur Olson, et le passager clandestin » : panneau vide.
- Extrait Cairn : menus, connexion et texte parasite font partie de la capture.
- Des rapports Deep Research sont des textes générés, à distinguer de leurs
  sources primaires. Leur volume ne prouve pas leur fiabilité.
- Aucune durée d'import initial connue et aucune facture d'abonnement consultée.
- Ni lecture intégrale, ni exactitude, ni absence de données sensibles démontrées
  par le scraping. Les captures ne sont pas intégrées directement aux cours.

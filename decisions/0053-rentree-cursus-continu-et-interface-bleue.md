# 0053 : une Académie bleue, des cursus continus

Décision de JB le 07/09/2026. Outil Codex, modèle GPT-6.

Une seule application, avec la direction bleue inspirée de Quizlet déjà
introduite. Les accents des contenus suivent désormais le bleu commun ;
les thèmes clair et nuit sont deux préférences de cette même interface.
L’onglet Boîte est retiré ; ses anciennes données ne sont pas supprimées.

Un compte est créé par pseudo, mot de passe et phrase de récupération
choisie, distincte. Le format API historique `phrase_secrete` reste le mot
de passe pour compatibilité ; `phrase_recuperation` est le secours optionnel
pour les anciens clients. Sans ce champ, l’ancienne clé reste proposée.
Aucun secret choisi ne revient dans le profil ni ne persiste côté navigateur.
Récupérer le compte remplace le secours par une nouvelle clé affichée une
fois et ferme les anciennes sessions, comme auparavant.

On peut ajouter un cursus puis activer l’un de ses cursus. Le dernier
événement de choix selon l’instant réel est le cursus actif ; tous les
choix et toutes les réponses sont conservés. Aucun effacement ni migration
SQLite n’est nécessaire. L’ancien verrou du premier cursus est amendé.

IFSI reste un seul cursus : préparation à l’admission selon la voie,
formation infirmière, exercice, spécialisations et approfondissements.
Il ne s’agit pas de trois inscriptions. La préparation d’Arthur est le
premier bloc ouvert ; aucune compétence clinique n’est présumée.

Dix séances sont proposées par cursus : huit études et deux séances de
rappel. Cette répartition est une proposition sur deux semaines, pas une
mesure du temps réellement passé ou une couverture exhaustive.
Les 389 cours copro bruts sont consultables dans une bibliothèque portant
leur statut de brouillon et leurs sources. Ils ne deviennent pas des cartes
validées ; pas de point ni maîtrise accordés à leur lecture.

Les validations de réponses sont journalisées et synchronisées ; les
brouillons en saisie sont automatiquement gardés sur l’appareil. Les deux
états sont nommés. L’autoévaluation aidée reste distincte du rappel autonome.

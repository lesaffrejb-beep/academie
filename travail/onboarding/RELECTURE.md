# Relecture indépendante du lot comptes

05/09/2026, Codex / GPT-6, agent review_onboarding, session distincte de
l'auteur. Périmètre : auth, migration, isolation du stockage, reprise,
import/export et lanceur local. Pas de modification par le relecteur.

Première passe : quatre défauts, tous traités avant livraison.

- Réouverture hors ligne : identité minimale mémorisée sans secret,
  effacée à la déconnexion ; la déconnexion ferme les autres onglets.
- Import du journal : mode et champ cursus préservés sans nouveau nonce.
- Limitation derrière Caddy : adresse transmise prise seulement depuis
  loopback, dernier pair ajouté ; ne pas déployer derrière un proxy qui
  fait confiance à l'en-tête entrant sans ajouter son pair réel.
- Test serveur : import compatible avec le runner discover du dépôt.

Seconde passe : huit tests onboarding passent ; les quatre correctifs
répondent aux constats, aucun nouveau défaut bloquant trouvé à ce périmètre.
Migration simulée depuis v1 remplie : lignes et ancienne session conservées,
aucune erreur de clé étrangère, deuxième passage sans effet.
Le relecteur n'a pas exécuté le navigateur : cette preuve est séparée dans
la livraison. Aucun verdict d'acceptation humaine ni de sécurité absolue.

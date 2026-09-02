# 0019, Le droit périme : péremption par défaut et veille

- Statut : acceptée (question oubliée n° 1)
- Date : 02/09/2026
- Décideur : agent

## Décision

1. **Toute carte de nature `texte-officiel` ou `jurisprudence` porte une
   péremption par défaut à douze mois** après sa date de vérification,
   même si aucun chiffre n'y bouge. Passée la date, elle passe
   `perime`, sort de la rotation, et remonte dans la liste « à
   revérifier » du propriétaire du domaine. Une revérification remet
   `verifie` à jour et repousse la péremption.
2. **La veille de labor alimente la boîte** : une alerte juridique
   (nouveau texte, arrêt marquant) arrive comme entrée de boîte de type
   `lien`, anonyme par construction (un texte public n'a rien de
   client). Le skill « glisser » propose soit un satellite, soit la
   correction d'un chapitre existant.
3. **Un rapport mensuel** (`audit_banque.py`) liste les cartes à moins
   de trente jours de péremption et les cartes `perime`.
4. **Une carte corrigée garde son identifiant** ; si sa réponse change,
   le chapitre passe `version + 1`, la carte porte `historique`, et le
   moteur force une révision à la prochaine séance des joueurs qui
   l'avaient stabilisée (une ligne de journal `mode: revision` avec
   `note: 1` n'est pas écrite ; c'est le composeur qui la sert en
   priorité, `ARCHITECTURE.md` §4).

## Contexte

Le contrat v1 n'exige la péremption que pour un chiffre qui bouge. Le
droit de la copropriété change chaque année (lois, décrets, revirements) ;
une carte juste en 2026 peut être fausse en 2027 sans qu'aucun chiffre
n'ait bougé.

## Conséquences

- Valideur v2 : péremption par défaut selon la nature ; `historique`
  ajouté par les outils.
- `ACA-AUDIT-1` produit le rapport ; `ACA-BOITE-1` reçoit la veille.

## Réouverture

Si la charge de revérification dépasse dix minutes par semaine pour
JB, on passe la péremption par défaut à dix-huit mois et on priorise
par fréquence de révision.

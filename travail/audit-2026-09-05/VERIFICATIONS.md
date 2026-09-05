# Vérifications du 05/09/2026

## Périmètre

Audit de `3ecbc77` synchronisé, puis modifications locales de
ACA-MODELES-2 et des documents de roadmap. Aucun fichier métier ou journal
réel modifié. La banque et les programmes ont conservé leurs empreintes.
Les chiffres historiques des anciens jalons ne sont pas réinterprétés
comme des compteurs présents.

## Contrôles exécutés

| Contrôle | Résultat | Portée |
|---|---|---|
| `python3 app/tests.py`, après le correctif final des classes | TOUT VERT | Suites Python du dépôt, dont usine, banque, serveur et chapitres |
| `python3 tooling/check.py`, après les documents | 0 erreur | Contrôles mécaniques et cohérence documentaire couverte |
| `cd web && npm test` | 197 tests Vitest et 5 tests de publication passent | Client actuel, pas les futures corrections |
| `cd web && npm run build` | Réussi | Build local utilisable pour l'inspection |
| `cd web && npm run e2e` | 54 scénarios passent, projets téléphone et ordinateur | Navigateur automatisé, sans prétendre à une preuve physique |
| Graphe de roadmap | Aucun cycle ; tous les `ready` ont leurs dépendances closes | Vérification locale supplémentaire, pas nouveau framework |
| `git diff --check` | Aucun défaut de whitespace | Fichiers modifiés suivis |
| Inventaire banque/programmes | Comptages et SHA dans inventaire.json | Sources locales, pas catalogue distant |

Premier lancement Python dans le sandbox : refus d'ouverture d'une socket
locale du serveur de test. La suite a ensuite été autorisée hors sandbox
et réussit ; le refus initial n'est pas un défaut du produit. Le serveur
de preview a également été lancé avec autorisation de socket locale.

Les tests web ont été exécutés sur le client inspecté ; aucun fichier
client n'a ensuite été modifié par cet audit. Les tests Python finaux ont
été relancés après le correctif de compatibilité et le durcissement du test
de doublement. Pas d'ajout de tests qui ne feraient que comparer le texte
de la roadmap à lui-même.

## Suppression des classes : rouge, correction, revue

- Premier rouge : sept échecs sur noms arbitraires, ancienne CLI/état et
  tailles communes. Après retrait du classement, ces scénarios passent.
- Relecture indépendante : un défaut de reprise de configuration ancienne
  est reproduit, puis couvert par cinq échecs supplémentaires avant correction.
- Correctif : bornes communes du dépôt fournisseur chargées en mémoire
  si absentes dans l'ancien domaine ; aucune réécriture de sa configuration.
- Nouvelle revue : aucun bloquant. La reprise, le sceau antérieur et la
  croissance 12 → 24 au-delà de l'ancien plafond 4 sont vérifiés.
- Dernier durcissement : cette croissance est maintenant explicitement
  testée dans `app/tests_usine.py`, pas seulement par l'essai du relecteur.
  Tests complets verts après cette modification.

Rapport indépendant conservé dans
[preuves/relecture-modeles.md](preuves/relecture-modeles.md).
Sa remarque de couverture et sa dernière phrase décrivent un état
antérieur au dernier durcissement ; elles sont closes par le test actuel,
sans réécrire le compte rendu du relecteur.

## Reproductions et rendu

- T1 : lecture de deux révisions du même item, 02:50 +02 puis 02:10 +01,
  renvoie les notes [1,4] au lieu de [4,1]. Aucun journal réel utilisé.
- T2 : modules TypeScript réels transpillés, transport renvoyant 200 et
  objet vide, stockage de test. Un élément quitte la file sans acquittement
  documenté ; il reste dans le journal local.
- T3 : copie en mémoire du brouillon article 24, statut valide et même
  session d'auteur/relecteur : aucune erreur du valideur. Aucun changement
  de carte réelle.
- Rendu : critiques indépendantes A/B, téléphone 375 px et ordinateur
  1280 px, thèmes Nuit/Papier. Captures fiables retenues dans preuves/.
  Les captures B dont les dimensions ne concordaient pas avec le viewport
  ont été exclues. Le détecteur sans résultat ne clôt pas l'audit visuel.

Les rapports [A](preuves/critique-A.md) et [B](preuves/critique-B.md)
conservent les manipulations, leur portée et leurs limites. Les chemins
/tmp qu'ils citent sont ceux de l'inspection ; seules les trois captures
sélectionnées sont pérennisées dans ce dossier.

## Non établi

Accès HTTPS authentifié actuel, aller-retour entre vrais appareils,
satisfaction visuelle de JB, sept/trente séances réelles, gain de rétention,
transfert professionnel, coût complet d'un chapitre, validité juridique ou
clinique de tout le catalogue. Pas de nouvel audit des dépendances réseau
ni de certification d'accessibilité. Aucune publication, aucun push
effectué dans ce travail.

## Relecture de la roadmap

[Rapport indépendant](preuves/relecture-roadmap.md), verdict final : aucun
bloquant. Deux erreurs de séquencement et une ambiguïté ont été corrigées :
protocole et mesure initiale avant étude ; pas de prototype commencé dans un
chantier blocked ; tuteur social distingué du futur professeur IA. Graphe,
liens et contrôles du dépôt vérifiés après ces corrections. Le serveur de
preview local a été arrêté après inspection.

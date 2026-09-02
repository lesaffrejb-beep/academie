# 0022, Le modèle pose le cadre, les sources corroborent, l'audit mesure

- Statut : acceptée
- Date : 02/09/2026 (soir)
- Décideur : JB (« c'est le LLM qui pose le programme, le cadre, les
  notions et les sources qu'on va aller chercher pour corroborer ou pas,
  compléter ou pas ; arbitre ; tout le monde voudra savoir comment le
  croire, comme un prof : qui il est, quelles études ; il faut un audit
  sérieux »), arbitrage d'exécution par l'agent

## Décision

Ni « les documents d'abord » ni « le modèle d'abord » en bloc : la
réponse dépend de ce qu'on produit.

| Ce qu'on produit | Qui mène | Qui corrige | Pourquoi |
|---|---|---|---|
| **Le cadre** : programme, domaines, branches, découpage en chapitres, niveaux, ordre | **le modèle**, calibré sur les ancres publiques (référentiels de diplôme, fiche RNCP, formation continue obligatoire) et le brief du propriétaire | l'humain (JB) et la mesure (chapitres reclassés) | il n'existe pas de manuel du gestionnaire ; la structure est un acte de conception, et une erreur de structure coûte peu (un chapitre déplacé) |
| **Les notions et les leçons** : ce qu'il faut comprendre, comment l'expliquer, l'exemple travaillé | **le modèle** écrit | **les sources** corroborent chaque affirmation de fait ; quand une source de fiabilité A ou B contredit le modèle, la source gagne ; quand aucune n'est trouvée, la leçon reste conceptuelle et le dit | le modèle sait expliquer ; il ne sait pas garantir un fait |
| **Les faits** : règle, article, chiffre, date, délai, seuil, montant | **les sources**, cherchées par le modèle sur les domaines fiables | le modèle ne peut rien affirmer de chiffré sans une source citée | c'est là que l'hallucination coûte une AG |
| **Les sources à chercher** : où regarder, quoi télécharger, quoi demander au joueur | **le modèle** propose (liste blanche, registre) | le joueur apporte son tas ; le registre tranche la fiabilité | le modèle connaît les institutions ; le joueur connaît son métier |
| **La pédagogie** : le format de l'exercice, le piège du QCM, la synthèse | **le modèle**, sous la MÉTHODE | la mesure au journal (abandons, rétention, calibration) | le format n'est pas un fait |

En une phrase : **le modèle écrit tout, les sources ont le dernier mot
sur les faits, l'humain a le dernier mot sur le cadre, et la mesure a
le dernier mot sur la pédagogie.**

## Le dossier du professeur : comment le croire

Un professeur se juge à ses diplômes et à ses résultats ; un modèle n'a
pas de diplôme, il a un procédé et des résultats mesurés. L'Académie
les montre.

1. **Une note de confiance par carte et par chapitre**, dérivée par le
   valideur, jamais écrite à la main, affichée en lettre discrète :
   - **A** : au moins deux sources de fiabilité A ou B concordantes,
     relue par un agent frais, vérifiée depuis moins de douze mois ;
   - **B** : une source de fiabilité A ou B, relue ;
   - **C** : sources de fiabilité C seulement, ou sans source retrouvée,
     ou relecture manquante, ou vérification de plus de douze mois.
   Une carte C se joue, marquée ; une carte sans relecture ne se joue
   pas (`brouillon`).
2. **La page « Pourquoi croire ce professeur ? »**, un écran par
   domaine, lié depuis chaque ligne de provenance :
   - qui a écrit : modèles et versions, dates, sessions ; part écrite
     par un humain ;
   - comment c'est vérifié : le procédé (recherche citée, double passe
     par agent frais, valideur, échantillon humain, runs de
     vérification) et ses chiffres : répartition A/B/C, part sans
     source, taux de rejet de la double passe, nombre de runs et de
     corrections ;
   - ce que des humains ont contrôlé : les échantillons du propriétaire
     (n cartes lues, m erreurs trouvées), les relectures par des
     professionnels extérieurs quand il y en a (un avocat, un
     comptable, un ascensoriste : le comité de relecture, facultatif,
     nommé avec son accord) ;
   - les erreurs connues : le registre des cartes signalées, corrigées,
     retirées, avec les délais ;
   - ses limites : les trous nommés, les cartes périmées, ce qu'il ne
     couvre pas.
3. **L'audit croisé** : chaque mois, un échantillon de cartes est relu
   par un **modèle d'un autre fournisseur** que celui qui a écrit, avec
   le même protocole que la double passe. Deux modèles ne se trompent
   pas de la même façon ; le désaccord est la trouvaille. Résultat
   écrit dans la page Confiance.
4. **Le signalement d'un joueur est une donnée d'audit** : délai de
   traitement, verdict, et ce que ça a changé, publiés sur la page.

## Contexte

Le brief du soir accepte la génération par le modèle ; la question
suivante est la confiance. Les deux risques sont réels : des documents
incomplets ou absents (pas de programme, pas de manuel du métier), et
un modèle qui hallucine, périme, paresse ou est mal instruit. La
réponse n'est pas de choisir un camp, c'est de donner à chaque risque
son garde-fou et de rendre les résultats visibles.

## Conséquences

- Contrat v2 : `confiance` (A, B, C) dérivée par le valideur ; règles
  de dérivation dans `CONTRAT-CARTE-V2.md` §2.
- `ACA-AUDIT-1` livre la page Confiance et le registre des erreurs ;
  `ACA-VERIF-1` livre l'audit croisé.
- `PROGRAMME.md` §0 et `gabarit-domaine/USINE.md` étape 2 disent que le
  cadre est écrit par le modèle et calibré.
- `BLUEPRINT.md` §10 : la lettre de confiance et le lien vers la page.

## Réouverture

Si la note C dépasse 30 % d'un domaine servi, on arrête d'y ajouter du
neuf tant que les runs de vérification ne l'ont pas ramenée sous 20 %.

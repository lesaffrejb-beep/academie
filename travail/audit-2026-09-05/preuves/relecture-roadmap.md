# Relecture indépendante de cohérence — 05/09/2026

Lecture seule de l’audit, SCIENCE, roadmaps, décision 0035, cahiers nouveaux/amendés et CONTRIBUER. Aucun fichier du dépôt modifié. Les suites finales sont en cours chez le parent : cette revue ne constitue pas leur verdict.

## Verdict final : aucun bloquant après corrections

Contre-lecture du lot corrigé :

- Point 1 clos : ACA-ETUDE-1 porte désormais protocole versionné, formes A/B figées et mesure initiale sans aide avant toute première étude humaine. ACA-TRANSFERT-1 exige cette preuve préalable, interdit sa reconstruction et réserve sa phase aux mesures différées et au bilan. JSON aligné.
- Point 2 clos : promesse de prototype anticipé supprimée ; cahier ETUDE rappelle explicitement de ne pas commencer blocked. Seul le contrat pilote peut avancer avant le bilan ; ROADMAP, JSON, AUDIT et 0035 concordent.
- Point 3 clos : ROADMAP décrit ACA-TUTEUR-1 comme rôle social consenti, et laisse le professeur adaptatif à cadrer après RESPONSE.
- VERIFICATIONS.md existe et distingue contrôles exécutés, reproductions, preuves humaines absentes et captures B exclues. Les résultats de suites y sont ceux attestés par le parent ; cette contre-lecture ne les a pas réexécutées.

Aucune édition du dépôt par le relecteur. Les remarques initiales ci-dessous sont conservées comme historique de revue, toutes closes.

## Remarques initiales, corrigées

### 1. P1 — Le protocole avant étude ne peut commencer qu’après une étude jouée

`chantiers/ACA-TRANSFERT-1.md:4` et `roadmap.json:871` imposent ACA-ETUDE-1 comme dépendance. Or ETUDE ferme après « étude réellement jouée » (`chantiers/ACA-ETUDE-1.md:31`). TRANSFERT exige ensuite de préparer les formes avant le pilote et de mesurer avant l’étude (`:11-14`). Le graphe ne contient pas de cycle formel, mais l’ordre exécutable rend la mesure initiale impossible ; préparer la baseline rétrospectivement détruit la preuve avant/après.

Correction minimale : placer la préparation du protocole, des formes figées et la mesure initiale dans ACA-ETUDE-1, explicitement avant sa première étude humaine (avec condition sans aide et trace de version). Laisser ACA-TRANSFERT-1 dépendre d’ETUDE pour les seuls rappels différés, analyse et bilan. Mettre les étapes de TRANSFERT au passé/prérequis documenté pour cette préparation ; ne pas ajouter une dépendance inverse qui créerait un cycle.

### 2. P1 — La préparation autorisée pendant le rituel reste interdite par le cadre d’exécution

`chantiers/ACA-ETUDE-1.md:8-10`, sa note JSON et 0035:31-32 autorisent la préparation et un prototype isolé pendant le rituel. Mais ETUDE est `blocked` jusqu’au rituel ; `CONTRIBUER.md:11-14` interdit de commencer un item blocked, même pour un squelette. Un futur agent doit soit violer le cadre soit ignorer la parallélisation annoncée.

Correction minimale sans affaiblir le cadre : supprimer la promesse de prototype anticipé des documents et annoncer que seul le contrat pilote ready peut avancer avant le bilan. Si la préparation pédagogique parallèle est voulue, créer un item distinct borné (préparation documentaire et protocole, sans injection dans banque jouée), avec cahier et dépendances propres ; ETUDE dépend alors de cette préparation et conserve son gate rituel pour jouer. Éviter une exception générale « on peut commencer blocked ».

### 3. P2 — ACA-TUTEUR-1 désigne le rôle social consenti, pas l’intégration d’un professeur IA

ROADMAP, section « IA, groupe et horizon », rattache à ACA-TUTEUR-1 « l’intégration ultérieure au produit » dans le paragraphe de progression du professeur IA. L’item JSON ACA-TUTEUR-1 (vers :608) ne porte qu’un rôle tuteur consenti, visibilité, retrait et absence d’export ; il dépend des cercles. Il n’a aucun livrable de correction pédagogique IA. Cela invite une reprise à élargir le chantier sensible hors de son résultat.

Correction minimale : préciser « ACA-TUTEUR-1 concerne le rôle social consenti ; l’intégration d’un professeur IA adaptatif reste à cadrer après ACA-RESPONSE-1 ». Pas de nouveau chantier d’IA nécessaire dans cet audit.

## Contrôles favorables et limites

- Parcours DFS de toutes les dépendances JSON : aucun cycle formel et aucune référence absente.
- Dépendances explicites des cahiers PUBLICATION, PILOTE-CONTRAT, ETUDE, TRANSFERT et METHODE concordent avec JSON ; les défauts 1/2 concernent le sens des phases, pas une faute de saisie du graphe.
- Publication/authentification et trajets physiques ne sont pas supprimés : déplacés explicitement dans PUBLICATION. Les sept séances sont conservées dans RITUAL parmi les trente.
- T1/T2/T3 restent explicitement non corrigés ; source disponible versus provenance structurée et schéma versus vérité sont distingués. Pas de nouvelle fausse assurance identifiée dans cette lecture.
- SCIENCE distingue les notices/résumés consultés du texte intégral manquant, le pilote d’une causalité générale, l’IA assistée du savoir autonome. Relecture de cohérence uniquement, pas nouvelle expertise exhaustive de toutes les publications.
- Aucun élargissement de produit ou suppression des garanties de péremption/provenance/identifiants constaté dans le contrat pilote. La version de correction de sens reste à spécifier avant usage.
- À la première lecture, MODELES-2 était ready et VERIFICATIONS.md restait à écrire ; ces états étaient transitoires, pas des défauts. VERIFICATIONS.md a été lu à la contre-lecture finale.

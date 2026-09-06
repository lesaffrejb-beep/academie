# Du souhait au chemin, avec un premier exemple électrique

Livraison locale du 6 septembre 2026. Outil Codex, modèle GPT-6 (identifiant
précis non exposé). Sources publiques, cas et profil d’essai fictifs.

## Ce qui est concret

[CHEMINS.md](../../CHEMINS.md), le [prompt](../../prompts/construire-un-chemin.md)
et le routage d’AGENTS définissent le travail de l’agent à chaque demande :
cible observable, rattachement, acquis à diagnostiquer, sources et manques,
progression, supports, critères de réussite, transfert et reprise.

Le [dossier électrique](chemin-electricite.json) donne deux voies : si les
mécanismes sont déjà expliqués, passer au cas ; sinon, comparer les schémas
avant le cas. Il n’attribue aucun acquis à JB. La lecture d’un rapport complet
reste une suite à construire, avec une source explicitement manquante.
Le client conserve une étude séquentielle ; l’agent adapte en conversation.

La CLI prépare un squelette puis vérifie un dossier instruit. Elle contrôle
références, dépendances, preuve déclarée d’un acquis observé, présence et
empreinte de l’original en mode strict, et étude associée dans la banque.
Le [verdict](VERDICT-CHEMIN.json) est une cohérence structurelle, sans jugement
de compétence. Les limites sont détaillées dans [la revue](RELECTURE-PIPELINE.md).
L’écart de péremption identifié par la revue a été corrigé et testé.

## Du document à l’étude

[Lecture contrôlée](LECTURE-INRS.md) : neuf pages INRS sélectionnées et
une page Promotelec, dix verdicts usine sur extraits physiques d’une page.
L’original INRS complet n’est pas déclaré relu. Les [notions et passages](NOTIONS-ELECTRICITE.md)
sont transformés en une leçon, six exercices dont deux schémas originaux,
puis une synthèse sur un cas nouveau. [Relecture distincte](RELECTURE-ELECTRICITE.md)
avec corrections avant promotion. Sept cartes, aucune recette de câblage,
aucune prescription numérique ou qualification professionnelle annoncée.

Les deux PDF originaux sont copiés dans
`/Volumes/NOIR 1/Academie/sources-publiques/2026-09-06-electricite/`.
[Manifeste](ARCHIVE-NOIR.json) : tailles et SHA-256 identiques aux originaux
locaux. Aucune archive complète de NotebookLM n’est revendiquée.

## Contrôles et observation

- Test électrique rouge avant contenu : ouverture absente, conservé dans `electricite-rouge.log`.
- Quatre E2E électriques verts, ordinateur et téléphone : ouverture, deux supports chargés, six questions, réponses et critères repris après rechargement, exclusion IFSI. Les API sont simulées pour ces scénarios ; les erreurs de proxy du scénario IFSI ne constituent pas une preuve de synchronisation.
- Dix E2E du graphe verts : accès aux études, relation parent/approfondissement, retour et filtrage du cursus, absence de débordement. Log `TESTS-GRAPHE.log`.
- 336 tests du client et six de publication verts ; compilation réalisée par les E2E. Log `TESTS-WEB.log`.
- `python3 app/tests.py` tout vert, dont les onze tests du nouveau contrôle ; `python3 tooling/check.py` zéro erreur après correction typographique du tampon de relecture. Logs conservés.
- Les deux captures mobiles sont examinées : schémas lisibles, légendes non coupées, bouton d’agrandissement visible. Aucune preuve d’usage sur téléphone physique.
- Navigateur de l’application sur le serveur local réel, avec une base séparée et un profil fictif : création, entrée dans le cursus, compteur de l’arbre, branche Électricité et ouverture de l’étude constatées. Le serveur d’essai est `http://127.0.0.1:5187/academie/`. Aucun acquis ni réponse de JB enregistré.

## Les compteurs et leur portée

Banque locale : 144 cartes, dix études. Copro : 134 cartes et huit études,
dont trois du socle et cinq approfondissements. L’arbre annonce séparément
389 chapitres prévus dans le socle. IFSI : dix cartes, deux études.

L’[audit de la collecte](AUDIT-CHAINE.md) précède cette nouvelle unité :
200 occurrences inventoriées ne sont pas 200 cours. Les captures de texte
et médias ne prouvent ni leur exhaustivité, ni leur lecture, ni leur
transformation en notions. Les cinq approfondissements s’appuient sur des
passages de cinq PDF publics, dont les deux ajoutés ici ; ils ne prouvent
pas la transformation automatique du corpus NotebookLM.

Cette livraison n’est pas installée sur le VPS. Le choix du chemin dépend
encore d’une vraie réponse au diagnostic. L’apprentissage, la rétention et
le transfert chez JB restent non mesurés.

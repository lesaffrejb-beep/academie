# Relecture indépendante ACA-MODELES-2 — 05/09/2026

Relecteur : Codex, agent indépendant `/root/design_review`, n’ayant pas écrit le changement. Mission : retrait des classifications de modèles, compatibilité de reprise documentaire, maintien des sceaux et contrôles. Aucun résultat UI B consulté. Aucun code produit ou état source réel modifié ; essais uniquement sur racines jetables.

## Verdict final après correctif : aucun bloquant restant

Le chargeur complète maintenant en mémoire les deux bornes absentes avec celles du dépôt produit, sans consulter les anciennes classes et sans réécrire le domaine. Relance indépendante de la suite usine : code 0, TOUT VERT. Le journal rouge additionnel fourni montre cinq échecs avant ce correctif.

Confirmation supplémentaire sur la fixture de reproduction initiale, toujours configurée dans l'ancien schéma : série placée à 2 et taille à 12 uniquement dans cette fixture ; validation réussie, taille passée à 24 (au-delà de l'ancien plafond 4), unité antérieure et sceau inchangés. Puis redéclaration `local-mini --classe petit` réussie avec taille commune 12. Le fichier academie.json du domaine est identique octet pour octet avant/après. Aucune nouvelle régression identifiée dans le correctif.

Observation de couverture non bloquante : le scénario automatisé actuel possède assez peu de pages pour terminer après seulement deux nouvelles validations une fois la taille passée à 12 ; il ne franchit donc plus le seuil de doublement après correctif. L'essai indépendant ci-dessus le couvre. Pour le pérenniser, placer la série à 2 avant une validation et vérifier explicitement la taille attendue, ou allonger le document de fixture.

## Historique du verdict initial : un bloquant de compatibilité, corrigé

### [P1] Reprendre un dépôt-domaine existant provoque des KeyError

Fichiers : `app/usine/etat.py:39`, `:124`, `:300`.

Le chargeur `config()` retourne la section usine telle quelle. Le nouveau code exige désormais `unite_initiale` et `unite_max` à plat. Un dépôt-domaine créé avant ce changement possède encore les bornes dans `usine.classes` : il n’est pas automatiquement mis à jour lorsque le dépôt produit et son gabarit changent. `ACADEMIE_RACINE` continue pourtant de pointer sur ce dépôt indépendant.

Reproduction sur une fixture temporaire avec texte artificiel, état comportant une unité validée et une ouverte, puis remplacement de la section usine par celle de `git show HEAD:academie.json` (ancien schéma) :

- `suivant <empreinte>` réussit et reprend l’unité existante.
- `declarer <empreinte> --outil codex --modele nouveau-modele --classe petit` échoue : `KeyError: 'unite_initiale'`, ligne 124.
- `valider <empreinte>` à la troisième unité propre échoue : `KeyError: 'unite_max'`, ligne 300.

Fixture de preuve : `/var/folders/qq/5q7p33xj69s6r0ys8y0qh3ww0000gn/T/academie-usine-gbwqav98` ; empreinte `3564534901fd1a77`. La série est placée à 2 dans cette fixture pour atteindre immédiatement le chemin de doublement. Aucun état réel touché.

Conséquence : l’ancien argument CLI est bien accepté, mais la reprise réelle d’un ancien dépôt-domaine reste bloquée. Pas de perte de sceau constatée ; l’exception survient avant sauvegarde de la validation. La compatibilité annoncée par MODELES/0034 est incomplète.

Correction attendue : normaliser l’ancienne configuration en mémoire avec des bornes communes documentées, indépendantes du nom ou de la classe, sans réécrire les sources et états réels. Ajouter un test CLI où état ET configuration viennent de l’ancien schéma, couvrant redéclaration et atteinte du seuil d’augmentation. Une alternative explicite de mise à jour de configuration doit éviter ces exceptions et être intégrée au parcours de reprise ; elle ne doit pas réintroduire le classement.

## Contrôles positifs

- Le journal rouge fourni comporte bien sept échecs pertinents ; le journal vert les ferme.
- Relance indépendante de `python3 app/tests_usine.py` : code 0, TOUT VERT (usine).
- Le code ne déduit plus de restriction du nom de modèle ; la recherche ciblée app/tooling/prompts/docs actives ne retrouve les anciennes clés que dans la compatibilité CLI, les tests et le contrôle de leur absence.
- `declarer --help` ne montre plus `--classe` ; son passage explicite génère l’avis d’obsolescence et ne crée plus de classe dans la nouvelle déclaration.
- Avec configuration neuve, le scénario d’état ancien conserve le sceau antérieur et l’unité ouverte ; une classe inconnue n’est plus consultée.
- La redéclaration remet la taille et la série à leur base commune, sans effacer unités ou journal. Ce comportement est expliqué dans le prompt de reprise.
- Les seuils de fidélité et contrôle numérique ne sont pas affaiblis dans le diff. Réduction après refus et augmentation après série restent testées.
- Les deux sections usine du produit et du gabarit ont la même nouvelle structure et les mêmes paramètres ; le contrôle global appelle maintenant controle_usine et refuse les anciennes clés dans ces deux configurations maintenues.
- Les instructions actives examinées retirent les autorisations fondées sur classes et conservent sources, cahier et relecture indépendante. La décision 0034 amende explicitement 0027.

## Couverture et limites

Relecture des diffs demandés, du cahier, décision 0034, MODELES et CONTRIBUTION §7/8 ; examen des fonctions de charge, déclaration, reprise, validation et résumé. Aucun audit de vérité documentaire ni modification de cartes. Gates complets du dépôt laissés à l’agent parent. Le test actuel de compatibilité ne couvre que l’ancien champ de déclaration dans une configuration déjà mise à jour, ce qui explique le faux sentiment de couverture sur les anciens dépôts-domaines.

# Contre-passe indépendante de l’étude

05/09/2026. Auteur : Codex, modèle GPT-6 ; session `/root/revue_science`,
distincte de celle qui implémente l’écran. Périmètre : écran Étude, moteur
de reprise/disponibilité, magasin multi-métier, publication des études et
attestation structurée. Aucun contenu métier nouveau ni correction de
code de production dans cette passe ; seuls tests, rapport et méthode §34.

Il s’agit d’une inspection de logiciel et de tests adverses. Aucun verdict
de lecture intégrale usine ni aucune observation humaine d’apprentissage.
Les assertions des cinq chapitres ne sont pas réauditées à la source par
cette passe ; leur relecture de contenu reste une preuve distincte.

## Défauts transmis au coordinateur

| Priorité | Déclencheur et constat initial | Correction attendue |
|---|---|---|
| P1 | Réponse aidée notée « Évident » : `mode:revision`, note FSRS haute, indicateur d’aide ignoré par le rejeu | Conserver essai assisté sans note de rappel autonome ; ne pas augmenter la stabilité comme une réussite sans aide. |
| P1 | Indice consulté puis rechargement avant validation : texte conservé mais `aide=false`, confiance perdue | Conserver ensemble texte, aide, confiance et choix pendant la reprise. |
| P1 | Corrigé QCM affiché puis rechargement : choix à nouveau modifiable et retour disparu | Conserver révélation et choix initial, ou requalifier explicitement la reprise assistée. |
| P2 | Choix QCM validé : journal écrit le texte libre vide au lieu du choix sélectionné | Conserver la réponse choisie et son résultat ; choix faux reste un rappel à reprendre. |
| P1 | Péremption illisible : comparaison avec `NaN` laisse servir la leçon | Refuser date non canonique ou calendrier impossible, comme pour les cartes. |
| P1 | Attestation dont tous les champs valent `true` : valideur ne contrôle que la présence | Types, date calendaire, identités textuelles et listes d’assertions/sources structurées ; les anciens tampons restent lisibles selon leur statut historique. |
| P2 | Changement copro vers IFSI : Profil associe journal global et cartes filtrées ; anciennes réponses deviennent « Carte indisponible » | Clarifier portée globale ou filtrer les indicateurs métier, sans tronquer le journal conservé/exporté. |
| P2 | Étude recommencée : clés de brouillon réutilisées avec anciennes réponses/indices/choix | Retirer le brouillon après écriture réussie ou distinguer les passages ; aucun effacement du journal. |

La correction du coordinateur a été observée en cours pour la date,
la note des exercices assistés et la conservation du choix QCM. Les autres
points exigent leur contre-test sur l’état intégré avant conclusion.

## Tests adverses ajoutés

- `web/src/moteur/etude.relecture.test.ts` : huit cas couvrant disponibilité
  positive, dernier jour inclus, quatre dates invalides, retrait après
  signalement/brouillon/péremption, ordre réel de reprise, séparation des
  chapitres/versions et conservation de la condition d’aide. Huit verts
  après correction du coordinateur.
- `app/tests_etude_relecture.py` : six cas isolés sur catalogue et attestation.
  La fixture valide est effectivement publiée ; une carte absente/périmée,
  un brouillon, un tampon historique ou la même session de relecture ne
  l’est pas. Six verts après correction du coordinateur ; test des champs booléens
  initialement rouge, puis positif lors de la contre-exécution.
- `web/tests/e2e/etude.relecture.spec.ts` : trois parcours navigateur pour
  aide/confiance après rechargement, absence de note FSRS sur essai assisté,
  choix initial et retour conservés après rechargement. Exécution à
  consigner par le coordinateur sur son build et navigateur configurés.

Les tests ne remplacent pas la lecture des sources métier. L’attestation
structurée identifie une passe distincte mais ne prouve pas à elle seule
la vérité d’une assertion ni la qualité de son examen. Aucun constat de
compétence clinique ou de maîtrise professionnelle ne se déduit du parcours.

## Cohérence pédagogique

La grille suit bien une réponse écrite, le statut final dit « parcourue »,
et le transfert différé reste « non mesuré ». L’étude sans indice reste
une activité à chaud après la leçon ; le journal doit conserver `format:
etude` pour éviter de l’assimiler plus tard à une mesure autonome différée.

L’entrée `METHODE.md` §34 documente cette boucle, sa filiation et ses
limites. Aucun effet chiffré, dose optimale ni récompense thérapeutique
n’est ajouté. Le critère d’une véritable mesure reste une réponse nouvelle
sans aide, après délai, corrigée selon une grille définie avant l’essai.

## Dernier état observé de cette passe

Le code intégré conserve désormais le retour révélé dans le brouillon,
verrouille le texte et le choix après révélation, puis retire le brouillon
après écriture réussie au journal. Les six tests Python adverses passent.
La correction de disponibilité passe les huit tests TypeScript adverses.
La portée du Profil multi-métier et les parcours navigateur doivent encore
être confirmés par le coordinateur.

`python3 tooling/check.py` lancé pendant les tests navigateur d’une autre
session signale deux occurrences de voix interdites dans une ressource
capturée sous `web/test-results/.playwright-artifacts-4/traces/`, sans
occurrence dans les livrables de cette passe. Le contrôle final doit être
rejoué une fois ces artefacts de test traités ; aucun résultat vert global
n’est revendiqué à cet instant.

## Contre-passe des corrections et validation du journal Étude

La contre-inspection confirme : aide sans note FSRS, brouillon groupant
texte/aide/confiance/choix/retour révélé, choix initial conservé et verrouillé
après retour, date de péremption canonique, attestation typée, brouillon
retiré après écriture réussie. Le Profil filtre désormais ses réponses et
libellés au métier actif. Réserve transmise : son total de points annoncé
« tous métiers » doit également utiliser un calcul global ; le calcul
observé mélange encore révisions globales et remplissage du métier actif.
Le coordinateur corrige ce dernier point et centralise les essais navigateur.

Une frontière supplémentaire a été confiée explicitement à cette session :
valider les cinq champs optionnels Étude déjà inscrits dans journal-v1.
Les validateurs serveur et client appliquent désormais les étapes admises,
version entière positive, index entier non négatif, texte limité à 5000
caractères Unicode et indicateur d’aide booléen. L’absence de ces champs
reste acceptée ; aucune propriété inconnue n’est supprimée ou interdite.
Les événements historiques sans champs Étude restent compatibles.

Tests écrits avant correction :

- `serveur/tests/test_etude_validation.py` : 36 sous-cas initialement en
  échec, puis trois tests positifs incluant toutes les étapes, types et
  bornes, limites Unicode, rejet atomique du lot et conservation exacte
  des propriétés inconnues lors de l’export.
- `web/src/donnees/api.etude.test.ts` : six tests initialement rouges,
  treize positifs après correction. Un acquittement contenant une étape
  inconnue est rejeté avant l’union ; une propriété inconnue historique
  reste inchangée.

Contre-exécution : `python3 -m unittest` sur validation Étude, journal et
parité serveur, **16 tests verts** ; Vitest API Étude, API existante et
relecture Étude, **30 tests verts**. Aucun build ni E2E lancé dans cette
passe. Aucun changement de `web/src/moteur/journal.ts` : la précision de
l’horodatage est traitée et contrôlée par la session dédiée au journal.

## Correction finale du calcul par métier

À la demande explicite du coordinateur, la réserve sur les points a été
corrigée dans `web/src/app/magasin.tsx` et le libellé du Profil. La vue
`journalPourMetier` retient les événements rattachés aux cartes, chapitres
ou domaines du métier actif ; seuls cette vue et le catalogue actif
alimentent les états calculés, la progression et les points. Le contexte
continue de fournir le journal complet, et l’export ne change pas. Les
anciens événements sans rattachement identifiable restent conservés ;
on ne leur invente pas de métier pour les indicateurs.

`web/src/app/magasin.metier.test.ts` : deux tests rouges avant correction,
puis verts. Un rappel et un examen copro donnent des points copro ; la
bascule IFSI donne zéro point, rappel, carte touchée et jour joué étrangers ;
le retour copro restaure le même bilan, sans aucune mutation du journal.
La régression vérifie aussi la conservation d’un événement historique sans
rattachement connu.

Dernière exécution ciblée : **34 tests TypeScript verts** dans cinq fichiers
(magasin, métier, API existante, API Étude et relecture Étude). La suite
serveur ciblée reste à **16 tests verts**. Aucun build ni scénario navigateur
relancé par cette session. La vérification de l’horodatage monotone, le
build, les essais navigateur et les contrôles globaux sont centralisés
par le coordinateur sur l’état final partagé.

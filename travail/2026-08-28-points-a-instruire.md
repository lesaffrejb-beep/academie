# Points à instruire — remontés par la production de cartes M1

28/08/2026. Les agents qui ont fabriqué les premières cartes ont
refusé de carder certaines affirmations de leurs fichiers sources.
Chaque ligne est un doute argumenté, pas une certitude : rien n'a été
corrigé dans les référentiels, rien n'est devenu une carte.

C'est la boucle d'amélioration prévue au BLUEPRINT §6.4 : quand
l'exercice révèle un trou dans une grille, c'est la grille qu'on
corrige. Elle a produit dès le premier lot.

## A. Dans `.agents/skills/erp-comptable/references/checklist-anomalies-comptes.md`

Ce fichier porte `status: validated`, `confidence: 0.85`, et il sert
aux études comptables réelles. Les quatre points sont en file
d'alertes.

| # | Affirmation de la checklist | Le doute |
|---|---|---|
| A1 | Art. 29-1 A : « > 15 % du budget (copro ≤ 200 lots) ou 25 % (> 200 lots) » | Les deux taux paraissent **inversés** (25 % en principe, ramené à 15 % au-delà de 200 lots), et l'assiette serait les **sommes exigibles** au sens des art. 14-1 et 14-2, pas « le budget ». |
| A2 | Art. 10-1 : mutation au a), recouvrement au c) | Probablement l'inverse. La substance a été cardée sans citer la lettre. |
| A3 | « Proposer un vote de l'AG pour un dépassement (art. 14-1) » | L'art. 14-1 ne prévoit pas ce vote d'autorisation. Affirmation écartée de la carte. |
| A4 | Art. 45-1 du décret 67-223 pour la restitution du solde de travaux | L'article visé traite de la tenue de la comptabilité. Non recoupé. |

## B. Dans `.agents/skills/erp-sinistres/references/`

| # | Affirmation | Le doute |
|---|---|---|
| B1 | « Art. 18 al. 2 » pour les mesures conservatoires | L'alinéa n'a pas été recoupé ; les cartes citent l'article seul. |
| B2 | Délai de 5 jours ouvrés tempête/grêle rattaché à l'art. L122-7 | Ce texte traite de l'étendue de la garantie tempête, pas d'un délai. **Aucune carte tempête produite.** |
| B3 | Détail multi-locaux de la recherche de fuite | Le fichier source porte lui-même un `[À VÉRIFIER]` à cet endroit. |

## B bis. Le décret 2025-1292, daté différemment par deux fichiers (en file d'alertes)

La veille juridique l'applique en doctrine pleine ; le radar de
conformité le range en `[À VÉRIFIER]` faute de trancher son entrée en
vigueur (25/12/2025 ou 21/02/2026). Périmètres différents, donc pas une
contradiction frontale — mais deux réponses possibles sur le même
décret, et cette date commande la renégociation des contrats de syndic.

**Conséquence immédiate** : la ligne 6 du radar (« état financier et
compte de gestion notifiés au plus tard avec l'ODJ ») ignore l'option
extranet que la veille admet pour les documents de l'article 11. Un
contrôle mené sur cette seule ligne déclarerait non conforme une
copropriété qui applique correctement le nouveau régime.

## B ter. Points non instruits du radar et de la veille (aucune carte fabriquée dessus)

1. Majorité applicable au vote d'une cotisation au fonds de travaux supérieure au minimum légal.
2. Périodicité de l'évaluation de l'état de conservation des matériaux de liste A (3 ans souvent cité, non confirmé).
3. Date d'entrée en vigueur de l'annexe 1 modifiée du décret 67-223 (contrat type).
4. Objet de l'alinéa de L126-31 CCH supprimé par la loi 2026-403 du 26/05/2026.
5. **Cass. 3e civ., 18 juin 2026** : numéro de pourvoi non recoupé. Une carte a **quand même été faite** sur le fond (corroboré par l'arrêt du 15/01/2026, lui référencé), avec la réserve inscrite **dans le champ `source` de la carte**, pour qu'elle voyage avec elle. À retrouver avant toute citation en séance.
6. Arrêts meublés de tourisme des 27 mars, 22 mai et 16 octobre 2025 : numéros non vérifiés, non cités.
7. Quel texte a créé l'article 10-4 du décret 67-223 : la veille donne l'entrée en vigueur sans nommer le véhicule.
8. Les 7 sujets du § 6 de la veille (nullité en cascade, carence d'appels de fonds, art. 10-1, usucapion, clause réputée non écrite, surélévation, DPE et obligation de délivrance) : non instruits, aucune carte.

## B quater. Un doublon à traiter à la validation

`procedure-terrain-quitus-sans-immunite` et `droit-veille-quitus-portee`
portent le même arrêt (29/02/2024) et la même règle de fond. Ids
distincts, donc le valideur passe, mais les deux tomberaient ensemble
en rotation. La première ajoute une nuance que la seconde n'a pas
(l'irrecevabilité de l'action en annulation quand on a voté pour).

**À traiter à la double passe de validation, pas avant** : fusionner
maintenant casserait des chaînes de prérequis pour un gain nul, puisque
aucune des deux n'est jouable tant qu'elle est `brouillon`.

## C. Dates de vérification manquantes dans `apprentissages-syndic.md`

Trois apprentissages ne portent aucune date. Les cartes qui en
dérivent ont reçu une date déduite, à confirmer — ou mieux, à inscrire
dans le fichier source :

- *Pièces jointes de convocation* → `2026-08-28` déduit (section postérieure à celle du 21/08).
- *Une demande interne n'est pas une décision manquante* → `2026-08-15` (date `updated` du frontmatter).
- *Garde-fou de vote des honoraires* → `2026-08-15` (idem).

## D. Ce que la production a laissé en réserve (matière identifiée, non cardée)

- **Électricité des communs / TRV** (`apprentissages-syndic`, 04/08/2026) : 4-5 cartes prêtes à écrire dans un `energie/electricite-communs.json` — le TRV acquis de droit (L337-7), la suppression du plafond 36 kVA, le piège « TRV = moins cher », la sortie sans frais, l'absence de vote d'AG. `peremption` obligatoire sur tout ce qui touche aux barèmes.
- **« Un grand livre ne dit pas de quel exercice il parle »** : la meilleure carte comptable encore disponible, aucun garde-fou existant ne l'attrape.
- **« Un chiffre de comparaison se cite au lot »** : trois cartes possibles.
- **Garde-fou du radar de fragilité** : « le taux d'impayés seul est une photo trompeuse, c'est la dette persistante sur deux exercices qui compte » — bonne carte `comptabilite`. En revanche la grille de pondération DREAL elle-même est un modèle régional daté : en tirer un QCM obligerait à inventer des seuils.

## E. Le modèle de domaines : deux manques constatés à l'usage

Six apprentissages de terrain n'entrent dans **aucun** des neuf
domaines. Ce n'est pas un défaut de la matière, c'est un trou du
modèle (BLUEPRINT §9) :

1. **Posture commerciale et relation client** — « le hors-forfait se
   rend visible, dans les deux sens » (un travail offert en silence est
   un travail dû la fois suivante), la durée des contrats de syndic.
   Ni droit, ni procédure, ni comptabilité.
2. **Méthode de travail : sources, IA, écrit défendable** — « un
   rapport de LLM ne vaut pas par ses affirmations, il vaut par ses
   questions », « citer une pièce, c'est citer la page », « un motif de
   vote ne s'infère jamais » (cardée de force en `procedure`).

Le second manque est ironique : c'est le domaine qui protégerait JB de
l'outil qu'il est en train de construire. **Arbitrage à rendre par JB**
— et il vaut mieux le rendre tôt : le domaine fait partie de l'id des
cartes, donc le changer plus tard coûtera soit des ids incohérents,
soit l'historique FSRS des cartes déplacées.

Écartés sans regret (règles de session, pas savoir métier) :
« vérification externe : six sources en direct », « le quotidien se lit
dans le repo ». Ils périment avec l'outil.

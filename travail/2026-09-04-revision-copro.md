# Révision copro : point de reprise du 04/09/2026

**Reprise du 04/09, publication demandée par JB :** [état livré, limites et suite](2026-09-04-publication-et-suite.md). Ce point actualise les mentions historiques de pause et de publication ci-dessous.

Lot L2 du [plan commun](rapports-chatgpt-pro/PLAN.md), cahier
[`ACA-COPRO-1`](../chantiers/ACA-COPRO-1.md), demandé par JB après
le classement des trois rapports et la finition IFSI.

## Arrêt demandé par JB

**Pause propre pendant la relecture L2. Ne pas marquer le chantier terminé.**
Les trois agents ont été interrompus. Les dernières retouches AG sont sur
disque, mais leur relecture croisée et leur note de sources n'étaient pas
terminées. Les paragraphes suivants décrivent les fichiers présents,
pas une validation éditoriale achevée.

Le statut `ready` dans `roadmap.json` signifie ici « reprenable depuis son
cahier » ; aucune exécution automatique n'a été créée. La sauvegarde
compressée est `travail/sauvegardes/copro-l2-2026-09-04.zip` ; elle contient
les fichiers du lot, le témoin avant L2, les scripts et logs temporaires
utiles. Elle ne remplace pas les modifications locales, conservées en place.
Rien n'a été committé, poussé ou publié. Le dépôt contient aussi des
modifications préexistantes front/journal/IFSI : ne pas les annuler ni
les inclure globalement dans un futur commit de ce lot.

## État de cette passe

34 chapitres ont reçu une correction ou une précision de champ.
Les 389 identifiants, titres, niveaux, prérequis, ponts et estimations
du programme existant sont conservés. Les retouches vivent dans les
données du générateur ; JSON et syllabus sont régénérés depuis elles.
La passe ne constitue pas un audit intégral des 389 chapitres.

| Surface | Traitement |
|---|---|
| Inventaire | Abstentions, pouvoirs, passerelles, notifications, régimes de copropriété, financement, assurances, représentation, garanties, diagnostics, normes, rôle du gestionnaire et activités du cabinet. |
| Banque v1 | Corrections ciblées sur majorité, notifications, fonds, DPE collectif et déclarations d'assurance. Les origines historiques restent présentes ; les auteurs et dates de correction sont consignés. |
| Cartes conventionnelles | `sinistres-irsi-tranches`, `sinistres-irsi-assureur-gestionnaire`, `sinistres-recherche-de-fuite`, `sinistres-cidre-abrogee` signalées ; contenu conservé, anciennes dates conservées, exclusion de la génération. |
| Chapitre article 24 | Correction du calcul, de la fausse chronologie 2020, du conseil syndical, du PV et des sources ; il reste brouillon. |
| Compteurs | 389 chapitres, dont 333 au socle ; 2 990 cartes cibles, dont 2 486 au socle. Banque : 84 cartes, dont 76 valides, 4 signalées, 4 brouillons. Deux chapitres v2 brouillons, 11 cartes, aucune promotion. |
| Durées | 310 h 45 d'études estimées pour le socle, hors rappels et mise en pratique. Durée de formation réelle non mesurée. |

## Preuves et sources

- [Table des 34 retouches avant/après](rapports-chatgpt-pro/copro-corrections.json).
- [Assemblées et votes](rapports-chatgpt-pro/copro-assemblees.md).
- [Financement et procédure](rapports-chatgpt-pro/copro-financement-procedure.md).
- [Assurance et cartes signalées](rapports-chatgpt-pro/copro-assurances.md).
- [Technique, énergie et activités du cabinet](rapports-chatgpt-pro/copro-technique.md).

Les notes indiquent les sources primaires, les périodes et champs, les
exceptions et les cas fictifs contradictoires. Le texte intégral actuel
d'IRSI et celui de la norme NF C 15-100 restent des sources à retrouver ;
ils ne sont pas reconstruits depuis le rapport LLM. La carte d'article 24
v1 et la carte comptable du double plancher étaient déjà correctes sur
leur règle principale : leur présence n'est pas assimilée à une erreur.

## Vérifications du lot

Les contrôles rouges ont précédé les retouches. Logs temporaires :
`/tmp/academie-copro-tests-rouge.log`,
`/tmp/academie-copro-assurances-rouge.log`,
`/tmp/academie-copro-technique-rouge.log` et les logs assemblées.
Le témoin avant L2 est `/tmp/academie-copro-avant-l2.json` ; les traces
durables des corrections sont dans les notes et le JSON ci-dessus.

La suite `python3 app/tests_copro.py` vérifie les identifiants, les deux
artefacts, la persistance des corrections et la sélection réelle du
générateur. Un test de texte ne prouve pas une règle de droit : les
sources et la relecture indépendante complètent ces contrôles.

Avant les dernières retouches AG, `python3 app/tests.py` était entièrement
vert et `python3 tooling/check.py` donnait zéro erreur ; logs
`/tmp/academie-copro-global.log` et `/tmp/academie-copro-check.log`.
Contrôle final après arrêt des agents : `app/tests.py` entièrement vert,
`tooling/check.py` zéro erreur et `git diff --check` sans erreur. Logs
`/tmp/academie-copro-pause-tests.log` et
`/tmp/academie-copro-pause-check.log`, inclus dans la sauvegarde. Ces
contrôles ne prouvent pas la justesse juridique de la dernière retouche AG.

Relecture au moment de l'arrêt :

- `verifie_rapport_strategie` n'a pas relevé de réserve sur les deux
  retouches de conformité écrites par `validation_ifsi` (fonds et DPE).
- `validation_ifsi` avait recoupé les quatre corrections assurance avec
  L113-2 et L125-2 et confirmé les quatre signalements ; son avis final
  sur les 34 retouches du programme restait à rendre.
- Les cinq cartes v1 AG retouchées, le chapitre article 24 et cinq de ses
  sept cartes venaient d'être écrits par `revue_pedagogique_ifsi` ; la
  relecture de `verifie_rapport_strategie` n'avait pas encore eu lieu.
- Les tampons restent donc en attente dans les fichiers. Ne pas transformer
  un résultat de tests en relecteur fictif ou en validation juridique.

### Première unité de reprise

1. Lire ce point puis le cahier. Comparer les fichiers courants à la
   sauvegarde ; ne pas relancer les scripts de correction aveuglément.
2. Terminer la note `copro-assemblees.md` à partir des sources déjà
   vérifiées et relire les cinq cartes v1 AG, le chapitre et ses cartes
   retouchées. Faire terminer la relecture des 34 objectifs du programme.
3. Corriger les seules réserves constatées, puis consigner les vrais
   auteurs/relecteurs dans les tampons existants et les notes.
4. Régénérer `site/banque.json` **après** cette relecture : sa dernière
   génération exclut déjà les quatre cartes signalées, mais précède les
   dernières retouches AG. Le fichier peut donc encore contenir les
   anciennes formulations AG. Aucun déploiement autorisé ici.
5. Rejouer `python3 app/tests_copro.py`, `python3 app/tests.py`, puis
   `python3 tooling/check.py`. Mettre à jour preuves et statut du chantier
   seulement si les relectures et contrôles sont terminés.

## Suite, sans recommencer ce lot

1. Retrouver une convention IRSI complète, datée, applicable et consultable,
   puis refaire les quatre cartes signalées avec leurs champs et exceptions.
   Les faire relire avant remise en service. Leurs anciens identifiants
   restent disponibles pour l'historique du joueur.
2. Traiter les défauts réels du client et du journal dans les cahiers
   existants ; lire `travail/audit-froid-2026-09-04.md` puis l'état courant
   de ces chantiers. Leur travail parallèle peut avoir avancé.
3. Préparer l'usage sur le client v2 souhaité par JB et mesurer le rituel
   existant. Aucune séance fictive, aucun score de compétence professionnelle.
4. Après les gates d'usage et de contenu, petit pilote AG, puis transfert
   IFSI diabète et dégât des eaux. Les contrats et parcours s'étendent
   seulement pour ce besoin ; pas de refonte massive avant preuve.

Cette passe prépare des fichiers locaux. Elle ne prouve pas leur présence
sur le serveur ni sur le téléphone ; aucune publication n'a été effectuée.

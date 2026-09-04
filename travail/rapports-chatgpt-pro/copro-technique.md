# Copro : vérification technique et professionnelle du rapport

Cahier `chantiers/ACA-COPRO-1.md`, lot L2. Vérification effectuée le
04/09/2026 par Codex / gpt-5.6-sol, à partir des assertions A §2 et B §3
du rapport original `sources/a708271c820f9311.txt`. Ce document conserve
les observations et propositions ; il n'est pas une source de droit ni
un verdict sur les points du rapport qui n'ont pas été contrôlés.

Les intitulés et identifiants ci-dessous ont été retrouvés dans
`programme/genere_copro.py` et `programme/copro.json`, puis recherchés dans
`banque/`. Une lacune de l'inventaire n'est pas présentée comme une erreur
existant déjà dans une carte. La source primaire précise le champ ; une
fiche institutionnelle facilite la lecture sans remplacer le texte.

## Deux corrections de cartes dans cette sous-tâche

Seul `banque/droit/conformite-annuelle.json` est modifié par cette
sous-tâche, pour les deux cartes ci-dessous. Identifiants, statuts,
origines et dates historiques `verifie` sont conservés. Chaque correction
porte une entrée `corrections` datée avec son auteur, sa portée et les URL
consultées. La mention `relecture: en-attente` sera traitée par l'agent
indépendant : aucun relecteur ni historique de rédaction v2 n'est inventé.

| Carte | Assertion initiale | Texte consulté, version et champ | Retouche |
|---|---|---|---|
| `droit-conformite-fonds-travaux-plancher` | La vigilance et le commentaire de source liaient le dépassement du budget et celui de la moitié des travaux par « ou ». | [Article 14-2-1 I et II, loi du 10 juillet 1965](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043967792), version depuis le 01/01/2023, consultée le 04/09/2026 : le II ajoute le second dépassement à celui du budget lorsqu'un PPT a été adopté ; l'assemblée se prononce. | Vigilance et source : avec un PPT adopté, dépassement du budget **ET** de 50 % du montant de ses travaux ; décision de l'assemblée, suspension non automatique. Sans PPT, seul le critère de budget déclenche la question à l'assemblée. Les planchers annuels de la réponse étaient déjà cumulatifs et ne changent pas. |
| `droit-conformite-dpe-collectif-champ` | « Les trois vagues étant passées, toutes les tailles sont désormais concernées », sans indication du territoire. | [CCH L126-31](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043976972), version affichée depuis le 28/05/2026 ; [article 158 VI et IX, loi Climat](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043957918/2026-06-20), calendrier et dérogation territoriale ; [Service Public F37504](https://www.service-public.gouv.fr/particuliers/vosdroits/F37504), vérifié le 01/01/2026. Tous consultés le 04/09/2026. | Question, réponse, distracteur et explication bornés à la **France métropolitaine**. Le lien précis du calendrier est ajouté. Aucun calendrier ultramarin entier n'est introduit dans cette carte. |

Contrôle éditorial ciblé avant correction :
`/tmp/academie-copro-technique-rouge.log`, sortie 1, quatre conditions en
échec. Après correction : `/tmp/academie-copro-technique-vert.log`, sortie 0.
Le script `/tmp/academie-copro-technique-controle.py` contrôle le champ,
le cumul, la décision d'assemblée, les identifiants/statuts/origines et
l'absence de modification des autres cartes. Ce contrôle constate une
régression textuelle ; il ne prouve pas à lui seul la règle juridique.

## Table de vérification et corrections minimales proposées

La colonne finale décrit le traitement conseillé à l'agent qui corrige
le générateur ; elle n'affirme pas que ces modifications ont déjà été
appliquées par cette sous-tâche. Toutes les sources ont été consultées le
04/09/2026.

| Sujet et assertion dans l'inventaire | Source, date et champ | Identifiants touchés et formulation minimale |
|---|---|---|
| Gaz/électricité : « Distinguer tarif réglementé et offre de marché pour un immeuble » reste ambigu. Aucune affirmation explicite d'un TRV gaz actuel retrouvée. | [CRE, marché du gaz](https://www.cre.fr/gaz/marche-de-detail-du-gaz-naturel/presentation.html), mise à jour 28/07/2026 : fin des contrats TRVG le 30/06/2023. [Code énergie L337-7](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049406625/2026-02-22), dispositions applicables depuis le 01/02/2025 : éligibilité électrique incluant les syndicats d'un immeuble unique d'habitation. | `energie.contrats-energie.tarifs-reglementes-et-marche` : distinguer les offres de marché du gaz et l'éligibilité aux tarifs réglementés de l'électricité selon le client et son contrat. |
| DPE : le programme n'écrit aucun coefficient erroné. La critique mentionne les paramètres 2026/2027. | [Arrêté du 19 août 2026](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000054747079), JORF du **26/08/2026**, articles 1 et 6 : remplacement de 1,9 par 1,7 au **01/01/2027** ; articles 3 et 4 pour les attestations. [Communiqué ministériel](https://www.ecologie.gouv.fr/presse/dpe-audits-energetiques-publication-larrete-abaissant-facteur-conversion-lelectricite-17-1er), 31/08/2026, complément institutionnel. La date de publication du texte est celle du JO, distincte de celle du communiqué. | `energie.dpe.la-methode-de-calcul` : rechercher le paramètre applicable à la date du diagnostic et distinguer texte en vigueur, modification future et attestation. Le texte 2027 est retrouvé ; ne pas le classer « sans source » et ne pas appliquer sa valeur avant son entrée en vigueur. |
| Calendrier DPE collectif : généralisation territoriale dans une carte existante. | [Article 158 VI et IX](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043957918/2026-06-20) et [Service Public](https://www.service-public.gouv.fr/particuliers/vosdroits/F37504), vérifié 01/01/2026 : dernière vague métropolitaine en 2026 ; les territoires ultramarins nommés relèvent d'une dérogation jusqu'en 2028. | `energie.dpe.le-dpe-collectif-et-son-calendrier` : vérifier territoire et date avant de conclure. Carte `droit-conformite-dpe-collectif-champ` corrigée ci-dessus. |
| LCB-FT : « Dire les obligations de vigilance du syndic » est effectivement trop général. | [CMF L561-2, 8°](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000050361611/2026-09-01), version indexée au 01/09/2026 ; [loi Hoguet, article 1](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512228/2026-08-22), syndic au 9°. Ce dernier n'est pas dans l'énumération immobilière du CMF. Conclusion tirée du croisement des textes : ne pas attribuer ce champ à la seule activité de syndic, ni en déduire une exemption de toutes les activités d'un cabinet. | `cabinet.donnees.lutte-contre-le-blanchiment` : déterminer quelles activités du cabinet relèvent de la LCB-FT et distinguer ce régime des contrôles contre la fraude au paiement. |
| Ravalement : notion isolée « dix ans », sans champ local. | [CCH L126-2 et L126-3](https://www.legifrance.gouv.fr/codes/section_lc/LEGITEXT000006074096/LEGISCTA000041565060), version affichée au 03/09/2026 ; [Service Public F640](https://www.service-public.gouv.fr/particuliers/vosdroits/F640), vérifié 06/03/2026. La périodicité dépend du dispositif local applicable, pas d'une règle uniforme sur tous les immeubles français. | `pathologie.facades.le-ravalement` et `travaux.urbanisme-des-travaux.ravalement-obligatoire-et-enseignes` : vérifier l'obligation locale puis distinguer entretien, ravalement et injonction. |
| Plomb/amiante : « 1950-1975 : béton, amiante, plomb » mélange repère constructif et champ documentaire. | [CSP L1334-8](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000031928065), version depuis le 28/01/2016 : CREP des parties communes concernées, construction avant le 01/01/1949. [CSP R1334-14](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000024140895/2026-06-12) : permis délivré avant le 01/07/1997 pour le champ amiante de cette section. Cela ne dit pas qu'un matériau dangereux serait impossible hors de ces repères documentaires. | Conserver l'ID `pathologie.epoques.1950-1975-beton-amiante-plomb` et clarifier la compétence. `pathologie.diagnostics.plomb` et `pathologie.diagnostics.amiante-et-dossier-technique-amiante` : distinguer histoire constructive, champ documentaire et repérage avant travaux. La carte `droit-conformite-dta-parties-communes` emploie déjà le bon critère de permis. |
| NF C 15-100 : « Dire ce que la norme électrique impose dans les communs » est trop absolu. | [Arrêté du 03/08/2016, articles 1, 4 et 5](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000032975211/), dispositions depuis le 08/08/2016 : champ des bâtiments neufs, normes datées donnant présomption de conformité et dates de dépôt applicables. Ce texte ne démontre pas une remise générale de tout ancien à la dernière édition. | `equipements.electricite.la-nf-c-15-100-pour-un-gestionnaire` : lire le champ d'un contrôle et distinguer réparation, mise en sécurité et conformité applicable aux travaux envisagés. Ne pas produire une règle inverse affirmant qu'une norme ne s'applique jamais aux rénovations. |
| Incendie : objectif universel sur désenfumage et extincteurs. Aucun seuil faux identifié dans le chapitre. | [Arrêté du 31/01/1986, article 3](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000038933527/2026-03-10), version depuis le 01/01/2020 : classement des bâtiments, dates d'application et situations particulières. | `equipements.acces.desenfumage-et-extincteurs` : identifier la famille, les dates et les équipements pour rechercher les obligations applicables et orienter les contrôles. Pas de matrice technique exhaustive fabriquée dans ce lot. |
| Toiture : « Conduire une visite de toiture en sécurité » met l'accent sur l'intervention personnelle. | [INRS, protections collectives d'un plan de travail](https://www.inrs.fr/risques/chutes-hauteur/equipements-temporaires-protection-collective-plan-travail.html), mise à jour 21/04/2023 : sécurisation préalable et protections collectives. La reformulation ci-contre est un choix de périmètre professionnel appuyé sur la prévention, pas une interdiction légale générale de toute visite par un gestionnaire. | `pathologie.toitures.la-visite-de-toiture` : préparer, faire réaliser et exploiter une inspection en vérifiant les conditions d'accès et les limites de son intervention. Un indice visuel ne devient pas un diagnostic certain par la seule réussite à un exercice. |
| Pré-état daté : le titre rapproche deux objets sans les distinguer. Le texte ne les qualifie pas explicitement d'identiques. | [CCH L721-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000043977384/2026-04-10), depuis le 01/01/2024 : informations précontractuelles ; [article 5 du décret de 1967](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053191253/2026-04-15), depuis le 25/12/2025 : état daté ; [enquête DGCCRF](https://www.economie.gouv.fr/dgccrf/laction-de-la-dgccrf/les-enquetes/syndics-de-copropriete-recherche-de-pratiques), 13/04/2021 : facturation sans commande préalable relevée comme anomalie. | `immobilier.vente.etat-date-et-pre-etat-date` : distinguer l'état daté réglementé, les informations à l'acquéreur et une prestation distincte commandée. Aucun nouveau prix nécessaire à cette clarification. |
| Carte professionnelle : intitulé incomplet, sans affirmation que tous les salariés auraient une carte. | [Loi Hoguet, articles 3 et 4](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000512228/2026-08-22), article 4 depuis le 25/11/2018 : habilitation par le titulaire, qualité et étendue des pouvoirs. | `cabinet.profession.carte-professionnelle-garantie-assurance` : identifier au nom de qui l'on agit, le titulaire et le collaborateur habilité, puis vérifier les pouvoirs. |
| Facturation électronique : véritable contenu dédié non retrouvé. | [Fiche DGFiP « Je suis un syndic de copropriété »](https://www.impots.gouv.fr/sites/default/files/media/1_metier/2_professionnel/EV/2_gestion/290_facturation_electronique/fiches_reforme/fiche-syndiccorpo.pdf), septembre 2025 : assujettissement, syndic professionnel/non professionnel, réception, émission et e-reporting selon la qualité du client. | Dans `comptabilite.factures.les-mentions-obligatoires-d-une-facture`, identifier l'entité facturée, son assujettissement et la nature du flux. Ne pas transposer automatiquement le régime du cabinet à chaque syndicat ni assimiler un appel de charges à une facture. |
| Meublés touristiques : inventaire peu précis mais une carte existante couvre déjà la réforme. | [Article 26 d), loi de 1965](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000050623612), depuis le 21/11/2024 ; [QPC 2025-1186 du 19/03/2026](https://qpc360.conseil-constitutionnel.fr/2026-03-19/decision-2025-1186-qpc-19-mars-2026-0) : conformité retrouvée. | `immobilier.location.meuble-de-tourisme-et-reglement-de-copropriete` : vérifier règlement, conditions de l'interdiction, résidence principale et règles communales. `droit-veille-meuble-tourisme-condition-ouverture` expose déjà la condition d'ouverture, la majorité et la limite résidence principale : cette connaissance n'est pas absente de la banque. |

## Limites et éléments non retrouvés

- Le texte intégral de l'édition actuelle de la NF C 15-100 et le détail
  de tous ses champs de rénovation ne sont pas consultés. La correction
  retire un absolu ; elle ne fournit pas un manuel de contrôle électrique.
- L'INRS justifie les principes de prévention. Aucun texte n'a été
  retrouvé établissant une interdiction générale de visite de toiture
  pour un gestionnaire ; aucune interdiction de cette nature n'est ajoutée.
- Les cartes toiture retrouvées portent sur des ouvrages précis. Leur
  présence ne prouve pas les erreurs de compétence dénoncées dans le
  syllabus. Leurs seuils techniques ne sont pas tous revérifiés ici.
- Pas de carte retrouvée affirmant un TRV gaz actuel, une périodicité
  nationale de ravalement, une LCB-FT générale du seul syndic ou une remise
  intégrale de tout ancien à la dernière NF C 15-100.
- La recherche sur les meublés ne couvre pas les règlements de toutes les
  communes ni toute la jurisprudence. La décision constitutionnelle citée
  dans la carte est retrouvée, mais cela ne prouve pas chaque formulation
  de cette carte au-delà des points contrôlés.
- La fiche DGFiP sert à distinguer les entités et flux. Elle ne suffit
  pas à classer toutes les situations fiscales possibles des syndicats.
- Les sources institutionnelles ne sont pas infaillibles : pour la
  suspension du fonds, la conjonction et la décision sont relues dans
  l'article 14-2-1 II lui-même. Une simplification qui remplacerait le
  cumul par une alternative ne doit pas être reprise.

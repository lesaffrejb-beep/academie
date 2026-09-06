# Couverture éditoriale copro

Artefact local seulement ; rattachement thématique, pas couverture des objectifs ni expertise acquise.

Généré par `python3 app/couverture_expertises.py --write`. Ne pas éditer les compteurs.

Une carte valide ici signifie son statut dans l'artefact, pas une nouvelle revue du fond.
Les études sont comptées par statut déclaré dans les fichiers source ; les valideurs restent requis.

| Domaine | Chapitres prévus | Cartes artefact | N4/N5 servies localement | Études déclarées valides |
|---|---:|---:|---:|---:|
| Droit de la copropriété | 60 | 43 | 0 | 3 |
| Bâtiment et pathologie | 46 | 10 | 0 | 0 |
| Technique des équipements | 38 | 13 | 0 | 0 |
| Comptabilité et finances de copropriété | 41 | 10 | 0 | 0 |
| Sinistres et assurances | 29 | 6 | 0 | 0 |
| Procédure et justice | 33 | 11 | 0 | 0 |
| Travaux, marchés et lecture de plans | 32 | 0 | 0 | 0 |
| Énergie et rénovation | 29 | 0 | 0 | 0 |
| Propriété, immobilier et urbanisme | 32 | 0 | 0 | 0 |
| Le cabinet : déontologie, contrats, relation | 42 | 0 | 0 | 0 |
| Culture | 7 | 0 | 0 | 0 |

Cartes copro sans rattachement exact à un chapitre : 76.

## Spécialisations à construire

Les cartes rattachées peuvent se retrouver dans plusieurs spécialités : ne pas les additionner.
Ce compteur ne démontre pas que les objectifs ci-dessous sont couverts.

### Droit de la copropriété et stratégie contentieuse

Identifiant : `juriste-copro`. Statut : a-construire.

Objectifs : Qualifier une situation ambiguë et hiérarchiser les textes ; comparer des décisions avec des faits différents ; défendre puis réviser une solution contradictoire.

Production attendue : Note motivée sur un dossier fictif avec pièces manquantes, arguments adverses et options de recours.

Limite : Formation au raisonnement juridique, pas attribution d'un titre d'avocat.

Sources à instruire (pas une lecture attestée) : Légifrance dans une version datée ; Judilibre ; doctrine juridique à confronter aux décisions.

Branches communes : `droit.statut`, `droit.majorites`, `droit.organes`, `droit.assemblee`, `droit.responsabilites`, `procedure.contentieux-ag`.

46 chapitres thématiquement rattachés ; 17 cartes avec rattachement exact.

### Propriété, servitudes, volumes et foncier

Identifiant : `propriete-foncier`. Statut : a-construire.

Objectifs : Croiser titres, plans et usage réel ; distinguer propriété, jouissance et charge ; identifier le besoin d'un géomètre ou d'un notaire.

Production attendue : Dossier de divergence entre titre, plan et occupation avec arbre des hypothèses.

Limite : Un plan pédagogique ne délimite pas une propriété réelle.

Sources à instruire (pas une lecture attestée) : Code civil ; publications notariales ; référentiels de géomètres à instruire.

Branches communes : `immobilier.propriete`, `droit.charges`, `immobilier.vente`.

18 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Urbanisme opérationnel et patrimoine

Identifiant : `urbanisme-patrimoine`. Statut : a-construire.

Objectifs : Séparer règlement, recommandation et diagnostic ; instruire la compatibilité d'un projet ; construire des variantes et leur chemin d'autorisation.

Production attendue : Note de faisabilité patrimoniale et dossier de questions à l'urbanisme sur des pièces fictives.

Limite : Le cahier d'Angers ne remplace pas le règlement ; toute conclusion locale nécessite les pièces actuelles.

Sources à instruire (pas une lecture attestée) : PSMV et PLUi opposables à retrouver ; cahier de recommandations Angers 707940074f138868 ; Code de l'urbanisme.

Branches communes : `immobilier.urbanisme`, `immobilier.local`, `travaux.urbanisme-des-travaux`.

12 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Droit des entreprises et contrats

Identifiant : `entreprises`. Statut : a-construire.

Objectifs : Lire pouvoirs et engagements d'une société ; repérer les risques de défaillance d'un cocontractant ; organiser la continuité contractuelle.

Production attendue : Dossier d'entreprise de travaux défaillante : pièces, responsabilités, options et consultations nécessaires.

Limite : Les fragments SCI existants ne couvrent pas ce cursus ; pas de conseil sur une entreprise réelle.

Sources à instruire (pas une lecture attestée) : Code de commerce ; Code civil ; ressources INPI et Bpifrance Création à rechercher.

Branches communes : `immobilier.acteurs-et-formes`, `travaux.marche-prive`, `procedure.organisation`.

14 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Pathologie du bâtiment et diagnostic différentiel

Identifiant : `pathologie`. Statut : a-construire.

Objectifs : Séparer symptôme et cause ; proposer des hypothèses concurrentes ; choisir une investigation discriminante.

Production attendue : Rapport de désordre avec chronologie, schémas originaux, incertitudes et protocole d'investigation.

Limite : Pas de diagnostic de sécurité à distance ni de conclusion structurelle sans examen compétent.

Sources à instruire (pas une lecture attestée) : AQC ; Cerema ; CSTB ; ouvrages dont les droits restent à vérifier.

Branches communes : `pathologie.structure`, `pathologie.humidite`, `pathologie.facades`, `pathologie.visite`.

22 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Structure, fondations et géotechnique

Identifiant : `structure-geotechnique`. Statut : a-construire.

Objectifs : Lire le chemin des charges ; distinguer mouvement de structure et altération de surface ; cadrer une mission d'étude.

Production attendue : Dossier fictif de fissuration avec lectures alternatives et demande argumentée au bureau d'études.

Limite : Aucun dimensionnement exécutable ni consigne d'étaiement sans professionnel compétent.

Sources à instruire (pas une lecture attestée) : Cerema ; AQC ; guides BRGM ; normes et notices accessibles légalement.

Branches communes : `pathologie.structure`, `pathologie.materiaux`, `travaux.plans`.

19 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Couverture, charpente et zinguerie

Identifiant : `couverture`. Statut : a-construire.

Objectifs : Lire la continuité d'évacuation des eaux ; repérer les interfaces entre ouvrages ; comparer réparations ponctuelles et réfection.

Production attendue : Analyse annotée d'une toiture fictive, comparaison de devis et grille de réception.

Limite : Apprentissage de lecture et de contrôle documentaire, pas habilitation au travail en hauteur.

Sources à instruire (pas une lecture attestée) : AQC ; cahier Angers 707940074f138868 ; DTU à consulter sous licence.

Branches communes : `pathologie.toitures`, `pathologie.materiaux`, `travaux.chantier`.

17 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Étanchéité, terrasses et interfaces

Identifiant : `etancheite`. Statut : a-construire.

Objectifs : Reconstituer un complexe de toiture-terrasse ; distinguer défaut d'étanchéité, condensation et évacuation ; examiner points singuliers et garanties.

Production attendue : Contre-analyse de sinistre de terrasse avec coupes, hypothèses et exigences de preuve.

Limite : Pas de prescription de complexe ou d'essai destructif sans étude adaptée.

Sources à instruire (pas une lecture attestée) : AQC ; CSTB ; règles professionnelles et DTU avec accès à vérifier.

Branches communes : `pathologie.toitures`, `pathologie.humidite`, `travaux.marche-prive`.

16 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Façades, matériaux anciens et restauration

Identifiant : `facades`. Statut : a-construire.

Objectifs : Identifier la logique constructive d'une façade ; comparer compatibilités des interventions ; relier eau, matériaux et usages.

Production attendue : Avis comparatif sur interventions de façade à partir de relevés et d'une coupe fictifs.

Limite : Identification sur image incertaine ; recommandations patrimoniales distinctes de prescriptions de chantier.

Sources à instruire (pas une lecture attestée) : Cahier Angers 707940074f138868 ; AQC ; Cerema ; référentiels patrimoniaux.

Branches communes : `pathologie.facades`, `pathologie.materiaux`, `pathologie.epoques`.

18 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Électricité, protections et lecture de schémas

Identifiant : `electricite`. Statut : a-construire.

Objectifs : Lire un schéma fonctionnel ; interroger la cohérence des protections et des usages ; prioriser les suites d'un rapport.

Production attendue : Analyse d'un rapport fictif, schéma commenté et demande de clarification à l'entreprise.

Limite : Aucun geste sous tension, aucune habilitation attribuée par l'application.

Sources à instruire (pas une lecture attestée) : INRS ; normes AFNOR sous licence ; textes officiels datés ; notices constructeurs.

Branches communes : `equipements.electricite`, `energie.irve`, `equipements.contrats`.

12 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Plomberie, réseaux d'eau et assainissement

Identifiant : `plomberie`. Statut : a-construire.

Objectifs : Tracer les réseaux et leurs responsabilités ; différencier fuite, refoulement et condensation ; lire un protocole de recherche et un devis.

Production attendue : Dossier de fuite intermittente : plan, chronologie, investigations comparées et décision conditionnelle.

Limite : Pas de manœuvre ni de protocole sanitaire exécuté à partir d'un exercice.

Sources à instruire (pas une lecture attestée) : AQC ; Cerema ; règlements sanitaires datés ; notices techniques.

Branches communes : `equipements.plomberie`, `sinistres.degat-des-eaux`, `equipements.contrats`.

14 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Chauffage collectif, hydraulique et régulation

Identifiant : `chauffage`. Statut : a-construire.

Objectifs : Lire une installation hydraulique ; relier températures, débits et régulation ; distinguer panne, réglage et défaut de conception.

Production attendue : Analyse d'une chaufferie fictive avec mesures contradictoires et plan de vérification de performance.

Limite : Ni qualification de chauffagiste ni autorisation d'intervenir sur gaz ou pression.

Sources à instruire (pas une lecture attestée) : ADEME ; Cerema ; notices d'équipements ; guides techniques à acquérir.

Branches communes : `equipements.chauffage`, `energie.chauffage-collectif`, `equipements.contrats`.

19 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Climatisation, pompes à chaleur et froid

Identifiant : `climatisation`. Statut : a-construire.

Objectifs : Comprendre un cycle et ses limites ; comparer confort d'été passif et systèmes actifs ; cadrer bruit, implantation et maintenance.

Production attendue : Comparatif technique argumenté de solutions avec conditions de fonctionnement et points non démontrés.

Limite : Branche dédiée manquante dans le programme actuel ; aucune qualification fluides frigorigènes.

Sources à instruire (pas une lecture attestée) : ADEME ; Cerema ; notices ; références sur fluides et acoustique à instruire.

Branches communes : `equipements.chauffage`, `energie.physique`, `energie.chauffage-collectif`.

19 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Ventilation, qualité de l'air et confort

Identifiant : `ventilation`. Statut : a-construire.

Objectifs : Lire les transferts d'air ; relier rénovation, usage et humidité ; interpréter des mesures sans confondre corrélation et cause.

Production attendue : Dossier de moisissures après travaux avec hypothèses et programme de mesures.

Limite : Pas de diagnostic sanitaire individuel ni de conclusion depuis une photo seule.

Sources à instruire (pas une lecture attestée) : Cerema ; ADEME ; INRS ; AQC.

Branches communes : `equipements.ventilation`, `pathologie.humidite`, `energie.physique`.

14 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Énergétique, économie et mesure de performance

Identifiant : `energie-modelisation`. Statut : a-construire.

Objectifs : Distinguer calcul conventionnel et consommation observée ; tester la sensibilité d'une rentabilité ; expliciter les hypothèses exclues d'un modèle.

Production attendue : Note de décision comparant intérêts privés et collectifs, incertitudes et résultats mesurés.

Limite : Un modèle agrégé ne prescrit pas les travaux d'un immeuble ; hypothèses historiques à dater.

Sources à instruire (pas une lecture attestée) : CAE Focus 322a2f5e843f45b9 ; ADEME ; SDES ; méthodologies DPE datées.

Branches communes : `energie.physique`, `energie.dpe`, `energie.audit-et-ppt`, `energie.chauffage-collectif`.

17 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Amiante, DTA et lecture critique de rapports

Identifiant : `diagnostics-amiante`. Statut : a-construire.

Objectifs : Distinguer objet, périmètre et limites d'un rapport ; repérer une pièce absente ; organiser l'interface entre diagnostic et projet de travaux.

Production attendue : Audit documentaire d'un dossier fictif avec questions au diagnostiqueur et points d'arrêt.

Limite : Pas de prélèvement, repérage réglementaire certifié ou intervention sur amiante enseigné comme geste autonome.

Sources à instruire (pas une lecture attestée) : INRS ; ministère chargé de la santé ; textes officiels et référentiels de certification à vérifier.

Branches communes : `pathologie.diagnostics`, `travaux.du-besoin-au-devis`, `travaux.chantier`.

14 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Plomb, CREP et risques sanitaires

Identifiant : `diagnostics-plomb`. Statut : a-construire.

Objectifs : Lire le périmètre et les résultats d'un constat ; distinguer constat, risque et action ; préparer une consultation compétente.

Production attendue : Contrôle critique d'un CREP fictif et dossier de coordination avant travaux.

Limite : Pas de certification de diagnostiqueur ni d'instructions d'exposition ou de prélèvement.

Sources à instruire (pas une lecture attestée) : Ministère chargé de la santé ; INRS ; textes officiels et méthodes en vigueur à rechercher.

Branches communes : `pathologie.diagnostics`, `pathologie.materiaux`, `travaux.chantier`.

16 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Architecture, maîtrise d'œuvre et AMO

Identifiant : `architecture-amo`. Statut : a-construire.

Objectifs : Transformer un besoin en programme ; comparer des variantes ; organiser rôles, interfaces, réception et suivi.

Production attendue : Dossier AMO de rénovation patrimoniale, pièces attendues et arbitrages entre coût, usage et conservation.

Limite : Pas attribution du titre d'architecte ; conception et maîtrise d'œuvre réelles à confier aux intervenants compétents.

Sources à instruire (pas une lecture attestée) : Cerema ; ANAH ; cahier Angers 707940074f138868 ; guides de maîtrise d'ouvrage.

Branches communes : `travaux.plans`, `travaux.renovation-globale`, `travaux.du-besoin-au-devis`, `travaux.chantier`.

18 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Économie de la construction et achats

Identifiant : `economie-construction`. Statut : a-construire.

Objectifs : Décomposer une offre ; repérer exclusions, quantités et interfaces ; comparer coût initial et coût d'usage.

Production attendue : Tableau de comparaison de devis fictifs avec réserves, variantes et négociation argumentée.

Limite : Les prix d'exercice sont fictifs, jamais des références de marché actuelles.

Sources à instruire (pas une lecture attestée) : Guides de maîtrise d'ouvrage ; contrats types à vérifier ; retours AQC.

Branches communes : `travaux.du-besoin-au-devis`, `travaux.marche-prive`, `comptabilite.factures`.

13 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Comptabilité, contrôle et audit

Identifiant : `comptabilite-audit`. Statut : a-construire.

Objectifs : Reconstituer des écritures et leurs pièces ; rapprocher trésorerie et engagements ; expliquer les anomalies et leurs corrections possibles.

Production attendue : Dossier comptable fictif complet avec rapprochements, annexes et note de contrôle contradictoire.

Limite : La comptabilité du syndicat ne se confond pas avec celle du cabinet ; aucun titre d'expert-comptable attribué.

Sources à instruire (pas une lecture attestée) : Textes comptables de copropriété ; ANC pour le périmètre entreprise à distinguer ; doctrine professionnelle.

Branches communes : `comptabilite.plan-comptable`, `comptabilite.annexes`, `comptabilite.controle`, `comptabilite.budget`.

22 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Recouvrement, sûretés et prévention des impayés

Identifiant : `recouvrement`. Statut : a-construire.

Objectifs : Fiabiliser la créance et les pièces ; comparer stratégies amiables et contentieuses ; intégrer solvabilité, coûts et temporalité.

Production attendue : Plan de recouvrement fictif avec variantes, preuves manquantes et contradiction.

Limite : Aucune décision réelle contre un débiteur ni promesse de résultat judiciaire.

Sources à instruire (pas une lecture attestée) : Légifrance ; Judilibre ; ANIL ; justice.fr.

Branches communes : `comptabilite.impayes`, `procedure.recouvrement`, `procedure.avant-le-proces`.

13 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Assurances et expertise contradictoire

Identifiant : `assurance-expertise`. Statut : a-construire.

Objectifs : Séparer causalité, responsabilité et garantie ; lire exclusions et conventions ; préparer une contradiction étayée.

Production attendue : Dossier de sinistre fictif : chronologie, tableau de garanties et questions à l'expert.

Limite : Les conventions ne sont pas des lois ; couverture d'un contrat réel non inférée.

Sources à instruire (pas une lecture attestée) : Code des assurances ; Code civil ; contrats et conventions avec nature et date.

Branches communes : `sinistres.contrat`, `sinistres.construction`, `sinistres.expertise`, `procedure.contentieux-batiment`.

14 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Sociologie de l'habitat et action collective

Identifiant : `sociologie`. Statut : a-construire.

Objectifs : Analyser intérêts, ressources et représentations ; distinguer observation et jugement ; étudier les blocages de décision.

Production attendue : Enquête fictive avec carte d'acteurs, hypothèses alternatives et démarche de concertation.

Limite : Pas de profilage psychologique des habitants ni de généralisation depuis un seul cas.

Sources à instruire (pas une lecture attestée) : Recherche académique à sélectionner ; travaux sur les communs ; PDHH 8760dfb3f168df2d comme contexte historique.

Branches communes : `culture.lectures`, `cabinet.conseil-syndical`, `cabinet.negocier`, `immobilier.local`.

17 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Copropriétés fragiles, habitat dégradé et accompagnement

Identifiant : `habitat-fragile`. Statut : a-construire.

Objectifs : Relier dégradation technique et financière ; distinguer aides, acteurs et procédures ; séquencer une stratégie soutenable.

Production attendue : Dossier transversal fictif de copropriété fragile avec diagnostic partagé et scénarios.

Limite : Le PDHH 2020-2025 n'établit pas les aides ni orientations en vigueur en 2026.

Sources à instruire (pas une lecture attestée) : ANAH ; ANIL ; PDHH 8760dfb3f168df2d ; textes actualisés à retrouver.

Branches communes : `comptabilite.impayes`, `immobilier.local`, `cabinet.cas-transverses`, `travaux.renovation-globale`.

22 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Direction d'agence immobilière

Identifiant : `direction-agence`. Statut : a-construire.

Objectifs : Relier capacité, qualité et rentabilité ; arbitrer recrutement, portefeuille et risque ; construire un contrôle interne.

Production attendue : Revue de direction fictive avec compte d'exploitation, charge et plan d'action contradictoire.

Limite : Le programme actuel ne couvre pas une formation de direction complète.

Sources à instruire (pas une lecture attestée) : Référentiels professionnels ; droit social et déontologie à vérifier ; littérature de gestion.

Branches communes : `cabinet.charge`, `comptabilite.honoraires`, `cabinet.profession`, `cabinet.contrat-de-syndic`.

13 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Direction régionale et pilotage de réseau

Identifiant : `direction-regionale`. Statut : a-construire.

Objectifs : Comparer agences sans masquer leurs contextes ; diagnostiquer un problème d'organisation ; piloter intégration et qualité.

Production attendue : Arbitrage fictif entre agences avec ressources limitées, risques et indicateurs vérifiables.

Limite : Pas d'évaluation RH réelle ni de classement des élèves ; données d'entreprise uniquement fictives.

Sources à instruire (pas une lecture attestée) : Littérature de gestion ; droit social ; contrôle interne et gouvernance à instruire.

Branches communes : `cabinet.charge`, `cabinet.cas-transverses`, `comptabilite.honoraires`.

15 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Entrepreneuriat et direction de proptech

Identifiant : `proptech`. Statut : a-construire.

Objectifs : Vérifier un problème utilisateur ; construire et tester un modèle économique ; arbitrer architecture, données, distribution et risques.

Production attendue : Dossier de lancement fictif avec hypothèses falsifiables, prototype, économie unitaire et risques.

Limite : Aucune branche produit complète aujourd'hui ; pas de promesse de viabilité ou de financement.

Sources à instruire (pas une lecture attestée) : Bpifrance Création ; INPI ; CNIL ; documentation technique primaire à sélectionner.

Branches communes : `cabinet.donnees`, `cabinet.profession`, `comptabilite.honoraires`.

12 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Management, droit social et personnel d'immeuble

Identifiant : `rh-social`. Statut : a-construire.

Objectifs : Distinguer employeur, mandataire et intervenant ; analyser charge et organisation ; préparer une décision documentée.

Production attendue : Cas fictif d'organisation du travail avec risques, dialogue et vérifications juridiques.

Limite : Pas de décision sur un salarié réel ni de conseil individuel sans pièces.

Sources à instruire (pas une lecture attestée) : Code du travail ; convention collective applicable ; INRS.

Branches communes : `cabinet.charge`, `cabinet.profession`, `droit.responsabilites`.

13 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Incendie, accessibilité et sécurité d'usage

Identifiant : `incendie-accessibilite`. Statut : a-construire.

Objectifs : Identifier le périmètre d'une vérification ; lire cheminements et interfaces ; prioriser la consultation de spécialistes.

Production attendue : Audit documentaire fictif avec plan annoté, inconnues et circuit de décision.

Limite : Aucun avis de conformité ni protocole de secours opérationnel depuis l'application.

Sources à instruire (pas une lecture attestée) : Textes officiels datés ; Cerema ; INRS ; guides publics.

Branches communes : `equipements.acces`, `travaux.plans`, `pathologie.visite`, `sinistres.autres-sinistres`.

16 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Acoustique et nuisances

Identifiant : `acoustique`. Statut : a-construire.

Objectifs : Distinguer source, transmission et réception ; organiser la collecte des observations ; comparer mesures et solutions proposées.

Production attendue : Dossier de nuisance fictive avec hypothèses, conditions de mesure et critique de devis.

Limite : Pas de conclusion de conformité sonore sans mesures et contexte appropriés.

Sources à instruire (pas une lecture attestée) : Cerema ; CSTB ; textes officiels ; méthodes de mesure sous licence.

Branches communes : `energie.physique`, `equipements.chauffage`, `immobilier.propriete`.

22 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Adaptation climatique, eau et résilience

Identifiant : `resilience`. Statut : a-construire.

Objectifs : Relier exposition, vulnérabilité et conséquences ; comparer adaptations et effets secondaires ; organiser une stratégie révisable.

Production attendue : Scénarios fictifs chaleur, eau et retrait-gonflement avec priorisation multicritère.

Limite : Une carte de risque ne diagnostique pas un bâtiment particulier.

Sources à instruire (pas une lecture attestée) : BRGM ; Géorisques ; Cerema ; ADEME.

Branches communes : `energie.physique`, `pathologie.structure`, `sinistres.autres-sinistres`, `immobilier.urbanisme`.

22 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Ascenseurs et équipements de sécurité

Identifiant : `ascenseurs`. Statut : a-construire.

Objectifs : Lire fonctions et interfaces ; comparer maintenance et modernisation ; exploiter les rapports de contrôle.

Production attendue : Audit d'un contrat et d'un historique de pannes fictifs avec stratégie de suivi.

Limite : Pas de dépannage, déverrouillage ou manipulation autonome enseigné.

Sources à instruire (pas une lecture attestée) : Textes officiels ; notices ; référentiels de contrôle accessibles légalement.

Branches communes : `equipements.ascenseurs`, `equipements.acces`, `equipements.contrats`.

13 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Données, cybersécurité, fraude et IA

Identifiant : `donnees-fraude`. Statut : a-construire.

Objectifs : Vérifier provenance et droits d'accès ; détecter une demande frauduleuse ; évaluer une sortie IA contre des pièces.

Production attendue : Dossier fictif de fraude documentaire et test d'un assistant avec journal de preuves.

Limite : Pas d'envoi de données clients à un tiers ; l'IA n'est pas un arbitre de vérité.

Sources à instruire (pas une lecture attestée) : CNIL ; ANSSI ; documentation technique primaire ; jeux d'essai fictifs.

Branches communes : `cabinet.donnees`, `comptabilite.controle`, `cabinet.ecrire`.

12 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

### Mesure, statistiques et raisonnement causal

Identifiant : `raisonnement-mesure`. Statut : a-construire.

Objectifs : Distinguer mesure, estimation et hypothèse ; analyser biais et ordres de grandeur ; réviser une décision face à une donnée contradictoire.

Production attendue : Critique d'une étude et analyse de sensibilité reproductible sur données fictives.

Limite : La corrélation ne démontre pas la cause ; aucune certitude fabriquée par un score.

Sources à instruire (pas une lecture attestée) : CAE Focus 322a2f5e843f45b9 ; INSEE ; ressources académiques méthodologiques.

Branches communes : `energie.physique`, `comptabilite.controle`, `culture.lectures`.

15 chapitres thématiquement rattachés ; 0 cartes avec rattachement exact.

## Empreintes des entrées

Ces empreintes permettent de détecter un rapport périmé ; elles ne prouvent pas un déploiement.

- `programme/specialisations/copro.json` : `95a354a08c5cd2e2c4f214e3c2650fdb6d723651fd4576cae0d91d32f01fcd4e`
- `programme/copro.json` : `efc14236cd110113d731c4faa368ce93168f9d07d95b9d53816e6eb5ca65a5e3`
- `site/banque.json` : `55ed50f27079e1c023b846f7bc35b32c36294d65028f1dd44df3594e39b55791`
- `chapitres/droit/assemblee/le-proces-verbal-et-sa-notification.json` : `faa5bf6ebcb8ee0f883c1c0bb39b61e1b36a60a9151e3d1cddad9b3018a7fd1f`
- `chapitres/droit/majorites/l-article-24.json` : `af20ad4fac670a7f8d7b1f4b673d7221885e576d185b59e251551082173ef666`
- `chapitres/droit/organes/le-syndic-et-ses-missions.json` : `0a3f3d58336801c8800ff93bc7d9d6f30485c84f6c00d9ee1c785be5f174c27f`
- `chapitres/methodes/communication/les-transmissions-orales.json` : `6590ce1919d3ef8c3f2f1a19e9f8ee42f9de0d12026ae20b2b26c4b1d4237b1a`
- `chapitres/pharmaco/securite/les-cinq-b.json` : `57bb78a0d4ff8e3e31dc858ffdff1ffe1a8cd605e468a60a5e9a1f71532a24cf`
- `chapitres/satellites/chaudiere-hybride.json` : `ed41ed2068945f0061e8ab7c2984ba6c446e2ea0ef313ad117e4cd74b1453845`

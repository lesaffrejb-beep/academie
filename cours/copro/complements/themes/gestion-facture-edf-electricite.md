# Lire et contrôler la facture EDF des parties communes

Statut : brouillon éditorial
Auteur : Codex / GPT-6 / acces_profils-2026-09-06
Domaine sources : comptabilite

## Partir du compteur, de la période et du contrat

Ce complément apprend à reconstituer une facture d’électricité de copropriété et à distinguer variation de prix, volume et régularisation. EDF est ici un fournisseur possible ; son nom ne prouve ni une offre réglementée ni un tarif particulier. Le chapitre propriétaire [C:energie.contrats-energie.gaz-et-electricite-pour-un-immeuble] porte le choix du contrat. Celui-ci doit être rapproché du point de livraison et des usages réellement alimentés : éclairage, ascenseur, ventilation, pompes ou autre équipement collectif. Un montant global de portefeuille ne permet pas de contrôler la facture d’un syndicat.

La facture présente abonnement, consommation, taxes et éventuels services. La puissance souscrite exprimée en kVA caractérise une capacité disponible ; les kWh mesurent une quantité d’énergie consommée. Les plages tarifaires peuvent avoir des prix différents. [S:edf-composantes] Il faut conserver unités et périodes : multiplier une puissance souscrite par le prix du kWh ne calcule pas une facture. Un appareil consommant fictivement une puissance constante de 1 kW pendant 10 heures utilise 10 kWh ; cela ne décrit pas la consommation d’un ascenseur dont le fonctionnement varie.

## Deux lectures qui ne doivent pas être additionnées

Économiquement, le prix rémunère la fourniture et l’accès aux réseaux, puis supporte la fiscalité. Le TURPE est le tarif d’utilisation des réseaux publics d’électricité ; dans une présentation intégrée, l’acheminement se répartit entre abonnement et consommation. Une mention « dont acheminement » précise une composante déjà comprise. La CTA repose sur la part fixe de l’acheminement ; l’accise est liée à la consommation, et la TVA constitue une autre couche. [S:edf-composantes] Une facture ou un contrat avec acheminement séparé doit être lu selon sa structure réelle : on n’ajoute pas automatiquement un second coût réseau.

La CRE distingue les coûts de réseau et ceux propres au fournisseur. Elle rappelle aussi que les offres dites fixes peuvent figer des périmètres différents : seule énergie ou certains prix hors taxes. Une promesse de prix fixe ne garantit donc pas un total annuel TTC constant lorsque consommation ou taxes changent. Sa présentation actuelle indique une TVA de 20 % sur les composantes électriques considérées ici. [S:cre-electricite] Aucun taux d’accise ni montant de CTA ci-dessous n’est présenté comme un barème applicable à tout syndicat ; leur catégorie, période et assiette doivent être contrôlées.

Les anciennes factures sont des preuves historiques, pas des modèles fiscaux actuels. La CRE rappelle l’intégration des anciennes taxes locales dans le dispositif national ; recopier leurs lignes en plus de l’accise actuelle peut créer un doublon. [S:cre-electricite] Un changement de prix au milieu d’une période peut aussi nécessiter plusieurs segments de calcul. [S:edf-facture]

## Cas fictif : reconstituer une facture et son solde

Une copropriété reçoit une facture pédagogique sans service supplémentaire. Hypothèses inventées pour le calcul : abonnement sur la période 60 € HT ; 900 kWh en heures pleines à 0,20 €/kWh HT ; 300 kWh en heures creuses à 0,15 €/kWh HT ; CTA affichée 6 € ; accise affichée 36 €. Les prix incluent déjà l’acheminement selon le contrat fictif. La facture mentionne aussi « dont acheminement : 70 € ». Deux acomptes déjà réglés totalisent 240 € TTC.

Correction : la consommation représente 900 × 0,20 + 300 × 0,15 = 225 € HT. Abonnement et consommation totalisent 285 €. Ajouter CTA et accise donne une base de 327 €. Sous l’hypothèse de TVA à 20 % correspondant au régime décrit, la TVA vaut 65,40 € et la facture 392,40 € TTC. Les 70 € signalés par « dont » ne s’ajoutent pas. Le solde après les 240 € réglés vaut 152,40 €. Chaque étape répond à une question différente : coût de fourniture facturé, fiscalité, dette totale et somme restant à payer.

Un conseil syndical compare les 152,40 € à la facture précédente de 300 € et annonce une forte économie. Cette conclusion est fausse : il compare un solde après acomptes à un coût de période. Il faut comparer des périodes, volumes, prix et périmètres équivalents. [C:comptabilite.bases.engagement-et-tresorerie] explique cette différence entre charge et paiement.

## Diagnostiquer l’écart avant de l’imputer aux usages

La facture distingue les consommations issues d’index et leur nature relevée ou estimée. [S:edf-facture] Si l’index précédent était sous-estimé, une facture de régularisation élevée peut rattraper une consommation ancienne. Cela ne démontre pas une panne récente. Inversement, un prix stable n’exclut pas une dérive réelle du volume. Le gestionnaire rapproche index, dates, historique des usages et éventuels travaux, puis formule une demande ciblée au fournisseur.

Transfert : la facture augmente alors que les kWh baissent et qu’un nouveau service apparaît. Attendus : isoler prix unitaire, part fixe, fiscalité, durée et service ; contrôler sa souscription ; calculer le coût comparable avant de conclure. Contre-argument à traiter : diminuer la puissance sans examiner les appels des équipements peut être une fausse économie. Le choix exige les données techniques et contractuelles utiles.

Les rubriques P1 à P5 d’un contrat de chauffage ne sont pas les taxes ni les lignes universelles d’une facture EDF. Leur contenu relève de [C:equipements.chauffage.les-contrats-p1-a-p5]. Schéma à faire pour montrer les deux lectures d’une facture sans compter deux fois l’acheminement ; aucun visuel n’est produit dans ce brouillon.

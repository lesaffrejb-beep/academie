# REGISTRE DES SOURCES, domaine copropriété

Ouvert le 02/09/2026, rempli le 03/09/2026 par le chantier
`ACA-SOURCES-1` depuis les 84 cartes de `banque/` et le tri NotebookLM.
Une ligne par source. Nature et parti selon `decisions/0004`, fiabilité
selon `sources/README.md`. Une source sans ligne ici ne fonde aucune
carte.

Ce fichier est **régénéré**, il ne se corrige pas à la main :
`sources/registre.json` fait foi, `python3 app/registre.py --md` produit
la page, et `python3 app/tests_sources.py` refuse le jour où les deux
divergent.

Une cellule « Vérifié le » vide dit « à vérifier » : la source est
connue, son texte n'a pas été lu à la source.

| Source | Domaine web ou référence | Nature | Parti | Fiabilité | Vérifié le | On en tire | On n'en tire pas |
|---|---|---|---|---|---|---|---|
| Légifrance : loi n° 65-557 du 10 juillet 1965, décret n° 67-223 du 17 mars 1967, décret n° 2005-240 et arrêté du 14 mars 2005, code civil, code de la construction et de l'habitation, code de procédure civile, code des procédures civiles d'exécution, code des assurances | legifrance.gouv.fr | texte-officiel |  | A | 2026-08-28 | toute règle de droit de la copropriété, dans sa version en vigueur datée | une version abrogée servie comme le droit d'aujourd'hui |
| Judilibre (Cour de cassation) | courdecassation.fr | jurisprudence |  | A | 2026-08-28 | lectures d'arrêt, règles de principe, avec la référence complète | une interprétation sans l'arrêt, un pourvoi non recoupé |
| ANIL et les ADIL | anil.org | institution |  | A | 2026-08-28 | fiches pratiques datées | un chiffre sans date |
| Service-public.fr | service-public.fr | institution |  | A | 2026-08-28 | démarches, délais | rien |
| ADEME | ademe.fr | institution |  | A | 2026-08-28 | énergie, rénovation | un prix (péremption) |
| ANAH et France Rénov' | anah.gouv.fr | institution |  | A | 2026-08-28 | les aides, avec péremption obligatoire | un montant sans date |
| Ministère de la transition écologique | ecologie.gouv.fr | institution |  | A | 2026-08-28 | diagnostic de performance énergétique, calendriers, plan pluriannuel de travaux | un barème sans sa date d'entrée en vigueur |
| Agences régionales de santé | ars.sante.fr | institution |  | A | 2026-08-28 | risque sanitaire des installations collectives, dont la légionelle | une consigne locale servie comme une règle nationale |
| Fiches pathologie bâtiment de l'Agence Qualité Construction | qualiteconstruction.com | norme |  | A | 2026-08-28 | le texte : constat, diagnostic, bonnes pratiques | aucune image (mentions légales) |
| Cerema | cerema.fr | institution |  | A | 2026-09-02 | guides techniques, dont les réseaux de chaleur | rien |
| Normes NF DTU (AFNOR, CSTB) | référence citée, texte non librement consultable | norme |  | A | 2026-08-28 | la référence et la règle de l'art telle que la doctrine la résume | aucune recopie du texte, qui est payant et non consultable |
| Convention IRSI (France Assureurs) | franceassureurs.fr, convention inter-assureurs non publiée | organisation-pro | défend les assureurs | B | à vérifier | le partage des sinistres dégât des eaux, recoupé le 28/08/2026 sur des sources professionnelles concordantes | une interprétation sans le texte, qui n'a pas été lu à la source |
| Grilles et radars de méthode de JB (relecture des comptes, conformité annuelle, urgence sinistre) | méthode maison, non publiée | terrain |  | C | 2026-08-28 | un ordre de lecture, une liste de contrôle, un réflexe de gestionnaire | une règle de droit ni un chiffre : ils se citent au texte officiel |
| Référentiel d'exploitation en copropriété (carnet documentaire de JB) | source non retrouvée à ce jour | editeur |  | C | à vérifier | l'usage des marchés d'exploitation de chauffage (P1 à P5), à recouper | rien d'opposable : à remplacer par un guide Cerema ou un NF DTU dès qu'il est retrouvé |
| Immocampus (portail de formation de l'employeur) | interne | support-interne |  | B | 2026-08-28 | une paraphrase, en couche interne seulement | toute recopie, toute distribution |
| Formation interne de l'employeur sur les espaces clients (transcription, 2026) | interne | support-interne |  | C | 2026-09-03 | une paraphrase en couche interne pour JB seul ; une notion générique passe au chapitre public avec une source publique | tout nom, toute capture, toute recopie ; jamais servi à un autre joueur |
| Cahier de recommandations du PSMV d'Angers (10 fiches-conseil, Angers Loire Métropole, 2023) | angersloiremetropole.fr | institution |  | A | 2026-09-03 | vocabulaire et pathologies du bâti ancien angevin, règles du site patrimonial ; dessins de Viollet-le-Duc (domaine public) réutilisables | les photos et dessins de l'agence (droits réservés) |
| Focus n° 106 du Conseil d'analyse économique, « Analyse socio-économique de la rénovation énergétique des logements » (juin 2024) | cae-eco.fr | institution |  | A | 2026-09-03 | coûts, bénéfices, valeur inobservée, rénovation performante contre par gestes (niveau IV) | ses chiffres au-delà de 2024 sans revérification |
| Plan départemental de l'habitat et de l'hébergement de Maine-et-Loire 2020-2025 | maine-et-loire.gouv.fr | institution |  | A | 2026-09-03 | méthode et orientations : habitat indigne, précarité énergétique, copropriétés fragiles du 49 | ses chiffres (période close) ; ses actions comme des règles |
| Éditeurs de logiciel, cabinets, courtiers, blogs commerciaux | divers | editeur | vend la prestation décrite | C | à vérifier | une piste à recouper | une carte servie sur cette seule source |
| Fédérations et syndicats de professionnels (FNAIM, UNIS, Plurience) | divers | organisation-pro | défend les syndics | B | à vérifier | la position, nommée comme telle | une règle de droit |
| Associations de copropriétaires et de consommateurs (ARC, UFC-Que Choisir, CLCV) | divers | association | défend les copropriétaires | B | à vérifier | la position, nommée comme telle | une règle de droit |

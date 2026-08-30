# INDEX-NOTEBOOKLM — ce que contient le carnet « Copropriété »

Relevé le 29/08/2026 en lisant le panneau Sources du carnet, **sans passer par
le modèle** : les titres sortent tels que Google les affiche, aucune
reformulation, aucun quota consommé. Doctrine d'usage du carnet :
[CORPUS.md](CORPUS.md) § 4. Données brutes :
[notebooklm-sources-brut.json](notebooklm-sources-brut.json).

Régénérer :

```bash
cd ~/.agents/skills/notebooklm && ./.venv/bin/python -u scripts/dump_sources.py \
  --notebook-url "https://notebook.google.com/notebook/567a033f-6a53-4321-a741-912f722403ea" \
  --out ~/Documents/Code/erp/academie/notebooklm-sources-brut.json
python3 app/index_notebooklm.py
```

## Le compte

L'interface annonce **300 sources**, et le carnet affiche « a atteint la
limite de sources » : il est plein, une source de plus suppose d'en retirer
une. Le relevé trouve **294 titres distincts**, donc **6 doublons**
(même titre déposé deux fois).

À noter : interrogé sur lui-même, le carnet a répondu « 278 sources ». Il se
trompe sur son propre contenu. C'est la première raison de ne jamais lui
faire compter ou inventorier quoi que ce soit : on lit le panneau, on ne
demande pas.

## Par nature de support

| Support | Nombre |
|---|---|
| web | 189 |
| pdf | 86 |
| markdown | 17 |
| youtube | 2 |

Les 17 fichiers markdown sont les « Essentiels métier » : de la
documentation interne d'employeur. **Le carnet est marqué « Public »** dans
son en-tête. À trancher par JB avant tout autre usage : du support interne
Sergic dans un carnet partageable par lien, ce n'est pas une question
d'Académie, c'est une question de confidentialité.

## Par nature de la source web (189 sources, 148 domaines)

| Nature | Nombre |
|---|---|
| Éditeur, cabinet ou blog commercial | 157 |
| Officiel ou institutionnel | 18 |
| Associatif, consommateur ou revue | 10 |
| Droit étranger (Québec / Canada) | 4 |

Classement **mécanique**, lu sur le nom de domaine et non sur le contenu :
il dit où regarder en premier, il ne tamponne rien.

Deux lectures qui comptent pour l'Académie :

1. **Le commercial domine.** C'est cohérent avec ce qu'on a observé au test
   du 29/08 : sur le fonds de travaux, la réponse était juste mais sourcée
   sur Hellio, Berenfus et Opéra Énergie alors que le PDF Légifrance de la
   loi de 1965 est dans le carnet. Un chiffre juste sourcé sur un blog reste
   un chiffre indéfendable : la carte se source sur le primaire.
2. **Il y a du droit québécois, et il est concentré sur un seul geste.**
   Quatre sources canadiennes (Éducaloi, quebec.ca, Lambert Avocats, l'Office
   québécois de la langue française) et **les quatre portent sur la mise en
   demeure**. Le vocabulaire est le nôtre, le droit ne l'est pas. Une
   question sur la mise en demeure d'un copropriétaire débiteur est donc
   exactement celle où le carnet peut répondre juste-en-apparence et faux en
   France : sur ce point, on ne l'interroge pas, on lit l'article 19-2 et le
   décret de 1967.

## Par catégorie

| Catégorie du carnet | Sources |
|---|---|
| Miscellaneous | 190 |
| Société Civile Immobilière | 22 |
| Comptabilité et Finances | 21 |
| Garanties et Assurances | 11 |
| Immobilier Neuf (VEFA) | 9 |
| Rénovation Énergétique | 9 |
| Impayés et Recouvrement | 8 |
| Assemblées Générales | 7 |
| Contentieux et Recours | 7 |
| Documents Techniques | 4 |
| Urbanisme et Territoires | 4 |
| Hors catégorie | 2 |

« Miscellaneous » pèse les deux tiers : le rangement du carnet ne vaut pas
plan de travail. Les catégories utiles pour l'Académie restent à construire
sur l'arbre des domaines du BLUEPRINT §9, pas sur celui-ci.

---

## La liste

Ordre : catégorie du carnet, puis titre. `[officiel]`, `[associatif]`,
`[commercial]`, `[étranger]` valent pour les sources web uniquement.


### Miscellaneous (190)

- # Essentiel Métier - Faites souscrire la Protect… — markdown interne
- # Essentiel Métier - Optimisez vos déclarations… — markdown interne
- # Essentiel Métier _ Les espaces client et User — markdown interne
- # Essentiels métiers - Lecture d’un appel de cha… — markdown interne
- # Essentiels métiers _ Rôle et responsabilité … — markdown interne
- # Les essentiels métier - Présentation des acte… — markdown interne
- # Les essentiels métiers - Copropriété, origin… — markdown interne
- # Parlons sobriété _ Comment installer des born… — markdown interne
- 00_INSTRUCTIONS_PRIORITAIRES — markdown interne
- 082026_guide_gerer-coproprietes-fragiles.pdf — PDF déposé
- [15. Ostrom et les biens communs \| Cairn.info](https://shs.cairn.info/les-geants-de-la-pensee-economique--9782262099404-page-299?lang=fr) — shs.cairn.info [associatif]
- 202602_guide-aides-financieres_WEB.pdf — PDF déposé
- 353673480-Fonctionnement-Ascenseur.pdf — PDF déposé
- 501456933-2012-Brochure-Copropriete-Def.pdf — PDF déposé
- 615274690-FT31-Ascenseur.pdf — PDF déposé
- 624085455-Bernard-Boublim-Contrat-d-entreprise.pdf — PDF déposé
- 681565792-guide-pratique-renover-copropriete.pdf — PDF déposé
- 687276924-Le-Guide-de-La-Copropriete-Ooreka.pdf — PDF déposé
- 689596305-Pathologie-Generale-Du-Batiment-Philippe-Philipparie-2019-Eyrolles-9782212677676-872f62cf98c62ccf96d321276862e729-Anna-s-Archive.pdf — PDF déposé
- 747074196-Schema-Responsabilite-DDE-IRSI.pdf — PDF déposé
- 749159518-Pathologie-Generale-Du-Batiment-D.pdf — PDF déposé
- 757997800-APC-REFERENTIEL-DTG-VF.pdf — PDF déposé
- 816010350-Cahier-Des-Charges-Maitrise-d-Ouevre-Renovation-Archi-Et-Energie.pdf — PDF déposé
- 840547639-DOC-20241107-WA0000.pdf — PDF déposé
- 858521287-La-pathologie-des-facades-4e-Edition-Philippe-PHILIPPARIE-Jean-Luc-THOMAS-CSTB-2023.pdf — PDF déposé
- 899949711-150-termes-immobilier.pdf — PDF déposé
- 921978188-Raisonnement-Econimique-de-La-Renovation-Energetique-2018-Tres-Bon-Elements.pdf — PDF déposé
- 930174891-Plan-Pluriannuel-de-Travaux-Rapport.pdf — PDF déposé
- [Accompagnement Plan Pluriannuel de Travaux (PPT) - Bureau Veritas Solutions](https://solutions.bureauveritas.fr/nos-solutions/accompagnement-plan-pluriannuel-de-travaux) — solutions.bureauveritas.fr [commercial]
- [Accélération et simplification de la rénovation de l'habitat dégradé et des grandes opérations d'aménagement - ANIL](https://www.anil.org/aj-loi-habitat-degrade/) — www.anil.org [officiel]
- AJDI2024-02-02-DOSSIER-2.pdf — PDF déposé
- ANAH_202509_guide-aides-financieres.pdf — PDF déposé
- ANAH_ChiffresCles-PAYS-DE-LA-LOIRE_VDEF_WEB_20260528.pdf — PDF déposé
- [Analyse juridique : réforme du droit des sûretés - ANIL](https://www.anil.org/aj-reforme-droit-suretes/) — www.anil.org [officiel]
- [Analyse socio-économique de la rénovation énergétique des logements](https://cae-eco.fr/static/pdf/focus-106-modelisation-reno-240625.pdf) — cae-eco.fr [commercial]
- apc-livret2-acteursactionsrenocopro-dec-150114043013-conversion-gate02.pdf — PDF déposé
- [Appels de Fonds de Copropriété en SCI : Écritures et Régularisation (2026)](https://sci-ai.app/appels-fonds-copropriete-sci) — sci-ai.app [commercial]
- Arrêté du 31 janvier 1986 relatif à la protection contre l'incendie des bâtiments d'habitation - Légifrance.pdf — PDF déposé
- Article 1 - Décret n° 2022-663 du 25 avril 2022 fixant les compétences et les garanties exigées pour les personnes établissant le projet de plan pluriannuel de travaux des immeubles soumis au statut de la copropriété - Légifrance.pdf — PDF déposé
- Article 2224 - Code civil - Légifrance.pdf — PDF déposé
- Article 2374 - Code civil - Légifrance.pdf — PDF déposé
- [Article 2374-1 of the French Civil Code \| French Legislation](https://www.french-business-law.com/french-legislation-art/article-2374-1-of-the-french-civil-code) — www.french-business-law.com [commercial]
- Article 2402 - Code civil - Légifrance.pdf — PDF déposé
- Article 72 - Décret n°72-678 du 20 juillet 1972.pdf — PDF déposé
- Article L113-12-2 - Code des assurances - Légifrance.pdf — PDF déposé
- Article L113-15-2 - Code des assurances - Légifrance.pdf — PDF déposé
- Article L173-1 - Code de la construction et de l'habitation - Légifrance.pdf — PDF déposé
- Article L241-1 - Code des assurances - Légifrance.pdf — PDF déposé
- Article L242-1 - Code des assurances - Légifrance.pdf — PDF déposé
- Article L313-3 - Code monétaire et financier - Légifrance.pdf — PDF déposé
- Article L519-1 - Code monétaire et financier - Légifrance.pdf — PDF déposé
- Article L561-2 - Code monétaire et financier - Légifrance.pdf — PDF déposé
- [Assurance dommages-ouvrage copropriété : tout savoir - Syndic One](https://www.syndic-one.com/blog/autour-de-la-copropriete/lassurance-dommages-ouvrage-copropriete-en-5-questions-reponses/) — www.syndic-one.com [commercial]
- [Avance de fonds travaux - Syndic de copropriété - Forum Diacamma](https://www.diacamma.org/forum/t/avance-de-fonds-travaux/3029) — www.diacamma.org [commercial]
- [Avance de trésorerie en copropriété : guide de bonne gestion - Copro'Assist](https://www.copro-assist.fr/avance-de-tresorerie-copro/) — www.copro-assist.fr [commercial]
- [Avances de trésorerie - Documentation - Copriciel](https://docs.copriciel.com/exercice/avances-de-tresorerie/) — docs.copriciel.com [commercial]
- [Bibliographie récente /// Pierre-Edouard Lagraulet - LDP Avocats](https://www.ldp-avocats.fr/actualites-droit-immobilier/bibliographie-immobilier-avocat/bibliographie-recente-pierre-edouard-lagraulet/) — www.ldp-avocats.fr [commercial]
- [CA Paris, Pôle 4 ch. 13, 7 octobre 2025, n° 22/07497 - COUR D'APPEL - Livv](https://app.livv.eu/decisions/LawLex202500009124JBJ) — app.livv.eu [commercial]
- [Cession de biens en copropriété et opposition au versement par le syndic](https://www.lemag-juridique.com/articles/immobilier-cession-biens-copropriete-opposition-versement-par-syndic-7320.htm) — www.lemag-juridique.com [commercial]
- [Cession de parts sociales d'une société civile immobilière (SCI)](https://entreprendre.service-public.gouv.fr/vosdroits/F36016) — entreprendre.service-public.gouv.fr [officiel]
- [Chapitre 2. La publicité des différentes sûretés immobilières - CAIRN - Droit et Administration](https://droit.cairn.info/droit-des-suretes--9782340063952-page-405?lang=fr) — droit.cairn.info [associatif]
- [Chapitre I - Les paradoxes de l'action collective ou le long chemin de l'intérêt au groupe - Cairn](https://shs.cairn.info/les-groupes-d-interet--9782200259983-page-23?lang=fr) — shs.cairn.info [associatif]
- Chapitre III _ Crédit immobilier (Articles L313-1 à L313-64) - Légifrance.pdf — PDF déposé
- Chapitre unique _ Diagnostic technique global des immeubles relevant du statut de la copropriété. (Articles L731-1 à L731-5) - Légifrance.pdf — PDF déposé
- [charges générales et spéciales de copropriété - ANIL](https://www.anil.org/votre-besoin/gerer-un-bien/copropriete/charges/) — www.anil.org [officiel]
- [Clé de Répartition des Charges \| Définition & Calcul concret - BailFacile](https://www.bailfacile.fr/guides/cles-de-repartition) — www.bailfacile.fr [commercial]
- [Code de la copropriété 2026, annoté et commenté - Boutique Lefebvre Dalloz](https://boutique.lefebvre-dalloz.fr/code-de-la-copropriete.html) — boutique.lefebvre-dalloz.fr [commercial]
- [Comment analyser le grand livre - UCS Sarcelles](https://ucssarcelles.org/site/wp-content/uploads/2025/05/ORCOD-SARCELLES-Formation-Comment-analyser-le-grand-livre-la-balance-et-les-5-annexes.pdf) — ucssarcelles.org [commercial]
- [Comment choisir un comptable pour son syndic de copropriété ? - Numbr](https://numbr.co/expertise-comptable/comment-choisir-un-comptable-pour-son-syndic-de-copropriete/) — numbr.co [commercial]
- [Comment choisir un syndic de copropriété efficace et réactif ?](https://commissaire-justice.fr/blog-juridique/choisir-syndic-copropriete/) — commissaire-justice.fr [commercial]
- [Comment engager la responsabilité juridique de son syndic ? - Matera](https://matera.eu/fr/articles/syndic-copropriete-responsabilite-juridique-syndic) — matera.eu [commercial]
- [Comment le paradoxe de l'action collective est-il surmonté (incitations sélectives, rétributions symboliques) ? - Les Sherpas](https://sherpas.com/p/ses/paradoxe-action-collective.html) — sherpas.com [commercial]
- commentvgtaliservotrecoproprit-180206114023.pdf — PDF déposé
- [Comprendre la différence entre Fonds de Roulement et Fonds de Travaux ALUR](https://jbbullet.notaires.fr/fonds-roulement-travaux-alur-copropriete/) — jbbullet.notaires.fr [commercial]
- [Comptabilisation des fonds de travaux - A votre écoute pour une aide aux coproprietaires, aux syndics bénévoles et aux conseils syndicaux](https://www.sos-syndic.info/2017/01/comptabilisation-des-fonds-de-travaux.html) — www.sos-syndic.info [commercial]
- [Compétence du juge de proximité en matière de copropriété - Lettre des réseaux](https://www.lettredesreseaux.com/P-1290-453-A1-competence-du-juge-de-proximite-en-matiere-de-copropriete.html) — www.lettredesreseaux.com [commercial]
- [Conflit entre associés : 5 solutions pour débloquer la situation \| JEM-AVOCAT](https://www.jem-avocat.fr/notes-expert/conflit-entre-associes-solutions/) — www.jem-avocat.fr [commercial]
- [Conflits en copropriété : l'angle mort psychologique - EVAL](https://www.eval.fr/ressources/par-secteur/politiques-habitat-logement/conflits-en-copropriete/) — www.eval.fr [commercial]
- [Contentieux : le régime juridique du trouble anormal de voisinage est inscrit dans le code civil dans le but de réduire les recours contre les activités agricoles (loi n°2024-346 du 15 avril 2024 visant à adapter le droit de la responsabilité civile aux enjeux actuels) - Cabinet Gossement AVOCATS](https://www.gossement-avocats.com/blog/trouble-anormal-de-voisinage-loi-n-2024-346-du-15-avril-2024-visant-a-adapter-le-droit-de-la-responsabilite-civile-aux-enjeux-actuels/) — www.gossement-avocats.com [commercial]
- convention-irsi.pdf — PDF déposé
- [Copropriété en difficulté : mesures préventives avec l'intervention d'un mandataire ad hoc](https://www.service-public.gouv.fr/particuliers/vosdroits/F20388) — www.service-public.gouv.fr [officiel]
- [Copropriété fragile ou en difficulté : définition - QualiSR](https://www.associationqualisr.org/coproprietes-fragiles/) — www.associationqualisr.org [commercial]
- [Crises of the commons: Elinor Ostrom's legacy of self-governance](https://csgs.kcl.ac.uk/crises-of-the-commons-elinor-ostroms-legacy-of-self-governance/) — csgs.kcl.ac.uk [commercial]
- DALBIN Pauline  .pdf — PDF déposé
- Décision du 18 décembre 2023 relative aux conditions d'octroi de crédits immobiliers - Légifrance.pdf — PDF déposé
- Décision du 29 septembre 2021 relative aux conditions d'octroi de crédits immobiliers - Légifrance.pdf — PDF déposé
- Décret n° 2015-342 du 26 mars 2015.pdf — PDF déposé
- Décret n° 2022-663 du 25 avril 2022 fixant les compétences et les garanties exigées pour les personnes établissant le projet de plan pluriannuel de travaux des immeubles soumis au statut de la copropriété - Légifrance.pdf — PDF déposé
- Décret n° 2022-780 du 4 mai 2022 relatif à l'audit énergétique mentionné à l'article L. 126-28-1 du code de la construction et de l'habitation - Légifrance.pdf — PDF déposé
- Décret n° 2025-508 du 10 mai 2025 relatif à la qualité de syndic d'intérêt collectif prévue à l'article 18-3 de la loi n° 65-557 du 10 juillet 1965 fixant le statut de la copropriété des immeubles bâtis - Légifrance.pdf — PDF déposé
- Décret n°2004-964 du 9 septembre 2004 relatif à la sécurité des ascenseurs et modifiant le code de la construction et de l'habitation. - Légifrance.pdf — PDF déposé
- Décret n°2005-1315 du 21 octobre 2005 modifiant le décret n° 72-678 du 20 juillet 1972 .pdf — PDF déposé
- Décret n°2006-555 du 17 mai 2006 relatif à l'accessibilité des établissements recevant du public, des installations ouvertes au public et des bâtiments d'habitation et modifiant le code de la construction et de l'habitation. - Légifrance.pdf — PDF déposé
- Décret n°67-223 du 17 mars 1967 pris pour l'application de la loi n° 65-557 du 10 juillet 1965 fixant le statut de la copropriété des immeubles bâtis - Légifrance.pdf — PDF déposé
- Décret n°96-97 du 7 février 1996 relatif à la protection de la population contre les risques sanitaires liés à une exposition à l'amiante dans les immeubles bâtis - Légifrance.pdf — PDF déposé
- [Droits d'enregistrement d'une cession de parts - AGN Avocats](https://www.agn-avocats.fr/blog/droit-des-affaires/cession-de-parts/droits-denregistrement-dune-cession-de-parts/) — www.agn-avocats.fr [commercial]
- [Droits d'enregistrement en cas de reprise d'entreprise - Bpifrance Création](https://bpifrance-creation.fr/encyclopedie/fiscalite-lentreprise/fiscalite-transmissionreprise/droits-denregistrement-cas-reprise) — bpifrance-creation.fr [commercial]
- Dynamique_demographique_2025_Adil49.pdf — PDF déposé
- [Enquête sur les difficultés de la copropriété : une étude de l'ADIL de Paris - ANIL](https://www.anil.org/documentation-experte/etudes-eclairages/etudes-et-eclairages-1999/enquete-sur-les-difficultes-de-la-copropriete-une-erp-de-ladil-de-paris/) — www.anil.org [officiel]
- [Estimation valeur sci et montant compte courant : je m'apprête à vendre nos parts sociales a mon mari et moi acquis en 2013. valeur 5€ donc 50 parts chacun soit 100€ en 2013, nous avons acquis un terrain et construit, le bâtiment a été amorti depuis... - Posée par Nath - Alexia](https://www.alexia.fr/questions/428502/estimation-valeur-sci-et-montant-compte-courant.htm) — www.alexia.fr [commercial]
- [Etude sociologique sur la décision de rénovation énergétique en copropriété (thèse 2011)](https://gbrisepierre.fr/projet/erp-sociologique-sur-la-decision-de-renovation-energetique-en-copropriete-these-2011/) — gbrisepierre.fr [commercial]
- [Family SARL or SCI France 2026: Tax Structure Choice - Hayot Expertise](https://hayot-expertise.fr/en/blog/family-sarl-or-sci-france-2026) — hayot-expertise.fr [commercial]
- [Faut-il un état daté pour vendre un logement dans une copropriété ? \| Service Public](https://www.service-public.gouv.fr/particuliers/vosdroits/F37294) — www.service-public.gouv.fr [officiel]
- Fiche-Pathologie-Batiment-G05-Entretien-Maintenance-Pac-Aerothermiques-AQC.pdf — PDF déposé
- Fiche-Pathologie-Batiment-G06-Entretien-Maintenance-VMC-Simple-Double-Flux-AQC.pdf — PDF déposé
- Fiche-Pathologie-Batiment-G07-Entretien-Maintenance-Plomberie-Sanitaire-AQC.pdf — PDF déposé
- [Focus sur les lois qui encadrent les copropriétés - Galian](https://www.galian-smabtp.fr/blog/focus-sur-les-lois-qui-encadrent-les-coproprietes) — www.galian-smabtp.fr [commercial]
- [Fonds de travaux ALUR : obligations, montant et gestion pratique (2026)](https://www.mon-syndic-benevole.fr/blog/fonds-de-travaux-alur-obligations-montant-gestion) — www.mon-syndic-benevole.fr [commercial]
- [Fonds travaux loi Alur : guide en copropriété - Hellio](https://copropriete.hellio.com/blog/renovation-energetique/fonds-travaux-loi-alur) — copropriete.hellio.com [commercial]
- [Fonds travaux loi ALUR : tout savoir - ADB Conseils](https://www.adbconseils.fr/fonds-travaux-loi-alur/) — www.adbconseils.fr [commercial]
- [Gestion de copropriété 2026 : PPT, DPE collectif et carte S - Efisio](https://efisio.fr/gestion-copropriete-2026-syndic-cpf/) — efisio.fr [commercial]
- [Gestion de copropriété : Moderniser votre syndicat au Québec - Le Courrier Sud](https://www.lecourriersud.com/publi-t/moderniser-gestion-copropriete-quebec/) — www.lecourriersud.com [commercial]
- [Gestionnaire de copropriété : 6 idées reçues qui ont la vie dure - Journal de l'Agence](https://www.journaldelagence.com/1412600-gestionnaire-de-copropriete-6-idees-recues-qui-ont-la-vie-dure) — www.journaldelagence.com [commercial]
- [Gestionnaire de copropriété : une reconversion professionnelle prometteuse - Studi](https://www.studi.com/fr/reconversion/gestionnaire-copropriete) — www.studi.com [commercial]
- [Guichet unique auto-entrepreneur : tout comprendre en 2026](https://www.portail-autoentrepreneur.fr/academie/creation-auto-entreprise/guichet-unique-auto-entrepreneur) — www.portail-autoentrepreneur.fr [commercial]
- [http://www - Lirsa \| Cnam](https://lirsa.cnam.fr/medias/fichier/olsonhtml__1263552515308.html) — lirsa.cnam.fr [commercial]
- [Initiative Copropriétés : plan national pour rénover les copropriétés - ALTEREA](https://www.alterea.fr/le-lab/initiative-coproprietes-nouveau-plan-national-pour-renover-coproprietes-degradees) — www.alterea.fr [commercial]
- [Intervenir en copropriété - Agence nationale de l'habitat](https://www.anah.gouv.fr/sites/default/files/2026-06/202510_guide_intervenir-en-copropriete_WEBA.pdf) — www.anah.gouv.fr [officiel]
- [Intégration des troubles anormaux de voisinage dans le Code civil - smabtp](https://www.smabtp.fr/sma/assurance/actualite/interation-troubles-anormaux-de-voisinage-dans-le-code-civil) — www.smabtp.fr [commercial]
- [Jurisprudence pour les travaux en copropriété​ : tout savoir - Hellio](https://copropriete.hellio.com/blog/vie-copro/jurisprudence-travaux-copropriete) — copropriete.hellio.com [commercial]
- [L'essentiel de la loi du 9 avril 2024 portant sur la rénovation de l'habitat dégradé - smabtp](https://www.smabtp.fr/sma/assurance/actualite/loi-9-avril-2024-renovation-habitat-degrade) — www.smabtp.fr [commercial]
- [La construction d'une maison sur terrain en SCI : nos conseils - Dougs](https://www.dougs.fr/blog/sci-terrain-constructible/) — www.dougs.fr [commercial]
- [La Gouvernance des biens communs : Pour une nouvelle approche des ressources naturelles - Wikipédia](https://fr.wikipedia.org/wiki/La_Gouvernance_des_biens_communs_:_Pour_une_nouvelle_approche_des_ressources_naturelles) — fr.wikipedia.org [commercial]
- [La régularisation des charges de copropriété - MeilleureCopro](https://www.meilleurecopro.com/les-guides-de-la-copropriete/regularisation-des-charges/) — www.meilleurecopro.com [commercial]
- [La super procédure de recouvrement de charges de la Loi ELAN - BJA \| Avocats](https://www.bjavocat.com/2018/12/09/la-super-procedure-de-recouvrement-de-la-loi-elan/) — www.bjavocat.com [commercial]
- [LA SURÉLÉVATION - Agence nationale de l'habitat](https://www.anah.gouv.fr/sites/default/files/2023-07/guide_surelevation_en_copropriete.pdf) — www.anah.gouv.fr [officiel]
- [Le guichet unique des formalités d'entreprise : le guide 2026 - Legalstart](https://www.legalstart.fr/fiches-pratiques/demarches-creation/guichet-unique/) — www.legalstart.fr [commercial]
- [Le Plan pluriannuel de travaux (PPT) est-il obligatoire en copropriété - Matera](https://matera.eu/fr/blog/le-plan-pluriannuel-de-travaux-ppt-est-il-obligatoire-en-copropriete) — matera.eu [commercial]
- [Le portage des logements dans les copropriétés dégradées : quel risque pour les collectivités territoriales ? \| Groupe Caisse des Dépôts](https://www.caissedesdepots.fr/eclairage/blog/articles/le-portage-des-logements-dans-les-coproprietes-degradees-quel-risque-pour-les) — www.caissedesdepots.fr [officiel]
- [Le privilège immobilier spécial devient une hypothèque légale spéciale! - Alvarez & Arlabosse](https://www.alvarez-arlabosse.com/presse-publication/le-privilege-immobilier-special-devient-une-hypotheque-legale-speciale/) — www.alvarez-arlabosse.com [commercial]
- [Le Projet de Plan Pluriannuel de Travaux - PPPT - Lelièvre Immobilier](https://www.lelievre-immobilier.com/actualites/le-projet-de-plan-pluriannuel-de-travaux-pppt) — www.lelievre-immobilier.com [commercial]
- [Le recouvrement des charges de copropriété en procédure collective - Cabinet BJA \| Avocats à la cour](https://www.bjavocat.com/2025/04/02/13281/) — www.bjavocat.com [commercial]
- [Le syndic de copropriété : un intermédiaire en devenir pour la rénovation énergétique](https://www.institutparisregion.fr/nos-travaux/publications/le-syndic-de-copropriete-un-intermediaire-en-devenir-pour-la-renovation-energetique/) — www.institutparisregion.fr [commercial]
- [Le syndicat des copropriétaires représenté par un syndic professionnel est un non-professionnel au sens de l'article L. 136-1 du Code de la consommation - SEBAN AVOCATS](https://www.seban-associes.avocat.fr/le-syndicat-des-coproprietaires-represente-par-un-syndicat-professionnel-est-un-est-non-professionnel-article-l-136-1-code-de-la-consommation/) — www.seban-associes.avocat.fr [commercial]
- [Les Annexes comptables - URCC PACA](https://www.urccpaca.fr/sites/default/files/Annexes-comptables-Visio-du-03.10.2024-LF-03.10.2024.pdf) — www.urccpaca.fr [commercial]
- [Les pouvoirs du Président du Tribunal judiciaire - Gdroit](https://gdroit.fr/les-pouvoirs-du-president-du-tribunal-judiciaire/) — gdroit.fr [commercial]
- [Les responsabilites en copropriete.pdf - CLCV](https://www.clcv.org/storage/app/media/coproprietaires/Les-responsabilites-en-copropriete.pdf) — www.clcv.org [associatif]
- [LES RISQUES DU METIER - KU Leuven Bibliotheken](https://bib.kuleuven.be/rbib/collectie/archieven/boeken/obfg-risquesmetier-2008.pdf) — bib.kuleuven.be [commercial]
- Lettre14_foncier_densite.pdf — PDF déposé
- [Licence (L3) mention Droit parcours type Juriste de copropriété - Executive Education](https://executive-education.ut-capitole.fr/accueil/formez-vous/licence-l3-mention-droit-parcours-type-juriste-de-copropriete) — executive-education.ut-capitole.fr [commercial]
- Livre VII _ TRAITEMENT DES SITUATIONS DE SURENDETTEMENT (Articles L711-1 à L771-12) - Légifrance.pdf — PDF déposé
- [Logement : les apports de la loi « habitat dégradé » \| Notaires de France](https://www.notaires.fr/fr/article/logement-les-apports-de-la-loi-habitat-degrade) — www.notaires.fr [commercial]
- LOI n° 2014-366 du 24 mars 2014 pour l'accès au logement et un urbanisme rénové (1) - Légifrance.pdf — PDF déposé
- Loi n° 65-557 du 10 juillet 1965 fixant le statut de la copropriété des immeubles bâtis - Légifrance.pdf — PDF déposé
- Loi n° 70-9 du 2 janvier 1970 réglementant les conditions d'exercice des activités relatives à certaines opérations portant sur les immeubles et les fonds de commerce - Légifrance.pdf — PDF déposé
- [Mancur Olson, et le passager clandestin](https://perso.amse-aixmarseille.fr/trannoy/documents/Olson-Trannoy_Tribuneete2011-1.pdf) — perso.amse-aixmarseille.fr [commercial]
- [Mon accompagnateur rénov' : la Cour des comptes alerte sur les risques](https://www.gazdaujourdhui.fr/mon-accompagnateur-renov-la-cour-des-comptes-alerte-sur-les-risques/) — www.gazdaujourdhui.fr [commercial]
- [Mon Accompagnateur Rénov' : la Cour des comptes appelle à plus de contrôles - Enerzine](https://www.enerzine.com/mon-accompagnateur-renov-la-cour-des-comptes-appelle-a-plus-de-controles/187612-2026-06) — www.enerzine.com [commercial]
- Note de conjoncture n°70_Janvier 2026 derniere version.pdf — PDF déposé
- PAQUET_Yannik_2016_archivage.pdf — PDF déposé
- Parc_locatif_Prive_2024_Adil49_v2.pdf — PDF déposé
- particuliers_vosdroits_F38425.pdf — PDF déposé
- Passager clandestin Mancur Olson #bac #ses #etude #methodoses #revision #sociologie #politique — vidéo YouTube
- [Paupérisation des copropriétés : un rapport du Sénat alerte sur un phénomène mal connu qui « bouge, s'amplifie et se transforme »](https://www.publicsenat.fr/actualites/parlementaire/pauperisation-des-coproprietes-un-rapport-du-senat-alerte-sur-un-phenomene-mal-connu-qui-bouge-samplifie-et-se-transforme) — www.publicsenat.fr [commercial]
- Plan pluriannuel de travaux (PPT) mis en place dans les copropriétés _ Service Public.pdf — PDF déposé
- [Plan pluriannuel des travaux : quelles sont les obligations ? - LeBonBail](https://www.lebonbail.fr/articles/plan-pluriannuel-des-travaux-quelles-sont-les-obligations) — www.lebonbail.fr [commercial]
- [Prêt collectif à adhésion automatique - Agence Etoile](https://www.agence-etoile.fr/2026/01/24/pret-collectif-a-adhesion-automatique/) — www.agence-etoile.fr [commercial]
- [Qu'est-ce que le « pré-état daté » ? Quelles obligations ? - fnaim.fr](https://www.fnaim.fr/4194-qu-est-ce-que-le-pre-etat-date-quelles-obligations.htm) — www.fnaim.fr [commercial]
- r23-736-11.pdf — PDF déposé
- Rapport CNH Avenir du métier de syndic Sep 2025.pdf — PDF déposé
- Rapport Deep Research : Comparative Legal, Operational, and Fiscal Analysis of the French Société Civile Immobilière (SCI) and the Co-ownership Status (Loi du 10 juillet 1965) — markdown interne
- Rapport Deep Research : L’Écosystème Invisible de la Copropriété : Analyse Systémique des Cinq Angles Morts de la Gestion Immobilière — markdown interne
- Rapport Deep Research : Théorie Générale du Droit Appliquée à la Gestion de Copropriété : Manuel Juridique et Pratique pour le Praticien de l'Immobilier — markdown interne
- Rapport Deep Research : État des lieux documentaire et audit des lacunes de gestion en copropriété — markdown interne
- Rapport-Observatoire-Qualite-Construction-2025-AQC.pdf — PDF déposé
- Rapport-Reduire-Vulnerabilite-Batiments-AQC.pdf — PDF déposé
- Rapport-REX-BP-ITE-Isolation-Thermique-Exterieur-Renovation-AQC.pdf — PDF déposé
- Rapportsurlessyndicsetlebiencommun_0.pdf — PDF déposé
- [Remboursement du pré-état daté : vos droits (2026) - Pre-etat-date.ai](https://pre-etat-date.ai/guide/remboursement-pre-etat-date) — pre-etat-date.ai [commercial]
- [Responsabilité du Syndic : Fautes de Gestion - 544 Cabinet d'Avocats](https://www.544.fr/copropriete/responsabilite-syndic-fautes-gestion) — www.544.fr [commercial]
- [Responsabilité du Syndic : Recours et Faute de Gestion \| CSJ AVOCATS](https://www.csj-avocats.fr/articles/responsabilite-syndic-recours-faute-gestion-1396.htm) — www.csj-avocats.fr [commercial]
- [Responsabilité du syndic : un avocat peut-il vous aider à obtenir réparation](https://goldwin-avocats.com/fr/faq/la-responsabilite-du-syndic-c-est-quoi/) — goldwin-avocats.com [commercial]
- [Retrait et sortie d'associé : guide complet pour sécuriser votre sortie - Victoris Avocat](https://www.victorisavocat.com/blog/retrait-sortie-associe-exclusion-deadlock-valorisation) — www.victorisavocat.com [commercial]
- Règlement de copropriété _ Service Public.pdf — PDF déposé
- [Réception et livraison de chantier immobilier : le guide complet - CLA Courtage](https://www.clacourtage.com/reception-et-livraison-dun-chantier-immobilier-differences-et-risques-pour-les-promoteurs/) — www.clacourtage.com [commercial]
- [Réforme droit des sûretés - Wargny Katz](https://www.wargny-katz.com/wp-content/uploads/2021/12/Reforme-des-suretes.pdf) — www.wargny-katz.com [commercial]
- [Régularisation des charges de copropriété \| avis 2026 - Radar Immobilier](https://www.radar-immobilier.com/regularisation-charges-copro/) — www.radar-immobilier.com [commercial]
- [Rénovation des copropriétés : emprunt collectif à adhésion automatique - ANIL](https://www.anil.org/aj-copropriete-emprunt-collectif-adhesion/) — www.anil.org [officiel]
- [Section 1. La compétence d'attribution - UNJF \| Institutions et principes fondamentaux du procès civil](https://cours.unjf.fr/repository/coursefilearea/file.php/22/Cours/04_item/globalprintcom.htm) — cours.unjf.fr [commercial]
- Section 2 _ Dispositions particulières aux copropriétés en difficulté. (Articles 29-1 A à 29-16) - Légifrance.pdf — PDF déposé
- [Simulateur droits d'enregistrement : cession de droits sociaux (actions et parts sociales)](https://www.biot-avocat.com/actualites/simulateur-droits-enregistrement-cession-droits-sociaux) — www.biot-avocat.com [commercial]
- [sous toutes réserves \| GDT - Vitrine linguistique - Gouvernement du Québec](https://vitrinelinguistique.oqlf.gouv.qc.ca/fiche-gdt/fiche/8410227/sous-toutes-reserves) — vitrinelinguistique.oqlf.gouv.qc.ca [**étranger**]
- [Syndic : comment gérer les mutations en copropriété ? - Matera](https://matera.eu/fr/blog/gestion-mutation-syndic) — matera.eu [commercial]
- Texte de base _ Convention collective nationale des gardiens, concierges et employés d'immeubles (réécrite par l'avenant n° 74 du 27 avril 2009 portant modification de la convention) - Légifrance.pdf — PDF déposé
- Titre II _ Règles relatives aux assurances de dommages (Articles L121-1 à L12-10-1) - Légifrance.pdf — PDF déposé
- [Trouble anormal de voisinage : que faire en cas de nuisances (loi 2024)](https://www.daumas-wilson.fr/fr/actualites-juridiques/id-201-responsabilites-troubles-anormaux-voisinage) — www.daumas-wilson.fr [commercial]
- [Troubles de voisinage : que change le nouvel article 1253 du Code civil](https://www.avocatayoun.fr/details-troubles+de+voisinage+que+change+le+nouvel+article+1253+du+code+civil-345) — www.avocatayoun.fr [commercial]
- [Vendre un bien en SCI, en indivision ou en copropriété - City&You](https://www.cityandyou.com/blog/2020/09/28/vendre-un-bien-en-sci-en-indivision-ou-en-copropriete) — www.cityandyou.com [commercial]
- Ventes_immobilieres_logements_MaineEtLoire_juin2024_adil49.pdf — PDF déposé
- vinci-mookfinal-tous-vf-210907140950.pdf — PDF déposé

### Société Civile Immobilière (22)

- Acheter sa résidence principale en SCI : bonne idée ou piège à éviter ? — vidéo YouTube
- [Acheter un bien immobilier à plusieurs : SCI ou indivision - Pichet](https://www.pichet.fr/guide/investir/acheter-appartement-sci-ou-indivision) — www.pichet.fr [commercial]
- [Cession de parts d'une SCI : étapes, fiscalité, formalités - L-Expert-Comptable.com](https://www.l-expert-comptable.com/a/531815-les-cessions-de-parts-sociales-au-sein-d-une-sci.html) — www.l-expert-comptable.com [commercial]
- [Cession de parts de SCI : 5 étapes essentielles à suivre - LegalPlace](https://www.legalplace.fr/guides/cession-parts-sci/) — www.legalplace.fr [commercial]
- [Cession parts SCI 2026 : procédure et fiscalité - CPIM Conseil en Patrimoine Immobilier](https://www.cpim.fr/cession-parts-sci-procedure-2026/) — www.cpim.fr [commercial]
- [Cession parts SCI 2026 : éviter l'erreur à 5 000 €](https://sci-ai.app/cession-parts-sci) — sci-ai.app [commercial]
- [Conflit entre Associés d'une SCI : Exclusion, Retrait & Dissolution - LLA Avocats](https://www.lla-avocats.fr/publications/droit-affaires/conflit-associes-sci/) — www.lla-avocats.fr [commercial]
- [Conflits entre associés d'une SCI familiale, comment en sortir ? - Héphaïstos Avocats](https://www.hephaistos-avocats.fr/conflits-entre-associes-dune-sci-familiale-comment-en-sortir/) — www.hephaistos-avocats.fr [commercial]
- [Création SCI : guide complet pour monter une Société Civile Immobilière en 2026](https://www.amarris-immo.fr/blog/investir-via-une-societe/creation-sci/) — www.amarris-immo.fr [commercial]
- [Declaring a property as SCI in France: procedure and advice - Paris Rental](https://en.parisrental.com/blog/landlords-guide/declaring-a-property-as-an-sci-in-france-procedure-and-advice) — en.parisrental.com [commercial]
- [Enregistrement cession de parts en SCI : démarches en 2026 - Investissement-Locatif.com](https://www.investissement-locatif.com/enregistrement-cession-de-parts.html) — www.investissement-locatif.com [commercial]
- [Le guichet unique INPI pour les formalités de SCI : mode d'emploi (2026)](https://sci-ai.app/guichet-unique-inpi-sci) — sci-ai.app [commercial]
- [LMNP et SCI : peut-on cumuler ? Guide 2026 - L-Expert-Comptable.com](https://www.l-expert-comptable.com/a/sci-lmnp) — www.l-expert-comptable.com [commercial]
- [LMNP ou SCI 2026 : 30 000 EUR de différence sur 10 ans](https://lmnp.ai/lmnp-ou-sci) — lmnp.ai [commercial]
- [Location meublée en SCI : ce que dit la loi en 2026 - LegalPlace](https://www.legalplace.fr/guides/location-meublee-sci/) — www.legalplace.fr [commercial]
- [Modèle de convention de compte courant d'associé en SCI (2026)](https://sci-ai.app/modele-convention-cca) — sci-ai.app [commercial]
- [Real Estate Civil Society (SCI): what you need to know - Service Public Entreprendre](https://entreprendre.service-public.gouv.fr/vosdroits/F38553?lang=en) — entreprendre.service-public.gouv.fr [officiel]
- [Real estate investment company (SCI): A wealth management tool - Alperea Assurances](https://alpassurances.fr/en/article/real-estate-civil-society-sci-a-wealth-management-tool) — alpassurances.fr [commercial]
- [SCI : cessions sous contrôle ? - Centaure Investissements](https://www.centaure-investissements.com/sci-cessions-sous-controle/) — www.centaure-investissements.com [commercial]
- [SCI et Location Meublée : Risques et Solutions (Guide 2026)](https://sci-ai.app/sci-location-meublee) — sci-ai.app [commercial]
- [SCI ou indivision : quel choix pour votre bien immobilier](https://e-immobilier.credit-agricole.fr/conseils/habiter/sci-ou-indivision) — e-immobilier.credit-agricole.fr [commercial]
- [Understanding SCI Taxes - My French House](https://www.my-french-house.com/blog/article/75461/understanding-sci-taxes) — www.my-french-house.com [commercial]

### Comptabilité et Finances (21)

- [Appels de fonds et écritures comptables - VILOGI.COM](https://www.vilogi.com/le-logiciel-syndic-copropriete/appels-de-fonds-et-ecritures-comptables_20-166-1-0-1.php) — www.vilogi.com [commercial]
- Arrêté du 14 mars 2005 relatif aux comptes du syndicat des copropriétaires - Légifrance.pdf — PDF déposé
- [Comptabilisation appel de fond travaux - Copro'Assist](https://www.copro-assist.fr/comptabilisation-appel-de-fond-travaux/) — www.copro-assist.fr [commercial]
- [Comptabilisation des appels de provisions sur opérations courantes - LOCKimmo](https://www.lockimmo.com/comptabilisation-des-appels-de-provisions-sur-operations-courantes/) — www.lockimmo.com [commercial]
- [Comptabilité copropriété : le guide - Seiitra](https://www.seiitra.com/blog/comptabilite-copropriete-le-guide/) — www.seiitra.com [commercial]
- [Comptabilité de copropriété : le guide complet pour les syndics - Berenfus](https://berenfus-immobilier.fr/copropriete/comptabilite-copropriete-guide-syndic/) — berenfus-immobilier.fr [commercial]
- [Copropriété : Comptabilisation des travaux et opérations exceptionnelles - LOCKimmo](https://www.lockimmo.com/copropriete-comptabilisation-des-travaux-et-operations-exceptionnelles/) — www.lockimmo.com [commercial]
- [Gestion comptable des copropriétés - ANIL](https://www.anil.org/aj-gestion-comptable-des-coproprietes/) — www.anil.org [officiel]
- [initiation à la comptabilité module 1 - Copro-Eco](https://www.copro-eco.fr/download.php?type=c) — www.copro-eco.fr [commercial]
- [Introduction à la comptabilité suite au décret de 2005 - Le Conseil syndical et La Copropriété](http://conseilsyndicalassoc.free.fr/comptabilite/introduction.php) — conseilsyndicalassoc.free.fr [associatif]
- [Jeux d Ecritures de régularisation de charges - VILOGI.COM](https://www.vilogi.com/le-logiciel-syndic-copropriete/ecritures-de-regularisation-de-charges_41-395-1-0-1.php) — www.vilogi.com [commercial]
- [la comptabilité de la copropriété - comptacop](https://www.comptacop.fr/index_decouvrir_courant.php) — www.comptacop.fr [commercial]
- [LES NOUVELLES REGLES COMPTABLES APPLICABLES AUX COPROPRIETES](http://ardsp.06480.free.fr/Files/guide_nouvelles_regles_comptables.pdf) — ardsp.06480.free.fr [associatif]
- [Plan comptable applicable aux copropriétés - Copro+](https://www.coproplus.fr/plan-comptable.html) — www.coproplus.fr [commercial]
- [Plan comptable copropriété : modèle CSV gratuit](https://logicielsyndic.fr/modeles/plan-comptable-copropriete) — logicielsyndic.fr [commercial]
- Rapport Deep Research : Rapport d'Ingénierie Comptable, de Gestion Financière et d'Audit de la Copropriété : Manuel à l'Usage des Gestionnaires Experts — markdown interne
- [Rapprochement bancaire : définition, utilité et méthode - Legalstart](https://www.legalstart.fr/fiches-pratiques/comptabilite-entreprise/comment-faire-rapprochement-bancaire/) — www.legalstart.fr [commercial]
- [Rapprochement Bancaire : Méthode et Écritures - Max Compta](https://www.maxcompta.com/blogs/blog-ecritures-comptables/rapprochement-bancaire) — www.maxcompta.com [commercial]
- [Rapprochement Bancaire : Méthode, Modèle et Écritures - Finref.fr](https://finref.fr/comptabilite/generale/rapprochement-bancaire/) — finref.fr [commercial]
- [Régularisation des charges courantes et clôture des comptes 489 de la copropriete Principes - VILOGI.COM](https://www.vilogi.com/le-logiciel-syndic-copropriete/principes-de-la-regularisation-des-charges-courantes-et-cloture-des-comptes-489_41-287-1-0-1.php) — www.vilogi.com [commercial]
- [Tout savoir sur le fonds de travaux Loi ALUR Comprendre la comptabilité de copropriété](https://www.homeland.immo/aide/tout-savoir-sur-le-fonds-de-travaux-loi-alur) — www.homeland.immo [commercial]

### Garanties et Assurances (11)

- [Assurance dommage-ouvrage travaux en copropriété - Hellio](https://copropriete.hellio.com/blog/renovation-energetique/assurance-dommage-ouvrage) — copropriete.hellio.com [commercial]
- [Assurance dommages-ouvrage - Service Public](https://www.service-public.gouv.fr/particuliers/vosdroits/F2032) — www.service-public.gouv.fr [officiel]
- [Assurance dommages-ouvrage copropriété : obligation et procédure](https://assurance-coproprietes.fr/assurances-complementaires/dommage-ouvrage) — assurance-coproprietes.fr [commercial]
- [Assurance dommages-ouvrage copropriété : obligations et coûts - AIAC Courtage](https://www.aiac.fr/actualites/immeuble/assurance-dommage-ouvrage-copropriete/) — www.aiac.fr [commercial]
- [Garantie de parfait achèvement : 5 éléments à retenir - Decennale.com](https://www.decennale.com/garantie-de-parfait-achevement/) — www.decennale.com [commercial]
- [Garantie de parfait achèvement : tout savoir - Groupama PJ](https://www.groupama-pj.fr/garantie-de-parfait-achevement-tout-savoir/) — www.groupama-pj.fr [commercial]
- [Garantie décennale : guide de l'article 1792 du Code civil - assurances April Pro](https://pro.april.fr/guide/garantie-decennale-article-1792-code-civil) — pro.april.fr [commercial]
- [Garantie parfait achèvement : tout ce qu'il faut savoir - Interconstruction](https://www.interconstruction.fr/actualites/quest-ce-que-la-garantie-de-parfait-achevement/) — www.interconstruction.fr [commercial]
- [Garanties de parfait achèvement : ce qu'il faut savoir - Côté Neuf](https://www.coteneuf.com/blog/garanties-de-parfait-achevement-ce-quil-faut-savoir) — www.coteneuf.com [commercial]
- [L'article 1792-6 du Code civil : la garantie de parfait achèvement - Demander Justice](https://www.demanderjustice.com/article-1792-6-du-code-civil-garantie-parfait-achevement) — www.demanderjustice.com [commercial]
- [Les travaux concernés par l'assurance dommages‑ouvrage en copropriété - Galian](https://www.galian-smabtp.fr/blog/les-travaux-concernes-par-l-assurance-dommages-ouvrage-en-copropriete) — www.galian-smabtp.fr [commercial]

### Immobilier Neuf (VEFA) (9)

- [Achat en VEFA et immeuble neuf : tout savoir sur la réception des parties communes](https://www.medicis-patrimoine.com/actualites-immobilier-neuf/guides-conseils/2022/10/24/3814-achat-en-vefa-tout-savoir-sur-la-livraison-des-parties-communes.html) — www.medicis-patrimoine.com [commercial]
- [Appels de fonds de copropriété en VEFA avant livraison : êtes-vous vraiment redevable](https://www.assoedc.com/appels-de-fonds-de-copropriete-en-vefa-avant-livraison-etes-vous-vraiment-redevable/) — www.assoedc.com [commercial]
- [Comment se déroule la livraison de mon bien immobilier neuf](https://www.homeland.immo/aide/comment-se-deroule-la-livraison-de-mon-bien-en-vefa) — www.homeland.immo [commercial]
- [Copropriété neuve, à partir de quand les charges sont-elles dues - Coproconseils](https://www.coproconseils.fr/copropriete-neuve-partir-de-quand-les-charges-sont-elles-dues/) — www.coproconseils.fr [commercial]
- [La levée des Réserves en VEFA : Le Guide Complet Matera](https://matera.eu/fr/articles/copropriete-neuve-levee-reserves) — matera.eu [commercial]
- [La livraison des parties communes en VEFA : définition, malfaçons et garanties - Matera](https://matera.eu/fr/articles/copropriete-neuve-livraison-parties-communes) — matera.eu [commercial]
- [Livraison VEFA : réception et livraison, ne pas confondre - Check my house](https://checkmy-house.fr/2026/06/06/vefa-reception-vs-livraison/) — checkmy-house.fr [commercial]
- [Réception et livraison VEFA : quelles sont les différences ? - Trouver un logement neuf](https://www.trouver-un-logement-neuf.com/immobilier-infos/difference-reception-livraison-vefa-9377.html) — www.trouver-un-logement-neuf.com [commercial]
- [Vente en VEFA : quel est le rôle du syndic ? - Crédit Agricole Immobilier](https://www.ca-immobilier.fr/actualites/achat/je-definis-mon-projet-d-achat-immobilier/vente-en-vefa-quel-est-le-role-du-syndic) — www.ca-immobilier.fr [commercial]

### Rénovation Énergétique (9)

- Arrêté du 31 mars 2021 relatif au diagnostic de performance énergétique pour les bâtiments ou parties de bâtiments à usage d'habitation en France métropolitaine - Légifrance.pdf — PDF déposé
- [Comprendre le plan pluriannuel de travaux en copropriété (PPT) - Hellio](https://copropriete.hellio.com/blog/renovation-energetique/plan-pluriannel-travaux) — copropriete.hellio.com [commercial]
- [Copropriété : les aides à la rénovation énergétique en 2026 - Hellio](https://copropriete.hellio.com/blog/renovation-energetique/guide-aides-financieres) — copropriete.hellio.com [commercial]
- Décret n° 2024-887 du 3 septembre 2024 relatif au prêt avance mutation ne portant pas intérêt destiné au financement de travaux permettant d'améliorer la performance énergétique des logements anciens - Légifrance.pdf — PDF déposé
- [les 3 étapes - de la rénovation énergétique et environnementale en copropriété](https://cdn.paris.fr/paris/2024/01/02/erp_guide-3-etapes_2023-231214-pap-bd-ZM08.pdf) — cdn.paris.fr [commercial]
- [Mener une rénovation énergétique en copropriété - Plan Bâtiment Durable](https://www.planbatimentdurable.developpement-durable.gouv.fr/IMG/pdf/guide_ademe_renovation_energetique_copropriete_1_.pdf) — www.planbatimentdurable.developpement-durable.gouv.fr [officiel]
- [Mon Accompagnateur Rénov' : la Cour des comptes appelle à renforcer les contrôles](https://infodiag.fr/mon-accompagnateur-renov-controles/) — infodiag.fr [commercial]
- [PPPT en copropriété : définition, obligation, contenu et prix 2026 - Opéra Énergie](https://opera-energie.com/pppt-projet-plan-pluriannuel-travaux/) — opera-energie.com [commercial]
- [Rapport pour une réhabilitation énergétique massive, simple et inclusive des logements privés - Banque des Territoires](https://www.banquedesterritoires.fr/sites/default/files/2021-03/RAPPORT%20sichel.pdf) — www.banquedesterritoires.fr [officiel]

### Impayés et Recouvrement (8)

- [Article 19-2 : la procédure accélérée au fond pour charges impayées - Grelier Avocat](https://www.grelieravocat.com/blog/procedure-acceleree-fond-article-19-2) — www.grelieravocat.com [commercial]
- [Article 19-2 de la loi du 10 juillet 1965 : précisions sur la mise en demeure et limites de la procédure accélérée](https://www.avocat-cannes.com/articles/article-19-loi-10-juillet-1965-precisions-sur-mise-demeure-limites-procedure-acceleree-34.htm) — www.avocat-cannes.com [commercial]
- [Impayés de Charges en Copropriété Paris : Procédure Complète de Recouvrement 2026](https://www.joya.fr/blog/impayes-de-charges-en-copropriete-paris-procedure-complete-de-recouvrement-2026) — www.joya.fr [commercial]
- [La procédure accélérée de recouvrement des charges de copropriété - Alpha Avocats](https://alpha-avocats.fr/la-procedure-acceleree-de-recouvrement-des-charges-de-copropriete/) — alpha-avocats.fr [commercial]
- [Nouvelle procédure en matière de charges de copropriété non réglées.](https://www.ebronquard-avocat.fr/post/nouvelle-proc%C3%A9dure-en-mati%C3%A8re-de-charges-de-copropri%C3%A9t%C3%A9-non-r%C3%A9gl%C3%A9es) — www.ebronquard-avocat.fr [commercial]
- [Recouvrement des charges : procédure accélérée et approbation des comptes](https://www.544.fr/copropriete/cass-3e-civ-20-novembre-2025-23-23-315-recouvrement-charges-approbation-comptes) — www.544.fr [commercial]
- [Recouvrement des charges de copropriété impayées - Service Public](https://www.service-public.gouv.fr/particuliers/vosdroits/F2603) — www.service-public.gouv.fr [officiel]
- [Recouvrement des charges de copropriété impayées : guide complet - Grelier Avocat](https://www.grelieravocat.com/blog/guide-recouvrement-charges-copropriete-impayees) — www.grelieravocat.com [commercial]

### Assemblées Générales (7)

- # Essentiel métier  Le déroulement d'une AG (su… — markdown interne
- # Les essentiels métiers - La convocation de l'a… — markdown interne
- [Article 24 en copropriété : guide sur la majorité simple​ \| Hellio](https://copropriete.hellio.com/blog/vie-copro/article-24) — copropriete.hellio.com [commercial]
- [Les majorités requises lors d'un vote en Assemblée Générale](https://www.lacgl.fr/IMG/UserFiles/Images/Fiche%201%20copro.pdf) — www.lacgl.fr [associatif]
- [LES REGLES DE MAJORITE Modalités de calcul des différentes majorités et résolutions concernées Il existe plusieurs types de - CLCV](https://www.clcv.org/storage/app/media/coproprietaires/Les-votes-en-ag.pdf) — www.clcv.org [associatif]
- [Les règles de majorité pour décider en assemblée générale de copropriété - ANIL](https://www.anil.org/majorite-decision-assemblee-generale-copropriete/) — www.anil.org [officiel]
- [Toutes les règles sur les majorités en copropriété - Manda](https://www.manda.fr/ressources/articles/les-majorites-en-copropriete) — www.manda.fr [commercial]

### Contentieux et Recours (7)

- [Comment contester une décision d'assemblée générale de copropriété](https://www.544.fr/copropriete/contester-decision-assemblee-generale-copropriete) — www.544.fr [commercial]
- [Comment écrire une lettre de mise en demeure? - Éducaloi](https://educaloi.qc.ca/capsules/comment-ecrire-une-lettre-de-mise-en-demeure/) — educaloi.qc.ca [**étranger**]
- [Contester une décision d'assemblée, faut-il toujours agir dans le délai de deux mois - UNPI](https://unpi.org/fr/1/15/911/Contester-une-decision-d-assemblee-faut-il-toujours-agir-dans-le-delai-de-deux-mois.html) — unpi.org [associatif]
- [Guide de rédaction d'une lettre de mise en demeure - Lambert Avocats](https://lambertavocats.ca/avocat-montreal/mise-en-demeure/) — lambertavocats.ca [**étranger**]
- [L'abc de la lettre de mise en demeure - FPB Avocats](https://fpbavocats.com/labc-de-la-lettre-de-mise-en-demeure/) — fpbavocats.com [commercial]
- [La minute droit de Maître Raison : l'abus de majorité en copropriété - Galian](https://www.galian-smabtp.fr/blog/minute-droit-maitre-raison-abus-majorite-copropri%C3%A9t%C3%A9) — www.galian-smabtp.fr [commercial]
- [Mise en demeure - Gouvernement du Québec](https://www.quebec.ca/justice-et-etat-civil/petites-creances/poursuivre/etapes-demande/mise-en-demeure) — www.quebec.ca [**étranger**]

### Documents Techniques (4)

- [Devis bâtiment : quelles mentions obligatoires ? \| Blog du BTP - Batappli](https://www.batappli.fr/blog-du-logiciel-batiment/quelles-sont-les-mentions-obligatoires-d-un-devis) — www.batappli.fr [commercial]
- [Mentions générales relatives aux devis et/ou factures Date du devis (devis + facture) ; Durée de validité de l'offre - Capeb](https://www.capeb.fr/www/capeb/media//centrevaldeloire/document/devisfacture.pdf) — www.capeb.fr [associatif]
- [Mentions obligatoires des factures dans le bâtiment - Mediabat](https://www.mediabat.com/mentions-obligatoires-factures-batiment/) — www.mediabat.com [commercial]
- [Quelles sont les mentions obligatoires d'un devis dans le bâtiment - Obat](https://www.obat.fr/blog/mentions-obligatoires-devis/) — www.obat.fr [commercial]

### Urbanisme et Territoires (4)

- Angers (49) Plan de Sauvegarde et de Mise en Valeur document d’urbanisme pour le cœur du Site patrimonial remarquable.pdf — PDF déposé
- bat_brochure_PDHH_A4.pdf — PDF déposé
- partie3_reunion_lancement_ppa_profil_humain-social-eco.pdf — PDF déposé
- Rapport_annuel_dep_49_2024.pdf — PDF déposé

### Hors catégorie (2)

- # Les essentiels métier - Savoir lire les annexe… — markdown interne
- NOT_GuideCopropriete_EP8_pap_REMPLACE.pdf — PDF déposé

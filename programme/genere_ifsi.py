#!/usr/bin/env python3
"""Le programme de l'infirmier, en une source : ce script porte les
DONNÉES (domaines, branches, chapitres, compétences, notions, parcours,
mots-clés) et génère deux sorties qui ne s'éditent jamais à la main :

    programme/ifsi.json    la version machine (fait foi)
    SYLLABUS-IFSI.md       le programme lisible

    python3 programme/genere_ifsi.py

Écrit le 04/09/2026 sur le brief de JB (« un arbre qui aille jusqu'au
concours d'infirmier d'Arthur, mais que s'ils veulent avancer ils
puissent faire sa formation, et aller beaucoup plus loin dans chaque
domaine »). Même mécanique que genere_copro.py, même règle de niveaux :

    I   Repères      ce que la sélection d'entrée en IFSI attend
    II  Mécanismes   ce que la sélection attend pour être bon, et le S1
    III Praticien    la formation en IFSI (les unités d'enseignement, les
                     dix compétences, les stages)
    IV  Doctrine     au-delà du diplôme : spécialités, pratique avancée,
                     controverses
    V   Frontière    recherche, état de l'art, contribuer

Le socle (niveau II partout) est l'entrée en IFSI. Les numéros d'unités
d'enseignement sont ceux de l'arrêté du 31 juillet 2009 relatif au
diplôme d'État d'infirmier ; les dix compétences aussi. Toute
affirmation chiffrée (durées, taux, doses) est laissée aux chapitres,
qui la sourceront ; ce squelette ne porte que des notions.
Les identifiants sont immuables une fois une carte publiée dessus.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import OrderedDict
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
NIVEAU_NOM = {1: "Repères", 2: "Mécanismes", 3: "Praticien", 4: "Doctrine", 5: "Frontière"}
CARTES_CIBLE = {1: 6, 2: 8, 3: 10, 4: 8, 5: 6}
ETUDE_MIN = {1: 45, 2: 60, 3: 75, 4: 90, 5: 90}
EXERCICES_PAR_NIVEAU = {1: ["flash", "qcm", "relier"], 2: ["qcm", "cas", "flash"], 3: ["cas", "libre", "feuille-blanche"],
                        4: ["lecture", "synthese"], 5: ["lecture", "synthese"]}

SOURCES_DROIT = ["Code de la santé publique (Légifrance)", "Arrêté du 31 juillet 2009 relatif au diplôme d'État d'infirmier (Légifrance)"]

# (clé, titre, ordre, niveau socle, pourquoi, sources primaires)
DOMAINES = [
    ("entree", "L'entrée en IFSI", 1, 2,
     "La porte : Parcoursup ou formation professionnelle, l'écrit, l'oral, le projet, le dossier.",
     ["Arrêté du 13 décembre 2018 relatif à l'admission en IFSI (Légifrance)", "Parcoursup (fiche de formation)", "Instituts de formation (règlement d'admission)", "Ministère de la Santé"]),
    ("sante-publique", "Santé publique et système de santé", 2, 2,
     "La culture sanitaire et sociale que l'écrit et l'oral mesurent, et l'UE 1.2.",
     ["Santé publique France", "Ministère de la Santé (solidarites-sante.gouv.fr)", "HAS", "DREES", "Sécurité sociale (ameli.fr)", "OMS"]),
    ("humaines", "Sciences humaines, droit et éthique", 3, 2,
     "Psychologie, sociologie, anthropologie, législation, déontologie : UE 1.1 et 1.3.",
     SOURCES_DROIT + ["Ordre national des infirmiers (déontologie)", "CCNE (avis)", "CNIL"]),
    ("corps", "Biologie et corps humain", 4, 2,
     "Anatomie, physiologie, cycles de la vie : UE 2.1 et 2.2, la base de tout raisonnement clinique.",
     ["Manuels d'anatomie-physiologie (éditeur, à recouper)", "Inserm", "Collège des enseignants (référentiels universitaires)"]),
    ("pathologies", "Processus pathologiques", 5, 2,
     "Traumatique, infectieux, psychopathologique, dégénératif, obstructif, tumoral : UE 2.3 à 2.9.",
     ["HAS (recommandations)", "Inserm", "Santé publique France", "Collèges des enseignants (référentiels)", "Institut national du cancer"]),
    ("hygiene", "Hygiène et infectiologie", 6, 2,
     "Précautions standard, chaîne de transmission, antisepsie, infections associées aux soins : UE 2.10.",
     ["Société française d'hygiène hospitalière (SF2H)", "Santé publique France", "HAS", "CPias"]),
    ("pharmaco", "Pharmacologie et calculs de doses", 7, 2,
     "Le médicament, ses voies, ses risques, et le calcul juste à chaque fois : UE 2.11 et 4.4.",
     ["ANSM", "Base de données publique des médicaments", "HAS", "Vidal (éditeur, à recouper)", "Omedit"]),
    ("soins", "Soins infirmiers et raisonnement clinique", 8, 2,
     "Le cœur du métier : démarche clinique, projet de soins, confort, relation, urgence, thérapeutiques, palliatif, qualité : UE 3.x et 4.x.",
     SOURCES_DROIT + ["HAS", "Référentiels de bonnes pratiques (sociétés savantes)", "Ordre national des infirmiers"]),
    ("methodes", "Méthodes, communication et anglais", 9, 2,
     "Travailler, écrire, chercher, transmettre, lire en anglais : UE 5.x, 6.1 et 6.2.",
     ["Arrêté du 31 juillet 2009 (Légifrance)", "HAS (transmissions ciblées)", "Bibliothèques universitaires (Cismef, PubMed)"]),
    ("stage", "Stages, compétences et posture", 10, 2,
     "Les dix compétences, le portfolio, l'encadrement, l'organisation du travail, le corps et le rythme.",
     ["Arrêté du 31 juillet 2009, annexe II (compétences)", "Instituts de formation (portfolio)", "INRS (prévention)", "HAS"]),
]
CULTURE = ("culture", "Culture", 11, None, "Le texte du bac : histoire du soin, littérature du corps et de la maladie, débats de société.",
           ["Textes publics choisis", "Presse de fond", "Histoire"])

B: "OrderedDict[str, list]" = OrderedDict()

B["entree"] = [
    ("voies", "Les voies d'accès", "qcm", [], [
        ("Qui entre en IFSI et par où", 1, "Dire les voies d'accès à la formation et laquelle est la sienne", ["Parcoursup", "formation professionnelle continue", "aide-soignant", "passerelle"]),
        ("La voie Parcoursup", 1, "Décrire ce que Parcoursup demande et regarde dans un dossier", ["dossier", "lettre de motivation", "attendus", "classement"]),
        ("La voie de la formation professionnelle", 1, "Dire les conditions et les épreuves de la voie professionnelle", ["expérience", "épreuve écrite", "entretien", "quota"]),
        ("Le calendrier d'une candidature", 2, "Tenir un calendrier de candidature sans rater une date", ["inscription", "vœux", "résultats", "confirmation"]),
        ("Financer sa formation", 2, "Nommer les financements possibles selon sa situation", ["région", "employeur", "France Travail", "promotion professionnelle"]),
        ("L'admission en question : histoire et réformes", 4, "Situer la fin du concours et ce que la réforme a changé", ["concours", "2019", "universitarisation", "critiques"]),
    ]),
    ("ecrit", "L'épreuve écrite", "libre", [], [
        ("Ce que l'écrit mesure", 1, "Dire ce que l'épreuve écrite évalue et sa forme", ["compréhension", "argumentation", "calcul", "durée"]),
        ("Lire un texte sanitaire et social", 2, "Dégager la thèse et les arguments d'un texte d'actualité", ["thèse", "argument", "reformulation", "plan"]),
        ("Argumenter en une page", 2, "Écrire une réponse structurée, personnelle et sans jargon", ["introduction", "deux parties", "exemple", "conclusion"]),
        ("Les calculs de l'écrit", 2, "Résoudre sans calculatrice les opérations attendues", ["fractions", "pourcentages", "règle de trois", "conversions"]),
        ("S'entraîner à l'écrit en conditions", 2, "Faire un sujet complet en temps limité et se corriger avec une grille", ["chronomètre", "grille", "relecture", "erreurs types"]),
    ]),
    ("oral", "L'entretien", "role", [], [
        ("Ce que l'oral mesure", 1, "Dire ce que le jury cherche en vingt minutes", ["motivation", "connaissance du métier", "aptitudes", "expression"]),
        ("Le projet professionnel", 2, "Raconter son parcours et son projet en trois minutes justes", ["parcours", "déclic", "métier réel", "projection"]),
        ("Les questions qui reviennent", 2, "Répondre aux questions classiques sans réciter", ["qualités", "défauts", "situation difficile", "actualité"]),
        ("Le sujet tiré au sort", 2, "Traiter un thème sanitaire ou social à l'oral en dix minutes de préparation", ["thème", "plan", "exemple", "avis"]),
        ("Simuler l'entretien", 2, "Passer un entretien blanc filmé et en tirer trois corrections", ["posture", "regard", "débit", "silence"]),
    ]),
    ("metier", "Le métier tel qu'il est", "cas", [], [
        ("Une journée d'infirmier", 1, "Décrire une journée type dans un service et à domicile", ["relève", "tour", "transmissions", "domicile"]),
        ("Où travaillent les infirmiers", 1, "Nommer les lieux d'exercice et leurs différences", ["hôpital", "libéral", "EHPAD", "scolaire", "entreprise"]),
        ("La formation en trois ans", 1, "Décrire la formation : semestres, unités, stages, diplôme", ["six semestres", "unités d'enseignement", "stages", "grade licence"]),
        ("Les spécialisations et les suites", 2, "Nommer les spécialités et les évolutions après le diplôme", ["puéricultrice", "IADE", "IBODE", "pratique avancée", "cadre"]),
        ("Les mots du métier", 2, "Comprendre le vocabulaire courant d'un service", ["constantes", "prescription", "protocole", "transmissions", "glossaire"]),
    ]),
]

B["sante-publique"] = [
    ("systeme", "Le système de santé", "qcm", [], [
        ("Qui soigne en France", 1, "Nommer les acteurs du système de santé et leurs rôles", ["hôpital public", "clinique", "médecine de ville", "ARS", "ministère"]),
        ("Le parcours de soins", 1, "Suivre un patient du médecin traitant à l'hôpital et au retour", ["médecin traitant", "orientation", "hospitalisation", "sortie"]),
        ("L'hôpital de l'intérieur", 2, "Décrire l'organisation d'un hôpital et d'un service", ["pôle", "service", "cadre", "chef de service", "CME"]),
        ("Les professions de santé", 2, "Distinguer les professions et leur champ", ["médicales", "paramédicales", "auxiliaires", "réglementées"]),
        ("Le financement de l'hôpital", 3, "Expliquer comment un hôpital est payé et ce que ça change au lit du patient", ["tarification à l'activité", "dotation", "ONDAM", "budget"]),
        ("L'hôpital en crise : diagnostics", 4, "Lire un rapport sur l'hôpital et en discuter les causes avancées", ["attractivité", "lits", "urgences", "rapports"]),
    ]),
    ("protection", "La protection sociale", "qcm", [], [
        ("La Sécurité sociale", 1, "Dire ce que couvre la Sécurité sociale et qui la finance", ["1945", "branches", "cotisations", "CSG"]),
        ("Remboursement, complémentaire, reste à charge", 2, "Calculer ce qu'un patient paie pour un soin courant", ["taux", "ticket modérateur", "mutuelle", "ALD", "cent pour cent"]),
        ("La CMU-C à la complémentaire santé solidaire", 2, "Orienter une personne sans couverture", ["CSS", "AME", "PUMa", "droits"]),
        ("Handicap et dépendance", 2, "Nommer les dispositifs d'aide au handicap et à la perte d'autonomie", ["MDPH", "AAH", "APA", "GIR", "EHPAD"]),
        ("Les comptes de la protection sociale", 4, "Discuter les équilibres et les réformes de la protection sociale", ["déficit", "réformes", "solidarité", "assurance"]),
    ]),
    ("population", "La santé des populations", "cas", [], [
        ("Les indicateurs de santé", 1, "Lire une espérance de vie, une mortalité, une prévalence", ["espérance de vie", "mortalité", "morbidité", "prévalence", "incidence"]),
        ("Les déterminants de santé", 2, "Expliquer pourquoi la santé dépend d'autre chose que des soins", ["social", "environnement", "comportements", "génétique", "inégalités"]),
        ("Prévention primaire, secondaire, tertiaire", 1, "Classer une action de prévention", ["vaccination", "dépistage", "éducation", "réadaptation"]),
        ("Les grands plans de santé publique", 2, "Nommer les priorités nationales et ce qu'elles demandent aux soignants", ["tabac", "obésité", "cancer", "santé mentale", "antibiorésistance"]),
        ("Épidémiologie : lire une étude", 3, "Lire une étude épidémiologique et en dire la portée", ["cohorte", "cas-témoins", "biais", "risque relatif"]),
        ("Les inégalités sociales de santé", 4, "Argumenter sur les inégalités de santé et les réponses possibles", ["gradient social", "accès", "territoires", "politiques"]),
        ("Santé mondiale et pandémies", 5, "Suivre l'état de l'art sur une menace sanitaire mondiale", ["OMS", "émergence", "One Health", "préparation"]),
    ]),
    ("actualite", "L'actualité sanitaire et sociale", "libre", [], [
        ("Les thèmes qui tombent", 1, "Nommer les grands thèmes des épreuves et leurs enjeux", ["fin de vie", "vieillissement", "addictions", "précarité", "numérique"]),
        ("Construire un avis sur un sujet de société", 2, "Prendre position sur un thème avec deux arguments et un exemple", ["thèse", "contre-argument", "exemple", "nuance"]),
        ("Lire la presse de santé", 2, "Suivre l'actualité de santé et en garder l'essentiel chaque semaine", ["sources", "fiabilité", "fiche", "revue de presse"]),
        ("Les débats du moment en santé", 4, "Défendre et attaquer une position sur un débat sanitaire actuel", ["controverse", "éthique", "économie", "science"]),
    ]),
]

B["humaines"] = [
    ("psycho", "Psychologie", "cas", [], [
        ("Les grands courants", 1, "Situer les courants de la psychologie et ce qu'ils apportent au soin", ["psychanalyse", "comportementale", "cognitive", "humaniste", "systémique"]),
        ("Le développement de la personne", 2, "Décrire les étapes du développement de l'enfant à la vieillesse", ["attachement", "stades", "adolescence", "vieillissement"]),
        ("Émotions, stress, mécanismes de défense", 2, "Reconnaître un mécanisme de défense chez un patient", ["déni", "régression", "projection", "stress", "coping"]),
        ("La relation soignant-soigné", 2, "Décrire ce qui se joue dans une relation de soin", ["transfert", "distance", "empathie", "juste distance"]),
        ("La psychologie de la douleur et de la maladie chronique", 3, "Accompagner le vécu psychique d'une maladie longue", ["deuil de la santé", "adaptation", "observance", "représentations"]),
        ("Psychologie et neurosciences : débats", 4, "Discuter ce que les neurosciences changent à la psychologie du soin", ["neurosciences", "cognition", "controverses"]),
    ]),
    ("socio", "Sociologie et anthropologie", "cas", [], [
        ("Les concepts de base", 1, "Définir groupe, rôle, statut, norme, culture", ["groupe", "rôle", "norme", "culture", "socialisation"]),
        ("La famille et ses formes", 2, "Décrire les formes de famille et leurs effets sur le soin", ["famille", "aidants", "monoparentalité", "recomposition"]),
        ("Culture, religion et soin", 2, "Adapter un soin à une culture sans juger", ["représentations", "interdits", "rites", "interprète"]),
        ("Le corps et la maladie dans la société", 3, "Analyser une situation de soin avec les outils de l'anthropologie", ["corps", "stigmate", "sick role", "médicalisation"]),
        ("Sociologie des professions de santé", 4, "Lire un travail de sociologie sur les infirmiers et en débattre", ["profession", "genre", "autonomie", "hiérarchie"]),
    ]),
    ("droit", "Législation et responsabilité", "qcm", [], [
        ("Le cadre légal de la profession", 1, "Dire où est écrit ce qu'un infirmier a le droit de faire", ["Code de la santé publique", "R. 4311", "rôle propre", "rôle prescrit"]),
        ("Les droits du patient", 1, "Énumérer les droits du patient et leur texte", ["loi de 2002", "information", "consentement", "dossier", "personne de confiance"]),
        ("Le secret professionnel", 2, "Appliquer le secret et ses exceptions dans un cas concret", ["secret", "partage", "équipe", "dérogations"]),
        ("La responsabilité de l'infirmier", 2, "Distinguer responsabilité civile, pénale, disciplinaire", ["faute", "civile", "pénale", "ordinale", "assurance"]),
        ("Prescription, protocole, délégation", 2, "Dire ce qu'un infirmier fait seul, sur prescription, sur protocole", ["prescription", "protocole", "collaboration", "aide-soignant"]),
        ("La fin de vie dans la loi", 2, "Décrire ce que la loi permet et interdit en fin de vie", ["Claeys-Leonetti", "directives anticipées", "sédation", "obstination déraisonnable"]),
        ("Écrire un signalement ou une déclaration d'événement", 3, "Rédiger une déclaration d'événement indésirable conforme", ["événement indésirable", "signalement", "maltraitance", "traçabilité"]),
        ("La jurisprudence infirmière", 4, "Lire une décision de justice concernant un infirmier et en tirer la règle", ["arrêt", "faute", "défaut de surveillance", "jurisprudence"]),
    ]),
    ("ethique", "Éthique et déontologie", "cas", [], [
        ("Morale, éthique, déontologie", 1, "Distinguer les trois mots et en donner un exemple chacun", ["morale", "éthique", "déontologie", "code"]),
        ("Les principes de l'éthique médicale", 2, "Appliquer bienfaisance, non-malfaisance, autonomie, justice à un cas", ["autonomie", "bienfaisance", "non-malfaisance", "justice"]),
        ("Le code de déontologie infirmier", 2, "Trouver dans le code la règle qui répond à une situation", ["Ordre", "devoirs", "confraternité", "indépendance"]),
        ("Le dilemme éthique au lit du patient", 3, "Conduire une réflexion éthique en équipe sur un cas", ["dilemme", "réunion", "argumentation", "décision collégiale"]),
        ("Les grands débats bioéthiques", 4, "Argumenter sur un débat bioéthique avec ses textes", ["CCNE", "PMA", "fin de vie", "génétique", "lois de bioéthique"]),
        ("Éthique du soin : les courants", 5, "Lire un texte de philosophie du soin et le situer", ["care", "vulnérabilité", "reconnaissance", "philosophie"]),
    ]),
]

B["corps"] = [
    ("bases", "Les bases de la biologie", "flash", [], [
        ("La cellule", 1, "Décrire une cellule et ses organites", ["membrane", "noyau", "mitochondrie", "ADN"]),
        ("Les tissus et les organes", 1, "Classer les tissus et dire comment ils forment un organe", ["épithélial", "conjonctif", "musculaire", "nerveux"]),
        ("Les molécules du vivant", 2, "Nommer les grandes molécules et leur rôle", ["protéines", "glucides", "lipides", "enzymes", "ATP"]),
        ("Génétique et hérédité", 2, "Expliquer une transmission génétique simple", ["gène", "chromosome", "dominant", "récessif", "mutation"]),
        ("Le milieu intérieur et l'homéostasie", 2, "Expliquer comment le corps garde ses constantes", ["homéostasie", "pH", "température", "rétrocontrôle"]),
        ("Biologie moléculaire et soin", 4, "Discuter ce que la biologie moléculaire change dans les soins", ["thérapie génique", "biomarqueurs", "médecine personnalisée"]),
    ]),
    ("grandes-fonctions", "Les grandes fonctions", "relier", [("cardio", "Cœur et vaisseaux"), ("respi", "Respiration"), ("digestif", "Digestion et nutrition"), ("renal", "Rein et équilibre hydrique"), ("nerveux", "Système nerveux et sens"), ("endocrinien", "Hormones"), ("locomoteur", "Os, muscles, peau"), ("sang", "Sang et immunité"), ("reproduction", "Reproduction")], [
        ("Le cœur et la circulation", 1, "Suivre le sang dans le cœur et les vaisseaux", ["oreillettes", "ventricules", "valves", "artères", "veines"], "cardio"),
        ("Pression artérielle et pouls", 2, "Expliquer d'où viennent la pression et le pouls et ce qui les fait varier", ["systole", "diastole", "débit", "résistance"], "cardio"),
        ("L'activité électrique du cœur", 3, "Lire un tracé normal et en nommer les ondes", ["nœud sinusal", "ECG", "onde P", "QRS"], "cardio"),
        ("Les voies respiratoires et les poumons", 1, "Décrire le trajet de l'air et les échanges gazeux", ["trachée", "bronches", "alvéoles", "diffusion"], "respi"),
        ("La mécanique ventilatoire", 2, "Expliquer inspiration, expiration et leur régulation", ["diaphragme", "volumes", "CO2", "centres respiratoires"], "respi"),
        ("Le tube digestif", 1, "Suivre un repas de la bouche au côlon", ["œsophage", "estomac", "intestin grêle", "côlon"], "digestif"),
        ("Digestion, absorption, glandes annexes", 2, "Expliquer le rôle du foie, du pancréas et de la bile", ["foie", "pancréas", "bile", "absorption"], "digestif"),
        ("Les besoins nutritionnels", 2, "Dire les besoins d'un adulte et lire une étiquette", ["calories", "macronutriments", "vitamines", "équilibre"], "digestif"),
        ("Le rein et la formation de l'urine", 1, "Décrire le néphron et ce qu'il fait", ["néphron", "filtration", "réabsorption", "urine"], "renal"),
        ("L'équilibre hydro-électrolytique", 2, "Expliquer le rôle du sodium, du potassium et de l'eau", ["natrémie", "kaliémie", "déshydratation", "œdème"], "renal"),
        ("Neurone, nerf, synapse", 1, "Décrire un neurone et la transmission d'un influx", ["neurone", "axone", "synapse", "neurotransmetteur"], "nerveux"),
        ("Le système nerveux central et périphérique", 2, "Situer les grandes structures et leurs fonctions", ["cerveau", "cervelet", "moelle", "nerfs crâniens", "végétatif"], "nerveux"),
        ("Les organes des sens et la douleur", 2, "Expliquer le trajet d'un message sensoriel et de la douleur", ["récepteurs", "voies", "nociception", "gate control"], "nerveux"),
        ("Les glandes endocrines", 1, "Nommer les glandes et leurs hormones principales", ["hypophyse", "thyroïde", "surrénales", "pancréas", "gonades"], "endocrinien"),
        ("La régulation de la glycémie", 2, "Expliquer insuline et glucagon et ce qui se dérègle", ["insuline", "glucagon", "glycémie", "hypoglycémie"], "endocrinien"),
        ("Le squelette et les articulations", 1, "Nommer les os et les types d'articulations", ["squelette", "articulation", "cartilage", "ligament"], "locomoteur"),
        ("Les muscles et le mouvement", 2, "Expliquer une contraction et un mouvement", ["muscle", "tendon", "contraction", "tonus"], "locomoteur"),
        ("La peau", 1, "Décrire les couches de la peau et ses fonctions", ["épiderme", "derme", "hypoderme", "barrière", "thermorégulation"], "locomoteur"),
        ("Le sang et ses cellules", 1, "Nommer les composants du sang et leur rôle", ["hématies", "leucocytes", "plaquettes", "plasma", "hémoglobine"], "sang"),
        ("L'immunité", 2, "Distinguer immunité innée et acquise et expliquer la vaccination", ["innée", "acquise", "anticorps", "lymphocytes", "vaccin"], "sang"),
        ("L'hémostase", 2, "Expliquer comment le sang coagule et ce qui l'empêche", ["plaquettes", "coagulation", "fibrine", "anticoagulant"], "sang"),
        ("Les appareils reproducteurs", 1, "Décrire les appareils et le cycle féminin", ["cycle", "ovulation", "hormones", "spermatogenèse"], "reproduction"),
        ("Grossesse et accouchement : les bases", 2, "Suivre une grossesse normale et ses étapes", ["fécondation", "placenta", "trimestres", "accouchement"], "reproduction"),
        ("Physiologie intégrée : le cas", 3, "Expliquer une situation clinique en reliant plusieurs fonctions", ["intégration", "compensation", "choc", "raisonnement"]),
        ("Physiologie : l'état de la recherche", 5, "Suivre un sujet de recherche en physiologie et le vulgariser", ["publication", "microbiote", "chronobiologie"]),
    ]),
    ("cycles", "Les cycles de la vie", "cas", [], [
        ("Le nouveau-né et l'enfant", 1, "Décrire les étapes du développement physique de l'enfant", ["croissance", "courbes", "réflexes", "acquisitions"]),
        ("L'adolescence", 2, "Décrire les changements de l'adolescence et leurs risques", ["puberté", "identité", "conduites à risque"]),
        ("L'adulte et le vieillissement", 2, "Distinguer vieillissement normal et pathologique", ["sénescence", "fragilité", "autonomie", "polypathologie"]),
        ("La mort et le corps", 2, "Décrire ce qui se passe à la mort et les soins du corps", ["agonie", "signes", "toilette mortuaire", "rites"]),
        ("Le vieillissement : théories et débats", 4, "Discuter les théories du vieillissement et la longévité", ["théories", "longévité", "prévention", "âgisme"]),
    ]),
]

B["pathologies"] = [
    ("sante-maladie", "Santé, maladie, handicap", "qcm", [], [
        ("Définir la santé et la maladie", 1, "Donner les définitions et leurs limites", ["OMS", "normal", "pathologique", "chronique", "aigu"]),
        ("Le handicap et ses classifications", 1, "Distinguer déficience, incapacité, désavantage", ["CIF", "déficience", "incapacité", "situation de handicap"]),
        ("Les accidents de la vie", 2, "Décrire les grands accidents de la vie et leur prévention", ["accident domestique", "route", "travail", "chute"]),
        ("Vivre avec une maladie chronique", 3, "Construire un accompagnement de maladie chronique", ["éducation thérapeutique", "observance", "aidants", "parcours"]),
        ("Modèles de la maladie : débats", 4, "Comparer modèle biomédical et modèle biopsychosocial", ["biomédical", "biopsychosocial", "chronicité", "critiques"]),
    ]),
    ("trauma", "Processus traumatiques", "cas", [], [
        ("Fractures, entorses, luxations", 1, "Reconnaître et décrire les lésions de l'appareil locomoteur", ["fracture", "entorse", "luxation", "immobilisation"]),
        ("Plaies et brûlures", 1, "Classer une plaie et une brûlure et dire l'urgence", ["plaie", "brûlure", "degré", "surface", "cicatrisation"]),
        ("Le traumatisme crânien et rachidien", 2, "Reconnaître les signes de gravité et la conduite à tenir", ["Glasgow", "rachis", "immobilisation", "surveillance"]),
        ("Le polytraumatisé", 2, "Décrire la prise en charge d'un polytraumatisé", ["choc", "hémorragie", "priorités", "damage control"]),
        ("Surveiller un opéré en traumatologie", 3, "Surveiller un patient opéré et repérer une complication", ["plâtre", "syndrome des loges", "thrombose", "douleur"]),
        ("Traumatologie : les évolutions", 4, "Discuter les évolutions de la prise en charge traumatologique", ["récupération améliorée", "ambulatoire", "doctrine"]),
    ]),
    ("infectieux", "Processus inflammatoires et infectieux", "qcm", [], [
        ("L'inflammation", 1, "Décrire les signes de l'inflammation et son sens", ["rougeur", "chaleur", "douleur", "œdème", "CRP"]),
        ("Bactéries, virus, champignons, parasites", 1, "Distinguer les agents infectieux et leurs traitements", ["bactérie", "virus", "antibiotique", "antiviral", "antifongique"]),
        ("Les grandes infections", 2, "Décrire pneumonie, infection urinaire, méningite, sepsis", ["pneumonie", "infection urinaire", "méningite", "sepsis"]),
        ("VIH, hépatites, tuberculose", 2, "Décrire les trois infections et leur prise en charge", ["VIH", "hépatite", "tuberculose", "dépistage", "traitement"]),
        ("Les maladies auto-immunes", 2, "Expliquer une maladie auto-immune et ses traitements", ["auto-immunité", "lupus", "polyarthrite", "immunosuppresseur"]),
        ("Surveiller un patient infecté", 3, "Surveiller un sepsis et alerter à temps", ["qSOFA", "fièvre", "lactates", "antibiothérapie", "alerte"]),
        ("L'antibiorésistance", 4, "Argumenter sur l'antibiorésistance et le bon usage", ["résistance", "bon usage", "One Health", "plan"]),
        ("Infectiologie : l'état de l'art", 5, "Suivre une émergence infectieuse et la science qui l'accompagne", ["émergence", "vaccins", "surveillance", "publication"]),
    ]),
    ("psy", "Processus psychopathologiques", "cas", [], [
        ("Normal et pathologique en psychiatrie", 1, "Dire ce qui fait passer d'un trouble à une maladie", ["souffrance", "durée", "fonctionnement", "classification"]),
        ("Dépression et troubles anxieux", 1, "Reconnaître une dépression et un trouble anxieux", ["tristesse", "anhédonie", "anxiété", "attaque de panique"]),
        ("Le risque suicidaire", 2, "Évaluer un risque suicidaire et agir", ["idées", "scénario", "urgence", "dangerosité", "protection"]),
        ("Schizophrénie et troubles bipolaires", 2, "Décrire les deux maladies et leurs traitements", ["délire", "hallucination", "manie", "neuroleptiques", "thymorégulateurs"]),
        ("Addictions", 2, "Décrire les addictions, le sevrage et l'accompagnement", ["dépendance", "sevrage", "substitution", "réduction des risques"]),
        ("Troubles du comportement alimentaire et de la personnalité", 2, "Reconnaître un TCA et un trouble de la personnalité", ["anorexie", "boulimie", "borderline", "alliance"]),
        ("L'hospitalisation sous contrainte", 2, "Décrire les soins sans consentement et les droits du patient", ["SDT", "SDRE", "juge", "isolement", "contention"]),
        ("L'entretien infirmier en psychiatrie", 3, "Conduire un entretien d'accueil et un entretien d'aide", ["accueil", "cadre", "écoute", "relance", "transmission"]),
        ("La psychiatrie en débat", 4, "Discuter les critiques et les réformes de la psychiatrie", ["désinstitutionnalisation", "contention", "rétablissement", "pair-aidance"]),
    ]),
    ("degeneratif", "Défaillances organiques et processus dégénératifs", "cas", [], [
        ("L'insuffisance cardiaque", 1, "Décrire l'insuffisance cardiaque et ses signes", ["dyspnée", "œdèmes", "poids", "décompensation"]),
        ("L'insuffisance respiratoire et la BPCO", 2, "Décrire la BPCO et l'insuffisance respiratoire", ["BPCO", "oxygène", "exacerbation", "saturation"]),
        ("L'insuffisance rénale et la dialyse", 2, "Décrire l'insuffisance rénale chronique et la dialyse", ["créatinine", "DFG", "dialyse", "greffe"]),
        ("Le diabète", 1, "Distinguer diabète de type 1 et 2 et leurs complications", ["type 1", "type 2", "HbA1c", "complications", "pied"]),
        ("Maladies neurodégénératives", 2, "Décrire Alzheimer, Parkinson, sclérose en plaques", ["Alzheimer", "Parkinson", "SEP", "troubles cognitifs"]),
        ("L'AVC", 2, "Reconnaître un AVC et dire l'urgence", ["FAST", "thrombolyse", "hémiplégie", "aphasie", "unité neurovasculaire"]),
        ("Le patient polypathologique âgé", 3, "Construire un plan de soins pour un patient âgé polypathologique", ["fragilité", "iatrogénie", "chutes", "dénutrition", "escarre"]),
        ("Vieillissement et défaillances : doctrine", 4, "Discuter les approches de la fragilité et de la dépendance", ["gériatrie", "fragilité", "prévention", "domicile"]),
    ]),
    ("obstructif", "Processus obstructifs", "qcm", [], [
        ("L'infarctus et l'angor", 1, "Reconnaître une douleur thoracique et dire l'urgence", ["angor", "infarctus", "troponine", "coronarographie"]),
        ("Phlébite et embolie pulmonaire", 2, "Décrire la maladie thromboembolique et sa prévention", ["thrombose", "embolie", "anticoagulant", "bas de contention"]),
        ("L'asthme", 1, "Décrire une crise d'asthme et son traitement", ["bronchospasme", "débit de pointe", "bronchodilatateur", "corticoïde"]),
        ("L'occlusion intestinale et la lithiase", 2, "Reconnaître une occlusion et une colique", ["occlusion", "vomissements", "lithiase", "colique néphrétique"]),
        ("L'artériopathie", 2, "Décrire l'artériopathie des membres inférieurs", ["claudication", "ischémie", "pouls", "amputation"]),
        ("Surveiller un patient coronarien", 3, "Surveiller un coronarien et éduquer aux facteurs de risque", ["facteurs de risque", "réadaptation", "traitement", "éducation"]),
    ]),
    ("tumoral", "Processus tumoraux", "cas", [], [
        ("Qu'est-ce qu'un cancer", 1, "Expliquer une tumeur, une métastase, un stade", ["tumeur", "bénin", "malin", "métastase", "stade"]),
        ("Les cancers les plus fréquents", 2, "Décrire sein, prostate, poumon, colorectal et leur dépistage", ["sein", "prostate", "poumon", "colorectal", "dépistage organisé"]),
        ("Chimiothérapie, radiothérapie, chirurgie", 2, "Décrire les traitements et leurs effets indésirables", ["chimiothérapie", "radiothérapie", "chirurgie", "aplasie", "nausées"]),
        ("Les hémopathies", 2, "Décrire leucémies et lymphomes", ["leucémie", "lymphome", "aplasie", "greffe de moelle"]),
        ("Accompagner un patient en oncologie", 3, "Suivre un patient du diagnostic au traitement, annonce comprise", ["annonce", "RCP", "voie centrale", "soins de support"]),
        ("Cancérologie : les évolutions", 4, "Discuter immunothérapie, thérapies ciblées, dépistage", ["immunothérapie", "thérapie ciblée", "surdiagnostic"]),
        ("Oncologie : la recherche", 5, "Suivre un essai clinique et le comprendre", ["essai", "phases", "consentement", "publication"]),
    ]),
]

B["hygiene"] = [
    ("transmission", "La chaîne de transmission", "qcm", [], [
        ("Les micro-organismes et leur transmission", 1, "Décrire la chaîne de transmission et ses maillons", ["réservoir", "porte de sortie", "transmission", "hôte"]),
        ("Les précautions standard", 1, "Appliquer les précautions standard dans tout soin", ["hygiène des mains", "gants", "masque", "AES", "déchets"]),
        ("Les précautions complémentaires", 2, "Choisir contact, gouttelettes ou air selon le germe", ["contact", "gouttelettes", "air", "isolement", "signalétique"]),
        ("L'hygiène des mains", 1, "Réaliser une friction et un lavage conformes", ["friction", "solution hydro-alcoolique", "cinq indications", "ongles"]),
        ("Les accidents d'exposition au sang", 2, "Réagir à un AES et le déclarer", ["AES", "piqûre", "conduite à tenir", "déclaration", "prophylaxie"]),
    ]),
    ("asepsie", "Antisepsie, asepsie, matériel", "cas", [], [
        ("Antiseptiques et désinfectants", 1, "Choisir et utiliser un antiseptique", ["antiseptique", "désinfectant", "spectre", "temps de contact"]),
        ("Nettoyage, désinfection, stérilisation", 2, "Décrire le circuit du matériel réutilisable", ["pré-désinfection", "stérilisation", "traçabilité", "usage unique"]),
        ("L'asepsie d'un soin", 2, "Préparer un soin stérile sans faute d'asepsie", ["champ", "gants stériles", "pince", "matériel"]),
        ("Les infections associées aux soins", 2, "Nommer les principales IAS et leur prévention", ["urinaire", "cathéter", "site opératoire", "pneumonie", "surveillance"]),
        ("Bactéries multirésistantes et épidémie en service", 3, "Gérer un cas de BMR ou une épidémie dans un service", ["BMR", "BHRe", "dépistage", "cohorting", "EOH"]),
        ("Hygiène hospitalière : doctrine et controverses", 4, "Discuter les recommandations d'hygiène et leurs preuves", ["SF2H", "preuves", "coût", "acceptabilité"]),
    ]),
    ("environnement", "Environnement, déchets, alimentation", "qcm", [], [
        ("Les déchets de soins", 1, "Trier un déchet d'activité de soins", ["DASRI", "ménager", "tri", "conteneur", "filière"]),
        ("L'environnement du patient", 2, "Entretenir l'environnement d'un patient et le bionettoyage", ["bionettoyage", "chambre", "surfaces", "linge"]),
        ("L'hygiène alimentaire en service", 2, "Appliquer les règles d'hygiène des repas et de la nutrition entérale", ["chaîne du froid", "repas", "nutrition entérale", "eau"]),
    ]),
]

B["pharmaco"] = [
    ("medicament", "Le médicament", "qcm", [], [
        ("Qu'est-ce qu'un médicament", 1, "Définir un médicament, une DCI, une forme galénique", ["DCI", "princeps", "générique", "forme galénique", "AMM"]),
        ("Les voies d'administration", 1, "Choisir la voie et dire ses contraintes", ["orale", "sous-cutanée", "intramusculaire", "intraveineuse", "autres"]),
        ("Pharmacocinétique", 2, "Expliquer absorption, distribution, métabolisme, élimination", ["absorption", "distribution", "métabolisme", "élimination", "demi-vie"]),
        ("Pharmacodynamie et effets indésirables", 2, "Expliquer l'effet d'un médicament et ses effets indésirables", ["récepteur", "dose-effet", "effet indésirable", "pharmacovigilance"]),
        ("Interactions et populations à risque", 2, "Repérer une interaction et adapter aux personnes âgées, enfants, femmes enceintes", ["interaction", "insuffisance rénale", "âgé", "grossesse"]),
        ("Le circuit du médicament", 2, "Décrire la prescription, la dispensation, l'administration et la traçabilité", ["prescription", "pharmacie", "administration", "traçabilité", "stupéfiants"]),
        ("Pharmacologie : les débats", 4, "Discuter l'évaluation, le prix et la sécurité des médicaments", ["essais", "prix", "déremboursement", "scandales"]),
    ]),
    ("classes", "Les classes thérapeutiques", "relier", [], [
        ("Antalgiques et anti-inflammatoires", 1, "Nommer les paliers antalgiques et leurs surveillances", ["paliers", "paracétamol", "morphine", "AINS", "surveillance"]),
        ("Antibiotiques", 2, "Nommer les grandes familles et les règles de bon usage", ["familles", "spectre", "durée", "allergie", "résistance"]),
        ("Anticoagulants et antiagrégants", 2, "Surveiller un patient sous anticoagulant", ["héparine", "AVK", "AOD", "INR", "saignement"]),
        ("Médicaments du cœur et de la tension", 2, "Nommer les classes cardiovasculaires et leurs surveillances", ["bêtabloquant", "IEC", "diurétique", "digitalique", "pression"]),
        ("Insuline et antidiabétiques", 2, "Administrer et surveiller un traitement du diabète", ["insuline", "schéma", "glycémie", "hypoglycémie", "metformine"]),
        ("Psychotropes", 2, "Nommer les psychotropes et leurs risques", ["anxiolytique", "antidépresseur", "neuroleptique", "hypnotique", "sevrage"]),
        ("Solutés, électrolytes et nutrition parentérale", 2, "Choisir un soluté et le surveiller", ["NaCl", "glucosé", "potassium", "perfusion", "surcharge"]),
        ("Chimiothérapies et biothérapies", 3, "Manipuler et surveiller une chimiothérapie en sécurité", ["cytotoxique", "extravasation", "protection", "biothérapie"]),
        ("Vaccins et sérums", 2, "Expliquer le calendrier vaccinal et une injection vaccinale", ["calendrier", "rappel", "contre-indication", "aiguille"]),
    ]),
    ("calculs", "Les calculs de doses", "libre", [], [
        ("Unités et conversions", 1, "Convertir masses, volumes et concentrations sans erreur", ["mg", "g", "mL", "pourcentage", "conversion"]),
        ("Dose, concentration, volume", 1, "Calculer un volume à prélever à partir d'une prescription", ["dose", "concentration", "volume", "règle de trois"]),
        ("Débits de perfusion", 2, "Calculer un débit en gouttes par minute et en mL par heure", ["débit", "gouttes", "mL/h", "durée", "pousse-seringue"]),
        ("Dilutions et reconstitutions", 2, "Reconstituer et diluer un médicament selon la prescription", ["reconstitution", "dilution", "solvant", "concentration finale"]),
        ("Doses par poids et par surface", 2, "Calculer une dose en mg/kg et en mg/m²", ["poids", "surface corporelle", "pédiatrie", "chimiothérapie"]),
        ("Le calcul juste en situation", 3, "Faire un calcul complet sous pression et le faire vérifier", ["double contrôle", "vraisemblance", "erreur", "alerte"]),
    ]),
    ("securite", "La sécurité du médicament", "cas", [], [
        ("Les cinq B", 1, "Vérifier bon patient, bon médicament, bonne dose, bonne voie, bon moment", ["cinq B", "identitovigilance", "étiquette", "vérification"]),
        ("Les erreurs médicamenteuses", 2, "Analyser une erreur médicamenteuse et ses causes", ["erreur", "never event", "déclaration", "REMED", "facteurs humains"]),
        ("Les médicaments à risque", 2, "Nommer les médicaments à risque et leurs règles", ["potassium", "insuline", "anticoagulants", "morphiniques", "double contrôle"]),
        ("L'administration en pratique", 3, "Préparer et administrer une tournée de médicaments sans erreur", ["pilulier", "check-list", "interruption", "traçabilité"]),
    ]),
]

B["soins"] = [
    ("clinique", "Raisonnement et démarche clinique", "cas", [], [
        ("Observer un patient", 1, "Recueillir les signes par les cinq sens et les constantes", ["observation", "constantes", "signes", "recueil"]),
        ("Les constantes et leurs normes", 1, "Mesurer et interpréter température, pouls, tension, saturation, fréquence respiratoire, douleur", ["température", "pouls", "tension", "SpO2", "EVA"]),
        ("Le recueil de données", 2, "Conduire un recueil de données structuré à l'entrée", ["anamnèse", "besoins", "antécédents", "traitement", "entourage"]),
        ("Les besoins et les modèles de soins", 2, "Utiliser un modèle conceptuel pour analyser une situation", ["Henderson", "quatorze besoins", "Orem", "modèle"]),
        ("Le diagnostic infirmier", 2, "Formuler un diagnostic infirmier et un problème en collaboration", ["diagnostic infirmier", "problème traité en collaboration", "signes", "cause"]),
        ("Le raisonnement clinique en situation", 3, "Analyser une situation clinique complète et prioriser", ["hypothèses", "priorités", "risques", "jugement clinique"]),
        ("Les théories de soins infirmiers", 4, "Comparer les grandes théories et dire ce qu'elles changent", ["Nightingale", "Peplau", "Watson", "paradigmes"]),
        ("La discipline infirmière : recherche", 5, "Suivre la recherche en sciences infirmières", ["sciences infirmières", "doctorat", "revues", "evidence"]),
    ]),
    ("projet", "Le projet de soins et l'organisation", "cas", [], [
        ("Le projet de soins", 1, "Dire ce qu'est un projet de soins et qui y contribue", ["objectifs", "actions", "évaluation", "équipe", "patient"]),
        ("Planifier une journée de soins", 2, "Organiser les soins d'un secteur sur une journée", ["planification", "priorités", "délégation", "imprévus"]),
        ("Les rôles infirmiers et l'interprofessionnalité", 2, "Situer l'infirmier dans l'équipe et ce que chacun fait", ["rôle propre", "aide-soignant", "médecin", "kiné", "coordination"]),
        ("Le dossier de soins et les transmissions", 2, "Tenir un dossier et faire des transmissions ciblées", ["dossier", "transmissions ciblées", "données", "actions", "résultats"]),
        ("Coordonner un parcours complexe", 3, "Organiser une sortie ou un parcours avec plusieurs intervenants", ["sortie", "domicile", "HAD", "coordination", "aidants"]),
        ("Organisation du travail : doctrine", 4, "Discuter les modèles d'organisation des soins", ["ratio", "lean", "magnet", "charge de travail"]),
    ]),
    ("confort", "Soins de confort et de bien-être", "cas", [], [
        ("La toilette et l'habillage", 1, "Faire une toilette en respectant pudeur et autonomie", ["toilette", "pudeur", "autonomie", "peau"]),
        ("L'alimentation et l'hydratation", 1, "Aider à manger et surveiller l'hydratation", ["repas", "fausse route", "hydratation", "dénutrition"]),
        ("L'élimination", 2, "Prendre en charge élimination urinaire et fécale, sonde comprise", ["incontinence", "sonde", "constipation", "stomie"]),
        ("Le sommeil, la mobilisation, la prévention des chutes", 2, "Installer, mobiliser et prévenir les chutes et escarres", ["positions", "transfert", "escarre", "chute", "contention"]),
        ("La douleur : évaluer et soulager", 2, "Évaluer une douleur et mettre en œuvre les moyens non médicamenteux", ["échelles", "Algoplus", "non médicamenteux", "réévaluation"]),
        ("Le confort en situation complexe", 3, "Adapter les soins de confort à un patient dépendant ou en fin de vie", ["dépendance", "soins de bouche", "positionnement", "dignité"]),
    ]),
    ("relation", "Soins relationnels", "role", [], [
        ("L'écoute et la communication", 1, "Écouter, reformuler et se taire à bon escient", ["écoute active", "reformulation", "non verbal", "silence"]),
        ("L'entretien d'accueil", 2, "Accueillir un patient et sa famille", ["accueil", "présentation", "information", "angoisse"]),
        ("La relation d'aide", 2, "Conduire une relation d'aide selon Rogers", ["empathie", "congruence", "regard positif", "relation d'aide"]),
        ("Annoncer, informer, rassurer", 2, "Informer un patient et accompagner une mauvaise nouvelle", ["annonce", "information", "consentement", "espoir"]),
        ("Le patient agressif, confus ou en refus", 3, "Désamorcer une situation tendue et respecter un refus", ["agressivité", "confusion", "refus de soin", "négociation"]),
        ("La relation de soin : doctrine", 4, "Discuter les courants de la relation de soin et le care", ["care", "paternalisme", "décision partagée", "sollicitude"]),
    ]),
    ("urgence", "Soins d'urgence", "cas", [], [
        ("Les gestes qui sauvent", 1, "Réaliser l'alerte, la RCP et l'usage d'un défibrillateur", ["alerte", "massage", "défibrillateur", "PLS", "AFGSU"]),
        ("Reconnaître une détresse vitale", 2, "Repérer une détresse respiratoire, circulatoire ou neurologique", ["détresse", "ABCDE", "choc", "coma"]),
        ("Le chariot d'urgence et les médicaments d'urgence", 2, "Connaître le chariot et les premiers médicaments", ["chariot", "adrénaline", "oxygène", "voie veineuse", "vérification"]),
        ("Hémorragie, obstruction, malaise, convulsion", 2, "Agir devant une hémorragie, une obstruction, un malaise, une crise", ["compression", "Heimlich", "hypoglycémie", "convulsion"]),
        ("L'urgence en service : cas", 3, "Conduire les premières minutes d'une urgence en attendant le médecin", ["priorités", "appel", "délégation", "transmission"]),
        ("Situations sanitaires exceptionnelles", 4, "Décrire le plan blanc, le damage control et les afflux massifs", ["plan blanc", "tri", "damage control", "attentat"]),
    ]),
    ("techniques", "Thérapeutiques et gestes techniques", "cas", [("prelevements", "Prélèvements"), ("injections", "Injections et perfusions"), ("dispositifs", "Sondes, drains, pansements")], [
        ("Les prélèvements sanguins", 1, "Réaliser une prise de sang et une hémoculture", ["tubes", "ordre", "hémoculture", "garrot", "identification"], "prelevements"),
        ("Glycémie capillaire, ECBU, autres prélèvements", 2, "Réaliser les prélèvements courants et les acheminer", ["glycémie", "ECBU", "prélèvement", "acheminement"], "prelevements"),
        ("Les gaz du sang et l'ECG", 3, "Réaliser un gaz du sang et un ECG et repérer l'anormal", ["gaz du sang", "ECG", "dérivations", "anomalie"], "prelevements"),
        ("Injections sous-cutanée et intramusculaire", 1, "Réaliser une injection selon la voie", ["site", "aiguille", "angle", "rotation"], "injections"),
        ("La voie veineuse périphérique", 2, "Poser, surveiller et retirer un cathéter périphérique", ["pose", "fixation", "surveillance", "phlébite", "retrait"], "injections"),
        ("Perfusions et pousse-seringues", 2, "Préparer et surveiller une perfusion et un pousse-seringue", ["montage", "débit", "compatibilité", "alarme"], "injections"),
        ("Voies centrales et chambres implantables", 3, "Manipuler une voie centrale et une chambre implantable", ["PICC", "chambre", "aiguille de Huber", "rinçage", "infection"], "injections"),
        ("Transfusion", 3, "Réaliser une transfusion et surveiller ses incidents", ["groupe", "contrôle ultime", "surveillance", "incident", "hémovigilance"], "injections"),
        ("Les pansements", 1, "Refaire un pansement simple et un pansement complexe", ["plaie", "propre", "détersion", "pansement", "cicatrisation"], "dispositifs"),
        ("Sonde urinaire, sonde gastrique", 2, "Poser et surveiller une sonde urinaire et une sonde gastrique", ["sondage", "asepsie", "surveillance", "retrait"], "dispositifs"),
        ("Drains, stomies, trachéotomie", 3, "Surveiller un drain, une stomie et une trachéotomie", ["drain", "stomie", "trachéotomie", "aspiration", "appareillage"], "dispositifs"),
        ("Oxygénothérapie et aérosols", 2, "Administrer de l'oxygène et un aérosol", ["lunettes", "masque", "débit", "aérosol", "humidification"], "dispositifs"),
        ("Le geste technique : doctrine et preuves", 4, "Discuter les recommandations qui changent un geste courant", ["recommandation", "preuve", "pratique", "changement"]),
    ]),
    ("risques", "Gestion des risques et qualité", "cas", [], [
        ("La sécurité du patient", 1, "Nommer les risques d'un séjour et les barrières", ["identitovigilance", "chute", "escarre", "infection", "erreur"]),
        ("Vigilances et déclaration", 2, "Déclarer un événement indésirable et connaître les vigilances", ["vigilances", "événement indésirable", "FEI", "culture de sécurité"]),
        ("L'évaluation des pratiques", 2, "Participer à un audit et à une revue de morbidité", ["audit", "RMM", "indicateurs", "certification"]),
        ("Analyser un événement indésirable grave", 3, "Conduire une analyse de cause selon une méthode", ["ALARM", "causes", "barrières", "plan d'action"]),
        ("Qualité et sécurité : doctrine", 4, "Discuter la certification, les indicateurs et leurs limites", ["HAS", "certification", "indicateurs", "bureaucratie"]),
    ]),
    ("education", "Soins éducatifs et préventifs", "cas", [], [
        ("Éduquer, informer, conseiller", 1, "Distinguer les trois et donner un exemple", ["information", "conseil", "éducation", "prévention"]),
        ("L'éducation thérapeutique du patient", 2, "Construire une séance d'éducation thérapeutique", ["diagnostic éducatif", "objectifs", "séance", "évaluation", "programme"]),
        ("Prévention et dépistage au quotidien", 2, "Saisir chaque soin pour prévenir", ["tabac", "vaccination", "dépistage", "nutrition", "activité"]),
        ("Éduquer un patient chronique : cas", 3, "Conduire un accompagnement éducatif sur plusieurs mois", ["diabète", "insuffisance cardiaque", "asthme", "autonomie"]),
        ("Éducation et prévention : doctrine", 4, "Discuter l'efficacité et l'éthique de l'éducation en santé", ["littératie", "efficacité", "responsabilisation", "nudge"]),
    ]),
    ("palliatif", "Soins palliatifs et fin de vie", "cas", [], [
        ("Les soins palliatifs", 1, "Dire ce que sont les soins palliatifs et où ils se font", ["définition", "unité", "équipe mobile", "domicile"]),
        ("Les symptômes de la fin de vie", 2, "Soulager douleur, dyspnée, encombrement, anxiété", ["douleur", "dyspnée", "râles", "anxiété", "sédation"]),
        ("Accompagner le patient et ses proches", 2, "Accompagner une famille et un patient jusqu'au décès", ["proches", "deuil", "rites", "présence"]),
        ("La décision en fin de vie", 3, "Participer à une procédure collégiale et à une limitation de traitement", ["collégialité", "LATA", "directives", "sédation profonde"]),
        ("Fin de vie : les débats", 4, "Argumenter sur l'aide à mourir avec les textes et les positions", ["aide à mourir", "euthanasie", "suicide assisté", "convention citoyenne"]),
    ]),
    ("cas-transverses", "Les cas transverses", "cas", [], [
        ("Une chute la nuit en gériatrie", 3, "Gérer une chute nocturne : évaluation, alerte, déclaration, prévention", ["chute", "traumatisme", "déclaration", "prévention"]),
        ("Un patient diabétique en hypoglycémie", 3, "Reconnaître et traiter une hypoglycémie, puis éduquer", ["hypoglycémie", "resucrage", "insuline", "éducation"]),
        ("Une fièvre sur cathéter", 3, "Suspecter une infection sur cathéter et agir", ["fièvre", "cathéter", "hémocultures", "retrait", "antibiotique"]),
        ("Une douleur thoracique dans le couloir", 3, "Prendre en charge une douleur thoracique dès la première minute", ["douleur thoracique", "ECG", "alerte", "surveillance"]),
        ("Un refus de soin chez une personne confuse", 3, "Concilier refus, sécurité et droits", ["refus", "confusion", "consentement", "personne de confiance"]),
        ("Une erreur de médicament découverte", 3, "Réagir à une erreur médicamenteuse et la déclarer", ["erreur", "patient", "médecin", "déclaration", "analyse"]),
        ("Une sortie à domicile d'un patient seul", 3, "Organiser une sortie sûre pour un patient isolé", ["sortie", "domicile", "aides", "libéral", "coordination"]),
        ("Une tentative de suicide aux urgences", 3, "Accueillir et sécuriser une personne après une tentative de suicide", ["évaluation", "sécurité", "psychiatre", "entourage"]),
    ]),
]

B["methodes"] = [
    ("travail", "Méthodes de travail", "libre", [], [
        ("Apprendre à apprendre", 1, "Organiser ses révisions et sa mémoire", ["répétition espacée", "fiches", "planning", "sommeil"]),
        ("Prendre des notes et lire un cours", 1, "Prendre des notes utiles et relire efficacement", ["notes", "structure", "surlignage", "relecture"]),
        ("Écrire un travail écrit", 2, "Rédiger une analyse de situation ou un travail de fin d'études", ["problématique", "plan", "citation", "bibliographie"]),
        ("Les évaluations de l'IFSI", 2, "Connaître les formes d'évaluation et s'y préparer", ["partiels", "analyse de pratique", "portfolio", "rattrapage"]),
        ("Le mémoire de fin d'études", 3, "Conduire un travail de fin d'études du sujet à la soutenance", ["question de départ", "cadre", "enquête", "soutenance"]),
    ]),
    ("recherche", "Recherche documentaire et démarche de recherche", "libre", [], [
        ("Trouver une source fiable", 1, "Distinguer une source fiable d'un site commercial", ["HAS", "PubMed", "Cismef", "fiabilité", "conflit d'intérêts"]),
        ("Lire un article scientifique", 2, "Lire un résumé et une méthode et en dire la portée", ["résumé", "méthode", "résultats", "limites", "niveau de preuve"]),
        ("La démarche de recherche", 2, "Décrire les étapes d'une recherche et ses outils", ["question", "hypothèse", "questionnaire", "entretien", "éthique"]),
        ("Les pratiques fondées sur les preuves", 3, "Chercher et appliquer une recommandation à sa pratique", ["EBN", "recommandation", "grade", "application"]),
        ("Écrire pour publier", 5, "Contribuer à un article ou une communication professionnelle", ["revue", "congrès", "poster", "relecture"]),
    ]),
    ("communication", "Communication écrite et orale", "role", [], [
        ("Les transmissions orales", 1, "Faire une relève claire et complète", ["relève", "SAED", "priorités", "concision"]),
        ("Écrire dans le dossier", 2, "Écrire une transmission ciblée juste et opposable", ["cible", "données", "actions", "résultats", "signature"]),
        ("Le téléphone et le mail professionnels", 2, "Appeler un médecin, écrire un mail, joindre une famille", ["appel", "SBAR", "mail", "confidentialité"]),
        ("Présenter un cas en réunion", 3, "Présenter un patient en staff ou en réunion de synthèse", ["synthèse", "staff", "pluridisciplinaire", "argument"]),
        ("Conduire un projet", 3, "Mener un petit projet de service de l'idée au bilan", ["projet", "objectifs", "planning", "bilan"]),
    ]),
    ("anglais", "Anglais professionnel", "flash", [], [
        ("Le vocabulaire du corps et des soins", 1, "Nommer en anglais le corps, les symptômes, les soins courants", ["body", "symptoms", "pain", "nurse", "ward"]),
        ("Accueillir un patient en anglais", 2, "Conduire un accueil et un recueil simples en anglais", ["greeting", "history", "allergies", "medication"]),
        ("Lire un article en anglais", 3, "Lire un résumé d'article de soins infirmiers en anglais", ["abstract", "methods", "findings", "nursing"]),
    ]),
]

B["stage"] = [
    ("competences", "Les dix compétences", "qcm", [], [
        ("Les dix compétences du référentiel", 1, "Énumérer les dix compétences et les regrouper", ["évaluer", "concevoir", "accompagner", "mettre en œuvre", "éduquer", "communiquer", "analyser", "rechercher", "organiser", "former"]),
        ("Les unités d'enseignement et les semestres", 1, "Situer chaque unité d'enseignement dans les six semestres", ["UE 1 à 6", "semestres", "crédits", "validation"]),
        ("Le portfolio", 2, "Remplir un portfolio avec des situations vécues", ["portfolio", "situations", "critères", "indicateurs", "auto-évaluation"]),
        ("Les actes et activités infirmiers", 2, "Relier un acte au texte qui l'autorise", ["actes", "R. 4311-5", "R. 4311-7", "prescription", "protocole"]),
        ("Le référentiel en question", 4, "Discuter les réformes du référentiel et la réingénierie", ["2009", "réingénierie", "universitarisation", "pratique avancée"]),
    ]),
    ("terrain", "Le stage sur le terrain", "cas", [], [
        ("Arriver en stage", 1, "Se présenter, comprendre le service, poser les objectifs", ["présentation", "livret d'accueil", "objectifs", "tuteur"]),
        ("Le tuteur, le maître de stage, le formateur", 1, "Distinguer les rôles de ceux qui encadrent", ["tuteur", "maître de stage", "formateur référent", "professionnel de proximité"]),
        ("Les quatre types de stage", 2, "Décrire les quatre familles de stage et ce qu'on y apprend", ["courte durée", "longue durée", "psychiatrie", "lieu de vie"]),
        ("L'analyse de pratique", 2, "Écrire une analyse de situation vécue en stage", ["situation", "questionnement", "analyse", "apprentissage"]),
        ("Le bilan de stage et l'évaluation", 2, "Préparer un bilan de stage et lire une évaluation", ["bilan", "critères", "acquis", "axes"]),
        ("Le stage difficile", 3, "Faire face à un stage difficile : conflit, maltraitance, échec", ["conflit", "signalement", "soutien", "recours"]),
    ]),
    ("posture", "Posture, corps, rythme", "cas", [], [
        ("La tenue et l'attitude professionnelles", 1, "Tenir la tenue, l'hygiène et l'attitude attendues", ["tenue", "bijoux", "téléphone", "vouvoiement"]),
        ("Ménager son dos et son corps", 2, "Appliquer les principes de manutention et de prévention", ["manutention", "lève-personne", "posture", "TMS"]),
        ("Le travail de nuit et les horaires", 2, "Gérer les horaires décalés et leur effet sur la santé", ["nuit", "douze heures", "sommeil", "vigilance"]),
        ("L'épuisement et la violence au travail", 3, "Repérer un épuisement, une violence, et savoir demander de l'aide", ["burn-out", "violence", "médecine du travail", "soutien"]),
        ("Conditions de travail des infirmiers : doctrine", 4, "Lire une enquête sur les conditions de travail et en débattre", ["enquête", "attractivité", "ratios", "sens"]),
    ]),
    ("encadrer", "Encadrer et former", "role", [], [
        ("Accueillir un étudiant ou un nouveau", 2, "Accueillir et guider un étudiant sur une journée", ["accueil", "objectifs", "démonstration", "feedback"]),
        ("Le tutorat", 3, "Être tuteur : objectifs, suivi, évaluation", ["tutorat", "contrat", "suivi", "évaluation"]),
        ("Former ses pairs", 3, "Préparer et animer une formation courte en service", ["formation", "objectifs", "support", "évaluation"]),
        ("La pédagogie en santé : doctrine", 4, "Discuter les approches pédagogiques en formation infirmière", ["simulation", "compétences", "réflexivité", "évaluation"]),
    ]),
    ("apres", "Après le diplôme", "qcm", [], [
        ("Le premier poste", 2, "Choisir et négocier un premier poste", ["CDD", "titularisation", "libéral", "intérim", "salaire"]),
        ("Les spécialités et la pratique avancée", 3, "Décrire les formations de spécialité et d'infirmier en pratique avancée", ["IADE", "IBODE", "puéricultrice", "IPA", "master"]),
        ("L'exercice libéral", 3, "Décrire l'installation et les règles du libéral", ["installation", "conventionnement", "NGAP", "tournée", "URSSAF"]),
        ("La profession infirmière : histoire et avenir", 4, "Situer l'histoire de la profession et ses évolutions", ["histoire", "Nightingale", "religieuses", "professionnalisation", "avenir"]),
        ("La recherche infirmière en France", 5, "Suivre l'état de la recherche infirmière et y contribuer", ["PHRIP", "doctorat", "chaires", "publication"]),
    ]),
]

B["culture"] = [
    ("histoire", "Histoire du soin", "lecture", [], [
        ("Des hospices à l'hôpital moderne", 1, "Raconter en trois étapes l'histoire de l'hôpital", ["hospice", "Hôtel-Dieu", "hôpital moderne", "1945"]),
        ("Les grandes figures", 2, "Situer Nightingale, Pasteur, Semmelweis et ce qu'ils ont changé", ["Nightingale", "Pasteur", "Semmelweis", "hygiène"]),
        ("Les épidémies qui ont fait l'histoire", 2, "Raconter une épidémie et ce qu'elle a changé", ["peste", "choléra", "grippe", "sida", "covid"]),
    ]),
    ("lectures", "Lectures du corps et de la maladie", "lecture", [], [
        ("Un roman de la maladie", 2, "Lire un texte littéraire sur la maladie et en parler", ["littérature", "récit", "maladie", "témoignage"]),
        ("Un film ou un documentaire sur l'hôpital", 2, "Regarder et discuter une œuvre sur le soin", ["documentaire", "fiction", "hôpital", "regard"]),
        ("La philosophie et le corps", 4, "Lire un texte philosophique sur le corps, la souffrance ou la mort", ["Canguilhem", "Ricoeur", "corps", "souffrance"]),
    ]),
]

# Ponts entre domaines : prérequis nommés en plus de ceux de la branche.
CROSS = {
    "soins.cas-transverses.une-chute-la-nuit-en-geriatrie": ["pathologies.degeneratif.le-patient-polypathologique-age", "soins.confort.le-sommeil-la-mobilisation-la-prevention-des-chutes", "soins.risques.vigilances-et-declaration"],
    "soins.cas-transverses.un-patient-diabetique-en-hypoglycemie": ["pathologies.degeneratif.le-diabete", "pharmaco.classes.insuline-et-antidiabetiques", "soins.education.l-education-therapeutique-du-patient"],
    "soins.cas-transverses.une-fievre-sur-catheter": ["hygiene.asepsie.les-infections-associees-aux-soins", "soins.techniques.la-voie-veineuse-peripherique", "pathologies.infectieux.les-grandes-infections"],
    "soins.cas-transverses.une-douleur-thoracique-dans-le-couloir": ["pathologies.obstructif.l-infarctus-et-l-angor", "soins.urgence.reconnaitre-une-detresse-vitale"],
    "soins.cas-transverses.un-refus-de-soin-chez-une-personne-confuse": ["humaines.droit.les-droits-du-patient", "soins.relation.le-patient-agressif-confus-ou-en-refus"],
    "soins.cas-transverses.une-erreur-de-medicament-decouverte": ["pharmaco.securite.les-erreurs-medicamenteuses", "humaines.droit.la-responsabilite-de-l-infirmier"],
    "soins.cas-transverses.une-sortie-a-domicile-d-un-patient-seul": ["soins.projet.coordonner-un-parcours-complexe", "sante-publique.protection.handicap-et-dependance"],
    "soins.cas-transverses.une-tentative-de-suicide-aux-urgences": ["pathologies.psy.le-risque-suicidaire", "soins.relation.l-entretien-d-accueil"],
    "pharmaco.calculs.debits-de-perfusion": ["soins.techniques.perfusions-et-pousse-seringues"],
    "soins.techniques.transfusion": ["corps.grandes-fonctions.le-sang-et-ses-cellules"],
    "soins.palliatif.la-decision-en-fin-de-vie": ["humaines.droit.la-fin-de-vie-dans-la-loi"],
    "entree.oral.le-sujet-tire-au-sort": ["sante-publique.actualite.construire-un-avis-sur-un-sujet-de-societe"],
}
# Ponts « voir aussi » sans prérequis.
PONTS = {
    "entree.ecrit.les-calculs-de-l-ecrit": ["pharmaco.calculs.unites-et-conversions"],
    "entree.metier.la-formation-en-trois-ans": ["stage.competences.les-unites-d-enseignement-et-les-semestres"],
    "hygiene.transmission.les-precautions-standard": ["pathologies.infectieux.bacteries-virus-champignons-parasites"],
    "corps.grandes-fonctions.l-immunite": ["pharmaco.classes.vaccins-et-serums"],
    "humaines.droit.le-secret-professionnel": ["methodes.communication.ecrire-dans-le-dossier"],
    "stage.competences.les-dix-competences-du-referentiel": ["soins.clinique.le-raisonnement-clinique-en-situation"],
}

# Les mots qu'Arthur entend, et où ils vivent dans l'arbre.
MOTS_CLES = {
    "Parcoursup": ["entree.voies.la-voie-parcoursup"],
    "oral, jury": ["entree.oral.ce-que-l-oral-mesure", "entree.oral.simuler-l-entretien"],
    "UE": ["stage.competences.les-unites-d-enseignement-et-les-semestres"],
    "portfolio": ["stage.competences.le-portfolio"],
    "rôle propre": ["humaines.droit.le-cadre-legal-de-la-profession", "soins.projet.les-roles-infirmiers-et-l-interprofessionnalite"],
    "transmissions ciblées": ["soins.projet.le-dossier-de-soins-et-les-transmissions", "methodes.communication.ecrire-dans-le-dossier"],
    "constantes": ["soins.clinique.les-constantes-et-leurs-normes"],
    "calcul de doses": ["pharmaco.calculs.dose-concentration-volume", "pharmaco.calculs.debits-de-perfusion"],
    "précautions standard": ["hygiene.transmission.les-precautions-standard"],
    "AFGSU": ["soins.urgence.les-gestes-qui-sauvent"],
    "diagnostic infirmier": ["soins.clinique.le-diagnostic-infirmier"],
    "IPA": ["stage.apres.les-specialites-et-la-pratique-avancee"],
}

# Le parcours vers l'entrée en IFSI : douze semaines, niveaux 1 et 2.
PARCOURS = [
    (1, "Le métier et la porte", ["entree.voies.qui-entre-en-ifsi-et-par-ou", "entree.metier.une-journee-d-infirmier", "entree.metier.ou-travaillent-les-infirmiers", "entree.metier.la-formation-en-trois-ans"], "entree.voies.la-voie-parcoursup"),
    (2, "Le système de santé", ["sante-publique.systeme.qui-soigne-en-france", "sante-publique.systeme.le-parcours-de-soins", "sante-publique.protection.la-securite-sociale", "sante-publique.population.prevention-primaire-secondaire-tertiaire"], "entree.voies.la-voie-de-la-formation-professionnelle"),
    (3, "Le corps, premières fonctions", ["corps.bases.la-cellule", "corps.bases.les-tissus-et-les-organes", "corps.grandes-fonctions.le-coeur-et-la-circulation", "corps.grandes-fonctions.les-voies-respiratoires-et-les-poumons"], "entree.ecrit.ce-que-l-ecrit-mesure"),
    (4, "Lire et argumenter", ["entree.ecrit.lire-un-texte-sanitaire-et-social", "sante-publique.actualite.les-themes-qui-tombent", "humaines.ethique.morale-ethique-deontologie", "humaines.droit.les-droits-du-patient"], "entree.ecrit.argumenter-en-une-page"),
    (5, "Compter juste", ["entree.ecrit.les-calculs-de-l-ecrit", "pharmaco.calculs.unites-et-conversions", "pharmaco.calculs.dose-concentration-volume", "corps.grandes-fonctions.le-tube-digestif"], "sante-publique.actualite.construire-un-avis-sur-un-sujet-de-societe"),
    (6, "Hygiène et gestes de base", ["hygiene.transmission.les-micro-organismes-et-leur-transmission", "hygiene.transmission.les-precautions-standard", "hygiene.transmission.l-hygiene-des-mains", "soins.urgence.les-gestes-qui-sauvent"], "entree.oral.ce-que-l-oral-mesure"),
    (7, "La personne", ["humaines.psycho.les-grands-courants", "humaines.socio.les-concepts-de-base", "corps.cycles.le-nouveau-ne-et-l-enfant", "corps.cycles.l-adulte-et-le-vieillissement"], "entree.oral.le-projet-professionnel"),
    (8, "Santé, maladie, société", ["pathologies.sante-maladie.definir-la-sante-et-la-maladie", "pathologies.sante-maladie.le-handicap-et-ses-classifications", "sante-publique.population.les-indicateurs-de-sante", "sante-publique.population.les-determinants-de-sante"], "sante-publique.actualite.lire-la-presse-de-sante"),
    (9, "Le soin au quotidien", ["soins.clinique.observer-un-patient", "soins.clinique.les-constantes-et-leurs-normes", "soins.confort.la-toilette-et-l-habillage", "soins.relation.l-ecoute-et-la-communication"], "entree.oral.les-questions-qui-reviennent"),
    (10, "Le cadre du métier", ["humaines.droit.le-cadre-legal-de-la-profession", "humaines.droit.le-secret-professionnel", "stage.competences.les-dix-competences-du-referentiel", "entree.metier.les-mots-du-metier"], "entree.oral.le-sujet-tire-au-sort"),
    (11, "Les grandes maladies", ["pathologies.degeneratif.le-diabete", "pathologies.obstructif.l-infarctus-et-l-angor", "pathologies.psy.depression-et-troubles-anxieux", "pathologies.tumoral.qu-est-ce-qu-un-cancer"], "entree.ecrit.s-entrainer-a-l-ecrit-en-conditions"),
    (12, "En conditions", ["sante-publique.protection.remboursement-complementaire-reste-a-charge", "sante-publique.population.les-grands-plans-de-sante-publique", "pharmaco.medicament.qu-est-ce-qu-un-medicament", "entree.voies.le-calendrier-d-une-candidature"], "entree.oral.simuler-l-entretien"),
]


def slug(s: str) -> str:
    s = s.replace("œ", "oe").replace("Œ", "Oe").replace("æ", "ae")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = s.lower().replace("'", "-").replace("’", "-")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def construit() -> dict:
    domaines = OrderedDict()
    for cle, titre, ordre, socle, pourquoi, sources in DOMAINES:
        domaines[cle] = {"titre": titre, "ordre": ordre, "niveau_socle": socle, "pourquoi": pourquoi, "sources_primaires": sources}
    domaines[CULTURE[0]] = {"titre": CULTURE[1], "ordre": CULTURE[2], "niveau_socle": None, "arbre": False, "pourquoi": CULTURE[4], "sources_primaires": CULTURE[5]}

    branches = OrderedDict()
    chapitres = []
    for dom, liste in B.items():
        branches[dom] = []
        for o, (bcle, btitre, exo, sous, chaps) in enumerate(liste, 1):
            branches[dom].append({"cle": bcle, "titre": btitre, "ordre": o, "exercice_dominant": exo,
                                  "sous_branches": [{"cle": sc, "titre": st} for sc, st in sous]})
            par_groupe_niveau: dict = {}
            entrees = []
            for ch in chaps:
                titre, niv, comp, notions = ch[0], ch[1], ch[2], ch[3]
                sb = ch[4] if len(ch) > 4 else None
                cid = f"{dom}.{bcle}.{slug(titre)}"
                par_groupe_niveau.setdefault((sb, niv), []).append(cid)
                entrees.append((cid, titre, niv, comp, notions, sb))
            for cid, titre, niv, comp, notions, sb in entrees:
                prereq = list(par_groupe_niveau.get((sb, niv - 1), []))
                if not prereq and sb is not None:
                    prereq = list(par_groupe_niveau.get((None, niv - 1), []))
                if not prereq and niv > 1:
                    for n in range(niv - 1, 0, -1):
                        prereq = list(par_groupe_niveau.get((sb, n), [])) or list(par_groupe_niveau.get((None, n), []))
                        if prereq:
                            break
                prereq += [p for p in CROSS.get(cid, []) if p not in prereq]
                exercices = [exo] + [e for e in EXERCICES_PAR_NIVEAU[niv] if e != exo]
                chapitres.append({
                    "id": cid, "domaine": dom, "branche": bcle, "sous_branche": sb, "titre": titre, "niveau": niv,
                    "niveau_nom": NIVEAU_NOM[niv], "competence": comp, "notions": notions, "prerequis": prereq,
                    "ponts": PONTS.get(cid, []), "exercices": exercices[:3], "exercice_dominant": exo,
                    "cartes_cible": CARTES_CIBLE[niv], "etude_minutes": ETUDE_MIN[niv], "satellite": False, "statut": "a-ecrire",
                })
    ids = {c["id"]: c for c in chapitres}
    for c in chapitres:
        for p in c["prerequis"]:
            assert p in ids, (c["id"], p)
            assert ids[p]["niveau"] <= c["niveau"], (c["id"], p)
        for p in c["ponts"]:
            assert p in ids, (c["id"], p)
    for k, v in MOTS_CLES.items():
        for p in v:
            assert p in ids, (k, p)
    for n, theme, chs, etude in PARCOURS:
        for p in chs + [etude]:
            assert p in ids, (n, p)
            assert ids[p]["niveau"] <= 2, (n, p)

    socle_ch = [c for c in chapitres if c["domaine"] != "culture" and c["niveau"] <= domaines[c["domaine"]]["niveau_socle"]]
    prog = OrderedDict()
    prog["_"] = ("Programme de l'infirmier en données. GÉNÉRÉ par programme/genere_ifsi.py : ne pas éditer à la main, "
                 "éditer les données du script. Fait foi sur SYLLABUS-IFSI.md. Les identifiants de chapitres sont immuables "
                 "une fois une carte publiée dessus.")
    prog["version"] = "0.1"
    prog["metier"] = "infirmier"
    prog["genere_le"] = "2026-09-04"
    prog["niveaux"] = {str(k): v for k, v in NIVEAU_NOM.items()}
    prog["socle"] = {"_": "Niveau à tenir par domaine pour valider le socle : ici, l'entrée en IFSI (niveau II partout).",
                     "niveaux": {k: v["niveau_socle"] for k, v in domaines.items() if v.get("niveau_socle")},
                     "chapitres": len(socle_ch), "cartes_cible": sum(c["cartes_cible"] for c in socle_ch)}
    prog["semaine_type"] = {"_": "Couleur des jours (BLUEPRINT §4, decisions/0016). Se règle par joueur.",
                            "lundi": "fondations", "mardi": "cours", "mercredi": "terrain", "jeudi": "cours", "vendredi": "exploration", "samedi": "etude", "dimanche": "libre"}
    prog["positionnement"] = {"_": "Vingt questions : deux par domaine de l'arbre, niveaux 1 et 2, branches distinctes.", "questions_par_domaine": 2, "niveaux": [1, 2]}
    prog["parcours"] = {"trimestre-1": {"_": "Douze semaines vers l'entrée en IFSI : quatre séances et une étude par semaine, niveaux 1 et 2. L'étude du samedi prépare l'écrit puis l'oral. Après, l'arbre est libre : la formation (niveau III) puis au-delà.",
                                        "semaines": [{"n": n, "theme": t, "chapitres": chs, "etude": e} for n, t, chs, e in PARCOURS]}}
    prog["mots_cles"] = {"_": "Ce qu'Arthur entend, et où ça vit dans l'arbre.", **MOTS_CLES}
    prog["domaines"] = domaines
    prog["branches"] = branches
    prog["chapitres"] = chapitres
    prog["compte"] = {"chapitres": len(chapitres), "par_niveau": {str(n): sum(1 for c in chapitres if c["niveau"] == n) for n in range(1, 6)},
                      "cartes_cible_total": sum(c["cartes_cible"] for c in chapitres),
                      "sous_branches": sum(len(b["sous_branches"]) for l in branches.values() for b in l)}
    return prog


def syllabus(prog: dict) -> str:
    roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    ids = {c["id"]: c for c in prog["chapitres"]}
    L = ["# Le programme de l'infirmier, chapitre par chapitre\n",
         f"Généré le {prog['genere_le']} par `programme/genere_ifsi.py` depuis `programme/ifsi.json`, qui fait foi. "
         "Un arbre qui va jusqu'à l'entrée en IFSI (niveaux I et II, le socle), puis la formation en trois ans "
         "(niveau III : unités d'enseignement, dix compétences, stages), puis au-delà (IV Doctrine, V Frontière).\n",
         "- **Niveaux** : I Repères (ce que la sélection attend), II Mécanismes (être bon à la sélection, le premier semestre), "
         "III Praticien (la formation, les gestes, les cas), IV Doctrine (débattre, critiquer), V Frontière (recherche, contribuer). Le socle = II partout.",
         "- **Une ligne = un chapitre** : niveau, titre, ce que tu sais faire à la fin, les notions, les exercices dominants, la durée d'une étude.",
         "- **Prérequis** : un chapitre de niveau n suppose les chapitres de niveau n-1 de sa sous-branche ; les ponts vers d'autres domaines sont nommés.\n",
         f"Compte : {prog['compte']['chapitres']} chapitres ({', '.join(f'{v} de niveau {k}' for k, v in prog['compte']['par_niveau'].items())}), "
         f"{prog['compte']['sous_branches']} sous-branches, {prog['compte']['cartes_cible_total']} cartes cibles ; socle : {prog['socle']['chapitres']} chapitres, "
         f"{prog['socle']['cartes_cible']} cartes cibles.\n",
         "## Les douze semaines vers l'entrée\n",
         "Quatre séances et une étude par semaine, niveaux I et II. L'étude du samedi prépare l'écrit puis l'oral. "
         "Après, l'arbre est libre : la séance protège le socle, l'étude va où on veut.\n",
         "| Semaine | Thème | Chapitres ouverts | Étude du samedi |", "|---|---|---|---|"]
    for s in prog["parcours"]["trimestre-1"]["semaines"]:
        L.append(f"| {s['n']} | {s['theme']} | " + " · ".join(ids[c]["titre"] for c in s["chapitres"]) + f" | {ids[s['etude']]['titre']} |")
    L += ["\n## Les mots entendus, et où ils vivent\n", "| Mot | Chapitres |", "|---|---|"]
    for k, v in prog["mots_cles"].items():
        if k != "_":
            L.append(f"| {k} | " + " · ".join(f"{ids[c]['titre']} ({ids[c]['domaine']})" for c in v) + " |")
    L.append("")
    for dom, d in prog["domaines"].items():
        L.append(f"## {d['ordre']}. {d['titre']}\n")
        L.append(f"{d['pourquoi']} Socle : " + (f"niveau {roman[d['niveau_socle']]}" if d.get("niveau_socle") else "hors arbre") + ". "
                 f"Sources primaires : {', '.join(d['sources_primaires'])}.\n")
        for b in prog["branches"][dom]:
            chs = [c for c in prog["chapitres"] if c["domaine"] == dom and c["branche"] == b["cle"]]
            L.append(f"### {d['ordre']}.{b['ordre']} {b['titre']}\n")
            L.append(f"Exercice dominant : {b['exercice_dominant']}. {len(chs)} chapitres.\n")
            for scle, stitre in [(None, None)] + [(s["cle"], s["titre"]) for s in b["sous_branches"]]:
                sous = [c for c in chs if c["sous_branche"] == scle]
                if not sous:
                    continue
                if stitre:
                    L.append(f"**{stitre}**\n")
                for c in sorted(sous, key=lambda c: (c["niveau"], c["titre"])):
                    cross = [p for p in c["prerequis"] if not p.startswith(f"{dom}.")]
                    ponts = (" Ponts : " + ", ".join(ids[p]["titre"] + " (" + ids[p]["domaine"] + ")" for p in cross + c["ponts"]) + ".") if (cross or c["ponts"]) else ""
                    L.append(f"- **{roman[c['niveau']]} · {c['titre']}** : {c['competence']}. Notions : {', '.join(c['notions'])}. "
                             f"Exercices : {', '.join(c['exercices'])} · étude {c['etude_minutes']} min.{ponts}")
                L.append("")
    L.append("## Ce que ce squelette attend des prochains agents\n")
    L.append("Pour chaque chapitre, dans l'ordre du parcours puis du socle : chercher les sources sur la liste blanche du domaine, écrire l'amorce, "
             "la leçon, les cartes, la synthèse, avec le tampon de provenance ; passer le valideur ; faire relire par un agent frais. "
             "Les chiffres (durées d'épreuve, taux, doses, normes) n'entrent qu'avec leur source. Les niveaux IV et V se font pousser par la boîte.")
    return "\n".join(L) + "\n"


def main() -> int:
    prog = construit()
    (RACINE / "programme" / "ifsi.json").write_text(json.dumps(prog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (RACINE / "SYLLABUS-IFSI.md").write_text(syllabus(prog), encoding="utf-8")
    print(json.dumps(prog["compte"], ensure_ascii=False), "socle :", prog["socle"]["chapitres"], prog["socle"]["cartes_cible"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

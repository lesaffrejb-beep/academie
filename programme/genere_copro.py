#!/usr/bin/env python3
"""Le programme du gestionnaire de copropriété, en une source : ce script
porte les DONNÉES du programme (domaines, branches, sous-branches,
chapitres, compétences, notions, parcours, mots-clés) et génère deux
sorties qui ne s'éditent jamais à la main :

    programme/copro.json   la version machine (fait foi, PROGRAMME.md)
    SYLLABUS.md            le programme lisible, comme un catalogue de
                           formation en ligne

    python3 programme/genere_copro.py

Écrit le 03/09/2026 sur le brief de JB (« imaginer l'arbre sur trois
mois, les compétences, les étapes ; écrire le squelette comme si on
pouvait déjà lire le programme d'une formation en ligne ; tout le chemin
dans chaque branche et ses subdivisions dès qu'il y a spécialisation »).
Les prochains agents remplissent les chapitres (chantier ACA-CONTENT-2) ;
ils ne redessinent pas l'arbre sans décision.

Règles portées ici : un chapitre de niveau n a pour prérequis les
chapitres de niveau n-1 de sa sous-branche (ou de sa branche), plus les
ponts nommés dans CROSS ; les identifiants sont immuables une fois une
carte publiée dessus (ceux du 02/09 sont conservés).
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

# (clé, titre, ordre, niveau socle, pourquoi, sources primaires)
DOMAINES = [
    ("droit", "Droit de la copropriété", 1, 3,
     "La grammaire du métier : sans elle rien ne se vote ni ne s'exécute.",
     ["Loi n° 65-557 du 10 juillet 1965 (Légifrance)", "Décret n° 67-223 du 17 mars 1967 (Légifrance)", "Judilibre", "ANIL", "Service-public.fr"]),
    ("pathologie", "Bâtiment et pathologie", 2, 2,
     "Le manque le plus coûteux sur le terrain, et le plus visuel.",
     ["Fiches pathologie bâtiment AQC (texte)", "Cerema", "Guides ANAH", "DTU (AFNOR, payant)", "Cahiers de recommandations des PSMV (Angers)"]),
    ("equipements", "Technique des équipements", 3, 2,
     "Les vrais mots : VMC, ascenseur, chaufferie, colonnes, sous-station.",
     ["Arrêtés et décrets applicables (ventilation, ascenseurs)", "Règlement sanitaire départemental", "ADEME", "Guides Cerema"]),
    ("comptabilite", "Comptabilité et finances de copropriété", 4, 3,
     "Débit, crédit, budget, annexes, excédents, impayés, factures.",
     ["Décret n° 2005-240 du 14 mars 2005", "Arrêté du 14 mars 2005 (plan comptable)", "Loi 65-557 art. 14-1 à 14-3", "ANIL", "Code général des impôts (TVA)"]),
    ("sinistres", "Sinistres et assurances", 5, 2,
     "Le quotidien : dégât des eaux, IRSI, dommages-ouvrage, expertise.",
     ["Code des assurances", "Code civil art. 1792 et s.", "Convention IRSI (France Assureurs, organisation-pro, à recouper)"]),
    ("procedure", "Procédure et justice", 6, 2,
     "Référé, tribunal judiciaire, avocat, commissaire de justice, injonction de payer, pénal.",
     ["Code de procédure civile", "Code de l'organisation judiciaire", "Loi 65-557 art. 19 à 19-2, 42", "Décret 67-223 art. 55", "Judilibre", "justice.fr"]),
    ("travaux", "Travaux, marchés et lecture de plans", 7, 2,
     "Devis, facture, marché privé, maîtrise d'œuvre, réception, plans, déclaration préalable, surélévation.",
     ["Code civil art. 1792 et s.", "Code de la construction et de l'habitation", "Code de l'urbanisme", "AQC", "Guides ANAH", "NF P 03-001 (AFNOR, payant, résumé de doctrine)"]),
    ("energie", "Énergie et rénovation", 8, 2,
     "DPE, audit, PPT, aides, chauffage, réseaux, bornes de recharge.",
     ["ADEME", "ecologie.gouv.fr", "Décrets et arrêtés DPE 2021", "Loi Climat et résilience", "ANAH / France Rénov'", "CRE", "Conseil d'analyse économique (doctrine)"]),
    ("immobilier", "Propriété, immobilier et urbanisme", 9, 2,
     "Propriété, servitudes, vente d'un lot, location, PLU, acteurs, le 49.",
     ["Code civil", "Code de l'urbanisme", "Loi n° 89-462", "Loi Hoguet", "ANIL", "DVF", "PLUi et PSMV d'Angers Loire Métropole", "Plan départemental de l'habitat (49)"]),
    ("cabinet", "Le cabinet : déontologie, contrats, relation", 10, 3,
     "Carte pro, contrat de syndic, cycle annuel, conseil syndical, assemblée en pratique, écrire, négocier, manager, RGPD.",
     ["Loi Hoguet et décret 72-678", "Décret 2015-1090 (déontologie)", "Décret 2015-342 (contrat type)", "CNIL", "Doctrine de négociation et de management (ouvrages)"]),
]
CULTURE = ("culture", "Culture", 11, None, "Le texte du bac : la propriété, l'habiter, la ville, l'histoire du logement.",
           ["Textes publics choisis", "Presse de fond", "Histoire"])

# Chapitre : (titre, niveau, compétence, [notions], sous_branche facultative)
# Branche : (clé, titre, exercice dominant, [sous-branches (clé, titre)], [chapitres])
B: "OrderedDict[str, list]" = OrderedDict()

B["droit"] = [
    ("statut", "Le statut de la copropriété", "qcm", [], [
        ("Qu'est-ce qu'une copropriété", 1, "Dire quand un immeuble est en copropriété et ce que ça déclenche", ["article 1", "lot", "immeuble bâti", "ordre public"]),
        ("Lots, parties privatives, parties communes", 1, "Ranger n'importe quel élément de l'immeuble dans privatif ou commun", ["article 2", "article 3", "présomption", "usage exclusif"]),
        ("Parties communes spéciales et à jouissance privative", 2, "Distinguer une partie commune spéciale d'une partie commune à jouissance privative et dire qui paie", ["articles 6-2 et 6-3", "ELAN", "charges spéciales"]),
        ("Tantièmes et quotes-parts", 2, "Expliquer d'où viennent les tantièmes d'un lot et à quoi ils servent", ["article 5", "quote-part", "tantième", "millièmes", "valeur relative"]),
        ("Le règlement de copropriété et l'état descriptif de division", 2, "Trouver dans un règlement la clause qui répond à une question courante", ["règlement", "état descriptif", "clause", "destination de l'immeuble"]),
        ("Fiche synthétique et immatriculation", 2, "Tenir à jour la fiche synthétique et l'immatriculation au registre", ["fiche synthétique", "registre national", "immatriculation"]),
        ("Diagnostiquer un règlement de copropriété ancien", 3, "Repérer les clauses réputées non écrites et proposer une mise en conformité", ["clause non écrite", "adaptation", "article 24 f", "mise en conformité"]),
        ("Histoire de la loi de 1965", 4, "Situer les grandes réformes et ce qu'elles ont changé", ["1938", "1965", "SRU", "ALUR", "ELAN", "Climat"]),
        ("La réforme permanente : controverses", 5, "Lire un rapport ou une proposition de réforme et en dire les enjeux", ["codification", "rapport", "controverse"]),
    ]),
    ("organes", "Le syndicat et ses organes", "qcm", [], [
        ("Le syndicat des copropriétaires", 1, "Dire ce qu'est le syndicat, sa personnalité et sa responsabilité", ["article 14", "personnalité civile", "responsabilité"]),
        ("Le syndic et ses missions", 1, "Énumérer les missions légales du syndic et leurs limites", ["article 18", "mandataire", "exécution des décisions", "conservation"]),
        ("Désignation, contrat, fin de mandat", 2, "Dérouler la désignation d'un syndic et la fin d'un mandat sans faute", ["article 25 c", "contrat", "durée", "révocation", "transmission"]),
        ("Le conseil syndical", 1, "Dire ce que fait et ne fait pas le conseil syndical", ["article 21", "assistance", "contrôle", "consultation"]),
        ("La délégation au conseil syndical", 2, "Expliquer ce que le syndicat peut déléguer au conseil et à quelles conditions", ["articles 21-1 à 21-5", "délégation", "assurance"]),
        ("Syndic bénévole et coopératif", 2, "Comparer les trois formes de syndic et leurs obligations", ["bénévole", "coopératif", "président-syndic"]),
        ("Administrateur provisoire et procédure d'alerte", 2, "Reconnaître une copropriété en difficulté et les outils du juge", ["article 29-1", "article 29-1 A", "mandataire ad hoc", "seuil d'impayés"]),
        ("Reprendre un immeuble : la transmission des archives", 3, "Réclamer et vérifier tout ce qu'un ancien syndic doit remettre", ["article 18-2", "archives", "fonds", "délais"]),
        ("La gouvernance de la copropriété en question", 4, "Argumenter sur les limites du modèle syndic-conseil-assemblée", ["gouvernance", "coopérative", "professionnalisation"]),
    ]),
    ("assemblee", "L'assemblée générale", "cas", [("preparer", "Préparer"), ("tenir", "Tenir"), ("apres", "Après")], [
        ("La convocation : forme et délai", 2, "Convoquer une assemblée régulière, dans les délais, par les bons moyens", ["décret art. 9", "vingt et un jours", "recommandé", "notification électronique"], "preparer"),
        ("L'ordre du jour et les inscriptions", 2, "Construire un ordre du jour et traiter les demandes d'inscription", ["décret art. 10", "question inscrite", "projet de résolution"], "preparer"),
        ("Les pièces jointes obligatoires", 2, "Joindre à chaque résolution la pièce que le décret exige", ["décret art. 11", "devis", "contrat", "annexes"], "preparer"),
        ("Pouvoirs et représentation", 2, "Vérifier les pouvoirs et appliquer les plafonds de mandats", ["article 22", "mandat", "trois pouvoirs", "cinq pour cent", "pouvoir en blanc"], "tenir"),
        ("Tenue de séance, bureau, feuille de présence", 2, "Ouvrir une assemblée et tenir la feuille de présence", ["bureau", "président", "scrutateur", "feuille de présence"], "tenir"),
        ("Vote par correspondance et visioconférence", 2, "Organiser le vote par correspondance et la participation à distance", ["article 17-1 A", "formulaire", "visioconférence", "abstention"], "tenir"),
        ("Le procès-verbal et sa notification", 2, "Rédiger un procès-verbal complet et le notifier dans le délai", ["décret art. 17", "décret art. 18", "opposants", "défaillants", "un mois"], "apres"),
        ("La contestation en deux mois", 2, "Dire qui peut contester, quoi, et jusqu'à quand", ["article 42", "deux mois", "opposant", "défaillant", "nullité"], "apres"),
        ("Diagnostiquer une convocation irrégulière", 3, "Trouver le vice d'une convocation et dire s'il est fatal", ["délai", "destinataire", "pièce manquante", "nullité"], "preparer"),
        ("Préparer une assemblée à risque", 3, "Anticiper une assemblée conflictuelle : ordre du jour, pièces, majorités, scénarios", ["risque", "scénario", "majorités", "conseil syndical"], "preparer"),
        ("L'assemblée dématérialisée : doctrine", 4, "Discuter les limites juridiques de l'assemblée à distance", ["dématérialisation", "jurisprudence", "doctrine"], "tenir"),
    ]),
    ("majorites", "Les majorités", "qcm", [], [
        ("L'article 24", 1, "Calculer une majorité simple, abstentions comprises, et dire ce qui s'y vote", ["voix exprimées", "présents et représentés", "gestion courante"]),
        ("L'article 25 et la passerelle", 2, "Calculer une majorité absolue et appliquer la passerelle du second vote", ["tous les copropriétaires", "tiers", "second vote", "article 25-1"]),
        ("L'article 26 et l'unanimité", 1, "Reconnaître une décision à double majorité ou à l'unanimité", ["double majorité", "deux tiers", "unanimité", "aliénation"]),
        ("Les cas particuliers", 2, "Trouver la majorité dérogatoire d'une décision atypique", ["accessibilité", "surélévation", "travaux d'intérêt collectif", "individualisation"]),
        ("Le tableau des majorités par décision", 3, "Donner la majorité de n'importe quelle résolution courante sans regarder", ["tableau", "ordre du jour", "erreur de majorité"]),
        ("L'abus de majorité", 4, "Reconnaître une décision régulière mais abusive et ce que le juge en fait", ["abus", "intérêt collectif", "rupture d'égalité", "jurisprudence"]),
    ]),
    ("charges", "Les charges et leur répartition", "cas", [], [
        ("Charges générales et charges spéciales", 1, "Classer une dépense en charge générale ou spéciale", ["article 10", "utilité", "conservation", "équipement"]),
        ("Les clés de répartition", 2, "Lire une clé de répartition et vérifier qu'elle est appliquée", ["clé", "grille", "tantièmes spéciaux", "règlement"]),
        ("La régularisation annuelle", 2, "Expliquer une régularisation à un copropriétaire, excédent compris", ["régularisation", "excédent", "insuffisance", "approbation des comptes"]),
        ("Modifier une répartition", 2, "Dire à quelle majorité et dans quels cas une répartition change", ["article 11", "unanimité", "changement d'usage", "travaux"]),
        ("Répondre à une contestation de charges", 3, "Traiter une contestation de charges du courrier au règlement", ["contestation", "action", "prescription", "cinq ans"]),
        ("Jurisprudence des clés de répartition", 4, "Lire un arrêt sur une clé de répartition et en tirer la règle", ["arrêt", "cassation", "clause"]),
    ]),
    ("travaux", "Les travaux et les parties communes", "cas", [("collectifs", "Travaux collectifs"), ("privatifs", "Travaux privatifs")], [
        ("Travaux votés et travaux urgents", 2, "Distinguer un travail voté, un travail urgent et un travail d'entretien", ["article 18", "décret art. 37", "urgence", "conservation"], "collectifs"),
        ("Le plan pluriannuel et le fonds de travaux", 2, "Expliquer le plan pluriannuel, le fonds et leurs obligations", ["article 14-2", "PPT", "fonds de travaux", "cotisation"], "collectifs"),
        ("Le diagnostic technique global", 2, "Dire quand un DTG est obligatoire et ce qu'il contient", ["DTG", "article L731-1", "contenu"], "collectifs"),
        ("Instruire une demande de travaux", 3, "Instruire une demande de travaux d'un copropriétaire jusqu'à l'ordre du jour", ["instruction", "pièces", "résolution", "conditions"], "privatifs"),
        ("Travaux privatifs affectant les communes", 2, "Reconnaître un travail privatif qui touche les communes et la majorité qu'il exige", ["article 25 b", "aspect extérieur", "autorisation"], "privatifs"),
        ("L'accès aux lots", 2, "Imposer l'accès à un lot pour des travaux collectifs sans faute", ["article 9", "accès", "indemnité", "préavis"], "privatifs"),
        ("La surélévation et le droit de surélever", 2, "Expliquer qui décide une surélévation et à qui appartient le droit de surélever", ["article 35", "surélévation", "cession du droit", "majorité"], "collectifs"),
    ]),
    ("mutations", "Les mutations de lots", "cas", [], [
        ("La vente d'un lot vue du syndic", 1, "Dérouler ce que le syndic fait quand un lot se vend", ["avis de mutation", "état daté", "pré-état daté", "questionnaire"]),
        ("L'avis de mutation et l'opposition", 2, "Former une opposition régulière au prix de vente", ["article 20", "opposition", "quinze jours", "notaire"]),
        ("Division et réunion de lots", 2, "Traiter une division ou une réunion de lots et ses effets sur les tantièmes", ["division", "réunion", "modificatif", "géomètre"]),
        ("Changement d'usage et location", 2, "Répondre à une question de changement d'usage ou de location courte", ["destination", "meublé de tourisme", "clause d'habitation bourgeoise"]),
        ("Le copropriétaire défaillant", 3, "Suivre un copropriétaire défaillant de la relance à la vente forcée, sans casser la procédure", ["défaillant", "recouvrement", "hypothèque", "vente forcée"]),
    ]),
    ("responsabilites", "Les responsabilités", "cas", [], [
        ("La responsabilité du syndicat", 1, "Dire quand le syndicat est responsable et de quoi", ["article 14", "vice de construction", "défaut d'entretien", "trouble"]),
        ("La responsabilité du syndic", 2, "Distinguer la responsabilité du syndic envers le syndicat et envers les tiers", ["mandataire", "contractuelle", "délictuelle", "faute de gestion"]),
        ("La responsabilité du copropriétaire", 2, "Dire ce qu'un copropriétaire doit au syndicat et à ses voisins", ["obligations", "troubles", "assurance"]),
        ("L'assurance obligatoire", 1, "Expliquer l'assurance obligatoire du copropriétaire et du syndicat", ["article 9-1", "responsabilité civile", "MRI"]),
        ("Troubles anormaux de voisinage", 2, "Qualifier un trouble anormal et dire qui répond", ["article 1253 du Code civil", "trouble anormal", "antériorité"]),
        ("Jurisprudence de responsabilité", 4, "Lire un arrêt de responsabilité et en tirer la règle", ["arrêt", "faute", "lien de causalité"]),
    ]),
]

B["pathologie"] = [
    ("materiaux", "Les matériaux et leur vieillissement", "photo", [], [
        ("Béton, ciment, mortier", 1, "Distinguer béton, ciment et mortier et dire à quoi chacun sert", ["liant", "granulat", "béton armé", "chaux"]),
        ("Les aciers et la corrosion", 1, "Reconnaître une corrosion d'armature et son mécanisme", ["carbonatation", "enrobage", "éclatement", "rouille"]),
        ("Bois et pierre", 1, "Reconnaître les pathologies courantes du bois et de la pierre", ["insectes", "champignons", "gélivité", "tuffeau", "schiste"]),
        ("Briques et enduits", 1, "Reconnaître les enduits et les briques et leurs désordres", ["enduit", "chaux", "ciment", "brique", "faïençage"]),
        ("Les isolants", 1, "Nommer les isolants courants et leurs défauts", ["laine", "polystyrène", "isolation par l'extérieur", "humidité"]),
        ("Reconnaître un matériau sur photo", 2, "Identifier un matériau sur une photo de chantier et dire son âge probable", ["diagnostic visuel", "époque", "matériau"]),
        ("Durabilité : l'état de la recherche", 5, "Lire une publication sur la durabilité et en tirer une vigilance", ["durabilité", "recherche", "bas carbone"]),
    ]),
    ("structure", "Structure et fondations", "photo", [("fissures", "Fissures"), ("balcons", "Balcons et porte-à-faux")], [
        ("Fondations et tassements", 2, "Expliquer un tassement et ses signes", ["fondation", "tassement différentiel", "argile", "sécheresse"], "fissures"),
        ("Microfissure, fissure, lézarde", 1, "Qualifier une fissure avec les bons mots, sans inventer de seuil", ["microfissure", "fissure", "lézarde", "traversante"], "fissures"),
        ("Fissures structurelles et leur lecture", 2, "Lire l'orientation et la position d'une fissure pour en soupçonner la cause", ["orientation", "escalier", "horizontale", "cause probable"], "fissures"),
        ("Témoins et suivi d'une fissure", 2, "Poser et lire un témoin, décider d'un suivi", ["témoin", "jauge", "évolution", "surveillance"], "fissures"),
        ("Balcons et corrosion des aciers", 2, "Reconnaître un balcon dangereux et savoir quoi faire", ["porte-à-faux", "armature", "éclatement", "mise en sécurité"], "balcons"),
        ("Carbonatation", 2, "Expliquer la carbonatation et ce qu'elle implique pour les réparations", ["carbonatation", "pH", "enrobage", "réparation"], "balcons"),
        ("Quand appeler un bureau d'études", 3, "Décider quand un désordre structurel dépasse le gestionnaire", ["bureau d'études", "diagnostic", "urgence", "sécurité"], "fissures"),
        ("Seuils et normes : ce qui est publié", 4, "Dire ce que les normes disent vraiment des fissures et ce qui relève du commerce", ["DTU", "norme", "seuil", "source"], "fissures"),
    ]),
    ("facades", "Façades", "photo", [], [
        ("Enduits et classes d'imperméabilité", 1, "Nommer les types d'enduit et de revêtement de façade", ["enduit", "revêtement", "classes I1 à I4", "imperméabilité"]),
        ("Le ravalement", 1, "Dire ce qu'est un ravalement, quand il est obligatoire et ce qu'il comprend", ["ravalement", "obligation", "injonction", "dix ans"]),
        ("L'isolation par l'extérieur et ses désordres", 2, "Reconnaître un désordre d'isolation par l'extérieur", ["ITE", "fissuration", "chocs", "ponts thermiques"]),
        ("Décollements et efflorescences", 2, "Distinguer décollement, cloquage, efflorescence et leur cause", ["décollement", "cloquage", "efflorescence", "sels"]),
        ("Diagnostiquer une façade avant devis", 3, "Faire le tour d'une façade et écrire ce qu'un devis doit couvrir", ["diagnostic", "cahier des charges", "sondage"]),
    ]),
    ("toitures", "Toitures et étanchéité", "photo", [("couvertures", "Couvertures"), ("terrasses", "Toitures-terrasses")], [
        ("Toiture-terrasse et relevés", 1, "Nommer les parties d'une toiture-terrasse et le rôle des relevés", ["étanchéité", "relevé", "acrotère", "évacuation"], "terrasses"),
        ("Souches, cheminées, ventilations primaires", 1, "Distinguer sur un toit une souche de cheminée, une ventilation primaire et un conduit de VMC", ["souche", "ventilation primaire", "conduit", "chapeau"], "couvertures"),
        ("Tuiles, ardoises, zinguerie", 1, "Nommer les ouvrages d'une couverture et leurs désordres", ["ardoise", "tuile", "faîtage", "noue", "solin", "chéneau", "dalle nantaise"], "couvertures"),
        ("Chéneaux et eaux pluviales", 2, "Suivre le chemin de l'eau de pluie du toit au réseau", ["EP", "chéneau", "descente", "dauphin", "regard"], "couvertures"),
        ("La visite de toiture", 3, "Conduire une visite de toiture en sécurité et en écrire le compte rendu", ["sécurité", "points de contrôle", "compte rendu"], "couvertures"),
        ("L'étanchéité : matériaux et garanties", 2, "Reconnaître un complexe d'étanchéité et ses garanties", ["bitume", "membrane", "protection", "garantie"], "terrasses"),
    ]),
    ("humidite", "L'humidité", "photo", [], [
        ("Remontées capillaires", 1, "Reconnaître une remontée capillaire et son traitement", ["capillarité", "salpêtre", "soubassement"]),
        ("Condensation", 1, "Reconnaître une condensation et son lien avec la ventilation", ["condensation", "point de rosée", "pont thermique", "moisissure"]),
        ("Infiltration", 1, "Reconnaître une infiltration et remonter à sa source", ["infiltration", "toiture", "façade", "menuiserie"]),
        ("Ponts thermiques et moisissures", 2, "Expliquer un pont thermique et son traitement", ["pont thermique", "nez de dalle", "isolation"]),
        ("Humidité et ventilation", 2, "Relier un désordre d'humidité à la ventilation du logement", ["ventilation", "VMC", "aération", "occupant"]),
        ("Un logement humide : que dire au copropriétaire", 3, "Instruire une plainte d'humidité jusqu'à la réponse écrite", ["instruction", "responsabilité", "réponse"]),
    ]),
    ("epoques", "Le bâti par époques", "datation", [], [
        ("Le bâti haussmannien et le bâti ancien", 1, "Reconnaître un immeuble ancien et ses pathologies typiques", ["pierre", "pan de bois", "plancher bois", "cheminées"]),
        ("1950-1975 : béton, amiante, plomb", 1, "Reconnaître le bâti des Trente Glorieuses et ses risques", ["préfabrication", "amiante", "plomb", "balcons"]),
        ("1975-1990", 1, "Reconnaître le bâti de la première réglementation thermique", ["RT 1974", "isolation", "VMC", "double vitrage"]),
        ("Le bâti récent", 1, "Reconnaître le bâti postérieur aux années 2000 et ses désordres", ["RT 2012", "étanchéité à l'air", "ITE", "garanties"]),
        ("Dater une façade", 2, "Dater une façade à dix ans près à partir de ses indices", ["indices", "matériaux", "menuiseries", "modénature"]),
        ("Les pathologies attendues par époque", 3, "Anticiper les désordres d'un immeuble à partir de sa date", ["prévision", "époque", "entretien"]),
    ]),
    ("diagnostics", "Diagnostics réglementaires du bâti", "qcm", [], [
        ("Amiante et dossier technique amiante", 1, "Dire ce que contient un DTA et quand il s'impose", ["amiante", "DTA", "repérage", "avant travaux"]),
        ("Plomb", 1, "Dire quand un diagnostic plomb s'impose et ce qu'il déclenche", ["plomb", "CREP", "parties communes"]),
        ("Termites", 1, "Dire où les termites sont un risque et ce que la loi impose", ["termites", "arrêté préfectoral", "déclaration"]),
        ("Radon", 2, "Expliquer le radon et les zones concernées", ["radon", "zones", "mesure"]),
        ("Tenir à jour les diagnostics", 3, "Tenir le tableau des diagnostics d'un immeuble sans trou", ["tableau", "péremption", "obligations"]),
    ]),
    ("visite", "La visite technique", "dessin", [], [
        ("Comment on regarde un immeuble", 1, "Faire le tour d'un immeuble dans le bon ordre", ["ordre", "extérieur", "communs", "locaux techniques"]),
        ("Ce qu'on photographie, ce qu'on note", 2, "Prendre des photos utiles et des notes exploitables", ["photo", "cadrage", "note", "anonymisation"]),
        ("Le compte rendu de visite technique", 3, "Écrire un compte rendu qui déclenche les bonnes actions", ["compte rendu", "priorité", "devis", "suivi"]),
    ]),
]

B["equipements"] = [
    ("ventilation", "Ventilation", "dessin", [], [
        ("Simple flux, double flux, hygro", 1, "Distinguer les systèmes de ventilation et leurs organes", ["simple flux", "double flux", "hygroréglable", "bouche", "entrée d'air"]),
        ("Le caisson et les courroies", 2, "Nommer les organes d'un caisson et expliquer pourquoi une courroie se détend", ["caisson", "courroie", "turbine", "moteur", "débit"]),
        ("Entretien et débits réglementaires", 2, "Dire ce qu'un contrat d'entretien VMC doit couvrir et les débits attendus", ["arrêté de 1982", "débits", "entretien", "nettoyage"]),
        ("Lire un rapport de contrôle VMC", 3, "Lire un rapport de contrôle et décider des suites", ["rapport", "mesure", "anomalie", "devis"]),
    ]),
    ("chauffage", "Chauffage collectif et eau chaude", "cas", [("gaz-fioul", "Chaudières gaz et fioul"), ("reseau", "Réseaux de chaleur et sous-stations"), ("pac", "Pompes à chaleur et hybrides")], [
        ("Chaudière gaz, fioul, condensation", 1, "Nommer les organes d'une chaufferie et expliquer la condensation", ["chaudière", "brûleur", "condensation", "circulateur", "vase d'expansion"], "gaz-fioul"),
        ("GRDF, le compteur et le raccordement gaz", 1, "Dire qui fait quoi entre le distributeur, le fournisseur et l'exploitant sur le gaz", ["GRDF", "distributeur", "fournisseur", "compteur", "coupure"], "gaz-fioul"),
        ("La sous-station de réseau de chaleur", 1, "Nommer les organes d'une sous-station et dire où s'arrête le réseau", ["sous-station", "échangeur", "primaire", "secondaire", "limite de prestation"], "reseau"),
        ("Le contrat de réseau de chaleur", 2, "Lire une facture de réseau de chaleur et ses parts fixe et variable", ["R1", "R2", "abonnement", "polices"], "reseau"),
        ("Les contrats P1 à P4", 2, "Expliquer P1, P2, P3, P4 et ce que chacun couvre", ["P1", "P2", "P3", "P4", "exploitant", "intéressement"], "gaz-fioul"),
        ("Les exploitants de chauffage", 2, "Dire ce qu'un exploitant doit rendre et comment le contrôler", ["exploitant", "compte rendu", "consommations", "pénalités"], "gaz-fioul"),
        ("Individualisation des frais", 2, "Expliquer l'individualisation des frais de chauffage et ses exceptions", ["individualisation", "répartiteur", "compteur", "exemption"], "gaz-fioul"),
        ("Eau chaude sanitaire et légionelles", 2, "Expliquer la production d'eau chaude collective et la prévention des légionelles", ["ballon", "bouclage", "légionelle", "température"], "gaz-fioul"),
        ("Pompes à chaleur et hybrides", 2, "Expliquer une pompe à chaleur collective et une chaudière hybride", ["PAC", "COP", "hybride", "appoint"], "pac"),
        ("La panne de janvier", 3, "Gérer une panne de chauffage collectif en hiver de l'appel à la réparation", ["urgence", "dépannage", "communication", "responsabilité"], "gaz-fioul"),
        ("Quelle énergie pour quel immeuble", 4, "Argumenter un choix d'énergie pour un immeuble donné", ["scénario", "coût global", "carbone", "réseau"], "pac"),
    ]),
    ("ascenseurs", "Ascenseurs", "photo", [], [
        ("Les organes d'un ascenseur", 1, "Nommer les organes d'un ascenseur avec les mots du technicien", ["machinerie", "cabine", "opérateur de porte", "parachute", "gaine"]),
        ("Le contrat de maintenance", 2, "Lire un contrat de maintenance et ses clauses obligatoires", ["maintenance", "clauses", "durée", "pièces"]),
        ("Le contrôle technique quinquennal", 2, "Dire ce qu'est le contrôle quinquennal et ce qu'on en fait", ["contrôle technique", "cinq ans", "rapport", "non-conformité"]),
        ("La mise en sécurité", 2, "Expliquer les obligations de mise en sécurité des ascenseurs existants", ["décret 2004-964", "sécurité", "obligations"]),
        ("L'ascenseur à l'arrêt", 3, "Gérer un ascenseur en panne longue avec les occupants et l'ascensoriste", ["panne", "communication", "délais", "pénalités"]),
    ]),
    ("plomberie", "Plomberie et réseaux", "dessin", [], [
        ("Colonnes EU, EV, EP", 1, "Distinguer eaux usées, eaux-vannes et eaux pluviales et leurs colonnes", ["EU", "EV", "EP", "colonne", "chute"]),
        ("Ventilation primaire et secondaire", 1, "Expliquer à quoi sert la ventilation d'une chute et où elle sort", ["ventilation primaire", "secondaire", "siphon", "souche"]),
        ("Surpresseur, compteurs, disconnecteur", 2, "Nommer les organes de l'arrivée d'eau et leur entretien", ["surpresseur", "compteur", "disconnecteur", "réducteur"]),
        ("La recherche de fuite", 2, "Organiser une recherche de fuite et savoir qui la paie", ["recherche de fuite", "IRSI", "destructive", "non destructive"]),
        ("Un dégât des eaux vu de la plomberie", 3, "Diagnostiquer l'origine probable d'un dégât des eaux à partir des réseaux", ["origine", "colonne", "joint", "étanchéité"]),
    ]),
    ("electricite", "Électricité des communs", "photo", [], [
        ("TGBT et colonnes montantes", 1, "Nommer le tableau général et les colonnes montantes et dire à qui elles appartiennent", ["TGBT", "colonne montante", "Enedis", "transfert"]),
        ("La NF C 15-100 pour un gestionnaire", 2, "Dire ce que la norme électrique impose dans les communs", ["NF C 15-100", "mise en conformité", "diagnostic"]),
        ("Éclairage des communs", 2, "Choisir un éclairage des communs et en réduire la consommation", ["détecteur", "LED", "minuterie", "TRV"]),
        ("Bornes de recharge", 2, "Expliquer une installation de recharge dans un parking collectif", ["IRVE", "droit à la prise", "infrastructure collective", "opérateur"]),
        ("Lire un rapport électrique", 3, "Lire un rapport de contrôle électrique et prioriser les travaux", ["rapport", "anomalie", "priorité"]),
    ]),
    ("acces", "Contrôle d'accès et sécurité", "photo", [], [
        ("Interphone, badges, ventouses, cellules", 1, "Nommer les organes d'un contrôle d'accès et leurs pannes courantes", ["interphone", "badge", "ventouse", "cellule", "gâche"]),
        ("Portails et portes de garage", 1, "Nommer les organes d'une porte automatique et ses obligations", ["moteur", "cellule", "sécurité", "entretien"]),
        ("Désenfumage et extincteurs", 1, "Dire ce que la sécurité incendie impose dans un immeuble d'habitation", ["arrêté de 1986", "désenfumage", "extincteur", "porte coupe-feu"]),
        ("La porte de parking en panne", 3, "Gérer une porte de parking en panne : sécurité, dépannage, communication", ["panne", "sécurité", "dépannage"]),
    ]),
    ("contrats", "Les contrats d'entretien", "cas", [], [
        ("Les obligations d'entretien par équipement", 1, "Dire pour chaque équipement ce que la loi impose d'entretenir", ["obligation", "ascenseur", "chaufferie", "VMC", "extincteurs"]),
        ("Le calendrier des contrôles", 2, "Tenir le calendrier des contrôles obligatoires d'un immeuble", ["calendrier", "périodicité", "rapport"]),
        ("Comparer deux contrats", 2, "Comparer deux contrats d'entretien sur ce qui compte", ["périmètre", "pièces", "délai d'intervention", "prix"]),
        ("Renégocier un contrat", 3, "Préparer et mener la renégociation d'un contrat d'entretien", ["renégociation", "mise en concurrence", "pénalités"]),
    ]),
]

B["comptabilite"] = [
    ("bases", "Les bases", "feuille-blanche", [], [
        ("Débit et crédit, la partie double", 2, "Passer une écriture simple en partie double", ["débit", "crédit", "partie double", "compte"]),
        ("Actif et passif", 1, "Dire ce qui est à l'actif et au passif d'un syndicat", ["actif", "passif", "créances", "dettes"]),
        ("Produits et charges", 2, "Distinguer un produit d'une charge et d'un encaissement", ["produit", "charge", "encaissement", "décaissement"]),
        ("Engagement et trésorerie", 2, "Expliquer la comptabilité d'engagement et ses effets sur les comptes", ["engagement", "trésorerie", "facture non parvenue"]),
        ("L'exercice comptable", 1, "Dire ce qu'est un exercice, sa clôture et son approbation", ["exercice", "clôture", "approbation", "période"]),
        ("Pourquoi une copropriété n'a pas de bilan", 2, "Expliquer ce que les annexes remplacent et pourquoi", ["annexes", "bilan", "décret 2005"]),
        ("Excédent, insuffisance et régularisation", 2, "Expliquer un excédent ou une insuffisance et son affectation", ["excédent", "insuffisance", "régularisation", "affectation"]),
        ("Histoire de la partie double", 4, "Situer la partie double dans l'histoire et dire ce qu'elle a permis", ["Pacioli", "histoire", "comptabilité"]),
    ]),
    ("plan-comptable", "Le plan comptable de la copropriété", "qcm", [], [
        ("Les classes de comptes", 1, "Nommer les classes du plan comptable et ce qu'elles contiennent", ["classe 1", "classe 4", "classe 5", "classe 6", "classe 7"]),
        ("Les comptes qu'on lit tous les jours", 1, "Reconnaître les comptes courants d'un grand livre de copropriété", ["450", "401", "512", "103", "105"]),
        ("Retrouver une écriture", 3, "Retrouver une écriture dans un grand livre à partir d'une question", ["grand livre", "écriture", "lettrage"]),
    ]),
    ("budget", "Budget, appels de fonds et financement", "cas", [("courant", "Le courant"), ("travaux", "Le financement des travaux")], [
        ("Le budget prévisionnel", 2, "Expliquer ce que couvre le budget prévisionnel et comment il se vote", ["article 14-1", "budget", "dépenses courantes", "vote"], "courant"),
        ("Les appels de fonds", 1, "Expliquer un appel de fonds trimestriel et sa date d'exigibilité", ["appel", "provision", "exigibilité", "trimestre"], "courant"),
        ("Les travaux hors budget", 2, "Expliquer comment se financent les travaux hors budget", ["article 14-2", "appel spécial", "échéancier"], "travaux"),
        ("Le fonds de travaux", 2, "Expliquer le fonds de travaux, son taux et son usage", ["fonds de travaux", "cotisation", "cinq pour cent", "affectation"], "travaux"),
        ("Avances et emprunt collectif", 2, "Distinguer avance de trésorerie, fonds de travaux et emprunt", ["avance", "fonds de roulement", "emprunt", "remboursement"], "courant"),
        ("L'emprunt collectif à adhésion individuelle", 2, "Expliquer l'emprunt collectif à adhésion individuelle et la caution", ["emprunt collectif", "adhésion", "caution", "article 26-4"], "travaux"),
        ("Le prêt avance mutation et les financements nouveaux", 1, "Dire ce qu'est le prêt avance mutation et à qui il sert", ["prêt avance mutation", "décret 2024-887", "financement"], "travaux"),
        ("Construire un budget", 3, "Construire un budget prévisionnel défendable devant le conseil syndical", ["construction", "historique", "indexation", "présentation"], "courant"),
    ]),
    ("annexes", "Les cinq annexes", "lecture", [], [
        ("L'annexe 1 : l'état financier", 1, "Lire l'état financier et y trouver la trésorerie et les dettes", ["annexe 1", "état financier", "trésorerie"]),
        ("L'annexe 2 : le compte de gestion général", 2, "Lire le compte de gestion et comparer au budget", ["annexe 2", "compte de gestion", "budget réalisé"]),
        ("L'annexe 3 : par clé de répartition", 2, "Lire la répartition des charges par clé", ["annexe 3", "clé", "répartition"]),
        ("Les annexes 4 et 5 : les travaux", 2, "Lire les annexes travaux et repérer un chantier non clôturé", ["annexe 4", "annexe 5", "travaux", "clôture"]),
        ("Les trois chiffres à regarder d'abord", 2, "Donner en trois chiffres l'état d'une copropriété", ["trésorerie", "impayés", "écart budget"]),
        ("Lire une annexe pour le conseil syndical", 3, "Présenter les annexes à un conseil syndical en dix minutes", ["présentation", "conseil syndical", "questions"]),
        ("Les limites du décret comptable", 4, "Argumenter sur ce que le décret comptable ne montre pas", ["limites", "engagement", "réforme"]),
    ]),
    ("controle", "Le contrôle des comptes", "cas", [], [
        ("Approbation et quitus", 2, "Distinguer l'approbation des comptes du quitus et leurs effets", ["approbation", "quitus", "responsabilité"]),
        ("Le rôle du conseil syndical", 1, "Dire ce que le conseil syndical contrôle et comment", ["contrôle", "pièces", "accès"]),
        ("Les anomalies classiques", 2, "Repérer les anomalies fréquentes d'un arrêté des comptes", ["anomalie", "doublon", "compte d'attente", "régularisation"]),
        ("L'audit d'un arrêté des comptes", 3, "Auditer un arrêté des comptes avec une grille et écrire le rapport", ["audit", "grille", "rapport"]),
    ]),
    ("impayes", "Les impayés", "datation", [], [
        ("Relance et mise en demeure", 2, "Dérouler la relance amiable jusqu'à la mise en demeure", ["relance", "mise en demeure", "recommandé", "trente jours"]),
        ("Les frais imputables", 2, "Dire quels frais de recouvrement s'imputent au seul débiteur", ["article 10-1", "frais", "imputation"]),
        ("Du comptable au juge", 2, "Dire quand un impayé passe du recouvrement amiable au judiciaire", ["seuil", "délai", "avocat", "article 19-2"]),
        ("Le plan de recouvrement", 3, "Construire le plan de recouvrement d'un immeuble et le présenter au conseil", ["plan", "priorité", "budget", "conseil syndical"]),
    ]),
    ("factures", "Factures, devis et TVA", "qcm", [], [
        ("Les mentions obligatoires d'une facture", 2, "Vérifier qu'une facture est conforme avant de la payer", ["mentions", "SIREN", "TVA", "date", "numéro"]),
        ("Les mentions d'un devis", 2, "Vérifier qu'un devis est complet avant de le présenter", ["devis", "validité", "assurance", "délai"]),
        ("La TVA à 20, 10 et 5,5 %", 2, "Appliquer le bon taux de TVA à des travaux en copropriété", ["taux", "attestation", "rénovation énergétique", "logement"]),
        ("Refuser une facture", 3, "Refuser ou contester une facture sans casser la relation", ["contestation", "réserve", "paiement partiel"]),
    ]),
    ("honoraires", "Les honoraires du syndic", "qcm", [], [
        ("Le contrat type et le forfait", 1, "Dire ce que le forfait couvre et ce qui est en dehors", ["contrat type", "forfait", "prestations particulières"]),
        ("Les prestations particulières", 2, "Facturer une prestation particulière sans erreur", ["article 18-1 A", "liste", "tarif", "assemblée"]),
        ("L'économie d'un cabinet", 4, "Expliquer comment un cabinet de syndic gagne sa vie et où sont les tensions", ["économie", "rentabilité", "honoraires travaux", "concurrence"]),
    ]),
]

B["sinistres"] = [
    ("contrat", "Le contrat d'assurance", "qcm", [], [
        ("Assuré, souscripteur, prime, franchise", 1, "Nommer les acteurs et les termes d'un contrat d'assurance", ["assuré", "souscripteur", "prime", "franchise"]),
        ("Garantie et exclusion", 1, "Lire une garantie et son exclusion", ["garantie", "exclusion", "plafond", "conditions générales"]),
        ("Les délais de déclaration", 1, "Déclarer un sinistre dans le délai qui s'applique", ["cinq jours", "deux jours", "dix jours", "déchéance"]),
        ("Lire des conditions particulières", 2, "Trouver dans des conditions particulières ce qui compte pour un sinistre", ["conditions particulières", "franchise", "garantie optionnelle"]),
    ]),
    ("mri", "La multirisque immeuble", "cas", [], [
        ("Ce que la MRI couvre", 1, "Dire ce que couvre une multirisque immeuble et ce qu'elle ne couvre pas", ["MRI", "incendie", "dégât des eaux", "responsabilité civile"]),
        ("La responsabilité civile du syndicat", 2, "Expliquer la garantie de responsabilité civile du syndicat et ses cas", ["responsabilité civile", "article 14", "tiers"]),
        ("Propriétaire non occupant et assurance du copropriétaire", 1, "Distinguer les assurances de l'immeuble, du propriétaire et de l'occupant", ["PNO", "occupant", "article 9-1"]),
        ("Vérifier une police", 3, "Vérifier une police d'immeuble et proposer les ajustements", ["vérification", "surface", "franchise", "renégociation"]),
    ]),
    ("degat-des-eaux", "Le dégât des eaux", "cas", [], [
        ("La convention IRSI et ses tranches", 1, "Dire à qui revient la gestion d'un dégât des eaux selon son montant", ["IRSI", "tranche", "assureur gestionnaire", "montant"]),
        ("L'assureur gestionnaire", 2, "Identifier l'assureur gestionnaire et ce qu'il doit faire", ["gestionnaire", "expertise pour compte commun", "recours"]),
        ("La recherche de fuite", 2, "Organiser la recherche de fuite et dire qui la prend en charge", ["recherche de fuite", "prise en charge", "destructive"]),
        ("Les recours", 2, "Expliquer les recours entre assureurs après indemnisation", ["recours", "subrogation", "responsable"]),
        ("Dérouler un dégât des eaux du 5e au 2e", 3, "Gérer un dégât des eaux multi-étages de la déclaration à la clôture", ["déclaration", "constat", "expertise", "clôture"]),
    ]),
    ("autres-sinistres", "Incendie, tempête, catastrophe naturelle", "qcm", [], [
        ("Incendie", 2, "Dérouler les premières mesures après un incendie", ["incendie", "mise en sécurité", "expertise", "relogement"]),
        ("Tempête et grêle", 2, "Déclarer un sinistre tempête et faire les mesures conservatoires", ["tempête", "grêle", "bâchage", "délai"]),
        ("Catastrophe naturelle", 2, "Expliquer l'arrêté de catastrophe naturelle et le délai de déclaration", ["arrêté", "catastrophe naturelle", "sécheresse", "délai"]),
        ("Vol et vandalisme", 2, "Traiter un vol ou un vandalisme dans les communs", ["vol", "vandalisme", "plainte", "franchise"]),
        ("Les mesures conservatoires", 3, "Décider et faire exécuter des mesures conservatoires sans dépasser ses pouvoirs", ["mesures conservatoires", "article 18", "urgence", "budget"]),
    ]),
    ("construction", "Les garanties de construction", "datation", [("garanties", "Les garanties légales"), ("do", "La dommages-ouvrage")], [
        ("Réception et parfait achèvement", 2, "Expliquer la réception et la garantie de parfait achèvement", ["réception", "réserves", "un an", "parfait achèvement"], "garanties"),
        ("Biennale et décennale", 1, "Distinguer la biennale et la décennale et dire ce qu'elles couvrent", ["biennale", "décennale", "article 1792", "solidité"], "garanties"),
        ("La dommages-ouvrage", 2, "Expliquer la dommages-ouvrage et quand la mobiliser", ["DO", "préfinancement", "délai", "expertise"], "do"),
        ("L'expertise judiciaire", 2, "Dire quand demander une expertise judiciaire et ce qu'elle produit", ["expertise judiciaire", "référé", "rapport"], "do"),
        ("Un désordre à deux ans", 3, "Traiter un désordre apparu deux ans après réception : garantie, assureur, délais", ["désordre", "délai", "mobilisation", "mise en demeure"], "garanties"),
    ]),
    ("expertise", "L'expertise", "cas", [], [
        ("Amiable, contradictoire, judiciaire", 1, "Distinguer les trois expertises et leurs effets", ["amiable", "contradictoire", "judiciaire"]),
        ("L'expert d'assuré", 2, "Dire quand un expert d'assuré est utile et qui le paie", ["expert d'assuré", "honoraires", "garantie"]),
        ("Préparer une expertise", 3, "Préparer une expertise : pièces, présents, questions", ["préparation", "pièces", "convocation"]),
    ]),
    ("gerer", "Gérer un sinistre", "datation", [], [
        ("De la déclaration à l'indemnité", 2, "Dérouler les étapes d'un sinistre de la déclaration à l'indemnité", ["déclaration", "expertise", "indemnité", "franchise"]),
        ("La méthode complète", 3, "Gérer un sinistre complexe avec plusieurs assureurs et plusieurs lots", ["méthode", "coordination", "suivi"]),
        ("Les contentieux d'assurance", 3, "Reconnaître un contentieux d'assurance et ses arguments", ["contentieux", "déchéance", "prescription biennale"]),
    ]),
]

B["procedure"] = [
    ("organisation", "L'organisation judiciaire", "relier", [], [
        ("Tribunal judiciaire, cour d'appel, Cour de cassation", 1, "Nommer les trois degrés et ce que chacun juge", ["tribunal judiciaire", "cour d'appel", "cassation", "degré"]),
        ("Le juge des contentieux de la protection", 1, "Dire ce que juge le juge des contentieux de la protection", ["JCP", "bail", "crédit", "surendettement"]),
        ("Le tribunal de commerce", 1, "Dire quand une affaire de copropriété passe au tribunal de commerce", ["commerce", "procédure collective", "société"]),
        ("Le pénal : procureur et tribunal correctionnel", 1, "Nommer les acteurs du pénal et le circuit d'une plainte", ["procureur", "correctionnel", "plainte", "instruction"]),
        ("La justice administrative", 1, "Dire quand une affaire relève du juge administratif", ["tribunal administratif", "urbanisme", "recours"]),
        ("Qui juge quoi en copropriété", 2, "Orienter n'importe quel litige de copropriété vers la bonne juridiction", ["compétence", "matière", "montant"]),
    ]),
    ("acteurs", "Les acteurs", "relier", [], [
        ("L'avocat et quand il est obligatoire", 1, "Dire quand l'avocat est obligatoire et comment on le mandate", ["avocat", "représentation obligatoire", "dix mille euros", "honoraires"]),
        ("Le commissaire de justice", 1, "Dire ce que fait le commissaire de justice pour un syndicat", ["commissaire de justice", "signification", "constat", "exécution"]),
        ("Notaire, expert judiciaire, médiateur, greffe", 1, "Nommer les autres acteurs et leur rôle", ["notaire", "expert", "médiateur", "greffe"]),
    ]),
    ("avant-le-proces", "Avant le procès", "datation", [], [
        ("Mise en demeure, recommandé, sommation", 2, "Écrire une mise en demeure qui vaut", ["mise en demeure", "recommandé", "sommation", "délai"]),
        ("Conciliation et médiation préalables", 2, "Dire quand une conciliation est obligatoire et comment elle se fait", ["conciliation", "médiation", "article 750-1", "petits litiges"]),
        ("Le protocole d'accord", 2, "Rédiger ou faire rédiger un protocole d'accord qui tient", ["protocole", "transaction", "concessions"]),
    ]),
    ("urgence", "Le référé et l'urgence", "cas", [], [
        ("Le référé et ses cas", 1, "Dire ce qu'est un référé et dans quels cas on l'utilise", ["référé", "urgence", "article 834", "article 835"]),
        ("Le référé expertise", 2, "Demander une expertise en référé et en suivre le déroulé", ["article 145", "expertise", "provision"]),
        ("La provision", 2, "Obtenir une provision en référé sur une créance non contestable", ["provision", "non sérieusement contestable"]),
        ("La procédure accélérée au fond", 2, "Utiliser la procédure accélérée au fond pour les charges", ["article 19-2", "accélérée", "provisions", "condamnation"]),
    ]),
    ("recouvrement", "Le recouvrement judiciaire", "datation", [("titre", "Obtenir un titre"), ("execution", "Exécuter")], [
        ("L'injonction de payer", 2, "Déposer une injonction de payer et gérer l'opposition", ["injonction", "requête", "opposition", "ordonnance"], "titre"),
        ("L'assignation", 2, "Lancer une assignation en paiement et suivre l'audience", ["assignation", "audience", "conclusions", "jugement"], "titre"),
        ("Hypothèque légale et privilège", 2, "Inscrire l'hypothèque légale du syndicat et expliquer le privilège", ["hypothèque légale", "article 19", "privilège", "article 19-1"], "execution"),
        ("Saisie-attribution et saisie immobilière", 2, "Faire exécuter un titre par saisie", ["saisie-attribution", "saisie immobilière", "commissaire de justice"], "execution"),
        ("Choisir la voie", 3, "Choisir la voie de recouvrement adaptée à un dossier", ["choix", "montant", "solvabilité", "délai"], "titre"),
    ]),
    ("contentieux-ag", "Le contentieux de l'assemblée", "cas", [], [
        ("La nullité d'assemblée", 1, "Dire ce qui rend une assemblée annulable", ["nullité", "convocation", "majorité", "article 42"]),
        ("Opposant et défaillant", 2, "Dire qui a qualité pour contester et dans quel délai", ["opposant", "défaillant", "deux mois"]),
        ("L'autorisation d'agir en justice", 2, "Obtenir l'autorisation d'agir et dire quand elle n'est pas nécessaire", ["décret art. 55", "autorisation", "exceptions"]),
        ("Répondre à une assignation", 3, "Réagir à une assignation contre le syndicat dans les délais", ["assignation", "avocat", "conseil syndical", "délais"]),
    ]),
    ("contentieux-batiment", "Le contentieux du bâtiment", "cas", [], [
        ("Référé expertise et responsabilité décennale", 2, "Lancer un contentieux de construction sur les bons fondements", ["référé expertise", "décennale", "assureur"]),
        ("L'appel en garantie", 2, "Expliquer l'appel en garantie et son intérêt", ["appel en garantie", "constructeur", "sous-traitant"]),
    ]),
    ("penal", "Le pénal en copropriété", "qcm", [], [
        ("Quand une affaire devient pénale", 1, "Reconnaître les infractions courantes autour d'une copropriété", ["abus de confiance", "mise en danger", "diffamation", "harcèlement"]),
        ("La plainte", 2, "Déposer plainte au nom du syndicat et suivre son sort", ["plainte", "constitution de partie civile", "classement"]),
    ]),
    ("lire", "Lire une décision", "lecture", [], [
        ("Visa, moyens, motifs, dispositif", 1, "Repérer les parties d'un arrêt et où se trouve la règle", ["visa", "moyens", "motifs", "dispositif"]),
        ("Cassation et rejet, portée", 2, "Dire ce que signifie une cassation, un rejet, et la portée d'un arrêt", ["cassation", "rejet", "portée", "revirement"]),
        ("Le commentaire d'arrêt", 4, "Commenter un arrêt de copropriété en une page", ["commentaire", "plan", "portée"]),
    ]),
]

B["travaux"] = [
    ("vocabulaire", "Le vocabulaire du chantier", "relier", [], [
        ("Échafaudage, nacelle et les moyens d'accès", 1, "Nommer les moyens d'accès d'un chantier et ce qu'ils coûtent", ["échafaudage", "nacelle", "cordistes", "location"]),
        ("MOA, MOE, BET, CSPS", 1, "Nommer les acteurs d'un chantier et leurs rôles", ["maîtrise d'ouvrage", "maîtrise d'œuvre", "bureau d'études", "coordonnateur"]),
        ("DOE, DIUO, DPGF, CCTP", 1, "Reconnaître les documents d'un marché de travaux", ["DOE", "DIUO", "DPGF", "CCTP", "CCAP"]),
        ("Lot, corps d'état, réception, réserves", 1, "Employer les mots d'un chantier sans se tromper", ["lot", "corps d'état", "réception", "réserve"]),
    ]),
    ("plans", "Lire un plan", "plan", [], [
        ("Échelles et types de plans", 1, "Reconnaître un plan de masse, un plan de niveau, une coupe, une façade", ["échelle", "plan de masse", "coupe", "façade"]),
        ("Les abréviations : EU, EV, EP, ECS, EF", 1, "Lire les abréviations des réseaux sur un plan", ["EU", "EV", "EP", "ECS", "EF", "VMC"]),
        ("Niveaux, cotes, symboles", 2, "Lire une cote, un niveau et les symboles courants", ["cote", "niveau", "symbole", "légende"]),
        ("Lire un plan de réseaux", 3, "Suivre une colonne ou une gaine sur un plan de réseaux", ["réseau", "gaine", "colonne", "regard"]),
    ]),
    ("du-besoin-au-devis", "Du besoin au devis", "cas", [], [
        ("Le cahier des charges", 2, "Écrire un cahier des charges court pour un travail courant", ["cahier des charges", "besoin", "périmètre"]),
        ("La mise en concurrence", 1, "Dire quand la mise en concurrence est obligatoire et comment la faire", ["article 21", "mise en concurrence", "seuil", "conseil syndical"]),
        ("Comparer des devis", 2, "Comparer trois devis sur ce qui compte", ["comparaison", "périmètre", "options", "prix"]),
        ("Attestations, Kbis, vigilance", 2, "Vérifier les pièces d'une entreprise avant de signer", ["attestation d'assurance", "Kbis", "vigilance URSSAF", "décennale"]),
        ("Le tableau comparatif", 3, "Présenter un tableau comparatif au conseil syndical", ["tableau", "critères", "recommandation"]),
    ]),
    ("marche-prive", "Le marché privé de travaux", "qcm", [], [
        ("Ce que règle la norme NF P 03-001", 1, "Dire ce que la norme règle et quand elle s'applique", ["NF P 03-001", "CCAG", "marché privé"]),
        ("Acompte, retenue de garantie, pénalités, révision", 2, "Lire les clauses financières d'un marché", ["acompte", "retenue de garantie", "pénalités", "révision"]),
        ("Sous-traitance et avenants", 2, "Traiter une sous-traitance et un avenant", ["sous-traitance", "agrément", "avenant"]),
        ("Le décompte définitif", 2, "Établir ou vérifier un décompte définitif", ["décompte", "solde", "réclamation"]),
    ]),
    ("chantier", "Le suivi de chantier", "datation", [], [
        ("Réunions et comptes rendus", 2, "Tenir une réunion de chantier et son compte rendu", ["réunion", "compte rendu", "planning"]),
        ("Sécurité et affichage", 1, "Dire ce qu'un chantier doit afficher et respecter", ["affichage", "sécurité", "CSPS", "panneau"]),
        ("Réception, réserves, garanties", 2, "Réceptionner un chantier et lever les réserves", ["réception", "réserves", "levée", "garanties"]),
        ("La réception", 3, "Conduire une réception avec la maîtrise d'œuvre et le conseil syndical", ["réception", "procès-verbal", "réserves"]),
    ]),
    ("urbanisme-des-travaux", "L'urbanisme des travaux", "qcm", [], [
        ("Déclaration préalable et permis", 1, "Dire quels travaux exigent une déclaration ou un permis", ["déclaration préalable", "permis", "seuils"]),
        ("Le PLU et les Bâtiments de France", 2, "Lire ce que le PLU et l'architecte des Bâtiments de France imposent", ["PLU", "ABF", "site patrimonial", "PSMV"]),
        ("Ravalement obligatoire et enseignes", 2, "Expliquer le ravalement obligatoire et les règles d'enseigne", ["ravalement", "injonction", "enseigne"]),
    ]),
    ("renovation-globale", "La rénovation globale", "cas", [], [
        ("Audit, DPE collectif, PPT", 1, "Dire ce que sont l'audit, le DPE collectif et le PPT et comment ils s'enchaînent", ["audit", "DPE collectif", "PPT"]),
        ("Les scénarios", 2, "Lire les scénarios d'un audit et les présenter", ["scénario", "gain", "coût", "étiquette"]),
        ("L'assistance à maîtrise d'ouvrage", 2, "Dire ce qu'un AMO apporte et ce qu'il coûte", ["AMO", "mission", "financement"]),
        ("Aides et financement", 2, "Monter le financement d'une rénovation globale", ["aides", "prêt collectif", "reste à charge"]),
        ("Rénovation performante contre rénovation par gestes", 4, "Argumenter sur la rénovation performante à partir des études disponibles", ["performante", "par gestes", "coût global", "valeur inobservée"]),
    ]),
    ("honoraires-travaux", "Les honoraires sur travaux", "qcm", [], [
        ("Les honoraires du syndic sur travaux", 1, "Dire comment se votent et se calculent les honoraires sur travaux", ["honoraires", "vote", "assiette"]),
        ("Les conflits d'intérêts", 2, "Reconnaître un conflit d'intérêts et le déclarer", ["conflit d'intérêts", "déclaration", "entreprise liée"]),
        ("Doctrine et déontologie des honoraires", 4, "Argumenter sur la juste rémunération des travaux", ["déontologie", "doctrine", "rémunération"]),
    ]),
]

B["energie"] = [
    ("physique", "La physique du bâtiment", "dessin", [], [
        ("Déperditions et isolation", 2, "Expliquer où un immeuble perd sa chaleur et comment on l'isole", ["déperdition", "U", "R", "isolation"]),
        ("Ponts thermiques et inertie", 2, "Expliquer un pont thermique et l'inertie d'un bâtiment", ["pont thermique", "inertie", "confort"]),
        ("Ventilation et humidité", 1, "Relier ventilation, humidité et qualité de l'air", ["ventilation", "humidité", "qualité de l'air"]),
        ("Le confort d'été", 2, "Expliquer le confort d'été et les gestes qui le protègent", ["confort d'été", "protection solaire", "surchauffe"]),
    ]),
    ("dpe", "Le DPE", "qcm", [], [
        ("Histoire du DPE", 1, "Situer les versions du DPE et ce qui a changé", ["2006", "2021", "opposabilité", "méthode"]),
        ("La méthode de calcul", 2, "Expliquer la méthode de calcul du DPE et ses entrées", ["3CL", "énergie primaire", "émissions"]),
        ("Les étiquettes", 1, "Lire une étiquette DPE et ses deux échelles", ["étiquette", "énergie", "climat", "classe"]),
        ("Le DPE collectif et son calendrier", 2, "Dire quand le DPE collectif est obligatoire et à quoi il sert", ["DPE collectif", "calendrier", "taille de copropriété"]),
        ("Fiabilité et contestation", 3, "Contester un DPE douteux avec méthode", ["fiabilité", "contestation", "diagnostiqueur"]),
        ("Le DPE en débat", 4, "Argumenter sur les limites du DPE", ["débat", "biais", "réforme"]),
    ]),
    ("calendrier", "Le calendrier des obligations", "qcm", [], [
        ("Les interdictions de location par étiquette", 1, "Donner le calendrier des interdictions de location et ses conditions", ["étiquette G", "étiquette F", "étiquette E", "décence"]),
        ("Ce que ça change pour la copropriété", 2, "Expliquer l'effet du calendrier sur une copropriété et ses bailleurs", ["copropriété", "bailleur", "travaux", "responsabilité"]),
    ]),
    ("audit-et-ppt", "Audit énergétique et PPT", "cas", [], [
        ("L'audit énergétique", 1, "Dire ce que contient un audit énergétique et qui peut le faire", ["audit", "contenu", "qualification"]),
        ("Le PPT et le DTG", 2, "Distinguer PPT et DTG et dire ce que l'assemblée en fait", ["PPT", "DTG", "vote", "actualisation"]),
        ("Le fonds de travaux", 1, "Relier le fonds de travaux au PPT", ["fonds", "PPT", "cotisation"]),
    ]),
    ("aides", "Les aides", "qcm", [], [
        ("Les aides nationales", 1, "Nommer les aides nationales à la rénovation en copropriété", ["MaPrimeRénov' Copropriété", "ANAH", "conditions"]),
        ("Les certificats d'économies d'énergie", 2, "Expliquer les CEE et comment une copropriété en bénéficie", ["CEE", "obligé", "prime"]),
        ("Le prêt collectif et les aides locales", 2, "Monter un plan d'aides avec le prêt collectif et les aides locales", ["prêt collectif", "aides locales", "cumul"]),
    ]),
    ("contrats-energie", "Les contrats d'énergie", "qcm", [], [
        ("Tarifs réglementés et marché", 1, "Distinguer tarif réglementé et offre de marché pour un immeuble", ["TRV", "marché", "éligibilité"]),
        ("Gaz et électricité pour un immeuble", 1, "Lire un contrat de gaz ou d'électricité des communs", ["contrat", "puissance", "abonnement", "GRDF", "Enedis"]),
        ("Le contrat d'exploitation de chauffage", 2, "Lire un contrat d'exploitation et ses clauses clés", ["exploitation", "intéressement", "durée", "révision"]),
        ("Les prix", 2, "Suivre les prix de l'énergie et leurs indices", ["indice", "prix", "CRE", "péremption"]),
    ]),
    ("chauffage-collectif", "Le chauffage collectif et ses choix", "cas", [], [
        ("Individualisation des frais", 1, "Dire quand l'individualisation est obligatoire et comment elle se fait", ["individualisation", "répartiteur", "obligation"]),
        ("Réseaux de chaleur", 2, "Expliquer le raccordement à un réseau de chaleur et ses obligations", ["réseau", "classement", "raccordement", "sous-station"]),
        ("Pompes à chaleur collectives", 2, "Expliquer une pompe à chaleur collective et ses conditions", ["PAC", "géothermie", "aérothermie", "acoustique"]),
        ("Quelle énergie pour quel immeuble", 4, "Argumenter un scénario énergétique complet pour un immeuble", ["scénario", "coût global", "carbone"]),
    ]),
    ("irve", "Bornes de recharge", "qcm", [], [
        ("Le droit à la prise", 1, "Expliquer le droit à la prise et la procédure", ["droit à la prise", "notification", "opposition", "délai"]),
        ("L'infrastructure collective", 2, "Expliquer une infrastructure collective de recharge et ses modèles", ["infrastructure collective", "opérateur", "Enedis", "modèle"]),
        ("Les opérateurs et leurs contrats", 2, "Comparer les offres d'opérateurs de recharge en copropriété", ["opérateur", "contrat", "abonnement", "propriété de l'infrastructure"]),
    ]),
]

B["immobilier"] = [
    ("propriete", "La propriété", "qcm", [], [
        ("La propriété et ses démembrements", 1, "Distinguer propriété, usufruit et nue-propriété", ["article 544", "usufruit", "nue-propriété"]),
        ("L'indivision", 2, "Expliquer l'indivision et qui vote en assemblée", ["indivision", "mandataire commun", "quote-part"]),
        ("Les servitudes", 1, "Reconnaître une servitude et ses effets", ["servitude", "fonds servant", "passage", "vue"]),
        ("La mitoyenneté", 2, "Expliquer la mitoyenneté d'un mur et son entretien", ["mitoyenneté", "mur", "présomption", "frais"]),
        ("Troubles anormaux de voisinage", 2, "Qualifier un trouble de voisinage et ses recours", ["trouble anormal", "article 1253", "antériorité"]),
        ("L'empiètement", 2, "Traiter un empiètement sur une partie commune", ["empiètement", "démolition", "prescription"]),
        ("Théories de la propriété", 4, "Discuter les fondements de la propriété et les communs", ["propriété", "communs", "Ostrom", "Olson"]),
    ]),
    ("vente", "La vente d'un lot", "datation", [], [
        ("Du compromis à l'acte", 1, "Dérouler une vente de lot du compromis à l'acte", ["compromis", "acte", "notaire", "délai"]),
        ("Diagnostics et surface", 1, "Nommer les diagnostics de vente et la surface Carrez", ["diagnostics", "Carrez", "DPE", "amiante"]),
        ("État daté et pré-état daté", 2, "Établir un état daté conforme et facturé au bon prix", ["état daté", "pré-état daté", "plafond", "contenu"]),
        ("L'opposition et les charges au prorata", 2, "Former une opposition et répartir les charges entre vendeur et acquéreur", ["opposition", "prorata", "exigibilité"]),
        ("Une vente avec opposition", 3, "Gérer une vente avec impayé jusqu'au règlement", ["opposition", "notaire", "règlement"]),
    ]),
    ("location", "La location", "qcm", [], [
        ("Le bail d'habitation", 1, "Nommer les règles clés du bail d'habitation", ["loi de 1989", "bail", "durée", "congé"]),
        ("La décence", 1, "Dire ce qu'est un logement décent et ce que le DPE y change", ["décence", "critères", "DPE"]),
        ("Les charges récupérables", 2, "Distinguer charges récupérables et non récupérables", ["décret 87-713", "récupérable", "régularisation"]),
        ("Meublé de tourisme et règlement de copropriété", 2, "Répondre à une question de location courte en copropriété", ["meublé de tourisme", "règlement", "destination", "déclaration"]),
    ]),
    ("urbanisme", "L'urbanisme", "qcm", [], [
        ("Le PLU et ses zones", 1, "Lire un PLU et trouver la zone d'un immeuble", ["PLU", "zone", "règlement", "PLUi"]),
        ("Les autorisations", 1, "Dire quelle autorisation d'urbanisme un projet exige", ["DP", "permis", "permis d'aménager"]),
        ("Servitudes d'utilité publique et préemption", 2, "Reconnaître une servitude d'utilité publique et un droit de préemption", ["servitude", "préemption", "DPU"]),
        ("Cadastre et division", 2, "Lire le cadastre et comprendre une division parcellaire", ["cadastre", "parcelle", "division", "géomètre"]),
        ("Le site patrimonial remarquable et le PSMV", 2, "Dire ce qu'un PSMV impose aux travaux dans le centre ancien", ["PSMV", "site patrimonial", "ABF", "fiches-conseil"]),
    ]),
    ("acteurs-et-formes", "Acteurs et formes", "relier", [], [
        ("Notaire, agent, promoteur, bailleur social", 1, "Nommer les acteurs de l'immobilier et leur rôle", ["notaire", "agent", "promoteur", "bailleur social"]),
        ("ADIL, mairie, préfecture", 1, "Savoir à qui s'adresser dans l'administration", ["ADIL", "mairie", "préfecture", "DDT"]),
        ("ASL, AFUL, division en volumes, copropriété horizontale", 2, "Distinguer les formes voisines de la copropriété", ["ASL", "AFUL", "volumes", "horizontale"]),
        ("La SCI copropriétaire", 2, "Traiter une SCI comme copropriétaire : représentation, appels, procédures", ["SCI", "gérant", "parts", "procédure collective"]),
    ]),
    ("fiscalite", "Fiscalité de base", "qcm", [], [
        ("Taxe foncière et enlèvement des ordures", 2, "Expliquer la taxe foncière et la TEOM et qui les paie", ["taxe foncière", "TEOM", "locataire"]),
        ("La plus-value", 2, "Expliquer la plus-value immobilière et ses exonérations", ["plus-value", "résidence principale", "abattement"]),
        ("Notions d'IFI et de TVA immobilière", 2, "Situer l'IFI et la TVA immobilière sans entrer dans le calcul", ["IFI", "TVA", "notions"]),
    ]),
    ("local", "Angers et le 49", "photo", [], [
        ("Le bâti d'Angers par époques", 1, "Reconnaître le bâti angevin : ardoise, tuffeau, schiste, ensembles d'après-guerre", ["ardoise", "tuffeau", "schiste", "Roseraie", "Belle-Beille"]),
        ("Le PLUi et le PSMV", 2, "Trouver ce que le PLUi et le PSMV imposent à un immeuble angevin", ["PLUi", "PSMV", "cœur de ville"]),
        ("Le plan départemental de l'habitat", 2, "Dire ce qu'un plan départemental de l'habitat contient et ce qui concerne les copropriétés", ["PDHH", "habitat indigne", "précarité énergétique", "copropriétés fragiles"]),
        ("Les fragilités observées", 3, "Lire le radar de fragilité d'une copropriété du 49", ["radar", "DREAL", "fragilité", "indicateurs"]),
    ]),
]

B["cabinet"] = [
    ("profession", "La profession", "qcm", [], [
        ("Carte professionnelle, garantie, assurance", 1, "Dire ce que la loi Hoguet exige pour exercer", ["loi Hoguet", "carte", "garantie financière", "RC pro"]),
        ("Le code de déontologie", 2, "Appliquer les règles du code de déontologie aux cas courants", ["déontologie", "décret 2015-1090", "conflit d'intérêts"]),
        ("La formation continue obligatoire", 1, "Dire l'obligation de formation continue et comment la satisfaire", ["formation continue", "heures", "renouvellement"]),
        ("Histoire et critique de la profession", 4, "Situer la profession de syndic et les critiques qui lui sont faites", ["histoire", "critique", "associations", "réputation"]),
    ]),
    ("contrat-de-syndic", "Le contrat de syndic", "qcm", [], [
        ("Le contrat type", 1, "Lire le contrat type et ses rubriques", ["contrat type", "décret 2015-342", "rubriques"]),
        ("Forfait et prestations particulières", 2, "Distinguer ce qui est au forfait et ce qui se facture en plus", ["forfait", "prestations particulières", "tarif"]),
        ("Durée, révocation, mise en concurrence", 2, "Gérer la fin d'un contrat et la mise en concurrence", ["durée", "révocation", "mise en concurrence", "article 21"]),
    ]),
    ("cycle-annuel", "Le cycle annuel", "datation", [], [
        ("De la clôture à l'assemblée", 1, "Dérouler les étapes de la clôture des comptes à la convocation", ["clôture", "arrêté des comptes", "conseil syndical", "convocation"]),
        ("De l'assemblée à l'exécution", 1, "Dérouler ce qui suit l'assemblée : procès-verbal, notifications, exécution", ["procès-verbal", "notification", "exécution", "appels"]),
        ("Les obligations annuelles", 2, "Tenir le radar des obligations annuelles d'un immeuble", ["radar", "obligations", "échéances"]),
        ("Dérouler une année sans rien oublier", 3, "Planifier l'année d'un portefeuille et ses jalons", ["planning", "portefeuille", "jalons"]),
    ]),
    ("conseil-syndical", "Le conseil syndical en pratique", "cas", [], [
        ("Rôle et réunion", 2, "Préparer et tenir une réunion de conseil syndical", ["réunion", "ordre du jour", "compte rendu"]),
        ("Préparer et restituer", 2, "Préparer un conseil syndical avec un dossier et restituer après", ["dossier", "restitution", "décisions"]),
        ("La psychologie d'un groupe", 2, "Reconnaître les dynamiques d'un conseil syndical et les canaliser", ["dynamique", "leader", "opposant", "consensus"]),
    ]),
    ("assemblee-en-pratique", "L'assemblée en pratique", "cas", [], [
        ("Animer et tenir le bureau", 2, "Animer une assemblée et tenir le bureau sans perdre le fil", ["animation", "bureau", "temps", "vote"]),
        ("Gérer les contestations et la salle", 2, "Répondre à une contestation en séance sans casser la séance", ["contestation", "salle", "réponse", "procès-verbal"]),
        ("Les fausses demandes de vote", 2, "Reconnaître une demande de vote qui n'en est pas une et la traiter", ["question diverse", "vœu", "décision", "résolution"]),
        ("Le procès-verbal en séance", 2, "Rédiger le procès-verbal en séance et le faire signer", ["procès-verbal", "séance", "signature", "mentions"]),
        ("Une assemblée qui tourne mal", 3, "Gérer une assemblée conflictuelle de la préparation à la sortie", ["conflit", "suspension", "sécurité", "police"]),
    ]),
    ("ecrire", "Écrire", "synthese", [], [
        ("Courrier, mail, notification", 2, "Choisir le bon support et la bonne forme pour écrire à un copropriétaire", ["courrier", "mail", "notification", "recommandé"]),
        ("Ton et engagements", 2, "Écrire sans s'engager au-delà de ce qu'on peut tenir", ["ton", "engagement", "réserve", "délai"]),
        ("Le silence n'est pas un accord", 2, "Traiter l'absence de réponse sans l'interpréter", ["silence", "relance", "accord"]),
    ]),
    ("negocier", "Négocier", "role", [], [
        ("Avec un prestataire", 2, "Négocier un devis ou un contrat avec un prestataire", ["prestataire", "prix", "délai", "pénalités"]),
        ("Méthode et alternatives", 2, "Préparer une négociation avec ses alternatives et ses limites", ["alternative", "limite", "intérêts", "positions"]),
        ("Préparer une négociation", 3, "Préparer et débriefer une négociation difficile", ["préparation", "débrief", "scénarios"]),
    ]),
    ("donnees", "Données, RGPD, blanchiment", "qcm", [], [
        ("Le RGPD au cabinet", 2, "Appliquer le RGPD aux données des copropriétaires", ["RGPD", "registre", "durée", "droits"]),
        ("Pièces jointes et données personnelles", 2, "Diffuser une convocation sans exposer des données personnelles", ["pièces jointes", "données", "notification collective"]),
        ("Lutte contre le blanchiment", 1, "Dire les obligations de vigilance du syndic", ["TRACFIN", "vigilance", "déclaration"]),
        ("Sécurité et cyber", 1, "Reconnaître une tentative d'hameçonnage et protéger les comptes", ["hameçonnage", "mot de passe", "fraude au virement"]),
        ("L'espace client en ligne", 1, "Dire ce que la loi impose comme accès en ligne et ce qu'un bon espace client contient", ["extranet", "article 18", "accès sécurisé", "documents"]),
    ]),
    ("charge", "Gérer sa charge et son équipe", "synthese", [], [
        ("Gérer son temps et déléguer", 2, "Organiser une semaine de gestionnaire et déléguer aux assistants", ["priorité", "délégation", "assistant", "binôme"]),
        ("Les échéances qui ne se ratent pas", 2, "Tenir les échéances légales avec un système, pas de tête", ["échéance", "système", "rappel", "Red Path"]),
        ("Manager un binôme et une équipe", 3, "Animer un binôme gestionnaire-assistant et faire monter une équipe", ["management", "feedback", "objectifs", "charge"]),
    ]),
    ("cas-transverses", "Les cas transverses", "cas", [], [
        ("Un dégât des eaux du 5e au 2e", 3, "Gérer un dégât des eaux multi-étages en mêlant assurance, technique, droit et relation", ["IRSI", "plomberie", "responsabilité", "communication"]),
        ("Une fissure avant l'assemblée", 3, "Traiter une fissure signalée à quinze jours d'une assemblée", ["fissure", "urgence", "devis", "majorité"]),
        ("Un impayé de dix-huit mois", 3, "Traiter un impayé ancien du comptable au juge", ["impayé", "injonction", "hypothèque", "défaillant"]),
        ("Le chauffage en panne en janvier", 3, "Gérer une panne de chauffage collectif en plein hiver", ["panne", "exploitant", "urgence", "communication"]),
        ("La copropriété classée G doit rénover", 3, "Conduire une copropriété passoire vers un vote de rénovation", ["DPE", "calendrier", "audit", "financement", "majorité"]),
        ("Un copropriétaire ferme sa loggia", 3, "Traiter une fermeture de loggia : parties communes, autorisation, urbanisme", ["loggia", "aspect extérieur", "article 25 b", "déclaration préalable"]),
        ("L'ascenseur à l'arrêt et une personne en fauteuil", 3, "Gérer un ascenseur à l'arrêt quand un occupant ne peut plus sortir", ["ascenseur", "urgence", "responsabilité", "communication"]),
        ("Une vente avec opposition", 3, "Gérer une vente de lot avec impayé et opposition", ["état daté", "opposition", "notaire", "frais"]),
        ("Une surélévation proposée par un promoteur", 3, "Instruire une proposition de surélévation de la lettre au vote", ["surélévation", "droit de surélever", "majorité", "urbanisme", "financement"]),
    ]),
]

B["culture"] = [
    ("lectures", "Lectures", "lecture", [], [
        ("La propriété : les textes fondateurs", 2, "Restituer la thèse d'un texte fondateur sur la propriété", ["propriété", "Locke", "Proudhon", "Code civil"]),
        ("L'habiter et le voisinage", 2, "Restituer un texte sur l'habiter et le voisinage", ["habiter", "voisinage", "sociologie"]),
        ("La ville", 2, "Restituer un texte sur la ville et sa fabrique", ["ville", "urbanisme", "densité"]),
        ("Histoire du logement", 3, "Situer les grandes étapes du logement en France", ["Haussmann", "HBM", "grands ensembles", "logement social"]),
        ("L'architecture et ses styles", 1, "Reconnaître les grands styles du bâti français", ["style", "haussmannien", "art déco", "moderne"]),
        ("Histoire de la copropriété", 3, "Raconter d'où vient la copropriété et ce qu'elle a changé", ["1938", "1965", "histoire", "communs"]),
        ("Les communs et le passager clandestin", 4, "Relier la gestion d'un immeuble aux théories de l'action collective", ["Ostrom", "Olson", "passager clandestin", "communs"]),
    ]),
]

# Ponts entre domaines : prérequis nommés en plus de ceux de la branche.
CROSS = {
    "cabinet.cas-transverses.un-degat-des-eaux-du-5e-au-2e": ["sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches", "equipements.plomberie.colonnes-eu-ev-ep", "droit.responsabilites.la-responsabilite-du-syndicat", "comptabilite.budget.les-travaux-hors-budget"],
    "cabinet.cas-transverses.une-fissure-avant-l-assemblee": ["pathologie.structure.microfissure-fissure-lezarde", "droit.travaux.travaux-votes-et-travaux-urgents", "droit.majorites.l-article-25-et-la-passerelle", "travaux.du-besoin-au-devis.comparer-des-devis"],
    "cabinet.cas-transverses.un-impaye-de-dix-huit-mois": ["comptabilite.impayes.relance-et-mise-en-demeure", "procedure.recouvrement.l-injonction-de-payer", "droit.mutations.le-coproprietaire-defaillant"],
    "cabinet.cas-transverses.le-chauffage-en-panne-en-janvier": ["equipements.chauffage.les-contrats-p1-a-p4", "cabinet.negocier.avec-un-prestataire", "droit.travaux.travaux-votes-et-travaux-urgents"],
    "cabinet.cas-transverses.la-copropriete-classee-g-doit-renover": ["energie.dpe.les-etiquettes", "energie.calendrier.les-interdictions-de-location-par-etiquette", "travaux.renovation-globale.audit-dpe-collectif-ppt", "droit.majorites.l-article-25-et-la-passerelle"],
    "cabinet.cas-transverses.un-coproprietaire-ferme-sa-loggia": ["droit.statut.lots-parties-privatives-parties-communes", "droit.travaux.travaux-privatifs-affectant-les-communes", "travaux.urbanisme-des-travaux.declaration-prealable-et-permis"],
    "cabinet.cas-transverses.l-ascenseur-a-l-arret-et-une-personne-en-fauteuil": ["equipements.ascenseurs.le-contrat-de-maintenance", "droit.responsabilites.la-responsabilite-du-syndicat", "cabinet.ecrire.courrier-mail-notification"],
    "cabinet.cas-transverses.une-vente-avec-opposition": ["immobilier.vente.etat-date-et-pre-etat-date", "droit.mutations.l-avis-de-mutation-et-l-opposition", "comptabilite.impayes.les-frais-imputables"],
    "cabinet.cas-transverses.une-surelevation-proposee-par-un-promoteur": ["droit.travaux.la-surelevation-et-le-droit-de-surelever", "droit.majorites.les-cas-particuliers", "travaux.urbanisme-des-travaux.le-plu-et-les-batiments-de-france"],
    "procedure.recouvrement.l-injonction-de-payer": ["comptabilite.impayes.relance-et-mise-en-demeure"],
    "energie.audit-et-ppt.le-ppt-et-le-dtg": ["droit.travaux.le-plan-pluriannuel-et-le-fonds-de-travaux"],
    "comptabilite.impayes.du-comptable-au-juge": ["procedure.avant-le-proces.mise-en-demeure-recommande-sommation"],
}
# Ponts « voir aussi » sans prérequis.
PONTS = {
    "sinistres.construction.reception-et-parfait-achevement": ["travaux.chantier.reception-reserves-garanties"],
    "equipements.chauffage.la-sous-station-de-reseau-de-chaleur": ["energie.chauffage-collectif.reseaux-de-chaleur"],
    "equipements.electricite.bornes-de-recharge": ["energie.irve.l-infrastructure-collective"],
    "pathologie.toitures.souches-cheminees-ventilations-primaires": ["equipements.plomberie.ventilation-primaire-et-secondaire"],
    "immobilier.urbanisme.le-site-patrimonial-remarquable-et-le-psmv": ["immobilier.local.le-plui-et-le-psmv", "travaux.urbanisme-des-travaux.le-plu-et-les-batiments-de-france"],
    "comptabilite.bases.excedent-insuffisance-et-regularisation": ["droit.charges.la-regularisation-annuelle"],
}

# Les mots que JB entend au travail, et où ils vivent dans l'arbre.
MOTS_CLES = {
    "sous-station": ["equipements.chauffage.la-sous-station-de-reseau-de-chaleur", "energie.chauffage-collectif.reseaux-de-chaleur"],
    "GRDF": ["equipements.chauffage.grdf-le-compteur-et-le-raccordement-gaz", "energie.contrats-energie.gaz-et-electricite-pour-un-immeuble"],
    "Dalkia (exploitant)": ["equipements.chauffage.les-exploitants-de-chauffage", "equipements.chauffage.les-contrats-p1-a-p4"],
    "WAAT (opérateur de recharge)": ["energie.irve.les-operateurs-et-leurs-contrats", "equipements.electricite.bornes-de-recharge"],
    "EP (eaux pluviales)": ["equipements.plomberie.colonnes-eu-ev-ep", "pathologie.toitures.cheneaux-et-eaux-pluviales"],
    "surélévation": ["droit.travaux.la-surelevation-et-le-droit-de-surelever", "cabinet.cas-transverses.une-surelevation-proposee-par-un-promoteur"],
    "emprunt collectif à adhésion individuelle": ["comptabilite.budget.l-emprunt-collectif-a-adhesion-individuelle"],
    "sinistre": ["sinistres.gerer.de-la-declaration-a-l-indemnite"],
    "contentieux": ["procedure.organisation.qui-juge-quoi-en-copropriete", "procedure.contentieux-ag.la-nullite-d-assemblee"],
    "IRSI": ["sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches"],
    "management": ["cabinet.charge.manager-un-binome-et-une-equipe"],
    "quote-part, tantième": ["droit.statut.tantiemes-et-quotes-parts"],
    "excédents": ["comptabilite.bases.excedent-insuffisance-et-regularisation", "droit.charges.la-regularisation-annuelle"],
    "chaudière hybride": ["equipements.chauffage.pompes-a-chaleur-et-hybrides"],
    "espace client": ["cabinet.donnees.l-espace-client-en-ligne"],
}

# Le parcours des trois premiers mois : treize semaines, quatre séances et
# une étude. Chaque semaine nomme les chapitres de niveau 1 qui entrent en
# neuf ; l'étude du samedi est le chapitre marqué.
PARCOURS = [
    (1, "Ce qu'est une copropriété", ["droit.statut.qu-est-ce-qu-une-copropriete", "droit.statut.lots-parties-privatives-parties-communes", "droit.statut.tantiemes-et-quotes-parts", "droit.organes.le-syndicat-des-coproprietaires"], "droit.statut.qu-est-ce-qu-une-copropriete"),
    (2, "Les organes et la première assemblée", ["droit.organes.le-syndic-et-ses-missions", "droit.organes.le-conseil-syndical", "droit.assemblee.la-convocation-forme-et-delai", "droit.assemblee.tenue-de-seance-bureau-feuille-de-presence"], "droit.assemblee.la-convocation-forme-et-delai"),
    (3, "Les majorités", ["droit.majorites.l-article-24", "droit.majorites.l-article-25-et-la-passerelle", "droit.majorites.l-article-26-et-l-unanimite", "droit.assemblee.le-proces-verbal-et-sa-notification"], "droit.majorites.l-article-25-et-la-passerelle"),
    (4, "Le bâtiment : matériaux et toits", ["pathologie.materiaux.beton-ciment-mortier", "pathologie.materiaux.les-aciers-et-la-corrosion", "pathologie.toitures.souches-cheminees-ventilations-primaires", "pathologie.toitures.tuiles-ardoises-zinguerie"], "pathologie.toitures.souches-cheminees-ventilations-primaires"),
    (5, "Fissures et humidité", ["pathologie.structure.microfissure-fissure-lezarde", "pathologie.structure.fondations-et-tassements", "pathologie.humidite.remontees-capillaires", "pathologie.humidite.condensation", "pathologie.humidite.infiltration"], "pathologie.structure.microfissure-fissure-lezarde"),
    (6, "Les équipements : air et eau", ["equipements.ventilation.simple-flux-double-flux-hygro", "equipements.ventilation.le-caisson-et-les-courroies", "equipements.plomberie.colonnes-eu-ev-ep", "equipements.plomberie.ventilation-primaire-et-secondaire"], "equipements.ventilation.le-caisson-et-les-courroies"),
    (7, "Les équipements : chaleur et ascenseur", ["equipements.chauffage.chaudiere-gaz-fioul-condensation", "equipements.chauffage.la-sous-station-de-reseau-de-chaleur", "equipements.chauffage.grdf-le-compteur-et-le-raccordement-gaz", "equipements.ascenseurs.les-organes-d-un-ascenseur"], "equipements.chauffage.la-sous-station-de-reseau-de-chaleur"),
    (8, "La comptabilité : les bases", ["comptabilite.bases.debit-et-credit-la-partie-double", "comptabilite.bases.actif-et-passif", "comptabilite.bases.produits-et-charges", "comptabilite.bases.l-exercice-comptable"], "comptabilite.bases.debit-et-credit-la-partie-double"),
    (9, "Budget, appels, annexes", ["comptabilite.budget.le-budget-previsionnel", "comptabilite.budget.les-appels-de-fonds", "comptabilite.annexes.l-annexe-1-l-etat-financier", "comptabilite.annexes.l-annexe-2-le-compte-de-gestion-general", "comptabilite.plan-comptable.les-classes-de-comptes"], "comptabilite.annexes.l-annexe-1-l-etat-financier"),
    (10, "Sinistres et assurances", ["sinistres.contrat.assure-souscripteur-prime-franchise", "sinistres.contrat.les-delais-de-declaration", "sinistres.mri.ce-que-la-mri-couvre", "sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches"], "sinistres.degat-des-eaux.la-convention-irsi-et-ses-tranches"),
    (11, "La justice et le recouvrement", ["procedure.organisation.tribunal-judiciaire-cour-d-appel-cour-de-cassation", "procedure.acteurs.l-avocat-et-quand-il-est-obligatoire", "procedure.urgence.le-refere-et-ses-cas", "comptabilite.impayes.relance-et-mise-en-demeure", "procedure.recouvrement.l-injonction-de-payer"], "procedure.urgence.le-refere-et-ses-cas"),
    (12, "Travaux, devis, énergie", ["travaux.vocabulaire.moa-moe-bet-csps", "travaux.du-besoin-au-devis.la-mise-en-concurrence", "comptabilite.factures.les-mentions-obligatoires-d-une-facture", "energie.dpe.les-etiquettes", "energie.calendrier.les-interdictions-de-location-par-etiquette"], "travaux.du-besoin-au-devis.la-mise-en-concurrence"),
    (13, "Le cabinet et la première épreuve", ["cabinet.profession.carte-professionnelle-garantie-assurance", "cabinet.cycle-annuel.de-la-cloture-a-l-assemblee", "cabinet.cycle-annuel.de-l-assemblee-a-l-execution", "immobilier.vente.du-compromis-a-l-acte"], "cabinet.cycle-annuel.de-la-cloture-a-l-assemblee"),
]


def slug(s: str) -> str:
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
                    # aucun chapitre de niveau n-1 dans le groupe : on remonte au premier niveau inférieur existant
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
    # chapitre déjà écrit le 03/09
    if (RACINE / "chapitres" / "droit" / "majorites" / "l-article-24.json").is_file():
        ids["droit.majorites.l-article-24"]["statut"] = "brouillon"

    socle_ch = [c for c in chapitres if c["domaine"] != "culture" and c["niveau"] <= domaines[c["domaine"]]["niveau_socle"]]
    prog = OrderedDict()
    prog["_"] = ("Programme du gestionnaire de copropriété en données. GÉNÉRÉ par programme/genere_copro.py : ne pas éditer à la main, "
                 "éditer les données du script. Fait foi sur PROGRAMME.md et SYLLABUS.md. Les identifiants de chapitres sont immuables "
                 "une fois une carte publiée dessus.")
    prog["version"] = "0.2"
    prog["metier"] = "gestionnaire de copropriété"
    prog["genere_le"] = "2026-09-03"
    prog["niveaux"] = {str(k): v for k, v in NIVEAU_NOM.items()}
    prog["socle"] = {"_": "Niveau à tenir par domaine pour valider le socle (BLUEPRINT §6, decisions/0013).",
                     "niveaux": {k: v["niveau_socle"] for k, v in domaines.items() if v.get("niveau_socle")},
                     "chapitres": len(socle_ch), "cartes_cible": sum(c["cartes_cible"] for c in socle_ch)}
    prog["semaine_type"] = {"_": "Couleur des jours (BLUEPRINT §4, decisions/0016).",
                            "lundi": "fondations", "mardi": "cours", "mercredi": "terrain", "jeudi": "cours", "vendredi": "exploration", "samedi": "etude", "dimanche": "libre"}
    prog["positionnement"] = {"_": "Vingt questions : deux par domaine de l'arbre, niveaux 1 et 2, branches distinctes.", "questions_par_domaine": 2, "niveaux": [1, 2]}
    prog["parcours"] = {"trimestre-1": {"_": "Les trois premiers mois : quatre séances et une étude par semaine, niveaux 1 et 2 (calibrage du 03/09), dans l'ordre du socle. Après, l'arbre est libre et la séance protège le socle.",
                                        "semaines": [{"n": n, "theme": t, "chapitres": chs, "etude": e} for n, t, chs, e in PARCOURS]}}
    prog["mots_cles"] = {"_": "Ce que JB entend au travail, et où ça vit dans l'arbre.", **MOTS_CLES}
    prog["domaines"] = domaines
    prog["branches"] = branches
    prog["chapitres"] = chapitres
    prog["compte"] = {"chapitres": len(chapitres), "par_niveau": {str(n): sum(1 for c in chapitres if c["niveau"] == n) for n in range(1, 6)},
                      "cartes_cible_total": sum(c["cartes_cible"] for c in chapitres),
                      "sous_branches": sum(len(b["sous_branches"]) for l in branches.values() for b in l)}
    return prog


def syllabus(prog: dict) -> str:
    L = []
    L.append("# SYLLABUS, le programme du gestionnaire de copropriété\n")
    L.append("Généré le 03/09/2026 par `programme/genere_copro.py` depuis `programme/copro.json` (qui fait foi). "
             "Ce fichier se lit comme le catalogue d'une formation en ligne : dix domaines, leurs branches et sous-branches, "
             f"{prog['compte']['chapitres']} chapitres sur cinq niveaux, ce que chacun apprend à faire, et le parcours des trois premiers mois. "
             "Aucun chapitre n'est encore écrit sauf un témoin (`chapitres/droit/majorites/l-article-24.json`) : les agents remplissent "
             "depuis ce squelette (chantier `ACA-CONTENT-2`), ils ne le redessinent pas sans décision.\n")
    L.append("## Comment lire\n")
    L.append("- **Niveaux** : I Repères (nommer, reconnaître), II Mécanismes (expliquer, appliquer), III Praticien (diagnostiquer, décider, rédiger), "
             "IV Doctrine (argumenter, critiquer), V Frontière (état de l'art, contribuer). Le socle = II partout, III en droit, comptabilité et cabinet.")
    L.append("- **Une ligne = un chapitre** : niveau, titre, ce que tu sais faire à la fin, les notions, les exercices dominants, la durée d'une étude.")
    L.append("- **Prérequis** : un chapitre de niveau n suppose les chapitres de niveau n-1 de sa sous-branche ; les ponts vers d'autres domaines sont nommés.")
    L.append("- **Sous-branches** : quand une branche se spécialise nettement (gaz contre réseau de chaleur, garanties contre dommages-ouvrage), la subdivision est dite.\n")
    L.append(f"Compte : {prog['compte']['chapitres']} chapitres ({', '.join(f'{v} de niveau {k}' for k, v in prog['compte']['par_niveau'].items())}), "
             f"{prog['compte']['sous_branches']} sous-branches, {prog['compte']['cartes_cible_total']} cartes cibles ; socle : {prog['socle']['chapitres']} chapitres, "
             f"{prog['socle']['cartes_cible']} cartes cibles.\n")
    L.append("## Le parcours des trois premiers mois\n")
    L.append("Quatre séances et une étude par semaine, en niveaux I et II (quinze chapitres du trimestre sont passés en II au calibrage du 03/09), dans l'ordre du socle. Chaque semaine ouvre quatre à cinq chapitres en neuf ; "
             "l'étude du samedi prend le chapitre marqué. Après le trimestre, l'arbre est libre : la séance protège le socle, l'étude va où on veut.\n")
    L.append("| Semaine | Thème | Chapitres ouverts | Étude du samedi |")
    L.append("|---|---|---|---|")
    ids = {c["id"]: c for c in prog["chapitres"]}
    for s in prog["parcours"]["trimestre-1"]["semaines"]:
        L.append(f"| {s['n']} | {s['theme']} | " + " · ".join(ids[c]["titre"] for c in s["chapitres"]) + f" | {ids[s['etude']]['titre']} |")
    L.append("\nLa treizième semaine se clôt par la première épreuve de domaine, sur le droit, si son remplissage le permet.\n")
    L.append("## Les mots entendus au travail, et où ils vivent\n")
    L.append("| Mot | Chapitres |")
    L.append("|---|---|")
    for k, v in prog["mots_cles"].items():
        if k == "_":
            continue
        L.append(f"| {k} | " + " · ".join(f"{ids[c]['titre']} ({ids[c]['domaine']})" for c in v) + " |")
    L.append("")
    roman = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V"}
    for dom, d in prog["domaines"].items():
        L.append(f"## {d['ordre']}. {d['titre']}\n")
        L.append(f"{d['pourquoi']} Socle : " + (f"niveau {roman[d['niveau_socle']]}" if d.get("niveau_socle") else "hors arbre") + ". "
                 f"Sources primaires : {', '.join(d['sources_primaires'])}.\n")
        for b in prog["branches"][dom]:
            chs = [c for c in prog["chapitres"] if c["domaine"] == dom and c["branche"] == b["cle"]]
            L.append(f"### {d['ordre']}.{b['ordre']} {b['titre']}\n")
            L.append(f"Exercice dominant : {b['exercice_dominant']}. {len(chs)} chapitres.\n")
            groupes = [(None, None)] + [(s["cle"], s["titre"]) for s in b["sous_branches"]]
            for scle, stitre in groupes:
                sous = [c for c in chs if c["sous_branche"] == scle]
                if not sous:
                    continue
                if stitre:
                    L.append(f"**{stitre}**\n")
                for c in sorted(sous, key=lambda c: (c["niveau"], c["titre"])):
                    ponts = ""
                    cross = [p for p in c["prerequis"] if not p.startswith(f"{dom}.")]
                    if cross or c["ponts"]:
                        ponts = " Ponts : " + ", ".join(ids[p]["titre"] + " (" + ids[p]["domaine"] + ")" for p in cross + c["ponts"]) + "."
                    L.append(f"- **{roman[c['niveau']]} · {c['titre']}** : {c['competence']}. Notions : {', '.join(c['notions'])}. "
                             f"Exercices : {', '.join(c['exercices'])} · étude {c['etude_minutes']} min.{ponts}")
                L.append("")
    L.append("## Ce que ce squelette attend des prochains agents\n")
    L.append("Pour chaque chapitre, dans l'ordre du parcours puis du socle : chercher les sources sur la liste blanche, écrire l'amorce, la leçon "
             "(300 à 800 mots), les cartes (six à dix, trois types au moins), la synthèse, avec le tampon de provenance ; passer le valideur ; "
             "faire relire par un agent frais ; mesurer le coût. Le chapitre témoin montre la forme. Les niveaux IV et V se font pousser par la boîte.")
    return "\n".join(L) + "\n"


def main() -> int:
    prog = construit()
    (RACINE / "programme" / "copro.json").write_text(json.dumps(prog, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (RACINE / "SYLLABUS.md").write_text(syllabus(prog), encoding="utf-8")
    print(json.dumps(prog["compte"], ensure_ascii=False), "socle :", prog["socle"]["chapitres"], prog["socle"]["cartes_cible"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

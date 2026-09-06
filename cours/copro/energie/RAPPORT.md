# Bilan privé énergie et couverture technique demandée par JB

Statut : brouillon éditorial
Auteur : Codex / GPT-6 / contenu_expert-2026-09-06

Les 29 chapitres énergie sont présents dans huit branches : physique (4), DPE (6), calendrier (2), audit et PPT (3), aides (3), contrats énergie (4), chauffage collectif (4), IRVE (3). Avec pathologie (46) et équipements (38), le lot attribué atteint 113 chapitres. Deux dossiers complémentaires sont comptés séparément du programme.

## Contrôles et portée

Contrôle documentaire local après rédaction : identifiants présents une fois chacun, titres exacts du programme, références C/S résolues et aucun balisage d’image, SVG ou Mermaid. Les exercices corrigés précédemment intitulés « Exercice » ou « Transférer » sont maintenant explicitement signalés comme transfert ; leur correction existante est conservée. Aucun texte de remplissage n’a été ajouté pour supprimer une alerte.

Comptage indicatif du corps des sections par espaces : équipements 20 801 mots (461–796 par chapitre) ; énergie 16 658 mots (524–885). Le comptage ne prouve ni profondeur suffisante pour chaque usage ni maîtrise de l’élève. Les 51 sources énergie, 51 sources pathologie et 45 sources équipements documentent précisément leur champ ; certains registres partagent la même source, ces nombres ne représentent pas autant d’ouvrages indépendants lus.

Les nouveaux cours restent des brouillons éditoriaux. Aucune auto-relecture n’est signée comme indépendante et aucun verdict usine n’est appliqué à ces textes originaux. La relecture croisée bornée d’autres agents doit conserver son propre périmètre. Les tests globaux, l’index et toute publication sont à la charge du coordinateur ; aucune modification de programme, banque, site ou état joueur n’a été faite par cet auteur.

## Points sensibles conservés

- Le DPE distingue énergie finale/primaire, millésime de méthode et performance physique. L’arrêté du 19 août 2026 prévoit un coefficient électrique futur de 1,7 au 1er janvier 2027 ; le coefficient de 1,9 reste celui décrit pour 2026. L’article d’entrée en vigueur a été ouvert ; la teneur de l’article de modification a été lue via l’index officiel, l’ouverture directe du texte ayant rencontré des erreurs. Cette limite est inscrite au registre.
- L’obligation de DPE collectif, le PPPT/PPT, le DTG, la décence locative et les votes de travaux sont distingués. Aucun résultat de diagnostic n’est déduit du simple respect d’une obligation de commande.
- MaPrimeRénov’ Copropriété : aide au syndicat, demande portée par le syndic en son nom. L’exercice sur 700 000 euros suppose des dépenses éligibles sur une assiette comparable au plafond ; le traitement HT/TTC réel reste à vérifier. Les aides conditionnelles, la trésorerie et la dette remboursable ne se confondent pas.
- P1–P5 : typologie contractuelle, aucun P5 universel. Le coefficient commun de répartition du chauffage vise l’énergie et comporte des exceptions historiques ; il n’est pas appliqué à toute la facture de maintenance.
- Droit à la prise : les articles actuels du CCH sont utilisés. Une ancienne page ministérielle consultée présente encore une ancienne procédure ; elle n’est pas retenue comme source de délais actuels.
- Aucune norme électrique, UPEC ou garde-corps intégrale non consultée n’est présentée comme lue. Aucun dimensionnement, indice minimal, niveau sonore, résistance au vent ou rendement garanti n’est inventé.

## Table précise de couverture technique

Les chemins sont relatifs à `cours/copro/`. Chaque ligne indique un développement, un mécanisme et un cas effectivement écrits ; elle ne constitue pas une validation professionnelle du thème.

| Sujet de JB | Texte propriétaire ou développement ajouté | Enseignement et limite |
|---|---|---|
| Climatisation, autorisation, bruit | `energie/physique.md`, `energie.physique.le-confort-d-ete` ; `energie/chauffage-collectif.md`, `energie.chauffage-collectif.pompes-a-chaleur-collectives` | Rejet de chaleur, apports, condensats, acoustique, fixation ; cas dernier étage et unités en toiture ; renvois aux chapitres droit travaux privatifs et troubles de voisinage. Pas de seuil sonore universel. |
| Store banne | `energie/physique.md`, `energie.physique.le-confort-d-ete` | Ombre avant vitrage, orientation, usage et efforts sur fixation ; cas de façade/ITE, autorisation et étude d’ancrage. Aucun classement vent prescrit. |
| Écologie et réchauffement | `complements/themes/technique-immeuble-2050.md` | Effet de serre, causes/conséquences, climat/ressources/eau ; cas de programme toiture et canicule. Source Météo-France et TRACC. |
| Comparaison des énergies | `energie/chauffage-collectif.md`, `energie.chauffage-collectif.quelle-energie-pour-quel-immeuble` ; dossier 2050 | Service comparable, enveloppe, émissions, coûts et dépendances. Aucun classement universel ni facteur carbone inventé. |
| P1, P2, P3, P4, P5 | `equipements/chauffage.md`, `equipements.chauffage.les-contrats-p1-a-p5` ; `energie/contrats-energie.md`, `energie.contrats-energie.le-contrat-d-exploitation-de-chauffage` | Énergie, conduite, renouvellement, financement, variantes de travaux ; cas pompe exclue et fourniture séparée. Aucun P5 légal uniforme. |
| Facture EDF | `equipements/chauffage.md`, même chapitre P1–P5 ; `energie/contrats-energie.md`, `energie.contrats-energie.gaz-et-electricite-pour-un-immeuble` | Fourniture, abonnement, quantités, périmètre, double facturation possible ; les postes P ne sont pas sa grille obligatoire. |
| Structure et fondations | `pathologie/structure.md`, `pathologie.structure.fondations-et-tassements` et `pathologie.structure.fissures-structurelles-et-leur-lecture` | Chemin des charges, tassement différentiel, hypothèses sol/réseau ; cas aile de cour. Pas de solution de stabilisation choisie sur photographie. |
| Lézarde et RGA | `pathologie/structure.md`, `pathologie.structure.microfissure-fissure-lezarde` et fondations | Description/activité/exposition distinguées ; RGA nommé et expliqué. Carte d’argile et chronologie ne prouvent pas seules la cause. |
| EP | `equipements/plomberie.md`, `equipements.plomberie.colonnes-eu-ev-ep` ; `pathologie/toitures.md`, `pathologie.toitures.cheneaux-et-eaux-pluviales` | Réseaux distincts, gravité, obstruction et débordement ; cas pluie et recherche de trajet. Pas de diamètre ou de débit normatif improvisé. |
| VMC hygroréglable | `equipements/ventilation.md`, `equipements.ventilation.simple-flux-double-flux-hygro` | Hygro A/B, tresse sensible, pression et chaîne d’air ; cas remplacement des fenêtres. Humidité différente de tous les polluants. |
| Enduit D2 | `pathologie/facades.md`, `pathologie.facades.enduits-et-classes-d-impermeabilite` ; `complements/themes/technique-enveloppe-abords-et-finitions.md`, section D2 | Revêtement décoratif, support et cause d’infiltration ; devis ambigu et fissure active. Normes complètes à retrouver. |
| Couvertine | Même dossier technique, section couvertine | Acrotère, rejet, joints, dilatation, tête de relevé ; cas angle ouvert et élargissement après ITE. Aucun détail dimensionné. |
| Toiture-terrasse et étanchéité | `pathologie/toitures.md`, `pathologie.toitures.toiture-terrasse-et-releves` et `pathologie.toitures.l-etancheite-materiaux-et-garanties` ; dossier technique | Continuité, niveaux, destinations, protection et accès ; cas dalles/bacs plantés. Pas de hauteur universelle. |
| Revêtements, résistance, poinçonnement, UPEC | Dossier enveloppe, section UPEC | Sollicitation du revêtement et complexe de pose ; cas hall/chariots. UPEC distinct de la portance de dalle et d’une étanchéité. Indices de locaux non consultés. |
| Ascenseur, machinerie, moteur, contrepoids | `equipements/ascenseurs.md`, `equipements.ascenseurs.les-organes-d-un-ascenseur` | Traction/hydraulique, déséquilibre, commande/frein, implantation ; cas panne d’un palier. Pas d’essai ou de déblocage par le gestionnaire. |
| Ascenseur GSM | Même chapitre ; `equipements.ascenseurs.la-mise-en-securite` | Chaîne téléalarme, technologie réelle, réception et secours ; cas boîtier neuf. Aucun calendrier d’opérateur extrapolé. |
| Garde-corps et ferronnerie | Dossier enveloppe, section garde-corps ; `pathologie/structure.md`, `pathologie.structure.balcons-et-corrosion-des-aciers` | Géométrie/résistance, corrosion, section résiduelle et ancrages ; cas remise en peinture. Normes intégrales et résistance à établir. |
| Bâtiment autonome et immeuble 2050 | `complements/themes/technique-immeuble-2050.md` | Bilan annuel, fonctionnement horaire, secours, stockage et réseau ; cas panneaux/batterie/toiture et partage solaire. Aucun label ou autonomie garantie. |
| RCU/réseau de chaleur | `equipements/chauffage.md`, `equipements.chauffage.la-sous-station-de-reseau-de-chaleur` et `equipements.chauffage.le-contrat-de-reseau-de-chaleur` ; `energie/chauffage-collectif.md`, `energie.chauffage-collectif.reseaux-de-chaleur` | Primaire/secondaire, échangeur, R1/R2, puissance et périmètre prioritaire. Carte de proximité différente d’une obligation ou offre ferme. |
| Dalkia | `equipements/chauffage.md`, `equipements.chauffage.les-exploitants-de-chauffage` ; `energie/contrats-energie.md`, contrat d’exploitation | Métier et périmètre contractuel ; cas défaut hydraulique. Page entreprise, aucune recommandation commerciale. |
| GRDF | `equipements/chauffage.md`, `equipements.chauffage.grdf-le-compteur-et-le-raccordement-gaz` et exploitants | Distribution/fourniture/maintenance distinguées, frontière d’incident. Pas d’attribution automatique d’un réseau à partir d’une marque. |
| Siphon disconnecteur | `equipements/plomberie.md`, `equipements.plomberie.surpresseur-compteurs-disconnecteur` | Assainissement distinct de protection d’eau potable ; garde d’eau, accès et circulation d’air. PDF Nicoll p.1 soumis à l’usine. |
| Curage | Même chapitre plomberie | Dépôts, bouchon, contre-pente et rupture distingués ; cas récidive au regard de sortie. Pas de périodicité nationale arbitraire. |
| « Trame désenfumage » | `equipements/acces.md`, `equipements.acces.desenfumage-et-extincteurs` | Terme ambigu : trappe, plan de repérage ou trame de contrôle à clarifier ; entrée d’air, évacuation et commande décrites. Aucun organe réglementaire imaginaire nommé trame. |
| Nid de poule | Dossier enveloppe, section nid de poule | Eau, gel-dégel, support et trafic ; cas récidive près d’avaloir. Source publique étrangère pour le mécanisme seulement. |
| Portail automatique et portillon | `equipements/acces.md`, `equipements.acces.portails-et-portes-de-garage` et `equipements.acces.la-porte-de-parking-en-panne` | Mouvement, sécurité, interverrouillage du portillon, panne et maintenance ; aucune neutralisation de sécurité. |
| Télécommande, interphone, combiné | `equipements/acces.md`, `equipements.acces.interphone-badges-ventouses-cellules` | Autorisation, communication et ouverture distinguées ; diagnostic par fonction. Notice du modèle à retrouver. |
| VIGIK+ | Même chapitre accès | Accès professionnels distinct des badges résidents, droits et administration ; cas prestataire refusé. Aucun calendrier commercial transformé en loi. |
| Minuteur astronomique | `equipements/electricite.md`, `equipements.electricite.eclairage-des-communs` | Calcul solaire vs capteur de lumière vs minuterie ; cas cour sombre et réglage. Ne remplace pas éclairage de sécurité. |
| MaPrimeRénov’, CEE, aides | `energie/aides.md`, trois chapitres | Conditions, assiette, engagement, cumuls à vérifier et trésorerie ; calculs fictifs corrigés. Aucune aide locale non retrouvée comptée certaine. |

Les compléments contiennent environ 1 957 et 1 402 mots respectivement au contrôle local. Les longueurs sont descriptives. Le principal travail restant est une relecture de fond indépendante avec les textes normatifs et études nécessaires à une utilisation prescriptive, puis une adaptation pédagogique aux acquis réellement observés.

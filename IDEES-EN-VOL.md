# IDÉES EN VOL — le registre qui ne perd rien

Créé le 30/08/2026 sur demande de JB (« prendre mes idées en vol pour
plus tard, ne pas les perdre »). Append-only : chaque idée lancée en
route atterrit ICI avec sa date, son statut, et où elle vit si elle a
été gravée. Une idée n'est jamais supprimée — elle change de statut.
Statuts : **GRAVÉE** (dans la spec/le produit, avec le pointeur) ·
**DIFFÉRÉE** (voulue, attend son chantier) · **À CREUSER** (pas
arbitrée) · **ÉCARTÉE** (dit pourquoi).

| Date | Idée (mots de JB) | Statut | Où / quoi |
|---|---|---|---|
| 29/08 | Régions à conquérir façon open map, « le boss de là-bas est trop dur mais t'as le droit d'y aller » | GRAVÉE | SPEC §3 carte-monde ; moteur `progression.py` |
| 29/08 | Quiz de positionnement (~20 questions) pour ne pas retaper les bases | GRAVÉE | SPEC §3 ; `quiz.py` ; écran maquette |
| 29/08 | Noter les questions fausses et pourquoi | GRAVÉE | SPEC §3 carnet d'erreurs ; `erreurs.py` |
| 29/08 | Boss de fin de région = examen (annales pour Arthur) | GRAVÉE | SPEC §3 ; format journal `examen` |
| 29/08 | Guerre de clan / tacles / choisir un thème chez l'autre | DIFFÉRÉE | M11 (défis), garde-fous posés |
| 29/08 | Payé le premier quart d'heure pour se former, si un jour agence | DIFFÉRÉE | Hors produit ; à ressortir le jour venu |
| 29/08 | Agent-compagnon : le back qui parle quand il n'y a plus rien à générer, et qui lance des skills | GRAVÉE | SPEC §4 ; construction M9/M10 |
| 29/08 | Auto-save, qu'on ne pense jamais à sauvegarder | GRAVÉE | SPEC §3 ; réel dans la maquette (journal à chaque clic) |
| 30/08 | La carte doit être une VRAIE carte, immersive, avec brouillard de guerre | GRAVÉE | SPEC §3 ; chantier front en cours |
| 30/08 | Entrer dans l'Académie = changer d'espace (plein écran jeu, autre menu) | GRAVÉE | SPEC §3 ; chantier front en cours |
| 30/08 | La carte en 3D (modèle 3D, brouillard) — packs d'assets .glb Three.js repérés (tweet Industrial Pack) | DIFFÉRÉE | SPEC §3 : chantier 3D après la 2,5D ; three@0.180 déjà dans le front ; licence des packs à vérifier AVANT (wiki/patterns/licence-outil-avant-fonctionnalite) |
| 30/08 | L'immeuble-monde : la carte de la copro est un immeuble (toiture = étanchéité, chaufferie = P1-P5, la rue = avocat/notaire/mairie) ; l'hôpital pour l'infirmier | GRAVÉE (cap) | SPEC §3 lieu-monde ; habillage v1.1, palais de mémoire (METHODE §11) |
| 30/08 | La carte est gigantesque : fin de branche = « théoriquement top 5 mondial du sujet » | GRAVÉE | SPEC §3 profondeur ; critère de construction du contenu |
| 30/08 | Cosmétiques de fin de zone sur un avatar (chapeau d'étudiant en droit, éclair dans la main), affichables ou non | GRAVÉE (différé build) | SPEC §3 (amende Q35) ; se construit avec M7/M11 |
| 30/08 | Tous les choix pédagogiques sourcés dans une méthode lisible par tous | GRAVÉE | `METHODE.md` (créé le 30/08) |
| 30/08 | L'algo est le prof : je clique une zone, je ne choisis jamais le format | GRAVÉE | SPEC §3 ; front en cours d'alignement |
| 30/08 | Documenter le pipeline « dessiner la carte d'un métier » pour chaque futur user | GRAVÉE | `gabarit-domaine/DESSINER-LA-CARTE.md` (créé le 30/08) |
| 29/08 | Branche Culture commune à tous les joueurs, terrain de défis | GRAVÉE | SPEC §3 ; config `arbre: false` |
| 29/08 | Module puzzle : « pas assez dur, j'apprends pas une langue » | ÉCARTÉE | Supprimé du front le 29/08 ; critère gravé (SPEC §3) |
| 29/08 | Scraper les sites de cours avec un robot | ÉCARTÉE | Droit des sources (SPEC §4) : dérivation depuis sources acquises, jamais de scraping |

| 30/08 | S'appuyer sur l'open source et les jeux existants : « choper des modèles, des modules, des fonctionnements ailleurs » | GRAVÉE | Benchmark licencié `travail/benchmark-2026-08-30.md` + lot d'icônes CC BY (game-icons.net) ; règle : licence vérifiée AVANT (wiki/patterns) |
| 30/08 | Îles en FORME de leur sujet (île-ascenseur, clé à molette, croix pharmaco), ponts/petits bateaux entre thèmes liés, boss = construire le pont | GRAVÉE | SPEC §3 « archipel parlant » (v1.05, entre-deux avant la 3D) |
| 30/08 | La carte est l'interface : pas de barre du bas, pas de bouton mode 3 minutes (s'arrêter tôt reste honorable) | GRAVÉE | SPEC §3 ; refonte lisibilité en cours |
| 30/08 | Zéro confettis ; célébrations = brouillard mental repoussé + citations des géants (Newton, Socrate), humilité et persévérance | GRAVÉE | SPEC §3 « épaules des géants » |

| 30/08 | « Trop dark, pas drôle, les modules se ressemblent — prends des libertés pour donner envie de rester » | GRAVÉE | SPEC §3 « la nuit n'est pas un tombeau » : couleurs par région, personnalité par type d'exercice, vie sur la carte, humour discret |

| 02/09 | « Une sorte de skill tree ; pourquoi pas abandonner le bateau, trop enfantin pour mes collègues ; ni genre ni âge » | GRAVÉE | `decisions/0001` ; BLUEPRINT §5 ; DA |
| 02/09 | « Un Duolingo de la copro » avec un pipeline pour que n'importe qui, 300 PDF et des sites fiables, se fasse son programme | GRAVÉE | `gabarit-domaine/USINE.md`, `sources/LISTE-BLANCHE.md`, `decisions/0008` |
| 02/09 | « La source s'affiche sur la question, on se méfie d'une source biaisée » | GRAVÉE | `decisions/0004` ; BLUEPRINT §10 |
| 02/09 | « Chaque chapitre fini ouvre le suivant, jusqu'à l'état de la science » | GRAVÉE | `decisions/0003` (niveaux 1-5) ; PROGRAMME §5 |
| 02/09 | « Passer sur papier parfois ? » | GRAVÉE | `decisions/0011` (dessin, feuille blanche) |
| 02/09 | « 15-20 minutes le matin, mais aussi une demi-journée, une journée » | GRAVÉE | `decisions/0005` ; BLUEPRINT §3 |
| 02/09 | « À glisser dans Académie : chaudière hybride, un chapitre dessus, peu importe où j'en suis » | GRAVÉE | `decisions/0009` ; `boite/` |
| 02/09 | « Un copain reprend tout le repo, fait ses fiches avec son LLM, et ça rentre dans mon truc » | GRAVÉE | `decisions/0008`, `0018` ; bibliothèque (ARCHITECTURE §6) |
| 02/09 | Saisons calées sur le calendrier du métier (proposition agent) | ÉCARTÉE | JB : « bizarre, j'aime pas » → semaine type, `decisions/0016` |
| 02/09 | « Des jours à thème : lundi rattrapage, vendredi exploration » | GRAVÉE | `decisions/0016` ; BLUEPRINT §4 |
| 02/09 | Cosmétiques de fin de zone sur un avatar (idée du 30/08) | ÉCARTÉE | `decisions/0015` : pas d'avatar, l'arbre est l'avatar, palettes et insignes |
| 02/09 | Voix générées (situations à écouter, podcast de chapitre) ; photothèque sûre | DIFFÉRÉE | JB : « plus lourd que QCM ou relier, plus tard » → `decisions/0017`, `ACA-MEDIA-1` |
| 02/09 | « Un mailing tout prêt au collègue : je viens de passer le niveau de base en compta » | GRAVÉE (partage manuel) | BLUEPRINT §13 : le produit fabrique la carte, le joueur l'envoie lui-même |
| 02/09 | « Je veux que tous les joueurs se voient » | GRAVÉE | `decisions/0010` amendée ; DOCTRINE §2 |
| 02/09 | « S'appuyer sur des repos open source (learning, QCM, relier, lecteurs, classement, profil) et reprendre le code pour en être maître » | GRAVÉE (chantier) | `travail/2026-09-02-reutilisation-a-verifier.md` ; `ACA-REUSE-1` |
| 02/09 | « Une fois les fiches générées par les autres, les stocker sur le VPS pour les suivants » | GRAVÉE | bibliothèque commune, ARCHITECTURE §6, `ACA-BIBLIOTHEQUE-1` |
| 02/09 | Le lieu-monde (l'immeuble en coupe) comme habillage de l'arbre | DIFFÉRÉE | derrière l'arbre lui-même ; METHODE §11 |

| 03/09 | « Que ce soit tellement cadré qu'un autre LLM ne puisse pas dévier en codant » | GRAVÉE | `decisions/0025`, `CONTRIBUER.md`, `chantiers/`, `tooling/check.py` |
| 03/09 | « Trancher la voix du site, pas infantilisant, comment l'app nous parle » | GRAVÉE | `decisions/0024`, `VOIX.md`, `contenu/voix.json` |
| 03/09 | « Trouver des modules, banques d'éléments, animations, icônes 2026 » | GRAVÉE (candidats) | `travail/2026-09-02-reutilisation-a-verifier.md` § banques d'éléments ; `ACA-REUSE-1` |
| 03/09 | « Imaginer l'arbre sur trois mois, les compétences, les étapes, comme le programme d'une formation en ligne, sans rédiger » | GRAVÉE | `SYLLABUS.md`, `programme/genere_copro.py` (parcours trimestre-1, sous-branches, compétences, notions, mots-clés) |
| 03/09 | « Les docs viennent peut-être à côté du programme, en étude de docs » | GRAVÉE | `decisions/0026` : bibliothèque, quatre voies vers l'arbre |
| 03/09 | « PDF vers quoi ? les images ? périmé ? dispo depuis l'app ? » | GRAVÉE | `decisions/0026`, `travail/2026-09-03-test-ingestion.md` |
| 03/09 | « Moi j'utilise des abonnements, jamais d'API » | GRAVÉE | `decisions/0026` §4 : l'usine tourne sur abonnement, l'API à titre indicatif |
| 03/09 | « Un sujet carte blanche test : c'est quoi le prompt, la méthode, les contraintes » | GRAVÉE | `boite/GLISSER.md`, satellite témoin `chapitres/satellites/chaudiere-hybride.json` |
| 03/09 | « Qu'un modèle plus petit ne puisse pas mal faire, mentir ou se planter ; forcé à faire petit à petit sans tricher ; des points de sauvegarde » | GRAVÉE | `decisions/0027`, `app/usine/`, `MODELES.md`, `CONTRIBUER.md` §8 |
| 03/09 | « Documente les modèles actuels, forces et faiblesses selon nos benchmarks, humblement » | GRAVÉE | `MODELES.md` (à relire le 03/12/2026) |
| 03/09 | « Un onboarding : nouveau pseudo, petit catalogue, créer le vôtre, le prompt à coller dans Claude Code, Codex, Antigravity, Cursor » | GRAVÉE | `COMMENCER.md`, `prompts/`, `programme/catalogue.json`, chantier `ACA-ONBOARDING-1` |

*Toute session qui entend JB lancer une idée en route l'ajoute ici
dans le commit du jour, même si elle est gravée ailleurs dans la
foulée : ce tableau est l'index de traçabilité.*

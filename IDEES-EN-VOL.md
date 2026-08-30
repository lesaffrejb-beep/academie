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

*Toute session qui entend JB lancer une idée en route l'ajoute ici
dans le commit du jour — même si elle est gravée ailleurs dans la
foulée : ce tableau est l'index de traçabilité.*

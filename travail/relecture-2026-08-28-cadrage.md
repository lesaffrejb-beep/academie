# Relecture 2026-08-28 — cadrage de l'Académie (pré-mortem par agent frais)

Protocole : `.agents/skills/erp-complete/references/pre-mortem.md`, adapté à
un cadrage produit (pas de chiffres de copro à recalculer ; l'agent a
attaqué la cohérence interne, les dépendances techniques réelles du
repo, la doctrine, et les angles juridiques/RGPD). Agent frais Opus,
lancé le 28/08/2026 après le second brief JB (renommage + ateliers).
Verdict rendu : **19 BLOQUANTS, 6 MINEURS, 5 questions sans réponse.**
Tous les bloquants sont réparés dans BLUEPRINT.md et ROADMAP.md le
jour même ; ce rapport trace chaque trouvaille et sa réparation.

Verdict global de l'agent (verbatim) : « Le cadrage est brillant sur
le papier et faux sur trois points vérifiables (un pré-mortem qui n'a
jamais eu lieu mais qui est certifié dans trois fichiers, une routine
du matin qui n'atteindra jamais le VPS, un partage aux collègues qui
ouvre tout le portefeuille), et il programme la panne sèche de contenu
vers le 20e matin, c'est-à-dire avant son propre gate de survie. »

## Les BLOQUANTS et leur réparation

| # | La trouvaille (résumée) | La réparation |
|---|---|---|
| 1 | Le pré-mortem était certifié dans 3 fichiers AVANT d'avoir eu lieu (le rapport n'existait pas) | Vrai au moment de l'audit : la ROADMAP avait été écrite en anticipant la passe. Le pré-mortem a maintenant EU lieu, ce rapport est la trace ; leçon retenue : on ne date jamais un contrôle avant de l'avoir passé |
| 2 | Stock M1 (60-80 cartes) = 12-27 matins de neuf : panne sèche avant le gate des 30 séances | L'approvisionnement devient une EXPLOITATION hebdo chiffrée (BLUEPRINT §7 : 15-20 cartes/sem, ~1 session agent, ~10 min JB), démarrée en M2 ; un matin sans neuf = séance valide (révisions seules) |
| 3 | Jusqu'à M3/M5 le produit est « Anki en moins bien » ; le différenciateur arrive après la fenêtre de conviction | Assumé en face (BLUEPRINT §2 : comparaison honnête avec Anki) ; export CSV Anki = assurance-vie du contenu ; option « démarrage express dans Anki pendant que M2 se construit » soumise à JB (§13.7) ; fil du réel v0 manuel dès M2 |
| 4 | La Routine 7h00 ne peut pas atteindre le VPS : maj-vps.sh est manuel (décision R10), le « fini quand » de M2 était inatteignable | La chaîne est décrite maillon par maillon (BLUEPRINT §10) ; la brique manquante est nommée : timer de pull systemd côté VPS, borné à academie/site/, GO JB requis (§13.8), inscrite dans M2 |
| 5 | « La routine graphe de 7h30 » n'existe pas sous ce nom ; la vraie (« Feuille de route du matin », trig_01R7…, 7h30 lun-ven) occupe déjà le créneau | Corrigé : la routine existante est nommée avec sa trace (meta/2026-08-19-roadmap-etape-2.md) ; l'Académie tourne à 7h00, AVANT, sans la toucher |
| 6 | Trois rituels se disputent 8h15 (Aujourd'hui/file RED, feuille de route du lundi, Académie) sans arbitrage | Ordre du matin proposé et soumis à JB (BLUEPRINT §1, §13.6) : Académie d'abord, SAUF Red Path — un RED non traité s'affiche en bandeau avant le tirage (règle dure 5 respectée structurellement) |
| 7 | Le partage collègues (M9) promettait un cloisonnement que l'hébergement réel contredit (basicauth partagé sur tout erp/site, clone complet du repo sur le VPS) | M9 gagne un préalable absolu : DISTRIBUTION séparée (site Académie autonome généré, propre vhost, propres identifiants, jamais le clone du repo) + revue anti-fuite mécanique dans le « fini quand » |
| 8 | « Pattern R10 » invoqué à tort : journal_io est borné aux JOURNAL OFF-*, un commit-push PAR écriture (10 cartes = 10 pushes) | Corrigé (BLUEPRINT §10, M8) : route dédiée POST /api/academie/revues, écriture par LOTS (une séance = un commit), présentée comme une EXTENSION du back à concevoir, pas un réemploi |
| 9 | « Pattern R8 » invoqué à tort pour le hors-ligne : R8 a explicitement refusé le service worker | Corrigé (§10, M8) : service worker PROPRE à l'Académie, avec la justification de pourquoi le refus R8 ne s'applique pas ici (séance figée à 7h00) ; M8 passe à deux sessions |
| 10 | Le socle scientifique ne respecte pas la règle qu'il impose aux cartes (9 références sans vérification, 2 chiffres nus) | Encadré d'honnêteté de sourçage ajouté en tête du §3 ; les 2 chiffres passent en [À VÉRIFIER] ; M1 inclut le re-sourçage (DOI/lien + date) de toutes les références |
| 11 | M1 demandait à JB de relire du markdown brut (interdit par CLAUDE.md) | « Fini quand » de M1 corrigé : 20 cartes rendues en HTML minimal |
| 12 | Tailles de chantier incompatibles avec les « fini quand » (7 séances réelles ≠ deux sessions) | Convention gravée en tête de ROADMAP : taille = sessions de construction, « fini quand » peut exiger EN PLUS un délai calendaire ; M1 et M2 redimensionnés |
| 13 | Trois semaines d'AG = arriéré FSRS en centaines de cartes, aucune règle ne l'attrapait | BLUEPRINT §4 et §8 : plafond d'affichage (~20 revues), ré-étalement automatique (on ré-étale, on ne jette jamais), mode vacances ; câblé dès M2 |
| 14 | L'atelier devis ne pouvait pas corriger : soit un audit que JB a déjà validé (rien d'appris), soit un jet LLM non vérifié (interdit) | Règle §6.6 : pièce choisie parmi les dossiers que JB n'a PAS traités ; corrigé produit AVANT l'atelier et validé par le circuit qualité des cartes ; corrigé non validé = atelier ne sort pas |
| 15 | La pièce réelle copiée dans etat/jb/ateliers/ violait la frontière reçu/produit (jamais de doublon du serveur dans le repo) | Règle §6.2 : l'atelier POINTE le .md converti (OFF-X/pieces/), ne copie jamais ; conséquence assumée (jouable seulement là où le coffre est présent, jamais dans la distribution collègues) |
| 16 | Granola : la question de consentement était posée à l'envers (le GO de JB ne couvre pas la parole des TIERS transcrits) | Arbitrage rendu §12.10 : transcriptions de réunions = NON par défaut ; alternatives sans tiers (JOURNAL, questions de JB à Claude, rituel dicté de sortie de réunion) ; §13.2 reformulé dans ce sens |
| 17 | Quatre traitements de données nouveaux, aucun au registre RGPD (pourtant « doctrine vivante ») | M2 : inscription au registre AVANT la première écriture de revues.jsonl (données d'apprentissage d'un salarié, contexte.jsonl, pointeurs d'ateliers) ; rappelé dans les risques |
| 18 | Photos de VT rangées dans la banque partagée que le §7 leur interdit ; « anonymisée » non défini | §7 et M4 : couche perso par défaut ; montée en banque photo par photo, anonymisée (définition écrite : cadrage serré, aucune adresse/plaque/visage/élément identifiable) ET validée par JB |
| 19 | revues.jsonl + arbre = cartographie des faiblesses d'un salarié, sans règle de lecture (risque outil d'évaluation) | Règle gravée §9 : état lisible par son propriétaire SEUL, aucun écran comparatif, bilan à JB seul, refus doctrinal de tout usage managérial, opposable ; arbitrage §12.9 |

## Les MINEURS et leur sort

| # | La trouvaille | Le sort |
|---|---|---|
| 20 | `etat/jb/` codé en dur dans l'arborescence | Corrigé : `etat/<profil>/` partout, jb = premier profil, « jamais de prénom en dur » rappelé §11 |
| 21 | « Le tram » = décor sans fait dans le repo | Corrigé : « en mobilité, hors du bureau » ; le critère M8 ne dépend plus d'un moyen de transport supposé |
| 22 | py-fsrs / ts-fsrs non déclarés (socle stdlib seule) | Corrigé §8 + M2 : déclaration dans tooling/requirements/ ou portage pur Python, arbitrage au chantier |
| 23 | Machine à sous à deux faces (2 modes en M2) + contradiction de ton sur le « dark pattern » | Corrigé : M2 = menu simple assumé, le tirage-machine à sous n'arrive qu'avec 4+ modes (M4) ; la ligne du tableau des patterns reformulée (la surprise porte sur l'emballage, jamais sur une monnaie) |
| 24 | « Rien en dessous de M1 » autorisait littéralement à démarrer M1 sans GO | Formulation durcie : « M1 et tout ce qui suit ne démarrent qu'après le GO de JB sur les arbitrages du §13 » |
| 25 | Le bloc FILE-ALERTES du 28/08 a été réécrit malgré la règle append-only | Assumé et tracé : le bloc n'avait jamais été fusionné ni lu par le front (même PR), le renommage rendait ses chemins faux ; la mention de réécriture figure dans le bloc lui-même. La règle reste intacte pour tout bloc publié |

## Les 5 questions de l'agent, et où vivent les réponses maintenant

1. **Qui fabrique les cartes du 21e au 120e matin, à quel coût ?** →
   BLUEPRINT §7 : exploitation hebdo chiffrée (lot 15-20 cartes, ~1
   session agent/semaine batchable en fenêtre creuse, ~10 min JB).
2. **Le matin du 12 septembre, après trois semaines d'AG ?** →
   BLUEPRINT §4/§8 : plafond ~20, ré-étalement automatique, mode
   vacances ; une reprise ressemble à une séance normale.
3. **Comment un collègue voit l'Académie sans voir le portefeuille ?**
   → ROADMAP M9, préalable absolu : distribution autonome générée,
   vhost et identifiants propres, revue anti-fuite dans le fini-quand.
4. **Combien coûte M1+M2 vs Anki + deux soirées de saisie ?** →
   BLUEPRINT §2 : comparaison honnête écrite ; export CSV Anki
   permanent ; option de démarrage express dans Anki soumise à JB
   (§13.7) — c'est lui qui tranche si la construction vaut son coût.
5. **À quoi verra-t-on que JB a appris, avant M7 ?** → ROADMAP, gate
   des ~30 séances : mini-test de rétention (20 cartes du premier lot
   rejouées à froid, score en clair), pas seulement des métriques
   d'usage.

## Ce que JB relit

Le BLUEPRINT (surtout §13, les 8 arbitrages), la ROADMAP (le bloc
« risque numéro un »), et ce rapport. Rien d'autre.

# Relecture 2026-08-29 — la roadmap Académie après la révision « produit autonome »

Protocole : `.agents/skills/erp-complete/references/pre-mortem.md`, adapté à
un cadrage produit. Agent frais Opus, lancé le 29/08/2026 sur demande
de JB (« premortem et fixe ce qui est faible »). Cible : la couche du
29/08 (M9-M11 réécrits, 4 arbitrages) jamais attaquée, plus la
cohérence roadmap ↔ code réel. Le rapport du 28/08
(`relecture-2026-08-28-cadrage.md`) restait acquis, ses réparations
n'ont pas été re-signalées — sauf une, qui n'avait pas tenu.

Verdict rendu : **13 BLOQUANTS, 8 MINEURS, 5 questions sans réponse.**
Tous réparés le jour même dans ROADMAP.md et BLUEPRINT.md ; ce rapport
trace chaque trouvaille et sa réparation.

Verdict global de l'agent (résumé) : la révision du 29/08 empile trois
chantiers produit sur un socle dont le maillon terminal ne fonctionne
pas (le timer met à jour un fichier que l'écran de JB ne lit pas), le
front de l'Académie vit DANS le React de l'ERP alors que la roadmap le
dit « isolé », et les quatre arbitrages n'ont aucune traduction
technique — deux contredisent frontalement des textes gravés (§9,
M6 v2).

## Les BLOQUANTS et leur réparation

| # | La trouvaille (résumée) | La réparation |
|---|---|---|
| 1 | La chaîne du matin n'atteint pas l'écran de JB : le timer régénère `academie/site/banque.json`, mais le front React consomme `erp/react/src/data/academie-banque.json` à la COMPILATION — sans rebuild + sync erp/site, la séance ne bouge jamais. Le bloquant n°4 du 28/08 n'était réparé que sur le papier | M2 « reste à faire » réécrit : le maillon cassé est nommé en n°1, avec les deux réparations possibles (fetch runtime de banque.json — préféré — ou timer étendu au rebuild) et l'aveu que le « fini quand » de M2 est inatteignable tant qu'il n'est pas posé |
| 2 | M9 chiffré « 2-3 sessions » alors que le front est tissé dans six+ fichiers de l'ERP (Academie.jsx, components/academie/, lib, data, App/Barre/Rail/Palette) ; « academie/ est isolé » est un fait faux | M9 : bloc « le coût réel de l'extraction, dit en face » (liste des fichiers, extraction = reconstruire le front hors châssis ERP) ; taille passée à « à chiffrer en ouverture » ; la ligne « isolé » du bloc risques corrigée en son contraire |
| 3 | M9 sans hébergeur, payeur, mainteneur ni brique d'auth (seul mécanisme existant : basicauth PARTAGÉ) ; « JB ne paie jamais pour les autres » contredit par l'infra que JB paie | M9 : « quatre briques que M9 doit NOMMER avant de coder » (auth, hébergement + payeur en arbitrage JB explicite, stockage de clé tiers, flux fournisseur→produit) ; arbitrage 3 reformulé en tête : « JB ne paie jamais l'IA des autres », l'infra reste à trancher |
| 4 | Arbitrage 3 (clé par personne) contredit M6 v2 resté écrit « clés côté serveur, D20 » | M6 réécrit : clé D20 serveur = profil JB mono-joueur seulement ; dès M9+, chaque appel LLM part sur la clé DU joueur |
| 5 | La clé API par personne n'a ni existence technique ni règle de sécurité ; « son propre abonnement (Claude Code, Codex, Antigravity) » n'est pas une architecture (pas d'endpoint appelable) | Arbitrage 3 et M9 : piste abonnement passée en `[À VÉRIFIER]` avec la raison ; stockage de clé tiers = brique de conception dédiée (jamais en clair, jamais dans un repo) |
| 6 | M10 confie la validation au seul arrivant, qui ne connaît pas encore la matière — le mécanisme exact qui fait apprendre des faussetés (précédent interne : `validated`/`confidence: 0.85` a couvert 4 citations fausses pendant 4 mois) | M10 : bloc « la qualité ne repose PAS sur l'arrivant seul » — la double passe par agent frais remontant aux sources reste obligatoire pour tout domaine généré (sur la clé de l'arrivant), l'arrivant n'est que l'échantillonneur ; le bouton « carte fausse » requalifié en filet, pas en contrôle |
| 7 | Arbitrage 1 (visibilité totale) casse le §9 gravé « aucun écran comparatif entre profils, jamais » — deux documents du dossier se contredisaient mot pour mot | §9 du BLUEPRINT AMENDÉ (pas contourné) : l'interdit absolu devient « hors cercle d'amis mutuellement consentis », l'interdit managérial intact ; M11 trace l'amendement explicitement (« une règle amendée sur brief tracé reste opposable ») |
| 8 | « Jamais d'usage managérial » = un vœu sans mécanisme ; rien n'empêche un manager d'être « ajouté en ami » | M11 : mécanismes minimums écrits (ajout strictement mutuel, retrait d'un clic silencieux, visibilité désactivable par domaine, avertissement à l'ajout, règle dans les conditions du produit) ; le risque résiduel de pression sociale est nommé comme non résolu |
| 9 | Registre RGPD muet sur l'Académie ; M9-M11 ajoutent des personnes concernées TIERCES, un hébergement et des transferts entre utilisateurs, sans base légale ni droit à l'effacement | M9 : le RGPD devient un PRÉALABLE bloquant (« pas de compte tiers sans » registre, base légale, information, durée, suppression de compte) ; risque « le RGPD change de nature à M9 » ajouté au bloc final |
| 10 | M10 dépend du « NotebookLM via le skill existant » — un skill de la session Claude de JB, pas une API qu'un produit web peut appeler pour un tiers | M10 : dépôt de documents = voie principale ; NotebookLM tiers = piste `[À VÉRIFIER]` avec la raison |
| 11 | Les défis de M11 sont la comparaison extrinsèque que la Loi 7 (SDT) du cadrage documente comme destructrice de motivation ; le garde-fou « pas de ligue » était déclaratif | M11 : bloc « défis vs Loi 7 » — la contradiction est dite en face, les défis restent (arbitrage JB) mais optionnels, jamais proposés d'office, et coupés si les données d'usage montrent une dégradation du rituel (critère et relevé à poser avant la première partie) |
| 12 | Arbitrage 4 (« réponse libre avancée dès que le rituel tient ») court-circuitait le gate des 30 séances et ne modifiait pas M6 : ordre indécidable pour une session qui reprend | Arbitrage 4 reformulé : la v1 réponse libre peut être avancée AU MÊME GATE que M4, jamais avant ; M6 renvoie à cette règle ; le coût LLM récurrent par correction est à chiffrer au moment d'avancer |
| 13 | M9 gaté par « plusieurs semaines », non mesurable (ni compteur, ni seuil, ni décideur), alors que M10-M11 en dépendent — violation de la convention de tête | M9 : gate mesurable (bilan des ~30 séances passé + 4 semaines supplémentaires à ≥ 4 séances/semaine dans `revues.jsonl` ; décideur JB) |

## Les MINEURS et leur sort

| # | La trouvaille | Le sort |
|---|---|---|
| 14 | BLUEPRINT parle d'`academie.yaml`, le fichier réel est `academie.json` | Corrigé (2 occurrences) |
| 15 | M1-bis inséré entre M2 et M3 dans le fil de lecture, ordre réel « après le pilote M1 » | Encadré ajouté en tête de M1-bis : le placement de lecture ne dit pas l'ordre |
| 16 | Doubles sections M1/M2 (« fait » + « cadrage d'origine ») sans règle de préséance | Troisième convention gravée en tête : le bloc d'avancement fait foi |
| 17 | Banque réelle (droit 28, compta 11, patho 10, sinistres 10) : équipements et procédure à zéro, sinistres non arbitré | Constat écrit dans M1 « reste à faire » : à rééquilibrer dans les prochains lots |
| 18 | M4 affirmait que la carte « souche » existait ; aucune carte de la banque ne contient le mot | Corrigé : la carte est à produire avec l'image |
| 19 | Le flux fournisseur → produit (format, fréquence, versionnage du contrat) n'existait nulle part | Intégré aux « quatre briques » de M9 (brique 4) |
| 20 | Risque « abandon de l'ami pilote » absent alors que les fini-quand de M10/M11 en dépendent | Risque ajouté, avec repli (domaine public de test, second profil JB : la mécanique se valide sans l'ami, l'ami valide le produit) |
| 21 | Risque « dérive de périmètre » jamais nommé sous l'angle M9-M11 (produit grand public qui ne sert pas la rétention de JB) | Risque ajouté : si le temps manque, c'est M9-M11 qu'on gèle |

## Les 5 questions de l'agent, et où vivent les réponses maintenant

1. **L'ami sans clé API, que voit-il ?** → Partiellement traité (le
   mode dégradé sans LLM n'est pas conçu) : à poser dans le cadrage
   d'ouverture de M9/M10. Reste OUVERT pour JB.
2. **Qui est responsable de traitement, qui répond à un effacement ?**
   → M9, préalable RGPD : JB responsable de traitement, suppression de
   compte obligatoire avant le premier compte tiers.
3. **Comment un arrivant détecte une carte fausse qu'il n'a pas encore
   apprise ?** → M10 : il ne le peut pas, donc la double passe par
   agent frais reste le contrôle qualité, l'arrivant n'échantillonne.
4. **Qu'est-ce qui empêche techniquement un manager d'être ami ?** →
   M11 : mécanismes minimums écrits ; le résiduel (pression sociale)
   est nommé non résolu, dit à JB tel quel.
5. **Après extraction, qui maintient deux dépôts ?** → M9, brique 4
   (versionnage du contrat, correction de bugs moteur) : nommée, à
   arbitrer en ouverture de chantier. Reste OUVERT pour JB.

## Ce que JB relit

La révision du 29/08 en tête de ROADMAP (arbitrages 3 et 4
reformulés), M9-M11, le §9 amendé du BLUEPRINT, et ce rapport. Deux
questions restent ouvertes pour lui : le mode dégradé sans LLM (Q1) et
la maintenance bicéphale après extraction (Q5).

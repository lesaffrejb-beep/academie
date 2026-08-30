# Relecture 2026-08-29 (soir) — la SPEC-PRODUIT et la Partie 4 du cadrage après la séance JB × Arthur

Protocole : `.agents/skills/erp-complete/references/pre-mortem.md`, adapté à
un document d'architecture. Agent frais Opus, lancé le 29/08/2026 au
soir. Cibles : `SPEC-PRODUIT.md` (version initiale), `CADRAGE-PRODUIT.md`
Partie 4, les amendements du soir (ROADMAP, BLUEPRINT §9, README,
CLAUDE.md). L'agent a vérifié contre le code réel (`app/*.py`,
`erp/react/src/**`, `banque/`, `etat/`) — c'est ce qui a produit les
trouvailles les plus dures.

Verdict rendu : **1 RED PATH, 20 BLOQUANTS, 12 MINEURS, 8 questions.**
Tous réparés le soir même dans les fichiers cibles ; ce rapport trace
les trouvailles majeures et leur réparation. Le rapport intégral de
l'agent est résumé ici ; les numéros (B0-B20, M1-M12) sont les siens.

## RED PATH — réparé avant tout le reste

**B0 — Un podium de cinq collègues réels nommés, avec des métriques de
performance inventées, était dans le build servi du front** :
`ProfilsErpConnector.jsx` (+ `PodiumLeaderboard.jsx`,
`ManagerPassportCard.jsx`) classait cinq personnes de l'agence avec
taux de vote AG, XP, « certifications » fabriqués — l'écran comparatif
que BLUEPRINT §9 interdit, l'anti-pollution de CLAUDE.md, et un
traitement RGPD de tiers non informés, servi derrière le basicauth
partagé. **Réparé le 29/08** : profils fictifs « Agence Démo »
(source + rebuild React + regénération `erp/site`, vérifié zéro nom
réel dans le bundle Académie), bloc RED dans FILE-ALERTES, fait
constaté écrit dans SPEC §5 comme preuve que le garde-fou §9 ne tient
pas sans mécanisme.

## Les bloquants majeurs et leur réparation (tous appliqués)

| # | Trouvaille (résumée) | Réparation |
|---|---|---|
| B1 | Rien n'enregistre une révision, nulle part : pas de localStorage, pas d'appel réseau, `revues.jsonl` jamais créé ; O1 ne réparait que la fraîcheur d'un écran qui n'écrit rien | O1 scindé en O1a (fetch runtime) et **O1b (le chemin d'écriture, brique sortie de M8)** ; ROADMAP M2 reste n°0 ; fini-quand : « une réponse jouée le matin est relisible le soir » |
| B2 | Gates circulaires : les gates M4 et M9 se mesurent dans un journal que seul M8 savait écrire | O1b posé en M2 ; gates annotés « mesurables à partir d'O1b » |
| B3 | La carte-monde n'avait aucun chantier (M7 restait « l'arbre ») | M7 réécrit (carte-monde + boss-examens), sort de `SkillTree.jsx` dit |
| B4 | « XP » indéfini, deux mesures accolées | Une formule unique : % des cartes `valide` de la région à stabilité ≥ 21 j (paramétré) ; XP = affichage dérivé |
| B5-B6 | La mécanique du quiz ne produisait pas l'effet promis (S standard = ~2 j, mesuré) et se contredisait sur le remplissage | Quiz réécrit : stabilité initiale paramétrée + `origine: "quiz"` au journal ; mauvaise réponse = rien ; le quiz OUVRE des régions, n'écrit jamais le remplissage |
| B7 | Le modèle A4 supposait chez Arthur un runtime jamais nommé | Runtime nommé (Claude Code / Desktop + fichiers), liste d'installation = étape 0 d'O7, repli v1 écrit (la fabrique tourne chez JB) |
| B8 | La soirée artisanale violait l'invariant « IA locale au coût du joueur » | Exception nommée et bornée dans l'invariant 2, avec la mesure comme justification |
| B9 | 10 €/mois vs double passe : mauvais ordre de grandeur | Fabrication (dizaines d'€, ponctuel, PAS couvert par 10 €) séparée de l'usage (~0 € en v1) ; v1 bornée à ~30 cartes ; GO/NO-GO chiffré avant toute promesse |
| B10-B11 | « Clé en localStorage » pas une architecture ; contradiction avec M6 v2 | Un seul chemin v1 : copier-coller pour tous ; clé navigateur `[À VÉRIFIER]` hors v1 ; M6 amendé |
| B12 | Le push n'avait pas de réceptionniste | Brique d'ingestion nommée dans O6 (jeton, re-validation, quarantaine) ; geste joueur = téléversement depuis le produit |
| B13 | Magic links : personne n'envoie le mail ; dépendance de 8h15 à un mail | Fournisseur d'envoi à choisir en O6 (sous-traitant au registre) ; magic link à l'inscription seulement + cookie ≥ 1 an ; repli manuel |
| B14 | Données de santé (art. 9) jamais nommées pour un domaine infirmier | Interdiction écrite (aucune donnée patient réelle, images licenciées seulement), reprise au guide d'agent et au contrôle de réception |
| B15 | Le RGPD commence à O4, pas à M9 (les données d'Arthur sont déjà dans le dépôt) | Information d'Arthur déplacée AVANT O4 ; question « pseudonymiser ? » posée à JB |
| B16 | Suppression 48 h impossible si les banques reçues sont dans git | Banques de joueurs HORS git (invariant 3) |
| B17 | Les couches `interne`/`perso` de JB perdaient leur domicile à l'extraction | Le serveur accepte les cartes liées à un profil unique, jamais servies à un autre ; `contexte.jsonl` ne quitte jamais le poste de JB |
| B18 | « Trois composants » : il y en a 16 (~5 200 lignes), dont des maquettes M11 avant gate | Chiffre corrigé dans M9 ; inventaire « survit / se jette » = entrée de chantier d'O6 |
| B19 | Le calendrier réel (~3 mois avant qu'Arthur joue) et la date de son concours absents | Calendrier plancher écrit au §7 ; date du concours = reste-dû immédiat ; parade : paquet Anki de ~30 cartes en clôture d'O4 (export_anki construit en O2) |
| B20 | La spec certifiait son propre pré-mortem au passé (le motif « validated sans lien ») | En-tête corrigé, pointe ce rapport réel |

Mineurs (M1-M12), tous appliqués : garde-fou des gates rétabli dans
CLAUDE.md ; `export_anki.py` passé au futur dans le CONTRAT §4 et
planifié en O2 ; fini-quand d'O2 chiffré (+30 cartes, 0 brouillon) ;
README (maillon cassé nommé dans le schéma, M0 à M11) ; mode dégradé
= défaut d'Arthur en v1 ; sous-domaine accepté ; `examen.py` seul
(il inclut les tests Académie) ; O5 détaillé (amendements M6/M7/M8 +
arbitrage 4 conservé) ; note SQLite dans M8 ; stockage du carnet
d'erreurs tranché (jsonl → SQLite, même schéma) ; seuils quiz/région
découplés ; les cinq morts du §5 ont chacune leur parade.

## Les 8 questions de l'agent, et où vivent les réponses

1. Date du concours d'Arthur → reste-dû immédiat (Partie 4).
2. Où s'écrit une révision d'ici M8 → O1b (localStorage + export, ou
   route back par lots — l'arbitrage fin se prend au chantier, le
   contrat client est stable par exigence).
3. Qui envoie les magic links → O6 choisit le fournisseur ; cookie
   longue durée gravé (SPEC §5). Le « qui paie » reste JB (infra).
4. Couches `interne`/`perso` après extraction → tranché (B17).
5. Arthur informé que ses données sont dans le dépôt → reste-dû avant
   O4 + question « pseudonymiser ? » posée à JB.
6. Sort des 16 composants → inventaire d'ouverture d'O6 ; le podium
   est déjà neutralisé (B0).
7. Budget de JB pour la soirée artisanale → reste-dû avant O7.
8. Déclencheur des pré-mortems personnels Q52 → la session qui ouvre
   M9 les réclame et ne s'ouvre pas sans (Partie 4).

## Ce que JB relit

SPEC-PRODUIT §2 (invariants durcis), §3 (quiz et remplissage
recalculés), §7 (O1a/O1b et le calendrier plancher), la table des
reste-dû de CADRAGE Partie 4, et le bloc RED du 29/08 dans
FILE-ALERTES.

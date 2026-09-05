# 0027, Le pas à pas imposé : points de sauvegarde, classes de modèles, rien sur parole

**Amendée le 05/09/2026 par [0034](0034-capacites-sans-classes-de-modeles.md) :**
les catégories de modèles, leurs plafonds et leurs restrictions sont retirés.
Le texte ci-dessous conserve la décision historique ; seuls les contrôles
documentaires et les points de reprise restent en vigueur.

- Statut : acceptée
- Date : 03/09/2026
- Décideur : agent, sur le brief de JB du 03/09 (« qu'un modèle plus
  petit ne puisse pas mal faire, mentir ou se planter ; s'il est nul ou
  tout petit, qu'il soit forcé à faire petit à petit sans pouvoir
  tricher ; des points de sauvegarde pour ne pas perdre les cent
  premières pages ; documenter les modèles, leurs forces et leurs
  limites, humblement ; un onboarding avec un petit catalogue et
  « créer le vôtre », tout prémâché pour Claude Code, Codex,
  Antigravity, Cursor »)

## Décision

1. **Tout travail long passe par un script qui distribue le travail par
   unités et juge chaque unité avant de donner la suivante.** Pour la
   lecture d'un document, c'est `app/usine/usine.py` : `preparer`
   (mécanique), `declarer`, puis la boucle `suivant` / `valider`, puis
   `fiche` et `registre`. Le modèle ne décide ni de la taille de l'unité
   ni du moment où elle est finie.
2. **Le modèle se déclare** (outil, modèle, classe) avant la première
   unité. Une classe inconnue vaut petit ; un nom de petit modèle
   (motif `modeles_petits` d'`academie.json`) ne se déclare pas grand.
   La classe fixe la taille initiale et le plafond des unités.
3. **La taille des unités suit les résultats, pas la déclaration** :
   trois unités propres d'affilée doublent la taille jusqu'au plafond de
   la classe ; un refus la divise par deux. Un petit modèle avance à
   petits pas ; un grand modèle qui trébuche aussi.
4. **Chaque unité validée est un point de sauvegarde** : le pivot est
   sur disque, l'état (`<empreinte>.etat.json`) porte l'unité, son sceau,
   la date et le modèle, et un journal. Après une coupure, `suivant`
   repart du disque ; rien n'est à garder en mémoire
   (`prompts/reprendre.md`).
5. **Rien n'est cru sur parole** : chaque `suivant` et chaque `etat`
   rejouent les contrôles des unités validées ; un état modifié à la main
   ou un pivot abîmé après validation repasse à faire, avec une ligne de
   journal « altération détectée ». Le pivot part **pré-rempli** du texte
   machine : le modèle nettoie, il ne part jamais d'une page blanche.
6. **Ce que la machine vérifie par page** : l'ancre `[p. n]` présente et
   dans l'ordre ; la couverture du texte machine (au moins 60 %) ; la
   part de mots absents de la page (au plus 35 %) ; aucun chiffre absent
   de la page ou de ses voisines ; sur une page à figures ou sans texte,
   une ligne `[figure : …]`, `[tableau : …]` ou `[page vide]` d'au moins
   six mots ; aucune consigne de départ laissée en place. Les seuils
   vivent dans `academie.json` (`usine`), jamais dans le code.
7. **Un chiffre lu en vision** (dans une ligne `[figure]` ou
   `[tableau]`) n'est pas refusé : il est compté « à vérifier » dans
   l'état et relu par un humain ou un agent frais avant de fonder une
   carte.
8. **La fiche d'un document** est vérifiée de la même façon : champs,
   nature admise, fiabilité pas au-dessus de sa nature, aucun chiffre
   absent du pivot ; la ligne de registre se déduit de la fiche.
9. **`MODELES.md`** est l'autoportrait humble des modèles : comment se
   reconnaître dans chaque outil, les trois classes et ce qu'on leur
   confie, les épreuves publiques qui nous intéressent avec leurs
   chiffres datés, les faiblesses connues et la parade en place. Il se
   relit tous les trois mois.
10. **Un seul texte de règles, des adaptateurs muets** : `AGENTS.md` est
    canonique ; `CLAUDE.md`, `GEMINI.md`, `.agents/rules/academie.md`
    (Antigravity) et `.cursor/rules/academie.mdc` (Cursor) ne font que
    renvoyer à lui. Aucune doctrine ne vit dans un dossier d'outil.
11. **L'arrivée d'un élève** est décrite dans `COMMENCER.md` : un pseudo,
    le catalogue (`programme/catalogue.json`, un seul parcours au
    03/09/2026), « créer le vôtre » avec les prompts prêts à coller de
    `prompts/`. L'écran correspondant est le chantier
    `ACA-ONBOARDING-1`, après le client v2.
12. **Périmètre** : cette décision étend le cahier `ACA-INGESTION-1`
    à `app/usine/etat.py`, `app/usine/fiche.py`, `app/tests_usine.py`
    et à la clé `usine` d'`academie.json` (et du gabarit).

## Contexte

Le test du 03/09 a montré qu'un grand modèle lit bien une page rendue et
recopie bien un texte extrait, et qu'il perd le fil sur un long document
comme les autres. JB travaille avec Claude Code, Codex et Antigravity, sur
abonnement, avec des modèles qui changent tous les trois mois ; ses
collègues et amis arriveront avec l'outil et le modèle qu'ils ont. La
seule façon de tenir « il ne faut pas me dire de bêtises » avec un
modèle qu'on ne choisit pas, c'est de ne rien lui demander qu'une
machine ne puisse contrôler, et de le faire avancer par unités qu'il ne
dimensionne pas lui-même.

## Conséquences

- `app/usine/` (pivot, transcription, état, fiche, ligne de commande) et
  `app/tests_usine.py` ; quatre mutations dans `app/tests.py`.
- `MODELES.md`, `COMMENCER.md`, `prompts/`, `programme/catalogue.json`,
  les adaptateurs par outil ; `AGENTS.md` règle 9 ; `CONTRIBUER.md` §8 ;
  `METHODE.md` §32 ; `check.py` (fichiers requis, tirets, clé `usine`
  identique dans les deux `academie.json`).
- `chantiers/ACA-INGESTION-1.md` mis à jour ; `chantiers/ACA-ONBOARDING-1.md`
  et son item dans `roadmap.json`.

## Réouverture

Si une famille de modèles rend, sur les épreuves du §4 de `MODELES.md`,
des résultats qui rendent le pas à pas inutile pour elle (lecture longue
sans perte mesurée, zéro ajout au résumé), on relève ses plafonds
d'unités dans `academie.json`. On ne retire jamais la revérification.

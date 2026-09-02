# Dix questions qu'on aurait dû se poser, et leurs réponses (02/09/2026)

Demande de JB : « pose dix questions auxquelles on aurait dû répondre
dans tout ce travail de cadrage qu'on a oublié de faire, et fais-le ».
Chaque réponse est gravée là où elle vit (décision, document) ; ce
fichier est l'index.

## 1. Que se passe-t-il quand une carte juste devient fausse parce que la loi a changé ?

Le contrat v1 ne périme que les chiffres qui bougent ; le droit change
sans chiffre. **Réponse** : péremption par défaut à douze mois pour
toute carte `texte-officiel` ou `jurisprudence`, rapport mensuel des
cartes à revérifier, la veille de labor alimente la boîte, une carte
corrigée garde son identifiant et se re-sert en priorité.
→ [`decisions/0019`](../decisions/0019-peremption-du-droit-et-veille.md).

## 2. Comment saura-t-on que ça sert sur le terrain, pas seulement à l'écran ?

La rétention mesurée n'est pas le transfert. **Réponse** : trois
mesures. L'épreuve à froid (rétention réelle, pas performance à chaud).
La calibration (l'écart entre confiance et justesse : un pro bien
calibré sait quand vérifier). Et le rituel de sortie de réunion : trente
secondes dictées, « je n'ai pas su répondre à X », qui entrent dans la
boîte ; la fréquence de ces « je n'ai pas su » sur les sujets déjà
validés est la mesure du transfert. Bilan trimestriel dans le profil.
→ `BLUEPRINT.md` §7 (confiance), §14 ; `ARCHITECTURE.md` §4 (`points.py`).

## 3. À qui appartient la banque, et sous quelle licence ?

Sans licence, personne ne peut reprendre le dépôt ni réutiliser ce
qu'un autre a livré. **Réponse proposée** : code MIT, contenu de la
couche `banque` en CC BY-SA 4.0, couche `interne` non redistribuable,
images chacune avec sa licence. JB tranche.
→ [`decisions/0018`](../decisions/0018-licences-du-code-et-du-contenu.md).

## 4. Que se passe-t-il si le VPS meurt un mardi soir ?

**Réponse** : le client garde une copie locale du journal et de la
banque, la séance du lendemain se joue hors-ligne ; l'état est
sauvegardé chaque nuit sur le VPS et copié mensuellement sur NOIR ; un
exercice de restauration trimestriel sur dossier vide prouve que la
sauvegarde est une sauvegarde ; l'export Anki reste l'assurance-vie.
→ `ARCHITECTURE.md` §3 ; `decisions/0006`.

## 5. Et l'accessibilité : daltonisme, lecteur d'écran, dyslexie, texte agrandi ?

« Ni genre ni âge » sans « ni handicap » serait incomplet. **Réponse** :
contraste AA, jamais une information par la couleur seule, cibles de
44 px, clavier complet, étiquettes de lecteur d'écran sur l'arbre et
`image.alt` obligatoire au contrat v2, mise en page qui tient à 200 %,
mouvement réduit respecté.
→ `DIRECTION-ARTISTIQUE.md` §7 ; `CONTRAT-CARTE-V2.md`.

## 6. Faut-il rappeler le joueur, et comment sans culpabiliser ?

**Réponse** : une notification par jour au plus, opt-in, à l'heure
choisie, silencieuse si la séance est faite, formulée en fait, PWA
seulement, aucun mail de relance.
→ [`decisions/0020`](../decisions/0020-telemetrie-zero-tiers.md) §4.

## 7. Que devient l'état d'un joueur quand une carte qu'il a stabilisée est corrigée ?

**Réponse** : l'identifiant ne change pas, l'historique FSRS reste ;
si la réponse a changé, le chapitre monte de version, la carte porte
son historique, et le composeur la re-sert en priorité à ceux qui
l'avaient stabilisée. Un chapitre réécrit porte `remplace`.
→ [`decisions/0019`](../decisions/0019-peremption-du-droit-et-veille.md) §4 ; `CONTRAT-CARTE-V2.md` §3.

## 8. Qu'est-ce qu'on mesure sur les gens, et où ça va ?

**Réponse** : le journal du joueur, lisible et exportable par lui, et
rien d'autre ; aucun tiers ; les mesures produit se calculent depuis le
journal sans lire les réponses, et se lisent par JB dans un rapport.
→ [`decisions/0020`](../decisions/0020-telemetrie-zero-tiers.md).

## 9. Quel est le « pourquoi » de chaque joueur, et l'outil s'en sert-il ?

Arthur a un concours ; JB a un cap à trois-cinq ans (expert bâtiment).
**Réponse** : le profil porte un **cap** (un objectif nommé, une
échéance facultative) ; il pèse sur le neuf hors socle et sur l'ordre
des propositions ; le bilan annuel le relit et demande s'il tient.
Sans cap, le programme suffit.
→ `BLUEPRINT.md` §3 (« cap ») ; journal-v1 `cap`.

## 10. Qui valide quand personne n'est expert, et combien de temps humain ça coûte ?

JB n'est pas juriste ni comptable ; Arthur découvre sa matière.
**Réponse** : la double passe par agent frais qui remonte à la source
est obligatoire partout ; « un arrivant ne valide jamais seul une
matière qu'il découvre » ; les cartes sans source primaire portent
« à recouper » à l'écran ; le budget humain est écrit : dix minutes de
relecture par semaine pour le propriétaire du domaine, et si ça
déborde, on baisse le débit de neuf, jamais on n'étire le temps.
→ `DOCTRINE.md` §3 invariants 1 à 3 ; `gabarit-domaine/USINE.md` étape 5 ; `ROADMAP.md` garde-fous.

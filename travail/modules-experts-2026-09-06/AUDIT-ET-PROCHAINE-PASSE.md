# Contenu pour l'essai de lundi : état et candidat approfondi

Date : 06/09/2026. Outil : Codex. Modèle : GPT-6, identifiant précis non
exposé. Agent : `/root/contenu_expert`, distinct du coordinateur. Mission :
audit de contenu et préparation d'un candidat ; pas de promotion, de changement
de parcours ni de publication. Ce document est un constat de code et de fichiers,
pas une acceptation d'usage. Les chemins sont relatifs à la racine du dépôt.

## Ce qui existe localement

`python3 app/valide_chapitres.py --rapport` retourne huit chapitres, 47 cartes :
35 au statut valide et 12 brouillons. Le généré `site/banque.json`, daté du
06/09, contient 111 cartes : les 76 cartes v1 et les 35 cartes v2. Son empreinte
et les comptes par type figurent dans `inventaire-local.json`.

Les six études déclarées valides ont toutes leurs cartes présentes dans
l'artefact local :

| Étude | Cartes | Cursus |
|---|---:|---|
| Le syndic et ses missions | 5 | Copropriété |
| L'article 24 | 7 | Copropriété |
| Le procès-verbal et sa notification | 5 | Copropriété |
| Les cinq B | 5 | IFSI |
| Les transmissions orales | 5 | IFSI |
| Une rénovation rentable pour qui ? | 8 | Copropriété |

Ce constat ne prouve pas le service pour un joueur donné : les signalements de
son journal, la péremption, le cursus actif, la disponibilité des supports et
le paquet réellement publié interviennent encore. La revue du pilote du
06/09 était limitée aux pages PDF 13-22 du Focus et dit elle-même que son
niveau déclaré ne démontre pas une expertise. Le README et le rapport de
couverture antérieurs sont des photographies dépassées sur ces compteurs.

## Formats : distinguer le contrat et l'expérience

Le valideur v2 accepte 14 types. L'artefact observé en contient neuf : flash 57,
QCM 36, libre 5, photo 4, synthèse 4, rôle 2, relier 1, datation 1, plan 1.
Cela ne démontre ni neuf interfaces distinctes en Étude ni neuf formats testés
sur appareil.

- Étude présente choix, réponse textuelle et support image ; sa synthèse a
  une grille. Les interfaces rôle, relier et datation de `ModulesSeance.tsx`
  ne sont pas appelées par cet écran. Les réponses y passent dans le journal
  avec `reponse_libre` et la version du contenu.
- Séance appelle les modules spécialisés rôle, relier, datation, synthèse/cas
  et propose l'inspection d'images. Au moment du constat, son enregistrement
  ne transmet que note, confiance et durée : la réponse libre et les critères
  cochés restent locaux au composant. La promesse générale de conservation
  des réponses des formats spécialisés n'est donc pas établie par ce code.
- `cas` possède des pas dans le contrat mais Séance le rend avec le module
  de synthèse ; cela n'établit pas une simulation à embranchements.
- Dessin, feuille blanche, lecture et écoute existent dans le contrat mais
  n'ont pas de cartes servies ici ni de preuve d'un lecteur dédié dans ce constat.

Anomalies transmises au coordinateur : les valeurs de repli de Relier inventent
des fonctions de ventilation si les données manquent ; celles de Datation
inventent une procédure de recouvrement et un délai. Le module Rôle affiche
une copie réussie même après rejet du presse-papier. Ces défauts ne doivent
pas devenir des contenus pédagogiques par défaut. Le constat précède les
corrections éventuelles des autres agents ; vérifier le diff final.

## Sources : ingestion contrôlée et assertions ne se confondent pas

`python3 app/usine/usine.py etat` a donné :

| Empreinte | Pages acceptées par les contrôles de l'usine |
|---|---:|
| `0a7537d478616271`, guide copropriétés fragiles | 195/195 |
| `322a2f5e843f45b9`, Focus 106 | 32/32 |
| `707940074f138868`, cahier Angers | 54/54 |
| `8760dfb3f168df2d`, PDHH | 24/180 |
| `3a763bd084d6ee3e`, texte | 8/8 |
| `a708271c820f9311`, texte | 43/43 |
| `f34fc8af2597118f`, texte | 20/20 |
| `2b2b00b69edc0bc7`, sous-titres internes | 0/24 |

Les trois textes ne reçoivent ici aucune qualification documentaire supplémentaire :
l'identification et les droits demandent leurs fiches. Aucun contenu interne
n'est repris dans le candidat. Le présent agent n'a pas effectué la lecture
intégrale de ces documents. Pour le candidat, il a consulté le pivot du Focus
aux pages 14-18 après le verdict d'état, ainsi que le rapport indépendant
`travail/pilote-renovation-10p/RELECTURE.md`. Aucune nouvelle fermeture d'unité
ni nouvelle validation de fiche n'est revendiquée.

Le pivot du guide fragile montre pourquoi une extraction intégrale n'autorise
pas la promotion automatique d'un chapitre : aux pages 8, 16 et 22, la figure
est résumée par une ligne générique sans transcription de tous ses libellés.
Les sceaux de couverture ne prouvent pas que ces schémas ont été décodés.

## Brouillon fragile : défauts factuels à reprendre avant service

Le fichier `chapitres/satellites/coproprietes-fragiles.json` reste brouillon.
Ce statut doit être conservé jusqu'à correction et relecture distincte.
Comparaison ponctuelle contre le pivot du guide, pas expertise juridique :

- Page 10 : la source énumère gouvernance, finances, bâti, puis solvabilité
  et situation sociale. Le chapitre enseigne trois piliers et fait disparaître
  cette quatrième dimension.
- Page 16 : la source précise qu'une difficulté ne condamne pas la copropriété
  à être en difficulté. La leçon affirme un entraînement mécanique des autres
  axes et une vigilance prédit l'échec certain d'un plan uniquement comptable.
- Page 12 : la source refuse de déduire les difficultés du seul niveau
  socioéconomique, de la localisation ou de l'époque constructive. La carte
  attribue à cette page une description des petits immeubles anciens sans
  syndic et la leçon un seuil de taille, non établis par le passage consulté.
- L'amorce exclut une voie judiciaire à partir d'informations fictives
  insuffisantes. Les seuils, délais, fonds travaux et effets de l'administration
  provisoire sont formulés sans texte primaire précis et actuel. Les pages
  citées et la page d'accueil de l'Anah ne constituent pas cette vérification.
- Les recommandations de recouvrement opposent bonne foi et négligence sans
  pièces permettant cette qualification. L'exercice doit demander des
  informations et des décisions conditionnelles, sans inventer une intention.

Ces exemples suffisent à réfuter une promotion fondée seulement sur les
195 pages acceptées par l'usine. Ils ne constituent pas une revue exhaustive.

## Candidat concret préparé

`contre-expertise-renovation.brouillon.json` est hors de `chapitres/` : il ne
peut pas entrer dans le générateur par ce chemin. Il contient une leçon de
3 959 caractères, huit exercices et une synthèse transversale. Sept types :
flash, QCM, photo, relier, libre, rôle et synthèse. Il réutilise un schéma
original déjà présent, sans redistribuer une figure du PDF.

Le résultat attendu dépasse le rappel de vocabulaire : classer les pièces,
comparer des périmètres, proposer une preuve discriminante, défendre un avis
face à une objection puis le réviser sur information nouvelle. Les scénarios
A/B et C/D sont explicitement fictifs, sans chiffre de performance inventé.
Les arguments pédagogiques suivent METHODE §§2-6, 17-18 et 38 ; aucun nouveau
gain scientifique ou mécanisme n'est revendiqué. La rétention différée et
le transfert restent à mesurer séparément.

L'objet et ses cartes restent `brouillon`, sans `verifie_par`. La date du
champ obligatoire `verifie` est la date de préparation et de confrontation
au pivot, pas une relecture indépendante. Le valideur de contrat retourne
zéro erreur pour cet objet. La validation formelle ne certifie pas son fond.

Pour son intégration : revue indépendante des questions, corrigés et pages
14-18 ; contrôle du schéma chargé ; traitement du type Relier sans données
inventées ; examen du comportement rôle et des réponses sauvegardées dans
le parcours choisi ; puis promotion et ajout au parcours par l'intégrateur.
La présence d'un rôle et d'un appariement dans le JSON ne garantit pas leur
interface spécialisée en Étude.

## Prochaines fabrications proposées

| Module | Production observable | Sources disponibles et travail restant |
|---|---|---|
| Défendre puis réviser un avis de rénovation | Note comparative contradictoire, pièce discriminante, trace de révision | Candidat préparé ; Focus p. 14-18, relecture indépendante restante |
| Fragilité : du signal au diagnostic partagé | Dossier fictif croisant les quatre dimensions, questions à chaque acteur, priorisation conditionnelle | Guide de 195 pages ingéré ; reconstruire le brouillon sur passages précis, inspecter les schémas, vérifier tout seuil judiciaire contre texte primaire |
| Façade ancienne : observer avant de prescrire | Description de relevé fictif, hypothèses concurrentes, question technique et compatibilité patrimoniale | Cahier Angers ingéré ; choisir les passages distribués/scellés, observer leurs figures, distinguer recommandation historique et règlement actuel, ajouter une source technique indépendante |

Lundi, privilégier un parcours permettant de réellement produire ces notes
et de retrouver la tentative après déconnexion. Le volume des PDF récupérés
ne remplace ni ces productions ni la qualité des retours.

## Vérifications de cette passe

- Contrat du candidat via `valide_chapitres.valide_chapitre` : zéro erreur.
- `python3 app/valide_chapitres.py --rapport` : sortie 0, comptes ci-dessus.
- `python3 app/tests.py` : une suite serveur d'état échoue au bind de socket
  (`PermissionError: Operation not permitted`) dans le sandbox. Les autres
  suites affichées passent ; ce résultat n'est pas présenté comme vert global.
- `python3 tooling/check.py` : résultat reporté dans `CONTROLES.md` après exécution.

Aucun code, parcours, statut existant ni état joueur modifié par cet agent.
Les commandes d'état de l'usine rejouent ses contrôles et peuvent persister
leur journal ; aucun état documentaire n'a été réécrit à la main.

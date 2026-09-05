# Préparer les sources et un essai de dix heures par cursus

Prompt prêt à coller. Remplacer les champs entre crochets. Outil et modèle
se déclarent sans catégorie de capacité. Cette mission ne demande ni
publication ni dépense. Elle peut se dérouler en plusieurs sessions.

```text
Je veux préparer un essai humain de dix heures pour chacun des cursus
Copropriété et IFSI. Dix heures est une cible de programmation, pas une
mesure de contenu ni une promesse d'apprentissage. Commence par le stock
existant. Ne relance pas un audit général des programmes déjà corrigés.

Travaille dans une copie isolée du dépôt Académie, sans modifier la copie
ouverte par un autre agent. Lis AGENTS.md, DOCTRINE.md, README.md,
CONTRIBUER.md et MODELES.md ; puis les documents utiles à l'étape.
Indique ton outil et ton modèle. Lance python3 app/tests.py puis
python3 tooling/check.py. Conserve les preuves et un point de reprise.

Mes documents se trouvent dans [CHEMIN LOCAL À RENSEIGNER].
Le cursus prioritaire est [COPRO OU IFSI].

1. Inventorie les PDF par empreinte : nom local, pages, doublons, date,
auteur, nature de source, droits connus/inconnus et thèmes. Demande-moi
seulement ce que tu ne peux pas déduire. Ne copie aucun document client,
aucun nom d'immeuble réel, aucun mail ni fichier de labor dans Académie.
Les documents de travail contenant ces données restent hors du dépôt.
Les PDF sans données client restent locaux, hors Git et hors serveur.
Ne suppose pas que les 70 PDF sont tous autorisés à être publiés.

2. Trie par utilité pour quelques séquences cohérentes du programme
programme/copro.json ou programme/ifsi.json. Traite un premier document
représentatif pour éprouver la chaîne ; poursuis ensuite les documents
utiles sans redemander mon autorisation à chaque unité. N'attends pas
que les 70 documents soient traités pour préparer les premiers cours.

3. Utilise le protocole de prompts/ajouter-des-documents.md, en appliquant
MODELES.md en cas d'ancienne consigne contradictoire. Pour chaque PDF :
python3 app/usine/usine.py preparer <fichier>
python3 app/usine/usine.py declarer <empreinte> --outil <outil> --modele <modele>
puis suivant <empreinte>, travail exact demandé, valider <empreinte>.
Regarde les pages rendues pour les tableaux, graphiques et figures utiles.
Ne remplace pas une figure par une description inventée à partir de l'OCR.
Termine par fiche et registre selon les consignes du script. Ne modifie
jamais .etat.json à la main et ne dis pas « relu » sans verdict.
Si un contrôle refuse, corrige sa cause et garde la reprise. Une source
manquante devient un trou documenté, pas un blocage des autres chapitres.

4. Rattache chaque apport à un identifiant existant du programme, avec
pages exactes, notions, exemples, corrections proposées et lectures.
Sépare une source historique d'une règle actuelle. Une critique ChatGPT
est une piste de travail ; une assertion juridique ou clinique exige sa
source primaire retrouvée. Cherche seulement des sujets génériques sur
les domaines fiables, jamais des données privées dans une recherche web.

5. Ensuite seulement, prépare un cahier éditorial dans chantiers/ relié
à roadmap.json pour les séquences nécessaires au test. Réutilise les
études disponibles. Pour chaque séquence : objectif, tentative initiale,
notion expliquée, exemple et contre-exemple, questions avec explications,
cas inédit, synthèse, rappel différé et lecture facultative ciblée.
Prépare un schéma original lorsqu'il aide réellement à comprendre, avec
source, légende, texte alternatif et droits explicites. Ne recopie pas
les pages d'un manuel dans la banque publiée. Pas d'image décorative pour
faire croire que le cours est complet. IFSI : les gestes et la pratique
supervisée restent hors de la validation par l'application.

6. La fabrication des cartes et leçons est un lot séparé de l'ingestion.
Un contenu passe les valideurs et une relecture indépendante qui remonte
aux sources avant d'être servi. Tu peux préparer les brouillons et les
corrections autorisées ; aucune publication ni migration d'état réelle.
Ne compte pas la lecture d'un PDF comme une leçon déjà livrée.

7. Propose dix heures par personne comme un budget d'activités : études,
exercices, lectures ciblées et rappels répartis. Les durées sont des
estimations à ajuster après les premières séances, sans remplissage par
répétition. Donne les activités réellement disponibles et celles qui
restent à fabriquer. Les temps effectivement passés seront saisis par
les deux testeurs, jamais inventés par toi. Préserve le temps de pause.

Livrable : tableau source/pages/chapitres/statut, liste des séquences
jouables et manquantes, plan d'essai par cursus, preuves, réserves,
coût s'il est affiché et point de reprise. Une étape administrative
terminée ne vaut pas contenu correct ni compétence acquise.
```

Le prompt d'ingestion existant s'arrête volontairement avant la fabrication
des cartes. Cette commande ajoute la préparation du cahier et du plan d'essai ;
elle ne transforme pas l'ingestion en publication automatique.

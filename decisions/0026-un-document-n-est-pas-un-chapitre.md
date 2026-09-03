# 0026, Un document n'est pas un chapitre : la bibliothèque, le pivot, l'abonnement d'abord

- Statut : acceptée
- Date : 03/09/2026
- Décideur : agent, sur les questions de JB (« ça se trouve les docs ne
  viennent pas dans le programme mais à côté ? », « PDF to quoi ? »,
  « les images, les schémas ? », « périmé ? », « quels textes restent en
  lecture ? », « dispo depuis l'app ? », « moi j'utilise des
  abonnements, jamais d'API »), après le test d'ingestion du 03/09
  (`travail/2026-09-03-test-ingestion.md`)

## Décision

1. **Un document est une source, pas un chapitre.** Il entre dans la
   **bibliothèque** du domaine (`sources/`, hors git, avec sa ligne de
   registre) et nourrit l'arbre par quatre voies, jamais en dictant
   l'ordre du programme : (a) une **contribution** à un chapitre
   existant (un fait, un exemple, un schéma décrit) ; (b) une
   **lecture** (type `lecture` : le document, ou un extrait, lu avec sa
   méthode, niveaux III à V) ; (c) un **satellite** quand il couvre un
   sujet que le programme n'a pas ; (d) une **correction** quand il
   contredit un chapitre. Le programme reste la colonne vertébrale.
2. **Le pivot est le Markdown par page.** Un document lu devient
   `sources/<empreinte>.md` : le texte par page avec des ancres
   `[p. n]`, les titres reconstitués, les tableaux en tableaux, et
   chaque figure décrite en une phrase à sa place ; à côté,
   `sources/<empreinte>.figures/` garde les pages à figures rendues en
   image, et la ligne de registre porte la nature, la date d'édition,
   la période de validité et la licence. Les chapitres citent le pivot
   avec sa page. Le PDF d'origine n'est jamais la matière de travail
   d'un agent, seulement sa preuve.
3. **L'outillage est local et libre** : `pdftotext -layout` pour le
   texte, `pdftohtml -xml` pour retrouver les titres par taille de
   police, `pdftoppm` pour rendre en image les pages à figures,
   `pdfimages` pour compter les images. Le modèle lit les pages rendues
   en vision. Aucun service tiers, aucune bibliothèque AGPL dans le
   produit.
4. **L'abonnement d'abord, l'API jamais requise.** L'usine tourne dans
   Claude Code (ou Codex) sur l'abonnement du joueur : lire un PDF
   rendu, chercher, écrire, relire. Les coûts en tokens sont mesurés et
   écrits à titre indicatif pour qui n'a pas d'abonnement ; aucune clé
   d'API n'est nécessaire à rien. NotebookLM et ses semblables sont des
   **pré-digesteurs cités** : bons pour trouver dans quel document
   chercher, jamais une source.
5. **Les images** : trois étages (`decisions/0017`) plus une règle
   nouvelle vérifiée sur pièce : un dessin du **domaine public** (les
   planches de Viollet-le-Duc reproduites dans un cahier public) se
   réutilise ; un dessin ou une photo d'une agence, d'une association ou
   d'un éditeur ne se réutilise jamais, on le décrit et on le redessine.
6. **Le périmé** : la ligne de registre porte la date d'édition et la
   période de validité ; un chapitre qui cite un chiffre du document
   hérite d'une péremption ; un rapport à période close (un plan
   2020-2025) reste une source de méthode, plus une source de chiffres.
7. **Ce qui reste en lecture intégrale** : les textes officiels courts,
   les arrêts, les fiches-conseil et les encadrés de doctrine, parce que
   la méthode de lecture est la compétence. **Ce qu'on abrège** : les
   rapports de politique publique, en un résumé de deux pages avec les
   chiffres datés. **Ce qu'on coupe** : ce qui est hors métier, dit
   dans la ligne de registre (« on n'en tire pas »).
8. **Le document depuis l'app** : la ligne source d'une carte mène à la
   page officielle du document ; le produit n'héberge un document que
   s'il est sous licence ouverte (Licence Ouverte, Creative Commons) ou
   si son éditeur l'autorise ; le pivot Markdown d'un document public
   peut être servi en lecture, avec sa page et sa licence. Un document
   interne n'est jamais servi, même à son propriétaire, depuis le
   serveur : il reste sur sa machine.
9. **Une formation interne transcrite** est un support interne : elle
   donne une couche `interne` pour son seul propriétaire, jamais un
   contenu partagé ; la transcription et les noms qu'elle porte ne
   quittent jamais `sources/interne/`. Une notion générique qu'elle
   contient (l'accès en ligne obligatoire d'une copropriété) va au
   chapitre public, avec une source publique.

## Contexte

Le test du 03/09 sur trois PDF publics (un cahier de recommandations
patrimoniales A3 de 54 pages à 912 images, un rapport économique de 32
pages à figures vectorielles, un plan départemental de 180 pages) et une
transcription de formation interne a montré : le texte s'extrait en
moins d'une seconde par document, les titres se retrouvent par taille
de police, les pages à figures se lisent très bien en vision, et le
document le plus riche pour l'arbre (le cahier patrimonial) est aussi
celui dont les images ne sont pas réutilisables. JB n'utilise pas
d'API : l'usine doit tourner sur un abonnement.

## Conséquences

- `gabarit-domaine/USINE.md` étape 1 et 4 : le pivot Markdown, les
  outils, la lecture en vision.
- Chantier `ACA-INGESTION-1` et son cahier.
- `sources/README.md` : le pivot et les figures.
- `decisions/0017` : la règle du domaine public s'y ajoute.

## Réouverture

Si un outil libre d'extraction structurée (mise en page, tableaux,
figures) devient plus fiable que le trio poppler plus vision, on le
prend, licence lue.

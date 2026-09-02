# 0017, Images en trois étages, audio plus tard

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« générer des voix c'est plus si cher », « trouver les
  photos en étant sûr de montrer exactement la bonne chose » ; puis :
  « ça me semble plus lourd que QCM ou relier, plus tard dans la
  roadmap »)

## Décision

**Images, du plus sûr au moins sûr :**

1. **Schémas SVG maison**, dessinés d'après les descriptions textuelles
   des sources (AQC, guides) : licence maison, légende sur le schéma.
   C'est l'image de la v2 ; deux existent déjà (`banque/images/`).
2. **Photothèque de terrain** (plus tard, `ACA-MEDIA-1`) : photos prises
   en visite par les joueurs, cadrées serré sur le détail technique,
   sans adresse ni visage, étiquetées par celui qui y était et
   **confirmées par un second joueur** avant d'entrer en banque. Les
   **quêtes de terrain** (« photographie une souche de ventilation
   primaire cette semaine ») remplissent la photothèque en jouant.
3. **Images générées** : admises seulement comme illustrations, marquées
   `generee: true` et affichées comme telles ; **jamais** comme photo
   de diagnostic. Une fissure générée est fausse de façons qu'un
   débutant ne voit pas.

Wikimedia Commons reste utilisable quand la licence et la légende
tiennent (mesuré maigre le 28/08).

**Audio (plus tard, `ACA-MEDIA-1`)** : deux usages, l'**écoute** (une
situation à écouter puis décider : un copropriétaire au téléphone, un
chauffagiste qui défend son P2) et le **podcast de chapitre** (sept
minutes générées depuis la leçon validée uniquement, pour le tram mains
occupées, qui se termine par trois questions). L'audio est fabriqué chez
le propriétaire du domaine, stocké avec l'empreinte du texte qu'il lit,
jamais généré par le serveur.

## Contexte

Le verrou des images est mesuré (CORPUS §2.6 ter) : AQC inexploitable
en image, Commons maigre. Le texte à voix coûte peu en 2026. JB a
tranché : ces deux chantiers viennent après le socle du produit.

## Conséquences

- Contrat v2 : `image.generee`, type `ecoute`, champ `audio`.
- `ACA-MEDIA-1` en « plus tard » dans la roadmap, après `ACA-CONTENT-2`.
- Le principe de modalité (narration + image plutôt que texte + image)
  et l'effet de signalisation restent sourcés dans Mayer & Fiorella
  (2021), déjà au cadrage.

## Réouverture

Quand `ACA-CONTENT-2` a livré le socle en niveau 1-2, on ouvre
`ACA-MEDIA-1` par la photothèque, l'audio ensuite.

# 0009, La boîte et les chapitres satellites

- Statut : acceptée
- Date : 02/09/2026
- Décideur : JB (« un bac à sable : j'ai entendu chaudière hybride, peu
  importe où j'en suis dans le skill tree, je veux un chapitre dessus »)

## Décision

1. Le dépôt porte une **boîte** (`boite/`) : on y glisse un mot-clé, une
   URL, un PDF, une capture d'écran, un dépôt git, une vidéo, un article
   scientifique. Le contenu lourd est hors git ; `boite/JOURNAL.md`
   (versionné) trace ce qui est entré, quand, et ce que c'est devenu.
2. Un skill « glisser dans l'Académie » transforme une entrée en
   **chapitre satellite** : un chapitre `brouillon` rattaché par
   proposition à la branche la plus proche de l'arbre, avec ses sources
   et ses trous nommés. Il passe la double passe et le valideur comme
   tout chapitre.
3. **Un satellite se joue tout de suite**, quel que soit l'état de l'arbre :
   il n'a pas de prérequis bloquant, seulement des prérequis conseillés.
   Il apparaît comme un nœud en orbite de sa branche ; quand la branche
   est atteinte, il s'y rattache et compte dans son remplissage.
4. La règle du trou nommé s'applique : « chaudière hybride » sans source
   primaire donne un chapitre de niveau 1 réduit et un trou nommé
   (« à sourcer : ADEME, guide Cerema, fabricant ») ; jamais un chapitre
   inventé.

## Contexte

labor a déjà `lab/boite/` (ce que JB colle ou envoie par Telegram) et le
skill `labor-veille` à quatre verdicts. L'Académie reprend le même geste
avec un verdict de plus : « chapitre ».

## Conséquences

- `boite/README.md` décrit le geste ; `ARCHITECTURE.md` §7 décrit le
  pipeline (extraction locale : `pdftotext`, OCR, sous-titres, vision ;
  jamais de scraping de site de cours).
- La banque gagne un dossier `banque/satellites/` ; le contrat chapitre
  porte `satellite: true` et `rattachement_propose`.
- Le rattachement final est un geste humain (JB ou le propriétaire du
  domaine) : l'agent propose, l'humain confirme.
- Le programme (`PROGRAMME.md`) reste la colonne vertébrale : les
  satellites nourrissent les niveaux 3 à 5 et les branches en friche, ils
  ne remplacent pas le tronc commun.

## Réouverture

Si les satellites dépassent en nombre les chapitres du tronc dans un
domaine, c'est que le programme est en retard : on rouvre le programme.

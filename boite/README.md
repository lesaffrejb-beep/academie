# boite/ : « à glisser dans l'Académie »

Ouverte le 02/09/2026 ([`decisions/0009`](../decisions/0009-la-boite-et-les-chapitres-satellites.md)).
Même geste que `labor/lab/boite/` : ce que JB croise et veut apprendre
atterrit ici, sans se demander où ça va dans l'arbre.

## Le geste

1. **Glisser** : un mot-clé (« chaudière hybride »), une URL, un PDF, une
   capture d'écran, un dépôt git, une vidéo, un article. Depuis le
   téléphone : la file de la boîte dans l'app (texte et liens). Depuis
   le Mac : déposer le fichier ici.
2. **Une ligne dans `JOURNAL.md`**, versionnée : date, ce que c'est, où
   ça vit (fichier local, lien), et l'état.
3. **Le skill « glisser dans l'Académie »** (à écrire, chantier
   `ACA-BOITE-1`), lancé sur le Mac, déroule l'usine courte : extraction
   locale (`pdftotext`, OCR, sous-titres, vision), recherche dans
   `sources/REGISTRE.md` puis dans la liste blanche, **chapitre
   satellite** en `brouillon` dans `banque/satellites/`, trous nommés,
   rattachement proposé à la branche la plus proche du programme.
4. **Double passe, valideur**, puis le satellite apparaît sur l'arbre,
   en orbite, jouable tout de suite.
5. **Rattachement** : un geste humain (JB ou le propriétaire du domaine)
   confirme la branche ; le satellite y compte alors.

## Les états d'une entrée

`a-traiter` → `chapitre-propose` → `rattache` ; ou `ecarte` avec son
motif (pas de source fiable, hors sujet, doublon d'un chapitre
existant). Une entrée écartée reste dans le journal : c'est un trou
nommé ou une décision, jamais un oubli.

## Ce qui ne rentre pas

Un document du portefeuille, un mail, une transcription de réunion, une
donnée client. La boîte est un sas vers la banque partagée : ce qui ne
peut pas y aller passe par le rituel de sortie de réunion (« je n'ai pas
su répondre à X », trente secondes, anonyme) et devient un mot-clé.

## Fichiers

- `README.md` (ce fichier) et `JOURNAL.md` : versionnés.
- Tout le reste : hors git (`.gitignore`), copie mensuelle sur NOIR avec
  `sources/`.

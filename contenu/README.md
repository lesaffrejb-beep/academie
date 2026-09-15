# contenu/

Les textes que le produit affiche, hors banque de connaissances.
Source de vérité pour la surface de jeu : les commandes et les artefacts
d'une séance les lisent tels quels, ils ne les réécrivent pas (décision
0054 : plus de client web).

| Fichier | Ce qu'il porte | Règle |
|---|---|---|
| `voix.json` | les micro-textes par moment, avec au moins trois variantes chacun | `VOIX.md` ; `tooling/check.py` refuse exclamation, emoji, mots du jeu, tiret cadratin |
| `citations.json` | les citations des jalons : texte, auteur, œuvre, date, note d'attribution | chaque entrée a une œuvre ou une lettre identifiable ; une paraphrase se dit |

Les clés de `voix.json` sont stables : la surface les référence par nom.
Une clé nouvelle s'ajoute avec ses trois variantes ; une clé ne se
supprime pas sans un chantier qui met la surface à jour.

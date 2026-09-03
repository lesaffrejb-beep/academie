# Cahier ACA-CONTENT-2 : les lots de chapitres du socle

Résultat attendu : les domaines du socle gagnent des lots de chapitres
de niveaux 1 et 2 (leçon, amorce, cartes, synthèse) générés par le
modèle avec recherche citée sur les sources fiables, tampon de
provenance sur chaque carte, double passe par agent frais et échantillon
humain.
Fini quand, par lot : zéro carte `brouillon` restante, part des cartes
sans source retrouvée écrite, zéro chiffre sans source, zéro erreur sur
l'échantillon de JB, coût mesuré par chapitre écrit dans
`gabarit-domaine/DESSINER-LA-CARTE.md` §6.
Dépend de : ACA-CONTRAT-2, ACA-CONTENT-MAP-1, ACA-RITUAL-1.
Bloque : ACA-DOMAIN-KIT-1, ACA-MEDIA-1.

## Périmètre

Peut créer ou modifier : `chapitres/<domaine>/<branche>/*.json`,
`programme/copro.json` (statut des chapitres : `a-ecrire` → `brouillon`
→ `valide` ; rien d'autre), `sources/registre.json` et `REGISTRE.md`
(sources nouvelles), `banque/images/` (schémas SVG maison, avec
licence), `travail/lot-<domaine>-AAAA-MM-JJ.md` (le rapport du lot :
sources cherchées, trous, coût, taux de rejet de la double passe).
Ne touche pas : le moteur, les contrats, les chapitres déjà `valide`
(une correction passe par un signalement et un chantier de correction),
les identifiants.

## Déjà tranché (ne pas rouvrir)

- Un chapitre = amorce, leçon 300-800 mots, cartes, synthèse
  (`decisions/0002`, `CONTRAT-CARTE-V2.md`).
- Le modèle écrit, cherche, cite, avoue ; aucun chiffre sans source ;
  provenance sur tout (`decisions/0021`, `0022`).
- Double passe par un agent frais qui remonte à la source, avant
  `valide` ; `verifie_par` obligatoire (`gabarit-domaine/USINE.md`
  étape 5 ; le valideur le refuse sinon).
- La voix des leçons et des cartes : `VOIX.md` §6 et §7.
- Les types par niveau : `BLUEPRINT.md` §7 ; trois types au moins par
  chapitre quand la matière le permet ; le concret avant la théorie.
- Un lot = une branche entière ou dix chapitres ; jamais plus de vingt
  cartes neuves par chapitre.
- Le temps humain de JB : dix minutes par semaine, échantillon de vingt
  cartes par lot ; si ça déborde, on baisse le débit.
- Les images : schémas SVG maison seulement (`decisions/0017`).

## Étapes, dans l'ordre (par lot)

1. Ouvrir le rapport du lot avec les chapitres visés et leurs sources
   attendues (programme, liste blanche, registre).
2. Chercher et lire les sources (pdftotext pour un PDF ; jamais
   WebFetch sur un PDF) ; noter chaque source au registre.
3. Écrire les chapitres en `brouillon`, provenance renseignée, sans
   source avouée quand c'est le cas.
4. `python3 app/valide_chapitres.py` vert.
5. Double passe : un agent frais par lot, qui ne voit pas la session de
   génération, remonte à chaque source, rend un verdict par carte
   (juste, faux, à reformuler, source introuvable) ; appliquer :
   `valide` + `verifie_par`, ou correction, ou `signale`, ou retrait
   avec trou nommé.
6. Échantillon de JB : vingt cartes tirées au hasard, lues en HTML
   (jamais en JSON) ; une erreur trouvée renvoie le lot en double passe.
7. Coût et taux de rejet écrits dans le rapport et dans
   `DESSINER-LA-CARTE.md` §6 ; statuts du programme mis à jour.

## Ce qu'on ne fait pas

- Pas de carte sur un chiffre sans source primaire (les seuils de
  fissuration, par exemple, restent qualitatifs et le disent).
- Pas de recopie d'un manuel, d'une fiche AQC ni d'un support interne ;
  paraphrase et lien.
- Pas de contenu labor, pas de nom, pas de montant réel.
- Pas de chapitre de niveau 3 et plus dans ce chantier (la boîte et les
  niveaux hauts viennent après).

## Preuve

```bash
python3 app/valide_chapitres.py --rapport && python3 app/tests.py && python3 tooling/check.py
```

JB voit : le rapport du lot, ses vingt cartes en HTML, et le coût.

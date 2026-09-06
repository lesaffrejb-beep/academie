# Contre-lecture du module électrique

6 septembre 2026 — Codex / GPT-6, passe indépendante
`professeur-20260906/graphe/relecture-electricite`, distincte de l’auteur
`professeur-20260906/root/electricite`.

**Verdict final : favorable à la promotion éditoriale de cette unité bornée.**
Les réserves initiales de portée documentaire et de qualification du
différentiel ont été corrigées par l’auteur puis contrôlées dans le fichier.
Aucun tampon n’a été ajouté au brouillon par cette passe. Le fonctionnement
du client et la publication restent des preuves distinctes à fournir.

## Périmètre contrôlé

Lecture du chapitre complet, de ses sept cartes (six exercices et une
synthèse), de `LECTURE-INRS.md`, des dix pivots et de leurs verdicts usine.
Les dix empreintes des pivots correspondent à `VERDICTS-FINAUX.json`.
Ces verdicts couvrent INRS PDF 18–20 et 25–30, ainsi que Promotelec PDF 1.
Ils ne couvrent pas les pages 21–24 ni l’original INRS entier. Les deux SVG
ont été rendus avec Sharp et inspectés comme images locales ; les rendus
INRS PDF 19 et Promotelec PDF 1 ont aussi été examinés pour comparaison.

État initial du chapitre : SHA-256
`7a99b93cbcc7aeff2bbc1376b09f9a73b8d136a25e8d3428d0ae4c57284f6fac`.

## Réserves initiales corrigées

1. **P2 — Les plages de sources affichées couvrent des pages non contrôlées.**
   Remplacer les mentions continues `18–28` (chapitre et synthèse) et
   `19–27` (carte `electricite-fonctionne`). Repères précis suffisants :
   chapitre **18–20 et 25–28** ; fonctionnement **19 et 25–27** ; synthèse
   **18–19 et 25–28**. Les neuf pages lues peuvent être indiquées séparément
   dans la provenance de lecture, sans laisser croire que 29–30 étayent
   des notions non enseignées ici. Les ancres vers la première page restent
   cohérentes avec ces ensembles discontinus.
2. **P2 — La réponse `electricite-complement` qualifie tout différentiel de
   protection complémentaire contre le contact direct.** INRS PDF 25
   précise un dispositif adapté à cette fonction, de haute sensibilité.
   Sans introduire de seuil : « Un différentiel adapté peut compléter les
   protections contre le contact direct ; il n’empêche pas à lui seul le
   contact. » Conserver la suite sur isolation et enveloppes, ainsi que
   l’absence de garantie d’évitement du choc.
3. **Précision documentaire recommandée :** ajouter **PDF 27** à la source
   de `electricite-contacts`, dont la réponse emploie la définition de
   « masse ». Les PDF 18–19 étayent déjà les deux catégories de contact ;
   la note 5 du PDF 27 donne la définition exacte de la masse.

**Contrôle du delta :** toutes les plages ci-dessus ont été resserrées,
PDF 27 a été ajouté aux contacts et la réponse commence désormais par
« Un différentiel adapté peut compléter les protections contre le contact
direct ». Elle précise que sa présence seule ne rend pas une partie sous
tension accessible sans danger. Aucune réserve éditoriale restante dans
le périmètre contrôlé. SHA-256 du brouillon corrigé, avant tampon/statut :
`d7716fa6a0f0cddad3ea8d5a170e639d0e534de8f7a823db69980589d73e177e`.

## Confrontation des affirmations

| Élément | Passage contrôlé | Conclusion |
|---|---|---|
| Surcharge, court-circuit et échauffement ; causes d’incendie multiples | INRS PDF 20 et 28 | La leçon conserve les autres causes, dont les mauvais contacts. Pas de garantie universelle attribuée au disjoncteur. |
| Défaut d’isolement, courant hors trajet normal et déséquilibre détecté | INRS PDF 27 ; Promotelec PDF 1 | Mécanisme cohérent, coupure conditionnée au déclenchement. Les formulations absolues du lexique sont écartées. |
| Interrupteur différentiel / disjoncteur différentiel | INRS PDF 27–28 ; Promotelec PDF 1 | Distinction correcte dans la leçon, `electricite-appareils`, `electricite-mecanismes` et `electricite-devis`. |
| Contact direct / indirect et état normal d’une masse | INRS PDF 18–19 ; définition PDF 27, note 5 | Cas A/B cohérents. Le métal n’est pas déclaré dangereux par nature. |
| Protection empêchant le contact ; complément différentiel | INRS PDF 25–26 | Leçon correctement limitée ; réponse de la carte à qualifier comme indiqué ci-dessus. |
| Terre et coupure ; autres dispositions dont double isolation | Tableau INRS PDF 25 ; PDF 27 | Pas de terre imposée indistinctement à tout appareil. La coupure peut relever du différentiel ou de la surintensité selon la disposition. |
| Fonctionnement rapporté ne démontrant pas la sécurité | Inférence depuis INRS PDF 19 et 25–27 | Inférence identifiée comme telle, aucune citation ou règle inventée. Information manquante distinguée de protection absente. |
| Devis et synthèse fictifs | Distinctions précédentes | Demandes de pièces et avis révisable cohérents ; aucun choix de calibre, aucune opération technique ou conclusion de conformité. |

La leçon propose une progression compréhensible : phénomène, fonction,
nom complet de l’appareil, type de contact, limites, application au devis.
L’amorce précède l’explication ; les exercices mobilisent comparaison,
rappel, qualification et transfert. Le nouveau cas de synthèse change
l’entrée du dossier. Cela constitue une unité enseignable, sans prouver
la réussite d’un élève, son autonomie professionnelle ou sa rétention.
Le parcours client demeure séquentiel et autoévalué ; cette relecture ne
valide aucun professeur adaptatif automatique.

## Schémas

- `electricite-mecanismes.svg`, SHA-256
  `6e4e0b96118ef7515dac8b20a66a0cab8f77d9d46dd693834c4b7268653c114c` :
  les repères A/B et les flèches distinguent demande excessive et dérivation
  indésirable. Les fonctions de protection attendues ne sont pas écrites
  dans le dessin. La simplification sans boucle complète est explicitement
  présentée comme schéma de raisonnement, aucun câblage à reproduire.
- `electricite-contacts.svg`, SHA-256
  `657732bec15d2a1ba93efc98543c5d9ca4bb49578912ca151598048a32ae56bd` :
  les deux états de la partie touchée sont distincts, sans afficher les
  mots « direct » et « indirect » à donner. Les pointillés relient les
  objets à un cartouche « Contact ». Aucun geste réel n’est demandé.

Les rendus complets sont lisibles, sans texte coupé ni superposition
observée. Les compositions diffèrent des figures originales examinées.
Le texte alternatif conserve les données utiles sans fournir la catégorie
attendue. Rendus : `/private/tmp/relecture-electricite-mecanismes.png` et
`/private/tmp/relecture-electricite-contacts.png`. La lisibilité dans le
client mobile et le chargement des supports restent à vérifier par l’auteur.

## Signature structurée proposée — delta contrôlé

Cette proposition identifie la passe et peut accompagner la promotion du
contenu corrigé. `assertions` et `sources` sont à réduire
au périmètre de chaque carte si le tampon y est copié.

```json
{
  "outil": "Codex",
  "modele": "GPT-6 (identifiant précis non exposé)",
  "session": "professeur-20260906/graphe/relecture-electricite",
  "date": "2026-09-06",
  "rapport": "travail/preuve-concrete-2026-09-06/RELECTURE-ELECTRICITE.md",
  "assertions": [
    "Distinctions surintensité, défaut d’isolement et fonctions des appareils confrontées aux passages contrôlés.",
    "Contacts direct et indirect, dispositions de protection et limites de l’inférence documentaire contrôlés.",
    "Deux SVG originaux rendus et inspectés ; aucune procédure de câblage ou garantie universelle enseignée."
  ],
  "sources": [
    "INRS ED 6345 (2019), PDF 18–20 et 25–28 ; lecture usine partielle 18–20 et 25–30, original non intégralement relu.",
    "Promotelec, lexique de l’installation électrique, PDF 1 ; vocabulaire corroboré, formulations absolues écartées."
  ]
}
```

Aucun contenu, SVG ou état usine modifié. Aucun test global, navigateur ou
déploiement exécuté pendant cette contre-lecture.

## Observation distincte sur le professeur adaptatif

CHEMINS.md, son prompt, METHODE.md §39 et décision 0051 définissent un
protocole d’agent cohérent avec les acquis inconnus et l’autoévaluation
actuelle. Après signalement, CHEMINS.md précise que le choix du chemin
s’effectue en conversation et que le client reste séquentiel. Le dossier
`chemin-electricite.json` propose désormais deux suites distinctes :
réussite vers `avis`, difficulté vers `mecanismes` puis `avis`. Ce sont
des propositions de chemin, pas des bifurcations exécutées par le client.
La divergence du contrôle de fraîcheur juridique dans `_servie` a été
signalée à l’auteur du script ; sa correction n’entre pas dans le présent
verdict éditorial sur l’électricité.

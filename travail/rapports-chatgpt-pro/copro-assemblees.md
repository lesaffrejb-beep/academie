# Copro : assemblées, note de reprise inachevée

**Reprise pour publication autorisée le 04/09/2026.** Les cinq retouches
v1 (passerelle et quatre cartes de notification) ont été contre-lues
par l’agent principal, qui ne les a pas écrites, contre les textes
24, 25-1, 42-1 et 64 à 64-2 réouverts : pas de réserve sur ces retouches.
Les contrats sont contrôlés par `app/tests.py`. La suite du document
conserve le point historique : **arrêt demandé par JB le 04/09/2026.** Les retouches sont écrites ; la
note complète et leur relecture indépendante restent à terminer. Auteur
des retouches : Codex / gpt-5.6-sol, agent `revue_pedagogique_ifsi`.

Fichiers : `banque/droit/majorites.json` (explication du distracteur de
la passerelle), `banque/droit/veille-recente.json` (notifications),
`chapitres/droit/majorites/l-article-24.json` (objectif, leçon, synthèse,
cinq cartes intégrées et sources). Les statuts et identifiants sont
conservés ; le chapitre et ses cartes restent brouillons.

Le rapport de recherche avait confirmé les références ci-dessous ;
elles servent à la relecture des modifications, pas à la présumer faite.

| Point à contrôler | Source primaire consultée pendant la recherche |
|---|---|
| Article 24 : voix exprimées, abstentions exclues | [Article 24 actuel](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000051749514) ; [version 2000](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006471772/2000-12-14) contient déjà « exprimées », donc la chronologie « depuis 2020 » du brouillon était fausse. |
| Désignation du conseil syndical | [Article 25 c](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000051749507/2026-03-10), avec passerelle seulement sous conditions. |
| Pouvoirs et cumul de voix | [Article 22](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039313531) : trois délégations, au-delà plafond de 10 % incluant voix propres et déléguées ; exception syndicat secondaire. |
| Passerelles distinctes | [25-1](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049398359), [26-1](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039313602/2026-05-16). Vérifier seuils, nature des travaux et absence de généralisation du second alinéa de 25-1. |
| Notification : loi et modalités | [42-1](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049398877), [décret 2025](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053159903), articles [64](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053191373), [64-1](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053191378), [64-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053191386) et [64-4](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000053191398/2026-05-12). Distinguer loi 2024, modalités 2025, rappel du choix postal et notification formelle. |
| Catégories à porter au PV | [Article 17 du décret](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000042078689/2026-04-15) : opposants, abstentionnistes et assimilés défaillants avec noms et voix. |
| Petites copropriétés et syndicats à deux | [41-8](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039301997), [41-9](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000039302004), [41-10](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039302006), [41-13 et suivants](https://www.legifrance.gouv.fr/codes/section_lc/JORFTEXT000000880200/LEGISCTA000039301950/2026-05-02). Distinguer nombre de lots et nombre de copropriétaires. |

À compléter : table avant/après des cartes effectivement changées,
cas contradictoires de calcul et verdict de relecture indépendante.
Le script et le témoin existent dans les fichiers temporaires
`/tmp/academie-copro-assemblees-{corrige.py,controles.py,avant.json}` ;
contrôle rouge de sept défauts dans
`/tmp/academie-copro-assemblees-rouge.log`. Ils sont inclus dans la
sauvegarde de pause. Ne pas réexécuter un script de correction sur une
version déjà modifiée sans comparaison préalable.

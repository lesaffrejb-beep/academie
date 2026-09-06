# Relecture indépendante bornée : inventaire, vente, ASL et SCI

Relecteur : Codex / GPT-6 / cours-copro-20260906/graphe.
Date : 6 septembre 2026. Auteur des textes examinés : agent racine.
Cette revue ne porte pas sur les 93 chapitres rédigés par le relecteur.

## Périmètre et verdict

Lecture complète de `app/cours_copro.py`, `app/tests_cours_copro.py`, des cinq
sections de `cours/copro/immobilier/vente.md` et des deux sections ASL/AFUL/
volumes/copropriété horizontale et SCI dans `immobilier/acteurs-et-formes.md`.
Registre immobilier consulté pour les références correspondantes.

Verdict : pas de contradiction juridique impactante retrouvée dans les
sept sections examinées après confrontation bornée aux textes ci-dessous.
Acceptables comme brouillons éditoriaux. Une défaillance reproductible de
l'indexation d'un registre invalide a été corrigée avec test rouge puis vert.
Aucune validation globale des 389 cours, aucune qualification professionnelle,
aucune lecture intégrale de tous les codes ou diagnostics n'est prononcée.

## Code : anomalie reproduite et correction

`controle` signalait correctement un registre de sources JSON invalide ou
sans métadonnées. `indexer` le relisait sans garde pour produire SOURCES.md,
après avoir déjà écrit INDEX.md et INVENTAIRE.json. Deux entrées de test
(`{` et une source réduite à son identifiant) reproduisent JSONDecodeError
et KeyError. Cela interrompait la génération au lieu de rendre l'erreur
consultable.

Correction minimale : le rendu bibliographique repère l'erreur de registre
produite par le contrôle et émet « Registre invalide » avec le chemin et le
renvoi à l'inventaire. Aucune source de ce registre n'est présentée comme
contrôlée. Les textes originaux sont inchangés, les erreurs de contrôle
persistent et le code de sortie de la commande reste non nul.

Preuve : `python3 -m unittest discover -s app -p tests_cours_copro.py` :
12 tests, échec initial avec les deux exceptions, puis 12/12 réussis après
correction. Les tests préexistants couvrent présence, doublon, identifiant,
références, auteur/statut, image, date, compléments séparés et tableau JB.
Aucune suite globale ni indexation du corpus partagé exécutée par ce relecteur.

Limites constatées : le repérage du cas, du transfert et de l'ancrage est
lexical, la longueur n'est pas une preuve de profondeur, le contrôle des
références vérifie la déclaration et l'existence sans visiter les URL ni
prouver la lecture. Les paragraphes répétés sont détectés à l'identique,
pas par paraphrase. Ces limites sont compatibles avec la formulation du
résultat qui refuse une validation de fond. L'index est un document local,
pas une transaction atomique de publication ; les modifications concurrentes
du corpus entre contrôle et rendu ne sont pas traitées comme une garantie.

## Vente : confrontation précise

- [Article 5 du décret de 1967](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000053191253),
  corps intégral relu, version depuis le 25 décembre 2025 : trois parties,
  approximations sous réserve d'apurement, cautionnement et annexe. Le cours
  distingue correctement l'information de l'état daté et la créance liquide
  et exigible susceptible d'opposition.
- [Décret de 1967, articles 5-1, 6, 6-2 et 6-3](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000305770/),
  passages effectivement relus : notification distincte de l'avis, provision
  budget, hors budget selon exigibilité et régularisation selon approbation.
  Les conventions vendeur/acquéreur ne remplacent pas l'imputation syndicale.
- [Loi de 1965, article 20](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000880200/),
  passage déjà consulté pendant le lot droit et réutilisé avec son périmètre
  connu : opposition au prix et contrôle préalable de l'acquéreur distingués.
  Le calcul fictif 2 000 + 1 500 − 400 = 3 100 est cohérent avec les hypothèses ;
  l'appel futur n'est pas rendu exigible par la vente.
- [DILA, état daté](https://www.service-public.gouv.fr/particuliers/vosdroits/F37294),
  page vérifiée le 18 février 2026, rubriques contenu et prix effectivement
  relues : plafond de 380 euros TTC et absence de multiplication pour lots
  vendus simultanément correctement rapportés. Aucun forfait imposé inventé.

Limites pédagogiques maintenues : le chapitre diagnostics enseigne surtout
la différence d'objet et de périmètre ; il ne fournit pas une liste exhaustive
ni les durées de validité. La réponse ministérielle de 2014 n'est pas traitée
comme état actuel exhaustif. Le cours ne constitue pas un formulaire d'acte
ni un calcul complet de computation de délai. Ce sont des limites nommées,
pas une preuve que tous les documents applicables ont été vérifiés.

## ASL, AFUL et SCI : confrontation précise

[Ordonnance du 1er juillet 2004](https://www.legifrance.gouv.fr/loda/id/JORFTEXT000000623191/),
articles 1 à 9 effectivement ouverts et relus, état au 6 septembre 2026 :
personne morale privée, droits et obligations attachés aux immeubles,
statuts/périmètre/financement, formalités et organes. Le cours évite justement
l'importation automatique des majorités de copropriété et la confusion des
patrimoines ; le cas de voie entre deux syndicats reste cohérent.

[Article L322-1 du Code de l'urbanisme](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006815268/)
intégralement ouvert et relu, version depuis juillet 2004 : rattachement des
AFU à l'ordonnance et dispositions spécifiques. La portée générale affirmée
est correcte. Le registre auteur indiquait une lecture indexée ; la présente
revue apporte une lecture du corps officiel, sans prétendre couvrir tous
les régimes AFUL ou les conditions d'une opération particulière.

[Article 1849 du Code civil](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000006444285/)
intégralement ouvert et relu, version depuis juillet 1978 : objet social,
pluralité de gérants et limites statutaires envers les tiers. Le cours
sépare correctement société propriétaire, associé, gérant, occupant et
payeur. Il ne crée pas un recours personnel automatique contre l'associé.

La division en volumes est examinée comme concept et interface ; la source
notariale ancienne n'a pas été relue intégralement dans cette revue. Aucun
montage concret n'est qualifié à partir de cette seule présentation. Les
statuts particuliers, jurisprudences de capacité, régularisation d'une ASL
et recours contre associés restent à approfondir.

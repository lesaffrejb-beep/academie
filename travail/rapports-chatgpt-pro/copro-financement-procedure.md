# Copro : financement et procédure

Contrôle ciblé du 04/09/2026. Auteur des retouches : Codex / gpt-5.6-sol,
agent principal. Recherche primaire indépendante : agent
`verifie_rapport_strategie`. Le rapport LLM sert de piste ; les liens
ci-dessous fondent les corrections. Le JSON `copro-corrections.json`
conserve les formulations avant/après et les identifiants exacts.

## Financement

| Assertion initiale | Règle, champ et source contrôlée | Traitement |
|---|---|---|
| Fonds ramené à « cinq pour cent » et confondu avec l'article 14-2 | [Article 14-2-1](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000043967792) : immeubles totalement ou partiellement d'habitation, dix ans après réception ; sans PPT adopté, minimum 5 % du budget ; avec PPT adopté, respect des deux minima 5 % du budget et 2,5 % des travaux du plan. | Les trois chapitres du fonds distinguent champ, adoption, double plancher et affectation. Article 14-2 reste le texte du PPT. |
| Suspension présentée dans la carte comme fonds supérieur au budget OU à 50 % du plan | Même article, II : dépassement du budget et, avec PPT adopté, **en outre** dépassement de 50 % des travaux ; l'assemblée se prononce, la suspension n'est pas automatique. | Carte `droit-conformite-fonds-travaux-plancher` corrigée dans `conformite-annuelle.json`. La fiche Service Public consultée donne un « ou » contradictoire : retenir ici le texte législatif. |
| Seul emprunt à adhésion individuelle décrit | [Article 26-4](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000049398702/2026-01-07) et [décret du 22/12/2025](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000053159903) : coexistence des régimes. Le III présume l'adhésion pour les travaux qu'il vise ; refus notifié sous deux mois et paiement intégral de la quote-part sous six mois, depuis notification du PV. | Objectifs des deux chapitres existants élargis à la distinction des régimes et de leur champ. Le titre historique reste stable. Aucun emprunt nouveau ni fiche contractuelle complète n'est créé. |

Cas contradictoires, purement fictifs : budget 100 000 €, travaux du PPT
400 000 € donnent des minima 5 000 € et 10 000 €, donc 10 000 € de
cotisation annuelle minimale. Avec budget 300 000 € et même PPT,
le maximum devient 15 000 €. Sans plan adopté, le second plancher ne
s'applique pas. Pour budget 100 000 €, PPT 400 000 €, fonds 150 000 €,
le dépassement du budget seul ne remplit pas les deux conditions de
suspension ; à 210 000 €, elles sont réunies et l'AG doit se prononcer.
L'égalité exacte aux seuils ne vaut pas dépassement.

## Procédure

| Assertion initiale | Règle, champ et source contrôlée | Traitement |
|---|---|---|
| « Dix mille euros » isolé pour dire quand l'avocat est obligatoire | [CPC article 761](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000051869371), à lire avec l'article 760 : représentation de principe devant le tribunal judiciaire, dispenses selon matière et procédure, réserve des compétences exclusives. | Le chapitre demande d'identifier juridiction, matière et procédure avant d'appliquer le seuil. Aucun calcul de représentation réduit au montant. |
| « Inscrire l'hypothèque légale du syndicat et expliquer le privilège » | [Article 19](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000039313565), [article 19-1](https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000044073475) et [Code civil 2402](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000044072139/2026-05-19) : distinguer hypothèque inscrite et hypothèque légale spéciale ; ancien privilège situé historiquement, renvoi actualisé depuis 2022. | Capacité et notions corrigées, titre et identifiant historique conservés. Le gestionnaire identifie la garantie et le professionnel à mobiliser ; aucun acte d'inscription produit. |

Contre-exemple de méthode : une demande de faible montant ne suffit pas
à conclure à une dispense d'avocat. Il faut d'abord connaître la matière,
la compétence et la procédure ; sans ces données, la réponse reste ouverte.

## Limites

La banque contient déjà une carte comptable correcte sur le double
plancher (`comptabilite-annexes-et-anomalies-fonds-travaux-double-plancher`).
Elle reste intacte. Aucun défaut de carte servie n'a été repéré pour
l'emprunt, l'avocat et l'hypothèque dans ce lot : leurs corrections portent
sur l'inventaire. Cette note ne certifie pas toutes les procédures.

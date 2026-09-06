# Relecture indépendante du pilote rénovation : dix pages

Date : 06/09/2026. Outil : Codex. Modèle : identifiant non exposé dans cet
agent. Session de revue : `/root/revue_pipeline`, lot
`pilote-renovation-10p-revue-20260906`. Le relecteur n'a écrit ni le chapitre
ni les schémas et ne les a pas modifiés.

## Verdict et périmètre

**Aucun bloquant factuel identifié pour ce chapitre de lecture critique.**
Avis favorable à son passage à la validation de contenu, sous réserve des
contrôles de contrat et du fonctionnement réel effectués séparément par
l'agent intégrateur. Cet avis n'est ni un verdict de publication, ni une
preuve de fonctionnement du client, ni une certification d'expertise.

Le chapitre a été examiné en statut `brouillon` : amorce, leçon, synthèse,
huit cartes, réponses, distracteurs, explications et métadonnées d'images.
Les trois fichiers SVG ont été examinés dans leur source pour leurs textes,
relations et caractère original ; leur rendu mobile et ordinateur n'a pas
été testé par cette revue.

Retour à la source : les dix rendus complets des pages PDF 13 à 22 ont été
inspectés, puis les passages correspondants du pivot ont été confrontés.
Le document est le Focus 106, juin 2024, pas un référentiel financier ou
technique actuel. Aucun contrôle externe de ses références secondaires ni
de la réglementation en vigueur n'est revendiqué.

Commande d'état exécutée :

```sh
python3 app/usine/usine.py etat 322a2f5e843f45b9
```

Résultat observé : `32/32 page(s) relues`, quatre unités, dernier événement
« fiche validée ». C'est l'état du document dans l'usine, pas une déclaration
que ce relecteur aurait personnellement revu ses 32 pages. La présente
revue porte seulement sur les pages 13-22 et leurs usages dans le pilote.

## Assertions confrontées aux pages originales

| Objet contrôlé | Preuve et conclusion |
|---|---|
| Perspectives, valeur privée et trésorerie | P. 14, décomposition en économies monétaires, confort et capitalisation ; p. 19-20, paradigmes privé/social et variante santé. La distinction pédagogique entre valorisation économique et encaissement est appropriée. Aucun versement n'est inventé. |
| Crédit à 5 % du revenu annuel | P. 15 : refus de crédit modélisé selon l'annuité de remboursement et hypothèse demandant encore un étayage empirique. La carte ne transforme pas ce seuil en règle bancaire, taux d'intérêt ou droit au crédit. |
| Frictions de 18 000 € et 14 000 € | P. 15-16 : coûts implicites calibrés, frictions additives pour les bailleurs d'appartements. Somme 32 000 € correcte. Le corrigé refuse leur ajout automatique au devis. |
| Représentation statistique | P. 17 : segments croisant logement, propriétaire et occupant ; base historique 2018 et limites des données. La leçon ne présente pas le modèle comme une visite du bâtiment. |
| Exclusions techniques | P. 18, corps et note 18 : coûts induits, VMC, contraintes architecturales et nuisances sonores ignorés par la représentation. Le chapitre demande une vérification propre au projet et n'autorise pas la suppression de ventilation ni une installation de PAC. |
| Rangs privés et sociaux | P. 20, encadré 3 : ordonnancements pouvant différer ; p. 21, figure 8 : identité des segments conservée et courbe privée en dents de scie. Le corrigé et la permutation fictive A/B/C traduisent correctement ce problème. |
| Abscisses et dénominateurs | P. 20-22 : parc des logements, émissions évitées rapportées à 2018, économies d'énergie rapportées à 2018. Le support et la carte distinguent correctement ces bases ; aucune économie individuelle garantie n'est déduite. |
| Contradiction santé | P. 13 : le texte attribue les pertes d'utilité à la morbidité et le décès à la mortalité ; le tableau 6a inverse les libellés. La contradiction est réelle. Les montants litigieux ne sont pas enseignés par le pilote. |
| Analyse de sensibilité | P. 14 et 16-18 : actualisation, horizon, prix anticipés, comportements et limites techniques. La liste de vérifications est explicitement une proposition pédagogique, non une procédure certifiée. |

Les questions ne réutilisent pas les prescriptions locatives de la note 15,
les montants de santé contradictoires, ni les chiffres dont la légende de
la figure 10 p. 22 contredit le texte. L'étude reste nommée et datée sur les
cartes ; elle ne sert pas à annoncer une aide, un prix ou un droit actuel.

## Schémas originaux

- `renovation-perspectives.svg` : catégories conceptuelles, capitalisation
  dite supposée, santé conditionnelle, aucun versement dessiné. Cohérent avec
  les pages 14 et 19-20 ; ne reproduit pas le graphique chiffré du PDF.
- `renovation-classements.svg` : les mêmes identifiants A/B/C sont permutés
  entre deux tris. La mention « Exemple fictif, sans données du Focus »
  empêche de prendre les rangs pour des résultats observés.
- `renovation-axes.svg` : trois familles de cumuls sans fausse courbe ni
  valeur inventée. Les références 2018 correspondent aux légendes sources.

Les fichiers source SVG examinés n'embarquent ni image extraite du PDF,
script, chargement externe, ni chiffre de performance reconstitué. La mention
de création originale et l'autorisation de diffusion du pilote ne valent
pas autorisation générale de republier les figures du Focus.

## Réserves et acceptations séparées

1. **Profondeur pédagogique** : malgré l'étiquette N4, les huit cartes sont
   surtout des distinctions et une lecture critique guidée. Le travail de
   synthèse est pertinent mais ce seul pilote ne démontre pas une compétence
   d'expert. Cette limite est annoncée dans la leçon et doit rester visible.
2. **Persistance des réponses** : la phrase « les réponses libres sont
   conservées » relève du comportement logiciel. Elle doit être vérifiée
   par les tests du client ; l'étude source et cette revue ne la prouvent pas.
3. **Usage des supports** : les textes alternatifs et les schémas sont
   sémantiquement cohérents ; lisibilité, chargement hors ligne, restitution
   avant/après corrigé et parcours clavier exigent leurs essais de rendu.
4. **Portée historique** : aucune actualisation juridique, aucun conseil
   d'investissement individualisé, aucune faisabilité technique n'est
   validé ici. Toute extension vers ces usages demandera d'autres preuves.

## Empreintes de la version examinée

```text
PDF Focus 106
322a2f5e843f45b99f324a9f185a63d75f6838602081e362002176451855dc43

chapitres/satellites/rentabilite-renovation.json
04ab8f3dc1d31b9186be2fe6b7a493ac039e87aa21586a79a77e54d27d6280cb

banque/images/renovation-axes.svg
e06cfc02b0fdaed4957f30c33efc6c8d357f91f5558aed09853338ab4df212f6

banque/images/renovation-classements.svg
e763f86966bc2338c83623cce04cbaa18be2bbf18f4d420cfb50d5bec4af5ab6

banque/images/renovation-perspectives.svg
45aa05c28cf7ecca7ef9ca7a872d72eed2989b0e986b80990182d2099a49c8f3
```

Une modification du contenu ou d'un schéma après ces empreintes exige la
relecture de la modification. L'ajout de la provenance de revue et le
changement de statut ne prouvent pas, à eux seuls, une acceptation produit.

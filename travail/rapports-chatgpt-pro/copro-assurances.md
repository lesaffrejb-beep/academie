# Copro : déclarations d'assurance et limites des cartes IRSI

04/09/2026. Lot `ACA-COPRO-1`, étape 3. Auteur des retouches : Codex,
gpt-5.6-sol. Relecture indépendante à effectuer ; aucun relecteur attribué.
Cette note documente les corrections, elle ne remplace pas les sources.

## Sources consultées et champ

| Source | Règle retenue | Limite |
|---|---|---|
| [Code des assurances, L113-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000035731302) | Avis dès connaissance ; délai contractuel au moins égal à cinq jours ouvrés, ramené à deux jours ouvrés pour le vol. Déchéance pour retard subordonnée à une clause et au préjudice établi par l'assureur ; exception cas fortuit ou force majeure. | Le minimum légal n'est pas nécessairement le délai du contrat. La qualification d'une cause de retard doit être examinée. |
| [Code des assurances, L125-2](https://www.legifrance.gouv.fr/codes/article_lc/LEGIARTI000047109081), version en vigueur depuis le 28/05/2026 | Pour la garantie CatNat, avis dès connaissance et au plus tard trente jours après publication de l'arrêté de reconnaissance. | La reconnaissance et les garanties restent à vérifier ; les cartes ne tranchent pas l'indemnisation d'un dossier réel. |
| [Service Public, assurance habitation et vol](https://www.service-public.gouv.fr/particuliers/vosdroits/F2028) | Récépissé de plainte parmi les justificatifs ; modalités de déclaration selon le contrat. | Fiche institutionnelle sur l'habitation, pas une police d'assurance de copropriété. Elle ne fonde pas une obligation universelle d'attendre un numéro de plainte avant l'avis à l'assureur. |
| [Service Public, assurance en copropriété](https://www.service-public.gouv.fr/particuliers/vosdroits/F2027) | IRSI est un accord entre assureurs, avec un champ et des exclusions. | Cette présentation ne remplace pas le texte conventionnel complet et sa version applicable ; ses simplifications ne servent pas à reconstruire les cartes de tranches ou de gestionnaire. |
| [Cour d'appel de Metz, RG 23/01001, décision publiée par la Cour de cassation](https://www.courdecassation.fr/decision/6793331f32b173f45a7c8d2f) | Dans ce litige, la convention IRSI n'affranchit pas le bailleur de ses obligations envers une locataire qui n'y est pas partie. | Il s'agit d'un arrêt de cour d'appel, pas d'un arrêt de la Cour de cassation ni de la publication intégrale de la convention. |

La recherche n'a pas permis de consulter une version primaire complète
de la convention IRSI. Les sources générales retrouvées ne suffisent pas
à attester ses seuils, ses exceptions et l'ensemble des règles reprises
dans les anciennes cartes. Aucun blog n'a été utilisé pour la reconstruire.

## Retouches dans la banque

Seul [banque/sinistres/sinistres.json](../../banque/sinistres/sinistres.json)
est concerné. Les identifiants, origines, prérequis et types de carte sont
conservés. Le champ libre `revision` porte la date, l'auteur, l'action, les
sources consultées et `statut_relecture: a-relire`. Il ne prétend pas être
une provenance carte-v2.

| Identifiant | Avant | Après |
|---|---|---|
| `sinistres-delai-degat-des-eaux` | Réponse fixée à cinq jours ouvrés ; distinction contractuelle reléguée à la vigilance. | Réponse complète : avis dès connaissance, délai du contrat, minimum de cinq jours ouvrés. Source IRSI sans rapport avec ce délai retirée de cette carte. |
| `sinistres-delai-vol-vandalisme` | Réponse et bon choix imposaient la plainte préalable ; un distracteur interdisait de compléter la plainte après l'avis. | Question, réponse et quatre choix distinguent avis rapide, délai contractuel et constitution des justificatifs. Le récépissé complète le dossier ; sa collecte ne doit pas faire dépasser le délai de déclaration. |
| `sinistres-delai-catastrophe-naturelle` | Trente jours corrects, mais explication laissant attendre la publication pour déclarer. | Avis dès connaissance et trente jours comme limite extérieure après publication. Référence actuelle à L125-2 ; l'historique de dix jours n'est plus nécessaire à cette carte. |
| `sinistres-decheance-de-garantie` | Présentation générale de la perte de couverture et formule selon laquelle aucune argumentation ne rattrapait le délai. | Question centrée sur les conditions de déchéance : clause, préjudice établi et exceptions. Retrait de l'affirmation générale sur la responsabilité du syndic, que la seule référence à l'article 18 ne démontrait pas. |
| `sinistres-irsi-tranches` | `valide`, tranches et gestionnaire déduits du seul montant, texte conventionnel non consulté. | `signale`, contenu historique conservé pour reprise et anciennes dates conservées. |
| `sinistres-irsi-assureur-gestionnaire` | `valide`, assureur de l'occupant présenté comme règle générale. | `signale`, contenu historique conservé pour reprise et anciennes dates conservées. |
| `sinistres-recherche-de-fuite` | `valide`, organisation et garantie présentées sans toutes les conditions conventionnelles. | `signale`, contenu historique conservé pour reprise et anciennes dates conservées. |
| `sinistres-cidre-abrogee` | `valide`, historique conventionnel daté sans texte primaire consulté. | `signale` faute de preuve primaire retrouvée dans cette recherche ; cela ne signifie pas que la date historique a été démontrée fausse. Anciennes dates conservées. |

Les quatre cartes corrigées portent `verifie: 2026-09-04` pour la lecture
des sources de cette retouche. Leur date précédente reste dans `revision`.
Les quatre cartes signalées gardent `verifie: 2026-08-28` et leurs dates
de péremption antérieures : elles ne sont pas déclarées revérifiées.
Le générateur existant exclut le statut `signale`. Le fichier généré du
site sera actualisé par le responsable du lot ; aucune publication n'est
effectuée par cette sous-tâche.

## Cas contradictoires de relecture

Situations fictives, destinées à vérifier les formulations ; aucune
donnée réelle de copropriété ou d'assuré.

| Situation | Ce que la formulation doit permettre de répondre |
|---|---|
| Un contrat accorde sept jours ouvrés pour déclarer un dégât des eaux ; l'avis arrive au sixième. | Le plancher de cinq jours ne rend pas l'avis hors du délai contractuel de sept jours. L'obligation d'aviser dès connaissance reste distincte de ce calcul. |
| Une police prétend n'accorder qu'un jour ouvré pour déclarer un vol. | Le délai contractuel de déclaration ne peut descendre sous le plancher légal de deux jours ouvrés. |
| Le récépissé de plainte n'est pas encore disponible, mais le délai contractuel de déclaration approche. | Donner avis à l'assureur dans le délai, déposer plainte et compléter les justificatifs ; ne pas enseigner d'attendre passivement le récépissé. |
| Des dommages sont connus avant la publication de l'arrêté CatNat. | Donner avis dès connaissance et suivre ensuite la publication ; les trente jours après publication ne prescrivent pas d'attendre l'arrêté. |
| La déclaration est tardive, mais aucune clause de déchéance n'est invoquée, ou aucun préjudice dû au retard n'est établi. | Ne pas conclure automatiquement à une perte de garantie ; vérifier les conditions de L113-2. |
| Une cause de retard susceptible de constituer un cas fortuit ou de force majeure est documentée. | Examiner cette qualification et ses preuves ; si elle est retenue, la déchéance pour ce retard ne peut être opposée. |
| Des dommages sont estimés à 3 000 euros HT, sans description du local, de la cause ni des assurances concernées. | Le montant seul ne détermine ni l'applicabilité d'IRSI ni l'assureur gestionnaire. Il faut le champ, les circonstances et la version conventionnelle ; les cartes anciennes restent signalées. |

## Contrôles et reprise

- Témoin avant édition : `/tmp/academie-copro-assurances-avant.json`.
- Huit assertions rouges avant correction :
  `/tmp/academie-copro-assurances-rouge.log`.
- Contrôle après correction :
  `/tmp/academie-copro-assurances-vert.log` ; il vérifie les distinctions
  éditoriales, les identifiants, les origines, les dates des cartes
  signalées et l'absence de modifications sur les autres cartes.
- Contrat existant : `python3 app/valide_banque.py` ; le résultat est
  consigné dans `/tmp/academie-copro-assurances-valideur.log`.

Les contrôles de texte préviennent une régression de rédaction ; ils ne
prouvent pas le droit. Il reste à effectuer la relecture indépendante,
à régénérer la banque locale et à lancer les contrôles complets du lot.

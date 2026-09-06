# Contre-lecture de la projection des satellites dans le graphe

06/09/2026. Outil : Codex ; modèle : GPT-6 ; agent : `/root/acces_profils`,
distinct de l'auteur du changement. Lecture du diff de `app/genere.py` et
`app/tests_etude_relecture.py`, des fonctions appelées et de l'artefact courant.
Aucun code, contenu ou état joueur modifié par cette relecture.

**Verdict : aucun défaut bloquant relevé dans ce delta de génération.**
L'absence des extensions servies dans l'arbre est corrigée sans faire du
rattachement un prérequis et sans ajouter les extensions copro au cursus IFSI.
Ce verdict ne couvre pas le rendu client en cours de développement par l'autre
agent, ni une publication ou un essai sur appareil.

## Chaîne de contrôle examinée

- `charge_etudes`, lignes 221-246, fournit les leçons à la nouvelle projection.
  Elle impose un chapitre au statut valide, une relecture structurée et la
  conformité au valideur, une péremption non dépassée, au moins une carte,
  tous les identifiants de cartes effectivement retenus et aucune carte
  expirée. L'ajout des métadonnées publiques intervient après ces contrôles.
- `chapitre_public`, lignes 136-138, utilise une liste fermée de champs.
  Le nœud transmet la structure et le rattachement ; il n'ajoute pas le corps
  de leçon, les réponses, la provenance ou le rapport du relecteur à l'arbre.
- `chapitres_publics`, lignes 141-147, part des chapitres du programme et ajoute
  uniquement les leçons marquées satellites dont le parent appartient à ce
  programme. Il exclut une extension dont l'identifiant serait déjà au socle.
  Le rattachement reste un champ distinct ; les listes `prerequis` et `ponts`
  sont celles de la source. Une liste vide omise par la projection n'est pas
  remplacée par le parent.
- `charge_metiers`, lignes 249-269, applique cette projection à chaque
  programme. Un parent absent du programme du métier ne fait pas entrer le
  satellite dans son arbre. L'attribution existante des cartes au métier
  continue de partir du lot retenu et du rattachement.
- `main`, lignes 420-425, calcule les études avant les nœuds et transmet le
  même catalogue contrôlé à la racine et aux projections par métier. Il
  n'introduit pas de deuxième catalogue de leçons moins filtré.

La fonction `chapitres_publics` prend un catalogue **déjà contrôlé** ; elle ne
répète pas la validation éditoriale. Les deux appels de production examinés
respectent cette précondition. Les chapitres du socle restent visibles comme
programme même lorsqu'ils n'ont pas de contenu jouable : cette présence
structurelle existante n'est pas une fuite de leçons en brouillon.

## Tests ciblés rejoués

`python3 app/tests_etude_relecture.py` : **7 tests, 0,005 s, OK**.

Le nouveau test vérifie le chemin `charge_etudes → charge_metiers`, la
conservation du rattachement et du prérequis déclaré, l'absence dans un métier
sans le parent et l'absence de prérequis inventé après suppression de la liste
source. Il couvre aussi les chapitres brouillon, expiré et avec ancien tampon
non structuré. Les tests préexistants contrôlent une carte absente, une carte
expirée malgré son identifiant retenu et l'indépendance/structure de la revue.

Une contre-passe supplémentaire a été exécutée en Python sur des copies de la
fixture, sans modifier les fichiers de tests. Dix cas passent :

| Cas | Résultat attendu et obtenu dans la projection |
|---|---|
| Satellite complet, relu et valide | Présent dans le programme du parent |
| Chapitre brouillon | Absent |
| Chapitre signalé | Absent |
| Chapitre au statut périmé | Absent |
| Date de péremption du chapitre dépassée | Absent |
| Relecture absente | Absent |
| Rattachement absent du programme | Absent |
| Carte manquante dans le lot retenu | Absent |
| Carte brouillon filtrée dans la chaîne de production normale | Absent |
| Carte expirée malgré son identifiant retenu | Absent |

Pour le cas positif, cette contre-passe vérifie en plus l'absence de prérequis
inventé, l'absence dans un autre programme et l'absence des champs de contenu
ou de fabrication dans le nœud projeté. Elle utilise les mêmes filtres de
cartes que le mode normal (`avec_brouillons=False`) et les fixtures publiques,
sans consulter de données client.

## Artefact courant vérifié en lecture seule

`site/banque.json` contient :

| Projection | Nœuds | Extensions |
|---|---:|---:|
| copro | 393 | 4 |
| ifsi | 375 | 0 |

Extensions copro observées :

- `satellite.travaux.contre-expertise-renovation`
- `satellite.droit.diagnostic-partage-fragilite`
- `satellite.pathologie.facade-ancienne-avant-devis`
- `satellite.travaux.rentabilite-renovation`

Chaque extension figure dans les études contrôlées ; son fichier source est
au statut valide. Rattachement, prérequis et ponts ont été comparés aux
fichiers des chapitres et sont identiques, à l'omission des listes vides près.
La liste de nœuds racine est identique à la projection copro. Aucun de ces
quatre satellites ne figure parmi les nœuds IFSI.

## Limites de preuve

Pas de suite globale, de navigateur ou de génération supplémentaire dans
cette contre-lecture. Le mode de développement `--avec-brouillons` n'est pas
une preuve de service public et n'a pas été utilisé. La règle de transition
existante qui permet des cartes individuellement relues dans un chapitre
brouillon n'est pas modifiée par le delta ; elle ne fait pas entrer sa leçon
ou son extension dans le nouvel arbre. Les cartes retirées par le journal
d'un joueur relèvent toujours des contrôles du client et ne sont pas un état
connu du générateur statique.

Aucune nouvelle correction n'est demandée sur ces deux fichiers avant la
publication ; la relecture du rendu du graphe reste une preuve distincte.

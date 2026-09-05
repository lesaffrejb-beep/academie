# LISTE BLANCHE, les sources de confiance par métier

Ouverte le 02/09/2026 sur le brief de JB (« il faudrait que les joueurs
en arrivant sachent très bien quoi déposer comme savoir ou où le
trouver ; reconnaître des sources comme fiables »). C'est le **kit de
démarrage** d'un dépôt-domaine : ce qu'on télécharge légalement, ce
qu'on demande au joueur, ce qu'on ne touche jamais.

Règles :

1. Une source de cette liste entre au registre avec sa nature et sa
   fiabilité ; elle peut fonder des cartes `banque`.
2. **Aller chercher** (télécharger, lire par l'API) n'est permis que sur
   les sources publiques qui l'autorisent (textes officiels, API
   ouvertes, PDF mis à disposition pour un usage documentaire). Jamais
   de robot sur un site de cours, un éditeur ou un forum.
3. Ce qui manque à cette liste se **demande au joueur** (étape 1 de
   l'usine) : son tas de PDF, ses cours, ses annales. Ils restent chez
   lui, en couche `interne` s'ils ne sont pas libres.
4. Une source commerciale ou partisane n'est pas interdite : elle est
   `editeur`, `organisation-pro` ou `association`, avec son parti, et
   la carte porte « à recouper ».

## Gestionnaire de copropriété (France)

| Source | Nature | Ce qu'on y prend | Comment |
|---|---|---|---|
| Légifrance (loi 65-557, décret 67-223, Code civil, CCH, Code de l'urbanisme, Code des assurances, CPC, décret 2005-240, arrêté 14/03/2005) | texte-officiel | tout le droit | lecture directe, API PISTE (compte gratuit) |
| Judilibre (Cour de cassation) | jurisprudence | arrêts, lectures d'arrêt | API ouverte |
| Cour de cassation, rapports annuels et communiqués | jurisprudence, doctrine | niveau 4 | lecture directe |
| ANIL et les ADIL | institution | fiches pratiques datées | lecture directe |
| Service Public, service-public.fr et service-public.gouv.fr | institution | démarches, délais | lecture directe, version datée |
| Vie-publique.fr | institution | histoire des lois, dossiers | lecture directe |
| ADEME (dont l'observatoire DPE) | institution | énergie, DPE, rénovation | lecture directe, données ouvertes |
| ANAH / France Rénov' | institution | aides (péremption obligatoire) | lecture directe |
| Ministère de la transition écologique (ecologie.gouv.fr) | institution | DPE, calendriers, PPT | lecture directe |
| CRE | institution | prix et tarifs (péremption) | lecture directe |
| CNIL | institution | RGPD au cabinet | lecture directe |
| INRS (inrs.fr) | institution | prévention BTP, coordination SPS, charge et risques psychosociaux | liens et lecture documentaire ; pas de reproduction non privée sans autorisation |
| DGCCRF (economie.gouv.fr) | institution | devis, garanties, pratiques contractuelles | lecture directe ; vérifier l'application au syndicat, pas au seul consommateur |
| DGFiP (impots.gouv.fr) | institution | fiscalité immobilière, notices par campagne | pages publiques seulement ; pas d'espace fiscal ni de donnée de contribuable |
| DITP (modernisation.gouv.fr) | institution | clarté des écrits | méthode publique, pas règle de droit ni preuve de psychologie d'AG |
| Ministère de la Culture, Histoire des arts | institution | architecture, notices patrimoniales | attribution et licence du sous-domaine/document ; aucune image présumée libre |
| Cité de l'architecture et du patrimoine | institution | pistes de lecture et ressources pédagogiques | liens ; droits propres au dossier avant toute reprise |
| Agence Qualité Construction (fiches pathologie) | norme | texte des fiches ; **aucune image** | PDF pour usage documentaire, `pdftotext` |
| Cerema (dont le portail réseaux de chaleur) | institution | guides techniques, chauffage urbain | lecture directe |
| Agences régionales de santé (ars.sante.fr) | institution | risque sanitaire des installations collectives, dont la légionelle | lecture directe |
| CSTB, AFNOR (DTU, NF P 03-001) | norme | références payantes : on cite, on résume la doctrine, on ne recopie pas | achat par le joueur si besoin |
| data.gouv.fr (DVF, RNC, cadastre) | institution | données ouvertes, le socle PostGIS du VPS | déjà chargé dans `socle` |
| France Assureurs (convention IRSI) | organisation-pro, défend les assureurs | le texte de la convention | lecture directe, à recouper |
| Fédérations de syndics (FNAIM, UNIS, Plurience) | organisation-pro, défend les syndics | positions, guides | lecture directe, parti affiché |
| ARC, UFC-Que Choisir, CLCV | association, défend les copropriétaires | positions, analyses critiques | lecture directe, parti affiché |
| Revues (AJDI, Loyers et copropriété, IRC) | doctrine | niveau 4 | abonnement du joueur, couche `interne` |
| Immocampus (employeur) | support-interne | paraphrase | couche `interne`, jamais redistribué |
| Le carnet NotebookLM « Copropriété » de JB | moteur de recherche sur corpus choisi | des pistes, jamais une source | `CORPUS.md` §4 |

Ce qu'on ne touche jamais : les sites de cours, les blogs anonymes, les
pages d'un autre droit (Québec, Belgique) qui partagent le vocabulaire.

### Repérage public du 04/09/2026

`ACA-CONTENT-MAP-1` a produit cinq plans de lecture dans
`travail/sources-{energie,travaux,immobilier,cabinet,culture}-2026-09-04.md`.
Les nouveaux hôtes du registre portent `repere_le` et une preuve limitée ;
`verifie` reste vide, car aucun corpus n'a été intégralement traité dans
l'usine. Cette liste autorise une recherche, **pas une déclaration de
lecture ou de validation automatique**.

Les droits ont été lus séparément : certains sites sont sous licence
ouverte, d'autres limitent la reprise. En particulier, les articles CNIL
sont sous CC BY-ND, les ressources France Rénov' sont sous droits ANAH,
les reproductions INRS non privées demandent une autorisation. Les
conditions d'Histoire des arts diffèrent de celles de culture.gouv.fr,
et celles du portail réseaux de chaleur de celles du site Cerema principal.
Les liens précis et les réserves sont dans les inventaires. Aucune
nouvelle autorisation de téléchargement massif ou de publication n'en découle.

### Complément du 05/09/2026

Le [complément DILA](../travail/sources-energie-2026-09-05.md) précise le
canal ouvert pour les fiches des quatre domaines concernés. La
[référence Culture](../travail/sources-culture-2026-09-05.md) ajoute une
notice BnF exacte à instruire, avec droits de notice et de livre distincts.
Recherche autorisée dans le catalogue BnF et Gallica pour cette piste ;
aucun téléchargement massif. Les deux nouvelles lignes du registre
restent des repérages, sans vérification intégrale du contenu métier.

### Ce que l'extraction des 84 cartes a révélé (03/09/2026)

Le chantier `ACA-SOURCES-1` a rattaché les 154 entrées de source des
cartes à `sources/registre.json`. Six domaines web seulement portent le
tout : `legifrance.gouv.fr` (114), `qualiteconstruction.com` (13),
`cerema.fr` (3), `courdecassation.fr` (3), `ecologie.gouv.fr` (1),
`ars.sante.fr` (1). Trois familles de sources sans URL sont apparues, et
sont désormais des lignes de registre à part entière :

- les **normes NF DTU**, citées pour mémoire, jamais recopiées : le
  texte est payant et non consultable ;
- la **convention IRSI**, `organisation-pro`, parti « défend les
  assureurs », **jamais lue à la source** : ses seuils ont été recoupés
  le 28/08/2026 sur des sources professionnelles concordantes. C'est le
  premier trou nommé du domaine ;
- les **grilles et radars de méthode de JB** (relecture des comptes,
  conformité annuelle, urgence sinistre), nature `terrain`, fiabilité C :
  un ordre de lecture, jamais une règle de droit.

Deux trous nommés en sortent, à instruire :

1. le **référentiel d'exploitation en copropriété** qui fonde la
   décomposition P1 à P5 n'a pas été retrouvé. Trois cartes reposent sur
   lui, classées `editeur` et fiabilité C en attendant un guide Cerema
   ou un NF DTU ;
2. l'arrêt **Cass. 3e civ. du 18 juin 2026** est cité sans numéro de
   pourvoi. Il est à retrouver sur Judilibre avant d'être servi.

## Concours et études en soins infirmiers (le domaine d'Arthur)

| Source | Nature | Ce qu'on y prend |
|---|---|---|
| Légifrance (Code de la santé publique, décrets de compétences) | texte-officiel | législation, éthique, déontologie |
| Haute Autorité de Santé | institution | recommandations |
| Santé publique France | institution | épidémiologie, prévention |
| ANSM | institution | pharmacologie, sécurité du médicament |
| Ordre national des infirmiers | institution | déontologie |
| Annales et notices officielles du concours | texte-officiel | la région « concours » (trou n° 1 du domaine) |
| Manuels et cours acquis | support-interne | couche `interne` seulement |

Ce qu'on ne touche jamais : une donnée patient, une photo clinique sans
licence, un forum d'étudiants.

## Le gabarit pour un métier nouveau

Pour chaque métier, remplir avant toute génération :

1. les **textes officiels** qui font foi (le code, la loi, le décret) ;
2. les **institutions** qui publient (l'agence, l'ordre, l'autorité) ;
3. les **normes et référentiels techniques** (et leur coût) ;
4. la **doctrine** signée et où elle vit (revues, manuels) ;
5. les **organisations professionnelles** et **associations**, avec leur
   parti ;
6. ce qui est **interdit** (l'équivalent des données patient) ;
7. les **ancres de niveau** (le diplôme d'entrée, le référentiel de
   compétences, la formation continue obligatoire).

Un métier dont on ne sait pas remplir les lignes 1 et 2 n'est pas prêt
pour l'usine : on le dit au joueur.

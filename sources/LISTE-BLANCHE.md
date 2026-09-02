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
| Service-public.fr | institution | démarches, délais | lecture directe |
| Vie-publique.fr | institution | histoire des lois, dossiers | lecture directe |
| ADEME (dont l'observatoire DPE) | institution | énergie, DPE, rénovation | lecture directe, données ouvertes |
| ANAH / France Rénov' | institution | aides (péremption obligatoire) | lecture directe |
| Ministère de la transition écologique (ecologie.gouv.fr) | institution | DPE, calendriers, PPT | lecture directe |
| CRE | institution | prix et tarifs (péremption) | lecture directe |
| CNIL | institution | RGPD au cabinet | lecture directe |
| Agence Qualité Construction (fiches pathologie) | norme | texte des fiches ; **aucune image** | PDF pour usage documentaire, `pdftotext` |
| Cerema | institution | guides techniques | lecture directe |
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

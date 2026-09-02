# Relecture 2026-09-02 (soir) : pré-mortem de la conception v2

Protocole : agent frais, lecture de toute la conception v2 contre le
code réel (`app/*.py`, `academie.json`, `programme/copro.json`), sans
modifier un fichier. Verdict rendu à 22:34 : **4 red paths, 16
bloquants, 18 mineurs, 12 questions**. Tout ce qui suit a été réparé le
soir même, sauf ce qui est marqué « reste dû ».

## Red paths, réparés

| # | Trouvaille | Réparation |
|---|---|---|
| R1 | La couche `perso` (pièces réelles, photos non anonymisées) était livrable et servie par le serveur, contre la doctrine | `perso` retirée des couches de livraison (`livraison-v1`) et des banques servies (`API.md`, `schema.sql`) ; redéfinie en v2 comme cartes personnelles sans donnée d'un tiers, jamais livrées (`CONTRAT-CARTE-V2.md` §1) |
| R2 | `schema.sql` codait la visibilité en opt-in par cercle, contre « tous se voient par défaut » | table `visibilites` remplacée par `masquages` (profil, domaine ou tout) ; « une même Académie » = tous les profils du serveur ; routes `/masquages` |
| R3 | Le bilan du mois partageable contenait les erreurs et leurs raisons (le carnet) | bilan privé ; la carte partageable ne porte que cartes stabilisées, domaines qui ont bougé, titre (`BLUEPRINT.md` §12) |
| R4 | La correction libre « clé du joueur » sans lieu d'appel, contre l'interdit de tout hôte tiers | v1 : liste de contrôle ou son propre assistant par copier-coller ; plus tard, exception opt-in et déclarée vers le seul fournisseur choisi par le joueur (`decisions/0020` amendée, `BLUEPRINT.md` §7) |

## Bloquants, réparés

B1 la maquette existe (`travail/maquette-2026-09-02.html`, publiée) ·
B2 renvois « §14 » corrigés en §16 · B3 la lettre devient
`note_confiance` · B4 `a_recouper`, `note_confiance` et
`source[].fiabilite` entrent au schéma comme champs dérivés écrits par le
générateur ; `sources/registre.json` nommé comme forme machine du
registre · B5 règle de migration du journal v0 écrite
(`CONTRAT-CARTE-V2.md` §5, `journal-v1` description) ; `decisions/0005`
alignée sur `format` · B6 `licence` ajoutée à la livraison et à la table
`banques` · B7 table `adoptions` · B8 `mode: signalement` au journal,
route `/signalements`, table `signalements` · B9 chantier `ACA-ARBRE-1`
(progression.py v2 au niveau du chapitre, fraîcheur, ouverture de
branche) et `decisions/0001` amendée · B10 socle `cabinet` = 3 sur le
domaine entier, texte aligné sur le JSON · B11 prérequis de niveau
supérieur retiré (devenu pont) ; zéro violation restante · B12
`PROGRAMME.md` §2 dit que `academie.json` sera aligné par
`ACA-PROGRAMME-1` · B13 quiz unifié : vingt questions, deux par domaine,
quatre pour un domaine adopté plus tard · B14 `METHODE.md` §30 (la fiche
se lit après) et §31 (les petits leviers) · B15 exceptions nommées au
« zéro tiers » : le fournisseur de mail, et le fournisseur de modèle
choisi par le joueur · B16 la livraison transporte `config` et
`programme` pour que le valideur rejoué à la réception ait de quoi
travailler.

## Mineurs, réparés ou assumés

Réparés : M1 (titre d'`AGENTS.md`), M2 (vocabulaire résiduel de
`METHODE.md`), M3 (neuf par séance « une à trois » partout ; vingt-deux
décisions ; « atteint vingt et un jours »), M4 (schéma et texte alignés :
`sources_concordantes`, `historique[].par`, `format`, chrono admis sur
quatre types seulement, longueur de leçon en caractères), M5 (niveaux 4
et 5 en `synthese` et `lecture`), M6 (`decisions/0018` dans « ce qui
reste à trancher »), M7 (rangs de `DOCTRINE.md` §4 complétés), M9
(sources à la fin en épreuve), M10 (DA et routes : provenance, lettre,
page Confiance), M11 (README et ROADMAP alignés sur l'invariant 1
amendé), M12 (`ACA-RITUAL-1` et `ACA-RITUAL-METRICS-1` dépendent de
`ACA-JOURNAL-SYNC-1`), M13 (`points.py` remplace `xp_affichee`), M14
(preuve d'`ACA-DOC-2` réécrite, commit poussé), M15 (registre contre
inventaire), M16 (le cap du profil contre le cap du journal), M17
(motifs des chiffres : articles et noms de textes exclus), M18 (un
`banque.json` sans `contrat` est lu comme v1).

**Reste dû, assumé** : M8, des chemins `labor/...` restent cités dans
`decisions/` et `METHODE.md` ; ce sont des pointeurs vers le dépôt privé
de JB, un copain qui reprend l'Académie les lira comme des références,
pas comme des dépendances (`serveur/README.md` le dit). Les titres et
l'ordre d'`academie.json` divergent de `copro.json` jusqu'à
`ACA-PROGRAMME-1`, dit dans `PROGRAMME.md` §2. `academie.json` ne porte
pas encore `seuil_fraicheur_jours` ni `nouveau_par_jour` ni `socle` :
`ACA-ARBRE-1`, `ACA-SEMAINE-1` et `ACA-JOURNEE-1` les ajoutent.

## Les douze questions d'un développeur, et les réponses

1. **Importer `etat/jb/revues.jsonl` dans le VPS** : `serveur/importer_journal.py`
   (chantier `ACA-JOURNAL-SYNC-1`) ; `mode: flash` devient `mode: revision`
   avec `format: seance` ; les lignes du quiz gardent `origine` et
   `stabilite_forcee` ; le carnet devient `mode: erreur` ; `nonce` =
   SHA-256 de la ligne d'origine. Le fichier source n'est jamais
   réécrit.
2. **Qui écrit jalons, scores de défis, signalements** : le serveur, dans
   ses tables dérivées, à partir des lignes de journal reçues (un jalon
   naît quand le recalcul détecte un domaine validé ; un score de défi
   se calcule depuis les lignes `format: defi`). Ces tables se
   recalculent depuis le journal ; elles ne sont pas une seconde vérité.
3. **`POST /journal`** : 500 lignes par lot ; `depuis` compare `recu_le`
   (horloge serveur) ; un lot refusé renvoie l'index de la ligne fautive,
   le client la met de côté dans un magasin local `rejets` et renvoie le
   reste. La file ne se bloque jamais.
4. **Le cookie du téléphone sans comptes** : l'outil de ligne de commande
   du serveur génère un magic link ; JB l'ouvre sur son téléphone ;
   cookie d'un an. Le jeton `outil` du skill « glisser » vaut 90 jours,
   révocable.
5. **Parité FSRS** : `app/vecteurs_fsrs.py` produit déjà des séquences et
   leurs états ; le chantier épingle `ts-fsrs` et vérifie qu'il prend les
   21 paramètres de FSRS-6 ; les poids par défaut vivent dans
   `app/planificateur.py` et seront publiés dans `banque.json`
   (`fsrs.poids`) par `ACA-ARBRE-1`.
6. **Contrat absent de `banque.json`** : lu comme `carte-v1`
   (`web/README.md`).
7. **États de nœud et de branche** : calculés par `progression.py` v2 et
   par le client en parité (`ACA-ARBRE-1`) ; `genere.py` publie les
   chapitres et leurs prérequis dans `banque.json` ; le client ne lit
   pas `programme/copro.json` directement.
8. **Palette au rang** : l'ordre d'`academie.json` après alignement
   (celui de `copro.json`) ; Culture est hors arbre, hors quiz (deux
   questions × dix domaines = vingt).
9. **L'onglet Cercle** : masqué (barre à trois entrées) tant que
   `ACA-CERCLE-1` n'est pas livré.
10. **La clé pour `libre` et `synthese`** : v1 sans clé (liste de
    contrôle, ou copier-coller vers son assistant) ; plus tard l'exception
    opt-in de `decisions/0020`.
11. **« Cette carte est fausse »** : `mode: signalement` au journal, effet
    local immédiat, puis route et table côté serveur.
12. **Semaine type** : `profils.reglages` fait foi ; le client la met en
    cache ; en cas de divergence, la copie serveur à la dernière
    synchronisation gagne ; le journal note le `jour` réellement appliqué.

## Ce que JB relit

`DOCTRINE.md` invariants 1 et 2 (le modèle écrit, la provenance
s'affiche), `decisions/0010` amendée (tous se voient), `0021` et `0022`
(provenance, confiance, audit croisé), `CONTRAT-CARTE-V2.md` §1
(couche `perso` v2) et §5 (migration du journal), et la maquette.

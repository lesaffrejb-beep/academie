# Pilote exécuté : dix pages vers une étude

Source : Focus 106, juin 2024, pages PDF 13-22 incluses. Empreinte complète
dans `extraction-mesuree.json`. L'usine indique 32/32 pages relues et une
fiche validée ; le présent lot réemploie ses unités sans changer leurs sceaux.
Outil d'intégration : Codex ; identifiant exact du modèle non exposé.

## Ordre réellement appliqué et raison

1. Identifier PDF, empreinte, pages et droits : éviter la mauvaise version
   et distinguer droit de lecture et droit de diffusion.
2. Extraire chaque page par Poppler layout puis Docling/RapidOCR, sans API.
   Poppler garde un témoin simple ; Docling restitue notamment les tables.
   Rendre aussi la page entière avec PyMuPDF : les axes ne se jugent pas
   seulement à la présence des mots dans le Markdown.
3. Comparer et arbitrer visuellement : jamais de vote entre sorties.
   Conserver les désaccords de la source et les lacunes des extracteurs.
4. Écrire les notions et leurs limites, puis leçon, exercices et synthèse
   avec sources localisées. Employer des schémas originaux pour le produit.
5. Relecture indépendante du contenu, puis contrôle de contrat. Statut
   valide seulement après l'avis `RELECTURE.md`, pas après extraction seule.
6. Vérifier affichage, zoom, support absent, conservation du brouillon,
   parcours complet et isolement du cursus. Voir `REVUE-CODE.md`.
7. Construire un paquet isolé des changements de comptes, sauvegarder,
   publier et vérifier les empreintes et l'accès réel. Voir `PUBLICATION.md`.

## Mesures et limites

Essai : Docling 2.126.0, Docling-core 2.95.0, PyMuPDF 1.28.2,
RapidOCR 3.9.2, Poppler 26.07.0 ; CPU, deux threads, poids déjà présents.
54,443 secondes pour la collecte après import, pas pour la création du cours.
Dix sorties success Docling ; dix témoins Poppler ; dix rendus entiers.
21 régions détectées : dix logos à exclure et onze régions de tableaux ou
graphiques candidates. Ce n'est pas onze supports prêts à publier.

Contrôle des recadrages p. 13, 14 et 22 : p. 14 perd la note explicative
et coupe le bas d'une légende ; les titres peuvent rester hors région.
La page complète reste donc obligatoire pour qualifier un support. Les
figures originales ne sont pas distribuées ; trois SVG originaux le sont.

Exemple de complémentarité : le tableau p. 20 est structuré par Docling ;
les courbes p. 22 exigent le rendu. Exemple d'échec : p. 13, Docling répartit
le texte d'une cellule fusionnée sur des lignes distinctes. L'image montre
la cellule commune. Même une structure de tableau plausible peut être fausse.
L'inversion mortalité/morbidité, elle, existe dans la source : elle n'est
pas corrigée en inventant une vérité. Les montants litigieux sont suspendus.

Les similarités de séquences dans le rapport ne sont pas des taux de justesse.
Ce test ne compare pas toutes les solutions du marché et ne mesure pas le
gain causal du mélange sur un corpus annoté. Les agents de relecture sont
des passes indépendantes, pas une expertise humaine du bâtiment.

Coût API d'extraction : zéro. Le temps machine et l'usage Codex de conception
et de relecture ne sont pas gratuits ; aucun coût total de cours n'est déduit
de ce chiffre. Aucun envoi du PDF à une API, abonnement ou modèle payant.

## Traçabilité des notions et exclusions

| Page | Notion conservée / arbitrage | Descendant |
|---|---|---|
| 13 | Contradiction texte/tableau, montants santé suspendus | carte anomalie |
| 14 | Bénéfices, horizon, actualisation ; note hors recadrage | perspectives, sensibilité |
| 15 | Crédit hypothétique, friction locative ; droit des loyers non enseigné | crédit, frictions |
| 16 | Friction collective calibrée, préférences ; pas de règle de répartition des charges | frictions, sensibilité |
| 17 | Segments statistiques, limites de représentativité | périmètre, leçon |
| 18 | Exclusions techniques ; potentiel modélisé non assimilable à faisabilité | périmètre |
| 19 | Perspectives privées/sociales, financement inclus | perspectives |
| 20 | Tris distincts et dénominateurs ; tableau structuré confronté au rendu | classements, axes |
| 21 | Courbes de gisement, hétérogénéité ; pas de gain individuel promis | classements, axes |
| 22 | Cumuls distincts ; légende figure 10 contradictoire au texte, chiffres non enseignés | axes, sensibilité |

Préfixe des huit cartes : `renovation-pilote-`. Chapitre :
`satellite.travaux.rentabilite-renovation`. La synthèse demande de transférer
ces distinctions à une proposition fictive. Ni simulateur de chantier,
ni diagnostic photographique, ni cours couvrant tous les métiers demandés.

## Reproduire et contrôler

```sh
python3 travail/pilote-renovation-10p/test_collecte.py
python3 travail/pilote-renovation-10p/test_routage.py
HF_HUB_OFFLINE=1 python travail/pilote-renovation-10p/collecte.py --out sources/benchmark-pdf/NOUVEL-ESSAI
python3 app/usine/usine.py etat 322a2f5e843f45b9
python3 app/genere.py --couches banque --sortie site/banque.json
python3 app/tests.py
python3 tooling/check.py
```

La commande de collecte exige un environnement Docling avec les versions
du rapport et les poids RapidOCR/Docling préchargés ; ce n'est pas le Python
stdlib du produit. `HF_HOME` et `XDG_CACHE_HOME` désignent le cache isolé de
l'essai ; sans les poids, le mode hors ligne échoue, il ne donne pas succès.
Elle refuse un PDF différent, un dossier existant et moins de 8 Gio libres.
Les preuves brutes restent locales dans
`sources/benchmark-pdf/pilote-renovation-10p/`, ignoré par Git.

Pour une contre-passe sans relire tout : tirer au sort trois pages parmi
13-22 avec une graine consignée avant lecture ; vérifier leurs empreintes,
une phrase, une unité et le lien exercice-source. Toujours ajouter les pages
critiques 13, 18, 20 et 22. Ici les dix pages ont été revues : aucun simple
sondage n'est présenté comme une relecture exhaustive.

Pour le client : `cd web`, `npm test`, puis `npm exec playwright test
tests/e2e/pilote-renovation.spec.ts tests/e2e/etude.spec.ts`. Les tests emploient
un profil fictif et ne prouvent pas la synchronisation réelle du serveur.
La reprise après rechargement mesure la persistance locale, pas le transfert
sur un second appareil. Les résultats finaux sont consignés à la publication.

# ARCHITECTURE, comment l'Académie est construite et où tout est stocké

Écrite le 02/09/2026. Reprend du `SPEC-PRODUIT` d'août ce qui tient (le
modèle A4, les invariants, l'usine) et tranche ce qui manquait : l'état
joueur synchronisé, le hors-ligne, la stack du front, les contrats de
données v2, l'archivage, l'auditabilité, le déploiement. Les décisions
qui la fondent : [`decisions/0006`](decisions/0006-etat-joueur-sur-le-serveur-client-hors-ligne.md),
[`0007`](decisions/0007-stack-front-et-dependances.md),
[`0008`](decisions/0008-chacun-son-depot-et-son-abonnement.md),
[`0009`](decisions/0009-la-boite-et-les-chapitres-satellites.md),
[`0018`](decisions/0018-licences-du-code-et-du-contenu.md),
[`0019`](decisions/0019-peremption-du-droit-et-veille.md),
[`0020`](decisions/0020-telemetrie-zero-tiers.md).

---

## 1. Les quatre pièces

```
 CHEZ CHAQUE JOUEUR (Mac de JB, machine d'Arthur…)
 ┌──────────────────────────────────────────────────────────────┐
 │ LE DÉPÔT-DOMAINE (privé, son compte, son abonnement)          │
 │   sources/    PDF, cours, vidéos, captures : JAMAIS dans git  │
 │   sources/REGISTRE.md   nature, parti, fiabilité par source   │
 │   boite/      ce qu'on glisse ; JOURNAL.md versionné          │
 │   banque/     chapitres et cartes JSON (contrat v2)           │
 │   academie.json, programme/<metier>.json                      │
 │   L'USINE : Claude Code + outils libres, tourne ici           │
 └──────────────┬───────────────────────────────────────────────┘
                │ « je publie ma livraison » (geste humain)
                ▼
 LE DÉPÔT PRODUIT `academie` (GitHub privé, compte JB)
 ┌──────────────────────────────────────────────────────────────┐
 │ app/        moteur Python (référence), valideurs, tests       │
 │ serveur/    API d'état : Python, SQLite, jetons, livraisons   │
 │ web/        client : Vite, React, TypeScript, PWA, ts-fsrs    │
 │ contrats/   JSON Schema des frontières                        │
 │ banque/     le domaine copro de JB (couches banque, interne)  │
 │ deploy/     systemd, Caddy, installation                      │
 └──────────────┬───────────────────────────────────────────────┘
                │ git pull + build (timer)
                ▼
 LE VPS DE JB (OVH, Caddy, systemd)               LE CLIENT
 ┌──────────────────────────────────┐    ┌──────────────────────┐
 │ /var/lib/academie/publication/   │◄───│ téléphone, ordinateur │
 │   banque.json + images + web/    │    │ PWA hors-ligne d'abord│
 │ /var/lib/academie/etat.sqlite    │◄──►│ IndexedDB : journal,  │
 │ /var/lib/academie/banques/<jou.> │    │ banque, file d'envoi  │
 │ aucune clé de modèle, aucun appel│    └──────────────────────┘
 └──────────────────────────────────┘
```

Les invariants, dans l'ordre où ils protègent :

1. Les sources restent chez le joueur ; le serveur ne voit que des
   fiches dérivées, validées.
2. Le traitement par modèle est local et au coût du joueur ; le serveur
   n'a aucune clé et n'appelle aucun modèle.
3. La livraison est un geste humain ; elle a un réceptionniste (jeton,
   re-validation, quarantaine, refus tracé).
4. JB n'est pas un joueur spécial : `academie/banque/` est son
   dépôt-domaine, livré au même serveur par le même chemin.
5. L'état joueur vit sur le serveur, se recalcule depuis le journal,
   s'exporte à tout moment, et n'est jamais dans git.

## 2. Où est stocké quoi

| Chose | Mac | PC du bureau | NOIR (SSD) | VPS | GitHub | Téléphone |
|---|---|---|---|---|---|---|
| Code, doctrine, contrats, moteur | clone | rien | bundle mensuel | clone déployé | **vérité** | |
| Banque copro validée (`banque`, `interne`) | clone | rien | bundle | clone déployé, servi | vérité (privé) | cache |
| Sources brutes (PDF, vidéos, transcriptions, captures Immocampus) | `sources/` hors git | rien | copie datée avec empreinte | **jamais** | **jamais** | |
| Boîte (ce qu'on glisse) | `boite/` hors git ; `JOURNAL.md` versionné | rien | | file d'attente synchronisée (texte seulement) | JOURNAL.md | capture |
| État joueur (journal, carnet, épreuves, insignes) | export JSON à la demande | rien | export mensuel | **vérité** (SQLite, hors git) | jamais | copie IndexedDB |
| Banques livrées par d'autres joueurs | | | | `/var/lib/academie/banques/`, hors git, sauvegardées | jamais | cache |
| Images et audio validés | clone | | bundle | servis | vérité | cache |
| Secrets (jetons, clé de session) | trousseau | jamais | jamais | `/etc/academie/` root seul | jamais | cookie |

Le PC du bureau est la machine de l'employeur : navigateur seulement.
Rien du produit n'y est cloné, rien de l'employeur n'entre dans le
produit.

## 3. Archivage et sauvegarde

- **Documents et décisions** : archivés intacts dans `archive/`, jamais
  réécrits ; une décision remplacée le dit et pointe la suivante.
- **Contenu** : une carte ne se supprime pas, elle passe `perime` ou
  `signale` ; son identifiant est immuable, c'est la clé de tout
  l'historique FSRS. Un chapitre porte `version` et `remplace`.
- **Sources** : chaque source citée est copiée localement au moment de
  la vérification (`sources/<empreinte>.<ext>` sur le Mac, hors git) et
  son empreinte SHA-256 est écrite dans la carte. Les liens meurent, les
  empreintes non. Copie mensuelle vers NOIR.
- **État joueur** : SQLite sauvegardé chaque nuit sur le VPS
  (`sauvegarde-socle` existant, périmètre étendu), export JSON du
  journal à un clic dans l'app, copie mensuelle sur NOIR ; export Anki
  du contenu comme assurance-vie de réversibilité.
- **Exercice de restauration** : une fois par trimestre, restaurer la
  sauvegarde de la veille sur un dossier vide et rejouer
  `python3 app/progression.py` dessus. Une sauvegarde jamais restaurée
  n'est pas une sauvegarde.

## 4. Le moteur (Python, la référence)

Ce qui existe et reste : `planificateur.py` (FSRS-6, comparé à
`py-fsrs`), `seance.py` (composition, entrelacement, ré-étalement),
`progression.py` (remplissage, ouverture, épreuve, XP dérivée),
`quiz.py`, `erreurs.py`, `valide_banque.py`, `genere.py`,
`vecteurs_fsrs.py`, 47 tests et les tests de mutation.

Ce qui s'ajoute, chantier par chantier :

| Module | Ce qu'il fait | Chantier |
|---|---|---|
| `valide_programme.py` | valide `programme/<metier>.json` : clés de domaines cohérentes avec `academie.json`, prérequis existants et de niveau inférieur ou égal, pas de cycle | ACA-PROGRAMME-1 |
| `valide_banque.py` v2 | contrat carte-v2 et chapitre-v1 : `chapitre`, niveau 1-5, `source[].nature`, types nouveaux, `attendus`, `image.alt`, empreintes | ACA-CONTRAT-2 |
| `seance.py` | semaine type, pondération socle, séance de domaine, « rappels d'ailleurs », graine journalisée | ACA-SEMAINE-1 |
| `etude.py` | composeur d'étude : amorce, leçon, exercices, synthèse | ACA-ETUDE-1 |
| `journee.py` | composeur de journée : études entrelacées, pauses, rappel du soir, plafond de neuf | ACA-JOURNEE-1 |
| `epreuves.py` | épreuve de domaine (avec part des domaines prérequis), transverse (dossier en pas), du gestionnaire ; verrou 24 h | ACA-EXAMEN-1 |
| `points.py` | points de savoir, niveau, titres, calibration : tout dérivé du journal | ACA-EXAMEN-1 |
| `rapport_rituel.py` | tableau de bord du rituel depuis le journal, sans lire les réponses | ACA-RITUAL-METRICS-1 |
| `audit_banque.py` | rapport HTML d'audit d'une banque : cartes par nature de source, « à recouper », sans source, périmées, trous, provenance par modèle | ACA-AUDIT-1 |
| `verif_run.py` | tire un lot de cartes à revérifier (sans source d'abord, puis anciennes, très révisées, juridiques), produit le dossier de recherche pour l'agent, écrit `historique` et le statut ; tourne chez le propriétaire du domaine | ACA-VERIF-1 |
| `export_anki.py` | `.apkg` via `genanki` (MIT) | ACA-EXPORT-1 |

Règle : le moteur ne connaît aucun métier, aucun prénom, aucun seuil en
dur. Tout vient de `academie.json` et de la banque.

**Parité FSRS** : `app/vecteurs_fsrs.py` produit des séquences de
révisions et leurs états attendus ; le client (`ts-fsrs`) doit les
reproduire à 10⁻⁴ près. Le test tourne en CI des deux côtés.

## 5. Les contrats de données

Tous dans [`contrats/`](contrats/README.md), en JSON Schema, versionnés.
Un artefact publié annonce la version du contrat qu'il respecte ; le
serveur refuse une version qu'il ne connaît pas.

| Contrat | Ce qu'il décrit | État |
|---|---|---|
| `carte-v1` | la carte actuelle (`CONTRAT-CARTE-V1.md`, valideur en place) | en vigueur |
| `carte-v2` | ajoute `chapitre`, niveau 1-5, `source[].nature` et `parti`, types `cas`, `dessin`, `feuille-blanche`, `synthese`, `lecture`, `ecoute`, `attendus`, `chrono`, `image.alt`, `empreinte`, `verifie_par`, `historique` | à instruire, `CONTRAT-CARTE-V2.md` |
| `chapitre-v1` | un chapitre : identité, niveau, prérequis, amorce, leçon, synthèse, cartes, sources, statut, `satellite` | à instruire |
| `journal-v1` | une ligne du journal : révision, examen, quiz, erreur, séance (graine, format, jour) | à instruire ; le journal actuel en est un sous-ensemble |
| `livraison-v1` | le manifeste d'une livraison : joueur, domaine, version de contrat, empreinte de la banque, couches, compte de cartes, registre des sources | à instruire |
| `programme-v1` | `programme/<metier>.json` | à instruire |

**La disposition v2 de la banque** : un fichier par chapitre,
`banque/<domaine>/<branche>/<chapitre>.json`, qui contient la leçon,
l'amorce, la synthèse et ses cartes. La migration des fichiers v1
(`banque/<domaine>/<branche>.json`, tableaux de cartes) est une
assignation de chaque carte à un chapitre, sans renumérotage.

## 6. Le serveur d'état

Squelette dans [`serveur/`](serveur/README.md) : `API.md` (les routes),
`schema.sql` (les tables), `README.md` (le pourquoi et le comment).

- **Stack** : Python, framework HTTP léger épinglé (FastAPI ou
  équivalent), SQLite en mode WAL, un seul processus sous systemd,
  derrière Caddy sur `/academie/api/`.
- **Identité** : un profil par joueur, créé par JB à la main tant qu'il
  n'y a pas de comptes ; ensuite magic link à l'inscription et sur un
  nouvel appareil, cookie de session d'au moins un an, jamais de mot de
  passe. Un fournisseur d'envoi de mail choisi et inscrit au registre
  comme sous-traitant ; repli : JB génère un lien à la main.
- **Le journal** : `POST /journal` reçoit un lot d'entrées (chaque
  entrée porte `quand`, `carte` ou `mode`, `nonce`), le serveur ajoute
  ce qu'il ne connaît pas, répond avec ce que le client n'a pas. Union
  pure, aucune suppression, aucune mise à jour.
- **Les livraisons** : `POST /livraisons` avec le jeton du joueur ; le
  serveur re-passe le valideur, met en quarantaine, JB (ou le
  propriétaire du domaine) accepte, la banque est servie. Refus tracé
  avec motif.
- **La bibliothèque** : `GET /bibliotheque` liste les domaines servis
  (couche `banque` seulement, licence de partage vérifiée) avec leur
  auteur, leur version, leur compte de chapitres et leur rapport
  d'audit ; un joueur adopte un domaine d'un geste, sans rien
  fabriquer. Ce qu'un joueur a digéré à ses frais sert au suivant. Les
  conversions de sources (`.md`, transcriptions) ne montent jamais :
  seules les fiches dérivées circulent.
- **Les cercles** : membres, visibilité (tous se voient par défaut,
  masquage par domaine), défis, ligue. Rien avant le gate du rituel.
- **Suppression** : `DELETE /profil` efface le profil, son journal, son
  carnet, ses livraisons en moins de 48 h ; possible parce que rien de
  tout ça n'est dans git.

## 7. La fabrication : l'usine et la boîte

L'usine ([`gabarit-domaine/USINE.md`](gabarit-domaine/USINE.md)) tourne
chez le joueur. Ses entrées, et l'outil libre qui les lit :

| Entrée | Outil | Sortie |
|---|---|---|
| PDF texte | `pdftotext -layout` (poppler) | texte ; jamais `WebFetch` sur un PDF (il hallucine, mesuré le 28/08) |
| PDF scanné, photo de page | `ocrmypdf` / `tesseract` | texte, relu |
| Vidéo (YouTube, replay interne) | `yt-dlp` pour les sous-titres, sinon `faster-whisper` en local | transcription, couche `interne` par défaut |
| Capture d'écran | modèle de vision, chez le joueur | texte et description |
| Page web fiable (liste blanche du registre) | lecture directe | texte ; jamais de scraping de site de cours |
| Mot-clé | recherche dans le registre des sources, puis liste blanche | pistes ou trou nommé |
| Dépôt git | son README et ses documents | pistes |

Les étapes : inventaire, registre des sources (nature, parti,
fiabilité), génération en `brouillon`, double passe par agent frais,
valideur, livraison. **Le modèle peut générer** un chapitre en cherchant
lui-même sur les domaines de la liste blanche (recherche, citation,
croisement ; jamais un site de cours), avec un tampon de provenance sur
chaque carte ; sans source retrouvée, il l'avoue et la carte reste
conceptuelle (`decisions/0021`). **Les runs de vérification**
(`verif_run.py`) retournent périodiquement sur un tirage de cartes voir
si quelque chose a changé, et laissent une ligne d'historique. Le tout
tourne chez le propriétaire du domaine. La boîte ([`boite/README.md`](boite/README.md))
est l'entrée courte de la même usine : une entrée, un chapitre
satellite.

**Images, trois étages** ([`decisions/0017`](decisions/0017-images-et-audio.md)) :
schémas SVG maison dessinés depuis les descriptions AQC (licence
maison, la v2) ; photothèque de terrain étiquetée par celui qui y était
et confirmée par un second joueur (plus tard) ; images générées admises
seulement comme illustrations marquées, jamais comme photo de
diagnostic. **Audio** : généré depuis la leçon validée, stocké avec
l'empreinte du texte, plus tard.

## 8. Sécurité et RGPD

- Étanchéité d'hébergement : utilisateur système `academie`, racine
  servie hors de tout clone labor, `ProtectSystem=strict` (unités
  existantes), le produit ne peut pas lire `outputs/` ni `coulisses/`.
- Registre des traitements : un traitement par cercle, base légale,
  durée, sous-traitant mail ; suppression sous 48 h avant le premier
  compte tiers.
- Aucune télémétrie tierce, aucun script externe, aucune police
  chargée d'un tiers à l'exécution : tout est servi depuis le VPS
  ([`decisions/0020`](decisions/0020-telemetrie-zero-tiers.md)). Ce
  qu'on mesure est dans le journal, et le joueur peut le lire.
- Scanner anti-fuite sur les couches `banque` et `interne` (slugs,
  immatriculations, ICS, noms du parc) ; aucune donnée de santé réelle
  pour un domaine médical.

## 9. Déploiement

Squelette dans [`deploy/`](deploy/README.md).

| Sur le VPS | Rôle |
|---|---|
| `/home/academie/repo` | clone du dépôt produit, lecture seule pour le service |
| `academie-publication.timer` | 05:15 : `genere.py --couches banque` puis build du client vers `/var/lib/academie/publication/` (existant, périmètre étendu au client) |
| `academie-etat.service` | l'API d'état, port local, SQLite dans `/var/lib/academie/` (à créer) |
| Caddy | `handle_path /academie/*` statique (existant) ; `/academie/api/*` vers l'API (à ajouter) |
| `sauvegarde-socle.timer` | étendu à `/var/lib/academie/` |

Auto-hébergement par un copain : `deploy/README.md` décrit une
installation en cinq étapes sur un Linux avec Python 3.12, Node, Caddy ;
aucune dépendance à labor ni au socle.

## 10. Auditabilité

Tout ce qui s'affiche répond à « pourquoi » :

- **une carte** : son dossier (source, nature, parti, empreinte, qui a
  vérifié et quand, historique des statuts) ;
- **une séance** : sa graine, ses paramètres, la version de la banque et
  du moteur, rejouable à l'identique ;
- **un score** : recalculé depuis le journal par une commande, jamais
  stocké ;
- **une mécanique** : son entrée dans `METHODE.md` ;
- **une décision** : son fichier daté ;
- **une banque** : son rapport d'audit HTML (`audit_banque.py`), lisible
  par un humain qui ne code pas ;
- **un domaine, pour le joueur** : la page « Pourquoi croire ce
  professeur ? » (`decisions/0022`), servie dans l'app depuis chaque
  ligne de provenance : qui a écrit (modèles, versions, humains),
  répartition des notes A/B/C, part sans source, taux de rejet de la
  double passe, échantillons humains, résultats de l'audit croisé par
  un modèle d'un autre fournisseur, registre des signalements et de
  leur traitement, trous et cartes périmées. Tout en est recalculé
  depuis la banque et le journal des vérifications, rien n'est
  déclaré.

## 11. Coûts

Fabrication d'un domaine : dizaines d'euros, ponctuels, mesurés et
écrits dans `gabarit-domaine/DESSINER-LA-CARTE.md` §6. Usage : voisin de
zéro (aucun appel de modèle côté serveur ; la réponse libre coûte à
celui qui a une clé). Hébergement : le VPS existant de JB. Aucun prix
n'est promis à un joueur avant mesure.

## 12. Le squelette, dossier par dossier

| Dossier | Ce qu'il porte | Prêt à |
|---|---|---|
| `app/` | le moteur, ses tests | coder les modules du §4 |
| `serveur/` | `README`, `API.md`, `schema.sql` | coder l'API contre le schéma |
| `web/` | `README` avec l'arborescence, les écrans, les composants | initialiser Vite et coder écran par écran |
| `contrats/` | JSON Schema v2 et `README` | brancher les valideurs |
| `programme/` | `copro.json`, `README` | écrire `valide_programme.py` |
| `banque/` | la banque v1, `satellites/README` | migrer vers la disposition v2 |
| `sources/` | `REGISTRE.md`, `.gitignore` | remplir le registre |
| `boite/` | `README`, `JOURNAL.md`, `.gitignore` | écrire le skill « glisser » |
| `deploy/` | unités existantes, `README` | ajouter l'API et le build |
| `gabarit-domaine/` | le kit d'un nouveau domaine | inchangé |

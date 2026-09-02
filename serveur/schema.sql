-- Schéma de l'API d'état, v1 (proposition du 02/09/2026).
-- SQLite, mode WAL. Appliqué par migrations numérotées ; ce fichier est
-- la migration 0001 le jour où le chantier ACA-JOURNAL-SYNC-1 l'ouvre.
-- Règle : rien ici ne calcule un score. Tout état de jeu se recalcule
-- depuis `journal` par le moteur (app/) ou par le client (ts-fsrs).

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- Un joueur. L'identifiant est opaque ; le mail ne sert qu'au magic link.
CREATE TABLE profils (
  id            TEXT PRIMARY KEY,               -- uuid
  mail          TEXT UNIQUE,                    -- nul tant que JB crée les profils à la main
  titre_affiche TEXT NOT NULL,                  -- ce que les autres voient, choisi par le joueur
  cree_le       TEXT NOT NULL,                  -- ISO 8601
  supprime_le   TEXT,                           -- demande de suppression ; effacement effectif sous 48 h
  reglages      TEXT NOT NULL DEFAULT '{}'      -- JSON : thème, semaine type, notifications
);

-- Sessions (cookie) et jetons d'outil (livraisons, boîte depuis la machine).
CREATE TABLE sessions (
  jeton_hache   TEXT PRIMARY KEY,               -- SHA-256 du jeton, jamais le jeton
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  genre         TEXT NOT NULL CHECK (genre IN ('cookie', 'outil', 'magic')),
  cree_le       TEXT NOT NULL,
  expire_le     TEXT NOT NULL,
  revoque_le    TEXT,
  appareil      TEXT                            -- libellé libre donné par le client
);

-- LE JOURNAL. Append-only. Aucune mise à jour, aucune suppression hors
-- effacement de profil. L'unicité fait l'union : rejouer un lot ne
-- change rien.
CREATE TABLE journal (
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  quand         TEXT NOT NULL,                  -- ISO 8601, écrit par le client
  mode          TEXT NOT NULL CHECK (mode IN ('revision','quiz','examen','erreur','seance','synthese')),
  nonce         TEXT NOT NULL,
  ligne         TEXT NOT NULL,                  -- la ligne journal-v1 complète, JSON
  recu_le       TEXT NOT NULL,                  -- horodatage serveur, pour `depuis`
  PRIMARY KEY (profil, quand, mode, nonce)
);
CREATE INDEX journal_profil_recu ON journal(profil, recu_le);

-- Les banques servies : une ligne par (domaine, version). Le fichier
-- vit sur disque, hors git ; la table ne porte que le manifeste.
CREATE TABLE banques (
  id            INTEGER PRIMARY KEY,
  domaine       TEXT NOT NULL,
  proprietaire  TEXT NOT NULL REFERENCES profils(id),
  contrat       TEXT NOT NULL,                  -- carte-v1 | carte-v2
  empreinte     TEXT NOT NULL,                  -- SHA-256 du banque.json
  couches       TEXT NOT NULL,                  -- JSON : ["banque"] ou ["banque","interne"]
  chemin        TEXT NOT NULL,                  -- /var/lib/academie/banques/<joueur>/<domaine>/<empreinte>.json
  genere_le     TEXT NOT NULL,
  servie        INTEGER NOT NULL DEFAULT 0,     -- 1 = c'est la version servie
  UNIQUE (domaine, empreinte)
);

-- Les livraisons reçues, acceptées ou refusées. Une livraison acceptée
-- devient une ligne de `banques`.
CREATE TABLE livraisons (
  id            TEXT PRIMARY KEY,               -- uuid
  joueur        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  domaine       TEXT NOT NULL,
  manifeste     TEXT NOT NULL,                  -- livraison-v1, JSON
  chemin        TEXT NOT NULL,                  -- l'archive reçue, en quarantaine
  etat          TEXT NOT NULL CHECK (etat IN ('quarantaine','acceptee','refusee')),
  motifs        TEXT NOT NULL DEFAULT '[]',     -- JSON : les motifs du valideur ou du refus
  recue_le      TEXT NOT NULL,
  decidee_le    TEXT,
  decidee_par   TEXT REFERENCES profils(id)
);

-- La boîte : file d'attente texte, synchronisée entre téléphone et
-- machine. Les fichiers ne montent jamais ici.
CREATE TABLE boite (
  id            TEXT PRIMARY KEY,
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  type          TEXT NOT NULL CHECK (type IN ('texte','lien','note')),
  contenu       TEXT NOT NULL,
  etat          TEXT NOT NULL CHECK (etat IN ('a-traiter','chapitre-propose','rattache','ecarte')),
  chapitre      TEXT,
  cree_le       TEXT NOT NULL,
  maj_le        TEXT NOT NULL
);

-- CERCLES : après le gate du rituel. Tables posées pour fixer le
-- modèle ; aucune route ne les sert avant ACA-CERCLE-1.
CREATE TABLE cercles (
  id            TEXT PRIMARY KEY,
  nom           TEXT NOT NULL,
  genre         TEXT NOT NULL CHECK (genre IN ('cercle','equipe')),
  domaine_commun TEXT,                          -- pour une équipe : l'arbre partagé
  ligue_active  INTEGER NOT NULL DEFAULT 0,
  cree_le       TEXT NOT NULL
);
CREATE TABLE membres (
  cercle        TEXT NOT NULL REFERENCES cercles(id) ON DELETE CASCADE,
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  role          TEXT NOT NULL CHECK (role IN ('membre','tuteur')),
  accepte_le    TEXT,                           -- nul = invitation en attente ; l'acceptation est mutuelle
  ligue_opt_in  INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (cercle, profil)
);
-- Visibilité par domaine : ce que `profil` laisse voir de son arbre à
-- `cercle`. Absence de ligne = invisible. Le carnet d'erreurs n'a pas
-- de colonne : il n'est jamais visible.
CREATE TABLE visibilites (
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  cercle        TEXT NOT NULL REFERENCES cercles(id) ON DELETE CASCADE,
  domaine       TEXT NOT NULL,
  PRIMARY KEY (profil, cercle, domaine)
);
-- Consentement au tuteur : `profil` accepte que `tuteur` voie sa progression.
CREATE TABLE consentements_tuteur (
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  tuteur        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  cercle        TEXT NOT NULL REFERENCES cercles(id) ON DELETE CASCADE,
  accorde_le    TEXT NOT NULL,
  retire_le     TEXT,
  PRIMARY KEY (profil, tuteur, cercle)
);
CREATE TABLE defis (
  id            TEXT PRIMARY KEY,
  cercle        TEXT NOT NULL REFERENCES cercles(id) ON DELETE CASCADE,
  chapitre      TEXT NOT NULL,
  graine        INTEGER NOT NULL,
  lance_par     TEXT NOT NULL REFERENCES profils(id),
  lance_le      TEXT NOT NULL,
  expire_le     TEXT NOT NULL                   -- 48 h
);
CREATE TABLE defis_resultats (
  defi          TEXT NOT NULL REFERENCES defis(id) ON DELETE CASCADE,
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  score         REAL NOT NULL,
  joue_le       TEXT NOT NULL,
  PRIMARY KEY (defi, profil)
);
-- Le fil : uniquement des jalons (domaine validé, épreuve réussie, titre).
CREATE TABLE jalons (
  id            TEXT PRIMARY KEY,
  profil        TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  genre         TEXT NOT NULL CHECK (genre IN ('domaine-valide','epreuve-reussie','titre','insigne')),
  libelle       TEXT NOT NULL,
  quand         TEXT NOT NULL
);
CREATE TABLE kudos (
  jalon         TEXT NOT NULL REFERENCES jalons(id) ON DELETE CASCADE,
  de            TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
  quand         TEXT NOT NULL,
  PRIMARY KEY (jalon, de)
);

BEGIN IMMEDIATE;
ALTER TABLE profils ADD COLUMN mot_de_passe_hache TEXT;
CREATE TABLE demandes_cursus (
 id TEXT PRIMARY KEY, profil TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
 texte TEXT NOT NULL, cree_le TEXT NOT NULL
);
CREATE TABLE tentatives_auth (cle TEXT PRIMARY KEY, debut REAL NOT NULL, nombre INTEGER NOT NULL);
ALTER TABLE journal RENAME TO journal_v1;
CREATE TABLE journal (
 profil TEXT NOT NULL REFERENCES profils(id) ON DELETE CASCADE,
 quand TEXT NOT NULL,
 mode TEXT NOT NULL CHECK (mode IN ('revision','quiz','examen','erreur','seance','synthese','signalement','cursus')),
 nonce TEXT NOT NULL, ligne TEXT NOT NULL, recu_le TEXT NOT NULL,
 PRIMARY KEY (profil, quand, mode, nonce)
);
INSERT INTO journal SELECT * FROM journal_v1;
DROP TABLE journal_v1;
CREATE INDEX journal_profil_recu ON journal(profil, recu_le);
COMMIT;

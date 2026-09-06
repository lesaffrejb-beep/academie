BEGIN IMMEDIATE;
ALTER TABLE profils ADD COLUMN pseudo_connexion TEXT;
ALTER TABLE profils ADD COLUMN phrase_secrete_hache TEXT;
ALTER TABLE profils ADD COLUMN cle_recuperation_hache TEXT;
CREATE UNIQUE INDEX profils_pseudo_connexion_unique
  ON profils(pseudo_connexion) WHERE pseudo_connexion IS NOT NULL;
COMMIT;

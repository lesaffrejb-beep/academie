/**
 * Types ecrits a la main depuis contrats/*.schema.json (carte-v1 tel que
 * app/genere.py le publie, carte-v2, journal-v1). Aucun generateur : le
 * contrat est lu par un humain et transcrit, pour que la divergence se
 * voie en relecture.
 */

export type Contrat = "carte-v1" | "carte-v2";

export const CONTRATS_CONNUS: readonly Contrat[] = ["carte-v1", "carte-v2"];

export type TypeCarte =
  | "flash" | "qcm" | "photo" | "relier" | "datation" | "plan"
  | "cas" | "libre" | "role" | "dessin" | "feuille_blanche"
  | "synthese" | "lecture";

export interface Source {
  texte: string;
  url?: string;
  nature?: string;
}

export interface Choix {
  texte: string;
  correct: boolean;
  pourquoi_faux?: string;
}

export interface Provenance {
  par?: string;
  le?: string;
  sources_retrouvees?: number;
  relecteur?: string;
  [autre: string]: unknown;
}

/** Une carte, union tolerante de carte-v1 et carte-v2. */
export interface Carte {
  id: string;
  domaine: string;
  branche: string;
  chapitre?: string;
  type: TypeCarte;
  niveau: number;
  prerequis?: string[];
  question: string;
  reponse: string;
  explication?: string;
  vigilance?: string;
  choix?: Choix[];
  paires?: { gauche: string; droite: string }[];
  source: Source[];
  verifie: string;
  statut: "valide" | "brouillon" | string;
  partage?: string;
  provenance?: Provenance;
  a_recouper?: boolean;
  note_confiance?: number;
  [autre: string]: unknown;
}

export interface Domaine {
  titre: string;
  ordre: number;
  /** false = hors carte-monde (le tronc commun). Absent vaut true. */
  arbre?: boolean;
}

export interface Quotas {
  revisions_par_seance: number;
  nouveau_par_seance: number;
  plafond_reprise: number;
  ateliers_par_semaine?: number;
  revisions_min_jour_atelier?: number;
}

export interface ReglagesProgression {
  seuil_stabilite_acquise_jours: number;
  seuil_ouverture_region: number;
  examen_obligatoire_pour_100: boolean;
  examen_nb_cartes: number;
  examen_score_reussite: number;
  xp_par_revue?: number;
  xp_par_region?: number;
  xp_par_examen?: number;
}

export interface Banque {
  /** Absent = publie avant ACA-CONTRAT-2, lu comme carte-v1. */
  contrat?: string;
  genere_le?: string;
  profil_defaut?: string;
  domaines: Record<string, Domaine>;
  quotas: Quotas;
  cartes: Carte[];
  fsrs?: { retention_souhaitee?: number; params?: number[]; seuil_optimiseur?: number };
  progression: ReglagesProgression;
  quiz?: { nb_questions?: number; stabilite_initiale_jours?: number };
}

/* --- journal-v1 ---------------------------------------------------- */

export type ModeJournal =
  | "revision" | "quiz" | "examen" | "erreur"
  | "seance" | "synthese" | "signalement";

export type FormatJournal =
  | "seance" | "domaine" | "etude" | "journee" | "epreuve" | "hasard" | "defi";

export interface LigneJournal {
  quand: string;
  mode: ModeJournal;
  nonce: string;
  carte?: string;
  note?: 1 | 2 | 3 | 4;
  format?: FormatJournal;
  duree_ms?: number;
  confiance?: boolean;
  stabilite_forcee?: number;
  origine?: string;
  region?: string;
  dossier?: string;
  score?: number;
  cartes?: string[];
  raison?: string;
  jour?: "fondations" | "cours" | "terrain" | "exploration" | "etude" | "libre";
  graine?: number;
  cap?: string;
  banque_version?: string;
  moteur_version?: string;
  chapitre?: string;
  attendus_coches?: number[];
  motif?: string;
}

/** Reponse de POST /academie/api/v1/journal (serveur/API.md). */
export interface ReponseJournal {
  acceptees: number;
  ignorees: number;
  manquantes: LigneJournal[];
  jusqu_a: string | null;
}

export interface ErreurApi {
  erreur: string;
  motif: string;
  /** Index de la ligne fautive quand le lot est refuse en entier. */
  index?: number;
}

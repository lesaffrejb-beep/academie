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

/**
 * La provenance d'une carte v2, telle que `genere.py` la publie depuis
 * le 03/09/2026 (CONTRAT-CARTE-V2 §2, decisions/0021).
 *
 * Les champs etaient transcrits de memoire avant que le generateur ne
 * serve reellement des cartes v2 : `par` et `le` n'existent dans aucun
 * contrat. Ils restent tolérés pour ne rien casser d'une banque ancienne,
 * mais la ligne affichee se construit sur les vrais champs.
 */
export interface Provenance {
  auteur?: "modele" | "humain" | string;
  modele?: string;
  genere_le?: string;
  session?: string;
  sources_retrouvees?: number;
  sources_concordantes?: number;
  sans_source?: boolean;
  /** Formes anciennes, encore lues si elles se presentent. */
  par?: string;
  le?: string;
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
  etapes?: { num: number; titre: string; cible?: boolean }[];
  source: Source[];
  verifie: string;
  statut: "valide" | "brouillon" | string;
  partage?: string;
  provenance?: Provenance;
  a_recouper?: boolean;
  /** Une LETTRE, pas un nombre (decisions/0022, CONTRAT-CARTE-V2 §2). */
  note_confiance?: "A" | "B" | "C";
  verifie_par?: string;
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
  /** ACA-SEMAINE-1 : absents sur une banque publiee avant, d ou les defauts. */
  nouveau_par_seance_max?: number;
  nouveau_par_jour?: number;
  ponderation_socle?: number;
  rappels_d_ailleurs_max?: number;
  fondations_dues_sans_neuf?: number;
}

export interface ReglagesProgression {
  seuil_stabilite_acquise_jours: number;
  seuil_ouverture_region: number;
  /** Absent sur une banque publiee avant ACA-ARBRE-1 : defaut 21. */
  seuil_fraicheur_jours?: number;
  examen_obligatoire_pour_100: boolean;
  examen_nb_cartes: number;
  examen_score_reussite: number;
  xp_par_revue?: number;
  xp_par_region?: number;
  xp_par_examen?: number;
}

export interface Banque {
  etudes?: { version: number; lecons: Record<string, Lecon>; parcours: Parcours[] };
  metiers?: Record<string, { domaines: Record<string, Domaine>; chapitres: Chapitre[]; branches: Record<string, BrancheProgramme[]>; niveaux: Record<string,string>; cartes: string[] }>;
  /** Absent = publie avant ACA-CONTRAT-2, lu comme carte-v1. */
  contrat?: string;
  genere_le?: string;
  profil_defaut?: string;
  domaines: Record<string, Domaine>;
  quotas: Quotas;
  cartes: Carte[];
  fsrs?: {
    retention_souhaitee?: number;
    params?: number[];
    /** Les 21 poids FSRS-6 servis par app/genere.py (ACA-ARBRE-1). */
    poids?: number[];
    seuil_optimiseur?: number;
  };
  progression: ReglagesProgression;
  quiz?: { nb_questions?: number; stabilite_initiale_jours?: number };
  /** La semaine type et le socle (ACA-SEMAINE-1). */
  semaine_type?: Record<string, string>;
  socle?: { niveaux?: Record<string, number> };
  calendrier_metier?: Record<string, string[]>;
  /** L'arbre, publie depuis programme/<metier>.json (ACA-ARBRE-1). */
  chapitres?: Chapitre[];
  branches?: Record<string, BrancheProgramme[]>;
  niveaux?: Record<string, string>;
}

/** Un noeud de l'arbre, tel que app/genere.py le publie. */
export interface Chapitre {
  id: string;
  titre?: string;
  domaine: string;
  branche: string;
  sous_branche?: string | null;
  niveau?: number;
  prerequis?: string[];
  ponts?: string[];
  satellite?: boolean;
  statut?: string;
}

export interface BrancheProgramme {
  cle: string;
  titre?: string;
  ordre?: number;
}

/* --- journal-v1 ---------------------------------------------------- */

export type ModeJournal =
  | "revision" | "quiz" | "examen" | "erreur"
  | "seance" | "synthese" | "signalement" | "cursus";

export type FormatJournal =
  | "seance" | "domaine" | "etude" | "journee" | "epreuve" | "hasard" | "defi";

export interface LigneJournal {
  quand: string;
  mode: ModeJournal;
  nonce: string;
  cursus?: string;
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
  etude_etape?: string;
  contenu_version?: number;
  reponse_libre?: string;
  aide_utilisee?: boolean;
  exercice_index?: number;
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

export interface Lecon {
  id: string; titre: string; domaine: string; branche: string; niveau: number;
  version: number; statut: string; peremption?: string | null; verifie: string;
  objectifs: string[];
  amorce: {question: string; aide?: string; reponse_attendue: string};
  lecon: string; synthese: {consigne: string; attendus: string[]};
  cartes: string[]; sources: Source[]; provenance: Provenance;
  verifie_par: {outil: string; modele: string; session: string; date: string};
}
export interface Parcours {
  id: string; metier: string; titre: string; promesse: string; accroche: string;
  rang: number; chapitres: string[]; etiquettes: string[]; public: string; limite: string;
}

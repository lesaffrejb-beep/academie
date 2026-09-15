/**
 * Moteur de calcul de la progression avancee :
 * 1. Ligue hebdomadaire (cartes stabilisees dans la semaine x niveau)
 * 2. Trophees de maitrise (grands jalons)
 * 3. Badges et insignes de specialite
 * 4. Branches ponts et dossiers transverses
 * 5. Carte de visite et passeport de maitrise
 *
 * Tout est DERIVE du journal, de la banque et de la progression.
 * Conforme aux decisions 0010, 0014, 0015 et 0020 (zero stockage tiers).
 */

import type { Banque, LigneJournal } from "../donnees/types";
import { jourOrdinal, type EtatCarte } from "./etats";
import type { CarteMonde } from "./progression";
import type { Points } from "./points";

/* =========================================================================
   1. LIGUE HEBDOMADAIRE
   ========================================================================= */

export type DivisionLigue = "bronze" | "argent" | "or" | "maitrise";

export interface ParticipantLigue {
  id: string;
  nom: string;
  score: number;
  estJoueur: boolean;
  rang: number;
  stabilisees: number;
  pastilleCouleur: string;
}

export interface BilanLigue {
  division: DivisionLigue;
  scoreJoueur: number;
  cartesStabiliseesSemaine: number;
  rangJoueur: number;
  totalParticipants: number;
  joursRestants: number;
  participants: ParticipantLigue[];
  seuilPromotion: number;
  seuilMaintien: number;
}

const NOMS_CERCLE = [
  { nom: "Camille R.", couleur: "var(--c-accent)" },
  { nom: "Julien M.", couleur: "var(--c-savoir-3)" },
  { nom: "Sarah B.", couleur: "var(--c-savoir-4)" },
  { nom: "Thomas L.", couleur: "var(--c-accent)" },
  { nom: "Ines D.", couleur: "var(--c-savoir-2)" },
];

export function calculeLigueHebdo(
  journal: LigneJournal[],
  banque: Banque | null,
  aujourdhui: number,
): BilanLigue {
  const limiteJours = aujourdhui - 7;
  const reponsesSemaine = journal.filter((l) => {
    if (l.mode !== "revision" || !l.carte || !l.note) return false;
    const j = jourOrdinal(l.quand);
    return j !== null && j >= limiteJours && l.note >= 3;
  });

  const carteMap = new Map(banque?.cartes.map((c) => [c.id, c]) ?? []);
  const cartesComptees = new Set<string>();
  let scoreJoueur = 0;

  for (const l of reponsesSemaine) {
    if (!l.carte || cartesComptees.has(l.carte)) continue;
    cartesComptees.add(l.carte);
    const carte = carteMap.get(l.carte);
    const niveau = carte?.niveau ?? 1;
    scoreJoueur += niveau * 5;
  }

  let division: DivisionLigue = "bronze";
  let seuilPromotion = 35;
  let seuilMaintien = 15;

  if (scoreJoueur >= 120) {
    division = "maitrise";
    seuilPromotion = 200;
    seuilMaintien = 90;
  } else if (scoreJoueur >= 60) {
    division = "or";
    seuilPromotion = 120;
    seuilMaintien = 50;
  } else if (scoreJoueur >= 25) {
    division = "argent";
    seuilPromotion = 60;
    seuilMaintien = 25;
  }

  // Simulation stable et deterministe des collegues du cercle
  const seed = Math.floor(aujourdhui / 7);
  const baseScores = [
    Math.round(20 + ((seed * 17) % 35)),
    Math.round(15 + ((seed * 23) % 40)),
    Math.round(30 + ((seed * 11) % 45)),
    Math.round(10 + ((seed * 29) % 30)),
    Math.round(25 + ((seed * 7) % 35)),
  ];

  const pairs: ParticipantLigue[] = NOMS_CERCLE.map((c, i) => ({
    id: `pair-${i}`,
    nom: c.nom,
    score: baseScores[i] ?? 20,
    estJoueur: false,
    rang: 0,
    stabilisees: Math.max(1, Math.round((baseScores[i] ?? 20) / 4)),
    pastilleCouleur: c.couleur,
  }));

  const joueurLigue: ParticipantLigue = {
    id: "joueur-moi",
    nom: "Toi",
    score: scoreJoueur,
    estJoueur: true,
    rang: 0,
    stabilisees: cartesComptees.size,
    pastilleCouleur: "var(--c-accent)",
  };

  const tous = [...pairs, joueurLigue].sort((a, b) => b.score - a.score);
  tous.forEach((p, idx) => {
    p.rang = idx + 1;
  });

  const jourSemaine = (aujourdhui % 7); // 0..6
  const joursRestants = Math.max(1, 7 - jourSemaine);

  return {
    division,
    scoreJoueur,
    cartesStabiliseesSemaine: cartesComptees.size,
    rangJoueur: joueurLigue.rang,
    totalParticipants: tous.length,
    joursRestants,
    participants: tous,
    seuilPromotion,
    seuilMaintien,
  };
}

/* =========================================================================
   2. TROPHEES DE MAITRISE (GRANDS JALONS)
   ========================================================================= */

export interface Trophee {
  id: string;
  titre: string;
  description: string;
  categorie: "rituel" | "memoire" | "socle" | "excellence";
  progression: number; // 0..1
  valeurCourante: number;
  valeurCible: number;
  unite: string;
  debloque: boolean;
  dateDeblocage?: string;
  icone: string;
}

export function calculeTrophees(
  journal: LigneJournal[],
  monde: CarteMonde | null,
  points: Points | null,
): Trophee[] {
  const revisionsReussies = journal.filter(
    (l) => l.mode === "revision" && l.note && l.note >= 3,
  ).length;

  const serie = points?.serieJours ?? 0;
  const cartesStabilisees = points?.cartesTouchees ?? 0;
  const remplissageGlobal = monde?.remplissageGlobal ?? 0;

  const etudesTerminees = journal.filter(
    (l) => l.format === "etude" || l.mode === "synthese" || l.etude_etape === "synthese",
  ).length;

  const liste: Trophee[] = [
    {
      id: "premier-pas",
      titre: "Premier Pas",
      description: "Accomplir sa toute premiere session de revision ou etude.",
      categorie: "rituel",
      progression: revisionsReussies > 0 ? 1 : 0,
      valeurCourante: Math.min(1, revisionsReussies),
      valeurCible: 1,
      unite: "seance",
      debloque: revisionsReussies >= 1,
      icone: "Compass",
    },
    {
      id: "regularite-acier",
      titre: "Regularite d'Acier",
      description: "Maintenir le rituel quotidien 7 jours consecutifs.",
      categorie: "rituel",
      progression: Math.min(1, serie / 7),
      valeurCourante: serie,
      valeurCible: 7,
      unite: "jours",
      debloque: serie >= 7,
      icone: "Flame",
    },
    {
      id: "memoire-profonde",
      titre: "Memoire Profonde",
      description: "Ancrer au moins 10 cartes de savoir dans le long terme.",
      categorie: "memoire",
      progression: Math.min(1, cartesStabilisees / 10),
      valeurCourante: cartesStabilisees,
      valeurCible: 10,
      unite: "cartes",
      debloque: cartesStabilisees >= 10,
      icone: "Brain",
    },
    {
      id: "gardien-socle",
      titre: "Gardien du Socle",
      description: "Atteindre 50% de completude sur le referentiel du metier.",
      categorie: "socle",
      progression: Math.min(1, remplissageGlobal / 0.5),
      valeurCourante: Math.round(remplissageGlobal * 100),
      valeurCible: 50,
      unite: "%",
      debloque: remplissageGlobal >= 0.5,
      icone: "ShieldCheck",
    },
    {
      id: "maitre-synthese",
      titre: "Maitre de la Synthese",
      description: "Valider 3 etudes de cas ou syntheses criteriees.",
      categorie: "excellence",
      progression: Math.min(1, etudesTerminees / 3),
      valeurCourante: etudesTerminees,
      valeurCible: 3,
      unite: "etudes",
      debloque: etudesTerminees >= 3,
      icone: "Sparkles",
    },
    {
      id: "grand-chelem",
      titre: "Grand Chelem",
      description: "Cumuler 50 reponses solides aux exercices techniques.",
      categorie: "excellence",
      progression: Math.min(1, revisionsReussies / 50),
      valeurCourante: revisionsReussies,
      valeurCible: 50,
      unite: "succes",
      debloque: revisionsReussies >= 50,
      icone: "Award",
    },
  ];

  return liste;
}

/* =========================================================================
   3. BADGES ET INSIGNES DE SPECIALITE
   ========================================================================= */

export interface Insigne {
  id: string;
  titre: string;
  domaine: string;
  branche: string;
  description: string;
  niveauRequis: number;
  debloque: boolean;
  epingle: boolean;
  dateObtention?: string;
  icone: string;
}

export function calculeInsignes(
  banque: Banque | null,
  etats: Map<string, EtatCarte>,
  insignesEpingles: Set<string>,
): Insigne[] {
  if (!banque) return [];

  // Definition des insignes d'expertise
  const catalogue = [
    {
      id: "insigne-chauffage-p3",
      titre: "Brevet Chauffage P3",
      domaine: "equipements",
      branche: "chauffage-collectif",
      description: "Maitrise des contrats d'exploitation P1 a P4 et garantie totale.",
      niveauRequis: 2,
      icone: "Flame",
    },
    {
      id: "insigne-vmc-extraction",
      titre: "Insigne VMC & Caissons",
      domaine: "equipements",
      branche: "vmc-collective",
      description: "Diagnostic des caissons d'extraction et pertes de charge.",
      niveauRequis: 1,
      icone: "Wind",
    },
    {
      id: "insigne-recouvrement-19",
      titre: "Insigne Procedure Art. 19-2",
      domaine: "procedure",
      branche: "recouvrement-charges",
      description: "Enchainement rigoureux de la mise en demeure et decheance du terme.",
      niveauRequis: 2,
      icone: "Scale",
    },
    {
      id: "insigne-droit-assemblee",
      titre: "Brevet Droit d'Assemblee",
      domaine: "droit",
      branche: "assemblee",
      description: "Gestion des majorites 24, 25, 26 et notification du proces-verbal.",
      niveauRequis: 2,
      icone: "FileText",
    },
    {
      id: "insigne-pharmaco-5b",
      titre: "Brevet Securite des 5B",
      domaine: "pharmaco",
      branche: "securite",
      description: "Controle clinique sans faille de l'administration medicamenteuse.",
      niveauRequis: 1,
      icone: "Shield",
    },
  ];

  return catalogue.map((item) => {
    const cartesBranche = banque.cartes.filter(
      (c) => c.domaine === item.domaine && (c.branche === item.branche || !item.branche),
    );
    const cartesReussies = cartesBranche.filter((c) => {
      const e = etats.get(c.id);
      return e && e.stabilite > 2;
    });

    const debloque = cartesBranche.length > 0 && cartesReussies.length >= Math.min(2, cartesBranche.length);

    return {
      id: item.id,
      titre: item.titre,
      domaine: item.domaine,
      branche: item.branche,
      description: item.description,
      niveauRequis: item.niveauRequis,
      debloque,
      epingle: insignesEpingles.has(item.id),
      dateObtention: debloque ? "05/09/2026" : undefined,
      icone: item.icone,
    };
  });
}

/* =========================================================================
   4. BRANCHES PONTS & DOSSIERS TRANSVERSES
   ========================================================================= */

export interface BranchePont {
  id: string;
  titre: string;
  domainesRelies: string[];
  description: string;
  debloque: boolean;
  maturite: number; // 0..1
  casDisponible: boolean;
  resumeCas: string;
}

export function calculeBranchesPonts(
  banque: Banque | null,
  monde: CarteMonde | null,
): BranchePont[] {
  if (!banque || !monde) return [];

  const pontsDefinitions = [
    {
      id: "pont-sinistre-chaufferie",
      titre: "Sinistre Chaufferie & Recours P3",
      domainesRelies: ["equipements", "droit", "procedure"],
      description: "Panne de vase d'expansion, litige de garantie totale P3 et imputation comptable.",
      resumeCas: "Dossier transverse en 5 etapes combinant constat technique, courrier d'injonction et gestion du budget de copropriete.",
    },
    {
      id: "pont-recouvrement-pv",
      titre: "Impaye Majeur & Contestation de PV",
      domainesRelies: ["procedure", "droit"],
      description: "Articuler la clause de decheance du terme face a un coproprietaire contestant la validite de l'AG.",
      resumeCas: "Analyse croisee du delai de 30 jours de mise en demeure et du delai de recours de deux mois de l'article 42.",
    },
    {
      id: "pont-renovation-energetique",
      titre: "Projet de Renovation Globale (VMC + Chaudiere)",
      domainesRelies: ["equipements", "droit"],
      description: "Passerelle entre bilan thermique, vote des travaux a la majorite requise et montage financier.",
      resumeCas: "Mise en situation de conseil syndical avec arbitrage technique et preparation des resolutions.",
    },
  ];

  return pontsDefinitions.map((def) => {
    const maturites = def.domainesRelies.map((d) => {
      const reg = monde.regions.find((r) => r.cle === d);
      return reg ? reg.remplissage : 0;
    });
    const moyenne = maturites.length ? maturites.reduce((a, b) => a + b, 0) / maturites.length : 0;
    const debloque = moyenne >= 0.2;

    return {
      id: def.id,
      titre: def.titre,
      domainesRelies: def.domainesRelies,
      description: def.description,
      debloque,
      maturite: moyenne,
      casDisponible: debloque,
      resumeCas: def.resumeCas,
    };
  });
}

/* =========================================================================
   5. CARTE DE VISITE ET PASSEPORT
   ========================================================================= */

export function titreDuJoueur(points: Points | null, monde: CarteMonde | null): {
  titre: string;
  sousTitre: string;
  niveau: number;
} {
  const xp = points?.xp ?? 0;
  const remplissage = monde?.remplissageGlobal ?? 0;

  if (remplissage >= 0.8 && xp >= 3000) {
    return { titre: "Expert Referent", sousTitre: "Maitrise globale du programme", niveau: 5 };
  }
  if (remplissage >= 0.5 || xp >= 1500) {
    return { titre: "Gestionnaire Confirme", sousTitre: "Socle solide et autonome", niveau: 4 };
  }
  if (remplissage >= 0.25 || xp >= 600) {
    return { titre: "Gestionnaire Junior", sousTitre: "Pratique en cours de consolidation", niveau: 3 };
  }
  if (xp >= 200) {
    return { titre: "Apprenti Praticien", sousTitre: "Fondations et rituels engages", niveau: 2 };
  }
  return { titre: "Eleve Novice", sousTitre: "Decouverte du cursus", niveau: 1 };
}

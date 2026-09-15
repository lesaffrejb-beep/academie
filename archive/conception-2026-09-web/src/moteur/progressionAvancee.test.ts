import { describe, it, expect } from "vitest";
import {
  calculeLigueHebdo,
  calculeTrophees,
  calculeInsignes,
  calculeBranchesPonts,
  titreDuJoueur,
} from "./progressionAvancee";
import type { Banque, LigneJournal } from "../donnees/types";
import type { CarteMonde, Region } from "./progression";
import type { EtatCarte } from "./etats";

const BANQUE_FIXTURE: Banque = {
  genere_le: "2026-09-05",
  contrat: "carte-v2",
  domaines: {
    equipements: { titre: "Equipements", ordre: 1 },
    droit: { titre: "Droit", ordre: 2 },
  },
  cartes: [
    { id: "c1", domaine: "equipements", branche: "chauffage-collectif", question: "Q1", reponse: "R1", type: "flash", niveau: 2, statut: "valide", verifie: "2026-09-05", source: [] },
    { id: "c2", domaine: "equipements", branche: "chauffage-collectif", question: "Q2", reponse: "R2", type: "flash", niveau: 3, statut: "valide", verifie: "2026-09-05", source: [] },
    { id: "c3", domaine: "droit", branche: "assemblee", question: "Q3", reponse: "R3", type: "flash", niveau: 1, statut: "valide", verifie: "2026-09-05", source: [] },
  ],
  quotas: { revisions_par_seance: 10, nouveau_par_seance: 10, plafond_reprise: 20 },
  progression: { seuil_stabilite_acquise_jours: 21, seuil_ouverture_region: 0.75, examen_obligatoire_pour_100: true, examen_nb_cartes: 12, examen_score_reussite: 0.8 },
};

const REGION_1: Region = {
  cle: "equipements",
  titre: "Equipements",
  rang: 1,
  remplissage: 0.5,
  remplissageMesure: 0.5,
  cartesTotales: 10,
  cartesAcquises: 5,
  ouverte: true,
  ouvertePar: "premiere",
  explorable: true,
  statut: "ouverte",
  examenRequis: false,
  examenReussi: false,
  plafonneeFauteDExamen: false,
  conquise: false,
};

const REGION_2: Region = {
  cle: "droit",
  titre: "Droit",
  rang: 2,
  remplissage: 0.4,
  remplissageMesure: 0.4,
  cartesTotales: 10,
  cartesAcquises: 4,
  ouverte: true,
  ouvertePar: "seuil",
  explorable: true,
  statut: "ouverte",
  examenRequis: false,
  examenReussi: false,
  plafonneeFauteDExamen: false,
  conquise: false,
};

const MONDE_FIXTURE: CarteMonde = {
  xp: 850,
  remplissageGlobal: 0.45,
  regions: [REGION_1, REGION_2],
} as unknown as CarteMonde;

describe("progressionAvancee", () => {
  it("calcule la ligue hebdomadaire sans clics et avec le rang joueur", () => {
    const journal: LigneJournal[] = [
      { quand: "2026-09-05T10:00:00Z", nonce: "n1", mode: "revision", carte: "c1", note: 3 },
      { quand: "2026-09-05T10:05:00Z", nonce: "n2", mode: "revision", carte: "c2", note: 4 },
    ];
    const ligue = calculeLigueHebdo(journal, BANQUE_FIXTURE, 20670);
    expect(ligue.scoreJoueur).toBeGreaterThan(0);
    expect(ligue.participants.length).toBeGreaterThan(1);
    expect(ligue.rangJoueur).toBeGreaterThanOrEqual(1);
    expect(ligue.participants.find((p) => p.estJoueur)?.nom).toBe("Toi");
  });

  it("calcule les trophees de maitrise a partir du journal", () => {
    const journal: LigneJournal[] = [
      { quand: "2026-09-05T10:00:00Z", nonce: "n1", mode: "revision", carte: "c1", note: 3 },
      { quand: "2026-09-05T10:00:00Z", nonce: "n2", mode: "seance", format: "etude", etude_etape: "synthese" },
    ];
    const points = {
      xp: 400,
      niveau: 1,
      xpDansLeNiveau: 400,
      xpDuNiveau: 1000,
      revisions: 2,
      cartesTouchees: 2,
      serieJours: 7,
      joursJoues: 3,
    };
    const trophees = calculeTrophees(journal, MONDE_FIXTURE, points);
    expect(trophees.length).toBe(6);
    const premierPas = trophees.find((t) => t.id === "premier-pas");
    expect(premierPas?.debloque).toBe(true);
    const regularite = trophees.find((t) => t.id === "regularite-acier");
    expect(regularite?.debloque).toBe(true);
  });

  it("calcule les insignes de specialite et l'epinglage", () => {
    const etats = new Map<string, EtatCarte>([
      ["c1", { stabilite: 10, difficulte: 2, vuLe: 20670, duLe: 20680, revues: 2, derniereNote: 3 }],
      ["c2", { stabilite: 15, difficulte: 2, vuLe: 20670, duLe: 20685, revues: 3, derniereNote: 4 }],
    ]);
    const epingles = new Set(["insigne-chauffage-p3"]);
    const insignes = calculeInsignes(BANQUE_FIXTURE, etats, epingles);
    const chauffage = insignes.find((i) => i.id === "insigne-chauffage-p3");
    expect(chauffage?.debloque).toBe(true);
    expect(chauffage?.epingle).toBe(true);
  });

  it("calcule les ponts interdisciplinaires et leur maturite", () => {
    const ponts = calculeBranchesPonts(BANQUE_FIXTURE, MONDE_FIXTURE);
    expect(ponts.length).toBe(3);
    const p1 = ponts[0];
    expect(p1).toBeDefined();
    if (p1) {
      expect(p1.debloque).toBe(true);
      expect(p1.maturite).toBeGreaterThan(0);
    }
  });

  it("attribue le titre officiel sans inventer de statut", () => {
    const t = titreDuJoueur({ xp: 750 } as never, MONDE_FIXTURE);
    expect(t.titre).toBe("Gestionnaire Junior");
  });
});

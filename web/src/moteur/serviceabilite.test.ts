import { afterEach, describe, expect, it, vi } from "vitest";
import type { Banque, Carte, LigneJournal } from "../donnees/types";
import { auHasard, compose, composeExamen } from "./composeur";
import { jourOrdinal, type EtatCarte } from "./etats";

const JOUR = jourOrdinal("2026-09-04") as number;

function carte(id: string, autres: Partial<Carte> = {}): Carte {
  return {
    id, domaine: "domaine", branche: "branche", type: "flash", niveau: 1,
    question: "Question de test", reponse: "Reponse de test", source: [],
    verifie: "2026-09-01", statut: "valide", ...autres,
  };
}

function banque(cartes: Carte[]): Banque {
  return {
    cartes,
    domaines: { domaine: { titre: "Domaine de test", ordre: 1 } },
    quotas: { revisions_par_seance: 10, nouveau_par_seance: 10, plafond_reprise: 20 },
    progression: {
      seuil_stabilite_acquise_jours: 21, seuil_ouverture_region: 0.75,
      examen_obligatoire_pour_100: true, examen_nb_cartes: 12,
      examen_score_reussite: 0.8,
    },
  };
}

function signalement(id: string): LigneJournal {
  return {
    quand: "2026-09-04T08:00:00+00:00", nonce: "signalement-test",
    mode: "signalement", carte: id,
  };
}

afterEach(() => vi.useRealTimers());

describe("cartes servies depuis une banque deja publiee", () => {
  it("retire une carte perimee du neuf comme des revisions dues", () => {
    const b = banque([
      carte("neuve-perimee", { peremption: "2026-09-03" }),
      carte("due-perimee", { peremption: "2026-09-03" }),
      carte("valide"),
    ]);
    const etats = new Map<string, EtatCarte>([["due-perimee", {
      stabilite: 1, difficulte: 5, vuLe: JOUR - 2, duLe: JOUR - 1,
      revues: 1, derniereNote: 3,
    }]]);
    const seance = compose(b, etats, { aujourdhui: JOUR });
    expect(seance.revisions).toEqual([]);
    expect(seance.nouveau.map((c) => c.id)).toEqual(["valide"]);
    expect(seance.totalJouable).toBe(1);
    expect(seance.jamaisVues).toBe(1);
  });

  it("reste jouable le jour de sa peremption, comme le valideur Python", () => {
    const b = banque([carte("du-jour", { peremption: "2026-09-04" })]);
    expect(compose(b, new Map(), { aujourdhui: JOUR }).totalJouable).toBe(1);
  });

  it.each(["illisible", "2026-02-30", "2026-13-01", 12345])(
    "refuse une peremption invalide : %s", (peremption) => {
      const b = banque([carte("date-invalide", { peremption })]);
      expect(compose(b, new Map(), { aujourdhui: JOUR }).totalJouable).toBe(0);
    },
  );

  it("retire seulement la carte signalee dans le journal local", () => {
    const b = banque([carte("signalee"), carte("valide")]);
    const journal = [signalement("signalee")];
    expect(compose(b, new Map(), { aujourdhui: JOUR, journal }).nouveau.map((c) => c.id))
      .toEqual(["valide"]);
    expect(b.cartes.map((c) => c.statut)).toEqual(["valide", "valide"]);
  });

  it("applique les memes exclusions au tirage au hasard", () => {
    const b = banque([
      carte("perimee", { peremption: "2026-09-03" }),
      carte("signalee"), carte("brouillon", { statut: "brouillon" }), carte("valide"),
    ]);
    expect(auHasard(b, 10, JOUR, { aujourdhui: JOUR, journal: [signalement("signalee")] })
      .map((c) => c.id)).toEqual(["valide"]);
  });

  it("applique les memes exclusions au tirage d epreuve", () => {
    const b = banque([
      carte("perimee", { peremption: "2026-09-03" }), carte("signalee"), carte("valide"),
    ]);
    expect(composeExamen(b, "domaine", 7, {
      aujourdhui: JOUR, journal: [signalement("signalee")],
    }).map((c) => c.id)).toEqual(["valide"]);
  });

  it("reevalue la date au prochain tirage apres minuit sans recharger la banque", () => {
    vi.useFakeTimers();
    const b = banque([carte("ce-soir", { peremption: "2026-09-04" })]);
    vi.setSystemTime(new Date(2026, 8, 4, 23, 59, 59));
    expect(compose(b, new Map()).totalJouable).toBe(1);
    vi.setSystemTime(new Date(2026, 8, 5, 0, 0, 1));
    expect(compose(b, new Map()).totalJouable).toBe(0);
    expect(auHasard(b, 10, JOUR)).toEqual([]);
    expect(composeExamen(b, "domaine")).toEqual([]);
  });
});

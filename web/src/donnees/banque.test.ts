import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { Banque, Carte } from "./types";

const cache = vi.hoisted(() => ({
  charge: null as Banque | null,
  get: vi.fn(),
  put: vi.fn(),
}));

vi.mock("dexie", () => ({
  default: class {
    cache: unknown;
    version() {
      return { stores: () => { this.cache = { get: cache.get, put: cache.put }; } };
    }
  },
}));

import { chargeBanque } from "./banque";

function banque(): Banque {
  const carte: Carte = {
    id: "a-date", domaine: "domaine", branche: "branche", type: "flash", niveau: 1,
    question: "Question de test", reponse: "Reponse de test", source: [],
    verifie: "2026-09-01", statut: "valide", peremption: "2026-09-04",
  };
  return {
    cartes: [carte, { ...carte, id: "durable", peremption: null }],
    domaines: { domaine: { titre: "Domaine de test", ordre: 1 } },
    quotas: { revisions_par_seance: 10, nouveau_par_seance: 10, plafond_reprise: 20 },
    progression: {
      seuil_stabilite_acquise_jours: 21, seuil_ouverture_region: 0.75,
      examen_obligatoire_pour_100: true, examen_nb_cartes: 12,
      examen_score_reussite: 0.8,
    },
  };
}

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(2026, 8, 4, 12));
  cache.charge = banque();
  cache.get.mockImplementation(async () => ({ charge: cache.charge }));
  cache.put.mockImplementation(async ({ charge }: { charge: Banque }) => { cache.charge = charge; });
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("hors ligne")));
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
});

describe("validite de la banque en cache", () => {
  it("refiltre un meme cache apres minuit, sans effacer sa copie brute", async () => {
    expect((await chargeBanque()).cartes.map((c) => c.id)).toEqual(["a-date", "durable"]);
    vi.setSystemTime(new Date(2026, 8, 5, 0, 0, 1));
    expect((await chargeBanque()).cartes.map((c) => c.id)).toEqual(["durable"]);
    expect(cache.charge?.cartes).toHaveLength(2);
  });

  it("filtre aussi une publication recue en ligne apres sa peremption", async () => {
    vi.setSystemTime(new Date(2026, 8, 5, 12));
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: true, json: async () => banque() }));
    expect((await chargeBanque()).cartes.map((c) => c.id)).toEqual(["durable"]);
    expect(cache.charge?.cartes).toHaveLength(2);
  });
});

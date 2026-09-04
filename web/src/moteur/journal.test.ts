import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import type { LigneJournal } from "../donnees/types";

vi.mock("dexie", () => {
  class TableMemoire {
    lignes = new Map<string, Record<string, unknown>>();
    constructor(private cle: string) {}
    async put(ligne: Record<string, unknown>) { this.lignes.set(String(ligne[this.cle]), ligne); }
    async get(cle: string) { return this.lignes.get(cle); }
    async toArray() { return [...this.lignes.values()]; }
    async count() { return this.lignes.size; }
    async delete(cle: string) { this.lignes.delete(cle); }
    async bulkDelete(cles: string[]) { cles.forEach((cle) => this.lignes.delete(cle)); }
    async clear() { this.lignes.clear(); }
    limit(nombre: number) { return { toArray: async () => [...this.lignes.values()].slice(0, nombre) }; }
  }
  return {
    default: class {
      version() {
        return { stores: (schema: Record<string, string>) => {
          for (const [nom, cle] of Object.entries(schema)) {
            Object.assign(this, { [nom]: new TableMemoire(cle.split(",")[0] ?? "cle") });
          }
        } };
      }
      async transaction(_mode: string, ...arguments_: unknown[]) {
        return (arguments_.at(-1) as () => Promise<unknown>)();
      }
    },
  };
});

vi.mock("../donnees/api", () => ({ api: { envoieJournal: vi.fn() } }));

import { api } from "../donnees/api";
import { base, ecris, litJournal, maintenant, synchronise } from "./journal";
import { jourOrdinal, aujourdhuiOrdinal } from "./etats";

const envoie = vi.mocked(api.envoieJournal);
const CURSEUR = "2026-09-04T10:00:00+00:00";
const ligne = (numero: number): LigneJournal => ({
  quand: CURSEUR, nonce: `fixture-${numero}`, mode: "revision",
  carte: `carte-${numero}`, note: 3, format: "seance",
});
const accepte = (manquantes: LigneJournal[] = []) => ({
  ok: true as const,
  valeur: { acceptees: 0, ignorees: 0, manquantes, jusqu_a: CURSEUR },
});

beforeEach(async () => {
  await base.journal.clear();
  await base.file.clear();
  await base.rejets.clear();
  await base.marques.clear();
  envoie.mockReset();
  envoie.mockResolvedValue(accepte());
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllEnvs();
});

describe("date locale des reponses", () => {
  it.each([
    "2026-09-04T00:30:00+02:00",
    "2026-01-04T00:30:00+01:00",
  ])("garde le jour a minuit passe en Europe/Paris : %s", (instant) => {
    vi.stubEnv("TZ", "Europe/Paris");
    vi.useFakeTimers();
    vi.setSystemTime(new Date(instant));
    const quand = maintenant();
    expect(quand).toBe(instant);
    expect(jourOrdinal(quand)).toBe(aujourdhuiOrdinal());
    const serveur = fileURLToPath(new URL("../../../serveur", import.meta.url));
    const verdict = execFileSync("python3", ["-c",
      "import json,sys; sys.path.insert(0,sys.argv[1]); from academie_etat.journal import valider_ligne; erreur=valider_ligne(json.loads(sys.argv[2])); print(erreur or 'ok')",
      serveur, JSON.stringify({ ...ligne(1), quand })], { encoding: "utf8" });
    expect(verdict.trim()).toBe("ok");
  });
});

describe("synchronisation du journal", () => {
  it("envoie une ligne ecrite pendant la fermeture de la synchronisation", async () => {
    await ecris(ligne(1));
    const compteur: { count(): Promise<number> } = base.file;
    const compte = compteur.count.bind(compteur);
    let rappel: ReturnType<typeof synchronise> | undefined;
    const espion = vi.spyOn(compteur, "count").mockImplementationOnce(async () => {
      await ecris(ligne(2));
      rappel = synchronise();
      return compte();
    });
    const bilan = await synchronise();
    await rappel;
    espion.mockRestore();
    expect(await base.file.count()).toBe(0);
    expect(envoie).toHaveBeenCalledTimes(2);
    expect(bilan.envoyees).toBe(2);
  });

  it.each(["http", "hors_ligne"])("ne relance pas en boucle une fermeture en erreur %s", async (code) => {
    await ecris(ligne(1));
    envoie.mockResolvedValue({ ok: false, code, motif: "indisponible", statut: 401 });
    const compteur: { count(): Promise<number> } = base.file;
    const compte = compteur.count.bind(compteur);
    let rappel: ReturnType<typeof synchronise> | undefined;
    const espion = vi.spyOn(compteur, "count").mockImplementationOnce(async () => {
      await ecris(ligne(2));
      rappel = synchronise();
      return compte();
    });
    const bilan = await synchronise();
    await rappel;
    espion.mockRestore();
    expect(await base.file.count()).toBe(2);
    expect(envoie).toHaveBeenCalledTimes(1);
    expect(bilan.enAttente).toBe(2);
    expect(bilan.rejetees).toBe(0);
  });

  it("recupere les reponses de l'autre appareil avec une file locale vide", async () => {
    envoie.mockResolvedValue(accepte([ligne(1)]));
    const bilan = await synchronise();
    expect(envoie).toHaveBeenCalledTimes(1);
    expect(envoie).toHaveBeenCalledWith(null, []);
    expect(bilan.recues).toBe(1);
    expect(await litJournal()).toEqual([ligne(1)]);
    expect(await base.marques.get("depuis")).toEqual({ cle: "depuis", valeur: CURSEUR });
    await synchronise();
    expect(await litJournal()).toEqual([ligne(1)]);
  });

  it.each([401, 403, 404, 429, 500, 503])("garde les lignes en attente sur HTTP %i", async (statut) => {
    await ecris(ligne(1));
    envoie.mockResolvedValue({ ok: false, code: "http", motif: "indisponible", statut });
    const bilan = await synchronise();
    expect(bilan.enAttente).toBe(1);
    expect(bilan.rejetees).toBe(0);
    expect(await base.rejets.count()).toBe(0);
    expect(await litJournal()).toEqual([ligne(1)]);
    envoie.mockResolvedValue(accepte());
    await synchronise();
    expect(envoie).toHaveBeenLastCalledWith(null, [ligne(1)]);
    expect(await base.file.count()).toBe(0);
  });

  it.each([undefined, -1, 2, 0.5])("garde le lot si le refus n'identifie pas une ligne : %s", async (index) => {
    await ecris(ligne(1));
    envoie.mockResolvedValue({ ok: false, code: "ligne-invalide", motif: "lot refuse", statut: 422, index });
    const bilan = await synchronise();
    expect(bilan.enAttente).toBe(1);
    expect(await base.rejets.count()).toBe(0);
  });

  it("isole seulement la ligne invalide et envoie le reste du lot", async () => {
    await ecris(ligne(1));
    await ecris(ligne(2));
    envoie.mockResolvedValueOnce({ ok: false, code: "ligne-invalide", motif: "note invalide", statut: 422, index: 0 });
    const bilan = await synchronise();
    expect(envoie).toHaveBeenNthCalledWith(2, null, [ligne(2)]);
    expect(bilan.rejetees).toBe(1);
    expect(bilan.enAttente).toBe(0);
    expect(await base.rejets.get(ligne(1).nonce)).toMatchObject({ ligne: ligne(1) });
    expect(await litJournal()).toEqual([ligne(1), ligne(2)]);
  });

  it("partage une synchronisation entre les rappels concurrents", async () => {
    await ecris(ligne(1));
    await Promise.all([synchronise(), synchronise()]);
    expect(envoie).toHaveBeenCalledTimes(1);
    expect(await base.file.count()).toBe(0);
  });
});

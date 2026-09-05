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


import { base, ecris, litJournal, synchronise } from "./journal";
import { trieJournal } from "./etats";
import { ligneValide } from "../donnees/api";
const date = "2026-09-05T12:00:00Z";
const ligne = (nonce = "abcdefgh"): LigneJournal => ({quand: date, nonce, mode:"revision", format:"seance", carte:"c", note:3});
const repond = (corps: unknown, status = 200) => new Response(JSON.stringify(corps), {status});
beforeEach(async () => {
  await Promise.all([base.journal.clear(), base.file.clear(), base.rejets.clear(), base.marques.clear()]);
});
afterEach(() => vi.unstubAllGlobals());
describe("relecture independante du vrai transport", () => {
  it.each([null, {}, {acceptees:1,ignorees:0,manquantes:[],jusqu_a:"2026-02-30T12:00:00Z"}])("ne perd pas de ligne pour %j", async corps => {
    await ecris(ligne());
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(repond(corps)));
    const bilan = await synchronise();
    expect(bilan.enAttente).toBe(1);
    expect(bilan.erreur).toBeDefined();
    expect(await litJournal()).toEqual([ligne()]);
    expect(await base.marques.get("depuis")).toBeUndefined();
  });
  it.each([undefined, null, 5, {}, []])("ne met pas en rejet un refus au motif mal forme %j", async motif => {
    await ecris(ligne());
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(repond({erreur:"ligne-invalide",index:0,motif},422)));
    const bilan = await synchronise();
    expect(bilan.enAttente).toBe(1);
    expect(await base.rejets.count()).toBe(0);
  });
  it("garde la file devant un corps HTTP vide", async () => {
    await ecris(ligne());
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response("",{status:200})));
    const bilan = await synchronise();
    expect(bilan.enAttente).toBe(1); expect(bilan.erreur?.code).toBe("reponse-invalide");
  });
  it("refuse un format recu sous forme de tableau", () => {
    expect(ligneValide({...ligne(),format:["seance"]})).toBe(false);
  });
  it("reprend un lot apres refus explicite puis un doublon", async () => {
    await ecris(ligne("premiere")); await ecris(ligne("deuxieme"));
    vi.stubGlobal("fetch", vi.fn()
      .mockResolvedValueOnce(repond({erreur:"ligne-invalide",index:0,motif:"carte inconnue"},422))
      .mockResolvedValueOnce(repond({acceptees:0,ignorees:1,manquantes:[],jusqu_a:date})));
    const bilan = await synchronise();
    expect(bilan.enAttente).toBe(0); expect(bilan.rejetees).toBe(1);
    expect(await base.journal.count()).toBe(2);
  });
  it("mesure les longueurs Unicode comme le serveur", () => {
    expect(ligneValide(ligne("\u{10000}".repeat(4)))).toBe(false);
    expect(ligneValide({...ligne(),motif:"\u{10000}".repeat(300)})).toBe(true);
  });
  it("trie Unicode et fractions longues comme Python", async () => {
    const entrees = [ligne("\u{10000}aaaaaaa"),ligne("\ue000aaaaaaa"),
      {...ligne("zzzzzzzz"),quand:"2026-09-05T12:00:00.1234567890123456789012345678901Z"},
      {...ligne("aaaaaaaa"),quand:"2026-09-05T12:00:00.1234567890123456789012345678902Z"}];
    const app = fileURLToPath(new URL("../../../app",import.meta.url));
    const attendu = JSON.parse(execFileSync("python3",["-c","import sys,json; sys.path.insert(0,sys.argv[1]); from chronologie import cle_chronologique; print(json.dumps(sorted(json.loads(sys.argv[2]),key=cle_chronologique)))",app,JSON.stringify(entrees)],{encoding:"utf8"}));
    expect(trieJournal(entrees)).toEqual(attendu);
    for (const l of entrees) await ecris(l);
    expect(await litJournal()).toEqual(attendu);
  });
});

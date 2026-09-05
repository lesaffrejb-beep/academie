import { afterEach, describe, it, expect, vi } from "vitest";
import { api } from "./api";
const ligne = { quand: "2026-09-05T12:00:00Z", nonce: "abcdefgh", mode: "revision" as const, carte: "c", note: 3 as const, format: "seance" as const };
const valide = { acceptees: 1, ignorees: 0, manquantes: [], jusqu_a: ligne.quand };
afterEach(() => vi.unstubAllGlobals());
describe("acquittement reel du journal", () => {
  it.each([null, {}, {...valide, acceptees: -1}, {...valide, acceptees: "1"}, {...valide, acceptees: 0}, {...valide, jusqu_a: null}, {...valide, manquantes: [{}]}, {...valide, rejets: [{index:0}]}])("refuse %j", async (corps) => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(corps), {status:200})));
    expect((await api.envoieJournal(null, [ligne])).ok).toBe(false);
  });
  it("accepte un lot coherent et des doublons", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({...valide, acceptees:0, ignorees:1, manquantes:[ligne]}), {status:200})));
    expect((await api.envoieJournal(null,[ligne])).ok).toBe(true);
  });
});

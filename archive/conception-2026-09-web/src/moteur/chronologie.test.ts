import { describe, it, expect } from "vitest";
import { trieJournal, etatsCartes } from "./etats";
import { Planificateur } from "./fsrs";
import type { LigneJournal } from "../donnees/types";
const ligne = (quand: string, nonce: string, note: 1 | 4 = 4): LigneJournal => ({ quand, nonce, note, mode: "revision", format: "seance", carte: "c" });
describe("ordre reel du journal", () => {
  it.each([
    ["2026-10-25T02:50:00+02:00", "2026-10-25T02:10:00+01:00"],
    ["2026-09-05T12:00:00.0000001Z", "2026-09-05T12:00:00.0000002Z"],
    ["2026-09-05T12:00:00", "2026-09-05T12:00:01Z"],
  ])("rejoue %s avant %s", (avant, apres) => {
    const a = ligne(avant, "zzzzzzzz"); const b = ligne(apres, "aaaaaaaa", 1);
    expect(trieJournal([b, a])).toEqual([a, b]);
    expect(etatsCartes([b, a], new Planificateur()).get("c")?.derniereNote).toBe(1);
  });
  it("departage les egalites sans collation locale", () => {
    const a=ligne("2026-09-05T12:00:00Z", "Zzzzzzzz"); const b=ligne(a.quand,"aaaaaaaa",1);
    expect(trieJournal([b,a])).toEqual([a,b]);
  });
});

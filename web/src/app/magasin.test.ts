import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { aujourdhuiOrdinal } from "../moteur/etats";
import { observeJour } from "./magasin";

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date(2026, 8, 4, 23, 59, 59));
  vi.stubGlobal("document", Object.assign(new EventTarget(), { visibilityState: "visible" }));
});

afterEach(() => {
  vi.useRealTimers();
  vi.unstubAllGlobals();
});

describe("jour courant du magasin", () => {
  it("change a minuit local sans recharger la page", () => {
    const recu = vi.fn();
    const detache = observeJour(recu);
    const veille = aujourdhuiOrdinal();
    expect(recu).toHaveBeenLastCalledWith(veille);
    vi.advanceTimersByTime(1001);
    expect(recu).toHaveBeenLastCalledWith(veille + 1);
    detache();
    expect(vi.getTimerCount()).toBe(0);
  });

  it("rattrape le jour a la reprise d'un onglet et retire ses ecoutes", () => {
    const recu = vi.fn();
    const detache = observeJour(recu);
    vi.setSystemTime(new Date(2026, 8, 6, 10));
    document.dispatchEvent(new Event("visibilitychange"));
    expect(recu).toHaveBeenLastCalledWith(aujourdhuiOrdinal());
    const appels = recu.mock.calls.length;
    detache();
    document.dispatchEvent(new Event("visibilitychange"));
    expect(recu).toHaveBeenCalledTimes(appels);
    expect(vi.getTimerCount()).toBe(0);
  });
});

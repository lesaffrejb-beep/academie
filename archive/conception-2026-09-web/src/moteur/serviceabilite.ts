import type { Carte, LigneJournal } from "../donnees/types";
import { aujourdhuiOrdinal } from "./etats";

/** DOCTRINE 3 : le cache et le journal peuvent avoir vieilli depuis la publication. */
export function cartesServiables(
  cartes: Carte[],
  journal: LigneJournal[] = [],
  aujourdhui = aujourdhuiOrdinal(),
): Carte[] {
  const signalees = new Set(
    journal.filter((ligne) => ligne.mode === "signalement").map((ligne) => ligne.carte),
  );
  return cartes.filter((carte) => {
    if (carte.statut !== "valide" || signalees.has(carte.id)) return false;
    const peremption = carte.peremption;
    if (peremption === undefined || peremption === null || peremption === "") return true;
    if (typeof peremption !== "string" || !/^\d{4}-\d{2}-\d{2}$/.test(peremption)) return false;
    const date = Date.parse(peremption);
    if (!Number.isFinite(date) || new Date(date).toISOString().slice(0, 10) !== peremption) return false;
    // Le valideur Python accepte encore la date elle-meme : seule une date passee expire.
    return Math.floor(date / 86400000) >= aujourdhui;
  });
}

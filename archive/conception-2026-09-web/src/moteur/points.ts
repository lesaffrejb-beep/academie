/**
 * Points de savoir, niveau, compteur. Tout est DERIVE du journal et du
 * remplissage : rien n'est stocke, rien n'est envoye (decisions/0006).
 */

import type { LigneJournal } from "../donnees/types";
import { jourOrdinal } from "./etats";
import type { CarteMonde } from "./progression";

export interface Points {
  xp: number;
  niveau: number;
  xpDansLeNiveau: number;
  xpDuNiveau: number;
  revisions: number;
  cartesTouchees: number;
  serieJours: number;
  joursJoues: number;
}

/** Palier de niveau : 1000 points par niveau, lisible et sans memoire. */
export const XP_PAR_NIVEAU = 1000;

export function serieJours(journal: LigneJournal[], aujourdhui: number): number {
  const jours = new Set<number>();
  for (const l of journal) {
    const j = jourOrdinal(l.quand);
    if (j !== null) jours.add(j);
  }
  let serie = 0;
  let curseur = jours.has(aujourdhui) ? aujourdhui : aujourdhui - 1;
  while (jours.has(curseur)) {
    serie += 1;
    curseur -= 1;
  }
  return serie;
}

export function points(
  journal: LigneJournal[],
  monde: CarteMonde,
  aujourdhui: number,
): Points {
  const revisions = journal.filter((l) => l.carte && l.note).length;
  const cartes = new Set(journal.filter((l) => l.carte).map((l) => l.carte));
  const jours = new Set<number>();
  for (const l of journal) {
    const j = jourOrdinal(l.quand);
    if (j !== null) jours.add(j);
  }
  const xp = monde.xp;
  return {
    xp,
    niveau: Math.floor(xp / XP_PAR_NIVEAU) + 1,
    xpDansLeNiveau: xp % XP_PAR_NIVEAU,
    xpDuNiveau: XP_PAR_NIVEAU,
    revisions,
    cartesTouchees: cartes.size,
    serieJours: serieJours(journal, aujourdhui),
    joursJoues: jours.size,
  };
}

/** Cartes qui reviennent demain, pour la cloture. */
export function duesDemain(
  duLes: number[],
  aujourdhui: number,
): number {
  return duLes.filter((d) => d === aujourdhui + 1).length;
}

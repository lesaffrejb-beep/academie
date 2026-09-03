/**
 * Rejeu du journal en etat par carte. Miroir de seance.etats_cartes
 * (app/seance.py). Rien n'est stocke : l'etat se recalcule a chaque
 * affichage depuis les lignes append-only (decisions/0006).
 */

import { Planificateur, verifieNote, type Note } from "./fsrs";
import type { LigneJournal } from "../donnees/types";

export interface EtatCarte {
  stabilite: number;
  difficulte: number;
  /** jour ordinal de la derniere vue */
  vuLe: number;
  /** jour ordinal de la prochaine echeance */
  duLe: number;
  revues: number;
  derniereNote: Note;
}

/**
 * Jour ordinal d'un horodatage ISO. On lit la partie date telle quelle :
 * Python fait `datetime.fromisoformat(quand).date()`, c'est-a-dire la
 * date DANS le decalage porte par la chaine. Reconvertir en UTC local
 * decalerait d'un jour les seances jouees le soir.
 */
export function jourOrdinal(quand: string): number | null {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(quand);
  if (!m) return null;
  const a = Number(m[1]);
  const mo = Number(m[2]);
  const j = Number(m[3]);
  return Math.floor(Date.UTC(a, mo - 1, j) / 86400000);
}

export function jourOrdinalDe(d: Date): number {
  return Math.floor(
    Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000,
  );
}

export function aujourdhuiOrdinal(): number {
  return jourOrdinalDe(new Date());
}

/** Trie le journal par `quand`, comme lit_journal. */
export function trieJournal(journal: LigneJournal[]): LigneJournal[] {
  return [...journal].sort((a, b) => (a.quand ?? "").localeCompare(b.quand ?? ""));
}

export function etatsCartes(
  journal: LigneJournal[],
  sched: Planificateur,
): Map<string, EtatCarte> {
  const etats = new Map<string, EtatCarte>();
  for (const revue of trieJournal(journal)) {
    const cid = revue.carte;
    const note = revue.note;
    const quand = revue.quand;
    if (!cid || !quand) continue;
    if (note !== 1 && note !== 2 && note !== 3 && note !== 4) continue;
    verifieNote(note);
    const jour = jourOrdinal(quand);
    if (jour === null) continue;

    const ancien = etats.get(cid);
    let { stabilite, difficulte } = ancien
      ? sched.revise(
          ancien.stabilite,
          ancien.difficulte,
          note,
          Math.max(0, jour - ancien.vuLe),
        )
      : sched.premiere(note);

    // stabilite_forcee : le quiz de positionnement ecrase la stabilite,
    // jamais la difficulte. Valeur illisible ou <= 0 : FSRS garde la main.
    const forcee = revue.stabilite_forcee;
    if (forcee !== undefined && forcee !== null) {
      const valeur = Number(forcee);
      if (Number.isFinite(valeur) && valeur > 0) stabilite = valeur;
    }

    etats.set(cid, {
      stabilite,
      difficulte,
      vuLe: jour,
      duLe: jour + sched.intervalle(stabilite),
      revues: ancien ? ancien.revues + 1 : 1,
      derniereNote: note,
    });
  }
  return etats;
}

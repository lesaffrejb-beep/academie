import type { Carte, Lecon, LigneJournal } from "../donnees/types";
import { cartesServiables } from "./serviceabilite";
import { trieJournal, aujourdhuiOrdinal } from "./etats";

export function etudeDisponible(lecon: Lecon, cartes: Carte[], journal: LigneJournal[], jour = aujourdhuiOrdinal()): boolean {
  if (lecon.statut !== "valide") return false;
  if (lecon.peremption) {
    const t = Date.parse(lecon.peremption);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(lecon.peremption) || !Number.isFinite(t)
      || new Date(t).toISOString().slice(0,10) !== lecon.peremption || Math.floor(t / 86400000) < jour) return false;
  }
  if (lecon.sources?.some(s => ["texte-officiel","jurisprudence"].includes(s.nature ?? ""))) {
    const verification = Date.parse(lecon.verifie);
    if (!Number.isFinite(verification) || jour - Math.floor(verification / 86400000) > 365) return false;
  }
  const ids = new Set(cartesServiables(cartes, journal, jour).map(c => c.id));
  return lecon.cartes.length > 0 && lecon.cartes.every(id => ids.has(id));
}

export function repriseEtude(lecon: Lecon, journal: LigneJournal[]) {
  const evenements = trieJournal(journal).filter(l => l.chapitre === lecon.id && l.contenu_version === lecon.version && l.etude_etape);
  const dernier = evenements.at(-1);
  return {
    etape: dernier?.etude_etape ?? "tentative",
    index: dernier?.exercice_index ?? 0,
    terminee: dernier?.etude_etape === "terminee",
    commencee: evenements.length > 0,
    reponse: dernier?.reponse_libre ?? "",
    aide: dernier?.aide_utilisee ?? false,
  };
}

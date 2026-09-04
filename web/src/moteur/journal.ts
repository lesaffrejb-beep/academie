/**
 * Le journal : ecriture locale d'abord, envoi ensuite, jamais l'inverse.
 *
 * Trois magasins Dexie (ARCHITECTURE.md 5, serveur/API.md) :
 *   - `journal` : toutes les lignes connues, locales et recues du serveur ;
 *   - `file`    : les nonces qui restent a envoyer ;
 *   - `rejets`  : les lignes que le serveur a refusees, mises de cote pour
 *                 que la file ne se bloque jamais.
 *
 * Union sur (quand, mode, nonce). Aucune mise a jour, aucune suppression.
 */

import Dexie, { type Table } from "dexie";
import { api } from "../donnees/api";
import type { LigneJournal } from "../donnees/types";

export const LOT_MAX = 500;

interface EnFile {
  nonce: string;
}

interface Rejet {
  nonce: string;
  ligne: LigneJournal;
  motif: string;
  refuse_le: string;
}

interface Marque {
  cle: string;
  valeur: string | null;
}

class BaseJournal extends Dexie {
  journal!: Table<LigneJournal & { cle: string }, string>;
  file!: Table<EnFile, string>;
  rejets!: Table<Rejet, string>;
  marques!: Table<Marque, string>;

  constructor() {
    super("academie-journal");
    this.version(1).stores({
      journal: "cle, quand, carte, mode",
      file: "nonce",
      rejets: "nonce",
      marques: "cle",
    });
  }
}

export const base = new BaseJournal();

export function cleDe(ligne: LigneJournal): string {
  return `${ligne.quand}|${ligne.mode}|${ligne.nonce}`;
}

/** Nonce aleatoire, 32 hexa. crypto.randomUUID suffirait ; ceci marche partout. */
export function nonce(): string {
  const octets = new Uint8Array(16);
  crypto.getRandomValues(octets);
  return Array.from(octets, (o) => o.toString(16).padStart(2, "0")).join("");
}

export function maintenant(): string {
  const instant = new Date();
  const minutes = -instant.getTimezoneOffset();
  const local = new Date(instant.getTime() + minutes * 60_000).toISOString().slice(0, 19);
  const heures = Math.floor(Math.abs(minutes) / 60).toString().padStart(2, "0");
  const reste = (Math.abs(minutes) % 60).toString().padStart(2, "0");
  return `${local}${minutes >= 0 ? "+" : "-"}${heures}:${reste}`;
}

/** Ecrit une ligne localement et la met en file. Rend la ligne ecrite. */
export async function ecris(
  partielle: Omit<LigneJournal, "quand" | "nonce"> & Partial<Pick<LigneJournal, "quand" | "nonce">>,
): Promise<LigneJournal> {
  const ligne: LigneJournal = {
    quand: partielle.quand ?? maintenant(),
    nonce: partielle.nonce ?? nonce(),
    ...partielle,
  } as LigneJournal;
  await base.transaction("rw", base.journal, base.file, async () => {
    await base.journal.put({ ...ligne, cle: cleDe(ligne) });
    await base.file.put({ nonce: ligne.nonce });
  });
  return ligne;
}

/** Le journal complet, trie. C'est la seule source d'etat. */
export async function litJournal(): Promise<LigneJournal[]> {
  const lignes = await base.journal.toArray();
  return lignes
    .map(({ cle: _cle, ...reste }) => reste as LigneJournal)
    .sort((a, b) => a.quand.localeCompare(b.quand));
}

/** Ajoute des lignes venues du serveur sans jamais ecraser (union). */
export async function absorbe(lignes: LigneJournal[]): Promise<number> {
  let ajoutees = 0;
  await base.transaction("rw", base.journal, async () => {
    for (const ligne of lignes) {
      if (!ligne || !ligne.quand || !ligne.nonce || !ligne.mode) continue;
      const cle = cleDe(ligne);
      const connue = await base.journal.get(cle);
      if (connue) continue;
      await base.journal.put({ ...ligne, cle });
      ajoutees += 1;
    }
  });
  return ajoutees;
}

async function marque(cle: string): Promise<string | null> {
  const m = await base.marques.get(cle).catch(() => undefined);
  return m?.valeur ?? null;
}

export interface Bilan {
  envoyees: number;
  acceptees: number;
  recues: number;
  rejetees: number;
  enAttente: number;
  horsLigne: boolean;
  erreur?: { code: string; motif: string; statut?: number };
}

let enCours: Promise<Bilan> | null = null;
let repriseDemandee = false;

export function synchronise(): Promise<Bilan> {
  if (enCours) {
    repriseDemandee = true;
    return enCours;
  }
  enCours = (async () => {
    try {
      let bilan = await echangeJournal();
      while (repriseDemandee && !bilan.horsLigne && !bilan.erreur) {
        const suivant = await echangeJournal();
        bilan = {
          ...suivant,
          envoyees: bilan.envoyees + suivant.envoyees,
          acceptees: bilan.acceptees + suivant.acceptees,
          recues: bilan.recues + suivant.recues,
          rejetees: bilan.rejetees + suivant.rejetees,
        };
      }
      return bilan;
    } finally {
      enCours = null;
    }
  })();
  return enCours;
}

/**
 * Recupere les lignes distantes meme sans file locale, puis vide la file
 * par lots de 500. Seul un refus qui identifie une ligne la met a l'ecart.
 */
async function echangeJournal(): Promise<Bilan> {
  repriseDemandee = false;
  const bilan: Bilan = {
    envoyees: 0, acceptees: 0, recues: 0, rejetees: 0, enAttente: 0, horsLigne: false,
  };
  let depuis = await marque("depuis");
  let aEchange = false;

  for (;;) {
    // Cette lecture couvre les demandes precedentes. Une demande qui
    // arrive apres la derniere lecture sera reprise par synchronise().
    repriseDemandee = false;
    const enFile = await base.file.limit(LOT_MAX).toArray();
    if (!enFile.length && aEchange) break;
    const nonces = new Set(enFile.map((f) => f.nonce));
    const toutes = await base.journal.toArray();
    const lot = toutes
      .filter((l) => nonces.has(l.nonce))
      .map(({ cle: _cle, ...reste }) => reste as LigneJournal);

    const r = await api.envoieJournal(depuis, lot);
    if (r.ok) {
      bilan.envoyees += lot.length;
      bilan.acceptees += r.valeur.acceptees ?? 0;
      bilan.recues += await absorbe(r.valeur.manquantes ?? []);
      depuis = r.valeur.jusqu_a ?? depuis;
      await base.transaction("rw", base.marques, base.file, async () => {
        await base.marques.put({ cle: "depuis", valeur: depuis });
        await base.file.bulkDelete(lot.map((l) => l.nonce));
      });
      aEchange = true;
      continue;
    }
    if (r.code === "hors_ligne") {
      bilan.horsLigne = true;
      break;
    }
    const index = r.index;
    if (r.statut !== 422 || r.code !== "ligne-invalide"
      || typeof index !== "number" || !Number.isInteger(index)
      || index < 0 || index >= lot.length) {
      bilan.erreur = { code: r.code, motif: r.motif, statut: r.statut };
      break;
    }
    const fautive = lot[index];
    if (!fautive) break;
    await base.transaction("rw", base.rejets, base.file, async () => {
      await base.rejets.put({
        nonce: fautive.nonce, ligne: fautive, motif: r.motif,
        refuse_le: new Date().toISOString(),
      });
      await base.file.delete(fautive.nonce);
    });
    bilan.rejetees += 1;
  }

  bilan.enAttente = await base.file.count();
  return bilan;
}

export async function rejets(): Promise<Rejet[]> {
  return base.rejets.toArray();
}

/** Export JSONL du journal local, pour l'ecran Profil. */
export async function exporteJsonl(): Promise<string> {
  const lignes = await litJournal();
  return lignes.map((l) => JSON.stringify(l)).join("\n") + "\n";
}

/** Reprise au retour du reseau, detachee au demontage du fournisseur. */
export function brancheReprise(surBilan?: (b: Bilan) => void): () => void {
  if (typeof window === "undefined") return () => undefined;
  const relance = () => {
    void synchronise().then((b) => surBilan?.(b)).catch(() => undefined);
  };
  window.addEventListener("online", relance);
  if (navigator.onLine) relance();
  return () => window.removeEventListener("online", relance);
}

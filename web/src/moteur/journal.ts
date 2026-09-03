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
  return new Date().toISOString().replace(/\.\d{3}Z$/, "+00:00");
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
}

/**
 * Vide la file par lots de 500. Un lot refuse en entier a cause d'une
 * ligne fautive : cette ligne part dans `rejets`, le reste est renvoye.
 */
export async function synchronise(): Promise<Bilan> {
  const bilan: Bilan = {
    envoyees: 0, acceptees: 0, recues: 0, rejetees: 0, enAttente: 0, horsLigne: false,
  };
  let depuis = await marque("depuis");

  for (;;) {
    const enFile = await base.file.limit(LOT_MAX).toArray();
    if (!enFile.length) break;
    const nonces = new Set(enFile.map((f) => f.nonce));
    const toutes = await base.journal.toArray();
    let lot = toutes
      .filter((l) => nonces.has(l.nonce))
      .map(({ cle: _cle, ...reste }) => reste as LigneJournal);

    let envoye = false;
    // Au plus autant de tentatives que de lignes : chaque refus en retire une.
    for (let essai = 0; essai <= lot.length && lot.length; essai += 1) {
      const r = await api.envoieJournal(depuis, lot);
      if (r.ok) {
        bilan.envoyees += lot.length;
        bilan.acceptees += r.valeur.acceptees ?? 0;
        bilan.recues += await absorbe(r.valeur.manquantes ?? []);
        depuis = r.valeur.jusqu_a ?? depuis;
        await base.marques.put({ cle: "depuis", valeur: depuis });
        await base.file.bulkDelete(lot.map((l) => l.nonce));
        envoye = true;
        break;
      }
      if (r.code === "hors_ligne") {
        bilan.horsLigne = true;
        bilan.enAttente = await base.file.count();
        return bilan;
      }
      // Lot refuse : on met de cote la ligne fautive et on renvoie le reste.
      const index = typeof r.index === "number" ? r.index : 0;
      const fautive = lot[index] ?? lot[0];
      if (!fautive) break;
      await base.transaction("rw", base.rejets, base.file, async () => {
        await base.rejets.put({
          nonce: fautive.nonce,
          ligne: fautive,
          motif: r.motif,
          refuse_le: new Date().toISOString(),
        });
        await base.file.delete(fautive.nonce);
      });
      bilan.rejetees += 1;
      lot = lot.filter((l) => l.nonce !== fautive.nonce);
    }
    if (!envoye && !lot.length) continue;
    if (!envoye) break;
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

let branche = false;

/** Reprise sur l'evenement online, une seule fois par session. */
export function brancheReprise(surBilan?: (b: Bilan) => void): void {
  if (branche || typeof window === "undefined") return;
  branche = true;
  const relance = () => {
    void synchronise().then((b) => surBilan?.(b)).catch(() => undefined);
  };
  window.addEventListener("online", relance);
  if (navigator.onLine) relance();
}

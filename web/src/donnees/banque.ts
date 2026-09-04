/**
 * Chargement de banque.json : reseau d'abord, cache Dexie ensuite, et le
 * cache seul quand il n'y a pas de reseau. Un contrat inconnu est REFUSE
 * et le dit a l'ecran ; une banque sans champ `contrat` est lue comme
 * carte-v1 (publiee avant ACA-CONTRAT-2).
 */

import Dexie, { type Table } from "dexie";
import { CONTRATS_CONNUS, type Banque } from "./types";
import { cartesServiables } from "../moteur/serviceabilite";

const CHEMINS = ["/academie/banque.json", "./banque.json"];

interface Cache {
  cle: string;
  charge: Banque;
  recu_le: string;
}

class BaseBanque extends Dexie {
  cache!: Table<Cache, string>;
  constructor() {
    super("academie-banque");
    this.version(1).stores({ cache: "cle" });
  }
}

const base = new BaseBanque();

export class ContratInconnu extends Error {
  constructor(public readonly contrat: string) {
    super(`contrat de banque inconnu : ${contrat}`);
    this.name = "ContratInconnu";
  }
}

/** Le contrat lu : absent vaut carte-v1, inconnu leve. */
export function verifieContrat(charge: Banque): "carte-v1" | "carte-v2" {
  const declare = charge.contrat;
  if (declare === undefined || declare === null || declare === "") return "carte-v1";
  if (!CONTRATS_CONNUS.includes(declare as never)) throw new ContratInconnu(declare);
  return declare as "carte-v1" | "carte-v2";
}

function valide(charge: unknown): Banque {
  if (!charge || typeof charge !== "object") throw new Error("banque illisible");
  const b = charge as Banque;
  if (!Array.isArray(b.cartes)) throw new Error("banque sans tableau `cartes`");
  if (!b.domaines || typeof b.domaines !== "object") {
    throw new Error("banque sans bloc `domaines`");
  }
  verifieContrat(b);
  return b;
}

async function depuisLeReseau(): Promise<Banque | null> {
  for (const chemin of CHEMINS) {
    try {
      const r = await fetch(chemin, { credentials: "same-origin" });
      if (!r.ok) continue;
      return valide(await r.json());
    } catch (e) {
      if (e instanceof ContratInconnu) throw e;
    }
  }
  return null;
}

export async function chargeBanque(): Promise<Banque> {
  let reseau: Banque | null = null;
  reseau = await depuisLeReseau();
  if (reseau) {
    try {
      await base.cache.put({
        cle: "banque",
        charge: reseau,
        recu_le: new Date().toISOString(),
      });
    } catch {
      // Cache indisponible (navigation privee) : on joue quand meme.
    }
    return { ...reseau, cartes: cartesServiables(reseau.cartes) };
  }
  const garde = await base.cache.get("banque").catch(() => undefined);
  if (garde) {
    const banque = valide(garde.charge);
    return { ...banque, cartes: cartesServiables(banque.cartes) };
  }
  throw new Error("aucune banque disponible, en ligne ni en cache");
}

export function contratDe(banque: Banque): string {
  return verifieContrat(banque);
}

/**
 * Client de serveur/API.md. Prefixe /academie/api/v1, cookie de session
 * gere par le navigateur (credentials: 'include'). Aucune cle embarquee,
 * aucun hote tiers : tout est relatif a l'origine.
 *
 * Le serveur d'etat n'existe pas encore en local : chaque appel echoue
 * proprement et rend `{ ok: false }`. Rien dans le client ne depend de sa
 * presence.
 */

import type { LigneJournal, ReponseJournal } from "./types";

export const PREFIXE = "/academie/api/v1";

export type Resultat<T> =
  | { ok: true; valeur: T }
  | { ok: false; code: string; motif: string; statut?: number; index?: number };

async function appelle<T>(
  route: string,
  init: RequestInit = {},
): Promise<Resultat<T>> {
  try {
    const reponse = await fetch(PREFIXE + route, {
      credentials: "include",
      headers: { "Content-Type": "application/json", ...(init.headers ?? {}) },
      ...init,
    });
    let corps: unknown = null;
    try {
      corps = await reponse.json();
    } catch {
      corps = null;
    }
    if (!reponse.ok) {
      const e = (corps ?? {}) as { erreur?: string; motif?: string; index?: number };
      return {
        ok: false,
        code: e.erreur ?? "http",
        motif: e.motif ?? `reponse ${reponse.status}`,
        statut: reponse.status,
        index: e.index,
      };
    }
    return { ok: true, valeur: corps as T };
  } catch {
    // Hors-ligne, serveur absent, DNS : un seul chemin, sans bruit.
    return { ok: false, code: "hors_ligne", motif: "serveur injoignable" };
  }
}

export interface Sante {
  ok: boolean;
  moteur_version?: string;
  contrats?: string[];
}

export const api = {
  sante: () => appelle<Sante>("/sante"),

  /** Un lot de 500 lignes au plus (serveur/API.md). */
  envoieJournal: (depuis: string | null, lignes: LigneJournal[]) =>
    appelle<ReponseJournal>("/journal", {
      method: "POST",
      body: JSON.stringify({ depuis, lignes }),
    }),

  profil: () => appelle<{ id: string; titre_affiche: string; cree_le: string }>("/profil"),

  deposeBoite: (contenu: string, type: "texte" | "lien" | "note" = "texte") =>
    appelle<{ id: string; etat: string }>("/boite", {
      method: "POST",
      body: JSON.stringify({ type, contenu }),
    }),

  litBoite: () => appelle<{ entrees: { id: string; contenu: string; etat: string }[] }>("/boite"),

  signale: (carte: string, motif: string) =>
    appelle<Record<string, unknown>>("/signalements", {
      method: "POST",
      body: JSON.stringify({ carte, motif }),
    }),
};

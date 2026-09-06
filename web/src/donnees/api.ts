import { compteActuel, type Compte } from "../app/compte";
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
      headers: { "Content-Type": "application/json", ...(compteActuel() ? {"X-Academie-Profil": compteActuel()?.id ?? ""} : {}), ...(init.headers ?? {}) },
      ...init,
    });
    let corps: unknown = null;
    try {
      corps = await reponse.json();
    } catch {
      corps = null;
    }
    if (!reponse.ok) {
      // Seul un refus complet peut autoriser la mise à l'écart d'une ligne.
      const e = objet(corps) ? corps : {};
      const refusValide = typeof e.erreur === "string" && typeof e.motif === "string";
      return {
        ok: false,
        code: refusValide ? e.erreur as string : "reponse-invalide",
        motif: refusValide ? e.motif as string : `Réponse ${reponse.status} invalide. Tes réponses restent en attente.`,
        statut: reponse.status,
        index: refusValide && typeof e.index === "number" && Number.isSafeInteger(e.index) ? e.index : undefined,
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
export type CompteEtCle = Compte & { cle_recuperation: string };

export const api = {
  sante: () => appelle<Sante>("/sante"),

  /** Un lot de 500 lignes au plus (serveur/API.md). */
  envoieJournal: async (depuis: string | null, lignes: LigneJournal[]): Promise<Resultat<ReponseJournal>> => {
    const r = await appelle<ReponseJournal>("/journal", {
      method: "POST", body: JSON.stringify({ depuis, lignes }),
    });
    if (!r.ok) return r;
    if (!acquittementValide(r.valeur, lignes.length)) return {
      ok: false, code: "reponse-invalide", motif: "Réception non confirmée. Tes réponses restent en attente.",
    };
    return r;
  },

  profil: () => appelle<Compte>("/profil"),
  comptesConnexion: () => appelle<{comptes:{pseudo:string;titre_affiche:string}[]}>("/auth/comptes"),
  inscription: (pseudo: string, phrase_secrete: string) => appelle<CompteEtCle>("/compte", {method:"POST", body:JSON.stringify({pseudo, phrase_secrete})}),
  connexion: (pseudo: string, phrase_secrete: string) => appelle<Compte>("/auth/connexion", {method:"POST", body:JSON.stringify({pseudo, phrase_secrete})}),
  recuperation: (pseudo: string, cle_recuperation: string, phrase_secrete: string) => appelle<CompteEtCle>("/auth/recuperation", {method:"POST", body:JSON.stringify({pseudo, cle_recuperation, phrase_secrete})}),
  deconnexion: () => appelle<{ok:boolean}>("/auth/deconnexion", {method:"POST"}),
  visibilite: (visibilite: boolean) => appelle<{ok:boolean}>("/profil", {method:"PATCH", body:JSON.stringify({visibilite})}),
  eleves: () => appelle<{eleves:{id:string; pseudo:string; cursus:string|null}[]}>("/eleves"),
  demandeCursus: (texte: string) => appelle<{ok:boolean}>("/demandes-cursus", {method:"POST",body:JSON.stringify({texte})}),

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

function objet(v: unknown): v is Record<string, unknown> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}
function iso(v: unknown): v is string {
  if (typeof v !== "string") return false;
  const m = /^(\d{4})-(\d{2})-(\d{2})[Tt](\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:[Zz]|([+-])(\d{2}):(\d{2}))$/.exec(v);
  if (!m) return false;
  const [annee, mois, jour, heure, minute, seconde] = m.slice(1, 7).map(Number);
  if (annee === undefined || mois === undefined || jour === undefined || heure === undefined
      || minute === undefined || seconde === undefined || annee < 1 || mois < 1 || mois > 12
      || jour < 1 || heure > 23 || minute > 59 || seconde > 59
      || Number(m[8] ?? 0) > 23 || Number(m[9] ?? 0) > 59) return false;
  const bissextile = annee % 4 === 0 && (annee % 100 !== 0 || annee % 400 === 0);
  const jours = [31, bissextile ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  return jour <= (jours[mois - 1] ?? 0) && Number.isFinite(Date.parse(v));
}
const entier = (v: unknown) => typeof v === "number" && Number.isSafeInteger(v);
const nombre = (v: unknown) => typeof v === "number" && Number.isFinite(v);
const formats = ["seance", "domaine", "etude", "journee", "epreuve", "hasard", "defi"];
const requis: Record<string, string[]> = {
  cursus: ["cursus"],
  revision: ["carte", "note", "format"], quiz: ["carte", "note", "stabilite_forcee", "origine"],
  examen: ["score"], erreur: ["carte"], seance: ["format", "graine", "banque_version", "moteur_version"],
  synthese: ["chapitre", "attendus_coches"], signalement: ["carte"],
};
/** Contrôle des lignes reçues avant union et avancement du curseur. */
export function ligneValide(v: unknown): v is LigneJournal {
  if (!objet(v) || !iso(v.quand) || typeof v.nonce !== "string" || Array.from(v.nonce).length < 8
      || typeof v.mode !== "string" || !Object.hasOwn(requis, v.mode)) return false;
  if (requis[v.mode]?.some(c => !(c in v))) return false;
  if (v.mode === "cursus" && (typeof v.cursus !== "string" || !v.cursus)) return false;
  if (v.mode === "examen" && !("region" in v) && !("dossier" in v)) return false;
  if ("note" in v && (!entier(v.note) || Number(v.note) < 1 || Number(v.note) > 4)) return false;
  if ("format" in v && (typeof v.format !== "string" || !formats.includes(v.format))) return false;
  if ("jour" in v && (typeof v.jour !== "string" || !["fondations", "cours", "terrain", "exploration", "etude", "libre"].includes(v.jour))) return false;
  if ("duree_ms" in v && (!entier(v.duree_ms) || Number(v.duree_ms) < 0)) return false;
  if ("graine" in v && !entier(v.graine)) return false;
  if ("confiance" in v && typeof v.confiance !== "boolean") return false;
  if ("stabilite_forcee" in v && (!nombre(v.stabilite_forcee) || Number(v.stabilite_forcee) <= 0)) return false;
  if ("score" in v && (!nombre(v.score) || Number(v.score) < 0 || Number(v.score) > 1)) return false;
  for (const c of ["carte", "origine", "region", "dossier", "cap", "banque_version", "moteur_version", "chapitre", "raison", "motif"]) {
    if (c in v && typeof v[c] !== "string") return false;
  }
  if (typeof v.raison === "string" && Array.from(v.raison).length > 200) return false;
  if (typeof v.motif === "string" && Array.from(v.motif).length > 300) return false;
  if ("cartes" in v && (!Array.isArray(v.cartes) || !v.cartes.every(c => typeof c === "string"))) return false;
  if ("attendus_coches" in v && (!Array.isArray(v.attendus_coches) || !v.attendus_coches.every(entier))) return false;
  if ("etude_etape" in v && (typeof v.etude_etape !== "string"
      || !["tentative", "principe", "exercices", "synthese", "grille", "terminee"].includes(v.etude_etape))) return false;
  if ("contenu_version" in v && (!entier(v.contenu_version) || Number(v.contenu_version) < 1)) return false;
  if ("exercice_index" in v && (!entier(v.exercice_index) || Number(v.exercice_index) < 0)) return false;
  if ("reponse_libre" in v && (typeof v.reponse_libre !== "string" || Array.from(v.reponse_libre).length > 5000)) return false;
  if ("aide_utilisee" in v && typeof v.aide_utilisee !== "boolean") return false;
  return true;
}
export function acquittementValide(v: unknown, taille: number): v is ReponseJournal {
  return objet(v) && entier(v.acceptees) && Number(v.acceptees) >= 0
    && entier(v.ignorees) && Number(v.ignorees) >= 0
    && Number(v.acceptees) + Number(v.ignorees) === taille
    && iso(v.jusqu_a) && Array.isArray(v.manquantes) && v.manquantes.every(ligneValide)
    && !("rejets" in v);
}

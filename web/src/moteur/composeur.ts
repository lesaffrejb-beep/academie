/**
 * La seance du jour. Miroir de seance.compose (app/seance.py) :
 * revisions dues plafonnees, entrelacement par domaine, neuf selon les
 * quotas embarques dans banque.json.
 *
 * Ecart assume : la graine. Python tire avec Mersenne Twister
 * (random.Random) ; ici c'est un mulberry32. Le tirage est reproductible
 * a graine egale COTE CLIENT, il n'est pas bit a bit celui du Python.
 * Aucun vecteur de conformite ne porte sur l'ordre de la seance ; la
 * parite exigee (app/vecteurs_fsrs.py) porte sur l'etat de memoire.
 */

import type { EtatCarte } from "./etats";
import { aujourdhuiOrdinal } from "./etats";
import type { Banque, Carte } from "../donnees/types";

export type Alea = () => number;

/** Generateur pseudo-aleatoire reproductible a graine fixee. */
export function alea(graine: number): Alea {
  let a = graine >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function melange<T>(liste: T[], rng: Alea): T[] {
  const sortie = [...liste];
  for (let i = sortie.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    const a = sortie[i] as T;
    const b = sortie[j] as T;
    sortie[i] = b;
    sortie[j] = a;
  }
  return sortie;
}

/** Alterne les domaines autant que possible (interleaving, METHODE 3.5). */
export function entrelace(cartes: Carte[], rng: Alea): Carte[] {
  const paquets = new Map<string, Carte[]>();
  for (const c of cartes) {
    const p = paquets.get(c.domaine);
    if (p) p.push(c);
    else paquets.set(c.domaine, [c]);
  }
  const ordre: Carte[] = [];
  let restants = [...paquets.values()];
  while (restants.length) {
    restants = melange(restants, rng);
    for (const paquet of [...restants]) {
      const tete = paquet.shift();
      if (tete) ordre.push(tete);
      if (!paquet.length) restants = restants.filter((p) => p !== paquet);
    }
  }
  return ordre;
}

export interface Seance {
  date: string;
  graine: number;
  revisions: Carte[];
  nouveau: Carte[];
  arriereReetale: number;
  totalJouable: number;
  jamaisVues: number;
}

export interface OptionsSeance {
  /** Restreint la seance a un domaine (format `domaine`). */
  domaine?: string;
  graine?: number;
  aujourdhui?: number;
}

export function compose(
  banque: Banque,
  etats: Map<string, EtatCarte>,
  options: OptionsSeance = {},
): Seance {
  const quotas = banque.quotas ?? {
    revisions_par_seance: 10,
    nouveau_par_seance: 1,
    plafond_reprise: 20,
  };
  const jour = options.aujourdhui ?? aujourdhuiOrdinal();
  const graine = options.graine ?? jour;

  let jouables = (banque.cartes ?? []).filter((c) => c.statut === "valide");
  if (options.domaine) jouables = jouables.filter((c) => c.domaine === options.domaine);

  const dues: { carte: Carte; etat: EtatCarte }[] = [];
  const neuvesToutes: Carte[] = [];
  for (const carte of jouables) {
    const etat = etats.get(carte.id);
    if (!etat) neuvesToutes.push(carte);
    else if (etat.duLe <= jour) dues.push({ carte, etat });
  }

  // Les plus en retard d'abord : ce sont celles qui s'effacent.
  dues.sort((a, b) => a.etat.duLe - b.etat.duLe);
  const plafond = quotas.plafond_reprise ?? 20;
  const arriere = Math.max(0, dues.length - plafond);
  const retenues = dues.slice(0, plafond).map((x) => x.carte);

  const rng = alea(graine);
  const revisions = entrelace(retenues, rng);
  const nouveau = melange(neuvesToutes, rng).slice(0, quotas.nouveau_par_seance ?? 1);

  return {
    date: new Date(jour * 86400000).toISOString().slice(0, 10),
    graine,
    revisions,
    nouveau,
    arriereReetale: arriere,
    totalJouable: jouables.length,
    jamaisVues: jouables.filter((c) => !etats.has(c.id)).length,
  };
}

/** Le tirage de l examen de region : a froid, deterministe a graine fixee. */
export function composeExamen(
  banque: Banque,
  region: string,
  graine = 0,
): Carte[] {
  const nb = banque.progression?.examen_nb_cartes ?? 12;
  const pool = (banque.cartes ?? [])
    .filter((c) => c.domaine === region && c.statut === "valide")
    .sort((a, b) => String(a.id).localeCompare(String(b.id)));
  return melange(pool, alea(graine)).slice(0, nb);
}

/** Au hasard : n cartes jouables, toutes regions confondues. */
export function auHasard(banque: Banque, n: number, graine: number): Carte[] {
  const pool = (banque.cartes ?? []).filter((c) => c.statut === "valide");
  return melange(pool, alea(graine)).slice(0, n);
}

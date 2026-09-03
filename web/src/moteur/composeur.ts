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
import { noeudsEtBranches, reglages } from "./progression";
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


/* --- la semaine type et le socle (ACA-SEMAINE-1) --------------------- */
//
// La couleur du jour ne pese QUE sur le neuf : les revisions dues sont
// servies tous les jours, dimanche compris (BLUEPRINT §4). Rien ici ne
// bloque quoi que ce soit.

export const JOURS_SEMAINE = [
  "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche",
] as const;

export type Couleur =
  | "fondations" | "cours" | "terrain" | "exploration" | "etude" | "libre";

/** La couleur d un jour ordinal selon `semaine_type`. Defaut : cours. */
export function couleurDuJour(banque: Banque, jourOrdinal: number): Couleur {
  // 1970-01-01 etait un jeudi : indice 3 dans JOURS_SEMAINE.
  const index = (((jourOrdinal + 3) % 7) + 7) % 7;
  const nom = JOURS_SEMAINE[index] as string;
  const table = (banque.semaine_type ?? {}) as Record<string, string>;
  return (table[nom] as Couleur) ?? "cours";
}

/** Combien de cartes neuves ce matin, et pourquoi. Fonction pure. */
export function quotaDeNeuf(
  banque: Banque,
  couleur: Couleur,
  dues: number,
  dejaDuJour: number,
): { quota: number; pourquoi: string[] } {
  const q = banque.quotas ?? ({} as Banque["quotas"]);
  const pourquoi: string[] = [];
  let quota = q.nouveau_par_seance ?? 1;
  if (couleur === "cours" || couleur === "terrain") {
    quota = q.nouveau_par_seance_max ?? quota;
  }
  if (couleur === "libre") {
    quota = 0;
    pourquoi.push("dimanche libre : rien de neuf n'est poussé");
  }
  if (couleur === "fondations") {
    const seuil = q.fondations_dues_sans_neuf ?? 15;
    if (dues > seuil) {
      quota = 0;
      pourquoi.push(
        `lundi fondations : ${dues} cartes dues, plus de ${seuil}, ` +
          "on rattrape avant d'ouvrir du neuf",
      );
    }
  }
  const parJour = q.nouveau_par_jour ?? 20;
  const reste = Math.max(0, parJour - dejaDuJour);
  if (reste < quota) {
    pourquoi.push(
      reste === 0
        ? `plafond de ${parJour} cartes neuves par jour atteint`
        : "plafond de neuf du jour presque atteint",
    );
  }
  return { quota: Math.min(quota, reste), pourquoi };
}

/**
 * `<domaine>.<branche>` du socle la moins avancee, ou null.
 *
 * Reutilise noeudsEtBranches : une seule mesure de remplissage dans tout
 * le moteur. Rend null quand le socle est tenu partout (la ponderation
 * s eteint, decisions/0013 §5) ou qu il n y a rien a mesurer.
 */
export function brancheSocleLaPlusFaible(
  cartes: Carte[],
  etats: Map<string, EtatCarte>,
  banque: Banque,
  jourCourant: number,
): string | null {
  if (!banque.chapitres?.length || !banque.socle) return null;
  const domainesSocle = new Set(Object.keys(banque.socle.niveaux ?? {}));
  if (!domainesSocle.size) return null;
  const { branches } = noeudsEtBranches(
    cartes, [], banque, etats, new Set<string>(), jourCourant,
  );
  const candidates = branches.filter(
    (b) => domainesSocle.has(b.domaine) && b.noeudsServis > 0,
  );
  if (!candidates.length) return null;
  const faible = candidates.reduce((a, b) => {
    if (b.remplissage !== a.remplissage) return b.remplissage < a.remplissage ? b : a;
    if (b.domaine !== a.domaine) return b.domaine < a.domaine ? b : a;
    return b.cle < a.cle ? b : a;
  });
  if (faible.remplissage >= reglages(banque).seuil_ouverture_region) return null;
  return `${faible.domaine}.${faible.cle}`;
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

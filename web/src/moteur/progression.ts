/**
 * La carte-monde. Miroir de app/progression.py : remplissage par region,
 * plafond sans examen, regions hors arbre, XP derivee. Aucune
 * comptabilite propre, aucun score stocke.
 */

import type { EtatCarte } from "./etats";
import type { Banque, Carte, Domaine, LigneJournal, ReglagesProgression } from "../donnees/types";

/** Pas un reglage : la regle : le 100 % n existe pas sans son examen. */
export const PLAFOND_SANS_EXAMEN = 0.99;

export const XP_PAR_REVUE = 10;
export const XP_PAR_REGION = 500;
export const XP_PAR_EXAMEN = 1000;

const CLES_REGLAGES = [
  "seuil_stabilite_acquise_jours",
  "seuil_ouverture_region",
  "examen_obligatoire_pour_100",
  "examen_nb_cartes",
  "examen_score_reussite",
] as const;

/** Echoue bruyamment plutot que de deviner un seuil (app/progression.py). */
export function reglages(banque: Banque): ReglagesProgression {
  const bloc = banque.progression;
  if (!bloc || typeof bloc !== "object") {
    throw new Error("banque : bloc `progression` absent");
  }
  const manquants = CLES_REGLAGES.filter((c) => !(c in bloc));
  if (manquants.length) {
    throw new Error("`progression` incomplete, manque : " + manquants.join(", "));
  }
  return bloc;
}

export interface Region {
  cle: string;
  titre: string;
  rang: number;
  remplissage: number;
  remplissageMesure: number;
  cartesTotales: number;
  cartesAcquises: number;
  ouverte: boolean;
  ouvertePar: "premiere" | "seuil" | "quiz" | null;
  explorable: true;
  statut: "ouverte" | "explorable" | "hors_carte";
  examenRequis: boolean;
  examenReussi: boolean;
  plafonneeFauteDExamen: boolean;
  conquise: boolean;
}

export interface CarteMonde {
  seuilStabiliteJours: number;
  seuilOuverture: number;
  examenNbCartes: number;
  examenScoreReussite: number;
  regions: Region[];
  horsCarte: Region[];
  remplissageGlobal: number;
  regionsOuvertes: string[];
  regionsConquises: string[];
  xp: number;
}

function tri(entrees: [string, Domaine][]): [string, Domaine][] {
  return entrees.sort((a, b) => {
    const oa = a[1].ordre ?? 999;
    const ob = b[1].ordre ?? 999;
    return oa !== ob ? oa - ob : a[0].localeCompare(b[0]);
  });
}

export function regionsOrdonnees(banque: Banque): [string, Domaine][] {
  return tri(Object.entries(banque.domaines ?? {}).filter(([, d]) => d.arbre !== false));
}

/** Les domaines exclus de la carte-monde (`"arbre": false`). */
export function regionsHorsCarte(banque: Banque): [string, Domaine][] {
  return tri(Object.entries(banque.domaines ?? {}).filter(([, d]) => d.arbre === false));
}

export function cartesRegion(cartes: Carte[], region: string): Carte[] {
  return cartes.filter((c) => c.domaine === region && c.statut === "valide");
}

/** Part des cartes valide de la region dont la stabilite atteint le seuil. */
export function remplissageBrut(
  cartes: Carte[],
  etats: Map<string, EtatCarte>,
  region: string,
  banque: Banque,
): number {
  const seuil = reglages(banque).seuil_stabilite_acquise_jours;
  const jouables = cartesRegion(cartes, region);
  if (!jouables.length) return 0;
  const acquises = jouables.filter(
    (c) => (etats.get(c.id)?.stabilite ?? 0) >= seuil,
  ).length;
  return acquises / jouables.length;
}

export function plafonne(brut: number, examenReussi: boolean, banque: Banque): number {
  const r = reglages(banque);
  if (!r.examen_obligatoire_pour_100 || examenReussi) return brut;
  return Math.min(brut, PLAFOND_SANS_EXAMEN);
}

/** Les lignes qui sont des RESULTATS d'examen (jamais des revisions). */
export function entreesExamen(journal: LigneJournal[]): LigneJournal[] {
  return journal.filter(
    (e) =>
      e.mode === "examen" &&
      e.carte === undefined &&
      typeof e.region === "string" &&
      typeof e.score === "number",
  );
}

export function examensReussis(journal: LigneJournal[], banque: Banque): Set<string> {
  const seuil = reglages(banque).examen_score_reussite;
  const sortie = new Set<string>();
  for (const e of entreesExamen(journal)) {
    if ((e.score ?? 0) >= seuil && e.region) sortie.add(e.region);
  }
  return sortie;
}

/** XP AFFICHEE, derivee, jamais stockee. Fonction pure. */
export function xpAffichee(
  journal: LigneJournal[],
  remplissages: Record<string, number>,
  banque: Banque,
): number {
  const bloc = banque.progression ?? ({} as ReglagesProgression);
  const parRevue = bloc.xp_par_revue ?? XP_PAR_REVUE;
  const parRegion = bloc.xp_par_region ?? XP_PAR_REGION;
  const parExamen = bloc.xp_par_examen ?? XP_PAR_EXAMEN;
  const reussies = journal.filter(
    (e) => e.carte && (e.note === 2 || e.note === 3 || e.note === 4),
  ).length;
  const somme = Object.values(remplissages).reduce((a, b) => a + b, 0);
  const examensTombes = examensReussis(journal, banque).size;
  return Math.round(parRevue * reussies + parRegion * somme + parExamen * examensTombes);
}

const arrondi4 = (x: number) => Math.round(x * 10000) / 10000;

export function carteMonde(
  cartes: Carte[],
  journal: LigneJournal[],
  banque: Banque,
  etats: Map<string, EtatCarte>,
  regionsOuvertesForcees: readonly string[] = [],
): CarteMonde {
  const r = reglages(banque);
  const forcees = new Set(regionsOuvertesForcees);
  const reussis = examensReussis(journal, banque);
  const exigeExamen = Boolean(r.examen_obligatoire_pour_100);

  const regions: Region[] = [];
  const remplissages: Record<string, number> = {};
  let precedentAtteint = true; // la region 1 est toujours ouverte
  let rang = 0;

  for (const [cle, meta] of regionsOrdonnees(banque)) {
    rang += 1;
    const jouables = cartesRegion(cartes, cle);
    const brut = remplissageBrut(cartes, etats, cle, banque);
    const examenTombe = reussis.has(cle);
    const affiche = plafonne(brut, examenTombe, banque);
    const parQuiz = forcees.has(cle);
    const ouverte = rang === 1 || precedentAtteint || parQuiz;
    const ouvertePar: Region["ouvertePar"] =
      rang === 1 ? "premiere" : precedentAtteint ? "seuil" : parQuiz ? "quiz" : null;

    regions.push({
      cle,
      titre: meta.titre ?? cle,
      rang,
      remplissage: arrondi4(affiche),
      remplissageMesure: arrondi4(brut),
      cartesTotales: jouables.length,
      cartesAcquises: jouables.filter(
        (c) => (etats.get(c.id)?.stabilite ?? 0) >= r.seuil_stabilite_acquise_jours,
      ).length,
      ouverte,
      ouvertePar,
      // Le moteur n'interdit rien : une region fermee se joue.
      explorable: true,
      statut: ouverte ? "ouverte" : "explorable",
      examenRequis: exigeExamen,
      examenReussi: examenTombe,
      plafonneeFauteDExamen: exigeExamen && !examenTombe && brut > PLAFOND_SANS_EXAMEN,
      conquise: affiche >= 1,
    });
    remplissages[cle] = affiche;
    precedentAtteint = brut >= r.seuil_ouverture_region;
  }

  const horsCarte: Region[] = regionsHorsCarte(banque).map(([cle, meta]) => {
    const jouables = cartesRegion(cartes, cle);
    return {
      cle,
      titre: meta.titre ?? cle,
      rang: 0,
      remplissage: arrondi4(remplissageBrut(cartes, etats, cle, banque)),
      remplissageMesure: arrondi4(remplissageBrut(cartes, etats, cle, banque)),
      cartesTotales: jouables.length,
      cartesAcquises: jouables.filter(
        (c) => (etats.get(c.id)?.stabilite ?? 0) >= r.seuil_stabilite_acquise_jours,
      ).length,
      ouverte: true,
      ouvertePar: null,
      explorable: true,
      statut: "hors_carte",
      examenRequis: false,
      examenReussi: false,
      plafonneeFauteDExamen: false,
      conquise: false,
    };
  });

  const cles = Object.keys(remplissages);
  const global = cles.length
    ? cles.reduce((a, c) => a + (remplissages[c] ?? 0), 0) / cles.length
    : 0;

  return {
    seuilStabiliteJours: r.seuil_stabilite_acquise_jours,
    seuilOuverture: r.seuil_ouverture_region,
    examenNbCartes: r.examen_nb_cartes,
    examenScoreReussite: r.examen_score_reussite,
    regions,
    horsCarte,
    remplissageGlobal: arrondi4(global),
    regionsOuvertes: regions.filter((x) => x.ouverte).map((x) => x.cle),
    regionsConquises: regions.filter((x) => x.conquise).map((x) => x.cle),
    xp: xpAffichee(journal, remplissages, banque),
  };
}

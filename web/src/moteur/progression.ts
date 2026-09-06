/**
 * La carte-monde. Miroir de app/progression.py : remplissage par region,
 * plafond sans examen, regions hors arbre, XP derivee. Aucune
 * comptabilite propre, aucun score stocke.
 */

import { jourOrdinal, aujourdhuiOrdinal } from "./etats";
import type { EtatCarte } from "./etats";
import type {
  Banque, BrancheProgramme, Carte, Chapitre, Domaine, LigneJournal, ReglagesProgression,
} from "../donnees/types";

/** Pas un reglage : la regle : le 100 % n existe pas sans son examen. */
export const PLAFOND_SANS_EXAMEN = 0.99;

/** Defaut quand la banque est anterieure a ACA-ARBRE-1 (decisions/0028). */
export const SEUIL_FRAICHEUR_DEFAUT = 21;

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
  noeuds: Noeud[];
  branches: Branche[];
  seuilFraicheurJours: number;
  cartesSansChapitre: number;
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

/* --- les noeuds et les branches (ACA-ARBRE-1, decisions/0028) -------- */

export type EtatNoeud = "inconnu" | "ouvert" | "en-cours" | "solide" | "valide" | "a-revoir";

export interface Noeud {
  id: string;
  titre: string;
  domaine: string;
  branche: string;
  sousBranche: string | null;
  niveau: number | null;
  satellite: boolean;
  rattachementPropose?: string;
  prerequis: string[];
  etat: EtatNoeud;
  remplissage: number;
  cartesTotales: number;
  cartesAcquises: number;
  derniereRevue: string | null;
  joursDepuisDerniereRevue: number | null;
  aRevoir: boolean;
  prerequisSatisfaits: boolean;
  /** Regle 1 de BLUEPRINT §5 : toujours vrai, sans exception. */
  jouable: true;
}

export interface Branche {
  domaine: string;
  cle: string;
  titre: string;
  rang: number;
  remplissage: number;
  noeuds: number;
  noeudsServis: number;
  noeudsValides: number;
  ouverte: boolean;
  explorable: true;
}

export function seuilFraicheur(banque: Banque): number {
  return banque.progression?.seuil_fraicheur_jours ?? SEUIL_FRAICHEUR_DEFAUT;
}

/** Les cartes jouables groupees par noeud. Sans `chapitre`, pas de noeud. */
export function cartesParChapitre(cartes: Carte[]): Map<string, Carte[]> {
  const par = new Map<string, Carte[]>();
  for (const c of cartes) {
    if (c.statut !== "valide") continue;
    const ch = c.chapitre;
    if (typeof ch !== "string" || !ch) continue;
    const liste = par.get(ch);
    if (liste) liste.push(c);
    else par.set(ch, [c]);
  }
  return par;
}

/** Combien de cartes jouables n'ont encore aucun noeud (ACA-CONTRAT-2). */
export function cartesSansChapitre(cartes: Carte[]): number {
  return cartes.filter((c) => c.statut === "valide" && !c.chapitre).length;
}

// Les jours ordinaux viennent de etats.ts (origine epoque Unix), la
// meme echelle que `duLe`. Melanger deux origines rendrait tout echu.

/**
 * L'etat d'un noeud (decisions/0028). `valide` se gagne a l'epreuve du
 * domaine, pas au remplissage : c'est ce qui rend vraie la regle 3 de
 * BLUEPRINT §5 sans rien stocker. La fraicheur ne declasse pas.
 */
export function etatNoeud(
  remplissage: number,
  joue: boolean,
  aDesCartes: boolean,
  examenReussi: boolean,
  aRevoir: boolean,
  banque: Banque,
): EtatNoeud {
  if (!aDesCartes) return "inconnu";
  if (joue && examenReussi) return "valide";
  if (!joue) return "ouvert";
  if (aRevoir) return "a-revoir";
  if (remplissage >= reglages(banque).seuil_ouverture_region) return "solide";
  return "en-cours";
}

export function noeudsEtBranches(
  cartes: Carte[],
  journal: LigneJournal[],
  banque: Banque,
  etats: Map<string, EtatCarte>,
  reussis: Set<string>,
  jourCourant: number,
): { noeuds: Noeud[]; branches: Branche[] } {
  const r = reglages(banque);
  const seuilStab = r.seuil_stabilite_acquise_jours;
  const seuilOuv = r.seuil_ouverture_region;
  const fraicheur = seuilFraicheur(banque);
  const parChapitre = cartesParChapitre(cartes);

  const noeuds: Noeud[] = [];
  const etatsParId = new Map<string, EtatNoeud>();

  for (const ch of (banque.chapitres ?? []) as Chapitre[]) {
    const siennes = parChapitre.get(ch.id) ?? [];
    const ids = new Set(siennes.map((c) => c.id));
    const acquises = siennes.filter((c) => (etats.get(c.id)?.stabilite ?? 0) >= seuilStab).length;
    const remplissage = siennes.length ? acquises / siennes.length : 0;

    let derniere: string | null = null;
    for (const e of journal) {
      if (e.carte && ids.has(e.carte) && e.quand && (derniere === null || e.quand > derniere)) {
        derniere = e.quand;
      }
    }
    const joue = derniere !== null;
    const jours =
      derniere === null ? null : jourCourant - (jourOrdinal(derniere) ?? jourCourant);
    // Seules les cartes DEJA VUES peuvent etre echues : une carte neuve
    // est a decouvrir, pas a revoir.
    const echue = siennes.some((c) => {
      const e = etats.get(c.id);
      return e !== undefined && e.duLe <= jourCourant;
    });
    const aRevoir = joue && jours !== null && jours > fraicheur && echue;
    const reussi = reussis.has(ch.domaine);
    const etat = etatNoeud(remplissage, joue, siennes.length > 0, reussi, aRevoir, banque);
    etatsParId.set(ch.id, etat);

    noeuds.push({
      id: ch.id,
      titre: ch.titre ?? ch.id,
      domaine: ch.domaine,
      branche: ch.branche,
      sousBranche: ch.sous_branche ?? null,
      niveau: ch.niveau ?? null,
      satellite: Boolean(ch.satellite),
      ...(ch.rattachement_propose ? {rattachementPropose: ch.rattachement_propose} : {}),
      prerequis: [...(ch.prerequis ?? [])],
      etat,
      remplissage: arrondi4(remplissage),
      cartesTotales: siennes.length,
      cartesAcquises: acquises,
      derniereRevue: derniere,
      joursDepuisDerniereRevue: jours,
      aRevoir,
      prerequisSatisfaits: true,
      jouable: true,
    });
  }

  // Le prerequis informe l'affichage, il n'interdit rien : satisfait
  // quand son noeud est solide ou mieux.
  for (const n of noeuds) {
    n.prerequisSatisfaits = n.prerequis.every((p) => {
      const e = etatsParId.get(p);
      return e === "solide" || e === "valide";
    });
  }

  const branches: Branche[] = [];
  for (const [domaine, liste] of Object.entries(banque.branches ?? {})) {
    let precedentAtteint = true;
    let rang = 0;
    const triees = [...(liste as BrancheProgramme[])].sort((a, b) => {
      const oa = a.ordre ?? 999;
      const ob = b.ordre ?? 999;
      return oa !== ob ? oa - ob : (a.cle ?? "").localeCompare(b.cle ?? "");
    });
    for (const b of triees) {
      rang += 1;
      const siens = noeuds.filter((n) => n.domaine === domaine && n.branche === b.cle);
      const avec = siens.filter((n) => n.cartesTotales > 0);
      const remplissage = avec.length
        ? avec.reduce((a, n) => a + n.remplissage, 0) / avec.length
        : 0;
      branches.push({
        domaine,
        cle: b.cle,
        titre: b.titre ?? b.cle,
        rang,
        remplissage: arrondi4(remplissage),
        noeuds: siens.length,
        noeudsServis: avec.length,
        noeudsValides: siens.filter((n) => n.etat === "valide").length,
        ouverte: rang === 1 || precedentAtteint,
        explorable: true,
      });
      precedentAtteint = remplissage >= seuilOuv;
    }
  }

  return { noeuds, branches };
}


export function carteMonde(
  cartes: Carte[],
  journal: LigneJournal[],
  banque: Banque,
  etats: Map<string, EtatCarte>,
  regionsOuvertesForcees: readonly string[] = [],
  jourCourant: number = aujourdhuiOrdinal(),
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
    // L'arbre n'existe que si la banque publie un programme : sans lui,
    // la carte-monde est exactement celle d'avant ACA-ARBRE-1.
    ...(banque.chapitres?.length
      ? noeudsEtBranches(cartes, journal, banque, etats, reussis, jourCourant)
      : { noeuds: [] as Noeud[], branches: [] as Branche[] }),
    seuilFraicheurJours: seuilFraicheur(banque),
    cartesSansChapitre: cartesSansChapitre(cartes),
  };
}

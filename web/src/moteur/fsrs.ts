/**
 * FSRS-6, miroir TypeScript de app/planificateur.py.
 *
 * Ecrit a la main plutot que pose sur ts-fsrs : la consigne est la
 * PARITE avec le Python, pas la reutilisation. ts-fsrs expose ses etats
 * (learning / review / relearning, fuzz, apprentissage par paliers) et
 * n'offre pas la formule court terme nue de app/planificateur.py sans
 * la contourner ; un miroir ligne a ligne est verifiable et ne derive
 * pas au prochain minor de la dependance. app/vecteurs_fsrs.py est le
 * juge : src/moteur/parite.test.ts le rejoue a 1e-4.
 *
 * Vocabulaire (BLUEPRINT 8) : S stabilite en jours, D difficulte 1..10,
 * R recuperabilite. Notes Anki : 1 rate, 2 dur, 3 bien, 4 facile.
 */

export const PARAMS_DEFAUT: readonly number[] = [
  0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001,
  1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014,
  1.8729, 0.5425, 0.0912, 0.0658, 0.1542,
];

export const RETENTION_DEFAUT = 0.9;
export const INTERVALLE_MAX = 36500;
export const STABILITE_MIN = 0.001;
export const DIFFICULTE_MIN = 1.0;
export const DIFFICULTE_MAX = 10.0;

export const RATE = 1;
export const DUR = 2;
export const BIEN = 3;
export const FACILE = 4;

export type Note = 1 | 2 | 3 | 4;

/**
 * round() de Python : arrondi au pair le plus proche sur un demi exact.
 * Math.round arrondirait 2.5 a 3 la ou Python rend 2 ; sur un intervalle
 * l'ecart se voit a l'oeil nu et ferait echouer la parite.
 */
export function arrondiPython(x: number): number {
  const bas = Math.floor(x);
  const reste = x - bas;
  if (reste > 0.5) return bas + 1;
  if (reste < 0.5) return bas;
  return bas % 2 === 0 ? bas : bas + 1;
}

export interface EtatFsrs {
  stabilite: number;
  difficulte: number;
}

export class Planificateur {
  readonly p: readonly number[];
  readonly retention: number;
  readonly intervalleMax: number;
  private readonly decay: number;
  private readonly factor: number;

  constructor(
    params: readonly number[] = PARAMS_DEFAUT,
    retention: number = RETENTION_DEFAUT,
    intervalleMax: number = INTERVALLE_MAX,
  ) {
    if (params.length !== 21) {
      throw new Error(`FSRS-6 attend 21 parametres, recu ${params.length}`);
    }
    if (!(retention >= 0.7 && retention <= 0.99)) {
      throw new Error("retention souhaitee hors bornes (0,70-0,99)");
    }
    this.p = params.slice();
    this.retention = retention;
    this.intervalleMax = intervalleMax;
    this.decay = -this.par(20);
    this.factor = Math.pow(0.9, 1 / this.decay) - 1;
  }

  private par(i: number): number {
    const v = this.p[i];
    if (v === undefined) throw new Error(`parametre ${i} absent`);
    return v;
  }

  /* --- lecture ---------------------------------------------------- */

  recuperabilite(stabilite: number, joursEcoules: number): number {
    if (stabilite <= 0) return 0;
    return Math.pow(1 + (this.factor * joursEcoules) / stabilite, this.decay);
  }

  intervalle(stabilite: number): number {
    const brut =
      (stabilite / this.factor) * (Math.pow(this.retention, 1 / this.decay) - 1);
    return Math.max(1, Math.min(arrondiPython(brut), this.intervalleMax));
  }

  /* --- premiere rencontre ----------------------------------------- */

  premiere(note: Note): EtatFsrs {
    verifieNote(note);
    return {
      stabilite: clampS(this.par(note - 1)),
      difficulte: clampD(this.difficulteInitiale(note)),
    };
  }

  /* --- revisions suivantes ---------------------------------------- */

  /** joursEcoules = 0 : reprise le jour meme, formule court terme. */
  revise(
    stabilite: number,
    difficulte: number,
    note: Note,
    joursEcoules: number,
  ): EtatFsrs {
    verifieNote(note);
    const d = clampD(this.difficulteSuivante(difficulte, note));
    if (joursEcoules <= 0) {
      return { stabilite: clampS(this.stabiliteCourtTerme(stabilite, note)), difficulte: d };
    }
    const r = this.recuperabilite(stabilite, joursEcoules);
    const s =
      note === RATE
        ? this.stabiliteApresOubli(difficulte, stabilite, r)
        : this.stabiliteApresRappel(difficulte, stabilite, r, note);
    return { stabilite: clampS(s), difficulte: d };
  }

  /* --- formules (miroir de app/planificateur.py) ------------------- */

  private difficulteInitiale(note: number): number {
    return this.par(4) - Math.pow(Math.E, this.par(5) * (note - 1)) + 1;
  }

  private difficulteSuivante(d: number, note: number): number {
    const delta = -(this.par(6) * (note - 3));
    const amorti = d + ((10.0 - d) * delta) / 9.0;
    const cible = this.difficulteInitiale(FACILE); // non bornee, comme la reference
    return this.par(7) * cible + (1 - this.par(7)) * amorti;
  }

  private stabiliteCourtTerme(s: number, note: number): number {
    let hausse =
      Math.pow(Math.E, this.par(17) * (note - 3 + this.par(18))) *
      Math.pow(s, -this.par(19));
    if (note === DUR || note === BIEN || note === FACILE) {
      hausse = Math.max(hausse, 1.0);
    }
    return s * hausse;
  }

  private stabiliteApresRappel(d: number, s: number, r: number, note: number): number {
    const penaliteDur = note === DUR ? this.par(15) : 1;
    const bonusFacile = note === FACILE ? this.par(16) : 1;
    return (
      s *
      (1 +
        Math.pow(Math.E, this.par(8)) *
          (11 - d) *
          Math.pow(s, -this.par(9)) *
          (Math.pow(Math.E, (1 - r) * this.par(10)) - 1) *
          penaliteDur *
          bonusFacile)
    );
  }

  private stabiliteApresOubli(d: number, s: number, r: number): number {
    const longTerme =
      this.par(11) *
      Math.pow(d, -this.par(12)) *
      (Math.pow(s + 1, this.par(13)) - 1) *
      Math.pow(Math.E, (1 - r) * this.par(14));
    const courtTerme = s / Math.pow(Math.E, this.par(17) * this.par(18));
    return Math.min(longTerme, courtTerme);
  }
}

/* --- garde-fous ---------------------------------------------------- */

export function verifieNote(note: number): asserts note is Note {
  if (note !== 1 && note !== 2 && note !== 3 && note !== 4) {
    throw new Error(`note ${note} inconnue : 1 rate, 2 dur, 3 bien, 4 facile`);
  }
}

export function clampS(s: number): number {
  return Math.max(s, STABILITE_MIN);
}

export function clampD(d: number): number {
  return Math.min(Math.max(d, DIFFICULTE_MIN), DIFFICULTE_MAX);
}

/** Le planificateur de la banque : parametres et retention du JSON. */
export function planificateurDe(fsrs?: {
  retention_souhaitee?: number;
  params?: number[];
}): Planificateur {
  const params =
    fsrs?.params && fsrs.params.length === 21 ? fsrs.params : PARAMS_DEFAUT;
  const retention = fsrs?.retention_souhaitee ?? RETENTION_DEFAUT;
  return new Planificateur(params, retention);
}

/**
 * La parite du miroir JS avec le planificateur Python.
 *
 * On ne lit pas site/vecteurs-fsrs.json : un fichier commite peut dater.
 * On lance `python3 app/vecteurs_fsrs.py --json` depuis la racine du
 * depot, donc le juge est le VRAI planificateur, a l'instant du test.
 *
 * Comparaison a 1e-4 sur stabilite, difficulte, intervalle et
 * recuperabilite, pour chaque etape de chaque sequence, y compris les
 * etapes a stabilite forcee (le quiz de positionnement).
 */

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { Planificateur, verifieNote, type Note } from "./fsrs";

const RACINE = fileURLToPath(new URL("../../..", import.meta.url));

interface Attendu {
  stabilite: number;
  difficulte: number;
  intervalle: number;
  recuperabilite: Record<string, number>;
}

interface Etape {
  note: number;
  jours: number;
  stabilite_forcee: number | null;
  attendu: Attendu;
}

interface Sequence {
  nom: string;
  retention: number;
  etapes: Etape[];
}

interface Vecteurs {
  tolerance: number;
  jours_recuperabilite: number[];
  sequences: Sequence[];
}

function vecteurs(): Vecteurs {
  const brut = execFileSync("python3", ["app/vecteurs_fsrs.py", "--json"], {
    cwd: RACINE,
    encoding: "utf-8",
    maxBuffer: 64 * 1024 * 1024,
  });
  return JSON.parse(brut) as Vecteurs;
}

const charge = vecteurs();
const TOLERANCE = charge.tolerance ?? 1e-4;

/**
 * Le rejeu du client, ligne a ligne comme moteur/etats.ts : premiere
 * rencontre, revision avec delai borne a zero, puis la stabilite forcee
 * appliquee APRES le moteur et seulement si elle est finie et positive.
 */
function rejoue(sequence: Sequence): { stabilite: number; difficulte: number }[] {
  const sched = new Planificateur(undefined, sequence.retention);
  const sortie: { stabilite: number; difficulte: number }[] = [];
  let etat: { stabilite: number; difficulte: number } | null = null;
  for (const etape of sequence.etapes) {
    verifieNote(etape.note);
    const note = etape.note as Note;
    etat = etat
      ? sched.revise(etat.stabilite, etat.difficulte, note, Math.max(0, etape.jours))
      : sched.premiere(note);
    const forcee = etape.stabilite_forcee;
    if (forcee !== null && forcee !== undefined) {
      const valeur = Number(forcee);
      if (Number.isFinite(valeur) && valeur > 0) {
        etat = { stabilite: valeur, difficulte: etat.difficulte };
      }
    }
    sortie.push(etat);
  }
  return sortie;
}

describe("parite du miroir FSRS avec app/planificateur.py", () => {
  it("les vecteurs Python sont lisibles et non vides", () => {
    expect(charge.sequences.length).toBeGreaterThan(20);
    expect(charge.jours_recuperabilite).toContain(0);
    const forcees = charge.sequences.some((s) =>
      s.etapes.some((e) => e.stabilite_forcee !== null),
    );
    expect(forcees).toBe(true);
  });

  for (const sequence of charge.sequences) {
    it(`sequence ${sequence.nom}`, () => {
      const sched = new Planificateur(undefined, sequence.retention);
      const obtenu = rejoue(sequence);
      sequence.etapes.forEach((etape, i) => {
        const etat = obtenu[i];
        expect(etat, `etape ${i} absente`).toBeDefined();
        if (!etat) return;
        const a = etape.attendu;
        const ou = `${sequence.nom} etape ${i}`;

        expect(etat.stabilite, `${ou} stabilite`).toBeCloseTo(a.stabilite, 4);
        expect(Math.abs(etat.stabilite - a.stabilite), `${ou} stabilite`)
          .toBeLessThan(TOLERANCE);
        expect(Math.abs(etat.difficulte - a.difficulte), `${ou} difficulte`)
          .toBeLessThan(TOLERANCE);

        // L'intervalle est entier des deux cotes : egalite stricte.
        expect(sched.intervalle(etat.stabilite), `${ou} intervalle`).toBe(a.intervalle);

        for (const [jours, attendue] of Object.entries(a.recuperabilite)) {
          const r = sched.recuperabilite(etat.stabilite, Number(jours));
          expect(Math.abs(r - attendue), `${ou} recuperabilite a ${jours} jours`)
            .toBeLessThan(TOLERANCE);
        }
      });
    });
  }

  it("la recuperabilite a zero jour vaut un", () => {
    const sched = new Planificateur();
    expect(sched.recuperabilite(10, 0)).toBeCloseTo(1, 12);
  });
});

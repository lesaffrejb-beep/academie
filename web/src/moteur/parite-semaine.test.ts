/**
 * La parite de la semaine type entre Python et le miroir TypeScript.
 *
 * Meme geste que parite.test.ts et parite-arbre.test.ts : on lance
 * `python3 app/vecteurs_semaine.py --json` depuis la racine du depot,
 * donc le juge est le VRAI seance.py, a l'instant du test.
 *
 * Ce qui est compare : la couleur du jour, le quota de neuf et son
 * pourquoi, la branche du socle a proteger. Ce qui ne l'est PAS : le
 * tirage. Python tire avec Mersenne Twister, le client avec un
 * mulberry32 ; comparer l'ordre ferait un test du generateur, pas du
 * produit. L'ecart est assume depuis le premier jour (composeur.ts).
 */

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { brancheSocleLaPlusFaible, couleurDuJour, quotaDeNeuf } from "./composeur";
import { etatsCartes, jourOrdinal } from "./etats";
import { Planificateur } from "./fsrs";
import type { Banque, Carte, LigneJournal } from "../donnees/types";

const RACINE = fileURLToPath(new URL("../../..", import.meta.url));

interface SceneQuota {
  nom: string;
  date: string;
  dues: number;
  deja_du_jour: number;
  attendu: { couleur: string; quota: number; pourquoi: string[] };
}

interface SceneSocle {
  nom: string;
  cartes: Carte[];
  journal: LigneJournal[];
  programme: { branches?: Banque["branches"]; chapitres?: Banque["chapitres"] };
  attendu: string | null;
}

interface Vecteurs {
  config: {
    quotas: Banque["quotas"];
    domaines: Banque["domaines"];
    progression: Banque["progression"];
    fsrs?: { retention_souhaitee?: number };
    semaine_type?: Record<string, string>;
    socle?: { niveaux?: Record<string, number> };
  };
  quotas: SceneQuota[];
  socle: SceneSocle[];
}

const vecteurs: Vecteurs = JSON.parse(
  execFileSync("python3", ["app/vecteurs_semaine.py", "--json"], {
    cwd: RACINE,
    encoding: "utf-8",
    maxBuffer: 32 * 1024 * 1024,
  }),
);

function banqueDe(cartes: Carte[], programme: SceneSocle["programme"] = {}): Banque {
  return {
    domaines: vecteurs.config.domaines,
    quotas: vecteurs.config.quotas,
    cartes,
    progression: vecteurs.config.progression,
    fsrs: vecteurs.config.fsrs,
    semaine_type: vecteurs.config.semaine_type,
    socle: vecteurs.config.socle,
    chapitres: programme.chapitres,
    branches: programme.branches,
  } as Banque;
}

describe("parite de la semaine type avec app/seance.py", () => {
  const banque = banqueDe([]);

  it("couvre les six couleurs de la semaine", () => {
    const couleurs = new Set(vecteurs.quotas.map((q) => q.attendu.couleur));
    expect([...couleurs].sort()).toEqual(
      ["cours", "etude", "exploration", "fondations", "libre", "terrain"],
    );
  });

  for (const scene of vecteurs.quotas) {
    it(`scene ${scene.nom} : meme couleur de jour`, () => {
      const jour = jourOrdinal(scene.date) as number;
      expect(couleurDuJour(banque, jour)).toBe(scene.attendu.couleur);
    });

    it(`scene ${scene.nom} : meme quota de neuf et meme pourquoi`, () => {
      const obtenu = quotaDeNeuf(
        banque,
        scene.attendu.couleur as never,
        scene.dues,
        scene.deja_du_jour,
      );
      expect(obtenu.quota).toBe(scene.attendu.quota);
      expect(obtenu.pourquoi).toEqual(scene.attendu.pourquoi);
    });
  }

  for (const scene of vecteurs.socle) {
    it(`scene socle ${scene.nom} : meme branche visee`, () => {
      const b = banqueDe(scene.cartes, scene.programme);
      const sched = new Planificateur(
        undefined,
        vecteurs.config.fsrs?.retention_souhaitee ?? 0.9,
      );
      const etats = etatsCartes(scene.journal, sched);
      // Le jour courant n'entre pas dans la mesure de remplissage ; on
      // passe celui des fixtures pour rester deterministe.
      const jour = jourOrdinal("2026-08-31") as number;
      expect(brancheSocleLaPlusFaible(scene.cartes, etats, b, jour)).toBe(
        scene.attendu,
      );
    });
  }
});

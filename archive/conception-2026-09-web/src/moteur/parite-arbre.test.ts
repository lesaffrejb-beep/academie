/**
 * La parite de l'arbre entre Python et le miroir TypeScript.
 *
 * Meme geste que parite.test.ts : on ne lit pas un fichier commite, qui
 * peut dater. On lance `python3 app/vecteurs_progression.py --json`
 * depuis la racine du depot, donc le juge est le VRAI progression.py, a
 * l'instant du test.
 *
 * Egalite STRICTE, pas a 1e-4 : un etat de noeud est un mot, pas un
 * flottant. Les remplissages sont deja arrondis a 1e-4 des deux cotes.
 *
 * Les dix scenes couvrent ce que decisions/0028 a tranche, dont les deux
 * pieges : un noeud validé qui le reste quand on lui ajoute des cartes,
 * et un noeud mur revu il y a trente jours qui n'est PAS a revoir.
 */

import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { etatsCartes, jourOrdinal } from "./etats";
import { Planificateur } from "./fsrs";
import { carteMonde, noeudsEtBranches, examensReussis } from "./progression";
import type { Banque, Carte, LigneJournal } from "../donnees/types";

const RACINE = fileURLToPath(new URL("../../..", import.meta.url));

interface NoeudAttendu {
  id: string;
  etat: string;
  remplissage: number;
  cartes_totales: number;
  cartes_acquises: number;
  a_revoir: boolean;
  jours_depuis_derniere_revue: number | null;
  prerequis_satisfaits: boolean;
  jouable: boolean;
}

interface BrancheAttendue {
  domaine: string;
  cle: string;
  remplissage: number;
  ouverte: boolean;
  noeuds: number;
  noeuds_servis: number;
  noeuds_valides: number;
}

interface Scene {
  nom: string;
  cartes: Carte[];
  journal: LigneJournal[];
  attendu: {
    noeuds: NoeudAttendu[];
    branches: BrancheAttendue[];
    cartes_sans_chapitre: number;
  };
}

interface Vecteurs {
  aujourdhui: string;
  config: {
    domaines: Banque["domaines"];
    progression: Banque["progression"];
    fsrs?: { retention_souhaitee?: number };
  };
  programme: { branches: Banque["branches"]; chapitres: Banque["chapitres"] };
  scenes: Scene[];
}

const vecteurs: Vecteurs = JSON.parse(
  execFileSync("python3", ["app/vecteurs_progression.py", "--json"], {
    cwd: RACINE,
    encoding: "utf-8",
    maxBuffer: 32 * 1024 * 1024,
  }),
);

function planificateur(): Planificateur {
  return new Planificateur(undefined, vecteurs.config.fsrs?.retention_souhaitee ?? 0.9);
}

/** La banque telle que app/genere.py la publierait pour ces vecteurs. */
function banqueDe(v: Vecteurs, cartes: Carte[]): Banque {
  return {
    domaines: v.config.domaines,
    quotas: { revisions_par_seance: 10, nouveau_par_seance: 1, plafond_reprise: 20 },
    cartes,
    progression: v.config.progression,
    fsrs: v.config.fsrs,
    chapitres: v.programme.chapitres,
    branches: v.programme.branches,
  } as Banque;
}

describe("parite de l'arbre avec app/progression.py", () => {
  const aujourdhui = jourOrdinal(vecteurs.aujourdhui) as number;

  it("couvre les six etats de noeud", () => {
    const etats = new Set(
      vecteurs.scenes.flatMap((s) => s.attendu.noeuds.map((n) => n.etat)),
    );
    expect([...etats].sort()).toEqual(
      ["a-revoir", "en-cours", "inconnu", "ouvert", "solide", "valide"],
    );
  });

  for (const scene of vecteurs.scenes) {
    it(`scene ${scene.nom} : memes etats de noeud`, () => {
      const banque = banqueDe(vecteurs, scene.cartes);
      const etats = etatsCartes(scene.journal, planificateur());
      const { noeuds } = noeudsEtBranches(
        scene.cartes,
        scene.journal,
        banque,
        etats,
        examensReussis(scene.journal, banque),
        aujourdhui,
      );
      const obtenu = noeuds.map((n) => ({
        id: n.id,
        etat: n.etat,
        remplissage: n.remplissage,
        cartes_totales: n.cartesTotales,
        cartes_acquises: n.cartesAcquises,
        a_revoir: n.aRevoir,
        jours_depuis_derniere_revue: n.joursDepuisDerniereRevue,
        prerequis_satisfaits: n.prerequisSatisfaits,
        jouable: n.jouable,
      }));
      expect(obtenu).toEqual(scene.attendu.noeuds);
    });

    it(`scene ${scene.nom} : memes branches`, () => {
      const banque = banqueDe(vecteurs, scene.cartes);
      const etats = etatsCartes(scene.journal, planificateur());
      const { branches } = noeudsEtBranches(
        scene.cartes,
        scene.journal,
        banque,
        etats,
        examensReussis(scene.journal, banque),
        aujourdhui,
      );
      const obtenu = branches.map((b) => ({
        domaine: b.domaine,
        cle: b.cle,
        remplissage: b.remplissage,
        ouverte: b.ouverte,
        noeuds: b.noeuds,
        noeuds_servis: b.noeudsServis,
        noeuds_valides: b.noeudsValides,
      }));
      expect(obtenu).toEqual(scene.attendu.branches);
    });

    it(`scene ${scene.nom} : memes cartes sans chapitre`, () => {
      const banque = banqueDe(vecteurs, scene.cartes);
      const etats = etatsCartes(scene.journal, planificateur());
      const monde = carteMonde(
        scene.cartes,
        scene.journal,
        banque,
        etats,
        [],
        aujourdhui,
      );
      expect(monde.cartesSansChapitre).toBe(scene.attendu.cartes_sans_chapitre);
      expect(monde.seuilFraicheurJours).toBe(
        vecteurs.config.progression.seuil_fraicheur_jours,
      );
    });
  }
});

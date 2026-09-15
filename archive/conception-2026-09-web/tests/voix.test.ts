/**
 * La voix : chaque cle que les ecrans affichent existe dans
 * contenu/voix.json, avec au moins trois variantes (VOIX.md,
 * decisions/0024). Un texte manquant s'ajoute la-bas, jamais dans
 * src/app/i18n.ts.
 *
 * Le test lit le vrai contenu/voix.json de la racine : pas de copie dans
 * web/, donc pas de divergence possible.
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { CLES_VOIX, LIB } from "../src/app/i18n";

const WEB = fileURLToPath(new URL("..", import.meta.url));
const VOIX = fileURLToPath(new URL("../../contenu/voix.json", import.meta.url));

interface FichierVoix {
  version?: string;
  textes: Record<string, string[]>;
}

const voix = JSON.parse(readFileSync(VOIX, "utf-8")) as FichierVoix;

/** Le tiret cadratin, ecrit par son point de code : ce fichier n'a pas le
 *  droit d'en porter un (tooling/check.py). */
const CADRATIN = String.fromCharCode(0x2014);

function sources(): string[] {
  const sortie: string[] = [];
  const visite = (dossier: string) => {
    for (const nom of readdirSync(dossier)) {
      if (nom === "node_modules" || nom.startsWith(".")) continue;
      const chemin = join(dossier, nom);
      if (statSync(chemin).isDirectory()) visite(chemin);
      else if (nom.endsWith(".ts") || nom.endsWith(".tsx")) sortie.push(chemin);
    }
  };
  visite(join(WEB, "src"));
  return sortie;
}

describe("la voix des ecrans", () => {
  it("contenu/voix.json est lisible", () => {
    expect(voix.textes).toBeTypeOf("object");
    expect(Object.keys(voix.textes).length).toBeGreaterThan(10);
  });

  for (const cle of CLES_VOIX) {
    it(`la cle ${cle} existe et a trois variantes`, () => {
      const variantes = voix.textes[cle];
      expect(variantes, `cle absente de contenu/voix.json : ${cle}`).toBeDefined();
      expect(Array.isArray(variantes)).toBe(true);
      expect(variantes?.length ?? 0).toBeGreaterThanOrEqual(3);
      for (const v of variantes ?? []) {
        expect(typeof v).toBe("string");
        expect(v.trim().length).toBeGreaterThan(0);
      }
    });
  }

  it("chaque cle passee a voix() est declaree dans CLES_VOIX", () => {
    const declarees = new Set<string>(CLES_VOIX);
    const appels = /\bvoix\(\s*["'`]([^"'`]+)["'`]/g;
    for (const chemin of sources()) {
      if (chemin.endsWith(join("src", "app", "i18n.ts"))) continue;
      const texte = readFileSync(chemin, "utf-8");
      for (const m of texte.matchAll(appels)) {
        const cle = m[1] ?? "";
        expect(declarees.has(cle), `${chemin} appelle voix("${cle}") non declaree`).toBe(true);
      }
    }
  });

  it("les libelles d'interface n'ont ni exclamation ni emoji", () => {
    const emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
    for (const [cle, valeur] of Object.entries(LIB)) {
      expect(valeur.includes("!"), `LIB.${cle} porte une exclamation`).toBe(false);
      expect(emoji.test(valeur), `LIB.${cle} porte un emoji`).toBe(false);
      expect(valeur.includes(CADRATIN), `LIB.${cle} porte un tiret cadratin`).toBe(false);
    }
  });

  it("les variantes de voix.json n'ont ni exclamation ni emoji", () => {
    const emoji = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}]/u;
    for (const cle of CLES_VOIX) {
      for (const v of voix.textes[cle] ?? []) {
        expect(v.includes("!"), `${cle} porte une exclamation`).toBe(false);
        expect(emoji.test(v), `${cle} porte un emoji`).toBe(false);
      }
    }
  });

  it("les variables entre accolades sont les memes dans chaque variante", () => {
    for (const cle of CLES_VOIX) {
      const variantes = voix.textes[cle] ?? [];
      const jeux = variantes.map(
        (v) => new Set([...v.matchAll(/\{(\w+)\}/g)].map((m) => m[1] as string)),
      );
      const premier = jeux[0];
      if (!premier) continue;
      for (const jeu of jeux) {
        expect([...jeu].sort(), `${cle} : variables divergentes`).toEqual([...premier].sort());
      }
    }
  });
});

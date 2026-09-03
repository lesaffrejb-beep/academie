/**
 * Aucun hote tiers. Le client ne charge ni script, ni police, ni image
 * d'ailleurs que de lui-meme (cahier ACA-FRONT-2, decisions/0020).
 *
 * Le controle est textuel : toute URL http(s) ecrite dans src/ ou dans
 * index.html doit pointer localhost. Un commentaire qui cite un site est
 * une URL de trop : il se reecrit sans le protocole.
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

const WEB = fileURLToPath(new URL("..", import.meta.url));

const RE_URL = /https?:\/\/[^\s"'`)<>\\]+/g;
const HOTES_TOLERES = new Set(["localhost", "127.0.0.1", "[::1]", "0.0.0.0"]);

function fichiers(racine: string, suffixes: string[]): string[] {
  const sortie: string[] = [];
  const visite = (dossier: string) => {
    for (const nom of readdirSync(dossier)) {
      if (nom === "node_modules" || nom.startsWith(".")) continue;
      const chemin = join(dossier, nom);
      if (statSync(chemin).isDirectory()) visite(chemin);
      else if (suffixes.some((s) => nom.endsWith(s))) sortie.push(chemin);
    }
  };
  visite(racine);
  return sortie;
}

function hoteDe(url: string): string {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

describe("aucun hote tiers", () => {
  const cibles = [
    ...fichiers(join(WEB, "src"), [".ts", ".tsx", ".css"]),
    join(WEB, "index.html"),
  ];

  it("il y a bien des fichiers a inspecter", () => {
    expect(cibles.length).toBeGreaterThan(10);
  });

  for (const chemin of cibles) {
    it(`${chemin.slice(WEB.length)} ne contacte que lui-meme`, () => {
      const texte = readFileSync(chemin, "utf-8");
      const etrangers = (texte.match(RE_URL) ?? [])
        .map(hoteDe)
        .filter((h) => !HOTES_TOLERES.has(h));
      expect(etrangers, `hotes tiers : ${etrangers.join(", ")}`).toEqual([]);
    });
  }

  it("index.html porte une CSP qui n'ouvre que self", () => {
    const html = readFileSync(join(WEB, "index.html"), "utf-8");
    expect(html).toContain("Content-Security-Policy");
    for (const directive of [
      "default-src 'self'",
      "connect-src 'self'",
      "script-src 'self'",
      "font-src 'self'",
      "object-src 'none'",
      "frame-ancestors 'none'",
    ]) {
      expect(html, `CSP sans ${directive}`).toContain(directive);
    }
  });

  it("aucun import de labor ni d'un autre depot", () => {
    for (const chemin of fichiers(join(WEB, "src"), [".ts", ".tsx"])) {
      const texte = readFileSync(chemin, "utf-8");
      expect(texte, chemin).not.toMatch(/from\s+["'][^"']*\b(labor|erp)\//);
    }
  });
});

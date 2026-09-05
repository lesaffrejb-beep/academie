import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import { afterEach, mock, test } from "node:test";
import { distribue, ecrisManifeste, prepare, fichiers } from "../preparer-publication.mjs";

const RACINE = fileURLToPath(new URL("../..", import.meta.url));
const temporaires = [];

function temporaire() {
  const dossier = fs.mkdtempSync(path.join(os.tmpdir(), "academie-publication-test-"));
  temporaires.push(dossier);
  return dossier;
}

function ecrit(racine, nom, contenu) {
  const cible = path.join(racine, nom);
  fs.mkdirSync(path.dirname(cible), { recursive: true });
  fs.writeFileSync(cible, contenu);
}

function permissions(racine, lectureSeule) {
  for (const entree of fs.readdirSync(racine, { withFileTypes: true })) {
    const cible = path.join(racine, entree.name);
    if (entree.isSymbolicLink()) continue;
    if (entree.isDirectory()) permissions(cible, lectureSeule);
    fs.chmodSync(cible, entree.isDirectory() ? lectureSeule ? 0o555 : 0o755 : lectureSeule ? 0o444 : 0o644);
  }
  fs.chmodSync(racine, lectureSeule ? 0o555 : 0o755);
}

afterEach(() => {
  mock.restoreAll();
  for (const dossier of temporaires.splice(0)) {
    permissions(dossier, false);
    fs.rmSync(dossier, { recursive: true, force: true });
  }
});

function distribution(racine) {
  for (const nom of ["index.html", "sw.js", "registerSW.js", "icone.svg", "voix.json",
    "assets/app.js", "assets/app.css", "assets/police.woff2", "images/schema.svg"]) {
    ecrit(racine, nom, nom === "voix.json" ? "{}" : `contenu ${nom}`);
  }
  ecrit(racine, "manifest.webmanifest", "{}");
  ecrit(racine, "banque.json", JSON.stringify({ cartes: [{ image: { fichier: "images/schema.svg" } }] }));
  ecrit(racine, ".vite/manifest.json", JSON.stringify({ "index.html": {
    file: "assets/app.js", css: ["assets/app.css"], assets: ["assets/police.woff2"],
  } }));
  ecrisManifeste(racine);
}

test("un asset manque : aucune partie de la publication existante ne bouge", () => {
  const travail = temporaire();
  const source = path.join(travail, "dist");
  const sortie = path.join(travail, "public");
  distribution(source);
  ecrit(sortie, "index.html", "ancienne page");
  fs.unlinkSync(path.join(source, "assets/app.js"));
  assert.throws(() => distribue(source, sortie), /manifest|absent|fichier/i);
  assert.equal(fs.readFileSync(path.join(sortie, "index.html"), "utf8"), "ancienne page");
  assert.deepEqual(fs.readdirSync(sortie), ["index.html"]);
});

test("les ressources non inventoriees ou alterees refusent la distribution", () => {
  const travail = temporaire();
  const source = path.join(travail, "dist");
  const sortie = path.join(travail, "public");
  distribution(source);
  ecrit(source, "assets/inattendu.js", "hors manifeste");
  assert.throws(() => distribue(source, sortie), /exactement/);
  fs.unlinkSync(path.join(source, "assets/inattendu.js"));
  ecrit(source, "assets/app.js", "contenu altere");
  assert.throws(() => distribue(source, sortie), /Empreinte/);
  assert.equal(fs.existsSync(sortie), false);
});

test("un lien vers le depot ne peut devenir une sortie de publication", () => {
  const travail = temporaire();
  const racine = path.join(travail, "sources");
  const lien = path.join(travail, "lien");
  fs.mkdirSync(racine);
  fs.symlinkSync(racine, lien, "dir");
  assert.throws(() => prepare({ racine, sortie: path.join(lien, "publication-refusee"), travail }), /hors du depot/);
  assert.throws(() => prepare({ racine, sortie: path.join(travail, "public"), travail: path.join(lien, "travail-refuse") }), /hors du depot/);
  assert.equal(fs.existsSync(path.join(racine, "publication-refusee")), false);
  assert.equal(fs.existsSync(path.join(racine, "travail-refuse")), false);
});

test("les ressources precedent l index, le service worker vient en dernier", () => {
  const travail = temporaire();
  const source = path.join(travail, "dist");
  const sortie = path.join(travail, "public");
  distribution(source);
  ecrit(sortie, "assets/ancien.js", "onglet encore ouvert");
  const renomme = fs.renameSync;
  const ordre = [];
  mock.method(fs, "renameSync", (depuis, vers) => {
    ordre.push(path.relative(sortie, vers));
    if (vers === path.join(sortie, "index.html")) {
      for (const nom of ["assets/app.js", "assets/app.css", "assets/police.woff2", "images/schema.svg"]) {
        assert.ok(fs.existsSync(path.join(sortie, nom)), `${nom} avant index.html`);
      }
    }
    return renomme(depuis, vers);
  });
  distribue(source, sortie);
  assert.deepEqual(ordre.slice(-2), ["index.html", "sw.js"]);
  assert.equal(fs.readFileSync(path.join(sortie, "assets/ancien.js"), "utf8"), "onglet encore ouvert");
});

test("les sources en lecture seule construisent ; un build refuse conserve l index", { timeout: 120000 }, () => {
  const travail = temporaire();
  const racine = path.join(travail, "sources");
  const sortie = path.join(travail, "public");
  fs.mkdirSync(racine);
  for (const nom of ["app", "banque", "chapitres", "programme", "contenu", "academie.json"]) {
    fs.cpSync(path.join(RACINE, nom), path.join(racine, nom), {
      recursive: true, filter: (f) => !f.split(path.sep).includes("__pycache__"),
    });
  }
  for (const nom of ["src", "public", "tests", "index.html", "package.json", "package-lock.json",
    "tsconfig.json", "vite.config.ts", "vitest.config.ts", "tailwind.config.ts", "postcss.config.js"]) {
    fs.cpSync(path.join(RACINE, "web", nom), path.join(racine, "web", nom), { recursive: true });
  }
  fs.symlinkSync(path.join(RACINE, "web/node_modules"), path.join(racine, "web/node_modules"), "dir");
  permissions(racine, true);
  const empreintes = () => fichiers(racine).map((nom) => ({ nom,
    hash: createHash("sha256").update(fs.readFileSync(path.join(racine, nom))).digest("hex"),
    mode: fs.statSync(path.join(racine, nom)).mode,
  }));
  const avant = empreintes();
  prepare({ racine, sortie, travail });
  assert.deepEqual(empreintes(), avant, "aucun fichier source ajoute, modifie ou rendu inscriptible");
  for (const nom of ["index.html", "sw.js", "banque.json", "publication-manifeste.json"]) {
    assert.ok(fs.existsSync(path.join(sortie, nom)), nom);
  }
  const banque = JSON.parse(fs.readFileSync(path.join(sortie, "banque.json"), "utf8"));
  assert.ok(banque.cartes.length > 0);
  const parcours = JSON.parse(fs.readFileSync(path.join(racine, "contenu/parcours.json"), "utf8")).parcours;
  assert.ok(parcours.length > 0);
  assert.deepEqual(banque.etudes.parcours, parcours, "les parcours jouables survivent au build isolé");
  for (const carte of banque.cartes) if (carte.image?.fichier) {
    assert.ok(fs.existsSync(path.join(sortie, carte.image.fichier)), carte.image.fichier);
  }
  const entree = path.join(racine, "web/src/main.tsx");
  fs.chmodSync(entree, 0o644);
  fs.writeFileSync(entree, "const invalide: number = null;");
  fs.chmodSync(entree, 0o444);
  ecrit(sortie, "index.html", "index sentinelle");
  assert.throws(() => prepare({ racine, sortie, travail }));
  assert.equal(fs.readFileSync(path.join(sortie, "index.html"), "utf8"), "index sentinelle");
});

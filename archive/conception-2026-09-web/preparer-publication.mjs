import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

const RACINE = fileURLToPath(new URL("..", import.meta.url));
const MANIFESTE = "publication-manifeste.json";
const CLIENT = ["src", "public", "tests", "index.html", "package.json", "package-lock.json",
  "tsconfig.json", "vite.config.ts", "vitest.config.ts", "tailwind.config.ts", "postcss.config.js"];
const DONNEES = ["academie.json", "banque", "chapitres", "programme", "cours"];
const REQUIS = ["index.html", "sw.js", "registerSW.js", "manifest.webmanifest", "icone.svg",
  "banque.json", "voix.json", "catalogue.json", "cours.json", "reprise.html", "reprise.js", ".vite/manifest.json"];

export function fichiers(racine, prefixe = "") {
  return fs.readdirSync(path.join(racine, prefixe), { withFileTypes: true }).flatMap((entree) => {
    const nom = path.posix.join(prefixe, entree.name);
    if (entree.isSymbolicLink()) return [];
    return entree.isDirectory() ? fichiers(racine, nom) : [nom];
  }).sort();
}

function empreinte(fichier) {
  return createHash("sha256").update(fs.readFileSync(fichier)).digest("hex");
}

function relatif(nom) {
  if (typeof nom !== "string" || !nom || path.isAbsolute(nom) || nom.includes("\\")
    || nom.split("/").some((segment) => segment === ".." || segment === "." || !segment)) {
    throw new Error(`Chemin de publication refuse : ${nom}`);
  }
  return nom;
}

function copieModifiable(source, cible) {
  fs.cpSync(source, cible, { recursive: true });
  function autorise(fichier) {
    const stat = fs.lstatSync(fichier);
    if (stat.isSymbolicLink()) throw new Error(`Lien refuse dans les sources de construction : ${fichier}`);
    fs.chmodSync(fichier, stat.isDirectory() ? 0o755 : 0o644);
    if (stat.isDirectory()) for (const nom of fs.readdirSync(fichier)) autorise(path.join(fichier, nom));
  }
  autorise(cible);
}

function cheminReel(cible) {
  if (fs.existsSync(cible)) return fs.realpathSync(cible);
  return path.join(cheminReel(path.dirname(cible)), path.basename(cible));
}

export function ecrisManifeste(source) {
  const entrees = fichiers(source).filter((nom) => nom !== MANIFESTE).map((nom) => ({
    chemin: nom, sha256: empreinte(path.join(source, nom)),
  }));
  fs.writeFileSync(path.join(source, MANIFESTE), JSON.stringify({ version: 1, fichiers: entrees }, null, 2) + "\n");
}

function verifie(source) {
  const manifeste = JSON.parse(fs.readFileSync(path.join(source, MANIFESTE), "utf8"));
  if (manifeste.version !== 1 || !Array.isArray(manifeste.fichiers)) throw new Error("Manifeste de publication illisible");
  const noms = manifeste.fichiers.map((fichier) => relatif(fichier.chemin));
  const presents = fichiers(source).filter((nom) => nom !== MANIFESTE);
  if (new Set(noms).size !== noms.length || JSON.stringify([...noms].sort()) !== JSON.stringify(presents)) {
    throw new Error("Le manifeste ne correspond pas exactement aux fichiers emis");
  }
  for (const nom of REQUIS) if (!noms.includes(nom)) throw new Error(`Fichier requis absent : ${nom}`);
  for (const fichier of manifeste.fichiers) {
    if (empreinte(path.join(source, fichier.chemin)) !== fichier.sha256) {
      throw new Error(`Empreinte differente du manifeste : ${fichier.chemin}`);
    }
  }
  const vite = JSON.parse(fs.readFileSync(path.join(source, ".vite/manifest.json"), "utf8"));
  for (const entree of Object.values(vite)) {
    for (const nom of [entree.file, ...(entree.css ?? []), ...(entree.assets ?? [])]) {
      if (!noms.includes(relatif(nom))) throw new Error(`Asset du manifeste Vite absent : ${nom}`);
    }
    for (const cle of [...(entree.imports ?? []), ...(entree.dynamicImports ?? [])]) {
      if (!vite[cle]) throw new Error(`Import du manifeste Vite absent : ${cle}`);
    }
  }
  const banque = JSON.parse(fs.readFileSync(path.join(source, "banque.json"), "utf8"));
  for (const carte of banque.cartes ?? []) {
    if (carte.image?.fichier && !noms.includes(relatif(carte.image.fichier))) {
      throw new Error(`Image de carte absente : ${carte.image.fichier}`);
    }
  }
  return noms;
}

export function distribue(source, sortie) {
  const noms = verifie(source);
  fs.mkdirSync(sortie, { recursive: true });
  const temporaire = fs.mkdtempSync(path.join(sortie, ".academie-publication-"));
  const ordre = [...noms.filter((nom) => nom !== "index.html" && nom !== "sw.js"), MANIFESTE, "index.html", "sw.js"];
  try {
    // Chaque remplacement est atomique ; les anciens assets restent pour les onglets ouverts.
    for (const nom of ordre) {
      const cible = path.join(sortie, nom);
      fs.mkdirSync(path.dirname(cible), { recursive: true });
      const copie = path.join(temporaire, "fichier");
      fs.copyFileSync(path.join(source, nom), copie);
      fs.renameSync(copie, cible);
    }
  } finally {
    fs.rmSync(temporaire, { recursive: true, force: true });
  }
  return ordre;
}

export function prepare({ racine = RACINE, sortie, travail = os.tmpdir(), python = "python3" }) {
  if (!sortie) throw new Error("Indiquer un dossier de sortie avec --sortie");
  racine = fs.realpathSync(racine);
  sortie = cheminReel(path.resolve(sortie));
  travail = cheminReel(path.resolve(travail));
  for (const dossier of [sortie, travail]) {
    if (dossier === racine || dossier.startsWith(racine + path.sep)) throw new Error("Sortie et travail doivent etre hors du depot source");
  }
  if (travail === sortie || travail.startsWith(sortie + path.sep)) throw new Error("Le travail doit rester hors de la publication");
  if (Number(process.versions.node.split(".")[0]) < 20) throw new Error("Node 20 ou plus est requis");
  const modules = path.join(racine, "web/node_modules");
  for (const nom of ["typescript/bin/tsc", "vite/bin/vite.js"]) {
    fs.accessSync(path.join(modules, nom), fs.constants.R_OK);
  }
  fs.mkdirSync(travail, { recursive: true });
  const atelier = fs.mkdtempSync(path.join(travail, "academie-construction-"));
  const web = path.join(atelier, "web");
  try {
    fs.mkdirSync(web);
    for (const nom of CLIENT) copieModifiable(path.join(racine, "web", nom), path.join(web, nom));
    // copy2 conserve le mode des images : seule la copie de travail devient modifiable.
    for (const nom of DONNEES) copieModifiable(path.join(racine, nom), path.join(atelier, nom));
    fs.symlinkSync(modules, path.join(web, "node_modules"), "dir");
    fs.mkdirSync(path.join(atelier, "contenu"));
    fs.copyFileSync(path.join(racine, "contenu/voix.json"), path.join(atelier, "contenu/voix.json"));
    fs.copyFileSync(path.join(racine, "contenu/parcours.json"), path.join(atelier, "contenu/parcours.json"));
    execFileSync(python, ["-B", path.join(racine, "app/genere.py"), "--couches", "banque",
      "--sortie", path.join(atelier, "site/banque.json")], {
      cwd: racine, env: { ...process.env, ACADEMIE_RACINE: atelier, PYTHONDONTWRITEBYTECODE: "1" },
      encoding: "utf8", maxBuffer: 8 * 1024 * 1024,
    });
    // Vite ecrit son config compile a cote de vite.config.ts : cette copie est modifiable.
    for (const args of [[path.join(modules, "typescript/bin/tsc"), "--noEmit", "--project", path.join(web, "tsconfig.json")],
      [path.join(modules, "vite/bin/vite.js"), "build", "--manifest", "--config", path.join(web, "vite.config.ts")]]) {
      execFileSync(process.execPath, args, { cwd: web, encoding: "utf8", maxBuffer: 8 * 1024 * 1024 });
    }
    const dist = path.join(web, "dist");
    ecrisManifeste(dist);
    return distribue(dist, sortie);
  } finally {
    fs.rmSync(atelier, { recursive: true, force: true });
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { values } = parseArgs({ options: {
      sortie: { type: "string" }, travail: { type: "string" }, racine: { type: "string" }, python: { type: "string" },
    } });
    const noms = prepare(values);
    console.log(`Preparation terminee : ${noms.length} fichiers dans ${path.resolve(values.sortie)}`);
  } catch (erreur) {
    console.error(erreur.stderr?.toString() || erreur.stdout?.toString() || erreur.message);
    process.exitCode = 1;
  }
}

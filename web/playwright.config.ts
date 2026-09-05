/**
 * Playwright pour les preuves de bout en bout d'ACA-FRONT-2.
 *
 * Ces tests ne sont PAS dans `npm test` et ne sont pas dans la porte du
 * depot : ils demandent un navigateur et un build. Le workflow web.yml
 * les exécute en CI ; lancement local : `npm run e2e`.
 *
 * Le serveur est `vite preview` sur le VRAI build : le service worker
 * n'existe pas en developpement, et sans lui « hors-ligne » ne veut rien
 * dire. On teste ce qui est publie, pas ce qui est servi a chaud.
 *
 * Le navigateur : ce depot n'epingle pas de version de Chromium et n'en
 * telecharge pas. `CHROMIUM` pointe l'executable fourni par la machine
 * (variable d'environnement, ou le chemin de l'image Cloud). Si elle est
 * absente, Playwright cherche son propre telechargement.
 */

import { defineConfig, devices } from "@playwright/test";

const CHROMIUM = process.env.CHROMIUM_PATH || undefined;
const PORT = 4173;
const BASE = `http://127.0.0.1:${PORT}/academie/`;

export default defineConfig({
  testDir: "./tests/e2e",
  // Une seule ouvriere : les tests partagent un IndexedDB par contexte et
  // mesurent des temps ; les paralleliser rendrait les mesures fausses.
  workers: 1,
  fullyParallel: false,
  timeout: 60_000,
  expect: { timeout: 10_000 },
  reporter: [["list"]],
  use: {
    baseURL: BASE,
    trace: "retain-on-failure",
    ...devices["Desktop Chrome"],
    launchOptions: { executablePath: CHROMIUM },
  },
  projects: [
    {
      name: "ordinateur",
      use: { viewport: { width: 1280, height: 800 } },
    },
    {
      // Le telephone est la cible reelle (BLUEPRINT §2) : la preuve des
      // trois secondes ne vaut que la ou la seance se joue.
      name: "telephone",
      use: { viewport: { width: 375, height: 812 }, isMobile: false },
    },
  ],
  webServer: {
    command: `npm run build && npm run preview -- --host 127.0.0.1 --port ${PORT} --strictPort`,
    url: BASE,
    reuseExistingServer: !process.env.CI,
    timeout: 180_000,
  },
});

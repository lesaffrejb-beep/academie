import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

/**
 * Les deux donnees que le client lit a l'execution ne sont PAS copiees
 * dans public/ : elles vivent a la racine du depot, ecrites par la
 * chaine Python, et une copie dans web/ divergerait en silence. En plus,
 * `contenu/voix.json` et `site/banque.json` portent des tirets cadratins
 * et des accents que tooling/check.py juge a leur place la-bas et nulle
 * part ailleurs.
 *
 * Le plugin les sert en developpement et les ecrit dans dist/ au build.
 * vite-plugin-pwa les met ensuite en cache (globPatterns couvre *.json).
 */
const DONNEES = [
  { nom: "banque.json", source: new URL("../site/banque.json", import.meta.url) },
  { nom: "voix.json", source: new URL("../contenu/voix.json", import.meta.url) },
] as const;

function donneesDuDepot(): Plugin {
  return {
    name: "academie-donnees-du-depot",
    configureServer(serveur) {
      serveur.middlewares.use((requete, reponse, suite) => {
        const chemin = (requete.url ?? "").split("?")[0] ?? "";
        const trouve = DONNEES.find((d) => chemin.endsWith(`/${d.nom}`));
        if (!trouve) return suite();
        let corps: Buffer;
        try {
          corps = readFileSync(trouve.source);
        } catch {
          reponse.statusCode = 404;
          reponse.end();
          return;
        }
        reponse.setHeader("Content-Type", "application/json; charset=utf-8");
        reponse.setHeader("Cache-Control", "no-store");
        reponse.end(corps);
      });
    },
    buildStart() {
      // Un changement de la banque ou de la voix redemarre le build.
      for (const d of DONNEES) this.addWatchFile(fileURLToPath(d.source));
    },
    generateBundle() {
      for (const d of DONNEES) {
        this.emitFile({
          type: "asset",
          fileName: d.nom,
          source: readFileSync(d.source),
        });
      }
    },
  };
}

// base /academie/ : le client est servi sous ce prefixe (serveur/API.md).
export default defineConfig({
  base: "/academie/",
  plugins: [
    react(),
    donneesDuDepot(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["icone.svg"],
      manifest: {
        name: "Academie",
        short_name: "Academie",
        description: "L'ecole d'un metier, jouee tous les jours.",
        lang: "fr",
        start_url: "/academie/",
        scope: "/academie/",
        display: "standalone",
        background_color: "#0d1117",
        theme_color: "#0d1117",
        icons: [
          {
            src: "icone.svg",
            sizes: "any",
            type: "image/svg+xml",
            purpose: "any maskable",
          },
        ],
      },
      workbox: {
        // La banque fait environ 200 ko : le defaut de Workbox (2 Mo)
        // suffit, on le dit pour que personne ne cherche.
        maximumFileSizeToCacheInBytes: 4 * 1024 * 1024,
        globPatterns: ["**/*.{js,css,html,svg,json,woff2}"],
        navigateFallback: "/academie/index.html",
        cleanupOutdatedCaches: true,
        runtimeCaching: [
          {
            // La banque : servie du cache d'abord, rafraichie en fond.
            urlPattern: ({ url }) => url.pathname.endsWith("/banque.json"),
            handler: "StaleWhileRevalidate",
            options: { cacheName: "academie-banque" },
          },
          {
            urlPattern: ({ url }) => url.pathname.endsWith("/voix.json"),
            handler: "StaleWhileRevalidate",
            options: { cacheName: "academie-voix" },
          },
        ],
      },
      devOptions: { enabled: false },
    }),
  ],
});

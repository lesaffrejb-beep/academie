import type { Config } from "tailwindcss";

/**
 * Aucun hexadecimal ici ni dans un composant : chaque couleur pointe une
 * variable CSS definie dans src/index.css (DIRECTION-ARTISTIQUE.md, 2).
 * La couche visuelle se refait en changeant ce fichier et index.css,
 * sans toucher a src/moteur/.
 */
const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        fond: "var(--c-fond)",
        surface: "var(--c-surface)",
        encre: "var(--c-encre)",
        "encre-2": "var(--c-encre-2)",
        trait: "var(--c-trait)",
        accent: "var(--c-accent)",
        succes: "var(--c-succes)",
        erreur: "var(--c-erreur)",
      },
      borderRadius: { ext: "20px", int: "12px" },
      fontFamily: {
        titre: "var(--f-titre)",
        texte: "var(--f-texte)",
      },
      spacing: { grille: "4px" },
    },
  },
  plugins: [],
};

export default config;

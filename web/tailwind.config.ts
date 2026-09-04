import type { Config } from "tailwindcss";

/**
 * Aucun hexadecimal ici ni dans un composant : chaque couleur, chaque
 * duree, chaque rayon pointe une variable CSS definie dans src/index.css
 * (DIRECTION-ARTISTIQUE.md §2, checklist §9). La couche visuelle se
 * refait en changeant ces deux fichiers, sans toucher a src/moteur/.
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
        "sur-accent": "var(--c-sur-accent)",
        succes: "var(--c-succes)",
        erreur: "var(--c-erreur)",
        brouillard: "var(--c-brouillard)",
      },
      borderRadius: { ext: "var(--r-ext)", int: "var(--r-int)" },
      // UNE ombre, reservee a ce qui flotte (DA §2). Il n'y en a pas
      // d'autre a nommer : un bouton n'a jamais d'ombre (§8 ter).
      boxShadow: { flottante: "var(--ombre-flottante)" },
      fontFamily: {
        titre: "var(--f-titre)",
        texte: "var(--f-texte)",
      },
      spacing: { grille: "4px", marge: "var(--marge)" },
      transitionDuration: {
        retour: "var(--d-retour)",
        ecran: "var(--d-ecran)",
        conquete: "var(--d-conquete)",
      },
      transitionTimingFunction: { mouvement: "var(--e-mouvement)" },
    },
  },
  plugins: [],
};

export default config;

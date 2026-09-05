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
        "surface-elevee": "var(--c-surface-elevee)",
        "surface-creuse": "var(--c-surface-creuse)",
        "surface-dock": "var(--c-surface-dock)",
        encre: "var(--c-encre)",
        "encre-2": "var(--c-encre-2)",
        "encre-3": "var(--c-encre-3)",
        trait: "var(--c-trait)",
        "bordure-subtile": "var(--c-bordure-subtile)",
        "bordure-forte": "var(--c-bordure-forte)",
        accent: "var(--c-accent)",
        "accent-fond": "var(--c-accent-fond)",
        "accent-texte": "var(--c-accent-texte)",
        "sur-accent": "var(--c-sur-accent)",
        "surface-fond": "var(--c-surface-fond)",
        succes: "var(--c-succes)",
        "succes-fond": "var(--c-succes-fond)",
        erreur: "var(--c-erreur)",
        "erreur-fond": "var(--c-erreur-fond)",
        avertissement: "var(--c-avertissement)",
        "avertissement-fond": "var(--c-avertissement-fond)",
        brouillard: "var(--c-brouillard)",
      },
      borderRadius: {
        xs: "var(--r-xs)",
        sm: "var(--r-sm)",
        int: "var(--r-int)",
        ext: "var(--r-ext)",
        carte: "var(--r-carte)",
        pilule: "var(--r-pilule)",
      },
      boxShadow: {
        flottante: "var(--ombre-flottante)",
        carte: "var(--ombre-carte)",
        dock: "var(--ombre-dock)",
        surlevee: "var(--ombre-surlevee)",
        pilule: "var(--ombre-pilule)",
      },
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

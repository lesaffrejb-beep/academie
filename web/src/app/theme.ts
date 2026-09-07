/** Papier (defaut) ou Nuit, et la palette d'accent par RANG de domaine. */

export type Theme = "nuit" | "papier";

const CLE = "academie.theme";

export function themeCourant(): Theme {
  try {
    const v = localStorage.getItem(CLE);
    if (v === "nuit" || v === "papier") return v;
  } catch {
    // Stockage refuse : Papier, le defaut.
  }
  return "papier";
}

export function poseTheme(theme: Theme): void {
  document.documentElement.setAttribute("data-theme", theme);
  try {
    localStorage.setItem(CLE, theme);
  } catch {
    // Sans persistance, le theme vaut pour la session.
  }
}

/**
 * L'accent vient du RANG du domaine, jamais de son nom : un autre metier
 * herite des palettes sans rien coder (DIRECTION-ARTISTIQUE.md 2).
 */
export function accentDuRang(_rang: number): string {
  return "var(--c-rang-1)";
}

/** Identité de cet onglet, séparée du cookie commun au navigateur. */
export interface Compte {
  id: string; titre_affiche: string; cree_le: string; cursus: string | null;
  reglages?: {visibilite?: boolean};
}
let identite: Compte | null = null;
export const compteActuel = () => identite;
export function poseCompte(c: Compte | null) { identite = c; }
const MEMOIRE = "academie-compte-reprise";
export function memoriseCompte(c: Compte) {
  try {localStorage.setItem(MEMOIRE, JSON.stringify(c));} catch { /* reprise hors ligne indisponible */ }
}
export function compteMemorise(): Compte | null {
  try { const c = JSON.parse(localStorage.getItem(MEMOIRE) ?? "null");
    return c && typeof c.id === "string" && typeof c.titre_affiche === "string"
      && (c.cursus === null || typeof c.cursus === "string") ? c as Compte : null;
  } catch { return null; }
}
export function oublieCompte(diffuse = true) {
  try {localStorage.removeItem(MEMOIRE);if (diffuse) localStorage.setItem("academie-session-fermee", String(Date.now()));} catch { /* accès refusé */ }
}
export const nomJournal = (id: string) => `academie-journal-compte:${id}`;
export const clePrivee = (cle: string, id = identite?.id ?? "anonyme") => `${cle}:compte:${id}`;
export function valideCompte(mail: string, mdp: string, pseudo: string): string {
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail.trim())) return "Indique une adresse mail valide.";
  if (!pseudo.trim() || pseudo.trim().length > 60) return "Choisis un pseudo entre 1 et 60 caractères.";
  if (mdp.length < 12 || mdp.length > 256) return "Choisis un mot de passe entre 12 et 256 caractères.";
  return "";
}

/** Identité de cet onglet, séparée du cookie commun au navigateur. */
export interface Compte {
  compte_personnel?: boolean;
  cursus_inscrits?: string[];
  id: string; titre_affiche: string; cree_le: string; cursus: string | null;
  reglages?: {visibilite?: boolean};
}
let identite: Compte | null = null;
export const compteActuel = () => identite;
export function poseCompte(c: Compte | null) { identite = c; }
const MEMOIRE = "academie-compte-reprise";
export function memoriseCompte(c: Compte) {
  // Une réponse d'inscription contient aussi une clé : seule l'identité persiste.
  const identite = {id:c.id,titre_affiche:c.titre_affiche,cree_le:c.cree_le,cursus:c.cursus,
    compte_personnel:c.compte_personnel,cursus_inscrits:c.cursus_inscrits,reglages:{visibilite:c.reglages?.visibilite}};
  try {localStorage.setItem(MEMOIRE, JSON.stringify(identite));} catch { /* reprise hors ligne indisponible */ }
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
export function valideCompte(phrase: string, pseudo: string): string {
  if (!pseudo.trim() || pseudo.trim().length > 60) return "Choisis un pseudo entre 1 et 60 caractères.";
  if (phrase.length < 12 || phrase.length > 256) return "Choisis un mot de passe entre 12 et 256 caractères.";
  return "";
}

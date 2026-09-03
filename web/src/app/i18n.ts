/**
 * Le SEUL fichier du client qui porte des chaines affichees.
 *
 * Deux registres :
 *   - `LIB` : les libelles d'interface (boutons, titres d'ecran). Ils
 *     n'ont pas de variante, ils ne sont pas de la voix.
 *   - la voix : contenu/voix.json, copie dans public/voix.json. Chaque
 *     cle a au moins trois variantes ; la graine de la seance en choisit
 *     une. Un texte manquant s'ajoute par une ligne dans
 *     contenu/voix.json, jamais ici (cahier ACA-FRONT-2).
 *
 * tests/voix.test.ts verifie que chaque cle de CLES_VOIX existe.
 */

export const LIB = {
  app: "Academie",
  chargement: "Chargement",
  arbre: "Arbre",
  boite: "Boite",
  profil: "Profil",
  credits: "Credits",
  confiance: "Confiance",
  seance: "Seance",
  domaine: "Domaine",
  noeud: "Noeud",
  cloture: "Cloture",
  reviser: "Reviser",
  continuer: "Continuer",
  etudier: "Etudier",
  epreuve: "Epreuve",
  auHasard: "Au hasard",
  bientot: "Bientot",
  reveler: "Voir la reponse",
  suivante: "Suivante",
  fermer: "Fermer",
  retour: "Retour",
  quitter: "Quitter",
  note1: "Rate",
  note2: "Dur",
  note3: "Bien",
  note4: "Facile",
  jetaisSur: "J'etais sur",
  sources: "Sources",
  provenance: "Provenance",
  carteFausse: "Cette carte est fausse",
  exporter: "Exporter le journal",
  deposer: "Deposer",
  file: "File d'attente",
  theme: "Theme",
  themeNuit: "Nuit",
  themePapier: "Papier",
  cartesDues: "cartes dues",
  cartesNeuves: "neuves",
  remplissage: "remplissage",
  niveau: "Niveau",
  points: "points",
  serie: "jours de suite",
  vide: "Rien a montrer",
  enAttente: "en attente d'envoi",
  horsLigne: "Hors ligne : tout est garde ici et partira au retour du reseau.",
} as const;

/** Les cles de voix que les ecrans affichent. voix.test.ts les verifie. */
export const CLES_VOIX = [
  "cap.jour",
  "cap.rien",
  "cap.reprise",
  "cap.sans_envie",
  "domaine.bandeau",
  "reponse.juste",
  "reponse.fausse",
  "reponse.confiante",
  "reponse.carnet",
  "cloture.stabilisees",
  "cloture.demain",
  "cloture.socle",
  "noeud.a_revoir",
  "noeud.inconnu",
  "source.sans_source",
  "source.a_recouper",
  "source.signaler",
  "boite.glisse",
  "erreur.reseau",
  "erreur.banque",
] as const;

export type CleVoix = (typeof CLES_VOIX)[number];

type Voix = { version?: string; textes: Record<string, string[]> };

let charge: Voix | null = null;

export async function chargeVoix(): Promise<void> {
  for (const chemin of ["/academie/voix.json", "./voix.json"]) {
    try {
      const r = await fetch(chemin, { credentials: "same-origin" });
      if (!r.ok) continue;
      const v = (await r.json()) as Voix;
      if (v && v.textes) {
        charge = v;
        return;
      }
    } catch {
      // Pas de voix : les ecrans affichent la cle, jamais une phrase inventee.
    }
  }
}

/**
 * Une variante, choisie par la graine. Sans voix chargee, rend la cle :
 * un texte manquant se voit, il ne se remplace pas par une invention.
 */
export function voix(
  cle: CleVoix,
  variables: Record<string, string | number> = {},
  graine = 0,
): string {
  const variantes = charge?.textes?.[cle];
  if (!variantes || !variantes.length) return cle;
  const choisie = variantes[Math.abs(Math.trunc(graine)) % variantes.length] ?? cle;
  return choisie.replace(/\{(\w+)\}/g, (tel, nom: string) =>
    nom in variables ? String(variables[nom]) : tel,
  );
}

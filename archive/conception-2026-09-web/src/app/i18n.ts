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
  app: "Académie",
  chargement: "Chargement",
  arbre: "Arbre",
  boite: "Boîte",
  profil: "Profil",
  credits: "Crédits",
  confiance: "Confiance",
  seance: "Séance",
  domaine: "Domaine",
  noeud: "Nœud",
  cloture: "Clôture",
  reviser: "Réviser",
  continuer: "Continuer",
  etudier: "Étudier",
  epreuve: "Épreuve",
  auHasard: "Au hasard",
  bientot: "Bientôt",
  reveler: "Voir la réponse",
  suivante: "Suivante",
  fermer: "Fermer",
  retour: "Retour",
  quitter: "Quitter",
  // Les quatre notes FSRS, dans les mots d'adulte de la DA §5. « Raté »
  // et « Facile » etaient les mots du moteur ; ceux-ci sont les mots du
  // joueur, et ils disent ce qu'on lui demande de juger : est-ce que ca
  // revient, et a quel prix.
  note1: "À revoir",
  note2: "Difficile",
  note3: "Bien",
  note4: "Évident",
  jetaisSur: "J'étais sûr",
  sources: "Sources",
  provenance: "Provenance",
  aRecouper: "À recouper",
  sansSource: "Sans source retrouvée",
  verifieLe: "vérifié le",
  relueLe: "relu le",
  sourcesConcordantes: "sources concordantes",
  carteFausse: "Cette carte est fausse",
  exporter: "Exporter le journal",
  deposer: "Déposer",
  file: "File d'attente",
  theme: "Thème",
  themeNuit: "Nuit",
  themePapier: "Papier",
  cartesDues: "cartes dues",
  carteDue: "carte due",
  cartesNeuves: "neuves",
  carteNeuve: "neuve",
  synchroniser: "Réessayer la synchronisation",
  synchronisationConnexion: "La session n'est plus reconnue. Le journal reste sur cet appareil.",
  synchronisationIndisponible: "La synchronisation est indisponible. Le journal reste sur cet appareil.",
  exportIndisponible: "Le journal n'a pas pu être exporté. Réessayez.",
  remplissage: "remplissage",
  niveau: "Niveau",
  points: "points",
  serie: "jours de suite",
  vide: "Rien à montrer",
  enAttente: "en attente d'envoi",
  horsLigne: "Hors ligne : tout est gardé ici et partira au retour du réseau.",
  // Raccourcis clavier de la DA §8 ter, annonces au lecteur d'ecran.
  raccourcis: "Espace révèle, 1 à 4 notent, Échap sort.",
  explorerDomaine: "Explorer le domaine",
  programme: "Programme",
  chapitres: "chapitres",
  cartes: "cartes",
  cartesDisponibles: "cartes disponibles",
  socle: "Socle",
  aExplorer: "À explorer",
  aEcrire: "À écrire",
  chapitreSansCarte: "Ce chapitre n'a pas encore de carte disponible.",
  reviserChapitre: "Réviser ce chapitre",
  prerequis: "Prérequis",
  objectifs: "Objectifs",
  aucunPrerequis: "Aucun prérequis",
  cartesNonRattachees: "Exercices de rappel hors chapitre",
  domainePrecedent: "Domaine précédent",
  domaineSuivant: "Domaine suivant",
  zoomPlus: "Agrandir l'arbre",
  zoomMoins: "Réduire l'arbre",
  recentrer: "Recentrer l'arbre",
  rechercheChapitre: "Rechercher un chapitre",
  tousNiveaux: "Tous les niveaux",
  aucunChapitre: "Aucun chapitre ne correspond.",
  retourDomaine: "Retour au domaine",
  joursJoues: "jours joués",
  revisions: "révisions",
  activite: "Activité",
  derniereActivite: "Dernières réponses",
  aucuneActivite: "Les premières réponses apparaîtront ici.",
  journal: "Journal",
  synchronisation: "Synchronisation",
  masquerGrain: "Grain du fond",
  apparence: "Apparence",
  progression: "Progression",
  apercu: "Aperçu du domaine",
  chapitre: "Chapitre",
  plus: "Plus",
  carteIndisponible: "Carte indisponible",
  lignesJournal: "lignes de journal",
  rejetsJournal: "réponses à vérifier",
  boiteConnexion: "Connecte-toi pour retrouver ta boîte.",
  boiteIndisponible: "La boîte est indisponible. Le texte reste dans ce champ.",
  boiteVide: "Aucune idée en attente.",
  boiteATraiter: "À traiter",
  boitePropose: "Chapitre proposé",
  boiteRattache: "Rattaché",
  boiteEcarte: "Écarté",
  taReponse: "Ta réponse",
  correction: "Correction",
  vigilance: "Vigilance",
  noteConfiance: "Note de confiance",
  imageIndisponible: "L'illustration n'a pas pu être chargée.",
  illustrationCarte: "Illustration de la carte",
  enregistrementImpossible: "L'enregistrement a échoué. Ta réponse reste affichée ; réessaie.",
  enregistrer: "Enregistrement",
  reessayer: "Réessayer",
  seanceTerminee: "La séance est terminée.",
  bilanDuJour: "Aujourd'hui",
  reponsesDuJour: "réponses aujourd'hui",
  cartesStabilisees: "cartes stabilisées",
  retournerArbre: "Retour à l'arbre",
} as const;

export const ETATS_NOEUD = {
  inconnu: "À explorer", ouvert: "Ouvert", "en-cours": "En cours",
  solide: "Solide", valide: "Validé", "a-revoir": "À revoir",
} as const;

export const TYPES_CARTE: Record<string, string> = {
  flash: "Rappel", qcm: "QCM", photo: "Photo", relier: "Relier", datation: "Chronologie",
  plan: "Lecture de plan", cas: "Cas", libre: "Réponse libre", role: "Mise en situation",
  dessin: "Dessin", feuille_blanche: "Feuille blanche", synthese: "Synthèse", lecture: "Lecture",
};

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

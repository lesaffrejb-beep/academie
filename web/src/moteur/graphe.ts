import type { Noeud } from "./progression";

export interface LienPrerequis { source: string; cible: string; interDomaine: boolean }

/** Projection du programme reçu : aucune inférence depuis rangs ou branches. */
export function voisinageChapitre(noeuds: Noeud[], id: string) {
  const parId = new Map(noeuds.map(n => [n.id, n]));
  const centre = parId.get(id) ?? null;
  const prerequis = centre?.prerequis.map(p => parId.get(p)).filter((n): n is Noeud => Boolean(n)) ?? [];
  const suites = centre ? noeuds.filter(n => n.prerequis.includes(id)) : [];
  const liens: LienPrerequis[] = centre ? [
    ...prerequis.map(n => ({source: n.id, cible: id, interDomaine: n.domaine !== centre.domaine})),
    ...suites.map(n => ({source: id, cible: n.id, interDomaine: n.domaine !== centre.domaine})),
  ] : [];
  return {centre, prerequis, suites, liens, absents: centre?.prerequis.filter(p => !parId.has(p)) ?? []};
}

function normalise(texte: string) {
  return texte.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLocaleLowerCase("fr").trim();
}

export function chercheChapitres(noeuds: Noeud[], recherche: string, domaine = "", branche = "") {
  const mots = normalise(recherche).split(/\s+/).filter(Boolean);
  return noeuds.filter(n => (!domaine || n.domaine === domaine) && (!branche || n.branche === branche)
    && mots.every(mot => normalise(`${n.titre} ${n.id}`).includes(mot)));
}

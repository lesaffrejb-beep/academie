import { describe, expect, it } from "vitest";
import type { Noeud } from "./progression";
import { chercheChapitres, voisinageChapitre } from "./graphe";

const n = (id: string, prerequis: string[] = [], domaine = "droit", titre = id): Noeud => ({
  id, titre, domaine, branche: "bases", niveau: 1, prerequis,
  cartesTotales: 0, cartesAcquises: 0, remplissage: 0, etat: "inconnu",
  sousBranche: null, derniereRevue: null, joursDepuisDerniereRevue: null, satellite: false,
  aRevoir: false, prerequisSatisfaits: false, jouable: true,
});

describe("graphe du programme, sans progression propre", () => {
  const base = n("base");
  const pont = n("pont", [], "technique", "Énergie partagée");
  const cible = n("cible", ["base", "pont", "absent"]);
  const suite = n("suite", ["cible"]);
  const autre = n("autre");
  const noeuds = [base, pont, cible, suite, autre];
  it("dessine exclusivement les prérequis directs, dans leur sens", () => {
    const g = voisinageChapitre(noeuds, "cible");
    expect(g.centre).toBe(cible);
    expect(g.prerequis).toEqual([base, pont]);
    expect(g.suites).toEqual([suite]);
    expect(g.liens).toEqual([
      { source: "base", cible: "cible", interDomaine: false },
      { source: "pont", cible: "cible", interDomaine: true },
      { source: "cible", cible: "suite", interDomaine: false },
    ]);
    expect(g.absents).toEqual(["absent"]);
  });
  it("ne fabrique ni nœud ni progression pour une référence inconnue", () => {
    expect(voisinageChapitre(noeuds, "inexistant")).toEqual({centre: null, prerequis: [], suites: [], liens: [], absents: []});
    expect(voisinageChapitre(noeuds, "cible").centre?.cartesTotales).toBe(0);
    expect(voisinageChapitre(noeuds, "cible").centre?.etat).toBe("inconnu");
  });
  it("cherche sans accents dans le seul programme reçu et applique les filtres", () => {
    expect(chercheChapitres(noeuds, "ENERGIE")).toEqual([pont]);
    expect(chercheChapitres(noeuds, "", "droit", "bases")).toEqual([base, cible, suite, autre]);
    expect(chercheChapitres(noeuds, "energie", "droit")).toEqual([]);
    expect(chercheChapitres([base], "pont")).toEqual([]);
  });
});

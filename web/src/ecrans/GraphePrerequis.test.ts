import {createElement} from "react";
import {renderToStaticMarkup} from "react-dom/server";
import {expect, it} from "vitest";
import {GraphePrerequis} from "./GraphePrerequis";
import {carteMonde} from "../moteur/progression";
import type {Banque} from "../donnees/types";

it("un prérequis absent du programme reste déclaré, sans se dire inexistant", () => {
  const banque: Banque = {cartes: [], domaines: {}, quotas: {revisions_par_seance: 10, nouveau_par_seance: 10, plafond_reprise: 20}, progression: {
    seuil_stabilite_acquise_jours: 21, seuil_ouverture_region: .75,
    examen_obligatoire_pour_100: true, examen_nb_cartes: 12, examen_score_reussite: .8,
  }, chapitres: [{id: "chapitre", titre: "Un chapitre", domaine: "d", branche: "b", prerequis: ["reference-absente"]}]};
  const monde = carteMonde([], [], banque, new Map(), [], 0);
  const html = renderToStaticMarkup(createElement(GraphePrerequis, {monde, banque, journal: [], jour: 0}));
  expect(html).toContain("Prérequis absent de ce programme");
  expect(html).toContain("reference-absente");
  expect(html).not.toContain("Aucun prérequis déclaré.");
  expect(html).toContain("Aucun prérequis disponible dans ce programme.");
});

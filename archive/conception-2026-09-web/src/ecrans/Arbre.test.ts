import {createElement} from "react";
import {renderToStaticMarkup} from "react-dom/server";
import {expect, it, vi} from "vitest";
import type {Banque, Carte, Lecon, LigneJournal} from "../donnees/types";
import type {CarteMonde} from "../moteur/progression";
import {carteMonde} from "../moteur/progression";
const magasin = vi.hoisted(() => ({banque: null as Banque | null, monde: null as CarteMonde | null,
  etats: new Map(), jour: Math.floor(Date.parse("2026-09-06") / 86400000), journal: [] as LigneJournal[]}));
vi.mock("../app/magasin", () => ({useMagasin: () => magasin}));
import {Arbre} from "./Arbre";

function affiche(journal: LigneJournal[] = []) {
  const carte: Carte = {id: "preuve", domaine: "d", branche: "b", type: "flash", niveau: 1,
    question: "Question", reponse: "Réponse", source: [], verifie: "2026-09-06", statut: "valide"};
  const lecon = {id: "socle", cartes: ["preuve"], statut: "valide", sources: []} as unknown as Lecon;
  const chapitres = ["socle", "prevu", "expire", "extension", "extension-incomplete", "extension-brouillon"]
    .map(id => ({id, titre: id, domaine: "d", branche: "b", satellite: id.startsWith("extension")}));
  const banque: Banque = {cartes: [carte], domaines: {d: {titre: "Domaine", ordre: 1}},
    quotas: {revisions_par_seance: 10, nouveau_par_seance: 10, plafond_reprise: 20},
    progression: {seuil_stabilite_acquise_jours: 21, seuil_ouverture_region: .75,
      examen_obligatoire_pour_100: true, examen_nb_cartes: 12, examen_score_reussite: .8}, chapitres,
    etudes: {version: 1, parcours: [], lecons: {
      socle: lecon, expire: {...lecon, id: "expire", peremption: "2026-09-05"},
      extension: {...lecon, id: "extension"},
      "extension-incomplete": {...lecon, id: "extension-incomplete", cartes: ["absente"]},
      "extension-brouillon": {...lecon, id: "extension-brouillon", statut: "brouillon"},
      "autre-cursus": {...lecon, id: "autre-cursus"},
    }},
  };
  magasin.banque = banque;
  magasin.journal = journal;
  magasin.monde = carteMonde(banque.cartes, journal, banque, new Map(), [], magasin.jour);
  return renderToStaticMarkup(createElement(Arbre));
}

it("sépare le socle prévu des études réellement disponibles et de leurs approfondissements", () => {
  const html = affiche();
  // En-tête et aperçu du domaine : les extensions ne gonflent jamais le socle.
  expect(html.match(/3 chapitres prévus dans le socle/g)).toHaveLength(2);
  expect(html.match(/2 études disponibles : 1 du socle · 1 approfondissement/g)).toHaveLength(2);
  expect(html).not.toContain("6 chapitres");
  expect(html).not.toContain("2/3");
});

it("retire du compteur disponible une étude dont la carte est signalée", () => {
  const html = affiche([{mode: "signalement", carte: "preuve"} as LigneJournal]);
  expect(html.match(/0 études disponibles : 0 du socle · 0 approfondissement/g)).toHaveLength(2);
  expect(html).toContain("3 chapitres prévus dans le socle");
});

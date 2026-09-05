import { describe, it, expect } from "vitest";
import { repriseEtude, etudeDisponible } from "./etude";
import type { Lecon, LigneJournal, Carte } from "../donnees/types";
const lecon = { id:"d.b.c", version:1, statut:"valide", peremption:"2027-01-01", cartes:["c"] } as Lecon;
const carte: Carte = { id:"c", domaine:"d", branche:"b", type:"flash", niveau:1, question:"q", reponse:"r", source:[], verifie:"2026-09-05", statut:"valide", peremption:"2027-01-01" };
describe("étude reprenable", () => {
  it("retire une leçon quand une carte manque ou expire", () => {
    expect(etudeDisponible(lecon, [], [], Math.floor(Date.parse("2026-09-05") / 86400000))).toBe(false);
    expect(etudeDisponible(lecon, [carte], [], 999999)).toBe(false);
  });
  it("ne conclut rien de la simple lecture", () => {
    const journal = [{quand:"2026-09-05T12:00:00Z", nonce:"abcdefgh",mode:"synthese",chapitre:lecon.id,attendus_coches:[],etude_etape:"principe",contenu_version:1}] as LigneJournal[];
    expect(repriseEtude(lecon,journal).terminee).toBe(false);
  });
  it("une nouvelle version ne reprend pas l'ancienne synthèse", () => {
    const journal = [{quand:"2026-09-05T12:00:00Z", nonce:"abcdefgh",mode:"synthese",chapitre:lecon.id,attendus_coches:[0],etude_etape:"terminee",contenu_version:1}] as LigneJournal[];
    expect(repriseEtude({...lecon,version:2},journal).terminee).toBe(false);
  });
});

import { compose } from "./composeur";
import type { Banque } from "../donnees/types";
it("la première séance privilégie les fondations du métier choisi", () => {
  const b = { domaines:{d:{titre:"D",ordre:1}},cartes:[{...carte,id:"avancee",niveau:3},{...carte,id:"base",niveau:1}],quotas:{revisions_par_seance:10,nouveau_par_seance:1,plafond_reprise:20},progression:{seuil_stabilite_acquise_jours:30,seuil_ouverture_region:0.3,examen_obligatoire_pour_100:true,examen_nb_cartes:12,examen_score_reussite:0.8}} as Banque;
  for(let graine=0;graine<20;graine++) expect(compose(b,new Map(),{graine,aujourdhui:Math.floor(Date.parse("2026-09-05") / 86400000)}).nouveau.map(c=>c.id)).toEqual(["base"]);
});

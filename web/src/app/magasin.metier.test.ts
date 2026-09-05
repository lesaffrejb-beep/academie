import { describe, expect, it } from "vitest";
import { journalPourMetier } from "./magasin";
import { etatsCartes, jourOrdinal } from "../moteur/etats";
import { carteMonde } from "../moteur/progression";
import { points } from "../moteur/points";
import { Planificateur } from "../moteur/fsrs";
import type { Banque, Carte, LigneJournal } from "../donnees/types";

function banque(domaine: string): Banque {
  const carte={id:`${domaine}-carte`,domaine,branche:"base",type:"flash",niveau:1,question:"q",reponse:"r",source:[],verifie:"2026-09-05",statut:"valide"} as Carte;
  return {cartes:[carte],domaines:{[domaine]:{titre:domaine,ordre:1}},chapitres:[],quotas:{revisions_par_seance:10,nouveau_par_seance:1,plafond_reprise:20},progression:{seuil_stabilite_acquise_jours:21,seuil_ouverture_region:0.5,examen_obligatoire_pour_100:true,examen_nb_cartes:10,examen_score_reussite:0.8}} as Banque;
}
const copro=banque("droit"), ifsi=banque("pharmaco");
const journal: LigneJournal[]=[
  {quand:"2026-09-05T10:00:00Z",nonce:"abcdefgh",mode:"revision",format:"etude",carte:"droit-carte",note:3},
  {quand:"2026-09-05T10:01:00Z",nonce:"ijklmnop",mode:"examen",region:"droit",score:1},
];
function bilan(b: Banque) {
  const propre=journalPourMetier(journal,b),jour=jourOrdinal("2026-09-05")!,sched=new Planificateur();
  return points(propre,carteMonde(b.cartes,propre,b,etatsCartes(propre,sched),[],jour),jour);
}
describe("indicateurs du métier actif",()=>{
  it("la bascule copro vers IFSI puis retour ne transporte ni rappel ni points ni examen",()=>{
    const avant=bilan(copro);
    expect(avant.revisions).toBe(1);
    expect(avant.xp).toBeGreaterThan(0);
    expect(bilan(ifsi)).toMatchObject({xp:0,revisions:0,cartesTouchees:0,joursJoues:0});
    expect(bilan(copro)).toEqual(avant);
    expect(journal).toHaveLength(2);
  });
  it("ne tronque jamais le journal brut et n'attribue pas un ancien événement sans métier",()=>{
    const brut=[...journal,{quand:"2026-09-05T10:02:00Z",nonce:"qrstuvwx",mode:"synthese",chapitre:"ancien-inconnu",attendus_coches:[]} as LigneJournal];
    const copie=JSON.stringify(brut);
    expect(journalPourMetier(brut,copro)).toEqual(journal);
    expect(JSON.stringify(brut)).toBe(copie);
  });
});

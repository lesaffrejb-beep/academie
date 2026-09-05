import { describe, expect, it } from "vitest";
import type { Carte, Lecon, LigneJournal } from "../donnees/types";
import { etudeDisponible, repriseEtude } from "./etude";
import { jourOrdinal } from "./etats";

const jour = jourOrdinal("2026-09-05")!;
const lecon = {id:"d.b.c",version:1,statut:"valide",verifie:"2026-09-05",peremption:"2027-01-01",cartes:["c"]} as Lecon;
const carte = {id:"c",chapitre:lecon.id,domaine:"d",branche:"b",type:"flash",niveau:1,question:"q",reponse:"r",source:[],verifie:"2026-09-05",statut:"valide",peremption:"2027-01-01"} as Carte;
const evenement = (champs: Partial<LigneJournal> = {}): LigneJournal => ({mode:"synthese",quand:"2026-09-05T10:00:00Z",nonce:"0123456789abcdef",chapitre:lecon.id,contenu_version:1,etude_etape:"principe",attendus_coches:[],...champs});

describe("contre-passe indépendante Étude", () => {
  it("sert le chapitre complet encore valable, y compris son dernier jour", () => {
    expect(etudeDisponible(lecon,[carte],[],jour)).toBe(true);
    expect(etudeDisponible({...lecon,peremption:"2026-09-05"},[carte],[],jour)).toBe(true);
  });
  it.each(["pas-une-date","2027-02-29","2026-13-01","2027-1-1"])("refuse la péremption illisible %s", (peremption) => {
    expect(etudeDisponible({...lecon,peremption},[carte],[],jour)).toBe(false);
  });
  it("retire l'étude si une seule carte est signalée, brouillon ou périmée", () => {
    expect(etudeDisponible(lecon,[carte],[evenement({mode:"signalement",carte:"c"})],jour)).toBe(false);
    expect(etudeDisponible(lecon,[{...carte,statut:"brouillon"}],[],jour)).toBe(false);
    expect(etudeDisponible(lecon,[{...carte,peremption:"2026-09-04"}],[],jour)).toBe(false);
    expect(etudeDisponible({...lecon,statut:"brouillon"},[carte],[],jour)).toBe(false);
  });
  it("reprend le dernier instant réel et conserve la condition d'aide", () => {
    const avant=evenement({quand:"2026-09-05T12:50:00+02:00",nonce:"bbbbbbbb",etude_etape:"principe"});
    const apres=evenement({quand:"2026-09-05T12:10:00+01:00",nonce:"aaaaaaaa",etude_etape:"exercices",exercice_index:1,reponse_libre:"réponse avec indice",aide_utilisee:true});
    expect(repriseEtude(lecon,[apres,avant])).toMatchObject({etape:"exercices",index:1,reponse:"réponse avec indice",aide:true,terminee:false});
  });
  it("une autre version ou un autre chapitre ne termine pas l'étude", () => {
    expect(repriseEtude(lecon,[evenement({contenu_version:2,etude_etape:"terminee"}),evenement({chapitre:"autre",etude_etape:"terminee"})])).toMatchObject({etape:"tentative",commencee:false,terminee:false});
  });
});

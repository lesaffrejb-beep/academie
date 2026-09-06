import {describe,it,expect} from "vitest";
import {associationsDe,combineAssociations} from "./supportSeance";
const paires={gauches:[{id:"1",label:"Observation"},{id:"2",label:"Hypothèse"}],droites:[{id:"a",label:"Mesure"},{id:"b",label:"Supposition"}]};
describe("limites et frontière de la réponse d'association",()=>{
  it("refuse un ajout au-delà du contrat sans tronquer le commentaire",()=>{
    const explication="a".repeat(5000);
    expect(()=>combineAssociations({"1":"a"},explication)).toThrow(/5 000 caractères/);
    expect(explication).toHaveLength(5000);
    expect(combineAssociations({"1":"a"},"a".repeat(4996))).toHaveLength(5000);
  });
  it("effacer les liens garde le commentaire littéral hors de la zone d'associations",()=>{
    const initial=associationsDe("1-a\n2-b",paires);
    expect(initial.liens).toEqual({"1":"a"});expect(initial.explication).toBe("2-b");
    const sansLiens=combineAssociations({},initial.explication);
    const reprise=associationsDe(sansLiens,paires);
    expect(reprise.liens).toEqual({});expect(reprise.explication).toBe("2-b");
    expect(combineAssociations({"1":"a"},reprise.explication)).toBe("1-a\n2-b");
  });
});

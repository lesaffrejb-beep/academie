import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { Lecon, LigneJournal } from "../donnees/types";
import { compareJournal } from "./chronologie";
import { repriseEtude } from "./etude";

// Une transaction IndexedDB rw verrouille les magasins communs, même entre onglets.
const disque = vi.hoisted(() => ({tables:new Map<string,Map<string,Record<string,unknown>>>(),suite:Promise.resolve()}));
vi.mock("dexie", () => {
  class TableMemoire {
    lignes: Map<string,Record<string,unknown>>;
    constructor(nom: string, private cle: string) {
      if (!disque.tables.has(nom)) disque.tables.set(nom,new Map());
      this.lignes = disque.tables.get(nom)!;
    }
    async put(ligne: Record<string,unknown>) {this.lignes.set(String(ligne[this.cle]),ligne);}
    async get(cle: string) {return this.lignes.get(cle);}
    async toArray() {return [...this.lignes.values()];}
    async count() {return this.lignes.size;}
    async delete(cle: string) {this.lignes.delete(cle);}
    async bulkDelete(cles: string[]) {cles.forEach(c=>this.lignes.delete(c));}
    async clear() {this.lignes.clear();}
    limit(n: number) {return {toArray:async()=>[...this.lignes.values()].slice(0,n)};}
  }
  return {default:class {
    version() {return {stores:(schema:Record<string,string>)=>{
      for (const [nom,cle] of Object.entries(schema)) Object.assign(this,{[nom]:new TableMemoire(nom,cle.split(",")[0]??"cle")});
    }};}
    async transaction(_mode:string,...args:unknown[]) {
      const operation=disque.suite.then(()=> (args.at(-1) as ()=>Promise<unknown>)());
      disque.suite=operation.then(()=>undefined,()=>undefined);
      return operation;
    }
  }};
});
import { base, ecris, litJournal, maintenant } from "./journal";
const lecon = {id:"fixture",version:1} as Lecon;
const etape = (nonce:string, etude_etape:LigneJournal["etude_etape"], reponse_libre="") => ({
  nonce, mode:"synthese" as const, chapitre:lecon.id, contenu_version:1,
  attendus_coches:[], etude_etape,reponse_libre,
});
beforeEach(async()=>{
  await Promise.all([base.journal.clear(),base.file.clear(),base.marques.clear(),base.rejets.clear()]);
  vi.useFakeTimers();vi.setSystemTime(new Date("2026-09-05T12:00:00.123Z"));
});
afterEach(()=>{vi.useRealTimers();vi.unstubAllEnvs();});

describe("ordre persistant de creation locale",()=>{
  it("garde les fractions de la vraie horloge",()=>{
    expect(Date.parse(maintenant())).toBe(Date.now());
  });
  it("reprend la derniere etape et la derniere reponse apres actions dans la meme milliseconde",async()=>{
    const debut=await ecris(etape("zzzzzzzz","principe","ancienne reponse"));
    const revision=await ecris({...etape("mmmmmmmm","rappel"),mode:"revision",carte:"c",note:3,format:"etude"});
    const fin=await ecris(etape("aaaaaaaa","synthese","nouvelle reponse"));
    expect(compareJournal(debut,revision)).toBeLessThan(0);
    expect(compareJournal(revision,fin)).toBeLessThan(0);
    expect(await litJournal()).toEqual([debut,revision,fin]);
    expect(repriseEtude(lecon,await litJournal())).toMatchObject({etape:"synthese",reponse:"nouvelle reponse"});
  });
  it("resiste au recul de l'horloge",async()=>{
    const avant=await ecris(etape("zzzzzzzz","principe"));
    vi.setSystemTime(new Date("2026-09-04T12:00:00Z"));
    const apres=await ecris(etape("aaaaaaaa","synthese","finale"));
    expect(compareJournal(avant,apres)).toBeLessThan(0);
    expect(repriseEtude(lecon,await litJournal()).reponse).toBe("finale");
  });
  it("partage le dernier instant avec un autre onglet et apres rechargement du module",async()=>{
    const avant=await ecris(etape("zzzzzzzz","principe"));
    vi.resetModules();
    const autre=await import("./journal");
    const [milieu,apres]=await Promise.all([
      ecris(etape("mmmmmmmm","rappel")),autre.ecris(etape("aaaaaaaa","synthese","finale")),
    ]);
    expect(compareJournal(avant,milieu)).toBeLessThan(0);
    expect(compareJournal(milieu,apres)).toBeLessThan(0);
    expect(repriseEtude(lecon,await autre.litJournal()).reponse).toBe("finale");
  });
  it("reprend un ancien journal sans marque sans reecrire ses identites",async()=>{
    const ancien=await ecris({...etape("zzzzzzzz","principe"),quand:"2026-09-05T12:00:00.123456789Z"});
    vi.setSystemTime(new Date("2026-09-05T11:00:00Z"));
    const nouveau=await ecris(etape("aaaaaaaa","synthese","finale"));
    expect(compareJournal(ancien,nouveau)).toBeLessThan(0);
    expect((await litJournal())[0]).toEqual(ancien);
  });
  it("franchit une seconde et le changement d'heure sans perdre la date locale",async()=>{
    vi.stubEnv("TZ","Europe/Paris");
    vi.setSystemTime(new Date("2026-10-25T00:59:59.999Z"));
    await ecris({...etape("zzzzzzzz","principe"),quand:"2026-10-25T02:59:59.999999+02:00"});
    const suivant=await ecris(etape("aaaaaaaa","synthese"));
    expect(suivant.quand).toBe("2026-10-25T02:00:00.000000+01:00");
    expect(repriseEtude(lecon,await litJournal()).etape).toBe("synthese");
  });
  it("laisse une date et un nonce explicites intacts",async()=>{
    const entree={...etape("importee","synthese"),quand:"2026-08-30T10:00:00.987654321+02:00"};
    expect(await ecris(entree)).toEqual(entree);
    expect(await litJournal()).toEqual([entree]);
  });
});

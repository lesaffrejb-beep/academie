import { describe, expect, it } from "vitest";
import { acquittementValide, ligneValide } from "./api";

const ligne={quand:"2026-09-05T12:00:00Z",mode:"synthese",nonce:"12345678",chapitre:"d.b.c",attendus_coches:[]};
const invalides: [string, unknown[]][] = [
  ["etude_etape",[null,true,[],{},1,"","inconnue"]],
  ["contenu_version",[null,true,[],{},"1",0,-1,1.5]],
  ["reponse_libre",[null,true,[],{},1,"x".repeat(5001),"\u{1f600}".repeat(5001)]],
  ["aide_utilisee",[null,0,1,"false",[],{}]],
  ["exercice_index",[null,true,[],{},"0",-1,0.5]],
];
describe("validation optionnelle Étude à la réception",()=>{
  it.each(["tentative","principe","exercices","synthese","grille","terminee"])("accepte l'étape %s et le texte Unicode à la limite",etude_etape=>{
    expect(ligneValide({...ligne,etude_etape,contenu_version:1,reponse_libre:"\u{1f600}".repeat(5000),aide_utilisee:false,exercice_index:0})).toBe(true);
  });
  for (const [champ,valeurs] of invalides) {
    it(`refuse chaque type ou borne invalide de ${champ}`,()=>{
      for (const valeur of valeurs) expect(ligneValide({...ligne,[champ]:valeur}),`${champ} / ${typeof valeur}`).toBe(false);
    });
  }
  it("accepte les anciens événements et préserve les extensions inconnues",()=>{
    const ancienne={...ligne,extension_historique:{opaque:[1,null,"texte"]}};
    const avant=JSON.stringify(ancienne);
    expect(ligneValide(ancienne)).toBe(true);
    expect(JSON.stringify(ancienne)).toBe(avant);
  });
  it("un acquittement contenant une étape inconnue ne permet pas l'union",()=>{
    const ack={acceptees:1,ignorees:0,jusqu_a:ligne.quand,manquantes:[{...ligne,etude_etape:"fantome"}]};
    expect(acquittementValide(ack,1)).toBe(false);
  });
});

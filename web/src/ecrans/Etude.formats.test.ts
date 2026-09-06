import {createElement} from "react";
import {renderToStaticMarkup} from "react-dom/server";
import {describe,it,expect,vi} from "vitest";
import type {Banque,Carte,Lecon,LigneJournal} from "../donnees/types";
const etat=vi.hoisted(()=>({banque:null as Banque|null,journal:[] as LigneJournal[],jour:0,note:vi.fn(),bilan:null}));
vi.mock("../app/magasin",()=>({useMagasin:()=>etat}));
import {Etude} from "./Etude";
const carte:Carte={id:"preuve",chapitre:"chapitre",domaine:"d",branche:"b",type:"relier",niveau:1,question:"Classe les pièces du dossier.",reponse:"Conserve les inconnues.",source:[],verifie:"2026-09-06",statut:"valide"};
function affiche(c:Carte) {
  const lecon={id:"chapitre",titre:"Titre",version:1,statut:"valide",cartes:[c.id],sources:[],provenance:{},verifie_par:{}} as unknown as Lecon;
  etat.banque={cartes:[c],etudes:{version:1,lecons:{chapitre:lecon},parcours:[]}} as unknown as Banque;
  etat.journal=[{mode:"synthese",chapitre:"chapitre",contenu_version:1,etude_etape:"exercices",exercice_index:0,quand:"2026-09-06T10:00:00Z",nonce:"test-formats"}];
  return renderToStaticMarkup(createElement(Etude,{id:"chapitre"}));
}
describe("les formats interactifs dans le vrai parcours étude",()=>{
  it("offre les associations structurées sans image inventée",()=>{
    const html=affiche({...carte,paires:[{gauche:"Observation",droite:"Mesure"},{gauche:"Hypothèse",droite:"Supposition"}]});
    expect(html).toContain("module-relier");expect(html).toContain("1. Observation");
    expect(html).not.toContain("Le support ne peut pas être chargé");
  });
  it("offre le prompt du rôle à copier",()=>{
    const html=affiche({...carte,type:"role",question:"Dialogue : « Tu es un interlocuteur. Expose ta réserve. »"});
    expect(html).toContain("Copier le prompt");
  });
  it("offre les étapes déclarées d'une datation sans exiger une image absente",()=>{
    const html=affiche({...carte,type:"datation",etapes:[{num:1,titre:"Observer"},{num:2,titre:"Comparer"}]});
    expect(html).toContain("module-datation");expect(html).toContain("Observer");
    expect(html).not.toContain("Le support ne peut pas être chargé");
  });
});

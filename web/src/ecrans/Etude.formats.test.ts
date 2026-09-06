import {createElement} from "react";
import {renderToStaticMarkup} from "react-dom/server";
import {describe,it,expect,vi} from "vitest";
import type {Banque,Carte,Lecon,LigneJournal,Source} from "../donnees/types";
const etat=vi.hoisted(()=>({banque:null as Banque|null,journal:[] as LigneJournal[],jour:0,note:vi.fn(),bilan:null}));
vi.mock("../app/magasin",()=>({useMagasin:()=>etat}));
import {Etude} from "./Etude";
import {ModuleRole} from "./ModulesSeance";
const carte:Carte={id:"preuve",chapitre:"chapitre",domaine:"d",branche:"b",type:"relier",niveau:1,question:"Classe les pièces du dossier.",reponse:"Conserve les inconnues.",source:[],verifie:"2026-09-06",statut:"valide"};
function affiche(c:Carte,etape="exercices",sources:Source[]=[]) {
  const lecon={id:"chapitre",titre:"Titre",version:1,statut:"valide",cartes:[c.id],sources,provenance:{},verifie_par:{},amorce:{reponse_attendue:"Réponse"},lecon:"Leçon"} as unknown as Lecon;
  etat.banque={cartes:[c],etudes:{version:1,lecons:{chapitre:lecon},parcours:[]}} as unknown as Banque;
  etat.journal=[{mode:"synthese",chapitre:"chapitre",contenu_version:1,etude_etape:etape,exercice_index:0,quand:"2026-09-06T10:00:00Z",nonce:"test-formats"} as LigneJournal];
  return renderToStaticMarkup(createElement(Etude,{id:"chapitre"}));
}
describe("les formats interactifs dans le vrai parcours étude",()=>{
  it("affiche le parti déclaré sans transformer l'éditeur en institution",()=>{
    const s={texte:"Document d'un fournisseur",nature:"editeur",parti:"Présente une solution commercialisée par l’auteur."};
    const html=affiche(carte,"principe",[s]);
    expect(html).toContain(s.parti);
    expect(html).not.toContain(">Institution<");
    expect(html).not.toContain("Les sources établissent les règles.");
  });
  it("conserve une nature absente comme non renseignée",()=>{
    const html=affiche(carte,"principe",[{texte:"Document sans nature"}]);
    expect(html).toContain("Nature non renseignée");
    expect(html).not.toContain(">Institution<");
  });
  it.each(["publication-externe","constructor"])("conserve la nature inconnue %s sans qualification inventée",nature=>{
    const html=affiche(carte,"principe",[{texte:"Document à qualifier",nature}]);
    expect(html).toContain(`>${nature}<`);
    expect(html).not.toContain(">Institution<");
  });
  it("offre les associations structurées sans image inventée",()=>{
    const html=affiche({...carte,paires:[{gauche:"Observation",droite:"Mesure"},{gauche:"Hypothèse",droite:"Supposition"}]});
    expect(html).toContain("module-relier");expect(html).toContain("1. Observation");
    expect(html).not.toContain("Le support ne peut pas être chargé");
  });
  it("offre le prompt du rôle à copier",()=>{
    const html=affiche({...carte,type:"role",question:"Dialogue : « Tu es un interlocuteur. Expose ta réserve. »"});
    expect(html).toContain("Copier le prompt");
  });
  it("le rôle conserve le contexte sans révéler l'indice non demandé",()=>{
    const c={...carte,type:"role",question:"Le conseil dit « Ils refusent de payer » ; le procès-verbal indique des pièces manquantes. Explique ce qui reste à vérifier.",aide:"Le partenaire ne doit inventer aucun fait nouveau."} as Carte;
    const html=renderToStaticMarkup(createElement(ModuleRole,{carte:c,reponse:"",surChangementReponse:()=>{},revele:false}));
    expect(html).toContain("le procès-verbal indique des pièces manquantes");
    expect(html).toContain("Explique ce qui reste à vérifier.");
    expect(html).not.toContain(c.aide);
  });
  it("le rôle sans citation fournit lui aussi le scénario à copier",()=>{
    const c={...carte,type:"role",question:"Prépare une réponse au conseil à partir des pièces disponibles."} as Carte;
    const html=renderToStaticMarkup(createElement(ModuleRole,{carte:c,reponse:"",surChangementReponse:()=>{},revele:false}));
    expect(html).toContain(c.question);
    expect(html).toContain("Copier le prompt");
  });
  it("offre les étapes déclarées d'une datation sans exiger une image absente",()=>{
    const html=affiche({...carte,type:"datation",etapes:[{num:1,titre:"Observer"},{num:2,titre:"Comparer"}]});
    expect(html).toContain("module-datation");expect(html).toContain("Observer");
    expect(html).not.toContain("Le support ne peut pas être chargé");
  });
});

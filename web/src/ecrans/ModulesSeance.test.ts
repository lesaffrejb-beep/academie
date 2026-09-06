import {createElement} from "react";
import {describe,it,expect} from "vitest";
import {renderToStaticMarkup} from "react-dom/server";
import {ModuleRelier,ModuleDatation} from "./ModulesSeance";
import type {Carte} from "../donnees/types";
const carte:Carte={id:"preuve",domaine:"d",branche:"b",type:"relier",niveau:1,question:"Classe les pièces du dossier.",reponse:"Conserve les inconnues.",source:[],verifie:"2026-09-06",statut:"valide"};
const props={reponse:"",surChangementReponse:()=>{},revele:false};
describe("les modules ne fabriquent pas le contenu absent",()=>{
  it("garde une réponse libre sans inventer les paires d'un schéma",()=>{
    const html=renderToStaticMarkup(createElement(ModuleRelier,{carte,...props}));
    expect(html).toContain("textarea");
    expect(html).not.toContain("Dépression et aspiration");
    expect(html).not.toContain("Repère 6");
  });
  it("conserve exactement les trois repères explicités dans la question",()=>{
    const question="Relie : (1) économie ; (2) confort ; (3) émissions. Catégories : (a) climat ; (b) usage ; (c) trésorerie.";
    const html=renderToStaticMarkup(createElement(ModuleRelier,{carte:{...carte,question},...props}));
    expect(html).toContain("économie");expect(html).toContain("confort");expect(html).toContain("émissions");
    expect(html).not.toContain("Repère 4");expect(html).not.toContain("Repère 6");
  });
  it("ne greffe aucune procédure juridique sur une question sans chronologie",()=>{
    const html=renderToStaticMarkup(createElement(ModuleDatation,{carte:{...carte,type:"datation"},...props}));
    expect(html).toContain("textarea");
    expect(html).not.toContain("30 jours");expect(html).not.toContain("Mise en demeure");
  });
});


it("les paires structurées gardent leurs identifiants avec un ordre de présentation distinct",()=>{
  const html=renderToStaticMarkup(createElement(ModuleRelier,{carte:{...carte,paires:[{gauche:"Observation",droite:"Mesure"},{gauche:"Hypothèse",droite:"Supposition"},{gauche:"Résultat",droite:"Calcul"}]},...props}));
  expect(html).toContain("1. Observation");expect(html).toContain("2. Hypothèse");
  expect(html.indexOf("Calcul")).toBeLessThan(html.indexOf("Mesure"));
  expect(html).not.toContain("Repère 4");
});

it("une chronologie structurée conserve exactement ses étapes et aucune autre",()=>{
  const html=renderToStaticMarkup(createElement(ModuleDatation,{carte:{...carte,type:"datation",etapes:[{num:1,titre:"Observer"},{num:2,titre:"Comparer"}]},...props}));
  expect(html).toContain("Observer");expect(html).toContain("Comparer");
  expect(html).not.toContain("Mise en demeure");
});

it("préserve les décimales à point dans les repères et chronologies extraits",()=>{
  const paires=renderToStaticMarkup(createElement(ModuleRelier,{carte:{...carte,question:"Associe : (1) Baisse de 2.5 % ; (2) Hausse. Catégories : (a) Valeur 1.2 ; (b) Valeur stable."},...props}));
  expect(paires).toContain("Baisse de 2.5 %");expect(paires).toContain("Valeur 1.2");
  const etapes=renderToStaticMarkup(createElement(ModuleDatation,{carte:{...carte,type:"datation",question:"(1) Observer 2.5 unités ; (2) Comparer 1.2 unités."},...props}));
  expect(etapes).toContain("Observer 2.5 unités");expect(etapes).toContain("Comparer 1.2 unités");
});

it("restaure les associations de la réponse sans interpréter le commentaire",()=>{
  const c={...carte,paires:[{gauche:"Observation",droite:"Mesure"},{gauche:"Hypothèse",droite:"Supposition"}]};
  const html=renderToStaticMarkup(createElement(ModuleRelier,{...props,carte:c,reponse:"1-a\nUne hypothèse ne devient pas 2-b automatiquement."}));
  expect(html).toContain('data-association="a"');expect(html).not.toContain('data-association="b"');
  const inconnu=renderToStaticMarkup(createElement(ModuleRelier,{...props,carte:c,reponse:"99-z\nJe conserve mon raisonnement."}));
  expect(inconnu).not.toContain('data-association="z"');
});

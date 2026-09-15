import type {Carte} from "../donnees/types";
interface Repere {id:string;label:string}
export interface PairesAffichees {gauches:Repere[];droites:Repere[]}
/** Affiche uniquement les repères explicites, jamais ceux d'un exemple métier. */
export function pairesDe(carte:Carte):PairesAffichees|null {
  if (Array.isArray(carte.paires) && carte.paires.length > 0) {
    if (!carte.paires.every(p=>p && typeof p.gauche==="string" && p.gauche.trim() && typeof p.droite==="string" && p.droite.trim())) return null;
    const droites=carte.paires.map((p,i)=>({id:String.fromCharCode(97+i),label:p.droite}));
    return {gauches:carte.paires.map((p,i)=>({id:String(i+1),label:p.gauche})),
      droites:droites.length>1 ? [...droites.slice(-1),...droites.slice(0,-1)] : droites};
  }
  const extrait=(regex:RegExp):Repere[]=>Array.from(carte.question.matchAll(regex),m=>({id:m[1]!.toLowerCase(),label:m[2]!.trim()}));
  const gauches=extrait(/\(([1-9]\d*)\)\s*((?:\.(?=\d)|[^;.\n])+)/g);
  const droites=extrait(/\(([a-z])\)\s*((?:\.(?=\d)|[^;.\n])+)/gi);
  return gauches.length && droites.length
    && new Set(gauches.map(p=>p.id)).size===gauches.length
    && new Set(droites.map(p=>p.id)).size===droites.length ? {gauches,droites} : null;
}
export function etapesDe(carte:Carte):{num:number;titre:string;cible?:boolean}[] {
  if (Array.isArray(carte.etapes) && carte.etapes.length > 0) {
    return carte.etapes.every(e=>e && Number.isSafeInteger(e.num) && typeof e.titre==="string" && e.titre.trim()) ? carte.etapes : [];
  }
  const etapes=Array.from(carte.question.matchAll(/(?:\(([1-9]\d*)\)|(?:^|\n)\s*([1-9]\d*)[.)])\s*((?:\.(?=\d)|[^;.\n])+)/g),m=>({num:Number(m[1]??m[2]),titre:m[3]!.trim()}));
  return etapes.length>1 && new Set(etapes.map(e=>e.num)).size===etapes.length ? etapes : [];
}

/** La première ligne est une liste d'associations ; le reste est une explication. */
export function associationsDe(reponse:string,paires:PairesAffichees|null) {
  const [premiere="",...suite]=reponse.split("\n");
  const liste=/^\s*\d+-[a-z](?:\s*,\s*\d+-[a-z])*\s*$/.test(premiere);
  const lignes=liste ? premiere.split(",").map(p=>p.trim().split("-")) : [];
  const valide=Boolean(paires && lignes.length && lignes.every(([g,d])=>
    paires.gauches.some(p=>p.id===g) && paires.droites.some(p=>p.id===d))
    && new Set(lignes.map(([g])=>g)).size===lignes.length);
  const liens:Record<string,string>={};
  if (valide) for (const [g,d] of lignes) if (g && d) liens[g]=d;
  return {liens,explication:valide || (premiere === "" && suite.length > 0) ? suite.join("\n") : reponse};
}

export function combineAssociations(liens:Record<string,string>,explication:string):string {
  const chaine=Object.entries(liens).sort(([a],[b])=>a.localeCompare(b,undefined,{numeric:true}))
    .map(([g,d])=>`${g}-${d}`).join(", ");
  // Même vide, la première ligne sépare les liens du commentaire littéral.
  const reponse=chaine + (explication ? "\n" + explication : "");
  if (reponse.length>5000) throw new RangeError("Ta réponse dépasserait 5 000 caractères. Raccourcis le texte avant d’ajouter une association.");
  return reponse;
}

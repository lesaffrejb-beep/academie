import Dexie from "dexie";
import { compteActuel, clePrivee } from "../app/compte";
import { ligneValide } from "../donnees/api";
import type { LigneJournal } from "../donnees/types";
import { base, BaseJournal, cleDe } from "./journal";

const PROPRIETAIRE = "compte-de-reprise";
const ORIGINE = "academie-journal";
export interface AncienTravail { total: number; invalides: number; autreCompte: boolean; importe: boolean; enAttente: number; refusees: number; brouillons: number }
const vide: AncienTravail = {total:0,invalides:0,autreCompte:false,importe:false,enAttente:0,refusees:0,brouillons:0};
const sansCle = ({cle:_cle,...l}:LigneJournal & {cle:string}) => l as LigneJournal;
function canonique(v:unknown):string {
  if (Array.isArray(v)) return `[${v.map(canonique).join(",")}]`;
  if (v && typeof v === "object") return `{${Object.entries(v).sort(([a],[b])=>a.localeCompare(b)).map(([k,w])=>`${JSON.stringify(k)}:${canonique(w)}`).join(",")}}`;
  return JSON.stringify(v) ?? "null";
}
export async function ancienTravail():Promise<AncienTravail> {
  const compte=compteActuel(), cible=base;
  if (!compte) return vide;
  const brouillons=anciensBrouillons();
  if (!(await Dexie.exists(ORIGINE))) return {...vide,brouillons:brouillons.size};
  const source=new BaseJournal(ORIGINE);
  try {
    const proprietaire=(await source.marques.get(PROPRIETAIRE))?.valeur;
    if (proprietaire && proprietaire!==compte.id) return {...vide,autreCompte:true};
    const lignes=(await source.journal.toArray()).map(sansCle);
    const valides=lignes.filter(l=>l.mode!=="cursus" && ligneValide(l));
    const connues=new Map((await cible.journal.toArray()).map(l=>[l.cle,sansCle(l)]));
    const nonces=new Set(valides.map(l=>l.nonce));
    const refusees=(await cible.rejets.toArray()).filter(l=>nonces.has(l.nonce)).length;
    const brouillonsCopies=(await cible.marques.get("reprise-brouillons"))?.valeur==="oui";
    return {total:valides.length,invalides:lignes.length-valides.length,autreCompte:false,refusees,brouillons:brouillons.size,
      importe:proprietaire===compte.id && (!brouillons.size || brouillonsCopies) && valides.every(l=>canonique(connues.get(cleDe(l)))===canonique(l)),enAttente:await cible.file.count()};
  } finally {source.close();}
}
/** Réserve la source avant copie : une interruption reste reprenable par le même compte. */
export async function recupereAncienTravail():Promise<number> {
  const compte=compteActuel(), cible=base;
  if (!compte?.cursus || compte.compte_personnel===false) throw Error("Crée ton compte et choisis ton cursus avant la reprise.");
  const brouillons=anciensBrouillons();
  if (!(await Dexie.exists(ORIGINE)) && !brouillons.size) return 0;
  const source=new BaseJournal(ORIGINE);
  try {
    const lignes=await source.transaction("rw",source.journal,source.marques,async()=>{
      const proprietaire=(await source.marques.get(PROPRIETAIRE))?.valeur;
      if (proprietaire && proprietaire!==compte.id) throw Error("Le travail de cet appareil est déjà rattaché à un autre compte.");
      const valides=(await source.journal.toArray()).map(sansCle).filter(l=>l.mode!=="cursus" && ligneValide(l));
      if (valides.length || brouillons.size) await source.marques.put({cle:PROPRIETAIRE,valeur:compte.id});
      return valides;
    });
    let nombre=0;
    await cible.transaction("rw",cible.journal,cible.file,async()=>{
      if (compteActuel()?.id!==compte.id || base!==cible) throw Error("Le compte a changé. Recharge la page avant de reprendre.");
      for(const l of lignes) {
        const cle=cleDe(l), ancienne=await cible.journal.get(cle);
        if (ancienne) {
          if(canonique(sansCle(ancienne))!==canonique(l)) throw Error("Deux versions d’une ancienne réponse diffèrent. Les originaux sont conservés ; demande de l’aide avant de reprendre.");
          continue;
        }
        await cible.journal.put({...l,cle});await cible.file.put({nonce:l.nonce});nombre++;
      }
    });
    for(const [cle,valeur] of brouillons) {
      const destination=clePrivee(cle,compte.id);
      if(localStorage.getItem(destination)===null && sessionStorage.getItem(destination)===null) localStorage.setItem(destination,valeur);
    }
    await cible.marques.put({cle:"reprise-brouillons",valeur:"oui"});
    return nombre;
  } finally {source.close();}
}
function anciensBrouillons():Map<string,string> {
  const resultat=new Map<string,string>();
  for(const stockage of [sessionStorage,localStorage]) {
    for(let i=0;i<stockage.length;i++) {
      const cle=stockage.key(i);
      if(!cle || cle.includes(":compte:") || (!cle.startsWith("academie-etude-brouillon:") && cle!=="academie-boite-brouillon")) continue;
      const valeur=stockage.getItem(cle);if(valeur) resultat.set(cle,valeur);
    }
  }
  return resultat;
}

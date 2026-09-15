import { useEffect, useState } from "react";
import { api } from "../donnees/api";
import { compteActuel, oublieCompte } from "../app/compte";
import { useMagasin } from "../app/magasin";

export function Eleves() {
  const compte=compteActuel(); const {synchronise,bilan}=useMagasin();
  const [titres,setTitres]=useState<Record<string,string>>({});
  const [eleves,setEleves]=useState<{id:string;pseudo:string;cursus:string|null}[]>([]);
  const [visible,setVisible]=useState(compte?.reglages?.visibilite !== false);
  const [erreur,setErreur]=useState(""); const [charge,setCharge]=useState(true); const [occupe,setOccupe]=useState(false);
  async function chargeEleves() {setErreur(""); const r=await api.eleves();setCharge(false);if (!r.ok) {setEleves([]);setErreur(r.motif);} else setEleves(r.valeur.eleves);}
  useEffect(()=>{void chargeEleves();void fetch(`${import.meta.env.BASE_URL}catalogue.json`).then(r=>r.json()).then(d=>setTitres(Object.fromEntries(d.parcours.map((p:{cle:string;titre:string})=>[p.cle,p.titre])))).catch(()=>undefined);},[]);
  async function masque() {setOccupe(true); const r=await api.visibilite(!visible);setOccupe(false);if (!r.ok) setErreur(r.motif);else {setVisible(!visible); if(compte) compte.reglages={...compte.reglages,visibilite:!visible};void chargeEleves();}}
  async function quitte() {setOccupe(true);const r=await api.deconnexion();setOccupe(false);if (!r.ok) setErreur(r.motif);else {oublieCompte();window.location.reload();}}
  return <section className="accueil"><h1>Les élèves</h1><p>Un même lieu pour apprendre. Chacun son cursus, chacun son rythme.</p><p>Seuls le pseudo et le cursus sont visibles ici. Les réponses, erreurs et temps restent privés.</p>
    {erreur && <p role="alert">{erreur}</p>}
    <div className="eleves-outils"><button className="action-etude" onClick={()=>void masque()} disabled={occupe}>{visible ? "Masquer mon profil" : "Rendre mon profil visible"}</button><button onClick={()=>void chargeEleves()}>Actualiser</button></div>
    <p role="status">{visible ? "Ton profil est visible aux élèves de cette Académie." : "Ton profil est masqué."}</p>
    {charge ? <p>Chargement des élèves…</p> : <ul className="eleves-liste">{eleves.map(e=><li key={e.id}><strong>{e.pseudo}{e.id===compte?.id ? " (toi)":""}</strong><span>{e.cursus ? titres[e.cursus] ?? e.cursus : "Cursus à choisir"}</span></li>)}</ul>}
    {!charge && !erreur && eleves.length===0 && <p>Aucun profil visible pour le moment.</p>}
    <h2>Ton espace personnel</h2><p>Connecté sous le pseudo {compte?.titre_affiche}. Les réponses enregistrées restent sur cet appareil et se synchronisent avec ton compte.</p>
    {bilan && <p role="status">{bilan.erreur?.motif ?? (bilan.horsLigne ? "Hors ligne : sauvegarde sur cet appareil." : bilan.enAttente ? `${bilan.enAttente} réponses en attente.` : "Sauvegarde synchronisée.")}</p>}
    <div className="eleves-outils"><button onClick={()=>void synchronise()}>Synchroniser maintenant</button><a href="#/profil">Exporter ma sauvegarde</a><button onClick={()=>void quitte()} disabled={occupe}>Me déconnecter</button></div>
  </section>;
}

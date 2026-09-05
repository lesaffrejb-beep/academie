import {useEffect,useState} from "react";
import {ancienTravail,recupereAncienTravail,type AncienTravail} from "../../moteur/reprise";
import {synchronise} from "../../moteur/journal";
export function Reprise({pseudo}:{pseudo:string}) {
  const [ancien,setAncien]=useState<AncienTravail|null>(null),[erreur,setErreur]=useState(""),[occupe,setOccupe]=useState(false);
  useEffect(()=>{void ancienTravail().then(setAncien).catch(()=>setErreur("La sauvegarde de cet appareil n’est pas accessible."));},[]);
  async function reprend() {
    setOccupe(true);setErreur("");
    try {
      await recupereAncienTravail();const b=await synchronise();
      if(b.erreur || b.horsLigne || b.enAttente || b.rejetees) setErreur(b.erreur?.motif ?? "Travail récupéré sur cet appareil. Reviens en ligne pour le synchroniser.");
      setAncien(await ancienTravail());
    } catch(e) {setErreur(e instanceof Error?e.message:"La reprise n’a pas abouti. Les originaux sont conservés.");}
    finally {setOccupe(false);}
  }
  if(!ancien && !erreur) return null;
  return <section className="compte-reprise"><h3>Ton travail déjà commencé</h3>
    {erreur && <p role="alert">{erreur}</p>}
    {ancien?.autreCompte ? <p>Le travail de cet appareil est déjà rattaché à un autre compte.</p> : (ancien?.total || ancien?.brouillons) ? <>
      {ancien.importe && !ancien.enAttente && !ancien.refusees ? <p role="status">{ancien.total ? "Ancien travail récupéré et synchronisé." : "Brouillons récupérés sur cet appareil."}</p> : <>
        <p>{ancien.total} réponses et étapes enregistrées avant les comptes sont présentes sur cet appareil. Si ce travail est le tien, tu peux le rattacher à <strong>{pseudo}</strong>.</p>
        <p>{ancien.brouillons} brouillons locaux peuvent aussi être récupérés. Les originaux sont conservés. Cette sauvegarde ne pourra être rattachée qu’à ce compte.</p>
        <button className="action-etude" disabled={occupe} onClick={()=>void reprend()}>{occupe?"Récupération en cours…":"Récupérer mon travail sur ce compte"}</button>
      </>}
    </> : <p>Aucune ancienne réponse à récupérer sur cet appareil. Tes nouvelles réponses seront sauvegardées sur ton compte.</p>}
    {Boolean(ancien?.brouillons) && <p>Les brouillons restent sur cet appareil. Valide tes réponses pour les retrouver sur un autre appareil.</p>}
    {Boolean(ancien?.refusees) && <p role="alert">Des anciennes réponses ont été refusées par le serveur. Elles restent conservées ici ; la synchronisation de ce travail n’est pas complète.</p>}
    {Boolean(ancien?.invalides) && <p>{ancien?.invalides} anciennes lignes ne peuvent pas être reprises automatiquement ; elles restent dans la sauvegarde d’origine.</p>}
  </section>;
}

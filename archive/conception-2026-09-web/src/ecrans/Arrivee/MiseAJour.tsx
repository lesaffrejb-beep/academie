import {useEffect,useState} from "react";
export function MiseAJour() {
  const [disponible,setDisponible]=useState(false);
  useEffect(()=>{
    if(!("serviceWorker" in navigator)) return;
    let dejaControle=Boolean(navigator.serviceWorker.controller);
    const changement=()=>{if(dejaControle)setDisponible(true);dejaControle=true;};
    navigator.serviceWorker.addEventListener("controllerchange",changement);
    return ()=>navigator.serviceWorker.removeEventListener("controllerchange",changement);
  },[]);
  if(!disponible)return null;
  return <aside className="mise-a-jour" aria-label="Mise à jour"><p>Une nouvelle version est prête. Termine ta réponse avant de l’ouvrir.</p><button onClick={()=>window.location.reload()}>Ouvrir la nouvelle version</button></aside>;
}

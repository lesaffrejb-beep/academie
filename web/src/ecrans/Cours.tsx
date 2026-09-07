import {useEffect,useState,type ReactNode} from 'react';
import {useMagasin} from '../app/magasin';
interface SourceBrute {id:string;titre:string;url:string;nature:string;etat:string;consulte_le:string|null;portee:string;limites:string}
interface CoursBrut {id:string;titre:string;domaine:string;texte:string;auteur:string;sources:SourceBrute[];liens:string[]}
export function Cours({id}:{id?:string}) {
 const {metier}=useMagasin();const [cours,setCours]=useState<CoursBrut[]>([]);const [erreur,setErreur]=useState('');const [recherche,setRecherche]=useState('');
 useEffect(()=>{if(metier!=='copro')return;let vivant=true;void fetch(`${import.meta.env.BASE_URL}cours.json`).then(r=>{if(!r.ok)throw Error();return r.json();}).then(d=>{if(d.statut!=='brouillon editorial'||!Array.isArray(d.chapitres))throw Error();if(vivant)setCours(d.chapitres);}).catch(()=>{if(vivant)setErreur('Les brouillons ne sont pas disponibles. Réessaie lorsque la connexion revient.');});return()=>{vivant=false;};},[metier]);
 if(metier!=='copro')return <section className="accueil"><h1>Les cours de ton cursus</h1><p>Les études de préparation IFSI sont accessibles depuis Apprendre.</p><a href="#/">Retrouver mes études</a></section>;
 const choisi=cours.find(c=>c.id===id);
 const titres=Object.fromEntries(cours.map(c=>[c.id,c.titre]));
 function refs(texte:string):ReactNode[] {return texte.split(/(\[S:[^\]]+\]|\[C:[^\]]+\])/g).map((part,i)=>{
  const s=/^\[S:([^\]]+)\]$/.exec(part);const c=/^\[C:([^\]]+)\]$/.exec(part);
  if(s){const ref=choisi?.sources.find(x=>x.id===s[1]);return ref&&/^https?:\/\//.test(ref.url)?<a key={i} href={ref.url} target="_blank" rel="noreferrer">[{ref.titre}]</a>:part;}
  if(c)return <a key={i} href={`#/cours/${c[1]}`}>{titres[c[1]!]??c[1]}</a>;
  return part;
 });}
 return <section className="accueil bibliotheque"><a href="#/">Apprendre</a><h1>{choisi?.titre??'Les cours écrits'}</h1><p className="cours-statut">Brouillons éditoriaux. Sources et corrections restent à recouper ; ces textes ne sont pas des études validées.</p>
 {erreur?<p role="alert">{erreur}</p>:!cours.length?<p>Ouverture de la bibliothèque…</p>:id&&!choisi?<p>Ce chapitre n’est pas présent dans cette bibliothèque.</p>:choisi?<>
 <a href="#/cours">Tous les cours</a><p>Rédaction : {choisi.auteur}</p>
 <article className="lecon-texte">{choisi.texte.split(/\n\s*\n/).map((p,i)=>p.startsWith('### ')?<h2 key={i}>{refs(p.replace(/^### /,''))}</h2>:<p key={i}>{refs(p)}</p>)}</article>
 <section><h2>Sources et portée de consultation</h2>{choisi.sources.map(s=><div className="cours-source" key={s.id}><a href={s.url} target="_blank" rel="noreferrer">{s.titre}</a><p>{s.nature}</p><p>{s.etat==='consultee'?`Consultation déclarée : ${s.consulte_le}`:'Source à vérifier'}</p><p>{s.portee}</p><p>{s.limites}</p></div>)}</section>
 </>:<><p>{cours.length} chapitres rédigés. Lis le cas avant sa correction ; aucune progression n’est attribuée à une simple lecture.</p><label>Rechercher un cours<input value={recherche} onChange={e=>setRecherche(e.target.value)} type="search"/></label><ul className="cours-index">{cours.filter(c=>(c.titre+' '+c.domaine).toLocaleLowerCase('fr').includes(recherche.toLocaleLowerCase('fr'))).map(c=><li key={c.id}><a href={`#/cours/${c.id}`}>{c.titre}</a><small>{c.domaine} · brouillon</small></li>)}</ul></>}
 </section>;
}

const $ = (id) => document.getElementById(id);
const COULEURS = ['#75ba9c','#78abc3','#df755e','#e7af51','#9f91c9','#78b3ae','#c08e6e','#83a66a','#bc82a7'];
const CLE = 'academie:revues:v1';

let banque = null;
let file = [];
let position = 0;
let choixActif = null;

function litRevues(){
  try { return JSON.parse(localStorage.getItem(CLE) || '[]'); }
  catch { return []; }
}

function ecritRevue(carte, note){
  const revues = litRevues();
  revues.push({carte:carte.id,note:Number(note),date:new Date().toISOString()});
  localStorage.setItem(CLE, JSON.stringify(revues.slice(-4000)));
}

function texte(el, valeur){ el.textContent = valeur == null ? '' : String(valeur); }
function titreDomaine(id){ return banque?.domaines?.[id]?.titre || id; }

function statistiques(){
  const revues = litRevues();
  const vues = new Set(revues.map(r=>r.carte));
  const total = banque?.cartes?.length || 0;
  const dates = [...new Set(revues.map(r=>String(r.date).slice(0,10)))].sort().reverse();
  let serie=0, curseur=new Date();
  for (let i=0;i<370;i++){
    const d=curseur.toISOString().slice(0,10);
    if(dates.includes(d)){serie++;curseur.setDate(curseur.getDate()-1)}
    else if(i===0){curseur.setDate(curseur.getDate()-1)} else break;
  }
  texte($('progression'), Math.round(100*vues.size/Math.max(total,1)));
  $('progression').append(Object.assign(document.createElement('small'),{textContent:'%'}));
  texte($('revues'), vues.size); texte($('serie'), serie);
  return {revues,vues,total};
}

function rendDomaines(){
  const {vues}=statistiques();
  const cont=$('domaines'); cont.replaceChildren();
  Object.entries(banque.domaines || {}).forEach(([id,config],i)=>{
    const cartes=banque.cartes.filter(c=>c.domaine===id);
    if(!cartes.length) return;
    const acquises=cartes.filter(c=>vues.has(c.id)).length;
    const bouton=document.createElement('button'); bouton.type='button'; bouton.className='domaine';
    bouton.style.setProperty('--accent',COULEURS[i%COULEURS.length]);
    const numero=document.createElement('span'); numero.className='numero'; texte(numero,String(i+1).padStart(2,'0'));
    const h=document.createElement('h3'); texte(h,config.titre || id);
    const p=document.createElement('p'); texte(p,`${acquises} explorée${acquises>1?'s':''} sur ${cartes.length}`);
    const jauge=document.createElement('div'); jauge.className='jauge';
    const niveau=document.createElement('i'); niveau.style.width=`${100*acquises/Math.max(cartes.length,1)}%`; jauge.append(niveau);
    bouton.append(numero,h,p,jauge); bouton.addEventListener('click',()=>demarre(id)); cont.append(bouton);
  });
}

function composeFile(domaine=null){
  const revues=litRevues();
  const derniere=new Map(); revues.forEach(r=>derniere.set(r.carte,r.date));
  const cartes=banque.cartes.filter(c=>!domaine||c.domaine===domaine);
  const neuves=cartes.filter(c=>!derniere.has(c.id));
  const dues=cartes.filter(c=>derniere.has(c.id)).sort((a,b)=>String(derniere.get(a.id)).localeCompare(String(derniere.get(b.id))));
  const melange=(xs)=>xs.map(v=>({v,k:crypto.getRandomValues(new Uint32Array(1))[0]})).sort((a,b)=>a.k-b.k).map(x=>x.v);
  return [...melange(dues).slice(0,8),...melange(neuves).slice(0,Math.max(2,10-Math.min(8,dues.length)))].slice(0,10);
}

function demarre(domaine=null){
  file=composeFile(domaine); position=0;
  if(!file.length) return;
  $('accueil').hidden=true; document.querySelector('.territoires').hidden=true; $('session').hidden=false;
  document.body.style.overflow='hidden'; afficheCarte();
}

function ajouteSources(carte){
  const box=$('sources'); box.replaceChildren();
  (carte.source||[]).forEach((s,i)=>{
    const span=document.createElement('span');
    if(i) span.append(' · ');
    if(s.url && /^https:\/\//.test(s.url)){
      const a=document.createElement('a'); a.href=s.url; a.target='_blank'; a.rel='noopener'; texte(a,s.texte||'Source'); span.append(a);
    } else texte(span,s.texte||'Source');
    box.append(span);
  });
  if(carte.verifie) box.append(` · vérifié le ${carte.verifie}`);
}

function afficheCarte(){
  const c=file[position]; choixActif=null;
  texte($('compteur'),`${position+1} / ${file.length}`); $('avance').style.width=`${100*position/file.length}%`;
  texte($('domaine-carte'),titreDomaine(c.domaine)); texte($('type-carte'),c.type); texte($('niveau-carte'),`niveau ${c.niveau||1}`);
  texte($('question'),c.question); texte($('reponse'),c.reponse); texte($('explication'),c.explication);
  $('explication-bloc').hidden=!c.explication; texte($('vigilance'),c.vigilance); $('vigilance-bloc').hidden=!c.vigilance;
  $('correction').hidden=true; $('notes').hidden=true; $('reveler').hidden=false;
  const img=$('image-carte'); img.hidden=true; img.removeAttribute('src');
  const fichier=c.image?.fichier;
  if(fichier && /^images\/[A-Za-z0-9._/-]+$/.test(fichier)){ img.src=fichier; img.alt=c.image?.alt||'Support de la question'; img.hidden=false; }
  const choix=$('choix'); choix.replaceChildren();
  (c.choix||[]).forEach((option,i)=>{
    const b=document.createElement('button'); b.type='button'; texte(b,option.texte);
    b.addEventListener('click',()=>{[...choix.children].forEach(x=>x.classList.remove('choisi'));b.classList.add('choisi');choixActif=i}); choix.append(b);
  });
  ajouteSources(c); $('question').focus?.();
}

function revele(){ $('correction').hidden=false; $('notes').hidden=false; $('reveler').hidden=true; }
function note(n){ ecritRevue(file[position],n); position++; if(position>=file.length) termine(); else afficheCarte(); }
function termine(){ quitte(); statistiques(); rendDomaines(); texte($('resume'),'Séance terminée. La trace reste sur cet appareil.'); }
function quitte(){ $('session').hidden=true; $('accueil').hidden=false; document.querySelector('.territoires').hidden=false; document.body.style.overflow=''; }

async function charge(){
  try{
    const reponse=await fetch('banque.json',{cache:'no-store'}); if(!reponse.ok) throw new Error(reponse.status);
    banque=await reponse.json();
  }catch(err){
    try{const cache=await caches.open('academie-data-v1');const reponse=await cache.match('banque.json');if(!reponse)throw err;banque=await reponse.json()}
    catch{$('erreur').hidden=false;return}
  }
  if(!Array.isArray(banque.cartes)||!banque.cartes.length){$('erreur').hidden=false;return}
  texte($('resume'),`${banque.cartes.length} cartes vérifiées · banque du ${banque.genere_le}`); rendDomaines();
}

$('commencer').addEventListener('click',()=>demarre()); $('quitter').addEventListener('click',quitte); $('reveler').addEventListener('click',revele);
$('notes').addEventListener('click',e=>{const n=e.target.closest('[data-note]')?.dataset.note;if(n)note(n)});
document.addEventListener('keydown',e=>{if($('session').hidden)return;if(e.key==='Escape')quitte();if(e.key===' '&& !$('reveler').hidden){e.preventDefault();revele()}});
if('serviceWorker' in navigator) navigator.serviceWorker.register('sw.js').catch(()=>{});
charge();

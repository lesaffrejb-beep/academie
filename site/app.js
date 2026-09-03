const $ = (id) => document.getElementById(id);
const NS = 'http://www.w3.org/2000/svg';
const COULEURS = ['#76c7a2','#70b8d5','#f08a68','#e5b454','#aa9ad5','#67b8b0','#c99672','#92b876','#cf8fb1'];
const CLE = 'academie:revues:v1';
const SEUIL_FRAICHEUR = 21;
const POSITIONS = [
  {x:360,y:690},{x:665,y:735},{x:990,y:690},{x:1305,y:720},
  {x:1430,y:430},{x:1190,y:225},{x:835,y:195},{x:500,y:250},{x:1450,y:120}
];
const COTES = [
  'M-106 15 C-105-29-72-67-30-72 C0-91 34-72 57-50 C100-44 116-12 103 20 C118 54 78 78 41 70 C8 91-23 74-47 72 C-88 79-119 52-106 15Z',
  'M-112 8 C-88-23-91-61-48-64 C-22-94 18-77 34-54 C79-72 112-39 101-5 C126 25 97 66 58 62 C32 91-8 77-27 65 C-67 83-118 55-112 8Z',
  'M-108 27 C-120-7-91-39-61-42 C-45-78-3-87 24-62 C59-83 100-56 92-20 C125 2 116 49 77 59 C51 87 7 69-12 72 C-55 91-100 68-108 27Z'
];
const ICONES = {
  pathologie:'M-42 20V-22L0-55 42-22V20M-16 20V-4H16V20',
  equipements:'M0-42V-57M0 42V57M-42 0H-57M42 0H57M-30-30L-42-42M30 30L42 42M30-30L42-42M-30 30L-42 42 M0-31A31 31 0 1 1 0 31A31 31 0 1 1 0-31M0-12A12 12 0 1 1 0 12A12 12 0 1 1 0-12',
  droit:'M0-52V39M-43-31H43M-32-31L-55 10H-9L-32-31M32-31L9 10H55L32-31M-28 39H28',
  procedure:'M-44-35L-16-55L10-18L-18 3ZM4-2L47 41M31 25L15 41M-48 49H15',
  sinistres:'M-20-53C-20-53-53-12-53 12A33 33 0 0 0 13 12C13-12-20-53-20-53ZM28-28C28-28 8-1 8 17A25 25 0 0 0 58 17C58-1 28-28 28-28Z',
  comptabilite:'M-45-26A45 16 0 0 0 45-26A45 16 0 0 0-45-26M-45-26V22A45 16 0 0 0 45 22V-26M-45-1A45 16 0 0 0 45-1',
  energie:'M8-58C19-25 48-18 42 18C36 53 4 60-17 43C-41 23-32-4-11-27C-12-6 5 4 9 20C26 1 18-26 8-58Z',
  plans:'M-55-42L-18-54L18-42L55-54V42L18 54L-18 42L-55 54ZM-18-54V42M18-42V54',
  culture:'M-55-43C-31-51-12-43 0-28C12-43 31-51 55-43V42C31 34 12 42 0 55C-12 42-31 34-55 42ZM0-28V55'
};

let banque = null;
let file = [];
let position = 0;
let choixActif = null;
let modeAmbiance = 'auto';

function svg(nom, attributs={}){
  const el=document.createElementNS(NS,nom);
  Object.entries(attributs).forEach(([k,v])=>el.setAttribute(k,String(v)));
  return el;
}

function litRevues(){
  try { return JSON.parse(localStorage.getItem(CLE) || '[]'); }
  catch { return []; }
}

function ecritRevue(carte, note){
  const revues = litRevues();
  const quand = new Date().toISOString();
  revues.push({carte:carte.id,note:Number(note),date:quand});
  localStorage.setItem(CLE, JSON.stringify(revues.slice(-4000)));
  Journal.ecrire({quand, mode:'revision', format:'seance', carte:carte.id, note:Number(note)});
}

// Journal v1 local + envoi par lots (ACA-JOURNAL-SYNC-1, serveur/API.md).
// Chaque réponse est écrite ici à l'instant, puis part vers
// /academie/api/v1/journal quand le réseau le permet. Une ligne refusée
// va dans `rejets` et le reste repart : la file ne se bloque jamais.
const Journal = (() => {
  const API = '/academie/api/v1';
  const K = {journal:'academie:journal:v1', file:'academie:journal:file', rejets:'academie:journal:rejets', depuis:'academie:journal:depuis'};
  const lit = k => { try { return JSON.parse(localStorage.getItem(k) || '[]'); } catch { return []; } };
  const ecrit = (k, v) => localStorage.setItem(k, JSON.stringify(v));
  const nonce = () => { const b = new Uint8Array(12); crypto.getRandomValues(b); return Array.from(b, x => x.toString(16).padStart(2, '0')).join(''); };
  const cle = l => `${l.quand}|${l.mode}|${l.nonce}`;
  let enCours = false;
  function ecrire(ligne){
    const l = {...ligne, nonce: nonce()};
    const journal = lit(K.journal); journal.push(l); ecrit(K.journal, journal.slice(-20000));
    const file = lit(K.file); file.push(l); ecrit(K.file, file);
    envoyer();
  }
  async function envoyer(){
    if (enCours || !navigator.onLine) return;
    const file = lit(K.file);
    if (!file.length && localStorage.getItem(K.depuis) !== null) return;
    enCours = true;
    try {
      const lot = file.slice(0, 500);
      const reponse = await fetch(API + '/journal', {method:'POST', credentials:'include', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({depuis: localStorage.getItem(K.depuis), lignes: lot})});
      if (reponse.status === 422) {
        const r = await reponse.json();
        if (typeof r.index === 'number' && r.index >= 0) {
          const rejets = lit(K.rejets); rejets.push({ligne: lot[r.index], motif: r.motif}); ecrit(K.rejets, rejets);
          ecrit(K.file, file.filter((_, i) => i !== r.index));
          enCours = false; return envoyer();
        }
        return;
      }
      if (!reponse.ok) return;
      const r = await reponse.json();
      const connues = new Set(lit(K.journal).map(cle));
      const journal = lit(K.journal);
      for (const l of r.manquantes || []) if (!connues.has(cle(l))) journal.push(l);
      journal.sort((a, b) => a.quand < b.quand ? -1 : a.quand > b.quand ? 1 : 0);
      ecrit(K.journal, journal.slice(-20000));
      ecrit(K.file, lit(K.file).filter(l => !lot.some(x => cle(x) === cle(l))));
      if (r.jusqu_a) localStorage.setItem(K.depuis, r.jusqu_a);
      if (lit(K.file).length) { enCours = false; return envoyer(); }
    } catch { /* hors-ligne ou serveur absent : on réessaie au retour du réseau */ }
    finally { enCours = false; }
  }
  window.addEventListener('online', envoyer);
  return {ecrire, envoyer, lit: () => lit(K.journal), rejets: () => lit(K.rejets)};
})();

function texte(el, valeur){ el.textContent = valeur == null ? '' : String(valeur); }
function titreDomaine(id){ return banque?.domaines?.[id]?.titre || id; }
function jourLocal(date=new Date()){
  const y=date.getFullYear(); const m=String(date.getMonth()+1).padStart(2,'0'); const d=String(date.getDate()).padStart(2,'0');
  return `${y}-${m}-${d}`;
}
function joursDepuis(iso){ return iso ? Math.max(0,Math.floor((Date.now()-new Date(iso).getTime())/86400000)) : Infinity; }

function statistiques(){
  const revues = litRevues();
  const vues = new Set(revues.map(r=>r.carte));
  const total = banque?.cartes?.length || 0;
  const dates = [...new Set(revues.map(r=>jourLocal(new Date(r.date))))].sort().reverse();
  let serie=0; const curseur=new Date();
  for (let i=0;i<370;i++){
    const d=jourLocal(curseur);
    if(dates.includes(d)){serie++;curseur.setDate(curseur.getDate()-1)}
    else if(i===0){curseur.setDate(curseur.getDate()-1)} else break;
  }
  const pct=Math.round(100*vues.size/Math.max(total,1));
  texte($('progression'),`${pct}%`); $('progression-jauge').style.width=`${pct}%`;
  texte($('revues'),vues.size); texte($('serie'),serie);
  const derniereParCarte=new Map(); revues.forEach(r=>derniereParCarte.set(r.carte,r.date));
  const derniereParDomaine=new Map();
  banque?.cartes?.forEach(c=>{
    const date=derniereParCarte.get(c.id); const courante=derniereParDomaine.get(c.domaine);
    if(date&&(!courante||date>courante)) derniereParDomaine.set(c.domaine,date);
  });
  return {revues,vues,total,pct,derniereParDomaine,derniere:revues.at(-1)?.date||null};
}

function domainsOrdonnes(){
  return Object.entries(banque.domaines||{}).sort((a,b)=>(a[1].ordre||99)-(b[1].ordre||99));
}

function etatDomaine(id, stats){
  const cartes=banque.cartes.filter(c=>c.domaine===id);
  const acquises=cartes.filter(c=>stats.vues.has(c.id)).length;
  const ratio=acquises/Math.max(cartes.length,1);
  const derniere=stats.derniereParDomaine.get(id);
  let etat='inexploree';
  if(!cartes.length) etat='friche';
  else if(derniere&&joursDepuis(derniere)>SEUIL_FRAICHEUR) etat='perimee';
  else if(acquises) etat=ratio>=.75?'maitrisee':'exploree';
  return {cartes,acquises,ratio,derniere,etat};
}

function cheminRoute(a,b){
  const mx=(a.x+b.x)/2+(b.y-a.y)*.12; const my=(a.y+b.y)/2-(b.x-a.x)*.12;
  return `M${a.x} ${a.y} Q${mx} ${my} ${b.x} ${b.y}`;
}

function ajouteBateau(g,d,reduit,index){
  const bateau=svg('g',{class:'bateau'});
  bateau.append(svg('path',{d:'M-22 7 Q0 21 22 7 L16 18 Q0 28-16 18Z',class:'coque'}));
  bateau.append(svg('path',{d:'M0 6V-24L19 2ZM-3-20L-17 2H-3Z',class:'voile'}));
  if(!reduit){
    const mouvement=svg('animateMotion',{dur:`${18+index*2}s`,repeatCount:'indefinite',path:d,rotate:'auto',begin:`-${index*3}s`});
    bateau.append(mouvement);
  }else bateau.setAttribute('transform','translate(800 450)');
  g.append(bateau);
}

function dessineIcone(g,id){
  const d=ICONES[id]||ICONES.culture;
  g.append(svg('path',{d,class:'icone-ile'}));
}

function dessineIle(id,config,index,stats){
  const p=POSITIONS[index]||{x:800+Math.cos(index)*560,y:450+Math.sin(index)*320};
  const etat=etatDomaine(id,stats); const couleur=COULEURS[index%COULEURS.length];
  const attributs={class:`ile ile-${etat.etat}${etat.cartes.length?'':' ile-vide'}`,transform:`translate(${p.x} ${p.y})`};
  if(etat.cartes.length){attributs.role='button';attributs.tabindex='0'}
  const g=svg('g',attributs);
  g.style.setProperty('--ile',couleur);
  g.setAttribute('aria-label',etat.cartes.length?`${config.titre}, ${etat.acquises} cartes abordées sur ${etat.cartes.length}`:`${config.titre}, terre en friche`);
  const title=svg('title'); title.textContent=g.getAttribute('aria-label'); g.append(title);
  const cote=COTES[index%COTES.length];
  g.append(svg('path',{d:cote,class:'recif'}));
  g.append(svg('path',{d:cote,class:'terre'}));
  const crete=svg('path',{d:cote,class:'crete',transform:'scale(.83)'}); g.append(crete);
  const icone=svg('g',{transform:'translate(0 -5) scale(.72)'}); dessineIcone(icone,id); g.append(icone);
  if(etat.etat==='inexploree'||etat.etat==='perimee'){
    const brume=svg('g',{class:'brume-ile'});
    brume.append(svg('ellipse',{cx:-42,cy:-8,rx:66,ry:24})); brume.append(svg('ellipse',{cx:38,cy:17,rx:75,ry:27}));
    g.append(brume);
  }
  const pct=Math.round(etat.ratio*100);
  const nom=svg('text',{x:0,y:116,'text-anchor':'middle',class:'nom-ile'}); nom.textContent=config.titre; g.append(nom);
  const statut=svg('text',{x:0,y:143,'text-anchor':'middle',class:'statut-ile'});
  statut.textContent=!etat.cartes.length?'Terre en friche':etat.etat==='perimee'?`Brume · dernière visite il y a ${joursDepuis(etat.derniere)} j`:etat.acquises?`${pct}% exploré · ${etat.acquises}/${etat.cartes.length}`:`À cartographier · ${etat.cartes.length} cartes`;
  g.append(statut);
  if(etat.cartes.length){
    const activer=()=>demarre(id); g.addEventListener('click',activer);
    g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();activer()}});
  }
  return {g,p,etat,id,config};
}

function dessineCarte(){
  const stats=statistiques(); const entrees=domainsOrdonnes(); const iles=[];
  const cont=$('iles'); const routes=$('routes'); cont.replaceChildren(); routes.replaceChildren();
  entrees.forEach(([id,config],i)=>{const ile=dessineIle(id,config,i,stats);iles.push(ile);cont.append(ile.g)});
  const reduit=matchMedia('(prefers-reduced-motion: reduce)').matches;
  iles.filter(x=>x.config.arbre!==false).slice(0,-1).forEach((ile,i)=>{
    const suivante=iles.filter(x=>x.config.arbre!==false)[i+1]; if(!suivante)return;
    const d=cheminRoute(ile.p,suivante.p); const ouverte=ile.etat.ratio>=(banque.progression?.seuil_ouverture_region||.75);
    const g=svg('g',{class:`route ${ouverte?'route-ouverte':'route-a-ouvrir'}`});
    g.append(svg('path',{d,class:'route-ombre'})); g.append(svg('path',{d,class:'route-trace'}));
    if(ouverte){
      const pont=svg('path',{d,class:'pont'}); g.append(pont);
    }else ajouteBateau(g,d,reduit,i);
    routes.append(g);
  });
  texte($('cartes-dues'),`${Math.min(banque.quotas?.revisions_par_seance||10,banque.cartes.length)} cartes à jouer`);
  appliqueAmbiance(stats);
}

function rendDomaines(){
  const stats=statistiques(); const cont=$('domaines'); cont.replaceChildren();
  domainsOrdonnes().forEach(([id,config],i)=>{
    const etat=etatDomaine(id,stats); const pct=Math.round(etat.ratio*100);
    const bouton=document.createElement('button'); bouton.type='button'; bouton.className=`domaine domaine-${etat.etat}`; bouton.disabled=!etat.cartes.length;
    bouton.style.setProperty('--accent',COULEURS[i%COULEURS.length]);
    const numero=document.createElement('span'); numero.className='numero'; texte(numero,String(i+1).padStart(2,'0'));
    const tag=document.createElement('span'); tag.className='tag-etat'; texte(tag,!etat.cartes.length?'En friche':etat.etat==='perimee'?'Sous brume':etat.acquises?'Explorée':'Inconnue');
    const h=document.createElement('h3'); texte(h,config.titre||id);
    const p=document.createElement('p'); texte(p,!etat.cartes.length?'Les sources et les cartes arrivent.':`${etat.acquises} abordée${etat.acquises>1?'s':''} sur ${etat.cartes.length}`);
    const jauge=document.createElement('div'); jauge.className='jauge'; const niveau=document.createElement('i'); niveau.style.width=`${pct}%`; jauge.append(niveau);
    bouton.append(numero,tag,h,p,jauge); if(etat.cartes.length)bouton.addEventListener('click',()=>demarre(id)); cont.append(bouton);
  });
}

function composeFile(domaine=null){
  const revues=litRevues(); const derniere=new Map(); revues.forEach(r=>derniere.set(r.carte,r.date));
  const cartes=banque.cartes.filter(c=>!domaine||c.domaine===domaine);
  const neuves=cartes.filter(c=>!derniere.has(c.id));
  const dues=cartes.filter(c=>derniere.has(c.id)).sort((a,b)=>String(derniere.get(a.id)).localeCompare(String(derniere.get(b.id))));
  const melange=(xs)=>xs.map(v=>({v,k:crypto.getRandomValues(new Uint32Array(1))[0]})).sort((a,b)=>a.k-b.k).map(x=>x.v);
  const plafond=banque.quotas?.revisions_par_seance||10; const nouvelles=banque.quotas?.nouveau_par_seance||2;
  return [...melange(dues).slice(0,plafond-nouvelles),...melange(neuves).slice(0,Math.max(nouvelles,plafond-Math.min(plafond-nouvelles,dues.length)))].slice(0,plafond);
}

function demarre(domaine=null){
  file=composeFile(domaine); position=0; if(!file.length)return;
  $('accueil').hidden=true; document.querySelector('.territoires').hidden=true; $('session').hidden=false;
  document.body.style.overflow='hidden'; afficheCarte();
}

function ajouteSources(carte){
  const box=$('sources'); box.replaceChildren();
  (carte.source||[]).forEach((s,i)=>{
    const span=document.createElement('span'); if(i)span.append(' · ');
    if(s.url&&/^https:\/\//.test(s.url)){const a=document.createElement('a');a.href=s.url;a.target='_blank';a.rel='noopener';texte(a,s.texte||'Source');span.append(a)}
    else texte(span,s.texte||'Source'); box.append(span);
  });
  if(carte.verifie)box.append(` · vérifié le ${carte.verifie}`);
}

function afficheCarte(){
  const c=file[position]; choixActif=null;
  texte($('compteur'),`${position+1} / ${file.length}`); $('avance').style.width=`${100*position/file.length}%`;
  texte($('domaine-carte'),titreDomaine(c.domaine)); texte($('type-carte'),c.type); texte($('niveau-carte'),`niveau ${c.niveau||1}`);
  texte($('question'),c.question); texte($('reponse'),c.reponse); texte($('explication'),c.explication);
  $('explication-bloc').hidden=!c.explication; texte($('vigilance'),c.vigilance); $('vigilance-bloc').hidden=!c.vigilance;
  $('correction').hidden=true; $('notes').hidden=true; $('reveler').hidden=false;
  const img=$('image-carte'); img.hidden=true; img.removeAttribute('src'); const fichier=c.image?.fichier;
  if(fichier&&/^images\/[A-Za-z0-9._/-]+$/.test(fichier)){img.src=fichier;img.alt=c.image?.alt||'Support de la question';img.hidden=false}
  const choix=$('choix'); choix.replaceChildren();
  (c.choix||[]).forEach((option,i)=>{const b=document.createElement('button');b.type='button';texte(b,option.texte);b.addEventListener('click',()=>{[...choix.children].forEach(x=>x.classList.remove('choisi'));b.classList.add('choisi');choixActif=i});choix.append(b)});
  ajouteSources(c); $('question').focus();
}

function revele(){$('correction').hidden=false;$('notes').hidden=false;$('reveler').hidden=true}
function note(n){ecritRevue(file[position],n);position++;if(position>=file.length)termine();else afficheCarte()}
function termine(){quitte();dessineCarte();rendDomaines();texte($('resume'),'Expédition terminée. La carte a gardé la trace.')}
function quitte(){$('session').hidden=true;$('accueil').hidden=false;document.querySelector('.territoires').hidden=false;document.body.style.overflow=''}

function phaseAuto(){const h=new Date().getHours();return h<6||h>=22?'nuit':h<9?'aube':h<18?'jour':'crepuscule'}
function appliqueAmbiance(stats=statistiques()){
  const phase=modeAmbiance==='auto'?phaseAuto():modeAmbiance; document.body.dataset.phase=phase;
  const age=joursDepuis(stats.derniere); const navigation=age===0?'mer claire':age<=7?'brise régulière':age<=SEUIL_FRAICHEUR?'brume au large':'mer dormante';
  const noms={aube:'Aube',jour:'Grand jour',crepuscule:'Crépuscule',nuit:'Nuit étoilée'};
  texte($('meteo'),`${phase==='nuit'?'☾':phase==='jour'?'☀':'◐'} ${noms[phase]} · ${navigation}`);
  texte($('ambiance'),modeAmbiance==='auto'?'Auto':phase==='jour'?'Clair':'Nuit');
}
function changeAmbiance(){modeAmbiance=modeAmbiance==='auto'?'jour':modeAmbiance==='jour'?'nuit':'auto';appliqueAmbiance()}
function activeAuClavier(el,action){el.addEventListener('click',action);el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();action()}})}

function dessineEtoiles(){
  const g=document.querySelector('.etoiles');
  for(let i=0;i<70;i++){const x=(i*197)%1580+10;const y=(i*i*37)%430+8;g.append(svg('circle',{cx:x,cy:y,r:i%9===0?2.2:1.2}))}
}

async function charge(){
  try{const reponse=await fetch('banque.json',{cache:'no-store'});if(!reponse.ok)throw new Error(reponse.status);banque=await reponse.json()}
  catch(err){try{const cache=await caches.open('academie-data-v1');const reponse=await cache.match('banque.json');if(!reponse)throw err;banque=await reponse.json()}catch{$('erreur').hidden=false;return}}
  if(!Array.isArray(banque.cartes)||!banque.cartes.length){$('erreur').hidden=false;return}
  texte($('resume'),`${banque.cartes.length} cartes vérifiées · banque du ${banque.genere_le}`); dessineCarte(); rendDomaines();
}

$('commencer').addEventListener('click',()=>demarre());
activeAuClavier($('phare'),()=>demarre());
activeAuClavier($('de'),()=>{const ids=domainsOrdonnes().map(([id])=>id).filter(id=>banque?.cartes.some(c=>c.domaine===id));if(ids.length)demarre(ids[crypto.getRandomValues(new Uint32Array(1))[0]%ids.length])});
$('ambiance').addEventListener('click',changeAmbiance); $('quitter').addEventListener('click',quitte); $('reveler').addEventListener('click',revele);
$('notes').addEventListener('click',e=>{const n=e.target.closest('[data-note]')?.dataset.note;if(n)note(n)});
document.addEventListener('keydown',e=>{if($('session').hidden)return;if(e.key==='Escape')quitte();if(e.key===' '&&!$('reveler').hidden){e.preventDefault();revele()}});
if('serviceWorker' in navigator)navigator.serviceWorker.register('sw.js').catch(()=>{});
dessineEtoiles(); appliqueAmbiance({derniere:null}); charge();

// Au chargement : ce qui attend dans la file part si le réseau est là.
window.addEventListener('load', () => Journal.envoyer());

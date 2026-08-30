const CACHE='academie-v1';
const FICHIERS=['./','index.html','style.css','app.js','banque.json'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FICHIERS)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE&&k.startsWith('academie-')).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET')return;
  e.respondWith(fetch(e.request).then(r=>{const copie=r.clone();caches.open(CACHE).then(c=>c.put(e.request,copie));return r}).catch(()=>caches.match(e.request).then(r=>r||caches.match('./'))));
});

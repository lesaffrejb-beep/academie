import {test,expect,type Page} from "@playwright/test";
const mdp="Phrase de test suffisamment longue";
async function inscrit(page:Page,pseudo:string,cursus:string) {
  await page.getByLabel("Ton pseudo",{exact:true}).fill(pseudo);
  await page.getByLabel("Phrase secrète",{exact:true}).fill(mdp);
  await page.getByRole("radio",{name:new RegExp(cursus)}).check();
  await page.getByRole("button",{name:"Créer mon espace",exact:true}).click();
  const cle=await page.locator(".arrivee-cle").textContent();
  await page.getByRole("button",{name:"J’ai enregistré ma clé",exact:true}).click();
  await expect(page.getByLabel("Ta réponse",{exact:true})).toHaveValue("");
  return cle!;
}
async function eleves(page:Page) {
  await page.getByRole("button",{name:"Quitter l’étude",exact:true}).click();
  await page.getByRole("button",{name:"Élèves",exact:true}).click();
}
test("deux comptes : contenu, sauvegarde, reconnexion, masquage et reprise hors ligne",async({page,context,browser})=>{
  const identifiant=crypto.randomUUID(); const pseudoA=`Copro ${identifiant}`,pseudoB=`IFSI ${identifiant}`;
  await page.goto("./");
  await inscrit(page,pseudoA,"Gestion de copropriété");
  await page.getByLabel("Ta réponse",{exact:true}).fill("Réponse privée A à conserver");
  await page.getByRole("button",{name:"Confronter ma réponse",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Le principe",exact:true})).toBeVisible();
  await eleves(page);
  await expect(page.getByText("Sauvegarde synchronisée.",{exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await inscrit(page,pseudoB,"Entrer en IFSI");
  await expect(page.getByRole("heading",{name:"Les cinq B",exact:true})).toBeVisible();
  await expect(page.getByText("Réponse privée A à conserver",{exact:true})).toHaveCount(0);
  await eleves(page);
  await expect(page.getByText(pseudoA,{exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Masquer mon profil",exact:true}).click();
  await expect(page.getByText(`${pseudoB} (toi)`,{exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await page.getByRole("button",{name:"Me connecter",exact:true}).click();
  await page.getByLabel("Ton pseudo",{exact:true}).fill(pseudoA);
  await page.getByLabel("Phrase secrète",{exact:true}).fill(mdp);
  await page.getByRole("button",{name:"Me connecter",exact:true}).last().click();
  await page.getByRole("button",{name:"Apprendre",exact:true}).click();
  await page.getByRole("button",{name:"Reprendre l’étude",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Le principe",exact:true})).toBeVisible();
  await page.getByText("Retrouver ta première réponse",{exact:true}).click();
  await expect(page.getByText("Réponse privée A à conserver",{exact:true})).toBeVisible();
  await page.evaluate(async()=>{await navigator.serviceWorker.ready;});
  await expect.poll(()=>page.evaluate(()=>Boolean(navigator.serviceWorker.controller))).toBe(true);
  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole("heading",{name:"Le principe",exact:true})).toBeVisible();
  await expect(page.getByRole("button",{name:"Créer mon espace",exact:true})).toHaveCount(0);
  await context.setOffline(false);
  const autre = await browser.newContext();
  const nouveau = await autre.newPage();
  await nouveau.goto("http://127.0.0.1:5197/academie/");
  await nouveau.getByRole("button",{name:"Me connecter",exact:true}).click();
  await nouveau.getByLabel("Ton pseudo",{exact:true}).fill(pseudoA);
  await nouveau.getByLabel("Phrase secrète",{exact:true}).fill(mdp);
  await nouveau.getByRole("button",{name:"Me connecter",exact:true}).last().click();
  await nouveau.getByRole("button",{name:"Reprendre l’étude",exact:true}).click();
  await nouveau.getByText("Retrouver ta première réponse",{exact:true}).click();
  await expect(nouveau.getByText("Réponse privée A à conserver",{exact:true})).toBeVisible();
  await autre.close();
});

test("un cookie changé par un autre onglet refuse la synchronisation",async({page})=>{
  const id=crypto.randomUUID();
  await page.goto("./");
  await inscrit(page,"Premier compte " + id,"Gestion de copropriété");
  await eleves(page);
  // APIRequestContext partage le cookie navigateur : simule un autre onglet.
  const r=await page.request.post("http://127.0.0.1:5197/academie/api/v1/compte",{data:{pseudo:"Second compte " + id,phrase_secrete:mdp}});
  expect(r.status()).toBe(201);
  await page.getByRole("button",{name:"Synchroniser maintenant",exact:true}).click();
  await expect(page.getByText(/Le compte a changé dans un autre onglet/)).toBeVisible();
});

test("accueil joignable connecté et ancien travail repris une seule fois",async({page})=>{
  const id=crypto.randomUUID();
  await page.goto("./");
  await page.evaluate(async()=>{
    await new Promise<void>((resolve,reject)=>{
      const r=indexedDB.open("academie-journal",10);
      r.onupgradeneeded=()=>{for(const [n,k] of [["journal","cle"],["file","nonce"],["rejets","nonce"],["marques","cle"]])r.result.createObjectStore(n!,{keyPath:k});};
      r.onerror=()=>reject(r.error);r.onsuccess=()=>{
        const db=r.result,t=db.transaction("journal","readwrite");
        const l={quand:"2026-09-05T10:00:00Z",mode:"revision",nonce:"reprise-locale-unique",carte:"carte-ancienne",note:3,format:"seance"};
        t.objectStore("journal").put({...l,cle:`${l.quand}|${l.mode}|${l.nonce}`});
        t.oncomplete=()=>{db.close();resolve();}; t.onerror=()=>reject(t.error);
      };
    });
  });
  await inscrit(page,"Mon espace de reprise " + id,"Gestion de copropriété");
  await eleves(page);
  await page.getByRole("link",{name:"Mon compte",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Ton compte, ton parcours.",exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Récupérer mon travail sur ce compte",exact:true}).click();
  await expect(page.getByText("Ancien travail récupéré et synchronisé.",{exact:true})).toBeVisible();
  await page.reload();
  await expect(page.getByText("Ancien travail récupéré et synchronisé.",{exact:true})).toBeVisible();
  const etat=await page.evaluate(async()=>{
    const profil=await (await fetch("/academie/api/v1/profil")).json();
    const r=await fetch("/academie/api/v1/journal",{method:"POST",headers:{"Content-Type":"application/json","X-Academie-Profil":profil.id},body:JSON.stringify({lignes:[]})});
    return (await r.json()).manquantes.filter((l:{nonce:string})=>l.nonce==="reprise-locale-unique").length;
  });
  expect(etat).toBe(1);
  await page.evaluate(async()=>{
    await new Promise<void>((resolve,reject)=>{
      const r=indexedDB.open("academie-journal");
      r.onsuccess=()=>{const d=r.result,t=d.transaction("journal","readwrite"),s=t.objectStore("journal"),q=s.getAll();
        q.onsuccess=()=>{const l=q.result[0];s.put({...l,note:1});};
        t.oncomplete=()=>{d.close();resolve();};t.onerror=()=>reject(t.error);
      };r.onerror=()=>reject(r.error);
    });
  });
  await page.reload();
  await expect(page.getByText("Ancien travail récupéré et synchronisé.",{exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:"Récupérer mon travail sur ce compte",exact:true}).click();
  await expect(page.getByRole("alert")).toContainText("Deux versions d’une ancienne réponse diffèrent");
  await page.getByRole("button",{name:"Utiliser un autre compte",exact:true}).click();
  await inscrit(page,"Autre compte " + id,"Gestion de copropriété");
  await eleves(page);await page.getByRole("link",{name:"Mon compte",exact:true}).click();
  await expect(page.getByText("Le travail de cet appareil est déjà rattaché à un autre compte.",{exact:true})).toBeVisible();
  await expect(page.getByRole("button",{name:"Récupérer mon travail sur ce compte",exact:true})).toHaveCount(0);
});


test("brouillon seul récupéré et accès indépendant du scope ancien",async({page,context})=>{
  await page.goto("./");
  await page.evaluate(async()=>{await navigator.serviceWorker.ready;localStorage.setItem("academie-boite-brouillon","Un brouillon commencé avant mon compte");});
  await expect.poll(()=>page.evaluate(()=>navigator.serviceWorker.controller?.scriptURL)).toContain("/academie/sw.js");
  await page.goto("/academie-acces/");
  await expect(page.getByRole("button",{name:"Créer mon espace",exact:true})).toBeVisible();
  await expect.poll(()=>page.evaluate(()=>navigator.serviceWorker.controller?.scriptURL)).toContain("/academie-acces/sw.js");
  const id=crypto.randomUUID();
  await inscrit(page,"Compte brouillon " + id,"Gestion de copropriété");
  await eleves(page);await page.getByRole("link",{name:"Mon compte",exact:true}).click();
  await page.getByRole("button",{name:"Récupérer mon travail sur ce compte",exact:true}).click();
  await expect(page.getByText("Brouillons récupérés sur cet appareil.",{exact:true})).toBeVisible();
  expect(await page.evaluate(()=>{
    const c=JSON.parse(localStorage.getItem("academie-compte-reprise")!);
    return localStorage.getItem(`academie-boite-brouillon:compte:${c.id}`);
  })).toBe("Un brouillon commencé avant mon compte");
  await context.setOffline(true);await page.reload();
  await expect(page.getByRole("heading",{name:"Ton compte, ton parcours.",exact:true})).toBeVisible();
  await expect(page.getByText("Brouillons récupérés sur cet appareil.",{exact:true})).toBeVisible();
  await context.setOffline(false);
});

test("la clé remplace une phrase perdue et devient invalide",async({page})=>{
  const id=crypto.randomUUID(), pseudo="Récupération " + id;
  await page.goto("./");
  const cle=await inscrit(page,pseudo,"Gestion de copropriété");
  const profilInitial=await (await page.request.get("/academie/api/v1/profil")).json();
  await eleves(page);
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await page.getByRole("button",{name:"Retrouver mon accès",exact:true}).click();
  await page.getByLabel("Ton pseudo",{exact:true}).fill(pseudo);
  await page.getByLabel("Clé de récupération",{exact:true}).fill(cle);
  await page.getByLabel("Nouvelle phrase secrète",{exact:true}).fill("Nouvelle phrase de test suffisamment longue");
  await page.getByRole("button",{name:"Changer ma phrase",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Garde ta clé de récupération.",exact:true})).toBeVisible();
  const nouvelle=await page.locator(".arrivee-cle").textContent();
  expect(nouvelle).not.toBe(cle);
  expect(await page.evaluate(()=>JSON.stringify({...localStorage}))).not.toContain(nouvelle);
  await page.getByRole("button",{name:"J’ai enregistré ma clé",exact:true}).click();
  await expect(page.locator(".arrivee-cle")).toHaveCount(0);
  const refusee=await page.request.post("/academie/api/v1/auth/recuperation",{data:{pseudo,cle_recuperation:cle,phrase_secrete:mdp}});
  expect(refusee.status()).toBe(401);
  const ancienMotDePasse=await page.request.post("/academie/api/v1/auth/connexion",{data:{pseudo,phrase_secrete:mdp}});
  expect(ancienMotDePasse.status()).toBe(401);
  await page.getByRole("button",{name:"Élèves",exact:true}).click();
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await page.getByRole("button",{name:pseudo,exact:true}).click();
  await page.getByLabel("Phrase secrète",{exact:true}).fill("Nouvelle phrase de test suffisamment longue");
  await page.getByRole("button",{name:"Me connecter",exact:true}).last().click();
  await expect(page.getByRole("button",{name:"Apprendre",exact:true})).toBeVisible();
  expect((await (await page.request.get("/academie/api/v1/profil")).json()).id).toBe(profilInitial.id);
  const secondeRecuperation=await page.request.post("/academie/api/v1/auth/recuperation",{data:{pseudo,cle_recuperation:nouvelle,phrase_secrete:"Dernière phrase de test suffisamment longue"}});
  expect(secondeRecuperation.status()).toBe(200);
  const compteRecupere=await secondeRecuperation.json();
  expect(compteRecupere.id).toBe(profilInitial.id);
  expect(compteRecupere.cle_recuperation).not.toBe(nouvelle);
});


test("inscription avec cursus puis clic sur le pseudo et mot de passe",async({page})=>{
  const pseudo="Accès direct " + crypto.randomUUID();
  await page.goto("./");
  await page.getByLabel("Ton pseudo",{exact:true}).fill(pseudo);
  await page.getByLabel("Phrase secrète",{exact:true}).fill(mdp);
  await page.getByRole("radio",{name:/Gestion de copropriété/}).check();
  await page.getByRole("button",{name:"Créer mon espace",exact:true}).click();
  const cle=await page.locator(".arrivee-cle").textContent();
  expect(cle).toBeTruthy();
  expect(await page.evaluate(()=>JSON.stringify({...localStorage}))).not.toContain(cle);
  await page.getByRole("button",{name:"J’ai enregistré ma clé",exact:true}).click();
  await expect(page.getByLabel("Ta réponse",{exact:true})).toBeVisible();
  expect((await (await page.request.get("/academie/api/v1/profil")).json()).cursus).toBe("copro");
  expect(await page.evaluate(()=>JSON.stringify({...localStorage}))).not.toContain(cle);
  await page.getByLabel("Ta réponse",{exact:true}).fill("Réponse du compte choisi dans la liste");
  await page.getByRole("button",{name:"Confronter ma réponse",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Le principe",exact:true})).toBeVisible();
  await eleves(page);
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await page.getByRole("button",{name:pseudo,exact:true}).click();
  await expect(page.getByLabel("Ton pseudo",{exact:true})).toHaveValue(pseudo.toLowerCase());
  await expect(page.getByLabel("Phrase secrète",{exact:true})).toBeFocused();
  await page.getByLabel("Phrase secrète",{exact:true}).fill(mdp);
  await page.getByRole("button",{name:"Me connecter",exact:true}).last().click();
  await expect(page.getByRole("button",{name:"Reprendre l’étude",exact:true})).toBeVisible();
});

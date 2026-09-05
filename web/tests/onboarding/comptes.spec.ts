import {test,expect,type Page} from "@playwright/test";
const mdp="Phrase de test suffisamment longue";
async function inscrit(page:Page,mail:string,pseudo:string,cursus:string) {
  await page.getByLabel("Ton pseudo",{exact:true}).fill(pseudo);
  await page.getByLabel("Adresse mail",{exact:true}).fill(mail);
  await page.getByLabel("Mot de passe",{exact:true}).fill(mdp);
  await page.getByRole("button",{name:"Créer mon espace",exact:true}).click();
  await page.getByRole("button",{name:new RegExp(cursus)}).click();
  await expect(page.getByLabel("Ta réponse",{exact:true})).toHaveValue("");
}
async function eleves(page:Page) {
  await page.getByRole("button",{name:"Quitter l’étude",exact:true}).click();
  await page.getByRole("button",{name:"Élèves",exact:true}).click();
}
test("deux comptes : contenu, sauvegarde, reconnexion, masquage et reprise hors ligne",async({page,context,browser})=>{
  const identifiant=crypto.randomUUID(); const mailA=`copro-${identifiant}@example.test`,mailB=`ifsi-${identifiant}@example.test`;
  await page.goto("./");
  await inscrit(page,mailA,`Copro ${identifiant}`,"Gestion de copropriété 3 études");
  await page.getByLabel("Ta réponse",{exact:true}).fill("Réponse privée A à conserver");
  await page.getByRole("button",{name:"Confronter ma réponse",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Le principe",exact:true})).toBeVisible();
  await eleves(page);
  await expect(page.getByText("Sauvegarde synchronisée.",{exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await inscrit(page,mailB,`IFSI ${identifiant}`,"Entrer en IFSI.*2 études");
  await expect(page.getByRole("heading",{name:"Les cinq B",exact:true})).toBeVisible();
  await expect(page.getByText("Réponse privée A à conserver",{exact:true})).toHaveCount(0);
  await eleves(page);
  await expect(page.getByText(`Copro ${identifiant}`,{exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Masquer mon profil",exact:true}).click();
  await expect(page.getByText(`IFSI ${identifiant} (toi)`,{exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:"Me déconnecter",exact:true}).click();
  await page.getByRole("button",{name:"Me connecter",exact:true}).click();
  await page.getByLabel("Adresse mail",{exact:true}).fill(mailA);
  await page.getByLabel("Mot de passe",{exact:true}).fill(mdp);
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
  await nouveau.getByLabel("Adresse mail",{exact:true}).fill(mailA);
  await nouveau.getByLabel("Mot de passe",{exact:true}).fill(mdp);
  await nouveau.getByRole("button",{name:"Me connecter",exact:true}).last().click();
  await nouveau.getByRole("button",{name:"Reprendre l’étude",exact:true}).click();
  await nouveau.getByText("Retrouver ta première réponse",{exact:true}).click();
  await expect(nouveau.getByText("Réponse privée A à conserver",{exact:true})).toBeVisible();
  await autre.close();
});

test("un cookie changé par un autre onglet refuse la synchronisation",async({page})=>{
  const id=crypto.randomUUID();
  await page.goto("./");
  await inscrit(page,`a-${id}@example.test`,"Premier compte","Gestion de copropriété 3 études");
  await eleves(page);
  // APIRequestContext partage le cookie navigateur : simule un autre onglet.
  const r=await page.request.post("http://127.0.0.1:5197/academie/api/v1/compte",{data:{mail:`b-${id}@example.test`,pseudo:"Second compte",mot_de_passe:mdp}});
  expect(r.status()).toBe(201);
  await page.getByRole("button",{name:"Synchroniser maintenant",exact:true}).click();
  await expect(page.getByText(/Le compte a changé dans un autre onglet/)).toBeVisible();
});

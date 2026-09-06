import {test,expect,type Page} from "./compte-fixture";

const chapitre="satellite.travaux.contre-expertise-renovation";
async function repond(page:Page,texte:string) {
  if (await page.locator(".etude-choix").isVisible()) await page.locator(".etude-choix button").first().click();
  else await page.getByRole("textbox",{name:"Ta réponse",exact:true}).fill(texte);
  await page.getByRole("button",{name:"Voir le retour",exact:true}).click();
  await page.getByRole("button",{name:"Bien",exact:true}).click();
}
async function journal(page:Page):Promise<Record<string,unknown>[]> {
  return page.evaluate(()=>new Promise((resolve,reject)=>{
    const r=indexedDB.open("academie-journal-compte:e2e-copro");
    r.onerror=()=>reject(r.error);
    r.onsuccess=()=>{
      const db=r.result,lecture=db.transaction("journal","readonly").objectStore("journal").getAll();
      lecture.onerror=()=>{db.close();reject(lecture.error);};
      lecture.onsuccess=()=>{db.close();resolve(lecture.result);};
    };
  }));
}
test("le parcours rénovation ouvre la contre-expertise et conserve ses productions",async({page},testInfo)=>{
  // API simulée : la preuve porte sur le contenu servi et le journal navigateur.
  await page.route("**/api/v1/journal",route=>route.fulfill({json:{
    acceptees:route.request().postDataJSON().lignes.length,ignorees:0,manquantes:[],jusqu_a:new Date().toISOString(),
  }}));
  await page.goto("./");
  await page.getByRole("button",{name:"Ouvrir le pilote rénovation",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Une rénovation rentable pour qui ?",exact:true})).toBeVisible();
  await page.getByRole("button",{name:"Besoin des bases",exact:true}).click();
  await page.getByRole("button",{name:"Mettre en pratique",exact:true}).click();
  for (let i=0;i<8;i++) {
    await expect(page.getByText(`Question ${i+1} sur 8`,{exact:false})).toBeVisible();
    await repond(page,"Je distingue les hypothèses du modèle et les données du bâtiment.");
  }
  await page.getByRole("textbox",{name:"Ta réponse",exact:true}).fill("Avis provisoire, exclusions explicites et informations manquantes.");
  await page.getByRole("button",{name:"Comparer à la grille",exact:true}).click();
  await page.getByRole("button",{name:"Garder cette étape",exact:true}).click();
  await page.getByRole("button",{name:"Continuer le parcours",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Défendre puis réviser un avis de rénovation",exact:true})).toBeVisible();
  await expect(page).toHaveURL(new RegExp(chapitre));
  const premiere="Je demande le périmètre commun et les pièces qui pourraient changer mon avis.";
  await page.getByRole("textbox",{name:"Ta réponse",exact:true}).fill(premiere);
  await page.reload();
  await expect(page.getByRole("textbox",{name:"Ta réponse",exact:true})).toHaveValue(premiere);
  await page.getByRole("button",{name:"Confronter ma réponse",exact:true}).click();
  await page.getByText("Retrouver ta première réponse",{exact:true}).click();
  await expect(page.getByText(premiere,{exact:true})).toBeVisible();
  await page.getByText("Sources et fabrication",{exact:true}).click();
  await expect(page.getByRole("link",{name:/CAE, Focus 106/})).toHaveAttribute("href",/focus-106-modelisation-reno-240625\.pdf#page=14$/);
  await page.getByRole("button",{name:"Mettre en pratique",exact:true}).click();
  for (let i=0;i<7;i++) {
    await expect(page.getByText(`Question ${i+1} sur 7`,{exact:false})).toBeVisible();
    if (i===2 || i===3) {
      const image=page.getByRole("img",{name:/Deux perspectives/});
      await expect(image).toBeVisible();
      await expect.poll(()=>image.evaluate((img:HTMLImageElement)=>img.naturalWidth)).toBeGreaterThan(0);
    }
    if (i===2) {
      await page.getByRole("textbox",{name:"Ta réponse",exact:true}).fill("Lecture du schéma : aucun versement automatique ne relie les bénéfices.");
      await page.reload();
      await expect(page.getByRole("textbox",{name:"Ta réponse",exact:true})).toHaveValue("Lecture du schéma : aucun versement automatique ne relie les bénéfices.");
    }
    if (i===3) {
      await page.getByRole("button",{name:/^1\. Économie monétaire/}).click();
      await page.getByRole("button",{name:/^\(a\)\s*Composante monétaire/}).click();
      await expect(page.getByRole("textbox",{name:"Ta réponse",exact:true})).toHaveValue("1-a");
      await page.getByRole("textbox",{name:"Ta réponse",exact:true}).fill("1-a\nJe distingue le flux et sa valorisation.");
      await page.reload();
      await expect(page.getByRole("textbox",{name:"Ta réponse",exact:true})).toHaveValue("1-a\nJe distingue le flux et sa valorisation.");
      await expect(page.getByRole("button",{name:/^1\. Économie monétaire/})).toHaveAttribute("data-association","a");
      await page.getByRole("button",{name:/^2\. Confort/}).click();
      await page.getByRole("button",{name:/^\(b\)\s*Bénéfice privé/}).click();
      await expect(page.getByRole("textbox",{name:"Ta réponse",exact:true})).toHaveValue("1-a, 2-b\nJe distingue le flux et sa valorisation.");
      await page.screenshot({path:`../travail/modules-experts-2026-09-06/contre-expertise-relier-${testInfo.project.name}.png`,fullPage:true});
      await repond(page,"1-a, 2-b\nJe distingue le flux et sa valorisation.");
    } else {
      if (i===6) await expect(page.getByRole("button",{name:"Copier",exact:true})).toBeVisible();
      await repond(page,`Production ${i+1} : je conserve les inconnues et les conditions de révision de mon avis.`);
    }
  }
  const synthese="Avis conditionnel : financement à documenter, périmètre comparable et preuve qui pourrait inverser le choix.";
  await page.getByRole("textbox",{name:"Ta réponse",exact:true}).fill(synthese);
  await page.getByRole("button",{name:"Comparer à la grille",exact:true}).click();
  await expect(page.locator(".reponse-conservee")).toHaveText(synthese);
  await page.reload();
  await expect(page.locator(".reponse-conservee")).toHaveText(synthese);
  await page.locator(".grille-etude input").nth(0).check();
  await page.locator(".grille-etude input").nth(2).check();
  await page.reload();
  await expect(page.locator(".grille-etude input").nth(0)).toBeChecked();
  await expect(page.locator(".grille-etude input").nth(1)).not.toBeChecked();
  await expect(page.locator(".grille-etude input").nth(2)).toBeChecked();
  await page.screenshot({path:`../travail/modules-experts-2026-09-06/contre-expertise-grille-${testInfo.project.name}.png`,fullPage:true});
  await page.getByRole("button",{name:"Garder cette étape",exact:true}).click();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  await page.reload();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  const traces=(await journal(page)).filter(l=>l.chapitre===chapitre);
  expect(traces.filter(l=>l.mode==="revision")).toHaveLength(7);
  expect(traces.find(l=>l.etude_etape==="terminee")).toMatchObject({reponse_libre:synthese,attendus_coches:[0,2]});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});

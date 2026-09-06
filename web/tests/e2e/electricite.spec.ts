import {test,expect,sessionTest} from "./compte-fixture";
const chapitre="satellite.equipements.comprendre-protections-electriques";
const titre="Électricité : comprendre ce qui protège";

test("électricité : du schéma à une réponse conservée",async({page},testInfo)=>{
  await page.route("**/api/v1/journal",route=>route.fulfill({json:{acceptees:route.request().postDataJSON().lignes.length,ignorees:0,manquantes:[],jusqu_a:new Date().toISOString()}}));
  await page.goto("./");
  await page.getByRole("button",{name:"Ouvrir Comprendre les protections électriques",exact:true}).click({timeout:7000});
  await expect(page.getByRole("heading",{name:titre,exact:true})).toBeVisible();
  const reponse=()=>page.getByRole("textbox",{name:"Ta réponse",exact:true});
  await reponse().fill("Une surcharge et un défaut d’isolement ne sont pas le même phénomène.");
  await page.reload();
  await expect(reponse()).toHaveValue("Une surcharge et un défaut d’isolement ne sont pas le même phénomène.");
  await page.getByRole("button",{name:"Confronter ma réponse",exact:true}).click();
  await page.getByText("Sources et fabrication",{exact:true}).click();
  await expect(page.locator(".sources-etude a")).toHaveCount(2);
  await expect(page.locator(".sources-etude a").filter({hasText:"INRS"})).toHaveAttribute("href",/TI-ED-6345.pdf#page=/);
  await page.getByRole("button",{name:"Mettre en pratique",exact:true}).click();
  let visuels=0;
  for(let i=0;i<6;i++) {
    await expect(page.getByText(`Question ${i+1} sur 6`,{exact:false})).toBeVisible();
    const support=page.locator(".etude-support img");
    if(await support.count()) {
      await expect(support).toBeVisible();
      await expect.poll(()=>support.evaluate((e:HTMLImageElement)=>e.complete&&e.naturalWidth>0)).toBe(true);
      await expect(support).toHaveAttribute("alt",/.{30}/);
      await page.screenshot({path:`../travail/preuve-concrete-2026-09-06/schema-${i+1}-${testInfo.project.name}.png`,fullPage:true});
      visuels++;
    }
    if(await page.locator(".etude-choix").isVisible()) await page.locator(".etude-choix button").first().click();
    else await reponse().fill(`Réponse ${i+1} : identifier le mécanisme, la protection et ce que le document ne prouve pas.`);
    await page.getByRole("button",{name:"Voir le retour",exact:true}).click();
    await page.getByRole("button",{name:"Bien",exact:true}).click();
  }
  expect(visuels).toBe(2);
  await reponse().fill("Je distingue surintensité et défaut d’isolement ; un interrupteur différentiel ne remplace pas la protection contre les surintensités. Le fonctionnement seul ne prouve pas la sécurité.");
  await page.getByRole("button",{name:"Comparer à la grille",exact:true}).click();
  await page.locator(".grille-etude input").nth(0).check();
  await page.reload();
  await expect(page.locator(".grille-etude input").nth(0)).toBeChecked();
  await expect(page.locator(".reponse-conservee")).toContainText("surintensité");
  await page.getByRole("button",{name:"Garder cette étape",exact:true}).click();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});

test("électricité : le module copro ne fuit pas vers IFSI",async({page})=>{
  await sessionTest(page,"ifsi");
  await page.goto(`./#/salle/etude/${chapitre}`);
  await expect(page.getByRole("heading",{name:"Cette étude est en vérification",exact:true})).toBeVisible();
  await expect(page.getByRole("heading",{name:titre,exact:true})).toHaveCount(0);
});

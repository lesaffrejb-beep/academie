import { expect, test, type Page } from "./compte-fixture";

async function debut(page: Page) {
  await page.goto("./");
  await page.getByRole("button", {name:"Commencer l’étude",exact:true}).click();
  await expect(page.getByLabel("Ta réponse")).toBeVisible();
}
async function premierExercice(page: Page) {
  await debut(page);
  await page.getByLabel("Ta réponse").fill("Réponse initiale personnelle.");
  await page.getByRole("button",{name:"Confronter ma réponse"}).click();
  await page.getByRole("button",{name:"Mettre en pratique"}).click();
  await expect(page.getByText(/Question 1 sur/)).toBeVisible();
}
async function lignes(page: Page): Promise<Record<string, unknown>[]> {
  return page.evaluate(() => new Promise<Record<string, unknown>[]>((resolve,reject) => {
    const req=indexedDB.open("academie-journal-compte:e2e-copro");
    req.onerror=()=>reject(req.error);
    req.onsuccess=()=>{
      const db=req.result;
      const lecture=db.transaction("journal","readonly").objectStore("journal").getAll();
      lecture.onerror=()=>{db.close();reject(lecture.error);};
      lecture.onsuccess=()=>{db.close();resolve(lecture.result);};
    };
  }));
}

test("l'indice survit au rechargement de la tentative",async({page})=>{
  await debut(page);
  await page.getByLabel("Ta réponse").fill("Mon raisonnement avec un indice.");
  await page.getByRole("button",{name:"Un indice",exact:true}).click();
  await page.getByLabel("Cette réponse te semble sûre").check();
  await page.reload();
  await expect(page.getByLabel("Ta réponse")).toHaveValue("Mon raisonnement avec un indice.");
  await expect(page.getByLabel("Cette réponse te semble sûre")).toBeChecked();
  await page.getByRole("button",{name:"Confronter ma réponse"}).click();
  await expect.poll(async()=> (await lignes(page)).find(l=>l.etude_etape==="principe")?.aide_utilisee).toBe(true);
});

test("une réponse avec indice ne reçoit aucune note de rappel autonome",async({page})=>{
  await premierExercice(page);
  await page.getByRole("button",{name:"Un indice",exact:true}).click();
  await page.getByLabel("Ta réponse").fill("Réponse produite avec aide.");
  await page.getByRole("button",{name:"Voir le retour"}).click();
  await expect(page.getByRole("button",{name:"Évident",exact:true})).toHaveCount(0);
  await page.getByRole("button",{name:"Continuer avec cette aide",exact:true}).click();
  await expect.poll(async()=> (await lignes(page)).filter(l=>l.carte).length).toBe(1);
  const ligne=(await lignes(page)).find(l=>l.carte)!;
  expect(ligne.aide_utilisee).toBe(true);
  expect(ligne.mode).toBe("synthese");
  expect(ligne.note).toBeUndefined();
  expect(ligne.reponse_libre).toBe("Réponse produite avec aide.");
});

test("un QCM conserve le choix initial et le retour après rechargement",async({page})=>{
  await premierExercice(page);
  await page.getByLabel("Ta réponse").fill("Une réponse sans indice.");
  await page.getByRole("button",{name:"Voir le retour"}).click();
  await page.getByRole("button",{name:"Bien",exact:true}).click();
  await expect(page.getByText(/Question 2 sur/)).toBeVisible();
  const option=page.locator(".etude-choix button").first();
  const reponse=(await option.textContent())!.slice(1);
  await option.click();
  await page.getByRole("button",{name:"Voir le retour"}).click();
  await page.reload();
  await expect(page.locator(".retour-etude")).toBeVisible();
  await expect(page.locator(".etude-choix button").first()).toBeDisabled();
  await page.getByRole("button",{name:"Bien",exact:true}).click();
  await expect.poll(async()=> (await lignes(page)).filter(l=>l.carte).length).toBe(2);
  expect((await lignes(page)).some(l=>l.reponse_libre===reponse)).toBe(true);
});

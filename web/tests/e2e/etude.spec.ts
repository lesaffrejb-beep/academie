import {sessionTest} from "./compte-fixture";
import { expect, test } from "./compte-fixture";

test("l'accueil conduit à une tentative et conserve la réponse après fermeture", async ({ page }) => {
  await page.goto("./");
  await expect(page.getByRole("heading", {name:"Tenir le fil d’une assemblée"})).toBeVisible();
  await page.getByRole("button", {name:"Commencer l’étude",exact:true}).click();
  await expect(page.getByLabel("Ta réponse")).toBeVisible();
  await expect(page.getByText("Le principe", {exact:true})).toHaveCount(0);
  await page.getByLabel("Ta réponse").fill("La résolution et une éventuelle délégation doivent être vérifiées.");
  await page.getByRole("button", {name:"Confronter ma réponse"}).click();
  await expect(page.getByRole("heading",{name:"Le principe"})).toBeVisible();
  await page.getByRole("button", {name:"Quitter l’étude"}).click();
  await page.getByRole("button", {name:"Reprendre l’étude",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Le principe"})).toBeVisible();
  await page.reload();
  await expect(page.getByRole("heading",{name:"Le principe"})).toBeVisible();
});

test("le métier IFSI ouvre ses propres contenus", async ({page}) => {
  await page.goto("./");
  await sessionTest(page,"ifsi");
  await page.reload();
  await expect(page.getByRole("heading",{name:"Prendre soin commence ici"})).toBeVisible();
  await page.getByRole("button",{name:"Commencer l’étude",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Les cinq B",exact:true})).toBeVisible();
});

test("une étude entière hors ligne garde production et rappels, puis recommence sans ancien corrigé", async ({page,context}) => {
  await page.goto("./");
  await page.getByRole("button",{name:"Commencer l’étude",exact:true}).click();
  await page.getByLabel("Ta réponse").fill("Je cherche le pouvoir dans la résolution.");
  await page.getByRole("button",{name:"Confronter ma réponse"}).click();
  await page.getByRole("button",{name:"Mettre en pratique"}).click();
  await context.setOffline(true);
  for (let i=0;i<4;i++) {
    await expect(page.getByText(`Question ${i+1} sur 4` ,{exact:false})).toBeVisible();
    if (await page.locator('.etude-choix').isVisible()) await page.locator('.etude-choix button').first().click();
    else await page.getByLabel('Ta réponse').fill('Raisonnement personnel de test.');
    await page.getByRole('button',{name:'Voir le retour',exact:true}).click();
    await page.getByRole('button',{name:'Bien',exact:true}).click();
  }
  await page.getByLabel('Ta réponse').fill('Une option hors de la résolution demande une vérification de son autorisation.');
  await page.getByRole('button',{name:'Comparer à la grille',exact:true}).click();
  await expect(page.locator('.reponse-conservee')).toContainText('option hors de la résolution');
  await page.locator('.grille-etude input').first().check();
  await page.getByRole('button',{name:'Garder cette étape',exact:true}).click();
  await expect(page.getByText('Ce qui reste à froid et se transfère : non mesuré.')).toBeVisible();
  await page.getByRole('button',{name:'Recommencer l’étude',exact:true}).click();
  await expect(page.getByLabel('Ta réponse')).toHaveValue('');
  await expect(page.getByRole('heading',{name:'Le principe',exact:true})).toHaveCount(0);
});

test("l'accueil et l'étude restent lisibles avec texte agrandi",async({page})=>{
  await page.goto('./');
  await page.addStyleTag({content:'html {font-size:200%}'});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  await page.getByRole('button',{name:'Commencer l’étude',exact:true}).click();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
});

import { expect, test } from "./compte-fixture";

test("le retour d'un dépôt ne supprime pas l'idée saisie pendant l'envoi", async ({ page }) => {
  let confirme!: () => void;
  const autorisation = new Promise<void>((resolve) => { confirme = resolve; });
  await page.route("**/api/v1/boite", async (route) => {
    if (route.request().method() === "POST") {
      await autorisation;
      await route.fulfill({ status: 201, json: { id: "fixture", etat: "a-traiter" } });
    } else await route.fulfill({ json: { entrees: [] } });
  });
  await page.goto("./#/boite");
  const texte = page.getByRole("textbox", { name: "Déposer" });
  await texte.fill("Première idée");
  await page.getByRole("button", { name: "Déposer", exact: true }).click();
  await expect(page.getByRole("button", { name: "Chargement" })).toBeDisabled();
  await texte.fill("Deuxième idée");
  confirme();
  await expect(page.getByRole("button", { name: "Chargement" })).toHaveCount(0);
  await expect(texte).toHaveValue("Deuxième idée");
});

test("un dépôt confirmé apparaît dans la file de la boîte", async ({ page }) => {
  const entrees: { id: string; contenu: string; etat: string }[] = [];
  await page.route("**/api/v1/boite", async (route) => {
    if (route.request().method() === "POST") {
      const { contenu } = route.request().postDataJSON() as { contenu: string };
      entrees.push({ id: "fixture", contenu, etat: "a-traiter" });
      await route.fulfill({ status: 201, json: { id: "fixture", etat: "a-traiter" } });
    } else await route.fulfill({ json: { entrees } });
  });
  await page.goto("./#/boite");
  await page.getByRole("textbox", { name: "Déposer" }).fill("Une idée de chapitre");
  await page.getByRole("button", { name: "Déposer", exact: true }).click();
  await expect(page.getByRole("textbox", { name: "Déposer" })).toHaveValue("");
  await expect(page.getByRole("listitem").filter({ hasText: "Une idée de chapitre" })).toBeVisible();
});

test("le brouillon survit à un changement d'écran et peut être abandonné",async({page})=>{
  await page.goto('./#/boite');
  await page.locator('textarea').fill('Une idée encore en brouillon');
  await page.getByRole('button',{name:'Apprendre',exact:true}).click();
  await page.getByRole('button',{name:'Boîte',exact:true}).click();
  await expect(page.locator('textarea')).toHaveValue('Une idée encore en brouillon');
  await page.getByRole('button',{name:'Abandonner le brouillon',exact:true}).click();
  await expect(page.locator('textarea')).toHaveValue('');
});

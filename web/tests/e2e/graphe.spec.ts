import { expect, test, sessionTest } from "./compte-fixture";

async function ouvre(page: import("./compte-fixture").Page) {
  await page.goto("./#/arbre");
  await page.getByRole("button", { name: "Graphe des prérequis", exact: true }).click();
  await expect(page.getByRole("region", {name: "Explorer les prérequis"})).toBeVisible();
}

test("les vrais liens se parcourent au clavier et les chapitres vides restent honnêtes", async ({ page }) => {
  await ouvre(page);
  const recherche = page.getByRole("searchbox", {name: "Chercher un chapitre"});
  await recherche.fill("article 25");
  const resultats = page.getByRole("list", {name: "Chapitres du programme"});
  const resultat = resultats.getByRole("button").first();
  await resultat.focus();
  await page.keyboard.press("Enter");
  const carte = page.getByTestId("graphe-relations");
  await expect(carte.getByRole("button", {name: /article 25/})).toHaveAttribute("aria-current", "true");
  const base = carte.locator('[data-groupe="prerequis"] button').first();
  await expect(base).toBeVisible();
  const cible = await base.getAttribute("data-noeud");
  await base.focus();
  await page.keyboard.press("Space");
  await expect(carte.locator(`[data-noeud="${cible}"]`)).toHaveAttribute("aria-current", "true");
  await recherche.fill("Qu'est-ce qu'une copropriété");
  await resultats.getByRole("button").first().click();
  await expect(page.getByTestId("graphe-detail").getByText("Au programme", {exact:true})).toBeVisible();
  await expect(page.getByTestId("graphe-detail").getByRole("button", {name:"Réviser ce chapitre"})).toBeDisabled();
  await expect(page.getByTestId("graphe-detail").getByText(/0 %/)).toHaveCount(0);
});

test("le graphe donne accès à une étude serviable", async ({ page }) => {
  await ouvre(page);
  await page.getByRole("searchbox", {name:"Chercher un chapitre"}).fill("article 24");
  await page.getByRole("list", {name:"Chapitres du programme"}).getByRole("button").first().click();
  await page.getByTestId("graphe-detail").getByRole("button", {name:"Étudier ce chapitre"}).click();
  await expect(page.getByRole("textbox", {name:"Ta réponse"})).toBeVisible();
});

test("un parent du programme ouvre son approfondissement façade et garde le retour", async ({page}, testInfo) => {
  await ouvre(page);
  await page.getByRole("searchbox", {name: "Chercher un chapitre"}).fill("Diagnostiquer une façade avant devis");
  await page.getByRole("list", {name: "Chapitres du programme"}).getByRole("button").click();
  const satellite = "satellite.pathologie.facade-ancienne-avant-devis";
  const parent = "pathologie.facades.diagnostiquer-une-facade-avant-devis";
  const approfondissement = page.getByRole("region", {name: "Approfondissements", exact: true}).getByRole("button", {name: /Façade ancienne/});
  await expect(approfondissement).toBeVisible();
  await expect(page.getByTestId("graphe-relations").locator(`[data-noeud="${satellite}"]`)).toHaveCount(0);
  await approfondissement.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByTestId("graphe-relations").locator(`[data-noeud="${satellite}"]`)).toBeFocused();
  const rattachement = page.getByRole("region", {name: "Rattachement", exact: true}).getByRole("button");
  await expect(rattachement).toHaveAttribute("data-noeud", parent);
  await expect(page.getByTestId("graphe-relations").getByText("Aucun prérequis déclaré.", {exact: true})).toBeVisible();
  await rattachement.click();
  await expect(page.getByTestId("graphe-relations").locator(`[data-noeud="${parent}"]`)).toBeFocused();
  await approfondissement.click();
  await page.screenshot({path: testInfo.outputPath("graphe-facade.png"), fullPage: true});
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  await page.getByTestId("graphe-detail").getByRole("button", {name: "Étudier ce chapitre"}).click();
  await expect(page).toHaveURL(new RegExp(satellite));
  await expect(page.getByRole("textbox", {name: "Ta réponse", exact: true})).toBeVisible();
  await expect(page.getByRole("heading", {name: "Façade ancienne : instruire avant de choisir un devis", exact: true})).toBeVisible();
});

test("les satellites copro restent absents de l’index IFSI", async ({page}) => {
  await sessionTest(page, "ifsi");
  await ouvre(page);
  await page.getByRole("searchbox", {name: "Chercher un chapitre"}).fill("satellite.pathologie.facade-ancienne-avant-devis");
  await expect(page.getByText("Aucun chapitre ne correspond à ces filtres.")).toBeVisible();
  await expect(page.getByRole("list", {name: "Chapitres du programme"}).getByRole("button")).toHaveCount(0);
});

test("filtre du cursus, recherche vide et rendus accessibles", async ({ page }) => {
  await sessionTest(page, "ifsi");
  await ouvre(page);
  await expect(page.getByRole("combobox", {name:"Domaine du graphe"})).not.toContainText("Droit de la copropriété");
  await page.getByRole("searchbox", {name:"Chercher un chapitre"}).fill("aucunchapitreneportececisurement");
  await expect(page.getByText("Aucun chapitre ne correspond à ces filtres.")).toBeVisible();
  await page.getByRole("button", {name:"Effacer les filtres"}).click();
  for (const theme of ["papier", "nuit"]) {
    await page.evaluate(t => {document.documentElement.dataset.theme = t; document.documentElement.style.fontSize = "100%";}, theme);
    await page.screenshot({path:test.info().outputPath(`graphe-${theme}.png`),fullPage:true});
    await page.evaluate(() => document.documentElement.style.fontSize = "200%");
    await expect(page.getByTestId("graphe-relations")).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
  }
});

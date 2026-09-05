import {sessionTest} from "./compte-fixture";
import { expect, test } from "./compte-fixture";

test("le thème se choisit dès l’accueil et persiste après rechargement", async ({ page }) => {
  await page.goto("./");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "papier");
  await page.getByRole("button", { name: "Activer le thème Nuit" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "nuit");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "nuit");
  await page.getByRole("button", { name: "Activer le thème Papier" }).click();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "papier");
});

test("les chapitres et le cas réel sont accessibles au téléphone dans les deux métiers", async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto("./");
  for (const metier of ["Copropriété", "Soins infirmiers"]) {
    await sessionTest(page,metier === "Copropriété" ? "copro":"ifsi");
    await page.reload();
    await expect(page.locator(".apercu-question")).toBeVisible();
    const question = await page.locator(".apercu-question").innerText();
    const chapitres = page.locator(".chapitre-ouvert");
    for (const chapitre of await chapitres.all()) {
      const boite = await chapitre.boundingBox();
      expect(boite?.width).toBeGreaterThanOrEqual(44);
      expect(boite?.height).toBeGreaterThanOrEqual(44);
    }
    await chapitres.first().focus();
    await page.keyboard.press("Enter");
    await expect(page.getByLabel("Ta réponse")).toBeVisible();
    await expect(page.locator(".question-etude")).toHaveText(question);
    await page.getByRole("button", { name: "Quitter l’étude" }).click();
  }
  await page.addStyleTag({ content: "html { font-size: 200% }" });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
});

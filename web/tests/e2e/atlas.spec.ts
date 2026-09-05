import { expect, test } from "@playwright/test";

test("la tablette conserve toutes les cibles dans le cadre de l'atlas", async ({ page }) => {
  for (const largeur of [768, 1024]) {
    await page.setViewportSize({ width: largeur, height: 1024 });
    await page.goto("./#/arbre");
    await expect(page.getByTestId("atlas")).toBeVisible();
    const horsCadre = await page.getByTestId("atlas").evaluate((cadre) => {
      const limite = cadre.getBoundingClientRect();
      return Array.from(cadre.querySelectorAll(".domaine-ligne")).filter((bouton) => {
        const r = bouton.getBoundingClientRect();
        return r.left < limite.left || r.right > limite.right;
      }).map((b) => b.getAttribute("aria-label"));
    });
    expect(horsCadre, `${largeur}px`).toEqual([]);
  }
});

test("l'atlas ouvre les vrais chapitres et distingue le programme du contenu", async ({ page }) => {
  await page.goto("./#/arbre");
  const atlas = page.getByTestId("atlas");
  await expect(atlas).toBeVisible();
  await expect(atlas.getByRole("button", { name: /Droit de la copropriété/ })).toBeVisible();
  await atlas.getByRole("button", { name: /Droit de la copropriété/ }).click();
  if ((page.viewportSize()?.width ?? 1280) >= 768) await page.getByRole("button", { name: "Explorer le domaine" }).click();
  await expect(page.getByRole("heading", { name: "Droit de la copropriété" })).toBeVisible();
  await expect(page.getByTestId("chapitre").first()).toBeVisible();
  await page.getByTestId("chapitre").first().click();
  await expect(page.getByRole("dialog")).toBeVisible();
  await expect(page.getByRole("heading", { name: /Qu'est-ce qu'une copropriété/ })).toBeVisible();
  await expect(page.getByRole("button", { name: "Réviser ce chapitre" })).toBeDisabled();
  await page.keyboard.press("Escape");
  await expect(page.getByRole("dialog")).toHaveCount(0);
  await expect(page.getByTestId("chapitre").first()).toBeFocused();
});

test("le rail et la carte restent lisibles avec deux thèmes et texte agrandi", async ({ page }) => {
  await page.goto("./#/arbre");
  await expect(page.getByTestId("atlas")).toBeVisible();
  for (const theme of ["papier", "nuit"]) {
    await page.getByRole("button", { name: "Profil", exact: true }).click();
    await page.getByRole("radio", { name: theme === "papier" ? "Papier" : "Nuit", exact: true }).check();
    await page.getByRole("button", { name: "Arbre", exact: true }).click();
    await expect(page.getByTestId("atlas")).toBeVisible();
    await page.addStyleTag({ content: "html { font-size: 200% }" });
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    await page.screenshot({ path: test.info().outputPath(`atlas-${theme}.png`), fullPage: true });
    await page.reload();
  }
});

 test("les domaines sont nommés et le programme ne simule pas des relations", async ({ page }) => {
  await page.goto("./#/arbre");
  const atlas = page.getByTestId("atlas");
  await expect(atlas.getByRole("button", { name: /Droit de la copropriété/ })).toBeVisible();
  await expect(atlas.locator("svg.atlas-liens")).toHaveCount(0);
  await expect(atlas.getByText("Au programme", { exact: true }).first()).toBeVisible();
  await expect(atlas.locator(".domaine-nom").first()).toBeVisible();
});

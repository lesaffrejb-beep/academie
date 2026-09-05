import { expect, test } from "./compte-fixture";

test("un refus de session reste visible et peut être réessayé", async ({ page }) => {
  let appels = 0;
  await page.route("**/api/v1/journal", async (route) => {
    appels += 1;
    if (appels === 1) await route.fulfill({ status: 401, json: { erreur: "non-authentifie", motif: "Session absente" } });
    else await route.fulfill({ json: { acceptees: 0, manquantes: [], jusqu_a: "2026-09-04T12:00:00+00:00" } });
  });
  await page.goto("./#/profil");
  await expect(page.getByText("La session n'est plus reconnue. Le journal reste sur cet appareil.")).toBeVisible();
  await page.getByRole("button", { name: "Réessayer la synchronisation" }).click();
  await expect(page.getByText("La session n'est plus reconnue. Le journal reste sur cet appareil.")).toHaveCount(0);
  expect(appels).toBe(2);
});

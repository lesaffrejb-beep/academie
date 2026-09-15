import {test as base, expect, type Page} from "@playwright/test";
export async function sessionTest(page:Page, cursus="copro") {
  await page.route("**/academie/api/v1/profil", route => route.fulfill({json:{
    id:`e2e-${cursus}`, titre_affiche:"Élève de test", cursus, cree_le:"2026-09-05T10:00:00Z", reglages:{}
  }}));
}
export const test=base.extend({page:async ({page},use)=>{await sessionTest(page);await use(page);}});
export {expect};
export type {Page};

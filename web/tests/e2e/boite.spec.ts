import {expect,test} from "./compte-fixture";
test("ancienne adresse de la boîte revient à l’accueil sans onglet Boîte",async({page})=>{
 await page.goto("./#/boite");
 await expect(page.getByRole("heading",{name:"Tenir le fil d’une assemblée",exact:true})).toBeVisible();
 await expect(page.getByRole("button",{name:"Boîte",exact:true})).toHaveCount(0);
});

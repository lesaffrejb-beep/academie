import {test, expect} from './compte-fixture';

const titre = 'Une rénovation rentable pour qui ?';
async function ouvrir(page: import('@playwright/test').Page) {
  await page.goto('./');
  await page.getByRole('button', {name: 'Ouvrir le pilote rénovation'}).click();
  await expect(page.getByRole('heading', {name: titre, exact: true})).toBeVisible();
  await page.getByRole('button', {name: 'Besoin des bases', exact: true}).click();
  await page.getByRole('button', {name: 'Mettre en pratique', exact: true}).click();
}
test('le pilote affiche les supports, mène à une production et reste lisible', async ({page}, testInfo) => {
  await ouvrir(page);
  await expect(page.getByRole('img', {name: /Deux perspectives/})).toBeVisible();
  const visuel = page.getByRole('img', {name: /Deux perspectives/});
  const largeur = (await visuel.boundingBox())!.width;
  await page.getByRole('button', {name: 'Agrandir le support', exact:true}).click();
  expect((await visuel.boundingBox())!.width).toBeGreaterThan(largeur * 1.5);
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth+1)).toBe(true);
  await page.getByRole('button', {name: 'Réduire le support', exact:true}).click();
  await page.screenshot({path:`../travail/pilote-renovation-10p/apercu-${testInfo.project.name}.png`,fullPage:true});
  for (let i=0; i<8; i++) {
    await expect(page.getByText(`Question ${i+1} sur 8`, {exact:false})).toBeVisible();
    if (await page.locator('.etude-choix').isVisible()) await page.locator('.etude-choix button').first().click();
    else await page.getByLabel('Ta réponse').fill('Je distingue hypothèse du modèle et information propre au bâtiment.');
    if (i === 0) {
      await page.reload();
      await expect(page.getByLabel('Ta réponse')).toHaveValue('Je distingue hypothèse du modèle et information propre au bâtiment.');
    }
    await page.getByRole('button', {name: 'Voir le retour', exact: true}).click();
    await page.getByRole('button', {name: 'Bien', exact: true}).click();
  }
  await expect(page.getByRole('button', {name: 'Comparer à la grille'})).toBeVisible();
  await page.getByLabel('Ta réponse').fill('Je demande les hypothèses, les coûts exclus et les données du projet avant de conclure.');
  await page.getByRole('button', {name: 'Comparer à la grille'}).click();
  await page.locator('.grille-etude input').first().check();
  await page.getByRole('button', {name: 'Garder cette étape'}).click();
  await expect(page.getByText('Ce qui reste à froid et se transfère : non mesuré.')).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth+1)).toBe(true);
});
test('support introuvable : pas de réponse créditée', async ({page}) => {
  await page.route('**/banque.json', async route => {
    const response = await route.fetch();
    const banque = await response.json();
    banque.cartes.find((c: {id:string}) => c.id === 'renovation-pilote-perspectives').image.fichier = 'images/support-absent.svg';
    await route.fulfill({json:banque});
  });
  await page.route('**/images/support-absent.svg', r => r.fulfill({status:404, contentType:'text/plain', body:'Absent'}));
  await ouvrir(page);
  await expect(page.getByText('Le support ne peut pas être chargé. Réessaie plus tard ; aucune réponse ne sera créditée.')).toBeVisible();
  await page.getByLabel('Ta réponse').fill('Réponse même sans support');
  await expect(page.getByRole('button', {name: 'Voir le retour', exact: true})).toBeDisabled();
});

for (const image of ['', false, null]) test(`support malformé ${JSON.stringify(image)} : retour bloqué`, async ({page}) => {
  await page.route('**/banque.json', async route => {
    const response = await route.fetch();
    const banque = await response.json();
    banque.cartes.find((c: {id:string}) => c.id === 'renovation-pilote-perspectives').image = image;
    await route.fulfill({json:banque});
  });
  await ouvrir(page);
  await expect(page.getByRole('alert')).toContainText('Le support ne peut pas être chargé');
  await page.getByLabel('Ta réponse').fill('Test');
  await expect(page.getByRole('button', {name: 'Voir le retour', exact:true})).toBeDisabled();
});

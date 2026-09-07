import {expect,test,sessionTest} from './compte-fixture';
test('bibliothèque brute, source et dix séances avec graphe',async({page})=>{
 await page.goto('./');
 await expect(page.locator('.demarrage li')).toHaveCount(10);
 await page.getByRole('link',{name:'Ouvrir la bibliothèque de cours'}).click();
 await expect(page.getByText(/389 chapitres rédigés/)).toBeVisible();
 await page.getByRole('searchbox',{name:'Rechercher un cours'}).fill('syndic et ses missions');
 await page.getByRole('link',{name:'Le syndic et ses missions',exact:true}).click();
 await expect(page.getByText(/Brouillons éditoriaux/)).toBeVisible();
 await expect(page.getByRole('heading',{name:'Sources et portée de consultation'})).toBeVisible();
 await page.getByRole('button',{name:'Arbre',exact:true}).click();
 await page.getByRole('button',{name:'Graphe des prérequis',exact:true}).click();
 await expect(page.getByTestId('graphe-relations')).toBeVisible();
});
test('IFSI reste continu, sans bibliothèque copro et avec huit premières études',async({page})=>{
 await sessionTest(page,'ifsi');await page.goto('./');
 await expect(page.getByRole('heading',{name:'Préparer ton entrée en IFSI',exact:true})).toBeVisible();
 await expect(page.locator('.demarrage li')).toHaveCount(10);
 await expect(page.getByRole('link',{name:'Ouvrir la bibliothèque de cours'})).toHaveCount(0);
 await page.getByRole('button',{name:'Commencer l’étude',exact:true}).click();
 await expect(page.getByRole('heading',{name:'La voie Parcoursup',exact:true})).toBeVisible();
});

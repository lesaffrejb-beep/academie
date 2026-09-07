import {test,expect,sessionTest,type Page} from "./compte-fixture";

const chapitre="satellite.pathologie.facade-ancienne-avant-devis";
const ouverture="Ouvrir Comprendre une façade ancienne";
const titre="Façade ancienne : instruire avant de choisir un devis";
const exercices=["materiau-inconnu","traces-et-causes","parcours-eau","nettoyage-calcin",
  "enduit-contradictoire","comparaison-offres","revision-avis","recommandation-reglement"];

async function journal(page:Page):Promise<Record<string,unknown>[]> {
  return page.evaluate(()=>new Promise((resolve,reject)=>{
    const r=indexedDB.open("academie-journal-compte:e2e-copro");
    r.onerror=()=>reject(r.error);
    r.onsuccess=()=>{
      const db=r.result,lecture=db.transaction("journal","readonly").objectStore("journal").getAll();
      lecture.onerror=()=>{db.close();reject(lecture.error);};
      lecture.onsuccess=()=>{db.close();resolve(lecture.result);};
    };
  }));
}

test("le parcours façade garde la tentative, huit exercices et la synthèse",async({page},testInfo)=>{
  await page.addInitScript(()=>{
    Object.defineProperty(navigator,"clipboard",{configurable:true,value:{
      writeText:async(texte:string)=>{(window as unknown as {copieRole:string}).copieRole=texte;},
    }});
  });
  // API simulée : contenu du vrai build et journal du navigateur, sans preuve VPS.
  await page.route("**/api/v1/journal",route=>route.fulfill({json:{
    acceptees:route.request().postDataJSON().lignes.length,ignorees:0,manquantes:[],jusqu_a:new Date().toISOString(),
  }}));
  await page.goto("./");
  await expect(page.getByRole("button",{name:ouverture,exact:true})).toBeVisible({timeout:10_000});
  await page.getByRole("button",{name:ouverture,exact:true}).click();
  await expect(page.getByRole("heading",{name:titre,exact:true})).toBeVisible();
  await expect(page).toHaveURL(new RegExp(chapitre));

  const premiere="La matière, le parcours de l’eau et les réparations antérieures restent à examiner avant de comparer les devis.";
  const reponse=()=>page.getByRole("textbox",{name:"Ta réponse",exact:true});
  await reponse().fill(premiere);
  await page.reload();
  await expect(reponse()).toHaveValue(premiere);
  await page.getByRole("button",{name:"Confronter ma réponse",exact:true}).click();
  await expect(page.getByRole("heading",{name:"Le principe",exact:true})).toBeVisible();
  await page.getByText("Retrouver ta première réponse",{exact:true}).click();
  await expect(page.getByText(premiere,{exact:true})).toBeVisible();
  await page.getByText("Sources et fabrication",{exact:true}).click();
  const sources=page.locator(".sources-etude a");
  await expect(sources).toHaveCount(1);
  await expect(sources).toContainText("pages PDF 2 et 11-14");
  await expect(sources).toHaveAttribute("href",
    "https://data.geopf.fr/annexes/gpu/documents/PSMV_244900015/e4859efbaa6a6b73f60a338e11f14048/244900015_cahier_recommandations_20241016.pdf#page=11");
  await expect(page.locator(".sources-etude").getByText("Institution",{exact:true})).toBeVisible();
  await expect(page.locator(".sources-etude li p")).toContainText("ne remplacent pas le règlement");
  await page.locator(".sources-etude").screenshot({path:`../travail/facade-2026-09-06/source-${testInfo.project.name}.png`});
  await page.getByRole("button",{name:"Mettre en pratique",exact:true}).click();

  const productions=new Map<string,string>();
  for (let i=0;i<exercices.length;i++) {
    await expect(page.getByText(`Question ${i+1} sur 8`,{exact:false})).toBeVisible();
    const identifiant=`facade-ancienne-${exercices[i]}`;
    if (i===4 || i===7) {
      await expect(page.locator(".module-role")).toBeVisible();
      await expect(page.getByRole("button",{name:"Copier",exact:true})).toBeVisible();
      if (i===4) {
        await page.getByRole("button",{name:"Copier",exact:true}).click();
        await expect(page.getByRole("button",{name:"Copié",exact:true})).toBeVisible();
        const copie=await page.evaluate(()=>(window as unknown as {copieRole:string}).copieRole);
        expect(copie).toBe("Cas fictif : un conseiller demande de retirer tous les enduits parce qu'un guide montre du tuffeau dégradé sous ciment ; comment réponds-tu sans minimiser le risque ni généraliser ?");
        expect(copie).not.toContain("Reconnais le risque décrit");
        await expect(page.locator(".indice-etude")).toHaveCount(0);
      }
      // Le rôle est offert au binôme : une production écrite, aucun échange simulé inventé.
      await expect(page.locator(".module-role textarea")).toHaveCount(1);
      await expect(page.getByRole("button",{name:/Envoyer|Démarrer.*conversation|Parler à.*IA/})).toHaveCount(0);
    }
    if (await page.locator(".etude-choix").isVisible()) {
      const choix=page.locator(".etude-choix button").first();
      productions.set(identifiant,await choix.evaluate(b=>Array.from(b.childNodes)
        .filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent??"").join("").trim()));
      await choix.click();
    } else {
      const texte=`Production ${i+1} : hypothèses concurrentes, preuve manquante et condition qui ferait réviser la priorité.`;
      productions.set(identifiant,texte);
      await reponse().fill(texte);
      if (i===4 || i===6) {
        await page.reload();
        await expect(reponse()).toHaveValue(texte);
        await expect(page.getByText(`Question ${i+1} sur 8`,{exact:false})).toBeVisible();
      }
    }
    if (i===4) await page.screenshot({path:`../travail/facade-2026-09-06/role-${testInfo.project.name}.png`,fullPage:true});
    await page.getByRole("button",{name:"Voir le retour",exact:true}).click();
    await page.getByRole("button",{name:"Bien",exact:true}).click();
  }

  const synthese="Le matériau reste à identifier, les traces ne prouvent pas une cause et les offres doivent partager le même périmètre. La pièce nouvelle modifie l’avis sans transformer une recommandation en obligation.";
  await reponse().fill(synthese);
  await page.getByRole("button",{name:"Comparer à la grille",exact:true}).click();
  await expect(page.locator(".reponse-conservee")).toHaveText(synthese);
  await expect(page.locator(".grille-etude input")).toHaveCount(7);
  await page.reload();
  await expect(page.locator(".reponse-conservee")).toHaveText(synthese);
  for (const i of [1,5]) await page.locator(".grille-etude input").nth(i).check();
  await page.reload();
  for (let i=0;i<7;i++) {
    if ([1,5].includes(i)) await expect(page.locator(".grille-etude input").nth(i)).toBeChecked();
    else await expect(page.locator(".grille-etude input").nth(i)).not.toBeChecked();
  }
  await page.screenshot({path:`../travail/facade-2026-09-06/grille-${testInfo.project.name}.png`,fullPage:true});
  await page.getByRole("button",{name:"Garder cette étape",exact:true}).click();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  await page.reload();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  const traces=(await journal(page)).filter(l=>l.chapitre===chapitre);
  expect(traces.find(l=>l.etude_etape==="principe")).toMatchObject({reponse_libre:premiere});
  const revisions=traces.filter(l=>l.mode==="revision");
  expect(revisions).toHaveLength(8);
  expect(revisions.map(l=>l.carte).sort()).toEqual(exercices.map(id=>`facade-ancienne-${id}`).sort());
  for (const [carte,texte] of productions) expect(revisions.find(l=>l.carte===carte)).toMatchObject({reponse_libre:texte});
  expect(traces.find(l=>l.etude_etape==="terminee")).toMatchObject({reponse_libre:synthese,attendus_coches:[1,5]});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});

test("le cursus IFSI ne sert pas le parcours façade",async({page})=>{
  await page.route("**/api/v1/journal",route=>route.fulfill({json:{
    acceptees:route.request().postDataJSON().lignes.length,ignorees:0,manquantes:[],jusqu_a:new Date().toISOString(),
  }}));
  await sessionTest(page,"ifsi");
  await page.goto("./");
  await expect(page.getByRole("heading",{name:"Préparer ton entrée en IFSI",exact:true})).toBeVisible();
  await expect(page.getByRole("button",{name:ouverture,exact:true})).toHaveCount(0);
  await page.goto(`./#/salle/etude/${chapitre}`);
  await expect(page.getByRole("heading",{name:"Cette étude est en vérification",exact:true})).toBeVisible();
  await expect(page.getByRole("heading",{name:titre,exact:true})).toHaveCount(0);
  await expect(page.getByRole("textbox",{name:"Ta réponse",exact:true})).toHaveCount(0);
});

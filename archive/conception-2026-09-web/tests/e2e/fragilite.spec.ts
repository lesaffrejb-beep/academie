import {test,expect,sessionTest,type Page} from "./compte-fixture";

const chapitre="satellite.droit.diagnostic-partage-fragilite";
const ouverture="Ouvrir Qualifier une copropriété fragile";
const titre="Fragilité : du signal au diagnostic partagé";
const exercices=["dimensions","report-decision","soldes-hypotheses","contre-stereotype",
  "priorite-conditionnelle","angles-manquants","conseil-partage","menage-inconnu"];

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

test("le parcours fragilité garde la tentative, huit exercices et la synthèse",async({page},testInfo)=>{
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
  await page.getByRole("button",{name:ouverture,exact:true}).click();
  await expect(page.getByRole("heading",{name:titre,exact:true})).toBeVisible();
  await expect(page).toHaveURL(new RegExp(chapitre));

  const premiere="Les soldes, le vote reporté, la trace humide et les ressources déclarées demandent des vérifications distinctes.";
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
  await expect(sources).toContainText("pages PDF 8, 10-16 et 22");
  await expect(sources).toHaveAttribute("href",
    "https://www.anah.gouv.fr/sites/default/files/2026-08/082026_guide_gerer-coproprietes-fragiles.pdf#page=10");
  await page.getByRole("button",{name:"Mettre en pratique",exact:true}).click();

  const productions=new Map<string,string>();
  for (let i=0;i<exercices.length;i++) {
    await expect(page.getByText(`Question ${i+1} sur 8`,{exact:false})).toBeVisible();
    const identifiant=`fragilite-${exercices[i]}`;
    if (i>=6) {
      await expect(page.locator(".module-role")).toBeVisible();
      await expect(page.getByRole("button",{name:"Copier",exact:true})).toBeVisible();
      if (i===6) {
        await page.getByRole("button",{name:"Copier",exact:true}).click();
        await expect(page.getByRole("button",{name:"Copié",exact:true})).toBeVisible();
        const copie=await page.evaluate(()=>(window as unknown as {copieRole:string}).copieRole);
        expect(copie).toContain("le procès-verbal mentionne des pièces techniques manquantes");
        expect(copie).toContain("formule une réponse");
        expect(copie).not.toContain("Le partenaire joue un membre du conseil");
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
      if (i===2 || i===6) {
        await page.reload();
        await expect(reponse()).toHaveValue(texte);
        await expect(page.getByText(`Question ${i+1} sur 8`,{exact:false})).toBeVisible();
      }
    }
    if (i===6) await page.screenshot({path:`../travail/fragilite-2026-09-06/role-${testInfo.project.name}.png`,fullPage:true});
    await page.getByRole("button",{name:"Voir le retour",exact:true}).click();
    await page.getByRole("button",{name:"Bien",exact:true}).click();
  }

  const synthese="La visite limitée ne clôt pas les finances, la gouvernance et la situation des ménages. Les pièces nouvelles modifient une priorité conditionnelle sans établir toutes les causes.";
  await reponse().fill(synthese);
  await page.getByRole("button",{name:"Comparer à la grille",exact:true}).click();
  await expect(page.locator(".reponse-conservee")).toHaveText(synthese);
  await expect(page.locator(".grille-etude input")).toHaveCount(8);
  await page.reload();
  await expect(page.locator(".reponse-conservee")).toHaveText(synthese);
  for (const i of [0,3,7]) await page.locator(".grille-etude input").nth(i).check();
  await page.reload();
  for (let i=0;i<8;i++) {
    if ([0,3,7].includes(i)) await expect(page.locator(".grille-etude input").nth(i)).toBeChecked();
    else await expect(page.locator(".grille-etude input").nth(i)).not.toBeChecked();
  }
  await page.screenshot({path:`../travail/fragilite-2026-09-06/grille-${testInfo.project.name}.png`,fullPage:true});
  await page.getByRole("button",{name:"Garder cette étape",exact:true}).click();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  await page.reload();
  await expect(page.getByText("Ce qui reste à froid et se transfère : non mesuré.",{exact:true})).toBeVisible();
  const traces=(await journal(page)).filter(l=>l.chapitre===chapitre);
  expect(traces.find(l=>l.etude_etape==="principe")).toMatchObject({reponse_libre:premiere});
  const revisions=traces.filter(l=>l.mode==="revision");
  expect(revisions).toHaveLength(8);
  expect(revisions.map(l=>l.carte).sort()).toEqual(exercices.map(id=>`fragilite-${id}`).sort());
  for (const [carte,texte] of productions) expect(revisions.find(l=>l.carte===carte)).toMatchObject({reponse_libre:texte});
  expect(traces.find(l=>l.etude_etape==="terminee")).toMatchObject({reponse_libre:synthese,attendus_coches:[0,3,7]});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1)).toBe(true);
});

test("le cursus IFSI ne sert pas le parcours fragilité",async({page})=>{
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

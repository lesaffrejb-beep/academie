import { expect, test, type Page } from "./compte-fixture";

test.use({ serviceWorkers: "block" });

const QUESTION = ".font-titre.text-xl";
const CARTE = {
  id: "fixture-a", domaine: "domaine", branche: "branche", type: "flash", niveau: 1,
  question: "Question de test A", reponse: "Correction de test A", statut: "valide",
  verifie: "2026-09-04", source: [{ texte: "Source de test", nature: "texte-officiel",
    url: "https://www.legifrance.gouv.fr/" }],
};

async function ouvre(page: Page, cartes: Record<string, unknown>[] = [CARTE],
  chemin = "./#/salle/seance/hasard", heure = new Date(2026, 8, 4, 12), pause = false) {
  await page.clock.install({ time: pause ? new Date(heure.getTime() - 1000) : heure });
  if (pause) await page.clock.pauseAt(heure);
  await page.route("**/banque.json", (route) => route.fulfill({ json: {
    cartes, domaines: { domaine: { titre: "Domaine de test", ordre: 1 } },
    quotas: { revisions_par_seance: 10, nouveau_par_seance: 10, plafond_reprise: 20 },
    progression: { seuil_stabilite_acquise_jours: 21, seuil_ouverture_region: 0.75,
      examen_obligatoire_pour_100: true, examen_nb_cartes: 12, examen_score_reussite: 0.8 },
  } }));
  await page.route("**/api/v1/journal", (route) => route.fulfill({ json: {
    acceptees: route.request().postDataJSON().lignes.length, ignorees: 0,
    manquantes: [], jusqu_a: "2026-09-04T12:00:00+00:00",
  } }));
  await page.goto(chemin);
  await expect(page.locator(QUESTION)).toBeVisible();
}

async function journal(page: Page): Promise<Record<string, unknown>[]> {
  return page.evaluate(() => new Promise((resolve, reject) => {
    const requete = indexedDB.open("academie-journal-compte:e2e-copro");
    requete.onerror = () => reject(requete.error);
    requete.onsuccess = () => {
      const base = requete.result;
      const lecture = base.transaction("journal", "readonly").objectStore("journal").getAll();
      lecture.onerror = () => { base.close(); reject(lecture.error); };
      lecture.onsuccess = () => { base.close(); resolve(lecture.result); };
    };
  }));
}

test("une seule ouverture et une seule note pour un double clic", async ({ page }) => {
  await ouvre(page, [CARTE, { ...CARTE, id: "fixture-b", question: "Question de test B" }]);
  await expect.poll(async () => (await journal(page)).filter((l) => l.mode === "seance").length).toBe(1);
  const avant = await page.locator(QUESTION).textContent();
  await page.getByRole("button", { name: "Voir la réponse" }).click();
  await page.getByRole("button", { name: "Bien", exact: true }).evaluate((b: HTMLButtonElement) => {
    b.click(); b.click();
  });
  await expect(page.locator(QUESTION)).not.toHaveText(avant ?? "");
  expect((await journal(page)).filter((l) => l.mode === "revision")).toHaveLength(1);
});

for (const type of ["photo", "relier", "datation", "plan"]) {
  test(`${type} montre sa vraie image et permet une reponse`, async ({ page }) => {
    await ouvre(page, [{ ...CARTE, type, image: {
      fichier: "images/vmc-caisson-coupe.svg", alt: "Coupe du caisson de ventilation",
      licence: "creation interne", credit: "Academie", source: "schema original",
    } }]);
    const image = page.getByRole("img", { name: "Coupe du caisson de ventilation" });
    await expect(image).toBeVisible();
    await expect.poll(() => image.evaluate((i: HTMLImageElement) => i.naturalWidth)).toBeGreaterThan(0);
    await page.getByRole("textbox", { name: "Ta réponse" }).fill("Une reponse de test");
    await page.getByRole("button", { name: "Voir la réponse" }).click();
    await expect(page.getByText("Correction de test A", { exact: true })).toBeVisible();
  });
}

test("les vraies sources sont repliees puis consultables apres reponse", async ({ page }) => {
  await ouvre(page);
  await expect(page.getByRole("link", { name: "Source de test" })).not.toBeVisible();
  await page.getByRole("button", { name: "Voir la réponse" }).click();
  await expect(page.locator("details")).not.toHaveAttribute("open");
  await page.locator("details summary").click();
  await expect(page.getByRole("link", { name: "Source de test" })).toHaveAttribute("href", "https://www.legifrance.gouv.fr/");
});

test("signaler retire immediatement la carte sans lui donner une note", async ({ page }) => {
  await ouvre(page, [CARTE, { ...CARTE, id: "fixture-b", question: "Question de test B" }]);
  const avant = await page.locator(QUESTION).textContent();
  await page.getByRole("button", { name: "Voir la réponse" }).click();
  await page.locator("details summary").click();
  await page.getByRole("button", { name: "Cette carte est fausse", exact: true }).click();
  await expect(page.locator(QUESTION)).not.toHaveText(avant ?? "");
  const lignes = await journal(page);
  expect(lignes.filter((l) => l.mode === "signalement")).toHaveLength(1);
  expect(lignes.filter((l) => l.mode === "revision")).toHaveLength(0);
});

test("une panne de stockage garde la correction et propose de reessayer", async ({ page }) => {
  await ouvre(page);
  await expect.poll(async () => (await journal(page)).filter((l) => l.mode === "seance").length).toBe(1);
  await page.getByRole("button", { name: "Voir la réponse" }).click();
  await page.evaluate(() => {
    // Dexie garde transaction.bind(db) a l ouverture ; l ecriture reste dynamique.
    const original = IDBObjectStore.prototype.put;
    IDBObjectStore.prototype.put = function (...args: Parameters<typeof original>) {
      if (this.name === "journal") throw new DOMException("stockage indisponible", "QuotaExceededError");
      return original.apply(this, args);
    };
  });
  await page.getByRole("button", { name: "Bien", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText("enregistrement");
  await expect(page.getByText("Correction de test A", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Bien", exact: true })).toBeEnabled();
  expect((await journal(page)).filter((l) => l.mode === "revision")).toHaveLength(0);
});

test("une seance de chapitre ne sert aucune carte d un autre chapitre", async ({ page }) => {
  await ouvre(page, [
    { ...CARTE, chapitre: "domaine.branche.cible" },
    { ...CARTE, id: "fixture-b", chapitre: "domaine.branche.autre", question: "Question hors chapitre" },
  ], "./#/salle/seance/chapitre:domaine.branche.cible");
  await expect(page.locator(QUESTION)).toHaveText("Question de test A");
  await page.getByRole("button", { name: "Voir la réponse" }).click();
  await page.getByRole("button", { name: "Bien", exact: true }).click();
  await expect(page.getByRole("heading", { name: "La séance est terminée." })).toBeVisible();
  expect((await journal(page)).filter((l) => l.mode === "revision").map((l) => l.carte)).toEqual(["fixture-a"]);
});

test("la carte expire a minuit dans une salle deja ouverte", async ({ page }) => {
  await ouvre(page, [{ ...CARTE, peremption: "2026-09-04" }],
    "./#/salle/seance/hasard", new Date(2026, 8, 4, 23, 59, 59), true);
  await page.clock.runFor(2000);
  await expect(page.locator(QUESTION)).not.toBeVisible();
  expect((await journal(page)).filter((l) => l.mode === "revision")).toHaveLength(0);
});

test("une mauvaise reponse QCM explique le choix et conserve la confiance", async ({ page }) => {
  await ouvre(page, [{ ...CARTE, type: "qcm", choix: [
    { texte: "Mauvais choix", correct: false, pourquoi_faux: "Explication du mauvais choix" },
    { texte: "Bonne reponse", correct: true },
    { texte: "Autre choix", correct: false, pourquoi_faux: "Autre explication" },
  ] }]);
  await page.getByRole("checkbox", { name: "J'étais sûr" }).check();
  await page.getByRole("button", { name: "Mauvais choix" }).click();
  await expect(page.locator(".salle-faux")).toBeVisible();
  await expect(page.getByText("Explication du mauvais choix", { exact: true })).toBeVisible();
  await page.getByRole("button", { name: "À revoir", exact: true }).click();
  await expect(page.getByRole("heading", { name: "La séance est terminée." })).toBeVisible();
  expect((await journal(page)).find((l) => l.mode === "revision")?.confiance).toBe(true);
});

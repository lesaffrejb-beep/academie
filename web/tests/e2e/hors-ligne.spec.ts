/**
 * Les preuves hors-ligne d'ACA-FRONT-2.
 *
 * Le cahier dit « fini quand » : première question en moins de trois
 * secondes réseau coupé sur téléphone, séance jouée réseau coupé,
 * envoyée au retour, aucun hôte tiers. `tests/hotes.test.ts` couvre le
 * troisième point en lisant le code ; ces trois-là se mesurent dans un
 * vrai navigateur, sur le vrai build, parce qu'aucune lecture de code ne
 * prouve qu'un service worker sert une banque quand le réseau est mort.
 *
 * Ce qui est mesuré, et pourquoi ainsi :
 *
 *   1. **Trois secondes hors-ligne.** On charge une fois en ligne pour
 *      que le service worker et Dexie prennent la banque, on coupe, on
 *      recharge, et on chronomètre de la navigation à la première
 *      question lisible. Le budget est celui du cahier, pas un confort.
 *   2. **La séance se joue et s'écrit.** Réseau coupé, on répond à trois
 *      cartes et on relit IndexedDB : les lignes `revision` sont là,
 *      avec leur ligne d'ouverture `seance`, et elles sont en file.
 *   3. **La file part au retour.** On rebranche, on intercepte
 *      `POST /journal` et on vérifie qu'il porte exactement les lignes
 *      mises de côté. Le serveur d'état n'a pas à tourner ici : ce qu'on
 *      teste, c'est que le client envoie ce qu'il a promis de garder.
 *
 * Ces tests jouent la séance **au hasard** (`#/salle/seance/hasard`),
 * pas la séance du jour. Raison : la séance du jour dépend de la couleur
 * du jour, et un dimanche elle ne sert rien du tout (`decisions/0016`).
 * Un test de bout en bout qui ne passe que du lundi au samedi n'est pas
 * un test. Les règles de composition, elles, sont couvertes ailleurs et
 * exactement, par `parite-semaine.test.ts` contre `app/seance.py`. Ici
 * on prouve le hors-ligne, le journal et les hôtes : le chemin de charge
 * est le même.
 *
 * Rien de tout cela n'est dans `npm test` ni dans la porte du dépôt : la
 * suite Python n'installe pas de navigateur. La CI web les lance séparément.
 */

import { expect, test, type Page } from "@playwright/test";

const BUDGET_MS = 3000;

/** Le titre de la première carte servie, quel que soit son type. */
const QUESTION = ".font-titre.text-xl";

/** La séance au hasard : dix cartes, quel que soit le jour. */
const SEANCE = "./#/salle/seance/hasard";

/** Lit le journal local sans passer par l'application (IndexedDB brut). */
async function journalLocal(page: Page): Promise<Record<string, unknown>[]> {
  return page.evaluate<Record<string, unknown>[]>(() => {
    return new Promise((resolve, reject) => {
      const ouverture = indexedDB.open("academie-journal");
      ouverture.onerror = () => reject(new Error("indexedDB indisponible"));
      ouverture.onsuccess = () => {
        const base = ouverture.result;
        if (!base.objectStoreNames.contains("journal")) {
          base.close();
          resolve([]);
          return;
        }
        const demande = base.transaction("journal", "readonly")
          .objectStore("journal")
          .getAll();
        demande.onerror = () => reject(new Error("lecture du journal impossible"));
        demande.onsuccess = () => {
          base.close();
          resolve(demande.result as Record<string, unknown>[]);
        };
      };
    });
  });
}

/** Combien de lignes attendent encore d'être envoyées. */
async function tailleDeLaFile(page: Page): Promise<number> {
  return page.evaluate<number>(() => {
    return new Promise((resolve, reject) => {
      const ouverture = indexedDB.open("academie-journal");
      ouverture.onerror = () => reject(new Error("indexedDB indisponible"));
      ouverture.onsuccess = () => {
        const base = ouverture.result;
        if (!base.objectStoreNames.contains("file")) {
          base.close();
          resolve(0);
          return;
        }
        const demande = base.transaction("file", "readonly").objectStore("file").count();
        demande.onerror = () => reject(new Error("lecture de la file impossible"));
        demande.onsuccess = () => {
          base.close();
          resolve(demande.result);
        };
      };
    });
  });
}

/** Charge une fois en ligne et attend que tout soit en cache. */
async function amorce(page: Page): Promise<void> {
  await page.goto("./");
  await expect(page.getByRole("button", { name: "Apprendre", exact: true })).toBeVisible();
  // Le service worker doit avoir pris la main : sans lui, « hors-ligne »
  // ne mesurerait que le cache HTTP du navigateur.
  await page.waitForFunction(
    () => navigator.serviceWorker?.controller !== null
      && navigator.serviceWorker?.controller !== undefined,
    undefined,
    { timeout: 20_000 },
  );
}

/**
 * Répond « Bien » à une carte, quel que soit son type.
 *
 * `isVisible()` ne patiente pas : sur le rendu de la carte suivante il
 * répond « non » avant que React n'ait posé le bouton, et on part sur la
 * mauvaise branche. On attend donc que l'UNE des deux formes soit là,
 * puis on choisit.
 */
async function repond(page: Page): Promise<void> {
  const reveler = page.getByRole("button", { name: "Voir la réponse" });
  const choix = page.locator("ul li button").first();
  await expect(reveler.or(choix).first()).toBeVisible();
  if (await reveler.isVisible()) {
    await reveler.click();
  } else {
    // QCM : cliquer un choix révèle la réponse.
    await choix.click();
  }
  const bien = page.getByRole("button", { name: "Bien", exact: true });
  await expect(bien).toBeVisible();
  const avant = await page.locator(QUESTION).first().textContent();
  await bien.click();
  // La note écrit dans IndexedDB avant de présenter la carte suivante.
  // Ne pas réinterroger le QCM désactivé de la carte qui se termine.
  await expect(page.locator(QUESTION).first()).not.toHaveText(avant ?? "");
}

/** Répond à `combien` cartes, en attendant chaque fois la suivante. */
async function joue(page: Page, combien: number): Promise<void> {
  for (let i = 0; i < combien; i += 1) {
    await expect(page.locator(QUESTION).first()).toBeVisible();
    await repond(page);
  }
}

test.describe("hors-ligne", () => {
  test("la première question s'affiche en moins de trois secondes, réseau coupé", async ({
    page, context,
  }) => {
    await amorce(page);
    await context.setOffline(true);

    const depart = Date.now();
    await page.goto(SEANCE);
    await expect(page.locator(QUESTION).first()).toBeVisible();
    const ecoule = Date.now() - depart;

    expect(
      ecoule,
      `première question en ${ecoule} ms hors-ligne, budget ${BUDGET_MS} ms (cahier ACA-FRONT-2)`,
    ).toBeLessThan(BUDGET_MS);
  });

  test("une séance jouée réseau coupé s'écrit localement et attend", async ({
    page, context,
  }) => {
    await amorce(page);
    await context.setOffline(true);
    await page.goto(SEANCE);
    await joue(page, 3);

    const journal = await journalLocal(page);
    const revisions = journal.filter((l) => l["mode"] === "revision");
    const ouvertures = journal.filter((l) => l["mode"] === "seance");

    expect(revisions.length, "trois réponses jouées, trois lignes au journal")
      .toBeGreaterThanOrEqual(3);
    expect(ouvertures.length, "la séance s'ouvre par une ligne mode: seance")
      .toBeGreaterThanOrEqual(1);

    const ouverture = ouvertures[0] as Record<string, unknown>;
    for (const cle of ["graine", "banque_version", "moteur_version", "format"]) {
      expect(ouverture[cle], `la ligne d'ouverture porte ${cle} (journal-v1)`)
        .toBeDefined();
    }
    for (const ligne of revisions) {
      expect(ligne["nonce"], "chaque ligne porte son nonce").toBeTruthy();
      expect(ligne["quand"], "chaque ligne porte sa date").toBeTruthy();
    }

    expect(await tailleDeLaFile(page), "rien n'a pu partir, tout attend en file")
      .toBeGreaterThanOrEqual(revisions.length + ouvertures.length);
  });

  test("au retour du réseau, la file part vers le serveur", async ({ page, context }) => {
    await amorce(page);
    await context.setOffline(true);
    await page.goto(SEANCE);
    await joue(page, 2);

    const enAttente = await tailleDeLaFile(page);
    expect(enAttente, "des lignes attendent avant le retour du réseau").toBeGreaterThan(0);

    // Le serveur d'état ne tourne pas ici : on tient sa place et on note
    // ce qu'on reçoit. Ce qui est prouvé, c'est que le client envoie ce
    // qu'il a promis de garder.
    const recues: Record<string, unknown>[] = [];
    await context.route("**/academie/api/v1/journal", async (route) => {
      const corps = route.request().postDataJSON() as { lignes?: Record<string, unknown>[] };
      for (const l of corps.lignes ?? []) recues.push(l);
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          acceptees: corps.lignes?.length ?? 0,
          ignorees: 0,
          manquantes: [],
          jusqu_a: new Date().toISOString(),
        }),
      });
    });

    await context.setOffline(false);
    await page.evaluate(() => window.dispatchEvent(new Event("online")));

    await expect
      .poll(() => recues.length, {
        message: "le client n'a rien envoyé au retour du réseau",
        timeout: 15_000,
      })
      .toBeGreaterThanOrEqual(enAttente);

    await expect
      .poll(() => tailleDeLaFile(page), {
        message: "la file ne s'est pas vidée après acceptation",
        timeout: 15_000,
      })
      .toBe(0);

    // Ce qui est parti est bien ce qui avait été joué, pas autre chose.
    const modes = new Set(recues.map((l) => l["mode"]));
    expect(modes.has("revision"), "les réponses jouées sont parties").toBe(true);
    expect(modes.has("seance"), "l'ouverture de séance est partie aussi").toBe(true);
    for (const l of recues) {
      expect(l["nonce"], "chaque ligne envoyée porte son nonce").toBeTruthy();
    }
  });

  test("aucun hôte tiers n'est contacté pendant une séance", async ({ page }) => {
    const etrangers: string[] = [];
    page.on("request", (r) => {
      const hote = new URL(r.url()).host;
      if (hote && !hote.startsWith("127.0.0.1") && !hote.startsWith("localhost")) {
        etrangers.push(r.url());
      }
    });

    await amorce(page);
    await page.goto(SEANCE);
    await joue(page, 1);

    expect(etrangers, `hôtes tiers contactés : ${etrangers.join(", ")}`).toEqual([]);
  });
});

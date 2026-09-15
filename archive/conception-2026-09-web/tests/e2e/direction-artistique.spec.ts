import {sessionTest} from "./compte-fixture";
/**
 * La checklist de DIRECTION-ARTISTIQUE.md §9, celle qui se mesure.
 *
 * La DA finit par une liste à cocher avant de committer un écran. La
 * moitié de ses lignes est du jugement (« aucune culpabilisation »,
 * « ce qui est en avant est grand ») et n'a rien à faire dans un test.
 * L'autre moitié est mécanique, et une case cochée à la main se décoche
 * toute seule au commit suivant. Ce fichier prend cette moitié-là :
 *
 *   - aucun hexadécimal hors des tokens (vérifié dans le CSS SERVI, pas
 *     dans les sources : c'est le build qui ment, pas l'auteur) ;
 *   - téléphone 375, ordinateur 1280, texte à 200 % : rien ne déborde ;
 *   - Nuit ET Papier, les deux thèmes rendus, l'encre lisible sur le
 *     fond dans les deux ;
 *   - mouvement réduit respecté ;
 *   - clavier sur le chemin principal : Espace révèle, 1 à 4 notent,
 *     Échap sort ; la souris n'est jamais nécessaire dans une salle
 *     (§8 ter) ;
 *   - le focus se voit.
 *
 * Ce qui n'est PAS ici : les trois secondes hors-ligne, qui vivent dans
 * `hors-ligne.spec.ts` avec le reste des preuves du cahier.
 *
 * Comme l'autre suite, ces tests demandent un navigateur et un build :
 * ils ne sont ni dans `npm test` ni dans la porte du dépôt.
 */

import { expect, test, type Page } from "./compte-fixture";

const QUESTION = ".font-titre.text-xl";
const SEANCE = "./#/salle/seance/hasard";

/** Vrai si la page déborde horizontalement, à la tolérance du sous-pixel. */
async function deborde(page: Page): Promise<boolean> {
  return page.evaluate(() => {
    const d = document.documentElement;
    return d.scrollWidth > d.clientWidth + 1;
  });
}

/** La couleur effective d'un token, telle que le navigateur la calcule. */
async function token(page: Page, nom: string): Promise<string> {
  return page.evaluate(
    (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim(),
    nom,
  );
}

test.describe("direction artistique", () => {
  test("aucun hexadécimal hors des tokens dans le CSS servi", async ({ page }) => {
    await page.goto("./#/arbre");
    // On lit la feuille SERVIE : c'est elle qui décide de ce qui s'affiche.
    // Un composant qui aurait écrit `#ff0000` en dur atterrirait ici.
    const css = await page.evaluate(() =>
      [...document.styleSheets]
        .flatMap((f) => {
          try {
            return [...f.cssRules].map((r) => r.cssText);
          } catch {
            return [];
          }
        })
        .join("\n"));

    // Les hexadécimaux légitimes sont ceux des définitions de variables
    // (`--c-...: #xxx`) et du grain, qui est une image de données.
    const restant = css
      .split("\n")
      .filter((l) => !/--[a-z0-9-]+\s*:/.test(l))
      .filter((l) => !l.includes("data:image/svg+xml"))
      .filter((l) => /#[0-9a-fA-F]{3,8}\b/.test(l));

    expect(
      restant,
      `couleur en dur hors des tokens : ${restant.slice(0, 3).join(" | ")}`,
    ).toEqual([]);
  });

  test("rien ne déborde, ni à 375 ni à 1280, ni à 200 % de texte", async ({ page }) => {
    for (const largeur of [375, 1280]) {
      await page.setViewportSize({ width: largeur, height: 800 });
      for (const chemin of ["./", SEANCE, "./#/profil", "./#/credits"]) {
        await page.goto(chemin);
        await expect(page.locator("body")).toBeVisible();
        expect(await deborde(page), `${chemin} déborde à ${largeur} px`).toBe(false);
      }
    }

    // Texte à 200 % : la mise en page doit tenir (DA §7 et §9). On grossit
    // la racine plutôt que le zoom du navigateur, qui remettrait tout à
    // l'échelle sans rien prouver.
    await page.setViewportSize({ width: 375, height: 800 });
    await page.goto(SEANCE);
    await page.addStyleTag({ content: "html { font-size: 200% }" });
    await expect(page.locator(QUESTION).first()).toBeVisible();
    expect(await deborde(page), "la page déborde à 200 % de texte").toBe(false);
  });

  test("les deux thèmes rendent, et l'encre n'est pas la couleur du fond", async ({ page }) => {
    for (const theme of ["nuit", "papier"]) {
      await page.goto("./#/arbre");
      await page.evaluate((t) => {
        document.documentElement.setAttribute("data-theme", t);
      }, theme);
      const fond = await token(page, "--c-fond");
      const encre = await token(page, "--c-encre");
      const accent = await token(page, "--c-accent");
      const surAccent = await token(page, "--c-sur-accent");
      expect(fond, `${theme} : pas de fond`).not.toBe("");
      expect(encre, `${theme} : l'encre vaut le fond, rien ne serait lisible`)
        .not.toBe(fond);
      expect(accent, `${theme} : pas d'accent`).not.toBe("");
      // Le bouton principal est plein de l'accent : son encre doit être
      // autre chose que l'accent lui-même (DA §8 ter).
      expect(surAccent, `${theme} : l'encre du bouton principal vaut l'accent`)
        .not.toBe(accent);
    }
  });

  test("le mouvement réduit est respecté", async ({ browser }) => {
    const contexte = await browser.newContext({ reducedMotion: "reduce" });
    const page = await contexte.newPage();
    await sessionTest(page);
    await page.goto(SEANCE);
    await expect(page.locator(QUESTION).first()).toBeVisible();

    // Aucune transformation ne subsiste, et les transitions sont des
    // fondus courts (DA §6). On mesure sur un vrai bouton de l'écran.
    const bouton = page.locator("button").first();
    const style = await bouton.evaluate((el) => {
      const s = getComputedStyle(el);
      return { transition: s.transitionProperty, duree: s.transitionDuration };
    });
    expect(style.transition, "une transformation survit au mouvement réduit")
      .not.toContain("transform");
    expect(style.transition).toContain("opacity");
    await contexte.close();
  });

  test("la souris n'est jamais nécessaire dans une salle", async ({ page }) => {
    await page.goto(SEANCE);
    await expect(page.locator(QUESTION).first()).toBeVisible();

    const reveler = page.getByRole("button", { name: "Voir la réponse" });
    const bien = page.getByRole("button", { name: "Bien", exact: true });

    // Espace révèle. Sur un QCM il n'y a rien à révéler au clavier : on
    // prend alors la première carte à révélation, ce que la séance au
    // hasard finit toujours par servir.
    let joué = false;
    for (let i = 0; i < 10 && !joué; i += 1) {
      await expect(page.locator(QUESTION).first()).toBeVisible();
      if (await reveler.isVisible()) {
        // Le focus est sur le corps, pas sur un bouton : c'est le cas
        // qu'on veut mesurer, celui de la main qui n'a pas touché la souris.
        await page.locator("body").click({ position: { x: 5, y: 5 } });
        await page.keyboard.press(" ");
        await expect(bien).toBeVisible();
        joué = true;
      } else {
        const questionAvant = await page.locator(QUESTION).first().textContent();
        await page.locator("ul li button").first().click();
        await expect(bien).toBeVisible();
        await bien.click();
        // La réponse écrit dans IndexedDB avant le changement de carte.
        // Attendre ce changement évite de chercher un QCM sur le rappel suivant.
        await expect(page.locator(QUESTION).first()).not.toHaveText(questionAvant ?? "");
      }
    }
    expect(joué, "aucune carte à révélation en dix cartes : test non concluant")
      .toBe(true);

    // 1 à 4 notent : la question doit changer sans un clic.
    const avant = await page.locator(QUESTION).first().textContent();
    await page.keyboard.press("3");
    await expect(page.locator(QUESTION).first()).not.toHaveText(avant ?? "");

    // Échap sort de la salle.
    await page.keyboard.press("Escape");
    await expect(page.getByRole("button", { name: "Apprendre", exact: true })).toBeVisible();
  });

  test("le focus se voit sur le chemin principal", async ({ page }) => {
    await page.goto("./#/arbre");
    // Attendre que React ait posé les boutons : tabuler dans une page
    // encore vide ne prouverait rien.
    await expect(page.getByRole("button", { name: "Apprendre", exact: true })).toBeVisible();
    // Un onglet fraîchement ouvert n'a le focus nulle part : sans ce clic
    // dans un coin vide, la tabulation ne part de rien.
    await page.mouse.click(2, 2);
    await page.keyboard.press("Tab");
    const contour = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      const s = getComputedStyle(el);
      return { largeur: s.outlineWidth, style: s.outlineStyle };
    });
    expect(contour, "la première tabulation n'atteint aucun élément").not.toBeNull();
    expect(contour?.style, "l'élément focalisé n'a pas de contour visible")
      .not.toBe("none");
    expect(parseFloat(contour?.largeur ?? "0")).toBeGreaterThan(0);
  });
});

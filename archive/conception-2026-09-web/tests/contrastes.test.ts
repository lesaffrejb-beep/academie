import { readFileSync } from "node:fs";
import { expect, test } from "vitest";

const css = readFileSync(new URL("../src/index.css", import.meta.url), "utf8");
const blocs = [css.split(":root {")[1]!.split("}")[0]!, css.split(':root[data-theme="papier"] {')[1]!.split("}")[0]!];
const luminance = (hex: string) => {
  const c = hex.slice(1).match(/../g)!.map(v => parseInt(v, 16) / 255)
    .map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
  return c[0]! * .2126 + c[1]! * .7152 + c[2]! * .0722;
};
const contraste = (a: string, b: string) => {
  const l = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (l[0]! + .05) / (l[1]! + .05);
};
for (const [i, bloc] of blocs.entries()) test(`textes et boutons lisibles en ${i ? "Papier" : "Nuit"}`, () => {
  const tokens = Object.fromEntries([...bloc.matchAll(/(--[\w-]+):\s*(#[a-f\d]{6});/gi)].map(m => [m[1]!, m[2]!]));
  const rangs = Array.from({ length: 10 }, (_, n) => `--c-rang-${n + 1}`);
  for (const fond of ["--c-fond", "--c-surface", "--c-surface-elevee", "--c-surface-creuse"])
    for (const texte of ["--c-encre", "--c-encre-2", "--c-encre-3", "--c-succes", "--c-erreur", "--c-avertissement", ...rangs])
      expect(contraste(tokens[texte]!, tokens[fond]!), `${texte} sur ${fond}`).toBeGreaterThanOrEqual(4.5);
  for (const rang of rangs)
    expect(contraste(tokens["--c-sur-accent"]!, tokens[rang]!), `bouton ${rang}`).toBeGreaterThanOrEqual(4.5);
});

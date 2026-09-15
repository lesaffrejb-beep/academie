import type { LigneJournal } from "../donnees/types";

function instant(quand: string): [number, string] {
  const m = /^(\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2})(?:\.(\d+))?([Zz]|[+-]\d{2}:\d{2})?$/.exec(quand);
  if (!m) return [-Infinity, ""];
  const secondes = Date.parse(`${m[1]?.toUpperCase().replace(" ", "T")}${(m[3] ?? "Z").toUpperCase()}`);
  return [Number.isFinite(secondes) ? secondes : -Infinity, (m[2] ?? "").replace(/0+$/, "")];
}

/** Python compare les points de code Unicode, pas les unités UTF-16. */
function compare(a: string, b: string): number {
  const aa = Array.from(a); const bb = Array.from(b);
  for (let i = 0; i < Math.min(aa.length, bb.length); i++) {
    const x = aa[i]?.codePointAt(0) ?? 0; const y = bb[i]?.codePointAt(0) ?? 0;
    if (x !== y) return x < y ? -1 : 1;
  }
  return aa.length - bb.length;
}

/** UTC pour les anciens horodatages sans zone ; fraction sans perte. */
export function compareJournal(a: LigneJournal, b: LigneJournal): number {
  const [ta, fa] = instant(a.quand ?? ""); const [tb, fb] = instant(b.quand ?? "");
  if (ta !== tb) return ta < tb ? -1 : 1;
  const longueur = Math.max(fa.length, fb.length);
  return compare(fa.padEnd(longueur, "0"), fb.padEnd(longueur, "0"))
    || compare(a.quand ?? "", b.quand ?? "") || compare(a.mode ?? "", b.mode ?? "")
    || compare(a.nonce ?? "", b.nonce ?? "");
}

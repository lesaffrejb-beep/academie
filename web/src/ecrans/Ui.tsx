/**
 * Briques nues. Mise en page minimale, tokens seulement, zero animation,
 * zero illustration : la couche visuelle se refait ici sans toucher au
 * moteur (consigne JB du 03/09/2026).
 */

import type { ButtonHTMLAttributes, ReactNode } from "react";

export function Bouton({
  enfants, primaire, ...reste
}: { enfants: ReactNode; primaire?: boolean } & ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      type="button"
      {...reste}
      className={
        "min-h-11 rounded-int border px-4 py-2 text-left disabled:opacity-50 " +
        (primaire
          ? "border-accent bg-surface text-encre"
          : "border-trait bg-surface text-encre")
      }
    >
      {enfants}
    </button>
  );
}

export function Feuille({ enfants, titre }: { enfants: ReactNode; titre?: string }) {
  return (
    <section className="rounded-ext border border-trait bg-surface p-4">
      {titre ? <h2 className="mb-2 font-titre text-lg">{titre}</h2> : null}
      {enfants}
    </section>
  );
}

export function Jauge({ part, accent }: { part: number; accent?: string }) {
  const pct = Math.max(0, Math.min(1, part));
  return (
    <div
      className="h-1 w-full rounded-int bg-trait"
      role="progressbar"
      aria-valuenow={Math.round(pct * 100)}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <div
        className="h-1 rounded-int"
        style={{ width: `${pct * 100}%`, background: accent ?? "var(--c-accent)" }}
      />
    </div>
  );
}

export function Titre({ enfants }: { enfants: ReactNode }) {
  return <h1 className="mb-4 font-titre text-2xl">{enfants}</h1>;
}

export function Secondaire({ enfants }: { enfants: ReactNode }) {
  return <p className="text-encre-2">{enfants}</p>;
}

export function pourcent(x: number): string {
  return `${Math.round(x * 100)} %`;
}

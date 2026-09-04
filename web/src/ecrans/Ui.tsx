/**
 * Briques nues. Tokens seulement, aucun hexadecimal, aucune illustration :
 * la couche visuelle se refait ici sans toucher au moteur.
 *
 * Ce qui vient de DIRECTION-ARTISTIQUE.md §8 ter et §2 depuis le 03/09
 * au soir : le bouton principal est PLEIN de l'accent, les autres sont
 * creux ; un bouton n'a jamais d'ombre ; hauteur 48 px sur telephone,
 * 40 sur ordinateur (au-dessus des 44 px de cible tactile du §7 la ou ca
 * compte, le doigt) ; l'etat presse est une echelle de 98 % en 120 ms,
 * pose dans `index.css` pour tous les boutons a la fois.
 *
 * L'ombre unique et douce est reservee a ce qui FLOTTE : la feuille.
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
        "min-h-12 rounded-int border px-4 py-2 text-left disabled:opacity-50 md:min-h-10 " +
        (primaire
          ? "border-accent bg-accent font-medium text-sur-accent"
          : "border-trait bg-surface text-encre")
      }
    >
      {enfants}
    </button>
  );
}

export function Feuille({ enfants, titre, flottante }: {
  enfants: ReactNode; titre?: string; flottante?: boolean;
}) {
  return (
    <section
      className={
        "rounded-ext border border-trait bg-surface p-4 "
        + (flottante ? "shadow-flottante" : "")
      }
    >
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

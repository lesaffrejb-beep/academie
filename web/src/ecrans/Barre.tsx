/** Barre a TROIS entrees : Cercle reste masque tant qu'ACA-CERCLE-1 n'est pas livre. */

import { LIB } from "../app/i18n";
import { va, type Route } from "../app/routage";

const ENTREES: { cle: Route["nom"]; chemin: string; libelle: string }[] = [
  { cle: "arbre", chemin: "/", libelle: LIB.arbre },
  { cle: "boite", chemin: "/boite", libelle: LIB.boite },
  { cle: "profil", chemin: "/profil", libelle: LIB.profil },
];

export function Barre({ route }: { route: Route }) {
  return (
    <nav
      aria-label={LIB.app}
      className="sticky bottom-0 flex border-t border-trait bg-surface"
    >
      {ENTREES.map((e) => (
        <button
          key={e.cle}
          type="button"
          onClick={() => va(e.chemin)}
          aria-current={route.nom === e.cle ? "page" : undefined}
          className={
            "min-h-12 flex-1 px-2 py-3 " +
            (route.nom === e.cle ? "text-encre underline" : "text-encre-2")
          }
        >
          {e.libelle}
        </button>
      ))}
    </nav>
  );
}

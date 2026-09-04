/** Barre a TROIS entrees : Cercle reste masque tant qu'ACA-CERCLE-1 n'est pas livre. */

import { LIB } from "../app/i18n";
import { va, type Route } from "../app/routage";
import { Network, Inbox, UserRound, BookOpen, Play, type LucideIcon } from "lucide-react";

const ENTREES: { cle: Route["nom"]; chemin: string; libelle: string; icon: LucideIcon }[] = [
  { cle: "arbre", chemin: "/", libelle: LIB.arbre, icon: Network },
  { cle: "boite", chemin: "/boite", libelle: LIB.boite, icon: Inbox },
  { cle: "profil", chemin: "/profil", libelle: LIB.profil, icon: UserRound },
];

export function Barre({ route }: { route: Route }) {
  return (
    <nav
      aria-label={LIB.app}
      className="navigation"
    >
      <a className="marque-rail" href="#/" aria-label={LIB.app}><BookOpen size={28} strokeWidth={1.2} /></a>
      <button className="seance-rail" type="button" title={LIB.seance}
        aria-label="Commencer une séance" onClick={() => va("/salle/seance")}><Play size={19} /></button>
      {ENTREES.map((e) => (
        <button
          key={e.cle}
          type="button"
          onClick={() => va(e.chemin)}
          aria-current={(route.nom === e.cle || (e.cle === "arbre" && ["domaine", "noeud"].includes(route.nom))) ? "page" : undefined}
          className="entree-nav"
        >
          <e.icon size={22} strokeWidth={1.5} aria-hidden="true" /><span>{e.libelle}</span>
        </button>
      ))}
      <a className="credits-rail" href="#/credits">{LIB.credits}</a>
    </nav>
  );
}

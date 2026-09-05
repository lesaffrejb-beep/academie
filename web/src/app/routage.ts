/**
 * Routage maison sur le fragment (#/...). Aucune dependance : le client
 * est jetable, il n'a pas besoin d'un routeur pour neuf ecrans.
 */

import { useEffect, useState } from "react";

export interface Route {
  nom:
    | "accueil" | "etude" | "arbre" | "domaine" | "noeud" | "seance" | "cloture"
    | "profil" | "boite" | "credits" | "confiance";
  parametre?: string;
}

export function analyse(fragment: string): Route {
  const chemin = fragment.replace(/^#\/?/, "").split("?")[0] ?? "";
  const bouts = chemin.split("/").filter(Boolean);
  const tete = bouts[0] ?? "";
  const queue = bouts.slice(1).join("/");
  switch (tete) {
    case "arbre": return {nom: "arbre"};
    case "domaine": return { nom: "domaine", parametre: queue };
    case "noeud": return { nom: "noeud", parametre: queue };
    case "salle":
      if (bouts[1] === "etude") return {nom:"etude", parametre:bouts.slice(2).join("/")};
      return bouts[1] === "cloture" ? { nom: "cloture" } : { nom: "seance", parametre: bouts[2] };
    case "profil": return { nom: "profil" };
    case "boite": return { nom: "boite" };
    case "credits": return { nom: "credits" };
    case "confiance": return { nom: "confiance", parametre: queue };
    default: return { nom: "accueil" };
  }
}

export function va(chemin: string): void {
  window.location.hash = chemin.startsWith("#") ? chemin : `#${chemin}`;
}

export function useRoute(): Route {
  const [route, setRoute] = useState<Route>(() => analyse(window.location.hash));
  useEffect(() => {
    const surChangement = () => setRoute(analyse(window.location.hash));
    window.addEventListener("hashchange", surChangement);
    return () => window.removeEventListener("hashchange", surChangement);
  }, []);
  return route;
}

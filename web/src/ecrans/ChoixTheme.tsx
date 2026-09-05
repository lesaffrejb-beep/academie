import { useEffect, useState } from "react";
import { Moon, Sun } from "lucide-react";
import { poseTheme, themeCourant } from "../app/theme";

export function ChoixTheme() {
  const [theme, setTheme] = useState(themeCourant);
  useEffect(() => {
    // Le profil peut aussi changer le thème pendant que l'en-tête est monté.
    const observation = new MutationObserver(() => {
      setTheme(document.documentElement.dataset.theme === "papier" ? "papier" : "nuit");
    });
    observation.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    return () => observation.disconnect();
  }, []);
  const suivant = theme === "nuit" ? "papier" : "nuit";
  const libelle = suivant === "papier" ? "Papier" : "Nuit";
  return <button className="choix-theme" aria-label={`Activer le thème ${libelle}`}
    onClick={() => { poseTheme(suivant); setTheme(suivant); }}>
    {suivant === "papier" ? <Sun size={18} strokeWidth={1.5} /> : <Moon size={18} strokeWidth={1.5} />}
    <span>{libelle}</span>
  </button>;
}

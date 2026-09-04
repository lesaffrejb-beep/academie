import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import { FournisseurMagasin, useMagasin } from "./app/magasin";
import { useRoute } from "./app/routage";
import { poseTheme, themeCourant } from "./app/theme";
import { LIB } from "./app/i18n";
import { Barre } from "./ecrans/Barre";
import { Arbre } from "./ecrans/Arbre";
import { Domaine } from "./ecrans/Domaine";
import { Noeud } from "./ecrans/Noeud";
import { Seance } from "./ecrans/Seance";
import { Cloture } from "./ecrans/Cloture";
import { Profil } from "./ecrans/Profil";
import { Boite } from "./ecrans/Boite";
import { Credits } from "./ecrans/Credits";
import { Confiance } from "./ecrans/Confiance";

poseTheme(themeCourant());

function Application() {
  const route = useRoute();
  const { pret, panne } = useMagasin();

  if (panne) return <div className="p-4">{panne}</div>;
  if (!pret) return <div className="p-4">{LIB.chargement}</div>;

  // La salle est plein ecran, sans barre (DIRECTION-ARTISTIQUE 4).
  const enSalle = route.nom === "seance" || route.nom === "cloture";

  let ecran: JSX.Element;
  switch (route.nom) {
    case "domaine": ecran = <Domaine cle={route.parametre ?? ""} />; break;
    case "noeud": ecran = <Noeud chemin={route.parametre ?? ""} />; break;
    case "seance": ecran = <Seance portee={route.parametre} />; break;
    case "cloture": ecran = <Cloture />; break;
    case "profil": ecran = <Profil />; break;
    case "boite": ecran = <Boite />; break;
    case "credits": ecran = <Credits />; break;
    case "confiance": ecran = <Confiance domaine={route.parametre} />; break;
    default: ecran = <Arbre />;
  }

  return (
    <div className={enSalle ? "application en-salle" : "application"}>
      {enSalle ? null : <header className="entete-app"><a href="#/" className="marque">{LIB.app}<span className="marque-point" /></a><span className="date-app">{new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long" }).format(new Date())}</span></header>}
      <main className="contenu-app">{ecran}</main>
      {enSalle ? null : <Barre route={route} />}
    </div>
  );
}

const racine = document.getElementById("racine");
if (racine) {
  createRoot(racine).render(
    <StrictMode>
      <FournisseurMagasin enfants={<Application />} />
    </StrictMode>,
  );
}

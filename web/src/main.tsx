import { StrictMode, useEffect } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./experience.css";
import { Accueil } from "./ecrans/Accueil";
import { Etude } from "./ecrans/Etude";
import { ChoixTheme } from "./ecrans/ChoixTheme";

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
  useEffect(() => {
    if (!pret) return;
    const retour = sessionStorage.getItem("academie-retour-noeud");
    if (route.nom === "domaine" && retour) {
      sessionStorage.removeItem("academie-retour-noeud");
      const bouton = Array.from(document.querySelectorAll<HTMLElement>("[data-chapitre]")).find(b => b.dataset.chapitre === retour);
      if (bouton) { bouton.focus(); return; }
    }
    if (route.nom === "noeud") return;
    const titre = document.querySelector<HTMLElement>("main h1");
    if (titre) { titre.tabIndex = -1; titre.focus({preventScroll:true}); }
    window.scrollTo(0,0);
  }, [route.nom, route.parametre, pret]);

  if (panne) return <div className="p-4">{panne}</div>;
  if (!pret) return <div className="p-4">{LIB.chargement}</div>;

  // La salle est plein ecran, sans barre (DIRECTION-ARTISTIQUE 4).
  const enSalle = route.nom === "etude" || route.nom === "seance" || route.nom === "cloture";

  let ecran: JSX.Element;
  switch (route.nom) {
    case "etude": ecran = <Etude id={route.parametre ?? ""} />; break;
    case "arbre": ecran = <Arbre />; break;
    case "domaine": ecran = <Domaine cle={route.parametre ?? ""} />; break;
    case "noeud": ecran = <Noeud chemin={route.parametre ?? ""} />; break;
    case "seance": ecran = <Seance portee={route.parametre} />; break;
    case "cloture": ecran = <Cloture />; break;
    case "profil": ecran = <Profil />; break;
    case "boite": ecran = <Boite />; break;
    case "credits": ecran = <Credits />; break;
    case "confiance": ecran = <Confiance domaine={route.parametre} />; break;
    default: ecran = <Accueil />;
  }

  return (
    <div className={enSalle ? "application en-salle" : "application"}>
      {enSalle ? null : <header className="entete-app"><a href="#/" className="marque">{LIB.app}<span className="marque-point" /></a><div className="entete-outils"><span className="date-app">{new Intl.DateTimeFormat("fr-FR", { weekday: "long", day: "numeric", month: "long" }).format(new Date())}</span><ChoixTheme key={route.nom} /></div></header>}
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

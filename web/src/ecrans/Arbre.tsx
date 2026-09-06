import { useState, type CSSProperties } from "react";
import { ArrowRight, ChevronLeft, ChevronRight, Play } from "lucide-react";
import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import { compose } from "../moteur/composeur";
import { etudeDisponible } from "../moteur/etude";
import type { Noeud } from "../moteur/progression";
import { Bouton } from "./Ui";
import { Glyphe } from "./Icones";
import { GrapheMindmap } from "./GrapheSavoir";
import { GraphePrerequis } from "./GraphePrerequis";

export function Arbre() {
  const { banque, monde, etats, jour, journal } = useMagasin();
  const [selection, selectionne] = useState(0);
  const [vueMode, setVueMode] = useState<"domaines" | "graphe">("domaines");
  if (!banque || !monde) return null;
  const regions = monde.regions;
  const region = regions[selection] ?? regions[0];
  const seance = compose(banque, etats, { aujourdhui: jour, journal });
  const dues = seance.revisions.length;
  const neuves = seance.nouveau.length;
  const noeuds = monde.noeuds.filter((n) => n.domaine === region?.cle);
  const branches = monde.branches.filter((b) => b.domaine === region?.cle);
  const etudesDisponibles = new Set(monde.noeuds.filter(n => {
    const lecon = banque.etudes?.lecons[n.id];
    return lecon && etudeDisponible(lecon, banque.cartes, journal, jour);
  }).map(n => n.id));
  const couverture = (chapitres: Noeud[]) => {
    const socle = chapitres.filter(n => !n.satellite).length;
    const etudesSocle = chapitres.filter(n => !n.satellite && etudesDisponibles.has(n.id)).length;
    const approfondissements = chapitres.filter(n => n.satellite && etudesDisponibles.has(n.id)).length;
    const disponibles = etudesSocle + approfondissements;
    return <>
      <p className="mesure-apercu">{`${socle} chapitre${socle > 1 ? "s" : ""} prévu${socle > 1 ? "s" : ""} dans le socle`}</p>
      <p className="mesure-apercu">{`${disponibles} étude${disponibles !== 1 ? "s" : ""} disponible${disponibles !== 1 ? "s" : ""} : ${etudesSocle} du socle · ${approfondissements} approfondissement${approfondissements > 1 ? "s" : ""}`}</p>
    </>;
  };
  const cap = seance.arriereReetale > 0 ? voix("cap.reprise", { dues }, jour)
    : dues || neuves ? `${dues} ${dues === 1 ? LIB.carteDue : LIB.cartesDues} · ${neuves} ${neuves === 1 ? LIB.carteNeuve : LIB.cartesNeuves}` : voix("cap.rien", {}, jour);
  const choisi = (index: number) => selectionne((index + regions.length) % regions.length);

  return <div className="page-arbre">
    <header className="titre-arbre">
      <div>
        <h1 className="titre-page">{LIB.arbre}</h1>
        {couverture(monde.noeuds)}
        <p>{banque.cartes.length} {LIB.cartesDisponibles}</p>
      </div>
      <div className="graphe-vues" role="group" aria-label="Vue du programme">
        <button type="button" onClick={() => setVueMode("domaines")} aria-pressed={vueMode === "domaines"}>Domaines</button>
        <button type="button" onClick={() => setVueMode("graphe")} aria-pressed={vueMode === "graphe"}>Graphe des prérequis</button>
      </div>
    </header>

    {vueMode === "graphe" ? (
      <GraphePrerequis monde={monde} banque={banque} journal={journal} jour={jour} />
    ) : (
      <div className="exploration-composition">
      <div className="index-domaines" data-testid="atlas" aria-label="Domaines du programme">
        {regions.map((r, i) => {
          const liste = monde.branches.filter(b => b.domaine === r.cle);
          return <button type="button" key={r.cle} className="domaine-ligne"
            aria-pressed={i === selection} onClick={() => { if (window.matchMedia("(max-width: 767px)").matches) va(`/domaine/${r.cle}`); else choisi(i); }}
            style={{ "--c-domaine": accentDuRang(r.rang) } as CSSProperties}>
            <div className="domaine-pastille" aria-hidden="true">
              <Glyphe rang={r.rang} taille={20} />
            </div>
            <div className="domaine-info">
              <span className="domaine-nom">{r.titre}</span>
              <span className="domaine-branches">{liste.slice(0, 2).map(b => b.titre).join(" · ")}</span>
            </div>
            <span className="domaine-contenu">{r.cartesTotales ? `${r.cartesTotales} ${LIB.cartesDisponibles}` : "Au programme"}</span>
            <ArrowRight size={18} aria-hidden="true" />
          </button>;
        })}
      </div>
      {region ? <aside className="apercu-domaine" style={{ "--c-domaine": accentDuRang(region.rang) } as CSSProperties} aria-label={LIB.apercu}>
        <div className="apercu-navigation">
          <div className="apercu-sceau" aria-hidden="true">
            <Glyphe rang={region.rang} taille={22} />
          </div>
          <div className="flex gap-1">
            <button className="bouton-icone" title={LIB.domainePrecedent} aria-label={LIB.domainePrecedent} onClick={() => choisi(selection - 1)}><ChevronLeft size={20} /></button>
            <button className="bouton-icone" title={LIB.domaineSuivant} aria-label={LIB.domaineSuivant} onClick={() => choisi(selection + 1)}><ChevronRight size={20} /></button>
          </div>
        </div>
        <h2>{region.titre}</h2>
        {couverture(noeuds)}
        <p className="mesure-apercu">{region.cartesTotales} {LIB.cartesDisponibles}</p>
        <ul className="branches-apercu">{branches.map((b) => <li key={b.cle}><span />{b.titre}</li>)}</ul>
        <GrapheMindmap region={region} branches={branches} noeuds={noeuds} classe="mt-3 mb-4" />
        <button className="lien-action" onClick={() => va(`/domaine/${region.cle}`)}>{LIB.explorerDomaine}<ArrowRight size={18} /></button>
      </aside> : null}
    </div>)}
    <footer className="cap-jour"><div><span className="point-cap" /><p>{cap}</p></div><div className="actions-cap">
      <button className="lien-hasard" onClick={() => va("/salle/seance/hasard")}>{LIB.auHasard}</button>
      <Bouton primaire onClick={() => va("/salle/seance")} enfants={<><Play size={16} />{LIB.seance}<ArrowRight size={18} /></>} />
    </div></footer>
  </div>;
}

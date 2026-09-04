import { useRef, useState, type CSSProperties } from "react";
import { ArrowRight, ChevronLeft, ChevronRight, Minus, Plus, RotateCcw, Play } from "lucide-react";
import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import { compose } from "../moteur/composeur";
import { Anneau, Glyphe } from "./Icones";
import { Bouton, pourcent } from "./Ui";

export function Arbre() {
  const { banque, monde, etats, jour, journal } = useMagasin();
  const [selection, selectionne] = useState(0);
  const [zoom, agrandis] = useState(1);
  const [rotation, tourne] = useState(0);
  const depart = useRef<{ x: number; rotation: number } | null>(null);
  if (!banque || !monde) return null;
  const regions = monde.regions;
  const region = regions[selection] ?? regions[0];
  const seance = compose(banque, etats, { aujourdhui: jour, journal });
  const dues = seance.revisions.length;
  const neuves = seance.nouveau.length;
  const noeuds = monde.noeuds.filter((n) => n.domaine === region?.cle);
  const branches = monde.branches.filter((b) => b.domaine === region?.cle);
  const cap = seance.arriereReetale > 0 ? voix("cap.reprise", { dues }, jour)
    : dues || neuves ? `${dues} ${dues === 1 ? LIB.carteDue : LIB.cartesDues} · ${neuves} ${neuves === 1 ? LIB.carteNeuve : LIB.cartesNeuves}` : voix("cap.rien", {}, jour);
  const choisi = (index: number) => selectionne((index + regions.length) % regions.length);

  return <div className="page-arbre">
    <header className="titre-arbre"><h1 className="titre-page">{LIB.arbre}</h1>
      <p>{monde.noeuds.length} {LIB.chapitres}<span className="separateur">/</span>{banque.cartes.length} {LIB.cartesDisponibles}</p>
    </header>
    <div className="atlas-composition">
      <div className="atlas-cadre" data-testid="atlas">
        <div className="atlas" style={{ "--zoom-atlas": zoom } as CSSProperties}
          onPointerDown={(e) => { if ((e.target as Element).closest("button")) return; depart.current = { x: e.clientX, rotation }; e.currentTarget.setPointerCapture(e.pointerId); }}
          onPointerMove={(e) => { if (depart.current) tourne(depart.current.rotation + (e.clientX - depart.current.x) * 0.25); }}
          onPointerUp={() => { depart.current = null; }} onPointerCancel={() => { depart.current = null; }}>
          <svg className="atlas-liens" viewBox="0 0 1000 680" preserveAspectRatio="none" aria-hidden="true">
            <ellipse className="atlas-orbite" cx="500" cy="340" rx="365" ry="245" />
            <ellipse className="atlas-orbite interne" cx="500" cy="340" rx="245" ry="164" />
            <path className="atlas-tronc" d="M 500 257 L 500 423" />
            {regions.map((r, i) => {
              const angle = ((i / regions.length) * 360 - 90 + rotation) * Math.PI / 180;
              const x = 500 + Math.cos(angle) * 365, y = 340 + Math.sin(angle) * 245;
              const chapitres = monde.noeuds.filter((n) => n.domaine === r.cle);
              return <g key={r.cle} style={{ color: accentDuRang(r.rang) }} className={i === selection ? "lien-actif" : ""}>
                <path className="atlas-lien" d={`M 500 340 Q ${500 + Math.cos(angle) * 160} ${340 + Math.sin(angle) * 15} ${x} ${y}`} />
                {chapitres.map((n, j) => {
                  const t = 0.43 + (j / Math.max(1, chapitres.length - 1)) * 0.4, offset = j % 2 === 0 ? -7 : 7;
                  return <circle key={n.id} className={n.cartesTotales ? "point-disponible" : "point-programme"}
                    cx={500 + (x - 500) * t + Math.sin(angle) * offset}
                    cy={340 + (y - 340) * t - Math.cos(angle) * offset} r={n.cartesTotales ? 2.5 : 1.5} />;
                })}
              </g>;
            })}
          </svg>
          <div className="atlas-coeur"><span className="coeur-trait" /><span>{LIB.socle}</span><small>{LIB.aExplorer}</small><span className="coeur-trait" /></div>
          {regions.map((r, i) => {
            const angle = ((i / regions.length) * 360 - 90 + rotation) * Math.PI / 180;
            return <button type="button" key={r.cle} className={`atlas-domaine ${i === selection ? "selectionne" : ""}`}
              aria-label={`${r.titre}, ${pourcent(r.remplissage)}, ${r.cartesTotales} ${LIB.cartesDisponibles}`}
              aria-pressed={i === selection} onClick={() => choisi(i)}
              style={{ left: `${50 + Math.cos(angle) * 36.5}%`, top: `${50 + Math.sin(angle) * 36}%`, "--c-domaine": accentDuRang(r.rang) } as CSSProperties}>
              <span className="disque-domaine"><Anneau part={r.remplissage} /><Glyphe rang={r.rang} /></span>
              <span className="nom-domaine">{r.titre}</span><span className="mesure-domaine">{pourcent(r.remplissage)}</span>
            </button>;
          })}
        </div>
        <div className="outils-atlas">
          <button className="bouton-icone" aria-label={LIB.zoomMoins} title={LIB.zoomMoins} onClick={() => agrandis(Math.max(0.8, zoom - 0.1))}><Minus size={18} /></button>
          <button className="bouton-icone" aria-label={LIB.recentrer} title={LIB.recentrer} onClick={() => { agrandis(1); tourne(0); }}><RotateCcw size={16} /></button>
          <button className="bouton-icone" aria-label={LIB.zoomPlus} title={LIB.zoomPlus} onClick={() => agrandis(Math.min(1.3, zoom + 0.1))}><Plus size={18} /></button>
        </div>
      </div>
      {region ? <aside className="apercu-domaine" style={{ "--c-domaine": accentDuRang(region.rang) } as CSSProperties} aria-label={LIB.apercu}>
        <div className="apercu-navigation"><span className="rang-domaine">{String(region.rang).padStart(2, "0")}</span><div>
          <button className="bouton-icone" title={LIB.domainePrecedent} aria-label={LIB.domainePrecedent} onClick={() => choisi(selection - 1)}><ChevronLeft size={20} /></button>
          <button className="bouton-icone" title={LIB.domaineSuivant} aria-label={LIB.domaineSuivant} onClick={() => choisi(selection + 1)}><ChevronRight size={20} /></button>
        </div></div>
        <h2>{region.titre}</h2><p className="mesure-apercu">{noeuds.length} {LIB.chapitres} · {region.cartesTotales} {LIB.cartesDisponibles}</p>
        <ul className="branches-apercu">{branches.slice(0, 4).map((b) => <li key={b.cle}><span />{b.titre}</li>)}</ul>
        <button className="lien-action" onClick={() => va(`/domaine/${region.cle}`)}>{LIB.explorerDomaine}<ArrowRight size={18} /></button>
      </aside> : null}
    </div>
    <footer className="cap-jour"><div><span className="point-cap" /><p>{cap}</p></div><div className="actions-cap">
      <button className="lien-hasard" onClick={() => va("/salle/seance/hasard")}>{LIB.auHasard}</button>
      <Bouton primaire onClick={() => va("/salle/seance")} enfants={<><Play size={16} />{LIB.seance}<ArrowRight size={18} /></>} />
    </div></footer>
  </div>;
}

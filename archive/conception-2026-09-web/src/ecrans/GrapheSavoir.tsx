import { useMemo, useState, useRef, type CSSProperties, type MouseEvent } from "react";
import {
  ArrowRight,
  Grid,
  Layers,
  Lock,
  Play,
  RotateCcw,
  Search,
  Sparkles,
  X,
  ZoomIn,
  ZoomOut,
} from "lucide-react";

import type { Banque } from "../donnees/types";
import type { Branche, CarteMonde, Noeud, Region } from "../moteur/progression";
import { accentDuRang } from "../app/theme";
import { va } from "../app/routage";
import { ETATS_NOEUD, LIB } from "../app/i18n";
import { Glyphe } from "./Icones";
import { AnneauProgression, CarteMagnetique, Liquid } from "./MicroAnimations";
import { pourcent } from "./Ui";

interface PointRadialDomaine {
  region: Region;
  angle: number;
  x: number;
  y: number;
  couleur: string;
}

interface PointRadialBranche {
  branche: Branche;
  domaineCle: string;
  angle: number;
  x: number;
  y: number;
  couleur: string;
  dBezier: string;
}

interface PointRadialChapitre {
  noeud: Noeud;
  domaineCle: string;
  brancheCle: string;
  angle: number;
  x: number;
  y: number;
  couleur: string;
  dBezier: string;
}

export type TypeSelectionNoeud = "racine" | "domaine" | "branche" | "chapitre";

export interface InfoNoeudInspecteur {
  type: TypeSelectionNoeud;
  id: string;
  titre: string;
  parentDomaine?: string;
  parentBranche?: string;
  niveau?: number | null;
  remplissage?: number;
  cartesTotales?: number;
  cartesAcquises?: number;
  prerequis?: string[];
  etat?: string;
  couleur?: string;
}

/**
 * GrapheStudio : Studio de visualisation et d exploration du graphe des connaissances.
 * Inspire des travaux de Josef Müller-Brockmann (grille suisse orthogonale et radiale)
 * et des interfaces contemporaines (Linear, Notion, Holi skill tree).
 */
export function GrapheStudio({
  monde,
  banque,
  selectionInitiale = 0,
  surSelectionDomaine,
}: {
  monde: CarteMonde;
  banque: Banque;
  selectionInitiale?: number;
  surSelectionDomaine?: (index: number) => void;
}) {
  const [vueMode, setVueMode] = useState<"radial" | "arborescence">("radial");
  const [connecteurStyle, setConnecteurStyle] = useState<"courbe" | "echelonne">("courbe");
  const [recherche, setRecherche] = useState("");
  const [niveauFiltre, setNiveauFiltre] = useState<number | null>(null);
  const [grilleActive, setGrilleActive] = useState(true);
  const [menuGooeyOuvert, setMenuGooeyOuvert] = useState(false);

  // Navigation Pan & Zoom
  const [zoom, setZoom] = useState(1);
  const [pan, setPan] = useState({ x: 0, y: 0 });
  const [estEnGlisse, setEstEnGlisse] = useState(false);
  const pointDepartRef = useRef({ x: 0, y: 0 });

  // Inspection
  const [noeudActif, setNoeudActif] = useState<InfoNoeudInspecteur | null>(() => {
    const r = monde.regions[selectionInitiale] ?? monde.regions[0];
    if (!r) return null;
    return {
      type: "domaine",
      id: r.cle,
      titre: r.titre,
      remplissage: r.remplissage,
      cartesTotales: r.cartesTotales,
      cartesAcquises: r.cartesAcquises,
      couleur: accentDuRang(r.rang),
    };
  });
  const [survolId, setSurvolId] = useState<string | null>(null);

  // Recalcul du layout radial 360 degres
  const layout = useMemo(() => {
    const cx = 440;
    const cy = 440;
    const R_DOMAINE = 135;
    const R_BRANCHE = 235;
    const R_CHAPITRE = 345;

    const regions = monde.regions;
    const branches = monde.branches;
    const noeuds = monde.noeuds;
    const nDomaines = Math.max(1, regions.length);
    const deltaDomaine = (2 * Math.PI) / nDomaines;

    const pointsDomaines: PointRadialDomaine[] = [];
    const pointsBranches: PointRadialBranche[] = [];
    const pointsChapitres: PointRadialChapitre[] = [];

    regions.forEach((r, i) => {
      const angleDomaine = i * deltaDomaine - Math.PI / 2;
      const xD = cx + R_DOMAINE * Math.cos(angleDomaine);
      const yD = cy + R_DOMAINE * Math.sin(angleDomaine);
      const couleur = accentDuRang(r.rang);

      pointsDomaines.push({
        region: r,
        angle: angleDomaine,
        x: xD,
        y: yD,
        couleur,
      });

      const branchesDom = branches.filter((b) => b.domaine === r.cle);
      const nBranches = branchesDom.length;
      const spanDomaine = deltaDomaine * 0.76;

      branchesDom.forEach((b, j) => {
        const angleBranche =
          nBranches === 1
            ? angleDomaine
            : angleDomaine + (j / (nBranches - 1) - 0.5) * spanDomaine;

        const xB = cx + R_BRANCHE * Math.cos(angleBranche);
        const yB = cy + R_BRANCHE * Math.sin(angleBranche);

        const cp1xB = cx + (R_DOMAINE + 42) * Math.cos(angleDomaine);
        const cp1yB = cy + (R_DOMAINE + 42) * Math.sin(angleDomaine);
        const cp2xB = cx + (R_BRANCHE - 42) * Math.cos(angleBranche);
        const cp2yB = cy + (R_BRANCHE - 42) * Math.sin(angleBranche);
        const dBezierBranche = "M " + xD + " " + yD + " C " + cp1xB + " " + cp1yB + " " + cp2xB + " " + cp2yB + " " + xB + " " + yB;

        pointsBranches.push({
          branche: b,
          domaineCle: r.cle,
          angle: angleBranche,
          x: xB,
          y: yB,
          couleur,
          dBezier: dBezierBranche,
        });

        const chapitresBr = noeuds.filter((n) => n.domaine === r.cle && n.branche === b.cle);
        const nChapitres = chapitresBr.length;
        const spanBranche = Math.min(0.28, (spanDomaine / Math.max(1, nBranches)) * 0.86);

        chapitresBr.forEach((ch, k) => {
          const angleChapitre =
            nChapitres === 1
              ? angleBranche
              : angleBranche + (k / (nChapitres - 1) - 0.5) * spanBranche;

          const xC = cx + R_CHAPITRE * Math.cos(angleChapitre);
          const yC = cy + R_CHAPITRE * Math.sin(angleChapitre);

          const cp1xC = cx + (R_BRANCHE + 42) * Math.cos(angleBranche);
          const cp1yC = cy + (R_BRANCHE + 42) * Math.sin(angleBranche);
          const cp2xC = cx + (R_CHAPITRE - 42) * Math.cos(angleChapitre);
          const cp2yC = cy + (R_CHAPITRE - 42) * Math.sin(angleChapitre);
          const dBezierChapitre = "M " + xB + " " + yB + " C " + cp1xC + " " + cp1yC + " " + cp2xC + " " + cp2yC + " " + xC + " " + yC;

          pointsChapitres.push({
            noeud: ch,
            domaineCle: r.cle,
            brancheCle: b.cle,
            angle: angleChapitre,
            x: xC,
            y: yC,
            couleur,
            dBezier: dBezierChapitre,
          });
        });
      });
    });

    return {
      cx,
      cy,
      R_DOMAINE,
      R_BRANCHE,
      R_CHAPITRE,
      pointsDomaines,
      pointsBranches,
      pointsChapitres,
    };
  }, [monde]);

  // Filtrage par recherche
  const texteRecherche = recherche.trim().toLocaleLowerCase("fr");
  const estFiltre = texteRecherche.length > 0 || niveauFiltre !== null;

  const noeudCorrespond = (id: string, titre: string, niveau?: number | null) => {
    if (niveauFiltre !== null && niveau !== undefined && niveau !== null && niveau !== niveauFiltre) {
      return false;
    }
    if (!texteRecherche) return true;
    return titre.toLocaleLowerCase("fr").includes(texteRecherche) || id.toLocaleLowerCase("fr").includes(texteRecherche);
  };

  // Gestion Pan & Zoom
  const surMouseDown = (e: MouseEvent<SVGSVGElement>) => {
    if ((e.target as HTMLElement).tagName === "circle" || (e.target as HTMLElement).tagName === "text") return;
    setEstEnGlisse(true);
    pointDepartRef.current = { x: e.clientX - pan.x, y: e.clientY - pan.y };
  };

  const surMouseMove = (e: MouseEvent<SVGSVGElement>) => {
    if (!estEnGlisse) return;
    setPan({
      x: e.clientX - pointDepartRef.current.x,
      y: e.clientY - pointDepartRef.current.y,
    });
  };

  const surMouseUp = () => setEstEnGlisse(false);

  const zoomAvant = () => setZoom((z) => Math.min(2.2, Math.round((z + 0.2) * 10) / 10));
  const zoomArriere = () => setZoom((z) => Math.max(0.6, Math.round((z - 0.2) * 10) / 10));
  const recentrerVue = () => {
    setZoom(1);
    setPan({ x: 0, y: 0 });
  };

  const activeDomaine = (domaineCle: string, index: number) => {
    const reg = monde.regions.find((r) => r.cle === domaineCle);
    if (!reg) return;
    setNoeudActif({
      type: "domaine",
      id: reg.cle,
      titre: reg.titre,
      remplissage: reg.remplissage,
      cartesTotales: reg.cartesTotales,
      cartesAcquises: reg.cartesAcquises,
      couleur: accentDuRang(reg.rang),
    });
    if (surSelectionDomaine) surSelectionDomaine(index);
  };

  const activeBranche = (b: Branche, couleur: string) => {
    setNoeudActif({
      type: "branche",
      id: b.cle,
      titre: b.titre,
      parentDomaine: b.domaine,
      remplissage: b.remplissage,
      cartesTotales: b.noeuds,
      couleur,
    });
  };

  const activeChapitre = (n: Noeud, couleur: string) => {
    setNoeudActif({
      type: "chapitre",
      id: n.id,
      titre: n.titre,
      parentDomaine: n.domaine,
      parentBranche: n.branche,
      niveau: n.niveau,
      remplissage: n.remplissage,
      cartesTotales: n.cartesTotales,
      cartesAcquises: n.cartesAcquises,
      prerequis: n.prerequis,
      etat: n.etat,
      couleur,
    });
  };

  return (
    <div className="graphe-studio relative flex flex-col rounded-3xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] shadow-md overflow-hidden transition-all">
      {/* Barre d outils superieure (HUD Josef Müller-Brockmann) */}
      <div className="flex flex-wrap items-center justify-between gap-3 p-4 border-b border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)]">
        {/* Fil d ariane contextuel */}
        <div className="flex items-center gap-2 text-xs text-[var(--c-encre-2)]">
          <button
            type="button"
            onClick={() => {
              setNoeudActif({
                type: "racine",
                id: "metier",
                titre: "Curriculum Métier",
                cartesTotales: banque.cartes.length,
                cartesAcquises: monde.noeuds.reduce((acc, n) => acc + n.cartesAcquises, 0),
                remplissage: monde.remplissageGlobal,
              });
            }}
            className="font-medium hover:text-[var(--c-encre)] transition"
          >
            Métier
          </button>
          {noeudActif && noeudActif.type !== "racine" ? (
            <>
              <span className="text-[var(--c-trait)]">/</span>
              <button
                type="button"
                onClick={() => {
                  const domCle = noeudActif.parentDomaine ?? (noeudActif.type === "domaine" ? noeudActif.id : undefined);
                  if (domCle) {
                    const r = monde.regions.find((reg) => reg.cle === domCle);
                    if (r) setNoeudActif({ type: "domaine", id: r.cle, titre: r.titre, couleur: accentDuRang(r.rang), remplissage: r.remplissage, cartesTotales: r.cartesTotales });
                  }
                }}
                className="font-medium hover:text-[var(--c-encre)] transition truncate max-w-[140px]"
              >
                {monde.regions.find((r) => r.cle === (noeudActif.parentDomaine ?? (noeudActif.type === "domaine" ? noeudActif.id : "")))?.titre ?? "Domaine"}
              </button>
            </>
          ) : null}
          {noeudActif && (noeudActif.type === "branche" || noeudActif.type === "chapitre") ? (
            <>
              <span className="text-[var(--c-trait)]">/</span>
              <span className="font-semibold text-[var(--c-encre)] truncate max-w-[180px]">
                {noeudActif.titre}
              </span>
            </>
          ) : null}
        </div>

        {/* Commandes HUD : Mode, Grille, Zoom */}
        <div className="flex items-center gap-2">
          {/* Selecteur de mode */}
          <div className="flex items-center p-0.5 rounded-full bg-[var(--c-surface)] border border-[var(--c-bordure-subtile)] text-xs">
            <button
              type="button"
              onClick={() => setVueMode("radial")}
              className={"px-2.5 py-1 rounded-full font-medium transition " + (vueMode === "radial" ? "bg-[var(--c-surface-elevee)] text-[var(--c-encre)] shadow-sm" : "text-[var(--c-encre-2)] hover:text-[var(--c-encre)]")}
            >
              <span className="hidden sm:inline">360° </span>Radial
            </button>
            <button
              type="button"
              onClick={() => setVueMode("arborescence")}
              className={"px-2.5 py-1 rounded-full font-medium transition " + (vueMode === "arborescence" ? "bg-[var(--c-surface-elevee)] text-[var(--c-encre)] shadow-sm" : "text-[var(--c-encre-2)] hover:text-[var(--c-encre)]")}
            >
              <span className="sm:hidden">Arbre</span>
              <span className="hidden sm:inline">Arborescence</span>
            </button>
          </div>

          {/* Grille Müller-Brockmann */}
          <button
            type="button"
            onClick={() => setGrilleActive(!grilleActive)}
            className={"p-1.5 rounded-lg border text-xs transition " + (grilleActive ? "border-[var(--c-encre)] bg-[var(--c-surface-elevee)] text-[var(--c-encre)]" : "border-[var(--c-bordure-subtile)] text-[var(--c-encre-2)] hover:text-[var(--c-encre)]")}
            title="Grille orthogonale suisse 8pt"
            aria-label="Afficher ou masquer la grille suisse"
          >
            <Grid size={15} />
          </button>

          {/* Outils de Zoom */}
          <div className="flex items-center rounded-lg border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] text-xs text-[var(--c-encre-2)]">
            <button
              type="button"
              onClick={zoomArriere}
              className="p-1.5 hover:text-[var(--c-encre)] transition"
              title="Zoom arrière"
              aria-label="Zoom arrière"
            >
              <ZoomOut size={15} />
            </button>
            <button
              type="button"
              onClick={recentrerVue}
              className="px-2 py-1 font-mono text-[11px] hover:text-[var(--c-encre)] border-x border-[var(--c-bordure-subtile)]"
              title="Recentrer et réinitialiser le zoom"
              aria-label="Recentrer la vue"
            >
              {Math.round(zoom * 100)}%
            </button>
            <button
              type="button"
              onClick={zoomAvant}
              className="p-1.5 hover:text-[var(--c-encre)] transition"
              title="Zoom avant"
              aria-label="Zoom avant"
            >
              <ZoomIn size={15} />
            </button>
          </div>
        </div>
      </div>

      {/* Barre de Recherche et Filtres */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-2.5 border-b border-[var(--c-bordure-subtile)] bg-[var(--c-surface)]">
        <div className="relative flex-1 min-w-[200px] max-w-sm">
          <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-[var(--c-encre-2)]" />
          <input
            type="search"
            value={recherche}
            onChange={(e) => setRecherche(e.target.value)}
            placeholder="Filtrer un concept, chapitre ou domaine..."
            className="w-full pl-8 pr-7 py-1 rounded-lg text-xs bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre)] focus:border-[var(--c-encre)] outline-none"
            aria-label="Rechercher dans le graphe"
          />
          {recherche ? (
            <button
              type="button"
              onClick={() => setRecherche("")}
              className="absolute right-2 top-1/2 -translate-y-1/2 text-[var(--c-encre-2)] hover:text-[var(--c-encre)]"
            >
              <X size={12} />
            </button>
          ) : null}
        </div>

        <div className="flex items-center gap-1.5 text-xs">
          <span className="text-[11px] text-[var(--c-encre-2)] mr-1">Niveau :</span>
          {[null, 1, 2, 3].map((niv) => (
            <button
              key={String(niv)}
              type="button"
              onClick={() => setNiveauFiltre(niv)}
              className={"px-2 py-0.5 rounded text-[11px] font-mono transition " + (niveauFiltre === niv ? "bg-[var(--c-encre)] text-[var(--c-fond)]" : "bg-[var(--c-surface-creuse)] text-[var(--c-encre-2)] hover:text-[var(--c-encre)] border border-[var(--c-bordure-subtile)]")}
            >
              {niv === null ? "Tous" : "N" + niv}
            </button>
          ))}

          {vueMode === "arborescence" ? (
            <div className="ml-3 pl-3 border-l border-[var(--c-bordure-subtile)] flex items-center gap-1.5">
              <button
                type="button"
                onClick={() => setConnecteurStyle("courbe")}
                className={"px-2 py-0.5 rounded text-[11px] transition " + (connecteurStyle === "courbe" ? "bg-[var(--c-surface-elevee)] text-[var(--c-encre)] font-semibold" : "text-[var(--c-encre-2)]")}
              >
                Courbes
              </button>
              <button
                type="button"
                onClick={() => setConnecteurStyle("echelonne")}
                className={"px-2 py-0.5 rounded text-[11px] transition " + (connecteurStyle === "echelonne" ? "bg-[var(--c-surface-elevee)] text-[var(--c-encre)] font-semibold" : "text-[var(--c-encre-2)]")}
              >
                Échelonné
              </button>
            </div>
          ) : null}
        </div>
      </div>

      {/* Zone Principale de Visualisation */}
      <div className={"relative w-full h-[520px] md:h-[620px] overflow-hidden " + (grilleActive ? "fond-grille-points" : "bg-[var(--c-surface)]")}>
        {vueMode === "radial" ? (
          /* VUE 1 : DENDROGRAMME RADIAL 360 DEGRES */
          <svg
            viewBox="0 0 880 880"
            className={"w-full h-full " + (estEnGlisse ? "cursor-grabbing" : "cursor-grab")}
            onMouseDown={surMouseDown}
            onMouseMove={surMouseMove}
            onMouseUp={surMouseUp}
            onMouseLeave={surMouseUp}
            role="img"
            aria-label="Visualisation radiale du graphe de compétences"
          >
            <defs>
              <filter id="lueur-synaptique" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="flou" />
                <feMerge>
                  <feMergeNode in="flou" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Grille circulaire suisse (Josef Müller-Brockmann) */}
            {grilleActive ? (
              <g className="grille-muller pointer-events-none" opacity={0.4}>
                <circle cx={layout.cx} cy={layout.cy} r={layout.R_DOMAINE} fill="none" stroke="var(--c-trait)" strokeWidth={1} strokeDasharray="3 3" />
                <circle cx={layout.cx} cy={layout.cy} r={layout.R_BRANCHE} fill="none" stroke="var(--c-trait)" strokeWidth={1} strokeDasharray="3 3" />
                <circle cx={layout.cx} cy={layout.cy} r={layout.R_CHAPITRE} fill="none" stroke="var(--c-trait)" strokeWidth={1} strokeDasharray="3 3" />
                <circle cx={layout.cx} cy={layout.cy} r={395} fill="none" stroke="var(--c-trait)" strokeWidth={0.7} />
                {/* Repères d angles radiaux */}
                {Array.from({ length: 24 }).map((_, idx) => {
                  const deg = (idx * 360) / 24;
                  const rad = (deg * Math.PI) / 180;
                  const x1 = layout.cx + 390 * Math.cos(rad);
                  const y1 = layout.cy + 390 * Math.sin(rad);
                  const x2 = layout.cx + 398 * Math.cos(rad);
                  const y2 = layout.cy + 398 * Math.sin(rad);
                  return <line key={idx} x1={x1} y1={y1} x2={x2} y2={y2} stroke="var(--c-trait)" strokeWidth={idx % 6 === 0 ? 1.5 : 0.8} />;
                })}
              </g>
            ) : null}

            {/* Groupe transformable : Pan & Zoom */}
            <g
              transform={"translate(" + pan.x + ", " + pan.y + ") scale(" + zoom + ")"}
              style={{
                transformOrigin: "440px 440px",
                transition: estEnGlisse ? "none" : "transform 220ms cubic-bezier(0.16, 1, 0.3, 1)",
              }}
            >
              {/* LIENS : Racine -> Domaines */}
              {layout.pointsDomaines.map((pd) => {
                const estActif =
                  noeudActif?.type === "racine" ||
                  noeudActif?.id === pd.region.cle ||
                  noeudActif?.parentDomaine === pd.region.cle ||
                  survolId === pd.region.cle;
                const matchRecherche = !estFiltre || noeudCorrespond(pd.region.cle, pd.region.titre);
                const dChemin = "M " + layout.cx + " " + layout.cy + " Q " + (layout.cx + layout.R_DOMAINE * 0.45 * Math.cos(pd.angle)) + " " + (layout.cy + layout.R_DOMAINE * 0.45 * Math.sin(pd.angle)) + " " + pd.x + " " + pd.y;

                return (
                  <g key={"lien-domaine-" + pd.region.cle}>
                    <path
                      d={dChemin}
                      fill="none"
                      stroke={estActif ? pd.couleur : "var(--c-trait)"}
                      strokeWidth={estActif ? 2.5 : 1.2}
                      opacity={matchRecherche ? (estActif ? 0.95 : 0.4) : 0.12}
                      className="transition-all duration-300"
                    />
                    {estActif ? (
                      <path
                        d={dChemin}
                        fill="none"
                        stroke={pd.couleur}
                        strokeWidth={3.5}
                        className="impulsion-synaptique pointer-events-none"
                        filter="url(#lueur-synaptique)"
                        opacity={0.85}
                      />
                    ) : null}
                  </g>
                );
              })}

              {/* LIENS : Domaines -> Branches */}
              {layout.pointsBranches.map((pb) => {
                const estActif =
                  noeudActif?.id === pb.branche.cle ||
                  noeudActif?.id === pb.domaineCle ||
                  noeudActif?.parentBranche === pb.branche.cle ||
                  survolId === pb.branche.cle ||
                  survolId === pb.domaineCle;
                const matchRecherche = !estFiltre || noeudCorrespond(pb.branche.cle, pb.branche.titre);

                return (
                  <g key={"lien-branche-" + pb.branche.cle}>
                    <path
                      d={pb.dBezier}
                      fill="none"
                      stroke={estActif ? pb.couleur : "var(--c-trait)"}
                      strokeWidth={estActif ? 2.2 : 1}
                      opacity={matchRecherche ? (estActif ? 0.9 : 0.35) : 0.1}
                      className="transition-all duration-300"
                    />
                    {estActif ? (
                      <path
                        d={pb.dBezier}
                        fill="none"
                        stroke={pb.couleur}
                        strokeWidth={3}
                        className="impulsion-synaptique pointer-events-none"
                        filter="url(#lueur-synaptique)"
                        opacity={0.85}
                      />
                    ) : null}
                  </g>
                );
              })}

              {/* LIENS : Branches -> Chapitres */}
              {layout.pointsChapitres.map((pc) => {
                const estActif =
                  noeudActif?.id === pc.noeud.id ||
                  noeudActif?.id === pc.brancheCle ||
                  noeudActif?.id === pc.domaineCle ||
                  survolId === pc.noeud.id;
                const matchRecherche = !estFiltre || noeudCorrespond(pc.noeud.id, pc.noeud.titre, pc.noeud.niveau);

                return (
                  <g key={"lien-chapitre-" + pc.noeud.id}>
                    <path
                      d={pc.dBezier}
                      fill="none"
                      stroke={estActif ? pc.couleur : "var(--c-trait)"}
                      strokeWidth={estActif ? 2 : 0.8}
                      opacity={matchRecherche ? (estActif ? 0.85 : 0.3) : 0.08}
                      className="transition-all duration-300"
                    />
                    {estActif ? (
                      <path
                        d={pc.dBezier}
                        fill="none"
                        stroke={pc.couleur}
                        strokeWidth={2.6}
                        className="impulsion-synaptique pointer-events-none"
                        filter="url(#lueur-synaptique)"
                        opacity={0.9}
                      />
                    ) : null}
                  </g>
                );
              })}

              {/* NOEUD CENTRAL : METIER / RACINE */}
              <g
                transform={"translate(" + layout.cx + ", " + layout.cy + ")"}
                className="cursor-pointer transition-transform duration-200 hover:scale-105"
                onClick={() => {
                  setNoeudActif({
                    type: "racine",
                    id: "metier",
                    titre: "Curriculum Métier",
                    cartesTotales: banque.cartes.length,
                    cartesAcquises: monde.noeuds.reduce((acc, n) => acc + n.cartesAcquises, 0),
                    remplissage: monde.remplissageGlobal,
                  });
                }}
                role="button"
                tabIndex={0}
                aria-label="Curriculum Métier"
              >
                <circle r={34} fill="var(--c-surface-elevee)" stroke="var(--c-bordure-forte)" strokeWidth={1.5} />
                <circle r={26} fill="var(--c-accent)" opacity={0.12} />
                <text
                  textAnchor="middle"
                  dominantBaseline="central"
                  fontSize="11"
                  fontWeight="600"
                  fill="var(--c-encre)"
                  fontFamily="var(--f-titre)"
                >
                  Métier
                </text>
              </g>

              {/* NOEUDS : DOMAINES */}
              {layout.pointsDomaines.map((pd, index) => {
                const estSelectionne = noeudActif?.id === pd.region.cle;
                const matchRecherche = !estFiltre || noeudCorrespond(pd.region.cle, pd.region.titre);
                const estSurvole = survolId === pd.region.cle;

                return (
                  <g
                    key={"noeud-domaine-" + pd.region.cle}
                    transform={"translate(" + pd.x + ", " + pd.y + ")"}
                    className="cursor-pointer transition-transform duration-200 hover:scale-110"
                    onClick={() => activeDomaine(pd.region.cle, index)}
                    onMouseEnter={() => setSurvolId(pd.region.cle)}
                    onMouseLeave={() => setSurvolId(null)}
                    role="button"
                    tabIndex={0}
                    aria-label={pd.region.titre}
                    opacity={matchRecherche ? 1 : 0.25}
                  >
                    {/* Onde orbitale pulsante si sélectionné */}
                    {estSelectionne ? (
                      <circle
                        r={22}
                        fill="none"
                        stroke={pd.couleur}
                        className="onde-orbitale pointer-events-none"
                      />
                    ) : null}
                    {/* Halo de lueur réactive au survol */}
                    {estSurvole ? (
                      <circle
                        r={26}
                        fill={pd.couleur}
                        opacity={0.3}
                        filter="url(#lueur-synaptique)"
                        className="pointer-events-none transition-opacity duration-200"
                      />
                    ) : null}
                    <circle
                      r={estSelectionne ? 18 : 14}
                      fill="var(--c-surface)"
                      stroke={pd.couleur}
                      strokeWidth={estSelectionne ? 3 : 2}
                      className="transition-all duration-200 shadow-sm"
                    />
                    <circle r={estSelectionne ? 9 : 7} fill={pd.couleur} />
                  </g>
                );
              })}

              {/* NOEUDS : BRANCHES */}
              {layout.pointsBranches.map((pb) => {
                const estSelectionne = noeudActif?.id === pb.branche.cle;
                const matchRecherche = !estFiltre || noeudCorrespond(pb.branche.cle, pb.branche.titre);
                const estSurvole = survolId === pb.branche.cle;

                return (
                  <g
                    key={"noeud-branche-" + pb.branche.cle}
                    transform={"translate(" + pb.x + ", " + pb.y + ")"}
                    className="cursor-pointer transition-transform duration-200 hover:scale-115"
                    onClick={() => activeBranche(pb.branche, pb.couleur)}
                    onMouseEnter={() => setSurvolId(pb.branche.cle)}
                    onMouseLeave={() => setSurvolId(null)}
                    role="button"
                    tabIndex={0}
                    aria-label={pb.branche.titre}
                    opacity={matchRecherche ? 1 : 0.2}
                  >
                    {estSelectionne ? (
                      <circle
                        r={15}
                        fill="none"
                        stroke={pb.couleur}
                        className="onde-orbitale pointer-events-none"
                      />
                    ) : null}
                    {estSurvole ? (
                      <circle
                        r={18}
                        fill={pb.couleur}
                        opacity={0.25}
                        filter="url(#lueur-synaptique)"
                        className="pointer-events-none transition-opacity duration-200"
                      />
                    ) : null}
                    <circle
                      r={estSelectionne ? 11 : 8}
                      fill="var(--c-surface-creuse)"
                      stroke={pb.couleur}
                      strokeWidth={estSelectionne ? 2.5 : 1.5}
                      className="transition-all duration-200"
                    />
                    <text
                      textAnchor="middle"
                      dominantBaseline="central"
                      fontSize="8"
                      fontWeight="600"
                      fill="var(--c-encre)"
                      fontFamily="var(--f-mono)"
                    >
                      {pb.branche.noeuds}
                    </text>
                  </g>
                );
              })}

              {/* NOEUDS : CHAPITRES (FEUILLES SATELLITES) */}
              {layout.pointsChapitres.map((pc) => {
                const estSelectionne = noeudActif?.id === pc.noeud.id;
                const matchRecherche = !estFiltre || noeudCorrespond(pc.noeud.id, pc.noeud.titre, pc.noeud.niveau);
                const estSurvole = survolId === pc.noeud.id;
                const estMaitrise = pc.noeud.remplissage >= 1;
                const enCours = pc.noeud.remplissage > 0 && !estMaitrise;

                return (
                  <g
                    key={"noeud-chapitre-" + pc.noeud.id}
                    transform={"translate(" + pc.x + ", " + pc.y + ")"}
                    className="cursor-pointer transition-transform duration-200 hover:scale-125"
                    onClick={() => activeChapitre(pc.noeud, pc.couleur)}
                    onMouseEnter={() => setSurvolId(pc.noeud.id)}
                    onMouseLeave={() => setSurvolId(null)}
                    role="button"
                    tabIndex={0}
                    aria-label={pc.noeud.titre}
                    opacity={matchRecherche ? 1 : 0.15}
                  >
                    {estSelectionne ? (
                      <circle
                        r={12}
                        fill="none"
                        stroke={pc.couleur}
                        className="onde-orbitale pointer-events-none"
                      />
                    ) : null}
                    {estSurvole ? (
                      <circle
                        r={14}
                        fill={pc.couleur}
                        opacity={0.3}
                        filter="url(#lueur-synaptique)"
                        className="pointer-events-none transition-opacity duration-200"
                      />
                    ) : null}
                    <circle
                      r={estSelectionne ? 9 : 6.5}
                      fill={estMaitrise ? pc.couleur : "var(--c-surface)"}
                      stroke={pc.couleur}
                      strokeWidth={estSelectionne ? 2.5 : 1.5}
                      className="transition-all duration-200"
                    />
                    {enCours ? (
                      <circle r={3} fill={pc.couleur} opacity={0.9} />
                    ) : null}
                    {estSelectionne || estSurvole ? (
                      <text
                        x={pc.x >= layout.cx ? 12 : -12}
                        y={3}
                        textAnchor={pc.x >= layout.cx ? "start" : "end"}
                        fontSize="10"
                        fontWeight="600"
                        fill="var(--c-encre)"
                        className="pointer-events-none drop-shadow-sm font-sans"
                      >
                        {pc.noeud.titre}
                      </text>
                    ) : null}
                  </g>
                );
              })}
            </g>
          </svg>
        ) : (
          /* VUE 2 : ARBORESCENCE & SKILL TREE INTERACTIF (Linear / Holi Organigram) */
          <div className="w-full h-full overflow-auto p-6 flex flex-col gap-6">
            {monde.regions.map((reg) => {
              const branchesDom = monde.branches.filter((b) => b.domaine === reg.cle);
              const couleur = accentDuRang(reg.rang);

              return (
                <CarteMagnetique
                  key={reg.cle}
                  intensite={2.2}
                  lueurCouleur={couleur}
                  classe="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] p-5 shadow-sm transition hover:border-[var(--c-domaine)]"
                  style={{ "--c-domaine": couleur } as CSSProperties}
                >
                  <div className="flex items-center justify-between pb-3 border-b border-[var(--c-bordure-subtile)]">
                    <div className="flex items-center gap-3">
                      <div
                        className="w-9 h-9 rounded-xl flex items-center justify-center text-[var(--c-domaine)]"
                        style={{ background: "color-mix(in srgb, var(--c-domaine) 15%, transparent)" }}
                      >
                        <Glyphe rang={reg.rang} taille={20} />
                      </div>
                      <div>
                        <h3 className="font-titre text-base text-[var(--c-encre)]">{reg.titre}</h3>
                        <p className="text-xs text-[var(--c-encre-2)]">
                          {branchesDom.length} branches · {reg.cartesTotales} {LIB.cartesDisponibles} · {pourcent(reg.remplissage)}
                        </p>
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => activeDomaine(reg.cle, reg.rang - 1)}
                      className="text-xs px-3 py-1 rounded-full border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] text-[var(--c-encre)] hover:border-[var(--c-domaine)] transition"
                    >
                      Détails
                    </button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5 mt-4">
                    {branchesDom.map((br) => {
                      const chapitres = monde.noeuds.filter((n) => n.branche === br.cle);

                      return (
                        <div
                          key={br.cle}
                          className="rounded-xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] p-3.5 flex flex-col gap-2.5"
                        >
                          <div className="flex items-center justify-between text-xs font-semibold text-[var(--c-encre)]">
                            <span className="flex items-center gap-1.5 truncate">
                              <span className="w-2 h-2 rounded-full" style={{ background: "var(--c-domaine)" }} />
                              {br.titre}
                            </span>
                            <span className="font-mono text-[11px] text-[var(--c-encre-2)] px-1.5 py-0.5 rounded bg-[var(--c-surface)] border border-[var(--c-bordure-subtile)]">
                              {chapitres.length}
                            </span>
                          </div>

                          <div className="flex flex-col gap-1.5">
                            {chapitres.map((ch) => {
                              const estActif = noeudActif?.id === ch.id;
                              const estMaitrise = ch.remplissage >= 1;

                              return (
                                <button
                                  key={ch.id}
                                  type="button"
                                  onClick={() => activeChapitre(ch, couleur)}
                                  className={"flex items-center justify-between p-2 rounded-lg text-left text-xs transition border " + (estActif ? "border-[var(--c-domaine)] bg-[var(--c-surface)] shadow-sm" : "border-transparent bg-[var(--c-surface)] hover:border-[var(--c-bordure-subtile)]")}
                                >
                                  <div className="flex items-center gap-2 truncate">
                                    <span className={"w-4 h-4 rounded-full text-[9px] font-mono flex items-center justify-center border " + (estMaitrise ? "bg-[var(--c-domaine)] text-[var(--c-fond)] border-transparent" : "bg-[var(--c-surface-creuse)] border-[var(--c-bordure-subtile)] text-[var(--c-encre-2)]")}>
                                      {ch.niveau}
                                    </span>
                                    <span className="truncate text-[var(--c-encre)]">{ch.titre}</span>
                                  </div>
                                  <span className="text-[10px] font-mono text-[var(--c-encre-2)] ml-2 flex-shrink-0">
                                    {Math.round(ch.remplissage * 100)}%
                                  </span>
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </CarteMagnetique>
              );
            })}
          </div>
        )}

        {/* FICHE INSPECTEUR FLOTTANTE (Linear Style) */}
        {noeudActif ? (
          <div
            key={noeudActif.id}
            className="salle-retour absolute bottom-4 left-4 max-w-sm w-[calc(100%-32px)] md:w-80 rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] p-4 shadow-xl backdrop-blur-md z-10"
          >
            <div className="flex items-start justify-between gap-2 mb-2">
              <span className="text-[10px] uppercase font-mono tracking-wider px-2 py-0.5 rounded-full bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre-2)]">
                {noeudActif.type}
              </span>
              <button
                type="button"
                onClick={() => setNoeudActif(null)}
                className="text-[var(--c-encre-2)] hover:text-[var(--c-encre)] p-1 rounded-md"
                aria-label="Fermer la fiche d inspection"
              >
                <X size={14} />
              </button>
            </div>

            <h4 className="font-titre text-base text-[var(--c-encre)] leading-snug">
              {noeudActif.titre}
            </h4>

            <div className="flex items-center justify-between my-3 py-2 border-y border-[var(--c-bordure-subtile)] text-xs text-[var(--c-encre-2)]">
              <div className="flex items-center gap-2">
                <AnneauProgression proportion={noeudActif.remplissage ?? 0} taille={28} />
                <span>{noeudActif.etat && (noeudActif.etat in ETATS_NOEUD) ? ETATS_NOEUD[noeudActif.etat as keyof typeof ETATS_NOEUD] : "Progression"}</span>
              </div>
              <span className="font-mono font-semibold text-[var(--c-encre)]">
                {noeudActif.remplissage !== undefined ? pourcent(noeudActif.remplissage) : "0 %"}
              </span>
            </div>

            {noeudActif.prerequis && noeudActif.prerequis.length > 0 ? (
              <div className="flex items-center gap-1.5 text-[11px] text-[var(--c-encre-2)] mb-2">
                <Lock size={12} className="text-[var(--c-encre-2)] flex-shrink-0" />
                <span>{noeudActif.prerequis.length} prérequis</span>
              </div>
            ) : null}

            {noeudActif.cartesTotales !== undefined ? (
              <p className="text-xs text-[var(--c-encre-2)] mb-3">
                {noeudActif.cartesTotales} {LIB.cartesDisponibles} {noeudActif.cartesAcquises !== undefined ? "(" + noeudActif.cartesAcquises + " acquises)" : ""}
              </p>
            ) : null}

            {/* Actions selon le type */}
            <div className="flex flex-col gap-1.5 pt-1">
              {noeudActif.type === "chapitre" ? (
                <>
                  <button
                    type="button"
                    onClick={() => va("/noeud/" + (noeudActif.parentDomaine ?? "") + "/" + noeudActif.id)}
                    className="bouton-tactile flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-[var(--c-encre)] text-[var(--c-fond)] text-xs font-semibold hover:opacity-90 transition"
                  >
                    Consulter la fiche
                    <ArrowRight size={14} />
                  </button>
                  <button
                    type="button"
                    onClick={() => va("/salle/seance/chapitre:" + noeudActif.id)}
                    className="bouton-tactile flex items-center justify-center gap-1.5 py-1.5 px-3 rounded-xl bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre)] text-xs font-medium hover:border-[var(--c-encre)] transition"
                  >
                    <Play size={13} />
                    Réviser ce chapitre
                  </button>
                </>
              ) : noeudActif.type === "domaine" ? (
                <button
                  type="button"
                  onClick={() => va("/domaine/" + noeudActif.id)}
                  className="bouton-tactile flex items-center justify-center gap-1.5 py-2 px-3 rounded-xl bg-[var(--c-encre)] text-[var(--c-fond)] text-xs font-semibold hover:opacity-90 transition"
                >
                  Ouvrir le domaine
                  <ArrowRight size={14} />
                </button>
              ) : null}
            </div>
          </div>
        ) : null}

        {/* MENU GOOEY LIQUIDE EN COIN INFERIEUR DROIT */}
        <div className="absolute bottom-6 right-6 z-20">
          <Liquid blur={5} contrast={13} fill="var(--c-surface-dock)">
            <Liquid.Item
              x={menuGooeyOuvert ? -52 : 0}
              y={0}
              transition={{ duration: 500, ease: "cubic-bezier(0.34, 1.56, 0.64, 1)" }}
            >
              <button
                type="button"
                onClick={recentrerVue}
                className="w-10 h-10 rounded-full flex items-center justify-center bg-[var(--c-surface-elevee)] text-[var(--c-encre)] border border-[var(--c-bordure-subtile)] shadow-md hover:scale-105 transition"
                title="Recentrer la vue"
                aria-label="Recentrer la vue"
              >
                <RotateCcw size={16} />
              </button>
            </Liquid.Item>

            <Liquid.Item
              x={menuGooeyOuvert ? -38 : 0}
              y={menuGooeyOuvert ? -38 : 0}
              delay={30}
              transition={{ duration: 500, ease: "cubic-bezier(0.34, 1.56, 0.64, 1)" }}
            >
              <button
                type="button"
                onClick={() => setVueMode(vueMode === "radial" ? "arborescence" : "radial")}
                className="w-10 h-10 rounded-full flex items-center justify-center bg-[var(--c-surface-elevee)] text-[var(--c-encre)] border border-[var(--c-bordure-subtile)] shadow-md hover:scale-105 transition"
                title="Basculer le mode d affichage"
                aria-label="Basculer le mode d affichage"
              >
                <Layers size={16} />
              </button>
            </Liquid.Item>

            <Liquid.Item
              x={0}
              y={menuGooeyOuvert ? -52 : 0}
              delay={60}
              transition={{ duration: 500, ease: "cubic-bezier(0.34, 1.56, 0.64, 1)" }}
            >
              <button
                type="button"
                onClick={() => va("/salle/seance/hasard")}
                className="w-10 h-10 rounded-full flex items-center justify-center bg-[var(--c-surface-elevee)] text-[var(--c-accent)] border border-[var(--c-bordure-subtile)] shadow-md hover:scale-105 transition"
                title="Séance au hasard"
                aria-label="Séance au hasard"
              >
                <Sparkles size={16} />
              </button>
            </Liquid.Item>

            <Liquid.Item>
              <button
                type="button"
                onClick={() => setMenuGooeyOuvert(!menuGooeyOuvert)}
                className="w-12 h-12 rounded-full flex items-center justify-center bg-[var(--c-encre)] text-[var(--c-fond)] shadow-lg hover:scale-105 transition active:scale-95"
                aria-label="Menu d actions rapides"
              >
                <span className={"text-lg font-bold transition-transform duration-300 " + (menuGooeyOuvert ? "rotate-45" : "")}>
                  +
                </span>
              </button>
            </Liquid.Item>
          </Liquid>
        </div>
      </div>
    </div>
  );
}

/**
 * Composant GrapheMindmap : visualisation arborescente en Mind Map d un domaine
 * avec connexions et noeuds (inspire des maquettes Mind Map et Organigramme).
 */
export function GrapheMindmap({
  region,
  branches,
  noeuds,
  classe = "",
}: {
  region: Region;
  branches: Branche[];
  noeuds: Noeud[];
  classe?: string;
}) {
  const [brancheActive, setBrancheActive] = useState<string | null>(branches[0]?.cle ?? null);
  const branchesAffichees = branches.slice(0, 6);
  const couleurDomaine = accentDuRang(region.rang);

  return (
    <div
      className={"graphe-mindmap relative flex flex-col gap-4 p-5 rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] shadow-sm " + classe}
      style={{ "--c-domaine": couleurDomaine } as CSSProperties}
    >
      <div className="flex items-center justify-between border-b border-[var(--c-bordure-subtile)] pb-3">
        <div className="flex items-center gap-2.5">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center text-[var(--c-domaine)]"
            style={{ background: "color-mix(in srgb, var(--c-domaine) 15%, transparent)" }}
            aria-hidden="true"
          >
            <Glyphe rang={region.rang} taille={18} />
          </div>
          <div>
            <span className="text-xs uppercase font-semibold tracking-wider text-[var(--c-encre-2)]">
              {LIB.arbre} · {region.titre}
            </span>
            <p className="text-xs text-[var(--c-encre-2)]">
              {branches.length} branches · {noeuds.filter(n => !n.satellite).length} chapitres du socle · {noeuds.filter(n => n.satellite).length} approfondissements
            </p>
          </div>
        </div>
        <span className="text-[11px] font-mono text-[var(--c-encre-2)] px-2 py-0.5 rounded-full bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)]">
          {LIB.arbre}
        </span>
      </div>

      <div className="relative min-h-[220px] flex flex-col gap-2.5 py-1">
        {branchesAffichees.map((b) => {
          const chapitresBranche = noeuds.filter((n) => n.branche === b.cle);
          const estActive = brancheActive === b.cle;

          return (
            <div
              key={b.cle}
              className="mindmap-branche flex flex-col gap-2 p-3 rounded-xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] transition duration-150 hover:border-[var(--c-domaine)]"
            >
              <button
                type="button"
                onClick={() => setBrancheActive(estActive ? null : b.cle)}
                className="flex items-center justify-between text-left w-full gap-2 text-xs font-semibold text-[var(--c-encre)]"
              >
                <span className="flex items-center gap-2">
                  <span
                    className="w-2 h-2 rounded-full"
                    style={{ background: "var(--c-domaine)" }}
                    aria-hidden="true"
                  />
                  {b.titre}
                </span>
                <span className="text-[11px] font-normal text-[var(--c-encre-2)] px-2 py-0.5 rounded-full bg-[var(--c-surface)] border border-[var(--c-bordure-subtile)]">
                  {chapitresBranche.length}
                </span>
              </button>

              {estActive && chapitresBranche.length > 0 ? (
                <div className="mindmap-feuilles flex flex-wrap gap-1.5 pt-2 border-t border-[var(--c-bordure-subtile)] pl-4">
                  {chapitresBranche.map((ch) => (
                    <button
                      key={ch.id}
                      type="button"
                      onClick={() => va("/noeud/" + region.cle + "/" + ch.id)}
                      className="mindmap-noeud inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[11px] bg-[var(--c-surface)] border border-[var(--c-bordure-subtile)] hover:border-[var(--c-domaine)] hover:text-[var(--c-domaine)] transition text-[var(--c-encre)]"
                    >
                      <span className="w-3.5 h-3.5 rounded-full bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] text-[9px] font-mono flex items-center justify-center">
                        {ch.niveau}
                      </span>
                      <span className="truncate max-w-[180px]">{ch.titre}</span>
                    </button>
                  ))}
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}

/**
 * Composant GrapheRadial : vue dendrogramme radial des domaines de competences
 * (inspire de la maquette dendrogramme radial).
 */
export function GrapheRadial({
  regions,
  selection,
  surSelection,
}: {
  regions: Region[];
  selection: number;
  surSelection: (index: number) => void;
}) {
  const taille = 380;
  const centre = taille / 2;
  const rayonInterne = 44;
  const rayonExterne = 135;

  const points = useMemo(() => {
    const n = regions.length;
    return regions.map((r, i) => {
      const angle = (i * (2 * Math.PI)) / n - Math.PI / 2;
      const x = centre + rayonExterne * Math.cos(angle);
      const y = centre + rayonExterne * Math.sin(angle);
      const xInterne = centre + rayonInterne * Math.cos(angle);
      const yInterne = centre + rayonInterne * Math.sin(angle);
      const bezierCx = centre + ((rayonInterne + rayonExterne) / 2) * Math.cos(angle + 0.12);
      const bezierCy = centre + ((rayonInterne + rayonExterne) / 2) * Math.sin(angle + 0.12);

      return {
        index: i,
        region: r,
        x,
        y,
        xInterne,
        yInterne,
        dBezier: "M " + xInterne + " " + yInterne + " Q " + bezierCx + " " + bezierCy + " " + x + " " + y,
        couleur: accentDuRang(r.rang),
      };
    });
  }, [regions, centre, rayonExterne, rayonInterne]);

  return (
    <div className="graphe-radial relative flex flex-col items-center justify-center p-4 rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] shadow-sm">
      <svg
        viewBox={"0 0 " + taille + " " + taille}
        className="w-full max-w-[380px] aspect-square"
        role="img"
        aria-label="Graphe radial des domaines"
      >
        <circle cx={centre} cy={centre} r={rayonInterne} fill="none" stroke="var(--c-trait)" strokeWidth={1} strokeDasharray="3 3" />
        <circle cx={centre} cy={centre} r={rayonExterne} fill="none" stroke="var(--c-trait)" strokeWidth={1} opacity={0.3} />

        {points.map((p) => {
          const estActif = p.index === selection;
          return (
            <path
              key={p.region.cle}
              d={p.dBezier}
              fill="none"
              stroke={estActif ? p.couleur : "var(--c-trait)"}
              strokeWidth={estActif ? 2.5 : 1.2}
              opacity={estActif ? 0.9 : 0.45}
              className="transition-all duration-300"
            />
          );
        })}

        <g transform={"translate(" + centre + ", " + centre + ")"}>
          <circle r={24} fill="var(--c-surface-elevee)" stroke="var(--c-bordure-forte)" strokeWidth={1.5} />
          <circle r={18} fill="var(--c-accent)" opacity={0.12} />
          <text
            textAnchor="middle"
            dominantBaseline="central"
            fontSize="9"
            fontWeight="600"
            fill="var(--c-encre)"
            fontFamily="var(--f-titre)"
          >
            Métier
          </text>
        </g>

        {points.map((p) => {
          const estActif = p.index === selection;
          return (
            <g
              key={p.region.cle}
              transform={"translate(" + p.x + ", " + p.y + ")"}
              className="cursor-pointer transition-transform duration-200 hover:scale-110"
              onClick={() => surSelection(p.index)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === "Enter" && surSelection(p.index)}
              aria-label={p.region.titre}
            >
              <circle
                r={estActif ? 14 : 10}
                fill="var(--c-surface)"
                stroke={p.couleur}
                strokeWidth={estActif ? 2.5 : 1.5}
                className="transition-all duration-200"
              />
              <circle r={estActif ? 7 : 5} fill={p.couleur} />
            </g>
          );
        })}
      </svg>

      <div className="mt-2 text-center">
        <p className="font-semibold text-sm text-[var(--c-encre)]">
          {regions[selection]?.titre}
        </p>
        <p className="text-xs text-[var(--c-encre-2)]">
          {regions[selection]?.cartesTotales ? regions[selection]?.cartesTotales + " " + LIB.cartesDisponibles : "Au programme"}
        </p>
      </div>
    </div>
  );
}

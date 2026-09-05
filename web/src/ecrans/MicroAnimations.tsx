import { useEffect, useMemo, useRef, useState, type CSSProperties, type MouseEvent, type ReactNode } from "react";

/**
 * Composant NombreAnime : decoupage des chiffres avec animation pop-in
 * et decalage physique (Transitions.dev - Number pop-in).
 */
export function NombreAnime({
  valeur,
  unite,
  classe = "",
}: {
  valeur: number | string;
  unite?: string;
  classe?: string;
}) {
  const [animant, setAnimant] = useState(true);
  const refGroupe = useRef<HTMLSpanElement>(null);
  const chaine = String(valeur);

  useEffect(() => {
    setAnimant(false);
    const rAF = requestAnimationFrame(() => {
      // Force un reflow avant de re-armer l'animation
      if (refGroupe.current) void refGroupe.current.offsetWidth;
      setAnimant(true);
    });
    return () => cancelAnimationFrame(rAF);
  }, [valeur]);

  return (
    <span
      ref={refGroupe}
      className={`t-digit-group ${animant ? "is-animating" : ""} ${classe}`}
      aria-label={`${chaine}${unite ? ` ${unite}` : ""}`}
    >
      {chaine.split("").map((caractere, index) => (
        <span
          key={`${index}-${caractere}`}
          className="t-digit"
          data-stagger={index > 0 ? Math.min(index, 5) : undefined}
          aria-hidden="true"
        >
          {caractere}
        </span>
      ))}
      {unite ? (
        <span className="ml-1 text-sm font-normal text-encre-2" aria-hidden="true">
          {unite}
        </span>
      ) : null}
    </span>
  );
}

/**
 * Composant OngletsGlissants : barre d'onglets avec pilule coulissante
 * (Transitions.dev - Tabs sliding).
 * La pilule mesure le decalage et la largeur de l'onglet actif.
 */
export interface OptionOnglet {
  id: string;
  libelle: string;
  badge?: string | number;
}

export function OngletsGlissants({
  onglets,
  actif,
  surSelection,
  ariaLabel,
}: {
  onglets: OptionOnglet[];
  actif: string;
  surSelection: (id: string) => void;
  ariaLabel?: string;
}) {
  const refBarre = useRef<HTMLDivElement>(null);
  const refPilule = useRef<HTMLSpanElement>(null);
  const premierRendu = useRef(true);

  useEffect(() => {
    const barre = refBarre.current;
    const pilule = refPilule.current;
    if (!barre || !pilule) return;

    const boutonActif = barre.querySelector<HTMLButtonElement>(
      `button[data-id="${actif}"]`,
    );
    if (!boutonActif) return;

    const gauche = boutonActif.offsetLeft;
    const largeur = boutonActif.offsetWidth;

    if (premierRendu.current) {
      // Premier affichage : positionnement instantane sans animation
      pilule.style.transition = "none";
      pilule.style.transform = `translateX(${gauche}px)`;
      pilule.style.width = `${largeur}px`;
      void pilule.offsetWidth; // Force reflow
      pilule.style.transition = "";
      premierRendu.current = false;
    } else {
      pilule.style.transform = `translateX(${gauche}px)`;
      pilule.style.width = `${largeur}px`;
    }
  }, [actif, onglets]);

  // Re-mesure lors du redimensionnement de la fenetre
  useEffect(() => {
    function redimensionne() {
      const barre = refBarre.current;
      const pilule = refPilule.current;
      if (!barre || !pilule) return;
      const boutonActif = barre.querySelector<HTMLButtonElement>(
        `button[data-id="${actif}"]`,
      );
      if (!boutonActif) return;
      pilule.style.transition = "none";
      pilule.style.transform = `translateX(${boutonActif.offsetLeft}px)`;
      pilule.style.width = `${boutonActif.offsetWidth}px`;
      void pilule.offsetWidth;
      pilule.style.transition = "";
    }
    window.addEventListener("resize", redimensionne);
    return () => window.removeEventListener("resize", redimensionne);
  }, [actif]);

  return (
    <div
      ref={refBarre}
      className="t-tabs"
      role="tablist"
      aria-label={ariaLabel}
    >
      <span ref={refPilule} className="t-tabs-pill" aria-hidden="true" />
      {onglets.map((onglet) => {
        const estActif = onglet.id === actif;
        return (
          <button
            key={onglet.id}
            data-id={onglet.id}
            type="button"
            role="tab"
            aria-selected={estActif}
            className="t-tab"
            onClick={() => surSelection(onglet.id)}
          >
            <span>{onglet.libelle}</span>
            {onglet.badge !== undefined ? (
              <span className="ml-1.5 rounded-full bg-trait px-1.5 py-0.5 text-xs text-encre-2">
                {onglet.badge}
              </span>
            ) : null}
          </button>
        );
      })}
    </div>
  );
}

/**
 * Composant VoletGlissant : panneau avec glissement vertical et flou
 * synchronise (Transitions.dev - Panel reveal).
 */
export function VoletGlissant({
  ouvert,
  enfants,
  children,
  classe = "",
}: {
  ouvert: boolean;
  enfants?: ReactNode;
  children?: ReactNode;
  classe?: string;
}) {
  return (
    <div
      className={`t-panel-slide ${classe}`}
      data-open={ouvert ? "true" : "false"}
    >
      {enfants ?? children}
    </div>
  );
}

/**
 * Composant EtatPenseur : texte avec balayage shimmer
 * (Transitions.dev - Thinking states).
 */
export function EtatPenseur({
  texte,
  textePlusLong,
  classe = "",
}: {
  texte: string;
  textePlusLong?: string;
  classe?: string;
}) {
  const gabarit = textePlusLong ?? texte;
  return (
    <span className={`t-think ${classe}`} role="status">
      <span className="t-think-sizer" aria-hidden="true">
        {gabarit}
      </span>
      <span className="t-think-text" data-text={texte}>
        {texte}
      </span>
    </span>
  );
}

/**
 * Composant AnneauProgression : jauge circulaire SVG precise
 * inspiree des maquettes Dribbble / Linear.
 */
export function AnneauProgression({
  proportion,
  taille = 64,
  epaisseur = 4,
  couleur,
  enfants,
  children,
  classe = "",
}: {
  proportion: number;
  taille?: number;
  epaisseur?: number;
  couleur?: string;
  enfants?: ReactNode;
  children?: ReactNode;
  classe?: string;
}) {
  const p = Math.max(0, Math.min(1, proportion));
  const rayon = (taille - epaisseur) / 2;
  const circonference = 2 * Math.PI * rayon;
  const decalage = circonference * (1 - p);
  const contenu = enfants ?? children;

  return (
    <div
      className={`relative inline-flex items-center justify-center ${classe}`}
      style={{ width: taille, height: taille }}
      role="progressbar"
      aria-valuenow={Math.round(p * 100)}
      aria-valuemin={0}
      aria-valuemax={100}
    >
      <svg
        width={taille}
        height={taille}
        viewBox={`0 0 ${taille} ${taille}`}
        className="absolute inset-0 -rotate-90"
        aria-hidden="true"
      >
        <circle
          cx={taille / 2}
          cy={taille / 2}
          r={rayon}
          fill="none"
          stroke="var(--c-trait)"
          strokeWidth={epaisseur}
          opacity={0.35}
        />
        <circle
          cx={taille / 2}
          cy={taille / 2}
          r={rayon}
          fill="none"
          stroke={couleur ?? "var(--c-accent)"}
          strokeWidth={epaisseur}
          strokeDasharray={circonference}
          strokeDashoffset={decalage}
          strokeLinecap="round"
          style={{
            transition: "stroke-dashoffset var(--d-conquete) var(--e-mouvement)",
          }}
        />
      </svg>
      {contenu ? (
        <div className="relative z-10 flex items-center justify-center">
          {contenu}
        </div>
      ) : null}
    </div>
  );
}

/**
 * Composant Liquid / Liquide : effet gooey organique base sur un filtre SVG
 * (feGaussianBlur + feColorMatrix + feComposite) avec transitions physiques elastiques.
 * Compatible avec l'API de `liquid-gooey`.
 */
export interface LiquidProps {
  blur?: number;
  contrast?: number;
  fill?: string;
  id?: string;
  className?: string;
  classe?: string;
  children?: ReactNode;
  enfants?: ReactNode;
}

export interface LiquidItemProps {
  x?: number;
  y?: number;
  scale?: number;
  delay?: number;
  transition?: {
    duration?: number;
    ease?: string;
  };
  className?: string;
  classe?: string;
  children?: ReactNode;
  enfants?: ReactNode;
}

export function Liquid({
  blur = 5,
  contrast = 13,
  fill,
  id = "filtre-liquide-gooey",
  className = "",
  classe = "",
  children,
  enfants,
}: LiquidProps) {
  const contenu = enfants ?? children;
  const classeFinale = className || classe;

  return (
    <div
      className={`relative inline-flex items-center justify-center ${classeFinale}`}
      style={{
        filter: `url(#${id})`,
      }}
    >
      <svg
        className="absolute pointer-events-none"
        style={{ width: 0, height: 0, position: "absolute" }}
        aria-hidden="true"
      >
        <defs>
          <filter id={id} x="-50%" y="-50%" width="200%" height="200%" colorInterpolationFilters="sRGB">
            <feGaussianBlur in="SourceGraphic" stdDeviation={blur} result="blur" />
            <feColorMatrix
              in="blur"
              type="matrix"
              values={`1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 ${contrast * 2} -${contrast}`}
              result="goo"
            />
            <feComposite in="SourceGraphic" in2="goo" operator="atop" />
          </filter>
        </defs>
      </svg>
      <div style={{ color: fill }}>{contenu}</div>
    </div>
  );
}

function LiquidItem({
  x = 0,
  y = 0,
  scale = 1,
  delay = 0,
  transition,
  className = "",
  classe = "",
  children,
  enfants,
}: LiquidItemProps) {
  const contenu = enfants ?? children;
  const duree = transition?.duration ?? 550;
  const courbe = transition?.ease ?? "cubic-bezier(0.34, 1.56, 0.64, 1)";
  const classeFinale = className || classe;

  return (
    <div
      className={`absolute ${classeFinale}`}
      style={{
        transform: `translate3d(${x}px, ${y}px, 0) scale(${scale})`,
        transition: `transform ${duree}ms ${courbe} ${delay}ms`,
        willChange: "transform",
      }}
    >
      {contenu}
    </div>
  );
}

Liquid.Item = LiquidItem;

// Alias francophone
export const Liquide = Liquid;

/**
 * Composant EclatParticules : explosion festive de micro-particules physiques
 * (confetti dopamine) avec dispersion angulaire, gravité et rotation.
 */
export interface EclatParticulesProps {
  actif?: boolean;
  nombre?: number;
  duree?: number;
  taille?: number;
  couleurs?: string[];
  classe?: string;
  onFin?: () => void;
}

export function EclatParticules({
  actif = true,
  nombre = 24,
  duree = 700,
  couleurs = ["var(--c-accent)", "var(--c-succes)", "var(--c-encre)", "var(--c-avertissement)"],
  classe = "",
  onFin,
}: EclatParticulesProps) {
  const [visible, setVisible] = useState(actif);

  useEffect(() => {
    if (!actif) {
      setVisible(false);
      return;
    }
    setVisible(true);
    const t = setTimeout(() => {
      setVisible(false);
      onFin?.();
    }, duree);
    return () => clearTimeout(t);
  }, [actif, duree, onFin]);

  const particules = useMemo(() => {
    return Array.from({ length: nombre }).map((_, i) => {
      const angle = (i / nombre) * 2 * Math.PI + (Math.random() - 0.5) * 0.4;
      const distance = 45 + Math.random() * 80;
      const vx = Math.cos(angle) * distance;
      const vy = Math.sin(angle) * distance;
      const rot = (Math.random() - 0.5) * 450;
      const couleur = couleurs[i % couleurs.length] ?? "var(--c-accent)";
      const tailleParticule = 4 + Math.random() * 4;
      const estCercle = i % 2 === 0;

      return {
        id: i,
        vx,
        vy,
        rot,
        couleur,
        taille: tailleParticule,
        estCercle,
      };
    });
  }, [nombre, couleurs]);

  if (!visible) return null;

  return (
    <div
      className={`pointer-events-none absolute inset-0 z-30 overflow-visible ${classe}`}
      aria-hidden="true"
    >
      {particules.map((p) => (
        <span
          key={p.id}
          className="absolute left-1/2 top-1/2"
          style={{
            width: `${p.taille}px`,
            height: `${p.taille}px`,
            marginLeft: `-${p.taille / 2}px`,
            marginTop: `-${p.taille / 2}px`,
            backgroundColor: p.couleur,
            borderRadius: p.estCercle ? "50%" : "1px",
            ["--p-vx" as string]: `${p.vx}px`,
            ["--p-vy" as string]: `${p.vy}px`,
            ["--p-rot" as string]: `${p.rot}deg`,
            animation: `eclat-particule ${duree}ms cubic-bezier(0.16, 1, 0.3, 1) both`,
          }}
        />
      ))}
    </div>
  );
}

/**
 * Composant CarteMagnetique : carte interactive avec inclinaison 3D physique (perspective)
 * et halo lumineux suivant la position du curseur (Linear / Apple style).
 */
export function CarteMagnetique({
  children,
  enfants,
  classe = "",
  className = "",
  intensite = 3,
  lueurCouleur = "var(--c-accent)",
  style = {},
  ...props
}: {
  children?: ReactNode;
  enfants?: ReactNode;
  classe?: string;
  className?: string;
  intensite?: number;
  lueurCouleur?: string;
  style?: CSSProperties;
  [cle: string]: unknown;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const [coordLueur, setCoordLueur] = useState<{ x: number; y: number; actif: boolean }>({
    x: 0,
    y: 0,
    actif: false,
  });
  const [rotation, setRotation] = useState({ x: 0, y: 0 });

  const surMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;

    setRotation({
      x: -y * intensite,
      y: x * intensite,
    });
    setCoordLueur({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top,
      actif: true,
    });
  };

  const surMouseLeave = () => {
    setRotation({ x: 0, y: 0 });
    setCoordLueur((c) => ({ ...c, actif: false }));
  };

  const contenu = enfants ?? children;
  const classeFinale = className || classe;

  return (
    <div
      ref={ref}
      onMouseMove={surMouseMove}
      onMouseLeave={surMouseLeave}
      className={`relative transition-transform duration-300 ease-out will-change-transform ${classeFinale}`}
      style={{
        ...style,
        transform: `perspective(800px) rotateX(${rotation.x}deg) rotateY(${rotation.y}deg)`,
      }}
      {...props}
    >
      {contenu}
      {coordLueur.actif ? (
        <div
          className="pointer-events-none absolute inset-0 rounded-[inherit] transition-opacity duration-300"
          style={{
            background: `radial-gradient(350px circle at ${coordLueur.x}px ${coordLueur.y}px, color-mix(in srgb, ${lueurCouleur} 10%, transparent), transparent 80%)`,
          }}
          aria-hidden="true"
        />
      ) : null}
    </div>
  );
}

/**
 * Composant BordureLumineuse : faisceau lumineux circulant le long
 * du périmètre de la carte (Border Beam).
 */
export function BordureLumineuse({
  children,
  enfants,
  classe = "",
  className = "",
  couleur = "var(--c-accent)",
  duree = 4,
}: {
  children?: ReactNode;
  enfants?: ReactNode;
  classe?: string;
  className?: string;
  couleur?: string;
  duree?: number;
}) {
  const contenu = enfants ?? children;
  const classeFinale = className || classe;

  return (
    <div className={`relative overflow-hidden rounded-[inherit] ${classeFinale}`}>
      {contenu}
      <svg
        className="pointer-events-none absolute inset-0 h-full w-full rounded-[inherit]"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <rect
          width="100%"
          height="100%"
          rx="16"
          fill="none"
          stroke={couleur}
          strokeWidth="1.5"
          strokeDasharray="60 140"
          style={{
            animation: `rayon-bordure ${duree}s linear infinite`,
            opacity: 0.85,
          }}
        />
      </svg>
    </div>
  );
}


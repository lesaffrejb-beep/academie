import {
  Scale, Layers, Cog, ChartNoAxesCombined, Shield, Landmark,
  Ruler, Leaf, Map, Handshake, BookOpen, type LucideIcon,
} from "lucide-react";

const GLYPHES: LucideIcon[] = [Scale, Layers, Cog, ChartNoAxesCombined,
  Shield, Landmark, Ruler, Leaf, Map, Handshake, BookOpen];

export function Glyphe({ rang, taille = 24 }: { rang: number; taille?: number }) {
  const Icone = GLYPHES[(Math.max(1, rang) - 1) % GLYPHES.length]!;
  return <Icone size={taille} strokeWidth={1.4} aria-hidden="true" />;
}

export function Anneau({ part, taille = 64 }: { part: number; taille?: number }) {
  const valeur = Math.min(1, Math.max(0, part));
  return <svg className="anneau" width={taille} height={taille} viewBox="0 0 64 64" aria-hidden="true">
    <circle className="anneau-fond" cx="32" cy="32" r="29" />
    <circle className="anneau-valeur" cx="32" cy="32" r="29" pathLength="100"
      strokeDasharray={`${valeur * 100} 100`} transform="rotate(-90 32 32)" />
  </svg>;
}

import { useState, useMemo, type ChangeEvent } from "react";
import {
  Check,
  Copy,
  HelpCircle,
  Link2,
  RotateCcw,
  Sparkles,
  Target,
  User,
  ZoomIn,
  ZoomOut,
  X,
} from "lucide-react";
import type { Carte } from "../donnees/types";
import { LIB } from "../app/i18n";

/**
 * 1. MODULE JEU DE ROLE & MISE EN SITUATION (type: "role")
 * Extrait le prompt de dialogue et l'objectif de négociation,
 * offre un bouton de copie tactile pour jouer le rôle en IA ou en binôme.
 */
export function ModuleRole({
  carte,
  reponse,
  surChangementReponse,
  revele,
}: {
  carte: Carte;
  reponse: string;
  surChangementReponse: (valeur: string) => void;
  revele: boolean;
}) {
  const [copie, setCopie] = useState(false);

  // Extraction du prompt entre guillemets français ou anglais
  const promptExtrait = useMemo(() => {
    const match = carte.question.match(/«([^»]+)»/) || carte.question.match(/"([^"]+)"/);
    return match && match[1] ? match[1].trim() : "";
  }, [carte.question]);

  // Extraction de l'interlocuteur
  const interlocuteur = useMemo(() => {
    if (promptExtrait) {
      const match = promptExtrait.match(/^Tu es ([^.]+)\./i);
      if (match && match[1]) return match[1].trim();
    }
    return "Interlocuteur de simulation";
  }, [promptExtrait]);

  // Extraction de l'objectif
  const objectif = useMemo(() => {
    const match = carte.question.match(/Objectif\s*:\s*([^.]+)/i);
    return match && match[1] ? match[1].trim() : "";
  }, [carte.question]);

  const copierPrompt = async () => {
    const texteACopier = promptExtrait || carte.question;
    try {
      await navigator.clipboard.writeText(texteACopier);
      setCopie(true);
      setTimeout(() => setCopie(false), 2200);
    } catch {
      // Fallback si presse-papier restreint
      setCopie(true);
      setTimeout(() => setCopie(false), 1500);
    }
  };

  return (
    <div className="module-role flex flex-col gap-4">
      {/* Carte Scénario Interlocuteur */}
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] p-4 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-[var(--c-bordure-subtile)]">
          <div className="flex items-center gap-2">
            <span className="w-8 h-8 rounded-full flex items-center justify-center bg-[var(--c-accent-fond)] text-[var(--c-accent)]">
              <User size={16} />
            </span>
            <div>
              <span className="text-[10px] font-mono uppercase tracking-wider text-[var(--c-encre-2)]">
                Interlocuteur
              </span>
              <p className="text-xs font-semibold text-[var(--c-encre)] capitalize">
                {interlocuteur}
              </p>
            </div>
          </div>
          {objectif ? (
            <span className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1 rounded-full bg-[var(--c-surface-creuse)] text-[var(--c-encre)] border border-[var(--c-bordure-subtile)] font-medium">
              <Target size={12} className="text-[var(--c-accent)]" />
              <span>Négociation</span>
            </span>
          ) : null}
        </div>

        {/* Encadré d'objectif */}
        {objectif ? (
          <div className="my-3 p-3 rounded-xl bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] text-xs text-[var(--c-encre)]">
            <strong className="text-[var(--c-accent)]">Objectif clé : </strong>
            <span>{objectif}.</span>
          </div>
        ) : null}

        {/* Bloc du prompt prêt à copier */}
        {promptExtrait ? (
          <div className="relative mt-2 p-3.5 rounded-xl border border-[var(--c-trait)] bg-[var(--c-surface-elevee)] text-xs text-[var(--c-encre)] font-sans italic">
            <p className="pr-24">« {promptExtrait} »</p>
            <button
              type="button"
              onClick={copierPrompt}
              className="bouton-tactile absolute top-3 right-3 inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-[var(--c-accent)] text-[var(--c-sur-accent)] text-[11px] font-medium shadow-sm transition"
              title="Copier le prompt pour simulateur IA ou binôme"
            >
              {copie ? <Check size={13} /> : <Copy size={13} />}
              <span>{copie ? "Copié !" : "Copier"}</span>
            </button>
          </div>
        ) : null}
      </div>

      {/* Saisie de la stratégie et des notes */}
      <div className="salle-reponse-libre">
        <label htmlFor="reponse-carte" className="text-xs font-semibold text-[var(--c-encre)]">
          {LIB.taReponse}
        </label>
        <textarea
          id="reponse-carte"
          rows={4}
          value={reponse}
          readOnly={revele}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => surChangementReponse(e.target.value)}
          placeholder="Note ici ta stratégie, tes questions au prestataire et les points non négociables..."
        />
      </div>
    </div>
  );
}

/**
 * 2. MODULE RELIER (type: "relier")
 * Double colonne interactive pour associer chaque repère technique à son rôle.
 */
export function ModuleRelier({
  carte,
  reponse,
  surChangementReponse,
  revele,
}: {
  carte: Carte;
  reponse: string;
  surChangementReponse: (valeur: string) => void;
  revele: boolean;
}) {
  // Parsing des éléments gauche (1 à 6) et droite (a à f) depuis la question
  const donneesPaires = useMemo(() => {
    if (carte.paires && Array.isArray(carte.paires) && carte.paires.length > 0) {
      return {
        gauches: carte.paires.map((p, i) => ({ id: p.gauche || String(i + 1), label: p.gauche })),
        droites: carte.paires.map((p, i) => ({ id: String.fromCharCode(97 + i), label: p.droite })),
      };
    }

    const itemsDroite: { id: string; label: string }[] = [];
    const regexRoles = /\(([a-f])\)\s*([^;.]+)/gi;
    let m: RegExpExecArray | null;
    while ((m = regexRoles.exec(carte.question)) !== null) {
      if (m[1] && m[2]) {
        itemsDroite.push({ id: m[1].toLowerCase(), label: m[2].trim() });
      }
    }

    const repGauche = Array.from({ length: Math.max(itemsDroite.length, 6) }).map((_, i) => ({
      id: String(i + 1),
      label: `Repère ${i + 1}`,
    }));

    return {
      gauches: repGauche,
      droites: itemsDroite.length > 0 ? itemsDroite : [
        { id: "a", label: "Dépression et aspiration" },
        { id: "b", label: "Amortissement des vibrations" },
        { id: "c", label: "Conversion d énergie électrique" },
        { id: "d", label: "Transmission de couple" },
        { id: "e", label: "Protection et canalisation du rejet" },
        { id: "f", label: "Collecte de l air extrait" },
      ],
    };
  }, [carte.paires, carte.question]);

  const [selectionGauche, setSelectionGauche] = useState<string | null>(null);
  const [liens, setLiens] = useState<Record<string, string>>({});

  const synchroniserReponse = (nouveauxLiens: Record<string, string>) => {
    const chaine = Object.entries(nouveauxLiens)
      .sort(([k1], [k2]) => k1.localeCompare(k2, undefined, { numeric: true }))
      .map(([g, d]) => `${g}-${d}`)
      .join(", ");
    surChangementReponse(chaine);
  };

  const lier = (droiteId: string) => {
    if (!selectionGauche || revele) return;
    const maj = { ...liens, [selectionGauche]: droiteId };
    setLiens(maj);
    setSelectionGauche(null);
    synchroniserReponse(maj);
  };

  const dissocier = (gaucheId: string) => {
    if (revele) return;
    const maj = { ...liens };
    delete maj[gaucheId];
    setLiens(maj);
    synchroniserReponse(maj);
  };

  const reinitialiser = () => {
    if (revele) return;
    setLiens({});
    setSelectionGauche(null);
    surChangementReponse("");
  };

  return (
    <div className="module-relier flex flex-col gap-4">
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] p-4 shadow-sm">
        <div className="flex items-center justify-between pb-3 mb-3 border-b border-[var(--c-bordure-subtile)]">
          <span className="text-xs font-semibold text-[var(--c-encre)] flex items-center gap-1.5">
            <Link2 size={15} className="text-[var(--c-accent)]" />
            <span>Associe chaque repère à son rôle</span>
          </span>
          {Object.keys(liens).length > 0 && !revele ? (
            <button
              type="button"
              onClick={reinitialiser}
              className="text-[11px] text-[var(--c-encre-2)] hover:text-[var(--c-encre)] transition flex items-center gap-1"
            >
              <RotateCcw size={12} />
              <span>Réinitialiser</span>
            </button>
          ) : null}
        </div>

        {/* Double colonne */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex flex-col gap-2">
            <span className="text-[11px] uppercase font-mono tracking-wider text-[var(--c-encre-2)]">
              1. Repères du schéma
            </span>
            <div className="flex flex-wrap gap-2">
              {donneesPaires.gauches.map((g) => {
                const estLie = liens[g.id] !== undefined;
                const estSelectionne = selectionGauche === g.id;

                return (
                  <button
                    key={g.id}
                    type="button"
                    disabled={revele}
                    onClick={() => setSelectionGauche(g.id)}
                    className={
                      "bouton-tactile px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2 border transition " +
                      (estSelectionne
                        ? "border-[var(--c-accent)] bg-[var(--c-accent)] text-[var(--c-sur-accent)] shadow-md"
                        : estLie
                        ? "border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] text-[var(--c-encre)]"
                        : "border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] text-[var(--c-encre)] hover:border-[var(--c-accent)]")
                    }
                  >
                    <span>{g.label}</span>
                    {estLie ? (
                      <span className="w-5 h-5 rounded-full bg-[var(--c-accent)] text-[var(--c-sur-accent)] text-[10px] font-mono flex items-center justify-center">
                        {liens[g.id]}
                      </span>
                    ) : null}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="flex flex-col gap-2">
            <span className="text-[11px] uppercase font-mono tracking-wider text-[var(--c-encre-2)]">
              2. Rôles proposés
            </span>
            <div className="flex flex-col gap-1.5">
              {donneesPaires.droites.map((d) => {
                const repAssocie = Object.entries(liens).find(([, val]) => val === d.id)?.[0];

                return (
                  <button
                    key={d.id}
                    type="button"
                    disabled={revele || !selectionGauche}
                    onClick={() => lier(d.id)}
                    className={
                      "p-2 rounded-xl text-left text-xs border transition flex items-start justify-between gap-2 " +
                      (repAssocie
                        ? "border-[var(--c-accent)] bg-[var(--c-surface-creuse)] text-[var(--c-encre)] font-medium"
                        : selectionGauche
                        ? "border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] text-[var(--c-encre)] hover:border-[var(--c-accent)] cursor-pointer"
                        : "border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] text-[var(--c-encre-2)] opacity-75")
                    }
                  >
                    <span className="flex items-baseline gap-1.5">
                      <strong className="font-mono text-[var(--c-accent)]">({d.id})</strong>
                      <span>{d.label}</span>
                    </span>
                    {repAssocie ? (
                      <span
                        onClick={(e) => {
                          e.stopPropagation();
                          dissocier(repAssocie);
                        }}
                        className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-[var(--c-accent)] text-[var(--c-sur-accent)] flex items-center gap-1 hover:opacity-90"
                      >
                        Repère {repAssocie}
                        {!revele ? <X size={10} /> : null}
                      </span>
                    ) : null}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {Object.keys(liens).length > 0 ? (
          <div className="mt-4 pt-3 border-t border-[var(--c-bordure-subtile)] flex flex-wrap items-center gap-2">
            <span className="text-[11px] text-[var(--c-encre-2)]">Associations :</span>
            {Object.entries(liens)
              .sort(([k1], [k2]) => k1.localeCompare(k2, undefined, { numeric: true }))
              .map(([g, d]) => (
                <span
                  key={g}
                  className="text-xs px-2 py-0.5 rounded-md bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] font-mono text-[var(--c-encre)]"
                >
                  {g} → {d}
                </span>
              ))}
          </div>
        ) : null}
      </div>

      <div className="salle-reponse-libre">
        <label htmlFor="reponse-carte">{LIB.taReponse}</label>
        <textarea
          id="reponse-carte"
          rows={2}
          value={reponse}
          readOnly={revele}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => surChangementReponse(e.target.value)}
          placeholder="Ex : 1-e, 2-c, 3-d..."
        />
      </div>
    </div>
  );
}

/**
 * 3. MODULE PHOTO & LECTURE DE PLAN (types: "photo", "plan")
 * Visualiseur d'image enrichi avec zoom loupe tactile et repères cliquables.
 */
export function ModulePhotoPlan({
  image,
  reponse,
  surChangementReponse,
  revele,
}: {
  image: { fichier: string; alt: string; credit: string };
  reponse: string;
  surChangementReponse: (valeur: string) => void;
  revele: boolean;
}) {
  const [zoom, setZoom] = useState(1);
  const [imageAbsente, setImageAbsente] = useState(false);

  const zoomer = () => setZoom((z) => Math.min(2.4, +(z + 0.35).toFixed(2)));
  const dezoomer = () => setZoom((z) => Math.max(1, +(z - 0.35).toFixed(2)));
  const reinitialiserZoom = () => setZoom(1);

  return (
    <div className="module-photo-plan flex flex-col gap-4">
      <div className="relative rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] p-3 shadow-sm overflow-hidden">
        <div className="absolute top-4 right-4 z-10 flex items-center rounded-lg border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] shadow-sm text-xs">
          <button
            type="button"
            onClick={dezoomer}
            disabled={zoom <= 1}
            className="p-1.5 text-[var(--c-encre-2)] hover:text-[var(--c-encre)] disabled:opacity-40 transition"
            title="Zoom arrière"
            aria-label="Zoom arrière"
          >
            <ZoomOut size={14} />
          </button>
          <button
            type="button"
            onClick={reinitialiserZoom}
            className="px-2 py-1 font-mono text-[11px] border-x border-[var(--c-bordure-subtile)] text-[var(--c-encre)]"
            title="Réinitialiser zoom"
          >
            {Math.round(zoom * 100)}%
          </button>
          <button
            type="button"
            onClick={zoomer}
            disabled={zoom >= 2.4}
            className="p-1.5 text-[var(--c-encre-2)] hover:text-[var(--c-encre)] disabled:opacity-40 transition"
            title="Zoom avant"
            aria-label="Zoom avant"
          >
            <ZoomIn size={14} />
          </button>
        </div>

        <figure className="salle-image m-0 flex flex-col items-center justify-center min-h-[220px] max-h-[380px] overflow-auto">
          <img
            src={image.fichier}
            alt={image.alt}
            onError={() => setImageAbsente(true)}
            className="max-h-[340px] max-w-full object-contain transition-transform duration-200"
            style={{ transform: `scale(${zoom})`, transformOrigin: "center center" }}
          />
          {image.credit ? (
            <figcaption className="text-[11px] text-[var(--c-encre-2)] mt-2 text-center">
              {image.credit}
            </figcaption>
          ) : null}
          {imageAbsente ? <p role="status">{LIB.imageIndisponible}</p> : null}
        </figure>
      </div>

      <div className="salle-reponse-libre">
        <label htmlFor="reponse-carte">{LIB.taReponse}</label>
        <textarea
          id="reponse-carte"
          rows={3}
          value={reponse}
          readOnly={revele}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => surChangementReponse(e.target.value)}
          placeholder="Décris le composant, son rôle et le diagnostic de défaillance..."
        />
      </div>
    </div>
  );
}

/**
 * 4. MODULE CHRONOLOGIE & DATATION (type: "datation")
 * Frise temporelle avec étapes ordonnées et identification de l'échéance manquante.
 */
export interface EtapeChronologie {
  num: number;
  titre: string;
  cible?: boolean;
}

export function ModuleDatation({
  carte,
  reponse,
  surChangementReponse,
  revele,
}: {
  carte: Carte;
  reponse: string;
  surChangementReponse: (valeur: string) => void;
  revele: boolean;
}) {
  const etapesProcedure = useMemo<EtapeChronologie[]>(() => {
    // 1. Étapes déclarées directement dans la carte
    if (carte.etapes && Array.isArray(carte.etapes) && carte.etapes.length > 0) {
      return carte.etapes as EtapeChronologie[];
    }
    // 2. Extraction dynamique d'étapes numérotées depuis la question
    const regexEtape = /(?:^|\s)([1-9])[\s.)-]+\s*([^;.\n]+)/g;
    const extraites: EtapeChronologie[] = [];
    let match: RegExpExecArray | null;
    while ((match = regexEtape.exec(carte.question)) !== null) {
      const num = Number(match[1]);
      const titre = match[2]?.trim() ?? "";
      if (titre && !extraites.some((e) => e.num === num)) {
        extraites.push({ num, titre, cible: titre.includes("?") || carte.question.includes(`étape ${num}`) });
      }
    }
    if (extraites.length >= 3) {
      return extraites.sort((a, b) => a.num - b.num);
    }
    // 3. Modèle procédural canonique pour le recouvrement de charges et la déchéance du terme
    return [
      { num: 1, titre: "Relance simple" },
      { num: 2, titre: "Mise en demeure" },
      { num: 3, titre: "Délai de 30 jours", cible: true },
      { num: 4, titre: "Déchéance du terme" },
      { num: 5, titre: "Titre exécutoire" },
      { num: 6, titre: "Mesures d exécution" },
    ];
  }, [carte.etapes, carte.question]);

  return (
    <div className="module-datation flex flex-col gap-4">
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] p-4 shadow-sm">
        <span className="text-[11px] uppercase font-mono tracking-wider text-[var(--c-encre-2)] mb-3 block">
          Frise chronologique de la procédure
        </span>

        <div className="flex items-center gap-1.5 overflow-x-auto pb-2">
          {etapesProcedure.map((etp, idx) => (
            <div key={etp.num} className="flex items-center flex-shrink-0">
              <div
                className={
                  "flex flex-col items-center justify-center p-2 rounded-xl border text-center transition min-w-[90px] " +
                  (etp.cible
                    ? "border-[var(--c-accent)] bg-[var(--c-accent-fond)] shadow-sm"
                    : "border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)]")
                }
              >
                <span
                  className={
                    "w-6 h-6 rounded-full flex items-center justify-center text-xs font-mono font-bold mb-1 " +
                    (etp.cible
                      ? "bg-[var(--c-accent)] text-[var(--c-sur-accent)]"
                      : "bg-[var(--c-surface)] text-[var(--c-encre-2)] border border-[var(--c-bordure-subtile)]")
                  }
                >
                  {etp.cible ? "?" : etp.num}
                </span>
                <span className="text-[11px] font-medium text-[var(--c-encre)] line-clamp-2">
                  {etp.titre}
                </span>
              </div>
              {idx < etapesProcedure.length - 1 ? (
                <span className="w-3 h-0.5 bg-[var(--c-trait)] mx-1" />
              ) : null}
            </div>
          ))}
        </div>
      </div>

      <div className="salle-reponse-libre">
        <label htmlFor="reponse-carte">{LIB.taReponse}</label>
        <textarea
          id="reponse-carte"
          rows={3}
          value={reponse}
          readOnly={revele}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => surChangementReponse(e.target.value)}
          placeholder="Nomme le délai, son point de départ et le rang de l étape..."
        />
      </div>
    </div>
  );
}

/**
 * 5. MODULE SYNTHESE & CAS REELS (types: "synthese", "cas")
 * Grille d'auto-évaluation des attendus pédagogiques apparaissant à la correction.
 */
export function ModuleSynthese({
  carte,
  reponse,
  surChangementReponse,
  revele,
}: {
  carte: Carte;
  reponse: string;
  surChangementReponse: (valeur: string) => void;
  revele: boolean;
}) {
  const [aideOuverte, setAideOuverte] = useState(false);
  const attendus = useMemo(() => {
    return Array.isArray(carte.attendus) ? (carte.attendus as string[]) : [];
  }, [carte.attendus]);

  const [critèresCoches, setCritèresCoches] = useState<Record<number, boolean>>({});

  const basculerCritere = (index: number) => {
    setCritèresCoches((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const nbCoches = Object.values(critèresCoches).filter(Boolean).length;

  return (
    <div className="module-synthese flex flex-col gap-4">
      {carte.aide ? (
        <div className="rounded-xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] overflow-hidden">
          <button
            type="button"
            onClick={() => setAideOuverte(!aideOuverte)}
            className="w-full flex items-center justify-between p-3 text-xs font-medium text-[var(--c-encre)] hover:bg-[var(--c-surface-creuse)] transition"
          >
            <span className="flex items-center gap-2 text-[var(--c-accent)]">
              <HelpCircle size={15} />
              <span>Besoin d un indice ?</span>
            </span>
            <span className="text-[11px] text-[var(--c-encre-2)]">
              {aideOuverte ? "Masquer" : "Afficher"}
            </span>
          </button>
          {aideOuverte ? (
            <div className="p-3 pt-0 text-xs text-[var(--c-encre-2)] border-t border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)]">
              {String(carte.aide)}
            </div>
          ) : null}
        </div>
      ) : null}

      <div className="salle-reponse-libre">
        <label htmlFor="reponse-carte">{LIB.taReponse}</label>
        <textarea
          id="reponse-carte"
          rows={4}
          value={reponse}
          readOnly={revele}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => surChangementReponse(e.target.value)}
          placeholder="Rédige ta transmission ou analyse complète sans inventer de données..."
        />
      </div>

      {revele && attendus.length > 0 ? (
        <div className="salle-retour rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface)] p-4 shadow-sm">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-[var(--c-bordure-subtile)]">
            <span className="text-xs font-semibold text-[var(--c-encre)] flex items-center gap-1.5">
              <Sparkles size={14} className="text-[var(--c-accent)]" />
              <span>Auto-évaluation : critères couverts</span>
            </span>
            <span className="text-xs font-mono px-2 py-0.5 rounded-full bg-[var(--c-surface-creuse)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre)]">
              {nbCoches} / {attendus.length}
            </span>
          </div>

          <ul className="flex flex-col gap-2">
            {attendus.map((critere, i) => {
              const estCoche = !!critèresCoches[i];

              return (
                <li key={i}>
                  <label className="flex items-start gap-2.5 p-2 rounded-xl text-xs text-[var(--c-encre)] hover:bg-[var(--c-surface-creuse)] transition cursor-pointer">
                    <input
                      type="checkbox"
                      checked={estCoche}
                      onChange={() => basculerCritere(i)}
                      className="mt-0.5 accent-[var(--c-accent)]"
                    />
                    <span className={estCoche ? "font-medium" : "text-[var(--c-encre-2)]"}>
                      {critere}
                    </span>
                  </label>
                </li>
              );
            })}
          </ul>
        </div>
      ) : null}
    </div>
  );
}

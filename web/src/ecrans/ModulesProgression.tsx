import { useState, useMemo } from "react";
import {
  Award, Compass, Flame, Brain, ShieldCheck, Sparkles, Share2,
  Pin, PinOff, Trophy, Timer, Lock,
  Info, Shield, Scale, Wind, FileText, ArrowRight, Check, X,
} from "lucide-react";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import {
  calculeLigueHebdo,
  calculeTrophees,
  calculeInsignes,
  calculeBranchesPonts,
  titreDuJoueur,
} from "../moteur/progressionAvancee";
import { CarteMagnetique, BordureLumineuse, EclatParticules, NombreAnime } from "./MicroAnimations";

/* =========================================================================
   1. MODULE PASSEPORT (CARTE DE VISITE 3D MAGNÉTIQUE)
   ========================================================================= */

export function ModulePasseport() {
  const { banque, points, monde, journal } = useMagasin();
  const [copie, setCopie] = useState(false);
  const [verso, setVerso] = useState(false);

  const titre = useMemo(() => titreDuJoueur(points, monde), [points, monde]);
  const epinglesIds = useMemo(() => {
    try {
      const brut = localStorage.getItem("academie-insignes-epingles");
      return new Set<string>(brut ? JSON.parse(brut) : ["insigne-chauffage-p3"]);
    } catch {
      return new Set<string>(["insigne-chauffage-p3"]);
    }
  }, []);

  const insignesCatalogue = useMemo(
    () => calculeInsignes(banque, new Map(), epinglesIds),
    [banque, epinglesIds],
  );
  const insignesAffiches = insignesCatalogue.filter((i) => epinglesIds.has(i.id)).slice(0, 3);

  const matricule = useMemo(() => {
    const totalRevisions = journal.filter((l) => l.mode === "revision").length;
    return `ACA-${new Date().getFullYear()}-${String(totalRevisions + 1042).padStart(5, "0")}`;
  }, [journal]);

  const copierLien = async () => {
    try {
      await navigator.clipboard.writeText(
        `Académie Professionnelle · ${titre.titre} (${matricule}) · ${points?.xp ?? 0} points de maîtrise`,
      );
      setCopie(true);
      setTimeout(() => setCopie(false), 2000);
    } catch {
      // Ignorer si refus presse-papier
    }
  };

  return (
    <div className="flex flex-col gap-6 items-center">
      <div className="w-full max-w-lg">
        <CarteMagnetique className="w-full">
          <div
            className="relative overflow-hidden rounded-2xl border border-[var(--c-bordure-subtile)] bg-gradient-to-br from-[var(--c-surface-elevee)] to-[var(--c-surface-creuse)] p-6 shadow-xl transition-all duration-300"
            style={{ minHeight: "260px" }}
          >
            <BordureLumineuse couleur="var(--c-accent)" duree={8} />

            {!verso ? (
              /* Recto : Passeport d'identité professionnelle */
              <div className="flex flex-col justify-between h-full gap-5">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-9 h-9 rounded-xl bg-[var(--c-accent)] text-white flex items-center justify-center font-bold text-sm shadow-md">
                      <span>{titre.niveau}</span>
                    </div>
                    <div>
                      <p className="text-[10px] uppercase font-bold tracking-wider text-[var(--c-encre-3)]">
                        Passeport de Maîtrise
                      </p>
                      <h2 className="text-base font-bold text-[var(--c-encre)]">{titre.titre}</h2>
                    </div>
                  </div>
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded-full border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-fond)] text-[var(--c-encre-2)]">
                    {matricule}
                  </span>
                </div>

                <div className="space-y-1">
                  <p className="text-xs text-[var(--c-encre-2)]">{titre.sousTitre}</p>
                  <div className="flex items-center gap-3 text-xs pt-1">
                    <span className="font-semibold text-[var(--c-encre)]">
                      <NombreAnime valeur={points?.xp ?? 0} /> <span className="font-normal text-[var(--c-encre-3)]">XP</span>
                    </span>
                    <span className="text-[var(--c-encre-3)]">·</span>
                    <span className="font-semibold text-[var(--c-encre)]">
                      {Math.round((monde?.remplissageGlobal ?? 0) * 100)}% <span className="font-normal text-[var(--c-encre-3)]">socle</span>
                    </span>
                    <span className="text-[var(--c-encre-3)]">·</span>
                    <span className="font-semibold text-[var(--c-encre)]">
                      {points?.serieJours ?? 0} <span className="font-normal text-[var(--c-encre-3)]">j série</span>
                    </span>
                  </div>
                </div>

                <div className="pt-2 border-t border-[var(--c-bordure-subtile)] flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-[var(--c-encre-3)]">Insignes :</span>
                    <div className="flex items-center gap-1.5">
                      {insignesAffiches.length > 0 ? (
                        insignesAffiches.map((insigne) => (
                          <span
                            key={insigne.id}
                            title={insigne.titre}
                            className="text-[11px] px-2 py-0.5 rounded-md bg-[var(--c-surface-elevee)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre)] flex items-center gap-1 font-medium"
                          >
                            <Sparkles size={11} className="text-[var(--c-accent)]" />
                            <span>{insigne.titre.replace("Brevet ", "").replace("Insigne ", "")}</span>
                          </span>
                        ))
                      ) : (
                        <span className="text-[11px] text-[var(--c-encre-3)] italic">Aucun insigne épinglé</span>
                      )}
                    </div>
                  </div>
                  <div className="w-4 h-4 rounded-full bg-[var(--c-succes-fond)] border border-[var(--c-succes)]/40 flex items-center justify-center">
                    <div className="w-2 h-2 rounded-full bg-[var(--c-succes)] animate-pulse" />
                  </div>
                </div>
              </div>
            ) : (
              /* Verso : Statistiques avancées et validation */
              <div className="flex flex-col justify-between h-full gap-4">
                <div>
                  <h3 className="text-xs uppercase font-bold tracking-wider text-[var(--c-encre-3)] mb-2">
                    Validation du Cursus
                  </h3>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <div className="p-2 rounded-lg bg-[var(--c-surface-fond)] border border-[var(--c-bordure-subtile)]">
                      <p className="text-[10px] text-[var(--c-encre-3)]">Cartes stabilisées</p>
                      <p className="font-bold text-sm text-[var(--c-encre)]">{points?.cartesTouchees ?? 0}</p>
                    </div>
                    <div className="p-2 rounded-lg bg-[var(--c-surface-fond)] border border-[var(--c-bordure-subtile)]">
                      <p className="text-[10px] text-[var(--c-encre-3)]">Révisions réussies</p>
                      <p className="font-bold text-sm text-[var(--c-encre)]">{points?.revisions ?? 0}</p>
                    </div>
                  </div>
                </div>
                <p className="text-[11px] text-[var(--c-encre-3)] italic">
                  Données certifiées conformes au journal local de l'Académie (décision 0015).
                </p>
              </div>
            )}
          </div>
        </CarteMagnetique>
      </div>

      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={() => setVerso(!verso)}
          className="bouton-tactile text-xs px-3.5 py-2 rounded-xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] text-[var(--c-encre)] font-medium hover:bg-[var(--c-surface-creuse)] transition"
        >
          {verso ? "Voir le recto" : "Voir les certifications (verso)"}
        </button>
        <button
          type="button"
          onClick={copierLien}
          className="bouton-tactile text-xs px-3.5 py-2 rounded-xl border border-[var(--c-accent)] bg-[var(--c-accent-fond)] text-[var(--c-accent-texte)] font-medium hover:opacity-90 transition flex items-center gap-1.5"
        >
          {copie ? <Check size={14} /> : <Share2 size={14} />}
          <span>{copie ? "Passeport copié !" : "Partager mon passeport"}</span>
        </button>
      </div>
    </div>
  );
}

/* =========================================================================
   2. MODULE LIGUE & CLASSEMENTS
   ========================================================================= */

export function ModuleLigue() {
  const { banque, journal, jour } = useMagasin();
  const [participe, setParticipe] = useState(() => {
    return localStorage.getItem("academie-ligue-optin") !== "non";
  });

  const bilan = useMemo(
    () => calculeLigueHebdo(journal, banque, jour),
    [journal, banque, jour],
  );

  const toggleParticipation = () => {
    const suivant = !participe;
    setParticipe(suivant);
    localStorage.setItem("academie-ligue-optin", suivant ? "oui" : "non");
  };

  const nomsDivisions: Record<string, string> = {
    bronze: "Division Bronze",
    argent: "Division Argent",
    or: "Division Or",
    maitrise: "Ligue de Maîtrise",
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Carte d'en-tête de ligue */}
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] p-5 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="w-12 h-12 rounded-int bg-[var(--c-accent-fond)] border border-[var(--c-accent)]/30 text-[var(--c-accent)] flex items-center justify-center">
            <Trophy size={24} />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-base font-bold text-[var(--c-encre)]">
                {nomsDivisions[bilan.division]}
              </h2>
              <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-full bg-[var(--c-surface-fond)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre-2)]">
                Hebdomadaire
              </span>
            </div>
            <p className="text-xs text-[var(--c-encre-2)] flex items-center gap-1.5 mt-0.5">
              <Timer size={13} />
              <span>Clôture du cycle dans {bilan.joursRestants} jour(s)</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-4 border-t md:border-t-0 md:border-l border-[var(--c-bordure-subtile)] pt-3 md:pt-0 md:pl-4">
          <div>
            <p className="text-[10px] uppercase text-[var(--c-encre-3)] font-medium">Ton score cette semaine</p>
            <p className="text-lg font-extrabold text-[var(--c-encre)]">
              <NombreAnime valeur={bilan.scoreJoueur} /> <span className="text-xs font-normal text-[var(--c-encre-3)]">pts</span>
            </p>
          </div>
          <div>
            <p className="text-[10px] uppercase text-[var(--c-encre-3)] font-medium">Rang actuel</p>
            <p className="text-lg font-extrabold text-[var(--c-accent)]">
              #{bilan.rangJoueur} <span className="text-xs font-normal text-[var(--c-encre-3)]">/ {bilan.totalParticipants}</span>
            </p>
          </div>
        </div>
      </div>

      {/* Règle doctrinale éthique */}
      <div className="p-3.5 rounded-xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] text-xs text-[var(--c-encre-2)] flex items-start gap-2.5">
        <Info size={16} className="text-[var(--c-accent)] shrink-0 mt-0.5" />
        <p>
          <strong className="text-[var(--c-encre)]">Règle éthique de l'Académie (décisions 0010 & 0014) :</strong> La ligue mesure uniquement les cartes stabilisées dans la semaine pondérées par niveau. Le temps passé et les clics répétés ne comptent pas.
        </p>
      </div>

      {/* Liste des participants du cercle */}
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] overflow-hidden shadow-sm">
        <div className="px-4 py-3 border-b border-[var(--c-bordure-subtile)] flex items-center justify-between text-xs font-semibold text-[var(--c-encre-3)] uppercase tracking-wider">
          <span>Classement de promotion</span>
          <span>Cartes stabilisées · Points</span>
        </div>

        <ul className="divide-y divide-[var(--c-bordure-subtile)]">
          {bilan.participants.map((p) => {
            return (
              <li
                key={p.id}
                className={`px-4 py-3 flex items-center justify-between text-sm transition-colors ${
                  p.estJoueur
                    ? "bg-[var(--c-accent-fond)] font-semibold text-[var(--c-accent-texte)]"
                    : "hover:bg-[var(--c-surface-creuse)] text-[var(--c-encre)]"
                }`}
              >
                <div className="flex items-center gap-3">
                  <span
                    className={`w-6 text-center font-mono font-bold text-xs ${
                      p.rang === 1
                        ? "text-[var(--c-rang-1)] font-extrabold"
                        : p.rang === 2
                        ? "text-[var(--c-encre-2)] font-bold"
                        : p.rang === 3
                        ? "text-[var(--c-rang-2)] font-bold"
                        : "text-[var(--c-encre-3)]"
                    }`}
                  >
                    {p.rang === 1 ? "1er" : `${p.rang}e`}
                  </span>
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs text-white shadow-sm"
                    style={{ backgroundColor: p.pastilleCouleur }}
                  >
                    {p.nom.charAt(0)}
                  </div>
                  <div>
                    <span className="font-medium">{p.nom}</span>
                    {p.estJoueur ? (
                      <span className="ml-2 text-[10px] px-1.5 py-0.2 rounded bg-[var(--c-accent)] text-white font-bold">
                        MOI
                      </span>
                    ) : null}
                  </div>
                </div>

                <div className="text-right font-mono text-xs">
                  <span className="text-[var(--c-encre-2)]">{p.stabilisees} cartes</span>
                  <span className="mx-2 text-[var(--c-encre-3)]">·</span>
                  <span className="font-bold text-[var(--c-encre)]">{p.score} pts</span>
                </div>
              </li>
            );
          })}
        </ul>
      </div>

      {/* Option discrétion */}
      <div className="flex items-center justify-between text-xs text-[var(--c-encre-2)] px-2">
        <span>Visibilité de promotion : {participe ? "Activée" : "Masquée"}</span>
        <button
          type="button"
          onClick={toggleParticipation}
          className="text-[var(--c-accent)] underline hover:opacity-80 transition"
        >
          {participe ? "Passer en mode discret" : "Participer à la ligue"}
        </button>
      </div>
    </div>
  );
}

/* =========================================================================
   3. MODULE TROPHÉES DE MAÎTRISE
   ========================================================================= */

export function ModuleTrophees() {
  const { monde, points, journal } = useMagasin();
  const [eclatId, setEclatId] = useState<string | null>(null);

  const trophees = useMemo(
    () => calculeTrophees(journal, monde, points),
    [journal, monde, points],
  );

  const iconesTrophees: Record<string, typeof Trophy> = {
    Compass,
    Flame,
    Brain,
    ShieldCheck,
    Sparkles,
    Award,
  };

  const debloques = trophees.filter((t) => t.debloque).length;

  const celebrer = (id: string) => {
    setEclatId(id);
    setTimeout(() => setEclatId(null), 800);
  };

  return (
    <div className="flex flex-col gap-6">
      {/* Synthèse */}
      <div className="flex items-center justify-between rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] p-4 shadow-sm">
        <div>
          <h2 className="text-sm font-bold text-[var(--c-encre)]">Jalons d'Accomplissement</h2>
          <p className="text-xs text-[var(--c-encre-2)]">Évolution de ta pratique et régularité</p>
        </div>
        <div className="text-right">
          <span className="text-lg font-extrabold text-[var(--c-accent)]">{debloques}</span>
          <span className="text-xs text-[var(--c-encre-3)]"> / {trophees.length} débloqués</span>
        </div>
      </div>

      {/* Grille Bento des Trophées */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {trophees.map((trophee) => {
          const Icone = iconesTrophees[trophee.icone] ?? Trophy;
          const estEclat = eclatId === trophee.id;
          return (
            <div
              key={trophee.id}
              onClick={() => trophee.debloque && celebrer(trophee.id)}
              className={`relative overflow-hidden rounded-2xl border p-4 transition-all duration-200 cursor-pointer ${
                trophee.debloque
                  ? "border-[var(--c-bordure-forte)] bg-[var(--c-surface-elevee)] shadow-sm hover:border-[var(--c-accent)]"
                  : "border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] opacity-70"
              }`}
            >
              {estEclat ? <EclatParticules nombre={24} duree={700} /> : null}

              <div className="flex items-start justify-between gap-3">
                <div
                  className={`w-10 h-10 rounded-xl flex items-center justify-center transition-transform ${
                    trophee.debloque
                      ? "bg-[var(--c-accent-fond)] text-[var(--c-accent)]"
                      : "bg-[var(--c-surface-fond)] text-[var(--c-encre-3)]"
                  }`}
                >
                  <Icone size={20} />
                </div>
                <span
                  className={`text-[10px] uppercase font-bold px-2 py-0.5 rounded-full ${
                    trophee.debloque
                      ? "bg-[var(--c-succes-fond)] text-[var(--c-succes)] border border-[var(--c-succes)]/30"
                      : "bg-[var(--c-surface-creuse)] text-[var(--c-encre-3)] border border-[var(--c-bordure-subtile)]"
                  }`}
                >
                  {trophee.debloque ? "Validé" : "En cours"}
                </span>
              </div>

              <div className="mt-3">
                <h3 className="text-sm font-bold text-[var(--c-encre)]">{trophee.titre}</h3>
                <p className="text-xs text-[var(--c-encre-2)] mt-0.5">{trophee.description}</p>
              </div>

              {/* Barre de progression */}
              <div className="mt-4 pt-3 border-t border-[var(--c-bordure-subtile)] flex items-center justify-between text-xs">
                <div className="flex-1 mr-3 h-2 rounded-full bg-[var(--c-surface-fond)] overflow-hidden">
                  <div
                    className="h-full bg-[var(--c-accent)] transition-all duration-500 rounded-full"
                    style={{ width: `${Math.round(trophee.progression * 100)}%` }}
                  />
                </div>
                <span className="font-mono text-[11px] text-[var(--c-encre-2)]">
                  {trophee.valeurCourante} / {trophee.valeurCible} {trophee.unite}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* =========================================================================
   4. MODULE BADGES & INSIGNES DE SPÉCIALITÉ
   ========================================================================= */

export function ModuleBadges() {
  const { banque, etats } = useMagasin();
  const [avertissement, setAvertissement] = useState<string | null>(null);
  const [epingles, setEpingles] = useState<Set<string>>(() => {
    try {
      const brut = localStorage.getItem("academie-insignes-epingles");
      return new Set(brut ? JSON.parse(brut) : ["insigne-chauffage-p3"]);
    } catch {
      return new Set(["insigne-chauffage-p3"]);
    }
  });

  const insignes = useMemo(
    () => calculeInsignes(banque, etats, epingles),
    [banque, etats, epingles],
  );

  const toggleEpingle = (id: string) => {
    const suivant = new Set(epingles);
    if (suivant.has(id)) {
      suivant.delete(id);
      setAvertissement(null);
    } else {
      if (suivant.size >= 3) {
        setAvertissement("Tu peux épingler au maximum 3 insignes sur ton passeport.");
        setTimeout(() => setAvertissement(null), 3500);
        return;
      }
      suivant.add(id);
      setAvertissement(null);
    }
    setEpingles(suivant);
    localStorage.setItem("academie-insignes-epingles", JSON.stringify(Array.from(suivant)));
  };

  const iconesInsignes: Record<string, typeof Shield> = {
    Flame,
    Wind,
    Scale,
    FileText,
    Shield,
  };

  return (
    <div className="flex flex-col gap-6">
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] p-4 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-[var(--c-encre)]">Brevets & Insignes de Spécialité</h2>
          <p className="text-xs text-[var(--c-encre-2)]">
            Épinglables sur ta carte de visite ({epingles.size} / 3 épinglés)
          </p>
        </div>
      </div>

      {avertissement ? (
        <div
          role="status"
          aria-live="polite"
          className="p-3 rounded-xl bg-[var(--c-surface-creuse)] border border-[var(--c-accent)] text-xs text-[var(--c-accent)] flex items-center justify-between gap-2"
        >
          <span>{avertissement}</span>
          <button
            type="button"
            onClick={() => setAvertissement(null)}
            className="text-[var(--c-encre-2)] hover:text-[var(--c-encre)] p-1 rounded transition"
            aria-label="Fermer le message"
          >
            <X size={13} />
          </button>
        </div>
      ) : null}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {insignes.map((insigne) => {
          const Icone = iconesInsignes[insigne.icone] ?? Shield;
          const estEpingle = epingles.has(insigne.id);
          return (
            <div
              key={insigne.id}
              className={`rounded-2xl border p-4 transition-all ${
                insigne.debloque
                  ? "border-[var(--c-bordure-forte)] bg-[var(--c-surface-elevee)] shadow-sm"
                  : "border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] opacity-60"
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div
                    className={`w-11 h-11 rounded-2xl flex items-center justify-center ${
                      insigne.debloque
                        ? "bg-[var(--c-accent)] text-white shadow-md"
                        : "bg-[var(--c-surface-fond)] text-[var(--c-encre-3)]"
                    }`}
                  >
                    <Icone size={20} />
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-[var(--c-encre)]">{insigne.titre}</h3>
                    <p className="text-[11px] text-[var(--c-encre-3)] uppercase font-semibold">
                      {insigne.domaine} · Niv. {insigne.niveauRequis}
                    </p>
                  </div>
                </div>

                {insigne.debloque ? (
                  <button
                    type="button"
                    onClick={() => toggleEpingle(insigne.id)}
                    className={`p-2 rounded-xl border transition ${
                      estEpingle
                        ? "bg-[var(--c-accent-fond)] border-[var(--c-accent)] text-[var(--c-accent-texte)]"
                        : "border-[var(--c-bordure-subtile)] text-[var(--c-encre-3)] hover:text-[var(--c-encre)]"
                    }`}
                    title={estEpingle ? "Détacher du passeport" : "Épingler au passeport"}
                  >
                    {estEpingle ? <Pin size={15} /> : <PinOff size={15} />}
                  </button>
                ) : (
                  <span title="Prérequis non atteints">
                    <Lock size={15} className="text-[var(--c-encre-3)]" />
                  </span>
                )}
              </div>

              <p className="text-xs text-[var(--c-encre-2)] mt-3">{insigne.description}</p>

              <div className="mt-3 pt-2.5 border-t border-[var(--c-bordure-subtile)] flex items-center justify-between text-[11px]">
                <span className="text-[var(--c-encre-3)]">
                  {insigne.debloque ? `Délivré le ${insigne.dateObtention}` : "À conquérir"}
                </span>
                {estEpingle ? (
                  <span className="font-semibold text-[var(--c-accent)]">Épinglé au passeport</span>
                ) : null}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

/* =========================================================================
   5. MODULE BRANCHES PONTS & DOSSIERS TRANSVERSES
   ========================================================================= */

export function ModulePonts() {
  const { banque, monde } = useMagasin();

  const ponts = useMemo(
    () => calculeBranchesPonts(banque, monde),
    [banque, monde],
  );

  return (
    <div className="flex flex-col gap-6">
      <div className="rounded-2xl border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] p-4 shadow-sm">
        <h2 className="text-sm font-bold text-[var(--c-encre)]">Passerelles Interdisciplinaires</h2>
        <p className="text-xs text-[var(--c-encre-2)]">
          Dossiers transverses reliant plusieurs domaines d'expertise (décision 0014 §5)
        </p>
      </div>

      <div className="space-y-4">
        {ponts.map((pont) => (
          <div
            key={pont.id}
            className={`rounded-2xl border p-5 transition-all ${
              pont.debloque
                ? "border-[var(--c-bordure-forte)] bg-[var(--c-surface-elevee)] shadow-sm"
                : "border-[var(--c-bordure-subtile)] bg-[var(--c-surface-creuse)] opacity-65"
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div>
                <div className="flex flex-wrap items-center gap-2 mb-1.5">
                  {pont.domainesRelies.map((d) => (
                    <span
                      key={d}
                      className="text-[10px] uppercase font-bold px-2 py-0.5 rounded-md bg-[var(--c-surface-fond)] border border-[var(--c-bordure-subtile)] text-[var(--c-encre-2)]"
                    >
                      {d}
                    </span>
                  ))}
                  <span className="text-xs text-[var(--c-encre-3)]">·</span>
                  <span className="text-xs font-semibold text-[var(--c-accent)]">
                    {Math.round(pont.maturite * 100)}% maturité requise
                  </span>
                </div>
                <h3 className="text-base font-bold text-[var(--c-encre)]">{pont.titre}</h3>
              </div>

              {pont.debloque ? (
                <button
                  type="button"
                  onClick={() => va("/salle/seance")}
                  className="bouton-tactile text-xs px-3.5 py-2 rounded-xl bg-[var(--c-accent)] text-white font-medium hover:opacity-90 transition flex items-center gap-1.5 self-start md:self-auto"
                >
                  <span>Ouvrir l'épreuve</span>
                  <ArrowRight size={14} />
                </button>
              ) : (
                <span className="text-xs text-[var(--c-encre-3)] flex items-center gap-1 self-start md:self-auto">
                  <Lock size={13} />
                  <span>Verrouillé</span>
                </span>
              )}
            </div>

            <p className="text-xs text-[var(--c-encre-2)] mt-3">{pont.description}</p>

            <div className="mt-4 p-3 rounded-xl bg-[var(--c-surface-fond)] border border-[var(--c-bordure-subtile)] text-xs text-[var(--c-encre)]">
              <strong className="text-[var(--c-encre-3)] uppercase text-[10px] block mb-1">
                Scénario du cas réel :
              </strong>
              {pont.resumeCas}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

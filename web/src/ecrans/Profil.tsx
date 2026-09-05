import { useEffect, useState } from "react";
import { Download, Moon, Sun, ArrowRight, RefreshCw, Trophy, Award, Shield, Network, UserRound, BarChart3 } from "lucide-react";
import { LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { poseTheme, themeCourant, type Theme } from "../app/theme";
import { exporteJsonl, rejets } from "../moteur/journal";
import { jourOrdinal } from "../moteur/etats";
import { Bouton, pourcent } from "./Ui";
import { NombreAnime, EtatPenseur, RituelSemainePill } from "./MicroAnimations";
import {
  ModulePasseport,
  ModuleLigue,
  ModuleTrophees,
  ModuleBadges,
  ModulePonts,
} from "./ModulesProgression";

type OngletProfil = "passeport" | "ligue" | "trophees" | "insignes" | "ponts" | "journal";

export function Profil({ ongletDefaut }: { ongletDefaut?: string }) {
  const { banque, points, monde, journal, bilan, jour, synchronise } = useMagasin();
  const [theme, setTheme] = useState<Theme>(themeCourant);
  const [nbRejets, setNbRejets] = useState(0);
  const [attente, attend] = useState(false);
  const [erreur, informe] = useState<string | null>(null);

  const [onglet, setOnglet] = useState<OngletProfil>(() => {
    if (ongletDefaut && ["passeport", "ligue", "trophees", "insignes", "ponts", "journal"].includes(ongletDefaut)) {
      return ongletDefaut as OngletProfil;
    }
    return "passeport";
  });

  useEffect(() => {
    if (ongletDefaut && ["passeport", "ligue", "trophees", "insignes", "ponts", "journal"].includes(ongletDefaut)) {
      setOnglet(ongletDefaut as OngletProfil);
    }
  }, [ongletDefaut]);

  useEffect(() => {
    void rejets().then((r) => setNbRejets(r.length)).catch(() => undefined);
  }, [journal.length]);

  const idsMetier = new Set(banque?.cartes.map((c) => c.id) ?? []);
  const reponses = journal.filter((l) => idsMetier.has(l.carte ?? "") && l.mode === "revision" && l.carte && l.note);
  const jours = new Set(reponses.map((l) => jourOrdinal(l.quand)).filter((j): j is number => j !== null));
  const derniere = reponses.slice(-5).reverse();
  const calendrier = Array.from({ length: 91 }, (_, i) => jour - 90 + i);
  const formatDate = (ordinal: number) =>
    new Date(ordinal * 86_400_000).toLocaleDateString("fr-FR", { day: "numeric", month: "long", timeZone: "UTC" });

  async function exporte() {
    informe(null);
    try {
      const texte = await exporteJsonl();
      const url = URL.createObjectURL(new Blob([texte], { type: "application/x-ndjson" }));
      const a = document.createElement("a");
      a.href = url;
      a.download = "journal.jsonl";
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      informe(LIB.exportIndisponible);
    }
  }

  async function relance() {
    attend(true);
    informe(null);
    try {
      await synchronise();
    } catch {
      informe(LIB.synchronisationIndisponible);
    } finally {
      attend(false);
    }
  }

  const onglets: { id: OngletProfil; label: string; icon: typeof UserRound }[] = [
    { id: "passeport", label: "Passeport", icon: UserRound },
    { id: "ligue", label: "Ligue", icon: Trophy },
    { id: "trophees", label: "Trophées", icon: Award },
    { id: "insignes", label: "Insignes", icon: Shield },
    { id: "ponts", label: "Ponts", icon: Network },
    { id: "journal", label: "Journal & Rituels", icon: BarChart3 },
  ];

  return (
    <div className="page-document">
      <header className="profil-entete">
        <div>
          <h1 className="titre-page">{LIB.profil}</h1>
          <p>
            {LIB.niveau} {points?.niveau ?? 1} · {points?.xp ?? 0} {LIB.points} · dans ce métier
          </p>
        </div>
        <span>{pourcent(monde?.remplissageGlobal ?? 0)} {LIB.progression.toLowerCase()} du métier</span>
      </header>

      {/* Bannière d'alerte synchronisation (garantit la visibilité immédiate pour les tests et l'accessibilité) */}
      {(erreur || bilan?.erreur) ? (
        <div className="p-4 mb-4 rounded-xl border border-[var(--c-erreur)]/30 bg-[var(--c-erreur-fond)] text-[var(--c-erreur)] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
          <p role="status">
            {erreur ?? (bilan?.erreur?.statut === 401 ? LIB.synchronisationConnexion : LIB.synchronisationIndisponible)}
          </p>
          <Bouton
            disabled={attente}
            onClick={() => void relance()}
            enfants={
              <>
                <RefreshCw size={14} />
                {attente ? <EtatPenseur texte={LIB.chargement} /> : LIB.synchroniser}
              </>
            }
          />
        </div>
      ) : null}

      <dl className="statistiques">
        <div>
          <dd><NombreAnime valeur={reponses.length} /></dd>
          <dt>{LIB.revisions}</dt>
        </div>
        <div>
          <dd><NombreAnime valeur={new Set(reponses.map((l) => l.carte)).size} /></dd>
          <dt>{LIB.cartes}</dt>
        </div>
        <div>
          <dd><NombreAnime valeur={jours.size} /></dd>
          <dt>{LIB.joursJoues}</dt>
        </div>
      </dl>

      <section className="profil-section mb-6">
        <h2>{LIB.apparence}</h2>
        <div className="themes" role="radiogroup" aria-label={LIB.theme}>
          {(["nuit", "papier"] as const).map((t) => (
            <label className="theme-option" key={t}>
              <input
                type="radio"
                name="theme"
                value={t}
                checked={theme === t}
                onChange={() => {
                  poseTheme(t);
                  setTheme(t);
                }}
              />
              {t === "nuit" ? <Moon size={17} /> : <Sun size={17} />}
              {t === "nuit" ? LIB.themeNuit : LIB.themePapier}
            </label>
          ))}
        </div>
      </section>

      {/* Barre de navigation d'onglets segmented */}
      <div className="flex gap-1.5 overflow-x-auto pb-2 mb-6 border-b border-[var(--c-bordure-subtile)] text-xs">
        {onglets.map((t) => {
          const actif = onglet === t.id;
          const Icone = t.icon;
          return (
            <button
              key={t.id}
              type="button"
              onClick={() => {
                setOnglet(t.id);
                window.location.hash = t.id === "passeport" ? "#/profil" : `#/profil/${t.id}`;
              }}
              className={`bouton-tactile px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 whitespace-nowrap font-medium ${
                actif
                  ? "bg-[var(--c-accent)] text-white shadow-sm"
                  : "text-[var(--c-encre-2)] hover:bg-[var(--c-surface-elevee)] hover:text-[var(--c-encre)]"
              }`}
            >
              <Icone size={14} />
              <span>{t.label}</span>
            </button>
          );
        })}
      </div>

      {/* Contenu selon l'onglet sélectionné */}
      <div className="profil-vue-contenu">
        {onglet === "passeport" ? (
          <ModulePasseport />
        ) : onglet === "ligue" ? (
          <ModuleLigue />
        ) : onglet === "trophees" ? (
          <ModuleTrophees />
        ) : onglet === "insignes" ? (
          <ModuleBadges />
        ) : onglet === "ponts" ? (
          <ModulePonts />
        ) : (
          /* Onglet Journal & Rituels (Historique, Heatmap, Apparence, Sauvegarde) */
          <div className="profil-grille">
            <section className="profil-section mb-6">
              <RituelSemainePill
                joursJoues={jours}
                jourActuel={jour}
                serieJours={points?.serieJours ?? 0}
              />
            </section>

            <section className="profil-section">
              <h2>{LIB.activite}</h2>
              <div
                className="heatmap"
                role="img"
                aria-label={`${LIB.activite}, ${formatDate(jour - 90)} - ${formatDate(jour)}`}
              >
                {calendrier.map((j) => (
                  <span
                    key={j}
                    className={`jour-activite ${jours.has(j) ? "joue" : ""}`}
                    title={`${formatDate(j)} : ${
                      reponses.filter((l) => jourOrdinal(l.quand) === j).length
                    } ${LIB.revisions}`}
                  />
                ))}
              </div>
              <p className="activite-legende">{formatDate(jour - 90)} - {formatDate(jour)}</p>
            </section>

            <section className="profil-section">
              <h2>{LIB.derniereActivite}</h2>
              {derniere.length ? (
                <ul className="journal-recent">
                  {derniere.map((l) => (
                    <li key={`${l.quand}|${l.mode}|${l.nonce}`}>
                      <span>{banque?.cartes.find((c) => c.id === l.carte)?.question ?? LIB.carteIndisponible}</span>
                      <time dateTime={l.quand}>
                        {new Date(l.quand).toLocaleDateString("fr-FR", { day: "numeric", month: "short" })}
                      </time>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="etat-vide">{LIB.aucuneActivite}</p>
              )}
            </section>

            <section className="profil-section">
              <h2>{LIB.journal}</h2>
              <Bouton
                onClick={() => void exporte()}
                enfants={
                  <>
                    <Download size={18} />
                    {LIB.exporter}
                  </>
                }
              />
              <p className="activite-legende">
                {journal.length} {LIB.lignesJournal} · {bilan?.enAttente ?? 0} {LIB.enAttente}
              </p>
              {nbRejets > 0 ? <p role="status">{nbRejets} {LIB.rejetsJournal}</p> : null}
              {bilan?.horsLigne ? <p className="activite-legende">{LIB.horsLigne}</p> : null}
              {erreur || bilan?.erreur ? (
                <p role="status">
                  {erreur ?? (bilan?.erreur?.statut === 401 ? LIB.synchronisationConnexion : LIB.synchronisationIndisponible)}
                </p>
              ) : null}
              <Bouton
                disabled={attente}
                onClick={() => void relance()}
                enfants={
                  <>
                    <RefreshCw size={16} />
                    {attente ? <EtatPenseur texte={LIB.chargement} /> : LIB.synchroniser}
                  </>
                }
              />
            </section>
          </div>
        )}
      </div>

      <footer className="liens-profil mt-8">
        <button className="lien-action" onClick={() => va("/confiance")}>
          {LIB.confiance}
          <ArrowRight size={16} />
        </button>
        <button className="lien-action" onClick={() => va("/credits")}>
          {LIB.credits}
          <ArrowRight size={16} />
        </button>
      </footer>
    </div>
  );
}

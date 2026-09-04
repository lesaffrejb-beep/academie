import { useEffect, useState } from "react";
import { Download, Moon, Sun, ArrowRight, RefreshCw } from "lucide-react";
import { LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { poseTheme, themeCourant, type Theme } from "../app/theme";
import { exporteJsonl, rejets } from "../moteur/journal";
import { jourOrdinal } from "../moteur/etats";
import { Bouton, pourcent } from "./Ui";

export function Profil() {
  const { banque, points, monde, journal, bilan, jour, synchronise } = useMagasin();
  const [theme, setTheme] = useState<Theme>(themeCourant);
  const [nbRejets, setNbRejets] = useState(0);
  const [attente, attend] = useState(false);
  const [erreur, informe] = useState<string | null>(null);
  useEffect(() => { void rejets().then((r) => setNbRejets(r.length)).catch(() => undefined); }, [journal.length]);
  const reponses = journal.filter((l) => l.mode === "revision" && l.carte && l.note);
  const jours = new Set(reponses.map((l) => jourOrdinal(l.quand)));
  const derniere = reponses.slice(-5).reverse();
  const calendrier = Array.from({ length: 91 }, (_, i) => jour - 90 + i);
  const formatDate = (ordinal: number) => new Date(ordinal * 86_400_000).toLocaleDateString("fr-FR", { day: "numeric", month: "long", timeZone: "UTC" });

  async function exporte() {
    informe(null);
    try {
    const texte = await exporteJsonl();
    const url = URL.createObjectURL(new Blob([texte], { type: "application/x-ndjson" }));
    const a = document.createElement("a"); a.href = url; a.download = "journal.jsonl"; a.click(); URL.revokeObjectURL(url);
    } catch { informe(LIB.exportIndisponible); }
  }

  async function relance() {
    attend(true); informe(null);
    try { await synchronise(); }
    catch { informe(LIB.synchronisationIndisponible); }
    finally { attend(false); }
  }

  return <div className="page-document">
    <header className="profil-entete"><div><h1 className="titre-page">{LIB.profil}</h1><p>{LIB.niveau} {points?.niveau ?? 1} · {points?.xp ?? 0} {LIB.points}</p></div><span>{pourcent(monde?.remplissageGlobal ?? 0)} {LIB.progression.toLowerCase()}</span></header>
    <dl className="statistiques"><div><dd>{reponses.length}</dd><dt>{LIB.revisions}</dt></div><div><dd>{new Set(reponses.map((l) => l.carte)).size}</dd><dt>{LIB.cartes}</dt></div><div><dd>{jours.size}</dd><dt>{LIB.joursJoues}</dt></div></dl>
    <div className="profil-grille">
      <section className="profil-section"><h2>{LIB.activite}</h2><div className="heatmap" role="img" aria-label={`${LIB.activite}, ${formatDate(jour - 90)} - ${formatDate(jour)}`}>
        {calendrier.map((j) => <span key={j} className={`jour-activite ${jours.has(j) ? "joue" : ""}`} title={`${formatDate(j)} : ${reponses.filter((l) => jourOrdinal(l.quand) === j).length} ${LIB.revisions}`} />)}
      </div><p className="activite-legende">{formatDate(jour - 90)} - {formatDate(jour)}</p></section>
      <section className="profil-section"><h2>{LIB.apparence}</h2><div className="themes" role="radiogroup" aria-label={LIB.theme}>
        {(["nuit", "papier"] as const).map((t) => <label className="theme-option" key={t}><input type="radio" name="theme" value={t} checked={theme === t} onChange={() => { poseTheme(t); setTheme(t); }} />{t === "nuit" ? <Moon size={17} /> : <Sun size={17} />}{t === "nuit" ? LIB.themeNuit : LIB.themePapier}</label>)}
      </div></section>
      <section className="profil-section"><h2>{LIB.derniereActivite}</h2>{derniere.length ? <ul className="journal-recent">{derniere.map((l) => <li key={`${l.quand}|${l.mode}|${l.nonce}`}><span>{banque?.cartes.find((c) => c.id === l.carte)?.question ?? LIB.carteIndisponible}</span><time dateTime={l.quand}>{new Date(l.quand).toLocaleDateString("fr-FR", { day: "numeric", month: "short" })}</time></li>)}</ul> : <p className="etat-vide">{LIB.aucuneActivite}</p>}</section>
      <section className="profil-section"><h2>{LIB.journal}</h2><Bouton onClick={() => void exporte()} enfants={<><Download size={18} />{LIB.exporter}</>} /><p className="activite-legende">{journal.length} {LIB.lignesJournal} · {bilan?.enAttente ?? 0} {LIB.enAttente}</p>{nbRejets > 0 ? <p role="status">{nbRejets} {LIB.rejetsJournal}</p> : null}{bilan?.horsLigne ? <p className="activite-legende">{LIB.horsLigne}</p> : null}
        {erreur || bilan?.erreur ? <p role="status">{erreur ?? (bilan?.erreur?.statut === 401 ? LIB.synchronisationConnexion : LIB.synchronisationIndisponible)}</p> : null}
        <Bouton disabled={attente} onClick={() => void relance()} enfants={<><RefreshCw size={16} />{attente ? LIB.chargement : LIB.synchroniser}</>} />
      </section>
    </div>
    <footer className="liens-profil"><button className="lien-action" onClick={() => va("/confiance")}>{LIB.confiance}<ArrowRight size={16} /></button><button className="lien-action" onClick={() => va("/credits")}>{LIB.credits}<ArrowRight size={16} /></button></footer>
  </div>;
}

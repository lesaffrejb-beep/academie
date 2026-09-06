import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from "react";
import {
  ArrowLeft, ArrowRight, BookOpen, Check, ChevronDown, ExternalLink, Flag,
  Image as ImageIcon, ListChecks, MessageSquare, X, ZoomIn, ZoomOut,
} from "lucide-react";
import { LIB, TYPES_CARTE, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import { auHasard, compose } from "../moteur/composeur";
import { aujourdhuiOrdinal } from "../moteur/etats";
import { cartesServiables } from "../moteur/serviceabilite";
import type { Carte, LigneJournal } from "../donnees/types";
import { Bouton, Jauge } from "./Ui";
import { EclatParticules, ToastExp, VoletGlissant } from "./MicroAnimations";
import {
  ModuleRole,
  ModuleRelier,
  ModuleDatation,
  ModuleSynthese,
} from "./ModulesSeance";

type TraceReponse = Pick<LigneJournal,"reponse_libre"|"attendus_coches">;
const MOTEUR_VERSION = "web-2.0.0";
const NIVEAUX = ["", "I", "II", "III", "IV", "V"];

export function Seance({ portee }: { portee?: string }) {
  const { banque, etats, jour, note, journal } = useMagasin();
  const [index, setIndex] = useState(0);
  const [enregistrement, setEnregistrement] = useState(false);
  const [erreur, setErreur] = useState<string | null>(null);
  const verrou = useRef(false);
  const ouverture = useRef<Promise<void> | null>(null);

  // Le tirage reste fixe ; seules les cartes devenues impropres en sortent.
  const tirage = useMemo(() => {
    if (!banque) return { cartes: [], neuves: new Set<string>(), graine: jour };
    if (portee === "hasard") {
      return { cartes: auHasard(banque, 10, jour, { journal, aujourdhui: jour }),
        neuves: new Set<string>(), graine: jour };
    }
    const chapitre = portee?.startsWith("chapitre:") ? portee.slice(9) : null;
    const b = chapitre ? { ...banque, cartes: banque.cartes.filter((c) => c.chapitre === chapitre) } : banque;
    const seance = compose(b, etats, {
      aujourdhui: jour, journal, ...(portee && !chapitre ? { domaine: portee } : {}),
    });
    return { cartes: [...seance.revisions, ...seance.nouveau],
      neuves: new Set(seance.nouveau.map((c) => c.id)), graine: jour };
    // Le journal et le jour evoluent pendant la salle, pas son tirage.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [banque, portee]);

  const disponibles = new Set(cartesServiables(tirage.cartes, journal, jour).map((c) => c.id));
  const position = tirage.cartes.findIndex((c, i) => i >= index && disponibles.has(c.id));
  const carte = tirage.cartes[position];
  const format = portee === "hasard" ? "hasard" : portee ? "domaine" : "seance";

  const ouvre = useCallback((): Promise<void> => {
    if (!banque) return Promise.resolve();
    if (!ouverture.current) {
      ouverture.current = note({
        mode: "seance", format, graine: tirage.graine,
        banque_version: banque.genere_le ?? "inconnue", moteur_version: MOTEUR_VERSION,
        ...(portee?.startsWith("chapitre:") ? { chapitre: portee.slice(9) }
          : portee && portee !== "hasard" ? { cap: portee } : {}),
      }).catch((e: unknown) => { ouverture.current = null; throw e; });
    }
    return ouverture.current;
  }, [banque, format, note, portee, tirage.graine]);

  useEffect(() => {
    if (tirage.cartes.length) void ouvre().catch(() => setErreur(LIB.enregistrementImpossible));
  }, [ouvre, tirage.cartes.length]);

  useEffect(() => {
    if (tirage.cartes.length && !carte) va("/salle/cloture");
  }, [carte, tirage.cartes.length]);

  const enregistre = useCallback(async (valeur: 1 | 2 | 3 | 4 | "signalement", confiance = false, duree = 0, trace:TraceReponse = {}) => {
    if (!carte || verrou.current) return;
    if (!cartesServiables([carte], journal, aujourdhuiOrdinal()).length) {
      setIndex(position + 1);
      return;
    }
    verrou.current = true;
    setEnregistrement(true);
    setErreur(null);
    try {
      await ouvre();
      await note(valeur === "signalement"
        ? { mode: "signalement", carte: carte.id }
        : { mode: "revision", format, carte: carte.id, note: valeur,
          duree_ms: Math.max(0, duree), confiance, ...trace,
          ...(tirage.neuves.has(carte.id) ? { origine: "nouveau" } : {}) });
      setIndex(position + 1);
    } catch {
      setErreur(LIB.enregistrementImpossible);
    } finally {
      verrou.current = false;
      setEnregistrement(false);
    }
  }, [carte, format, journal, note, ouvre, position, tirage.neuves]);

  if (!banque) return null;
  if (!carte) return <div className="salle">
    <h1 className="font-titre text-2xl">{LIB.seance}</h1>
    <p>{voix("cap.rien", {}, jour)}</p>
    <Bouton onClick={() => va("/")} enfants={<><ArrowLeft size={18} />{LIB.retournerArbre}</>} />
  </div>;

  const domaine = banque.domaines[carte.domaine];
  return <div className="salle" style={{ "--c-accent": accentDuRang(domaine?.ordre ?? 1) } as CSSProperties}>
    <header className="salle-entete">
      <button type="button" className="bouton-icone" aria-label={LIB.quitter} title={LIB.quitter}
        onClick={() => va("/")}><ArrowLeft size={22} /></button>
      <div className="salle-identite"><span>{domaine?.titre ?? carte.domaine}</span>
        <span>{Math.max(0, position) + 1} / {tirage.cartes.length}</span></div>
    </header>
    <Jauge part={Math.max(0, position) / tirage.cartes.length} />
    {erreur ? <p role="alert" className="salle-erreur">{erreur}</p> : null}
    <Exercice key={carte.id} carte={carte} graine={tirage.graine}
      enregistrement={enregistrement} enregistre={enregistre} />
  </div>;
}

function Exercice({ carte, graine, enregistrement, enregistre }: {
  carte: Carte; graine: number; enregistrement: boolean;
  enregistre: (valeur: 1 | 2 | 3 | 4 | "signalement", confiance?: boolean, duree?: number, trace?:TraceReponse) => Promise<void>;
}) {
  const [revele, setRevele] = useState(false);
  const [eclat, setEclat] = useState(false);
  const [expGagnee, setExpGagnee] = useState<number | null>(null);
  const [confiance, setConfiance] = useState(false);
  const [choisi, setChoisi] = useState<number | null>(null);
  const [reponse, setReponse] = useState("");
  const [attendusCoches,setAttendusCoches] = useState<number[]>([]);
  const [imageAbsente, setImageAbsente] = useState(false);
  const [zoomImage, setZoomImage] = useState(1);
  const debut = useRef(Date.now());
  const titre = useRef<HTMLHeadingElement>(null);
  const correct = carte.choix?.findIndex((c) => c.correct) ?? -1;
  const qcm = carte.type === "qcm" && Boolean(carte.choix?.length);
  const Icone = qcm ? ListChecks : carte.image ? ImageIcon : carte.type === "flash" ? BookOpen : MessageSquare;
  const image = imageDe(carte);

  useEffect(() => { titre.current?.focus({ preventScroll: true }); }, []);

  useEffect(() => {
    function clavier(e: KeyboardEvent) {
      if (e.altKey || e.ctrlKey || e.metaKey || e.repeat || enregistrement) return;
      if (e.key === "Escape") { e.preventDefault(); va("/"); return; }
      const cible = e.target as HTMLElement | null;
      if (["INPUT", "TEXTAREA", "SELECT"].includes(cible?.tagName ?? "") || cible?.isContentEditable) return;
      if (revele && ["1", "2", "3", "4"].includes(e.key)) {
        e.preventDefault();
        const noteChoisie = Number(e.key) as 1 | 2 | 3 | 4;
        const gain = (noteChoisie === 4 ? 30 : noteChoisie === 3 ? 20 : noteChoisie === 2 ? 10 : 5);
        setExpGagnee(gain);
        if (noteChoisie >= 3) setEclat(true);
        void enregistre(noteChoisie, confiance, Date.now() - debut.current, {reponse_libre:qcm && choisi!==null ? carte.choix?.[choisi]?.texte ?? "" : reponse,attendus_coches:attendusCoches});
      } else if (!revele && qcm && ["1", "2", "3", "4"].includes(e.key)) {
        const choix = Number(e.key) - 1;
        if (carte.choix?.[choix]) {
          e.preventDefault();
          setChoisi(choix);
          setRevele(true);
          if (choix === correct) {
            setEclat(true);
            setExpGagnee(15);
          }
        }
      } else if (!revele && !qcm && (e.key === " " || e.key === "Enter") && cible?.tagName !== "BUTTON") {
        e.preventDefault(); setRevele(true);
      }
    }
    window.addEventListener("keydown", clavier);
    return () => window.removeEventListener("keydown", clavier);
  }, [carte.choix, confiance, correct, enregistre, enregistrement, qcm, revele, choisi, reponse, attendusCoches]);

  return <>
    <article className={`salle-carte salle-carte-${carte.type}`}>
      <div className="salle-type"><Icone size={18} /><span>{TYPES_CARTE[carte.type] ?? carte.type}</span>
        <span>{NIVEAUX[carte.niveau] ?? carte.niveau}</span></div>
      <h1 ref={titre} tabIndex={-1} className="salle-question font-titre text-xl">{carte.question}</h1>
      {image ? (
        <figure className="salle-image relative group overflow-hidden">
          <img
            src={image.fichier}
            alt={image.alt}
            onError={() => setImageAbsente(true)}
            style={zoomImage > 1 ? { transform: `scale(${zoomImage})`, transformOrigin: "center" } : undefined}
            className="transition-transform duration-200"
          />
          {(carte.type === "photo" || carte.type === "plan") ? (
            <div className="absolute top-2 right-2 flex items-center rounded-lg border border-[var(--c-bordure-subtile)] bg-[var(--c-surface-elevee)] shadow-sm text-xs">
              <button
                type="button"
                onClick={() => setZoomImage((z) => Math.max(1, +(z - 0.35).toFixed(2)))}
                disabled={zoomImage <= 1}
                className="p-1.5 text-[var(--c-encre-2)] hover:text-[var(--c-encre)] disabled:opacity-30 transition"
                title="Zoom arrière"
              >
                <ZoomOut size={13} />
              </button>
              <button
                type="button"
                onClick={() => setZoomImage(1)}
                className="px-2 py-0.5 font-mono text-[11px] text-[var(--c-encre)] border-x border-[var(--c-bordure-subtile)]"
              >
                {Math.round(zoomImage * 100)}%
              </button>
              <button
                type="button"
                onClick={() => setZoomImage((z) => Math.min(2.4, +(z + 0.35).toFixed(2)))}
                disabled={zoomImage >= 2.4}
                className="p-1.5 text-[var(--c-encre-2)] hover:text-[var(--c-encre)] disabled:opacity-30 transition"
                title="Zoom avant"
              >
                <ZoomIn size={13} />
              </button>
            </div>
          ) : null}
          {image.credit ? <figcaption>{image.credit}</figcaption> : null}
          {imageAbsente ? <p role="status">{LIB.imageIndisponible}</p> : null}
        </figure>
      ) : null}

      {carte.type === "role" ? (
        <ModuleRole
          carte={carte}
          reponse={reponse}
          surChangementReponse={setReponse}
          revele={revele}
        />
      ) : carte.type === "relier" ? (
        <ModuleRelier
          carte={carte}
          reponse={reponse}
          surChangementReponse={setReponse}
          revele={revele}
        />
      ) : carte.type === "datation" ? (
        <ModuleDatation
          carte={carte}
          reponse={reponse}
          surChangementReponse={setReponse}
          revele={revele}
        />
      ) : (carte.type === "synthese" || carte.type === "cas") ? (
        <ModuleSynthese
          attendusCoches={attendusCoches}
          surChangementAttendus={setAttendusCoches}
          carte={carte}
          reponse={reponse}
          surChangementReponse={setReponse}
          revele={revele}
        />
      ) : qcm ? (
        <ul className="salle-choix relative">
          {expGagnee ? (
            <ToastExp
              montant={expGagnee}
              visible={expGagnee > 0}
              surFin={() => setExpGagnee(null)}
              classe="-top-10 left-1/2 -translate-x-1/2"
            />
          ) : null}
          {carte.choix?.map((c, i) => <li key={i}>
            <button type="button" disabled={revele || enregistrement} onClick={() => {
              setChoisi(i);
              setRevele(true);
              if (i === correct) {
                setEclat(true);
                setExpGagnee(15);
              }
            }}
              className={`salle-choix-bouton relative${revele && i === correct ? " est-juste" : revele && i === choisi ? " est-faux" : ""}`}>
              {revele && i === correct && i === choisi ? <EclatParticules nombre={18} duree={650} /> : null}
              <span className="salle-choix-repere">{revele && i === correct ? <Check size={18} />
                : revele && i === choisi ? <X size={18} /> : i + 1}</span><span>{c.texte}</span>
            </button>
          </li>)}
        </ul>
      ) : carte.type !== "flash" ? (
        <div className="salle-reponse-libre">
          <label htmlFor="reponse-carte">{LIB.taReponse}</label>
          <textarea id="reponse-carte" maxLength={5000} rows={4} value={reponse} readOnly={revele}
            onChange={(e) => setReponse(e.target.value)} />
        </div>
      ) : null}

      {!revele ? <div className="salle-reveler">
        <label className="salle-confiance"><input type="checkbox" checked={confiance}
          onChange={(e) => setConfiance(e.target.checked)} />{LIB.jetaisSur}</label>
        {!qcm ? <Bouton primaire disabled={enregistrement} onClick={() => setRevele(true)}
          enfants={<>{LIB.reveler}<ArrowRight size={18} /></>} /> : null}
      </div> : <VoletGlissant ouvert={revele}><div className="salle-retour" aria-live="polite">
        <h2 className={qcm && choisi !== correct ? "salle-faux" : "salle-juste"}>
          {qcm ? <>{choisi === correct ? <Check size={20} /> : <X size={20} />}
            {voix(choisi === correct ? "reponse.juste" : "reponse.fausse", {}, graine)}</> : LIB.correction}
        </h2>
        <p>{carte.reponse}</p>
        {qcm && choisi !== null && choisi !== correct && carte.choix?.[choisi]?.pourquoi_faux
          ? <p>{carte.choix[choisi]?.pourquoi_faux}</p> : null}
        {carte.explication ? <p>{carte.explication}</p> : null}
        {carte.vigilance ? <p className="salle-vigilance"><strong>{LIB.vigilance}.</strong> {carte.vigilance}</p> : null}
        {qcm && confiance && choisi !== correct ? <p>{voix("reponse.confiante", {}, graine)}</p> : null}
      </div></VoletGlissant>}
    </article>
    {revele ? <>
      <div className="salle-notes relative" aria-busy={enregistrement}>
        {expGagnee ? (
          <ToastExp
            montant={expGagnee}
            visible={expGagnee > 0}
            surFin={() => setExpGagnee(null)}
            classe="-top-12 left-1/2 -translate-x-1/2"
          />
        ) : null}
        {eclat ? <EclatParticules nombre={26} duree={750} onFin={() => setEclat(false)} /> : null}
        {([LIB.note1, LIB.note2, LIB.note3, LIB.note4] as const).map((libelle, i) =>
          <Bouton key={libelle} primaire={i === 2} disabled={enregistrement}
            className={`bouton-tactile salle-note-${i + 1}`}
            onClick={() => {
              const gain = (i === 3 ? 30 : i === 2 ? 20 : i === 1 ? 10 : 5);
              setExpGagnee(gain);
              if (i >= 2) setEclat(true);
              void enregistre((i + 1) as 1 | 2 | 3 | 4, confiance, Date.now() - debut.current, {reponse_libre:qcm && choisi!==null ? carte.choix?.[choisi]?.texte ?? "" : reponse,attendus_coches:attendusCoches});
            }}
            enfants={libelle} />)}
      </div>
      <Sources carte={carte} graine={graine} enregistrement={enregistrement}
        signale={() => void enregistre("signalement")} />
    </> : null}
  </>;
}

function imageDe(carte: Carte): { fichier: string; alt: string; credit: string } | null {
  if (!carte.image || typeof carte.image !== "object") return null;
  const image = carte.image as Record<string, unknown>;
  if (typeof image.fichier !== "string" || !/^images\/[A-Za-z0-9._/-]+$/.test(image.fichier)
    || image.fichier.split("/").includes("..")) return null;
  return {
    fichier: `/academie/${image.fichier}`,
    alt: typeof image.alt === "string" && image.alt.trim() ? image.alt : `${LIB.illustrationCarte} : ${carte.question}`,
    credit: typeof image.credit === "string" ? image.credit : "",
  };
}

export function ligneProvenance(carte: Carte): string {
  const p = carte.provenance;
  if (!p) return "";
  const morceaux: string[] = [];
  const auteur = p.modele ?? (p.auteur === "humain" ? "humain" : undefined) ?? p.par;
  const quand = p.genere_le ?? p.le;
  if (auteur) morceaux.push(quand ? `${auteur}, ${quand}` : String(auteur));
  else if (quand) morceaux.push(String(quand));
  if (typeof p.sources_concordantes === "number" && p.sources_concordantes > 0) {
    morceaux.push(`${p.sources_concordantes} ${LIB.sourcesConcordantes}`);
  }
  if (carte.verifie_par) morceaux.push(`${LIB.relueLe} ${carte.verifie} · ${typeof carte.verifie_par === "string" ? carte.verifie_par : "passe indépendante"}`);
  return morceaux.length ? `${LIB.provenance} : ${morceaux.join(" · ")}` : "";
}

function Sources({ carte, graine, enregistrement, signale }: {
  carte: Carte; graine: number; enregistrement: boolean; signale: () => void;
}) {
  const sources = carte.source ?? [];
  const provenance = ligneProvenance(carte);
  return <details className="salle-sources">
    <summary><BookOpen size={18} /><span>{LIB.sources}</span>
      {carte.note_confiance ? <span aria-label={`${LIB.noteConfiance} ${carte.note_confiance}`}>{carte.note_confiance}</span> : null}
      <ChevronDown size={16} /></summary>
    <div className="salle-dossier">
      <p className="text-encre-2">{LIB.verifieLe} {carte.verifie}</p>
      {sources.length && !carte.provenance?.sans_source ? <ul>{sources.map((source, i) => {
        const parti = (source as typeof source & { parti?: string }).parti;
        const url = source.url && /^https?:\/\//.test(source.url) ? source.url : null;
        return <li key={i}>{url ? <a href={url} target="_blank" rel="noopener noreferrer">
          {source.texte}<ExternalLink size={14} aria-hidden="true" /></a> : <span>{source.texte}</span>}
          {source.nature ? <small>{source.nature}{parti ? ` · ${parti}` : ""}</small> : null}</li>;
      })}</ul> : <p>{voix("source.sans_source", {}, graine)}</p>}
      {carte.a_recouper ? <p>{voix("source.a_recouper", {}, graine)}</p> : null}
      {provenance ? <p className="text-encre-2">{provenance}</p> : null}
      <div className="salle-dossier-actions">
        <Bouton disabled={enregistrement} onClick={signale} enfants={<><Flag size={16} />{LIB.carteFausse}</>} />
        <a href={`#/confiance/${carte.domaine}`}>{LIB.confiance}<ArrowRight size={16} /></a>
      </div>
    </div>
  </details>;
}

import { clePrivee } from "../app/compte";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { ArrowLeft, ArrowRight, Check, Lightbulb, ExternalLink } from "lucide-react";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import type { Carte, Lecon, LigneJournal, Source } from "../donnees/types";
import { etudeDisponible, repriseEtude } from "../moteur/etude";
import { SupportEtude } from "./SupportEtude";
import {ModuleRelier,ModuleRole,ModuleDatation} from "./ModulesSeance";

export function Etude({ id }: {id: string}) {
  const { banque, journal, jour } = useMagasin();
  const lecon = banque?.etudes?.lecons[id];
  if (!banque || !lecon || !etudeDisponible(lecon, banque.cartes, journal, jour)) return <section className="etude-indisponible"><h1>Cette étude est en vérification</h1><p>Une source ou une carte demande une nouvelle vérification. Tes réponses restent dans ton journal.</p><button className="action-etude" onClick={() => va("/")}>Retour à l’accueil</button></section>;
  return <SalleEtude key={`${id}-${lecon.version}`} lecon={lecon} cartes={lecon.cartes.map(cid => banque.cartes.find(c => c.id === cid)).filter((c): c is Carte => c !== undefined)} />;
}

function SalleEtude({lecon, cartes}: {lecon: Lecon; cartes: Carte[]}) {
  const { banque, journal, note, bilan } = useMagasin();
  const reprise = repriseEtude(lecon, journal);
  const [etape, setEtape] = useState(reprise.etape);
  const [index, setIndex] = useState(reprise.index);
  const [texte, setTexte] = useState("");
  const [aide, setAide] = useState(false);
  const [confiance, setConfiance] = useState(false);
  const [revelee, setRevelee] = useState(false);
  const [choix, setChoix] = useState<number | null>(null);
  const [coches, setCoches] = useState<number[]>([]);
  const [occupe, setOccupe] = useState(false);
  const [erreur, setErreur] = useState("");
  const [supportCharge, setSupportCharge] = useState<string | null>(null);
  const titre = useRef<HTMLHeadingElement>(null);
  const verrou = useRef(false);
  const parcours = banque?.etudes?.parcours.find(p => p.chapitres.includes(lecon.id));
  const prochaineId = parcours?.chapitres[(parcours.chapitres.indexOf(lecon.id) ?? -1) + 1];
  const exercices = cartes.filter(c => c.type !== "synthese");
  const originale = exercices[index];
  const decalage = originale ? Array.from(originale.id).reduce((n,c) => n + c.charCodeAt(0),0) % (originale.choix?.length || 1) : 0;
  const carte: Carte | undefined = originale ? {...originale, choix: originale.choix ? [...originale.choix.slice(decalage), ...originale.choix.slice(0,decalage)] : undefined} : undefined;
  const supportNecessaire = Boolean(carte && (Object.hasOwn(carte, 'image') || ['photo', 'plan'].includes(carte.type)));
  const cleBrouillon = clePrivee(`academie-etude-brouillon:${lecon.id}:${lecon.version}:${etape}:${index}`);
  useEffect(() => {
    try {
      const b = JSON.parse((localStorage.getItem(cleBrouillon) ?? sessionStorage.getItem(cleBrouillon)) ?? "{}");
      setTexte(typeof b.texte === "string" ? b.texte : ""); setAide(b.aide === true);
      setChoix(typeof b.choix === "number" ? b.choix : null); setConfiance(b.confiance === true); setRevelee(b.revelee === true);
      const indices:number[]=Array.isArray(b.coches) ? b.coches.filter((i:unknown):i is number=>
        typeof i === "number" && Number.isInteger(i) && i>=0 && i<lecon.synthese.attendus.length) : [];
      setCoches([...new Set(indices)].sort((a,b)=>a-b));
    } catch { setTexte(""); setAide(false); setChoix(null); setConfiance(false); setRevelee(false); setCoches([]); }
    titre.current?.focus({preventScroll:true});
    window.scrollTo(0,0);
  }, [cleBrouillon]);
  useEffect(() => {
    const echap = (e: KeyboardEvent) => { if (e.key === "Escape" && !verrou.current) va("/"); };
    window.addEventListener("keydown", echap); return () => window.removeEventListener("keydown", echap);
  }, []);
  function brouillon(changement: {texte?:string; aide?:boolean; choix?:number; confiance?:boolean; revelee?:boolean; coches?:number[]}) {
    const b = {texte, aide, choix, confiance, revelee, coches, ...changement};
    setTexte(b.texte); setAide(b.aide); setChoix(b.choix); setConfiance(b.confiance); setRevelee(b.revelee); setCoches(b.coches);
    try { localStorage.setItem(cleBrouillon,JSON.stringify(b)); } catch { /* brouillon en mémoire */ }
  }
  function ecritTexte(t: string) { brouillon({texte:t}); }
  async function enregistre(suite: string, champs: Partial<LigneJournal> = {}, prochainIndex = index) {
    if (verrou.current) return;
    verrou.current = true; setOccupe(true); setErreur("");
    try {
      await note({mode:"synthese", chapitre:lecon.id, attendus_coches:coches, format:"etude", contenu_version:lecon.version, etude_etape:suite, exercice_index:prochainIndex, reponse_libre:texte, aide_utilisee:aide, confiance, ...champs});
      try { localStorage.removeItem(cleBrouillon); sessionStorage.removeItem(cleBrouillon); } catch { /* réponse déjà dans le journal */ }
      setEtape(suite); setIndex(prochainIndex); setRevelee(false); setChoix(null); setAide(false); setCoches([]);
    } catch { setErreur("Ta réponse n’a pas pu être enregistrée. Réessaie avant de quitter."); }
    finally { verrou.current = false; setOccupe(false); }
  }
  async function noteCarte(noteFsrs: 1 | 2 | 3 | 4) {
    if (!carte || (supportNecessaire && supportCharge !== carte.id)) return;
    await enregistre(index + 1 < exercices.length ? "exercices" : "synthese", {
      mode: aide ? "synthese" : "revision", carte:carte.id,
      ...(aide ? {} : {note:noteFsrs}), reponse_libre:carte.choix?.[choix ?? -1]?.texte ?? texte,
    }, index + 1);
  }
  const numero = etape === "tentative" ? 1 : etape === "principe" ? 2 : etape === "exercices" ? 3 : 4;
  const source = <DossierSources sources={lecon.sources} lecon={lecon} />;
  return <div className="salle-etude" style={{"--c-accent":accentDuRang(parcours?.rang ?? 1)} as CSSProperties}>
    <header className="etude-barre"><button className="sortie-etude" disabled={occupe} onClick={() => va("/")} aria-label="Quitter l’étude"><ArrowLeft size={20} /><span>Reprendre plus tard</span></button><span>{parcours?.titre}</span><span>Étude</span></header>
    <ol className="etude-fil" aria-label="Étapes de l’étude">{["Tenter", "Comprendre", "Pratiquer", "Expliquer"].map((e,i) => <li key={e} aria-current={i + 1 === numero ? "step" : undefined}><span>{i + 1 < numero ? <Check size={13} /> : i + 1}</span>{e}</li>)}</ol>
    <div className="etude-corps">
      <h1 ref={titre} tabIndex={-1}>{lecon.titre}</h1>
      {etape === "tentative" && <>
        <p className="etude-intro">Commence avec ce que tu sais. Tu pourras demander un indice.</p>
        <h2 className="question-etude">{lecon.amorce.question.replace(/\s+([;?!:])/g,"\u202f$1")}</h2>
        <label className="reponse-etude">Ta réponse<textarea value={texte} onChange={e => ecritTexte(e.target.value)} rows={4} maxLength={5000} placeholder="Pose ton raisonnement, même incomplet." /></label>
        <label className="confiance-etude"><input type="checkbox" checked={confiance} onChange={e => brouillon({confiance:e.target.checked})} />Cette réponse te semble sûre</label>
        {aide ? <p className="indice-etude"><Lightbulb size={18}/>{lecon.amorce.aide}</p> : <button className="aide-etude" onClick={() => brouillon({aide:true})}><Lightbulb size={18}/>Un indice</button>}
        <div className="etude-actions"><button className="action-etude" disabled={!texte.trim() || occupe} onClick={() => void enregistre("principe")}>Confronter ma réponse<ArrowRight size={19}/></button><button className="lien-action" disabled={occupe} onClick={() => void enregistre("principe",{aide_utilisee:true,reponse_libre:"Sans réponse initiale"})}>Besoin des bases</button></div>
      </>}
      {etape === "principe" && <>
        <section className="retour-amorce"><h2>Le principe</h2><p>{lecon.amorce.reponse_attendue}</p><details><summary>Retrouver ta première réponse</summary><p>{journal.filter(l => l.chapitre === lecon.id && l.contenu_version === lecon.version && l.etude_etape === "principe").at(-1)?.reponse_libre}</p></details></section>
        <article className="lecon-texte">{lecon.lecon.split("\n\n").map((p,i) => <p key={i}>{p}</p>)}</article>
        {source}
        <div className="etude-actions"><button className="action-etude" disabled={occupe} onClick={() => void enregistre("exercices",{},0)}>Mettre en pratique<ArrowRight size={19}/></button></div>
      </>}
      {etape === "exercices" && carte && <>
        <p className="etude-intro">Question {index + 1} sur {exercices.length} · {carte.type === "qcm" ? "Décider" : "Rappeler sans aide"}</p>
        <h2 className="question-etude">{carte.question}</h2>
        {supportNecessaire && <SupportEtude key={carte.id} image={carte.image} onCharge={ok => setSupportCharge(ok ? carte.id : null)} />}
        {carte.choix ? <div className="etude-choix">{carte.choix.map((c,i) => <button key={i} aria-pressed={choix === i} disabled={revelee} onClick={() => brouillon({choix:i})}><span>{String.fromCharCode(65+i)}</span>{c.texte}</button>)}</div>
          : carte.type === "relier" ? <ModuleRelier key={carte.id} carte={carte} reponse={texte} surChangementReponse={ecritTexte} revele={revelee}/>
          : carte.type === "role" ? <ModuleRole key={carte.id} carte={carte} reponse={texte} surChangementReponse={ecritTexte} revele={revelee}/>
          : carte.type === "datation" ? <ModuleDatation key={carte.id} carte={carte} reponse={texte} surChangementReponse={ecritTexte} revele={revelee}/>
          : <label className="reponse-etude">Ta réponse<textarea disabled={revelee} rows={3} maxLength={5000} value={texte} onChange={e => ecritTexte(e.target.value)} /></label>}
        {!revelee ? <><button className="aide-etude" onClick={() => brouillon({aide:true})}><Lightbulb size={18}/>Un indice</button>{aide && <p className="indice-etude">{String(carte.aide ?? "Identifie la règle qui change la décision, puis l’information manquante.")}</p>}<div className="etude-actions"><button className="action-etude" disabled={supportNecessaire && supportCharge !== carte.id || (carte.choix ? choix === null : !texte.trim())} onClick={() => brouillon({revelee:true})}>Voir le retour<ArrowRight size={19}/></button></div></>
          : <section className="retour-etude" aria-live="polite"><h3>{carte.choix ? carte.choix[choix ?? -1]?.correct ? "C’est ça." : "À reprendre." : "Compare ton raisonnement"}</h3><p>{carte.reponse}</p><p>{carte.explication}</p>{carte.choix && !carte.choix[choix ?? -1]?.correct && <p>{carte.choix[choix ?? -1]?.pourquoi_faux}</p>}{source}
            <p className="etude-intro">{aide ? "Réponse avec indice : aucun rappel autonome n’est crédité." : "Comment ce rappel s’est-il passé ?"}</p>{aide ? <button className="action-etude" disabled={occupe} onClick={() => void noteCarte(1)}>Continuer avec cette aide</button> : <div className="etude-notes">{(["À revoir", "Difficile", "Bien", "Évident"] as const).map((n,i) => <button key={n} disabled={occupe} onClick={() => void noteCarte(carte.choix && !carte.choix[choix ?? -1]?.correct ? 1 : (i + 1) as 1|2|3|4)}>{n}</button>)}</div>}</section>}
      </>}
      {etape === "synthese" && <>
        <p className="etude-intro">Une situation nouvelle. Écris sans ouvrir la leçon.</p><h2 className="question-etude">{lecon.synthese.consigne}</h2>
        <label className="reponse-etude">Ta réponse<textarea rows={6} maxLength={5000} value={texte} onChange={e => ecritTexte(e.target.value)} placeholder="Explique ta décision et ce qui reste à vérifier." /></label>
        <div className="etude-actions"><button className="action-etude" disabled={!texte.trim() || occupe} onClick={() => void enregistre("grille")}>Comparer à la grille<ArrowRight size={19}/></button></div>
      </>}
      {etape === "grille" && <>
        <h2 className="question-etude">Ce que ta réponse doit faire apparaître</h2>
        <p className="reponse-conservee">{reprise.reponse}</p><p>Coche uniquement ce que tu avais écrit. Cette autoévaluation ne certifie pas une compétence.</p>
        <div className="grille-etude">{lecon.synthese.attendus.map((a,i) => <label key={i}><input type="checkbox" checked={coches.includes(i)} onChange={e => brouillon({coches:e.target.checked ? [...coches,i].sort((a,b)=>a-b) : coches.filter(n => n !== i)})}/>{a}</label>)}</div>{source}
        <div className="etude-actions"><button className="action-etude" disabled={occupe} onClick={() => void enregistre("terminee",{reponse_libre:reprise.reponse})}>Garder cette étape<Check size={19}/></button></div>
      </>}
      {etape === "terminee" && <section className="etude-cloture"><span className="sceau-etude"><Check size={32}/></span><h2>Un peu plus clair.<br /><em>À faire revenir.</em></h2><p>Tu as parcouru cette étude. Tes rappels sont planifiés à partir de tes réponses.</p><p className="etude-intro">Ce qui reste à froid et se transfère : non mesuré.</p><div className="etude-actions">{prochaineId ? <button className="action-etude" onClick={() => va(`/salle/etude/${prochaineId}`)}>Continuer le parcours<ArrowRight size={19}/></button> : <button className="action-etude" onClick={() => va("/")}>Retour au parcours<ArrowRight size={19}/></button>}<button className="lien-action" onClick={() => void enregistre("tentative",{},0)}>Recommencer l’étude</button></div></section>}
      {erreur && <p role="alert">{erreur}</p>}
      <footer className="etude-sauvegarde">{bilan?.erreur || bilan?.horsLigne ? "Conservé sur cet appareil · synchronisation en attente" : "Tes réponses sont conservées sur cet appareil"}</footer>
    </div>
  </div>;
}
function DossierSources({sources,lecon}: {sources: Source[]; lecon: Lecon}) {
  const natures:Record<string,string>={"texte-officiel":"Texte officiel",jurisprudence:"Jurisprudence",institution:"Institution",norme:"Norme",doctrine:"Doctrine",editeur:"Éditeur","presse-pro":"Presse professionnelle","organisation-pro":"Organisation professionnelle",association:"Association","support-interne":"Support interne",terrain:"Terrain"};
  return <details className="sources-etude"><summary>Sources et fabrication</summary>
    <ul>{sources.map((s,i) => <li key={i}>
      <span>{s.nature?.trim() ? Object.hasOwn(natures,s.nature) ? natures[s.nature] : s.nature : "Nature non renseignée"}</span>
      {s.url && /^https:\/\//.test(s.url) ? <a href={s.url} target="_blank" rel="noreferrer">{s.texte}<ExternalLink size={13}/></a> : s.texte}
      {s.parti?.trim() && <p>{s.parti}</p>}
    </li>)}</ul>
    <p>Écrit par {lecon.provenance.modele ?? "auteur non renseigné"} · {lecon.provenance.genere_le}. Relecture : {lecon.verifie_par.modele}, {lecon.verifie_par.date}.</p>
    <p>Les sources étayent le contenu. Les situations fictives et l’ordre des exercices sont des choix pédagogiques.</p>
  </details>;
}

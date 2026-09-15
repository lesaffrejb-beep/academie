import { useEffect, useRef, useState, type ReactNode, type FormEvent } from "react";
import { ArrowRight, BookOpen, Check, ArrowLeft } from "lucide-react";
import { useRoute, va } from "../../app/routage";
import { Reprise } from "./Reprise";
import { api } from "../../donnees/api";
import { type Compte, poseCompte, memoriseCompte, compteMemorise, oublieCompte, valideCompte } from "../../app/compte";
import { ouvreCompte, ecris, litJournal, synchronise } from "../../moteur/journal";
import { chargeBanque } from "../../donnees/banque";
import { ChoixTheme } from "../ChoixTheme";
import "./arrivee.css";

interface Parcours { cle:string; titre:string; chapitres:number; chapitres_ecrits:number; cartes_jouables:number }
export function PorteCompte({enfants}:{enfants:ReactNode}) {
  const route=useRoute();
  const [compte, setCompte] = useState<Compte|null>(null);
  const [charge, setCharge] = useState(true);
  useEffect(() => { let vivant = true; void api.profil().then(r => {
    if (!vivant) return;
    const c = r.ok && r.valeur?.id ? r.valeur : !r.ok && r.code === "hors_ligne" ? compteMemorise() : null;
    if (c) {poseCompte(c);ouvreCompte(c.id);setCompte(c);memoriseCompte(c);}
    else if (!r.ok && r.statut === 401) oublieCompte(false);
    setCharge(false);
  }); return () => {vivant=false;}; }, []);
  useEffect(() => {const ferme = (e:StorageEvent) => {if (e.key === "academie-session-fermee") window.location.reload();};window.addEventListener("storage",ferme);return () => window.removeEventListener("storage",ferme);},[]);
  const entree = (c:Compte) => {memoriseCompte(c);poseCompte(c); ouvreCompte(c.id);setCompte(c);};
  if (charge) return <main className="arrivee"><p>Ouverture de ton espace…</p></main>;
  if (!compte || compte.compte_personnel===false || !compte.cursus || route.nom==="arrivee") return <Arrivee compte={compte} surCompte={entree} />;
  return <>{enfants}</>;
}
function Arrivee({compte,surCompte}:{compte:Compte|null;surCompte:(c:Compte)=>void}) {
  const [mode,setMode]=useState<"creation"|"connexion"|"recuperation">("creation");
  const [comptes,setComptes]=useState<{pseudo:string;titre_affiche:string}[]>([]);
  const [compteCree,setCompteCree]=useState<Compte|null>(null);
  const [cursusChoisi,setCursusChoisi]=useState("");
  const motDePasse=useRef<HTMLInputElement>(null);
  const personnel=Boolean(compte?.compte_personnel && compte.cursus);
  const [secours,setSecours]=useState("");
  const [phrase,setPhrase]=useState(""); const [pseudo,setPseudo]=useState(""); const [cle,setCle]=useState(""); const [cleAffichee,setCleAffichee]=useState("");
  const [catalogue,setCatalogue]=useState<Parcours[]>([]); const [erreur,setErreur]=useState("");
  const [occupe,setOccupe]=useState(false); const [demande,setDemande]=useState(false); const [texte,setTexte]=useState(""); const [envoyee,setEnvoyee]=useState(false);
  useEffect(() => {void fetch(`${import.meta.env.BASE_URL}catalogue.json`).then(r => {if (!r.ok) throw Error(); return r.json();}).then(d => setCatalogue(d.parcours)).catch(() => setErreur("Le catalogue est indisponible. Recharge la page."));},[]);
  useEffect(() => {if (!compte) void api.comptesConnexion().then(r => {
    if (r.ok && Array.isArray(r.valeur?.comptes)) setComptes(r.valeur.comptes);
  });},[compte]);
  async function soumet(e:FormEvent) {
    e.preventDefault(); if (occupe) return;
    const refus = valideCompte(phrase,pseudo) || (mode === "creation" && (secours.length < 12 || secours === phrase) ? "Choisis une phrase de récupération distincte du mot de passe, avec au moins 12 caractères." : "");
    if (refus) {setErreur(refus);return;}
    if (mode === "creation" && !cursusChoisi) {setErreur("Choisis ton cursus pour commencer.");return;}
    setOccupe(true);setErreur("");
    const r = await (mode === "connexion" ? api.connexion(pseudo,phrase) : mode === "recuperation" ? api.recuperation(pseudo,cle,phrase) : api.inscription(pseudo,phrase,secours));
    setOccupe(false);setPhrase("");setSecours("");
    if (!r.ok) {setErreur(r.motif);return;}
    if (!r.valeur?.id) {setErreur("Le serveur n’a pas confirmé ton compte.");return;}
    const {cle_recuperation:cleRecue,...identite} = r.valeur as Compte & {cle_recuperation?:unknown};
    if (typeof cleRecue === "string") {
      setCompteCree(identite);setCleAffichee(cleRecue);setCle("");
    } else {surCompte(identite);if(identite.cursus) va("/");else if(cursusChoisi) await choisit(cursusChoisi,identite);}
  }
  async function confirmeCle() {
    if (!compteCree || occupe) return;
    setCleAffichee("");setCompteCree(null);surCompte(compteCree);
    if (compteCree.cursus) va("/");
    else if (cursusChoisi) await choisit(cursusChoisi,compteCree);
  }
  async function choisit(cle:string,identite:Compte|null=compte) {
    if (!identite || occupe) return;
    setOccupe(true);setErreur("");
    try {
      const ancien = (await litJournal()).filter(l => l.mode === "cursus").at(-1);
      if (ancien?.cursus !== cle) await ecris({mode:"cursus",cursus:cle});
      const bilan = await synchronise();
      if (bilan.horsLigne || bilan.erreur || bilan.enAttente) {setErreur(bilan.erreur?.motif ?? "Connexion nécessaire pour confirmer ton cursus. Ton choix est conservé ici.");return;}
      const r=await api.profil();
      if (!r.ok || r.valeur.cursus !== cle) {setErreur("Le cursus n’est pas encore confirmé par le serveur.");return;}
      const b = await chargeBanque();
      const premiere = b.etudes?.parcours.find(p => p.metier === cle)?.chapitres[0];
      window.location.hash = premiere ? `#/salle/etude/${premiere}` : "#/";
      surCompte(r.valeur);
      if (identite.cursus) {window.location.hash="#/";window.location.reload();}
    } catch {setErreur("La sauvegarde locale n’est pas disponible. Vérifie les réglages du navigateur.");}
    finally {setOccupe(false);}
  }
  async function changeCompte() {
    setOccupe(true);setErreur("");const r=await api.deconnexion();setOccupe(false);
    if(!r.ok) {setErreur(r.motif);return;}
    oublieCompte();window.location.hash="#/arrivee";window.location.reload();
  }
  async function depose(e:FormEvent) {e.preventDefault();setOccupe(true);setErreur(""); const r=await api.demandeCursus(texte);setOccupe(false);if (!r.ok) setErreur(r.motif);else {setEnvoyee(true);setTexte("");}}
  return <div className="arrivee-page"><header className="arrivee-entete"><a href="#/">Académie</a><ChoixTheme /></header><main className="arrivee">
    <aside className="arrivee-intro"><BookOpen size={36} strokeWidth={1.2}/><p className="arrivee-repere">Ton métier, un peu plus loin.</p><h1>{personnel ? "Ton compte, ton parcours." : compte ? "Choisis où commencer." : "Un espace pour apprendre. Le tien."}</h1><p>Un cas pour réfléchir. Des sources pour comprendre. Des questions pour faire revenir ce qui compte.</p><ul><li><Check size={18}/> Tes réponses et ta progression restent dans ton espace.</li><li><Check size={18}/> Tu retrouves ton cursus en te reconnectant.</li><li><Check size={18}/> Tu choisis si les autres élèves te voient.</li></ul></aside>
    <section className="arrivee-formulaire" aria-label={personnel || !compte ? "Compte" : "Choix du cursus"}>
      {erreur && <p role="alert" className="arrivee-erreur">{erreur}</p>}
      {cleAffichee ? <><h2>Garde ta clé de récupération.</h2><p>Copie-la dans un gestionnaire de mots de passe ou un fichier local hors de l’Académie. Elle n’apparaîtra plus après cet écran.</p><output className="arrivee-cle">{cleAffichee}</output><p className="arrivee-detail">Si tu perds ta phrase secrète et cette clé, ton compte ne pourra pas être récupéré.</p><button className="action-etude" disabled={occupe} onClick={()=>void confirmeCle()}>J’ai enregistré ma clé<ArrowRight size={19}/></button></> : personnel && compte ? <><h2>{compte.titre_affiche}</h2><p>Ton compte est connecté. Tes réponses validées se synchronisent dans ton espace personnel.</p><div className="compte-actions"><button className="action-etude" onClick={()=>va("/")}>Continuer mon parcours<ArrowRight size={19}/></button><button onClick={()=>va("/arbre")}>Voir mon arbre</button><button onClick={()=>va("/eleves")}>Mes sauvegardes et les élèves</button><button disabled={occupe} onClick={()=>void changeCompte()}>Utiliser un autre compte</button></div><h3>Mes cursus</h3><p>Un seul cursus s’affiche à la fois. Ajouter un cursus conserve toutes tes réponses.</p><div className="arrivee-cursus">{catalogue.map(p=><button key={p.cle} disabled={occupe || compte.cursus===p.cle} onClick={()=>void choisit(p.cle)}><strong>{p.titre}</strong><span>{compte.cursus===p.cle ? "Cursus actif" : compte.cursus_inscrits?.includes(p.cle) ? "Reprendre ce cursus" : "Ajouter et commencer"}</span></button>)}</div><Reprise pseudo={compte.titre_affiche}/></> : !compte ? <><div className="arrivee-modes"><button aria-pressed={mode==="creation"} onClick={() => {setMode("creation");setErreur("");}}>Créer mon compte</button><button aria-pressed={mode==="connexion"} onClick={() => {setMode("connexion");setErreur("");}}>Me connecter</button><button aria-pressed={mode==="recuperation"} onClick={() => {setMode("recuperation");setErreur("");}}>Retrouver mon accès</button></div>{comptes.length > 0 && mode !== "recuperation" && <div className="arrivee-comptes" aria-label="Comptes de cette Académie"><p>Déjà inscrit ? Choisis ton nom.</p>{comptes.map(c=><button key={c.pseudo} type="button" disabled={occupe} onClick={()=>{setMode("connexion");setPseudo(c.pseudo);setPhrase("");setErreur("");motDePasse.current?.focus();}}>{c.titre_affiche}</button>)}</div>}<h2>{mode === "connexion" ? "Retrouver ton espace" : mode === "recuperation" ? "Choisir un nouveau mot de passe" : "Bienvenue à l’Académie"}</h2><form onSubmit={e => void soumet(e)}>
        <label>Ton pseudo<input value={pseudo} onChange={e=>setPseudo(e.target.value)} maxLength={60} required autoComplete="username"/></label>
        {mode === "recuperation" && <label>Phrase ou clé de récupération<input value={cle} onChange={e=>setCle(e.target.value)} required autoComplete="off"/></label>}
        <label>{mode === "recuperation" ? "Nouveau mot de passe" : "Mot de passe"}<input ref={motDePasse} type="password" value={phrase} onChange={e=>setPhrase(e.target.value)} required minLength={12} maxLength={256} autoComplete={mode === "connexion" ? "current-password":"new-password"}/></label>
        {mode === "creation" && <label>Phrase secrète de récupération<input type="password" value={secours} onChange={e=>setSecours(e.target.value)} minLength={12} maxLength={256} required autoComplete="off"/></label>}
        {mode === "creation" && <fieldset className="arrivee-choix"><legend>Ton cursus</legend>{catalogue.map(p=><label key={p.cle}><input type="radio" name="cursus" value={p.cle} checked={cursusChoisi===p.cle} onChange={()=>setCursusChoisi(p.cle)} required/><span><strong>{p.titre}</strong><small>{p.chapitres_ecrits} études disponibles · {p.cartes_jouables} cartes</small></span></label>)}</fieldset>}
        {mode === "creation" && <p className="arrivee-detail">Au moins 12 caractères. Ton pseudo sera proposé sur cet écran de connexion et ton cursus sera visible aux élèves. Tu peux te masquer dans Élèves. La phrase de récupération te permettra de remplacer un mot de passe oublié. Conserve-la séparément ; elle ne sera pas réaffichée.</p>}
        {mode === "recuperation" && <p className="arrivee-detail">Après ce changement, toutes les autres sessions seront fermées. Une nouvelle clé remplacera la phrase ou clé de récupération utilisée ; conserve-la.</p>}
        <button className="action-etude" disabled={occupe}>{occupe ? "Connexion en cours…" : mode === "connexion" ? "Me connecter" : mode === "recuperation" ? "Changer mon mot de passe" : "Créer mon espace"}<ArrowRight size={19}/></button>
      </form></> : <><h2>Bienvenue, {compte.titre_affiche}.</h2><p>Un cursus actif, une sauvegarde personnelle. Le programme indique l’horizon ; les études disponibles sont le contenu que tu peux essayer.</p>
      {!demande ? <div className="arrivee-cursus">{catalogue.map(p=><button key={p.cle} disabled={occupe} onClick={()=>void choisit(p.cle)}><strong>{p.titre}</strong><span>{p.chapitres_ecrits} études disponibles · {p.cartes_jouables} cartes</span><span>{p.chapitres} chapitres au programme</span><ArrowRight size={20}/></button>)}<button onClick={()=>setDemande(true)} disabled={occupe}><strong>Nouveau cursus</strong><span>Décrire à Jean-Baptiste ce que tu veux apprendre</span></button></div> : <form onSubmit={e=>void depose(e)}><button type="button" onClick={()=>setDemande(false)}><ArrowLeft size={16}/> Retour aux cursus</button><label>Ta situation et ton envie d’apprendre<textarea value={texte} onChange={e=>setTexte(e.target.value)} maxLength={2000} required rows={5}/></label><button className="action-etude" disabled={occupe || !texte.trim()}>Enregistrer la demande</button>{envoyee && <p role="status">Demande enregistrée pour Jean-Baptiste. Tu peux commencer un cursus disponible.</p>}</form>}
      <p className="arrivee-detail">La première étude commence par ta réponse à un cas. Elle ne mesure pas encore ton niveau.</p></>}
      {compte && !personnel && <button disabled={occupe} onClick={()=>void changeCompte()}>Utiliser un autre compte</button>}
    </section></main><footer className="arrivee-pied">Des sources à chaque étape. Ta progression t’appartient.</footer></div>;
}

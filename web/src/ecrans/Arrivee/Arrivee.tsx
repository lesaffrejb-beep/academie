import { useEffect, useState, type ReactNode, type FormEvent } from "react";
import { ArrowRight, BookOpen, Check, ArrowLeft } from "lucide-react";
import { api } from "../../donnees/api";
import { type Compte, poseCompte, memoriseCompte, compteMemorise, oublieCompte, valideCompte } from "../../app/compte";
import { ouvreCompte, ecris, litJournal, synchronise } from "../../moteur/journal";
import { chargeBanque } from "../../donnees/banque";
import { ChoixTheme } from "../ChoixTheme";
import "./arrivee.css";

interface Parcours { cle:string; titre:string; chapitres:number; chapitres_ecrits:number; cartes_jouables:number }
export function PorteCompte({enfants}:{enfants:ReactNode}) {
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
  if (!compte || !compte.cursus) return <Arrivee compte={compte} surCompte={entree} />;
  return <>{enfants}</>;
}
function Arrivee({compte,surCompte}:{compte:Compte|null;surCompte:(c:Compte)=>void}) {
  const [connexion,setConnexion]=useState(false);
  const [mail,setMail]=useState(""); const [mdp,setMdp]=useState(""); const [pseudo,setPseudo]=useState("");
  const [catalogue,setCatalogue]=useState<Parcours[]>([]); const [erreur,setErreur]=useState("");
  const [occupe,setOccupe]=useState(false); const [demande,setDemande]=useState(false); const [texte,setTexte]=useState(""); const [envoyee,setEnvoyee]=useState(false);
  useEffect(() => {void fetch(`${import.meta.env.BASE_URL}catalogue.json`).then(r => {if (!r.ok) throw Error(); return r.json();}).then(d => setCatalogue(d.parcours)).catch(() => setErreur("Le catalogue est indisponible. Recharge la page."));},[]);
  async function soumet(e:FormEvent) {
    e.preventDefault(); if (occupe) return;
    const refus = connexion ? "" : valideCompte(mail,mdp,pseudo);
    if (refus) {setErreur(refus);return;}
    setOccupe(true);setErreur("");
    const r = await (connexion ? api.connexion(mail,mdp) : api.inscription(mail,mdp,pseudo));
    setOccupe(false);setMdp("");
    if (!r.ok) {setErreur(r.motif);return;}
    if (!r.valeur?.id) {setErreur("Le serveur n’a pas confirmé ton compte.");return;}
    surCompte(r.valeur);
  }
  async function choisit(cle:string) {
    if (!compte || occupe) return;
    setOccupe(true);setErreur("");
    try {
      const ancien = (await litJournal()).find(l => l.mode === "cursus");
      if (ancien?.cursus && ancien.cursus !== cle) {setErreur("Un choix est déjà en attente de sauvegarde. Reprends ce cursus.");return;}
      if (!ancien) await ecris({mode:"cursus",cursus:cle});
      const bilan = await synchronise();
      if (bilan.horsLigne || bilan.erreur || bilan.enAttente) {setErreur(bilan.erreur?.motif ?? "Connexion nécessaire pour confirmer ton cursus. Ton choix est conservé ici.");return;}
      const r=await api.profil();
      if (!r.ok || r.valeur.cursus !== cle) {setErreur("Le cursus n’est pas encore confirmé par le serveur.");return;}
      const b = await chargeBanque();
      const premiere = b.etudes?.parcours.find(p => p.metier === cle)?.chapitres[0];
      window.location.hash = premiere ? `#/salle/etude/${premiere}` : "#/";
      surCompte(r.valeur);
    } catch {setErreur("La sauvegarde locale n’est pas disponible. Vérifie les réglages du navigateur.");}
    finally {setOccupe(false);}
  }
  async function depose(e:FormEvent) {e.preventDefault();setOccupe(true);setErreur(""); const r=await api.demandeCursus(texte);setOccupe(false);if (!r.ok) setErreur(r.motif);else {setEnvoyee(true);setTexte("");}}
  return <div className="arrivee-page"><header className="arrivee-entete"><a href="#/">Académie</a><ChoixTheme /></header><main className="arrivee">
    <aside className="arrivee-intro"><BookOpen size={36} strokeWidth={1.2}/><p className="arrivee-repere">Ton métier, un peu plus loin.</p><h1>{compte ? "Choisis où commencer." : "Un espace pour apprendre. Le tien."}</h1><p>Un cas pour réfléchir. Des sources pour comprendre. Des questions pour faire revenir ce qui compte.</p><ul><li><Check size={18}/> Tes réponses et ta progression restent dans ton espace.</li><li><Check size={18}/> Tu retrouves ton cursus en te reconnectant.</li><li><Check size={18}/> Tu choisis si les autres élèves te voient.</li></ul></aside>
    <section className="arrivee-formulaire" aria-label={compte ? "Choix du cursus" : "Compte"}>
      {erreur && <p role="alert" className="arrivee-erreur">{erreur}</p>}
      {!compte ? <><div className="arrivee-modes"><button aria-pressed={!connexion} onClick={() => {setConnexion(false);setErreur("");}}>Créer mon compte</button><button aria-pressed={connexion} onClick={() => {setConnexion(true);setErreur("");}}>Me connecter</button></div><h2>{connexion ? "Retrouver ton espace" : "Bienvenue à l’Académie"}</h2><form onSubmit={e => void soumet(e)}>
        {!connexion && <label>Ton pseudo<input value={pseudo} onChange={e=>setPseudo(e.target.value)} maxLength={60} required autoComplete="nickname"/></label>}
        <label>Adresse mail<input type="email" value={mail} onChange={e=>setMail(e.target.value)} required maxLength={254} autoComplete="email" inputMode="email"/></label>
        <label>Mot de passe<input type="password" value={mdp} onChange={e=>setMdp(e.target.value)} required minLength={connexion ? undefined : 12} maxLength={256} autoComplete={connexion ? "current-password":"new-password"}/></label>
        {!connexion && <p className="arrivee-detail">Au moins 12 caractères. Ton pseudo et ton cursus seront visibles aux élèves de cette Académie ; tu peux te masquer dans Élèves.</p>}
        <button className="action-etude" disabled={occupe}>{occupe ? "Connexion en cours…" : connexion ? "Me connecter" : "Créer mon espace"}<ArrowRight size={19}/></button>
        {connexion && <details><summary>Mot de passe oublié</summary><p>Demande à Jean-Baptiste un lien de secours à usage unique. L’envoi automatique de mails n’est pas encore disponible.</p></details>}
      </form></> : <><h2>Bienvenue, {compte.titre_affiche}.</h2><p>Un cursus actif, une sauvegarde personnelle. Le programme indique l’horizon ; les études disponibles sont le contenu que tu peux essayer.</p>
      {!demande ? <div className="arrivee-cursus">{catalogue.map(p=><button key={p.cle} disabled={occupe} onClick={()=>void choisit(p.cle)}><strong>{p.titre}</strong><span>{p.chapitres_ecrits} études disponibles · {p.cartes_jouables} cartes</span><span>{p.chapitres} chapitres au programme</span><ArrowRight size={20}/></button>)}<button onClick={()=>setDemande(true)} disabled={occupe}><strong>Nouveau cursus</strong><span>Décrire à Jean-Baptiste ce que tu veux apprendre</span></button></div> : <form onSubmit={e=>void depose(e)}><button type="button" onClick={()=>setDemande(false)}><ArrowLeft size={16}/> Retour aux cursus</button><label>Ta situation et ton envie d’apprendre<textarea value={texte} onChange={e=>setTexte(e.target.value)} maxLength={2000} required rows={5}/></label><button className="action-etude" disabled={occupe || !texte.trim()}>Enregistrer la demande</button>{envoyee && <p role="status">Demande enregistrée pour Jean-Baptiste. Tu peux commencer un cursus disponible.</p>}</form>}
      <p className="arrivee-detail">La première étude commence par ta réponse à un cas. Elle ne mesure pas encore ton niveau.</p></>}
    </section></main><footer className="arrivee-pied">Des sources à chaque étape. Ta progression t’appartient.</footer></div>;
}

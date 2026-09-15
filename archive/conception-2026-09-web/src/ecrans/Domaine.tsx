import { useState, type CSSProperties } from "react";
import { ArrowLeft, ArrowRight, Search, Play } from "lucide-react";
import { ETATS_NOEUD, LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import { Anneau, Glyphe } from "./Icones";
import { Bouton, pourcent } from "./Ui";

export function Domaine({ cle }: { cle: string }) {
  const { banque, monde } = useMagasin();
  const [recherche, cherche] = useState("");
  const [niveau, changeNiveau] = useState("");
  if (!banque || !monde) return null;
  const region = [...monde.regions, ...monde.horsCarte].find((r) => r.cle === cle);
  if (!region) return <div className="page-document">{LIB.vide}</div>;
  const noeuds = monde.noeuds.filter((n) => n.domaine === cle);
  const affiches = noeuds.filter((n) => (!niveau || n.niveau === Number(niveau)) && n.titre.toLocaleLowerCase("fr").includes(recherche.toLocaleLowerCase("fr")));
  const branches = monde.branches.filter((b) => b.domaine === cle);
  const anciennes = banque.cartes.filter((c) => c.domaine === cle && !c.chapitre);
  return <div className="page-domaine" style={{ "--c-accent": accentDuRang(region.rang), "--c-domaine": accentDuRang(region.rang) } as CSSProperties}>
    <button className="lien-retour" onClick={() => va("/arbre")}><ArrowLeft size={18} />{LIB.arbre}</button>
    <header className="entete-domaine"><div className="sceau-domaine"><Anneau part={region.remplissage} taille={80} /><Glyphe rang={region.rang} taille={30} /></div>
      <div><h1 className="titre-page">{region.titre}</h1><p>{noeuds.length} {LIB.chapitres} · {region.cartesTotales} {LIB.cartesDisponibles} · {pourcent(region.remplissage)}</p></div>
      <Bouton primaire disabled={!region.cartesTotales} onClick={() => va(`/salle/seance/${cle}`)} enfants={<><Play size={16} />{LIB.reviser}</>} />
    </header>
    <div className="outils-domaine"><label className="recherche"><Search size={19} aria-hidden="true" /><input type="search" aria-label={LIB.rechercheChapitre} placeholder={LIB.rechercheChapitre} value={recherche} onChange={(e) => cherche(e.target.value)} /></label>
      <select aria-label={LIB.niveau} value={niveau} onChange={(e) => changeNiveau(e.target.value)}><option value="">{LIB.tousNiveaux}</option>{[...new Set(noeuds.map((n) => n.niveau))].sort().map((n) => n !== null ? <option key={n} value={n}>{LIB.niveau} {n}</option> : null)}</select>
    </div>
    {!affiches.length ? <p className="etat-vide">{LIB.aucunChapitre}</p> : <div className="branches-domaine">
      {branches.map((b) => {
        const enfants = affiches.filter((n) => n.branche === b.cle);
        if (!enfants.length) return null;
        return <section className="branche-domaine" key={b.cle}><h2>{b.titre}<span>{enfants.length}</span></h2><ol>
          {enfants.map((n) => <li key={n.id}><button data-testid="chapitre" data-chapitre={n.id} className="noeud-chapitre" onClick={() => va(`/noeud/${cle}/${n.id}`)}>
            <span className={`sceau-chapitre ${n.cartesTotales ? "" : "sans-cartes"}`}><Anneau part={n.remplissage} taille={44} /><span>{n.niveau}</span></span>
            <span className="texte-chapitre"><span>{n.titre}</span><small>{n.cartesTotales ? `${ETATS_NOEUD[n.etat]} · ${n.cartesTotales} ${LIB.cartes}` : LIB.aEcrire}</small></span><ArrowRight size={16} />
          </button></li>)}
        </ol></section>;
      })}
    </div>}
    {anciennes.length ? <section className="anciennes-cartes"><h2>{LIB.cartesNonRattachees}</h2><p>{anciennes.length} {LIB.cartesDisponibles}</p><Bouton onClick={() => va(`/salle/seance/${cle}`)} enfants={LIB.reviser} /></section> : null}
  </div>;
}

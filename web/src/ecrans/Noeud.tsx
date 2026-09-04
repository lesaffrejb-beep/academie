import { useEffect, useRef } from "react";
import { ArrowRight, X } from "lucide-react";
import { ETATS_NOEUD, LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { Bouton } from "./Ui";
import { Domaine } from "./Domaine";
import { Anneau } from "./Icones";

export function Noeud({ chemin }: { chemin: string }) {
  const { banque, monde } = useMagasin();
  const [domaine, ...reste] = chemin.split("/");
  const id = reste.join("/");
  const feuille = useRef<HTMLDialogElement>(null);
  useEffect(() => { feuille.current?.showModal(); return () => feuille.current?.close(); }, []);
  if (!banque || !monde || !domaine) return null;
  const noeud = monde.noeuds.find((n) => n.id === id);
  const cartes = banque.cartes.filter((c) => c.chapitre === id);
  const sources = [...new Map(cartes.flatMap((c) => c.source ?? []).map((s) => [s.url ?? s.texte, s])).values()];
  const ferme = () => va(`/domaine/${domaine}`);
  return <><Domaine cle={domaine} /><dialog ref={feuille} className="fiche-noeud" aria-labelledby="titre-noeud" onCancel={(e) => { e.preventDefault(); ferme(); }} onClick={(e) => { if (e.target === e.currentTarget) { const r = e.currentTarget.getBoundingClientRect(); if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) ferme(); } }}>
    <div className="fiche-poignee" /><div className="fiche-entete"><span>{LIB.niveau} {noeud?.niveau ?? ""}</span><button autoFocus className="bouton-icone" aria-label={LIB.fermer} title={LIB.fermer} onClick={ferme}><X size={21} /></button></div>
    <div className="fiche-sceau"><Anneau part={noeud?.remplissage ?? 0} taille={80} /><span>{noeud?.niveau}</span></div>
    <h2 id="titre-noeud">{noeud?.titre ?? LIB.vide}</h2><p className="fiche-etat">{noeud ? ETATS_NOEUD[noeud.etat] : ""} · {cartes.length} {LIB.cartesDisponibles}</p>
    {!cartes.length ? <p className="etat-vide">{LIB.chapitreSansCarte}</p> : null}
    <section className="fiche-section"><h3>{LIB.prerequis}</h3>{noeud?.prerequis.length ? <ul>{noeud.prerequis.map((p) => <li key={p}>{monde.noeuds.find((n) => n.id === p)?.titre ?? p}</li>)}</ul> : <p>{LIB.aucunPrerequis}</p>}</section>
    {sources.length ? <section className="fiche-section"><h3>{LIB.sources}</h3><ul>{sources.map((s) => <li key={s.url ?? s.texte}>{s.url && /^https?:\/\//.test(s.url) ? <a href={s.url} target="_blank" rel="noreferrer">{s.texte}</a> : s.texte}</li>)}</ul></section> : null}
    <div className="fiche-actions"><Bouton primaire disabled={!cartes.length} onClick={() => va(`/salle/seance/chapitre:${id}`)} enfants={<>{LIB.reviserChapitre}<ArrowRight size={18} /></>} /></div>
  </dialog></>;
}

import { useEffect, useId, useMemo, useRef, useState, type CSSProperties } from "react";
import { ArrowRight, Network, Search } from "lucide-react";
import type { Banque, LigneJournal } from "../donnees/types";
import type { CarteMonde, Noeud } from "../moteur/progression";
import { chercheChapitres, voisinageChapitre } from "../moteur/graphe";
import { cartesServiables } from "../moteur/serviceabilite";
import { etudeDisponible, repriseEtude } from "../moteur/etude";
import { ETATS_NOEUD, LIB } from "../app/i18n";
import { accentDuRang } from "../app/theme";
import { va } from "../app/routage";
import "./graphePrerequis.css";

export function GraphePrerequis({monde, banque, journal, jour}: {
  monde: CarteMonde; banque: Banque; journal: LigneJournal[]; jour: number;
}) {
  const [recherche, rechercheChange] = useState("");
  const [domaine, domaineChange] = useState("");
  const [branche, brancheChange] = useState("");
  const [id, selectionne] = useState(() => monde.noeuds.find(n => banque.etudes?.lecons[n.id])?.id ?? monde.noeuds[0]?.id ?? "");
  const [limite, limiteChange] = useState(30);
  const [suivreFocus, focusChange] = useState(false);
  const conteneur = useRef<HTMLDivElement>(null);
  const marqueur = useId().replace(/:/g, "");
  const [traits, traitsChange] = useState<{d: string; interDomaine: boolean}[]>([]);
  const resultats = useMemo(() => chercheChapitres(monde.noeuds, recherche, domaine, branche), [monde.noeuds, recherche, domaine, branche]);
  const graphe = useMemo(() => voisinageChapitre(monde.noeuds, id), [monde.noeuds, id]);
  const centre = graphe.centre;
  const regions = [...monde.regions, ...monde.horsCarte];
  const nomDomaine = (n: Noeud) => regions.find(r => r.cle === n.domaine)?.titre ?? n.domaine;
  const couleur = (n: Noeud) => accentDuRang(regions.find(r => r.cle === n.domaine)?.rang ?? 1);
  const cartes = useMemo(() => cartesServiables(banque.cartes, journal, jour), [banque.cartes, journal, jour]);
  const comptes = new Map<string, number>();
  for (const carte of cartes) if (carte.chapitre) comptes.set(carte.chapitre, (comptes.get(carte.chapitre) ?? 0) + 1);
  const etat = (n: Noeud) => n.cartesTotales ? ETATS_NOEUD[n.etat] : "Au programme";
  const lecon = centre ? banque.etudes?.lecons[centre.id] : undefined;
  const etude = lecon && etudeDisponible(lecon, banque.cartes, journal, jour) ? lecon : null;
  const nombreCartes = centre ? comptes.get(centre.id) ?? 0 : 0;
  const choisi = (n: Noeud, suivre = false) => { selectionne(n.id); focusChange(suivre); };

  useEffect(() => {
    if (!suivreFocus) return;
    conteneur.current?.querySelector<HTMLButtonElement>('[aria-current="true"]')?.focus({preventScroll: true});
    focusChange(false);
  }, [id, suivreFocus]);

  // Les traits suivent les vraies cibles HTML, y compris après zoom du texte.
  useEffect(() => {
    const cadre = conteneur.current;
    if (!cadre) return;
    const mesure = () => {
      const r = cadre.getBoundingClientRect();
      const positions = new Map(Array.from(cadre.querySelectorAll<HTMLElement>("[data-noeud]")).map(el => [el.dataset.noeud, el.getBoundingClientRect()]));
      const vertical = window.matchMedia("(max-width: 767px)").matches;
      traitsChange(graphe.liens.flatMap(lien => {
        const a = positions.get(lien.source), b = positions.get(lien.cible);
        if (!a || !b) return [];
        const coteDroit = lien.source === graphe.centre?.id;
        const x1 = (vertical ? coteDroit ? a.right : a.left : a.right) - r.left;
        const y1 = a.top + a.height / 2 - r.top;
        const x2 = (vertical ? coteDroit ? b.right : b.left : b.left) - r.left;
        const y2 = b.top + b.height / 2 - r.top;
        const rail = coteDroit ? r.width - 3 : 3;
        const d = vertical ? `M${x1},${y1} H${rail} V${y2} H${x2}`
          : `M${x1},${y1} C${(x1+x2)/2},${y1} ${(x1+x2)/2},${y2} ${x2},${y2}`;
        return [{d, interDomaine: lien.interDomaine}];
      }));
    };
    const observateur = new ResizeObserver(mesure);
    observateur.observe(cadre);
    cadre.querySelectorAll<HTMLElement>("[data-noeud]").forEach(el => observateur.observe(el));
    mesure();
    return () => observateur.disconnect();
  }, [graphe]);

  const noeud = (n: Noeud, courant = false) => <button key={n.id} type="button" data-noeud={n.id}
    aria-current={courant ? "true" : undefined} className="graphe-chapitre" style={{"--c-domaine": couleur(n)} as CSSProperties}
    onClick={() => choisi(n, true)}>
    <span className="graphe-noeud-titre">{n.titre}</span>
    <span className="graphe-noeud-meta">{n.niveau ? `${LIB.niveau} ${n.niveau} · ` : ""}{etat(n)}</span>
    {centre && n.domaine !== centre.domaine ? <span className="graphe-noeud-domaine">{nomDomaine(n)}</span> : null}
  </button>;

  return <section className="graphe-prerequis" aria-label="Explorer les prérequis">
    <div className="graphe-introduction"><Network size={24} aria-hidden="true"/><div>
      <h2>Chaque chapitre, ses bases et ses suites</h2>
      <p>Choisis un chapitre pour suivre les liens du programme. Tu peux explorer dans l’ordre qui t’intéresse.</p>
    </div></div>
    <div className="graphe-filtres">
      <label className="graphe-recherche"><span>Chercher un chapitre</span><span className="graphe-champ"><Search size={18} aria-hidden="true"/><input type="search" value={recherche} onChange={e => {rechercheChange(e.target.value); limiteChange(30);}} /></span></label>
      <label><span>Domaine du graphe</span><select value={domaine} onChange={e => {domaineChange(e.target.value); brancheChange(""); limiteChange(30);}}>
        <option value="">Tous les domaines</option>{regions.map(r => <option key={r.cle} value={r.cle}>{r.titre}</option>)}
      </select></label>
      <label><span>Branche du graphe</span><select value={branche} disabled={!domaine} onChange={e => {brancheChange(e.target.value); limiteChange(30);}}>
        <option value="">Toutes les branches</option>{monde.branches.filter(b => b.domaine === domaine).map(b => <option key={b.cle} value={b.cle}>{b.titre}</option>)}
      </select></label>
    </div>
    <div className="graphe-espace">
      <aside className="graphe-index" aria-label="Index du programme">
        <p role="status">{resultats.length} chapitre{resultats.length > 1 ? "s" : ""} sur {monde.noeuds.length}</p>
        {!resultats.length ? <p>Aucun chapitre ne correspond à ces filtres.</p> : null}
        {(recherche || domaine || branche) ? <button className="lien-action" onClick={() => {rechercheChange(""); domaineChange(""); brancheChange(""); limiteChange(30);}}>Effacer les filtres</button> : null}
        <ul aria-label="Chapitres du programme">{resultats.slice(0, limite).map(n => <li key={n.id}>
          <button type="button" aria-pressed={n.id === id} onClick={() => choisi(n)}>
            <span>{n.titre}</span><span className="graphe-noeud-meta">{etat(n)}{(comptes.get(n.id) ?? 0) > 0 ? ` · ${comptes.get(n.id)} cartes disponibles` : ""}</span>
          </button>
        </li>)}</ul>
        {resultats.length > limite ? <button className="lien-action" onClick={() => limiteChange(limite + 30)}>Afficher les chapitres suivants</button> : null}
      </aside>
      <div className="graphe-lecture">
        {centre ? <>
          <div className="graphe-selection"><h3>{centre.titre}</h3><p>{nomDomaine(centre)} · {monde.branches.find(b => b.domaine === centre.domaine && b.cle === centre.branche)?.titre ?? centre.branche}</p></div>
          <p className="graphe-legende">Les flèches vont des prérequis vers leurs suites. Les pointillés traversent un autre domaine.</p>
          <div ref={conteneur} className="graphe-relations" data-testid="graphe-relations">
            <svg className="graphe-traits" aria-hidden="true"><defs><marker id={marqueur} viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 8 4 L 0 8 z" fill="var(--c-encre-2)"/></marker></defs>
              {traits.map((t, i) => <path key={i} d={t.d} fill="none" stroke="var(--c-encre-2)" strokeWidth="1.2" strokeDasharray={t.interDomaine ? "4 4" : undefined} markerEnd={`url(#${marqueur})`} />)}
            </svg>
            <section className="graphe-groupe" data-groupe="prerequis"><h4>Les bases</h4><div className="graphe-noeuds">{graphe.prerequis.length ? graphe.prerequis.map(n => noeud(n)) : <p className="graphe-absence">{graphe.absents.length ? "Aucun prérequis disponible dans ce programme." : "Aucun prérequis déclaré."}</p>}</div></section>
            <section className="graphe-groupe" data-groupe="centre"><h4>Ce chapitre</h4><div className="graphe-noeuds">{noeud(centre, true)}</div></section>
            <section className="graphe-groupe" data-groupe="suites"><h4>Pour aller plus loin</h4><div className="graphe-noeuds">{graphe.suites.length ? graphe.suites.map(n => noeud(n)) : <p className="graphe-absence">Aucune suite directe déclarée.</p>}</div></section>
          </div>
          {graphe.absents.length ? <p className="graphe-absence">Prérequis absent{graphe.absents.length > 1 ? "s" : ""} de ce programme : {graphe.absents.join(", ")}.</p> : null}
          <section className="graphe-detail" data-testid="graphe-detail" aria-label="Étudier le chapitre sélectionné">
            <div><h3>{centre.titre}</h3><p>{etat(centre)}</p>
              {nombreCartes ? <p>{nombreCartes} carte{nombreCartes > 1 ? "s" : ""} disponible{nombreCartes > 1 ? "s" : ""} · {centre.cartesAcquises} à stabilité suffisante selon le moteur de rappel.</p> : <p>Aucune carte disponible pour ce chapitre.</p>}
              {lecon && !etude ? <p>L’étude demande une vérification avant de pouvoir être ouverte.</p> : null}
            </div>
            <div className="graphe-actions">{etude ? <button className="action-etude" onClick={() => va(`/salle/etude/${etude.id}`)}>{repriseEtude(etude, journal).commencee ? "Reprendre ce chapitre" : "Étudier ce chapitre"}<ArrowRight size={18}/></button> : null}
              <button className="lien-action" disabled={!nombreCartes} onClick={() => va(`/salle/seance/chapitre:${centre.id}`)}>{LIB.reviserChapitre}<ArrowRight size={18}/></button>
              <button className="lien-action" onClick={() => va(`/noeud/${centre.domaine}/${centre.id}`)}>Fiche et sources<ArrowRight size={18}/></button>
            </div>
          </section>
        </> : <p>Aucun chapitre n’est publié dans ce cursus.</p>}
      </div>
    </div>
  </section>;
}

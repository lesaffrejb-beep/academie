import { compteActuel } from "../app/compte";
import { ArrowRight, ArrowUpRight, Check, RotateCcw, Network } from "lucide-react";
import type { CSSProperties } from "react";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import { etudeDisponible, repriseEtude } from "../moteur/etude";
import { NombreAnime } from "./MicroAnimations";

export function Accueil() {
  const { banque, journal, metier, choisisMetier, etats, jour, points } = useMagasin();
  if (!banque) return null;
  const parcours = banque.etudes?.parcours.find(p => p.metier === metier);
  const lecons = parcours?.chapitres.map(id => banque.etudes?.lecons[id]).filter(l => l !== undefined) ?? [];
  const disponibles = lecons.filter(l => etudeDisponible(l, banque.cartes, journal, jour));
  const prochaine = disponibles.find(l => !repriseEtude(l, journal).terminee) ?? disponibles[0];
  const reprise = prochaine ? repriseEtude(prochaine, journal) : null;
  const total = disponibles.reduce((n, l) => n + l.cartes.length, 0);
  const dues = banque.cartes.filter(c => (etats.get(c.id)?.duLe ?? Infinity) <= jour).length;
  const commence = () => prochaine && va(`/salle/etude/${prochaine.id}`);

  return <div className="accueil" style={{ "--c-accent": accentDuRang(parcours?.rang ?? 1) } as CSSProperties}>
    <div className="flex flex-wrap items-center justify-between gap-3 mb-2">
      {!compteActuel()?.cursus && <div className="choix-metier" aria-label="Choisir ton métier">
        <button aria-pressed={metier === "copro"} onClick={() => choisisMetier("copro")}>Copropriété</button>
        <button aria-pressed={metier === "ifsi"} onClick={() => choisisMetier("ifsi")}>Soins infirmiers</button>
      </div>}
      <button
        type="button"
        onClick={() => va("/profil")}
        className="bouton-tactile flex items-center gap-2.5 px-3 py-1.5 rounded-full bg-[var(--c-surface)] border border-[var(--c-bordure-subtile)] text-xs text-[var(--c-encre)] shadow-sm hover:border-[var(--c-accent)]"
      >
        <span className="w-5 h-5 rounded-full bg-[var(--c-accent-fond)] text-[var(--c-accent-texte)] font-bold font-mono text-[11px] flex items-center justify-center">
          {points?.niveau ?? 1}
        </span>
        <span className="font-semibold">Niveau {points?.niveau ?? 1}</span>
        <span className="text-[var(--c-encre-3)]">·</span>
        <span className="font-mono text-[var(--c-encre-2)]"><NombreAnime valeur={points?.xpDansLeNiveau ?? 0} /> / {points?.xpDuNiveau ?? 1000} XP</span>
        <span className="text-[var(--c-encre-3)]">·</span>
        <span className="font-mono text-[var(--c-accent)] font-semibold">{points?.serieJours ?? 0}j série</span>
      </button>
    </div>
    <section className="accueil-ouverture">
      <div className="invitation">
        <h1>{parcours?.titre ?? "Apprendre ton métier"}</h1>
        <p>{parcours?.promesse ?? "Un cas concret. Ton raisonnement. Et quelque chose qui reste."}</p>
        <div className="invitation-actions">
          <button className="action-etude" onClick={commence} disabled={!prochaine}>
            {reprise?.terminee ? "Revoir le parcours" : reprise?.commencee ? "Reprendre l’étude" : "Commencer l’étude"}<ArrowRight size={21} />
          </button>
          <span className="invitation-detail"><span><NombreAnime valeur={disponibles.length} /> chapitres · <NombreAnime valeur={total} /> cartes</span><span>À ton rythme</span></span>
        </div>
      </div>
      {prochaine && <aside className="apercu-cas" aria-labelledby="titre-apercu">
        <h2 id="titre-apercu">{prochaine.titre}</h2>
        <p className="apercu-question">{prochaine.amorce.question.replace(/\s+([;?!:])/g, "\u202f$1")}</p>
      </aside>}
    </section>
    {parcours ? <section className="parcours-ouvert" aria-labelledby="titre-parcours">
      <div className="parcours-entete"><div><h2 id="titre-parcours">Les étapes du parcours</h2><p>{parcours.accroche}</p></div><span className="parcours-public">{parcours.public}</span></div>
      <ol className="fil-chapitres">{lecons.map((lecon, i) => {
        const etat = repriseEtude(lecon, journal); const disponible = etudeDisponible(lecon, banque.cartes, journal, jour);
        return <li key={lecon.id}>
          <button className="chapitre-ouvert" disabled={!disponible} onClick={() => va(`/salle/etude/${lecon.id}`)}>
            <span className={`chapitre-numero ${etat.terminee ? "parcouru" : ""}`}>{etat.terminee ? <Check size={21} /> : String(i + 1).padStart(2, "0")}</span>
            <span className="chapitre-contenu"><strong>{lecon.titre}</strong><span>{lecon.objectifs[0]}</span></span>
            <span className="chapitre-etat">{!disponible ? "En vérification" : etat.terminee ? "Étude parcourue" : etat.commencee ? "À reprendre" : `${lecon.cartes.length} cartes`}<ArrowRight size={21} /></span>
          </button>
        </li>;
      })}</ol>
      <p className="limite-parcours">{parcours.limite}</p>
    </section> : <section className="parcours-ouvert"><h2>Les études sont en vérification</h2><p>Tu peux réviser les cartes disponibles ou explorer le programme.</p></section>}
    <section className="accueil-suite">
      {banque.etudes?.parcours.filter(p => p.metier === metier && p.id !== parcours?.id).map(p => {
        const l = p.chapitres.map(id => banque.etudes?.lecons[id]).find(l => l && etudeDisponible(l, banque.cartes, journal, jour));
        return l ? <button key={p.id} aria-label={`Ouvrir ${p.id === 'renovation' ? 'le pilote rénovation' : p.titre}`} onClick={() => va(`/salle/etude/${l.id}`)}><span><strong>{p.titre}</strong><span>{p.promesse}</span></span><ArrowRight size={20}/></button> : null;
      })}
      <button onClick={() => va("/salle/seance")}><RotateCcw size={24} strokeWidth={1.4} /><span><strong>Faire revenir le savoir</strong><span>{dues ? `${dues} cartes à réviser aujourd’hui` : "Une séance de rappel, sans pression"}</span></span><ArrowRight size={20} /></button>
      <button onClick={() => va("/arbre")}><Network size={24} strokeWidth={1.4} /><span><strong>Voir plus loin</strong><span>Explorer l’arbre de ton métier</span></span><ArrowRight size={20} /></button>
    </section>
    <footer className="accueil-note"><span>Des sources à chaque étape.</span><span>Ta progression t’appartient.</span><a href="#/confiance">Pourquoi cette méthode <ArrowUpRight size={14} /></a></footer>
  </div>;
}

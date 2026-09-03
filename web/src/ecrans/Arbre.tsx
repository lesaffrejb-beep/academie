/** L'arbre : la liste des domaines et leur remplissage, plus le cap du jour. */

import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { accentDuRang } from "../app/theme";
import { compose } from "../moteur/composeur";
import { Bouton, Feuille, Jauge, Secondaire, Titre, pourcent } from "./Ui";

export function Arbre() {
  const { banque, monde, etats, jour, points } = useMagasin();
  if (!banque || !monde) return null;

  const seance = compose(banque, etats, { aujourdhui: jour });
  const dues = seance.revisions.length;
  const socle = monde.horsCarte.reduce((a, r) => a + r.cartesTotales, 0);

  const bandeau =
    dues === 0
      ? voix("cap.rien", {}, jour)
      : seance.arriereReetale > 0
        ? voix("cap.reprise", { dues }, jour)
        : voix("cap.jour", { jour: seance.date, couleur: LIB.arbre, dues, socle }, jour);

  return (
    <div className="flex flex-col gap-4 p-4">
      <Titre enfants={LIB.arbre} />
      <Feuille enfants={
        <>
          <p>{bandeau}</p>
          <p className="mt-2 text-encre-2">
            {LIB.niveau} {points?.niveau ?? 1} · {monde.xp} {LIB.points} ·{" "}
            {points?.serieJours ?? 0} {LIB.serie}
          </p>
          <div className="mt-3 flex gap-2">
            <Bouton primaire onClick={() => va("/salle/seance")} enfants={LIB.seance} />
            <Bouton onClick={() => va("/salle/seance/hasard")} enfants={LIB.auHasard} />
          </div>
        </>
      } />

      <ul className="flex flex-col gap-2">
        {[...monde.regions, ...monde.horsCarte].map((r) => (
          <li key={r.cle}>
            <button
              type="button"
              onClick={() => va(`/domaine/${r.cle}`)}
              className="w-full rounded-ext border border-trait bg-surface p-4 text-left"
            >
              <span className="flex items-baseline justify-between gap-2">
                <span className="font-titre">{r.titre}</span>
                <span className="text-encre-2">{pourcent(r.remplissage)}</span>
              </span>
              <span className="mt-2 block">
                <Jauge part={r.remplissage} accent={accentDuRang(r.rang || 10)} />
              </span>
              <Secondaire enfants={
                `${r.cartesAcquises}/${r.cartesTotales} ${LIB.remplissage}` +
                (r.statut === "hors_carte" ? " · hors carte" : r.ouverte ? "" : " · en silhouette")
              } />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

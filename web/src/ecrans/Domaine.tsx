/** Vue domaine : le bandeau du matin et les propositions. */

import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { compose } from "../moteur/composeur";
import { Bouton, Feuille, Secondaire, Titre, pourcent } from "./Ui";

export function Domaine({ cle }: { cle: string }) {
  const { banque, monde, etats, jour } = useMagasin();
  if (!banque || !monde) return null;
  const region =
    [...monde.regions, ...monde.horsCarte].find((r) => r.cle === cle) ?? null;
  if (!region) return <div className="p-4">{LIB.vide}</div>;

  const seance = compose(banque, etats, { aujourdhui: jour, domaine: cle });
  const noeuds = [
    ...new Set(
      banque.cartes.filter((c) => c.domaine === cle && c.statut === "valide")
        .map((c) => c.branche),
    ),
  ].sort();

  return (
    <div className="flex flex-col gap-4 p-4">
      <Bouton onClick={() => va("/")} enfants={LIB.retour} />
      <Titre enfants={region.titre} />
      <Feuille enfants={
        <>
          <p>
            {voix("domaine.bandeau", {
              domaine: region.titre,
              dues: seance.revisions.length,
              neuves: seance.nouveau.length,
              chapitre: noeuds[0] ?? "",
            }, jour)}
          </p>
          <Secondaire enfants={`${pourcent(region.remplissage)} ${LIB.remplissage}`} />
          <div className="mt-3 flex flex-wrap gap-2">
            <Bouton primaire onClick={() => va(`/salle/seance/${cle}`)} enfants={LIB.reviser} />
            <Bouton onClick={() => va(`/salle/seance/${cle}`)} enfants={LIB.continuer} />
            <Bouton disabled title={LIB.bientot} enfants={`${LIB.etudier} · ${LIB.bientot}`} />
            <Bouton disabled title={LIB.bientot} enfants={`${LIB.epreuve} · ${LIB.bientot}`} />
            <Bouton onClick={() => va("/salle/seance/hasard")} enfants={LIB.auHasard} />
          </div>
        </>
      } />

      <ul className="flex flex-col gap-2">
        {noeuds.map((n) => (
          <li key={n}>
            <button
              type="button"
              onClick={() => va(`/noeud/${cle}/${n}`)}
              className="w-full rounded-ext border border-trait bg-surface p-4 text-left"
            >
              {n}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

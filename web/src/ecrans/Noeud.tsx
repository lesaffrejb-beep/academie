/** La feuille du noeud : etat, prerequis, sources, les cartes du noeud. */

import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { Bouton, Feuille, Secondaire, Titre } from "./Ui";

export function Noeud({ chemin }: { chemin: string }) {
  const { banque, etats, jour } = useMagasin();
  const [domaine, ...reste] = chemin.split("/");
  const branche = reste.join("/");
  if (!banque || !domaine) return <div className="p-4">{LIB.vide}</div>;

  const cartes = banque.cartes.filter(
    (c) => c.domaine === domaine && c.branche === branche && c.statut === "valide",
  );
  const dues = cartes.filter((c) => {
    const e = etats.get(c.id);
    return e ? e.duLe <= jour : false;
  }).length;
  const jamais = cartes.filter((c) => !etats.has(c.id)).length;

  return (
    <div className="flex flex-col gap-4 p-4">
      <Bouton onClick={() => va(`/domaine/${domaine}`)} enfants={LIB.retour} />
      <Titre enfants={branche} />
      <Feuille enfants={
        <>
          <p>
            {jamais === cartes.length
              ? voix("noeud.inconnu", {}, jour)
              : voix("noeud.a_revoir", { n: dues }, jour)}
          </p>
          <Secondaire enfants={`${cartes.length} cartes · ${dues} ${LIB.cartesDues} · ${jamais} ${LIB.cartesNeuves}`} />
          <div className="mt-3">
            <Bouton primaire onClick={() => va(`/salle/seance/${domaine}`)} enfants={LIB.seance} />
          </div>
        </>
      } />
      <ul className="flex flex-col gap-2">
        {cartes.map((c) => (
          <li key={c.id} className="rounded-ext border border-trait bg-surface p-4">
            <p className="font-titre">{c.question}</p>
            <Secondaire enfants={`niveau ${c.niveau} · ${c.type} · verifie le ${c.verifie}`} />
          </li>
        ))}
      </ul>
    </div>
  );
}

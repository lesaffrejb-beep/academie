/** La cloture : stabilise, revient demain, socle. Tout est recalcule. */

import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { Bouton, Feuille, Titre, pourcent } from "./Ui";

export function Cloture() {
  const { banque, monde, etats, jour } = useMagasin();
  if (!banque || !monde) return null;

  const seuil = monde.seuilStabiliteJours;
  const stabilisees = [...etats.values()].filter(
    (e) => e.stabilite >= seuil && e.vuLe === jour,
  ).length;
  const demain = [...etats.values()].filter((e) => e.duLe === jour + 1).length;
  const socle = monde.horsCarte[0]?.remplissage ?? monde.remplissageGlobal;

  return (
    <div className="flex flex-col gap-4 p-4">
      <Titre enfants={LIB.cloture} />
      <Feuille enfants={
        <>
          <p>{voix("cloture.stabilisees", { n: stabilisees }, jour)}</p>
          <p>{voix("cloture.demain", { n: demain }, jour)}</p>
          <p>{voix("cloture.socle", { pct: pourcent(socle).replace(" %", "") }, jour)}</p>
          <p className="mt-2 text-encre-2">{voix("cap.sans_envie", {}, jour)}</p>
        </>
      } />
      <Bouton primaire onClick={() => va("/")} enfants={LIB.fermer} />
    </div>
  );
}

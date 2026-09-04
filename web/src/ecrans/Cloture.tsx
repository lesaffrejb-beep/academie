import { ArrowRight, Check } from "lucide-react";
import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { etatsCartes, jourOrdinal } from "../moteur/etats";
import { cartesServiables } from "../moteur/serviceabilite";
import { Bouton } from "./Ui";

export function Cloture() {
  const { banque, monde, etats, jour, journal, sched } = useMagasin();
  if (!banque || !monde || !sched) return null;

  const avant = etatsCartes(journal.filter((ligne) => (jourOrdinal(ligne.quand) ?? jour) < jour), sched);
  const disponibles = cartesServiables(banque.cartes, journal, jour);
  const seuil = monde.seuilStabiliteJours;
  const stabilisees = disponibles.filter((carte) =>
    (etats.get(carte.id)?.stabilite ?? 0) >= seuil && (avant.get(carte.id)?.stabilite ?? 0) < seuil,
  ).length;
  const demain = disponibles.filter((carte) => etats.get(carte.id)?.duLe === jour + 1).length;
  const reponses = journal.filter((ligne) => ligne.mode === "revision" && jourOrdinal(ligne.quand) === jour).length;

  return <div className="cloture">
    <div className="cloture-sceau" aria-hidden="true"><Check size={34} strokeWidth={1.3} /></div>
    <h1 className="font-titre">{LIB.seanceTerminee}</h1>
    <p>{voix("cloture.demain", { n: demain }, jour)}</p>
    <div className="cloture-bilan">
      <h2>{LIB.bilanDuJour}</h2>
      <div><span className="cloture-chiffre">{stabilisees}</span><span>{LIB.cartesStabilisees}</span></div>
      <p>{reponses} {LIB.reponsesDuJour}</p>
    </div>
    <Bouton primaire onClick={() => va("/")} enfants={<>{LIB.retournerArbre}<ArrowRight size={18} /></>} />
  </div>;
}

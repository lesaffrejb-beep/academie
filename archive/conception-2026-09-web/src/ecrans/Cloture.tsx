import { ArrowRight, Check } from "lucide-react";
import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { etatsCartes, jourOrdinal } from "../moteur/etats";
import { cartesServiables } from "../moteur/serviceabilite";
import { Bouton } from "./Ui";
import { AnneauProgression, BordureLumineuse, EclatParticules, JaugeExp, NombreAnime, VoletGlissant } from "./MicroAnimations";

export function Cloture() {
  const { banque, monde, etats, jour, journal, sched, points } = useMagasin();
  if (!banque || !monde || !sched) return null;

  const avant = etatsCartes(journal.filter((ligne) => (jourOrdinal(ligne.quand) ?? jour) < jour), sched);
  const disponibles = cartesServiables(banque.cartes, journal, jour);
  const seuil = monde.seuilStabiliteJours;
  const stabilisees = disponibles.filter((carte) =>
    (etats.get(carte.id)?.stabilite ?? 0) >= seuil && (avant.get(carte.id)?.stabilite ?? 0) < seuil,
  ).length;
  const demain = disponibles.filter((carte) => etats.get(carte.id)?.duLe === jour + 1).length;
  const reponsesJour = journal.filter((ligne) => ligne.mode === "revision" && jourOrdinal(ligne.quand) === jour);
  const reponses = reponsesJour.length;
  const xpGagnesJour = reponsesJour.reduce((acc, l) => acc + (l.note === 4 ? 30 : l.note === 3 ? 20 : l.note === 2 ? 10 : 5), 0);

  return <div className="cloture">
    <div className="cloture-sceau relative" aria-hidden="true">
      <EclatParticules nombre={24} duree={800} />
      <Check size={36} strokeWidth={1.4} />
    </div>
    <h1 className="font-titre text-3xl md:text-4xl">{LIB.seanceTerminee}</h1>
    <p className="text-encre-2 max-w-prose">{voix("cloture.demain", { n: demain }, jour)}</p>
    <VoletGlissant ouvert={true} classe="w-full flex justify-center">
      <BordureLumineuse couleur="var(--c-succes)" duree={5} classe="rounded-2xl max-w-sm w-full">
        <div className="cloture-bilan flex flex-col gap-4">
          <h2>{LIB.bilanDuJour}</h2>
        <div className="flex flex-col items-center gap-3 py-2">
          <AnneauProgression
            proportion={stabilisees > 0 ? 1 : 0.15}
            taille={108}
            epaisseur={5}
            couleur="var(--c-succes)"
          >
            <div className="flex flex-col items-center">
              <NombreAnime valeur={stabilisees} classe="cloture-chiffre" />
            </div>
          </AnneauProgression>
          <span className="text-sm font-medium text-encre">{LIB.cartesStabilisees}</span>
        </div>
        <p className="text-sm text-encre-2">
          <NombreAnime valeur={reponses} classe="font-semibold text-encre" /> {LIB.reponsesDuJour}
        </p>

        <div className="pt-3 border-t border-[var(--c-bordure-subtile)] w-full">
          <JaugeExp
            xpDansLeNiveau={points?.xpDansLeNiveau ?? 0}
            xpDuNiveau={points?.xpDuNiveau ?? 1000}
            niveau={points?.niveau ?? 1}
            gainRecent={xpGagnesJour}
          />
        </div>
      </div>
    </BordureLumineuse></VoletGlissant>
    <Bouton primaire onClick={() => va("/")} enfants={<>{LIB.retournerArbre}<ArrowRight size={18} /></>} />
  </div>;
}

/**
 * Confiance : ce que le client sait de la fiabilite de ce qu'il sert.
 * Aucun jugement invente : ce sont les champs de la banque, comptes.
 */

import { LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { Bouton, Feuille, Secondaire, Titre, pourcent } from "./Ui";

export function Confiance({ domaine }: { domaine?: string }) {
  const { banque } = useMagasin();
  if (!banque) return null;
  const cartes = domaine
    ? banque.cartes.filter((c) => c.domaine === domaine)
    : banque.cartes;
  const avecSource = cartes.filter((c) => (c.source ?? []).length > 0).length;
  const aRecouper = cartes.filter((c) => c.a_recouper === true).length;
  const brouillons = cartes.filter((c) => c.statut !== "valide").length;
  const avecProvenance = cartes.filter((c) => c.provenance !== undefined).length;

  return (
    <div className="flex flex-col gap-4 p-4">
      <Titre enfants={LIB.confiance} />
      <Feuille enfants={
        <>
          <p>{cartes.length} cartes {domaine ? `dans ${domaine}` : "servies"}.</p>
          <Secondaire enfants={`${avecSource} avec au moins une source (${pourcent(cartes.length ? avecSource / cartes.length : 0)})`} />
          <Secondaire enfants={`${cartes.length - avecSource} sans source retrouvee`} />
          <Secondaire enfants={`${aRecouper} a recouper`} />
          <Secondaire enfants={`${brouillons} hors statut valide, jamais servies en seance`} />
          <Secondaire enfants={`${avecProvenance} portent un tampon de provenance (carte-v2)`} />
        </>
      } />
      <Bouton onClick={() => va("/profil")} enfants={LIB.retour} />
    </div>
  );
}

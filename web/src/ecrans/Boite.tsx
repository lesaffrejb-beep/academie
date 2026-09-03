/** La boite : un depot de texte, POST /boite. Hors ligne, on le dit. */

import { useState } from "react";
import { LIB, voix } from "../app/i18n";
import { api } from "../donnees/api";
import { useMagasin } from "../app/magasin";
import { Bouton, Feuille, Secondaire, Titre } from "./Ui";

export function Boite() {
  const { jour } = useMagasin();
  const [texte, setTexte] = useState("");
  const [etat, setEtat] = useState<string | null>(null);

  async function depose() {
    if (!texte.trim()) return;
    const r = await api.deposeBoite(texte.trim());
    setEtat(r.ok ? `depose : ${r.valeur.etat}` : voix("erreur.reseau", {}, jour));
    if (r.ok) setTexte("");
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      <Titre enfants={LIB.boite} />
      <Feuille enfants={
        <>
          <p>{voix("boite.glisse", {}, jour)}</p>
          <label className="mt-3 block">
            <span className="sr-only">{LIB.deposer}</span>
            <textarea
              value={texte}
              onChange={(e) => setTexte(e.target.value)}
              rows={5}
              className="w-full rounded-int border border-trait bg-fond p-3 text-encre"
            />
          </label>
          <div className="mt-3">
            <Bouton primaire onClick={() => void depose()} enfants={LIB.deposer} />
          </div>
          {etat ? <Secondaire enfants={etat} /> : null}
        </>
      } />
      <Feuille titre={LIB.file} enfants={<Secondaire enfants={LIB.vide} />} />
    </div>
  );
}

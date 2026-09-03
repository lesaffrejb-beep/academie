/** Credits : les licences des dependances et la methode. web/LICENCES.md fait foi. */

import { LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { Bouton, Feuille, Secondaire, Titre } from "./Ui";

const DEPENDANCES: { nom: string; version: string; licence: string }[] = [
  { nom: "react", version: "18.3.1", licence: "MIT" },
  { nom: "react-dom", version: "18.3.1", licence: "MIT" },
  { nom: "dexie", version: "4.0.11", licence: "Apache-2.0" },
  { nom: "vite", version: "5.4.11", licence: "MIT" },
  { nom: "vite-plugin-pwa", version: "0.21.1", licence: "MIT" },
  { nom: "tailwindcss", version: "3.4.17", licence: "MIT" },
  { nom: "typescript", version: "5.6.3", licence: "Apache-2.0" },
  { nom: "vitest", version: "2.1.8", licence: "MIT" },
];

export function Credits() {
  const { banque } = useMagasin();
  return (
    <div className="flex flex-col gap-4 p-4">
      <Titre enfants={LIB.credits} />
      <Feuille enfants={
        <>
          <Secondaire enfants={
            `Banque generee le ${banque?.genere_le ?? "inconnue"}, contrat ${banque?.contrat ?? "carte-v1"}.`
          } />
          <Secondaire enfants="Aucune police, aucun script, aucune image charges d'un tiers." />
        </>
      } />
      <Feuille titre="Dependances" enfants={
        <ul className="flex flex-col gap-1">
          {DEPENDANCES.map((d) => (
            <li key={d.nom}>
              {d.nom} {d.version} · {d.licence}
            </li>
          ))}
        </ul>
      } />
      <Bouton onClick={() => va("/profil")} enfants={LIB.retour} />
    </div>
  );
}

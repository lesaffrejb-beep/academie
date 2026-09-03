/** Profil : les compteurs derives, le theme, l'export JSON du journal. */

import { useEffect, useState } from "react";
import { LIB } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { poseTheme, themeCourant, type Theme } from "../app/theme";
import { exporteJsonl, rejets } from "../moteur/journal";
import { Bouton, Feuille, Secondaire, Titre, pourcent } from "./Ui";

export function Profil() {
  const { points, monde, journal, bilan } = useMagasin();
  const [theme, setTheme] = useState<Theme>(themeCourant);
  const [nbRejets, setNbRejets] = useState(0);

  useEffect(() => {
    void rejets().then((r) => setNbRejets(r.length)).catch(() => undefined);
  }, [journal.length]);

  async function exporte() {
    const texte = await exporteJsonl();
    const url = URL.createObjectURL(new Blob([texte], { type: "application/x-ndjson" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "journal.jsonl";
    a.click();
    URL.revokeObjectURL(url);
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      <Titre enfants={LIB.profil} />
      <Feuille enfants={
        <>
          <p>
            {LIB.niveau} {points?.niveau ?? 1} · {points?.xp ?? 0} {LIB.points}
          </p>
          <Secondaire enfants={
            `${points?.revisions ?? 0} revisions · ${points?.cartesTouchees ?? 0} cartes · ` +
            `${points?.serieJours ?? 0} ${LIB.serie} · ${points?.joursJoues ?? 0} jours joues`
          } />
          <Secondaire enfants={`${pourcent(monde?.remplissageGlobal ?? 0)} ${LIB.remplissage}`} />
        </>
      } />

      <Feuille titre={LIB.theme} enfants={
        <div className="flex gap-2">
          {(["nuit", "papier"] as const).map((t) => (
            <Bouton
              key={t}
              primaire={theme === t}
              onClick={() => {
                poseTheme(t);
                setTheme(t);
              }}
              enfants={t === "nuit" ? LIB.themeNuit : LIB.themePapier}
            />
          ))}
        </div>
      } />

      <Feuille enfants={
        <>
          <Bouton primaire onClick={() => void exporte()} enfants={LIB.exporter} />
          <Secondaire enfants={
            `${journal.length} lignes · ${bilan?.enAttente ?? 0} ${LIB.enAttente} · ${nbRejets} rejets`
          } />
          {bilan?.horsLigne ? <Secondaire enfants={LIB.horsLigne} /> : null}
        </>
      } />

      <div className="flex gap-2">
        <Bouton onClick={() => va("/credits")} enfants={LIB.credits} />
        <Bouton onClick={() => va("/confiance")} enfants={LIB.confiance} />
      </div>
    </div>
  );
}

/**
 * La salle : une carte a la fois. Flash et QCM de la banque v1 se jouent
 * vraiment ; les autres types s'annoncent et se notent comme un flash.
 * Chaque reponse ecrit une ligne journal-v1 (mode revision, format
 * seance) avant tout affichage suivant.
 */

import { useEffect, useMemo, useRef, useState } from "react";
import { LIB, voix } from "../app/i18n";
import { useMagasin } from "../app/magasin";
import { va } from "../app/routage";
import { auHasard, compose } from "../moteur/composeur";
import type { Carte } from "../donnees/types";
import { Bouton, Feuille, Jauge, Secondaire, Titre } from "./Ui";

const MOTEUR_VERSION = "web-2.0.0";

export function Seance({ portee }: { portee?: string }) {
  const { banque, etats, jour, note, journal } = useMagasin();
  const [index, setIndex] = useState(0);
  const [revele, setRevele] = useState(false);
  const [confiance, setConfiance] = useState(false);
  const [choisi, setChoisi] = useState<number | null>(null);
  const [debut, setDebut] = useState(() => Date.now());
  const [ouverte, setOuverte] = useState(false);
  const neuves = useRef<Set<string>>(new Set());

  const cartes = useMemo<Carte[]>(() => {
    if (!banque) return [];
    if (portee === "hasard") return auHasard(banque, 10, jour);
    const s = compose(banque, etats, {
      aujourdhui: jour,
      journal,
      ...(portee ? { domaine: portee } : {}),
    });
    // On retient QUI est neuf : sans ce marquage au journal, le plafond
    // `nouveau_par_jour` ne mordrait jamais cote client (ACA-SEMAINE-1).
    neuves.current = new Set(s.nouveau.map((c) => c.id));
    return [...s.revisions, ...s.nouveau];
    // etats change a chaque reponse : la seance est figee au montage.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [banque, jour, portee]);

  // Ligne d'ouverture de seance (journal-v1, mode "seance").
  useEffect(() => {
    if (!banque || ouverte || !cartes.length) return;
    setOuverte(true);
    void note({
      mode: "seance",
      format: portee === "hasard" ? "hasard" : portee ? "domaine" : "seance",
      graine: jour,
      banque_version: banque.genere_le ?? "inconnue",
      moteur_version: MOTEUR_VERSION,
      ...(portee && portee !== "hasard" ? { cap: portee } : {}),
    });
  }, [banque, cartes.length, jour, note, ouverte, portee]);

  if (!banque) return null;
  if (!cartes.length) {
    return (
      <div className="flex flex-col gap-4 p-4">
        <Titre enfants={LIB.seance} />
        <Feuille enfants={<p>{voix("cap.rien", {}, jour)}</p>} />
        <Bouton onClick={() => va("/")} enfants={LIB.quitter} />
      </div>
    );
  }

  const carte = cartes[index];
  if (!carte) return null;
  const correct = carte.choix?.findIndex((c) => c.correct) ?? -1;

  async function noter(valeur: 1 | 2 | 3 | 4) {
    if (!carte) return;
    await note({
      mode: "revision",
      format: portee === "hasard" ? "hasard" : portee ? "domaine" : "seance",
      carte: carte.id,
      note: valeur,
      duree_ms: Math.max(0, Date.now() - debut),
      confiance,
      ...(neuves.current.has(carte.id) ? { origine: "nouveau" } : {}),
    });
    if (index + 1 >= cartes.length) {
      va("/salle/cloture");
      return;
    }
    setIndex(index + 1);
    setRevele(false);
    setChoisi(null);
    setConfiance(false);
    setDebut(Date.now());
  }

  return (
    <div className="flex flex-col gap-4 p-4">
      <Jauge part={(index + 1) / cartes.length} />
      <div className="flex items-baseline justify-between">
        <Secondaire enfants={`${carte.domaine} · ${carte.type}`} />
        <button type="button" className="text-encre-2 underline" onClick={() => va("/")}>
          {LIB.quitter}
        </button>
      </div>

      <Feuille enfants={
        <>
          <p className="font-titre text-xl">{carte.question}</p>

          {carte.type === "qcm" && carte.choix ? (
            <ul className="mt-4 flex flex-col gap-2">
              {carte.choix.map((c, i) => (
                <li key={c.texte}>
                  <button
                    type="button"
                    disabled={revele}
                    onClick={() => {
                      setChoisi(i);
                      setRevele(true);
                    }}
                    className={
                      "w-full rounded-int border p-3 text-left " +
                      (revele && i === correct
                        ? "border-succes"
                        : revele && i === choisi
                          ? "border-erreur"
                          : "border-trait")
                    }
                  >
                    {c.texte}
                    {revele && i === choisi && !c.correct && c.pourquoi_faux ? (
                      <span className="mt-2 block text-encre-2">{c.pourquoi_faux}</span>
                    ) : null}
                  </button>
                </li>
              ))}
            </ul>
          ) : null}

          {!revele && carte.type !== "qcm" ? (
            <div className="mt-4 flex flex-col gap-2">
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={confiance}
                  onChange={(e) => setConfiance(e.target.checked)}
                />
                {LIB.jetaisSur}
              </label>
              <Bouton primaire onClick={() => setRevele(true)} enfants={LIB.reveler} />
            </div>
          ) : null}

          {revele ? (
            <div className="mt-4 flex flex-col gap-3">
              <p>{carte.reponse}</p>
              {carte.explication ? <Secondaire enfants={carte.explication} /> : null}
              {carte.vigilance ? <Secondaire enfants={carte.vigilance} /> : null}
              {confiance && choisi !== null && choisi !== correct ? (
                <p>{voix("reponse.confiante", {}, jour)}</p>
              ) : null}
              <p className="text-encre-2">{voix("reponse.carnet", {}, jour)}</p>
            </div>
          ) : null}
        </>
      } />

      {revele ? (
        <>
          <div className="flex flex-wrap gap-2">
            <Bouton onClick={() => void noter(1)} enfants={LIB.note1} />
            <Bouton onClick={() => void noter(2)} enfants={LIB.note2} />
            <Bouton primaire onClick={() => void noter(3)} enfants={LIB.note3} />
            <Bouton onClick={() => void noter(4)} enfants={LIB.note4} />
          </div>
          <Sources carte={carte} graine={jour} />
        </>
      ) : null}
    </div>
  );
}

function Sources({ carte, graine }: { carte: Carte; graine: number }) {
  const { note } = useMagasin();
  const sources = carte.source ?? [];
  return (
    <Feuille titre={LIB.sources} enfants={
      <>
        {sources.length ? (
          <ul className="flex flex-col gap-2">
            {sources.map((s) => (
              <li key={s.texte} className="text-encre-2">{s.texte}</li>
            ))}
          </ul>
        ) : (
          <p>{voix("source.sans_source", {}, graine)}</p>
        )}
        {carte.a_recouper ? <p className="mt-2">{voix("source.a_recouper", {}, graine)}</p> : null}
        {carte.provenance ? (
          <Secondaire enfants={
            `${LIB.provenance} : ${String(carte.provenance.par ?? "inconnue")}` +
            (carte.provenance.le ? `, ${String(carte.provenance.le)}` : "")
          } />
        ) : null}
        <div className="mt-3">
          <Bouton
            onClick={() => void note({ mode: "signalement", carte: carte.id })}
            enfants={`${LIB.carteFausse} · ${voix("source.signaler", {}, graine)}`}
          />
        </div>
      </>
    } />
  );
}

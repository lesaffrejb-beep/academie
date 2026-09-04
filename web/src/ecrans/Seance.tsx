/**
 * La salle : une carte a la fois. Flash et QCM de la banque v1 se jouent
 * vraiment ; les autres types s'annoncent et se notent comme un flash.
 * Chaque reponse ecrit une ligne journal-v1 (mode revision, format
 * seance) avant tout affichage suivant.
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
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

  const carte = cartes[index];
  const correct = carte?.choix?.findIndex((c) => c.correct) ?? -1;

  const noter = useCallback(async (valeur: 1 | 2 | 3 | 4) => {
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
  }, [carte, cartes.length, confiance, debut, index, note, portee]);

  /*
   * Le clavier de la DA §8 ter : Espace revele, 1 a 4 notent, Echap sort.
   * « La souris n'est jamais necessaire dans une salle » n'est pas un
   * confort : c'est la promesse d'accessibilite du §7, et elle ne tient
   * que si les touches existent avant les jolis ecrans.
   *
   * Deux precautions. On ne detourne rien quand la frappe va dans un
   * champ ou quand une combinaison est en cours (Ctrl+1 change d'onglet,
   * ce n'est pas a nous). Et Espace ne fait rien si le focus est deja sur
   * un bouton : le navigateur l'active tout seul, l'intercepter le
   * declencherait deux fois.
   */
  useEffect(() => {
    function surTouche(e: KeyboardEvent) {
      if (e.altKey || e.ctrlKey || e.metaKey) return;
      const cible = e.target as HTMLElement | null;
      const balise = cible?.tagName;
      if (balise === "INPUT" || balise === "TEXTAREA" || cible?.isContentEditable) return;
      if (e.key === "Escape") {
        e.preventDefault();
        va("/");
        return;
      }
      if (!carte) return;
      if (e.key === " " && !revele) {
        if (balise === "BUTTON") return;
        e.preventDefault();
        setRevele(true);
        return;
      }
      if (revele && ["1", "2", "3", "4"].includes(e.key)) {
        e.preventDefault();
        void noter(Number(e.key) as 1 | 2 | 3 | 4);
      }
    }
    window.addEventListener("keydown", surTouche);
    return () => window.removeEventListener("keydown", surTouche);
  }, [carte, noter, revele]);

  if (!banque) return null;
  if (!cartes.length || !carte) {
    return (
      <div className="flex flex-col gap-4 p-4">
        <Titre enfants={LIB.seance} />
        <Feuille enfants={<p>{voix("cap.rien", {}, jour)}</p>} />
        <Bouton onClick={() => va("/")} enfants={LIB.quitter} />
      </div>
    );
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

      {/* La carte en cours FLOTTE : c'est la seule chose en avant de
          l'ecran de seance (DA §2 et §8 bis). */}
      <Feuille flottante enfants={
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

/**
 * La ligne de provenance de la DA §5 : « Généré par Claude Opus le
 * 21/08/2026 · 2 sources concordantes · relu le 22/08 ».
 *
 * Elle se construit sur les champs du contrat v2, pas sur des champs
 * inventes : `auteur`, `modele`, `genere_le`, `sources_concordantes`,
 * plus le `verifie_par` de la carte. Un champ absent disparait de la
 * ligne au lieu d'y ecrire « inconnue » : dire « generee par inconnue »
 * serait pire que ne rien dire.
 */
export function ligneProvenance(carte: Carte): string {
  const p = carte.provenance;
  if (!p) return "";
  const morceaux: string[] = [];
  const auteur = p.modele ?? (p.auteur === "humain" ? "une personne" : undefined) ?? p.par;
  const quand = p.genere_le ?? p.le;
  if (auteur) morceaux.push(quand ? `${auteur}, ${quand}` : String(auteur));
  else if (quand) morceaux.push(String(quand));
  if (typeof p.sources_concordantes === "number" && p.sources_concordantes > 0) {
    morceaux.push(`${p.sources_concordantes} ${LIB.sourcesConcordantes}`);
  }
  if (carte.verifie_par) morceaux.push(`${LIB.relueLe} ${carte.verifie}`);
  if (!morceaux.length) return "";
  return `${LIB.provenance} : ${morceaux.join(" · ")}`;
}

function Sources({ carte, graine }: { carte: Carte; graine: number }) {
  const { note } = useMagasin();
  const sources = carte.source ?? [];
  const provenance = ligneProvenance(carte);
  return (
    <Feuille flottante titre={LIB.sources} enfants={
      <>
        {/* La note de confiance en lettre, en tete : c'est ce que le
            joueur lit avant de croire la carte (decisions/0022, DA §5). */}
        {carte.note_confiance ? (
          <p className="mb-2">
            <span className="font-titre text-lg" aria-hidden="true">
              {carte.note_confiance}
            </span>
            <span className="sr-only">{`Note de confiance ${carte.note_confiance}`}</span>
            <span className="ml-2 text-encre-2">{`${LIB.verifieLe} ${carte.verifie}`}</span>
          </p>
        ) : null}
        {sources.length ? (
          <ul className="flex flex-col gap-2">
            {sources.map((s) => (
              <li key={s.texte} className="text-encre-2">
                {s.texte}
                {/* La NATURE de la source, pas seulement son titre : une
                    fiche d'editeur et un texte officiel ne se croient pas
                    pareil (decisions/0004). */}
                {s.nature ? <span className="ml-2 text-encre-2">· {s.nature}</span> : null}
              </li>
            ))}
          </ul>
        ) : (
          <p>{voix("source.sans_source", {}, graine)}</p>
        )}
        {carte.a_recouper ? <p className="mt-2">{voix("source.a_recouper", {}, graine)}</p> : null}
        {provenance ? <Secondaire enfants={provenance} /> : null}
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

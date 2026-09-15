import { compteActuel, clePrivee } from "./compte";
/**
 * Le magasin : banque, journal, etats, carte-monde. Tout est recalcule a
 * chaque changement du journal ; rien n'est stocke a part les lignes.
 */

import {
  createContext, useCallback, useContext, useEffect, useMemo, useState,
  type ReactNode,
} from "react";
import { chargeBanque, ContratInconnu } from "../donnees/banque";
import type { Banque, LigneJournal } from "../donnees/types";
import { planificateurDe, type Planificateur } from "../moteur/fsrs";
import { aujourdhuiOrdinal, etatsCartes, type EtatCarte } from "../moteur/etats";
import { carteMonde, type CarteMonde } from "../moteur/progression";
import { points, type Points } from "../moteur/points";
import { brancheReprise, ecris, litJournal, synchronise, type Bilan } from "../moteur/journal";
import { chargeVoix } from "./i18n";

interface Magasin {
  metier: string;
  choisisMetier: (metier: string) => void;
  pret: boolean;
  panne: string | null;
  banque: Banque | null;
  journal: LigneJournal[];
  etats: Map<string, EtatCarte>;
  monde: CarteMonde | null;
  points: Points | null;
  sched: Planificateur | null;
  jour: number;
  bilan: Bilan | null;
  note: (ligne: Parameters<typeof ecris>[0]) => Promise<void>;
  rafraichis: () => Promise<void>;
  synchronise: () => Promise<void>;
}

const Contexte = createContext<Magasin | null>(null);

/** Vue pour les indicateurs du métier ; le journal conservé reste complet. */
export function journalPourMetier(journal: LigneJournal[], banque: Banque): LigneJournal[] {
  const cartes = new Set(banque.cartes.map(c => c.id));
  const chapitres = new Set(banque.chapitres?.map(c => c.id) ?? []);
  const domaines = new Set(Object.keys(banque.domaines));
  return journal.filter(l => {
    if (l.carte !== undefined) return cartes.has(l.carte);
    if (l.chapitre !== undefined) return chapitres.has(l.chapitre);
    if (l.region !== undefined) return domaines.has(l.region);
    if (l.cartes?.length) return l.cartes.every(id => cartes.has(id));
    // Les anciens événements sans rattachement restent exportables, sans
    // leur inventer un métier pour calculer les points ou les jours joués.
    return false;
  });
}

export function observeJour(surJour: (jour: number) => void): () => void {
  let minuterie: ReturnType<typeof setTimeout>;
  const actualise = () => {
    surJour(aujourdhuiOrdinal());
    clearTimeout(minuterie);
    const instant = new Date();
    const minuit = new Date(instant.getFullYear(), instant.getMonth(), instant.getDate() + 1);
    minuterie = setTimeout(actualise, Math.max(1, minuit.getTime() - instant.getTime()));
  };
  const auRetour = () => {
    if (document.visibilityState === "visible") actualise();
  };
  actualise();
  document.addEventListener("visibilitychange", auRetour);
  return () => {
    clearTimeout(minuterie);
    document.removeEventListener("visibilitychange", auRetour);
  };
}

export function FournisseurMagasin({ enfants }: { enfants: ReactNode }) {
  const [pret, setPret] = useState(false);
  const [panne, setPanne] = useState<string | null>(null);
  const [banqueComplete, setBanque] = useState<Banque | null>(null);
  const [metier, setMetier] = useState(() => {
    if (compteActuel()?.cursus) return compteActuel()?.cursus as string;
    try { return localStorage.getItem(clePrivee("academie-metier")) ?? "copro"; } catch { return "copro"; }
  });
  const choisisMetier = (cle: string) => {
    if (compteActuel()?.cursus || !banqueComplete?.metiers?.[cle]) return;
    setMetier(cle);
    try { localStorage.setItem(clePrivee("academie-metier"), cle); } catch { /* préférence facultative */ }
  };
  const banque = useMemo(() => {
    if (!banqueComplete) return null;
    const m = banqueComplete.metiers?.[metier];
    if (!m) return banqueComplete;
    const ids = new Set(m.cartes);
    return {...banqueComplete, ...m, cartes: banqueComplete.cartes.filter(c => ids.has(c.id))};
  }, [banqueComplete, metier]);
  const [journal, setJournal] = useState<LigneJournal[]>([]);
  const [bilan, setBilan] = useState<Bilan | null>(null);
  const [jour, setJour] = useState(aujourdhuiOrdinal);

  useEffect(() => observeJour(setJour), []);

  const rafraichis = useCallback(async () => {
    setJournal(await litJournal());
  }, []);

  useEffect(() => {
    let vivant = true;
    let detacheReprise: () => void = () => undefined;
    void (async () => {
      await chargeVoix();
      try {
        const b = await chargeBanque();
        if (!vivant) return;
        setBanque(b);
      } catch (e) {
        if (!vivant) return;
        setPanne(
          e instanceof ContratInconnu
            ? `Cette banque annonce le contrat "${e.contrat}", que ce client ne sait pas lire. Rien ne sera joue tant qu'il n'est pas mis a jour.`
            : "La banque n'a pas pu etre chargee, ni depuis le reseau ni depuis le cache.",
        );
      }
      try {
        setJournal(await litJournal());
      } catch {
        // Pas d'IndexedDB : on joue, rien ne se garde.
      }
      if (!vivant) return;
      setPret(true);
      detacheReprise = brancheReprise((b) => {
        if (!vivant) return;
        setBilan(b);
        void litJournal().then((lignes) => {
          if (vivant) setJournal(lignes);
        }).catch(() => undefined);
      });
    })();
    return () => {
      vivant = false;
      detacheReprise();
    };
  }, []);

  const sched = useMemo(
    () => (banque ? planificateurDe(banque.fsrs) : null),
    [banque],
  );
  const journalMetier = useMemo(
    () => (banque ? journalPourMetier(journal, banque) : []),
    [journal, banque],
  );
  const etats = useMemo(
    () => (sched ? etatsCartes(journalMetier, sched) : new Map<string, EtatCarte>()),
    [journalMetier, sched],
  );
  const monde = useMemo(
    () => (banque ? carteMonde(banque.cartes, journalMetier, banque, etats, [], jour) : null),
    [banque, journalMetier, etats, jour],
  );
  const pts = useMemo(
    () => (monde ? points(journalMetier, monde, jour) : null),
    [journalMetier, monde, jour],
  );

  const note = useCallback(
    async (ligne: Parameters<typeof ecris>[0]) => {
      await ecris(ligne);
      setJournal(await litJournal());
      void synchronise().then(async (b) => {
        setBilan(b);
        setJournal(await litJournal());
      }).catch(() => undefined);
    },
    [],
  );

  const relance = useCallback(async () => {
    setBilan(await synchronise());
    setJournal(await litJournal());
  }, []);

  const valeur: Magasin = {
    metier, choisisMetier, pret, panne, banque, journal, etats, monde, points: pts, sched, jour, bilan,
    note, rafraichis, synchronise: relance,
  };
  return <Contexte.Provider value={valeur}>{enfants}</Contexte.Provider>;
}

export function useMagasin(): Magasin {
  const m = useContext(Contexte);
  if (!m) throw new Error("useMagasin hors du fournisseur");
  return m;
}

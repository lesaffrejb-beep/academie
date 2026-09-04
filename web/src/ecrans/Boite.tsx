import { useCallback, useEffect, useState } from "react";
import { Plus } from "lucide-react";
import { LIB, voix } from "../app/i18n";
import { api } from "../donnees/api";
import { useMagasin } from "../app/magasin";
import { Bouton, Titre } from "./Ui";

const ETATS: Record<string, string> = {
  "a-traiter": LIB.boiteATraiter, "chapitre-propose": LIB.boitePropose,
  rattache: LIB.boiteRattache, ecarte: LIB.boiteEcarte,
};

export function Boite() {
  const { jour } = useMagasin();
  const [texte, setTexte] = useState("");
  const [message, informe] = useState<string | null>(null);
  const [chargement, charge] = useState(true);
  const [envoi, envoie] = useState(false);
  const [entrees, liste] = useState<{ id: string; contenu: string; etat: string }[]>([]);
  const rafraichis = useCallback(async () => {
    charge(true);
    const r = await api.litBoite();
    if (r.ok && r.valeur && Array.isArray(r.valeur.entrees)) { liste(r.valeur.entrees); informe(null); }
    else informe(!r.ok && r.statut === 401 ? LIB.boiteConnexion : LIB.boiteIndisponible);
    charge(false);
  }, []);
  useEffect(() => { void rafraichis(); }, [rafraichis]);
  async function depose() {
    if (!texte.trim() || envoi) return;
    const soumis = texte;
    envoie(true);
    const r = await api.deposeBoite(soumis.trim());
    if (r.ok) { setTexte((courant) => courant === soumis ? "" : courant); await rafraichis(); }
    else informe(r.statut === 401 ? LIB.boiteConnexion : LIB.boiteIndisponible);
    envoie(false);
  }
  return <div className="page-document"><Titre enfants={LIB.boite} />
    <form className="boite-depot" onSubmit={(e) => { e.preventDefault(); void depose(); }}>
      <label><span className="sr-only">{LIB.deposer}</span><textarea value={texte} onChange={(e) => setTexte(e.target.value)} rows={4} maxLength={20000} className="boite-texte" /></label>
      <div className="boite-actions"><p>{voix("boite.glisse", {}, jour)}</p><Bouton primaire disabled={!texte.trim() || envoi} onClick={() => void depose()} enfants={<><Plus size={18} />{envoi ? LIB.chargement : LIB.deposer}</>} /></div>
    </form>
    <section className="profil-section"><h2>{LIB.file}</h2>
      {message ? <div role="status"><p>{message}</p><button className="lien-action" onClick={() => void rafraichis()}>{LIB.reessayer}</button></div>
        : chargement ? <p role="status">{LIB.chargement}</p>
          : entrees.length ? <ul className="journal-recent">{entrees.map((e) => <li key={e.id}><span>{e.contenu}</span><small>{ETATS[e.etat] ?? e.etat}</small></li>)}</ul> : <p className="etat-vide">{LIB.boiteVide}</p>}
    </section>
  </div>;
}

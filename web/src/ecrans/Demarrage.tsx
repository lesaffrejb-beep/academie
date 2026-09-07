import plans from '../donnees/demarrages.json';
import {useMagasin} from '../app/magasin';
import {etudeDisponible,repriseEtude} from '../moteur/etude';
export function Demarrage() {
 const {metier,banque,journal,jour}=useMagasin();
 const plan=plans[metier as keyof typeof plans];if(!plan||!banque)return null;
 return <details className="demarrage" open><summary>Tes deux premières semaines</summary><p>Dix séances proposées, à répartir à ton rythme. Les rappels reprennent ce que tu as travaillé ; une étude parcourue ne signifie pas une compétence acquise.</p><ol>{plan.map((s,i)=>{
  const lecon='chapitre' in s ? banque.etudes?.lecons[s.chapitre!]:undefined;
  const disponible=s.type==='rappel'||Boolean(lecon&&etudeDisponible(lecon,banque.cartes,journal,jour));
  const titre=lecon?.id==='entree.ecrit.les-calculs-de-l-ecrit'?'Proportionnalité et pourcentages':lecon?.titre??('titre'in s?s.titre:'Étude en vérification');
  return <li key={i}><small>Séance {i+1} · {i<5?'Première semaine':'Deuxième semaine'}</small>{disponible?<a href={lecon?`#/salle/etude/${lecon.id}`:'#/salle/seance'}>{titre}{lecon&&repriseEtude(lecon,journal).terminee?' · parcourue':''}</a>:<p>{titre} · en vérification</p>}<p>{s.objectif}</p></li>;
 })}</ol></details>;
}

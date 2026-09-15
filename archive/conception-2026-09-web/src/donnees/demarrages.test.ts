import {it,expect} from 'vitest';
import plans from './demarrages.json';
import {readFileSync} from 'node:fs';
it('propose dix séances par cursus avec huit études distinctes et deux rappels',()=>{
 const banque=JSON.parse(readFileSync(new URL('../../../site/banque.json',import.meta.url),'utf8'));
 for(const [metier,plan] of Object.entries(plans)){
  expect(plan).toHaveLength(10);
  const etudes=plan.filter(s=>s.type==='etude');expect(etudes).toHaveLength(8);
  expect(new Set(etudes.map(s=>'chapitre'in s?s.chapitre:'')).size).toBe(8);
  for(const s of etudes){if(!('chapitre'in s))throw Error('chapitre absent');
   const l=banque.etudes.lecons[s.chapitre!];expect(l?.statut).toBe('valide');
   expect(banque.metiers[metier].chapitres.some((c:{id:string})=>c.id===l.id)).toBe(true);
  }
 }
});

import {it,expect} from 'vitest';
import {createElement} from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {Barre} from './Barre';
import {analyse} from '../app/routage';
it('retire la boîte de la navigation et des anciennes adresses',()=>{
 expect(renderToStaticMarkup(createElement(Barre,{route:{nom:'accueil'}}))).not.toContain('Boîte');
 expect(analyse('#/boite').nom).toBe('accueil');
});

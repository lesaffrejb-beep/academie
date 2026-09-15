import {expect, it} from 'vitest';
import {supportEtude} from './validationSupport';
const i = {fichier:'images/test.svg', alt:'Support', credit:'Académie'};
it('autorise seulement un média local nommé et attribué', () => {
  expect(supportEtude(i)).toEqual(i);
  for (const fichier of ['../test.svg','images/../test.svg','https://localhost/image.png','images/sous/test.svg','images/test.svg?x=1'])
    expect(supportEtude({...i,fichier})).toBeNull();
  expect(supportEtude({...i,alt:''})).toBeNull();
  expect(supportEtude(null)).toBeNull();
});

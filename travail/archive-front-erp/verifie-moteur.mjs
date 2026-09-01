#!/usr/bin/env node
/**
 * verifie-moteur.mjs — le miroir FSRS JS dit-il la même chose que Python ?
 *
 *     node erp/react/scripts/verifie-moteur.mjs
 *
 * Deux moteurs pour une seule vérité, c'est une divergence qui arrive.
 * Elle serait silencieuse (aucune exception, aucun écran cassé) et
 * porterait sur la seule donnée irréparable : l'état de mémoire du
 * joueur. Ce script existe pour qu'elle ne puisse pas passer.
 *
 * Il ne compare pas des formules isolées : il rejoue le PARCOURS complet
 * d'une carte, exactement comme `seance.etats_cartes` — première
 * rencontre, révisions avec délai, reprise le jour même, et le champ
 * `stabilite_forcee` du quiz de positionnement.
 *
 * Les vecteurs sont publiés par le dépôt autonome Académie, puis
 * versionnés à côté de ce script. Leur provenance et leur date font
 * partie de l'artefact : ERP ne lit ni le code ni les données sources
 * d'Académie pour exécuter ce contrôle hors ligne.
 *
 * Sortie : 0 si tout passe, 1 sinon. Ligne par ligne en cas d'échec :
 * la séquence, l'étape, le champ, l'écart.
 */

import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { Planificateur, appliqueRevue } from '../src/lib/academie-moteur.js';

const ICI = dirname(fileURLToPath(import.meta.url));
const VECTEURS = resolve(ICI, 'vecteurs-fsrs.json');

/* Combien d'écarts on détaille avant de résumer : un mur de 400 lignes
   ne se lit pas, les dix premières suffisent à trouver la cause. */
const ECARTS_DETAILLES = 12;

function lisVecteurs() {
  let brut;
  try {
    brut = readFileSync(VECTEURS, 'utf8');
  } catch {
    console.error(`✗ vecteurs absents : ${VECTEURS}`);
    console.error('  → republier l’artefact depuis le dépôt Académie');
    process.exit(1);
  }
  return JSON.parse(brut);
}

function ecart(obtenu, attendu) {
  if (!Number.isFinite(obtenu) || !Number.isFinite(attendu)) return Infinity;
  return Math.abs(obtenu - attendu);
}

function main() {
  const charge = lisVecteurs();
  const tol = charge.tolerance ?? 1e-4;
  const echecs = [];
  let comparaisons = 0;

  // Le miroir doit porter les MÊMES paramètres, pas seulement les mêmes
  // formules : un paramètre recopié de travers passe toutes les
  // vérifications de structure et fausse chaque intervalle.
  const refParams = charge.params || [];
  const sondeParams = new Planificateur({}).p;
  refParams.forEach((v, i) => {
    comparaisons += 1;
    if (ecart(sondeParams[i], v) > 1e-12) {
      echecs.push(`paramètres · p[${i}] : JS ${sondeParams[i]} ≠ Python ${v}`);
    }
  });

  for (const seq of charge.sequences || []) {
    let sched;
    try {
      sched = new Planificateur({ retention: seq.retention });
    } catch (e) {
      echecs.push(`${seq.nom} · construction refusée : ${e.message}`);
      continue;
    }
    let etat = null;
    seq.etapes.forEach((etape, i) => {
      etat = appliqueRevue(sched, etat, etape.note, etape.jours,
        etape.stabilite_forcee);
      const att = etape.attendu;
      const obtenu = {
        stabilite: etat.stabilite,
        difficulte: etat.difficulte,
        intervalle: sched.intervalle(etat.stabilite),
      };
      for (const champ of ['stabilite', 'difficulte', 'intervalle']) {
        comparaisons += 1;
        const e = ecart(obtenu[champ], att[champ]);
        if (e > tol) {
          echecs.push(`${seq.nom} · étape ${i + 1} (note ${etape.note}, `
            + `${etape.jours} j) · ${champ} : JS ${obtenu[champ]} `
            + `≠ Python ${att[champ]} (écart ${e.toExponential(2)})`);
        }
      }
      for (const [jours, r] of Object.entries(att.recuperabilite || {})) {
        comparaisons += 1;
        const obt = sched.recuperabilite(etat.stabilite, Number(jours));
        const e = ecart(obt, r);
        if (e > tol) {
          echecs.push(`${seq.nom} · étape ${i + 1} · R(${jours} j) : `
            + `JS ${obt} ≠ Python ${r} (écart ${e.toExponential(2)})`);
        }
      }
    });
  }

  const nbSeq = (charge.sequences || []).length;
  if (echecs.length) {
    console.error(`\n✗ ROUGE — le miroir FSRS JS diverge du moteur Python.\n`);
    echecs.slice(0, ECARTS_DETAILLES).forEach((l) => console.error(`   ${l}`));
    if (echecs.length > ECARTS_DETAILLES) {
      console.error(`   … et ${echecs.length - ECARTS_DETAILLES} autre(s).`);
    }
    console.error(`\n${echecs.length} écart(s) sur ${comparaisons} comparaison(s), `
      + `${nbSeq} séquence(s), tolérance ${tol}.`);
    console.error('Le Python fait foi : corriger erp/react/src/lib/academie-moteur.js.');
    return 1;
  }
  console.log(`VERT — miroir FSRS conforme : ${comparaisons} comparaison(s) `
    + `sur ${nbSeq} séquence(s), tolérance ${tol}.`);
  console.log(`  vecteurs du ${charge.genere_le} (artefact du dépôt Académie)`);
  return 0;
}

process.exit(main());

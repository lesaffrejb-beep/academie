# Licences du client v2

Relevé du 03/09/2026, sur l'arbre installé par `npm install` dans `web/`
(`package-lock.json` fait foi). Chaque version est épinglée sans `^` dans
`package.json` : une montée de version est un geste, pas un effet de bord.
La méthode de relevé est celle de `travail/benchmark-2026-08-30.md`
partie 4, étendue au client.

Aucune de ces dépendances n'est chargée depuis un tiers à l'exécution :
tout est empaqueté par Vite et servi par l'Académie elle-même
(`decisions/0020`, `tests/hotes.test.ts`).

## Dépendances d'exécution

| Paquet | Version | Licence | Ce qu'elle fait ici |
| --- | --- | --- | --- |
| `react` | 18.3.1 | MIT | rendu des écrans |
| `react-dom` | 18.3.1 | MIT | montage dans le navigateur |
| `dexie` | 4.0.11 | Apache-2.0 | IndexedDB : journal, file d'envoi, cache de banque |
| `lucide-react` | 1.40.0 | ISC, MIT pour les glyphes hérités de Feather | navigation et boutons, licence officielle consultée le 04/09/2026 |
| `@fontsource-variable/fraunces` | 5.3.0 | OFL-1.1 | la serif à empattements, titres (DA §2) |
| `@fontsource-variable/source-sans-3` | 5.3.0 | OFL-1.1 | la sans humaniste, texte et interface (DA §2) |

Les deux polices sont **auto-hébergées**, comme la DA l'exige : rien
n'est chargé de `fonts.googleapis.com` ni d'ailleurs. Le `LICENSE` de
chaque paquet porte la SIL Open Font License 1.1 (relevé le 03/09/2026
dans `node_modules/@fontsource-variable/*/LICENSE`) : Fraunces est
© 2020 The Fraunces Project Authors (Undercase Type), Source Sans 3 est
© Google Inc. L'OFL autorise l'usage et la redistribution embarquée ;
elle interdit la vente des fichiers de police seuls et impose de ne pas
réutiliser le nom réservé pour une version modifiée ; nous ne modifions
rien.

Seul le sous-ensemble `latin` de chaque famille est servi
(`src/polices.css` explique pourquoi) : deux fichiers, 65 ko au total,
contre dix fichiers et 340 ko si on importait les paquets tels quels.

Le moteur FSRS n'est pas une dépendance : `src/moteur/fsrs.ts` est un
miroir écrit à la main de `app/planificateur.py`, jugé par
`src/moteur/parite.test.ts`. `ts-fsrs` (MIT), annoncé dans
`web/README.md` et `decisions/0007`, n'a donc pas été installé : voir la
section « Écart avec le cahier » plus bas.

## Dépendances de construction et de test

| Paquet | Version | Licence | Ce qu'elle fait ici |
| --- | --- | --- | --- |
| `vite` | 5.4.11 | MIT | serveur de développement et empaquetage |
| `@vitejs/plugin-react` | 4.3.4 | MIT | JSX et rafraîchissement rapide |
| `vite-plugin-pwa` | 0.21.1 | MIT | manifeste, service worker, précache (Workbox) |
| `vitest` | 2.1.8 | MIT | tests de parité, d'hôtes et de voix |
| `@playwright/test` | 1.62.1 | Apache-2.0 | `tests/e2e/` : hors-ligne, checklist de la DA |
| `typescript` | 5.6.3 | Apache-2.0 | typage strict, `tsc --noEmit` avant le build |
| `tailwindcss` | 3.4.17 | MIT | utilitaires de mise en page, tokens en variables CSS |
| `postcss` | 8.4.49 | MIT | chaîne CSS |
| `autoprefixer` | 10.4.20 | MIT | préfixes navigateurs |
| `@types/node` | 22.10.2 | MIT | types Node pour `vite.config.ts` et les tests |
| `@types/react` | 18.3.12 | MIT | types React |
| `@types/react-dom` | 18.3.1 | MIT | types React DOM |

`vite-plugin-pwa` embarque Workbox (Apache-2.0, Google) : Workbox n'est
pas installé directement, il arrive par cette dépendance et son code
finit dans `dist/workbox-*.js`.

## Dépendances transitives

434 paquets au total dans `node_modules` au 03/09/2026 au soir (428 le
matin, plus Playwright et les deux polices). Répartition des licences
déclarées :

| Licence | Paquets |
| --- | --- |
| MIT | 384 |
| ISC | 18 |
| Apache-2.0 | 13 |
| BlueOak-1.0.0 | 7 |
| BSD-2-Clause | 4 |
| BSD-3-Clause | 4 |
| OFL-1.1 | 2 |
| CC-BY-4.0 | 1 |
| MIT ou CC0-1.0 | 1 |

Les deux lignes qui ne sont pas des licences logicielles courantes :

- `caniuse-lite` 1.0.30001810, CC-BY-4.0 : base de données de support
  navigateurs, utilisée par `autoprefixer` à la construction. Rien de son
  contenu n'est redistribué dans `dist/`.
- `type-fest` 0.16.0, MIT ou CC0-1.0 : types seulement, aucun code livré.

BlueOak-1.0.0 (`glob`, `minimatch`, `minipass`, `path-scurry`,
`jackspeak`, `@isaacs/cliui`, `package-json-from-dist`) est une licence
permissive approuvée OSI, sans obligation de redistribution.

Le relevé se refait :

```bash
cd web && node -e 'const fs=require("fs"),p=require("path"),c={};
(function w(d){for(const n of fs.readdirSync(d)){if(n.startsWith(".")&&n!==".bin")continue;
const q=p.join(d,n);if(n.startsWith("@")){w(q);continue;}
try{const j=JSON.parse(fs.readFileSync(p.join(q,"package.json"),"utf8"));
const l=typeof j.license==="string"?j.license:"non declaree";c[l]=(c[l]||0)+1}catch{}}})("node_modules");
console.log(c)'
```

## Ce qui n'est pas encore installé

Ces briques sont annoncées par `web/README.md` et `decisions/0007` mais
n'entrent qu'avec la couche visuelle et les tests de bout en bout. Elles
sont relevées ici pour que la vérification de licence soit déjà faite.

| Paquet | Version visée | Licence | Pour quoi |
| --- | --- | --- | --- |
| `motion` | à figer | MIT | animations, sous la seconde |
| game-icons.net | sans version | CC BY 3.0 | glyphes de chapitre, attribution visible dans Crédits |

## Écart avec le cahier

`ts-fsrs` (MIT) est cité par `web/README.md` et `decisions/0007` comme la
dépendance de composition hors-ligne. Elle n'a pas été installée : ce
que le cahier exige, c'est la parité à 1e-4 avec `app/planificateur.py`,
pas la réutilisation d'une bibliothèque. `ts-fsrs` expose ses propres
états (apprentissage, réapprentissage, paliers, flou sur l'intervalle) et
n'offre pas la formule court terme nue du Python sans être contournée ;
un miroir de 200 lignes se relit, se juge par vecteurs, et ne dérive pas
au prochain incrément de la dépendance. Le juge est
`app/vecteurs_fsrs.py`, rejoué par `src/moteur/parite.test.ts` à chaque
`npm test`. Si la parité casse un jour, c'est le miroir qui a tort.

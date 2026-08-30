# Charte & Architecture Design System — L'Académie Copro (2026)

Ce document formalise les décisions de design, la grille de tokens, l'architecture des 5 piliers d'apprentissage et les directives pour faire évoluer l'interface de **L'Académie Copro** sans jamais casser la cohérence visuelle ni réintroduire de classes non standard.

---

## 1. Les 5 Piliers Architecturaux de l'Académie

L'Académie Copro s'articule autour de 5 piliers rigoureux, fidèles au [`academie/BLUEPRINT.md`](../../academie/BLUEPRINT.md) :

1. **☕ La Matinale (15 min FSRS)** :
   - Hero banner d'état quotidien avec streak et points XP.
   - Grille Bento asymétrique des 5 grandes filières métier.
   - Module phare d'actualité/doctrine et défi quotidien express.

2. **🎯 Quizz & Arène (7 Modes de Jeu Spécialisés)** :
   - **Flashcards 3D** : Rappel actif avec 4 notes FSRS (Raté / Dur / Bien / Facile).
   - **Arène Express (30s)** : Sprint chrono sur scénarios d'AG et calculs de seuils.
   - **Photo-Diagnostic Bâtiment** : Identification sur le terrain des organes techniques (souches, VMC, fissures I1-I4, sous-stations).
   - **Sprint des Délais Légaux (45s)** : Réflexes sur les délais stricts (convocations, notifications, PV, contestations 42 al. 2).
   - **Duel de Négociation & Psychologie d'AG** : Gestion des contestations de salle avec jauge de sérénité.
   - **Détecteur de Vices & Fausses Demandes de Vote** : Audit des PV d'AG pour déjouer les fausses demandes de vote internes.
   - **Puzzle Juridique** : Reconstitution des règles de droit dans l'ordre exact.

3. **📖 Ateliers de Lecture (Le Côté Bac / Exemples Travaillés)** :
   - Interface immersive split-screen : Document authentique annoté à gauche / Fiche méthode, questions de restitution et extraction de cartes FSRS à droite.
   - **Atelier 1** : Lire un arrêt de la Cour de cassation (Visa, Motifs, Dispositif, règle syndic).
   - **Atelier 2** : Auditer un devis réel du portefeuille (Assurance décennale, TVA, déchets).
   - **Atelier 3** : Décodage des 5 annexes comptables & balance générale (Comptes 450, 103, 512).
   - **Atelier 4** : Déjouer les fausses demandes de vote (Le réflexe des 2 derniers PV).
   - **Atelier 5** : Le texte de fond / Culture & Société (Lussault : copropriété et micro-société).

4. **🌲 Arbre de Compétences (Tech Tree 8 Domaines Métier)** :
   - Pathologie du bâtiment, Technique des équipements, Droit de la copropriété, Procédure & contentieux, Comptabilité syndic, Énergie & réglementation, Lecture de plans & DOE, Culture & Doctrine.

5. **👤 Profils Équipe & ERP Maya** :
   - Interconnexion aux profils réels des gestionnaires, assistants et comptables (`JB`, `Lucas Levard`, `Hugo Lambert`, `Florence Goujon`, `Coraline Salmon`).
   - Métriques ERP réelles : Portefeuille sous gestion, AG de l'année, taux de vote en séance, alertes traitées.
   - Passeport de compétences certifié 3D avec signature cryptographique opposable.

---

## 2. Table des Tokens Officiels du Design System

### 2.1 Surfaces & Fonds
| Token Tailwind | Utilisation | Rendu Thème Clair / Sombre |
|---|---|---|
| `bg-surface` | Carte standard, modale, conteneur principal | Blanc pur (clair) / Gris bleuté nuit (sombre) |
| `bg-surface-subtle` | Zone en creux, encadré secondaire, fond d'input | Teinte très légère pour créer de la profondeur |
| `bg-surface-hover` | État au survol d'un item de liste ou d'un bouton | Contraste doux au hover |
| `bg-canvas` | Fond d'écran global de l'application | Gris doux neutre |

### 2.2 Bordures
| Token Tailwind | Utilisation |
|---|---|
| `border-bordure` | Bordure standard (1px) de séparation des cartes et listes |
| `border-bordure-forte` | Bordure renforcée pour inputs actifs ou délimiteurs majeurs |
| `border-bordure-subtile` | Ligne très fine de séparation interne |

### 2.3 Couleurs Sémantiques & Badges
| Statut / Fonction | Fond doux | Texte | Bordure | Action / Accent fort |
|---|---|---|---|---|
| **Bleu (Primaire / Métier)** | `bg-bleu-soft` | `text-bleu` | `border-bleu-clair/50` | `bg-bleu text-white shadow-bleu` |
| **Vert (Succès / Validation / 100%)** | `bg-vert-soft` | `text-vert-text` | `border-vert-border` | `bg-vert text-white` |
| **Jaune / Or (XP / Champion / Trophée)** | `bg-jaune-soft` | `text-jaune-text` | `border-jaune-border` | `bg-jaune text-noir` |
| **Corail (Alerte / Chrono / Litige)** | `bg-corail-soft` | `text-corail-text` | `border-corail-border` | `bg-corail text-white` |

---

## 2bis. L'espace de jeu (30/08/2026) — la peau dédiée

Depuis le brief JB du 30/08 (« entrer dans l'Académie doit changer
d'espace : autre menu, autres couleurs, cohérent mais carrément en mode
jeu »), l'Académie n'est plus un écran de l'ERP : c'est un **mode plein
écran**, sans rail ni barre (état porté par `App.jsx`, `route.vue ===
'academie'`). Trois conséquences de design :

1. **L'espace est toujours sombre.** Il force la classe `dark` tant
   qu'il est monté, sans réécrire la préférence de thème de l'ERP (on la
   retrouve en sortant). Une carte-monde en fond blanc n'est pas une
   carte ; c'est une rupture assumée, pas un oubli du mode jour.
2. **Une sous-palette, déclarée comme les autres** dans le `:root` de
   `src/index.css`, sous `.espace-academie` : la mer (`--jeu-mer`,
   `--jeu-mer-profonde`, `--jeu-mer-horizon`, `--jeu-mer-clair`,
   `--jeu-mer-reflet`, `--jeu-etoile`), la terre (`--jeu-terre`,
   `--jeu-terre-haute`, `--jeu-terre-crete`, `--jeu-plage`, `--jeu-cote`,
   `--jeu-relief`, `--jeu-chemin`), les lumières chaudes
   (`--jeu-lanterne`, `--jeu-feu`, `--jeu-bois`), les états
   (`--jeu-brouillard`, `--jeu-brouillard-voile`, `--jeu-perime`,
   `--jeu-lueur`, `--jeu-conquise`, `--jeu-encours`, `--jeu-boss`), le
   HUD, et **une couleur par île** : `--jeu-ile-1` à `--jeu-ile-10` plus
   `--jeu-ile-commune`, attribuées AU RANG (jamais au nom du domaine —
   un domaine étranger hérite de la même variété sans rien coder pour
   lui). La règle « zéro hexadécimal dans un composant » tient : la
   carte SVG n'écrit que des `var(--jeu-*)`.
3. **Le joueur ne choisit jamais un format d'exercice** (arbitrage JB,
   30/08). Pas de menu de modes : on clique un LIEU sur la carte, ou le
   phare, ou le dé, et le moteur compose. Les anciennes maquettes de
   mini-jeux vivent hors du chemin, dans `AnnexesMaquette.jsx`.

## 2ter. L'archipel parlant (30/08/2026 au soir) — la refonte

Verdicts de JB sur la première carte : « on comprend rien à l'UI »,
« trop dark, sombre pas plaisant, pas drôle, gaming trop sérieux », « la
carte doit être une carte ». Ce que la refonte fixe comme règles :

1. **Une chose à lire à la fois.** Plus aucun calque posé sur la carte :
   le premier lancement est un écran plein cadre (`EcranAccueil.jsx`),
   la légende s'efface dès qu'un panneau d'île s'ouvre, et chaque île a
   un couloir d'étiquette réservé (largeur du chip calculée sur le texte
   — une légende qui déborde va mordre l'île voisine).
2. **La carte EST l'interface.** Plus de barre d'actions en bas : la
   séance du matin est un **phare** (avec le compte de cartes dues),
   l'expédition aléatoire est un **dé** qui flotte, une île se clique.
   Le « mode 3 minutes » n'est plus un bouton.
3. **Les silhouettes parlent** (`archipel.js`) : le tracé d'une icône
   game-icons.net sert de côte, habillé en île (récif, plage, terre
   teintée, crête intérieure, marée de progression). Les fichiers sont
   importés en `?raw` et le rectangle de fond est jeté — l'attribution
   CC BY 3.0 est AFFICHÉE dans l'app (`CreditsIcones.jsx`, entrée
   « Crédits » du menu du HUD) : c'est une condition de licence.
4. **Le pont remplace la citadelle** : l'examen d'une île construit le
   pont vers la suivante, tracé en direct. Entre deux îles visibles non
   reliées, un petit bateau fait la navette.
5. **Deux couches de brouillard** : *shroud* (jamais explorée, nom
   masqué) et *fog périmé* (explorée mais plus revue depuis le seuil de
   stabilité — île délavée, « périmée · N j »). La fraîcheur est
   calculée par `EspaceJeu` depuis le journal, jamais par le moteur.
6. **Paliers nommés** (En friche / Explorée / Maîtrisée / Conquise) :
   affichage seul, dérivé du remplissage mesuré.
7. **Les célébrations : citation sourcée + brouillard qui recule.**
   Banque dans `src/lib/academie-citations.js`, chaque entrée porte son
   œuvre ou sa lettre. **Aucun confetti, nulle part.**
8. **Aucun calque n'entre en `AnimatePresence`, et aucun ne part d'une
   opacité 0.** Sous React.StrictMode + framer 11, une sortie coincée
   laisse un nœud invisible qui avale tous les clics ; et si l'onglet
   est en arrière-plan, rAF gèle et un calque qui devait s'allumer reste
   à zéro. Les calques entrent en animation (translation seulement) et
   disparaissent net. Piège diagnostiqué à l'essai le 30/08/2026.

## 3. Checklist de Conformité avant tout Commit

Toute future modification ou ajout dans `src/components/academie/*` doit valider la checklist suivante :

- [ ] **Zéro classe hors-tokens** : pas de `slate-*`, `amber-*`, `rose-*`, `indigo-*`, ni hexadécimaux bruts.
- [ ] **Tabular Nums** : `tabular-nums font-mono` sur tout score, timer, pourcentage ou décompte.
- [ ] **Micro-interaction** : `active:scale-[0.98]` et `cursor-pointer` sur chaque bouton/carte cliquable.
- [ ] **Rayons imbriqués** : bordures concentriques harmonieuses ($R_{int} = R_{ext} - P$).
- [ ] **Responsive** : tester en mobile (375px), tablette et desktop large.
- [ ] **Build de production** : `npm run build` exécuté avec 0 erreur.

# Assessment B — Académie — 5 septembre 2026

Analyse isolée, aucune modification produit. Cible : web/src/ecrans et web/src/app ; navigateur local http://127.0.0.1:4173/academie/. Doctrine, README, web/AGENTS et Impeccable critique lus. Aucun résultat A consulté.

## Détecteur

Une seule exécution : `node /Users/jb/.codex/skills/impeccable/scripts/detect.mjs --json web/src/ecrans web/src/app`.
Code de sortie 0. JSON intégral : `[]`. Zéro constat, zéro règle, aucune localisation ni faux positif à évaluer. Fichier conservé : `/tmp/academie-audit-design-B/detector.json`. Cette absence de signal ne mesure pas la qualité visuelle, le contraste rendu, ni les parcours UX.

## Preuves navigateur et états

Nouvel onglet dédié, navigateur Codex In-app Browser, lecture DOM et actions UI documentées. Pas de lecture/manipulation du stockage. Pas de soumission de boîte, pas de réponse de séance.

- Accueil : 389 chapitres / 76 cartes disponibles. Navigation Arbre, Boîte, Profil explicitement libellée et `aria-current` présent. Dix domaines avec noms accessibles et état sélectionné `aria-pressed`.
- Droit : 60 chapitres / 26 cartes ; tous les chapitres lus affichent « À écrire ». Bouton Réviser domaine actif, section « Cartes en cours de rattachement » en fin de liste. Le détail « Qu’est-ce qu’une copropriété » explique zéro carte disponible et désactive « Réviser ce chapitre ». La séparation programme/jouable est honnête mais impose des clics sans apprentissage dans le parcours Explorer.
- Feuille native `dialog`, nom accessible, focus initial sur Fermer, Escape ferme effectivement et retourne au domaine. **Défaut concret : après Escape, `document.activeElement.tagName` = BODY**, pas le chapitre déclencheur ; ouverture et fermeture remontent/remontent des composants Domaine distincts. Correction suggérée : restaurer focus + position sur le chapitre d’origine. Source `web/src/ecrans/Noeud.tsx:15`, `:20` et `web/src/main.tsx:34`.
- Navigation Profil depuis rail : focus reste sur le bouton Profil ; Tab suivant va à Crédits, donc passe après le contenu qui vient d’être affiché. Titre document demeure « Academie ». Aucun focus de titre/main lors des changements de route dans `web/src/main.tsx:33`. Dégradation clavier/lecteur d’écran à corriger avec destination de focus et annonce de page.
- Focus visible confirmé au clavier sur Crédits : outline `rgb(207, 170, 115) solid 2px`.
- Recherche « zzzz audit introuvable » : message « Aucun chapitre ne correspond. » ; champ et filtre Niveau restent présents, effacement du champ rétablit les résultats. Message non live dans le code ; pas de contrôle dédié « Effacer les filtres ».
- Boîte sans API : « La boîte est indisponible. Le texte reste dans ce champ. » dans `role=status`, Réessayer accessible ; réessai revient proprement au même état. Bouton Déposer désactivé champ vide.
- **Défaut concret de brouillon :** saisie locale « Brouillon temporaire audit », navigation Profil puis Boîte, retour à une textarea vide (`value === ""`) et Déposer désactivé. Aucun envoi effectué. Le message de conservation est limité à rester sur la page, mais ne le dit pas. Source `web/src/ecrans/Boite.tsx:15`. Priorité P1 si la boîte est censée accueillir des notes longues et intermittentes ; conserver un brouillon local et indiquer son état.
- Profil vide : 0 points, révisions, cartes et jours, « Les premières réponses apparaîtront ici. » Journal 0 lignes / 0 en attente ; indisponibilité sync explicitée avec conservation sur cet appareil et bouton de réessai. Cela prouve le rendu d’indisponibilité local, pas une synchronisation réelle ni hors réseau.
- Heatmap `role=img` nommée « Activité, 7 juin - 5 septembre », données par jour seulement dans des `title` de spans. Interprétation de code : l’alternative accessible de l’image ne résume pas l’activité réelle et les titres ne constituent pas une consultation clavier équivalente ; à vérifier avec lecteur d’écran réel.
- Console : aucune erreur ni warning retourné lors de la lecture (maximum 20). Ce constat ne signifie pas absence de requêtes échouées ; les états API indisponibles sont visibles.

## Mesures et captures

Thème Nuit inchangé pendant B. Les dimensions ont été modifiées uniquement après confirmation parent que A avait terminé ses captures, puis réinitialisation tentée. Cette dernière a échoué après interruption du tour : « Browser is not available: 2 ». Dernier override demandé 1280 × 900 ; parent doit rétablir le viewport si le navigateur est encore accessible.

- DOM à 375 × 812 : absence de débordement horizontal document sur Arbre et Profil. Dix domaines 48 × 48 ; noms de domaines tous en `display:none`. L’aperçu expose seulement le domaine sélectionné : utilisateur voyant doit deviner les glyphes ou parcourir les flèches pour identifier sa matière. CTA Séance 141,375 × 51 à y=677, navigation basse 68 de haut. Profil : boutons Exporter et Sync 51 de haut ; navigation 125 × 68.
- DOM à 1280 × 720, Profil : absence de débordement horizontal. Boutons Exporter et Sync 40 de haut ; liens rail Crédits 33 × 16,8 et marque 28 × 28. Ces petites cibles sont mesurées sur ordinateur ; pas une conclusion de non-conformité WCAG sans examiner espacements/exemptions.
- DOM après override 1280 × 900, Arbre : absence de débordement document, atlas 840 px et noms 13,12 px `display:block`.
- Capture fiable consultée : `/tmp/academie-audit-design-B/arbre-375-viewport.png` (375 × 812), montre l’état mobile décrit : glyphes sans noms, domaine sélectionné dessous, Séance près de la barre.
- `/tmp/academie-audit-design-B/boite.png` et `/tmp/academie-audit-design-B/profil.png` prises avant modifications B, DOM mesuré 1280 × 720.
- Captures fullPage `/tmp/academie-audit-design-B/arbre-375-nuit.png`, `profil-375-nuit.png` présentent une mise à l’échelle et une grande marge vide incompatibles avec le viewport mesuré : artefact capture probable, **ne pas attribuer ce vide au produit**.
- Capture `/tmp/academie-audit-design-B/arbre-1280-nuit.png` produite juste après resize ne fait que 416 px de large malgré DOM innerWidth 1280 : contexte capture/viewport incohérent, **ne pas l’utiliser comme preuve desktop**. Une inspection desktop fiable peut venir de A.

## Limites et statut Impeccable

Pas d’overlay : evaluate est explicitement read-only selon l’API Browser ; aucune tentative de mutation, aucun script injecté. Pas de présentation [Human] ni serveur live Impeccable lancé. Le serveur web parent est conservé ; B ne l’a ni lancé ni arrêté. Fallback : détecteur CLI, DOM rendu, interactions natives et capture mobile viewport.

Non mesurés par B : Papier, texte/zoom 200 %, mouvement réduit dans navigateur, contrastes chiffrés des pixels rendus, VoiceOver réel, téléphone physique, réseau coupé, sources après réponse, persistance/synchronisation du journal, perf réseau. Les règles CSS de focus et `prefers-reduced-motion` sont présentes, ce qui ne prouve pas leur acceptation sur appareils.

Priorités B à synthétiser sans ancrer A : P1 brouillon perdu, P2 focus navigation/fermeture, P2 identification mobile par icônes seulement, P2 clarifier parcours chapitres vides vs cartes jouables. Les déficits de contenu restent des limites produit constatées, pas des données à inventer.

Rapport et preuves conservés volontairement dans /tmp pour synthèse parent. Questions finales et persistance de critique relèvent du parent. Aucun fichier du dépôt modifié.

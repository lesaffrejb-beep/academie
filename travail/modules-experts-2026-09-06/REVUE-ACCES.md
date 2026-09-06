# Revue indépendante : accès du petit groupe

06/09/2026. Relecteur : `/root/contenu_expert`, Codex / GPT-6 (identifiant
précis non exposé). Auteur des modifications : agent `/root/acces_profils`.
Lecture du diff en cours de travail ; aucun fichier d'authentification ou
de parcours modifié par le relecteur.

## Conclusion bornée

Aucun nouveau défaut bloquant identifié dans l'ajout de l'annuaire de
connexion, le choix du cursus à l'inscription et le maintien de l'écran
de clé avant ouverture du compte. Cette revue ne vaut pas audit exhaustif
de sécurité, preuve navigateur ou acceptation du VPS.

## Objets examinés

- `serveur/academie_etat/app.py` : nouvelle route GET `/auth/comptes`,
  sortie JSON avec `Cache-Control: no-store`, aucune écriture ni session
  créée par consultation.
- `serveur/academie_etat/auth.py` : projection limitée à pseudo normalisé
  de connexion et nom affiché ; seuls les comptes personnels avec phrase
  hachée et non supprimés, respectant la visibilité et les masquages,
  sont éligibles. Le compte technique initial n'apparaît pas.
- `web/src/app/compte.ts` : projection explicite avant stockage ; la clé
  de récupération reçue à la création ne passe plus dans localStorage.
- `web/src/ecrans/Arrivee/Arrivee.tsx` : inscription conserve la clé à
  l'écran sans encore ouvrir le compte ; après confirmation, l'identité
  et la base du compte sont posées avant l'écriture append-only du cursus.
  La reprise avec clé d'un compte ayant un cursus conserve aussi l'écran
  de clé. Le serveur confirme le cursus avant ouverture du parcours.
- `web/src/donnees/api.ts`, tests associés et cahier ACA-ACCES-LOCAL-1.

L'affichage des pseudos sur l'écran sans session est une propriété demandée
par JB et expliquée à l'inscription ; il ne constitue pas dans ce périmètre
une divulgation accidentelle. La revue contrôle que les réponses, cursus,
identifiants internes et secrets ne sont pas ajoutés à cette projection.

## Vérifications exécutées par le relecteur

- `python3 -m unittest discover -s serveur/tests -p test_onboarding.py` :
  12 tests passent. Couvre notamment sel et hachage, rotation clé/sessions,
  journaux et cursus isolés, refus de cookie d'un autre compte, annuaire
  minimal, masquage global et suppression. Routeur sans socket, base locale
  en mémoire ; aucun compte réel utilisé.
- `npx vitest run src/app/compte.test.ts src/moteur/journal.relecture.test.ts`
  depuis `web/` : deux fichiers et 17 tests passent. Projection locale sans
  clé, séparation de comptes, cas de synchronisation défaillante couverts.
- Sonde supplémentaire sur base en mémoire : un masquage du seul cursus
  actif retire aussi le compte de `/auth/comptes` ; une fois retiré, la
  projection comporte exactement `pseudo` et `titre_affiche`. En-tête
  `Cache-Control: no-store` constaté.

Les tests navigateur ajoutés ont été inspectés mais ne sont pas exécutés
par ce relecteur. Ils doivent prouver création/cursus, conservation de la
clé, déconnexion, clic sur le pseudo, focus du mot de passe et reprise.
L'agent auteur et l'intégrateur portent ces vérifications. L'identité par
onglet et le refus 409 en cas de cookie divergent restent des protections
existantes, sans affaiblissement identifié dans ce diff.

Les empreintes des fichiers examinés figurent dans
`revue-acces-empreintes.json` ; toute modification ultérieure exige une
revue du changement concerné.

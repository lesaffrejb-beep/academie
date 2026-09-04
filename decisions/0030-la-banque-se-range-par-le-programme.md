# 0030. La banque se range par le programme, et un trou se comble par un chapitre

Date : 04/09/2026. Arbitrage rendu pour `ACA-CONTRAT-2` étape 2, sur
délégation de JB (« arbitre tout pour que le prochain agent puisse
avancer »), à partir de
`travail/assignation-cartes-chapitres-2026-09-03.md`.

## Décision

1. **Les vingt et un changements de domaine sont acceptés tels que
   proposés.** Le programme (`programme/copro.json`) est la carte ; les
   fichiers de la banque v1 n'étaient que des thèmes de travail d'août.
   Une carte va au chapitre qui dit son sujet, même si sa région change.
2. **Les vingt-quatre « à confirmer » sont prises au premier choix**
   de la table, sans exception. Règle pour les suivantes : entre deux
   chapitres plausibles, on prend celui du même niveau que la carte ;
   à niveau égal, celui du domaine qui porte la notion, pas celui qui
   la subit.
3. **Un trou du programme se comble par un chapitre, pas par un
   rangement forcé.** Deux chapitres de niveau 2 sont créés dans
   `programme/genere_copro.py`, leçon `[à écrire]` (`0026`) :
   - `droit.assemblee.la-notification` (branche `assemblee`,
     sous-branche `preparer`, prérequis
     `droit.assemblee.la-convocation-forme-et-delai`) : reçoit les
     quatre cartes de notification électronique de `droit/veille-recente`
     (`notification-electronique-principe`, `lre-prestataire-qualifie`,
     `mention-voie-postale`, `point-depart-des-delais`) ;
     `pieces-espace-en-ligne` reste sur
     `droit.assemblee.les-pieces-jointes-obligatoires`.
   - `procedure.recouvrement.la-decheance-du-terme` (branche
     `recouvrement`, prérequis
     `procedure.avant-le-proces.mise-en-demeure-recommande-sommation`,
     et lui-même prérequis de `procedure.recouvrement.choisir-la-voie`) :
     reçoit `decheance-assiette` et `datation-decheance`.
4. **`equipements.chauffage.les-contrats-p1-a-p4` devient
   `les-contrats-p1-a-p5`** (titre « Les contrats P1 à P5 », notion
   « P5 » ajoutée). Les deux références dans `genere_copro.py` suivent.
   Les cinq cartes de chauffage y vont.
5. **Les deux cartes de survol** gardent la proposition :
   `cinq-annexes` sur `comptabilite.annexes.l-annexe-1-l-etat-financier`
   (le premier chapitre d'une branche accueille le survol de la
   branche), `calendrier-des-vagues` sur
   `cabinet.cycle-annuel.les-obligations-annuelles`.

## Contexte

56 assignations sûres, 24 défendables autrement, 4 sans chapitre, 3
trous révélés. Un agent ne pouvait pas trancher seul (`0021`) ; JB a
délégué. Aucune carte n'est réécrite, aucun identifiant de carte ne
change (`0019`).

## Conséquences

- L'étape 2 d'`ACA-CONTRAT-2` est mécanique : recopier la table dans
  `app/migre_banque.py` avec ces cinq points, régénérer le programme,
  `app/valide_programme.py` et `app/valide_chapitres.py` verts,
  archiver `banque/`.
- La carte-monde change de forme (droit perd sept cartes, comptabilité
  en gagne). C'est voulu.
- Les deux chapitres neufs ont une leçon à écrire : ligne dans
  `ACA-CONTENT-2`.

## Réouverture

Si JB, en jouant (`ACA-RITUAL-1`), trouve une carte mal rangée, il le
dit dans `IDEES-EN-VOL.md` ; on déplace la carte, on ne rouvre pas la
règle.

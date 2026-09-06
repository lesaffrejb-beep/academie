# Revue indépendante du code du pilote de dix pages

06/09/2026. Outil Codex, modèle GPT-6 ; agent `audit_expertise`, distinct de
l'auteur de l'implémentation. Première passe, avant correction des constats.

## Périmètre

Diffs de `app/genere.py`, `web/src/ecrans/Etude.tsx`, `Accueil.tsx`,
`web/src/experience.css` ; nouveaux `SupportEtude.tsx`, `supportEtude.ts`
et test, `web/tests/e2e/pilote-renovation.spec.ts` ; `collecte.py`,
`test_collecte.py`, `test_routage.py` de ce dossier. Lecture des consommateurs
existants seulement pour suivre le routage et le journal. Aucune modification
des comptes, aucun examen du chapitre pédagogique ni des PDF.

## Constats à corriger avant acceptation du support

1. **P2, agrandissement inopérant sur ordinateur.** `SupportEtude.tsx`
   applique seulement `minWidth: 700`, alors que `.etude-corps` peut mesurer
   710 px et que l'image conserve `width: 100%`. Dans cette configuration,
   cliquer sur « Agrandir le support » change le libellé, sans agrandir
   l'image. Employer un agrandissement effectif relatif au cadre et vérifier
   la largeur avant/après sur les deux dimensions d'écran.
2. **P2, valeur de support invalide faussement autorisée.** `Etude.tsx`
   affiche le composant dès que `image != null`, mais protège le retour et
   le crédit avec `Boolean(carte.image)` ou `carte.image`. Une chaîne vide,
   `false` ou `0` dans une banque malformée provoque donc une alerte du
   composant tout en autorisant le retour et l'enregistrement. Employer le
   même critère de présence et le même état de chargement dans les trois
   chemins. Un test du validateur de support seul ne vérifie pas ce chemin
   d'intégration.

Ces constats ont été communiqués à l'auteur ; aucun code d'implémentation
n'a été modifié par le relecteur.

## Résultats et réserves

- Le routage du satellite dépend de l'identifiant exact du chapitre parent,
  non du seul domaine. Le test fourni démontre l'inclusion copro et
  l'exclusion IFSI. La génération principale valide les chapitres avant
  de construire cet artefact ; `charge_metiers` n'est pas un nouveau valideur.
- Le composant refuse les chemins distants, traversées et supports sans
  texte alternatif ou crédit. L'erreur de chargement remet le crédit à
  l'état bloqué pour une image représentée par un objet normal. Le texte
  saisi reste disponible : aucune suppression de brouillon ou du journal
  n'a été ajoutée par le composant.
- Les écritures de réponses conservent leur chemin existant : sauvegarde
  append-only, puis suppression du seul brouillon après succès. Cette
  inspection n'est pas une preuve de synchronisation réelle téléphone/Mac.
- Les deux E2E fournis couvrent le parcours jusqu'à la synthèse et l'image
  réseau absente. Ils ne vérifient pas encore l'agrandissement, la reprise
  après rechargement, le contenu du journal, ni un support de forme invalide.
  La comparaison de largeur de document est faite après la sortie des
  exercices : elle ne prouve pas l'absence de débordement pendant le zoom.
- La collecte est bornée à dix pages et refuse un PDF de mauvaise empreinte.
  Elle conserve des empreintes de sorties et n'assimile pas une similarité
  textuelle à un consensus. Les recadrages ne sont pas validés par ce script.
  `HF_HUB_OFFLINE=1` reste une précondition annoncée dans la docstring,
  non imposée par le script ; les options Docling interdisant les services
  distants ne constituent pas seules une preuve d'absence de téléchargement
  de modèles. Aucun appel de collecte lourd n'a été relancé par le relecteur.

## Vérifications exécutées par le relecteur

- `python3 travail/pilote-renovation-10p/test_routage.py` : 1 test, vert.
- `python3 travail/pilote-renovation-10p/test_collecte.py` : 3 tests, verts.
- Depuis `web`, `npm exec vitest run src/ecrans/supportEtude.test.ts` :
  1 test, vert.

Les E2E, contrôles complets du dépôt et vérifications visuelles ne sont pas
attribués à cette première passe. Verdict : deux corrections ciblées avant
acceptation du support visuel ; aucune perte de données introduite trouvée
dans le diff examiné, avec les réserves de test ci-dessus.

## Contre-relecture après corrections

Même relecteur, 06/09/2026. Cette section remplace le verdict provisoire
ci-dessus ; les constats initiaux sont conservés pour la traçabilité.

- **P2 agrandissement corrigé.** Le style agrandi applique désormais
  `width: 200%` et `maxWidth: none`, avec un minimum de largeur. Le cadre
  conserve son défilement interne. Le nouveau test navigateur compare la
  largeur réelle de l'image avant/après, vérifie le débordement de la page
  pendant le zoom, puis réduit le support.
- **P2 support invalide corrigé.** `supportNecessaire` repose sur la
  présence `image != null` ou sur un format exigeant une image ; il est
  partagé par le rendu, le bouton de retour et `noteCarte`. Un support
  absent d'une carte visuelle ne devient plus une question sans image.
  Les nouveaux E2E injectent chaîne vide, booléen faux et `null` puis
  vérifient l'alerte et le blocage du retour.
- L'utilitaire s'appelle désormais `validationSupport.ts`, distinct de
  `SupportEtude.tsx` aussi sur un système de fichiers insensible à la
  casse. Le test de l'utilitaire a été relancé par le relecteur après
  renommage : 1 test vert.
- Le parcours navigateur comprend maintenant un rechargement de page
  avant le retour de la première question et vérifie la conservation
  exacte de la réponse saisie. La clôture du parcours demeure testée.

Verdict de contre-relecture du code : **aucun bloquant trouvé dans le
périmètre examiné**. Les deux défauts signalés sont corrigés à l'inspection
et ont des scénarios de régression adaptés. L'exécution des E2E renforcés
est pilotée par l'auteur ; aucun résultat de cette exécution n'est encore
attribué à la présente contre-relecture.

Réserves restantes : pas d'assertion directe de non-ajout d'événement
dans IndexedDB pour les supports rejetés ; l'absence de crédit repose
ici sur le blocage de l'action et la garde de `noteCarte`. La synchronisation
réelle et l'acceptation sur un téléphone physique restent des preuves
distinctes. La collecte lourde, les sources PDF et le contenu du chapitre
ne sont toujours pas couverts par cet avis de code.

## Résultats transmis par l'auteur et revue de l'installateur

L'auteur a transmis les résultats suivants : 18 E2E verts sur le workspace
et sur un clone de livraison isolé conservant l'authentification originale,
299 tests Vitest et 6 contrôles de publication verts. Ces exécutions sont
attribuées à l'auteur, non au relecteur.

Revue statique supplémentaire de `installer_pilote.py`, sans exécution ni
publication par le relecteur : le manifeste et les empreintes bornent les
fichiers transférés, le paquet doit correspondre au SHA demandé, la copie
publique précède les remplacements atomiques par fichier, index puis service
worker en dernier. Les fichiers de données joueur et l'API ne sont pas
restaurés par cet installateur. L'installateur ne nécessite pas Node.
Les anciens assets additionnels sont conservés, ce qui protège les onglets
encore ouverts. Le contrôle Caddy porte sur la lisibilité des fichiers
installés ; il ne remplace pas un essai HTTPS authentifié.

Le premier rollback laissait le clone détaché. L'auteur l'a corrigé : main
initiale exigée, ancien SHA conservé, refus d'une HEAD tierce, restauration
de la branche et de HEAD, vérification avant autorisation de redémarrer le
timer. Ce point est corrigé à l'inspection.

Un dernier point a été signalé avant utilisation : la sauvegarde ne doit
pas précéder la mise au repos du générateur, et le constat d'un service
actif ne doit pas déclencher une restauration concurrente alors qu'aucune
mutation de livraison n'a commencé. Au dernier état inspecté, l'arrêt du
timer arrivait après `cp -a` et le refus du service actif était dans le bloc
qui restaure la publication. Déplacer arrêt/refus avant sauvegarde et avant
le bloc de mutation, ou démontrer un verrou réellement partagé par le
générateur installé. Ne pas attribuer un avis favorable de déploiement à
cette version tant que ce point reste ouvert.

## Clôture des réserves de l'installateur

Dernière contre-lecture du fichier, 06/09/2026 : **les deux réserves de
déploiement signalées sont closes à l'inspection statique**.

1. Le rollback restaure bien la branche `main` et son ancien SHA, vérifie
   ces deux valeurs et laisse le timer arrêté si cette restauration échoue.
2. L'arrêt du timer puis le contrôle du service précèdent désormais toute
   sauvegarde et le bloc de mutation. Le service doit être explicitement
   `ActiveState=inactive` ; tous les autres états, dont `activating`, sont
   refusés hors du bloc de rollback. Un générateur en cours ne déclenche
   donc plus une restauration concurrente. Le choix de `systemctl show`
   évite d'assimiler le code d'échec de `is-active` à une preuve d'arrêt :
   le [code primaire de systemd](https://raw.githubusercontent.com/systemd/systemd/main/src/systemctl/systemctl-is-active.c)
   exclut notamment `activating` des états reconnus par cette commande.

Verdict borné : aucun autre bloquant statique trouvé dans l'installateur
actuellement examiné. Aucun déploiement, test d'échec réel, contrôle ACL
distant ou redémarrage VPS n'a été exécuté par le relecteur. Les vérifications
de publication et le retour arrière réel restent à constater lors de
l'exécution autorisée. Une action administrative indépendante qui démarrerait
manuellement le générateur pendant la livraison reste hors du verrou de ce
script si elle ne le respecte pas ; la fenêtre de livraison doit rester
exclusive.

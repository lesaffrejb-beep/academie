# Essayer l'accueil et les comptes

Actualisation du soir : intégration sur main et publication VPS demandées
par JB ; voir [le compte rendu de publication](PUBLICATION-VPS.md).
La description de copie isolée ci-dessous retrace la première livraison.

05/09/2026. Outil Codex, modèle GPT-6. Décision 0042, cahier
ACA-ONBOARDING-1. Copie indépendante issue du commit 89cc630, sans les
modifications non commitées de la session principale. Branche
`codex/onboarding-premiere-connexion`. Aucun push ni déploiement VPS.

## Lancer et essayer

Dans la copie dédiée : `npm --prefix web run build`, puis
`python3 serveur/essai_local.py --port 5186`. Ouvrir
[le premier essai sur ce Mac](http://127.0.0.1:5186/academie/).
La base dédiée `etat/essai-local.sqlite` reste hors Git. Le navigateur
conserve un journal par identifiant de compte ; les brouillons sont aussi
séparés. Les anciennes réponses anonymes ne sont jamais attribuées
implicitement à un nouveau compte. Les exporter depuis l'ancien client
avant toute reprise humaine explicite.

Créer chacun son compte mail/mot de passe/pseudo, choisir son cursus.
La première étude demande une tentative, puis propose la leçon et ses
exercices. L'onglet Élèves montre les pseudos et cursus, permet de se
masquer, synchroniser, exporter et se déconnecter. Un seul cursus actif
par compte. Le mot de passe n'est pas un chiffrement du disque local.
Le lien magique fourni manuellement par JB reste le secours ; pas de
mail de récupération automatique ni de vérification de possession.

Le build et l'API sont servis ensemble sur loopback. Pour l'essai depuis
les téléphones, la publication et la migration sur le VPS restent à
faire autoriser ; cette livraison n'est pas encore accessible à distance.
Le client et l'API doivent être installés ensemble, avec le catalogue.
Les bases de test utilisent des adresses fictives `example.test` et ne
sont ni copiées dans la base d'essai vierge ni comptées comme élèves réels.

## Ce qui est disponible pour apprendre

| Cursus | Programme | Études jouables | Cartes |
|---|---:|---:|---:|
| Copropriété | 389 chapitres | 3 | 93, dont 76 v1 |
| IFSI | 375 chapitres | 2 | 10 |

Sources : programmes JSON et `site/banque.json`, recalculés dans cette
session. Les cinq études comportent tentative, notion, exemples,
questions, explications, sources et synthèse. Quatre cartes portent une
image, avec deux fichiers SVG distincts ; pas de carte de type lecture
servie dans cette banque. Un programme écrit n'est pas un cours livré.

Les critiques IFSI et copro sont prises en compte dans les révisions
antérieures, désormais accompagnées de contre-relectures : le lot copro
est clos au périmètre de ses corrections (ROADMAP.md et livraison
experience-2026-09-05). Les cartes IRSI/CIDRE signalées restent exclues.
Cela ne transforme pas les 764 chapitres de programme en 764 cours.

Dix heures de cours variés par personne ne sont pas démontrées par ce
stock. La cible est à préparer par des séquences et lectures choisies,
puis à ajuster aux temps réellement observés. Ni temps de robot ni
répétition forcée pour remplir ce volume. Le transfert et la compétence
clinique restent distincts de la réussite des cartes.

## Les 70 PDF

La doctrine garde les documents chez le joueur, hors Git et hors serveur.
L'usine prépare, distribue et contrôle des unités ; les apports sont
rattachés aux chapitres avec leurs pages. Les lectures et schémas utiles
se sélectionnent ensuite ; cartes et leçons demandent un cahier et une
relecture indépendante. Aucune donnée client de labor n'entre ici.

[Prompt à coller à l'agent](../../prompts/essai-10h-et-pdf.md).
Il distingue inventaire, lecture contrôlée, rattachement, cahier éditorial,
fabrication et essai humain. Le chemin réel des PDF reste à renseigner ;
aucun des 70 PDF n'a été traité dans cette livraison de comptes.

## Preuves

- [Relecture indépendante](RELECTURE.md), défauts corrigés et limites.
- `preuves/python.log` : contrôles métier, contenu et serveur.
- `preuves/controle.log` : cohérence du dépôt.
- `preuves/client.log` et `preuves/build.log` : tests et build.
- `preuves/mobile.log`, `preuves/mobile-reprise.log`, `preuves/ordinateur.log` :
  38 scénarios par viewport ; contexte du test mouvement réduit corrigé
  pour lui fournir son compte fictif, puis reprise verte.
- `preuves/comptes-reels.log` : vrai build et API locale avec comptes fictifs,
  sauvegardes séparées, reconnexion, masquage, réouverture hors ligne,
  restauration dans un navigateur vierge et cookie changé entre onglets.
  Deux scénarios passent ; 290 tests client et cinq tests de publication
  passent aussi.

Les tests de contenu interceptent uniquement leur profil de fixture ; le
test comptes utilise le vrai serveur, SQLite et les cookies. La revue
visuelle a examiné l'inscription mobile et la navigation des deux cursus.
Aucune modification de l'état joueur réel, aucun essai humain mesuré,
aucune acceptation visuelle de JB présumée.

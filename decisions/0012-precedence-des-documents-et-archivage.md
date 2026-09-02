# 0012, Précédence des documents et archivage de la conception d'août

- Statut : acceptée
- Date : 02/09/2026
- Décideur : agent, sur le mandat de JB (« si les bases ne sont pas
  solides, tu peux les virer » ; « tout ce qu'il faut pour qu'un humain
  et une IA puissent avancer dans de bonnes conditions »)

## Décision

1. Les quatre documents de conception d'août (`BLUEPRINT` v1,
   `SPEC-PRODUIT`, `CADRAGE-PRODUIT`, `DESIGN`) sont déplacés **intacts**
   dans `archive/conception-2026-08/`. Ils ne pilotent plus rien.
2. La conception v2 tient en six documents à la racine : `DOCTRINE`,
   `BLUEPRINT`, `PROGRAMME`, `METHODE` (avec `CADRAGE-SCIENTIFIQUE` en
   bibliographie), `ARCHITECTURE`, `DIRECTION-ARTISTIQUE`, plus
   `ROADMAP` et `decisions/`.
3. La précédence est celle de `DOCTRINE.md` §4. Le valideur prime sur
   tout texte de format.
4. Ce qui est **gardé sans changement** parce que solide : le moteur
   Python et ses tests, le contrat carte-v1 (jusqu'au v2), la banque, le
   gabarit de domaine et son guide, `CORPUS.md`, `METHODE.md` (étendu),
   `CADRAGE-SCIENTIFIQUE.md`, `IDEES-EN-VOL.md`, les documents
   NotebookLM, la publication VPS.
5. Ce qui est **déclaré remplaçable** : le client (`client/`, `site/`),
   `tooling/check.py` pour sa partie archipel.

## Contexte

Le 02/09, le dépôt portait 8 300 lignes de documents en couches
(28/08, 29/08, 30/08), avec trois documents qui « faisaient foi » chacun
sur une partie. Un agent frais ne savait plus quoi lire. Le brief du
02/09 change l'habillage, le rythme, la profondeur et le social : une
réécriture cohérente coûte moins qu'une cinquième couche.

## Conséquences

- `README.md` et `AGENTS.md` réécrits ; `gabarit-domaine/` et
  `CONTRAT-CARTE-V1.md` pointent vers les nouveaux documents.
- Les commentaires du code qui citent « BLUEPRINT §n » ou
  « SPEC-PRODUIT §n » restent valables via la table de concordance de
  `BLUEPRINT.md` §14 ; ils se mettent à jour au fil des chantiers qui
  touchent ces fichiers, jamais en masse.
- Toute session qui trouve une contradiction entre deux documents la
  règle par la précédence et laisse une ligne dans `decisions/` si elle
  a dû trancher.

## Réouverture

Quand la v2 aura elle-même trois couches, on recommence.

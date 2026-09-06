# 0047 : Un pipeline documentaire économe, ouvert et auditable

- Statut : politique retenue sur demande explicite de JB ; automatisation
  complémentaire à réaliser, résultats et réserves dans le dossier de preuves.
- Date : 06/09/2026.
- Auteur : Codex / GPT-6.
- Complète 0026, 0027, 0034 et 0046 ; ne retire ni les unités ni les sceaux.

## Contexte et critères

JB veut reprendre le pipeline avec d'autres agents, maîtriser son coût et
contrôler au hasard. La lecture visuelle de tout et la réécriture manuelle
de toutes les pages mobilisent inutilement un agent généraliste lorsqu'une
extraction déterministe suffit. Mais les trois PDF fournis exposent des
colonnes mélangées, du texte masqué et des scans dans des pages textuelles.

Critères : fidélité au visible, attribution à la page, indépendance de
l'outil agent, coût observable, confidentialité, droits et réversibilité.
Ni un Markdown propre ni un score lexical ne certifient le fond.

## Décision

1. Conserver le PDF original et son SHA-256 ; diagnostiquer les pages avant
   tout traitement cher. Extraction native locale comme première passe.
2. Escalader les seules pages nécessaires : autre extraction, structure de
   document/table, OCR ciblé, puis vision pour les figures et conflits.
   Garder les versions, options, sorties et erreurs. Aucun moteur cloud ni
   API payante requis ; tout nouvel envoi ou coût demande autorisation.
3. Comparer sur des témoins réels et des références visuelles. Les outils
   non exécutés restent « non mesurés » ; aucun champion universel déduit.
   Le banc autonome n'ajoute aucune dépendance au produit. Les licences
   des moteurs et des poids restent à examiner avant leur intégration.
4. Séparer fidélité de transcription, validité de l'assertion et efficacité
   pédagogique. Chaque assertion enseignée doit rejoindre une page, une
   portée, un statut et les contenus qui l'utilisent.
5. Concevoir grille/production avant cours ; produire leçon, exercices et
   corrigés spécifiques, pièces contradictoires et cas de transfert.
   Un moteur interactif sans données propres n'est pas un cours.
6. Cumuler relecture indépendante des éléments critiques et sondage du
   reste avec graine choisie après gel du lot. Une erreur critique suspend
   les descendants concernés et étend le contrôle à la même famille de pages.
7. Coût API, durée machine et coût tokens sont des mesures distinctes.
   Inconnu reste inconnu ; aucune économie ou fiabilité chiffrée inventée.
8. Les sorties tierces par page du banc restent littérales. Le contrôle des
   tirets exclut uniquement `sources/benchmark-pdf/ESSAI/document-NNNN.md`,
   comme il exclut déjà les pivots de sources. Il continue de contrôler les
   textes éditoriaux, rapports, JSON et cours ; aucune preuve brute n'est
   retouchée pour satisfaire une règle typographique de notre voix.

## Options examinées

- Poppler seul : rapide et déjà utilisé, insuffisant sur les scans mixtes
  et certains contenus masqués ; gardé comme témoin, pas arbitre du visible.
- MarkItDown/pypdf/pdfplumber : comparateurs locaux ; gain dépendant de la
  page. MarkItDown sans OCR ne résout pas les scans de notre échantillon.
- PyMuPDF : comparateur utile mesuré hors produit ; intégration/licence non
  décidée par ce banc.
- Docling : deux configurations avec RapidOCR désormais mesurées ; des
  défauts subsistent. PyMuPDF4LLM sans OCR également essayé.
- Marker/MinerU/PDF-Extract-Kit/olmOCR/TATR : options spécialisées ; poids,
  environnement, périmètre et licences à prendre en compte ; non testés ici.
- Firecrawl : collecte web et parsing document documentés ; pas requis pour
  nos fichiers locaux, aucun envoi effectué. Son composant pdf-inspector
  local a été mesuré sans OCR ; pas le service cloud.
- Vision généraliste sur toutes les pages : conserve un intérêt de contrôle,
  mais n'est plus notre stratégie d'extraction par défaut.

Les capacités et limites sont sourcées dans
`travail/expertise-2026-09-06/COMPARATIF-OUTILS.md` ; ne pas les assimiler
aux résultats locaux de `BENCHMARK.md`.

## Conséquences, risques et réouverture

Le protocole opérationnel est `travail/expertise-2026-09-06/PIPELINE.md`.
Le moteur usine actuel ne possède pas encore ce routage par page ni de
verrou automatique assertion → descendants. Ils restent des étapes
manuelles explicites ; aucun état « validé » supplémentaire n'est simulé.

Le choix de moteur peut changer après essai sur le corpus de JB et un
échantillon nouveau. La correction humaine/agent n'est pas infaillible ;
l'échantillonnage ne prouve pas l'absence de tout défaut. Une nouvelle
version de moteur ou de source déclenche la reprise des contrôles concernés.

Le code du banc est partageable sous les règles du dépôt ; les PDF et leurs
transcriptions ne deviennent pas libres par conversion. Aucun compte ni
état joueur n'est modifié. Aucune publication incluse.

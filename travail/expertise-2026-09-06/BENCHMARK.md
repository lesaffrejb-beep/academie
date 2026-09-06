# Essai local de conversion PDF — 06/09/2026

Codex / GPT-6. Banc autonome dans ce dossier, sans dépendance ajoutée à
l'application. **Six pages difficiles, huit configurations, vingt témoins
par configuration.** Ce sont des tests ciblés, pas un taux de fiabilité.

## Pièces et mesure

Angers p. 1/9/12, Focus p. 26/32, PDHH p. 6. Les empreintes complètes,
les témoins et leur raison sont dans `benchmark-temoins.json`.
Le rendu original a été inspecté pour établir ces témoins ; pas de
transcription de référence exhaustive, pas de CER/WER calculé.
La p. 26 vérifie une association ligne/chiffres, pas l'ensemble du tableau.

Résultats détaillés partageables : `benchmark-resultats.json` (version
script, SHA des témoins, SHA des sorties, résultat de chaque témoin).
Sorties intégrales et commandes :
`sources/benchmark-pdf/2026-09-06-comparatif-04/rapport.json`, hors git.
Le PDF original n'a pas été modifié, ni le journal usine.

| Configuration | Version testée | Témoins satisfaits / 20 | Durée cumulée des six processus |
|---|---|---:|---:|
| Poppler layout | 26.07.0 | 8 | 0,587 s |
| Poppler raw | 26.07.0 | 11 | 0,569 s |
| PyMuPDF texte | 1.28.2 | 14 | 0,987 s |
| PyMuPDF tri spatial | 1.28.2 | 12 | 0,990 s |
| pypdf plain | 6.10.0 | 11 | 0,968 s |
| pypdf layout | 6.10.0 | 12 | 0,863 s |
| pdfplumber extract_text | 0.11.9 | 11 | 1,383 s |
| MarkItDown, sans OCR/LLM | 0.1.7 | 9 | 4,496 s |

48 extractions abouties, zéro erreur d'exécution sur cette passe. Cela
ne signifie pas zéro erreur d'extraction : aucun moteur ne passe tous les
témoins. Toutes les configurations manquent les témoins scannés de la
couverture Angers et du corps de l'arrêté PDHH. Les parasites du Focus p. 32
subsistent dans les sorties testées. La discussion et le tableau du Focus
p. 26 sont contradictoires dans le document lui-même : l'extracteur ne peut
pas décider lequel est vrai.

PyMuPDF texte satisfait davantage de **ces** témoins ; ce n'est ni une
estimation de sa précision globale, ni une décision de l'intégrer. `raw`
peut coller les mots, `sort` peut casser des relations, le Markdown peut
fabriquer des tableaux. Le contrôle visuel de MarkItDown p. 12 montre des
lignes de prose réparties en cellules qui ne sont pas une table du document.

## Limites de l'expérience

- Pages choisies pour leurs défauts connus : sélection biaisée, volontaire.
  Le test de résistance ne représente pas les 266 pages des trois PDF.
- Témoins établis par l'auteur avant comparaison, mais non annotés par un
  panel humain. Les vérifier et étendre les références avant tout classement.
- Présence/absence normalise Unicode et espaces. Les négatifs tolèrent la
  fragmentation par espaces et séparateurs Markdown ; cela reste un contrôle
  lexical, pas une preuve d'absence de tout parasite. Un moteur peut réussir
  un témoin et dégrader tout le reste de la page.
- Un processus lancé par page, une seule répétition finale, caches non vidés.
  Les durées incluent imports et lancement ; pas un débit de production.
- MarkItDown reçoit une page réemballée en mémoire par pypdf ; SHA du dérivé
  conservé dans le rapport intégral. Ce biais doit être retiré ou partagé
  par tous les concurrents avant une comparaison de production.
- Plusieurs méthodes partagent leur extraction sous-jacente. Ce ne sont
  pas huit observations statistiquement indépendantes.
- Aucune API de conversion : coût API du banc 0. Installation, calcul local,
  abonnement et revue ne sont pas gratuits ; tokens agent non mesurés.
- Cette première passe n'exécute pas de moteur OCR. Les extensions réelles
  figurent séparément dans `BENCHMARK-STRUCTURE.md` ; les options uniquement
  documentaires restent identifiées dans `COMPARATIF-OUTILS.md`.

## Reproduction

Les trois PDF doivent être présents aux chemins du manifeste. Le script
vérifie SHA-256 et nombre de pages avant tout résultat. Une autre édition
est refusée, pas comparée silencieusement. Aucun export propriétaire requis.

```sh
python3 travail/expertise-2026-09-06/test_benchmark_pdf.py
python3 travail/expertise-2026-09-06/benchmark_pdf.py \
  --out sources/benchmark-pdf/MON-ESSAI-NEUF \
  --pymupdf-python CHEMIN-PYTHON-PYMUPDF \
  --bundled-python CHEMIN-PYTHON-PYPDF-PDFPLUMBER \
  --markitdown-python CHEMIN-PYTHON-MARKITDOWN
```

Les `CHEMIN-...` sont des exécutables Python à remplacer, pas des clés API.
Omettre `--markitdown-python` donne `non-mesure`. Un moteur absent ou un
timeout donne `erreur`, témoins inconnus, jamais un succès par défaut.
Le coordinateur retourne normalement après production du rapport même si
un moteur échoue : lire ses statuts, pas seulement le code de sortie shell.
Il refuse de réutiliser un répertoire de sortie existant.

Environnements employés sur ce Mac :

- coordinateur et PyMuPDF : `/opt/homebrew/opt/python@3.14/bin/python3.14` ;
- pypdf/pdfplumber : Python du runtime Codex `26.904.11930` ;
- MarkItDown : `/private/tmp/academie-pdf-bench.uNpd2O/venv/bin/python`,
  environnement temporaire avec `--system-site-packages`, installé par pip,
  pas une modification du Python applicatif.

Pour une reprise portable, créer des environnements dédiés et épingler les
versions du tableau. MarkItDown a notamment utilisé pdfminer.six 20251230,
pdfplumber 0.11.9 et pypdf 6.10.0. Le runtime d'origine est partagé en lecture :
ce n'est pas un conteneur hermétique. Le rapport enregistre la plateforme.
Une reproduction sur une autre machine doit conserver ses propres durées.

## Tests rouges et corrections du banc

1. Les tests ont d'abord échoué faute de module `benchmark_pdf`.
2. Les sept garde-fous initiaux ont passé après implémentation : empreinte,
   positifs/négatifs, absence de résultat, chiffres/signes, ordre et tirage.
3. La première passe a conservé douze erreurs PyMuPDF : un avertissement
   de l'ancien import `fitz` précédait le JSON. Import corrigé en `pymupdf` ;
   aucune erreur transformée en résultat vide prétendument correct.
4. Un test rouge supplémentaire a montré qu'un parasite découpé par des
   cellules pouvait échapper au témoin négatif. Normalisation ciblée corrigée,
   sans effacer les signes/unités des contrôles numériques positifs.
5. La revue indépendante a révélé des faux positifs numériques (sous-chaîne,
   décimale, signe). Deux tests rouges puis correction des frontières.
6. Passe finale : dix tests dédiés passent, 48 résultats mesurés. Les passes
   précédentes restent dans `sources/benchmark-pdf/`, non écrasées.

## Sondage reproductible pour le prochain relecteur

```sh
python3 travail/expertise-2026-09-06/benchmark_pdf.py \
  --audit-seed MA-GRAINE-CHOISIE-APRES-GEL --audit-size 8
```

Produit un plan `a-auditer`, pas un verdict. Le tri par SHA-256 est documenté
dans le code ; pages imposées exclues du tirage, mais toujours à contrôler
en plus. Exemple de graine déjà essayée : `JB-2026-09-06-controle-01`.

| Document | Pages tirées avec cette graine |
|---|---|
| Angers | 11, 19, 22, 23, 31, 36, 47, 53 |
| Focus | 6, 8, 10, 12, 18, 20, 25, 27 |
| PDHH | 19, 28, 40, 111, 145, 148, 156, 166 |

Ce tirage a été testé, **ces pages n'ont pas toutes été auditées**. Le
relecteur indépendant choisira une autre graine et conservera ses erreurs,
même si elles contredisent le choix de moteur proposé.

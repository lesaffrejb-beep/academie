# Relecture indépendante du premier banc

06/09/2026. Avis de l'agent `revue_pipeline`, retranscrit par Codex / GPT-6.
Relecture technique d'agent, pas validation humaine ni lecture complète des PDF.

La revue a détecté les faux positifs numériques du comparateur ; correction
précédée de deux tests rouges, puis dix tests verts. Sur la passe
`comparatif-04`, les 48 résultats, les empreintes du script, des témoins et
des sorties ont été vérifiés. Les témoins des pages Angers 9/12 et PDHH 6 ont
été confrontés aux images. Aucun bloquant restant signalé sur ce périmètre.

Le sondage a été exécuté deux fois : mêmes pages, exclusions respectées.
Cela n'audite pas les pages tirées. Le comparateur reste lexical, sans analyse
générale des quantités. Les documents web n'ont pas été revérifiés par ce
relecteur. Les extensions structurées/OCR ne sont pas couvertes par cet avis.

La désynchronisation du résumé (passe 03/huit tests) signalée par le relecteur
a été corrigée dans `BENCHMARK.md`. Aucun original ou sceau usine n'a changé.

## Complément structuré

Nouvelle passe du même relecteur indépendant : trois tests dédiés verts,
quatre rapports finaux complets, scripts embarqués et 24 sorties avec SHA
conformes. Comptages confirmés : PyMuPDF4LLM 16/20, Docling hybride 16/20,
Docling FULL_PAGE 17/20, pdf-inspector 8/20. Calculs conditionnels du budget
API confirmés : scénario A 0,665 / 6,65 / 11,704 dollars, B Luna 2,5536 dollars.
Il ne s'agit pas de dépenses mesurées.

Deux réserves rappelées par la revue : FULL_PAGE garde des parasites dans
Focus 32 ; pdf-inspector local n'est pas le service cloud Firecrawl.
Ces distinctions sont explicites dans `BENCHMARK-STRUCTURE.md`.

## Frontière typographique des preuves brutes

Après test rouge puis vert, la dernière revue confirme que l'exception de
`tooling/check.py` ne touche que la typographie des pages brutes du banc :
42 fichiers des sept passes présentes, aucun rapport/cours/JSON actuel.
Réserve : la convention dépend du chemin et du nom, pas du manifeste ;
ne pas nommer un rapport éditorial `rapport-2026.md` dans un dossier d'essai.
Contrôles finaux : `python3 app/tests.py` vert, puis
`python3 tooling/check.py` zéro erreur et `git diff --check` sans défaut.

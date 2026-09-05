# Cahier ACA-PILOTE-CONTRAT-1 : contrat sûr pour trois chapitres

Résultat : un pilote v2 coexiste avec la banque v1 sans mensonge de contrat,
doublon ni provenance inventée. Dépend de ACA-PROGRAMME-1 et ACA-SOURCES-1.
Bloque ACA-ETUDE-1 ; la migration globale reste ACA-CONTRAT-2.

Périmètre : contrats, `app/valide_chapitres.py`, génération/publication de
banque, lecture client du contrat et tests associés ; fixtures et rapport.
Aucune promotion de brouillon, migration de banque ou réécriture de journal.

1. Tests rouges : ID dupliqué entre v1/v2, contrat mixte annoncé, expiration,
   source numérique absente, provenance incomplète, relecture dans la même
   session que l'écriture. Reprendre la reproduction conservée par l'audit.
2. Définir l'attestation : auteur et session, source consultée, assertion
   examinée, date, réserves. Une autre session du même modèle est possible ;
   un nom différent ne prouve pas l'indépendance. Le contrôle structurel
   n'atteste jamais à lui seul la vérité ni la fidélité à une source.
3. Prouver la publication mixte prévue, avec étiquette globale compatible
   v1 tant que nécessaire. Afficher honnêtement une provenance manquante ;
   ne pas créer de faux tampon rétroactif. Exclure les cartes invalides.
4. Distinguer mémoire FSRS de l'item, version du contenu et preuve de
   compétence. Spécifier le traitement d'une correction de sens avant le
   pilote ; aucun score de compétence dérivé du seul calendrier FSRS.
5. Revue indépendante, tests Python et web ciblés, build, `app/tests.py`
   puis `tooling/check.py`. Reporter les défauts de contenu au lot éditorial.

Fini quand : fixtures adverses refusées, mélange sûr, contrat/documentation
alignés, aucune origine inventée, rapport avec limites. Ce résultat ne vaut
pas validation scientifique ou métier des trois futurs chapitres.

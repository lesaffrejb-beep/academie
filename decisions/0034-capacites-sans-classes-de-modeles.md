# 0034, Capacités observées, sans classes de modèles

Date : 05/09/2026. Décision explicite de JB pendant l'audit Académie :
retirer les catégories petit, moyen et grand et poursuivre le travail.
Amende 0027, `MODELES.md`, `CONTRIBUER.md` §8 et `AGENTS.md` §9.

Le nom d'un modèle ne fixe plus ce qu'il peut faire. Aucun tableau de
classement n'autorise ou n'interdit un cahier, une carte, une relecture
ou un niveau de chapitre. L'outil, le modèle connu et la session restent
utiles pour retracer la production et la relecture.

L'usine conserve les contrôles documentaires et la reprise par unités.
Les valeurs communes sont 12 pages au départ et 25 au plus, configurées
et identiques dans le gabarit. Elles reprennent une enveloppe déjà utilisée
par le dépôt ; ce sont des choix opératoires, sans autorité scientifique.
Les refus réduisent la taille ; les contrôles successifs permettent de
l'augmenter. L'identité du modèle n'intervient pas.

Compatibilité : les états existants gardent leurs unités, sceaux et
historique. Leur ancien champ de classe est ignoré. Un ancien argument
CLI est toléré, signalé obsolète et ignoré ; il n'apparaît plus dans l'aide
ni dans les prompts. Aucun état réel ni journal joueur n'est migré.

Les contrôles de configuration communs entrent dans `tooling/check.py` :
la fonction existait mais n'était pas appelée par la porte globale.
Les seuils de fidélité, contrôles de chiffres et relecture restent en place.
Leur réussite ne certifie pas la vérité d'un document.

Pour le code et l'audit, la déclaration dans le point de travail suffit.
L'usine ne distribue que les unités de documents. Les limites relatives
aux données client, aux actes irréversibles et à la publication demeurent.

Exécution et preuves : `chantiers/ACA-MODELES-2.md` et tests usine.
Les essais couvrent noms inconnus, option obsolète, anciens états,
changement d'agent, sceaux conservés et adaptation aux contrôles.

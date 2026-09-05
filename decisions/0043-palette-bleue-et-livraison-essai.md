# 0043 : Palette bleue et livraison de l'essai

05/09/2026, demande explicite de JB. Outil Codex, modèle GPT-6.

JB demande de reprendre les travaux interrompus, de conserver les modules,
l'onboarding et la palette bleue des captures fournies, puis de pousser sur
main et publier sur le VPS pour un essai le soir même.

La palette Papier devient blanc froid/bleu, Nuit bleu profond. Les accents
restent attribués par rang de domaine. Les contrastes des textes et boutons
sont ajustés dans les tokens, sans changer cette direction. Source Sans 3,
OFL et déjà auto-hébergée, sert les titres et le corps ; la police Hurme
mentionnée dans le diff n'est pas disponible dans le dépôt. Aucune police
propriétaire ni ressource distante n'est ajoutée. Cette décision remplace
les mentions de palette rosée/prune et de titres Fraunces des décisions
précédentes pour le client actuel. Les modules et les animations sont gardés.

Les comptes élèves restent personnels, séparés en SQLite et IndexedDB.
L'accès HTTP de test donné par JB est ajouté uniquement à Académie dans
Caddy ; les autres applications gardent leurs règles. Il ne remplace pas
le compte élève. La migration 0002 s'applique après sauvegarde SQLite.
Les anciens clients ne doivent pas pouvoir déposer un journal sans indiquer
le profil auquel il appartient quand ils utilisent un cookie partagé.

Le volume disponible reste un petit pilote : aucune promesse de dix heures
par métier, de programme intégral ni d'effet pédagogique mesuré. La preuve
sur téléphone physique et l'acceptation de JB restent ouvertes après les
contrôles automatisés et le parcours HTTPS authentifié.

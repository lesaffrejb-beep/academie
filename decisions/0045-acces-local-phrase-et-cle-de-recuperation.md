# 0045. Accès local : pseudo, phrase secrète et clé de récupération

06/09/2026, JB, Codex, GPT-5.6. Après perte d'un mot de passe et refus
d'un service d'envoi de mails pour un cercle de quatre personnes.

## Décision

Un compte se crée avec un pseudo unique et une phrase secrète de 12 à
256 caractères. L'adresse mail ne fait plus partie de l'accès, du
client, ni de la création de compte.

À la création, le serveur génère une clé de récupération aléatoire de
128 bits. Elle est affichée une seule fois, avec l'instruction de la
mettre dans un gestionnaire de mots de passe ou un fichier local hors du
dépôt. Le serveur n'en garde qu'un hachage scrypt. Elle permet de choisir
une nouvelle phrase secrète et produit immédiatement une nouvelle clé.
Toutes les anciennes sessions sont alors révoquées.

Si la phrase secrète et la clé de récupération sont toutes deux perdues,
le compte et son journal ne sont pas récupérables. Il n'existe pas de
secours par mail, ni de contournement par JB.

Les comptes d'essai existants, leurs sessions et leurs journaux distants
sont supprimés par une commande locale qui exige la phrase de confirmation
exacte. Les journaux déjà présents dans les navigateurs ne sont pas
effacés par le serveur et ne sont jamais rattachés silencieusement à un
nouveau compte.

## Conséquences

- La phrase et la clé ne sont jamais conservées en clair.
- Un pseudo n'est pas un secret, mais il est unique afin de rendre la
  connexion praticable à quatre personnes.
- Les tentatives de connexion et de récupération sont limitées par
  origine et par pseudo haché, avec le même refus générique qu'un compte
  absent.
- Le lien magique et toute dépendance à un fournisseur de mail sortent de
  l'accès courant.

## Réouverture

Un code court sur appareil déjà reconnu pourra être envisagé après un
usage réel. Il ne remplacera ni la phrase secrète ni la clé de
récupération.

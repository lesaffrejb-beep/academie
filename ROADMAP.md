# Roadmap Académie — active

Académie transforme des sources vérifiées en une pratique de quinze minutes qui
rend JB réellement meilleur. Le produit échoue s'il est impressionnant mais
n'est pas ouvert le matin, ou s'il récompense des clics sans améliorer la
rétention et le transfert vers le terrain.

Cette page est la seule roadmap active ; `roadmap.json` est la file exécutable.
Le cadrage M0-M11 d'août 2026 est conservé sans perte dans
[`archive/roadmaps/`](archive/roadmaps/README.md).

## La preuve recherchée

- au moins 4 séances par semaine, sans culpabilisation après une coupure ;
- une séance courte jouable en moins de 5 secondes et terminable en 3 minutes ;
- rétention à froid mesurée après environ 30 séances ;
- transfert visible : une erreur terrain devient apprentissage, puis disparaît ;
- 100 % des cartes servies sourcées, datées, valides et dans la bonne couche ;
- coût de génération et de correction LLM connu avant généralisation.

## Maintenant — prouver le rituel

1. Produire le tableau de bord minimal du rituel depuis le journal append-only :
   séances commencées/finies, abandons, durée si disponible, rappels et modes.
2. Éprouver l'archipel SVG désormais autonome : phare, îles, routes, bateaux,
   brouillard et cycle jour/nuit doivent rester lisibles sur mobile et refléter
   uniquement la progression locale réelle, sans import métier ni accès à ERP.
3. Jouer environ 30 séances réelles, puis refaire à froid 20 cartes du premier
   lot. Le résultat décide du format suivant.
4. Cartographier les sources crédibles pour les trois domaines encore vides :
   énergie, plans et culture ; ne pas produire de volume avant le bilan d'usage.

## Ensuite — augmenter ce qui fait apprendre

1. Corriger d'abord les frictions révélées par le journal du rituel.
2. Tester réponse libre ou atelier selon le bilan : recommandation par défaut,
   réponse libre sourcée sur un petit lot, avec coût par correction mesuré.
3. Alimenter les domaines utiles par lots de 15–20 cartes, double passe et
   échantillon humain ; un arrivant ne valide jamais seul une matière qu'il
   découvre.
4. Relier le carnet d'erreurs aux prochains exercices sans le rendre visible à
   d'autres profils.
5. Accepter du contenu ERP uniquement via un artefact anonymisé et validé.

## Plus tard — ouvrir sans détruire le produit

1. Éprouver le kit de domaine sur Arthur ou un domaine public de secours.
2. N'ouvrir un second compte qu'après le bilan des 30 séances et quatre semaines
   supplémentaires à au moins quatre séances par semaine.
3. Décider alors authentification, paiement de l'infrastructure, suppression de
   compte et responsabilité de traitement.
4. Les amis et défis arrivent en dernier, derrière consentement mutuel et mesure
   de leur effet sur le rituel. La comparaison sociale est coupée si elle nuit à
   l'apprentissage.

## Questions d'architecture déjà prémâchées

### Client autonome

- **Recommandation** : React + TypeScript + Vite dans Académie, en extrayant
  seulement les composants utiles du front ERP ; aucune bibliothèque de design
  copiée si elle doit vivre dans Socle.
- La banque est chargée au runtime depuis l'artefact publié. Un échec réseau
  conserve la dernière banque valide ; jamais d'écran blanc le matin.
- La 2,5D est désormais un habillage SVG/CSS autonome. Three.js et les assets 3D
  n'entrent qu'après preuve du rituel et budget de performance mobile.

### État d'apprentissage

- **Maintenant** : journal JSONL append-only local et exportable, parce qu'il n'y
  a qu'un joueur et que FSRS sait tout recalculer.
- **Au premier vrai multi-compte** : SQLite côté serveur avec migrations,
  sauvegarde et suppression de profil testées.
- PostgreSQL n'entre qu'en cas de concurrence ou volume mesurés que SQLite ne
  tient plus. Aucun service de cache n'est prévu.

### Authentification

- **Maintenant** : accès privé existant ; aucun système de comptes à maintenir.
- **Plus tard** : magic links à durée courte, sessions révocables et aucune clé
  API de tiers stockée. Le RGPD et la suppression de compte précèdent le pilote.

### IA dans la séance

- Le cœur — banque, FSRS, quiz exacts et progression — fonctionne sans LLM.
- La réponse libre commence par une expérience bornée et sourcée. La correction
  transporte la réponse et les sources nécessaires, pas tout le profil.
- Aucun abonnement Codex ou Claude n'est supposé appelable par une application.
  Une API dédiée exige plafond de coût, journal et mode dégradé.

### Fabrication d'un domaine

- **Recommandation** : dépôt de documents + kit local reproductible ; NotebookLM
  reste une source d'import avec provenance, jamais une dépendance runtime.
- Le contrat carte est versionné. L'artefact publié annonce sa version, ses
  couches et son hash ; le serveur refuse une version incompatible.

## Garde-fous de produit

- Pas de streak punitive, dette de révisions ou classement public.
- Pas de social, 3D, marketplace ou multi-tenant avant preuve du rituel.
- Pas de donnée client ERP, même dans un prompt de génération.
- Toute carte fausse est retirée du service immédiatement, puis corrigée à la
  source ; le bouton de signalement n'est pas le contrôle qualité principal.
- Une modification de règle pédagogique exige une source et un test de mesure.

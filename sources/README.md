# sources/

Le registre des sources du domaine copropriété, et les copies locales.

- `REGISTRE.md` : **versionné**. Une ligne par source : nature, parti,
  fiabilité (A, B, C), date de vérification, ce qu'on en tire, ce qu'on
  n'en tire pas. Les cartes héritent de la nature et du parti posés
  ici ([`decisions/0004`](../decisions/0004-la-source-porte-sa-nature-et-son-parti.md)).
- Tout le reste (`*.pdf`, `*.txt`, `*.html`, vidéos, transcriptions,
  captures) : **jamais versionné**, `.gitignore` en place. Copie locale
  sur le Mac, nommée par empreinte SHA-256, copie mensuelle sur NOIR
  (`ARCHITECTURE.md` §3). Un fichier de ce dossier ne monte jamais sur
  le serveur ni dans une livraison.

Le **pivot** d'un document lu (`decisions/0026`) : `sources/<empreinte>.md`
(Markdown par page, ancres `[p. n]`, titres, tableaux, figures décrites)
et `sources/<empreinte>.figures/` (pages à figures rendues). Hors git
comme le document. Les chapitres citent le pivot avec sa page.

L'usine (`app/usine/usine.py`, `decisions/0027`) ajoute à côté :
`<empreinte>.pages/` (le texte machine par page, témoin des contrôles),
`<empreinte>.structure.json` (titres candidats par taille de police),
`<empreinte>.etat.json` (unités, déclaration du modèle, sceaux, journal ;
revérifié à chaque `suivant`), `<empreinte>.fiche.json` (la fiche, dont
se déduit la ligne de registre) et, pour un document rattaché,
`<empreinte>.rattachements.json`. Tout hors git. Un document interne a
les mêmes fichiers sous `sources/interne/`.

Fiabilité :

| Note | Ce que ça veut dire |
|---|---|
| A | primaire, opposable : texte officiel, jurisprudence, institution, norme |
| B | secondaire sérieuse : doctrine signée, presse professionnelle, organisation professionnelle ou association avec parti déclaré |
| C | à recouper : éditeur, blog, notice, contenu commercial. Une carte qui n'a que du C porte le marqueur « à recouper » |

Le tri du carnet NotebookLM du 29/08 (`NOTEBOOKLM-A-RETIRER.md`) est la
première matière de ce registre. Dans un dépôt-domaine fabriqué avec le
gabarit, le même tableau s'appelle `sources/INVENTAIRE.md` (il porte en
plus le tas et les trous nommés) ; les colonnes nature, parti et
fiabilité y sont les mêmes. Le chantier `ACA-SOURCES-1` produit aussi la
forme machine `sources/registre.json` (versionnée), que le générateur lit
pour hériter `fiabilite` sur chaque source de carte.

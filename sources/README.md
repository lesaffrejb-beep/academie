# sources/

Le registre des sources du domaine copropriété, et les copies locales.

D'où vient un document et comment l'amener (Google Drive, iCloud,
NotebookLM, téléphone, page web, vidéo) : [`AMENER-UN-DOCUMENT.md`](AMENER-UN-DOCUMENT.md).

- `registre.json` : **versionné, il fait foi**. La forme machine du
  registre : une entrée par source, avec son `domaine_web` ou son
  `motif` (ce qui rattache une source de carte à sa ligne). Le
  générateur y lira `fiabilite` ; `app/tests_sources.py` refuse une
  source de carte qui n'a pas de ligne.
- `REGISTRE.md` : **versionné, régénéré**, jamais corrigé à la main :
  `python3 app/registre.py --md > sources/REGISTRE.md`. Une ligne par source : nature, parti,
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

L'**original** reste sur disque à côté du pivot : `preparer` copie le
fichier déposé sous son empreinte et ne l'écrase jamais. Un document
Markdown garde son original en `<empreinte>.source.md`, parce que le
pivot occupe déjà `<empreinte>.md` ; un PDF, un `.vtt`, un `.srt` ou un
`.txt` garde `<empreinte><extension>`. L'archive porte exactement les
octets du fichier déposé et se retrouve par son empreinte. Un `.vtt` ou
un `.srt` est nettoyé de ses horodatages, numéros de séquence et
étiquettes de locuteur avant d'être découpé en pages ; un `.txt` ou un
`.md` est repris tel qu'il est écrit, lignes numériques et préfixes
avant deux-points compris.

L'usine (`app/usine/usine.py`, `decisions/0027`) ajoute à côté :
`<empreinte>.pages/` (le texte machine par page, témoin des contrôles),
`<empreinte>.structure.json` (titres candidats par taille de police),
`<empreinte>.etat.json` (unités, déclaration du modèle, sceaux, journal ;
revérifié à chaque `suivant`), `<empreinte>.fiche.json` (la fiche, dont
se déduit la ligne de registre) et, pour un document rattaché,
`<empreinte>.rattachements.json`. Tout hors git. Un document interne a
les mêmes fichiers sous `sources/interne/`.

**Le dépôt.** Jette un PDF (ou une transcription) dans
`sources/a-preparer/`, puis `python3 app/usine/usine.py deposer`. Chaque
fichier est préparé comme par `preparer` et reste à sa place ; un
document déjà préparé est sauté. Un fichier qui échoue n'arrête pas les
suivants : le bilan compte les préparés, les documents déjà présents et
les échecs, nomme les échecs, et `deposer` sort non nul tant qu'il en
reste un ; aucun fichier du dépôt n'est supprimé ni déplacé. Dans
`<empreinte>.figures/`, les pages à figures sont rendues (`p-####.png`,
une page entière) et les images réelles extraites (`img-*.png`,
réutilisables telles quelles). Un PDF scanné sans couche texte est
signalé : `ocrmypdf --language fra` sur le fichier, puis `deposer` à
nouveau. Le dossier de dépôt n'est pas versionné (seul un `.gitkeep`
l'est).

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
fiabilité y sont les mêmes.

Le chantier `ACA-SOURCES-1` a rempli le registre le 03/09/2026 : 22
lignes, les 154 entrées de source des 84 cartes rattachées, `nature` (et
`parti` quand il existe) écrite sur chacune. L'héritage de `fiabilite`
au moment de la publication reste à faire : c'est `ACA-CONTRAT-2`.

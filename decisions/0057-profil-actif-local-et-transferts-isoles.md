# 0057. Un profil actif local, des transferts isolés

**Décision.** Un dossier d'état peut désigner le profil qui joue :
`etat/profil-actif.json`, hors git. Une commande sans `--profil` suit
ce choix. Écrire un profil (`profil --pseudo X ...`) l'active, et
`profil --activer X` sélectionne un profil déjà écrit. Un transfert
(`exporter` / `importer`) ne mélange jamais deux profils : l'import
refuse une sauvegarde dont le `profil` diffère avant la moindre
écriture, et seules des préférences validées voyagent avec le journal.

**Contexte.** Le 21/09/2026, JB amène le dépôt sur le poste Windows du
travail et Arthur clone chez lui. `ACA-ONBOARDING-2` avait posé
`etat/<pseudo>/profil.json`, mais aucune commande ne retenait le
pseudo choisi : sans `--profil`, la surface retombait sur
`profil_defaut` (`jb`). Un profil Arthur venait donc d'être écrit que
`accueil` et `etat` parlaient encore de JB. La revue a montré deux
autres fuites : `importer` fusionnait un journal sans regarder son
profil, et `exporter` laissait les préférences derrière lui. Le même
jour, le contrôle des pseudos a été durci : `re.match` avec `$`
acceptait un saut de ligne final, un point final ou `CON` passaient, et
`Arthur` / `arthur` pouvaient viser le même dossier sur un système de
fichiers insensible à la casse.

**Conséquences.** Chaque clone garde son choix local, comme il garde
son `etat/` : rien à synchroniser, aucune configuration partagée
réécrite. La précédence est `--profil`, puis la sélection locale, puis
`profil_defaut` pour ne pas casser un poste existant. Une sélection
illisible ou un profil incohérent nomment un trou au lieu de retomber
sur JB. Le format `academie-sauvegarde-1` gagne une clé `prefs`
facultative ; les sauvegardes sans elle restent importables, et un
profil local déjà présent n'est jamais écrasé.

**Réouverture.** Un besoin de plusieurs profils actifs sur un même
poste, un état partagé entre plusieurs machines, ou l'arrivée d'un
registre RGPD des états joueurs.

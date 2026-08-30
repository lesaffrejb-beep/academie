#!/usr/bin/env python3
"""
Liste de suppression pour le carnet NotebookLM « Copropriété ».

Le carnet est PLEIN (300/300). Chaque source retiree libere une place pour
une source primaire. Ce script range les sources a retirer par motif, du
plus evident au plus discutable, et dit ce qu'on garde et pourquoi.

Le classement de INDEX-NOTEBOOKLM.md est mecanique (nom de domaine). Ici
c'est un JUGEMENT, pose source par source : il se relit et se conteste.

  python3 app/tri_notebooklm.py
"""

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import index_notebooklm as ix  # noqa: E402

RACINE = Path(__file__).resolve().parents[1]
SORTIE = RACINE / "NOTEBOOKLM-A-RETIRER.md"
DATE = "29/08/2026"

# Doublons releves dans le panneau (meme titre depose deux fois).
DOUBLONS = [
    "Recouvrement des charges de copropriété impayées - Service Public",
    "202602_guide-aides-financieres_WEB.pdf",
    "Article 19-2 : la procédure accélérée au fond pour charges impayées - Grelier Avocat",
    "Le Plan pluriannuel de travaux (PPT) est-il obligatoire en copropriété - Matera",
]

# Motif -> domaines. Un domaine ne figure qu'une fois : le premier motif gagne.
MOTIFS = [
    ("Droit québécois",
     """Même vocabulaire, autre droit. Les six portent sur la mise en demeure ou
la gestion de « syndicat » au Québec : c'est le piège exact où une réponse
paraît juste et est fausse en France.""",
     {"educaloi.qc.ca", "lambertavocats.ca", "www.quebec.ca",
      "vitrinelinguistique.oqlf.gouv.qc.ca", "fpbavocats.com",
      "www.lecourriersud.com"}),

    ("Contenu généré par IA",
     """Des domaines qui produisent de la page à la chaîne. Faire citer par une
IA du texte écrit par une IA, pour en tirer une carte, c'est empiler trois
étages sans jamais toucher une source. À retirer sans hésiter.""",
     {"sci-ai.app", "lmnp.ai", "pre-etat-date.ai"}),

    ("Hors sujet ou pur marketing",
     """Rien à apprendre : une page boutique, une offre de formation, un forum,
une fiche de révision de lycéen, un article « 6 idées reçues ».""",
     {"www.studi.com", "sherpas.com", "executive-education.ut-capitole.fr",
      "boutique.lefebvre-dalloz.fr", "www.journaldelagence.com",
      "www.portail-autoentrepreneur.fr", "bpifrance-creation.fr",
      "www.alexia.fr", "commissaire-justice.fr", "www.eval.fr",
      "www.diacamma.org", "ucssarcelles.org"}),

    ("Page en anglais pour expatriés",
     """Vulgarisation pour acheteurs étrangers, sans valeur juridique, et
doublon de la version française déjà présente.""",
     {"en.parisrental.com", "www.my-french-house.com",
      "www.french-business-law.com", "hayot-expertise.fr", "alpassurances.fr"}),

    ("Éditeur de logiciel ou syndic concurrent",
     """La comptabilité de copropriété se lit dans l'arrêté du 14 mars 2005 et
le plan comptable, pas dans la documentation commerciale d'un éditeur. C'est
la grappe qui a produit la réponse indéfendable du 29/08 sur le fonds de
travaux (sourcée Hellio, Berenfus, Opéra Énergie, PDF Légifrance ignoré).""",
     {"www.vilogi.com", "www.lockimmo.com", "docs.copriciel.com",
      "logicielsyndic.fr", "www.coproplus.fr", "www.comptacop.fr",
      "www.copro-eco.fr", "www.seiitra.com", "berenfus-immobilier.fr",
      "www.meilleurecopro.com", "www.radar-immobilier.com",
      "www.syndic-one.com", "efisio.fr", "numbr.co", "matera.eu",
      "www.joya.fr", "www.mon-syndic-benevole.fr", "www.bailfacile.fr",
      "www.lebonbail.fr", "www.coproconseils.fr", "www.copro-assist.fr",
      "www.sos-syndic.info", "www.maxcompta.com", "finref.fr",
      "www.homeland.immo", "www.adbconseils.fr", "www.urccpaca.fr"}),

    ("Courtier, assureur ou promoteur",
     """Huit pages sur la garantie de parfait achèvement, six sur la
dommages-ouvrage, cinq sur la réception VEFA : la même chose répétée par des
vendeurs. L'article 1792-6 du Code civil et le PDF Légifrance couvrent tout,
en mieux.""",
     {"www.decennale.com", "www.demanderjustice.com", "www.groupama-pj.fr",
      "pro.april.fr", "www.aiac.fr", "assurance-coproprietes.fr",
      "www.coteneuf.com", "www.interconstruction.fr", "checkmy-house.fr",
      "www.clacourtage.com", "www.trouver-un-logement-neuf.com",
      "www.medicis-patrimoine.com", "www.ca-immobilier.fr",
      "e-immobilier.credit-agricole.fr", "www.agence-etoile.fr",
      "www.lelievre-immobilier.com", "www.pichet.fr", "www.cityandyou.com",
      "www.centaure-investissements.com", "www.cpim.fr",
      "www.investissement-locatif.com", "www.amarris-immo.fr",
      "www.dougs.fr", "www.legalstart.fr", "www.legalplace.fr",
      "www.l-expert-comptable.com", "www.alterea.fr", "opera-energie.com",
      "www.enerzine.com", "www.gazdaujourdhui.fr", "infodiag.fr",
      "www.mediabat.com", "www.obat.fr", "www.batappli.fr",
      "copropriete.hellio.com", "www.manda.fr", "solutions.bureauveritas.fr",
      "www.assoedc.com"}),
]

# Ce qu'on GARDE bien que le classement mecanique l'ait dit « commercial ».
GARDES = [
    ("Cabinets d'avocats",
     """De la doctrine, souvent la seule analyse disponible d'un arrêt récent.
C'est la meilleure part du lot « commercial », et elle reste citable à
condition de remonter à l'arrêt.""",
     {"www.544.fr", "www.grelieravocat.com", "www.bjavocat.com",
      "alpha-avocats.fr", "www.gossement-avocats.com",
      "www.seban-associes.avocat.fr", "www.wargny-katz.com",
      "www.alvarez-arlabosse.com", "www.daumas-wilson.fr",
      "www.avocat-cannes.com", "www.ebronquard-avocat.fr",
      "www.ldp-avocats.fr", "www.csj-avocats.fr", "goldwin-avocats.com",
      "www.jem-avocat.fr", "www.lla-avocats.fr", "www.hephaistos-avocats.fr",
      "www.victorisavocat.com", "www.agn-avocats.fr", "www.biot-avocat.com",
      "www.avocatayoun.fr", "www.galian-smabtp.fr", "www.smabtp.fr",
      "www.lemag-juridique.com", "www.lettredesreseaux.com",
      "www.gdroit.fr", "gdroit.fr", "app.livv.eu"}),

    ("Institutionnel, universitaire ou associatif mal classé",
     """Le nom de domaine ne dit pas tout : ces sources-là sont de la même
famille que l'ANIL et Service-Public.""",
     {"www.notaires.fr", "jbbullet.notaires.fr", "www.publicsenat.fr",
      "www.institutparisregion.fr", "cae-eco.fr", "cdn.paris.fr",
      "fr.wikipedia.org", "csgs.kcl.ac.uk", "perso.amse-aixmarseille.fr",
      "gbrisepierre.fr", "lirsa.cnam.fr", "cours.unjf.fr", "bib.kuleuven.be",
      "www.fnaim.fr", "www.associationqualisr.org"}),
]


def main():
    sources = ix.charge()
    par_domaine = defaultdict(list)
    for s in sources:
        if s["type"] == "web":
            par_domaine[s["domaine"]].append(s)

    attribue = set()
    lots = []
    for titre, texte, domaines in MOTIFS:
        items = []
        for d in sorted(domaines):
            if d in attribue:
                continue
            attribue.add(d)
            items.extend(par_domaine.get(d, []))
        lots.append((titre, texte, sorted(items, key=lambda s: s["titre"].lower())))

    total = sum(len(i) for _, _, i in lots) + len(DOUBLONS)
    commercial = [s for s in sources if s.get("nature") == "commercial"]

    md = [f"""# NOTEBOOKLM — ce qu'on retire du carnet

Établi le {DATE} à partir de [INDEX-NOTEBOOKLM.md](INDEX-NOTEBOOKLM.md).
Régénérer : `python3 app/tri_notebooklm.py`.

Le carnet est **plein : 300 sources sur 300**. Retirer n'est donc pas du
ménage, c'est **libérer des places pour du primaire**. Cette liste en dégage
**{total}**.

Le classement de l'index est mécanique, lu sur le nom de domaine. **Celui-ci
est un jugement**, posé source par source : il se relit et se conteste. Rien
n'est supprimé par un agent — la suppression se fait à la main dans le
panneau Sources, qui est trié alphabétiquement, d'où les titres exacts
ci-dessous.

## Le compte

| Lot | Sources |
|---|---|""",
          f"| Doublons | {len(DOUBLONS)} |"]
    for titre, _, items in lots:
        md.append(f"| {titre} | {len(items)} |")
    md.append(f"| **Total à retirer** | **{total}** |")
    md.append(f"""
Pour mémoire, le classement mécanique comptait {len(commercial)} sources
« commerciales ». On n'en retire pas {len(commercial)} : une bonne part est
de la doctrine d'avocats ou de l'institutionnel mal étiqueté (voir « Ce qu'on
garde » en fin de page).

---

## 1. Doublons ({len(DOUBLONS)})

Même titre déposé deux fois. Quatre places gagnées, zéro perte : à faire en
premier.
""")
    for t in DOUBLONS:
        md.append(f"- {t}")

    md.append("""
Réserve : l'interface annonce 300 sources, le relevé en identifie 298 en
comptant ces doublons. **Deux entrées restent non identifiées** — peut-être
deux doublons de plus. À vérifier à l'œil dans le panneau.
""")

    for n, (titre, texte, items) in enumerate(lots, start=2):
        md.append(f"\n## {n}. {titre} ({len(items)})\n")
        md.append(texte.strip() + "\n")
        for s in items:
            md.append(f"- {s['titre']} — *{s['domaine']}*")

    md.append("\n---\n\n## Ce qu'on garde\n")
    for titre, texte, domaines in GARDES:
        gardes = []
        for d in sorted(domaines):
            gardes.extend(par_domaine.get(d, []))
        md.append(f"\n### {titre} ({len(gardes)})\n")
        md.append(texte.strip() + "\n")
        for s in sorted(gardes, key=lambda x: x["titre"].lower()):
            md.append(f"- {s['titre']} — *{s['domaine']}*")

    md.append(f"""
---

## Et après : par quoi remplacer

{total} places libres ne valent que par ce qu'on y met. Le socle légal est
mieux fourni qu'il n'y paraît — loi de 1965, décret de 1967, arrêté du
14 mars 2005, loi ALUR, décret PPPT de 2022, décret syndic d'intérêt
collectif de 2025 sont bien là, en PDF Légifrance. Ce qui manque, vérifié
titre par titre sur le relevé :

| Manque | Ce qu'il y a à la place aujourd'hui |
|---|---|
| **Loi ELAN du 23 novembre 2018** (texte) | un article de cabinet d'avocats |
| **Loi Climat et Résilience du 22 août 2021** (texte) | rien — alors que c'est elle qui fixe les 2,5 % du PPT au fonds de travaux, chiffre que le carnet a sorti en le sourçant sur des blogs |
| **Loi Habitat dégradé du 9 avril 2024** (texte) | un article d'assureur |
| **Articles 1792 et suivants du Code civil** sur Légifrance | huit pages de courtiers et d'assureurs sur la garantie de parfait achèvement |
| **Jurisprudence de cassation** | une seule décision au carnet, un arrêt de cour d'appel |

La règle qui se dégage : **partout où le carnet n'a que du commentaire, il
cite le commentaire.** Remplacer les 116 retraits par ces textes-là suffit à
corriger le défaut observé au test du 29/08, sans rien changer au reste.
""")

    SORTIE.write_text("\n".join(md).rstrip() + "\n")
    print(f"{SORTIE.relative_to(RACINE)} écrit : {total} sources à retirer")


if __name__ == "__main__":
    main()

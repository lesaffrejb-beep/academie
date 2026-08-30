#!/usr/bin/env python3
"""
Fabrique l'index lisible du carnet NotebookLM a partir du dump brut du
panneau Sources.

  # 1. extraire (hors repo, cote skill)
  cd ~/.agents/skills/notebooklm && ./.venv/bin/python -u scripts/dump_sources.py \
      --notebook-url "https://notebook.google.com/notebook/<ID>" \
      --out ~/Documents/Code/erp/academie/notebooklm-sources-brut.json

  # 2. mettre en forme (ici)
  python3 app/index_notebooklm.py

Le classement par nature de source est MECANIQUE : il se lit sur le nom de
domaine, pas sur le contenu. Il trie ce qu'il faut aller verifier, il ne
tamponne rien.
"""

import json
import urllib.parse
from collections import Counter, defaultdict
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
BRUT = RACINE / "notebooklm-sources-brut.json"
SORTIE = RACINE / "INDEX-NOTEBOOKLM.md"
DATE = "29/08/2026"

OFFICIEL = {
    "legifrance.gouv.fr", "www.legifrance.gouv.fr",
    "service-public.gouv.fr", "www.service-public.gouv.fr",
    "entreprendre.service-public.gouv.fr", "www.service-public.fr",
    "anil.org", "www.anil.org", "anah.gouv.fr", "www.anah.gouv.fr",
    "ecologie.gouv.fr", "www.ecologie.gouv.fr",
    "cohesion-territoires.gouv.fr", "www.cohesion-territoires.gouv.fr",
    "economie.gouv.fr", "www.economie.gouv.fr",
    "impots.gouv.fr", "www.impots.gouv.fr", "bofip.impots.gouv.fr",
    "senat.fr", "www.senat.fr", "assemblee-nationale.fr", "www.assemblee-nationale.fr",
    "courdecassation.fr", "www.courdecassation.fr",
    "ccomptes.fr", "www.ccomptes.fr",
    "insee.fr", "www.insee.fr", "data.gouv.fr", "www.data.gouv.fr",
    "ademe.fr", "www.ademe.fr", "librairie.ademe.fr",
    "cstb.fr", "www.cstb.fr", "inpi.fr", "www.inpi.fr",
    "banquedesterritoires.fr", "www.banquedesterritoires.fr",
    "caissedesdepots.fr", "www.caissedesdepots.fr",
    "justice.fr", "www.justice.fr", "angers.fr", "www.angers.fr",
    "maine-et-loire.gouv.fr", "www.maine-et-loire.gouv.fr",
    "adil49.org", "www.adil49.org",
}

ASSOCIATIF = {
    "clcv.org", "www.clcv.org", "unpi.org", "www.unpi.org",
    "lacgl.fr", "www.lacgl.fr", "arc-copro.fr", "www.arc-copro.fr",
    "capeb.fr", "www.capeb.fr", "ffbatiment.fr", "www.ffbatiment.fr",
    "cairn.info", "www.cairn.info", "shs.cairn.info",
    "qualitel.org", "www.qualitel.org",
    "parisclimat.fr", "www.apc-paris.com",
    "conseilsyndicalassoc.free.fr", "ardsp.06480.free.fr",
}

def nature(domaine):
    """Nature presumee d'une source web, lue sur le seul nom de domaine.

    Le test « etranger » se fait sur la TERMINAISON, jamais sur un morceau :
    « .ca » cherche n'importe ou attrape capeb.fr, cairn.info et
    caissedesdepots.fr, qui sont tout ce qu'il y a de plus francais.
    """
    if not domaine:
        return "inconnu"
    d = domaine.lower()
    if d.endswith(".ca") or ".qc.ca" in d or "quebec" in d or "educaloi" in d:
        return "etranger"
    if d in OFFICIEL or d.endswith(".gouv.fr"):
        return "officiel"
    if d in ASSOCIATIF or d.endswith("cairn.info"):
        return "associatif"
    return "commercial"


LIBELLE_NATURE = {
    "officiel": "Officiel ou institutionnel",
    "associatif": "Associatif, consommateur ou revue",
    "commercial": "Éditeur, cabinet ou blog commercial",
    "etranger": "Droit étranger (Québec / Canada)",
    "inconnu": "Nature indéterminée",
}


def charge():
    sources = json.loads(BRUT.read_text())
    for s in sources:
        icone = s.get("icone") or ""
        if icone.startswith("web:"):
            s["type"] = "web"
            s["url"] = icone[4:]
            s["domaine"] = urllib.parse.urlparse(s["url"]).netloc
        else:
            s["type"] = {"drive_pdf": "pdf", "markdown": "markdown",
                         "video_youtube": "youtube"}.get(icone, icone or "inconnu")
            s["url"] = None
            s["domaine"] = None
        s["nature"] = nature(s["domaine"]) if s["type"] == "web" else None
    return sources


def tableau(lignes, entetes):
    out = ["| " + " | ".join(entetes) + " |",
           "|" + "|".join(["---"] * len(entetes)) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in lignes]
    return "\n".join(out)


def main():
    sources = charge()
    total = len(sources)

    par_cat = defaultdict(list)
    for s in sources:
        par_cat[s["categorie"] or "Hors catégorie"].append(s)

    types = Counter(s["type"] for s in sources)
    natures = Counter(s["nature"] for s in sources if s["type"] == "web")
    domaines = Counter(s["domaine"] for s in sources if s["type"] == "web")

    md = []
    md.append(f"""# INDEX-NOTEBOOKLM — ce que contient le carnet « Copropriété »

Relevé le {DATE} en lisant le panneau Sources du carnet, **sans passer par
le modèle** : les titres sortent tels que Google les affiche, aucune
reformulation, aucun quota consommé. Doctrine d'usage du carnet :
[CORPUS.md](CORPUS.md) § 4. Données brutes :
[notebooklm-sources-brut.json](notebooklm-sources-brut.json).

Régénérer :

```bash
cd ~/.agents/skills/notebooklm && ./.venv/bin/python -u scripts/dump_sources.py \\
  --notebook-url "https://notebook.google.com/notebook/567a033f-6a53-4321-a741-912f722403ea" \\
  --out ~/Documents/Code/erp/academie/notebooklm-sources-brut.json
python3 app/index_notebooklm.py
```

## Le compte

L'interface annonce **300 sources**, et le carnet affiche « a atteint la
limite de sources » : il est plein, une source de plus suppose d'en retirer
une. Le relevé trouve **{total} titres distincts**, donc **{300 - total} doublons**
(même titre déposé deux fois).

À noter : interrogé sur lui-même, le carnet a répondu « 278 sources ». Il se
trompe sur son propre contenu. C'est la première raison de ne jamais lui
faire compter ou inventorier quoi que ce soit : on lit le panneau, on ne
demande pas.

## Par nature de support

{tableau([(t, n) for t, n in types.most_common()], ["Support", "Nombre"])}

Les 17 fichiers markdown sont les « Essentiels métier » : de la
documentation interne d'employeur. **Le carnet est marqué « Public »** dans
son en-tête. À trancher par JB avant tout autre usage : du support interne
Sergic dans un carnet partageable par lien, ce n'est pas une question
d'Académie, c'est une question de confidentialité.

## Par nature de la source web ({sum(natures.values())} sources, {len(domaines)} domaines)

{tableau([(LIBELLE_NATURE[n], c) for n, c in natures.most_common()], ["Nature", "Nombre"])}

Classement **mécanique**, lu sur le nom de domaine et non sur le contenu :
il dit où regarder en premier, il ne tamponne rien.

Deux lectures qui comptent pour l'Académie :

1. **Le commercial domine.** C'est cohérent avec ce qu'on a observé au test
   du 29/08 : sur le fonds de travaux, la réponse était juste mais sourcée
   sur Hellio, Berenfus et Opéra Énergie alors que le PDF Légifrance de la
   loi de 1965 est dans le carnet. Un chiffre juste sourcé sur un blog reste
   un chiffre indéfendable : la carte se source sur le primaire.
2. **Il y a du droit québécois, et il est concentré sur un seul geste.**
   Quatre sources canadiennes (Éducaloi, quebec.ca, Lambert Avocats, l'Office
   québécois de la langue française) et **les quatre portent sur la mise en
   demeure**. Le vocabulaire est le nôtre, le droit ne l'est pas. Une
   question sur la mise en demeure d'un copropriétaire débiteur est donc
   exactement celle où le carnet peut répondre juste-en-apparence et faux en
   France : sur ce point, on ne l'interroge pas, on lit l'article 19-2 et le
   décret de 1967.

## Par catégorie
""")

    md.append(tableau(
        [(cat, len(items)) for cat, items in sorted(par_cat.items(), key=lambda kv: -len(kv[1]))],
        ["Catégorie du carnet", "Sources"]))

    md.append("""
« Miscellaneous » pèse les deux tiers : le rangement du carnet ne vaut pas
plan de travail. Les catégories utiles pour l'Académie restent à construire
sur l'arbre des domaines du BLUEPRINT §9, pas sur celui-ci.

---

## La liste

Ordre : catégorie du carnet, puis titre. `[officiel]`, `[associatif]`,
`[commercial]`, `[étranger]` valent pour les sources web uniquement.
""")

    marqueur = {"officiel": "officiel", "associatif": "associatif",
                "commercial": "commercial", "etranger": "**étranger**"}

    for cat, items in sorted(par_cat.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        md.append(f"\n### {cat} ({len(items)})\n")
        for s in sorted(items, key=lambda x: x["titre"].lower()):
            titre = s["titre"].replace("|", "\\|")
            if s["type"] == "web":
                # une URL a espaces casse le lien markdown
                lien = urllib.parse.quote(s["url"], safe=":/?#[]@!$&'()*+,;=%~")
                md.append(f"- [{titre}]({lien}) — {s['domaine']} [{marqueur[s['nature']]}]")
            elif s["type"] == "pdf":
                md.append(f"- {titre} — PDF déposé")
            elif s["type"] == "markdown":
                md.append(f"- {titre} — markdown interne")
            elif s["type"] == "youtube":
                md.append(f"- {titre} — vidéo YouTube")
            else:
                md.append(f"- {titre} — {s['type']}")

    SORTIE.write_text("\n".join(md).rstrip() + "\n")
    print(f"{SORTIE.relative_to(RACINE)} écrit : {total} sources, {len(par_cat)} catégories")


if __name__ == "__main__":
    main()

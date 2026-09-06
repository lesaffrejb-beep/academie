"""Candidat rédactionnel, hors banque servie. Aucun état usine modifié."""
import copy, json
from pathlib import Path
D=Path(__file__).parent
CID='satellite.pathologie.facade-ancienne-avant-devis'
PARENT='pathologie.facades.diagnostiquer-une-facade-avant-devis'
URL='https://data.geopf.fr/annexes/gpu/documents/PSMV_244900015/e4859efbaa6a6b73f60a338e11f14048/244900015_cahier_recommandations_20241016.pdf'
HASH='707940074f1388686398dd795457acbf3ab30d6bcd2ae2a65c3a88f3888b1fba'
def src(pages):
 return {'texte':f"Angers, Cahier de recommandations, copie locale édition 2023 scellée par l'usine, pages PDF {pages}. Lien public retrouvé ; identité binaire avec ce téléchargement non contrôlée. Recommandations, sans prescription juridique actuelle.",'url':URL+'#page='+str(pages).split('-')[0],'nature':'institution','parti':'Recommandations patrimoniales locales ; ne remplacent pas le règlement.','empreinte':HASH}
PROV={'auteur':'modele','outil':'Codex','modele':'GPT-6','genere_le':'2026-09-06','session':'objectif-lundi-20260906/graphe-facade','sources_retrouvees':1,'sources_concordantes':0,'sans_source':False}
cards=[]
def card(slug,typ,q,r,e,v,pages,**extra):
 c={'id':'facade-ancienne-'+slug,'chapitre':CID,'domaine':'pathologie','branche':'facades','type':typ,'niveau':4,'question':q,'reponse':r,'explication':e,'vigilance':v,'source':[src(pages)],'provenance':copy.deepcopy(PROV),'verifie':'2026-09-06','peremption':None,'statut':'brouillon','partage':'banque',**extra};cards.append(c)
def choices(*items):
 return [{'texte':t,'correct':ok,**({'pourquoi_faux':why} if not ok else {})} for t,ok,why in items]
card('materiau-inconnu','flash',
 "Dans un dossier fictif, une façade claire est décrite comme du tuffeau sans reconnaissance des matériaux : que peux-tu tenir pour établi ?",
 "Seul l'aspect clair rapporté est établi ; la nature tuffeau reste une hypothèse à vérifier. Le diagnostic doit reconnaître matériaux, dispositions constructives et transformations avant de définir l'intervention.",
 "Le cahier distingue pierre de taille et maçonnerie de moellons, puis demande une connaissance détaillée du support et de son histoire.",
 "Une ressemblance ne suffit pas à choisir un procédé de nettoyage.",'11')
card('traces-et-causes','qcm',
 "Cas fictif : des traces apparaissent sous des appuis et au pied du mur après pluie, sans autre examen ; quelle conclusion est défendable ?",
 "Les traces orientent l'examen des trajets de l'eau mais ne départagent pas encore ruissellement, rejaillissement et autres apports d'humidité. Il faut confronter leur localisation aux ouvrages et aux observations complémentaires.",
 "Le schéma du cahier représente plusieurs trajets de l'eau autour d'une façade. Une position de tache ne devient pas à elle seule la preuve d'une cause unique.",
 "La date d'observation après pluie ne démontre pas que la pluie explique tout.",'12',choix=choices(
 ('Des remontées capillaires expliquent nécessairement toutes les traces.',False,'Une trace basse ne suffit pas à établir cette origine, ni à expliquer celles sous les appuis.'),
 ('Plusieurs apports restent possibles ; examiner leurs trajets avant de conclure.',True,''),
 ('La pluie étant observée, les joints et les ouvrages de toiture sont hors sujet.',False,"Ces ouvrages participent précisément à l'orientation et à l'évacuation des eaux."),
 ("L'aspect des traces permet de choisir immédiatement la peinture qui convient.",False,"L'aspect ne renseigne ni complètement le support ni la cause de l'humidité.")))
card('parcours-eau','libre',
 "Cas fictif : un devis ne décrit que le parement ; quels ouvrages et relations demandes-tu d'examiner pour comprendre les traces autour d'une corniche, d'un appui, d'un larmier et du soubassement ?",
 "Demande un examen reliant couverture et évacuation des eaux, corniche, appuis, larmiers, joints et pied de façade aux traces localisées. Le rapport doit dire ce qui a été observé, ce qui reste inaccessible et quelles causes demeurent possibles.",
 "Le cahier présente la corniche comme protection, le larmier comme moyen d'écarter les eaux du parement, et les rejaillissements comme une voie d'altération au pied du mur. Ce sont des pistes d'examen, pas un diagnostic du cas.",
 "Une liste d'ouvrages sans relation avec les traces ne résout pas la cause.",'12-14',aide="Relie l'arrivée, le chemin et l'évacuation de l'eau aux zones observées.")
card('nettoyage-calcin','qcm',
 "Cas fictif : une proposition promet une pierre très claire après nettoyage, sans diagnostic ni essai sur place ; quel point doit conditionner l'avis ?",
 "L'adéquation du procédé au matériau, à son état et à son épiderme doit être établie avant de retenir la proposition. La clarté obtenue ne suffit pas à démontrer la conservation de la pierre.",
 "Le cahier explique le rôle protecteur du calcin et le risque d'altération par un nettoyage inadapté ; il indique l'intérêt d'échantillons sur place pour apprécier la méthode.",
 "Le module ne choisit ni abrasif, ni pression, ni produit de traitement.",'12-13',choix=choices(
 ("Choisir la proposition dont la photographie paraît la plus claire.",False,"L'apparence ne démontre pas que l'épiderme de la pierre est préservé."),
 ("Refuser définitivement tout nettoyage, quel que soit le diagnostic.",False,"Le cahier conditionne le procédé au support ; il ne conclut pas à une impossibilité générale."),
 ("Demander diagnostic du support et éléments permettant d'évaluer l'adéquation du procédé.",True,''),
 ("Retenir le procédé utilisé sur une pierre plus dure du voisinage.",False,"La méthode ne se transpose pas sans identification et examen de la pierre concernée.")))
card('enduit-contradictoire','role',
 "Cas fictif : un conseiller demande de retirer tous les enduits parce qu'un guide montre du tuffeau dégradé sous ciment ; comment réponds-tu sans minimiser le risque ni généraliser ?",
 "Le risque montré mérite un examen du support, du revêtement et de l'humidité ; il ne prouve pas que tout enduit sur toute maçonnerie soit inadapté. Je demande une reconnaissance et un avis motivé avant de définir les travaux.",
 "Le cahier distingue le parement en pierre de taille de maçonneries de moellons généralement enduites. La page consacrée aux revêtements inadaptés ne justifie donc pas une suppression indifférenciée.",
 "Ne remplace pas une généralisation favorable à l'enduit par une généralisation inverse.",'11-14',aide="Reconnais le risque décrit, puis nomme ce qu'il faut établir dans le cas présent.")
card('comparaison-offres','qcm',
 "Cas fictif : A promet une teinte uniforme et B prévoit un diagnostic sans annoncer de traitement définitif ; que peux-tu conclure sur ces offres ?",
 "Leurs prestations et leurs résultats attendus diffèrent : il faut préciser le besoin et rendre les périmètres comparables avant de choisir. La présence d'un diagnostic dans B ne prouve pas à elle seule sa qualité, mais l'uniformité annoncée par A ne démontre pas sa compatibilité avec le support.",
 "Le cahier subordonne l'intervention à la connaissance du matériau et de son état ; l'appréciation esthétique ne remplace pas cet examen.",
 "Un intitulé de prestation ne prouve pas qu'elle sera suffisamment réalisée.",'11-13',choix=choices(
 ("A est préférable puisque son résultat esthétique est plus précis.",False,"La précision esthétique laisse ouverte la question du matériau et des risques."),
 ("B est nécessairement complète parce que le mot diagnostic figure au devis.",False,"Le contenu, les limites et les compétences mobilisées doivent être explicités."),
 ("Les offres sont équivalentes puisqu'elles concernent la même façade.",False,"Leur objet et leurs investigations diffèrent, même si le bâtiment est le même."),
 ("Clarifier le besoin, les investigations et les exclusions avant la comparaison.",True,'')))
card('revision-avis','libre',
 "Cas fictif : le rapport confirme désormais le tuffeau mais laisse inaccessible une corniche et ne conclut pas sur l'origine des traces ; comment révises-tu ton avis initial ?",
 "La nature du matériau n'est plus une simple hypothèse dans le périmètre reconnu ; les causes et l'état de la corniche restent indéterminés. L'avis doit conserver ces limites et préciser quelle investigation professionnelle pourrait les lever avant de définir l'intervention.",
 "Le diagnostic détaillé demandé dans le cahier porte à la fois sur les matériaux et sur l'état global, avec recherche des causes. Une information nouvelle peut résoudre une question sans fermer le dossier.",
 "N'étends pas une reconnaissance locale à toutes les parties non examinées.",'11-14')
card('recommandation-reglement','role',
 "Un interlocuteur présente la fiche-conseil Angers comme la preuve d'une obligation opposable actuelle pour son projet : quelle distinction poses-tu ?",
 "Cette fiche expose des recommandations et précise qu'elle ne se substitue pas au règlement. Pour qualifier les prescriptions applicables au projet, il faut retrouver les pièces réglementaires et leur portée ; ce dossier ne fournit pas cette vérification juridique actuelle.",
 "La page de sommaire sépare expressément les fiches-conseil des prescriptions opposables du règlement du PSMV. Une recommandation technique ne devient pas une règle juridique par sa seule publication institutionnelle.",
 "Ne donne ni autorisation supposée, ni délai, ni procédure actuelle non vérifiée.",'2')
card('note-au-conseil','synthese',
 "Cas fictif nouveau : une façade présente un pied de mur taché, des moulures masquées et un revêtement intact en apparence ; le matériau reste inconnu, alors que le conseil veut valider un simple nettoyage : quel avis provisoire rédiges-tu ?",
 "L'aspect ne permet pas de qualifier le support ni d'écarter un problème sous le revêtement ; le nettoyage reste à définir après diagnostic. Demande reconnaissance des matériaux et de l'histoire de la façade, examen des trajets de l'eau et des ouvrages, puis une proposition motivée dont les limites et les conditions de révision sont explicites.",
 "Le cahier relie l'histoire du bâti, les matériaux, la gestion des eaux et les revêtements à l'analyse préalable. Le cas est inventé et aucune cause n'y est établie.",
 "L'avis organise les questions à résoudre, il n'est pas un ordre de travaux.",'11-14',attendus=["Séparer observations rapportées, hypothèses et inconnues.","Demander la reconnaissance des matériaux et des transformations.","Relier les traces aux eaux et aux ouvrages sans fixer une cause unique.","Exiger une appréciation du procédé au regard du support et de son état.","Conserver un argument favorable à l'entretien sans en déduire le traitement.","Nommer l'information susceptible de faire réviser l'avis."])
lesson="""Avant de comparer des devis pour une façade ancienne, tu dois savoir ce que la comparaison cherche à résoudre. Une couleur irrégulière, une pierre creusée et un revêtement qui masque les moulures ne posent pas nécessairement la même question. Ce dossier s'appuie sur le cahier de recommandations d'Angers, édition historique consultée localement. Ses exemples servent à apprendre un raisonnement préalable ; ils ne définissent ni les travaux d'un bâtiment réel ni ses obligations actuelles.

Commence par séparer les observations, les hypothèses et les inconnues. Dans un dossier fictif, « traces au pied du mur » décrit un constat rapporté. « Remontées capillaires » propose une explication. « Nature du support non reconnue » indique une limite. Passer directement du constat à un produit ferait disparaître les questions encore ouvertes. Une hypothèse devient utile quand tu précises quelle observation professionnelle pourrait la conforter ou la contredire.

Reconnais ensuite les matériaux et l'histoire de la façade. Le cahier distingue la pierre de taille, assemblée selon un appareil, des maçonneries de moellons généralement enduites. Il décrit le tuffeau comme une pierre calcaire poreuse et fragile. Une façade claire ne suffit pourtant pas à identifier ce matériau. Des archives, des transformations et un diagnostic sur place permettent de comprendre ce qui est conservé, recouvert ou remplacé. Ne transforme pas un exemple angevin en identification de toute façade ancienne.

Lis aussi la façade comme un ensemble d'ouvrages qui orientent l'eau. Le schéma du cahier relie couverture et évacuation, corniche, appui, larmier et soubassement. Un larmier vise à éloigner les eaux du parement ; des rejaillissements peuvent atteindre les parties basses. Cette lecture conduit à examiner les relations entre les traces, les joints et les ouvrages. Elle ne prouve pas que toute humidité vienne de la pluie. Demande au diagnostic de distinguer ce qui est observé, inaccessible et encore susceptible de plusieurs explications.

Le choix d'une intervention dépend de cette connaissance. Le cahier souligne qu'un nettoyage inadapté peut accélérer les dégradations et endommager l'épiderme protecteur du tuffeau, appelé calcin. Une pierre rendue plus claire n'est donc pas une preuve suffisante de conservation. Les éléments permettant d'apprécier l'adéquation d'une méthode, dont des échantillons sur place dans le cadre professionnel, doivent répondre à l'état réel du support. Tu n'as pas à déduire ici une pression, un produit ou une méthode de remplacement.

La même prudence vaut pour les revêtements. Le cahier montre des situations où un enduit inadapté retient l'humidité et où un aspect extérieur intact masque une dégradation du tuffeau. Ce risque donne une question à instruire, pas une raison de supprimer tous les enduits. La distinction initiale entre pierre de taille et moellons reste nécessaire. Il faut établir la nature du revêtement, celle du support et leur comportement, puis faire définir une intervention compatible.

Exemple fictif : A propose de retrouver une teinte uniforme ; B prévoit de reconnaître le support mais ne décrit pas les parties accessibles. Tu peux reconnaître l'intérêt d'un entretien sans approuver A sur son seul résultat esthétique. Tu peux demander le contenu du diagnostic B sans le considérer complet par son intitulé. Ton avis compare les objets, relève les exclusions et annonce ce qui permettrait ensuite de choisir. Si un rapport confirme le tuffeau mais laisse la corniche inaccessible, seule une partie de l'incertitude est levée.

Enfin, le cahier indique lui-même que ses fiches ne remplacent pas le règlement. Le dossier ne tranche aucune prescription opposable actuelle. Demain matin, tu sauras rédiger une demande de diagnostic distinguant matériaux, histoire, eaux, revêtements et limites d'accès, puis un avis conditionnel que tu pourras réviser sur pièces. Cette production prépare le dialogue avec les professionnels ; elle ne certifie pas une compétence de diagnostic."""
chapter={'id':CID,'titre':'Façade ancienne : instruire avant de choisir un devis','domaine':'pathologie','branche':'facades','niveau':4,'prerequis':[],'ponts':[PARENT],'satellite':True,'rattachement_propose':PARENT,'objectifs':["Séparer constat, hypothèse causale et matériau encore inconnu.","Définir les questions d'un diagnostic reliant support, revêtement et gestion des eaux.","Comparer des propositions sur leur objet et réviser un avis lorsque les preuves évoluent."],'amorce':{'question':"Cas fictif : une façade claire porte des traces sous les appuis et un revêtement sans fissure visible ; un devis propose un nettoyage uniforme, sans reconnaissance du matériau ni examen des ouvrages d'eau : quel avis provisoire donnes-tu au conseil ?",'aide':"Écris ce qui est vu, supposé et manquant avant de choisir une intervention.",'reponse_attendue':"Le dossier ne permet pas encore de définir le nettoyage. La couleur et l'aspect du revêtement ne qualifient ni le matériau ni son état ; je demande un diagnostic reliant support, transformations et trajets de l'eau, avec les limites d'accès et les pièces qui pourraient changer l'avis."},'lecon':lesson,'synthese':{'consigne':"Cas nouveau fictif : un rapport identifie localement du tuffeau, propose une explication aux traces et laisse les ouvrages hauts non examinés ; une offre promet de rendre les moulures lisibles mais ne précise pas le procédé : rédige une note au conseil distinguant acquis, hypothèses, inconnues, demande complémentaire et condition d'évolution de ton avis.",'attendus':["Limiter l'identification du tuffeau aux zones effectivement reconnues.","Conserver l'explication des traces comme hypothèse tant qu'elle n'est pas établie.","Demander l'examen des ouvrages hauts et des trajets de l'eau pertinents.","Demander comment le procédé sera apprécié au regard du support et de son état.","Reconnaître l'intérêt patrimonial sans le confondre avec une preuve de compatibilité.","Formuler une condition précise de révision de l'avis.","Ne déduire aucune prescription juridique actuelle du cahier de recommandations."]},'sources':[src('2'),src('11-14')],'provenance':copy.deepcopy(PROV),'statut':'brouillon','partage':'banque','verifie':'2026-09-06','version':1,'cartes':cards}
(D/'facade-ancienne-avant-devis.json').write_text(json.dumps(chapter,ensure_ascii=False,indent=2)+'\n')
print(len(lesson),len(lesson.split()),len(cards),sorted(set(c['type'] for c in cards)))

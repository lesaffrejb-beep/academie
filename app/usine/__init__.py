"""L'usine : un document réel devient un pivot Markdown par page, pas à pas.

Le script fait ce qu'une machine fait bien (extraire, découper, rendre,
compter, vérifier) et impose au modèle ce qu'il fait mal quand il est
petit ou fatigué : avancer par unités courtes, écrire sur disque après
chaque unité, ne rien inventer. L'état est revérifiable : chaque
`suivant` rejoue les contrôles des unités déjà validées, donc modifier
l'état à la main ne sert à rien (decisions/0026, decisions/0027).
"""

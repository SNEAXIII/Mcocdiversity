class Joueur:
    def __init__(self, group):
        self.persos = []
        self.defs = []
        self.group = group

    def __add__(self, personnage):
        self.persos.append(personnage)


class Personnage:
    def __init__(self, nom: str):
        self.nom = nom
        self.possede= [] # rank,sig,owners
        self.


class Possede:
    def __init__(self):


class Group:
    def __init__(self,id):
        self.id = id


class Joueur:
    def __init__(self, group):
        self.persos = []
        self.defs = []
        self.group = group

    def addListe(self, personnage):
        self.persos.append(personnage)





class Personnage:
    def __init__(self, nom: str):
        self.nom = nom
        self.possede= [] # rank,sig,owners
        self.dispo = True


class Possede:
    def __init__(self):

class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []
        self.p_score = 0

    def getScore(self):
        return int(self.p_score / 15)

    def dump(self):
        stringReturn = f"\nJoueur : {self.name}\nPuissance théorique du joueur: {self.getScore()}\n"
        for _def in self.defs:
            stringReturn += f"  → {_def}\n"
        return stringReturn

    def __str__(self):
        if self.p_score ==0:
            return f"{self.name}\nVide\n\n"
        stringReturn = f"{self.name}\n{self.getScore()}\n"
        for _def in self.defs:
            stringReturn += f"{_def}\n"
        return f"{stringReturn}\n"

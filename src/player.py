class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []
        self.pScore = 0

    def getScore(self):
        return int(self.pScore / 20)

    def dump(self):
        stringReturn = f"\nJoueur : {self.name}\nPuissance théorique du joueur: {self.getScore()}\n"
        for _def in self.defs:
            stringReturn += f"  → {_def}\n"
        return stringReturn + "\n"

    def __str__(self):
        stringReturn = f"{self.name}\n{self.getScore()}\n"
        for _def in self.defs:
            stringReturn += f"{_def}\n"
        return f"{stringReturn}\n"

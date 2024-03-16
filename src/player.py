class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []
        self.p_score = 0

    def get_score(self):
        return int(self.p_score / 15)

    def dump(self):
        string_return = f"\nJoueur : {self.name}\nPuissance théorique du joueur: {self.get_score()}\n"
        for _def in self.defs:
            string_return += f"  → {_def}\n"
        return string_return

    def __str__(self):
        if self.p_score ==0:
            return f"{self.name}\nVide\n\n"
        string_return = f"{self.name}\n{self.get_score()}\n"
        for _def in self.defs:
            string_return += f"{_def}\n"
        return f"{string_return}\n"

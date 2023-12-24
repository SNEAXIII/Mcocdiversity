from random import choice

LINE = "=" * 35 + "\n"


class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []
        self.pScore = 0

    def getScore(self):
        return int(self.pScore / 20)

    def dump(self):
        stringReturn = f"{LINE}Joueur : {self.name}\nPuissance théorique du joueur: {self.getScore()}\n"
        for _def in self.defs:
            stringReturn += f"  → {_def}\n"
        return stringReturn + LINE


class Group:
    def __init__(self):
        self.gScore = 0
        self.allDefs = {}
        self.selectedDefs = set()
        self.unselectedDefs = set()
        self.allPlayer = {}
        self.allRanks = \
            {
                "7r3": 326,
                "6r6": 265,
                "7r2": 264,
                "6r5": 217,
                "7r1": 210,
                "6r4": 188,
                "6r3": 164,
                "6r2": 138,
                "6r1": 100
            }

        self.rangeRank = max(self.allRanks.values()), min(self.allRanks.values()) - 1, -1

    def getScore(self):
        return int(self.gScore / 50)

    def dump(self):
        stringReturn = ""
        for defName in self.allDefs:
            stringReturn += f"{defName}\n"
            for intRank in self.allDefs[defName]:
                stringReturn += f"{self.convertRankIntToStr(intRank)}-->{self.allDefs[defName][intRank]}\n"
            stringReturn += "\n"
        return stringReturn

    def __str__(self):
        stringReturn = f"Puissance théorique du groupe : {self.getScore()}\n"
        for player in self.allPlayer.values():
            stringReturn += player.dump()
        return stringReturn + (f"Les défenseurs choisis sont : {self.strAllDefSelected()}\n"
                               f"Les défenseurs non choisis sont : {self.strAllDefUnSelected()}\n")

    def strAllDefSelected(self):
        sortedSelectedDef = sorted(self.selectedDefs, key=lambda x: (-x[1], x[0]))
        sortedSelectedDefFormat = [f"{_def[0]} {self.convertRankIntToStr(_def[1])}" for _def in sortedSelectedDef]

        return ", ".join(sortedSelectedDefFormat)

    def strAllDefUnSelected(self):
        return ", ".join(sorted(list(self.unselectedDefs)))

    def addPlayer(self, player: Player):
        self.allPlayer[player.name] = player

    def addNewDef(self, owner: str, defName: str, rank: str, strSig: str):
        sig = int(strSig)
        if defName not in self.allDefs:
            self.allDefs[defName] = {}
            for idRank in range(*self.rangeRank):
                self.allDefs[defName][idRank] = {}
        defNameDefRank = self.allDefs[defName][self.convertRankStrToInt(rank)]
        if not sig in defNameDefRank:
            defNameDefRank[sig] = set()
        defNameDefRank[sig].add(owner)

    def convertRankStrToInt(self, rank: str):
        if not rank in self.allRanks:
            raise Exception(f"Le rang est mal saisi : {rank}")
        return self.allRanks[rank]

    def convertRankIntToStr(self, value: int):
        for strRank, intRank in self.allRanks.items():
            if value == intRank:
                return strRank
        raise Exception(f"Aucun rang correspond trouvée pour la valeur : {value}")

    def findThePlayerForRankForDef(self, defName: str, rank: int):
        if defName not in self.allDefs:
            return False
        dictDefRank = self.allDefs[defName][rank]
        if len(dictDefRank):
            maxSig = max(dictDefRank.keys())
            return choice(list(dictDefRank[maxSig]))
        return False

    @staticmethod
    def isDefRankEmpty(dictionary: dict):
        return all(not bool(s) for s in dictionary.values())

    def findTheBestDefs(self):
        for rank in self.allRanks.values():
            for defName in list(self.allDefs):
                playerOrFalseOrDoublon = self.findThePlayerForRankForDef(defName, rank)
                if playerOrFalseOrDoublon:
                    self.addDefInPlayer(playerOrFalseOrDoublon, defName, rank)

    def addDefInPlayer(self, player: str, defName: str, rank: int):
        self.allPlayer[player].defs.append(f"{defName} {self.convertRankIntToStr(rank)}")
        if not defName in self.selectedDefs:
            self.selectedDefs.add((defName,rank))
        else:
            raise Exception(f"Le défenseur {defName} à été enregistré 2 fois")
        if len(self.allPlayer[player].defs) == 5:
            selectedDef = None
        else:
            selectedDef = defName
        self.deleteOneDefDict(defName)
        self.deleteOnePlayerInDefsDict(player, selectedDef)
        self.gScore += rank
        self.allPlayer[player].pScore += rank

    def deleteOneDefDict(self, defName: str):
        del self.allDefs[defName]

    def deleteOnePlayerInDefsDict(self, player: str, defToUpdate: str = None):
        for _def, ranks in list(self.allDefs.items()):
            if defToUpdate and defToUpdate != _def:
                continue
            for rank, allSig in list(ranks.items()):
                for sig, names in list(allSig.items()):
                    if player in names:
                        names.discard(player)
                        if not names:
                            del allSig[sig]
                        if self.isDefRankEmpty(allSig):
                            self.unselectedDefs.add(_def)
                            self.deleteOneDefDict(_def)

    def isEmptyDef(self):
        return not bool(self.allDefs)

    def isFullOfDef(self):
        return len(self.selectedDefs) == 50


class Groups:
    def __init__(self):
        self.groups = {1: Group(), 2: Group(), 3: Group()}

    def addPlayerToAGroup(self, idGroup: int, playerName: str):
        if len(self.groups[idGroup].allPlayer) != 10:
            self.groups[idGroup].addPlayer(Player(playerName))
            return
        raise Exception(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {idGroup}!!!")

    def addDefToOneGroup(self, idGroup: int, playerName: str, defName: str, rank: str, sig: int):
        self.groups[idGroup].addNewDef(playerName, defName.capitalize(), rank, sig)

    def dump(self):
        for id, group in self.groups.items():
            print(f"Groupe numéro {id}\n{group}")


groups = Groups()

with open("data", encoding="utf-8") as f:
    data = [line.replace("\n", "") for line in f.readlines()]
playerName = None
group = None
for line in data:
    if line == "#":
        playerName = None
        group = None
    elif line.startswith("+"):
        if playerName is not None:
            raise Exception("Le joueur ne peux être saisi 2 fois")
        playerName = line.lstrip("+")
    elif line.startswith("-"):
        if playerName is None:
            raise Exception("Le joueur doit être saisi avant son groupe")
        elif group is not None:
            raise Exception("Le groupe ne peux être saisi 2 fois")
        group = int(line.lstrip("-"))
        groups.addPlayerToAGroup(group, playerName)
    else:
        # todo erreur potancielle ici --> defName,rank,sig = line.split(" ")
        groups.addDefToOneGroup(group, playerName, *line.split(" "))
group1 = groups.groups[1]
group1.findTheBestDefs()
groups.dump()
print(group1.strAllDefUnSelected())
print(group1.getScore())
a = "test"

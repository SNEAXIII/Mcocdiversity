from random import choice

from src.player import Player


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

        self.rangeRank = self.allRanks.values()

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

    def addNewDef(self, owner: str, defName: str, rank: str, sig: int):
        if defName not in self.allDefs:
            if any(tupleDef[0] == defName for tupleDef in self.selectedDefs):
                return
            self.allDefs[defName] = {}
            for idRank in self.rangeRank:
                self.allDefs[defName][idRank] = {}
        defNameDefRank = self.allDefs[defName][self.convertRankStrToInt(rank)]
        if not sig in defNameDefRank:
            defNameDefRank[sig] = set()
        defNameDefRank[sig].add(owner)

    def convertRankStrToInt(self, rank: str):
        lowerRank = rank.lower()
        if not lowerRank in self.allRanks:
            raise Exception(f"Le rang est mal saisi : {rank}")
        return self.allRanks[lowerRank]

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
            # todo print(debug)
            if len(dictDefRank[maxSig]) > 1:
                listePlayer = dictDefRank[maxSig]
                printListePlayer = ", ".join(listePlayer)
                lenListePlayer = len(listePlayer)
                print(f"{lenListePlayer} players --> {defName} --> {self.convertRankIntToStr(rank)} --> {printListePlayer}")
            return choice(list(dictDefRank[maxSig]))
        return False

    @staticmethod
    def isDefRankEmpty(dictionary: dict):
        return all(not bool(s) for s in dictionary.values())

    def findTheBestDefs(self):
        for rank in self.allRanks.values():
            for defName in list(self.allDefs):
                playerOrFalse = self.findThePlayerForRankForDef(defName, rank)
                if playerOrFalse:
                    self.addDefInPlayer(playerOrFalse, defName, rank)

    def addDefInPlayer(self, player: str, defName: str, rank: int):
        if not any(tupleDef[0] == defName for tupleDef in self.selectedDefs):
            self.selectedDefs.add((defName, rank))
        else:
            raise Exception(f"Le défenseur {defName} à été enregistré 2 fois")

        if len(self.allPlayer[player].defs) == 4:
            selectedDef = None
        else:
            selectedDef = defName
        self.allPlayer[player].defs.append(f"{defName} {self.convertRankIntToStr(rank)}")
        self.gScore += rank
        self.allPlayer[player].pScore += rank
        self.deleteOneDefDict(defName)
        self.deleteOnePlayerInDefsDict(player, selectedDef)

    def deleteOneDefDict(self, defName: str):
        if defName in self.allDefs:
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

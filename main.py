class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []


class Group:
    def __init__(self):
        self.allDefs = {}
        self.selectDefs = {}
        self.allPlayer = {}
        self.allRanks = \
            {
                "7r3": 8,
                "7r2": 7,
                "7r1": 6,
                "6r6": 7,
                "6r5": 5,
                "6r4": 4,
                "6r3": 3,
                "6r2": 2,
                "6r1": 1
            }
        self.rangeRank = max(self.allRanks.values()), min(self.allRanks.values()) - 1, -1

    def __str__(self):
        stringReturn = ""
        for defName in self.allDefs:
            stringReturn += defName + "\n"
            for intRank in self.allDefs[defName]:
                stringReturn += f"{self.convertRankIntToStr(intRank)}-->{self.allDefs[defName][intRank]}" + "\n"
            stringReturn += "\n"
        return stringReturn

    def addPlayer(self, player: Player):
        self.allPlayer[player.name] = player

    def addNewDef(self, owner: str, defName: str, rank: str, sig: int):
        if defName not in self.allDefs:
            self.allDefs[defName] = {}
            for x in range(*self.rangeRank):
                self.allDefs[defName][x] = {}
        self.allDefs[defName][self.convertRankStrToInt(rank)][owner] = sig

    def convertRankStrToInt(self, rank: str):
        if not rank in self.allRanks:
            raise Exception(f"Le rang est mal saisi : {rank}")
        return self.allRanks[rank]

    def convertRankIntToStr(self, value: int):
        for strRank, intRank in self.allRanks.items():
            if value == intRank:
                return strRank
        raise Exception(f"Aucun rang correspond trouvée pour la valeur : {value}")

    def countTheRankForDef(self, defName: str, rank: int):
        dictDefRank = self.allDefs[defName][rank]
        if len(dictDefRank):
            if list(dictDefRank.values()).count(max(dictDefRank.values())) == 1:
                return 1
            else:
                print(f"il y a plusieurs candidats pour {defName} au rang {rank}")
                return 0
        else:
            return 0

    def findThePlayerForRankForDef(self, defName: str, rank: int):
        print(len(self.allDefs[defName][rank]))

    def findTheBestDefs(self, force: bool = False):
        # implétementer le force
        for rank in self.allRanks.values():
            toDelete = []
            # todo mettre une while tant qu'il y a des persos a supprimer
            for defName in self.allDefs:
                count = self.countTheRankForDef(defName, rank)
                if count == 1:
                    if self.addDefInPlayer():
                        toDelete.append()
                    else:
                        # todo verifier si c'est valide
                        continue
                    # todo décrementer un indice si ya rien a suppr
                print(defName, rank)

            # todo addmultidelete here
    def addDefInPlayer
    # todo ajouter un def a un player si il en pas pas 5

    def deleteADefsDict(self, defName: str):
        del self.allDefs[defName]

    def deleteMultiDefsDict(self, listDefName: list):
        for defName in listDefName:
            self.deleteADefsDict(defName)

    def deleteAPlayerInDefsDict(self, player: str):
        for _def in self.allDefs:
            for rank in self.allDefs[_def]:
                try:
                    del self.allDefs[_def][rank][player]
                except KeyError:
                    pass

    # todo lors de la suppression d'un player dans les defenseurs, vérifier si il en reste un et l'ajouter a ses defs
    # todo verifier qu'il y a un seul et unique def par groupe


class Groups:
    def __init__(self):
        self.groups = {1: Group(), 2: Group(), 3: Group()}

    def addPlayerToAGroup(self, idGroup: int, playerName: str):
        if len(self.groups[idGroup].allPlayer) != 10:
            self.groups[idGroup].addPlayer(Player(playerName))
            return
        raise Exception(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {idGroup}!!!")

    def addDefToAGroup(self, idGroup: int, playerName: str, defName: str, rank: str, sig: int):
        self.groups[idGroup].addNewDef(playerName, defName.capitalize(), rank, sig)

    def dump(self):
        for id, group in self.groups.items():
            print(f"Groupe numéro {id}\n{group}")


groups = Groups()

# groups.addPlayerToAGroup(1, "Mrbal'")
# groups.addPlayerToAGroup(1, "Legacy'")
# groups.addDefToAGroup(1,"Mrbal'","Shuri","7r3",0)
# groups.addDefToAGroup(1,"Mrbal'","Absman","6r6",200)
# groups.addDefToAGroup(1,"Legacy'","Shuri","7r3",0)

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
        print(playerName, group)
        groups.addPlayerToAGroup(group, playerName)
    else:
        # todo erreur potancielle ici
        # defName,rank,sig = line.split(" ")
        groups.addDefToAGroup(group, playerName, *line.split(" "))

# groups.groups[1].countTheRankForDef("Shuri", 8)
# groups.groups[1].deleteAPlayerInDefsDict("LEGACY LEGION")
# groups.groups[1].deleteAPlayerInDefsDict("Mrbal'")

# groups.groups[1].findTheBestDefs()

groups.dump()
print(groups.groups[1].countTheRankForDef("Absman",6))
a = "test"
